====
Miko
====

.. image:: https://img.shields.io/pypi/v/miko.svg
        :target: https://pypi.python.org/pypi/miko

.. image:: https://img.shields.io/travis/abregman/miko.svg
        :target: https://travis-ci.org/abregman/miko

.. image:: https://readthedocs.org/projects/miko/badge/?version=latest
        :target: https://readthedocs.org/projects/miko/?badge=latest
        :alt: Documentation Status


Get a list of OpenStack project's library requirements

* Free software: ISC license
* Documentation: https://miko.readthedocs.org.


Installation
------------
* Clone the repo: ``git@github.com:bregman-arie/miko.git``
* Install pip: ``sudo dnf install -y python-pip``
* Change working dir into the cloned project's root: ``cd miko``
* Install the package: ``sudo python setup.py install``

Uninstall
---------
``sudo pip uninstall miko``


Usage
-----

* To check if any openstack project is using 'mario' library::

        $ miko --library mario

* To see additional information while running `miko` use the `--debug` flag::

        $ miko --library mario --debug

* To use your personal user::

        $ miko --library beautifulsoup4 --user <my_github_username>


TODO
----
* Addition of an offline mode (potentialy to sqlite db).
        * add relational db capabilities to user (top, references etc).
* Parsing of each project's structure, to avoid 404 errors on invalid requirements.
* Further performance increase for initial data fetching. 

Credits
-------

