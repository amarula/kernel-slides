# Kernel development slides

## Purpose

The purpose of these slides is to provide some notes to newcomers to kernel
development. As approaching the Linux kernel development is difficult, we aim to
simplify the procedure.

## Technology

We use [slidev](https://github.com/slidevjs/slidev) for writing our slides. This
allows us to have a common template, to be able to export slides in a very fast
way and to review them as text, allowing us to use git to correct us without
doing it "the old way" (not as old as saving them on ~~floppy disks~~ USB
devices and passing them around).

## How to use

### Init

The first thing you want to do is

```
npm init slidev
```

in the root folder. This allows you to create a folder, the CLI is interactive
and does a good job at installing everything for you.

### The server

Then, it starts a server, usually on localhost:3030. Watch out: with the current
template, Chromium displays the intended thing. If you want to use the browser,
sadly Firefox has a little offset that has to be adjusted. On a note, Firefox
SHOULD be right, but people in the world use Chromium. When in Rome, do as the
Romans.

This said, at some point you may want to close the server. This can be done
brutally using Ctrl+C, or elegantly, just pressing ``Q``. to restart the server,
the only thing you need is writing ```slidev``` inside your project.

And that's all, for slidev tutorials/stuff you can go to the
[slidev](https://sli.dev/) website.