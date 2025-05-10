from graphene_django import DjangoObjectType
import graphene

from .models import Form, Section, Content, Question, QuestionOption, Answer


class FormType(DjangoObjectType):
    class Meta:
        model = Form
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
        
class SectionItemType(graphene.Union):
    class Meta:
        types = (ContentType, QuestionType)
    
    @classmethod
    def resolve_type(cls, instance, info):
        if isinstance(instance, Content):
            return ContentType
        if isinstance(instance, Question):
            return QuestionType
        
        return None

class SectionType(DjangoObjectType):
    item = graphene.Field(SectionItemType)

    class Meta:
        model = Section
        fields = "__all__"

    def resolve_item(self, info):
        content = Content.objects.filter(section=self).first()
        if content:
            return content
        
        return Question.objects.filter(section=self).filter()

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = "__all__"

'''
query section($form_id: ID!) {
  sectionsByForm(formId: $form_id){
    title
    item {
      __typename
      ... on ContentType {
        text
      }
    }
  }
}
'''