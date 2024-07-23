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
