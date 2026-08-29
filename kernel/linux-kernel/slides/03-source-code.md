---
layout: section
hideInToc: true
---
# Linux kernel source code

---
layout: default
---
# Programming language

- Implemented in **C**, like all UNIX systems; a little **assembly** for CPU/machine init,
  exceptions, and critical library routines.
- **No C++** (see the classic LKML post: https://lkml.org/lkml/2004/1/20/20).
- **Rust** support is being introduced — e.g. `drivers/net/phy/ax88796b_rust.rs`.
- Compiled with **gcc** (many GCC-specific extensions; a plain ANSI C compiler will not build it).
- A subset of architectures can also be built with **Clang/LLVM**: https://clangbuiltlinux.github.io/

---
layout: default
---
# No C library

- The kernel must be standalone and cannot use user-space code.
  - **Architectural:** user space is built on top of kernel services, not the opposite.
  - **Technical:** the kernel is on its own during boot, before a root filesystem is available.
- Kernel code must supply its own library implementations (string utils, crypto, decompression…).
- You **cannot** use the standard C library in kernel code (`printf()`, `memset()`, `malloc()`…).
- The kernel provides similar functions: `printk()`, `memset()`, `kmalloc()`…

---
layout: default
---
# Portability

- Linux kernel code is designed to be portable; everything outside `arch/` should be portable.
- The kernel provides macros/functions to abstract architecture-specific details:
  - Endianness · I/O memory access · memory barriers · the DMA API (cache flush/invalidate).
- **Never use floating point in kernel code** — your code may run on a CPU without an FPU.

---
layout: default
---
# Kernel↔user API/ABI stability

- **Kernel→userspace API is stable** — user-space source code does not need changes when moving
  to a newer kernel (system calls, `/proc` and `/sys` content cannot be removed or changed, only
  extended).
- **Kernel→userspace ABI is stable** — binaries are portable: memory layout, variable sizes,
  structure organization, calling convention are stable over time (e.g. LSB for x86-64).

---
layout: default
---
# Linux internal API/ABI instability

- **Internal API is not stable** — a driver's source code is not portable across versions.
  - In-tree drivers are updated by whoever changes the API: works great for mainline code.
  - An out-of-tree driver compiled for one version may no longer compile/work on another.
  - See `Documentation/process/stable-api-nonsense.rst` for the rationale.
- **Internal ABI is not stable** — a binary module compiled for one kernel version cannot be used
  with another; the module-loading utilities check this before insertion.

---
layout: default
---
# Kernel memory constraints

- **No memory protection**: the kernel doesn't recover from illegal memory accesses — it dumps
  an *oops* on the console.
- **Fixed-size stack** (8 or 4 KiB). Unlike user space, it cannot grow. **Don't use recursion!**
- **No swapping** of kernel memory (except tmpfs, which lives entirely in page cache/swap).

---
layout: default
---
# Kernel licensing constraints

- Linux is licensed under the **GNU GPL version 2** — you may use, study, modify, and share it.
- When the software is redistributed (modified or not), GPL requires redistribution under the
  same license, with source code.
  - Modifications to the kernel are derivative works and must be released under GPLv2.
- You are only required to do so **when the device starts being distributed**, and **to your
  customers**, not the whole world.
- GPL has been successfully enforced in courts.

---
layout: default
---
# Proprietary code and the kernel

- It is illegal to distribute a binary kernel with **statically compiled proprietary drivers**.
- **Kernel modules are a grey area** — unclear whether they are legal.
  - The kernel community's general opinion: proprietary modules are bad
    (`Documentation/process/kernel-driver-statement.rst`).
  - Legally, each driver is its own case: is it a derivative work? was it designed for another OS?
- Is it really useful to keep drivers secret anyway?

---
layout: default
---
# Advantages of GPL drivers

- You don't have to write your driver from scratch — reuse code from similar free drivers.
- Your drivers can be freely and easily shipped by others (distributions, build systems).
- **Legal certainty**: a GPL driver is fine from a legal point of view.

---
layout: default
---
# Advantages of mainlining your drivers

- Reviewers and maintainers review your code, helping you improve it and understand the APIs.
- Once accepted, you get **cost-free bug/security fixes**, new features, and improvements.
- Your work automatically follows API changes; your code stays valid across kernel versions.
- Users access your code much more easily.
- This will for sure **reduce your maintenance and support work**.

---
layout: default
---
# User space device drivers

**When possible**: USB via `libusb`, SPI via `spidev`, I2C via `i2c-dev`, GPIOs via `libgpiod`,
MMIO via `UIO`.

- Only usable when there's no need for an existing kernel subsystem (networking, filesystems),
  and no need for the kernel to multiplex the device (single application).

**Advantages:** no kernel coding skills needed · any language · can stay proprietary · can be
killed/debugged · floating point · potentially higher performance (no syscalls).

**Drawbacks:** kernel has no access · standard apps can't use it · no kernel helpers · adapt apps
when hardware changes · harder interrupt handling (higher latency).

> Kernel drivers should always be preferred.

---
layout: default
---

# Userspace GPIO: gpio-cdev and gpiolib

- **gpiolib sysfs** — old, scriptable interface (`/sys/class/gpio`); deprecated.
- **gpio-cdev** — new, higher-performance interface using character devices `/dev/gpiochip*`.

```c
struct gpiohandle_request req;
struct gpiohandle_data data;

fd = open("/dev/gpiochip0", O_RDWR);
req.lineoffsets[0] = LED_PIN;
req.flags = GPIOHANDLE_REQUEST_OUTPUT;
req.default_values[0] = 0;
ioctl(fd, GPIO_GET_LINEHANDLE_IOCTL, &req);   /* get the line handle */
data.values[0] = 1;
ioctl(req.fd, GPIOHANDLE_SET_LINE_VALUES_IOCTL, &data);  /* set high */
```

- Handles multiple pin transitions in one call; more robust interrupt handling.

---
layout: default
hideInToc: true
---

# Userspace PWM

- Most SoCs have circuits that produce a wave with a configurable **period** and **duty cycle**.
- Use cases: dimmable LEDs/backlights, servo motors (deflection ∝ duty cycle).

```bash
echo 0 > /sys/class/pwm/pwmchip0/export      # export PWM channel 0
# then write period (ns) and duty_cycle (ns):
echo 1000000 > /sys/class/pwm/pwmchip0/pwm0/period
echo 500000  > /sys/class/pwm/pwmchip0/pwm0/duty_cycle
echo 1       > /sys/class/pwm/pwmchip0/pwm0/enable
```

---
layout: default
hideInToc: true
---

# Userspace I2C: i2c-dev

- `i2c-dev` exposes I²C master controllers as `/dev/i2c-*` (one node per controller;
  `CONFIG_I2C_CHARDEV`).
- Access slaves with `read(2)`, `write(2)`, and `ioctl(2)` (structures in `linux/i2c-dev.h`).
- Tools: `i2cdetect` (scan a bus), `i2cget` / `i2cset` (read/write a peripheral's register).

```c
file = open("/dev/i2c-0", O_RDWR);
ioctl(file, I2C_SLAVE, 0x55);                  /* select slave address */
data = i2c_smbus_read_byte_data(file, 0x00);   /* read a byte */
close(file);
```

---
layout: default
hideInToc: true
---

# Userspace SPI: spidev

- SPI devices are accessed via `/dev/spidevB.C` (bus B, chip-select C).
- `read()`/`write()` are half-duplex (chip-select deactivated in between); full-duplex and
  composite transfers via `ioctl(SPI_IOC_MESSAGE(n))`.
- Configure transfer parameters with `SPI_IOC_RD/WR_MODE`, `SPI_IOC_RD/WR_BITS_PER_WORD`,
  `SPI_IOC_RD/WR_MAX_SPEED_HZ`, …
- SPI modes are (CPOL, CPHA): CPOL = clock idle level, CPHA = clock edge for sampling.
