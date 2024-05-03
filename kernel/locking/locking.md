---
theme: ../../template
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

# Locking
## An introduction to linux kernel locking
### Michael Nazzareno Trimarchi

---
layout: default
hideInToc: true
---

## Table of contents

<Toc minDepth="1" maxDepth="2"/>

---
layout: default
---

# What is a critical section?

- Concurrent accesses to shared resources can lead to unexpected/erroneous behavior.
- We need to protect access
- ..serialized.
- No more than one process or thread at a time.
- A process or thread will be suspended or will be spin wait to get the resource.

---
layout: default
---

# Locking reason and critical section

<div class="font-small">

- Application would like to share resources.
- Resources must be access in a way that we allow serialization.
- Just increment and reading a value from different context can be problematic.

```c
int c = 10;

void thread_a(void)
{
	c = c + 1;
}
```
```c
void thread_b(void)
{
	c = c + 1;
}
```

C will be seen by A as 11 or A can see C as 12.
This depends in when value are really incremented

</div>

---
layout: default
---

# Race conditions and critical section

- Overlap access depends on timing on a shared resource is called a race condition.
- The code that show the issue is called critical region.
- SMP machine and preemption impact the design of operating system because this can
  lead to measure issues.
- Preempt a task in a task during a critical region, imply a potential race condition.
- We need to recognize and solve when simultaneous events can happen.
