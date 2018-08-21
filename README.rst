faker_credit_score
==================

|pypi| |unix_build| |coverage| |license|

faker_credit_score is a community-created provider for the `Faker`_ Python package.

This package provides fake credit score data for testing purposes:

* FICO Score 8
* Equifax Beacon 5.0
* Experian/Fair Isaac Risk Model V2SM
* TransUnion FICO Risk Score, Classic 04

Usage
-----

Install with pip:

.. code:: bash

    pip install faker_credit_score

Or install with setup.py

.. code:: bash

    git clone https://github.com/crd/faker_credit_score.git
    cd faker_credit_score && python setup.py install

Add the ``CreditScore`` Provider to your ``Faker`` instance:

.. code:: python

    from faker import Faker
    from faker_credit_score import CreditScore

    fake = Faker()
    fake.add_provider(CreditScore)

    fake.credit_score()
    791
    fake.credit_score_provider()
    'TransUnion'
    fake.credit_score_name()
    'TransUnion FICO Risk Score, Classic 04'


.. |pypi| image:: https://img.shields.io/pypi/v/faker_credit_score.svg?style=flat-square&label=version
    :target: https://pypi.python.org/pypi/faker_credit_score
    :alt: Latest version released on PyPi

.. |unix_build| image:: https://img.shields.io/travis/crd/faker_credit_score/master.svg?style=flat-square&label=unix%20build
    :target: http://travis-ci.org/crd/faker_credit_score
    :alt: Build status of the master branch on Mac/Linux

.. |coverage| image:: https://img.shields.io/coveralls/crd/faker_credit_score/master.svg?style=flat-square
    :target: https://coveralls.io/r/crd/faker_credit_score?branch=master
    :alt: Test coverage

.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square
    :target: https://github.com/crd/faker_credit_score/blob/master/LICENSE
    :alt: BSD 3-Clause License

.. _Faker: https://github.com/joke2k/faker
