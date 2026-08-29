---
layout: section
hideInToc: true
---
# Clocking & power management

---
layout: default
---

# What is a clock?

- A signal that oscillates between 0 and 1 at a certain frequency, supposed constant.
- Acts as the "heartbeat" of the hardware components connected to it, letting them operate
  correctly and, if needed, synchronously with each other.
- It is never perfect: jitter, non-instantaneous switching, etc.
- Usually originates from a **quartz crystal**, which is very precise in frequency response.

---
layout: two-cols-header
---

# A clock signal

::left::

Logically:

<img src="/images/clk-digital.png" style="border-radius:20px; width:350px" />

::right::

Through an oscilloscope:

<img src="/images/clk-osc.png" style="border-radius:20px; width:350px" />

---
layout: two-cols-header
---

# The clock tree

::left::

- The system takes a reference clock (e.g. from a crystal) and generates a **clock tree** to give
  every component the correct frequency.
- This is done by gating, multiplying, dividing and muxing the original source.

::right::

<img src="/images/clk-tree.jpg" style="border-radius:20px; height:370px; margin-left:50px" />

---
layout: default
title: Clock manipulation
---

# Clock gating

- The simplest way to manipulate a clock signal.
- Prevents a clock from reaching components that don't need one at the moment (e.g. turned off).
- Useful because it removes the power consumption from flip-flops switching state.

<img src="/images/clk-gate.png" style="border-radius:20px; width:400px; margin-left:250px" />

---
layout: default
hideInToc: true
---

# Clock dividing

- Dividing the input clock frequency by a given amount.
- A divider can be analog or digital; the latter is most common, handling up to a few GHz.
- Divisions by a power of 2: a simple binary counter.
- Any even integer: a Johnson counter.

<img src="/images/johnson-table.png" style="height:250px; border-radius:10px; margin-left:750px" />
<img src="/images/johnson-counter.png" style="height:250px; border-radius:10px; margin-top:-265px" />

---
layout: default
hideInToc: true
---

# Clock multiplying

- Multiplying the input clock frequency by a given amount.
- Useful to generate a high-frequency clock from a lower oscillator (e.g. a few GHz from 24 MHz).
- Done with a **Phase-Locked Loop** (PLL) together with clock dividers.

<img src="/images/pll-multiplier.png" style="border-radius:10px; height:150px; margin-left:150px" />

- Note: an absolute error in the input clock (e.g. 24 MHz ± 120 kHz) is multiplied with the
  frequency (50× → 1.2 GHz ± 6 MHz).

---
layout: default
hideInToc: true
---

# Clock multiplexing

- A component can need different clock frequencies at different times — achieved by routing
  clock signals through a multiplexer.
- A clock multiplexer usually has $2^n$ input lines, $n$ control lines, and one output line:

<img src="/images/mux.png" style="border-radius:20px; height:120px; background:white; margin-left:320px" />

---
layout: default
---

# The kernel's clock subsystem: a brief history

- Each driver that dealt with clocks had to do it by itself — lots of duplicated,
  platform-specific, incompatible code.
- Because of this, the **Common Clock Framework (CCF)** was born.
- Drivers are now only responsible for populating the framework; the goal is to be able to link
  clocks across different drivers.

---
layout: two-cols-header
---

# The Common Clock Framework

::left::

It introduces a common structure (in `drivers/clk/clk.c`):

```c
struct clk_core {
        const char              *name;
        const struct clk_ops    *ops;
        struct clk_hw           *hw;
        struct module           *owner;
        struct clk_core         *parent;
        const char              **parent_names;
        struct clk_core         **parents;
        u8                      num_parents;
        u8                      new_parent_index;
        [...]
};
```

::right::

And a set of common APIs to operate on a clock node, in `include/linux/clk-provider.h`:

```c
struct clk_ops {
        int       (*prepare)(struct clk_hw *hw);
        void      (*unprepare)(struct clk_hw *hw);
        int       (*is_prepared)(struct clk_hw *hw);
        [...]
        int       (*enable)(struct clk_hw *hw);
        void      (*disable)(struct clk_hw *hw);
        int       (*is_enabled)(struct clk_hw *hw);
        [...]
        int       (*determine_rate)(struct clk_hw *hw,
                                    struct clk_rate_request *req);
        int       (*set_parent)(struct clk_hw *hw, u8 index);
        u8        (*get_parent)(struct clk_hw *hw);
        int       (*set_rate)(struct clk_hw *hw,
                              unsigned long rate,
                              unsigned long parent_rate);
        [...]
        void      (*init)(struct clk_hw *hw);
        [...]
};
```

