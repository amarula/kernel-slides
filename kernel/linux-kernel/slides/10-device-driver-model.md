---
layout: section
hideInToc: true
---
# Device & driver model

---
layout: default
---
# The need for a device model

- The kernel runs on many architectures/platforms, so code must be maximally reusable.
- The same USB device driver should work on an x86 PC and an ARM platform, even with different
  USB controllers.
- This requires clean organization: device drivers separated from controller drivers, hardware
  description separated from the drivers.
---
layout: default
hideInToc: true
---
# The need for a device model

<div style="text-align:center;">
  <img src="/images/device-model.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Bus drivers

- The first component of the device model is the **bus driver** — one per bus type (USB, PCI, SPI,
  MMC, I2C…).
- It is responsible for:
  - registering the bus type (`struct bus_type`);
  - registering **adapter drivers** (USB controllers, I2C adapters…) that detect devices;
  - registering **device drivers** that manage the devices;
  - **matching** device drivers against detected devices;
  - defining bus-specific structures (`struct usb_driver`, `struct usb_interface`…).

---
layout: default
---
# sysfs

- The bus/device/driver structures are internal; **sysfs** exports them to user space.
- Used by **udev** for automatic module loading, firmware loading, mounting media…
- Usually mounted at `/sys`:
  - `/sys/bus/` — list of buses.
  - `/sys/devices/` — list of devices.
  - `/sys/class/` — devices grouped by framework (net, input, block…) regardless of bus.

---
layout: default
---
# Example: the USB bus



- Core infrastructure: `drivers/usb/core/` (`struct bus_type` in `driver.c`, registered in `usb.c`).
- Adapter drivers: `drivers/usb/host/` (EHCI, UHCI, OHCI, XHCI…).
- Device drivers: everywhere, classified by type (`drivers/net/usb/`).
---
layout: default
hideInToc: true
---
# Example: the USB bus

<div style="text-align:center;">
  <img src="/images/usb-bus.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Device identifiers & registration

```c
static struct usb_device_id rtl8150_table[] = {
    { USB_DEVICE(VENDOR_ID_REALTEK, PRODUCT_ID_RTL8150) },
    { USB_DEVICE(VENDOR_ID_MELCO, PRODUCT_ID_LUAKTX) },
    [...]
    {}
};
MODULE_DEVICE_TABLE(usb, rtl8150_table);

static struct usb_driver rtl8150_driver = {
    .name = "rtl8150",
    .probe = rtl8150_probe,
    .disconnect = rtl8150_disconnect,
    .id_table = rtl8150_table,
};

module_usb_driver(rtl8150_driver);
```

- `MODULE_DEVICE_TABLE()` lets `depmod` extract device↔driver relationships so udev can
  auto-load drivers.

---
layout: default
---
# probe() and disconnect()

- The `probe()` method runs for each device bound to the driver; it receives a bus-specialized
  device structure (`struct usb_interface`, `struct pci_dev`…) and is responsible for:
  - initializing the device, mapping I/O memory, registering interrupt handlers;
  - registering the device to the right kernel framework (e.g. the network infrastructure).
- The `disconnect()`/`remove()` method unregisters and shuts the device down.

---
layout: default
---
# The model is recursive

Drivers combine a **bus infrastructure** (device model) and a **framework**; buses can be stacked
(USB device → I2C adapter → I2C device), so the model nests recursively:

```
ALSA / Network Stack / IIO       ← frameworks
  ↑ (register to)
USB Device Driver / I2C Adapter Driver / Network Driver
  ↑ (bus core)
USB Core / I2C Core / PCI Core
```

---
layout: default
---
# Platform devices

- A huge family of non-discoverable devices live directly in a SoC: UART, Ethernet, SPI/I2C
  controllers, graphics, audio…
- The **platform bus** handles such devices (controlled through memory-mapped registers).
- It works like any other bus, but devices are **enumerated statically** rather than discovered.

```c
static struct platform_driver serial_imx_driver = {
    .probe   = serial_imx_probe,
    .remove  = serial_imx_remove,
    .id_table = imx_uart_devtype,
    .driver  = {
        .name = "imx-uart",
        .of_match_table = imx_uart_dt_ids,
        .pm   = &imx_serial_port_pm_ops,
    },
};
module_platform_driver(serial_imx_driver);
```

---
layout: default
---
# Platform devices & resources

- Platform devices are instantiated statically: legacy `struct platform_device` lists, or (current
  way) by parsing a Device Tree.
- Resources come through a `struct resource` array (I/O addresses, IRQs), subsystem APIs
  (`clk_get()`, `gpio_request()`, `dma_request_channel()`), or direct DT lookups:
  ```c
  res = platform_get_resource(pdev, IORESOURCE_MEM, 0);
  sport->rxirq = platform_get_irq(pdev, 0);
  ```
- Per-compatible driver data via `.data` in `of_device_id` + `of_device_get_match_data()`.

---
layout: default
---
# Driver data structures and links



- Three structures: **bus device** (embeds `struct device`), **framework device** (may embed one),
  and **driver private data** (holds references to both).
- Use `dev_set_drvdata()` / `dev_get_drvdata()` (bus) and `container_of()` (embedded framework
  device) to link them.
---
layout: default
hideInToc: true
---
# Driver data structures and links

<div style="text-align:center;">
  <img src="/images/driver-data-links.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
