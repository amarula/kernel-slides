---
layout: section
hideInToc: true
---
# Resources

---
layout: default
---
# Useful resources

- Kernel documentation: https://kernel.org/doc/
- Mailing list FAQ/etiquette: https://subspace.kernel.org/etiquette.html
- Mailing lists archive: https://lore.kernel.org/
- Kernel Newbies: https://kernelnewbies.org/ (glossary, LinuxChanges)
- eLinux wiki: https://elinux.org
- LWN (Linux Weekly News): https://lwn.net/
- VFS and path lookup: `Documentation/filesystems/{vfs,path-lookup}.rst`
- Page cache and folios: `Documentation/mm/page_cache.rst`
- linux-insides: https://github.com/0xAX/linux-insides (CC BY-NC-SA 4.0)
- Conferences: Embedded Linux Conference, Linux Plumbers, Kernel Recipes, linux.conf.au
- Contributing: `Documentation/process/submitting-patches.rst`,
  https://kernelnewbies.org/UpstreamMerge

---
layout: default
hideInToc: true
---
# Deep dives in this deck

The material from the former standalone presentations now lives in these chapters:

- `11-i2c.md` — I2C and the i2c-gpio bit-banging driver
- `12-frameworks.md` — regmap, devres and the input subsystem
- `16-clocking-power.md` — Common Clock Framework and devfreq
- `20-locking.md` — locking and critical sections

---
layout: default
hideInToc: true
---

# Inspiration & license

- **Bootlin's "Linux kernel and driver development training"**
  - Slides: https://bootlin.com/doc/training/linux-kernel/
  - Source: https://github.com/bootlin/training-materials/
  - © Copyright 2004-2026, Bootlin — **Creative Commons BY-SA 3.0**
    (https://creativecommons.org/licenses/by-sa/3.0/)
- **"Introduction to Linux Kernel"** (Amarula Solutions, Michael Trimarchi), which itself takes
  inspiration from public slides and presentations under **CC BY-SA 3.0**.
- **`linux-insides`** by 0xAX (https://github.com/0xAX/linux-insides) — used as a structural and
  conceptual reference for the kernel-internals material. `linux-insides` is licensed
  **CC BY-NC-SA 4.0**; no text or diagrams from it are reproduced here.

All diagrams were recreated as editable draw.io sources under `kernel/linux-kernel/diagrams/`
and rendered to `kernel/linux-kernel/public/images/`.
