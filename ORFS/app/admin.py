from django.contrib import admin
from .models import MyUser,UserProfile,Post,Image,Review,ReportPost
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin


class UserAdmin(BaseUserAdmin):
   

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["id","email", "name","phone", "is_admin"]
    list_filter = ["is_admin"]
    fieldsets = [
        ('User Credentials', {"fields": ["email", "password"]}),
        ("Personal info", {"fields": ["name","phone"]}),
        ("Permissions", {"fields": ["is_admin"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "name","phone", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email","phone"]
    ordering = ["email"]
    filter_horizontal = []

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user','name','email','phone','picture']
    list_filter = ['user','name','email','phone']

# Now register the new UserAdmin...
admin.site.register(MyUser, UserAdmin)




admin.site.register(Image)
admin.site.register(Review)
admin.site.register(ReportPost)
# Register your models here.


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display= ['id','title','owner']