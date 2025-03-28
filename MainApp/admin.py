from django.contrib import admin
from .models import Snippet, Comment

admin.site.register([Snippet, Comment])

# Register your models here.
