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
