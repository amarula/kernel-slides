---
layout: section
hideInToc: true
---
# Kernel frameworks

---
layout: default
---
# Types of devices

- **Network devices** — interfaces, visible via `ip a`.
- **Block devices** — access to raw storage, device files in `/dev`.
- **Character devices** — all other devices (input, sound, graphics, serial…), device files in
  `/dev`.
- **Sysfs devices** — only a sysfs representation (e.g. pinctrl, IIO).

→ Most devices are **character devices**.

---
layout: default
---
# Everything is a file

- A key UNIX design decision: represent most system objects as **files**, manipulated with the
  normal file API (`open`, `read`, `write`, `close`…).
- A **device file** associates a user-space filename to a triplet the kernel understands:
  - **type**: char or block
  - **major**: class of the device
  - **minor**: unique identifier within a class
- By convention device files live in `/dev`.
- Since Linux 2.6.32, **devtmpfs** mounts on `/dev` and contains devices registered to frameworks;
  udev/mdev supplement it (permissions, module loading, symlinks).

---
layout: default
---
# A character driver in the kernel



- A character driver implements operations from `struct file_operations` (`read`, `write`,
  `ioctl`…); the filesystem layer calls them when the corresponding system call happens.
---
layout: default
hideInToc: true
---
# A character driver in the kernel

<div style="text-align:center;">
  <img src="/images/char-device.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# File operations

```c
struct file_operations {
    struct module *owner;
    ssize_t (*read) (struct file *, char __user *, size_t, loff_t *);
    ssize_t (*write) (struct file *, const char __user *, size_t, loff_t *);
    long (*unlocked_ioctl) (struct file *, unsigned int, unsigned long);
    int (*mmap) (struct file *, struct vm_area_struct *);
    int (*open) (struct inode *, struct file *);
    int (*release) (struct inode *, struct file *);
    ...
};
```

- Many operations exist; all are optional.
- `open()`/`release()` are called on open/close (implement only if needed); `struct file` has a
  `void *private_data` you can use freely.

---
layout: default
---
# Exchanging data with user space

- Kernel code **must not** directly access user-space memory (`memcpy()` or pointer dereference):
  user pointers may be invalid, or a malicious app could pass a kernel address.
- Use dedicated functions and **check return values** (non-zero → return `-EFAULT`):
  - Single value: `get_user(v, p);` / `put_user(v, p);`
  - Buffer: `copy_to_user(to, from, n);` / `copy_from_user(to, from, n);`
- Zero-copy options for large transfers: `mmap()` or `get_user_pages()`.

---
layout: default
---
# unlocked_ioctl()

- `long unlocked_ioctl(struct file *f, unsigned int cmd, unsigned long arg)`
- Associated with the `ioctl()` system call; extends the driver beyond read/write
  (e.g. serial speed, video format, querying a serial number).
- `cmd` identifies the operation (see `Documentation/driver-api/ioctl.rst` for numbering);
  `arg` is an optional argument (integer, address…). The semantics are driver-specific.

```c
switch (cmd) {
case PHN_SET_REG:
    if (copy_from_user(&r, argp, sizeof(r)))
        return -EFAULT;
    break;
case PHN_GET_REG:
    if (copy_to_user(argp, &r, sizeof(r)))
        return -EFAULT;
    break;
default:
    return -ENOTTY;
}
```

---
layout: default
---
# Beyond character drivers: frameworks



- Many drivers are not raw character drivers; they plug into a **framework** specific to a device
  type (framebuffer, V4L, serial…).
- The framework implements `file_operations` **once** and shares it across all its devices —
  minimizing boilerplate and giving a coherent user-space interface.
---
layout: default
hideInToc: true
---
# Beyond character drivers: frameworks

<div style="text-align:center;">
  <img src="/images/kernel-frameworks.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Input subsystem



- Handles all input events from the human user (keyboards, mice, touchscreens…).
- **Device drivers** talk to the hardware and feed events; **event handlers** forward them
  (mostly via `evdev`).
