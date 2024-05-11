---
theme: ../template
fonts:
  sans: Open Sans
  serif: IBM Plex Serif
  mono: IBM Plex Mono
  weights: '200,400,700'
image: 'https://images.unsplash.com/photo-1517077304055-6e89abbf09b0?q=80&w=2069'
transition: slide-left
mdc: true
layout: cover
hideInToc: true
---

# Open source contributions
# tips and trick
### Dario Binacchi

---
layout: default
hideInToc: true
---

## Table of contents

<Toc minDepth="1" maxDepth="2"/>

---
layout: default
---

# Why contribute to FOSS projects?

- Learn New Skills, Tools & Technologies
- It is Fun and gives you Personal Satisfaction
- Meet New People
- Improve Your Communication Skills
- Build Confidence
- Build Your Reputation
- Design, develop and fix once we are developers, we are lazy

---
layout: default
hideInToc: true
---

# Why contribute to FOSS projects?

For me:
- It's fun, it's a source of inspiration and satisfaction
- I don't like to think that everything I've developed in my life can be lost without
having had a chance to be useful for someone else

**Tip:**

- Take the time to find out what your motivations are. It will help you choose
the project and community that is right for you

---
layout: default
---

# So where to start from ?

- Choose a project. Better to start with a familiar one
- Download the source tree
- Read the documentation. Some bash commands can help you:

```bash
find ./ -iname "*contrib*" -or -iname "*coding*" -or -iname "*style*"
grep -ri contrib
grep -Eri 'submit.*patch'
grep -Eri 'coding.*style'
```

---
layout: default
hideInToc: true
---

# So where to start from ?

- Read the documentation.
  Examples:
  - Busybox: docs/\{contributing.txt,style-guide.txt\}
  - Buildroot: docs/manual/contribute.txt
  - Linux: Documentation/process/\{coding-style.rst,submitting-patches.rst\}
  - U-Boot: doc/develop folder
  - Zephyr: doc/contribute/guidelines.rst

---
layout: default
---

# Subscribe to the mailing list

Follow the discussions of your interest and try to get as much info as possible in order to understand:
- How the thread develops (timings, idioms, behaviors adopted, ...)
- How to ask
- How to answer
- How and where to get additional info
- Who are the most active people
- The rules of the community/subsystem

---
layout: default
---

# Subscribe to patchwork, gerrit or …

- Patches that have been sent to a mailing list are caught by the system, and appear on a web page
- Useful for both maintainers and contributors
- Any comments posted that reference the patch are appended to the patch page
- Assign each patch a delegate (he merge or reject the patch)
- Assign each patch a state (Accepted, Rejected, Under Review ...)

---
layout: default
hideInToc: true
---

# Subscribe to patchwork, gerrit or …

- Check if your project is in the list of softwares managed by patchwork,
gerrit or what else.
It's far easier to understand how the patch review is going.
- Used for Buildroot, Linux and U-Boot  
  **https://patchwork.ozlabs.org/project/buildroot/list/**  
  **https://patchwork.ozlabs.org/project/uboot/list/**  
  **https://patchwork.kernel.org/**  

---
layout: default
---

# Set up the development environment

- Compiler
- Debugger
- Testing framework
- Are you an embedded developer?
  - You need a board or an hardware emulator
  - Lot of cheap and popular hardware devices I started with a beaglebone black
  - Even a custom board can go well
  - No hardware? try with QEMU
  - Better to use the mainline software version
  - Allows you to test the patch

---
layout: default
hideInToc: true
---

# Set up the development environment

- Text Editor
  - Any text editor for developers is good
  - Set coding style  
  - For Linux like projects
    - Emacs (~/emacs.d/init.el)
    - ; set k&r style
    - (setq c-default-style "k&r")
    - ; indent with 8 spaces
    - (setq c-basic-offset 8)
  - vi[m] (~/.vimrc)
  :set tabstop=8 softtabstop=8 shiftwidth=8 noexpandtab cindent cc=80
  | %retab

