---
layout: section
hideInToc: true
---
# Developing kernel modules

---
layout: default
---
# Hello module

```c
// SPDX-License-Identifier: GPL-2.0
/* hello.c */
#include <linux/init.h>
#include <linux/module.h>
#include <linux/kernel.h>

static int __init hello_init(void)
{
    pr_alert("Good morrow to this fair assembly.\n");
    return 0;
}

static void __exit hello_exit(void)
{
    pr_alert("Alas, poor world, what treasure hast thou lost!\n");
}

module_init(hello_init);
module_exit(hello_exit);
MODULE_LICENSE("GPL");
MODULE_DESCRIPTION("Greeting module");
MODULE_AUTHOR("William Shakespeare");
```

---
layout: default
---
# Hello module explanations

- **Kernel-specific headers** `linux/xxx.h` — no access to the usual C library.
- An **initialization function**, called on load; returns 0 on success, negative on failure;
  declared by the `module_init()` macro (the name is a convention).
- A **cleanup function**, called on unload; declared by `module_exit()`.
- **Metadata** declared with `MODULE_LICENSE()`, `MODULE_DESCRIPTION()`, `MODULE_AUTHOR()`.
- `__init` code is removed after init; `__exit` code is discarded when built statically.

---
layout: default
---
# Symbols exported to modules

- From a module, only a limited number of kernel functions can be called — they must be
  **explicitly exported**.
- `EXPORT_SYMBOL(symbol)` — export to all modules.
- `EXPORT_SYMBOL_GPL(symbol)` — export only to GPL modules.
- A normal driver should not need any non-exported function.

---
layout: default
---
# Module license

- Used to restrict the functions a non-GPL module can use
  (the `EXPORT_SYMBOL` vs `EXPORT_SYMBOL_GPL` distinction).
- A proprietary module **taints** the kernel (visible in crashes/oopses).
- Values: GPL-compatible (`GPL`, `GPL v2`, `GPL and additional rights`, `Dual MIT/GPL`,
  `Dual BSD/GPL`, `Dual MPL/GPL`) or `Proprietary`.
- Users can check with `/proc/sys/kernel/tainted`.

---
layout: default
---
# Compiling a module

Two solutions:

- **Out of tree** (code outside the kernel tree): not integrated into the kernel build; must be
  built separately; can only be a module.
- **Inside the kernel tree**: well integrated; can be built statically or as a module.

Out-of-tree Makefile:

```make
ifneq ($(KERNELRELEASE),)
obj-m := hello.o
else
KDIR := /path/to/kernel/sources
all:
	$(MAKE) -C $(KDIR) M=$$PWD
endif
```

- `KDIR`: kernel source or headers directory (must be configured — `.config`).

---
layout: default
---
# Modules and kernel version

- To compile, a module needs **kernel headers** (definitions of functions, types, constants).
  - Full kernel sources (configured + `make modules_prepare`), or
  - only headers (`linux-headers-*` packages, or `make headers_install`).
- Sources/headers must be **configured**; you also need the kernel Makefile, `scripts/`, etc.
- A module built against version X **will not load** in kernel version Y (`Invalid module format`).

---
layout: default
---
# New driver in kernel sources

1. Add your source file to the right directory, e.g. `drivers/usb/serial/navman.c`.
2. Describe the config interface in the directory's `Kconfig`:
   ```ini
   config USB_SERIAL_NAVMAN
       tristate "USB Navman GPS device"
       depends on USB_SERIAL
       help
         To compile this driver as a module, choose M here: the module
         will be called navman.
   ```
3. Add a line in the `Makefile`:
   ```make
   obj-$(CONFIG_USB_SERIAL_NAVMAN) += navman.o
   ```
4. `make xconfig` to see the option; `make` to build. See `Documentation/kbuild/` for details.

---
layout: default
---
# Module parameters

```c
// SPDX-License-Identifier: GPL-2.0
#include <linux/init.h>
#include <linux/module.h>

MODULE_LICENSE("GPL");

static char *whom = "world";
module_param(whom, charp, 0644);
MODULE_PARM_DESC(whom, "Recipient of the hello message");

static int howmany = 1;
module_param(howmany, int, 0644);
MODULE_PARM_DESC(howmany, "Number of greetings");
```

- `module_param(name, type, perm)` — `type` in `byte, short, ushort, int, uint, long, ulong,
  charp, bool, invbool`; `perm` controls `/sys/module/<module>/parameters/<param>`.
- Arrays via `module_param_array()`.
