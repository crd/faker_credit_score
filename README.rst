faker_credit_score
==================

|pypi| |status| |license| |black|

faker_credit_score is a community-created provider for the `Faker`_ test data
generator Python package.

This package provides fake credit score data for testing purposes. The most common non-industry specific credit scoring models are supported:

* FICO Score 8
* FICO Score 9
* FICO Score 10
* FICO Score 10 T
* VantageScore 3.0
* VantageScore 4.0
* UltraFICO
* Equifax Beacon 5.0
* Experian/Fair Isaac Risk Model V2SM
* TransUnion FICO Risk Score, Classic 04

Installation
------------

Install with pip (this will also install `Faker`_ if you don't already have it):

.. code:: bash

    $ pip install faker-credit-score

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

    $ pytest --cov=faker_credit_score
    ..............
    ----------------------------------------------------------------------
    Ran 14 tests in 0.406s

    OK

    $ coverage report
    Name                             Stmts   Miss  Cover
    ----------------------------------------------------
    faker_credit_score/__init__.py      58      0   100%

.. |pypi| image:: https://img.shields.io/pypi/v/faker-credit-score.svg
   :target: https://pypi.org/project/faker-credit-score/
   :alt: Latest version released on PyPI

.. |status| image:: https://github.com/crd/faker_credit_score/actions/workflows/release.yml/badge.svg
   :target: https://github.com/crd/faker_credit_score/actions/workflows/release.yml
   :alt: Release workflow status (tests + publish)

.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg
   :target: https://opensource.org/licenses/BSD-3-Clause
   :alt: BSD 3-Clause License

.. |black| image:: https://img.shields.io/badge/code%20style-black-000000.svg
   :target: https://github.com/psf/black
   :alt: Black code formatter

.. _Faker: https://github.com/joke2k/faker
