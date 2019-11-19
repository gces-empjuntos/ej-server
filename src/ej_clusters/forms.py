from django import forms
from django.utils.translation import ugettext_lazy as _
from ej.forms import EjModelForm
from .models import Stereotype, Cluster


class StereotypeForm(EjModelForm):
    """
    Create and edit new stereotypes
    """

    class Meta:
        """ We have to add the owner attribute to enable the unique owner + name
            validation constraint. This is not ideal since we have to fake the
            existence of this field using default values

            Attributes:
                model
                fields
        """

        model = Stereotype
        fields = ["name", "description", "owner"]

    def __init__(self, *args, owner=None, instance=None, **kwargs):
        self.owner_instance = owner = owner or instance.owner
        kwargs["instance"] = instance
        kwargs["initial"] = {"owner": owner, **kwargs.get("initial", {})}
        super(StereotypeForm, self).__init__(*args, **kwargs)

    def full_clean(self):
        self.data = self.data.copy()
        self.data["owner"] = str(self.owner_instance.id)
        return super().full_clean()


class ClusterForm(EjModelForm):
    """
    Edit clusters when configuring opinion groups
    """

    class Meta:
        """ Form clusters
            Attributes:
                model: what cluster
                fields: what fields name, description or stereotypes
                help_texts: what choice
                labels: label types
        """
        model = Cluster
        fields = ["name", "description", "stereotypes"]
        help_texts = {
            "stereotypes": _(
                "You can select multiple personas for each group. Personas are "
                "users used as reference that you control and define the opinion "
                "profile of groups."
            )
        }
        labels = {"stereotypes": _("Personas"), "new_persona": ""}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["stereotypes"].required = False


class ClusterFormNew(ClusterForm):
    new_persona = forms.BooleanField(
        required=False,
        initial=True,
        help_text=_("Create new persona with the name of the group if no other persona isselected."),
    )

    def clean(self):
        if not self.cleaned_data["new_persona"] and not self.cleaned_data["stereotypes"]:
            self.add_error( "stereotypes", 
                            _("You must select a persona or create a new one.")
            )

    def _save_m2m(self):
        super()._save_m2m()
        has_stereotypes = len(self.cleaned_data["stereotypes"]) != 0
        if self.cleaned_data["new_persona"] and not has_stereotypes:
            owner = self.instance.clusterization.conversation.author
            stereotype, _ = Stereotype.objects.get_or_create(
                name=self.cleaned_data["name"], 
                description=self.cleaned_data["description"], 
                owner=owner
            )
            self.instance.stereotypes.add(stereotype)
