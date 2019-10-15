from boogie.configurations import Conf, env
from constance import config

class ConstanceConf(Conf):
    """
    Dynamic django settings, edit on admin page
    """

    CONSTANCE_BACKEND = env("constance.backends.database.DatabaseBackend")
    CONSTANCE_IGNORE_ADMIN_VERSION_CHECK = True

    def get_constance_config(self):
        return {
            "EJ_MAX_BOARD_NUMBER": (
                self.EJ_MAX_BOARD_NUMBER,
                "Maximum number of boards that a common user can create",
                int,
            ),
            "EJ_PROFILE_STATE_CHOICES": (
                self.EJ_PROFILE_STATE_CHOICES,
                "State choices for state field in profile",
                "choicesfield",
            ),
            "EJ_USER_HOME_PATH": (
                self.EJ_USER_HOME_PATH,
                "Landing page for logged user",
                str,
            ),
            "EJ_ANONYMOUS_HOME_PATH": (
                self.EJ_ANONYMOUS_HOME_PATH,
                "Landing page for anonymous user",
                str,
            ),
            "EJ_PROFILE_PHOTO": (
                self.EJ_PROFILE_PHOTO,
                "Landing page for anonymous user",
                bool,
            ),
            "EJ_PROFILE_RACE": (
                self.EJ_PROFILE_RACE,
                "Landing page for anonymous user",
                bool,
            ),
            "EJ_PROFILE_GENDER": (
                self.EJ_PROFILE_GENDER,
                "Landing page for anonymous user",
                bool,
            ),
            "EJ_PROFILE_BIRTH_DATE": (
                self.EJ_PROFILE_BIRTH_DATE,
                "Landing page for anonymous user",
                bool,
            ),
            "EJ_PROFILE_OCCUPATION": (
                self.EJ_PROFILE_OCCUPATION,
                "Landing page for anonymous user",
                bool,
            ),
            "EJ_PROFILE_CITY": (
                self.EJ_PROFILE_CITY,
                "Landing page for anonymous user",
                bool,
            ),
            "EJ_PROFILE_STATE": (
                self.EJ_PROFILE_STATE,
                "Landing page for anonymous user",
                bool,
            ),
            "EJ_PROFILE_COUNTRY": (
                self.EJ_PROFILE_COUNTRY,
                "Landing page for anonymous user",
                bool,
            ),
            "EJ_PROFILE_POLITICAL_ACTIVITY": (
                self.EJ_PROFILE_POLITICAL_ACTIVITY,
                "Landing page for anonymous user",
                bool,
            ),
            "EJ_PROFILE_BIOGRAPHY": (
                self.EJ_PROFILE_BIOGRAPHY,
                "Landing page for anonymous user",
                bool,
            ),   
        }

    CONSTANCE_ADDITIONAL_FIELDS = {
        "charfield": [
            "django.forms.fields.CharField",
            {"widget": "django.forms.TextInput", "required": False},
        ],
        "choicesfield": ["django.forms.ChoiceField", {"required": False}],
    }

    CONSTANCE_CONFIG_FIELDSETS = {
        "EJ Options": ("EJ_MAX_BOARD_NUMBER", "EJ_PROFILE_STATE_CHOICES", "EJ_USER_HOME_PATH", "EJ_ANONYMOUS_HOME_PATH")
    }

    # Auxiliary options
    EJ_USER_HOME_PATH = env("/start/", name="{attr}")
    EJ_ANONYMOUS_HOME_PATH = env("/conversations/", name="{attr}")

    EJ_PROFILE_PHOTO = env(True, name="{attr}")
    EJ_PROFILE_RACE = env(True, name="{attr}")
    EJ_PROFILE_GENDER = env(True, name="{attr}")
    EJ_PROFILE_BIRTH_DATE = env(True, name="{attr}")
    EJ_PROFILE_OCCUPATION = env(True, name="{attr}")
    EJ_PROFILE_CITY = env(True, name="{attr}")
    EJ_PROFILE_STATE = env(True, name="{attr}")
    EJ_PROFILE_COUNTRY = env(True, name="{attr}")
    EJ_PROFILE_POLITICAL_ACTIVITY = env(True, name="{attr}")
    EJ_PROFILE_BIOGRAPHY = env(True, name="{attr}")

    EJ_MAX_BOARD_NUMBER = env(1, name="{attr}")
    EJ_PROFILE_STATE_CHOICES = env(
        (
            ("AC", "Acre"),
            ("AL", "Alagoas"),
            ("AP", "Amapá"),
            ("AM", "Amazonas"),
            ("BA", "Bahia"),
            ("CE", "Ceará"),
            ("DF", "Distrito Federal"),
            ("ES", "Espírito Santo"),
            ("GO", "Goiás"),
            ("MA", "Maranhão"),
            ("MT", "Mato Grosso"),
            ("MS", "Mato Grosso do Sul"),
            ("MG", "Minas Gerais"),
            ("PA", "Pará"),
            ("PB", "Paraíba"),
            ("PR", "Paraná"),
            ("PE", "Pernambuco"),
            ("PI", "Piauí"),
            ("RJ", "Rio de Janeiro"),
            ("RN", "Rio Grande do Norte"),
            ("RS", "Rio Grande do Sul"),
            ("RO", "Rondônia"),
            ("RR", "Roraima"),
            ("SC", "Santa Catarina"),
            ("SP", "São Paulo"),
            ("SE", "Sergipe"),
            ("TO", "Tocantins"),
        ),
        name="{attr}",
    )