---
layout: default
hideInToc: true
---
# Input subsystem

<div style="text-align:center;">
  <img src="/images/input-subsystem.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Input subsystem API

```c
struct input_dev *dev = devm_input_allocate_device(&pdev->dev);

set_bit(EV_KEY, dev->evbit);   /* event types */
set_bit(BTN_0, dev->keybit);   /* event codes */

input_register_device(dev);

/* send events */
input_report_key(dev, BTN_LEFT, value);
input_report_rel(dev, REL_X, delta);
input_sync(dev);
```

- `evdev` user interface: each input device is `/dev/input/event<X>`; `read()` returns
  `struct input_event { timeval time; unsigned short type, code; unsigned int value; }`.
- Test with `evtest`. Polled devices via `input_setup_polling()`.

---
layout: default
---

# What is regmap?

- Initially an API for accessing registers on non-memory-mapped buses, like I²C and SPI.
- Introduced in **kernel v3.1** by Mark Brown (Wolfson Microelectronics, 2011).
- Later implemented for memory-mapped I/O too.
- Allows device drivers to interact with hardware registers in a unified manner.
- Located at `drivers/base/regmap/*`.

---
layout: two-cols
transition: fade
---

# Why regmap?

- It applies what was already used for ASoC (audio processing chips), abstracting it for general use.
- Before, drivers had redundant and similar code when dealing with these buses.
- Simplifies driver development.

::right::

<img src="/images/drivers.svg" class="content-image-right"
     style="background-color:white; border-radius:20px; width:400px; margin-left:30px"/>

---
layout: two-cols
hideInToc: true
---

# Why regmap?

- It applies what was already used for ASoC (audio processing chips), abstracting it for general use.
- Before, drivers had redundant and similar code when dealing with these buses.
- Simplifies driver development.

::right::

<img src="/images/regmap.svg" class="content-image-right"
     style="background-color:white; border-radius:20px; width:400px; margin-left:30px"/>

---
layout: default
transition: slide-left
---

# Practical steps to using regmap

<div class="center">

<v-clicks>

- Create and fill in a `struct regmap_config` with all necessary information.
- Inside the driver's probe function, call `devm_regmap_init_i2c`, `devm_regmap_init_spi`, or
  `devm_regmap_init_mmio`, depending on the connection type.
- When reading/writing registers, call `regmap_read` and `regmap_write` functions.
    - There also exist other kinds of reads and writes, like `regmap_bulk_read`,
      `regmap_bulk_write`, `regmap_write_async`.
- Devres will free the structure for you when finished.

</v-clicks>

</div>

---
layout: default
---

# The `regmap_config` structure

- Defined in `include/linux/regmap.h`.
- Provides configuration options for `struct regmap`.
- Some interesting elements (most are optional):

````md magic-move

```c
struct regmap_config {
    const char *name;
    int reg_bits;  /* register address length, in bits */
    int reg_stride;  /* valid register addresses must be multiples of the stride */
    [...]
    int val_bits;  /* register size, in bits */
    [...]
}
```

```c
struct regmap_config {
    [...]
    bool disable_locking;  /* don't use locking mechanisms */
    regmap_lock lock;  /* optional callback which overrides the default locking function */
    regmap_unlock unlock;  /* same as above for unlocking */
    void *lock_arg;  /* the only argument to be passed to the custom lock/unlock functions */
    [...]
}
```

```c
struct regmap_config {
    [...]
    /* optional callback functions which should return true
    if the register is writeable, readable or volatile */
    bool (*writeable_reg)(struct device *dev, unsigned int reg);
    bool (*readable_reg)(struct device *dev, unsigned int reg);
    bool (*volatile_reg)(struct device *dev, unsigned int reg);
    [...]
}
```

```c
struct regmap_config {
    [...]
    unsigned int max_register;  /* maximum valid register address */
    bool max_register_is_0;  /* if true, consider value in max_register even if zero */
    [...]
}
```