---
layout: default
hideInToc: true
---

# The Common Clock Framework

- For each clock, only some callbacks must be provided.
  - `prepare`/`unprepare` and `init` are mandatory; only clock gates can `enable`/`disable`;
    a divider supports `set_rate`, etc.
- Drivers populate the framework with clock nodes; specifying the parents list for each node
  generates the clock tree.
- When a callback is called, the correct behavior is propagated through the tree.
  - Calling `set_rate` on a clock that doesn't directly support it parses the tree towards the root
    to perform the operation (re-parenting or setting rates of other nodes).

---
layout: default
hideInToc: true
transition: fade
---

# The Common Clock Framework

- Another example: calling `enable`/`disable` on a clock that doesn't directly support it parses
  the tree until a clock **gate** is found.
- There is an **enable counter** for gates, so a whole section isn't cut off by mistake.
  `enable`/`disable` increment/decrement a counter; the gate only cuts the clock when its counter
  reaches 0.

<img src="/images/disable-animation-1.png" style="border-radius:10px; width:350px; margin-left:200px" />

---
layout: default
hideInToc: true
transition: fade
---

# The Common Clock Framework

- Another example: calling `enable`/`disable` on a clock that doesn't directly support it parses
  the tree until a clock **gate** is found.
- There is an **enable counter** for gates, so a whole section isn't cut off by mistake.
  `enable`/`disable` increment/decrement a counter; the gate only cuts the clock when its counter
  reaches 0.

<img src="/images/disable-animation-2.png" style="border-radius:10px; width:350px; margin-left:200px" />

---
layout: default
hideInToc: true
transition: fade
---

# The Common Clock Framework

- Another example: calling `enable`/`disable` on a clock that doesn't directly support it parses
  the tree until a clock **gate** is found.
- There is an **enable counter** for gates, so a whole section isn't cut off by mistake.
  `enable`/`disable` increment/decrement a counter; the gate only cuts the clock when its counter
  reaches 0.

<img src="/images/disable-animation-3.png" style="border-radius:10px; width:350px; margin-left:200px" />

---
layout: default
hideInToc: true
transition: fade
---

# The Common Clock Framework

- Another example: calling `enable`/`disable` on a clock that doesn't directly support it parses
  the tree until a clock **gate** is found.
- There is an **enable counter** for gates, so a whole section isn't cut off by mistake.
  `enable`/`disable` increment/decrement a counter; the gate only cuts the clock when its counter
  reaches 0.

<img src="/images/disable-animation-4.png" style="border-radius:10px; width:350px; margin-left:200px" />

---
layout: default
hideInToc: true
transition: fade
---

# The Common Clock Framework

- Another example: calling `enable`/`disable` on a clock that doesn't directly support it parses
  the tree until a clock **gate** is found.
- There is an **enable counter** for gates, so a whole section isn't cut off by mistake.
  `enable`/`disable` increment/decrement a counter; the gate only cuts the clock when its counter
  reaches 0.

<img src="/images/disable-animation-5.png" style="border-radius:10px; width:350px; margin-left:200px" />

---
layout: default
hideInToc: true
---

# The Common Clock Framework

- Another example: calling `enable`/`disable` on a clock that doesn't directly support it parses
  the tree until a clock **gate** is found.
- There is an **enable counter** for gates, so a whole section isn't cut off by mistake.
  `enable`/`disable` increment/decrement a counter; the gate only cuts the clock when its counter
  reaches 0.

<img src="/images/disable-animation-6.png" style="border-radius:10px; width:350px; margin-left:200px" />

---
layout: default
---

# Devicetree support

- By declaring every node properly — with its type, properties and all of its parents — the clock
  tree is correctly generated and supported by the CCF without any logic inside the clock
  controller driver itself.
- This allows for clean and modern programming.

---
layout: default
---
# Enabling hardware

To become functional, hardware blocks require:

- **Power** applied (regulators, power domains).
- **Clocks** ticking — blocks on buses (AHB/APB/AXI) need an input clock to respond, otherwise
  you get bus hangs; bus-exposing devices (e.g. SPI) have a second, tunable clock.
- **Resets** released.

---
layout: default
---
# Common Clock Framework (CCF)



- A clock tree from the crystal → PLLs → gates/dividers → devices. Managed by the CCF
  (`drivers/clk/`), shared refcounted resources; DT declares clocks and their associations.
