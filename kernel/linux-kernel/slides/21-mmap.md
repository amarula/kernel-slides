---
layout: section
hideInToc: true
---
# Appendix: mmap()

---
layout: default
---
# mmap() overview



- `mmap()` maps a file's (or device's) contents into the process virtual address space — useful
  for device files, avoiding expensive `read`/`write`/`ioctl` for direct access to I/O memory.
---
layout: default
hideInToc: true
---
# mmap() overview

<div style="text-align:center;">
  <img src="/images/mmap-overview.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Implementing mmap

- Kernel side: implement the `mmap` file operation and initialize the mapping with
  `remap_pfn_range()`:
  ```c
  int (*mmap)(struct file *, struct vm_area_struct *);

  remap_pfn_range(vma, vma->vm_start, ACME_PHYS >> PAGE_SHIFT,
                  size, vma->vm_page_prot);
  ```
- User side: `mmap(start, length, prot, flags, fd, offset)` → a virtual address to read/write.
- The MMU converts process virtual addresses to physical ones; the device driver is loaded and
  defines the `mmap` fop; no expensive read/write syscalls. Inspect with `/proc/<pid>/maps` or
  `pmap`; `devmem2` uses `mmap` on `/dev/mem`.
