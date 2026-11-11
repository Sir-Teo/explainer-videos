# Computer Science, Built — Part 32: Virtual Memory

Part 32 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the second part of Act VI, *One Machine, Many Programs*. Every program believes
it owns a huge, private, contiguous memory, and none of them does. Address translation keeps up the illusion with a
radix tree that the hardware walks and the TLB caches. Memory is finite, so some page must leave; Belady showed which
page is optimal, and that adding memory can make things worse. The same machinery gives copy-on-write fork, shared
libraries, virtual machines and containers. Pebble gains an MMU, and PebbleOS runs every process at the same virtual
addresses.

The instruments are in [`explainer/cs/os/`](../../../explainer/cs/os) (tested in `tests/test_cs32_vm.py`):
* `mmu.py`, **Pebble's MMU**:
  - an Sv32-like two-level walk (10 + 10 + 12 bits), 4 MiB superpages, and the PTE bits V, R, W, X, U, A, D;
  - the `ptbr` control register (CSR 9); faults 12 (fetch), 13 (load) and 15 (store) with the address in `tval`;
  - an LRU TLB of any size, flushed on every write of `ptbr` unless address-space tags are on;
  - counts of hits, misses, walks, memory references per walk, flushes and faults;
* `vmos.py`, **PebbleOS with paging**:
  - the boot loader builds a table per process: the kernel's supervisor-only superpage in L1 entry 0, and the process
    at virtual 4–5 MiB through its own L2 table, code R+X, data R+W;
  - the kernel (46 more instructions, 330 in all) switches `ptbr` with the process and serves demand-zero faults;
    every other fault kills only the offender;
  - Part 13's compiler gains `target="vm"`, which page-aligns the data;
* `virt.py`, **trap and emulate**: Part 31's PebbleOS, unmodified, as a guest in user mode. The hypervisor keeps the
  guest's virtual mode and control registers, emulates `csrr`, `csrw`, `eret`, `halt` and device accesses, and
  reflects the guest processes' traps; `exits` counts its work by kind;
* `paging.py`: replacement (OPT, FIFO, LRU, CLOCK, 2Q, ARC, LIRS, random) over any trace; Mattson's stack distances
  and LRU's whole miss curve in one pass; a Belady-anomaly search; Denning's working set; a thrashing simulator; a
  buddy allocator and a slab allocator.

The simplified MMU rejects write-without-read PTE encodings and superpage physical bases that are not 4 MiB aligned.
With zero resident frames, every reference faults under every replacement policy. Buddy allocation requires a
positive page count. The slab example models occupancy only: allocation returns a slab index, not an object address;
it tracks free slots without storing object bytes or running constructors.

Measured on this machine (`videos/cs/cs32/compute.py` compiles and runs a small C program):
* a pointer chase over 1 to 131,072 pages, with 4 KiB pages and with 2 MiB huge pages: the TLB staircase;
* the first touch of a page (a fault) against a mapped page;
* `fork` with 256 MiB resident, and the child's first and second write to each page;
* a new PID and user namespace with `unshare`; this process's namespaces and cgroup controllers;
* whether this processor is affected by Meltdown.

## Chapters

* **Hook.** Two processes store their pid at the same virtual address, `0x405004`, and read it back: one sees 1, the
  other 2. The two physical addresses, `0x109004` and `0x110004`.
* **1. Protection and relocation.**
  - What Part 31's PebbleOS could not do: a program linked for one address, a fixed region each, no sharing, nothing
    larger than memory.
  - Atlas (Manchester, 1962): the one-level store, 512-word pages, a drum behind core.
* **2. Base and bounds, and segments.**
  - Base and bounds, and segment tables.
  - First fit over 1,024 units: the first refusal wants 90 units with 138 free in 8 holes, the largest 63; 247
    refusals in 4,000 steps. External fragmentation, and Part 11's malloc.
* **3. Paging.**
  - The address split, animated: L1 index 1, L2 index 5, offset 4.
  - The PTE's bits, and who sets each one. The walk of `0x405004` in both processes' tables.
* **4. Multi-level page tables.**
  - The radix tree: one process needs 8 KiB of tables instead of a 4 MiB flat array.
  - Flat tables for 32, 48 and 57 bits: 4 MiB, 512 GiB, 256 TiB. x86-64's 9 + 9 + 9 + 9 + 12 and five levels.
    Inverted and hashed tables.
