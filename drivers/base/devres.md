---
# try also 'default' to start simple
theme: ../../template
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
background:
fonts:
  sans: Open Sans
  serif: IBM Plex Serif
  mono: IBM Plex Mono
  weights: '200,400,700'
# some information about your slides, markdown enabled
title: Devres
# apply any unocss classes to the current slide
class: text-center
# https://sli.dev/custom/highlighters.html
highlighter: shiki
# https://sli.dev/guide/drawing
drawings:
  persist: false
list-style-type: disc
# slide transition: https://sli.dev/guide/animations#slide-transitions
transition: slide-left
# enable MDC Syntax: https://sli.dev/guide/syntax#mdc-syntax
mdc: true
hideInToc: true

layout: cover
---

# DEVRES

## Device Resource Manager

### By Amarula Solutions


Authors: Flavia Caforio, Andrea Calabrese

<!--
welcome presentation di devres by me and Flavia ..
-->

---
layout: default
hideInToc: true

---

# Index

<Toc />


---
layout: section
---

# Peripheral mapping
<img src="images/commodore64.jpg"></img>

---
layout: default
---

# Overview

## Handle resource management

- Remember to register the device...
- ... and **deregister** it!

## Many devices, many responsabilities!

- Clock
- DMA
- DRM drivers
- GPIO
- I2C (can only add)
- MEM
- ...

<!--
Here start listing what devres does. Tell how important it is!
-->

---
layout: default
hideInToc: true

---

# devres.c

## Wait, there's more!

- Internal string management
- malloc/realloc/free pages
  - Also per-CPU
- Add/Remove actions
  - When plugging in...
  - ... and on cleanup
  - parameters and results through **void***
- Foreach cycles
- Everything is exported under GPL!

<!--
Self-explanatory, linked list with many benefits
-->

### Low level drivers can be simplified a lot by using devres!
---
hideInToc: true
dragPos:
  foo: Left,Top,Width,Height,Rotate
---

# devres.c: a list of devices... literally

<div v-drag="[56,100,430,311]" style="z-index: 0">
```c
struct device {
	struct kobject kobj;
	struct device		*parent;

	struct device_private	*p;

	const char		*init_name; /* initial name of the device */
	const struct device_type *type;
[...]
	struct device_driver *driver;	/* which driver has allocated this
					   device */
	void		*platform_data;	/* Platform specific data, device
					   core doesn't touch it */
	void		*driver_data;	/* Driver data, set and get with
					   dev_set_drvdata/dev_get_drvdata */
	struct mutex		mutex;	/* mutex to synchronize calls to
					 * its driver.
					 */
[...] power info
	u32			id;	/* device instance */
	spinlock_t		devres_lock;
	struct list_head	devres_head;
[...] dma info
	void	(*release)(struct device *dev);
	enum device_removable	removable;
};
```
</div>

<div v-drag="[500,100,470,311]" style="z-index: 0">
It contains many data included:

- its kobject
- the parent
- private data
- initial name
- device type
- its driver and driver data
- a mutex that synchronizes call to the driver
- power info
- the DMA mask, range map, parameters and pools
- whether it is removable or not
</div>

<!--
Focus on structure. it is a tree, kobject is managed, private data allows for
general data passing, remember to point the spinlock for devres!
-->

---
hideInToc: true
dragPos:
  foo: Left,Top,Width,Height,Rotate
---

# `struct device`

The devres library saves devices in a linked list:
- Defined in linux/device.h
- here is the device to register!

Device structure part used by devres:
<div v-drag="[56,250,430,311]" style="z-index: 0">
```c
struct device {
[...]
	spinlock_t		devres_lock;
	struct list_head	devres_head;
[...]
};
```
</div>

<div v-drag="[500,250,470,311]" style="z-index: 0">
In this list it is possible to:

- Add/Remove entries (devres_add/devres_remove)
- Search for an entry (devres_find)
- Perform operations on all entries (devres_for_each_res)
</div>

<!--
Spinlock important: we are in the kernel drivers, no mutexes here
-->

---
layout: default
hideInToc: true
---

# `struct device`

## Wait... was it a tree all along?

- Parent needed
  - if last leaf detached...
  - ...automatically remove everything possible!

After all, devices are still under a tree

