from cms.utils.urlutils import admin_reverse
from cms.models import Placeholder
from lotus.factories import CategoryFactory, TagFactory


from djangocms_lotus.factories import UserFactory
from djangocms_lotus.utils.tests import html_pyquery


def test_get_form_view_add(db, client, settings):
    """
    Plugin creation form should return a success status code from GET request and
    should have all expected field inputs.
    """
    # Request to plugin form must be authenticated with a staff
    client.force_login(UserFactory(flag_is_superuser=True))

    # Create some categories and tags to fill select choices
    CategoryFactory(title="foo"),
    CategoryFactory(title="bar", language="fr"),
    TagFactory(name="ping")

    # Get placeholder destination
    placeholder = Placeholder.objects.create(slot="content")

    # Get the edition plugin form url and open it
    url = admin_reverse("cms_placeholder_add_plugin")
    response = client.get(url, {
        "plugin_type": "ArticleFluxPlugin",
        "placeholder_id": placeholder.pk,
        "cms_path": "/{}/".format(settings.LANGUAGE_CODE),
        "plugin_language": settings.LANGUAGE_CODE,
        "plugin_position": 1,
    })

    # Expected http success status
    assert response.status_code == 200

    # Parse resulting plugin form and collect input and select form elements
    dom = html_pyquery(response)
    inputs = sorted(
        [
            item.get("name")
            for item in dom.find("#articleflux_form input, #articleflux_form select")
        ]
    )
    assert inputs == [
        "_popup",
        "_save",
        "csrfmiddlewaretoken",
        "featured_only",
        "from_categories",
        "from_tags",
        "length",
        "template",
        "title",
    ]

    categories = [
        item.text
        for item in dom.find("#articleflux_form #id_from_categories option")
    ]
    assert categories == ["bar", "foo"]

    tags = [
        item.text
        for item in dom.find("#articleflux_form #id_from_tags option")
    ]
    assert tags == ["ping"]
