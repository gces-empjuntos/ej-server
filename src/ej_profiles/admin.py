from django.contrib import admin
from django.utils.translation import ugettext_lazy as _
from constance import config

from . import models

descr = lambda msg: lambda f: setattr(f, "short_description", msg) or f


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    config.EJ_PROFILE_PHOTO
    config.EJ_PROFILE_RACE
    config.EJ_PROFILE_GENDER
    config.EJ_PROFILE_BIRTH_DATE
    config.EJ_PROFILE_OCCUPATION

    config.EJ_PROFILE_CITY
    config.EJ_PROFILE_STATE
    config.EJ_PROFILE_COUNTRY

    config.EJ_PROFILE_POLITICAL_ACTIVITY
    config.EJ_PROFILE_BIOGRAPHY

    fieldsets = (
        (
            _("Basic information"),
            {"fields": ["profile_photo", 
                        "race", 
                        "gender", 
                        "birth_date" , 
                        "occupation" ]},
        ),
        (_("Address"), {"fields": ["city", 
                                   "state", 
                                   "country"]}),

        (_("Advanced"), {"fields": ["political_activity", 
                                    "biography"]}),
    )
    list_display = ("name", "email", "is_superuser")
    search_fields = ["user__name", "user__email"]

