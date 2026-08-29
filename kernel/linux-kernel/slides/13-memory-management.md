---
layout: section
hideInToc: true
---
# Memory management

---
layout: default
---
# Physical vs. virtual memory



- The CPU accesses memory through an **MMU** using virtual addresses; physical and virtual
  address spaces differ.
---
layout: default
hideInToc: true
---
# Physical vs. virtual memory

<div style="text-align:center;">
  <img src="/images/memory-32bit.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Virtual memory organization

- The **top quarter** is reserved for **kernel space**: kernel code and core data, module loading,
  and all kernel physical mappings — identical in every address space (`PAGE_OFFSET` boundary).
- The **lower part** is per-process: program code/data, memory-mapped files. Each process has its
  own address space.

---
layout: default
---

# Memory zones and nodes

- Physical pages are grouped into **zones** by usage constraint (layout is architecture-dependent):
  - **ZONE_DMA** — memory usable by devices for legacy DMA.
  - **ZONE_NORMAL** — normally-mapped pages, directly accessible by the kernel.
  - **ZONE_HIGHMEM** — memory not permanently mapped into the kernel address space (32-bit only).
- On **NUMA** systems, memory is arranged in banks with different access latency from each CPU.
  Each bank is a **node**; the kernel builds an independent memory-management subsystem per node,
  with its own zones, free/used page lists, and statistics.

---
layout: default
---
# 32-bit limitations vs 64-bit

- **32-bit (3G/1G split):** less than 1 GiB is directly addressable through kernel virtual
  addresses. Options: change the split (`CONFIG_VMSPLIT_2G/1G`) or enable **highmem** (explicit
  mapping of extra physical memory).
- **64-bit (4 KiB pages):** ample address space — the kernel identity-maps all RAM; no highmem
  needed.
---
layout: default
hideInToc: true
---
# 32-bit limitations vs 64-bit

<div style="text-align:center;">
  <img src="/images/memory-64bit.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---

# Page cache and anonymous memory

- **Page cache** — file data read from storage is cached in RAM to avoid repeated disk access.
  Written pages are marked **dirty** and must be written back to the backing device before reuse.
- **Anonymous memory** — memory not backed by a file: program stacks, heaps, and explicit `mmap()`.
  - A read returns a **zero-filled** page; a write allocates a real physical page.
  - Anonymous pages are marked dirty and can be **swapped out** under memory pressure.

---
layout: default
---

# Memory reclaim

- **Reclaim** frees reclaimable pages and repurposes them:
  - **Reclaimable** — page cache (data already on disk) and anonymous pages (swappable).
  - **Unreclaimable** — kernel internal structures and DMA buffers, pinned until freed by their owner.
- Below the **low watermark**, `kswapd` wakes and frees pages asynchronously; below the **min
  watermark**, allocations trigger **direct reclaim** and the allocating task stalls.
- **Compaction** moves occupied pages to group free pages, enabling large physically-contiguous
  allocations; it runs via `kcompactd` (async) or on demand (sync).
- As a last resort, the **OOM killer** selects a task to kill so its memory can be reclaimed.

---
layout: default
---
# Kernel memory allocators



- **Page allocator** — contiguous physical pages (powers of two), identity-mapped.
- **SLAB** — caches of same-size objects (grows/shrinks as needed).
- **kmalloc** — general purpose, physically contiguous (SLAB for small, page allocator for large).
- **vmalloc** — large, *non*-physically-contiguous areas (not for DMA).
---
layout: default
hideInToc: true
---
# Kernel memory allocators

<div style="text-align:center;">
  <img src="/images/kernel-allocators.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Page allocator

- For medium-size allocations; a page is usually 4 KiB (some archs: 4/8/16/64 KiB).
- **Buddy allocator** → only power-of-two page counts (1, 2, 4, 8…); typical max 8192 KiB.
- Returns physically contiguous pages in the identity-mapped area (fragmentation matters; CMA can
  reserve memory at boot).

```c
unsigned long get_zeroed_page(gfp_t gfp_mask);
unsigned long __get_free_page(gfp_t gfp_mask);
unsigned long __get_free_pages(gfp_t gfp_mask, unsigned int order);
void free_page(unsigned long addr);
void free_pages(unsigned long addr, unsigned int order);
```

- Common flags: `GFP_KERNEL` (may block; fine except in interrupt context) and `GFP_ATOMIC`
  (never blocks; may fail).

---
layout: default
---
# SLAB allocator



- Caches of same-size objects; object size can be smaller or larger than a page.
- Used for frequently-instantiated structures (directory entries, file objects, packet descriptors,
  process descriptors). See `/proc/slabinfo`.
- Implementations: `CONFIG_SLUB` (default), `CONFIG_SLUB_TINY` (minimal footprint).
- `kmalloc` relies on generic `kmalloc-XXX` SLAB caches for small sizes.
---
layout: default
hideInToc: true
---
# SLAB allocator

<div style="text-align:center;">
  <img src="/images/slab-caches.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---

# SLUB debugging and tuning

- `/proc/slabinfo` lists caches; the `slabinfo` tool (`tools/mm/slabinfo.c`) shows merged caches
  (`-a`) and can plot them (`-X` + `slabinfo-gnuplot.sh`).
