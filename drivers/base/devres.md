---
# try also 'default' to start simple
theme: ../../template
# random image from a curated Unsplash collection by Anthony
# like them? see https://unsplash.com/collections/94734566/slidev
background:
# some information about your slides, markdown enabled
title: Devres
# apply any unocss classes to the current slide
class: text-center
# https://sli.dev/custom/highlighters.html
highlighter: shiki
# https://sli.dev/guide/drawing
drawings:
  persist: false
# slide transition: https://sli.dev/guide/animations#slide-transitions
transition: slide-left
# enable MDC Syntax: https://sli.dev/guide/syntax#mdc-syntax
mdc: true


layout: cover
---

# DEVRES

## Device Resource Manager

### By Amarula Solutions


Authors: Flavia Caforio, Andrea Calabrese

<!--
The last comment block of each slide will be treated as slide notes. It will be visible and editable in Presenter Mode along with the slide. [Read more in the docs](https://sli.dev/guide/syntax.html#notes)
-->

---
layout: default
---

# Index

<Toc />


---
layout: section
---

# Peripheral mapping
<img src="images/commodore64.jpg"></img>


<!--
You can have `style` tag in markdown to override the style for the current page.
Learn more: https://sli.dev/guide/syntax#embedded-styles
-->

---
layout: default
---

# devres.c

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

---
layout: default
hideInToc: true
---

# devres.c

## devres: a list of devices... literally

The devres library saves devices in a list:

```
struct devres_node {
	struct list_head		entry;
	dr_release_t		    release;
	const char*         name;
	size_t				      size;
};
```

In this list it is possible to:

- Add/Remove entries (devres_add/devres_remove)
- Search for an entry (devres_find)
- Perform operations on all entries (devres_for_each_res)

All functions take a struct device as a parameter

---
layout: default
---

# struct device

- Defined in linux/device.h
- here is the device to register!

It contains data about:

- its kobject
- the parent
- private data
- initial name
- its driver and driver data
- a mutex that synchronizes call to the driver
- power info
- the DMA mask, range map, parameters and pools
- whether it is removable or not


---
layout: default
---

# Example usage

Simple example (thanks for your help ChatGPT)

```

static int __init sample_device_init(void)
{
    // DEVRES: allocate data for the device
    data_buffer = devm_kzalloc(&THIS_MODULE->dev, BUFFER_SIZE, GFP_KERNEL);
    if (!data_buffer) {
        printk(KERN_ERR "Out of memory!\n");
        return -ENOMEM;
    }
    register_chrdev(0, DEVICE_NAME, &fops);
    return 0;
}
```

devm_kzalloc uses kzalloc internally to allocate data and create the resource.

---
layout: default
hideInToc: true
---

# Example usage

Simple example (thanks for your help ChatGPT)

```

static void __exit mio_device_exit(void)
{
    // DEVRES: Deallocating device memory
    devm_kfree(&THIS_MODULE->dev, data_buffer);

    unregister_chrdev(0, DEVICE_NAME);
}
```

devm_kfree uses kfree internally and releases the resource.


---
layout: last-slide
---