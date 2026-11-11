# Computer Science, Built — Part 34: Storage

Part 34 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), and the last part of Act VI, *One Machine, Many Programs*. Memory forgets when the
power goes, so data must live on spinning platters or in flash that wears out, both thousands of times slower than
memory and both written a block at a time. An append that needs three block writes can be cut short by a crash
between any two of them. Careful ordering, journals, logs and copy-on-write trees are the answers; RAID's parity is
Part 28's codes at work, and real disks fail more often, and more quietly, than their datasheets say. PebbleOS gets a
disk and reads the novels from its own file system.

The instruments are in `explainer/cs/store/` (tested in `tests/test_cs34_storage.py`):
* `fs.py`, **PebbleFS**, a small Unix file system on 1 KiB blocks:
  - superblock, inode and data bitmaps, a table of 64-byte inodes (ten direct pointers, one single- and one
    double-indirect), a journal, and data; directories of 32-byte entries; the largest file is
    (10 + 256 + 65,536) KiB;
  - create, mkdir, write and append, read, link, unlink, and an atomic rename; allocation in a row (`next`, with a
    per-file goal) or at random (an aged disk); delayed allocation with `fsync`;
  - five commit modes: `none`; `careful` (data, bitmaps, indirect blocks, inodes, directories, with a flush between
    groups, the reverse when freeing); `writeback`, `ordered` and `data` journaling, with a descriptor block, copies
    and a commit block, optional barriers and a checksum of the copies in the commit block; recovery replays a
    committed transaction and discards an uncommitted one;
  - `fsck`: six invariants (used blocks marked, marked blocks owned, no block owned twice, entries name live inodes,
    link counts, sizes covered), with repair;
  - **crash injection**: every write and flush is recorded; `crash_states` yields every disk a crash could leave
    (everything before the last flush, and any subset of the writes after it, since disks reorder), and
    `crash_test` mounts, checks and reads each one.
* `disk.py`: the hard disk model (seek time t_min + (t_max − t_min)√(d/C), half a turn, transfer; a short forward
  gap on the same turn costs only its passing), the time of a block trace, FCFS, SSTF, SCAN and C-SCAN on a static
  queue and under Poisson load; a rough flash drive for comparison.
* `flash.py`: a page-mapped flash translation layer with greedy or FIFO garbage collection, over-provisioning,
  skewed traffic, TRIM and sequential (zoned) writes; write amplification and erase counts.
* `lfs.py`: Rosenblum and Ousterhout's cleaner simulation (greedy and cost-benefit, uniform and hot-and-cold).
* `raid.py`: RAID 0/1/4/5/6 layouts, XOR parity, RAID 6's P and Q over GF(256) (Part 28's field, the polynomial
  Linux uses) with two-disk recovery, small-write costs, rebuild risk, MTTDL by formula, exact Markov chain and
  simulation.
  The exact chain uses a positive recurrence that stays accurate when failures are rare. Failures and repairs
  are independent exponential clocks with one repair at a time; the formulas are fast-repair approximations.
  Rebuild URE probabilities assume independent Poisson errors at the stated per-bit rate. Datasheet bounds are
  not observed rates, and an unreadable stripe does not imply loss of every byte in the array.