* **5. The TLB.**
  - The Job's pipeline under paged PebbleOS: 4 entries miss 3.58% of the time, 8 miss 0.80%, 16 miss 0.009% (63
    misses in 712,311 accesses).
  - With a switch every 500 instructions, 16 entries: 508 misses flushing, 151 with ASIDs.
  - The staircase on this machine: 1.9 ns per access over 64 pages, 4.4 ns over 128, 97 ns over 65,536 pages with
    4 KiB pages and 58 ns with 2 MiB pages.
* **6. Page faults.**
  - A fault end to end; demand paging.
  - Where an evicted page goes: clean pages are dropped, dirty ones written to swap. Under LRU with 8 frames, 10,242
    of the Job's 23,077 evictions (44%) are dirty; `kswapd`.
  - On this machine: 1,732 ns for a first touch against 25 ns for a mapped page. The effective access time: one
    fault per million accesses to a disk costs 8%.
* **7. Which page to evict.**
  - Belady's OPT and its exchange argument.
  - Belady's string: FIFO faults 9 times with 3 frames and 10 with 4. Random strings with the anomaly: 2 of 20,000.
  - LRU's stack property, proved; no anomaly in 5,000 random strings.
  - How bad can LRU be: 4 pages in a cycle with 3 frames, 120 faults in 120 references against OPT's 42. Sleator and
    Tarjan (1985): k/(k − h + 1). On the Job's trace, LRU with 2h frames beats OPT with h for h = 2, 4, 8, 16.
  - CLOCK's hand.
* **8. Working sets and thrashing.**
  - The Job's 120,412 references to 39 pages of 1 KiB through every policy; at 8 frames OPT 12,474, LRU 23,085,
    FIFO 29,363 faults.
  - Mattson's stack distances worked by hand on `abcbadca`: distances ∞ ∞ ∞ 2 3 ∞ 4 3, so LRU misses 8, 7, 5, 4
    with 1 to 4 frames.
  - A hot set with scans: LRU is flushed, and LIRS and ARC resist.
  - Denning's working set along the trace. Thrashing: utilisation peaks at 0.51 with 3 processes and falls to 0.001
    at 8.
* **9. Copy-on-write, zero pages and mmap.**
  - fork without copying, animated.
  - On this machine: fork with 256 MiB takes 5.8 ms; the child's first write to a page 3.1 µs, the second 26 ns.
  - The zero page, `mmap` and shared libraries.
* **10. The kernel's own mapping.**
  - The kernel in every address space, supervisor-only; a user read of it exits −13.
  - Meltdown (2018) and KPTI. This machine: "Not affected".
* **11. Kernel allocators.**
  - The buddy system: 3 pages from 16 leave free blocks of 4 (at 4) and 8 (at 8).
  - Random traffic over 1,024 pages: 583 splits, 517 merges, **no** refusals, against segments' 247.
  - This machine's `/proc/buddyinfo`: 5.7 GiB free, 47% of it in 4 MiB blocks, 8 single pages; compaction.
  - Slab: 10,000 objects of 72 bytes in 0.73 MB instead of 40.96 MB.
* **12. Virtual machines.**
  - Popek and Goldberg (1974): trap and emulate.
  - Part 31's PebbleOS as a guest: identical output and identical guest instruction counts (14,987 and 558,092).
    The letter-printers make 594 exits, mostly control registers; the pipeline makes 5,127, of which 4,810 are the
    device: paravirtual devices.
  - x86's 17 sensitive unprivileged instructions, binary translation, Xen, VT-x.
  - The nested walk: (n + 1)(m + 1) − 1 = 24 references; shadow page tables.
* **13. Containers.**
  - One kernel, different views: inside `unshare`, the shell is pid 1 and uid 0, and sees 3 processes of the host's
    82. Eight namespaces, the cgroup controllers.
  - VMs against containers; Dirty COW (2016); gVisor and Firecracker.
* **14. PebbleOS gains virtual memory.**
  - What changed: the MMU, the boot loader, two instructions per switch and the fault handler; 284 → 330 kernel
    instructions.
  - One process's page table, read out: 7 of 256 pages mapped (28 KiB), code R X, data R W, A and D set by the MMU.
  - Four processes: `good` prints eight A's; `codewrite` dies with exit −15 and `wild` with −13; `grower` takes 16
    page faults and prints G. The console: `AAAAAAAAG`.
  - The Job's pipeline: 558,092 instructions unpaged, 558,104 paged with everything mapped (146 frames), 580,365 with
    zero pages on demand (7 faults, 24 frames). The output is identical.