---
layout: default
hideInToc: true
---

# Set up the development environment

- Email client
  - Support raw text mode
  - Configure git send email (~/.gitconfig)

```bash
  # I Use Gmail
  [sendemail]
  smtpServer = smtp.gmail.com
  smtpServerPort = 587
  smtpEncryption = tls
  smtpUser = dario.binacchi@amarulasolutions.com
  smtppass = <my-password>
  aliasesfile = ~/git-mailrc
  aliasfiletype = mutt
```

---
layout: default
hideInToc: true
---

# Okay, let's go! what about as a first patch?

<div class="font-small">

- Avoid complex new features at the beginning. At least before you feel confident with the process
- You read documentation. Was there a typo?

My first patch in U-Boot (1 insertion(+))

</div>

```c
commit e198bb51dd55afbeaeb2008c05a5e640fcfe4b3c
Author: Dario Binacchi <dariobin@libero.it>
Date:   Sun Dec 29 13:44:18 2019 +0100

    	tools: .gitignore: add asn1_compiler

    	Add the tool to the ignore list to prevent being marked as unversioned.

    	Signed-off-by: Dario Binacchi <dariobin@libero.it>
    	Reviewed-by: Bin Meng <bmeng.cn@gmail.com>

diff --git a/tools/.gitignore b/tools/.gitignore
index d0176a7283ff..82bdce27829a 100644
--- a/tools/.gitignore
+++ b/tools/.gitignore
@@ -1,3 +1,4 @@
+/asn1_compiler
 	/atmel_pmecc_params
 	/bin2header
 	/bmp_logo
```

---
layout: default
---

# It's time for an example

- Project: U-Boot
- Hardware: BSH SMM S2 board
- Type: BUG

---
layout: default
---

# Patch preparation

- Create the branch
```bash
cd ~/projects/u-boot
git checkout master
git pull
git checkout -b bsh-yet-remove-console-from-bootargs
```
- Edit the file(s) to fix the issue
```bash
emacs include/configs/imx8mn_bsh_smm_s2.h
```
- Commit the change
```bash
git add bsh-yet-remove-console-from-bootargs
# Sign your work
git commit -s
# Commit message template
# subsystem: title
# <empty line>
# Describe what is the purpose of the patch in lines of 75
# characters max
#  <empty line>
#  Signed-off-by: <developer-email>
```

---
layout: default
hideInToc: true
---

# Patch preparation - Tags

- **Signed-off-by**: indicates that the signer was involved in the development of the patch,
or that he/she was in the patch's delivery path
- **Co-developed-by**: states that the patch was co-created by multiple developers. Must be
immediately followed by a Signed-off-by: of the associated co-author
- **Suggested-by**: indicates that the patch idea is suggested by the person named and ensures
credit to the person for the idea
- **Fixes**: indicates that the patch fixes an issue in a previous commit
- **Reported-by**: gives credit to people who find bugs and report them
- **Tested-by**: indicates that the patch has been successfully tested by the person named
- **Reviewed-by**: states that the patch is an appropriate modification
- **Acked-by**: a person who was not directly involved in the preparation or handling of
the patch but wishes to signify and record his approval

---
layout: default
hideInToc: true
---

# Patch preparation - Output

```c
commit ca606ece36afddeaa1ed90a3791f9d404c12d0e5
Author: Dario Binacchi <dario.binacchi@amarulasolutions.com>
Date:   Wed Jan 4 14:08:37 2023 +0100

    configs: imx8mn_bsh_smm_s2: remove console from bootargs

    The Linux kernel device tree already specifies the device to be used for
    boot console output with a stdout-path property under /chosen.

    Commit 36b661dc919da ("Merge branch 'next'") re-added the console
    setting that commit bede82f750752 ("configs: imx8mn_bsh_smm_s2: remove
    console from bootargs") had previously removed.

    Fixes: 36b661dc919da ("Merge branch 'next'")
    Signed-off-by: Dario Binacchi <dario.binacchi@amarulasolutions.com>

diff --git a/include/configs/imx8mn_bsh_smm_s2.h b/include/configs/imx8mn_bsh_s>
index e97b8e871d22..deeed9c2f582 100644
--- a/include/configs/imx8mn_bsh_smm_s2.h
+++ b/include/configs/imx8mn_bsh_smm_s2.h
@@ -14,7 +14,7 @@
 #include <config_distro_bootcmd.h>

 #define NANDARGS \
-       "nandargs=setenv bootargs console=${console} " \
+       "nandargs=setenv bootargs " \
                "${optargs} " \
                "mtdparts=${mtdparts} " \
                "root=${nandroot} " \
```

