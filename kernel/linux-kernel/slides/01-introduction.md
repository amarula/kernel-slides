---
layout: section
hideInToc: true
---
# Linux kernel introduction

---
layout: default
---
# Origin

- The Linux kernel was created as a hobby in **1991** by Finnish student **Linus Torvalds**.
  - Linux quickly became the kernel of choice for free-software operating systems.
- Torvalds managed to create a large, dynamic developer and user community around Linux.
- Today, about **2000+ people** contribute to each kernel release, individuals and companies,
  big and small.

---
layout: default
---
# Linux kernel in the system

<div style="text-align:center;">
  <img src="/images/kernel-in-system.svg" style="background:white; border-radius:14px; padding:10px; max-height:400px; max-width:88%;" />
</div>

---
layout: default
---
# Linux kernel main roles

- **Manage all hardware resources**: CPU, memory, I/O.
- Provide a set of **portable, architecture- and hardware-independent APIs** so that user-space
  applications and libraries can use the hardware resources.
- Handle **concurrent access** to hardware resources from different applications.
  - Example: a single network interface is used by many applications through multiple network
    connections; the kernel "multiplexes" the hardware resource.

---
layout: default
---
# System calls

- The main interface between the kernel and user space is the set of **system calls**.
- About **400 system calls** provide the main kernel services:
  - File and device operations, networking, inter-process communication, process management,
    memory mapping, timers, threads, synchronization primitives…
- The system call interface is wrapped by the **C library**; applications normally never make a
  system call directly, but use the corresponding C library function.

---
layout: default
hideInToc: true
---
# System calls

<div style="text-align:center;">
  <img src="/images/system-call.svg" style="background:white; border-radius:14px; padding:10px; max-height:420px; max-width:82%;" />
</div>

---
layout: default
---
# Pseudo filesystems

- Linux exposes system and kernel information in user space through **pseudo filesystems**
  (sometimes called virtual filesystems).
- They let applications see directories and files that exist on no real storage — they are created
  and updated on the fly by the kernel.
- The two most important are:
  - **`proc`** (`/proc`): OS-related information (processes, memory management parameters…).
  - **`sysfs`** (`/sys`): the system represented as a tree of devices connected by buses.

---
layout: default
---

# The /proc pseudo filesystem

- A pseudo filesystem, **real-time**, residing in virtual memory.
- Tracks the processes running on the machine and the state of the system.
- Recreated on every boot; highly dynamic — its size is `0` and its last-modification time is the
  last boot time.
- Its contents are read by utilities like `top`, `ps`, `lspci`, `dmesg`, …

---
layout: default
hideInToc: true
---

# Key files in /proc

- `buddyinfo` — number of free areas of each order for the buddy allocator.
- `cmdline` — the kernel command line.
- `cpuinfo` — information about the processor(s).
- `devices` — device drivers configured into the running kernel (char and block).
- `interrupts` — number of interrupts per IRQ line.
- `iomem` / `ioports` — current memory / I/O-port map of the system's devices.
- `meminfo` — RAM utilization. `modules` — loaded modules. `mounts` — mounts in use.
- `loadavg` — load average (used by `top`, `htop`).

---
layout: default
hideInToc: true
---

# /proc/&lt;pid&gt; and /proc/sys

- Each numbered directory in `/proc` is a running process:
  - `cmdline` — the command line used to invoke it.
  - `cwd` / `exe` / `root` — symlinks to the working dir, executable, and root.
  - `environ` — process environment variables.
  - `fd` — the process's open file descriptors.
  - `maps` — parts of the address space mapped to a file. `status` — process info.
- `/proc/sys` — tweak kernel parameters at runtime (`echo` to change; lost on reboot):
  - `/proc/sys/kernel/printk` — kernel log level.
  - `/proc/sys/net/ipv4/ip_forward` — enable IP forwarding (`0` → `1`).
  - `/proc/sys/vm` — virtual-memory subsystem tunables.

---
layout: default
hideInToc: true
---

# The sys pseudo filesystem

- A pseudo filesystem, real-time, mounted on `/sys`.
- Contains information about **devices and drivers**; some files are writable for configuration
  and control. Tied to the kernel's **device driver model**.
- Key directories:
  - `block` — one subdirectory per discovered block device.
  - `bus` — per physical bus type with support registered in the kernel.
  - `class` — per registered device class (a functional type of device).
  - `devices` — the global device hierarchy (every physical device).
  - `module` — per loaded module; `power` — the power subsystem.
