"""
routes_sterotypes.py
====================

Generates routes to stereotypes groups
"""


from django.shortcuts import redirect
from boogie.router import Router
from ej_clusters.forms import StereotypeForm
from ej_clusters.utils import check_stereotype
from .models import Stereotype

app_name = "ej_cluster"
urlpatterns = Router(
    template="ej_clusters/stereotypes/{name}.jinja2", 
    models={"stereotype": Stereotype}, 
    login=True
)

@urlpatterns.route("")
def group_conversations_stereotype(user_request):
    """
    Create a group with conversations from each stereotype
        user_request: request of prefetch_related method
    """
    stereotypes = []
    for stereotype in user_request:
        stereotype.conversations = conversations = []
        for cluster in stereotype.clusters.all():
            conversations.append(cluster.clusterization.conversation)
        stereotypes.append(stereotype)
    return stereotypes

@urlpatterns.route("")
def list_stereotypes(request):
    """
    Create a dict with all stereotype
        request: request type
    """
    user_request = request.user.stereotypes.prefetch_related("clusters__clusterization__conversation")
    stereotypes = group_conversations_stereotype(user_request)
    stereotypes_dict = {"stereotypes": stereotypes}
    return stereotypes_dict


@urlpatterns.route("add/")
def create_stereotypes(request):
    """
    Create a dict with all stereotype forms
        request: request type
    """
    form = StereotypeForm(request=request, owner=request.user)
    if form.is_valid_post():
        form.save()
        return redirect("stereotypes:list")
    form_dict = {"form": form}
    return form_dict


@urlpatterns.route("<model:stereotype>/edit/")
def edit_stereotypes(request, stereotype):
    """
    Create a dict with all stereotype forms
        request: request type
    """
    check_stereotype(stereotype, request.user)
    form = StereotypeForm(request=request, instance=stereotype)

    if request.POST.get("action") == "delete":
        stereotype.delete()
        return redirect("stereotypes:list")
    elif form.is_valid_post():
        form.save()
        return redirect("stereotypes:list")
    form_stereotype_dict = {"form": form, "stereotype": stereotype}
    return form_stereotype_dict
