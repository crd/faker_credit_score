# Contributing to faker-credit-score

Thanks for your interest! This project is small and friendly — contributions of all sizes are welcome, including first-time open source contributors.

## Getting started

1. Fork the repo and clone your fork
2. Install dependencies with [uv](https://docs.astral.sh/uv/):
   ```bash
   uv sync --dev
   ```
3. Run the tests:
   ```bash
   uv run pytest --cov=faker_credit_score
   ```

## Making changes

1. Create a branch from `develop` (not `main`)
2. Write tests for any new functionality — we maintain 100% coverage
3. Make sure all tests pass before submitting
4. Open a pull request against `develop`

## What we'd love help with

- **New credit score models** — if you know of a scoring model we're missing, add it to `credit_score_data` in `__init__.py`
- **Documentation** — examples, tutorials, or improving the README
- **Bug reports** — open an issue with steps to reproduce

## Code style

We use [Black](https://github.com/psf/black) for formatting. Keep things simple and consistent with existing code.

## Questions?

Open an issue — happy to help you find something to work on.
