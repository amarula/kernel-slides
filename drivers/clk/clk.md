---
theme: ../../template
transition: slide-left
mdc: true
layout: cover
hideInToc: true
---

# clk
## An introduction to the clock subsystem
### Patrick Barsanti

---
layout: default
hideInToc: true
---

# Table of contents

<Toc minDepth="1" maxDepth="2"/>

---
layout: default
---

# What is a clock?

- A signal which oscillates between 0 and 1 with a certain frequency, supposed constant.
- Acts as the "heartbeat" of the hardware components connected to it, allowing them to operate correctly and, if needed, synchronously with each other.
- It is never perfect, there are many factors and imperfections at play, like jitter, non-instantaneous switching, etc.
- Usually originates from a quartz crystal, as it is very precise in frequency response.

---
layout: two-cols-header
---

# A clock signal

::left::

Logically:

<img src="/images/clk-digital.png"
     style="border-radius:20px; width:350px" />

::right::

Through an oscilloscope:

<img src="/images/clk-osc.png"
     style="border-radius:20px; width:350px" />

<!--

Note that a clock does not necessarily have to have 50% duty cycle,
so the time it stays high and the time it stays low are not necessarily
the same.

Also, from the oscillator's readings, we can note the imperfections
in the signal, which is never a proper square wave.

-->

---
layout: two-cols-header
---

# The clock tree

::left::

- The system takes a reference clock (e.g. from a crystal) as a
  source and generates a clock tree to give all the components the correct
  frequency clock.
- This is done by gating, multiplying, dividing and muxing the original source.

::right::

<img src="/images/clk-tree.jpg"
     style="border-radius:20px; height:370px; margin-left:50px" />

<div style="font-size:10px; text-align:right">