---
layout: default
hideInToc: true
---
# Common Clock Framework (CCF)

<div style="text-align:center;">
  <img src="/images/clock-framework.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Clocks, resets, runtime PM

```c
devm_clk_get(&pdev->dev, "fck");      /* lookup */
clk_prepare_enable(clk);              /* clock should run */
clk_get_rate(clk);  clk_set_rate(clk, rate);
clk_disable_unprepare(clk);
```

- **Resets:** `devm_reset_control_get()`, `reset_control_assert()`, `reset_control_deassert()`.
- **Runtime PM:** per-device idle state with `runtime_suspend/resume/idle` in `struct dev_pm_ops`;
  API `pm_runtime_enable()`, `pm_runtime_get_sync()`, `pm_runtime_put()`, `pm_runtime_disable()`.
  May itself use resets, clocks, and power.

---
layout: default
---

# DEVFREQ

- Provides a standard kernel interface for **Dynamic Voltage and Frequency Scaling** (DVFS) on
  arbitrary devices.
- Exposes controls for adjusting frequency through **sysfs** files (like the cpufreq subsystem).
- Automatically adjusts device frequency using **governors** (if possible).

---
layout: default
hideInToc: true
---

# Governors

To offer dynamic frequency scaling, devfreq must be able to tell a "target frequency" to
drivers — this is done using **governors**. Different approaches exist, based on different
governors.

---
layout: default
---

# How governors work

Each governor initializes a `struct devfreq_governor`:

```c
static struct devfreq_governor devfreq_passive = {
    .name = DEVFREQ_GOV_PASSIVE,
    .flags = DEVFREQ_GOV_FLAG_IMMUTABLE,
    .get_target_freq = devfreq_passive_get_target_freq,
    .event_handler = devfreq_passive_event_handler,
};
```

- **name** — the governor name.
- **get_target_freq** — returns the next frequency decided by the governor.
- **event_handler** — handles the governor's lifecycle events.
- flags: `DEVFREQ_GOV_FLAG_IMMUTABLE` (never changeable), `DEVFREQ_GOV_FLAG_IRQ_DRIVEN`
  (interrupt-driven instead of a timer).

Call `devfreq_add_governor()` to add a governor.

---
layout: default
hideInToc: true
---

# How governors work

`event_handler` — callback for DEVFREQ to notify events to governors:

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
layout: default
---

# Adding a DEVFREQ driver

- Initialize the `struct devfreq_dev_profile`:
  - implement a `*_target` function to set the frequency,
  - set `polling_ms` to the timer period,
  - choose a timer type: "deferrable" or "delayed".
- Call `devfreq_add_device()` to create a devfreq instance.
- Get the clock and OPP table from the Devicetree:
  - `devm_clk_get()`, `dev_pm_opp_of_add_table()`.

---
layout: default
hideInToc: true
---

# Adding a DEVFREQ driver

Add the device with `devm_devfreq_add_device(device, devfreq_dev_profile, governor, data)`.
Choose a governor (or implement your own):

- `DEVFREQ_GOV_SIMPLE_ONDEMAND` — frequency based on recent device load.
- `DEVFREQ_GOV_PERFORMANCE` — always the maximum frequency.
- `DEVFREQ_GOV_POWERSAVE` — always the minimum frequency.
- `DEVFREQ_GOV_USERSPACE` — a user-specified frequency.
- `DEVFREQ_GOV_PASSIVE` — based on the parent devfreq device's frequency.

---
layout: default
---

# Sysfs

DEVFREQ exposes a sysfs interface:

```c
DEVICE_ATTR_RW(governor);              /* governor name */
DEVICE_ATTR_RO(available_governors);
DEVICE_ATTR_RO(available_frequencies);
DEVICE_ATTR_RO(target_freq);
DEVICE_ATTR_RO(cur_freq);
DEVICE_ATTR_RW(min_freq);
DEVICE_ATTR_RW(max_freq);
DEVICE_ATTR_RW(trans_stat);            /* frequency transition stats */
DEVICE_ATTR_RW(polling_interval);
DEVICE_ATTR_RW(timer);                 /* deferrable or delayed */
```

---
layout: default
---

# How it all works together

- `dev_pm_qos_update_request()` sets the min and max frequencies.
- The timer calls the governor to get the target frequency:
  `devfreq->governor->get_target_freq()`.
- The governor gets the device load via `devfreq_dev_profile->get_dev_status(...)`
  and returns the target frequency.
- devfreq sets the new frequency: `devfreq->profile->target(...)`.
