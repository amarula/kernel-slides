---
layout: section
hideInToc: true
---
# Kernel configuration and building

---
layout: default
---
# Kernel configuration

- The kernel contains thousands of device drivers, filesystem drivers, and network protocols.
- Thousands of options selectively compile parts of the source.
- **Kernel configuration** = defining the set of options you want your kernel built with.
- The set depends on:
  - the target architecture and your hardware (device drivers);
  - the capabilities you want (network, filesystems, real-time) — generic options available on all
    architectures.

---
layout: default
---
# Kernel configuration and build system

- The configuration and build system is based on multiple **Makefiles**; you only interact with
  the top-level Makefile.
- Interaction is through **make targets** (configuration, compilation, installation…).
- Run `make help` to see all available targets.

```bash
cd linux/
make <target>
```

---
layout: default
---
# Specifying the target architecture

- Set `ARCH` to the name of a directory under `arch/`: `ARCH=arm`, `ARCH=arm64`, `ARCH=riscv`…
- By default the build system assumes the host architecture (native build).
- The build system uses `ARCH` to select the target's configuration options and source/headers.

---
layout: default
---
# Choosing a compiler

- The compiler invoked is `$(CROSS_COMPILE)gcc`.
- Needed already at **configuration time** (some options depend on the compiler's capabilities).
- **Native build:** leave `CROSS_COMPILE` undefined.
- **Cross build:** set the prefix, e.g. `CROSS_COMPILE=arm-linux-gnueabi-`.
- Set `LLVM=1` to compile with Clang.

---
layout: default
---
# Specifying ARCH and CROSS_COMPILE

Two ways:

1. On the `make` command line:
   ```bash
   make ARCH=arm CROSS_COMPILE=arm-linux- ...
   ```
   Drawback: easy to forget, screwing up your build and configuration.

2. As environment variables:
   ```bash
   export ARCH=arm
   export CROSS_COMPILE=arm-linux-
   ```
   Drawback: only works in the current shell. Consider a sourced env file (see https://direnv.net/).

---
layout: default
---
# Initial configuration

Start from a configuration that works!

- **Desktop/server:** start from your running kernel's config:
  ```bash
  cp /boot/config-`uname -r` .config
  ```
- **Embedded:** default configurations stored in-tree as minimal files in `arch/<arch>/configs/`.
  - `make help` lists available configurations for your platform.
  - `make foo_defconfig` loads one (erases your current `.config`!).
  - ARM 32-bit: usually one default config per CPU family; ARM 64-bit: one big config to customize.

---
layout: default
---
# Create your own default configuration

- Use `make menuconfig` to change the configuration; saving overwrites `.config` (not in Git).
- When happy, create a minimal default configuration:
  ```bash
  make savedefconfig
  mv defconfig arch/<arch>/configs/myown_defconfig
  ```
- Add the file to Git so others get the same `.config` with `make myown_defconfig`.
- Embedded build systems have their own commands, e.g. `make linux-menuconfig` and
  `make linux-update-defconfig` in Buildroot.

---
layout: default
---
# Built-in or module?

- The kernel image is a single file linking all object files for enabled features.
  - Loaded in memory by the bootloader; all built-in features are available immediately, before
    any filesystem exists.
- Some features (drivers, filesystems) can be built as **modules**:
  - Plugins loaded/unloaded dynamically; each is a separate file in the filesystem.
  - A filesystem is required to use modules — impossible during early boot.

---
layout: default
---
# Kernel option types (Kconfig)

- **`bool`** — `y` (include) or `n` (exclude).
- **`tristate`** — `y`, `m` (module), or `n`.
- **`int`** — integer values.
- **`hex`** — hexadecimal values (e.g. `CONFIG_PAGE_OFFSET=0xC0000000`).
- **`string`** — e.g. `CONFIG_LOCALVERSION=-no-network`, useful to distinguish two kernels.

---
layout: default
---
# Kernel option dependencies

```ini
config B                        config A
    depends on A                    select B
```

- `depends on`: `B` is not visible until `A` is enabled (works well for dependency chains).
- `select`: when `A` is enabled, `B` is enabled too and cannot be disabled (used for hardware
  features or libraries; avoid selecting symbols that have `depends on`).

```ini
config SPI_ATH79
    tristate "Atheros AR71XX/AR724X/AR913X SPI controller driver"
    depends on ATH79 || COMPILE_TEST
    select SPI_BITBANG
    help
      This enables support for the SPI controller present on the
      Atheros AR71XX/AR724X/AR913X SoCs.
```

---
layout: default
---
# Kernel configuration details

- Stored in the `.config` file at the root of the sources.
  - Simple text file, `CONFIG_PARAM=value`, grouped in sections, prefixed with `CONFIG_`.
  - "No" is encoded as `# CONFIG_FOO is not set`.
  - Included by the top-level Makefile; not usually edited by hand (dependencies).

```ini
# CD-ROM/DVD Filesystems
CONFIG_ISO9660_FS=m
CONFIG_JOLIET=y
# CONFIG_UDF_FS is not set
```

---
layout: default
---
# xconfig and menuconfig

- `make xconfig` — graphical interface, file browser, search with `Ctrl+F`. Needs `qtbase5-dev`.
- `make menuconfig` — terminal interface, very efficient; same interface as BusyBox/Buildroot.
  Needs `libncurses-dev`. Alternative: `make nconfig`.

All tools load/save the **same `.config`** and show the **same set of options**.

---
layout: default
---
# make oldconfig

- Useful to **upgrade a `.config`** from an earlier kernel release: it asks values for new
  parameters (unlike `menuconfig`/`xconfig`, which silently set defaults).
- After editing `.config` by hand, run `make oldconfig` to set values for new parameters that
  appeared because of dependency changes.
- Undoing changes: the tools keep a `.config.old` backup — `cp .config.old .config`.

---
layout: default
---
# Kernel compilation

- Only works from the top source directory; don't run as a privileged user.
- Run several jobs in parallel (`make -j$(nproc)`); use **ccache** for faster rebuilds:
  ```bash
  export CROSS_COMPILE="ccache arm-linux-"
  ```
---
layout: default
hideInToc: true
---
# Kernel compilation

<div style="text-align:center;">
  <img src="/images/kernel-build-overview.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Kernel compilation results

- `arch/<arch>/boot/Image` — uncompressed kernel image.
- `arch/<arch>/boot/*Image*` — compressed images (`bzImage` x86, `zImage` ARM, `Image.gz` RISC-V…).
- `arch/<arch>/boot/dts/<vendor>/*.dtb` — compiled Device Tree blobs.
- All kernel modules, spread over the tree, as `.ko` files.
- `vmlinux` — raw uncompressed ELF image, useful for debugging (not for booting).

---
layout: default
---
# Kernel installation

- **Native:** `sudo make install` installs `/boot/vmlinuz-<version>`,
  `/boot/System.map-<version>`, `/boot/config-<version>`, then re-runs the bootloader config.
- **Embedded:** `make install` is rarely used (kernel is a single file; no standard deployment).
  Deployment is manual or via build-system scripts; behavior customizable in
  `arch/<arch>/boot/install.sh`.
- **Modules (native):** `sudo make modules_install` → `/lib/modules/<version>/`
  (`kernel/`, `modules.alias`, `modules.dep`, `modules.symbols`, `modules.builtin`).
- **Modules (embedded):** use `INSTALL_MOD_PATH`:
  ```bash
  make INSTALL_MOD_PATH=<dir>/ modules_install
  ```
- **Cleanup:** `make clean` / `mrproper` / `distclean`, or `git clean -fdx`.
