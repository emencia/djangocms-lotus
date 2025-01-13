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

    # Expected form in response HTML
    dom = html_pyquery(response)
    assert len(dom.find("#articleflux_form")) == 1
