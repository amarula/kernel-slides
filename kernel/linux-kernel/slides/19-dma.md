---
layout: section
hideInToc: true
---
# Direct Memory Access (DMA)

---
layout: default
---
# DMA principles



- DMA copies data directly between devices and RAM, without going through the CPU.
- **Peripheral DMA**: some controllers embed their own DMA controller.
- **External DMA controllers**: drivers submit **DMA descriptors** to a shared controller.
---
layout: default
hideInToc: true
---
# DMA principles

<div style="text-align:center;">
  <img src="/images/dma-integration.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
---
# DMA controllers

<div style="text-align:center;">
  <img src="/images/dma-controllers.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>
---
layout: default
hideInToc: true
---
# DMA descriptors

<div style="text-align:center;">
  <img src="/images/dma-descriptors.svg" style="background:white; border-radius:14px; padding:10px; max-height:480px; max-width:90%;" />
</div>

- Descriptors describe source/destination/size/config and are **chained**.
---
layout: default
---
# Cache coherency & addressing

- DMA does not access the CPU cache — take care of coherency:
  - **Invalidate** cache lines when the CPU reads memory written by DMA.
  - **Flush/clean** cache lines when the CPU writes before starting a DMA transfer.
- CPUs use virtual pointers (`void *`), but DMA controllers use `dma_addr_t` (physical, or
  IOMMU-mapped).
- DMA buffers must be **physically contiguous**: use `kmalloc()` (≤128 KiB) or
  `__get_free_pages()` (≤8 MB), **not** `vmalloc()`/`malloc()`.
- Set the device's **DMA mask** with `dma_set_mask_and_coherent()`.

---
layout: default
---
# DMA APIs: dma-mapping & dmaengine

**dma-mapping** (allocate/manage DMA buffers, handle coherency, IOMMU mappings):

- Coherent: `dma_alloc_coherent()` / `dma_free_coherent()`.
- Streaming: `dma_map_single()` / `dma_unmap_single()`, `dma_map_sg()`, `dma_map_resource()`.
- Check errors with `dma_mapping_error()`; sync with `dma_sync_single_for_cpu/device()`.

**dmaengine** (abstract the DMA controller — slave API):

```c
dma_request_chan(dev, "tx");                 /* exclusive channel */
dmaengine_slave_config(chan, &txconf);       /* direction, buswidth, burst, addr */
desc = dmaengine_prep_slave_single(chan, buf, len, DMA_MEM_TO_DEV, flags);
cookie = dmaengine_submit(desc);
dma_async_issue_pending(chan);
```

**dma-buf**: share DMA buffers between devices (not covered here).
