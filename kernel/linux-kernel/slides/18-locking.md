---
layout: section
hideInToc: true
---
# Locking

---
layout: default
---

# What is a critical section?

- Concurrent access to shared resources can lead to unexpected, erroneous behavior.
- We need to protect access — **serialize** it.
- No more than one process or thread at a time.
- A process or thread will be suspended or spin-wait to get the resource.

---
layout: default
hideInToc: true
---

# Locking reason and critical section

- Applications want to share resources.
- Resources must be accessed in a way that allows serialization.
- Simply incrementing and reading a value from different contexts can be problematic.

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

Thread A may read `c` as 11 or 12, depending on when the values are actually incremented.

---
layout: default
hideInToc: true
---

# Race conditions and critical section

- An overlapping access, depending on timing, to a shared resource is a **race condition**.
- The code that exhibits the issue is called a **critical region**.
- SMP machines and preemption impact OS design because they can lead to these issues.
- Preempting a task inside a critical region implies a potential race condition.
- We need to recognize and solve situations where simultaneous events can happen.

---
layout: default
---
# Sources of concurrency

- The kernel's state is global and visible in all execution contexts. Concurrency arises from:
  - **Interrupts** (interrupt the current thread; shared resources),
  - **Kernel preemption** (switch between threads),
  - **Multiprocessing** (code runs in parallel on different CPUs).
- Keep as much state **local** as possible; for shared resources that can't be local, use locking.
---
layout: default
hideInToc: true
---
# Sources of concurrency

<div style="text-align:center;">
  <img src="/images/lock-protection.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# Mutexes

- The kernel's main locking primitive; a binary lock (counting semaphores exist but are rarely
  used). The requester **blocks** when the lock is held → only usable where sleeping is allowed.

```c
#include <linux/mutex.h>
DEFINE_MUTEX(name);                 /* static */
void mutex_init(struct mutex *lock);/* dynamic */

void mutex_lock(struct mutex *lock);            /* sleeps; cannot be interrupted */
int  mutex_lock_killable(struct mutex *lock);   /* fatal-signal interruptible */
int  mutex_lock_interruptible(struct mutex *lock);
void mutex_unlock(struct mutex *lock);          /* release as soon as possible */
```

---
layout: default
---
# Spinlocks

- Locks for code that **cannot sleep** (interrupt handlers) or doesn't want to sleep. They spin in
  a loop until the lock is available. **Never call functions that can sleep while holding one!**

```c
DEFINE_SPINLOCK(my_lock);                  /* static */
void spin_lock_init(spinlock_t *lock);     /* dynamic */

void spin_lock(spinlock_t *lock);
void spin_unlock(spinlock_t *lock);

/* also protect against interrupts / softirqs */
void spin_lock_irqsave(spinlock_t *lock, unsigned long flags);
void spin_unlock_irqrestore(spinlock_t *lock, unsigned long flags);
void spin_lock_bh(spinlock_t *lock);
void spin_unlock_bh(spinlock_t *lock);
```

- Acquiring a spinlock disables **preemption** (and migration) on the local CPU to avoid deadlock.
- Reader/writer spinlocks also exist (multiple simultaneous readers).

---
layout: default
---
# Deadlocks & debugging

- **Rule 1:** don't call a function that can acquire the same lock.
- **Rule 2:** if you need multiple locks, always acquire them in the **same order**.
- Debugging:
  - `CONFIG_PROVE_LOCKING` (lockdep) — proves locking correctness (ordering, spinlocks in
    interrupt vs process context).
  - `CONFIG_DEBUG_ATOMIC_SLEEP` — detect sleeping in atomic sections.
  - `CONFIG_KCSAN` — data-race detector (Linux 5.8+).

---
layout: default
---
# Alternatives to locking: RCU & atomics

- **RCU** (Read-Copy-Update) for frequent reads, infrequent writes:
  ```c
  rcu_read_lock();
  p = rcu_dereference(shared_conf);
  /* ... read consistent snapshot ... */
  rcu_read_unlock();

  rcu_assign_pointer(shared_conf, newconf);
  synchronize_rcu();   /* wait for pre-existing readers */
  kfree(oldconf);      /* now safe */
  ```
- **Atomic variables** (`atomic_t`) for integer values — even `n++` is not atomic on all CPUs:
  `atomic_inc()`, `atomic_dec()`, `atomic_add()`, `atomic_inc_return()`, `atomic_read()`…
- **Atomic bit operations** for bitmaps: `set_bit()`, `clear_bit()`, `test_bit()`,
  `test_and_set_bit()`…

> Use mutexes where sleeping is allowed, spinlocks where it isn't, atomics for integers/addresses.