---
layout: default
hideInToc: true
---

# Patch test

- On hardware
- Trigger CI pipeline
  - <span style="color:red">./.azure-pipelines.yml </span>
  - <span style="color:red">./gitlab-ci.yml </span>
- Run tests locally
  - <span style="color:red">./tools/buildman/buildman -o /tmp -PEWM aarch64 </span>
  - <span style="color:red">./test/py/test.py --bd sandbox --build </span>
  - <span style="color:blue">https://www.mail-archive.com/u-boot@lists.denx.de/msg361820.html </span>

---
layout: default
hideInToc: true
---

# Patch check

- Use patman
- <span style="color:blue">https://github.com/siemens/u-boot/blob/master/tools/patman/README </span>
- Tool to automate patch formatting, check and submission
- Converts a git branch in a set of patches
- Invokes checkpatch.pl to verify the patches  
Useful for any project (Linux too) that uses checkpatch.pl
- patman command line arguments
  - <span style="color:red">patman -n (dry run) </span>
  - <span style="color:red">patman -c (use the n first commits) </span>
  - <span style="color:red">patman -s (skit the first n commits) </span>
- Our example
  - <span style="color:red">./tools/patman/patman -c 1 -n </span>

---
layout: default
hideInToc: true
---

# Patch posting

<div class="font-small">

- Use patman, yes it again
- Behavior controlled by a set of tags in the commits
- Calls get_maintainer.pl to fill cc list (or use tags in commits)
- Reduces an unnecessary source of errors and annoyances versus when it's handed manually
- Patman Tags
  - **Series-to**: email address or alias to send this patch series
  - **Series-cc**: email address or alias to copy this patch series
  - **Series-version**: set the version. Will add a v to the patch subject
  - **Series-prefix**: Set the patches prefix (i.e: RFC or RESEND)
  - **Cover-letter**: Content of the cover letter, fist line is the subject
  - **Series-changes**: Changelog for patch series revision
  - **Commit-notes**: Notes for each commit, appear after “---” cut
  - **Patch-cc**: email address or alias to copy this patch
- For each patch series revision, the output will be consistent

</div>

---
layout: default
hideInToc: true
---

# Patch posting - Tags

```c
commit ca606ece36afddeaa1ed90a3791f9d404c12d0e5 (HEAD -> imx8mn-yet-remove-console-from-bootargs)
Author: Dario Binacchi <dario.binacchi@amarulasolutions.com>
Date:   Wed Jan 4 14:08:37 2023 +0100

    configs: imx8mn_bsh_smm_s2: remove console from bootargs
    
    The Linux kernel device tree already specifies the device to be used for
    boot console output with a stdout-path property under /chosen.

    Commit 36b661dc919da ("Merge branch 'next'") re-added the console
    setting that commit bede82f750752 ("configs: imx8mn_bsh_smm_s2: remove
    console from bootargs") had previously removed.

    Fixes: 36b661dc919da ("Merge branch 'next'")
    Signed-off-by: Dario Binacchi <dario.binacchi@amarulasolutions.com>

    Patch-cc: amarula
    Series-cc: Tom Rini <trini@konsulko.com>,
    Series-cc: Stefano Babic <sbabic@denx.de>,
    Series-cc: Fabio Estevam <festevam@gmail.com>

diff --git a/include/configs/imx8mn_bsh_smm_s2.h b/include/configs/imx8mn_bsh_smm_s2.h
index e97b8e871d22..deeed9c2f582 100644
--- a/include/configs/imx8mn_bsh_smm_s2.h
+++ b/include/configs/imx8mn_bsh_smm_s2.h
@@ -14,7 +14,7 @@
 #include <config_distro_bootcmd.h>

 #define NANDARGS \
-       "nandargs=setenv bootargs console=${console} " \
+       "nandargs=setenv bootargs " \
                "${optargs} " \
                "mtdparts=${mtdparts} " \
                "root=${nandroot} " \
```

