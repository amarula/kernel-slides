---
# try also 'default' to start simple
theme: seriph
# some information about your slides, markdown enabled
title: Linux kernel
info: |
  ## Focus
  i2c-gpio  


transition: slide-left

---

# What i2c-gpio achieves?

  Key points

---

# What i2c-gpio achieves
<br> Linux kernel driver for bitbanging I2C bus using the GPIO API. <br>
<br>It provides functionality for toggling SDA and SCL lines, handling incomplete I2C transfers, and injecting faults for testing purposes.<br>
<br>The driver supports platform data configuration and works with ACPI and Device Tree setups.<br>


# GPIO API

<br>GPIO API provides functions(all functions starting as gpiod_) to configure, read and write to GPIO pins.<br>

<!--The GPIO API in the I2C GPIO driver context allows the driver to control the GPIO pins that simulate the I2C bus signals. By using functions from this API, the driver can bitbang the I2C protocol, providing a software implementation of I2C communication using general-purpose pins. --> 

---

# What is bit banging?

Bit banging is a method of using software to send and receive signals which would otherwise be done by hardware which in this case would be UART, SPI, I2C

# why we need it here?

<br>Makes platform independent as long as hardware supports GPIO pins<br>
<br>Flexible to work with custom hardware<br>
<br>Flexible to work with systems lacking dedicated hardware controllers<br>

---

# Let's dive into the code

entry point

```ts {all|5|7|7-8|10|all} 
static struct platform_driver i2c_gpio_driver = {
	.driver		= {
		.name	= "i2c-gpio",
		.of_match_table	= i2c_gpio_dt_ids, //Device Tree Match Table
		.acpi_match_table = i2c_gpio_acpi_match, //ACPI Match Table
	},
	.probe		= i2c_gpio_probe,
	.remove_new	= i2c_gpio_remove,
};      

static int __init i2c_gpio_init(void)
{
	int ret;

	ret = platform_driver_register(&i2c_gpio_driver);
	if (ret)
		printk(KERN_ERR "i2c-gpio: probe failed: %d\n", ret);

	return ret;
}
subsys_initcall(i2c_gpio_init);

```
<!--
Populating data inside i2c_gpio_driver struct
Initialization and registration of a platform driver for an I2C GPIO driver in the Linux kernel
-->

---

# I2C GPIO driver code

Start condition for claiming the bus

Step 1 
```ts {all|5|7|7-8|10|all}
i2c_gpio_setsda_val(void *data, int state)
```

Step 2 
```ts {all|5|7|7-8|10|all}
i2c_gpio_setscl_val(void *data, int state)
```

<!--
state - The state to set the SDA pin to (0 for low, 1 for high)
(show image of slight delay scl starts with)

address slaveaddress(client?) 7bit MSB first

what is data here?
-->

---

```ts {all|5|7|7-8|10|all}
i2c_gpio_getsda(void *data)
```
<!--
read the current state of the SDA line
-->
---

```ts {all|5|7|7-8|10|all}
i2c_gpio_getscl(void *data)
```
<!--
read the current state of the SCL line
-->
---

# i2c_gpio_get_properties
<!--
Typically ARM architecture uses device tree and x86 uses ACPI

device_property_read_bool does not have to worry about if it is DT or ACPI

1. Properties are read whether the SDA and SCL lines are open-drain, output-only, or have no pull-up resistors
2. Then, the necessary configuration properties from the firmware (DT or ACPI) are assigned to the driver's platform data structure, enabling the I2C GPIO driver to be properly configured based on the hardware description provided by the system.
-->
---

# i2c_gpio_get_desc

---

# i2c gpio probe

Function that gets called by the kernel to ask the driver to initialize and 
  prepare everything about the device and make it ready to work

```ts {all|5|7|7-8|10|all}
	priv = devm_kzalloc(dev, sizeof(*priv), GFP_KERNEL);
	if (!priv)
		return -ENOMEM;


	adap = &priv->adap;
	bit_data = &priv->bit_data;
	pdata = &priv->pdata;
```
<!--
  allocating mem for driver specific information
Devm functions basically allocates memory in a order resources are allocated and deallocates those memory automatically in a reverse order. The most commonly used allocation flag is GFP_KERNEL means that allocation is performed on behalf of a process running in the kernel space. This means that the calling function is executing a system call on behalf of a process.

