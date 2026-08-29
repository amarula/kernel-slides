#!/usr/bin/env python3
"""Generate draw.io (.drawio) diagrams for the Linux kernel deck."""
import os, html

OUT = os.path.expanduser("~") + "/work/michael/kernel-slides/kernel/linux-kernel/diagrams"

# Palette
BLUE   = "#5d8392"
BLUE_D = "#3d5b66"
LIGHT  = "#dce8ec"
WHITE  = "#ffffff"
YELLOW = "#fdcb0b"
DARK   = "#1f2937"
GRAY   = "#9aa7af"
GREEN  = "#7ba37b"
RED    = "#c96a6a"
PURPLE = "#8f7bb8"
ORANGE = "#d99a5b"

def esc(s):
    return html.escape(str(s), quote=True)

class D:
    def __init__(self, name, w=900, h=520):
        self.name = name
        self.w = w
        self.h = h
        self.cells = []
        self.nid = 2

    def id(self):
        i = self.nid
        self.nid += 1
        return str(i)

    def box(self, x, y, w, h, text, fill=LIGHT, stroke=BLUE, font=DARK,
            bold=False, rounded=True, size=13, align="center", dashed=False,
            extra="", white=True, italic=False, raw=False):
        style = f"rounded={'1' if rounded else '0'};whiteSpace=wrap;html=1;" \
                f"fillColor={fill};strokeColor={stroke};fontColor={font};" \
                f"fontSize={size};align={align};verticalAlign=middle;"
        if bold:
            style += "fontStyle=1;"
        if italic:
            style += "fontStyle=2;"
        if dashed:
            style += "dashed=1;"
        if extra:
            style += extra
        cid = self.id()
        val = text if raw else esc(text)
        self.cells.append(
            f'<mxCell id="{cid}" value="{val}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return cid

    def label(self, x, y, w, h, text, size=12, fill="none", font=DARK,
              bold=False, align="center", italic=False, extra="", stroke="none",
              bg=False):
        if bg:
            fill = "#ffffff"
            stroke = "#ffffff"
        style = f"text;html=1;align={align};verticalAlign=middle;fontSize={size};whiteSpace=wrap;"
        if bold:
            style += "fontStyle=1;"
        if italic:
            style += "fontStyle=2;"
        style += f"fontColor={font};fillColor={fill};strokeColor={stroke};"
        style += "resizable=0;"
        if extra:
            style += extra
        cid = self.id()
        self.cells.append(
            f'<mxCell id="{cid}" value="{esc(text)}" style="{style}" vertex="1" parent="1">'
            f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry"/></mxCell>')
        return cid

    def edge(self, x1, y1, x2, y2, color=BLUE, w=2, arrow="block", dashed=False,
             label=None, lx=None, ly=None, lw=None, lh=22, label_size=11,
             label_font=DARK, label_bold=False, exit_=None, entry_=None):
        style = f"endArrow={arrow};html=1;strokeColor={color};strokeWidth={w};rounded=0;"
        if dashed:
            style += "dashed=1;"
        if exit_:
            style += f"exitX={exit_[0]};exitY={exit_[1]};exitDx=0;exitDy=0;"
        if entry_:
            style += f"entryX={entry_[0]};entryY={entry_[1]};entryDx=0;entryDy=0;"
        cid = self.id()
        self.cells.append(
            f'<mxCell id="{cid}" value="" style="{style}" edge="1" parent="1">'
            f'<mxGeometry relative="1" as="geometry">'
            f'<mxPoint x="{x1}" y="{y1}" as="sourcePoint"/>'
            f'<mxPoint x="{x2}" y="{y2}" as="targetPoint"/></mxGeometry></mxCell>')
        if label:
            if lw is None:
                lw = max(36, int(len(label) * 6.5) + 18)
            if lx is None:
                lx = (x1 + x2) / 2 - lw / 2
            if ly is None:
                ly = (y1 + y2) / 2 - lh / 2
            self.label(lx, ly, lw, lh, label, size=label_size,
                       bold=label_bold, font=label_font, bg=True)
        return cid

    def render(self):
        m = (f'<mxGraphModel dx="1200" dy="800" grid="1" gridSize="10" guides="1" '
             f'tooltips="1" connect="1" arrows="1" fold="1" page="1" pageScale="1" '
             f'pageWidth="{self.w}" pageHeight="{self.h}" math="0" shadow="0" '
             f'background="none">'
             f'<root><mxCell id="0"/><mxCell id="1" parent="0"/>'
             + "".join(self.cells) + "</root></mxGraphModel>")
        return ('<mxfile host="app.diagrams.net" agent="kernel-slides" version="24.0.0">'
                f'<diagram name="{esc(self.name)}" id="{esc(self.name)}">{m}</diagram></mxfile>')


DIAGRAMS = []

# ---------------------------------------------------------------------------
# 1. kernel-in-system
# ---------------------------------------------------------------------------
d = D("kernel-in-system", 900, 560)
d.label(0, 6, 900, 26, "Linux kernel in the system", size=16, bold=True)
# User space
d.box(40, 60, 820, 130, "", fill="#f3f6f7", stroke=GRAY, rounded=False)
d.label(52, 68, 300, 22, "User space", size=13, bold=True)
d.box(80, 100, 150, 60, "User\napplication A", fill=WHITE)
d.box(300, 100, 150, 60, "User\napplication B", fill=WHITE)
d.box(520, 100, 120, 60, "C library", fill=WHITE)
d.box(680, 100, 130, 60, "Libraries", fill=WHITE)
# kernel
d.box(40, 250, 820, 120, "", fill="#eaf2f4", stroke=BLUE, rounded=False)
d.label(52, 258, 300, 22, "Kernel", size=13, bold=True)
d.box(120, 300, 240, 50, "Linux kernel", fill=BLUE, font=WHITE, bold=True, size=15)
d.label(420, 300, 300, 20, "Call to services", size=11, italic=True)
d.label(420, 322, 300, 20, "Event notification / information exposition", size=11, italic=True)
# hardware
d.box(40, 430, 820, 90, "", fill="#f3f6f7", stroke=GRAY, rounded=False)
d.label(52, 438, 300, 22, "Hardware", size=13, bold=True)
d.box(200, 470, 200, 40, "Hardware devices", fill=WHITE)
d.edge(210, 250, 210, 190, label="system calls", lx=250, ly=205)
d.edge(360, 350, 360, 430, label="manages / interrupts", lx=400, ly=375)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 2. system-call
# ---------------------------------------------------------------------------
d = D("system-call", 760, 480)
d.label(0, 6, 760, 26, "System calls: the kernel/user interface", size=16, bold=True)
d.box(40, 60, 680, 110, "", fill="#f3f6f7", stroke=GRAY, rounded=False)
d.label(52, 66, 300, 20, "User space application", size=13, bold=True)
d.box(90, 96, 280, 50, "open() / read() / write() …\n(C library functions)", fill=WHITE)
d.box(410, 96, 260, 50, "~400 system calls\n(file, net, IPC, mm, timers…)", fill=WHITE)
d.box(40, 230, 680, 120, "", fill="#eaf2f4", stroke=BLUE, rounded=False)
d.label(52, 236, 300, 20, "Kernel", size=13, bold=True)
d.box(160, 272, 200, 46, "System call handler", fill=BLUE, font=WHITE, bold=True)
d.edge(370, 170, 250, 272, label="syscall (trap)", lx=260, ly=200)
d.edge(500, 170, 300, 272, label="", dashed=True)
d.box(420, 272, 220, 46, "Kernel services\n(drivers, mm, scheduler…)", fill=WHITE)
d.edge(360, 295, 420, 295)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 3. dev-model
# ---------------------------------------------------------------------------
d = D("dev-model", 920, 460)
d.label(0, 6, 920, 26, "Linux development model (since 2003)", size=16, bold=True)
d.label(10, 50, 430, 20, "2-week merge window", size=12, bold=True)
d.label(470, 50, 440, 20, "6–10 week bug-fixing period", size=12, bold=True)
d.box(10, 80, 430, 44, "Merge window\n(new features only)", fill=GREEN, font=WHITE, bold=True)
d.box(470, 80, 440, 44, "Bug-fixing period (release candidates)", fill=BLUE, font=WHITE, bold=True)
# timeline
d.box(10, 170, 900, 6, "", fill=DARK, rounded=False)
for i, lab in enumerate(["7.0", "7.1-rc1", "7.1-rc2", "7.1-rc3", "7.1-rc4", "7.1-rc5", "7.1"]):
    x = 20 + i * 128
    d.box(x, 190, 110, 34, lab, fill=LIGHT)
    d.label(x, 226, 110, 20, "", size=10)
d.label(20, 258, 800, 20, "“master” branch (Linus Torvalds)", size=12, italic=True)
d.label(10, 300, 430, 20, "Stable branch (stable team): 7.1.1, 7.1.2 …", size=12, bold=True)
d.box(10, 328, 430, 40, "7.1 stable branch — bug & security fixes only", fill=YELLOW)
d.label(10, 396, 900, 20, "Last release of each year becomes LTS (Long Term Support).", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 4. kernel-build-overview
# ---------------------------------------------------------------------------
d = D("kernel-build-overview", 920, 480)
d.label(0, 6, 920, 26, "Kernel building overview", size=16, bold=True)
d.box(30, 50, 410, 40, "Environment setup and configuration", fill=BLUE, font=WHITE, bold=True)
d.box(480, 50, 410, 40, "Kernel building and deployment", fill=BLUE, font=WHITE, bold=True)
left = [
    ("ARCH=arm", "target architecture"),
    ("CROSS_COMPILE=arm-linux-", "cross-compiler"),
    ("make soc_defconfig", "reference configuration"),
    ("make menuconfig", "customize configuration"),
]
right = [
    ("make", "compile kernel + modules"),
    ("make install", "install the kernel"),
    ("make modules_install", "install modules"),
]
for i, (t, s) in enumerate(left):
    y = 110 + i * 80
    d.box(40, y, 210, 60, f"{t}\n{s}", fill=WHITE)
for i, (t, s) in enumerate(right):
    y = 110 + i * 80
    d.box(520, y, 210, 60, f"{t}\n{s}", fill=WHITE)
d.edge(250, 140, 520, 140)
d.edge(250, 220, 520, 220, label="make", lx=365, ly=198)
d.edge(250, 300, 520, 300)
d.edge(250, 380, 520, 380)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 5. device-tree-flow
# ---------------------------------------------------------------------------
d = D("device-tree-flow", 760, 420)
d.label(0, 6, 760, 26, "Device Tree: from source to blob", size=16, bold=True)
d.box(50, 80, 200, 60, "Device Tree Source\n.dts / .dtsi", fill=WHITE)
d.box(330, 80, 220, 60, "Device Tree Compiler\ndtc (+ C preprocessor)", fill=BLUE, font=WHITE, bold=True)
d.box(630, 80, 90, 60, "Device\nTree Blob\n.dtb", fill=LIGHT)
d.edge(250, 110, 330, 110, label="compiles")
d.edge(550, 110, 630, 110, label="produces")
d.box(50, 220, 260, 50, "Written by a developer\ntree of nodes + properties", fill=WHITE)
d.box(330, 220, 220, 50, "Syntax checking only\n(no semantic validation)", fill=WHITE)
d.box(630, 220, 90, 50, "OS-agnostic,\nfew tens of KB", fill=WHITE)
d.edge(180, 140, 180, 220)
d.edge(440, 140, 440, 220)
d.edge(675, 140, 675, 220)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 6. device-tree-tree
# ---------------------------------------------------------------------------
d = D("device-tree-tree", 860, 620)
d.label(0, 6, 860, 26, "Device Tree overall structure (simplified)", size=16, bold=True)
d.box(20, 60, 820, 46, "/ (root)  —  model, compatible, #address-cells, #size-cells", fill=BLUE, font=WHITE, bold=True)
d.box(40, 140, 220, 40, "cpus { … }", fill=LIGHT)
d.box(290, 140, 220, 40, "memory@80000000 { … }", fill=LIGHT)
d.box(540, 140, 220, 40, "chosen { … }", fill=LIGHT)
d.box(40, 220, 200, 40, "ocp { … }", fill=LIGHT)
d.edge(120, 106, 150, 140)
d.edge(400, 106, 400, 140)
d.edge(650, 106, 650, 140)
d.edge(650, 180, 140, 220)
d.box(60, 300, 200, 40, "intc: interrupt-controller", fill=WHITE)
d.box(290, 300, 180, 40, "usb0: usb@47401300", fill=WHITE)
d.box(500, 300, 200, 40, "l4_per: interconnect", fill=WHITE)
d.edge(140, 260, 160, 300)
d.edge(140, 260, 380, 300)
d.edge(140, 260, 600, 300)
d.box(540, 380, 180, 40, "i2c0: i2c@40012000", fill=WHITE)
d.edge(600, 340, 630, 380)
d.box(560, 460, 220, 40, "eeprom@50 (I2C device)", fill=YELLOW)
d.edge(630, 420, 660, 460)
d.label(80, 560, 720, 20, "Node ≈ device/IP block; properties ≈ device characteristics; phandles point to other nodes.",
        size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 7. pin-muxing
# ---------------------------------------------------------------------------
d = D("pin-muxing", 900, 520)
d.label(0, 6, 900, 26, "Pin muxing", size=16, bold=True)
d.box(60, 80, 120, 40, "GPIO", fill=WHITE)
d.box(60, 160, 120, 40, "UART 3", fill=WHITE)
d.box(60, 240, 120, 40, "SPI 1", fill=WHITE)
d.box(60, 320, 120, 40, "I2C 0", fill=WHITE)
d.box(320, 50, 260, 40, "Pins", fill=BLUE, font=WHITE, bold=True)
d.box(320, 120, 260, 34, "GPIO0", fill=LIGHT)
d.box(320, 180, 260, 34, "UART3 RX / TX", fill=LIGHT)
d.box(320, 240, 260, 34, "SPI1 MISO / MOSI", fill=LIGHT)
d.box(320, 300, 260, 34, "I2C0 SCL / SDA", fill=LIGHT)
for y in (100, 180, 260, 340):
    d.edge(180, y, 320, y + 25)
d.box(620, 120, 130, 40, "Mux", fill=YELLOW, bold=True)
d.box(620, 240, 130, 40, "Mux", fill=YELLOW, bold=True)
d.edge(580, 137, 620, 137)
d.edge(580, 257, 620, 257)
d.edge(685, 160, 685, 240, label="configuration", lx=710, ly=180)
d.box(660, 330, 200, 46, "Configuration registers", fill=WHITE)
d.edge(620, 277, 700, 330)
d.box(300, 420, 300, 46, "SoC — pins are multiplexed\n(software configurable)", fill=LIGHT, bold=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 8. pinctrl-subsystem
# ---------------------------------------------------------------------------
d = D("pinctrl-subsystem", 920, 540)
d.label(0, 6, 920, 26, "pinctrl subsystem", size=16, bold=True)
d.box(60, 60, 200, 46, "Device drivers\n(consumers)", fill=WHITE)
d.box(60, 140, 200, 46, "Device drivers", fill=WHITE)
d.box(60, 220, 200, 46, "Device drivers", fill=WHITE)
d.box(340, 60, 260, 200, "Pinctrl subsystem core\ndrivers/pinctrl/{core,devicetree,\npinconf,pinmux}.c", fill=BLUE, font=WHITE, bold=True)
d.edge(260, 83, 340, 120, label="request pin muxing", lx=280, ly=70)
d.edge(260, 163, 340, 160)
d.edge(260, 243, 340, 200)
d.box(660, 60, 220, 200, "SoC-specific pinctrl driver\ndrivers/pinctrl/pinctrl-*.c", fill=LIGHT)
d.label(660, 100, 220, 20, "pinctrl_ops — list pins/groups", size=11)
d.label(660, 140, 220, 20, "pinmux_ops — control muxing", size=11)
d.label(660, 180, 220, 20, "pinconf_ops — pin configuration", size=11)
d.edge(600, 160, 660, 160, label="pinctrl_desc", lx=620, ly=140)
d.box(340, 300, 260, 46, "SoC .dtsi — provides list of pin groups", fill=WHITE)
d.box(340, 380, 260, 46, "Board .dts — associations pin groups ↔ devices", fill=WHITE)
d.edge(470, 260, 470, 300)
d.edge(470, 346, 470, 380)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 9. device-model
# ---------------------------------------------------------------------------
d = D("device-model", 920, 500)
d.label(0, 6, 920, 26, "Device model: three core data structures", size=16, bold=True)
d.box(60, 70, 240, 60, "struct bus_type\n(USB, PCI, I2C…)", fill=BLUE, font=WHITE, bold=True)
d.box(360, 70, 240, 60, "struct device_driver\n(a driver for a bus)", fill=LIGHT)
d.box(660, 70, 200, 60, "struct device\n(a device on a bus)", fill=LIGHT)
d.edge(300, 100, 360, 100, label="registers", lx=318, ly=80)
d.edge(600, 100, 660, 100, label="binds", lx=618, ly=80)
d.box(360, 190, 240, 60, "struct usb_driver /\nstruct platform_driver /\nstruct i2c_driver", fill=WHITE)
d.box(660, 190, 200, 60, "struct usb_interface /\nstruct platform_device /\nstruct i2c_client", fill=WHITE)
d.label(360, 150, 240, 30, "inherits (specialized)", size=11, italic=True)
d.label(660, 150, 200, 30, "inherits (specialized)", size=11, italic=True)
d.edge(480, 130, 480, 190)
d.edge(760, 130, 760, 190)
d.box(360, 300, 500, 60, "sysfs (/sys) — /sys/bus, /sys/devices, /sys/class", fill=YELLOW)
d.edge(480, 250, 480, 300, label="exported to user space", lx=500, ly=262)
d.label(40, 400, 860, 20, "The kernel uses inheritance to create bus-specialized device/driver structures.", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 10. usb-bus
# ---------------------------------------------------------------------------
d = D("usb-bus", 920, 500)
d.label(0, 6, 920, 26, "USB bus — device model view", size=16, bold=True)
d.box(40, 60, 840, 40, "USB Core — registers the bus_type", fill=BLUE, font=WHITE, bold=True)
d.box(60, 130, 180, 60, "USB Adapter driver A\n(dwc3)", fill=LIGHT)
d.box(300, 130, 180, 60, "USB Adapter driver B\n(dwc2)", fill=LIGHT)
d.box(540, 130, 160, 54, "USB Device driver 1\n(ftdi-sio)", fill=WHITE)
d.box(720, 130, 140, 54, "USB Device driver 2\n(hid-apple)", fill=WHITE)
d.edge(180, 100, 180, 130, label="registers", lx=192, ly=108)
d.edge(420, 100, 420, 130)
d.edge(620, 100, 620, 130)
d.edge(790, 100, 790, 130)
# devices
d.box(60, 260, 180, 44, "USB1 bus", fill=LIGHT)
d.box(300, 260, 180, 44, "USB2 bus", fill=LIGHT)
d.box(540, 240, 80, 40, "DEV1", fill=WHITE)
d.box(640, 240, 80, 40, "DEV2", fill=WHITE)
d.box(720, 240, 80, 40, "DEV3", fill=WHITE)
d.box(540, 330, 80, 40, "DEV4", fill=WHITE)
d.box(640, 330, 80, 40, "DEV5", fill=WHITE)
d.edge(150, 190, 150, 260)
d.edge(390, 190, 390, 260)
d.edge(580, 184, 580, 240)
d.edge(760, 184, 760, 240)
d.edge(540, 280, 390, 282)
d.edge(680, 280, 680, 330)
d.label(300, 410, 300, 30, "Hardware view: devices\nbehind each controller", size=11, italic=True, align="left")
d.label(560, 410, 300, 30, "Device model view: drivers\nmatch detected devices", size=11, italic=True, align="left")
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 11. i2c-bus
# ---------------------------------------------------------------------------
d = D("i2c-bus", 920, 360)
d.label(0, 6, 920, 26, "An I2C bus example", size=16, bold=True)
d.box(60, 70, 160, 70, "Processor", fill=BLUE, font=WHITE, bold=True)
d.box(260, 70, 180, 70, "I2C controller\n(master)", fill=LIGHT)
d.edge(220, 105, 260, 105)
# bus line
d.edge(440, 105, 860, 105, w=2, color=DARK, label="SDA / SCL (two wires)", lx=580, ly=80)
d.box(500, 150, 120, 70, "I2C\ntouchscreen\ncontroller", fill=WHITE)
d.box(640, 150, 120, 70, "I2C GPIO\nexpander", fill=WHITE)
d.box(780, 150, 120, 70, "I2C audio\ncodec", fill=WHITE)
d.edge(560, 105, 560, 150)
d.edge(700, 105, 700, 150)
d.edge(840, 105, 840, 150)
d.box(500, 250, 120, 30, "addr = 0x2C", fill=YELLOW, size=11)
d.box(640, 250, 120, 30, "addr = 0x1A", fill=YELLOW, size=11)
d.box(780, 250, 120, 30, "addr = 0x6E", fill=YELLOW, size=11)
d.label(300, 310, 500, 20, "Each slave is identified by a unique I2C address on the bus.", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 12. char-device
# ---------------------------------------------------------------------------
d = D("char-device", 900, 560)
d.label(0, 6, 900, 26, "From user space to the kernel: character devices", size=16, bold=True)
d.box(30, 50, 840, 170, "", fill="#f3f6f7", stroke=GRAY, rounded=False)
d.label(42, 56, 300, 20, "User space", size=13, bold=True)
d.box(60, 90, 180, 50, "Read Buffer", fill=WHITE)
d.box(60, 160, 180, 50, "Write String", fill=WHITE)
d.box(320, 90, 220, 50, "/dev/foo", fill=YELLOW, bold=True)
d.box(600, 120, 220, 40, "Major / Minor", fill=WHITE)
d.edge(240, 115, 320, 115)
d.edge(240, 185, 320, 130)
d.edge(540, 115, 600, 135)
# divider
d.label(30, 230, 840, 26, "— user space / kernel space boundary —", size=11, italic=True)
d.box(30, 270, 840, 170, "", fill="#eaf2f4", stroke=BLUE, rounded=False)
d.label(42, 276, 300, 20, "Kernel", size=13, bold=True)
d.box(60, 310, 220, 50, "Read Handler\n(read)", fill=WHITE)
d.box(60, 380, 220, 50, "Write Handler\n(write)", fill=WHITE)
d.box(420, 310, 240, 120, "Device\n(character driver)", fill=BLUE, font=WHITE, bold=True)
d.edge(280, 335, 420, 335)
d.edge(280, 405, 420, 390)
d.label(460, 470, 300, 24, "file_operations: open, read, write, ioctl…", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 13. kernel-frameworks
# ---------------------------------------------------------------------------
d = D("kernel-frameworks", 920, 520)
d.label(0, 6, 920, 26, "Kernel frameworks", size=16, bold=True)
for i, name in enumerate(["Application", "Application", "Application"]):
    d.box(60 + i * 280, 50, 200, 40, name, fill="#f3f6f7")
d.box(60, 110, 800, 40, "System Call Interface", fill=GRAY, font=WHITE, bold=True)
for i, name in enumerate(["Character\nDriver", "Framebuffer\nCore", "V4L\nCore", "TTY\nCore", "Block\nCore"]):
    d.box(40 + i * 172, 190, 160, 56, name, fill=BLUE, font=WHITE, bold=True)
for i, name in enumerate(["Framebuffer\nDriver", "V4L\nDriver", "TTY\nDriver", "Serial\nCore", "IDE/SCSI\nCore"]):
    d.box(40 + i * 172, 300, 160, 56, name, fill=LIGHT)
d.label(40, 384, 780, 30, "Drivers plug into a framework API; the framework implements file_operations once for all devices.",
        size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 14. input-subsystem
# ---------------------------------------------------------------------------
d = D("input-subsystem", 860, 560)
d.label(0, 6, 860, 26, "Input subsystem", size=16, bold=True)
d.box(40, 50, 780, 40, "User space application (X.Org / Wayland / evtest)", fill="#f3f6f7")
d.label(40, 100, 780, 22, "— user space / kernel space —", size=11, italic=True)
d.box(40, 130, 780, 40, "System call interface / Character driver API (evdev)", fill=GRAY, font=WHITE, bold=True)
d.box(120, 200, 620, 90, "Input subsystem (input core)\nEvent handlers · drivers/input/{input.c,evdev.c…}", fill=BLUE, font=WHITE, bold=True)
d.box(120, 340, 180, 60, "input driver A", fill=LIGHT)
d.box(340, 340, 180, 60, "input driver B", fill=LIGHT)
d.box(560, 340, 180, 60, "input driver C", fill=LIGHT)
d.edge(210, 290, 210, 340)
d.edge(430, 290, 430, 340)
d.edge(650, 290, 650, 340)
d.label(120, 420, 620, 30, "Device drivers talk to hardware and feed events; event handlers forward them (evdev → /dev/input/eventX).",
        size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 15. misc-subsystem
# ---------------------------------------------------------------------------
d = D("misc-subsystem", 880, 500)
d.label(0, 6, 880, 26, "misc subsystem", size=16, bold=True)
d.box(40, 50, 800, 40, "User space application", fill="#f3f6f7")
d.label(40, 100, 800, 22, "— user space / kernel space —", size=11, italic=True)
d.box(40, 130, 800, 40, "System call interface / Character driver API", fill=GRAY, font=WHITE, bold=True)
d.box(60, 210, 240, 70, "input subsystem", fill=BLUE, font=WHITE, bold=True)
d.box(340, 210, 240, 70, "watchdog subsystem", fill=BLUE, font=WHITE, bold=True)
d.box(620, 210, 200, 70, "misc subsystem", fill=YELLOW, bold=True)
d.box(60, 330, 110, 54, "input\ndriver 1", fill=LIGHT)
d.box(180, 330, 110, 54, "input\ndriver 2", fill=LIGHT)
d.box(340, 330, 110, 54, "watchdog\ndriver A", fill=LIGHT)
d.box(620, 330, 90, 54, "misc\ndriver a", fill=LIGHT)
d.box(720, 330, 90, 54, "misc\ndriver b", fill=LIGHT)
d.label(40, 430, 800, 24, "misc is a thin layer over the character driver API for devices that fit no other framework.",
        size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 16. driver-data-links
# ---------------------------------------------------------------------------
d = D("driver-data-links", 920, 520)
d.label(0, 6, 920, 26, "Driver data structures and links", size=16, bold=True)
d.box(60, 70, 220, 60, "Bus device\n(struct i2c_client,\nstruct usb_interface)", fill=BLUE, font=WHITE, bold=True)
d.box(360, 70, 220, 60, "Framework device\n(struct input_dev,\nstruct rtc_device)", fill=LIGHT)
d.box(660, 70, 200, 60, "Driver private data\n(driver-specific)", fill=YELLOW)
d.label(60, 130, 220, 20, "embeds struct device", size=11, italic=True)
d.label(360, 130, 220, 20, "may embed struct device", size=11, italic=True)
d.edge(170, 130, 170, 300, dashed=True, label="dev_set_drvdata()", lx=40, ly=210)
d.edge(280, 130, 470, 130, label="dev_set_drvdata()", lx=300, ly=110)
d.edge(580, 100, 660, 100, label="stores refs to both", lx=600, ly=80)
d.box(60, 300, 220, 50, "bus callbacks →\ndev_get_drvdata()", fill=WHITE)
d.box(360, 300, 220, 50, "framework callbacks →\ncontainer_of()", fill=WHITE)
d.box(660, 300, 200, 50, "holds *bus_dev, *framework_dev", fill=WHITE)
d.edge(170, 350, 170, 300)
d.edge(470, 350, 470, 300)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 17. memory-32bit
# ---------------------------------------------------------------------------
d = D("memory-32bit", 900, 560)
d.label(0, 6, 900, 26, "Physical vs. virtual memory (32-bit, 3G/1G split)", size=16, bold=True)
d.box(40, 60, 360, 40, "Physical address space", fill=BLUE, font=WHITE, bold=True)
d.box(500, 60, 360, 40, "Virtual address space", fill=BLUE, font=WHITE, bold=True)
d.box(40, 120, 360, 40, "I/O memory", fill=LIGHT)
d.box(40, 180, 360, 80, "RAM\n(ZONE_NORMAL + ZONE_HIGHMEM)", fill=LIGHT)
d.box(500, 120, 360, 40, "0xFFFFFFFF — kernel (1 GiB)\nvmalloc + identity mapping", fill=YELLOW)
d.box(500, 180, 360, 40, "0xC0000000 (PAGE_OFFSET)", fill=WHITE)
d.box(500, 240, 360, 90, "Process n (3 GiB)\n0x00000000", fill="#f3f6f7")
d.box(220, 320, 180, 60, "CPU + MMU", fill=BLUE, font=WHITE, bold=True)
d.edge(300, 260, 300, 320, label="MMU maps", lx=340, ly=270)
d.edge(320, 140, 500, 140, label="", lx=390, ly=130)
d.edge(400, 60, 500, 60, label="")
d.label(80, 470, 760, 26, "Only <1 GiB is directly addressable via kernel virtual addresses; the rest is highmem or used by user space.",
        size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 18. memory-64bit
# ---------------------------------------------------------------------------
d = D("memory-64bit", 900, 560)
d.label(0, 6, 900, 26, "Physical vs. virtual memory (64-bit, 4 KiB pages)", size=16, bold=True)
d.box(40, 60, 360, 40, "Physical address space", fill=BLUE, font=WHITE, bold=True)
d.box(500, 60, 360, 40, "Virtual address space", fill=BLUE, font=WHITE, bold=True)
d.box(40, 120, 360, 40, "I/O memory", fill=LIGHT)
d.box(40, 180, 360, 80, "RAM\n(16 MiB × TiB space)", fill=LIGHT)
d.box(500, 120, 360, 40, "0xFFFFFFFFFFFFFFFF — kernel (256 TiB)\nvmalloc + identity mapping", fill=YELLOW)
d.box(500, 180, 360, 40, "0xFFFF000000000000", fill=WHITE)
d.box(500, 240, 360, 90, "Process n (256 TiB)\n0x0000000000000000", fill="#f3f6f7")
d.box(220, 320, 180, 60, "CPU + MMU", fill=BLUE, font=WHITE, bold=True)
d.edge(300, 260, 300, 320)
d.edge(320, 140, 500, 140)
d.label(80, 470, 760, 26, "Enough address space so the kernel can identity-map all of RAM (no highmem needed).",
        size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 19. kernel-allocators
# ---------------------------------------------------------------------------
d = D("kernel-allocators", 900, 560)
d.label(0, 6, 900, 26, "Kernel memory allocators", size=16, bold=True)
d.box(60, 60, 780, 40, "Some kernel code (drivers, subsystems)", fill="#f3f6f7")
d.box(100, 140, 300, 60, "kmalloc allocator\n(uses SLAB caches)", fill=LIGHT)
d.box(560, 140, 300, 60, "vmalloc allocator\n(non-contiguous memory)", fill=LIGHT)
d.edge(300, 100, 250, 140)
d.edge(600, 100, 710, 140)
d.box(100, 240, 300, 60, "SLAB allocator\ncaches of same-size objects", fill=LIGHT)
d.edge(250, 200, 250, 240)
d.box(100, 340, 300, 60, "Page allocator (buddy)\nphysically contiguous pages 4k, 8k, 16k…", fill=BLUE, font=WHITE, bold=True)
d.edge(250, 300, 250, 340)
d.edge(710, 200, 350, 370, dashed=True, label="large areas", lx=500, ly=260)
d.label(120, 430, 660, 30, "kmalloc → physically contiguous; vmalloc → virtual-only, not suitable for DMA.", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 20. slab-caches
# ---------------------------------------------------------------------------
d = D("slab-caches", 900, 420)
d.label(0, 6, 900, 26, "SLAB allocator: caches of same-size objects", size=16, bold=True)
d.box(40, 60, 360, 40, "4 KiB pages (from page allocator)", fill=LIGHT, bold=True)
d.box(40, 140, 360, 120, "Cache 1 — objects of 512 bytes", fill=WHITE)
d.box(480, 140, 380, 120, "Cache 2 — objects of 1024 bytes", fill=WHITE)
d.edge(220, 100, 220, 140)
d.edge(220, 100, 670, 140)
for x in (60, 140, 220, 300):
    d.box(x, 180, 60, 40, "", fill=GREEN)
for x in (500, 580, 660, 740):
    d.box(x, 180, 100, 40, "", fill="#dce8ec")
d.box(60, 230, 60, 20, "used", fill=GREEN, size=10)
d.box(140, 230, 60, 20, "free", fill="#dce8ec", size=10)
d.label(300, 330, 600, 24, "See /proc/slabinfo — used for frequently-instantiated kernel structures.", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 21. mmio
# ---------------------------------------------------------------------------
d = D("mmio", 880, 440)
d.label(0, 6, 880, 26, "Memory-mapped I/O (MMIO)", size=16, bold=True)
d.box(60, 70, 240, 70, "CPU", fill=BLUE, font=WHITE, bold=True)
d.box(360, 60, 200, 46, "RAM", fill=LIGHT)
d.box(360, 150, 200, 46, "MMIO registers", fill=YELLOW)
d.edge(180, 105, 360, 83)
d.edge(180, 105, 360, 173)
d.box(620, 60, 200, 140, "Physical memory\naddress space\n(one address bus)", fill="#f3f6f7")
d.edge(560, 83, 620, 90)
d.edge(560, 173, 620, 150)
d.label(80, 200, 700, 30, "Same address bus addresses memory and device registers; accessed with normal load/store instructions.",
        size=12, italic=True)
d.label(80, 250, 700, 30, "Access must use accessor functions (readl/writel…) for ordering and endianness.", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 22. ioremap
# ---------------------------------------------------------------------------
d = D("ioremap", 880, 440)
d.label(0, 6, 880, 26, "ioremap() — map I/O memory into virtual space", size=16, bold=True)
d.box(40, 60, 360, 40, "Physical memory address space", fill=BLUE, font=WHITE, bold=True)
d.box(500, 60, 340, 40, "Virtual memory address space", fill=BLUE, font=WHITE, bold=True)
d.box(40, 130, 120, 60, "RAM", fill=LIGHT)
d.box(200, 130, 160, 60, "MMIO registers\n@ 0xAFFEBC00", fill=YELLOW)
d.box(500, 130, 120, 60, "Kernel", fill=LIGHT)
d.box(500, 220, 120, 60, "User", fill="#f3f6f7")
d.box(660, 130, 180, 60, "0xCDEFA000\n(virtual mapping)", fill=YELLOW)
d.edge(280, 160, 660, 160, label="ioremap(0xAFFEBC00, 4096)", lx=360, ly=138, lw=220)
d.label(120, 360, 700, 26, "ioremap() returns a virtual address the CPU can use to access MMIO registers.", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 23. clock-framework
# ---------------------------------------------------------------------------
d = D("clock-framework", 920, 560)
d.label(0, 6, 920, 26, "Common Clock Framework (CCF)", size=16, bold=True)
d.box(40, 60, 260, 90, "Device driver\n(i2c-omap, …)\nuses clk_get(), clk_enable()…", fill=WHITE)
d.box(360, 60, 240, 90, "Clock framework\n(core)", fill=BLUE, font=WHITE, bold=True)
d.edge(300, 105, 360, 105, label="public clock API", lx=318, ly=85)
# clock drivers
d.box(660, 50, 220, 40, "Clock driver: fixed-rate", fill=LIGHT)
d.box(660, 100, 220, 40, "Clock driver: fixed-factor", fill=LIGHT)
d.box(660, 150, 220, 40, "Clock driver: gate", fill=LIGHT)
d.box(660, 200, 220, 40, "Clock driver: mux", fill=LIGHT)
d.box(660, 250, 220, 40, "Clock driver: divider", fill=LIGHT)
d.box(660, 300, 220, 40, "Clock driver: foo / bar", fill=LIGHT)
d.edge(600, 90, 660, 70, label="clk_ops", lx=620, ly=60)
d.edge(600, 120, 660, 120)
d.edge(600, 150, 660, 170)
d.edge(600, 180, 660, 220)
d.edge(600, 210, 660, 270)
d.edge(600, 240, 660, 320)
d.box(360, 220, 240, 60, "Device Tree — describes clocks\nand their relationships", fill=YELLOW)
d.edge(480, 150, 480, 220)
d.label(40, 400, 860, 30, "Provided by base framework vs. clock driver code; drivers/clk/ · debugfs clock tree.", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 24. thread-life
# ---------------------------------------------------------------------------
d = D("thread-life", 920, 520)
d.label(0, 6, 920, 26, "A thread's life (task states)", size=16, bold=True)
d.box(60, 60, 240, 60, "Thread created\n(fork() / pthread_create())", fill=WHITE)
d.box(60, 180, 240, 70, "TASK_RUNNING\n(ready, not running)", fill=GREEN, font=WHITE, bold=True)
d.box(60, 320, 240, 70, "TASK_RUNNING\n(actually running)", fill=GREEN, font=WHITE, bold=True)
d.box(420, 180, 280, 70, "TASK_INTERRUPTIBLE /\nTASK_UNINTERRUPTIBLE /\nTASK_KILLABLE (waiting)", fill=YELLOW)
d.box(420, 360, 280, 60, "EXIT_ZOMBIE\n(terminated, waiting for parent)", fill=RED, font=WHITE, bold=True)
d.edge(180, 120, 180, 180)
d.edge(180, 250, 180, 320, label="elected by scheduler", lx=200, ly=280)
d.edge(300, 215, 420, 215, label="sleeps on wait queue", lx=330, ly=200)
d.edge(420, 250, 250, 250, label="woken up / signal", lx=320, ly=270)
d.edge(300, 215, 560, 380, dashed=True, label="exits", lx=560, ly=300)
d.edge(300, 320, 180, 320, label="preempted", lx=240, ly=340)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 25. softirq-flow
# ---------------------------------------------------------------------------
d = D("softirq-flow", 920, 420)
d.label(0, 6, 920, 26, "Softirq execution flow", size=16, bold=True)
d.box(40, 70, 140, 50, "IRQ12\ntriggered", fill=WHITE)
d.box(40, 150, 140, 50, "IRQ42\ntriggered", fill=WHITE)
d.edge(180, 95, 300, 95, label="IRQs disabled", lx=210, ly=75)
d.edge(180, 175, 300, 175)
d.box(300, 70, 120, 50, "Handler\nIRQ12", fill=BLUE, font=WHITE, bold=True)
d.box(300, 150, 120, 50, "Handler\nIRQ42", fill=BLUE, font=WHITE, bold=True)
d.edge(420, 95, 540, 95, label="IRQs enabled", lx=450, ly=75)
d.edge(420, 175, 540, 175)
d.box(540, 50, 100, 42, "Softirq\nHI_SOFTIRQ", fill=YELLOW)
d.box(540, 120, 100, 42, "Softirq\nNET_RX", fill=YELLOW)
d.box(540, 190, 100, 42, "Softirq\nTASKLET", fill=YELLOW)
d.edge(640, 70, 720, 70)
d.edge(640, 140, 720, 140)
d.edge(640, 210, 720, 210)
d.box(720, 70, 160, 50, "Process foo\n(scheduler)", fill=GREEN, font=WHITE, bold=True)
d.edge(720, 120, 780, 140, label="once all IRQ handlers done,\nsoftirqs run", lx=700, ly=110, lw=180, lh=26)
d.label(60, 300, 800, 30, "Softirqs run with interrupts enabled but before the scheduler — sleeping is not allowed. ksoftirqd handles overflow.",
        size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 26. lock-protection
# ---------------------------------------------------------------------------
d = D("lock-protection", 900, 440)
d.label(0, 6, 900, 26, "Concurrency protection with locks", size=16, bold=True)
d.box(40, 60, 200, 50, "Thread 1", fill=LIGHT, bold=True)
d.box(660, 60, 200, 50, "Thread 2", fill=LIGHT, bold=True)
d.box(40, 150, 200, 50, "Acquire lock", fill=BLUE, font=WHITE, bold=True)
d.box(660, 150, 200, 50, "Acquire lock", fill=BLUE, font=WHITE, bold=True)
d.box(40, 240, 200, 50, "Critical section\n(protected)", fill=GREEN, font=WHITE, bold=True)
d.box(660, 240, 200, 50, "Wait for lock release\n/ try again", fill=YELLOW)
d.box(40, 330, 200, 50, "Release lock", fill=WHITE)
d.edge(140, 110, 140, 150)
d.edge(760, 110, 760, 150)
d.edge(140, 200, 140, 240)
d.edge(760, 200, 760, 240, label="failure", lx=780, ly=215)
d.edge(140, 290, 140, 330)
d.edge(760, 290, 760, 330, dashed=True)
d.edge(140, 355, 760, 265, dashed=True, label="success", lx=440, ly=360)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 27. dma-integration
# ---------------------------------------------------------------------------
d = D("dma-integration", 900, 480)
d.label(0, 6, 900, 26, "DMA integration", size=16, bold=True)
d.box(60, 60, 220, 60, "CPU", fill=BLUE, font=WHITE, bold=True)
d.box(340, 60, 220, 60, "Data cache", fill=LIGHT)
d.box(620, 60, 220, 60, "DMA controller", fill=YELLOW, bold=True)
d.edge(280, 90, 340, 90)
d.edge(560, 90, 620, 90)
d.box(340, 180, 220, 60, "Memory (RAM)", fill=LIGHT)
d.box(620, 180, 220, 60, "Peripheral device", fill=WHITE)
d.edge(450, 120, 450, 180)
d.edge(730, 120, 730, 180)
d.edge(560, 210, 620, 210, label="bus", lx=580, ly=190)
d.label(120, 320, 700, 30, "DMA copies data directly between devices and RAM, without going through the CPU.", size=12, italic=True)
d.label(120, 360, 700, 30, "Cache coherency: flush before DMA reads, invalidate after DMA writes.", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 28. dma-controllers
# ---------------------------------------------------------------------------
d = D("dma-controllers", 920, 460)
d.label(0, 6, 920, 26, "External DMA controller (dmaengine)", size=16, bold=True)
d.box(60, 60, 800, 40, "RAM", fill=LIGHT, bold=True)
d.box(100, 130, 120, 40, "Descriptor + Buffer", fill=WHITE)
d.box(300, 130, 120, 40, "Descriptor + Buffer", fill=WHITE)
d.box(500, 130, 120, 40, "Descriptor + Buffer", fill=WHITE)
d.edge(160, 100, 160, 130)
d.edge(360, 100, 360, 130)
d.edge(560, 100, 560, 130)
d.box(180, 220, 400, 46, "DMA controller", fill=BLUE, font=WHITE, bold=True)
d.edge(160, 170, 300, 220)
d.edge(360, 170, 380, 220)
d.edge(560, 170, 460, 220)
d.box(100, 320, 180, 46, "SPI controller", fill=WHITE)
d.box(360, 320, 180, 46, "Audio interface", fill=WHITE)
d.box(620, 320, 180, 46, "Network controller", fill=WHITE)
d.edge(220, 266, 190, 320)
d.edge(330, 266, 450, 320)
d.edge(450, 266, 710, 320)
d.label(120, 400, 700, 24, "Drivers submit DMA descriptors; each peripheral has FIFOs + request lines.", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 29. dma-descriptors
# ---------------------------------------------------------------------------
d = D("dma-descriptors", 900, 360)
d.label(0, 6, 900, 26, "DMA descriptors (chained)", size=16, bold=True)
for i in range(3):
    x = 60 + i * 270
    d.box(x, 70, 220, 190, "", fill=WHITE)
    d.label(x, 82, 220, 20, "Source", size=11)
    d.label(x, 108, 220, 20, "Destination", size=11)
    d.label(x, 134, 220, 20, "Size", size=11)
    d.label(x, 160, 220, 20, "Configuration", size=11)
    d.label(x, 186, 220, 20, "Next →", size=11, bold=True)
d.edge(280, 165, 330, 165, label="", arrow="block")
d.edge(550, 165, 600, 165, arrow="block")
d.label(60, 300, 780, 24, "Descriptors describe source/destination/size/config and are chained via a next pointer.", size=12, italic=True)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 30. mmap-overview
# ---------------------------------------------------------------------------
d = D("mmap-overview", 900, 480)
d.label(0, 6, 900, 26, "mmap() overview", size=16, bold=True)
d.box(40, 60, 200, 50, "Process", fill=LIGHT, bold=True)
d.box(40, 150, 200, 50, "Virtual address space", fill="#f3f6f7")
d.box(320, 60, 260, 50, "mmap() system call", fill=BLUE, font=WHITE, bold=True)
d.box(660, 60, 200, 50, "Device driver\n(mmap fop)", fill=LIGHT)
d.box(660, 150, 200, 50, "Physical address space", fill="#f3f6f7")
d.box(320, 150, 260, 50, "MMU (page tables)", fill=YELLOW, bold=True)
d.edge(240, 85, 320, 85)
d.edge(580, 85, 660, 85)
d.edge(140, 110, 140, 150)
d.edge(760, 110, 760, 150)
d.edge(580, 175, 660, 175)
d.edge(140, 200, 320, 200)
d.edge(450, 200, 760, 200)
d.label(120, 340, 700, 30, "The driver initializes the mapping with remap_pfn_range(); the MMU maps process virtual → device physical.",
        size=12, italic=True)
DIAGRAMS.append(d)


# ---------------------------------------------------------------------------
# 31. boot-sequence
# ---------------------------------------------------------------------------
d = D("boot-sequence", 920, 220)
d.label(0, 6, 920, 26, "U-Boot boot sequence", size=16, bold=True)
# (name, what it loads, what it initializes, fill, font color)
stages = [
    ("Boot ROM", "loads: SPL (first stage)", "inits: CPU + on-chip SRAM", BLUE, WHITE),
    ("SPL", "loads: U-Boot proper", "inits: DDR (DRAM)", LIGHT, DARK),
    ("U-Boot proper", "loads: kernel image + DTB", "inits: FS, network, drivers", LIGHT, DARK),
    ("Linux kernel", "loads: rootfs (initramfs)", "inits: hardware, runs init", YELLOW, DARK),
]
for i, (name, loads, inits, fill, font) in enumerate(stages):
    x = 40 + i * 215
    d.box(x, 70, 180, 100, f"{name}\n{loads}\n{inits}", fill=fill, font=font)
for i in range(len(stages) - 1):
    d.edge(40 + i * 215 + 180, 120, 40 + (i + 1) * 215, 120)
DIAGRAMS.append(d)

# ---------------------------------------------------------------------------
# 32. cfs-rbtree
# ---------------------------------------------------------------------------
d = D("cfs-rbtree", 760, 400)
d.label(0, 6, 760, 26, "CFS runqueue: red-black tree ordered by vruntime", size=16, bold=True)
d.box(320, 60, 110, 44, "vruntime = 40", fill=LIGHT)
d.box(160, 160, 110, 44, "vruntime = 25", fill=LIGHT)
d.box(490, 160, 110, 44, "vruntime = 60", fill=LIGHT)
d.box(80, 270, 110, 44, "vruntime = 10\n← leftmost", fill=YELLOW, bold=True)
d.box(240, 270, 110, 44, "vruntime = 30", fill=LIGHT)
d.box(410, 270, 110, 44, "vruntime = 50", fill=LIGHT)
d.box(570, 270, 110, 44, "vruntime = 80", fill=LIGHT)
d.edge(375, 104, 215, 160)
d.edge(375, 104, 545, 160)
d.edge(215, 204, 135, 270)
d.edge(215, 204, 295, 270)
d.edge(545, 204, 465, 270)
d.edge(545, 204, 625, 270)
DIAGRAMS.append(d)


def main():
    os.makedirs(OUT, exist_ok=True)
    for d in DIAGRAMS:
        path = os.path.join(OUT, d.name + ".drawio")
        with open(path, "w") as f:
            f.write(d.render())
        print("wrote", path)

if __name__ == "__main__":
    main()