* **15. Frontier: translation reach and memory tiers.**
  - TLB reach (64 × 4 KiB = 256 KiB; 1,536 × 1 GiB = 1.5 TiB) against 16 GiB and 4 TiB memories.
  - Direct segments, range TLBs, Ingens and HawkEye, Midgard, Mosaic pages.
  - CXL memory tiers and TPP; relaxed virtual memory on Armv8-A; TLB shootdowns. Open problems. Outro.

## Build

```bash
python -m videos.cs.cs32.compute           # every number in the part (about five minutes)
python tools/build.py cs32 -q l            # a 480p preview
python tools/build.py cs32                 # 1080p
```

## Problems, with solutions

1. **OPT is optimal.** Prove by an exchange argument that Belady's OPT (on a fault, evict the page whose next use is
   farthest in the future) minimises the number of faults.

   *Solution.* Let S be any schedule that agrees with OPT on the first j requests. We build S′ that agrees with OPT
   on the first j + 1 requests and has no more misses than S. If request j + 1 hits, or S and OPT evict the same
   page, take S′ = S. Otherwise the request misses, S evicts f and OPT evicts e, so by OPT's choice f is requested
   again before e. Let S′ evict e, and from then on copy S. The two memories differ only in that S′ holds f where S
   holds e, until the first request y at which one of these happens:
   - y is neither e nor f, and S evicts e. Then S′ evicts f, and the memories are equal at the same cost.
   - y = f (this must come before any request for e). S′ hits; S misses and evicts some page x. If x = e, the
     memories are now equal and S′ has one miss fewer. Otherwise S′ evicts x and loads e, which costs it one miss,
     as S paid one; the memories are equal.

   A request for e cannot come first, since f is requested before e. In every case S′ has no more misses than S, and
   agrees with OPT on j + 1 requests. (S′ may load a page that was not requested, but any such schedule can be
   rewritten to load pages only on demand without adding misses.) By induction on j, OPT has no more misses than any
   schedule. This is the farthest-in-future argument of Belady (1966), in the form of Kleinberg and Tardos's
   *Algorithm Design*, §4.3.

2. **LRU's stack property.** Prove that LRU has the stack property, so it has no anomaly; show that FIFO's three- and
   four-frame memories are not nested on Belady's string.

   *Solution.* With k frames, after any prefix of the requests, LRU holds exactly the k distinct pages most recently
   used (fewer if fewer have been used): it evicts the least recent, and keeps every other. The k most recent are
   among the k + 1 most recent, so M_k(t) ⊆ M_{k+1}(t) at every time t. A hit with k frames is therefore a hit with
   k + 1, and faults can only fall as frames are added. This is Mattson's inclusion property, and it is what lets one
   pass of stack distances give LRU's whole miss curve.

   FIFO, on 1 2 3 4 1 2 5 1 2 3 4 5: after the seventh request (5), three frames hold {1, 2, 5} and four frames hold
   {2, 3, 4, 5}. Page 1 is in the smaller memory and not the larger, so the next request (1) hits with three frames
   and faults with four. In all, FIFO faults 9 times with three frames and 10 with four.