- Enable per-cache or global debugging with the `slab_debug` parameter: `F` sanity checks, `Z`
  red-zone, `P` poisoning, `U` user tracking, `T` tracing, `A` failslab (needs `CONFIG_SLUB_DEBUG=y`).
- Per-cache toggles live under `/sys/kernel/slab/<cache>/` (`sanity_checks`, `red_zone`, `poison`,
  `trace`, `failslab`…).
- **Slab merging**: without debug options, SLUB merges similar caches to save memory; debugging
  disables it.

---
layout: default
---
# kmalloc, vmalloc, devm

- `void *kmalloc(size_t size, gfp_t flags);` + `kfree()` — primary allocator, physically
  contiguous, sizes rounded up to the smallest SLAB cache. `kzalloc()` zeroes, `kcalloc()` arrays,
  `krealloc()` resizes.
- `void *vmalloc(unsigned long size);` + `vfree()` — non-contiguous pages; large areas possible;
  not for DMA.
- Device-managed: `devm_kmalloc`, `devm_kzalloc`, `devm_kcalloc`, `devm_kfree`.

**Debugging:** KASAN (out-of-bounds/use-after-free), KFENCE (low-overhead), Kmemleak (leaks).
KASAN and Kmemleak have significant overhead — development only.

---
layout: default
---

# Multi-Gen LRU (MGLRU)

- An alternative reclaim implementation replacing the classic **active/inactive** two-list LRU.
- Pages are organized into **multiple generations** by access time, so the kernel can separate hot
  from cold pages and make better eviction decisions — less `kswapd` CPU, better performance under
  memory pressure.
- Enable with `CONFIG_LRU_GEN=y` and `CONFIG_LRU_GEN_ENABLED=y`; runtime control via
  `/sys/kernel/mm/lru_gen/enabled` (bitmask).
- `min_ttl_ms` protects the working set of the last N milliseconds from eviction (thrashing
  prevention) — typical values `1000`–`3000`.

---
layout: default
---

# Shrinkers

- **Shrinkers** are subsystems that free reclaimable objects (dentries, inodes, slab caches) under
  memory pressure.
- Each registered shrinker has a debugfs directory at `<debugfs>/shrinker/<name>/`:
  - `count` — reports how many objects could be freed (one line per cgroup).
  - `scan` — actually reclaims a requested number of objects (write `<cgid> <node> <n>`).
- Mostly a testing/debugging interface: `count` is readable by non-root, `scan` requires write
  access.

---
layout: default
---

# zswap — compressed swap cache

- A lightweight **compressed cache for swap pages**: pages being swapped out are compressed and
  held in a RAM pool (using `zsmalloc`) instead of written straight to the swap device.
- When the pool fills, pages are evicted to the backing swap device on an LRU basis.
- Configured via `/sys/module/zswap/parameters/`: `enabled`, `compressor` (e.g. `lzo`),
  `max_pool_percent`.
- Benefits: less swap I/O, less wear on the swap device (e.g. SSD), better performance on
  memory-constrained systems — trading CPU cycles for reduced I/O.

---
layout: default
---

# Huge pages: HugeTLB vs THP

- Huge pages (e.g. 2 MiB / 1 GiB on x86) are mapped by higher-level page-table entries, **reducing
  TLB pressure** and improving performance.
- Two mechanisms:

| | HugeTLB (`hugetlbfs`) | Transparent Hugepages (THP) |
| --- | --- | --- |
| Reservation | explicit (boot / sysfs) | automatic, on demand |
| Application changes | `MAP_HUGETLB` or `hugetlbfs` | none |
| Swappable | no | yes |
| Use case | explicit large-memory apps (DB, JVM) | general-purpose, transparent |

---
layout: default
---

# HugeTLB pages

- Huge pages backed by the `hugetlbfs` pseudo-filesystem; requires `CONFIG_HUGETLBFS`.
- Preallocate at boot: `hugepagesz=<size> hugepages=N` (node-specific `hugepages=0:1,1:2`).
- Adjust at runtime: `/proc/sys/vm/nr_hugepages` (+ `nr_overcommit_hugepages` for surplus);
  per-size attributes under `/sys/kernel/mm/hugepages/`.
- Access via `mmap(MAP_HUGETLB)`, files on a mounted `hugetlbfs`, or SysV shared memory.
- **Not swappable**; needs physically contiguous memory; mappings must be hugepage-aligned.

---
layout: default
---

# Transparent Hugepages (THP)

- Automatically backs anonymous and `tmpfs`/`shmem` mappings with huge pages — **no application
  changes, no reservation**.
- Modes (`/sys/kernel/mm/transparent_hugepage/enabled`): `always`, `madvise`
  (`madvise(MADV_HUGEPAGE)`), `never`; also multi-size THP (e.g. 16 KiB–512 KiB).
- `khugepaged` collapses contiguous base pages into THPs in the background (tunable under
  `khugepaged/`).
- Monitor via `/proc/meminfo` (`AnonHugePages`, `ShmemHugePages`) and `/proc/vmstat` (`thp_*`).
- Mode changes affect only **future** mappings — restart applications to apply.
