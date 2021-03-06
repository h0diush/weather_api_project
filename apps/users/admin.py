from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import TokenTelegramBot, User


@admin.register(User)
class UserAdminModel(UserAdmin):
    ordering = ['email', 'username', 'phone']
    model = User
    list_display = ['upper_get_full_name', 'email', 'get_output_phone', 'city',
                    'tg_id']
    list_filter = ['username', 'email', 'phone']

    def upper_get_full_name(self, obj):
        if obj.first_name != '' and obj.last_name != '' and obj.surname != '':
            return f'{obj.get_full_name()} ({obj.username})'
        return obj.username

    def get_output_phone(self, obj):
        return obj.get_phone()

    upper_get_full_name.short_description = 'ФИО(Имя пользователя)'
    get_output_phone.short_description = 'Номер телефона'

    fieldsets = (
        ("Авторизация", {'fields': ('username', 'email', 'password')}),
        ("Персональная информация", {
            'fields': (
                'first_name', 'last_name', 'surname', 'phone', 'city', 'tg_id'
            )}),
        ("Разрешения", {
            'fields': ('is_staff', 'is_active', 'is_superuser',)}),
        ("Дополнительная информация", {
            'fields': ('last_login', 'date_joined',)}),
    )
    add_fieldsets = (
        (None,
         {
             "classes": ("wide",),
             'fields': (
                 'username',
                 'email',
                 'phone',
                 'password1',
                 'password2',
                 'is_staff',
                 'is_active'
             )
         }),
    )


admin.site.register(TokenTelegramBot)