```c
struct regmap_config {
    [...]
    /* instead of the callback functions (writeable_reg, readable_reg,
    volatile_reg), these tables can be used to contain the valid addresses
    that can be written, read, or are volatile */
    const struct regmap_access_table *wr_table;
    const struct regmap_access_table *rd_table;
    const struct regmap_access_table *volatile_table;
    [...]
}
```

```c
struct regmap_config {
    [...]
    const struct reg_default *reg_defaults;  /* power on reset values for the registers */
    unsigned int num_reg_defaults;  /* number of elements in reg_defaults */
    enum regcache_type cache_type;  /* actual cache type */
    [...]
}
```

```c
struct regmap_config {
    [...]
    unsigned long read_flag_mask;  /* bit mask to apply when reading a register */
    unsigned long write_flag_mask;  /* bit mask to apply when writing */
    bool zero_flag_mask;  /* if true, apply read_flag_mask and write_flag_mask even if they are zero*/
    [...]
}
```

````

---
layout: default
---

# Example of regmap initialisation

Taken from `drivers/mfd/stmfx.c`, for the STMicroelectronics MultiFunction eXpander (a GPIO
expander over I²C).

```c
static const struct regmap_config stmfx_regmap_config = {
    .reg_bits       = 8,
    .reg_stride     = 1,
    .val_bits       = 8,
    .max_register   = STMFX_REG_MAX,
    .volatile_reg   = stmfx_reg_volatile,
    .writeable_reg  = stmfx_reg_writeable,
    .cache_type     = REGCACHE_MAPLE,
};
```

```c
static int stmfx_probe(struct i2c_client *i2c)
{
    [...]
    stmfx->map = devm_regmap_init_i2c(client, &stmfx_regmap_config);
    [...]
}
```

---
layout: default
---

# The `devm_regmap_init_i2c` function

Found in `drivers/base/regmap/regmap-i2c.c`.

```c
struct regmap *__devm_regmap_init_i2c(struct i2c_client *i2c, const struct regmap_config *config,
                                      struct lock_class_key *lock_key, const char *lock_name)
{
    const struct regmap_bus *bus = regmap_get_i2c_bus(i2c, config);

    if (IS_ERR(bus))
        return ERR_CAST(bus);

    return __devm_regmap_init(&i2c->dev, bus, &i2c->dev, config, lock_key, lock_name);
}
EXPORT_SYMBOL_GPL(__devm_regmap_init_i2c);
```

Gets the i2c bus information, then passes it all to `__devm_regmap_init`, which calls
`__regmap_init` (in `drivers/base/regmap/regmap.c`) to allocate and initialise a `struct regmap`.

---
layout: fact
hideInToc: true
---

# Something curious:

Some functions are declared and exported as `__foo`, while drivers call them as `foo`. How?

<br>

<v-click>

Inside the header file, there is a wrapper macro named `foo`, which calls `__foo` while also
checking lock dependencies at runtime. From `include/linux/regmap.h`:

```c
#define regmap_init_i2c(i2c, config)					\
	__regmap_lockdep_wrapper(__regmap_init_i2c, #config,		\
				i2c, config)
```

</v-click>

---
layout: default
---

# The `regmap_read` function

Defined in `drivers/base/regmap/regmap.c`. Takes the map, the register to read, and a pointer to
where the read value should be stored.

```c
int regmap_read(struct regmap *map, unsigned int reg, unsigned int *val)
{
    int ret;
    if (!IS_ALIGNED(reg, map->reg_stride))
        return -EINVAL;

    map->lock(map->lock_arg);
    ret = _regmap_read(map, reg, val);
    map->unlock(map->lock_arg);

    return ret;
}
```

Checks register alignment, locks the map, calls `_regmap_read`, unlocks, and returns.

---
layout: default
hideInToc: true
---

# The internal `_regmap_read`

````md magic-move

