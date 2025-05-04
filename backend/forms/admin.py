from django.contrib import admin
from .models import Form, Section, Content, Question, QuestionOption, Answer

admin.site.register(Form)
admin.site.register(Section)
admin.site.register(Content)
admin.site.register(Question)
admin.site.register(QuestionOption)
admin.site.register(Answer)
