---
layout: section
hideInToc: true
---
# Processes, scheduling & interrupts

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

---
layout: default
---
# Registering an interrupt handler

```c
int devm_request_irq(struct device *dev, unsigned int irq, irq_handler_t handler,
                     unsigned long irq_flags, const char *devname, void *dev_id);
```

- `irq`: IRQ channel (use `platform_get_irq()`); `devname` for `/proc/interrupts` (use
  `pdev->name`); `dev_id`: opaque pointer (per-device data; cannot be NULL on a shared line).
- Common `irq_flags`: `IRQF_SHARED` (shared line — all handlers called), `IRQF_ONESHOT`
  (threaded interrupts; line kept disabled until the thread runs).

```c
irqreturn_t foo_interrupt(int irq, void *dev_id);   /* returns IRQ_HANDLED, IRQ_NONE, IRQ_WAKE_THREAD */
```

---
layout: default
---
# Interrupt handler constraints

- No guarantee which address space is active — **can't transfer data to/from user space**.
- Runs outside the scheduler — **cannot sleep** (use `GFP_ATOMIC`).
- Runs with all interrupts disabled on the local CPU — must **complete quickly**.
- A typical handler: acknowledge the interrupt, read/write data, wake up waiters on a
  per-device queue.

---
layout: default
---
# Top half and bottom half

- Hard IRQ handlers run with interrupts masked; no nesting; higher-priority IRQs are delayed.
- **Top half** = the real handler (as fast as possible); **bottom half** = deferred mechanisms for
  post-processing:
  - **softirqs** (interrupt context, interrupts enabled, no sleeping; subsystem use — network…);
  - **threaded IRQs** (`IRQ_WAKE_THREAD`, process context, may sleep);
  - **workqueues** (general-purpose deferred work, process context).
---
layout: default
hideInToc: true
---
# Top half and bottom half

<div style="text-align:center;">
  <img src="/images/softirq-flow.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Threaded IRQs & workqueues

- **Threaded interrupts** (`devm_request_threaded_irq`) run a `thread_fn` in process context;
  may sleep; priority tunable; heavily used by PREEMPT_RT.
- **Workqueues** defer work generally (background jobs). Works (`INIT_WORK`) become threads
  running in process context (interrupts enabled, sleeping allowed); queue with `schedule_work()`.

| Mechanism | Context | IRQs | Can sleep | Typical use |
| --- | --- | --- | --- | --- |
| Hard IRQ | interrupt | disabled | No | fast handling |
| Softirq | interrupt | enabled | No | net, timers, RCU |
| Threaded IRQ | process | enabled | Yes | blocking IRQ handling |
| Workqueue | process | enabled | Yes | background workers |
