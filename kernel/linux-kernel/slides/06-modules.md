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
# Inside /proc/modules and /sys/module

- `/proc/modules` lists loaded modules; each line has:
  - **name**, **size** in bytes, **refcount**, **dependencies**, **state** (`Live`, `Loading`,
    `Unloading`), and the **kernel address** of the module.
- `/sys/module/<name>/` exposes module attributes:
  - `parameters/` — one file per module parameter (writable if permitted);
  - `version/` — `MODULE_VERSION()` string;
  - `refcnt/` — current reference count;
  - `sections/` — section addresses (debugging).
- Built-in modules only appear in `/sys/module/` if they have a version or at least one parameter.

---
layout: default
---
# Module autoloading

- The kernel emits a **uevent** when a device is discovered; udev/mdev receives it through
  netlink and asks `modprobe` to load a matching driver.
- `MODULE_DEVICE_TABLE()` records device IDs in the module; `depmod` builds
  `/lib/modules/<version>/modules.alias` and `modules.dep`.
- `modprobe <module>` resolves dependencies and loads the module and its dependencies.
- `/etc/modprobe.d/*.conf` supplies options and aliases (`options`, `alias`, `blacklist`).
- Modules needed before the root filesystem is available must be in the **initramfs**; the rest
  can be loaded on demand from the root filesystem.

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
