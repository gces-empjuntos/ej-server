from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponseServerError
from django.urls import reverse

from boogie import rules
from boogie.rules import proxy_seq
from hyperpython import a
from . import urlpatterns, conversation_url
from ..models import Conversation
from ej_conversations.models import FavoriteConversation, ConversationBoard


@urlpatterns.route('', name='list')
def conversation_list(request, board=None):
    user = request.user

    if board:
        create_url = reverse('user-conversation:create')
        conversations = Conversation.objects.filter(author=board.owner)
    else:
        create_url = reverse('conversation:create')
        conversations = Conversation.objects.filter(is_promoted=True)

    clist = {
        'conversations': moderated_conversations(user, conversations),
        'can_add_conversation': user.has_perm('ej_conversations.can_add_conversation', board),
    }

    if board and board.owner == user:
        clist['add_link'] = a(_('Add new conversation'), href=create_url)
    else:
        clist['add_link'] = ''

    return clist


@urlpatterns.route(conversation_url)
def detail(request, conversation, owner=None):
    user = request.user
    comment = conversation.next_comment(user, None)
    n_comments = rules.compute('ej_conversations.remaining_comments', conversation, user)
    favorites = FavoriteConversation.objects.filter(conversation=conversation)
    ctx = {
        'conversation': conversation,
        'comment': comment,
        'owner': owner,
        'edit_perm': user.has_perm('ej_conversations.can_edit_conversation', conversation),
        'can_comment': user.has_perm('ej_conversations.can_comment', conversation),
        'remaining_comments': n_comments,
        'login_link': a(_('login'), href=reverse('auth:login')),
        'favorites': favorites,
    }

    if comment and request.POST.get('action') == 'vote':
        vote = request.POST['vote']
        if vote not in {'agree', 'skip', 'disagree'}:
            return HttpResponseServerError('invalid parameter')
        comment.vote(user, vote)

    elif request.POST.get('action') == 'comment':
        comment = request.POST['comment'].strip()

        # FIXME: do not hardcode this and use a proper form!
        comment = comment[:210]
        try:
            ctx['comment'] = conversation.create_comment(user, comment)
        except (PermissionError, ValidationError) as ex:
            ctx['comment_error'] = str(ex)
    elif request.POST.get('action') == 'favorite':
        conversation.toggle_favorite(user)
    return ctx


@urlpatterns.route(conversation_url + 'info/')
def info(conversation):
    return {
        'conversation': conversation,
        'info': conversation.statistics(),
    }


@urlpatterns.route(conversation_url + 'leaderboard/')
def leaderboard(conversation):
    return {
        'conversation': conversation,
        'info': conversation.statistics(),
    }


def moderated_conversations(user, qs=None):
    perm = 'ej_conversations.can_moderate_conversation'
    kwargs = {
        'can_moderate': lambda x: user.has_perm(perm, x)
    }
    if qs is None:
        qs = Conversation.objects.filter(is_promoted=True)
    return proxy_seq(qs, user=user, **kwargs)
