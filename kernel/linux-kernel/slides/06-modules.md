---
layout: section
hideInToc: true
---
# Kernel modules

---
layout: default
---
# Module utilities

- `modinfo <module>` — info about a module without loading it (parameters, license,
  description, dependencies).
- `sudo insmod <module_path>.ko` — load a module (full path required).
- `sudo modprobe <top_module>` — load a module **and its dependencies**; looks in
  `/lib/modules/<version>/`.
- `lsmod` — list loaded modules (compare with `/proc/modules`).
- `sudo rmmod <module>` / `sudo modprobe -r <module>` — remove a module (only if unused).

> When loading fails, `insmod` rarely gives enough details — check `dmesg`.

---
layout: default
---
# Passing parameters to modules

- Find available parameters: `modinfo usb-storage`.
- Through `insmod`: `sudo insmod ./usb-storage.ko delay_use=0`.
- Through `modprobe`: put `options usb-storage delay_use=0` in `/etc/modprobe.d/`.
- Through the kernel command line (when built statically): `usb-storage.delay_use=0`.
- Current values: `/sys/module/<name>/parameters/` (one file per parameter; writable if the
  module allows it).
