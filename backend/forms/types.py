from graphene_django import DjangoObjectType
import graphene
from graphene_file_upload.scalars import Upload

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
        
        return Question.objects.filter(section=self).first()

class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = "__all__"


class QuestionOptionInputType(graphene.InputObjectType):
    id = graphene.ID()
    text = graphene.String(required = True)

class QuestionInputType(graphene.InputObjectType):
    id = graphene.ID()
    answer_type = graphene.String(required = True)
    is_required = graphene.Boolean()
    min_range = graphene.Int()
    max_range = graphene.Int()
    options = graphene.List(QuestionOptionInputType)

class ContentInputType(graphene.InputObjectType):
    id = graphene.ID()
    text = graphene.String()
    type = graphene.String(required = True)
    text = graphene.String()
    image = Upload()
    video = Upload()