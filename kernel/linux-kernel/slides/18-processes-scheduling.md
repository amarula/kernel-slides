---
layout: section
hideInToc: true
---
# Processes & scheduling

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
# The fair scheduler: from CFS to EEVDF

- The **fair scheduler** distributes CPU time among runnable tasks of the same priority.
- **CFS** (Completely Fair Scheduler) was merged in Linux 2.6.23 (2007) and used
  `vruntime`: the task with the smallest virtual runtime ran next.
- **EEVDF** (Earliest Eligible Virtual Deadline First) replaced CFS in Linux 6.6 (2023).
- EEVDF keeps the `vruntime` accounting and the red-black tree, but selects tasks using
  **lag** (fairness) and a **virtual deadline** (latency).
- Both schedulers are work-conserving: an idle CPU does not sit idle while a runnable task
  exists elsewhere.

---
layout: default
---
# EEVDF: lag and eligibility

- Each task has a **vruntime** `v_i` and a weight `w_i` (derived from its nice value).
- The scheduler maintains the weighted average vruntime `V` of all runnable tasks.
- A task's **lag** is the service it is owed (or has already exceeded):

  $$lag_i = S - s_i = w_i \cdot (V - v_i)$$

  - `S`: ideal service time; `s_i`: service already received.
  - `lag_i > 0`: the task is owed CPU time.
  - `lag_i < 0`: the task has received more than its share.
- Only **eligible** tasks (`lag_i >= 0`) are considered for execution.

---
layout: default
---
# EEVDF: virtual deadline and selection

- Every eligible task has a **virtual deadline** (VD):

  $$vd_i = v_i + \frac{slice_i}{w_i}$$

  - `slice_i` is the task's time slice; shorter slices get earlier deadlines and better latency.
  - The kernel computes the weighted slice with `calc_delta_fair()`.
- EEVDF picks the eligible task with the **earliest VD**.
- The runqueue is still a **red-black tree**, now keyed by `deadline`; the leftmost eligible node
  is the best candidate.
- The base slice is `sysctl_sched_base_slice` (**700 µs by default**, scaled with the number of
  CPUs); per-task slices are derived from it.
- The `min_vruntime` augmentation lets the scheduler skip subtrees with no eligible task.

---
layout: default
hideInToc: true
---
# EEVDF runqueue

<div style="text-align:center;">
  <img src="/images/eevdf-rbtree.svg" style="background:white; border-radius:14px; padding:10px; width:950px; max-width:92%; height:auto;" />
</div>

---
layout: default
---
# EEVDF: sleep, wake and lag decay

- When a task sleeps, it is marked for **deferred dequeue** (`sched_delayed`) instead of being
  removed immediately.
- Its **lag decays** with virtual runtime while it sleeps, so a long-sleeping task does not
  accumulate an unbounded CPU debt.
- The old CFS wake-up heuristic (`vruntime = max(old, min_vruntime - target_latency)`) is gone.
- `avg_vruntime()` and `zero_vruntime` provide the reference point for eligibility.
- This also prevents a task from briefly sleeping to reset a negative lag and gain an unfair
  advantage.

---
layout: default
---
# Scheduling classes and policies

- The scheduler tries **scheduling classes** in priority order:

  `stop` → `deadline` → `RT` → `fair` → `ext` → `idle`

- `pick_next_task()` asks each class for a task; the first class with a runnable task wins.
- `ext` (sched_ext) is optional and can take over fair tasks when enabled.
- User-visible policies select a class:
  - `SCHED_OTHER`, `SCHED_BATCH`, `SCHED_IDLE` → fair (EEVDF)
  - `SCHED_FIFO`, `SCHED_RR` → RT
  - `SCHED_DEADLINE` → deadline
  - `SCHED_EXT` (6.12+) → ext
- `SCHED_FIFO` runs until it blocks or a higher-priority RT task preempts it; `SCHED_RR` adds a
  round-robin timeslice.

---
layout: default
---
# SMP scheduling

- Each CPU has its own **runqueue** (`struct rq`) and its own fair/RT/deadline queues.
- `schedule()` only looks at the current CPU's runqueue; it does not scan all CPUs.
- **Load balancing** moves tasks between runqueues to keep the CPUs busy.
- **Migration** happens when a task wakes up, blocks, or is explicitly moved; tasks have a CPU
  affinity mask (`sched_setaffinity()`, `taskset`).
- RT tasks can be pushed and pulled between CPUs; deadline tasks use global admission control and
  a migration protocol.

---
layout: default
---
# schedule() and __schedule()

- `schedule()` is the entry point used when a task blocks or voluntarily yields.
- It calls `__schedule_loop()` → `__schedule()`:

```c
/* simplified */
static void __sched notrace __schedule(int sched_mode)
{
    struct task_struct *prev = rq->curr;
    struct task_struct *next;

    next = pick_next_task(rq, prev, &rf);
    if (likely(prev != next))
        rq = context_switch(rq, prev, next, &rf);
}
```

- `__schedule()` runs with preemption disabled and the runqueue lock held.
- `pick_next_task()` walks the scheduling classes in priority order.
- `context_switch()` switches the address space and the CPU register state.
- Sleeping is not allowed in atomic context, so `schedule()` must not be called there.
