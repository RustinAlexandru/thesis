from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from moderation.admin import ModerationAdmin

from .models import Ninegag, UserProfile, Joke, Youtube, PostComment


# class Admin(admin.ModelAdmin):
    # readonly_fields = ('date_added',)

class NinegagAdmin(ModerationAdmin):
    readonly_fields = ('date_added',)



class UserProfileInline(admin.StackedInline):
    model = UserProfile

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline,]


class JokeAdmin(ModerationAdmin):
    list_display = ("text", "category")


class YoutubeAdmin(admin.ModelAdmin):
    list_display = ("title", 'pk', "added_at")

# Register your models here.
# admin.site.register(Ninegag, Admin)
admin.site.register(UserProfile)
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(Joke, JokeAdmin)
admin.site.register(Ninegag, NinegagAdmin)
admin.site.register(Youtube, YoutubeAdmin)
admin.site.register(PostComment)
