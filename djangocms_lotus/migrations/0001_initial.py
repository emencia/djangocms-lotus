# Generated by Django 5.1.4 on 2025-01-10 02:22
from django.conf import settings
import django.db.models.deletion
from django.db import migrations, models

from ..choices import get_latestflux_template_choices, get_latestflux_template_default

class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("cms", "0035_auto_20230822_2208_squashed_0036_auto_20240311_1028"),
        ("lotus", "0005_add_article_category_alt_text"),
        (
            "taggit",
            "0006_rename_taggeditem_content_type_object_id_taggit_tagg_content_8fc721_idx",
        ),
    ]

    operations = [
        migrations.CreateModel(
            name="ArticleFlux",
            fields=[
                (
                    "cmsplugin_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        related_name="%(app_label)s_%(class)s",
                        serialize=False,
                        to="cms.cmsplugin",
                    ),
                ),
                (
                    "title",
                    models.CharField(
                        default="", max_length=150, verbose_name="title"
                    ),
                ),
                (
                    "template",
                    models.CharField(
                        choices=get_latestflux_template_choices(),
                        default=get_latestflux_template_default(),
                        max_length=150,
                        verbose_name="template",
                    ),
                ),
                (
                    "length",
                    models.PositiveSmallIntegerField(
                        default=settings.CMSLOTUS_ARTICLE_FLUX_LIMIT_DEFAULT,
                        verbose_name="length"
                    ),
                ),
                (
                    "featured_only",
                    models.BooleanField(
                        blank=True, default=False, verbose_name="featured only"
                    ),
                ),
                (
                    "from_categories",
                    models.ManyToManyField(
                        blank=True,
                        related_name="articleflux",
                        to="lotus.category",
                        verbose_name="from categories",
                    ),
                ),
                (
                    "from_tags",
                    models.ManyToManyField(
                        blank=True, to="taggit.tag", verbose_name="from tags"
                    ),
                ),
            ],
            options={
                "verbose_name": "Article flux",
                "verbose_name_plural": "Article flux",
            },
            bases=("cms.cmsplugin",),
        ),
    ]
