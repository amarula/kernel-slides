---
layout: section
hideInToc: true
---
# misc subsystem

---
layout: default
---
# Why a misc subsystem?

- Many frameworks exist (input, network, video, audio…), but some devices fit **none** of them
  (FPGA devices, other weird devices).
- Such drivers could be raw character drivers (`cdev_init()`/`cdev_add()`), but the **misc
  subsystem** makes it easier:
  - A thin layer above the character driver API.
  - Devices are integrated in the device model (device files in devtmpfs).
---
layout: default
hideInToc: true
---
# Why a misc subsystem?

<div style="text-align:center;">
  <img src="/images/misc-subsystem.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# misc API

```c
int misc_register(struct miscdevice *misc);
void misc_deregister(struct miscdevice *misc);

struct miscdevice {
    int minor;                       /* or MISC_DYNAMIC_MINOR */
    const char *name;                /* device node name */
    const struct file_operations *fops;
    struct list_head list;
    struct device *parent;           /* underlying physical device */
    struct device *this_device;
    const char *nodename;
    umode_t mode;
};
```

- misc devices are regular character devices: `open`/`close`, `read`/`write`, `ioctl`.
