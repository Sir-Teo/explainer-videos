# Computer Science, Built — Part 55: Trusting Trust

Part 55 of a sixty-one-part course in computer science (see [the series plan](../README.md) and
[the syllabus](../SYLLABUS.md)), the fifth and last part of Act X, *Horizons and Trust*, and the end of the degree.
Security is a property of the whole tower, and every layer we built leaks: buffers overflow, speculation leaves
traces, DRAM rows disturb their neighbours, parsers confuse code with data. In 1984 Ken Thompson showed that even a
compiler you built yourself can hide a backdoor its own source never shows. We build his attack against our own
compiler, then catch it with diverse double-compiling, and close the series by walking the tower one last time, from
a NAND gate to a cluster.

The instruments are in `explainer/cs/trust/` (tested in `tests/test_cs55_memory.py` and `tests/test_cs55_trojan.py`):
* `memory.py`: Part 11's stack smash run on Pebble under every combination of stack canary, W^X and ASLR; the entropy
  of ASLR with a small runnable confirmation; return-oriented programming — Galileo-style gadget discovery on our
  fixed-width ISA and a gadget chain that runs with W^X on; and a tiny borrow checker for Rust-style ownership (Part
  14's affine types).
* `auth.py`: password entropy and guessing times, with a Zipf model of human choice; HOTP and TOTP checked against
  the RFC 4226 and 6238 test vectors; and the Needham–Schroeder protocol explored by a breadth-first Dolev–Yao search
  that finds Lowe's attack and clears his fix.
* `access.py`: Lampson's access matrix and its two slicings (ACLs and capabilities), the confused deputy, the
  Bell–LaPadula lattice, and a bounded safety search over the HRU model.
* `web.py`: SQL injection on Part 35's own database engine and the parameterised-query fix (a parsing fix, Part 12);
  and an HTML templater, escaped against raw, parsed to show the trees differ.
* `trojan.py`: Thompson's trojan compiler built on our own machinery — the backdoored login, the self-reproducing
  compiler (Part 25's quine), and the fixpoint — then Wheeler's diverse double-compiling that catches it, and a toy
  reproducible build.

## Chapters

* **Hook.** Every layer of the tower, named with the leak that crosses it: Rowhammer (Part 5), Spectre (Part 8), the
  stack smash (Part 11), a sandbox escape (Part 31), the compiler backdoor (Part 13), a BGP hijack (Part 36),
  injection (Part 42), the xz backdoor (Part 41). Then the attack that closes the series: our clean compiler binary
  (499 bytes), our trojaned one (1,119 bytes), and a compiler rebuilt from the clean source by the trojaned binary —
  1,119 bytes again, the same hash, byte for byte.
* **1. Threat models and principles.** The CIA triad; a threat model as assets, a trust boundary and trusted
  computing base, an adversary, and the attack surface; a timeline of the attacks this part meets (the Morris worm
  1988, Aleph One 1996, Rowhammer 2014, Spectre and Meltdown 2018, xz-utils 2024); Saltzer and Schroeder's eight
  principles (1975), plus work factor and compromise recording; and the defender's asymmetry — one way in against
  every layer at once.
* **2. Memory corruption, and return-oriented programming.** The Part 11 stack smash into the saved return address;
  three defences run on Pebble under all eight combinations (canary → *caught*; W^X alone → *blocked* by a no-execute
  fault; a wrong ASLR guess → a *fault* at probability 1/64 in the demo); ASLR's arithmetic (p = 2⁻ᵏ, expected tries
  2ᵏ) with published layout entropies (32-bit stack 19 bits, 32-bit mmap 16, 32-bit PIE 8, 64-bit mmap 28, 64-bit
  PIE 30) and a runnable check (64 placements, exactly 1 hit, rate 2⁻⁶); ROP (Shacham 2007) — 8 gadgets discovered
  in our binary, a chain that prints "pwned" and halts with W^X fully on, while the canary still trips first; CFI
  (Abadi et al. 2005), shadow stacks, CHERI.
* **3. Memory safety.** The ≈70% statistic (Microsoft 2019 and Chromium each reported about seventy per cent of
  serious bugs were memory-safety bugs); ownership as an affine type — drop contraction, each value one owner (Part
  14); a tiny borrow checker run on ten programs, all ten verdicts matching what Rust would say; what is proved (no
  use-after-free, double free, data race or dangling pointer, by construction) and what is not (`unsafe`, logic
  errors); RustBelt's machine-checked soundness proof (Jung et al. 2018, Part 54).
* **4. When the hardware leaks.** Rowhammer (Kim et al. 2014) — 110 of 129 DDR3 modules flipped bits, some after
  ≈139,000 activations inside one 64 ms refresh; Spectre and Meltdown (2018) — speculation past a bounds check leaves
  a cache line warm, read back with Flush+Reload (Yarom & Falkner 2014); side channels generally (time, power, cache,
  sound) and Kocher's 1996 timing attack; constant-time code; the lesson that a mitigation is never free (the
  roofline of Part 9 moves) and the move to a hardware–software contract.
