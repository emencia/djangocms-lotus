from django.conf import settings

from cms.api import add_plugin, create_page
from cms.models import Placeholder
from cms.test_utils.testcases import CMSTestCase

try:
    from djangocms_versioning.models import Version
except ImportError:
    Version = None


def cms_page_create_helper(title, template, author, language=None, reverse_id=None,
                           is_home=False, publish=False):
    """
    Helper to quickly create a CMS page.

    Since DjangoCMS 4 has hardly leveled up the way to programmatically create a page
    and publish it, we need some helper around their programmatic API (sigh).

    .. Note::
        Currently i don't know how to publish page when "djangocms_versioning" is not
        installed, it may even be automatically published since there is no version.
        It seems a very possible behavior because from tests the plugin render is
        working without versionning.

    Arguments:
        title (string): Page content title.
        template (string): Page content template
        author (User): User object for authoring page creation.

    Keyword Arguments:
        language (string): Language code.
        reverse_id (string): Reverse id for page if given else Page would have none.
        is_home (boolean): Define page as the new homepage.
        publish (boolean): Define if page should be published else it will be a draft
            to publish yourself using ``version.publish(author)``.

    Returns:
        tuple: To ease further manipulation, this method return a tuple containing
        respectively the Page object, its PageContent page and then its last version
        object.
    """
    language = language or settings.LANGUAGE_CODE

    page = create_page(
        title,
        template,
        language,
        reverse_id=reverse_id,
        created_by=author,
    )

    if is_home:
        page.set_as_homepage()

    page_content = page.pagecontent_set(
        manager="admin_manager"
    ).latest_content().last()

    version = None
    if Version:
        version = Version.objects.get(object_id=page_content.id)

    if publish and version:
        version.publish(author)

    return page, page_content, version


class CMSPluginTestCase(CMSTestCase):
    """
    Enriched CMS test case object to include useful stuff about plugin
    rendering.

    .. NOTE::
        The CMSTestCase mixin from DjangoCMS is making queries in its "tearDown"
        method which causes database transaction errors with tests that have
        already generated a database error.

        A workaround is to decorate such tests with
        ``django.db.transaction`` (or to use it as a context manager) so that
        the test has its own transaction that is rolled back before the TearDown
        method sends its queries to the database.
    """

    def get_practical_plugin_context(self, extra_context=None):
        """
        Build a template context with dummy request object and
        instanciated content renderer suitable to perform full rendering of
        any plugin.

        .. NOTE::
            CMSTestCase use a dummy AnonymousUser on default behavior. You can
            override it with a custom user as an ``user`` attribute on your
            test case object.

        Keyword Arguments:
            extra_context (dict): Dictionnary to add extra variable to context.
                Default to an empty dict.

        Returns:
            django.template.Context: Template context filled with request
            object as ``request`` item and content renderer as
            ``cms_content_renderer`` item.
        """
        context = self.get_context()
        if extra_context:
            context.update(extra_context)

        renderer = self.get_content_renderer(request=context["request"])

        # 'cms_content_renderer' is the expected var name from CMS rendering
        # machinery
        context["cms_content_renderer"] = renderer

        return context

    def create_basic_render(self, plugin, slot_name="test", lang="en",
                            copy_relations_from=None, children=None, **kwargs):
        """
        A shortcut to create a basic render for a plugin.

        Arguments:
            plugin (cms.plugin_base import CMSPluginBase): Plugin model used to create
                plugin object.

        Keyword Arguments:
            slot_name (string): Template placeholder name where to push the plugin.
                Default to a slot named ``test``.
            lang (string): Language code to use for plugins to create. Default to
                ``en``.
            copy_relations_from (object): If model, which plugin is based on, has
                relations they need to be copied onto the created object. For this case
                you need to create a dummy object before and pass it to this argument.
                See Plugin reference from DjangoCMS reference for details.
            children (list): A list of lists for each children plugin to attach to
                the main one. This only allows for one level of children, there is no
                recursive capability. Each plugin item is a list where the first item
                is the plugin model to use and the second one is a dict of keyword
                arguments for model fields to give to ``add_plugin``.

        Returns:
            tuple: A tuple of items, respectively the used placeholder object, the
            created main plugin object, the used template context for rendering and
            finally the built HTML for the plugin.
        """
        # Create a dummy slot if not given in arguments
        placeholder = (kwargs.pop("placeholder", None)
                       or Placeholder.objects.create(slot=slot_name))

        # Template context
        context = self.get_practical_plugin_context()

        # Init plugin with some content
        model_instance = add_plugin(
            placeholder,
            plugin,
            lang,
            **kwargs
        )

        # Create and attach children plugins if any
        if children:
            for plugin_type, child_kwargs in children:
                child_kwargs["target"] = model_instance
                add_plugin(
                    placeholder,
                    plugin_type,
                    lang,
                    **child_kwargs
                )

        # Copy relation when asked, this is required for plugin model with
        # foreign key since djangocms machinery does not perform it with API
        if copy_relations_from and hasattr(model_instance, "copy_relations"):
            model_instance.copy_relations(copy_relations_from)

        # Render placeholder so plugin is fully rendered in real situation
        html = context["cms_content_renderer"].render_placeholder(
            placeholder, context=context, language=lang
        )

        return placeholder, model_instance, context, html
