djtranslationchecker
====================

Checks your Django message files for missing / fuzzy translations

Usage
-----

Add ``djtranslationchecker`` to your ``INSTALLED_APPS``, then::

    $ python manage.py translationchecker

This will check all ``.po`` files in subdirectories of your ``INSTALLED_APPS``.
If any of them contain missing translations or fuzzy translations, the command will exit with an error.
