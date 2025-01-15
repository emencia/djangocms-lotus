
=========
Changelog
=========

Development
***********

.. todo::

    Main goal was from Lotus issue #80:

    - [x] have a CMS plugin to include articles in a cms page;
    - [ ] have a CMS plugin to include category list in a cms page;
    - [ ] have a CMS apphook to integrate Lotus as a CMS page;
    - [x] perform again the admin override that seems overwritten by admin-style,
      currently it results on Article and Category change form in admin to lack of
      additional buttons for translation and preview;

.. todo::

    * [x] Wrongly pushed to my repo instead of the emencia one, move it then the git remotes;
    * [x] Include option values in default template;
    * [x] Enable django debug toolbar for development;
    * [~] Test coverage;
      * [x] Models;
      * [x] Factories;
      * [x] Plugin form;
      * [x] Plugin render (watch for performed sql queries);
    * [x] Categories choices with language in plugin admin form;
    * [ ] We could post-save clean category choices depending target language during
      plugin form save ?
    * [x] django debug toolbar must be conditionnated to its install and moved from
      ``[dev]`` requirement in a new extra requirement (like ``djdt`` or ``debug``);
    * [ ] Backport admin stylesheet fix to Lotus for django-admin-style compatibility
      since this is only about to push style rules inside selector
      ``.djangocms-admin-style.app-lotus #content ...``;

* Started with supports:

  * Python>=3.10;
  * Django>=4.2,<5.2;
  * DjangoCMS>=4.1.0;

* Adjusted requirements for Lotus, Django and Python supports;
* Added first working version for plugin "Article flux";
* Template for plugin "Article flux" include the Lotus article item template to list
  articles so the same look and feel is adopted;
* Included stylesheet patch (for django-admin-style) for Lotus admin category tree
  view. This may be temporary because Lotus may include patch in futur release. So for
  now the Lotus settings for admin form CSS have to be changed to use the right path: ::

    LOTUS_ADMIN_ALBUM_ASSETS["css"]["all"] = ("css/cmslotus-admin/lotus-admin.css",)
    LOTUS_ADMIN_ARTICLE_ASSETS["css"]["all"] = ("css/cmslotus-admin/lotus-admin.css",)
    LOTUS_ADMIN_CATEGORY_ASSETS["css"]["all"] = ("css/cmslotus-admin/lotus-admin.css",)

* Added 'django-debug-toolbar' to the development requirements;
* Added test coverage for ArticleFlux model, factory, form and plugin;


Version 0.1.0 - Unreleased
**************************

* First commit.
