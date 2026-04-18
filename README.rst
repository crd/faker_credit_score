faker_credit_score
==================

*Stop hardcoding 720 in your tests.*

|pypi| |status| |coverage| |license|

A `Faker`_ provider that generates realistic credit scores across 10 industry
scoring models — FICO 8, VantageScore, Equifax Beacon, and more. Constrain by
tier, get real bureau names, and test the paths that actually matter.

Why this exists
---------------

Hardcoding ``credit_score = 720`` in your fixtures doesn't test anything. You
don't know if that's "good" for FICO 8 or "fair" for Equifax Beacon 5.0. And
``random.randint(300, 850)`` gives you numbers that don't map to any real model.

If you're building a lending flow, an insurance quote engine, or anything that
branches on creditworthiness — you need scores that come from the right ranges,
tied to real bureau names, in the right tiers.

**Before:**

.. code:: python

    # What does 720 even test? Which model? Which tier?
    user["credit_score"] = 720

**After:**

.. code:: python

    fake.credit_score(tier="poor")           # 542 — test the denial path
    fake.credit_score(tier="exceptional")    # 831 — test the approval path

    result = fake.credit_score_full("fico5")
    # CreditScoreResult(name='Equifax Beacon 5.0', provider='Equifax', score=687)

Installation
------------

.. code:: bash

    pip install faker-credit-score

Two lines to add it to your existing Faker setup:

.. code:: python

    from faker import Faker
    from faker_credit_score import CreditScore

    fake = Faker()
    fake.add_provider(CreditScore)

Usage
-----

Generate Scores
~~~~~~~~~~~~~~~

.. code:: python

    fake.credit_score()
    # 791

    fake.credit_score("fico5")
    # 687

    fake.credit_score_name()
    # 'TransUnion FICO Risk Score, Classic 04'

    fake.credit_score_provider()
    # 'TransUnion'

Full Credit Score Result
~~~~~~~~~~~~~~~~~~~~~~~~

Returns a ``CreditScoreResult`` namedtuple with ``name``, ``provider``, and
``score`` fields:

.. code:: python

    fake.credit_score_full()
    # CreditScoreResult(name='FICO Score 8', provider='Equifax', score=791)

    name, provider, score = fake.credit_score_full("fico5")

Also works from the command line:

.. code:: bash

    $ faker credit_score -i faker_credit_score
    756

    $ faker credit_score_full -i faker_credit_score
    Equifax Beacon 5.0
    Equifax
    687

Credit Score Tiers
~~~~~~~~~~~~~~~~~~

Generate scores constrained to a tier, or classify existing scores:

.. code:: python

    fake.credit_score(tier="poor")
    # 542

    fake.credit_score(tier="exceptional")
    # 831

    fake.credit_score_tier()
    # 'good'

    fake.credit_score_tier(score=720)
    # 'good'

Supported tiers: ``poor`` (300-579), ``fair`` (580-669), ``good`` (670-739),
``very_good`` (740-799), ``exceptional`` (800-850).

Supported Models
~~~~~~~~~~~~~~~~

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

Contributing
------------

Contributions are welcome, including from first-time open source contributors.
See `CONTRIBUTING.md <CONTRIBUTING.md>`_ for setup instructions and ideas.

Testing
-------

.. code:: bash

    $ pytest --cov=faker_credit_score
    ..............................
    30 passed

    $ coverage report
    Name                             Stmts   Miss  Cover
    ----------------------------------------------------
    faker_credit_score/__init__.py      57      0   100%

.. |pypi| image:: https://img.shields.io/pypi/v/faker-credit-score.svg?style=flat-square
   :target: https://pypi.org/project/faker-credit-score/
   :alt: Latest version released on PyPI

.. |status| image:: https://github.com/crd/faker_credit_score/actions/workflows/release.yml/badge.svg?style=flat-square
   :target: https://github.com/crd/faker_credit_score/actions/workflows/release.yml
   :alt: Release workflow status

.. |coverage| image:: https://coveralls.io/repos/github/crd/faker_credit_score/badge.svg?branch=develop&style=flat-square
    :target: https://coveralls.io/github/crd/faker_credit_score?branch=develop
    :alt: Test coverage

.. |license| image:: https://img.shields.io/badge/License-BSD%203--Clause-blue.svg?style=flat-square
    :target: https://github.com/crd/faker_credit_score/blob/master/LICENSE
    :alt: BSD 3-Clause License

.. _Faker: https://github.com/joke2k/faker
