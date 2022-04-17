from django.contrib import admin

# Register your models here.
from .models import Lobby,Topic,Post,User

admin.site.register(Lobby)
admin.site.register(Topic)
admin.site.register(Post)
admin.site.register(User)