* **5. Who are you? Authentication.** Password entropy H = L·log₂N and expected crack time 2ᴴ/2R: at 10¹⁰ guesses/s,
  8 lowercase letters (≈38 bits) last about 10 s, 16 lowercase (≈75 bits) some 70,000 years; a Zipf model (after
  Bonneau 2012) where 10 guesses crack 18% of users and a million crack 86%, about 14 points per decade; salting, and
  a slow salted hash (10/s per core) buying a factor of 10⁹, so 8 lowercase now take over 300 years per core (bcrypt,
  scrypt, Argon2, Part 29); TOTP as an HMAC over the clock, reproducing all six RFC 6238 SHA-1 vectors (HOTP at
  counter 1 is 287082); passkeys and WebAuthn (2019, Part 30); and Needham–Schroeder (1978) with Lowe's attack
  (1995), found by our model checker (Part 54) among 19 states, and the fix — Bob names himself in message 2 — leaving
  no attack among 17.
* **6. Access control.** Lampson's matrix (1971) and a reference monitor; ACLs down the columns against capabilities
  along the rows; the confused deputy (Hardy 1988), run both ways — ambient authority overwrites the billing file,
  a capability refuses; Bell–LaPadula (1973), no read up and no write down over a lattice, five checks agreeing
  (including a flow that climbs a level yet is still denied for a missing category); the HRU safety question
  (Harrison, Ruzzo & Ullman 1976) — our bounded search finds a leak after 2 states, a revoke-only system none — and
  its undecidability by reduction from halting (Part 25).
* **7. Isolation.** Address spaces and page tables (Parts 31–32), so the wall is the kernel itself (seL4, ≈10,000
  lines, proved to enforce it — Klein et al. 2009); a ladder of walls (language sandbox, process, container, VM,
  separate machines) where an escape goes through whatever is shared (Dirty COW 2016, VENOM 2015); system-call
  filters (seccomp 2005, BPF filters since 2012; Capsicum 2010); site isolation (Chrome, on by default 2018, after
  Spectre) and WebAssembly's in-process sandbox (every major browser since 2017); SGX enclaves (2015) and their
  breaks (the controlled channel, Xu, Cui & Peinado 2015; Foreshadow 2018).
* **8. The web.** The same-origin policy (scheme, host, port) and the gap it leaves — a page may send where it cannot
  read; XSS, data parsed as code, our templater's raw output yielding a live `script` element where the escaped one
  yields only text; CSRF as the browser-as-confused-deputy, fixed with SameSite cookies and per-form tokens; SQL
  injection on Part 35's engine — an unquoted field turns the filter into `id = id` and all three rows' secrets spill
  — and its cure, a parsing fix (Part 12): parse the template once, bind values as finished leaves; PKI failure
  (DigiNotar 2011) and Certificate Transparency (RFC 6962, 2013).
* **9. Networks under attack.** Source-address spoofing, since routers forward on the destination alone (BCP 38,
  2000); amplification with factor A = r/q and measured factors (SNMPv2 6.3, SSDP 30.8, DNS 28–54, CharGEN 358.8, NTP
  556.9, memcached up to 51,000 — US-CERT TA14-017A), and GitHub absorbing ≈1.35 Tb/s off open memcached servers on
  28 February 2018; BGP hijacks on Part 36's 125-network internet (49 of 124 follow a same-prefix origin, all 124 a
  more-specific one; a quarter adopting RPKI leaves 61 fooled — Pakistan Telecom's 2008 YouTube hijack); Kaminsky's
  DNS race (≈656 races, about a minute, with a 16-bit ID; some 43 million races and ≈50 days once the source port is
  randomised; DNSSEC removes the guess); and the end-to-end lesson — assume the path is hostile, TLS guards what is
  said but not whether it arrives.
