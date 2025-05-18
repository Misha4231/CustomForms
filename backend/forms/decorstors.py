from functools import wraps
from graphql import GraphQLError

from .models import Form, Section
from users.models import User

# checks if a requesting user is the owner of form
def form_owner(func):
    @wraps(func)
    def wrapper(cls, root, info, form_id, *args, **kwargs):
        user = info.context.user
        if not user or not user.is_authenticated:
            raise GraphQLError("Authentication required.")
        
        try:
            form = Form.objects.get(pk=form_id)
        except Form.DoesNotExist:
            raise GraphQLError("Form does not exists")
        
        if form.owner != user:
            raise GraphQLError("You don't have permission to modify this form")

        return func(cls, root, info, form, *args, **kwargs) # replacec form_id with form to avoid double fetch of the same data from database

    return wrapper

# having section id, checks if a requesting user is the owner of form
def form_owner_section_id(func):
    @wraps(func)
    def wrapper(cls, root, info, section_id,  *args, **kwargs):
        try:
            section = Section.objects.select_related('form').get(pk=section_id)
        except Section.DoesNotExist:
            raise GraphQLError("Session does not exist")
        
        form_id = section.form.id
        
        # utilize form_owner to avoid repetition
        return form_owner(func)(cls, root, info, form_id, section, *args, **kwargs)
    
    return wrapper