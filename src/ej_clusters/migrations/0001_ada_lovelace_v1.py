# Generated by Django 2.1.10 on 2019-07-02 16:16
"""
0001_ada_lovelace_v1.py
=======================
Migration
"""

import boogie.fields.enum_field
import django.utils.timezone
import model_utils.fields
import ej_clusters.enums
import ej_conversations.models.vote
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    replaces = [("ej_clusters", "0001_first_migration"), ("ej_clusters", "0002_update_field_choices")]

    initial = True

    dependencies = [
        ("ej_conversations", "0001_first_migration"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Cluster",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, 
                        primary_key=True, 
                        serialize=False, 
                        verbose_name="ID"
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, 
                                editable=False, 
                                verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, 
                                editable=False, 
                                verbose_name="modified"
                    ),
                ),
                ("name", models.CharField(max_length=64, verbose_name="Name")),
                (
                    "description",
                    models.TextField(
                        blank=True, 
                        help_text="How was this cluster conceived?", 
                        verbose_name="Description"
                    ),
                ),
            ],
            options={"abstract": False},
        ),
        migrations.CreateModel(
            name="Clusterization",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, 
                        primary_key=True, 
                        serialize=False, 
                        verbose_name="ID"
                    ),
                ),
                (
                    "created",
                    model_utils.fields.AutoCreatedField(
                        default=django.utils.timezone.now, 
                        editable=False, 
                        verbose_name="created"
                    ),
                ),
                (
                    "modified",
                    model_utils.fields.AutoLastModifiedField(
                        default=django.utils.timezone.now, 
                        editable=False, 
                        verbose_name="modified"
                    ),
                ),
                (
                    "cluster_status",
                    boogie.fields.enum_field.EnumField(
                        ej_clusters.enums.ClusterStatus, 
                        default=ej_clusters.enums.ClusterStatus(0)
                    ),
                ),
                ("unprocessed_votes", models.PositiveSmallIntegerField(default=0, editable=False)),
                ("unprocessed_comments", models.PositiveSmallIntegerField(default=0, editable=False)),
                (
                    "conversation",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="clusterization",
                        to="ej_conversations.Conversation",
                    ),
                ),
            ],
            options={"ordering": ["conversation_id"]},
        ),
        migrations.CreateModel(
            name="Stereotype",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, primary_key=True, serialize=False, verbose_name="ID"
                    ),
                ),
                ("name", models.CharField(max_length=64, verbose_name="Name")),
                (
                    "description",
                    models.TextField(
                        blank=True,
                        help_text="A detailed description of your stereotype for future reference. 
                                   You can specify a background history, 
                                   or give hints on the exact profile the stereotype wants to capture.",
                        verbose_name="Description",
                    ),
                ),
                (
                    "conversation",
                    models.ForeignKey(
                        blank=True,
                        help_text="Conversation associated with the stereotype.",
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stereotypes",
                        to="ej_conversations.Conversation",
                    ),
                ),
                (
                    "owner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="StereotypeVote",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True, 
                        primary_key=True, 
                        serialize=False, 
                        verbose_name="ID"
                    ),
                ),
                (
                    "choice",
                    boogie.fields.enum_field.EnumField(
                        ej_conversations.models.vote.Choice, 
                        verbose_name="Choice"
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="votes",
                        to="ej_clusters.Stereotype",
                    ),
                ),
                (
                    "comment",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stereotype_votes",
                        to="ej_conversations.Comment",
                        verbose_name="Comment",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="cluster",
            name="clusterization",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="clusters",
                to="ej_clusters.Clusterization",
            ),
        ),
        migrations.AddField(
            model_name="cluster",
            name="stereotypes",
            field=models.ManyToManyField(related_name="clusters", to="ej_clusters.Stereotype"),
        ),
        migrations.AddField(
            model_name="cluster",
            name="users",
            field=models.ManyToManyField(blank=True, 
                                            related_name="clusters", 
                                            to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterUniqueTogether(name="stereotype", 
                                        unique_together={("name", "conversation")}),
    ]
