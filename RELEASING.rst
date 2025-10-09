# Release Process (hatch-vcs + uv)

## Overview

This project uses **tag-driven versioning** via `hatch-vcs`: the package version is **derived from the Git tag** on the commit you release. You **do not** edit a static `version = ...` in `pyproject.toml`. During build/install, Hatch writes a generated version file at `faker_credit_score/_version.py`; do **not** commit it.

## Prerequisites

* GitHub Actions workflow `.github/workflows/release.yml` present on the commit you will tag.
* Repo secrets:

  * `TEST_PYPI_API_TOKEN` (TestPyPI “API token” value, starts with `pypi-`)
  * `PYPI_API_TOKEN` (PyPI “API token” value, starts with `pypi-`)
* GitHub Environments:

  * `testpypi` (no approvals needed)
  * `pypi` (protected; require reviewers for promotion)

## Branching model

* Default integration branch: `develop`
* Protected release branch: `master`
* Feature work: short-lived branches off `develop`

## Feature workflow

1. Create a feature branch off `develop`::

   git checkout -b feature/<slug> origin/develop

2. Commit code + tests. Open a PR **into** `develop`. No version edits.

## Cutting a release (e.g., 0.5.1)

1. **Sync & branch from develop**::

   git fetch origin --tags
   git checkout -b release/0.5.1 origin/develop

2. **Finalize docs/CHANGELOG** on the release branch, then push::

   git commit -am "chore(release): prepare 0.5.1" || true
   git push -u origin release/0.5.1

3. **Open a PR**: `release/0.5.1` → `master`. Merge when green (this ensures the workflow file is in the commit you'll tag).

4. **Tag on master** (this sets the package version via hatch-vcs)::

   git checkout master
   git pull
   git tag v0.5.1
   git push origin v0.5.1

5. **Wait for CI** to:

   * run tests on a Python matrix,
   * build artifacts,
   * publish to **TestPyPI** automatically.

6. **Verify the TestPyPI install** locally (allow deps from PyPI)::

   uv venv -q && source .venv/bin/activate
   uv pip install 
   --index-url [https://test.pypi.org/simple/](https://test.pypi.org/simple/) 
   --extra-index-url [https://pypi.org/simple](https://pypi.org/simple) 
   --index-strategy unsafe-best-match 
   "faker-credit-score==0.5.1"

   python - <<'PY'
   from faker import Faker
   from faker_credit_score import CreditScore
   f = Faker(); f.add_provider(CreditScore)
   print("ok:", bool(f.credit_score()))
   PY

7. **Promote to PyPI**: In GitHub → *Actions* → *Release* run for tag `v0.5.1` → approve the **promote-pypi** job in the protected `pypi` environment.

8. **Sync branches** back::

   git checkout develop
   git pull
   git merge --no-ff origin/master
   git push

## Hotfix workflow (e.g., 0.5.2)

1. Branch from `master`::

   git checkout -b hotfix/0.5.2 origin/master

2. Commit the fix + tests, push, open PR **into** `master` and merge.

3. Tag & release::

   git checkout master && git pull
   git tag v0.5.2
   git push origin v0.5.2

4. CI publishes to TestPyPI → verify locally → approve promotion to PyPI.

5. Back-merge `master` → `develop`::

   git checkout develop && git pull
   git merge --no-ff origin/master
   git push

## Pre-releases (RCs)

* Create a release branch off `develop` and tag RCs directly (no version edits)::

  git tag v0.6.0rc1
  git push origin v0.6.0rc1

* CI will publish the RC to TestPyPI. Iterate with `v0.6.0rc2`, etc.

* When stable, tag the final::

  git tag v0.6.0
  git push origin v0.6.0

## Notes on the generated version file

* `faker_credit_score/_version.py` is **generated** by Hatch's VCS build hook during build/install; don't commit it.
* At runtime you may access the version either by::

  from faker_credit_score._version import **version**

  or via package metadata (robust in editable installs)::

  from importlib.metadata import version
  version("faker-credit-score")

## Manual build/publish (local)

If you need to publish manually from your machine (not typical once CI is set up):

Build both sdist & wheel::

uv build --sdist --wheel

Publish to **TestPyPI** (using the named index in `pyproject.toml`)::

export UV_PUBLISH_TOKEN="pypi-...testpypi..."
uv publish --index testpypi --token "$UV_PUBLISH_TOKEN"

Publish to **PyPI** (only after testing)::

export UV_PUBLISH_TOKEN="pypi-...pypi..."
uv publish --token "$UV_PUBLISH_TOKEN"

Automatic branch sync (master → develop)
-------------------------------------

After a successful tagged release (normal or hotfix), the CI will automatically open a pull request from ``master`` into ``develop`` to ensure the development line includes the exact release commit(s) and workflow changes.

What to do:
- Navigate to the PR titled ``merge: back-merge release <tag> from master into develop``.
- If conflicts exist, resolve them in the PR.
- Merge the PR once checks pass.

Rationale:
- Normal releases are cut from ``develop`` and merged into ``master``; tagging and publishing happen on ``master``. The back-merge PR ensures ``develop`` stays aligned post-release.
- Hotfixes are cut from ``master``; tagging/publishing occur on ``master``. The same back-merge PR brings the hotfix back into ``develop``.

Manual fallback (only if CI cannot open the PR):
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If CI fails to create the PR, open one manually:

- Base: ``develop``  
- Compare: ``master``  
- Title: ``merge: back-merge release <tag> from master into develop``

If you must do it locally (rare):

.. code-block:: bash

   git fetch origin --tags
   git switch -c sync/master-into-develop origin/develop
   git merge origin/master           # resolve conflicts if any
   git push -u origin sync/master-into-develop

Then open a PR from ``sync/master-into-develop`` to ``develop`` and merge.

## Troubleshooting

* **Resolver says version not found on TestPyPI**: force a fresh index view or allow multi-index selection::

  uv cache clean faker-credit-score
  uv pip install --refresh 
  --index-url [https://test.pypi.org/simple/](https://test.pypi.org/simple/) 
  --extra-index-url [https://pypi.org/simple](https://pypi.org/simple) 
  --index-strategy unsafe-best-match 
  "faker-credit-score==X.Y.Z"

* **Actions error “No virtual environment found”**: ensure the test job uses `uv sync` (creates `.venv`) and tests with `uv run pytest -q`.

* **Workflows didn't run on tag**: confirm the tag was pushed on a commit **that already contains** `.github/workflows/release.yml` (merge your release PR to `master` before tagging).

## Compatibility & build environment

* Package is pure-Python (`py3-none-any`); build interpreter version does not constrain wheel compatibility.
* CI tests on a matrix (e.g., 3.9-3.13); **publish jobs** build from a pinned, boringly-stable Python (e.g., 3.11) to avoid day-0 ecosystem surprises.