* **10. Supply chains.** The dependency tree (P ≈ e⁻ⁿᵖ: a thousand packages at one bad in ten thousand give a ≈10%
  chance of trouble, set by the least careful stranger); dependency confusion (Birsan 2021); build poisoning
  (SolarWinds 2020, fewer than 18,000 customers), where a signature says who built a binary, not from what source;
  the xz-utils backdoor (2024) hidden in the release tarball's build script, not the repository; its accidental
  discovery by Andres Freund on 29 March 2024 from a ≈500 ms slowdown (CVE-2024-3094); and the defences — SLSA
  (2021), SBOMs, reproducible builds — none of which checks that the source is honest.
* **11. Reflections on trusting trust.** Thompson's three stages, built on our own compiler. Stage 1: a backdoored
  `login` (236 bytes honest, 279 bytes with the extra line) — but the line is in the source. Stage 2: move it into
  the compiler, which backdoors `login` as it compiles it — but now the compiler's source shows it. Stage 3: Part
  25's quine, so the compiler also writes the trojan into any compiler it compiles; delete the trojan from every
  source file and the trojaned binary (1,119 bytes), compiling the clean source, reproduces itself bit for bit — a
  fixpoint — and still lets the magic password into `login`. The magic string is in no source. (Thompson 1984;
  Karger & Schell's Multics review, 1974.)
* **12. Catching the trojan.** Diverse double-compiling (Wheeler 2005, thesis 2009): with a second, independent
  compiler T (ours never inspects what it compiles), form X = T(c) and Z = X(c), and test Z = A bit for bit. On the
  honest compiler the two stage-1 binaries differ (499 vs 498 bytes) but both stage-2 binaries are 499 bytes and
  equal — *clean*. On Thompson's compiler stage 2 gives 1,119 bytes from the suspect against 499 from X — *TROJAN
  DETECTED*, because the trojan cannot hide in a compiler it never touched. The bit-for-bit test needs reproducible
  builds (our toy build's timestamp/path make two hashes differ until normalised; Tor and Debian since 2013), and the
  trusted compiler itself is grown from an auditable seed (bootstrappable builds; GNU Guix's full-source bootstrap,
  2023).
* **13. The tower, end to end.** The Job climbs once more, from a NAND gate to the cluster, over ≈24,907,061 bytes of
  novels. Each layer is asked what it trusts and how the series earned it — physics on/off, gates by exhaustive check,
  the ISA by agreement with a reference, machine code by a hardened convention, languages by fuzzing and proof and
  DDC, the kernel by the MMU checking every access, storage by injected crashes, networks and replicas by injected
  faults, the application by inheriting everything below. Four leaks are drawn as arcs where a promise went unchecked:
  Rowhammer, Spectre, the trojan, the BGP hijack. The tower is lit end to end.
* **14. Frontier: the open problems of the series.** The questions the degree met and left open (P vs NP; whether
  one-way functions exist; ω, now < 2.372 (2024); BB(6), now that BB(5) = 47,176,870 was proved in 2024; splay-tree
  optimality; the unique games conjecture; BPP = P; circuit lower bounds; a C memory model; practical quantum
  advantage; verified software at scale — Part 61 returns to each). Three frontiers of trust: memory safety at scale,
  leak-free speculation at an affordable cost, and bootstrapping a whole toolchain from an auditable seed. Four open
  problems and the ★ research problem.
* **Outro.** The pebble again: Part 1's Euclid, 24 and 18 becoming 6 and 6; the ten acts as one tower; the ledger,
  row 20 — the Job as one line of Python on this machine, about 1.27 s, against Part 6's single-cycle Pebble at 281 s;
  the six problems; the final reading list; and on to Act XI, the research frontier.

## Build

```bash
python -m videos.cs.cs55.compute
python -m unittest tests.test_cs55_memory tests.test_cs55_trojan
python tools/build.py cs55
```

## Problems, with solutions

1. **ASLR entropy.** Compute the entropy of a 30-bit ASLR offset, and the expected number of attempts to the first
   hit, with and without re-randomisation.

   *Solution.* With k independent random bits the base takes one of 2ᵏ equally likely placements, so the entropy is
   H = k = 30 bits, and a fixed single-address exploit succeeds with probability p = 2⁻³⁰ ≈ 9.31×10⁻¹⁰. If the layout
   is re-randomised on every retry, each attempt is an independent Bernoulli trial, so the number of tries to the
   first hit is geometric with mean 1/p = 2³⁰ = 1,073,741,824. If instead the attacker sweeps the placements
   sequentially without re-randomisation, the hit is equally likely to be the 1st, 2nd, …, 2ᵏ-th candidate, so the
   expected number of tries is (2³⁰ + 1)/2 = 536,870,912.5. These are the 64-bit PIE row of the instrument's table;
   note re-randomisation roughly doubles the expected work, because a sequential sweep never repeats a guess. (The
   same arithmetic with k = 16 gives the ≈65,000-try 32-bit brute force of Shacham et al., 2004.)

2. **A one-byte write by ROP.** Find the gadgets for a return-oriented chain that writes one byte to the console on
   Pebble, using only code already in the binary.

   *Solution.* Pebble is a fixed-width ISA, so there are no unaligned "unintended" gadgets; scanning aligned
   instructions for a terminator (a `jalr` — which includes `ret` — or `halt`) and walking back over the straight-line
   tail before it yields eight gadgets. Two carry the write. `restore3` at offset 72 is
   `lw s0,0(sp); lw s1,4(sp); lw ra,8(sp); addi sp,sp,12; ret`: it loads s0, s1 and the next return address from the
   stack. `wb` at offset 92 is `sb s1,0(s0); lw ra,0(sp); addi sp,sp,4; ret`: it stores the byte in s1 to the address
   in s0, then pops the next return address. The overflow overwrites the saved return address with `restore3`, and
   above it places the stack words ⟨IO_CONSOLE = 0xFFFF0000, the byte, `wb`⟩ followed by ⟨`halt` at offset 24⟩.
   `restore3` loads s0 = the console port, s1 = the byte, ra = `wb`; `wb` writes the byte to the console and returns
   into `halt`. Only *code* addresses and data appear on the stack — no stack address — which is exactly why stack
   ASLR does not stop the attack, and why W^X does not either: no injected byte is ever executed. (The full
   five-letter "pwned" chain is this block repeated per letter, 20 stack words, from buffer base 1,048,208.)

3. **Lowe's attack.** Trace the man-in-the-middle on Needham–Schroeder, and show why naming B inside message 2 stops
   it.

   *Solution.* Write {m}ₓ for m sealed with X's public key, Nₐ and N_b for the two nonces. The intruder I is a
   network party Alice is willing to talk to. (1) Alice starts an honest session with I: {Nₐ, A}ᵢ. (2) I decrypts it
   and re-seals it for Bob, {Nₐ, A}_B; Bob believes Alice is calling. (3) Bob replies {Nₐ, N_b}ₐ. (4) I cannot read
   it (it is sealed for Alice), so it forwards it unchanged to Alice. (5) Alice, in her session with I, returns
   I's expected nonce: {N_b}ᵢ. (6) I decrypts N_b and re-seals {N_b}_B to Bob, who completes, believing he spoke to
   Alice. Now Bob is authenticated to a party who is really I, and I holds Bob's secret nonce N_b. Our breadth-first
   Dolev–Yao search reaches this in 19 states, with the intruder knowing N_b. Lowe's fix puts the responder's name
   in message 2: {Nₐ, N_b, B}ₐ. When I forwards Bob's reply to Alice in step 4, Alice sees it names B, but she
   believes she is talking to I, not B, so the identity check fails and she aborts; I cannot repair the message
   because it is sealed for Alice and I cannot decrypt it. The search then explores 17 states and finds no attack.

4. **Bound parameters cannot be injected.** Show, by an argument about the parser, that a query with bound parameters
   cannot be injected.

   *Solution.* Injection works by making user input change the *shape* of the parse tree — a quote closes a string,
   `OR '1'='1'` adds a disjunct, `--` comments out the rest. With bound parameters the query *template* is parsed
   exactly once, before any value arrives, into a fixed tree whose value positions are holes (our `prepare`). Binding
   (`bind`) copies that tree and replaces each hole, by position, with a finished literal node `("lit", value)`; the
   value is never handed to the tokeniser or the parser. Therefore the set of parse trees the engine can execute is a
   function of the template text alone and is independent of every user value: no byte of input can add, remove or
   reshape a node. Formally, for a fixed template T the executed query is T with its leaves substituted, and leaf
   substitution cannot change T's structure, so no input yields a tree outside {T with leaves bound}. Our engine makes
   this visible: binding the string `"id"` into the `WHERE id = ?` lookup returns 0 rows (it is compared as data),
   whereas pasting `id` in yields all 3 rows; the tautology and comment payloads, which derail the concatenated
   query's tokeniser, bind to a harmless 11- and 7-character username. (The parse error on the concatenated path is
   itself the symptom: the input reached the parser.)

5. **Build.** Trojan our compiler in a new way, and show that diverse double-compiling still detects it.

   *Solution notes.* Work against `explainer/cs/trust/trojan.py`. Write a fresh self-reproducing block the way the
   instrument's `_TROJAN` is written — a `%r`-template T′ whose single hole takes its own text, so that B′ = T′ % T′
   is the spliced code and, inside B′, the stored copy pasted into itself rebuilds B′ exactly (Part 25's quine). Give
   it a different payload than the shipped one: a different magic password in the `login` branch, and/or a different
   way of recognising a compiler's source and splicing B′ into it (for instance keying on the `def compile(src):`
   line and inserting B′ just after it, rather than on the `# TROJAN-SLOT` comment). Build the suspect binary A =
   `clean_compile(T′-trojaned source)` and check the three Thompson claims with `thompson_report`-style assertions:
   A's `login` accepts the new magic password, A compiling the *clean* compiler source reproduces A bit for bit (the
   fixpoint), and the magic string appears in no source file. Then run `ddc(A)`. Stage 1 compiles the clean source
   with A (which splices B′ in) and, independently, with the trusted compiler (which never inspects its input, so it
   splices nothing); stage 2 compiles the clean source again with each stage-1 binary. The suspect branch carries B′
   through both stages while the trusted branch stays honest, so the two stage-2 binaries differ and the verdict is
   *TROJAN DETECTED*. Running this confirms it: the new trojan is a genuine fixpoint (I measured a 1,166-byte binary
   reproducing itself, with the magic word in no source) and DDC flags it (stage-2 suspect 1,166 bytes against a
   499-byte honest stage-2), because the independent compiler does not share the trojan, whatever payload or trigger
   the trojan uses. The attack is only ever on our own toy compiler and `login`.

