from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from constance import config

from . import models

descr = lambda msg: lambda f: setattr(f, "short_description", msg) or f


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    
    # config.EJ_PROFILE_PHOTO
    # config.EJ_PROFILE_RACE
    # config.EJ_PROFILE_GENDER
    # config.EJ_PROFILE_BIRTH_DATE
    # config.EJ_PROFILE_OCCUPATION

    # config.EJ_PROFILE_CITY
    # config.EJ_PROFILE_STATE
    # config.EJ_PROFILE_COUNTRY

    # config.EJ_PROFILE_POLITICAL_ACTIVITY
    # config.EJ_PROFILE_BIOGRAPHY
    
    basic_field_list = []
    if config.EJ_PROFILE_PHOTO:
        basic_field_list.append("profile_photo")
    if config.EJ_PROFILE_RACE:
        basic_field_list.append("race")
    if config.EJ_PROFILE_GENDER:
        basic_field_list.append("gender")
    if config.EJ_PROFILE_BIRTH_DATE:
        basic_field_list.append("birth_date")
    if config.EJ_PROFILE_OCCUPATION:
        basic_field_list.append("occupation")
    print(basic_field_list)
    
    adress_field_list =[]
    if config.EJ_PROFILE_CITY:
        adress_field_list.append("city")
    if config.EJ_PROFILE_STATE:
        adress_field_list.append("state")
    if config.EJ_PROFILE_COUNTRY:
        adress_field_list.append("country")
    print(adress_field_list)

    advanced_field_list = []
    if config.EJ_PROFILE_POLITICAL_ACTIVITY:
        advanced_field_list.append("political_activity")
    if config.EJ_PROFILE_BIOGRAPHY:
        advanced_field_list.append("biography")
    print(advanced_field_list)

    fieldsets = (
        (
            _("Basic information"),
            {"fields": basic_field_list},
        ),
        (_("Address"), {"fields": adress_field_list}),

        (_("Advanced"), {"fields": advanced_field_list}),
    )
    list_display = ("name", "email", "is_superuser")
    search_fields = ["user__name", "user__email"]

