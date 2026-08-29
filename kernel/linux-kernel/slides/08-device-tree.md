---
layout: section
hideInToc: true
---
# Hardware description & Device Tree

---
layout: default
---
# Discoverable vs. non-discoverable hardware

- **Discoverable** (USB, PCI): devices can be enumerated and their characteristics retrieved by
  the bus controller alone.
  - `lsusb`, `lspci` list detected devices.
  - A detected device does not mean a driver is bound to it — matching uses vendor/product ID,
    device class, subclass…
- **Non-discoverable**: needs an explicit description. Historically:
  1. **Compiled C data structures** (old embedded Linux/U-Boot) — not maintainable.
  2. **ACPI tables** (x86 and some ARM64) — provided by firmware.
  3. **Device Tree** (OpenFirmware) — now the standard on embedded architectures (ARM, ARM64,
     RISC-V, PowerPC, MIPS…).

---
layout: default
---
# Device Tree: from source to blob



- A tree data structure describing the hardware is written by a developer in a `.dts`
  (**Device Tree Source**) file.
- Processed by the **`dtc`** compiler (plus a C preprocessor pass) → a `.dtb` (**Device Tree
  Blob**).
- The `.dtb` accurately describes the platform in an OS-agnostic way (a few dozen KB). Once
  loaded in memory it's also called **FDT** (Flattened Device Tree).
---
layout: default
hideInToc: true
---
# Device Tree: from source to blob

<div style="text-align:center;">
  <img src="/images/device-tree-flow.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Device Tree base syntax

- A **tree of nodes**, each with **properties**.
- A node ≈ a device or IP block; properties ≈ device characteristics.
- Notions of **cells** in property values and **phandles** to point to other nodes.
- `dtc` only does **syntax** checking — no semantic validation.
---
layout: default
hideInToc: true
---
# Device Tree base syntax

<div style="text-align:center;">
  <img src="/images/device-tree-tree.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# DT overall structure (example)

```c
/ {
    #address-cells = <1>;
    #size-cells = <1>;
    model = "TI AM335x BeagleBone Black";
    compatible = "ti,am335x-bone-black", "ti,am335x-bone", "ti,am33xx";

    cpus { ... };
    memory@80000000 { ... };
    chosen { ... };

    ocp {
        intc: interrupt-controller@48200000 { ... };
        usb0: usb@47401300 { ... };
        l4_per: interconnect@44c00000 {
            i2c0: i2c@40012000 {
                baseboard_eeprom: eeprom@50 {
                    compatible = "atmel,24c256";
                    reg = <0x50>;
                };
            };
        };
    };
};
```

---
layout: default
---
# Device Tree inheritance

- DT files can be **split and included** into each other. `.dtsi` files are included; `.dts` are
  final trees (only `.dts` is accepted by `dtc`).
- Typically `.dtsi` holds **SoC-level** info common to several boards; the `.dts` holds
  **board-level** info.
- Inclusion **overlays** the including tree over the included tree (in `#include` order), letting
  an including file override values.
- **Labels** (`uart0:`) allow referencing a node later as `&uart0 { status = "okay"; };` — the
  preferred way to tweak a node in a board file.

---
layout: default
---
# Device Tree design principles

- Describe **hardware** (how it is), not configuration (how you use it).
- **OS-agnostic** — the same DT for U-Boot, FreeBSD, or Linux; no need to change it on OS update.
- Describe the **integration** of components, not their internals (internals belong in drivers):
  IRQ lines, DMA channels, clocks, reset lines…
- Like all beautiful principles, sometimes violated.

---
layout: default
---
# The properties

- **Generic**, apply to most nodes (`compatible`, `reg`, `#address-cells`…) — defined in the core
  schema at https://github.com/devicetree-org/dt-schema.
- **Consumer/provider relationships** (`clocks`, `interrupts`, `regulators`…).
- **Subsystem-specific** (`spi-cpha`, `i2c-scl-internal-delay-ns`, `mac-address`…).
- **Vendor/device-specific**, prefixed with `<vendor>,` (`ti,hwmods`, `xlnx,num-channels`…).
- Some are deprecated — watch the bindings!

---
layout: default
---
# The compatible property

- A **list of strings**, from the most specific to the least specific.
- Describes the binding the node complies with; uniquely identifies the device's programming model.
- Used by the OS to **find the appropriate driver**. Typical form: `vendor,model`.
  - `compatible = "arm,armv7-timer";`
  - `compatible = "st,stm32mp1-dwmac", "snps,dwmac-4.20a";`
- Special value `simple-bus`: a bus where all sub-nodes are memory-mapped devices.

---
layout: default
---
# reg and cells

- `reg` is the most important property after `compatible`:
  - **Memory-mapped devices:** base physical address + size (multiple entries allowed).
  - **I2C devices:** the slave address on the bus.
  - **SPI devices:** the chip-select number.
  - The **unit address** (node name after `@`) must match the first `reg` entry.
- Property values are **32-bit cells**; the compiler doesn't track entry boundaries. The parent
  declares the formatting with:
  - `#address-cells` — cells used for the address.
  - `#size-cells` — cells used for the size.

---
layout: default
---
# Status and resources

- **`status`**: `okay`/`ok` (device in use) or `disabled` (not in use). In `.dtsi` files, all
  externally-interfaceable devices have `status = "disabled"`, enabled per-board in the `.dts`.
- **Resources** shared by multiple blocks: interrupt lines, clock/reset/DMA controllers.
  - The controller is described as a node (with `#interrupt-cells`, `#clock-cells`, `#dma-cells`).
  - Consumers reference it with phandles:
    ```c
    spi3: spi@4000c000 {
        interrupts = <GIC_SPI 51 IRQ_TYPE_LEVEL_HIGH>;
        clocks = <&rcc SPI3_K>;
        resets = <&rcc SPI3_R>;
        dmas = <&dmamux1 61 0x400 0x05>, <&dmamux1 62 0x400 0x05>;
    };
    ```

---
layout: default
---
# Device Tree bindings & validation

- Bindings describe how a piece of hardware should be described; they are improved through the
  kernel contribution process and reviewed by DT binding maintainers.
- **Legacy:** human-readable `.txt` files (hard to parse). **Current norm:** **YAML** specifications
  (easy for humans and tools).
- Validation:
  - `make dt_binding_check` — verify YAML bindings are valid.
  - `make dtbs_check` — validate DTs against bindings (optionally scope with `DT_SCHEMA_FILES=`).
- YAML structure: `%YAML 1.2`, `$id`, `$schema`, `title`, `maintainers`, `properties`…
  - Types: `boolean`, `$ref: .../uint32`, `string`, `phandle-array`…
  - Constraints: `minimum`/`maximum`, `default`, `minItems`/`maxItems`, `const`, `enum`,
    `oneOf`/`anyOf`/`allOf`, `dependencies`, `required`, `additionalProperties`.
