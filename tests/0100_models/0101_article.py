from django.core.exceptions import ValidationError

import pytest

from lotus.factories import CategoryFactory, TagFactory

from djangocms_lotus.factories import ArticleFluxFactory
from djangocms_lotus.models import ArticleFlux


def test_basic(db):
    """
    Basic model saving with required fields should not fail
    """
    instance = ArticleFlux(title="Foo")
    instance.full_clean()
    instance.save()

    created = ArticleFlux.objects.get(pk=instance.id)

    assert ArticleFlux.objects.filter(title="Foo").count() == 1
    assert created.title == "Foo"


def test_model_required_fields(db):
    """
    Basic model validation with missing required fields should fail.
    """
    flux = ArticleFlux()

    with pytest.raises(ValidationError) as excinfo:
        flux.full_clean()

    assert excinfo.value.message_dict == {
        "title": [
            "This field cannot be blank."
        ],
    }


def test_factory_basic(db):
    """
    Factory should create object without any required arguments.
    """
    flux = ArticleFluxFactory()
    # Force model validation since factory bypass it
    flux.full_clean()
    assert ArticleFlux.objects.filter(pk=flux.id).count() == 1


def test_factory_relations(db):
    """
    Factory relations should be managed correctly depending factory arguments.
    """
    # On default no relations are filled
    flux = ArticleFluxFactory()
    assert flux.from_categories.all().count() == 0

    # Automatically create a single random relation
    flux = ArticleFluxFactory(from_categories=True, from_tags=True)
    assert flux.from_categories.all().count() == 1
    assert flux.from_tags.all().count() == 1

    # Assign given objects
    flux = ArticleFluxFactory(
        from_categories=[
            CategoryFactory(slug="foo"),
            CategoryFactory(slug="baguette", language="fr"),
        ],
        from_tags=[TagFactory(slug="bar")],
    )

    categories = [(item.slug, item.language) for item in flux.from_categories.all()]
    assert categories == [("foo", "en"), ("baguette", "fr")]

    tags = [item.slug for item in flux.from_tags.all()]
    assert tags == ["bar"]
