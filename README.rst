====
Miko
====

.. image:: https://img.shields.io/pypi/v/miko.svg
        :target: https://pypi.python.org/pypi/miko

.. image:: https://img.shields.io/travis/haim0n/miko.svg
        :target: https://travis-ci.org/haim0n/miko

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

Usage
-----

* To check if any openstack project is using 'mario' library::

        $ miko --library mario

* To see additional information while running `miko` use the `--debug` flag::

        $ miko --library mario --debug

* To use your personal user::

        $ miko --library beautifulsoup4 --user <my_github_username>


Credits
-------