```c
static int _regmap_read(struct regmap *map, unsigned int reg, unsigned int *val)
{
    int ret;
    void *context = _regmap_map_get_context(map);

    if (!map->cache_bypass) {
        ret = regcache_read(map, reg, val);
        if (ret == 0)
            return 0;
    }

    if (map->cache_only)
        return -EBUSY;

    if (!regmap_readable(map, reg))
        return -EIO;
    [...]
}
```

```c
static int _regmap_read(struct regmap *map, unsigned int reg, unsigned int *val)
{
    [...]
    ret = map->reg_read(context, reg, val);
    if (ret == 0) {
        if (regmap_should_log(map))
            dev_info(map->dev, "%x => %x\n", reg, *val);

        trace_regmap_reg_read(map, reg, *val);

        if (!map->cache_bypass)
            regcache_write(map, reg, *val);
    }
    return ret;
}
```

````

Tries the cache first; on a miss it reads the register, then writes the result back into the cache.

---
layout: default
---

# The `regmap_write` function

Also defined in `drivers/base/regmap/regmap.c`, and accepts the same arguments.

```c
int regmap_write(struct regmap *map, unsigned int reg, unsigned int val)
{
    int ret;

    if (!IS_ALIGNED(reg, map->reg_stride))
        return -EINVAL;

    map->lock(map->lock_arg);
    ret = _regmap_write(map, reg, val);
    map->unlock(map->lock_arg);

    return ret;
}
```

Basically the same as `regmap_read`: checks alignment, locks, calls `_regmap_write`, unlocks.

---
layout: default
hideInToc: true
---

# The internal `_regmap_write`

````md magic-move

```c
int _regmap_write(struct regmap *map, unsigned int reg, unsigned int val)
{
    int ret;
    void *context = _regmap_map_get_context(map);

    if (!regmap_writeable(map, reg))
        return -EIO;

    if (!map->cache_bypass && !map->defer_caching) {
        ret = regcache_write(map, reg, val);
        if (ret != 0)
            return ret;
        if (map->cache_only) {
            map->cache_dirty = true;
            return 0;
        }
    }
    [...]
}
```

```c
int _regmap_write(struct regmap *map, unsigned int reg, unsigned int val)
{
    [...]
    ret = map->reg_write(context, reg, val);
    if (ret == 0) {
        if (regmap_should_log(map))
            dev_info(map->dev, "%x <= %x\n", reg, val);

        trace_regmap_reg_write(map, reg, val);
    }

    return ret;
}
```

````

If caching is not bypassed or deferred, writes in cache. Then writes to the actual hardware register.

---
layout: default
---

# Freeing

<div class="center">

If you use `devm_` to initialise your regmap, devres will free the allocated space for you.

</div>

---
layout: default
---
# Device-managed allocations (devres)

- `probe()` allocates many resources that must be freed on failure *and* in `remove()` — lots of
  rarely-tested error handling.
- **Device-managed allocations** associate resources with the `struct device`, released
  automatically when the device disappears or is unbound.
- Functions are prefixed with `devm_` (e.g. `devm_kmalloc`, `devm_ioremap_resource`,
  `devm_request_irq`, `devm_input_allocate_device`).

```c
foo = devm_kzalloc(&pdev->dev, sizeof(*foo), GFP_KERNEL);
```

- Caveats: cleanup happens when the `struct device` is cleaned up (no refcounting); don't use for
  memory accessed after remove (e.g. an open device file); watch out for circular references.

---
layout: default
hideInToc: true
---

# devres: a list of devices… literally

The devres library stores resources in a **linked list** attached to the device. The relevant part of
`struct device` (in `linux/device.h`):

```c
struct device {
    [...]
    spinlock_t      devres_lock;    /* protects the list */
    struct list_head devres_head;   /* list of devres nodes */
    [...]
};
```

On this list you can add/remove entries (`devres_add`/`devres_remove`), search an entry
(`devres_find`), and run operations on all entries (`devres_for_each_res`).

