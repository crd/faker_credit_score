faker_credit_score
==================

|pypi| |unix_build| |coverage| |license| |codacy| |black|

faker_credit_score is a community-created provider for the `Faker`_ test data
generator Python package.

This package provides fake credit score data for testing purposes. The most common non-industry specific credit scoring models are supported:

* FICO Score 8
* VantageScore 3.0
* FICO Score 10
* FICO Score 10 T
* Equifax Beacon 5.0
* Experian/Fair Isaac Risk Model V2SM
* TransUnion FICO Risk Score, Classic 04

Installation
------------

Install with pip:

.. code:: bash

    $ pip install faker-credit-score

Alternatively, install with setup.py:

.. code:: bash

    $ git clone https://github.com/crd/faker_credit_score.git
    $ cd faker_credit_score && python setup.py install

Usage
-----

From the Command Line
~~~~~~~~~~~~~~~~~~~~~

.. code:: bash

    $ faker credit_score -i faker_credit_score
    756

From within your Python Project
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Add the ``CreditScore`` Provider to your ``Faker`` instance:

.. code:: python

    from faker import Faker
    from faker_credit_score import CreditScore

    fake = Faker()
    fake.add_provider(CreditScore)

    fake.credit_score_name()
    # 'TransUnion FICO Risk Score, Classic 04'
    fake.credit_score_provider()
    # 'TransUnion'
    fake.credit_score()
    # 791

Contributing
------------

By all means, contribute! I'd be happy to work with any first-time open source contributors so please, don't be shy.

Testing
-------

Execute unit tests and calculate code coverage like so:

.. code:: bash

    $ coverage run -m unittest tests/*
    ..............
    ----------------------------------------------------------------------
    Ran 14 tests in 0.406s

    OK

    $ coverage report
    Name                             Stmts   Miss  Cover
    ----------------------------------------------------
    faker_credit_score/__init__.py      58      0   100%


.. |pypi| image:: https://img.shields.io/pypi/v/faker_credit_score.svg?style=flat-square&label=version
    :target: https://pypi.python.org/pypi/faker_credit_score
    :alt: Latest version released on PyPi

.. |unix_build| image:: https://img.shields.io/travis/crd/faker_credit_score/develop.svg?style=flat-square&label=unix%20build
    :target: http://travis-ci.org/crd/faker_credit_score
    :alt: Build status of the develop branch on Mac/Linux

.. |coverage| image:: https://img.shields.io/coveralls/crd/faker_credit_score/develop.svg?style=flat-square
    :target: https://coveralls.io/r/crd/faker_credit_score?branch=develop
    :alt: Test coverage

.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square
    :target: https://github.com/crd/faker_credit_score/blob/master/LICENSE
    :alt: BSD 3-Clause License

.. |codacy| image:: https://api.codacy.com/project/badge/Grade/accb555dd0ae4e9598333988d57487e7
    :target: https://www.codacy.com/manual/crd/faker_credit_score?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=crd/faker_credit_score&amp;utm_campaign=Badge_Grade
    :alt: Codacy code quality grade

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg?style=flat-square
    :target: https://github.com/ambv/black
    :alt: Black code formatter

.. _Faker: https://github.com/joke2k/faker
