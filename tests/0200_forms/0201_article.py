from lotus.factories import CategoryFactory, TagFactory

from djangocms_lotus.choices import get_latestflux_template_default
from djangocms_lotus.forms import ArticleFluxForm
from djangocms_lotus.models import ArticleFlux
from djangocms_lotus.utils.tests import flatten_form_errors


def test_empty(db):
    """
    Empty form should not be valid because of required fields.
    """
    f = ArticleFluxForm({})

    validation = f.is_valid()
    assert validation is False
    assert flatten_form_errors(f) == {
        "length": ["This field is required."],
        "template": ["This field is required."],
        "title": ["This field is required."],
    }


def test_invalid(db):
    """
    Invalid field values should raises specific errors.
    """
    f = ArticleFluxForm({
        "title": "",
        "length": -1,
        "template": "nope",
    })

    validation = f.is_valid()
    assert validation is False

    # import json
    # print(json.dumps(flatten_form_errors(f), indent=4))

    assert flatten_form_errors(f) == {
        "title": ["This field is required."],
        "length": ["Ensure this value is greater than or equal to 0."],
        "template": [
            "Select a valid choice. nope is not one of the available choices.",
        ],
    }


def test_valid(client, db, settings):
    """
    Form with correct data should succeed and save object.
    """
    category_foo = CategoryFactory(title="foo")
    CategoryFactory(title="bar", language="fr")
    tag_ping = TagFactory(name="ping")
    TagFactory(name="pong")

    f = ArticleFluxForm({
        "title": "Foo",
        "length": 42,
        "template": get_latestflux_template_default(),
        "from_categories": [category_foo.id],
        "from_tags": [tag_ping.id],
    })
    validation = f.is_valid()
    assert validation is True

    created = f.save()
    assert ArticleFlux.objects.count() == 1

    flux = ArticleFlux.objects.get(pk=created.id)
    assert list(flux.from_categories.all().values_list("id", flat=True)) == [
        category_foo.id,
    ]
    assert list(flux.from_tags.all().values_list("id", flat=True)) == [tag_ping.id]