---
layout: default
hideInToc: true
---

# Patch posting - Output

```console
tools/patman/patman -c 1 -n
# Dry run, so not doing much. But I would do this:

Send a total of 1 patch with no cover letter.
0001-configs-imx8mn_bsh_smm_s2-remove-console-from-bootar.patch
Cc:  Ariel D'Alessandro <ariel.dalessandro@collabora.com>
Cc:  Michael Trimarchi <michael@amarulasolutions.com>
Cc:  linux-amarula@amarulasolutions.com
Cc:  u-boot@lists.denx.de
Cc:	 Fabio Estevam <festevam@gmail.com>
Cc:	 Stefano Babic <sbabic@denx.de>
Cc:	 Tom Rini <trini@konsulko.com>
Version:  None
Prefix:	  None
Postfix:	  None
Git command: git send-email --annotate --cc "Stefano Babic <sbabic@denx.de>" --cc "Fabio Estevam <festevam@gmail.com>"  
--cc "Tom Rini <trini@konsulko.com>" --cc-cmd "tools/patman/patman send --cc-cmd /tmp/patman.385629"  
0001-configs-imx8mn_bsh_smm_s2-remove-console-from-bootar.patch

# Post the patch
tools/patman/patman -c 1
```

---
layout: default
---

# Getting feedback - Answer

- Give maintainers at least a week to answer, better 2
- Use patchwork to get info on patch status
- If the maintainer is active only in some time windows, try to be reactive,  
but always and only after doing your homework. We are technicians, but we  
are also human. You will learn to understand the maintainer's preferences  
on how communication should take place

---
layout: default
hideInToc: true
---

# Getting feedback - Answer

- Always answer the emails in-line
- Be polite, be respectful
  - You can disagree with the review
  - Use facts
  - Address the problem
- When discussing your patches remove unnecessary context from the email
- People don’t want to scroll hundred of lines to read an answer of a couple of lines
- Do not post attachments

---
layout: default
hideInToc: true
---

# Getting feedback - Patch revisions

- First patch doesn’t have to be perfect
- After feedback has been addressed, a new revision should be posted 
- Patches that have been ignored and are re-sent should have a RESEND prefix
- Use patman again
  - **Series-version**
  - **Series-changes**
  - **Series-prefix**

---
layout: default
hideInToc: true
---

# Getting feedback - Patch revisions

```c
commit ca606ece36afddeaa1ed90a3791f9d404c12d0e5 (HEAD -> imx8mn-yet-remove-console-from-bootargs)
Author: Dario Binacchi <dario.binacchi@amarulasolutions.com>
Date:   Wed Jan 4 14:08:37 2023 +0100

    configs: imx8mn_bsh_smm_s2: remove console from bootargs
    [...]
    Commit 36b661dc919da ("Merge branch 'next'") re-added the console
    setting that commit bede82f750752 ("configs: imx8mn_bsh_smm_s2: remove
    console from bootargs") had previously removed.

    Fixes: 36b661dc919da ("Merge branch 'next'")
    Signed-off-by: Dario Binacchi <dario.binacchi@amarulasolutions.com>
    Reviewed-by: Fabio Estevam <festevam@denx.de>

    Patch-cc: amarula
    Series-cc: Tom Rini <trini@konsulko.com>,
    Series-cc: Stefano Babic <sbabic@denx.de>,
    Series-cc: Fabio Estevam <festevam@gmail.com>

    Series-prefix: RESEND

    Series-version: 2
    Series-changes: 2
    - Add the 'Reviewed-by' tag.
    - Improve commit message.

diff --git a/include/configs/imx8mn_bsh_smm_s2.h b/include/configs/imx8mn_bsh_smm_s2.h
```

