---
theme: ../../../template
fonts:
  sans: Open Sans
  serif: IBM Plex Serif
  mono: IBM Plex Mono
  weights: '200,400,700'
image: 'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?q=80&w=2069'
transition: slide-left
mdc: true
layout: cover
---

# regmap
## A generic hardware register access API
### Margherita Milani, Patrick Barsanti

---
layout: default
hideInToc: true
---

# Table of contents

<Toc minDepth="1" maxDepth="2"/>

---
layout: default
---

# What is regmap?

<div class="center">

- Initially an API for accessing registers on non-memory mapped buses, like
I²C and SPI.
- Introduced in `Kernel v3.1` by Mark Brown, Wolfson Microelectronics, 2011.
- Later implemented also for memory-mapped I/O.
- Allows device drivers to interact with hardware registers in a unified manner.
- Located at `drivers/base/regmap/*`.

</div>

---
layout: two-cols
transition: fade
---

# Why regmap?

- It applies what was already being used for ASoC (audio processing chip),
abstracting it for general use.
- Before, drivers had redundant and similar code when dealing with these buses.
- Simplifies driver development.

<img src="/images/drivers.svg" class="content-image-right"/>

---
layout: two-cols
layoutClass: gap16
hideInToc: true

---

# Why regmap?

- It applies what was already being used for ASoC (audio processing chip),
abstracting it for general use.
- Before, drivers had redundant and similar code when dealing with these buses.
- Simplifies driver development.

<img src="/images/regmap.svg" class="content-image-right"/>

---
layout: default
transition: slide-left
---

# Practical steps to using regmap

<div class="center">

<v-clicks>

- Create and fill in a `struct regmap_config` with all necessary information.
- Inside the driver's probe function, call
`devm_regmap_init_i2c`, `devm_regmap_init_spi`, or `devm_regmap_init_mmio`,
depending on the connection type.
- When reading/writing to registers, call `regmap_read` and
`regmap_write` functions.
    - There also exist other kinds of reads and writes, like `regmap_bulk_read`,
      `regmap_bulk_write`, `regmap_write_async`.
- Devres will free the structure for you when finished.

</v-clicks>

</div>

---
title: The *regmap_config* structure
---

# The `regmap_config` structure

- Defined in `include/linux/regmap.h`.
- Provides configuration options for `struct regmap`.
- Let's see some interesting elements (most are optional):

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

# Example of regmap initialisation

Taken from `drivers/mfd/stmfx.c` driver, for the **M**ulti**F**unction
e**X**pander by ST Microelectronics, which is a GPIO expander over I²C.

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

<br>

```c
static int stmfx_probe(struct i2c_client *i2c)
{
    [...]
    stmfx->map = devm_regmap_init_i2c(client, &stmfx_regmap_config);
    [...]
}
```

---
title: The *devm_regmap_init_i2c* function
---

# The `devm_regmap_init_i2c` function

Found in `drivers/base/regmap/regmap-i2c.c`.

```c {all|4|9|all}
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

Gets i2c bus information, then passes it all to `__devm_regmap_init`.
`__devm_regmap_init` then calls `__regmap_init` (found in
`drivers/base/regmap/regmap.c`),
which uses the `struct regmap_config` and the bus information to
allocate space for and initialise a `struct regmap`.

---
layout: fact
hideInToc: true
---

## Some functions are declared and exported as `__foo`,
## while in drivers they are called as `foo`. How?

<v-click>

<div align=left>

Inside the header file, there is a wrapper macro named `foo`, which calls
`__foo` while also checking lock dependencies at runtime.
The following example is taken from `include/linux/regmap.h`:

```c
#define regmap_init_i2c(i2c, config)					\
	__regmap_lockdep_wrapper(__regmap_init_i2c, #config,		\
				i2c, config)
```

</div>

</v-click>

---
title: The *regmap_read* function
---
# The `regmap_read` function

Defined in `drivers/base/regmap/regmap.c`.
Accepts three arguments: the map to read from, the register to be read, and the
pointer to where the read value should be stored.

```c {all|4,5|7|8|9|all}
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

It checks if the register address is aligned with the specified stride, locks
the map, calls internal function `_regmap_read`, unlocks the map and returns.

<!--
the lock by default is a mutex but can be explicitly specified
to be a spinlock, for example with fast_io flag in regmap_config
-->

---
level: 2
title: The internal *_regmap_read*
---

# The internal `_regmap_read`

````md magic-move

```c {all|6,7,8,9,10|12,13|15,16}
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

```c {all|4|5,11,12,13|all}
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

If supported, tries to read from cache.
If not, or if cache miss, attempts to read register. If successful, then
also writes result in cache.

---
title: The *regmap_write* function
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

Basically the same as `regmap_read`: checks alignment, locks, calls internal
`_regmap_write`, unlocks.

---
level: 2
title: The internal *_regmap_write*
---

# The internal `_regmap_write`

````md magic-move

```c {all|6,7|9,10,17|9,11,12,17|9,13,14,15,16,17}
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

```c {all|4|all}
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

If caching is not bypassed or deferred, writes in cache.
Then, writes in the actual hardware register.

---
layout: default
---

# Freeing

<div class="center">

If you use `devm_` to initialise your regmap, devres will free the allocated
space for you.

And to know more about how this works... you can take a look at our presentation
about devres! :)

</div>
---
layout: last-slide
hideInToc: true
---

