---
theme: ../../template
fonts:
  sans: Open Sans
  serif: IBM Plex Serif
  mono: IBM Plex Mono
  weights: '200,400,700'
image: 'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?q=80&w=2069'
transition: slide-left
mdc: true
layout: cover
title: Devfreq
hideInToc: true
---

# DEVFREQ

## A Linux kernel DEVFREQ driver introduction

#### Francesco Nicoletta Puzzillo

---
layout: default
hideInToc: true
---

# Index

<Toc />

---

# DEVFREQ

<div class="center">

- Provides a standard kernel interface for Dynamic Voltage and Frequency
  Switching on arbitrary devices

- Exposes controls for adjusting frequency through sysfs files (like the
  cpufreq subsystem)

- Automatically adjust device frequency by governors (if possible)

</div>

---

# Governors

<div class="center">

But what is a governor?

In order to offer dynamic frequency scaling, devfreq must be able to
tell a "target frequency" to drivers. This is done using governors.

How to decide what frequency should be used? There are different approaches
based on different governors.

</div>

---

# How governors work

Each governor initializes a devfreq_governor struct. For example:
```c
static struct devfreq_governor devfreq_passive = {
	.name = DEVFREQ_GOV_PASSIVE,
	.flags = DEVFREQ_GOV_FLAG_IMMUTABLE,
	.get_target_freq = devfreq_passive_get_target_freq,
	.event_handler = devfreq_passive_event_handler,
};
```

- **name** is the name of the governor
- **get_target_freq** gets the next frequency decided by the governor
- **event_handler** handles the governor event for the governor lifecycle.
- flags can be
  - **DEVFREQ_GOV_FLAG_IMMUTABLE** if the governor is never changeable to
  others
  - **DEVFREQ_GOV_FLAG_IRQ_DRIVEN** if the governor is working with interrupts
  instead of a timer

Call *devfreq_add_governor* to add a governor

---
hideInToc: true

# How governors work

event_handler Callback for DEVFREQ to notify events to governors.
```c
	switch (event) {
	case DEVFREQ_GOV_START:
		devfreq_monitor_start(devfreq);
		break;

	case DEVFREQ_GOV_STOP:
		devfreq_monitor_stop(devfreq);
		break;

	case DEVFREQ_GOV_UPDATE_INTERVAL:
		devfreq_update_interval(devfreq, (unsigned int *)data);
		break;

	case DEVFREQ_GOV_SUSPEND:
		devfreq_monitor_suspend(devfreq);
		break;

	case DEVFREQ_GOV_RESUME:
		devfreq_monitor_resume(devfreq);
		break;

	default:
		break;
	}
```

---

# Adding a DEVFREQ driver

<div class="center">

- Initialize the devfreq_dev_profile struct
  - Implement *_target function to set the frequency
  - Set polling_ms to the timer period
  - Choose a timer type. It can be “deferrable” or “delayed”
- Call the devfreq_add_device() function to create a devfreq instance
- Get clock and OPP table from Devicetree
  - devm_clk_get()
  - dev_pm_opp_of_add_table()

</div>

---
hideInToc: true

# Adding a DEVFREQ driver

Add the device calling devm_devfreq_add_device(device, devfreq_dev_profile,
governor, data)
Choose a Governor between these defaults (or implement your own):

- DEVFREQ_GOV_SIMPLE_ONDEMAND - Chooses frequency based on the recent load on
the device
- DEVFREQ_GOV_PERFORMANCE - Sets the frequency at the maximum available
frequency
- DEVFREQ_GOV_POWERSAVE - Sets the frequency at the minimum available frequency
- DEVFREQ_GOV_USERSPACE - Sets the frequency at the user specified one
- DEVFREQ_GOV_PASSIVE - Sets the frequency based on the frequency of its parent
devfreq device

---

# Sysfs

<div class="center">

DEVFREQ exposes a sysfs interface

```c
DEVICE_ATTR_RW(governor); // governor name
DEVICE_ATTR_RO(available_governors);
DEVICE_ATTR_RO(available_frequencies);
DEVICE_ATTR_RO(target_freq);
DEVICE_ATTR_RO(cur_freq);
DEVICE_ATTR_RW(min_freq);
DEVICE_ATTR_RW(max_freq);
DEVICE_ATTR_RW(trans_stat); // frequency transition statistics
DEVICE_ATTR_RW(polling_interval);
DEVICE_ATTR_RW(timer); // timer type (deferrable or delayed)
```

This can be used to interact with devfreq using the sysfs virtual file system.

</div>

---

# How it all works together

<div class="center">

- *dev_pm_qos_update_request()* sets min and max frequencies
- The timer calls the governor to get the target frequency
  `devfreq->governor->get_target_freq()`
- The governor gets the device load `devfreq_dev_profile->get_dev_status(...)`
  and returns the target frequency to devfreq
- devfreq sets the new device frequency `devfreq->profile->target(...)`

</div>

---
layout: last-slide
---
