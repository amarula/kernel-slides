---
layout: section
hideInToc: true
---
# Booting the kernel

---
layout: default
---

# Boot sequence overview

```
Power on ─► Boot ROM ─► Boot ─► Kernel ─► OS init ─► RUN! ─► Shutdown
```

- **Boot ROM** — executes code from a well-known location, chosen among several peripherals
  (NAND, eMMC, USB, serial…); loads the first boot stage of the bootloader.
- **Boot** — a bootloader such as U-Boot (SPL + u-boot.img), possibly OP-TEE / ATF.
- **Linux image** — `uImage`, `fitImage`, or `zImage`.
- **RUN** — mount a filesystem (initramfs, rootfs on a block device, or network disk) and run the
  first program (`init`).

---
layout: default
---

# What is a bootloader?

- Initializes the hardware peripherals needed to boot: CPU, DDR, storage devices.
- Provides software components: filesystem support (FAT, ext4…), network stack and drivers.
- It is the first component that lets you boot a complete Linux solution.

---
layout: default
---

# U-Boot: SPL and U-Boot proper

- U-Boot is both a **first-stage** and **second-stage** bootloader, loaded by the SoC's ROM from a
  supported boot device (SD, eMMC, NOR/NAND flash, …).
- **SPL** (Secondary Program Loader) — first stage; **U-Boot proper** — second stage.
- U-Boot supports booting Linux directly from the first stage with **Falcon mode**.

<div style="text-align:center;">
  <img src="/images/boot-sequence.svg" style="background:white; border-radius:14px; padding:10px; max-height:340px; max-width:88%;" />
</div>

---
layout: default
---
# Hardware description

- Many embedded architectures have lots of **non-discoverable hardware** (serial, Ethernet, I2C,
  NAND, USB controllers…).
- This hardware must be **described and passed to the kernel**.
- The bootloader/firmware provides this description at kernel start:
  - x86: **ACPI** tables.
  - most embedded devices: an OpenFirmware **Device Tree** (DT).
- This way, a kernel supporting different SoCs knows which SoC/device init hooks to run.

---
layout: default
---
# Booting with U-Boot

- ARM32: U-Boot boots `zImage` (command `bootz`).
- ARM64 / RISC-V: boots `Image` (command `booti`).
- U-Boot should also pass a **DTB** to the kernel. Typical process:

```console
1. Load zImage        at address X in memory
2. Load <board>.dtb   at address Y in memory
3. boot[z|i] X - Y        (the '-' means "no initramfs")
```

---
layout: default
---
# Kernel command line

- In addition to compile-time configuration, the kernel behavior can be adjusted at boot with the
  **kernel command line** — a string of arguments.
  - `root=` for the root filesystem; `console=` for kernel messages destination.
  - Example: `console=ttyS0 root=/dev/mmcblk0p2 rootwait`.
  - Many more, documented in `Documentation/admin-guide/kernel-parameters.rst`.

**Passing it** (U-Boot stores it in the `bootargs` variable):
- `CONFIG_CMDLINE_FROM_BOOTLOADER` — use only the bootloader string.
- `CONFIG_CMDLINE_FORCE` — use only the configured `CONFIG_CMDLINE`.
- `CONFIG_CMDLINE_EXTEND` — concatenate both.

---
layout: default
---
# Kernel log

- The kernel keeps messages in a **circular buffer** (size via `CONFIG_LOG_BUF_SHIFT`).
- Available through the **`dmesg`** command; also shown on the console pointed by `console=`.
- Console messages can be filtered by level: `console=ttyS0 loglevel=5`.
- You can write to the kernel log from user space: `echo "<n>Debug info" > /dev/kmsg`.