---
layout: default
hideInToc: true
---

# devres: a tree all along

- Devices are arranged in a **tree** (each has a parent).
- When a device is removed, resources of its children can be released automatically.
- A `spinlock` (not a mutex) protects the list — we are in kernel drivers.

---
layout: default
hideInToc: true
---

# Devres structures

```c
struct devres {
    struct devres_node   node;
    /* data[] is aligned with ARCH_DMA_MINALIGN so the whole
     * struct devres has the same alignment when kmalloc()ed */
    u8 __aligned(ARCH_DMA_MINALIGN) data[];
};

struct devres_node {
    struct list_head  entry;
    dr_release_t      release;   /* function that frees the resource */
    const char        *name;     /* used for searching */
    size_t            size;
};
```

---
layout: default
hideInToc: true
---

# devres alloc, add, free

Simple driver example — SPI controller (`devres_alloc` → `devres_add`, or `devres_free`):

```c
struct spi_controller *__devm_spi_alloc_controller(struct device *dev,
                                                   unsigned int size, bool slave)
{
    struct spi_controller **ptr, *ctlr;

    ptr = devres_alloc(devm_spi_release_controller, sizeof(*ptr), GFP_KERNEL);
    if (!ptr)
        return NULL;

    ctlr = __spi_alloc_controller(dev, size, slave);
    if (ctlr) {
        ctlr->devm_allocated = true;
        *ptr = ctlr;
        devres_add(dev, ptr);
    } else {
        devres_free(ptr);
    }
    return ctlr;
}
```

---
layout: default
hideInToc: true
---

# Devres alloc

```c
void *__devres_alloc_node(dr_release_t release, size_t size, gfp_t gfp, int nid,
                          const char *name)
{
    struct devres *dr;

    dr = alloc_dr(release, size, gfp | __GFP_ZERO, nid);
    if (unlikely(!dr))
        return NULL;
    set_node_dbginfo(&dr->node, name, size);
    return dr->data;
}

static __always_inline struct devres *alloc_dr(dr_release_t release,
                                               size_t size, gfp_t gfp, int nid)
{
    size_t tot_size;
    struct devres *dr;

    if (!check_dr_size(size, &tot_size))
        return NULL;

    dr = kmalloc_node_track_caller(tot_size, gfp, nid);
    if (unlikely(!dr))
        return NULL;

    if (!(gfp & __GFP_ZERO))       /* don't clear memory twice */
        memset(dr, 0, offsetof(struct devres, data));

    INIT_LIST_HEAD(&dr->node.entry);
    dr->node.release = release;
    return dr;
}
```

---
layout: default
hideInToc: true
---

# Devres add

```c
void devres_add(struct device *dev, void *res)
{
    struct devres *dr = container_of(res, struct devres, data);
    unsigned long flags;

    spin_lock_irqsave(&dev->devres_lock, flags);
    add_dr(dev, &dr->node);
    spin_unlock_irqrestore(&dev->devres_lock, flags);
}

static void add_dr(struct device *dev, struct devres_node *node)
{
    devres_log(dev, node, "ADD");
    BUG_ON(!list_empty(&node->entry));
    list_add_tail(&node->entry, &dev->devres_head);
}
```

---
layout: default
hideInToc: true
---

# Devres free

```c
void devres_free(void *res)
{
    if (res) {
        struct devres *dr = container_of(res, struct devres, data);

        BUG_ON(!list_empty(&dr->node.entry));
        kfree(dr);
    }
}
```

Frees the resource and its container. The node must not be in the list anymore.

---
layout: default
hideInToc: true
---

# Devres remove

```c
void *devres_remove(struct device *dev, dr_release_t release,
                    dr_match_t match, void *match_data)
{
    struct devres *dr;
    unsigned long flags;

    spin_lock_irqsave(&dev->devres_lock, flags);
    dr = find_dr(dev, release, match, match_data);
    if (dr) {
        list_del_init(&dr->node.entry);
        devres_log(dev, &dr->node, "REM");
    }
    spin_unlock_irqrestore(&dev->devres_lock, flags);

    return dr ? dr->data : NULL;
}
```

