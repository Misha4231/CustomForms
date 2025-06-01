import graphene
import datetime
from graphql import GraphQLError
from django.db.models import Max, F
from django.db import transaction

from .models import Form, Section, Content, Question, QuestionOption, Answer, Submition
from .types import *
from .decorstors import form_owner, form_owner_section_id
from users.decorators import login_required

class FormCreateMutation(graphene.Mutation):
    class Arguments:
        title = graphene.String(required=True)
        description = graphene.String(required=False)
    
    form = graphene.Field(FormType)
    
    @classmethod
    def mutate(cls, root, info, title, description = ''):
        if not info.context.user.is_authenticated:
            raise GraphQLError("not authenticated")
        
        form = Form(title=title, description=description, owner=info.context.user)
        form.save()
        return FormCreateMutation(form=form)
        
class FormUpdateMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        title = graphene.String()
        description = graphene.String()
    
    form = graphene.Field(FormType)
    
    @classmethod
    def mutate(cls, root, info, id, title=None, description=None):
        form = Form.objects.get(pk=id)
        if title != None: # can be empty string
            form.title = title
        if description != None:
            form.description = description
        form.save()
        
        return FormUpdateMutation(form=form)
        
class SectionCreateMutation(graphene.Mutation):
    class Arguments:
        form_id = graphene.ID()
        type = graphene.String()
        order = graphene.Int()

    section = graphene.Field(SectionType)

    @classmethod
    @form_owner
    def mutate(cls, root, info, form, type = 'question', order = 0):
        sections = Section.objects.filter(form=form)

        max_order = sections.aggregate(Max('order'))['order__max'] or 0 # get the maximum order value from sections
        if order > max_order + 1: # if order argument is grater then the maximum possible order
            order = max_order + 1
    
        # increment order of sections at or after the desired insert position
        sections.filter(order__gte=order).update(order=F('order') + 1)

        # create new section
        section = Section.objects.create(
            title='',
            form=form,
            type='question' if type == 'question' else 'content',
            order=order
        )

        if type == 'question':
            Question.objects.create(section=section, answer_type='short')
        else:
            Content.objects.create(section=section, type=type)

        return SectionCreateMutation(section)

class SectionRemoveMutation(graphene.Mutation):
    class Arguments:
        section_id = graphene.ID()

    ok = graphene.Boolean()

    @classmethod
    @form_owner_section_id
    def mutate(cls, root, info, form: Form, section: Section):
        Section.objects.filter(form=form, order__gt=section.order).update(order=F('order') - 1)

        section.delete()
        return SectionRemoveMutation(True)
        
class SectionUpdateMutation(graphene.Mutation):
    class Arguments:
        section_id = graphene.ID(required=True)
        title = graphene.String()
        content = ContentInputType()
        question = QuestionInputType()

    section = graphene.Field(SectionType)

    @classmethod
    @form_owner_section_id
    def mutate(cls, root, info, form: Form, section: Section, title=None, content=None, question=None):
        if title:
            section.title = title
            section.save()

        if section.type == 'content' and content:
            content_obj = Content.objects.get(section=section)
            
            content_obj.type = content.type
            content_obj.text = content.text
            
            # if media is not attached, leave the same
            content_obj.image = content.image or content_obj.image
            content_obj.video = content.video or content_obj.video

            content_obj.save()
        elif section.type == 'question' and question:
            question_obj = Question.objects.get(section=section)

            question_obj.answer_type = question.answer_type
            question_obj.is_required = question.is_required or False
            question_obj.min_range = question.min_range
            question_obj.max_range = question.max_range
            question_obj.save()

            if question.options:
                QuestionOption.objects.filter(question=question_obj).delete()
                for option_input in question.options:
                    QuestionOption.objects.create(question = question_obj, text=option_input.text)
            else:
                QuestionOption.objects.filter(question=question_obj).delete()

        return SectionUpdateMutation(section)

class SubmitAnswerMutation(graphene.Mutation):
    class Arguments:
        form_id = graphene.ID()
        answers = graphene.List(AnswerInputType)

    submission = graphene.Field(SubmitionType)

    @classmethod
    @login_required
    def mutate(cls, root, info, form_id, answers):
        saved_answers = []

        form = Form.objects.get(pk=form_id)
        submission = Submition.objects.create(
                user=info.context.user,
                form=form,
                submitted_at=datetime.datetime.now()
        )
        try:
            with transaction.atomic():
                for answer in answers:
                    section = Section.objects.select_related('form').get(pk=answer.id)
                    question = Question.objects.get(section=section)
                    
                    new_answer = Answer()
                    new_answer.question = question
                    new_answer.submition = submission
                    
                    type = question.answer_type.lower()
                    if type == 'short':
                        new_answer.short_text = answer.text
                    elif type == 'long':
                        new_answer.long_text = answer.text
                    elif type == 'checkbox':
                        new_answer.save()  # Save first to allow M2M assignment
                        selected_options = [QuestionOption.objects.get(pk=opt_id) for opt_id in answer.options]
                        new_answer.selected_options.set(selected_options)
                    elif type == 'radio':
                        new_answer.save()  # Save first to allow M2M assignment
                        selected_option = [QuestionOption.objects.get(pk=answer.option)]
                        new_answer.selected_options.set(selected_option)
                    elif type == 'range':
                        new_answer.range_value = answer.rangeVal
                    else:
                        new_answer.date_value = answer.date

                    new_answer.save()
                    saved_answers.append(new_answer)

                submission.save()

        except Section.DoesNotExist:
            raise GraphQLError("Section does not exist")
        except Question.DoesNotExist:
            raise GraphQLError("Question does not exist")
        except QuestionOption.DoesNotExist:
            raise GraphQLError("One or more selected options do not exist")
        except Exception as e:
            raise GraphQLError(f"Unexpected error: {str(e)}")

        return SubmitAnswerMutation(submission=submission)


class Query(graphene.ObjectType):
    all_user_forms = graphene.List(FormType, userId=graphene.Int(required=True))
    form = graphene.Field(FormType, id=graphene.Int(required=True))
    sections_by_form = graphene.List(SectionType, form_id=graphene.ID(required=True))
    section_options = graphene.List(QuestionOptionType, section_id=graphene.ID(required=True))
    get_submitions = graphene.List(SubmitionType, form_id=graphene.ID(required=True))
    answers = graphene.List(AnswerType, submission_id=graphene.ID(required=True))

    def resolve_all_user_forms(root, info, userId):
        return Form.objects.filter(owner__id=userId).order_by('-pk')

    def resolve_form(root, info, id):
        return Form.objects.get(pk=id)

    def resolve_sections_by_form(root, info, form_id):
        return Section.objects.filter(form__id=form_id).order_by('order')
    
    def resolve_section_options(root, info, section_id):
        return QuestionOption.objects.select_related('question__section').filter(question__section__id=section_id)
    
    def resolve_get_submitions(root, info, form_id):
        return Submition.objects.filter(form__id = form_id).order_by('submitted_at')
    
    def resolve_answers(root, info, submission_id):
        return Answer.objects.filter(submition__id = submission_id)

class Mutation(graphene.ObjectType):
    create_form = FormCreateMutation.Field()
    update_form = FormUpdateMutation.Field()
    add_section = SectionCreateMutation.Field()
    remove_section = SectionRemoveMutation.Field()
    update_section = SectionUpdateMutation.Field()
    submit_answer = SubmitAnswerMutation.Field()