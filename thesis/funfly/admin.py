from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from moderation.admin import ModerationAdmin

from .models import Ninegag, UserProfile, Joke, Youtube, PostComment
from .forms import UserProfileForm


# class Admin(admin.ModelAdmin):
    # readonly_fields = ('date_added',)



class UserProfileInline(admin.StackedInline):
    model = UserProfile
    form = UserProfileForm

class UserProfileAdmin(UserAdmin):
    inlines = [ UserProfileInline,]

class UserProfileAdmin2(admin.ModelAdmin):
    form = UserProfileForm
    filter_horizontal = ['follows',]

class NinegagAdmin(ModerationAdmin):
    list_display = ("title", "pk", "is_video")
    readonly_fields = ('date_added',)

class JokeAdmin(ModerationAdmin):
    list_display = ("text", "category")
    readonly_fields = ('date_added',)


class YoutubeAdmin(admin.ModelAdmin):
    list_display = ("title", "pk", "date_added")


# class PostCommentAdmin(admin.ModelAdmin):
# list_display = ("user")

# Register your models here.
# admin.site.register(Ninegag, Admin)
# admin.site.register(UserProfile)
admin.site.unregister(User)
admin.site.register(User, UserProfileAdmin)
admin.site.register(UserProfile, UserProfileAdmin2)
admin.site.register(Joke, JokeAdmin)
admin.site.register(Ninegag, NinegagAdmin)
admin.site.register(Youtube, YoutubeAdmin)
admin.site.register(PostComment)
