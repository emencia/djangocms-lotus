
=========
Changelog
=========

Version 0.2.0 - 2025/01/15
**************************

* Started with supports:

  * Python>=3.9;
  * Django>=4.2;
  * DjangoCMS>=4.1.0;
  * Lotus>=0.9.0;

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


Version 0.1.0 - 2025/01/09
**************************

First commit, no package was released for this version.
