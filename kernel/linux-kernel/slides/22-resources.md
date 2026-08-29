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
- Conferences: Embedded Linux Conference, Linux Plumbers, Kernel Recipes, linux.conf.au
- Contributing: `Documentation/process/submitting-patches.rst`,
  https://kernelnewbies.org/UpstreamMerge

---
layout: default
hideInToc: true
---
# Deep dives in this repo

This deck merges the standalone subsystem presentations already in this repository:

- `drivers/base/regmap/regmap.md` — the regmap register-access API
- `drivers/clk/clk.md` — the clock subsystem and the Common Clock Framework
- `drivers/devfreq/devfreq.md` — the devfreq (DVFS) subsystem
- `drivers/base/devres.md` — the device resource manager (devres) internals
- `kernel/locking/locking.md` — kernel locking and critical sections
- `i2c-gpio.md` — the i2c-gpio bit-banging driver

---
layout: default
hideInToc: true
---

# Inspiration & license

This deck is a derivative of:

- **Bootlin's "Linux kernel and driver development training"**
  - Slides: https://bootlin.com/doc/training/linux-kernel/
  - Source: https://github.com/bootlin/training-materials/
  - © Copyright 2004-2026, Bootlin — **Creative Commons BY-SA 3.0**
    (https://creativecommons.org/licenses/by-sa/3.0/)
- **"Introduction to Linux Kernel"** (Amarula Solutions, Michael Trimarchi), which itself takes
  inspiration from public slides and presentations under **CC BY-SA 3.0**.

All diagrams were recreated as editable draw.io sources under `kernel/linux-kernel/diagrams/`
and rendered to `kernel/linux-kernel/public/images/`.

---
layout: last-slide
hideInToc: true
---
