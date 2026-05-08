# Changelog

## [0.7.2](https://github.com/EIGSEP/casperfpga/compare/v0.7.1...v0.7.2) (2026-05-08)


### Bug Fixes

* drop stale future dep, relax redis cap to &lt;8 ([455a950](https://github.com/EIGSEP/casperfpga/commit/455a9502dab6585aefc4071a3ae9e143697a4930))

## [0.7.1](https://github.com/EIGSEP/casperfpga/compare/v0.7.0...v0.7.1) (2026-05-02)


### Bug Fixes

* add backports.ssl_match_hostname for tornado 4.x on Python 3.12 ([7fee9cd](https://github.com/EIGSEP/casperfpga/commit/7fee9cd94879a24670ea0e3d8fd2a7b09134fcae))
* bump katcp&gt;=0.9.3 for Python 3.10+ collections.abc compat ([59a50f0](https://github.com/EIGSEP/casperfpga/commit/59a50f0490df457d506c4f80bbb3986d67ea6582))
* pin tftpy&lt;=0.8.0 to avoid SNAP TAPCP write timeouts ([#7](https://github.com/EIGSEP/casperfpga/issues/7)) ([8d06b54](https://github.com/EIGSEP/casperfpga/commit/8d06b54f0cccd6cde061113060f50b695b1e05e8))
* replace Thread.setDaemon/isAlive for Python 3.13 compatibility ([03ee97a](https://github.com/EIGSEP/casperfpga/commit/03ee97aa797016a275160b88a6658887e8055b75))
* support ref=None in new SnapAdc constructor for external clocks ([fc5a5d3](https://github.com/EIGSEP/casperfpga/commit/fc5a5d3eaff1c250b6b1a83d3b9cdbf4a07e14e8))
* update Python version classifiers to match CI matrix ([902766c](https://github.com/EIGSEP/casperfpga/commit/902766c2c7933d4e73cc07db13e8660cf66cbf35))


### Documentation

* add claude.md ([13c8127](https://github.com/EIGSEP/casperfpga/commit/13c81272bba91d97f3986f867c8f96ceeb8ef616))
