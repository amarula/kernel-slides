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
  - 5.0 → 5.19 · 6.0 (Oct 2022) → 6.19 · 7.0 (Apr 2026) → …
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

- Linux v6.19 sources: close to **92k files, 42M lines, 1.4 GiB** — but a compressed kernel is
  only a few megabytes.
- Why so big? Numerous device drivers, network protocols, architectures, filesystems — the core
  is small!
- By number of lines: `drivers/` 61%, `arch/` 12%, `tools/` 5.4%, `sound/` 3.9%, `fs/` 3.8%,
  `Documentation/` 3.8%, `include/` 3.4%, `net/` 3.1%, `kernel/` 1.3%, `lib/` 0.8%, `mm/` 0.5%…

---
layout: default
---

# Linux source organization

- `Documentation/` — kernel documentation.
- `arch/` — one subdirectory per architecture; each holds `kernel/`, `lib/`, `mm/`, `boot/`, …
  that override architecture-independent stubs; `lib/` has optimized routines (memcpy,
  checksums…).
- `drivers/` — the largest amount of code; device, bus, platform, and general directories
  (`drivers/char`, `drivers/block`, `drivers/net`, `drivers/scsi`, …).
- `fs/` — the VFS framework plus per-filesystem subdirectories.
- `include/` — `include/linux` (kernel headers), `include/asm-generic` (generic arch code),
  `include/uapi` (the user-space API, becomes `/usr/include/linux/` on install).
- `init/` — main kernel initialization (`version.c` prints the version banner at boot).
- `kernel/`, `mm/`, `lib/`, `net/`, `ipc/`, `scripts/`, `tools/`, …
