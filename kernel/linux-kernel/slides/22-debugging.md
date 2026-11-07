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
# Dynamic debug in practice

- `CONFIG_DYNAMIC_DEBUG` compiles `pr_debug()` / `dev_dbg()` calls but leaves them disabled.
- Control file: `/proc/dynamic_debug/control` (also available through debugfs).
- Enable by matching source file, function, line, module or format string:

```console
$ echo 'file foo.c line 42 +p' > /proc/dynamic_debug/control
$ echo 'module foo +p' > /proc/dynamic_debug/control
$ echo 'func foo_probe +p' > /proc/dynamic_debug/control
```

- `+p` enables, `-p` disables; `=p` sets the flags exactly.
- Enable at boot with `dyndbg="file foo.c +p"` on the kernel command line.
- Check the current state: `grep foo /proc/dynamic_debug/control`.

---
layout: default
---
# DebugFS

- A virtual filesystem to export debugging info to user space (`CONFIG_DEBUG_FS`).
- Mount: `sudo mount -t debugfs none /sys/kernel/debug`.
- `debugfs` is a pseudo filesystem on VFS: `debugfs_create_*()` installs dentries and file
  operations; see the **VFS and page cache** chapter.

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
# Decoding an oops

- An oops prints a register dump, a stack trace and the faulting instruction (RIP/EIP).
- Build the kernel with `CONFIG_DEBUG_INFO=y` and keep `vmlinux`.
- With debug info:

```console
$ gdb vmlinux
(gdb) list *0xffffffff81234567
```

- Without debug info, use the symbol+offset from the oops:

```console
$ ./scripts/faddr2line vmlinux foo_driver+0x1a/0x40
```

- `CONFIG_KALLSYMS` / `CONFIG_KALLSYMS_ALL` improve symbol resolution.
- `scripts/decode_stacktrace.sh` resolves a pasted stack trace against `vmlinux`.

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
# Tracing: ftrace, perf and BPF

- **ftrace** — built-in tracer (`CONFIG_FUNCTION_TRACER`, `CONFIG_FTRACE`):
  - `/sys/kernel/tracing/` (or `/sys/kernel/debug/tracing/`);
  - function tracer, function_graph, event tracers, `trace-cmd`.
- **perf** — sampling and hardware/software events:
  - `perf top`, `perf record` / `perf report`, `perf trace`.
- **BPF** — programmable tracing with kprobes, tracepoints and `bpftrace`:

```console
$ bpftrace -e 'kprobe:do_sys_open { printf("%s\n", comm); }'
```

- Use ftrace for "what is the kernel doing?" and perf/BPF for latency and frequency analysis.
- `trace_printk()` is only for early debugging; remove it before upstreaming.

---
layout: default
---
# Reporting bugs

- On a vendor kernel, contact the vendor (the community has less interest in custom kernels).
- Otherwise, reproduce on the **latest kernel** first; investigate (`Documentation/admin-guide/
  bug-bisect.rst`); search mailing-list archives.
- Report to the subsystem mailing list or the maintainer (`MAINTAINERS` file), with as many
  useful details as possible.
