---
layout: section
hideInToc: true
---
# I/O memory

---
layout: default
---
# Memory-mapped I/O (MMIO)



- The same address bus addresses memory and device registers; registers are accessed with normal
  load/store instructions.
- Request the region with `request_mem_region()` / `release_mem_region()` (see `/proc/iomem`).
---
layout: default
hideInToc: true
---
# Memory-mapped I/O (MMIO)

<div style="text-align:center;">
  <img src="/images/mmio.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# ioremap()



```c
#include <linux/io.h>
void __iomem *ioremap(phys_addr_t phys_addr, unsigned long size);
void iounmap(void __iomem *addr);
```

- Load/store instructions work with virtual addresses, but I/O memory is not mapped by default —
  `ioremap()` creates the virtual mapping. **Check for a NULL return!**
- Prefer the managed `devm_platform_ioremap_resource(pdev, index)`.
---
layout: default
hideInToc: true
---
# ioremap()

<div style="text-align:center;">
  <img src="/images/ioremap.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# MMIO access functions

- Care is required: MMIO can be weakly ordered, endianness may differ, and direct pointer
  dereferencing may not work on some architectures.
- Use architecture-independent accessors:

| Name | Device endianness | Memory barriers |
| --- | --- | --- |
| `read/write` | little | yes |
| `ioread/iowrite` | little | yes |
| `ioreadbe/iowritebe` | big | yes |
| `__raw_read/__raw_write` | native | no |
| `read_relaxed/write_relaxed` | little | no |

- `/dev/mem` gives user space direct access to physical addresses (`devmem2`); restricted by
  `CONFIG_STRICT_DEVMEM` / `CONFIG_IO_STRICT_DEVMEM`.