`find_dr()` iterates the list **in reverse** (`list_for_each_entry_reverse`) and returns the first
entry matching the release function and (optional) match callback.

---
layout: default
hideInToc: true
---

# Devres destroy

```c
int devres_destroy(struct device *dev, dr_release_t release,
                   dr_match_t match, void *match_data)
{
    void *res;

    res = devres_remove(dev, release, match, match_data);
    if (unlikely(!res))
        return -ENOENT;

    devres_free(res);
    return 0;
}
```

`destroy` = `remove` + `free`. Example caller:

```c
void devm_usb_put_phy(struct device *dev, struct usb_phy *phy)
{
    int r;

    r = devres_destroy(dev, devm_usb_phy_release, devm_usb_phy_match, phy);
    dev_WARN_ONCE(dev, r, "couldn't find PHY resource\n");
}
```

---
layout: default
hideInToc: true
---

# Groups

Grouping resources is useful for middle layers, for managing group policies, and for releasing
everything at once.

```c
struct devres_group {
    struct devres_node  node[2];   /* open + close markers */
    void                *id;
    int                 color;
    /* -- 8 pointers -- */
};
```

- `devres_open_group()` — create a group.
- `devres_release_group()` — release all resources in the group.
- `devres_remove_group()` — drop the group (keep its resources).

---
layout: default
hideInToc: true
---

# devres_open_group

```c
void *devres_open_group(struct device *dev, void *id, gfp_t gfp)
{
    struct devres_group *grp;
    unsigned long flags;

    grp = kmalloc(sizeof(*grp), gfp);
    if (unlikely(!grp))
        return NULL;

    grp->node[0].release = &group_open_release;
    grp->node[1].release = &group_close_release;
    INIT_LIST_HEAD(&grp->node[0].entry);
    INIT_LIST_HEAD(&grp->node[1].entry);
    set_node_dbginfo(&grp->node[0], "grp<", 0);
    set_node_dbginfo(&grp->node[1], "grp>", 0);
    grp->id = grp;
    if (id)
        grp->id = id;

    spin_lock_irqsave(&dev->devres_lock, flags);
    add_dr(dev, &grp->node[0]);
    spin_unlock_irqrestore(&dev->devres_lock, flags);
    return grp->id;
}
```

The `id` can be specified, or automatically created by passing `NULL`; it is returned either way.

---
layout: default
hideInToc: true
---

# devres_remove_group / devres_release_group

```c
void devres_remove_group(struct device *dev, void *id)
{
    struct devres_group *grp;
    unsigned long flags;

    spin_lock_irqsave(&dev->devres_lock, flags);
    grp = find_group(dev, id);
    if (grp) {
        list_del_init(&grp->node[0].entry);
        list_del_init(&grp->node[1].entry);
        devres_log(dev, &grp->node[0], "REM");
    } else
        WARN_ON(1);
    spin_unlock_irqrestore(&dev->devres_lock, flags);
    kfree(grp);
}
```

```c
int devres_release_group(struct device *dev, void *id)
{
    struct devres_group *grp;
    unsigned long flags;
    LIST_HEAD(todo);
    int cnt = 0;

    spin_lock_irqsave(&dev->devres_lock, flags);
    grp = find_group(dev, id);
    if (grp) {
        struct list_head *first = &grp->node[0].entry;
        struct list_head *end = &dev->devres_head;
        if (!list_empty(&grp->node[1].entry))
            end = grp->node[1].entry.next;

        cnt = remove_nodes(dev, first, end, &todo);
        spin_unlock_irqrestore(&dev->devres_lock, flags);
        release_nodes(dev, &todo);
    } else {
        WARN_ON(1);
        spin_unlock_irqrestore(&dev->devres_lock, flags);
    }
    return cnt;
}
```
