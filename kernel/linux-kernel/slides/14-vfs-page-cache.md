---
layout: section
hideInToc: true
---
# VFS and page cache

---
layout: default
---
# VFS: one interface, many filesystems

- The **Virtual File System** (VFS) gives userspace a single file API (`open`, `read`, `write`,
  `stat`, `mmap`…) and lets many filesystem implementations coexist.
- It defines **abstract objects** and **operation vectors**; each filesystem fills in the methods.
- The same VFS layer serves:
  - disk filesystems (`ext4`, `btrfs`, `xfs`, …);
  - pseudo filesystems (`proc`, `sysfs`, `debugfs`, `tracefs`, `tmpfs`);
  - device files in `/dev`, pipes and sockets.
- Drivers usually meet VFS through `struct file_operations` (char devices) and through the page
  cache (file-backed I/O).

---
layout: default
---
# The VFS objects

- `struct super_block` — one mounted filesystem instance (`s_op`, `s_root`, block size…).
- `struct inode` — one file/directory/symlink/device; metadata, `i_op`, `i_fop`, `i_mapping`,
  `i_size`.
- `struct dentry` — one name in the directory cache; points to an inode (`d_parent`, `d_name`,
  `d_op`).
- `struct file` — one open file description (`f_op`, `f_path`, `f_inode`, `f_pos`,
  `private_data`).
- `struct address_space` — page-cache view of an inode's data (`i_pages`, `a_ops`, `i_mmap`).

---
layout: default
hideInToc: true
---
# VFS object relationships

<div style="text-align:center;">
  <img src="/images/vfs-objects.svg" style="background:white; border-radius:14px; padding:10px; width:1000px; max-width:94%; height:auto;" />
</div>

---
layout: default
---
# Path lookup and mounts

- A **path** is a `(vfsmount, dentry)` pair (`struct path`); `struct file` embeds one.
- `link_path_walk()` walks the pathname component by component through the **dentry cache**;
  `walk_component()` resolves one component.
- Lookup first runs under **RCU** (`LOOKUP_RCU`); on a cache miss or rename it falls back to
  ref-walk and may call `i_op->lookup()`.
- A **mount** attaches a filesystem's root dentry at a mount point; `struct vfsmount` identifies
  the mount.
- `openat2()` adds `RESOLVE_*` restrictions (no symlinks, no `..`, beneath a directory…).
- `d_path()` converts a `struct path` back to a printable path (used by `/proc`).

---
layout: default
---
# Opening a file

- `openat()` path: `do_sys_open()` → `do_file_open()` → `path_openat()` → `do_open()` →
  `do_dentry_open()` → `f_op->open()`.
- `path_openat()` resolves the path and allocates a `struct file`; `do_open()` runs the
  filesystem's `atomic_open`/`create`/`open` logic.
- `do_dentry_open()` sets `f_op` from the inode (`i_fop`), checks permissions, and calls the
  driver's `open()`.
- `struct file` carries `private_data` for the driver, `f_pos`, `f_flags` and `f_path`.
- `close()` → `filp_close()` → `f_op->flush()` (if any) → `fput()` → `f_op->release()`.

---
layout: default
---
# The page cache and address_space

- `struct address_space` is the page-cache view of an inode's data:
  - `i_pages` — XArray of folios indexed by file offset;
  - `a_ops` — `address_space_operations` supplied by the filesystem;
  - `i_mmap` — reverse mapping for mmap.
- `address_space_operations` is folio-based:
  - `read_folio()`, `readahead()`, `writepages()`, `dirty_folio()`;
  - `invalidate_folio()`, `release_folio()`, `migrate_folio()`.
- Dirty and writeback state is tagged in the XArray (`PAGECACHE_TAG_DIRTY`,
  `PAGECACHE_TAG_WRITEBACK`).
- `inode->i_mapping` is the address_space; `file->f_mapping` points to it.
- Normal reads, writes and `mmap()` go through the page cache; `O_DIRECT` bypasses it.

---
layout: default
---
# Read path

- `vfs_read()` validates the file and calls `f_op->read()` or `new_sync_read()`; the latter calls
  the file's `read_iter()` operation.
- Buffered filesystems use `filemap_read()` (or iomap): look up the folio in `i_pages`,
  start readahead on a miss, wait for I/O, mark it uptodate, then copy to userspace.
- Key helpers: `filemap_get_folio()`, `filemap_read_folio()`, `filemap_readahead()`,
  `folio_mark_uptodate()`, `copy_to_user()`.
