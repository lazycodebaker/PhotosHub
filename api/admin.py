
from api.models import UserModel , PhotoModel
from django.contrib import admin

@admin.register(UserModel)
class UserAdminModel(admin.ModelAdmin):
    list_display = ('id','user','auth_token','is_verified','joined_on')


@admin.register(PhotoModel)
class UserAdminModel(admin.ModelAdmin):
    list_display = ('id','user','photo')



