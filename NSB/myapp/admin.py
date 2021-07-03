from django.contrib import admin
from .models import *
# Register your models here.

admin.site.register(User)
admin.site.register(Service_upload)
admin.site.register(Idea_upload)
admin.site.register(Idea_evalu_comment)
admin.site.register(Service_evalu_upload)