<!--
Devices are under a tree: when a device is unplugged, if no leaf is found also
the parents get "unplugged"
-->

---
layout: default
hideInToc: true
---
# Devres structures

```c
struct devres {
	struct devres_node		node;
	/*
	 * Some archs want to perform DMA into kmalloc caches
	 * and need a guaranteed alignment larger than
	 * the alignment of a 64-bit integer.
	 * Thus we use ARCH_DMA_MINALIGN for data[] which will force the same
	 * alignment for struct devres when allocated by kmalloc().
	 */
	u8 __aligned(ARCH_DMA_MINALIGN) data[];
};
```

```c
struct devres_node {
	struct list_head		entry;
	dr_release_t			release;
	const char			*name;
	size_t				size;
};
```

<!--
It's a linked list. dr_release_t manages the release, is a function. Name used
for searching
-->

---
layout: default
---

# Example usage - devres alloc, add, free

Simple driver example
SPI driver
```c {all|7,8}
struct spi_controller *__devm_spi_alloc_controller(struct device *dev,
						   unsigned int size,
						   bool slave)
{
	struct spi_controller **ptr, *ctlr;

	ptr = devres_alloc(devm_spi_release_controller, sizeof(*ptr),
			   GFP_KERNEL);
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
<!--
ctlr is the controller structure on success
-->

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
```

<!--
Allocation of the node for the list. alloc_dr: internal allocation
-->

---
layout: default
hideInToc: true
---

# Devres alloc - `alloc_dr`
```c
static __always_inline struct devres * alloc_dr(dr_release_t release,
						size_t size, gfp_t gfp, int nid)
{
	size_t tot_size;
	struct devres *dr;

	if (!check_dr_size(size, &tot_size))
		return NULL;

	dr = kmalloc_node_track_caller(tot_size, gfp, nid);
	if (unlikely(!dr))
		return NULL;

	/* No need to clear memory twice */
	if (!(gfp & __GFP_ZERO))
		memset(dr, 0, offsetof(struct devres, data));

	INIT_LIST_HEAD(&dr->node.entry);
	dr->node.release = release;
	return dr;
}
```

<!--
allocates device resource, internally
-->

---
layout: default
hideInToc: true
---

# Example usage

