
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
      * [ ] Plugin form;
      * [ ] Plugin render (watch for performed sql queries);
    * [ ] Categories choices with language in plugin admin form;
    * [ ] We could post-save clean category choices depending target language during
      plugin form save ?
    * [ ] django debug toolbar must be conditionnated to its install and moved from
      ``[dev]`` requirement in a new extra requirement (like ``djdt`` or ``debug``);

* Started with supports:

  * Python>=3.10;
  * Django>=4.2,<5.2;
  * DjangoCMS>=4.1.0;

* Adjusted requirements for Lotus, Django and Python supports;
* Added first working version for plugin "Article flux";
* Included stylesheet patch (for django-admin-style) for Lotus admin category tree view;
* Added 'django-debug-toolbar' to the development requirements;
* Added test coverage for models, factories, forms;


Version 0.1.0 - Unreleased
**************************

* First commit.
