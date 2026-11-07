---
layout: section
hideInToc: true
---
# Linux kernel sources

---
layout: default
---
# Location of the official kernel sources

- The **mainline** versions, as released by Torvalds.
  - Follow the kernel's development model (the `master` branch).
  - May not yet contain the latest developments from a specific area.
  - A good pick for a product's development phase.
  - https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git

---
layout: default
---
# Linux versioning scheme

- Until 2003: a new "stabilized" release branch every 2–3 years (2.0, 2.2, 2.4). Development
  branches took 2–3 years to merge (too slow!).
- Since 2003: a new official release about **every 10 weeks**.
  - 2.6 (Dec 2003) → 2.6.39 (May 2011) · 3.0 → 3.19 · 4.0 → 4.20
  - 5.0 → 5.19 · 6.0 (Oct 2022) → 6.19 · 7.0 (Apr 2026) → 7.3 (Oct 2026) · 7.4-rc1 (Nov 2026)
- Features are added progressively; since 2003 developers have done so without a massively
  incompatible development branch.
- **Major version numbers have no specific meaning!**

---
layout: default
---
# Linux development model

<div style="text-align:center;">
  <img src="/images/dev-model.svg" style="background:white; border-radius:14px; padding:10px; max-height:400px; max-width:88%;" />
</div>

---
layout: default
---
# The release cycle

- Each release starts with a **two-week merge window**:
  - Torvalds pulls new features from subsystem trees;
  - the `master` branch is unstable during this period.
- The merge window closes and **`-rc1`** is tagged.
- For the next **6–10 weeks**, weekly **release candidates** (`-rc2` … `-rc7`) are published:
  - only bug fixes and regression fixes;
  - no new features.
- When the release is considered stable, the final version is tagged and the cycle restarts.
- A typical cycle lasts **9–11 weeks**.

---
layout: default
---
# What goes into a release?

- **Merge window:** new features, new drivers, new APIs and cleanups.
- **`-rc` phase:** fixes only — regressions, build failures, security issues.
- **Stable releases:** after the final tag, the stable team backports selected fixes to
  `7.3.1`, `7.3.2`, …; no new features.
- **LTS:** selected releases get long-term maintenance (6.12, 6.18, …).
- **`linux-next`:** integration tree where subsystem trees are merged before the merge window;
  it catches cross-tree conflicts early.
- **Rule of thumb:** if a change is not ready before the merge window closes, it waits for the
  next cycle.

---
layout: default
---
# Need to further stabilize official kernels

- **Issue:** bug and security fixes are only merged into the `master` branch — you must update to
  the latest kernel to benefit from them.
- **Solution:** a **stable team** goes through all patches merged into Torvalds' tree and
  backports the relevant ones into **stable branches** (`7.1.1`, `7.1.2`, …) for at least a few
  months.
- Stable versions bring no new features — only bug and security fixes.
- https://git.kernel.org/pub/scm/linux/kernel/git/stable/linux.git

---
layout: default
---
# Need for long term support (LTS)

- The **last release of each year** becomes an **LTS** (Long Term Support) release, supported for
  at least 2 years; projected EOL may be extended up to 6 years based on industry interest.
- Example: since Android O (2017), all new Android devices must run an LTS kernel.
- "If you are not using a supported distribution kernel, or a stable / longterm kernel, you have
  an insecure kernel." — Greg Kroah-Hartman (2019).
- **CIP** (Civil Infrastructure Platform) supports selected LTS versions (4.4, 4.19, 5.10, 6.1,
  6.12) for at least 10 years: https://cip-project.org/

---
layout: default
---
# Location of non-official kernel sources

- **Vendor kernels** (chip vendors supply their own sources):
  - Focus on hardware support first; can have a large delta with mainline.
  - Sometimes break support for other platforms without caring.
  - Useful only early, before mainline has caught up; usually no updates → unsuitable for products.
- **Community trees** (architecture, driver, filesystem communities…):
  - Usually newer but fewer stable features, only for cutting-edge development.
  - Not suitable for products.

---
layout: default
---
# Linux kernel size and structure

- Linux v7.3 sources: close to **96k files, 41M lines, 1.8 GiB** — but a compressed kernel is
  only a few megabytes.
- Why so big? Numerous device drivers, network protocols, architectures, filesystems — the core
  is small!
- By lines (cloc, v7.3): `drivers/` 65%, `arch/` 6%, `tools/` 6%, `sound/` 4%, `fs/` 4%,
  `Documentation/` 4%, `include/` 3.6%, `net/` 3.2%, `kernel/` 1.4%, `lib/` 0.8%, `mm/` 0.6%…

---
layout: default
---
# Source tree tour: arch and drivers

- `arch/<arch>/` — one directory per architecture:
  - `kernel/`, `mm/`, `lib/`, `boot/`, `include/asm/`;
  - overrides generic code and provides optimized routines (`memcpy`, checksums).
- `drivers/` — the largest part of the tree:
  - `char/`, `block/`, `net/`, `scsi/`, `usb/`, `i2c/`, `spi/`, `gpio/`, `mmc/`, `dma/`…;
  - bus-specific, class-specific and platform-specific drivers.
- `sound/`, `gpu/`, `media/`, `input/` — framework-specific driver trees.
- `firmware/` — firmware blobs and build-time firmware data.

---
layout: default
---
# Source tree tour: core, fs and include

- `fs/` — the VFS framework plus one directory per filesystem (`ext4/`, `btrfs/`, `xfs/`…).
- `include/`:
  - `include/linux/` — kernel-internal headers;
  - `include/asm-generic/` — portable architecture fallbacks;
  - `include/uapi/` — user-space ABI headers (installed as `/usr/include/linux/`).
- `init/` — `main.c`, `version.c`, `initramfs.c`; `start_kernel()`.
- `kernel/` — scheduler, locking, time, RCU, tracing, cgroups, modules.
- `mm/` — page allocator, SLUB, vmalloc, page cache, reclaim, swap.
- `lib/`, `net/`, `ipc/`, `security/`, `crypto/`, `block/`, `scripts/`, `tools/`,
  `Documentation/`.
