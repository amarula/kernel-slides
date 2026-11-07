---
layout: section
hideInToc: true
---
# Processes & scheduling

---
layout: default
---

# CFS: the virtual runtime (vruntime)

- The **Completely Fair Scheduler** (CFS) accounts each task's run time with a **vruntime**:
  the actual runtime, weighted by the number of runnable processes and the task niceness.
- Every time a thread runs for `t` ns, `vruntime += t` (weighted by niceness).
- CFS always picks the process with the **smallest vruntime**.

---
layout: default
hideInToc: true
---

# CFS: task selection

- CFS selects the task with the minimum vruntime.
- It keeps runnable processes in a **red-black tree** (a self-balancing binary search tree) so it can
  efficiently find the task with the smallest vruntime.
- The selected task is the **leftmost** node of the tree.

<div style="text-align:center;">
  <img src="/images/cfs-rbtree.svg" style="background:white; border-radius:14px; padding:10px; max-height:340px; max-width:88%;" />
</div>

---
layout: default
hideInToc: true
---

# CFS: task just created or awakened

- CFS maintains `min_vruntime` — the smallest vruntime among all tasks in the runqueue.
- A **new task** is created with `vruntime = min_vruntime - adjustment` and inserted into the tree.
- An **awakened task** gets `vruntime = max(old vruntime, min_vruntime - targeted_latency)`.
- Using `min_vruntime - target_latency` as a lower bound prevents a task that blocked for a long
  time from monopolizing the CPU.

---
layout: default
---
# Process vs. thread

- A **process** (from `fork()`) has an address space (code, data, stack, libraries) and a single
  **thread** — the only entity the scheduler knows.
- Additional threads via `pthread_create()` run in the **same address space**.
- In the kernel each thread is a `struct task_struct`; the scheduler makes no difference between
  the initial thread and extra threads.

---
layout: default
---
# Mode, address space, context

- **Mode** is the privilege level:
  - *Kernel mode:* any instruction, any I/O, any memory.
  - *User mode:* some instructions forbidden, some memory inaccessible.
- **Address space**: split into kernel space (kernel-mode code) and user space (applications).
- **Context** determines what operations are allowed (mostly about sleepability):
  - *Process context*: most operations allowed (most permissive).
  - *Atomic context* (interrupt, softirq, NMI, spinlock regions): **sleeping is not allowed**.

---
layout: default
---
# A thread's life

<div style="text-align:center;">
  <img src="/images/thread-life.svg" style="background:white; border-radius:14px; padding:10px; max-height:400px; max-width:88%;" />
</div>

---
layout: default
---
# Sleeping

- Sleeping is needed when a user-space or kernel-space thread waits for data.
- **Wait queues** store the list of threads waiting for an event:
  ```c
  wait_event(queue, condition);
  wait_event_interruptible(queue, condition);      /* most common */
  wait_event_timeout(queue, condition, timeout);
  ```
- Wake up: `wake_up(&queue);` / `wake_up_interruptible(&queue);`.
- **Exclusive vs non-exclusive**: `wait_event_interruptible_exclusive()` — `wake_up()` wakes all
  non-exclusive threads but only one exclusive thread (avoid waking many threads for one event).
- **Completions**: `wait_for_completion()`, `complete()`, `complete_all()`, `reinit_completion()`.
- Blocking helpers: `udelay()` (atomic, ≤10µs), `usleep_range()`/`msleep()` (sleep), `fsleep()`.

