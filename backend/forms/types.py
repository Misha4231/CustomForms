from graphene_django import DjangoObjectType
import graphene

from .models import Form, Section, Content, Question, QuestionOption, Answer


class FormType(DjangoObjectType):
    class Meta:
        model = Form
        fields = "__all__"

class SectionType(DjangoObjectType):
    class Meta:
        model = Section
        fields = "__all__"

class ContentType(DjangoObjectType):
    class Meta:
        model = Content
        fields = "__all__"

class QuestionOptionType(DjangoObjectType):
    class Meta:
        model = QuestionOption
        fields = "__all__"

class QuestionType(DjangoObjectType):
    options = graphene.List(QuestionOptionType)

    class Meta:
        model = Question
        fields = "__all__"

    def resolve_options(self, info):
        return self.options.all()
        
class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = "__all__"