- Readahead (`page_cache_sync_ra()` / `page_cache_async_ra()`) brings in adjacent folios to
  amortize I/O.
- A cache hit avoids the storage device entirely.

---
layout: default
---
# Write path and writeback

- `vfs_write()` → `f_op->write()` or `new_sync_write()` → `f_op->write_iter()`.
- Buffered filesystems use `generic_perform_write()` or `iomap_file_buffered_write()`:
  - get or create the folio in `i_pages`;
  - copy from userspace and mark the folio dirty.
- Dirty folios are written back by `writepages()` (writeback threads,
  `balance_dirty_pages()`), then marked clean; `fsync()` waits for the writeback.
- `filemap_write_and_wait_range()` is the common “write and wait” helper.
- Direct I/O (`O_DIRECT`) bypasses the page cache and uses `direct_IO`/iomap.
- `mmap()`-dirtied folios are written back the same way.

---
layout: default
---
# mmap and page faults

- `mmap()` → `mmap_region()` → `call_mmap_prepare()` (formerly `call_mmap()`), which calls the
  file's `mmap()` operation; the filesystem installs a `vm_operations_struct`.
- File-backed faults go through `filemap_fault()`:
  - look up the folio, read it if needed, mark it uptodate/accessed;
  - map it into the process page tables.
- `filemap_map_pages()` maps several already-present folios in one fault (fault-around).
- `VM_SHARED` mappings see writes from other mappings; `VM_PRIVATE` uses copy-on-write.
- `msync()` writes dirty shared folios back; `MADV_DONTNEED` drops PTEs.
- Driver MMIO `mmap()` is different: it uses `remap_pfn_range()` (see the mmap appendix).

---
layout: default
---
# Buffered, direct and iomap I/O

- **Buffered I/O** — data goes through the page cache; reads and writes hit RAM, writeback is
  asynchronous; the right choice for normal file I/O.
- **Direct I/O (`O_DIRECT`)** — bypasses the page cache; the application must align buffers and
  offsets; used by databases and storage applications.
- **iomap** — modern filesystem I/O framework used by XFS, ext4, btrfs, f2fs, zonefs and gfs2 for
  parts of their I/O paths; supports buffered, direct and DAX I/O with folios.
- **`buffer_head`** — legacy block-buffer abstraction; still used by some filesystems, but new
  code should use iomap and folios.
- Drivers usually do not implement these; they see the block layer or the page cache directly.

---
layout: default
---
# Dentries, inodes and pseudo filesystems

- **Dentry cache (dcache)** — maps names to dentries; `d_lookup()` / `d_add()`; `d_revalidate()`
  lets a filesystem invalidate stale entries.
- **Inode cache (icache)** — `iget()` / `iput()`; inodes stay while referenced (`i_count`,
  `i_nlink`).
- Both caches are **shrinkable**: dentries and inodes are reclaimed under memory pressure (the
  shrinkers from the memory chapter).
- **Pseudo filesystems** plug into the same VFS:
  - `proc` — per-process and kernel state;
  - `sysfs` — devices and drivers, built on `kernfs`;
  - `debugfs` / `tracefs` — debugging interfaces.
- `seq_file` and the `simple_*` helpers reduce boilerplate for read-only pseudo files.

---
layout: default
---
# Folio lifecycle and driver takeaways

- Page-cache folio lifecycle: allocate → read/uptodate → dirty → writeback → clean/reclaim.
- State lives with the folio: `_refcount`, lock, `mapping`, `index`; the XArray tracks dirty and
  writeback tags.
- In flight: `filemap_get_folio()` takes a reference; `folio_put()` releases it;
  `folio_lock()` serializes I/O and truncate.
- Driver takeaways:
  - char drivers implement `file_operations`; VFS does the dispatch;
  - use `copy_to_user()` / `copy_from_user()`, never direct user pointers;
  - file-backed `mmap()` uses `filemap_fault()`; MMIO `mmap()` uses `remap_pfn_range()`;
  - when an API gives you a `struct page *`, use `page_folio()` / `folio_page()` at the boundary.
- See the memory chapter for reclaim, MGLRU and shrinkers; see the mmap appendix for driver MMIO.

---
layout: default
hideInToc: true
---
# Folio lifecycle

<div style="text-align:center;">
  <img src="/images/folio-lifecycle.svg" style="background:white; border-radius:14px; padding:10px; width:950px; max-width:94%; height:auto;" />
</div>