Simple driver example
SPI driver
```c {all|12|16}
struct spi_controller *__devm_spi_alloc_controller(struct device *dev,
						   unsigned int size,
						   bool slave)
{
	struct spi_controller **ptr, *ctlr;

	ptr = devres_alloc(devm_spi_release_controller, sizeof(*ptr),
			   GFP_KERNEL);
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

<!--
In this example, the SPI controller first allocates the SPI controller, then
adds it to the device. If the controller allocation failed, then it frees the
allocated SPI release controller structure
-->

---
layout: default
hideInToc: true
---

# Devres add
<v-clicks>
```c {all|3,5|6|7|8|all}
void devres_add(struct device *dev, void *res)
{
	struct devres *dr = container_of(res, struct devres, data);
	unsigned long flags;

	spin_lock_irqsave(&dev->devres_lock, flags);
	add_dr(dev, &dr->node);
	spin_unlock_irqrestore(&dev->devres_lock, flags);
}
```

```c {all|5}
static void add_dr(struct device *dev, struct devres_node *node)
{
	devres_log(dev, node, "ADD");
	BUG_ON(!list_empty(&node->entry));
	list_add_tail(&node->entry, &dev->devres_head);
}
```

<!--
... But what is devres_add? Well, a new node is added!
-->

```c
static inline void __list_add(struct list_head *new,
			      struct list_head *prev, struct list_head *next)
{
	next->prev = new;
	new->next = next;
	new->prev = prev;
	prev->next = new;
}
```
</v-clicks>

<!--
linked list here!
-->
---
layout: default
hideInToc: true
---

# Example usage

Simple driver example
SPI driver
```c {all|18}
struct spi_controller *__devm_spi_alloc_controller(struct device *dev,
						   unsigned int size,
						   bool slave)
{
	struct spi_controller **ptr, *ctlr;

	ptr = devres_alloc(devm_spi_release_controller, sizeof(*ptr),
			   GFP_KERNEL);
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
<!--
Again, now we will focus on free!
-->

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

<!--
It frees the resource, also looking for the container. It also checks if
the container has any node entry, as it should have none. Then it frees also
the container. If there is no resource, then... why are we even calling it?
-->

---
layout: default
---
# Example usage - devres destroy, remove

```c{all|5}
void devm_usb_put_phy(struct device *dev, struct usb_phy *phy)
{
	int r;

	r = devres_destroy(dev, devm_usb_phy_release, devm_usb_phy_match, phy);
	dev_WARN_ONCE(dev, r, "couldn't find PHY resource\n");
}
```

# Devres destroy

```c{all|6}
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

<!--
Destroying a resource lets it delete all the contents and free memory.
-->

---
layout: default
hideInToc: true
---

# Devres remove

```c{all|7|13|8|10}
void * devres_remove(struct device *dev, dr_release_t release,
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

	if (dr)
		return dr->data;
	return NULL;
}
```

<!--
Spinlock to protect the finding of the resource and the deletion
-->

---
layout: default
hideInToc: true
---

# Devres remove - `find_dr`

```c
static struct devres *find_dr(struct device *dev, dr_release_t release,
			      dr_match_t match, void *match_data)
{
	struct devres_node *node;

	list_for_each_entry_reverse(node, &dev->devres_head, entry) {
		struct devres *dr = container_of(node, struct devres, node);

		if (node->release != release)
			continue;
		if (match && !match(dev, dr->data, match_data))
			continue;
		return dr;
	}

	return NULL;
}
```

<!-- the next previous the current previous -->

---
dragPos:
  foo: Left,Top,Width,Height,Rotate
---

# Groups

Grouping devices is useful
- for middle layers
- for managing group policies
- for releasing everything!
<div v-drag="[56,244,420,208]" style="z-index: 0">
the structure:
```c
struct devres_group {
	struct devres_node		node[2];
	void				*id;
	int				color;
	/* -- 8 pointers */
};
```
</div>
<div v-drag="[500,150,420,208]" style="z-index: 0">

Usage:
- devres_open_group() for creating a group
- devres_release_group() for releasing all resources in the group
- devres_remove_group() used when we don't need a group anymore
</div>

---
layout: default
---

# Example usage - devres group

Grouping example from devres.rst:

```c{all|1}
  if (!devres_open_group(dev, NULL, GFP_KERNEL))
	return -ENOMEM;

  acquire A;
  if (failed)
	goto err;

  acquire B;
  if (failed)
	goto err;
  ...

 err:
  devres_release_group(dev, NULL);
  return err_code;
```

You can find the same structure in ```static int i2c_device_probe(struct device *dev)```.
---
dragPos:
  foo: Left,Top,Width,Height,Rotate
hideInToc: true
---

# devres_open_group

<div v-drag="[58,100,406,384]" style="z-index: 0">
```c
void * devres_open_group(struct device *dev, void *id, gfp_t gfp)
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

</div>

<div v-drag="[500,120,406,384]" style="z-index: 0">

- Id can be specified or automatically created by passing NULL.
- In any case, it returns the id.

</div>

---
layout: default
hideInToc: true
---

# Example usage - devres group

Grouping example from devres.rst:

```c{all|13}
  if (!devres_open_group(dev, NULL, GFP_KERNEL))
	return -ENOMEM;

  acquire A;
  if (failed)
	goto err;

  acquire B;
  if (failed)
	goto err;
  ...

  devres_remove_group(dev, NULL);
  return 0;

 err:
  devres_release_group(dev, NULL);
  return err_code;
```

---
layout: default
hideInToc: true
---
# devres_remove_group
<div style="width:406px">
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
</div>

---
layout: default
hideInToc: true
---

# Example usage - devres group

Grouping example from devres.rst:

```c{all|17}
  if (!devres_open_group(dev, NULL, GFP_KERNEL))
	return -ENOMEM;

  acquire A;
  if (failed)
	goto err;

  acquire B;
  if (failed)
	goto err;
  ...

  devres_remove_group(dev, NULL);
  return 0;

 err:
  devres_release_group(dev, NULL);
  return err_code;
```
---
layout: default
hideInToc: true
---

# devres_release_group

<div style="width:500px">
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
</div>

---
layout: last-slide
---