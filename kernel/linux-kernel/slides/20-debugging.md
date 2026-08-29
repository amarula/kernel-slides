---
layout: section
hideInToc: true
---
# Kernel debugging

---
layout: default
---
# Logging: printk, pr_*, dev_*

- `printk()` — works in all contexts; log levels 0 (emergency) to 7 (debug); `*_ratelimited()`
  variants; not recommended for upstream contributions.
- `pr_*()` — `pr_emerg()`, `pr_alert()`, `pr_crit()`, `pr_err()`, `pr_warn()`, `pr_notice()`,
  `pr_info()`, `pr_cont()`, `pr_debug()`. Prefix with `#define pr_fmt(fmt) "foo: " fmt`.
- `dev_*()` — device-name prefix, take a `struct device *` first arg; use in drivers.
- Extra format specifiers: `%p` (hashed pointer), `%px`, `%pK`, `%pOF` (DT node), `%pr`
  (resource), `%pa` (physical address), `%pe` (error pointer).
- `pr_debug()`/`dev_dbg()` compiled only with `DEBUG` or `CONFIG_DYNAMIC_DEBUG`
  (`/proc/dynamic_debug/control`). Loglevel via `loglevel=` or `/proc/sys/kernel/printk`.

---
layout: default
---
# DebugFS

- A virtual filesystem to export debugging info to user space (`CONFIG_DEBUG_FS`).
- Mount: `sudo mount -t debugfs none /sys/kernel/debug`.

```c
struct dentry *debugfs_create_dir(const char *name, struct dentry *parent);
struct dentry *debugfs_create_u8(const char *name, mode_t mode,
                                 struct dentry *parent, u8 *value);
struct dentry *debugfs_create_blob(const char *name, mode_t mode,
                                   struct dentry *parent,
                                   struct debugfs_blob_wrapper *blob);
/* also debugfs_create_file() for custom/writable files */
```

---
layout: default
---
# kgdb, JTAG, early traces

- **Magic SysRq**: debug/rescue commands even when the kernel is in trouble (`h` help, `s` sync,
  `b` reboot, `w`/`t` stacks). Embedded: send a break char, then the command key.
- **kgdb** (`CONFIG_KGDB`): run the kernel under gdb over a serial line (`kgdboc=ttyS0,115200`,
  `kgdbwait`, then `arm-linux-gdb ./vmlinux` → `target remote /dev/ttyS0`).
- **JTAG**: gdb-compatible dongles directly, or via **OpenOCD**.
- **Early traces**: if it breaks before the console is up (`CONFIG_DEBUG_LL` + `earlyprintk` on
  ARM, or `CONFIG_SERIAL_EARLYCON`).
- Tips: enable `CONFIG_KALLSYMS_ALL`, `CONFIG_DEBUG_INFO`, `CONFIG_DEBUG_DRIVER`.

---
layout: default
---
# Reporting bugs

- On a vendor kernel, contact the vendor (the community has less interest in custom kernels).
- Otherwise, reproduce on the **latest kernel** first; investigate (`Documentation/admin-guide/
  bug-bisect.rst`); search mailing-list archives.
- Report to the subsystem mailing list or the maintainer (`MAINTAINERS` file), with as many
  useful details as possible.