Image source:
[Silicon Labs](https://silabs.com/)

</div>

---
layout: default
title: Clock manipulation
---

# Clock gating

- The most simple way to manipulate a clock signal.
- Its purpose is to prevent a clock from reaching components which
  do not require one in that moment (e.g. the component is turned off).
- This is useful because it removes the power consumption given by
  flip-flops switching states.

<img src="/images/clk-gate.png"
     style="border-radius:20px; width:400px;
            margin-left:250px" />

<!--

Whenever some part of the system can be shut off, we can "gate" it,
so it no longer effectively receives the clock signal.
In this way, the only power dissipation is given from current leakages,
but not anymore from switching the state of the flip-flops.

So, at the cost of having more complex electronics and some extra control
lines, we are able to consume less power, which is pretty important for
embedded.

-->

---
layout: default
hideInToc: true
---

# Clock dividing

- Dividing the input clock frequency by a given amount.
- A clock divider can be an analog or digital.
  The latter is the most common, handles up to a few GHz.
- In case of divisions by a power of 2, a simple
  [binary counter](https://en.wikipedia.org/wiki/Frequency_divider#Digital)
  can be used.
- For any even integer, a
  [Johnson counter](https://en.wikipedia.org/wiki/Ring_counter#Johnson_counter)
  can be used:

<img src="/images/johnson-table.png"
     style="height:250px; border-radius:10px; margin-left:750px" />

<img src="/images/johnson-counter.png"
     style="height:250px; border-radius:10px; margin-top:-265px" />

<!--

Original frequency -> f

For the binary counter, basically just connecting the n-th bit line
will mean connecting to a clock which is f/(2^n).
The second-least significant bit will be f/2, the third-most f/4,
and so on.

A Johnson counter is basically a series of flip-flops connected
as a shift register, where the negated output of the last one is
connected back as input to the first one. The even integer number for which
you want to divide will be double the number of flip-flops, so the number
of bits in the shift register, because going back to zero takes 2n steps.

-->

---
layout: default
hideInToc: true
---

# Clock multiplying

- Multiplying the input clock frequency by a given amount.
- Useful to generate a high frequency clock starting from a lower
  oscillator (e.g. a few GHz from 24MHz oscillator).
- This is very complex, done with a
  [Phase-Locked Loop](https://en.wikipedia.org/wiki/Phase-locked_loop)
  (PLL) together with clock dividers.
  Interesting, but not in the scope of this presentation.

<img title="PLL Multiplier"
     src="/images/pll-multiplier.png"
     style="border-radius:10px; height:150px; margin-left:150px" />

- Note also that if the input clock has a certain absolute error
  (e.g. 24MHz ± 120KHz), this will be multiplied along with the
  frequency (e.g. 50x multiplier -> 1.2GHz ± 6MHz).

---
layout: default
hideInToc: true
---

# Clock multiplexing

- A component can need different clock frequencies at different times.
  This is achieved by having clock signals routed towards it through a
  multiplexer.
- A clock multiplexer usually has $2^n$ input lines,
  $n$ control lines, and one output line:

<img title="Multiplexer"
     src="/images/mux.png"
     style="border-radius:20px; height:120px;
            background:white; margin-left:320px" />

---
layout: default
---

# The kernel's clock subsystem: a brief history

- Each driver in the linux kernel which had to deal with clocks
  and related objects had to do it by itself.  
  This brought a lot of duplicated, platform-specific and
  incompatible code.
- Because of this, the Common Clock Framework (CCF) was born.
- Drivers are now only responsible for populating the framework,
  and the goal is to be able to link clocks across different drivers.

---
layout: two-cols-header
---

# The Common Clock Framework

::left::

<div style="margin-right:50px">

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

</div>

::right::

And introduces a set of common APIs to operate on a clock node,
in `include/linux/clk-provider.h`:
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

<!--

Note that clocks in the linux kernel have so-called parents,
which can be more than one, because of the clock muxing we spoke
about earlier.

Re-parenting a clock means changing the muxes in order to be attached
to a different clock node.

clk_ops in the linux kernel are more than 20.
In u-boot, on the other hand, this is simplified. There are only 9,
and some that are shown are not even present.

-->

---
hideInToc: true
---

# The Common Clock Framework

- For each clock, some (not all) of the callback functions must be provided.
  - For example `prepare`/`unprepare` and `init` are mandatory,
    however only clock gates can `enable`/`disable`, a clock divider
    supports `set_rate`, etc.
- Drivers will populate the framework with clock nodes, and by specifying
  the parents list for each node, the clock tree will be generated.
- When one of the callbacks for a clock node is called, the correct
  behaviour will be propagated through the clock tree and will affect all
  other clocks that are supposed to be affected.
  - For example by calling `set_rate` on a clock which does not directly
    support it, the tree will be parsed towards the root to perform that
    operation, for example by re-parenting or setting rates of other
    clock nodes.

---
hideInToc: true
transition: fade
---

# The Common Clock Framework

- Another example: by calling `enable`/`disable` on a clock node which
  does not directly support it, the tree will be parsed until a clock
  gate is found.  
  There is an enable counter for gates which makes sure that
  a whole section is not cut off from receiving a clock by mistake.
  So, `enable`/`disable` basically increment/decrement a counter;
  before that gate cuts off the clock signal to all the clock nodes
  connected to it, its counter must reach 0.

<img src="/images/disable-animation-1.png"
     style="border-radius:10px; width:350px; margin-left:200px" />

---
hideInToc: true
transition: fade
---

# The Common Clock Framework

- Another example: by calling `enable`/`disable` on a clock node which
  does not directly support it, the tree will be parsed until a clock
  gate is found.  
  There is an enable counter for gates which makes sure that
  a whole section is not cut off from receiving a clock by mistake.
  So, `enable`/`disable` basically increment/decrement a counter;
  before that gate cuts off the clock signal to all the clock nodes
  connected to it, its counter must reach 0.

<img src="/images/disable-animation-2.png"
     style="border-radius:10px; width:350px; margin-left:200px" />

---
hideInToc: true
transition: fade
---

# The Common Clock Framework

- Another example: by calling `enable`/`disable` on a clock node which
  does not directly support it, the tree will be parsed until a clock
  gate is found.  
  There is an enable counter for gates which makes sure that
  a whole section is not cut off from receiving a clock by mistake.
  So, `enable`/`disable` basically increment/decrement a counter;
  before that gate cuts off the clock signal to all the clock nodes
  connected to it, its counter must reach 0.

<img src="/images/disable-animation-3.png"
     style="border-radius:10px; width:350px; margin-left:200px" />

---
hideInToc: true
transition: fade
---

# The Common Clock Framework

- Another example: by calling `enable`/`disable` on a clock node which
  does not directly support it, the tree will be parsed until a clock
  gate is found.  
  There is an enable counter for gates which makes sure that
  a whole section is not cut off from receiving a clock by mistake.
  So, `enable`/`disable` basically increment/decrement a counter;
  before that gate cuts off the clock signal to all the clock nodes
  connected to it, its counter must reach 0.

<img src="/images/disable-animation-4.png"
     style="border-radius:10px; width:350px; margin-left:200px" />

---
hideInToc: true
transition: fade
---

# The Common Clock Framework

- Another example: by calling `enable`/`disable` on a clock node which
  does not directly support it, the tree will be parsed until a clock
  gate is found.  
  There is an enable counter for gates which makes sure that
  a whole section is not cut off from receiving a clock by mistake.
  So, `enable`/`disable` basically increment/decrement a counter;
  before that gate cuts off the clock signal to all the clock nodes
  connected to it, its counter must reach 0.

<img src="/images/disable-animation-5.png"
     style="border-radius:10px; width:350px; margin-left:200px" />

---
hideInToc: true
---

# The Common Clock Framework

- Another example: by calling `enable`/`disable` on a clock node which
  does not directly support it, the tree will be parsed until a clock
  gate is found.  
  There is an enable counter for gates which makes sure that
  a whole section is not cut off from receiving a clock by mistake.
  So, `enable`/`disable` basically increment/decrement a counter;
  before that gate cuts off the clock signal to all the clock nodes
  connected to it, its counter must reach 0.

<img src="/images/disable-animation-6.png"
     style="border-radius:10px; width:350px; margin-left:200px" />
