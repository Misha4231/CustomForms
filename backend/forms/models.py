from django.db import models
from users.models import User

# Create your models here.
class Form(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(max_length=500)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.title

# Each form can have multiple sections. Each section can have multiple contents and questions
class Section(models.Model):
    title = models.CharField(max_length=100)
    form = models.ForeignKey(Form, on_delete=models.CASCADE)
    type = models.CharField(choices=[('question', 'Question'), ('content', 'Content')])

    def __str__(self):
        return f"{self.form.title}: {self.title}"
    
class Content(models.Model):
    CONTENT_TYPES = [
        ('text', 'Text'),
        ('image', 'Image'),
        ('video', 'Video')
    ]
    
    section = models.OneToOneField(Section, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=CONTENT_TYPES)
    
    text = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='content_images/', blank=True, null=True)
    video = models.FileField(upload_to='content_videos/', blank=True, null=True)
    
    def __str__(self):
        return f"{self.section.title} ({self.type})"
    
class Question(models.Model):
    ANSWER_TYPES = [
        ('short', 'Short answer'),
        ('long', "Long answer"),
        ('radio', 'Multiple choice'),
        ('checkbox', 'Checkboxes'),
        ('range', 'Linear scale'),
        ('date', 'Date')
    ]
    
    section = models.OneToOneField(Section, on_delete=models.CASCADE)
    answer_type = models.CharField(max_length=10, choices=ANSWER_TYPES)
    is_required = models.BooleanField(default=False)
    
    min_range = models.IntegerField(blank=True, null=True) 
    max_range = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.section.title
    
# for radio, checlbox and dropdown
class QuestionOption(models.Model):
    question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    def __str__(self):
        return self.text
    
    
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    submitted_at = models.DateTimeField(auto_now_add=True)
    
    short_text = models.CharField(max_length=255, blank=True, null=True)
    long_text = models.TextField(blank=True, null=True)
    selected_options = models.ManyToManyField(QuestionOption, blank=True)  # for checkbox, radio, dropdown
    range_value = models.IntegerField(blank=True, null=True)
    date_value = models.DateField(blank=True, null=True)

    def __str__(self):
        return f"{self.user} - {self.question}"

    def get_value(self):
        # Helper to get the actual answer value in a generic way
        if self.short_text:
            return self.short_text
        elif self.long_text:
            return self.long_text
        elif self.selected_options.exists():
            return list(self.selected_options.values_list('text', flat=True))
        elif self.range_value is not None:
            return self.range_value
        elif self.date_value:
            return self.date_value
        return None