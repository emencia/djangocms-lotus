from freezegun import freeze_time

from cms.api import add_plugin

from djangocms_lotus.factories import UserFactory
from djangocms_lotus.plugins.articleflux import ArticleFluxPlugin
from djangocms_lotus.utils.tests import html_pyquery
from djangocms_lotus.utils.cms_tests import cms_page_create_helper

from tests.datasets import LotusAdvancedDataset


def apply_plugin_params(plugin, length=10, featured_only=False, from_categories=[],
                        from_tags=[]):
    """
    Helper to apply default plugin parameters along custom ones from arguments.
    """
    plugin.length = length
    plugin.featured_only = featured_only
    plugin.save()
    plugin.from_categories.set(from_categories)
    plugin.from_tags.set(from_tags)
    plugin.refresh_from_db()


@freeze_time("2012-10-15 10:00:00")
def test_render_basic(db, admin_client, client, settings):
    """
    Plugin should be properly rendered in a Page and article filtering should be done
    right depending plugin parameters.
    """
    # Create a proper Lotus datas
    dataset = LotusAdvancedDataset()

    # Create dummy page where to insert plugin
    page, content, version = cms_page_create_helper(
        "Foo",
        settings.TEST_PAGE_TEMPLATES,
        UserFactory(flag_is_superuser=True),
        publish=True
    )

    # Get placeholder destination
    placeholder = page.get_placeholders(settings.LANGUAGE_CODE).get(slot="content")

    # Create plugin into page placeholder
    plugin = add_plugin(
        placeholder,
        ArticleFluxPlugin,
        settings.LANGUAGE_CODE,
        title="Foo flux",
    )

    url = page.get_absolute_url(language=settings.LANGUAGE_CODE)

    # Plugin is present in rendered HTML and Lotus filtering is correctly done
    apply_plugin_params(plugin)
    response = client.get(url)
    dom = html_pyquery(response)
    titles = [item.text for item in dom.find(".article-flux-plugin__article .title")]
    assert titles == [
        "05. pinned, published past hour",
        "04. published past hour",
        "06. featured, published past hour",
        "08. published past hour, end next hour",
        "02. published yesterday"
    ]

    # Private is shown to staff users
    apply_plugin_params(plugin)
    response = admin_client.get(url)
    dom = html_pyquery(response)
    titles = [item.text for item in dom.find(".article-flux-plugin__article .title")]
    assert titles == [
        "05. pinned, published past hour",
        "04. published past hour",
        "06. featured, published past hour",
        "07. private, published past hour",
        "08. published past hour, end next hour",
        "02. published yesterday"
    ]

    # Length parameter is respected (we restore default params for sanity)
    apply_plugin_params(plugin, length=2)
    response = client.get(url)
    dom = html_pyquery(response)
    titles = [item.text for item in dom.find(".article-flux-plugin__article .title")]
    assert titles == [
        "05. pinned, published past hour",
        "04. published past hour",
    ]

    # Featured parameter is respected
    apply_plugin_params(plugin, featured_only=True)
    response = client.get(url)
    dom = html_pyquery(response)
    titles = [item.text for item in dom.find(".article-flux-plugin__article .title")]
    assert titles == ["06. featured, published past hour"]

    # From categories parameter is respected
    apply_plugin_params(plugin, from_categories=[dataset.cat_bar])
    response = client.get(url)
    dom = html_pyquery(response)
    titles = [item.text for item in dom.find(".article-flux-plugin__article .title")]
    assert titles == [
        "02. published yesterday"
    ]

    # From tags parameter is respected
    apply_plugin_params(plugin, from_tags=[dataset.tag_pong])
    response = client.get(url)
    dom = html_pyquery(response)
    titles = [item.text for item in dom.find(".article-flux-plugin__article .title")]
    assert titles == [
        "02. published yesterday"
    ]
