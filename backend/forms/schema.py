import graphene
from graphene_django import DjangoObjectType
from .models import Form, Section, Content, Question, QuestionOption, Answer



schema = None