---
layout: default
hideInToc: true
---

# Getting feedback - Patch revisions

<div class="font-large">

- If a new patch is added to a series, mention it in the changelog
- Re-post the whole series even if changes are needed for only  
a few patches
- Update patchwork state for old patches. For example, If you  
send v2 archive v1
- Always try to facilitate the maintainer work

</div>

---
layout: default
hideInToc: true
---

# Patch landed

- The work is not done when patches get merged
- Make sure to be responsive in a timely manner if issues are found
- Don't post patches and then disappear if bugs are found after merging
- Open source is about trust and this has to be earned
- Maintainers expects submitters to be trustable.  
If that's not the case, they will be less fond to merge  
patches in future
- Be ready to fix issues if these are found

---
layout: default
---

# Scattered notes

- The first patch doesn't have to be perfect. But if the underlying idea  
is good and you follow the maintainer's suggestions, eventually it will be merged
- To accept a patch that adds a feature, the maintainer can request  
the addition of a test  
<span style="color:blue">https://xenomai.org/pipermail/xenomai/2021-November/046832.html </span>
- At least check that the patch compiled correctly  
<span style="color:blue">https://lore.kernel.org/lkml/202210180937.sOYDt4IP-lkp@intel.com/ </span>

---
layout: default
hideInToc: true
---

# Scattered notes

- Want to contribute but don't know what kind of patch to submit?
  - The software driver for the device is missing 
  - New policies have been defined for the implementation of software  
  components that make the current code legacy 
    - DM in U-Boot  
    <span style="color:blue">https://www.mail-archive.com/u-boot@lists.denx.de/msg381487.html </span>
    - slcan driver in Linux  
    <span style="color:blue">https://lore.kernel.org/netdev/20220607094752.1029295-1-dario.binacchi@amarulasolutions.com/ </span>
  - Documentation is always welcome

---
layout: default
hideInToc: true
---

# Scattered notes

- The maintainer is not responsive?
  - Resend the patch
  - Ask for attention in the patch thread  
  <span style="color:red">
  A gently ping to remind this patch to you. I have no idea about why  
  it didn't yet deserve any reply. Is there anything I'm still missing?  
  <br/>
  I'm looking forward to hear from you.  
  <br/>
  Thanks and regards
  </span>

---
layout: default
hideInToc: true
---

# Scattered notes

- Set up e-mail aliases in your mailrc

```text
~/.gitconfig
[sendemail]
…
aliasesfile = ~/git-mailrc
aliasfiletype = mutt

~/git-mailrc
alias uboot        u-boot@lists.denx.de
alias amarula    linux-amarula@amarulasolutions.com
alias michael     michael@amarulasolutions.com
alias angelo      angelo@amarulasolutions.com
alias me            dario.binacchi@amarulasolutions.com
alias u-boot       uboot

git send-email --to u-boot --cc amarula -cc angelo --cc michael file.patch
```

---
layout: default
---

# Resources

- <span style="color:blue">https://elinux.org/images/0/0d/Oct26_Rybczynska_From_an_Idea_to_a_Patch_in_the_Linux_Mainline.pdf </span>  
From and idea to a patch in the Linux mainline
- <span style="color:blue">https://javierm.fedorapeople.org/slides/kernel_dev_process.pdf </span>
Linux kernel development process
- Rebel Code: Linux and the Open Source Revolution by Glyn Moody
- Free as in Freedom: Richard Stallman’s Crusade for Free Software by Sam Williams
- Just for fun: the story of an accidental revolutionary by Linus Torvalds and David Diamond

---
layout: default
---

# Q/A

<div class="font-large">

**Thank you for your time**

<center>

**Any Questions?**

</center>
</div>

