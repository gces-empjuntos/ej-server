import logging

from autoslug import AutoSlugField
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel, StatusModel
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase

from boogie import rules
from boogie.rest import rest_api
from .comment import Comment, normalize_status
from .vote import Vote, Choice
from ..managers import ConversationManager

NOT_GIVEN = object()
log = logging.getLogger('ej_conversations')


def slug_base(conversation):
    title = conversation.title
    if conversation.status != conversation.STATUS.promoted:
        username = conversation.author.username
        title = f'{username}--{title}'
    return title.lower()


class TaggedConversation(TaggedItemBase):
    """
    Add tags to Conversations with real Foreign Keys
    """
    content_object = models.ForeignKey('Conversation', on_delete=models.CASCADE)


@rest_api(exclude=['status_changed'])
class Conversation(TimeStampedModel, StatusModel):
    """
    A topic of conversation.
    """
    STATUS = Choices(
        ('personal', _('Personal')),
        ('promoted', _('Promoted')),
        ('pending', _('Pending')),
    )
    title = models.CharField(
        _('Title'),
        max_length=255,
        help_text=_(
            'A short description about this conversations. This is used internally '
            'and to create URL slugs. (e.g. School system)'
        )
    )
    text = models.TextField(
        _('Question'),
        help_text=_(
            'A question that is displayed to the users in a conversation card. (e.g.: How can we '
            'improve the school system in our community?)'
        ),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='conversations',
        help_text=_(
            'Only the author and administrative staff can edit this conversation.'
        )
    )
    slug = AutoSlugField(
        unique=True,
        populate_from=slug_base,
    )
    objects = ConversationManager()
    tags = TaggableManager(through=TaggedConversation)
    votes = property(lambda self: Vote.objects.filter(comment__conversation=self))
    is_promoted = property(lambda self: self.status == self.STATUS.promoted)

    class Meta:
        ordering = ['created']
        permissions = (
            ('is_publisher', _('Can publish promoted conversations')),
            ('is_moderator', _('Can moderate comments in any conversation')),
        )

    @property
    def approved_comments(self):
        return self.comments.filter(status=Comment.STATUS.approved)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.id is None:
            pass
        super().save(*args, **kwargs)

    def clean(self):
        can_edit = 'ej_conversations.can_edit_conversation'
        if self.is_promoted and not self.author.has_perm(can_edit, self):
            raise ValidationError(_(
                'User does not have permission to create a promoted '
                'conversation.')
            )

    def get_absolute_url(self, user=None):
        kwargs = {'conversation': self}
        if user is None:
            return reverse('conversation:detail', kwargs=kwargs)
        else:
            kwargs['user'] = user
            return reverse('conversation:detail-for-user', kwargs=kwargs)

    def user_votes(self, user):
        """
        Get all votes in conversation for the given user.
        """
        return Vote.objects.filter(comment__conversation=self, author=user)

    def create_comment(self, author, content, commit=True, *, status=None,
                       check_limits=True, **kwargs):
        """
        Create a new comment object for the given user.

        If commit=True (default), comment is persisted on the database.

        By default, this method check if the user can post according to the
        limits imposed by the conversation. It also normalizes duplicate
        comments and reuse duplicates from the database.
        """

        # Convert status, if necessary
        kwargs['status'] = normalize_status(status)

        # Check limits
        if check_limits and not author.has_perm('ej_conversations.can_comment', self):
            log.info('failed attempt to create comment by %s' % author)
            raise PermissionError('user cannot comment on conversation.')

        kwargs.update(author=author, content=content.strip())
        comment = make_clean(Comment, commit, conversation=self, **kwargs)
        log.info('new comment: %s' % comment)
        return comment

    def statistics(self):
        """
        Return a dictionary with basic statistics about conversation.
        """

        # Fixme: this takes several SQL queries. Maybe we can optimize later
        return dict(
            # Vote counts
            votes=dict(
                agree=vote_count(self, Choice.AGREE),
                disagree=vote_count(self, Choice.DISAGREE),
                skip=vote_count(self, Choice.SKIP),
                total=vote_count(self),
            ),

            # Comment counts
            comments=dict(
                approved=comment_count(self, Comment.STATUS.approved),
                rejected=comment_count(self, Comment.STATUS.rejected),
                pending=comment_count(self, Comment.STATUS.pending),
                total=comment_count(self),
            ),

            # Participants count
            participants=get_user_model().objects
                .filter(votes__comment__conversation_id=self.id)
                .distinct()
                .count(),
        )

    def user_statistics(self, user):
        """
        Get information about user.
        """
        max_votes = (
            self.comments
                .filter(status=Comment.STATUS.approved)
                .exclude(author_id=user.id)
                .count()
        )
        given_votes = 0 if user.id is None else (
            Vote.objects
                .filter(comment__conversation_id=self.id, author=user)
                .count()
        )

        e = 1e-50  # for numerical stability
        return dict(
            votes=given_votes,
            missing_votes=max_votes - given_votes,
            participation_ratio=given_votes / (max_votes + e),
        )

    def next_comment(self, user, default=NOT_GIVEN):
        """
        Returns a random comment that user didn't vote yet.

        If default value is not given, raises a Comment.DoesNotExit exception
        if no comments are available for user.
        """
        comment = rules.compute('ej_conversations.next_comment', self, user)
        if comment is not None:
            return comment
        elif default is NOT_GIVEN:
            msg = _('No comments available for this user')
            raise Comment.DoesNotExist(msg)
        else:
            return default


def vote_count(conversation, which=None):
    """
    Return the number of votes of a given type.
    """
    kwargs = dict(comment__conversation_id=conversation.id)
    if which is not None:
        kwargs['choice'] = which
    return Vote.objects.filter(**kwargs).count()


def comment_count(conversation, type=None):
    """
    Return the number of comments of a given type.
    """
    kwargs = {'status': type} if type is not None else {}
    return conversation.comments.filter(**kwargs).count()


def make_clean(cls, commit=True, **kwargs):
    obj = cls(**kwargs)
    obj.full_clean()
    if commit:
        obj.save()
    return obj