3. **The nested walk.** Derive (n + 1)(m + 1) − 1 for the nested walk, and the count when a walk cache holds every
   upper level of both tables.

   *Solution.* A guest walk reads n guest entries. Each lives at a guest-physical address, which the hardware must
   translate through the host's m levels (m references) before reading it (1 reference): m + 1 references per guest
   level. The guest walk ends with the guest-physical address of the data, which needs one more host walk of m
   references. So n(m + 1) + m = nm + n + m = (n + 1)(m + 1) − 1; for 4 and 4, 24. The grid picture: n + 1 rows (n
   guest entries and the data) times m + 1 columns (m host entries and the read), less the final read of the data
   itself, which is not part of translation.

   With a cache of every non-leaf entry of both tables, and of the host translations of the guest's table pages
   (AMD's nested TLB), a miss reads only the guest's leaf entry (1 reference, its host address already known) and
   then the host's leaf entry for the data's guest-physical page (1 reference): 2, against 1 for a native walk with a
   walk cache. Real walk caches are small, so measured nested misses fall between these bounds (Bhargava et al.,
   2008).

4. **Buddy waste.** Show that a buddy block is always more than half used, and find the expected waste for request
   sizes uniform on 1..2^k.

   *Solution.* A request of s pages, 2^{j−1} < s ≤ 2^j, gets a block of 2^j, and s > 2^{j−1} = 2^j/2; for s = 1, the
   block is exactly 1. So every block is more than half used (or full). For s uniform on 1..2^k: the sizes in
   (2^{j−1}, 2^j] waste 2^j − s, which runs from 2^{j−1} − 1 down to 0, an average of (2^{j−1} − 1)/2 over 2^{j−1}
   sizes. Summing, the total waste is ½ ∑_{j=1}^{k} (4^{j−1} − 2^{j−1}) = ½[(4^k − 1)/3 − (2^k − 1)], so the
   expected waste is about 2^k/6 pages. The expected request is (2^k + 1)/2, so a block's expected size is about
   2^k · 2/3, and the waste is about **a quarter of the memory allocated** (a third of what was asked for). For
   k = 10, exactly 170.2 pages wasted on average, 24.9% of what is allocated.

5. **Build: a copy-on-write fork for PebbleOS.** Share frames read-only, copy on the store fault, and count the
   copies.

   *Solution.*
   - Add `sys_fork`: take a free PCB, copy the parent's registers and set the child's `a0` to 0; take a root and an
     L2 frame; copy the root's two entries (the kernel's superpage and the pointer to the new L2).
   - Copy the parent's L2 entries into the child's L2, clearing W in both and setting a software bit COW (bit 8, the
     RSW field Pebble's MMU ignores) on every entry that was writable. Keep a reference count per frame, in a kernel
     array indexed by frame number, and increment it for each shared frame.
   - Write the parent's `ptbr` again, to flush its stale writable translations from the TLB.
   - In `pfault`: a store fault (cause 15) on a valid entry with COW set is not a protection error. If the frame's
     count is 1, set W, clear COW and retry. Otherwise take a frame, copy 4 KiB, map it W in this process, decrement
     the old frame's count, count the copy (`ncow`), and retry.
   - Test: a parent fills 16 pages, forks, and the child writes 4 of them. The child sees the parent's data, each
     process sees its own writes, and `ncow` = 4. For fork followed at once by exit, `ncow` = 0, except for the stack
     page the call itself writes.

6. ★ **Research: offline huge-page promotion.** Given a trace, a TLB of k entries and a budget of wasted frames,
   choose the aligned regions to promote to huge pages. Is it NP-hard? How close is greedy on the Job's trace?

   *Where to start.*
   - The model. A region is promoted whole: it costs (region size − pages of it the trace touches) wasted frames, and
     all its pages share one TLB entry. The objective is the number of misses of an LRU TLB with k entries on the
     trace of entries (each reference mapped to its region if promoted, else to its page). Measure it with
     `explainer/cs/os/paging.faults(trace, k, "lru")`. Scale the Job's 1 KiB-page trace from `compute._job_trace` to
     regions of 4 or 16 pages, since its address space is only 1 MiB.
   - Sanity checks. If k is at least the number of entries, only compulsory misses remain, and promotion helps by
     merging them. With OPT as the TLB's policy instead of LRU, is the problem easier?
   - Hardness. The gains are not additive (promoting two regions can help more or less than the sum). If they were,
     the problem would be a knapsack, weakly NP-hard and solved by dynamic programming in pseudo-polynomial time. Try
     a reduction from a strongly NP-hard problem through the LRU interaction, for example from a packing problem in
     which promoted regions must keep the working set under k.
   - Algorithms. Greedy by marginal misses saved per wasted frame; compare it with exhaustive search on small
     instances and with an integer program. A submodularity check (are the marginal gains diminishing?) would give
     greedy a (1 − 1/e)-style guarantee if it holds, and a counterexample if it does not.
   - Literature. Navarro et al., "Practical, transparent operating system support for superpages" (OSDI 2002);
     Kwon et al., Ingens (OSDI 2016); Panwar et al., HawkEye (ASPLOS 2019); Ram et al., Trident (ISCA 2021).

   Deployed systems promote by heuristics. A hardness result, or an algorithm with a provable ratio, for the offline
   problem would tell them how far from optimal they can be.

## 习题与解答

1. **OPT 最优。** 用交换论证证明：Belady 的 OPT（缺页时换出下一次使用最远的页）使缺页次数最少。

   *解答。* 设任意调度 S 在前 j 个请求上与 OPT 一致。构造 S′，使它在前 j + 1 个请求上与 OPT 一致且缺页不多于 S。若第 j + 1 个
   请求命中，或 S 与 OPT 换出同一页，令 S′ = S。否则 S 换出 f，OPT 换出 e，由 OPT 的选择，f 在 e 之前会再被请求。令 S′ 换出 e，
   此后照搬 S。两者的内存只差在：S′ 持有 f 处 S 持有 e，直到第一个出现下列情况之一的请求 y：
   - y 既非 e 也非 f，而 S 换出 e：S′ 换出 f，两者内存相同，代价相同。
   - y = f（它必在对 e 的任何请求之前）：S′ 命中；S 缺页并换出某页 x。若 x = e，内存已相同，S′ 少一次缺页；否则 S′ 换出 x 并装入
     e，付出一次缺页，与 S 相同，内存相同。

   对 e 的请求不可能先出现，因为 f 先于 e 被请求。每种情况下 S′ 的缺页都不多于 S，且在 j + 1 个请求上与 OPT 一致。（S′ 可能装入
   未被请求的页，但任何这样的调度都能改写为只按需装入而不增加缺页。）对 j 归纳，OPT 的缺页不多于任何调度。这是 Belady（1966）
   的“最远未来”论证，写法取自 Kleinberg 与 Tardos《算法设计》§4.3。

2. **LRU 的栈性质。** 证明 LRU 有栈性质，因此没有异常；并说明 FIFO 在 Belady 串上三帧与四帧的内存不嵌套。

   *解答。* k 帧时，在请求的任意前缀之后，LRU 恰好持有最近使用过的 k 个不同页：它换出最久未用的，保留其余。最近的 k 个包含于
   最近的 k + 1 个之中，所以每一时刻 M_k(t) ⊆ M_{k+1}(t)。k 帧时的命中在 k + 1 帧时也命中，缺页只会随帧数增加而减少。这就是
   Mattson 的包含性质，也正是它让一遍栈距离就能给出 LRU 的整条缺页曲线。FIFO 在 1 2 3 4 1 2 5 1 2 3 4 5 上：第七个请求（5）
   之后，三帧持有 {1, 2, 5}，四帧持有 {2, 3, 4, 5}。页 1 在小内存中而不在大内存中，于是下一个请求（1）三帧命中、四帧缺页。FIFO
   共缺页：三帧 9 次，四帧 10 次。

3. **嵌套页表遍历。** 推导嵌套遍历的 (n + 1)(m + 1) − 1，以及遍历缓存持有两张表所有上层时的次数。

   *解答。* 客户机遍历读 n 个客户机表项；每个都位于一个客户机物理地址上，硬件必须先经主机的 m 级翻译（m 次访存）再读它（1 次）：
   每个客户机层级 m + 1 次。遍历最后得到数据的客户机物理地址，还需一次 m 次访存的主机遍历。共 n(m + 1) + m = (n + 1)(m + 1) − 1；
   4 与 4 时为 24。网格图：n + 1 行（n 个客户机表项和数据）乘 m + 1 列（m 个主机表项和读取），减去不属于翻译的那次数据读取。
   若缓存了两张表的所有非叶表项，以及客户机页表页的主机翻译（AMD 的嵌套 TLB），一次缺失只需读客户机叶表项（1 次，其主机地址已知），
   再读数据所在客户机物理页的主机叶表项（1 次）：共 2 次，而带遍历缓存的原生遍历为 1 次。实际的遍历缓存很小，实测的嵌套缺失介于
   两界之间（Bhargava 等，2008）。

4. **伙伴系统的浪费。** 证明伙伴块总是用了一半以上，并求请求大小在 1..2^k 上均匀分布时的期望浪费。

   *解答。* 大小 s 满足 2^{j−1} < s ≤ 2^j 的请求得到 2^j 的块，而 s > 2^j/2；s = 1 时块恰为 1。所以每块用了一半以上（或全满）。
   s 在 1..2^k 上均匀时，(2^{j−1}, 2^j] 中的大小浪费 2^j − s，从 2^{j−1} − 1 降到 0，在 2^{j−1} 个大小上平均 (2^{j−1} − 1)/2。
   求和得总浪费 ½[(4^k − 1)/3 − (2^k − 1)]，期望浪费约 2^k/6 页。期望请求为 (2^k + 1)/2，块的期望大小约 2^k · 2/3，浪费约为
   **已分配内存的四分之一**（所请求量的三分之一）。k = 10 时，平均恰浪费 170.2 页，占已分配的 24.9%。

5. **动手：给 PebbleOS 加写时复制的 fork。** 只读共享页框，在写缺页时复制，并统计复制次数。

   *解答。* 加 `sys_fork`：取空闲 PCB，复制父进程寄存器并把子进程的 `a0` 设为 0；取一个根页框和一个 L2 页框，写入根表的两项
   （内核超级页和指向新 L2 的指针）。把父进程的 L2 表项复制到子进程，两边都清除 W，并在原本可写的表项上置软件位 COW（第 8 位，
   Pebble 的 MMU 忽略的 RSW 字段）。为每个页框维护引用计数（内核中按页框号索引的数组），共享的页框各加一。重写父进程的 `ptbr`，
   冲掉 TLB 中过时的可写翻译。在 `pfault` 中：对有效且置了 COW 的表项的写缺页（原因 15）不是保护错误。若页框计数为 1，置 W、清 COW
   并重试；否则取新页框、复制 4 KiB、在本进程中以 W 映射、旧页框计数减一、复制计数 `ncow` 加一，然后重试。测试：父进程写满 16 页，
   fork，子进程写其中 4 页；子进程看到父进程的数据，各自看到自己的写，`ncow` = 4。fork 后立即 exit 时 `ncow` = 0，只有调用本身
   写到的栈页除外。

6. ★ **研究：离线大页提升。** 给定访问序列、k 项的 TLB 和浪费页框的预算，选择要提升为大页的对齐区域。它是 NP 难的吗？贪心在
   Job 的序列上离最优多远？

   *从哪里开始。* 模型：区域整体提升，浪费（区域大小 − 序列触及的页数）个页框，区域内所有页共用一个 TLB 项；目标是 k 项 LRU TLB
   在表项序列上的缺失数（每次访问若所在区域已提升则映射到区域，否则映射到页），用 `explainer/cs/os/paging.faults(trace, k, "lru")`
   测量。Job 的地址空间只有 1 MiB，把 `compute._job_trace` 的 1 KiB 页序列缩放到 4 或 16 页的区域。检查：若 k 不小于表项数，只剩
   强制缺失，提升靠合并它们起作用；若 TLB 用 OPT 而不是 LRU，问题会更容易吗？难度：收益不可加（提升两个区域的效果可能大于或小于
   两者之和）；若可加，问题就是背包，弱 NP 难，可用伪多项式动态规划求解。试着通过 LRU 的相互作用从强 NP 难问题归约，例如提升的
   区域必须使工作集保持在 k 以下的装箱问题。算法：按每个浪费页框节省的缺失数贪心；在小实例上与穷举和整数规划比较。检验次模性
   （边际收益是否递减）：若成立，贪心有 (1 − 1/e) 式的保证；若不成立，给出反例。文献：Navarro 等（OSDI 2002）；Kwon 等，Ingens
   （OSDI 2016）；Panwar 等，HawkEye（ASPLOS 2019）；Ram 等，Trident（ISCA 2021）。实际系统靠启发式提升；离线问题的难度结果，或
   有可证比率的算法，能告诉它们离最优有多远。

## Glossary additions

虚拟内存 virtual memory · 地址空间 address space · 虚拟地址 virtual address · 物理地址 physical address · 地址翻译 address
translation · 重定位 relocation · 基址与界限 base and bounds · 段 segment · 外部碎片 external fragmentation · 内部碎片
internal fragmentation · 页 page · 页框 frame · 页号 page number · 页内偏移 offset · 页表 page table · 页表项 page-table
entry · 有效位 valid bit · 访问位 accessed bit · 脏位 dirty bit · 多级页表 multi-level page table · 页表遍历 page-table
walk · 超级页 superpage · 大页 huge page · 倒排页表 inverted page table · 快表 TLB · 地址空间标识 ASID · TLB 覆盖范围 TLB
reach · TLB 击落 TLB shootdown · 缺页 page fault · 按需调页 demand paging · 交换 swapping · 有效访问时间 effective access time ·
页面置换 page replacement · Belady 异常 Belady's anomaly · 栈性质 stack property · 栈距离 stack distance · 时钟算法 CLOCK ·
工作集 working set · 抖动 thrashing · 写时复制 copy-on-write · 零页 zero page · 内存映射文件 memory-mapped file · 共享库
shared library · 内核页表隔离 KPTI · 伙伴系统 buddy system · slab 分配器 slab allocator · 虚拟机 virtual machine · 虚拟机监控器
hypervisor · 陷入并模拟 trap and emulate · 敏感指令 sensitive instruction · 二进制翻译 binary translation · 半虚拟化
paravirtualization · 影子页表 shadow page table · 嵌套页表 nested paging · 容器 container · 命名空间 namespace · 控制组 cgroup ·
内存分层 memory tiering

## Sources

*Canon.* Books:
- Arpaci-Dusseau & Arpaci-Dusseau, *Operating Systems: Three Easy Pieces* (OSTEP, v1.10, 2023), virtualisation of
  memory;
- Tanenbaum & Bos, *Modern Operating Systems* (5th ed., 2023), ch. 3;
- Gorman, *Understanding the Linux Virtual Memory Manager* (2004);
- Bhattacharjee & Lustig, *Architectural and Operating System Support for Virtual Memory* (2017);
- Smith & Nair, *Virtual Machines: Versatile Platforms for Systems and Processes* (2005).

Papers:
- History: Kilburn, Edwards, Lanigan & Sumner, "One-Level Storage System" (1962); Denning, "Virtual Memory"
  (Computing Surveys, 1970).
- Replacement:
  - Belady, "A study of replacement algorithms for a virtual-storage computer" (1966); Belady, Nelson & Shedler,
    "An anomaly in space-time characteristics of certain programs" (1969);
  - Mattson, Gecsei, Slutz & Traiger, "Evaluation techniques for storage hierarchies" (1970);
  - Denning, "The working set model for program behavior" (1968); Carr & Hennessy, WSClock (1981);
  - Sleator & Tarjan, "Amortized efficiency of list update and paging rules" (CACM 1985); Fiat et al.,
    "Competitive paging algorithms" (1991);
  - Johnson & Shasha, 2Q (1994); Jiang & Zhang, LIRS (2002); Megiddo & Modha, ARC (2003).
- Allocators: Knowlton, "A fast storage allocator" (1965); Bonwick, "The Slab Allocator" (USENIX 1994).
- The kernel's mapping: Lipp et al., "Meltdown" (USENIX Security 2018); Gruss et al., KAISER (2017).
- Virtualisation:
  - Popek & Goldberg, "Formal requirements for virtualizable third generation architectures" (CACM 1974);
  - Robin & Irvine, "Analysis of the Intel Pentium's ability to support a secure virtual machine monitor" (2000);
  - Bugnion et al., "Bringing virtualization to the x86 architecture with the original VMware Workstation" (TOCS
    2012); Barham et al., "Xen and the art of virtualization" (SOSP 2003);
  - Adams & Agesen, "A comparison of software and hardware techniques for x86 virtualization" (ASPLOS 2006);
  - Bhargava, Serebrin, Spadini & Manne, "Accelerating two-dimensional page walks for virtualized systems" (ASPLOS
    2008).
- Containers: Kerrisk, "Namespaces in operation" (LWN, 2013); Agache et al., Firecracker (NSDI 2020); Young et al.,
  "The true cost of containing: a gVisor case study" (HotCloud 2019).
- Frontier:
  - Basu, Gandhi, Chang, Hill & Swift, "Efficient virtual memory for big memory servers" (ISCA 2013); Karakostas et
    al., "Redundant memory mappings" (ISCA 2015);
  - Kwon et al., Ingens (OSDI 2016); Panwar et al., HawkEye (ASPLOS 2019); Gupta et al., Midgard (ISCA 2021); Gosakan
    et al., "Mosaic pages" (ASPLOS 2023);
  - Maruf et al., "TPP: transparent page placement for CXL-enabled tiered memory" (ASPLOS 2023);
  - Simner et al., "Relaxed virtual memory in Armv8-A" (ESOP 2022); Kumar et al., LATR (ASPLOS 2018).
