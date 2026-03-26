# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project context

This is **EIGSEP's maintenance fork** of [casper-astro/casperfpga](https://github.com/casper-astro/casperfpga), a Python library for interacting with CASPER FPGA hardware (ROACH, SKARAB, SNAP, etc.). The upstream default branch is `py38`; ours is `main`.

**Maintenance philosophy:** The hardware is deprecated. The goal is *not* to add features but to keep the software working as Python and dependency versions evolve. Stay as close to upstream as possible — the community tests that code on real hardware. Changes should be minimal and focused on compatibility fixes (Python EOL migrations, dependency updates, deprecation fixes).

## Build and test commands

```bash
# Install from source (editable)
pip install -e .[test]

# Run full test suite
pytest

# Run a single test file
pytest tests/test_utils.py

# Run a single test
pytest tests/test_utils.py::test_function_name -v
```

There is no linter or formatter configured. CI runs pytest across Python 3.9, 3.10, and 3.11.

## Package layout

The directory structure does **not** follow the standard `src/` layout convention. Instead, `src/` *is* the `casperfpga` package (mapped via `package_dir` in `setup.py`):

```
src/           → casperfpga        (main package)
progska/       → casperfpga.progska (C extension for SKARAB programming)
debug/         → casperfpga.debug
scripts/       → CLI entry points (casperfpga_program.py, etc.)
tests/         → pytest suite
```

## Architecture

**CasperFpga** (`src/casperfpga.py`) is the central class. It auto-detects hardware type and selects the appropriate transport:

- **Transports** handle communication with different hardware platforms: `KatcpTransport` (ROACH), `SkarabTransport` (SKARAB — largest module at ~4500 lines), `TapcpTransport` (TAPCP), plus `AlveoTransport`, `ItpmTransport`, PCIe transports, and `DummyTransport` for testing.

- **Device classes** (all inherit from `Memory` base in `src/memory.py`) represent on-FPGA resources: `Register`, `Snap`, `Sbram`, `Qdr`, `TenGbe`, `FortyGbe`, `OneHundredGbe`. These are auto-created when an FPG file is programmed.

- **ADC classes**: `SnapAdc`, `SkarabAdc`, `KatAdc`, `Adc_4X16G_ASNT`, `RFDC` — each ~800-1000 lines with hardware-specific calibration routines.

- **`skarab_definitions.py`** (~2400 lines) contains register/command constants for SKARAB protocol — treat as reference data, not logic.

- **`utils.py`** handles FPG file parsing (gzipped metadata + bitstream) and host resolution.

## Key conventions

- The C extension (`progska/`) compiles during install. If you only need to test Python code, the import smoke tests in `tests/test_imports.py` cover module availability.
- Test data lives in `tests/data/` and uses `pytest-datadir` for fixture paths.
- `setup.cfg` excludes `debug/` from pytest collection (`norecursedirs = debug`).
