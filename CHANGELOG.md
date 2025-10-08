Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.5.2] - 2025-10-08

Minor housekeeping, bringing documentation and pipelines up to standard.

### Added

- Introduced RELEASING.rst

### Changed

- Fixed README badges
- Created a Github Action for test coverage
- Eliminated unused references to travis

## [0.5.1] - 2025-09-28

### Added

- Added support for credit score FICO Score 9
- Added support for redit score VantageScore 4.0
- Added support forcredit score UltraFICO

### Changed

- Migrated from [pipenv](https://pipenv.pypa.io/) to [UV](https://docs.astral.sh/uv/)
- Transitioned to Github Actions for build and release