priv private data needed for managing the I2C GPIO driver. The primary purpose of these assignments is to make it easier to reference these members without repeatedly dereferencing priv
-->

---

# 
```ts {all|5|7|7-8|10|all}
	if (fwnode) {
		i2c_gpio_get_properties(dev, pdata);
	} else {
		/*
		 * If all platform data settings are zero it is OK
		 * to not provide any platform data from the board.
		 */
		if (dev_get_platdata(dev))
			memcpy(pdata, dev_get_platdata(dev), sizeof(*pdata));
	}
```
<!--
if firmware node available `i2c_gpio_get_properties` is called to retrieve and set the platform-specific data (pdata) for the I2C GPIO driver.
if no fwnode and platform data associated with the device represented by the dev no platform data provided from the board
if device platform data available and no fw node device specific platform data is provided
-->
---
# 

if (pdata->sda/scl_is_open_drain || pdata->sda/scl_has_no_pullup)
	gflags = GPIOD_OUT_HIGH;
	else
		gflags = GPIOD_OUT_HIGH_OPEN_DRAIN;
	priv->sda/scl = i2c_gpio_get_desc(dev, "sda/scl", 1, gflags);
	if (IS_ERR(priv->sda/scl))
		return PTR_ERR(priv->sda/scl)

	if (gpiod_cansleep(priv->sda) || gpiod_cansleep(priv->scl))
		dev_warn(dev, "Slow GPIO pins might wreak havoc into I2C/SMBus bus timing");
	else
		bit_data->can_do_atomic = true;

	bit_data->setsda = i2c_gpio_setsda_val;
	bit_data->setscl = i2c_gpio_setscl_val;

  	if (!pdata->scl_is_output_only)
		bit_data->getscl = i2c_gpio_getscl;
	if (!pdata->sda_is_output_only)
		bit_data->getsda = i2c_gpio_getsda;

<!--
some issue with above code not showing properly on slide, removed formatting now
Configure i2c atomicity based on gpiod is atomic or not
-->
---

# 
```ts {all|5|7|7-8|10|all}
	if (pdata->udelay)
		bit_data->udelay = pdata->udelay;
	else if (pdata->scl_is_output_only)
		bit_data->udelay = 50;			/* 10 kHz */
	else
		bit_data->udelay = 5;			/* 100 kHz */

	if (pdata->timeout)
		bit_data->timeout = pdata->timeout;
	else
		bit_data->timeout = HZ / 10;		/* 100 ms */

	bit_data->data = priv;
  ```

scl output only means slower communication
The line ```bit_data->data = priv;``` is crucial for linking the specific private data structure with the bit-banging algorithm's configuration structure. This allows the algorithm to access any necessary additional data or state information specific to this particular instance of the I2C adapter.
i2c_adapter is the structure used to identify a physical i2c bus along with the access algorithms necessary to access it.

If fwnode is present, the adapter's name is set to the device's name.
If fwnode is absent, the adapter's name is generated using the platform device's ID to ensure it is unique.

---

  Configuring and initializing an I2C adapter in the Linux kernel, ensuring that the adapter is properly linked with its bit-banging algorithm data, classified correctly, associated with its parent device, and linked with the appropriate firmware node. In this setup, the parent device is the platform device representing the hardware providing the GPIOs for the I2C bit-banging bus. This association helps manage the device hierarchy and resource dependencies in the kernel.

  the pdev->id provides a unique identifier for the I2C bus, and the adapter is registered with the I2C core, making the bus available for use by I2C client devices in the system. If registration fails, the error is returned and can be handled appropriately.

  The platform_set_drvdata function is used in the Linux kernel to associate driver-specific data with a platform device. This association allows the driver to retrieve its data structure later, typically in other callback functions, using the platform device structure.

---

  Providing information on SDA and SCL lines used and if clock stretching is used
  (clock stretching)

---

# i2c_gpio_remove

 Adapter is removed

---

```ts {all|5|7|7-8|10|all} 

static const struct of_device_id i2c_gpio_dt_ids[] = {
    { .compatible = "i2c-gpio", },
    { /* sentinel */ }
};

```

<!--
This is for device drivers to match with devices compatible with the I2C GPIO controller driver
-->
