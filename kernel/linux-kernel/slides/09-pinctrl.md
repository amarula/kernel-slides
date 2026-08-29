---
layout: section
hideInToc: true
---
# Pin muxing (pinctrl)

---
layout: default
---
# What is pin muxing?

- Modern SoCs have more hardware blocks than available pins — not all functions can be exposed
  simultaneously.
- **Pins are multiplexed**: they expose the function of block A *or* block B.
- The multiplexing is usually **software configurable**.
---
layout: default
hideInToc: true
---
# What is pin muxing?

<div style="text-align:center;">
  <img src="/images/pin-muxing.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# pinctrl subsystem

- Since Linux 3.2, a **pinctrl** subsystem (`drivers/pinctrl/`) handles pin muxing:
  - A **pin muxing driver interface** for SoC-specific drivers.
  - A **consumer interface** for device drivers.
- Most pinctrl drivers provide a DT binding; the muxing is described in the DT
  (`Documentation/devicetree/bindings/pinctrl`).
---
layout: default
hideInToc: true
---
# pinctrl subsystem

<div style="text-align:center;">
  <img src="/images/pinctrl-subsystem.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# pinctrl in the Device Tree

- Consumer devices use `pinctrl-<x>` and `pinctrl-names` properties:
  - `pinctrl-0`, `pinctrl-1`… link to a pin configuration for a given **state**.
  - `pinctrl-names` associates a name to each state; the name `default` is selected automatically.
- Pin configurations are child nodes of the pinctrl device (SoC `.dtsi` or board `.dts`), and are
  referenced via phandles.

```c
i2c0: i2c@11000 {
    pinctrl-names = "default";
    pinctrl-0 = <&pmx_twsi0>;
};
```