6. **★ Research.** A provably correct, reproducible software stack built up from an auditable seed of a few hundred
   bytes.

   *Discussion.* Open. The pieces exist in isolation but have never been composed into one end-to-end chain of
   evidence. Diverse double-compiling proves a binary corresponds to its source, but assumes the independent compiler
   is not trojaned the same way and says nothing about whether the source is honest (xz's backdoor was written by a
   maintainer). Reproducible builds let anyone rebuild a release and compare bytes, but full distributions are only
   partly reproducible. Bootstrapping projects (GNU Mes, Guix's full-source bootstrap of 2023) grow a toolchain from a
   seed small enough to read, but without a correctness proof for each step. And verified compilers (CompCert) and
   kernels (seL4, Part 54) are machine-checked, but at component scale, not composed from the seed up. A good partial
   answer would take a *minimal* stack — an auditable seed, a tiny assembler, a small C compiler, a small kernel —
   make every build reproducible, and give a single machine-checked proof that each stage preserves semantics, so that
   trusting the running system reduces to reading the few hundred bytes of the seed. Even one fully proved and
   reproducible rung above the seed, or a formal statement of the composed guarantee, would be new.

## 习题与解答

1. **ASLR 的熵。** 计算 30 位 ASLR 偏移的熵，以及首次命中所需的期望尝试次数，分别考虑重新随机化与不重新随机化两种情形。

   *解答。* 若地址中有 k 个独立的随机位，基址就落在 2ᵏ 个等可能的位置之一，所以熵为 H = k = 30 位，而一个写死单一地址的攻击
   以概率 p = 2⁻³⁰ ≈ 9.31×10⁻¹⁰ 命中。若每次重试都重新随机化布局，则每次尝试都是独立的伯努利试验，首次命中的尝试次数服从几何分布，
   均值为 1/p = 2³⁰ = 1,073,741,824。若攻击者不重新随机化、顺序地扫过所有位置，则命中等可能是第 1、2、…、2ᵏ 个候选，期望尝试次数
   为 (2³⁰ + 1)/2 = 536,870,912.5。这正是仪器表中的 64 位 PIE 那一行；注意重新随机化大致使期望工作量翻倍，因为顺序扫描从不重复一个
   猜测。（同样的算术在 k = 16 时给出 Shacham 等人 2004 年约 6.5 万次的 32 位暴力破解。）

2. **用 ROP 写一个字节。** 找出一条返回导向链所需的指令片段（gadget），它只用二进制里已有的代码，向 Pebble 的控制台写一个字节。

   *解答。* Pebble 是定长指令集，所以不存在非对齐的"意外"片段；在对齐的指令边界上扫描以终止指令（`jalr`——包括 `ret`——或 `halt`）
   结尾、再向前回溯其直线尾部，得到八个片段。其中两个承担写操作。偏移 72 处的 `restore3` 是
   `lw s0,0(sp); lw s1,4(sp); lw ra,8(sp); addi sp,sp,12; ret`：它从栈上装入 s0、s1 和下一个返回地址。偏移 92 处的 `wb` 是
   `sb s1,0(s0); lw ra,0(sp); addi sp,sp,4; ret`：它把 s1 里的字节存到 s0 所指的地址，再弹出下一个返回地址。溢出把保存的返回地址
   覆盖为 `restore3`，其上放置栈字 ⟨IO_CONSOLE = 0xFFFF0000、该字节、`wb`⟩，再接 ⟨偏移 24 处的 `halt`⟩。`restore3` 装入
   s0 = 控制台端口、s1 = 字节、ra = `wb`；`wb` 把字节写到控制台并返回进 `halt`。栈上只出现*代码*地址与数据，没有一个栈地址——这正是
   栈的 ASLR 挡不住这种攻击的原因，也是 W^X 挡不住它的原因：没有任何注入的字节被执行。（完整的五字母 "pwned" 链就是这个片段按字母
   重复，共 20 个栈字，缓冲区基址 1,048,208。）

3. **Lowe 的攻击。** 追踪 Needham–Schroeder 上的中间人攻击，并说明为什么在消息 2 中写入 B 的名字能阻止它。

   *解答。* 记 {m}ₓ 为用 X 的公钥封装的 m，Nₐ、N_b 为两个一次性随机数（nonce）。入侵者 I 是 Alice 愿意与之通信的一个网络方。
   （1）Alice 向 I 发起诚实会话：{Nₐ, A}ᵢ。（2）I 解密后为 Bob 重新封装 {Nₐ, A}_B；Bob 相信是 Alice 在呼叫。（3）Bob 回复
   {Nₐ, N_b}ₐ。（4）I 读不了它（它是封给 Alice 的），于是原样转发给 Alice。（5）Alice 在与 I 的会话里返回 I 期待的随机数：
   {N_b}ᵢ。（6）I 解出 N_b，再把 {N_b}_B 重新封给 Bob，Bob 完成会话，相信自己与 Alice 通了话。此时 Bob 把自己认证给了一个其实是
   I 的一方，而 I 掌握了 Bob 的秘密随机数 N_b。我们的广度优先 Dolev–Yao 搜索在 19 个状态里到达此处，入侵者确实知道了 N_b。Lowe 的
   修复是在消息 2 里写入响应者的名字：{Nₐ, N_b, B}ₐ。当 I 在第 4 步把 Bob 的回复转发给 Alice 时，Alice 看到它写着 B，但她以为自己
   在和 I 通话、而非 B，于是身份校验失败、她中止会话；I 无法改写这条消息，因为它是封给 Alice 的、I 解不开。搜索这时探索 17 个状态，
   找不到攻击。

4. **绑定参数不可被注入。** 用一个关于分析器（parser）的论证，证明使用绑定参数的查询不可被注入。

   *解答。* 注入靠的是让用户输入改变解析树的*形状*——一个引号闭合字符串，`OR '1'='1'` 加上一个析取项，`--` 注释掉其余部分。使用绑定
   参数时，查询*模板*恰好被解析一次，在任何值到来之前，解析成一棵固定的树，其取值位置是一个个"洞"（我们的 `prepare`）。绑定（`bind`）
   复制这棵树，按位置把每个洞替换成一个完成的字面量节点 `("lit", value)`；该值从不交给分词器或分析器。因此引擎能执行的解析树集合只是模板
   文本的函数，与每个用户值无关：没有一个输入字节能增加、删除或重塑任何节点。形式地说，对固定模板 T，被执行的查询就是把 T 的叶子替换后的
   结果，而叶替换不能改变 T 的结构，所以没有输入能产生 {把叶子绑定后的 T} 之外的树。我们的引擎让这一点可见：把字符串 `"id"` 绑定进
   `WHERE id = ?` 的查询返回 0 行（它作为数据被比较），而把 `id` 拼接进去则返回全部 3 行；在拼接路径上使分词器出轨的"永真式"与"注释"
   载荷，绑定后不过是长度 11 和 7 的无害用户名。（拼接路径上的解析错误本身就是症状：输入到达了分析器。）

5. **动手。** 用一种新的方式给我们的编译器植入木马，并说明多样化双重编译（DDC）仍能检测到它。

   *解答要点。* 在 `explainer/cs/trust/trojan.py` 上动手。像仪器里的 `_TROJAN` 那样写一个新的自复制代码块——一个 `%r` 模板 T′，
   其唯一的洞填入它自己的文本，于是 B′ = T′ % T′ 就是被拼入的代码，而在 B′ 内部，存着的那份副本填入自身又恰好重建出 B′（第 25 部分的
   奎因/quine 技巧）。给它一个与出厂版不同的载荷：在 `login` 分支里用不同的"魔法口令"，并且/或者用不同的方式识别编译器源码并把 B′ 拼进去
   （例如识别 `def compile(src):` 这一行、把 B′ 插在它之后，而不是识别 `# TROJAN-SLOT` 注释）。构造嫌疑二进制 A =
   `clean_compile(被 T′ 木马化的源码)`，并用类似 `thompson_report` 的断言检查 Thompson 的三条主张：A 的 `login` 接受新的魔法口令；
   A 编译*干净的*编译器源码时逐字节地复现出 A（不动点）；魔法字符串不出现在任何源文件里。然后运行 `ddc(A)`。阶段一用 A 编译干净源码
   （A 会把 B′ 拼进去），并独立地用可信编译器编译（它从不审视所编译的内容，所以什么也不拼）；阶段二再用各自的阶段一二进制编译干净源码。
   嫌疑分支在两个阶段里都带着 B′，而可信分支始终诚实，所以两个阶段二二进制不同，裁决为 *TROJAN DETECTED*。实际运行能证实这一点：新木马
   确是不动点（我测得一个 1,166 字节的二进制复现出自身，魔法字出现在任何源码里都没有），DDC 把它标了出来（阶段二嫌疑 1,166 字节对诚实
   阶段二的 499 字节），因为独立编译器不共享这个木马，无论木马用什么载荷或触发条件。这个攻击始终只针对我们自己的玩具编译器和 `login`。

6. **★ 研究。** 一个可证明正确、可重现的软件栈，从一颗几百字节、可审读的种子一路搭起来。

   *讨论。* 尚未解决。各个零件单独存在，却从未被组合成一条端到端的证据链。多样化双重编译证明一个二进制对应其源码，但它假设独立编译器没有被
   以同样方式植入木马，也完全不保证源码本身诚实（xz 的后门正是一位维护者写的）。可重现构建让任何人重建一个发行版并逐字节比对，但完整的
   发行版只是部分可重现。自举项目（GNU Mes、Guix 2023 年的全源自举）从小到能读的种子长出工具链，却没有对每一步的正确性证明。而经过机器
   校验的编译器（CompCert）与内核（seL4，第 54 部分）停在部件规模，没有从种子一路组合起来。好的部分答案会取一个*最小*的栈——可审读的
   种子、一个微型汇编器、一个小 C 编译器、一个小内核——让每一次构建可重现，并给出一条机器校验的证明，证明每一级都保持语义，使得信任运行中的
   系统归结为读那几百字节的种子。哪怕在种子之上做出一级完全证明且可重现的台阶，或给出组合保证的一个形式化陈述，都会是新的结果。

## Glossary additions

* **confidentiality, integrity, availability (the CIA triad)** — the three promises a secure system makes; a breach
  is any one of them broken.
* **threat model, trust boundary, trusted computing base (TCB), attack surface, adversary** — what you defend, the
  line trust crosses, the part that must be correct, every way in, and against whom.
* **economy of mechanism, fail-safe defaults, complete mediation, open design, separation of privilege, least
  privilege, least common mechanism, psychological acceptability** — Saltzer and Schroeder's principles (1975).
* **stack smash, stack canary, W^X (NX), ASLR** — overwriting a saved return address; a secret word that detects it;
  memory that is never both writable and executable; randomising addresses so a fixed guess usually misses.
* **return-oriented programming (ROP), gadget, control-flow integrity (CFI), shadow stack, CHERI** — reusing
  instruction tails already in the binary to compute without injecting code; the defences that guard control flow.
* **memory safety, ownership, affine type, move, borrow (shared, mutable), borrow checker, `unsafe`** — ruling out
  a whole class of bug in the type system; each value one owner; using a value at most once; the Rust discipline and
  its escape hatch.
* **Rowhammer, speculative execution, transient execution, side channel, Flush+Reload, constant-time code** —
  disturbing neighbouring DRAM rows; running ahead of a check and leaving a trace; information that leaks through
  time, power or cache; code whose time and memory do not depend on secrets.
* **password entropy, salt, slow (memory-hard) hash, HOTP, TOTP, passkey, WebAuthn** — bits of randomness in a
  password; a per-user prefix; a hash made deliberately expensive; one-time codes as an HMAC over a counter or the
  clock; a per-site signing key in place of a shared secret.
* **Needham–Schroeder, Dolev–Yao model, nonce, man-in-the-middle, model checking** — an authentication protocol; an
  intruder that owns the network; a fresh random challenge; a relay attack; the breadth-first search that finds it.
* **access matrix, ACL, capability, ambient authority, confused deputy, reference monitor** — Lampson's protection
  state and its two slicings; a request borrowing the rights of a privileged go-between; the component that checks
  every access.
* **Bell–LaPadula, no read up, no write down, security lattice, HRU safety** — a secrecy model and the flows it
  forbids; the undecidable question of whether a right can ever leak.
* **isolation, sandbox, seccomp, site isolation, enclave, controlled channel** — walls between programs and their
  costs; a system-call filter; a process per site; a region sealed even from the OS, and how the OS reads it anyway.
* **same-origin policy, XSS, CSRF, SQL injection, parameterised (bound) query, PKI, Certificate Transparency** — the
  web's trust boundary and the confusions of code and data across it; the parsing fix; a failing certificate anchor
  and the append-only log that exposes it.
* **source spoofing, amplification (reflection) attack, BGP hijack, RPKI, Kaminsky's attack, DNSSEC** — writing a
  false return address; a protocol whose answer dwarfs its question; believing a route or a DNS answer, and the
  signatures that stop it.
* **supply chain, dependency confusion, SLSA, SBOM, reproducible build** — the strangers whose code you run;
  resolving a public package over a private one; graded build evidence; a bill of materials; a build that gives the
  same bytes every time.
* **trusting trust, quine, fixpoint, diverse double-compiling (DDC), bootstrapping** — a backdoor that survives with
  no trace in any source; a program that prints its own text; a self-reproducing trojaned binary; Wheeler's
  cross-check with an independent compiler; growing a trusted toolchain from an auditable seed.

## Sources

* R. Anderson, *Security Engineering* (3rd ed., 2020); M. Bishop, *Computer Security: Art and Science* (2nd ed.,
  2018); J. Erickson, *Hacking: The Art of Exploitation* (2nd ed., 2008).
* J. Saltzer and M. Schroeder, "The protection of information in computer systems", Proc. IEEE 1975; B. Lampson,
  "Protection", ACM Operating Systems Review 1974; G. Harrison, W. Ruzzo and J. Ullman, "Protection in operating
  systems", CACM 1976; D. Bell and L. LaPadula, *Secure Computer Systems* (MITRE, 1973); N. Hardy, "The confused
  deputy", ACM Operating Systems Review 1988.
* L. Szekeres, M. Payer, T. Wei and D. Song, "SoK: eternal war in memory", IEEE S&P 2013; H. Shacham, "The geometry
  of innocent flesh on the bone: return-into-libc without function calls", CCS 2007; M. Abadi, M. Budiu, Ú. Erlingsson
  and J. Ligatti, "Control-flow integrity", CCS 2005; R. Jung, J.-H. Jourdan, R. Krebbers and D. Dreyer, "RustBelt:
  securing the foundations of the Rust programming language", POPL 2018.
* Y. Kim et al., "Flipping bits in memory without accessing them", ISCA 2014; P. Kocher et al., "Spectre attacks:
  exploiting speculative execution", IEEE S&P 2019; Y. Yarom and K. Falkner, "Flush+Reload", USENIX Security 2014.
* R. Needham and M. Schroeder, "Using encryption for authentication in large networks of computers", CACM 1978;
  G. Lowe, "Breaking and fixing the Needham–Schroeder public-key protocol", TACAS 1996; J. Bonneau, "The science of
  guessing", IEEE S&P 2012; RFC 4226 (HOTP, 2005) and RFC 6238 (TOTP, 2011).
* G. Klein et al., "seL4: formal verification of an OS kernel", SOSP 2009; Y. Xu, W. Cui and M. Peinado,
  "Controlled-channel attacks", IEEE S&P 2015.
* K. Thompson, "Reflections on trusting trust", CACM 1984; D. A. Wheeler, *Fully Countering Trusting Trust through
  Diverse Double-Compiling* (PhD thesis, 2009); the Reproducible Builds and Bootstrappable Builds projects.
* US-CERT alert TA14-017A, "UDP-based amplification attacks" (2014); RFC 2827 (BCP 38, 2000); RFC 6962 (Certificate
  Transparency, 2013); CVE-2024-3094 (xz-utils, 2024).
