# Computer Science, Built — Part 11: The Running Program

Part 11 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the first part of Act III, *Speaking to the Machine*. One program, followed from source
text to a running process: how its data becomes bytes, its control flow branches, its calls a stack and its names
addresses; how the heap is managed; how object files are linked and loaded; and how one unchecked copy turns input
into code. Pebble gains an object-file format, a linker and a loader (`explainer/cs/pebble/link.py`), a heap
simulator with five allocators (`heap.py`), the Job rewritten as four linked files with frames and a heap list
(`jobv1.py`), and a stack-smash demonstration with its defences (`smash.py`), all tested in `tests/test_cs11_link.py`
and `tests/test_cs11_running.py`. This machine's side is measured by compiling small C programs and reading them
with readelf; every number is computed in `compute.py`.

* **From text to a running process.** The Job as four object files with 16 holes, linked into 864 bytes, printing the
  same twenty words as Part 6's program; a greeting program that prints "pwned" when given 81 chosen bytes.
* **1. A program's life.** Compiler, assembler, linker, loader; one `call lookup` followed from source to a patched
  jump.
* **2. Data in memory.** Endianness measured (`0d 0c 0b 0a`), Cohen (1980); alignment and padding compiled here
  (12 bytes against 8 for the same fields; the Job's node 24 bytes on x86-64, 16 on Pebble); row-major arrays;
  pointer arithmetic.
* **3. Control flow.** Ifs and loops as branches, the unsigned range test; a dense switch compiled by gcc -O2 into a
  jump table, each case a tail call through the PLT.
* **4. The call stack.** Pebble's calling convention (a0–a5, ra, caller-saved t0–t3, callee-saved s0–s2, 16-byte sp);
  lookup's frame; fact(10) frame by frame on the emulator (10 frames, 160 bytes); gdb's backtrace of a C factorial
  on this machine, its frames 32 bytes apart and their saved return addresses.
* **5. Recursion, depth and tail calls.** Ackermann on Pebble: A(3, 6) = 509 in 172,233 calls, 511 frames deep; a
  tail call made a jump (1,616 bytes of stack and 1,013 instructions against 0 and 409); guard pages and limits.
* **6. The heap.** malloc and free; free lists, Knuth's boundary tags, coalescing; a real trace: Perl counting Pride
  and Prejudice, 146,336 allocations recorded with an LD_PRELOAD interposer, nearly all of 16 bytes or less, peaking
  near 2 MB live.
* **7. Five allocators.** First fit, next fit, best fit, segregated fits and the buddy system on that trace:
  fragmentation 1.13, 1.14, 1.13, 1.13 and 1.79; 3.3, 16.7, 2.1, 0.9 and 2.2 blocks examined per request; the buddy
  system (Knowlton 1965); ptmalloc, jemalloc, tcmalloc, mimalloc.
* **8. Knuth's rule and Robson's bounds.** Derive the approximate hole-count relation under stationary,
  uniformly random deletion and immediate coalescing, neglecting boundary/growth effects. The stored `p` uses the
  full run while hole averages use the post-warm-up window. Replay an eight-phase adversarial trace on first fit
  and best fit: total block sizes 32–4,096 bytes (ratio 128), heap/M 1–4.5. The matching reference curve is an
  illustration, not an exact finite universal theorem or a proof against every allocator.
* **9. Object files.** ELF sections, symbols and relocations of two C files compiled here; gcc turning a counting loop
  into `strlen`; strong and weak symbols; the linker's errors.
* **10. Linking, step by step.** Pebble's linker on the Job: resolution, layout (text, data, 384 KB of bss), the 16
  relocations patched; static archives and link order (`main.o libjob.a` takes only `count.o`, 16 KB against
  112 KB; `libjob.a main.o` fails with an undefined reference).
* **11. Dynamic linking.** This host's hello binaries occupy 741 KiB static and
  16 KiB dynamic. Recorded best batch-average launches are 0.63
  and 0.90 ms, including process creation/execution; the difference does not isolate linking.
  PIC includes PC-relative references and GOT indirection. The PLT diagram illustrates optional lazy binding;
  eager binding and compiler/linker options change it. Interposition records the Perl trace.
* **12. Loading and the address space.** /proc/self/maps; ASLR across three PIE runs; `setarch -R` is rejected in this environment, so no fixed-address result is claimed;
  argv and argc on the stack, as Pebble's loader builds them.
* **13. Undefined behaviour.** `x + 1 > x` folded to 1; a wrapping loop running 3 times at -O0 and 2 at -O2; a null
  check deleted at -O2; the 2009 Linux TUN bug; UBSan and AddressSanitizer catching an overflow, a heap overrun, a
  use after free and a stack overrun; red zones, quarantine and shadow memory; workload-specific overhead measured here. The shadow check handles partial groups; the standard ASan runtime is a
  testing tool, not a production-hardened security runtime.
* **14. Smashing the stack.** The frame; an 81-byte toy Pebble input (72 code bytes, padding, a saved address and newline); the Morris worm
  (1988), Aleph One (1996); a canary, a no-execute stack, randomization, bounds; return-oriented programming.
* **15. The Job, linked.** Version 1 against version 0: identical output; +4% on a paragraph, −6% on chapter 1, −11%
  on 20,000 bytes; 320 bytes of stack at most.
* **16. Frontier: bounds, semantics, capabilities.** A CHERI-style capability machine traps the attack on its 65th
  byte; CompCert, Cerberus and pointer provenance; open questions about allocators' worst cases and use-after-free.
* **Recap, where this comes back, in practice, problems.**

## Interpretation and measurement scope

The numerical cache is a recorded experiment, not a cross-platform promise. All twenty original JSON payloads are
preserved during this polish. Binary sizes are KiB (1,024 bytes); heap charts use decimal MB. Host instruction
selection, addresses, launch/sanitizer times and ABI layout belong to the recorded compiler/platform. ASLR is
not a bounds check. The capability model is a small spatial check, not complete CHERI or temporal revocation.
CompCert's semantic-preservation theorem has a supported language, verified passes and trusted boundaries.

Heap ratio means **peak heap / peak requested live bytes**, including headers, alignment, rounding and holes;
the two peaks need not be simultaneous. Blocks examined per allocation are simulated operations, not elapsed
speed. Boundary tags are a conceptual design; the Python simulator uses dictionaries/lists and does not charge
a literal footer. Buddy payload requests include the 8-byte header and 16-byte alignment before power-of-two
rounding: 16 bytes needs a 32-byte block, while 25 or 30 bytes needs 64. The diagrams and narration now agree.

The startup stack drawing intentionally omits Linux environment pointers and auxiliary-vector details. The GOT/PLT
view shows one lazy-binding path. Runtime, compiler, library and defense behavior depends on configuration;
passing a finite simulator or sanitizer run is not a proof of correctness for all programs.

## Build

```bash
python -m videos.cs.cs11.compute           # every number in the part (about a minute; needs gcc, readelf, perl)
python tools/build.py cs11 -q l            # a 480p preview
python tools/build.py cs11                 # 1080p
```

The measurements (`layout`, `switch`, `elf`, `dynamic`, `aslr`, `maps`, `ub`) belong to the computer and compiler
that run them; `heap` records its trace once into `.cache/cs11/perl.mtrace` and replays it.

## Problems, with solutions

1. **Padding.** On x86-64, how big is `struct { char a; double b; short c; char d; }`? Reorder it to make it as small
   as possible.

   *Solution.* `a` at 0, seven bytes of padding, `b` at 8, `c` at 16, `d` at 18, then padding to a multiple of 8:
   **24 bytes**. Largest first, `{ double b; short c; char a; char d; }`: 8 + 2 + 1 + 1 = 12, padded to **16**.

2. **A frame.** Write the prologue and epilogue of a Pebble function that calls another function and uses `s0` and
   `s1`. How big is its frame?

   *Solution.* It must save `ra` (the call overwrites it) and both s-registers: 12 bytes, rounded up to keep `sp`
   16-byte aligned: **16 bytes**.

   ```
   f:   addi sp, sp, -16        lw   s1, 4(sp)
        sw   ra, 12(sp)         lw   s0, 8(sp)
        sw   s0, 8(sp)          lw   ra, 12(sp)
        sw   s1, 4(sp)          addi sp, sp, 16
        ...                     ret
   ```

3. **Holes.** A first-fit heap holds 1,000 blocks, and 80% of allocations split their hole. About how many holes?

   *Solution.* Knuth's rule: ½ p N = ½ × 0.8 × 1,000 = **about 400**, assuming uniformly selected frees, stationarity and negligible boundary/growth effects.
   This estimates hole count, not wasted bytes. The displayed 399 is a finite-sample mean for this workload.

4. **A relocation.** `la t0, sym` with `sym` at `0x12345`: what do the immediates become?

   *Solution.* 0x12345 = 74,565. `lui` takes the top 22 bits, 74,565 >> 10 = **72** (`0x48`); `ori` the low 10,
   74,565 & 1023 = **837** (`0x345`). Check: 72 × 1024 + 837 = 74,565.

5. **Build: an allocator in Pebble.** Write first-fit `malloc` and `free` with boundary tags in Pebble assembly, replay
   Perl's first 10,000 events on the emulator, and compare with `heap.py`.

   *Solution sketch.* Keep each block's size, with the low bit as the in-use flag, in a header word and in a footer
   word; keep free blocks in an address-ordered doubly linked list (next and previous pointers in the free block's
   payload). `malloc` walks the list from its head and splits when the remainder is at least 32 bytes; `free` reads
   the footer just before its header to find the previous block, and the header just after its end to find the
   next, merging with either if free. Drive it from a tape of events: generate the tape from `heap.events(...)[:10000]`
   as 32-bit records (op, id, size), and keep a table of id → pointer in the Pebble program's `.bss`. With the same
   header, alignment and split rules as `heap.FirstFit`, the high-water mark should match `heap.py`'s exactly; any
   difference is a bug in one of them. The emulator runs about a million instructions a second, so the replay takes
   a few seconds.

6. ★ **Research: define the allocation model before comparing bounds.** State the live-storage bound,
   minimum allocation unit, maximum block size, online information and whether live blocks may move. Compare
   Robson's 1971/1974 general bounds with his 1977 policy-specific first-fit/best-fit results. What does the
   chapter's eight-phase trace actually establish?

   *Worked guidance.* The replay establishes measured behavior for two particular implementations on one trace.
   Its curve is not a proof of a universal finite formula. Enumerate tiny legal traces while checking live-storage
   limits, block disjointness and units; a counterexample can disprove a proposed upper bound, while an apparent
   pattern still needs proof. Separate general lower bounds from policy-specific upper bounds and account for
   finite-size corrections. Moving or fragmented allocation and constrained lifetimes change the model.

## 习题与解答

1. **填充。** 在 x86-64 上，`struct { char a; double b; short c; char d; }` 有多大？重排字段使它尽可能小。

   *解答。* `a` 在 0，七个字节的填充，`b` 在 8，`c` 在 16，`d` 在 18，再填充到 8 的倍数：**24 字节**。按从大到小排，
   `{ double b; short c; char a; char d; }`：8 + 2 + 1 + 1 = 12，填充到 **16**。

2. **一个栈帧。** 写出一个调用了别的函数、并使用 `s0` 和 `s1` 的 Pebble 函数的序言和尾声。它的帧有多大？

   *解答。* 它必须保存 `ra`（调用会覆盖它）和两个 s 寄存器：12 字节，为保持 `sp` 16 字节对齐向上取整：**16 字节**。
   代码见上面英文部分。

3. **空洞。** 一个首次适配的堆里有 1,000 个块，80% 的分配会切开它的空洞。大约有多少个空洞？

   *解答。* 克努特法则：½ p N = ½ × 0.8 × 1,000 = **约 400**，前提是均匀选择释放、近似平稳，且忽略边界与堆扩展。它估计空洞个数而非浪费字节；399 是该负载下的有限样本均值。

4. **一次重定位。** `sym` 在 `0x12345` 时，`la t0, sym` 的立即数变成什么？

   *解答。* 0x12345 = 74,565。`lui` 取高 22 位，74,565 >> 10 = **72**（`0x48`）；`ori` 取低 10 位，74,565 & 1023 =
   **837**（`0x345`）。验算：72 × 1024 + 837 = 74,565。

5. **动手：Pebble 上的分配器。** 用 Pebble 汇编写出带边界标签的首次适配 `malloc` 和 `free`，在模拟器上重放 Perl 的
   前 10,000 个事件，并与 `heap.py` 比较。

   *解答提要。* 把每个块的大小（最低位作为在用标志）放在头部字和尾部字里；空闲块按地址顺序串成双向链表（next 和 prev
   指针放在空闲块的载荷里）。`malloc` 从表头开始走，剩余至少 32 字节时切开；`free` 读自己头部之前的尾部字找到前一个块，
   读自己末尾之后的头部字找到后一个块，空闲就合并。用事件带驱动它：把 `heap.events(...)[:10000]` 生成 32 位记录
   （操作、编号、大小）的带子，在 Pebble 程序的 `.bss` 里放一张编号 → 指针的表。头部、对齐和切分规则与 `heap.FirstFit`
   相同的话，最高水位应当与 `heap.py` 完全一致；任何差别都是其中一方的错误。

6. ★ **研究：比较界之前先定义分配模型。** 明确活动存储上限、最小分配单位、最大块大小、在线信息，
   以及是否允许移动活动块。比较罗布森1971/1974年的一般界与1977年的首次适配、最佳适配专门结果。
   本章八阶段轨迹实际证明了什么？

   *解答指导。* 重放只确立两种具体实现对一条轨迹的测量，不是普遍有限公式的证明。枚举微小合法轨迹，
   检查活动存储上限、块不重叠及单位。反例能推翻候选上界，而观察到规律仍需证明。区分一般下界与特定策略
   上界，并计入有限大小修正。允许移动、允许请求分片或限制生命周期，都会改变模型。

## Glossary additions

源代码 source code · 编译器 compiler · 汇编器 assembler · 链接器 linker · 装载器 loader · 进程 process · 字节序 endianness ·
大端 / 小端 big-endian / little-endian · 对齐 alignment · 填充 padding · 行主序 row-major order · 指针运算 pointer arithmetic ·
跳转表 jump table · 调用约定 calling convention · 调用者保存 / 被调用者保存 caller-saved / callee-saved · 栈帧 stack frame ·
活动记录 activation record · 序言 / 尾声 prologue / epilogue · 尾调用 tail call · 保护页 guard page · 堆 heap · 空闲链表 free
list · 边界标签 boundary tag · 合并 coalescing · 首次适配 first fit · 下次适配 next fit · 最佳适配 best fit · 分离适配
segregated fits · 伙伴系统 buddy system · 内部碎片 / 外部碎片 internal / external fragmentation · 五十百分比法则 fifty-percent
rule · 目标文件 object file · 节 section · 符号表 symbol table · 重定位 relocation · 强符号 / 弱符号 strong / weak symbol ·
静态链接 / 动态链接 static / dynamic linking · 位置无关代码 position-independent code · 全局偏移表 GOT · 过程链接表 PLT ·
延迟绑定 lazy binding · 插桩替换 interposition · 地址空间 address space · 地址空间布局随机化 ASLR · 未定义行为 undefined
behaviour · 栈溢出攻击 stack smashing · 栈金丝雀 stack canary · 不可执行栈 no-execute stack · 返回导向编程 return-oriented
programming · 能力 capability · 指针来源 pointer provenance

## Sources

*Canon.* Books: Bryant & O'Hallaron, *Computer Systems: A Programmer's Perspective*, 3rd ed., ch. 3, 7, 9; Levine,
*Linkers and Loaders* (2000); Knuth, *The Art of Computer Programming*, vol. 1, §2.5 (dynamic storage allocation,
boundary tags, the fifty-percent rule); the System V Application Binary Interface with its x86-64 and RISC-V
supplements; the ISO C standard (undefined behaviour, annex J).

Papers: Knowlton, "A fast storage allocator" (1965); Robson, "An estimate of the store size necessary for dynamic
storage allocation" (1971) and "Bounds for some functions concerning dynamic storage allocation" (1974); Robson,
"Worst case fragmentation of first fit and best fit storage allocation strategies" (1977); Cohen, "On holy wars and a
plea for peace" (1980); Gingell, Lee, Dang & Weeks, "Shared libraries in SunOS" (1987); Spafford, "The Internet worm
program: an analysis" (1988); Wilson, Johnstone, Neely & Boles, "Dynamic storage allocation: a survey and critical
review" (1995); Aleph One, "Smashing the stack for fun and profit", Phrack 49 (1996); Johnstone & Wilson, "The memory
fragmentation problem: solved?" (1998); Shacham, "The geometry of innocent flesh on the bone: return-into-libc
without function calls" (2007).

*Recent.* Leroy, "Formal verification of a realistic compiler", CACM (2009); Wang, Zeldovich, Kaashoek & Solar-Lezama,
"Towards optimization-safe systems: analyzing the impact of undefined behavior" (2013); Watson et al., "CHERI: a hybrid
capability-system architecture for scalable software compartmentalization", IEEE S&P (2015); Memarian et al., "Into
the depths of C: elaborating the de facto standards", PLDI (2016) and "Exploring C semantics and pointer provenance",
POPL (2019); Arm, the Morello prototype (2022).
