.. image:: https://img.shields.io/badge/licence-AGPL--3-blue.svg
   :target: http://www.gnu.org/licenses/agpl-3.0-standalone.html
   :alt: License: AGPL-3

===============
Improved Search
===============

This module extends the search functionality to add simple shortcuts for
more complex search conditions.

At this moment only a type of fuzzy search is implemented:
It matches records containing all the words in the expression searched for,
regardless of their order.

It is only available when specifically enabled,
and is only implemented for the "contains" (`ilike`) operation.


Installation
============

No specific requirements.


Configuration
=============

To enable this feature on a view, the `{search_fuzzy_enable=True}` key
must be set in the Context.
Ususally this would be done on the Window Action responsible for opening
the views where we want to enable this behaviour.


Usage
=====

Once enabled, on the view search box (list or kanban views), type words
separated with spaces and the records containing all the typed
words will be matched.

For example, in a demo database, on the Contacts / Customers try searching
for " brown john" with this feature enabled, and the result "John M. Brown"
will be seen.


.. image:: https://odoo-community.org/website/image/ir.attachment/5784_f2813bd/datas
   :alt: Try me on Runbot
   :target: https://runbot.odoo-community.org/runbot/149/8.0

.. repo_id is available in https://github.com/OCA/maintainer-tools/blob/master/tools/repos_with_ids.txt
.. branch is "8.0" for example

Known issues / Roadmap
======================

There are more search improvements to implement:
* Support operators, such as ">", "<", ".." (between interval), etc.
* Support smart date tokens, such as "t" for today, "m" for current month, "ytd" for year to date.

The above can be implemented for all models, not requiring to be enabled by a context flag.

Bug Tracker
===========

Bugs are tracked on `GitHub Issues
<https://github.com/OCA/serevr-tools/issues>`_. In case of trouble, please
check there if your issue has already been reported. If you spotted it first,
help us smashing it by providing a detailed and welcomed feedback.

Credits
=======

Images
------

* Odoo Community Association: `Icon <https://github.com/OCA/maintainer-tools/blob/master/template/module/static/description/icon.svg>`_.

Contributors
------------

* Daniel Reis <https://github.com/dreispt>

Maintainer
----------

.. image:: https://odoo-community.org/logo.png
   :alt: Odoo Community Association
   :target: https://odoo-community.org

This module is maintained by the OCA.

OCA, or the Odoo Community Association, is a nonprofit organization whose
mission is to support the collaborative development of Odoo features and
promote its widespread use.

To contribute to this module, please visit https://odoo-community.org.