* `lsm.py`: an LSM tree with leveled or tiered compaction and per-run Bloom filters (Part 20's), and a B-tree's write
  amplification under an LRU buffer pool.
* `cow.py`: a copy-on-write tree whose pointers carry SHA-256 checksums, with snapshots, bit rot and repair from a
  mirror.

PebbleOS's **disk** (`explainer/cs/os/fsos.py`): three registers on the I/O page (block, address, command) copy a
block into memory by DMA. The kernel gains about 260 instructions (`kernel.py` grew empty hooks for them, so Parts
31–33 are unchanged): the superblock read at boot, `bread` with a four-block buffer cache, `iget`, `bmap`, an `open`
system call that walks a path, and `read` from an open file or from standard input redirected from a file.
`predict_reads` models the kernel's reads in Python; the tests check it against the device's log.

## Chapters

* **Hook.** One block appended to a one-block file, with no ordering: the bitmap, data and inode writes, and all
  eight subsets a crash can leave. Two are corrupt (a used block marked free); two lose a block; and one is perfectly
  consistent to fsck yet ends the file with a deleted file's `PASSWORD=hunter2`. Across four operations, 34 of 126
  crash points corrupt the file system and 22 show the wrong bytes; ordered journaling: all 150 intact.
* **1. Persistence.** The bottom of Part 9's hierarchy: memory 100 ns, flash about 80 µs, the disk 13 ms
  (129,606×: if memory took a second, the disk would take 1.5 days). DRAM leaks; storage keeps bits without power,
  in blocks. IBM's 350 disk (1956). One block write is atomic; two are not.
* **2. Disks.** Seek, rotation, transfer, from the model: 8.8 ms average seek, 4.17 ms half turn, 27 µs for 4 KiB at
  150 MB/s; a random 4 KiB read 13.0 ms. Random 4 KiB reads deliver 0.32 MB/s against 150 MB/s in order: 475×. The
  textbook queue from cylinder 53: FCFS 640 cylinders, SSTF 236, SCAN 299, C-SCAN 322. Under 72 requests a second:
  FCFS's mean 96 ms; SSTF 30 ms but a worst case of 240 ms; SCAN 31 ms and 177 ms. NCQ; Linux's schedulers.
* **3. Flash.** Pages, erase blocks, wear. The FTL as a log with a garbage collector (animated). Write amplification
  simulated on 256 blocks of 64 pages: 7.5 at 7% spare, 2.4 at 28%, close to the estimate (1 + p)/2p; FIFO a little
  worse. 90% of writes to 10% of the data: the busiest block erased 42 times against a mean of 15. TRIM: from 7.5 to
  2.1 with 20% trimmed. NVMe's queues.
* **4. Files and directories.** Inodes, directories as tables of names, paths (Multics 1965, Unix 1974). The Unix
  calls, and the descriptor → open file → inode chain. Links, unlink, an atomic rename; symbolic links.
* **5. A simple file system.** PebbleFS on 8,192 blocks: 1 superblock, 1 + 1 bitmap blocks, 16 inode-table blocks,
  64 journal blocks, 8,109 data blocks. The inode and its pointer tree; the largest file, 67,381,248 bytes. PebbleOS's
  kernel opening `/novels/emma`: block 0, the inode table, two directory blocks, then the data: 201 reads for
  200,000 bytes.
* **6. Locality.** The old Unix file system's 2% of the bandwidth; FFS (1984) and cylinder groups. A 4 MiB file:
  written alone, 41 ms on the model disk (the platter's limit is 28 ms); interleaved with another file, 70 ms; on
  an aged disk, 16.8 s, 406× slower; on flash 1.6 ms against 329 ms. Extents, delayed allocation, preallocation.
* **7. Crash consistency.** fsck's six invariants, and what it cannot see. The checker. No ordering: 19 writes in four
  operations, 126 crash points, 34 corrupt, 22 wrong bytes. Careful ordering: 0 and 0, with 14 leaks, at the price of
  13 flushes instead of 5; soft updates (1994). fsck reads grow with the disk (25, 92, 359 distinct blocks for 2,048,
  8,192, 32,768); replaying a journal reads 4 blocks for an append.
* **8. Journaling.** One ordered-mode append, write by write: data, flush; descriptor and copies, flush; commit,
  flush; checkpoint, flush; clear. Crash after any write: discarded before the commit, replayed after it, always the
  old file or the new. Writeback (90 of 214 crash points with the wrong bytes), ordered and data (all intact; 53
  writes against 46). No flush before the commit: 25 of 208 corrupt, by recovery itself; a checksum of the copies
  (ext4's `journal_checksum`): none.
* **9. The log-structured file system.** Rosenblum and Ousterhout (1992): every write sequential; the inode map and
  checkpoint; the cleaner's write cost 2/(1 − u). Simulated at 75% utilization: greedy 4.7 (uniform), 4.5 (hot and
  cold), cost-benefit 3.6; the utilizations of cleaned segments, unimodal for greedy, bimodal for cost-benefit.
* **10. Copy-on-write and checksums.** WAFL (1994), ZFS (2005): copy the path to a new root, switch the uberblock.
  Four blocks per change in a tree of depth 3. Checksums in pointers: a flipped bit caught and repaired from a mirror.
  Snapshots: after 13 writes, 113 blocks instead of 170. Transaction groups.
* **11. RAID.** Patterson, Gibson and Katz (1988). RAID 0, 1 and 5 layouts; capacity and random-I/O table. Parity, and
  the small-write problem (2 reads and 2 writes). RAID 6's P and Q over GF(256): all 15 pairs of lost disks out of six
  rebuilt. Eight 16 TB disks, a 44-hour rebuild: another failure 0.03% (datasheet) or 0.11% (3% a year); an
  unreadable sector 59% at 10⁻¹⁵ per bit, 99.99% at 10⁻¹⁴. MTTDL, RAID 5: 45,835 years by the formula; formula 1,607,
  exact 1,687, simulated 1,738 at MTTF/MTTR = 300.
* **12. Disks in the field.** Schroeder and Gibson (2007): 2–4% replaced a year, up to 13%, against 0.88% on the
  datasheet; no flat bathtub; failures cluster. MTTDL at 3%: 3,913 years. Latent sector errors (3.45% of 1.53 million
  disks in 32 months), silent corruption (over 400,000 checksum mismatches), lost and misdirected writes. The
  end-to-end argument; checksums; scrubbing; replication.
* **13. fsync, and what applications must do.** The four places a write waits; fsync, flushes, the directory.
  Replacing a file, crashed at every point: in place, 6 of 18 torn; write and rename, intact, but with delayed
  allocation 36 of 97 leave an empty file (ext4, 2009); write, fsync, rename: all intact. Pillai et al. (2014): 60
  vulnerabilities in 11 applications. fsyncgate (PostgreSQL, 2018).
* **14. LSM trees.** O'Neil et al. (1996); memtable, log, SSTables, Bloom filters. Leveled against tiered compaction
  on a tiny tree, flush by flush. At 200,000 puts over 100,000 keys: leveled writes 11.9× and keeps 2 runs; tiered
  2.2× with 19 runs; reads for absent keys 2 and 19 without filters, 0.016 and 0.16 with 10 bits a key; space 1.01
  and 1.83. A B-tree: 41× write amplification, 18× with half its leaves cached. The RUM conjecture.
* **15. PebbleOS gets a disk.** The device and the kernel's file-system code; `cat /novels/emma` byte for byte. The
  thirty novels on PebbleFS: 24,971,526 bytes, 24,640 block reads, 76 jumps; 0.51 s on the model disk, 102 s on an
  aged disk, 17 ms on flash. A key-value store: *Pride and Prejudice*'s word counts in an LSM tree whose runs are
  files. **Ledger row 12**: tok reading from PebbleFS piped to the job, fitted on 32 passages (held-out error 0.2%
  for tok, 1.5% for the kernel), 2.65 billion instructions, 2.15 s of computation plus 0.51 s of disk: 2.66 s. The
  kernel spends 22.1 instructions a byte, against 23.0 from the tape.
* **16. Frontier: storage that can be trusted.** The LSM design space: Monkey's Bloom allocation (0.041 against 0.012
  wasted reads per absent lookup at 10 bits a key, 3.5×), Dostoevsky. Verified crash consistency: 2^k crash states
  (9 for 3 writes, 1,025 for 10); FSCQ, Yggdrasil, CrashMonkey. Zoned storage: write amplification 1.0 for
  sequential writes against 7.5 random. Six open problems.
* **Outro.** Recap, payoffs, practice, problems, next part.

## Build

```bash
python -m videos.cs.cs34.compute          # every item (pebble takes about five minutes)
python -m unittest tests.test_cs34_storage
python tools/build.py cs34
```

## Problems, with solutions

1. **The average seek.** Derive the average seek of the square-root model: show E√|U − V| = 8/15 for independent
   uniform U, V on [0, 1].

   *Solution.* D = |U − V| has density 2(1 − d) on [0, 1] (the two triangles of the unit square beyond distance d have
   total area (1 − d)², so P(D > d) = (1 − d)²). Then E√D = ∫₀¹ 2(1 − d) d^{1/2} dd = 2(2/3 − 2/5) = 8/15. So the
   average seek is t_min + (t_max − t_min)·8/15 = 0.5 + 15.5 × 8/15 = 8.77 ms.

2. **Write amplification and write cost.** Show that a flash collector whose victims hold on average a fraction u of
   live pages has write amplification 1/(1 − u), and that LFS's cleaner, which also reads each segment, has write
   cost 2/(1 − u).

   *Solution.* Collecting a victim of B pages copies uB live pages and frees B pages, of which (1 − u)B are new free
   space after the copies. The host then fills those (1 − u)B pages. In steady state, per (1 − u)B host writes the
   flash writes (1 − u)B + uB = B pages: amplification B / ((1 − u)B) = 1/(1 − u). LFS's cleaner must also read the
   whole segment (B) to find its live blocks, so the traffic per (1 − u)B of new data is B + uB + (1 − u)B = 2B: a
   write cost of 2/(1 − u). (For flash the FTL knows which pages are live from its map, so it reads only the uB live
   pages, and those reads are cheap compared with programs and erases.)

3. **Ordered journaling is atomic.** Show that ordered journaling with a commit block leaves, after any crash and
   replay, either the old file system or the new one, for an operation whose data goes only to newly allocated
   blocks.

   *Solution.* The writes come in four flushed epochs: (1) the new data, into blocks free in the old file system;
   (2) the descriptor and copies; (3) the commit; (4) the checkpoint, then clearing the journal.
   - *Crash before the commit is durable.* No home metadata block has been written (they are written only in epoch
     4), and the data went only to blocks the old metadata calls free, so the old file system is intact. Recovery
     finds a descriptor without a matching commit (a stale commit from an earlier transaction has a different
     sequence number) and discards it.
   - *Crash after the commit is durable.* The copies were flushed before the commit, so the journal holds the
     complete new metadata. Recovery writes every copy to its home. Some homes may already hold the new contents
     (a partial checkpoint); writing them again changes nothing, so replay is idempotent, and a crash during replay
     is handled by replaying again. The data was flushed in epoch 1, so the new file system is complete.
   - The argument uses the flush between the copies and the commit; without it the commit can be durable while a copy
     is not, and replay installs a stale block, which is what the checker found (25 of 208 corrupt) and what a
     checksum of the copies in the commit block repairs. Data overwritten *in place* is not covered: chapter 13's
     torn files.

4. **RAID 6.** Derive the formula that recovers two lost data blocks from P and Q.

   *Solution.* Let x < y be the lost disks, and let P′ and Q′ be P and Q with the surviving data added back in:
   P′ = Dx ⊕ Dy and Q′ = g^x·Dx ⊕ g^y·Dy, in GF(256) with g = 2. Multiply the first by g^y and add the second:
   g^y·P′ ⊕ Q′ = (g^x ⊕ g^y)·Dx. Since g generates the field's multiplicative group (order 255) and 0 < y − x < 255,
   g^x ≠ g^y, so the coefficient is nonzero and Dx = (g^y P′ ⊕ Q′)/(g^x ⊕ g^y) = (g^{y−x} P′ ⊕ g^{−x} Q′)/(g^{y−x} ⊕ 1),
   byte by byte. Then Dy = P′ ⊕ Dx. If one data disk and P are lost, recover the data from Q alone
   (Dx = Q′·g^{−x}); if P and Q are lost, recompute them.

5. **Build: writing files in PebbleOS.** Give PebbleOS a `write` system call for files, allocating blocks with a
   bitmap, and crash-test it with the checker.

   *Outline.* Add command 2 (write) to the device, and have `DiskMachine` append each written block to a `Disk.trace`
   and treat a store of 3 as a flush. In the kernel, `write(3, buf, n)` reads the inode; for each block past the end
   of the file it reads the data bitmap, finds a clear bit, sets it, and records the block in the inode (through
   `bmap`, extended to allocate an indirect block when needed); it copies the bytes into the data buffer and writes
   it. Order the writes as `careful` mode does: data and bitmap, flush, inode, flush. Then run the program, take the
   trace, and give it to `crash_states` with the disk before the program ran; every state should pass `fsck` with at
   worst leaks. Count the kernel's instructions per byte written, against `read`'s 22.

6. **★ Research: minimum flushes.** For each PebbleFS operation, find the fewest flushes (and a write order) so that
   every crash state is at worst a leak. Is there a polynomial algorithm from the dependency graph?

   *What is known, and a start.* For one operation, write the safety rules as a dependency graph on the blocks it
   writes: a block must be durable before any block that points to it (data before indirect block before inode
   before directory entry when allocating; a pointer cleared before the block or inode is freed). A schedule with f
   flushes is a division of the writes into f epochs, and a crash leaves only leaks exactly when every dependency goes
   from an earlier epoch to a later one. So the minimum is the number of blocks on the longest dependency path,
   achieved by giving each write its depth in the graph: polynomial (a topological sort). Careful mode is not
   minimal: it puts the bitmap in an epoch of its own, though nothing the bitmap points to depends on it. Merging
   the data and the bitmap epochs when allocating, the checker confirms every crash point is still at worst a leak,
   with 11 flushes for the four operations instead of 13. The open part is many operations at once: one block holds
   many inodes and many bitmap bits, so two operations can require opposite orders of the same two blocks, a cycle.
   Soft updates break such cycles by rolling back an update in the buffer before writing the block. Minimizing
   flushes for a batch with shared blocks resembles feedback arc set, which is NP-hard in general; whether it is
   NP-hard for the structures a file system creates is open.

## 习题与解答

1. **平均寻道时间。** 推导平方根模型的平均寻道时间：证明对 [0, 1] 上独立均匀的 U、V，E√|U − V| = 8/15。

   *解答。* D = |U − V| 在 [0, 1] 上的密度为 2(1 − d)（单位正方形中距离超过 d 的两个三角形面积共为 (1 − d)²，所以
   P(D > d) = (1 − d)²）。于是 E√D = ∫₀¹ 2(1 − d) d^{1/2} dd = 2(2/3 − 2/5) = 8/15，平均寻道为
   0.5 + 15.5 × 8/15 = 8.77 ms。

2. **写放大与写代价。** 证明：若闪存回收器所选的受害块平均有比例 u 的页仍然有效，写放大为 1/(1 − u)；而 LFS 的清理器
   还要读整个段，写代价为 2/(1 − u)。

   *解答。* 回收一个 B 页的块要复制 uB 个有效页，复制后净得 (1 − u)B 个空页，由主机写满。稳态下，每 (1 − u)B 次主机写，
   闪存写 (1 − u)B + uB = B 页，写放大为 1/(1 − u)。LFS 清理器还要读整个段（B）才能找出有效块，所以每 (1 − u)B 的新数据，
   磁盘流量为 B + uB + (1 − u)B = 2B，写代价 2/(1 − u)。（闪存转换层靠映射表就知道哪些页有效，只需读那 uB 页，而读远比编程
   和擦除便宜。）

3. **有序日志是原子的。** 证明：对只把数据写进新分配块的操作，带提交块的有序日志在任何崩溃并重放之后，留下的要么是旧文件
   系统，要么是新文件系统。

   *解答。* 写分四个以刷新隔开的阶段：(1) 新数据写进旧文件系统中空闲的块；(2) 描述块与副本；(3) 提交块；(4) 检查点，然后
   清空日志。
   - *提交块落盘之前崩溃。* 元数据的原位块一个都没写（只在第 4 阶段写），数据只写进旧元数据认为空闲的块，所以旧文件系统
     完好。恢复时看到没有匹配提交块的描述块（之前事务留下的旧提交块序号不同），丢弃它。
   - *提交块落盘之后崩溃。* 副本在提交之前已刷新，日志里有完整的新元数据，恢复把每个副本写回原位。有些原位块可能已是新
     内容（检查点做了一半），再写一遍不改变任何东西，所以重放是幂等的，重放中途崩溃就再重放一次。数据在第 1 阶段已刷新，
     新文件系统完整。
   - 论证用到了副本与提交之间的那次刷新；去掉它，提交块可能先于某个副本落盘，重放就装上了过期的块，正是检查器找到的
     （208 个中 25 个损坏），而在提交块里存副本的校验和可以修复。*原地*覆写的数据不在此列：第 13 章的撕裂文件。

4. **RAID 6。** 推导用 P 和 Q 恢复两个丢失数据块的公式。

   *解答。* 设丢失的盘为 x < y，把幸存数据加回 P、Q 得 P′ = Dx ⊕ Dy，Q′ = g^x·Dx ⊕ g^y·Dy（GF(256)，g = 2）。第一式乘
   g^y 再加第二式：g^y·P′ ⊕ Q′ = (g^x ⊕ g^y)·Dx。g 生成乘法群（阶 255），0 < y − x < 255，故 g^x ≠ g^y，系数非零，
   Dx = (g^{y−x} P′ ⊕ g^{−x} Q′)/(g^{y−x} ⊕ 1)（逐字节）。然后 Dy = P′ ⊕ Dx。若丢的是一个数据盘和 P，只用 Q 恢复
   （Dx = Q′·g^{−x}）；若丢的是 P 和 Q，重新计算即可。

5. **动手：让 PebbleOS 写文件。** 给 PebbleOS 加一个写文件的 `write` 系统调用，用位图分配块，并用检查器做崩溃测试。

   *思路。* 给设备加命令 2（写），让 `DiskMachine` 把每个写出的块追加到 `Disk.trace`，并把写 3 当作刷新。内核里，
   `write(3, buf, n)` 读出 inode；对文件末尾之后的每个块，读数据位图、找一个空位、置位，并把块记入 inode（通过扩展后的
   `bmap`，需要时分配间接块）；把字节拷进数据缓冲再写出。按 `careful` 模式排序：数据与位图，刷新，inode，刷新。运行程序，
   取出 trace，连同运行前的磁盘交给 `crash_states`；每个状态都应通过 `fsck`，至多泄漏。统计每写一字节的内核指令数，与
   `read` 的 22 条比较。

6. **★ 研究：最少刷新。** 对 PebbleFS 的每个操作，找出最少的刷新次数（及写入顺序），使每个崩溃状态至多是泄漏。能否从依赖图
   在多项式时间内求出？

   *已知结果与起点。* 对单个操作，把安全规则写成它所写各块上的依赖图：一个块必须先于指向它的块落盘（分配时：数据先于
   间接块先于 inode 先于目录项；释放时：先清指针，再释放块或 inode）。有 f 次刷新的调度就是把写分成 f 个阶段；崩溃只会
   泄漏，当且仅当每条依赖都从较早阶段指向较晚阶段。所以最少次数是最长依赖路径上的块数，按每个写在图中的深度分配阶段即可
   达到：拓扑排序，多项式时间。careful 模式并不最优：它让位图单独占一个阶段，而没有什么东西依赖于位图所指的内容。分配时把
   数据与位图合为一个阶段，检查器确认每个崩溃点仍至多泄漏，四个操作共 11 次刷新而不是 13 次。开放的是多个操作同时进行：一个
   块里有许多 inode 和许多位图位，两个操作可能要求同一对块的相反顺序，形成环。软更新在写块前于缓冲中回滚某个更新来打破这种
   环。带共享块的一批操作的最少刷新类似反馈弧集问题，后者一般是 NP 难的；对文件系统产生的结构是否 NP 难，尚未可知。

## Glossary additions

* **block device**: storage seen as a numbered array of fixed-size blocks, read and written whole.
* **seek, rotational delay, transfer**: the three parts of a disk access.
* **FTL** (flash translation layer): the drive's map from logical to physical pages, with garbage collection.
* **write amplification**: bytes the device (or engine) writes per byte the host asks it to write.
* **over-provisioning**: flash kept hidden from the host as spare space for the collector.
* **TRIM**: the command by which a file system tells a drive which blocks are free.
* **inode**: the record of a file's metadata and the location of its blocks; **extent**: a (first block, length) run.
* **fsck**: the offline check of a file system's invariants.
* **journal** (write-ahead log): changes recorded, and committed with one block write, before they are made.
* **ordered mode**: data written to its home before the metadata that points to it commits.
* **copy-on-write**: never overwrite; write new copies up to a new root; **snapshot**: an old root kept alive.
* **scrub**: reading everything to find and repair latent errors while redundancy exists.
* **RAID**: redundancy across disks: striping, mirroring, parity (RAID 5), double parity (RAID 6).
* **MTTDL**: mean time to data loss.
* **LSM tree**: a write-optimized index of sorted runs merged by **compaction**, leveled or tiered.
* **zoned storage**: devices whose zones must be written sequentially and reset whole.

## Sources

* R. H. Arpaci-Dusseau and A. C. Arpaci-Dusseau, *Operating Systems: Three Easy Pieces*, persistence chapters.
* A. Petrov, *Database Internals*, part I; D. Giampaolo, *Practical File System Design*.
* M. K. McKusick, W. N. Joy, S. J. Leffler and R. S. Fabry, "A Fast File System for UNIX", ACM TOCS (1984).
* G. R. Ganger and Y. N. Patt, "Metadata Update Performance in File Systems", OSDI (1994): soft updates.
* R. Hagmann, "Reimplementing the Cedar File System Using Logging and Group Commit", SOSP (1987).
* M. Rosenblum and J. K. Ousterhout, "The Design and Implementation of a Log-Structured File System", ACM TOCS (1992).
* D. Hitz, J. Lau and M. Malcolm, "File System Design for an NFS File Server Appliance", USENIX (1994): WAFL.
* D. A. Patterson, G. Gibson and R. H. Katz, "A Case for Redundant Arrays of Inexpensive Disks (RAID)", SIGMOD (1988).
* H. P. Anvin, "The mathematics of RAID-6".
* B. Schroeder and G. A. Gibson, "Disk Failures in the Real World", FAST (2007).
* L. N. Bairavasundaram et al., "An Analysis of Latent Sector Errors in Disk Drives", SIGMETRICS (2007); "An Analysis
  of Data Corruption in the Storage Stack", FAST (2008).
* J. H. Saltzer, D. P. Reed and D. D. Clark, "End-to-End Arguments in System Design", ACM TOCS (1984).
* C. Ruemmler and J. Wilkes, "An Introduction to Disk Drive Modeling", IEEE Computer (1994).
* N. Agrawal et al., "Design Tradeoffs for SSD Performance", USENIX ATC (2008).
* T. S. Pillai et al., "All File Systems Are Not Created Equal", OSDI (2014).
* P. O'Neil, E. Cheng, D. Gawlick and E. O'Neil, "The Log-Structured Merge-Tree", Acta Informatica (1996).
* F. Chang et al., "Bigtable", OSDI (2006).
* M. Athanassoulis et al., "Designing Access Methods: The RUM Conjecture", EDBT (2016).
* N. Dayan, M. Athanassoulis and S. Idreos, "Monkey: Optimal Navigable Key-Value Store", SIGMOD (2017);
  "Dostoevsky", SIGMOD (2018).
* H. Chen et al., "Using Crash Hoare Logic for Certifying the FSCQ File System", SOSP (2015).
* H. Sigurbjarnarson et al., "Push-Button Verification of File Systems via Crash Refinement", OSDI (2016).
* J. Mohan et al., "Finding Crash-Consistency Bugs with Bounded Black-Box Crash Testing", OSDI (2018).
* M. Bjørling et al., "ZNS: Avoiding the Block Interface Tax for Flash-based SSDs", USENIX ATC (2021).
