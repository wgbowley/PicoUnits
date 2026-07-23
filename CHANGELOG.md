# Changelog

All notable changes to PicoUnits will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

*(ISO-DATE is used for all updates)*

## [1.0.6] - 2026-07-24

### Added
- `.picounits` configuration file inheritance for base symbols and order
- Unit tests for extensions: construction, deserialization, syntax
- New `extensions\core` module structure with `construction.py`, `deserialization.py`, `syntax.py`
- Validation for derived unit imports (only one `.ut` file allowed)
- lowercase names for all constant prefixes, dimensions and quality

### Changed
- Major refactor of `DynamicLoader` with identity behavior
- Refactored `Parser` class for better maintainability / traceability
- Improved module search path for users
- Renamed `unit_validator` module to `expects`
- Better error messages for parsing failures
- Improved prefix extraction from `prefix(unit)` syntax
- Enhanced parentheses handling for quantities

### Fixed
- Reciprocal unit scaling error
- Squared scaling for length (instead of linear scaling)
- Area notion inconsistencies
- Missing format key warning handling
- Column-wise prefix extraction for lists

### Documentation
- Improved logo with dark/light mode support
- New color palettes
