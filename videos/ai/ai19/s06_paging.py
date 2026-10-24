from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai19.common import (CONTIGC, F, KVC, PAGEDC, PART, PREFILLC, RESERVEC, hbars, load, take_away, x_)

PALETTE = [C.TRUE_P, C.KEY, C.BITS, C.MLP, C.HOT, C.EMBED, C.PROB, C.ENTROPY, C.MODEL_Q, C.LATENT]


def memory_map(snap, pool, block=16, cols=64, cell=0.15, center=(0, 1.4)):
    """The cache's memory as a grid of cells of ``block`` tokens: each request its colour, bright where its tokens
    are, dim where it holds memory it hasn't filled, dark where memory is free."""
    n = pool // block
    rows = n // cols
    owner = np.full(n, -1)
    fill = np.zeros(n)
    for st, alloc, used, rid in np.asarray(snap).reshape(-1, 4):
        a, b = int(st) // block, int(st + alloc) // block
        for k in range(a, b):
            owner[k] = int(rid)
            fill[k] = np.clip((used - (k - a) * block) / block, 0, 1)
    g = VGroup()
    for k in range(n):
        r, c = divmod(k, cols)
        if owner[k] < 0:
            col, op = GREY_D, 0.12
        else:
            col = PALETTE[owner[k] % len(PALETTE)]
            op = 0.9 if fill[k] > 0 else 0.22
        g.add(Square(cell * 0.86, stroke_width=0, fill_color=col, fill_opacity=op)
              .move_to([center[0] + (c - cols / 2 + 0.5) * cell, center[1] - (r - rows / 2 + 0.5) * cell, 0]))
    return g


class Paging(VoiceoverScene):
    def construct(self):
        self.card()
        self.maps()
        self.blocks()
        self.prefix()

    def card(self):
        card = chapter_card(5, r"Pages and shared prefixes", r"How should the cache's memory be handed out?",
                            part=PART)
        with self.voiceover("Chapter five. Pages and shared prefixes."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def maps(self):
        p = load("paging")
        pool, mx = int(p["pool"]), int(p["max_len"])
        modes = [("reserve", r"reserved at the maximum, \ $2{,}048$ tokens", RESERVEC),
                 ("contiguous", r"exactly its length, \ in one piece", CONTIGC),
                 ("paged", r"pages of $16$ tokens, \ anywhere", PAGEDC)]
        maps = [memory_map(p[f"snap_{m}"], pool) for m, _, _ in modes]
        head = label(rf"the cache's memory: \ ${pool:,}$ tokens, \ one square $= 16$ \ (a moment of the simulation)"
                     .replace(",", "{,}"), font_size=22, color=GREY_A).to_edge(UP, buff=0.3)
        sub = [label(t, font_size=24, color=c_).next_to(maps[0], DOWN, buff=0.2) for _, t, c_ in modes]
        used = [100 * p[m]["used"] for m, _, _ in modes]
        run = [p[m]["running"] for m, _, _ in modes]
        b1 = hbars(used, [r"reserved", r"one piece", r"pages"], [c_ for _, _, c_ in modes], width=3.0, row_h=0.45,
                   font_size=20, lo=0, hi=100, fmt_v=lambda v: rf"{v:.0f}\%")
        b1.move_to([-2.6, -2.3, 0])
        t1 = label(r"memory holding tokens", font_size=20, color=GREY_A).next_to(b1, UP, buff=0.15)
        b2 = hbars(run, [r"reserved", r"one piece", r"pages"], [c_ for _, _, c_ in modes], width=3.0, row_h=0.45,
                   font_size=20, lo=0, hi=max(run) * 1.1, fmt_v=lambda v: rf"{v:.1f}")
        b2.move_to([3.6, -2.3, 0])
        t2 = label(r"conversations at once \ (average)", font_size=20, color=GREY_A).next_to(b2, UP, buff=0.15)
        hc = history_card(2023, r"Woosuk Kwon et al., \ vLLM", rf"PagedAttention: \ other systems used only "
                          rf"${F.VLLM['used'][0]}$--${F.VLLM['used'][1]}\%$ of the cache's memory for tokens; \ "
                          rf"${F.VLLM['gain'][0]}$--${F.VLLM['gain'][1]}\times$ the throughput", width=5.0,
                          font_size=17, color=PAGEDC).to_corner(DR, buff=0.25)
        tg = p["paged"]["throughput"] / p["reserve"]["throughput"]
        cg = p["paged"]["running"] / p["reserve"]["running"]
        if tg > 1.5:
            tsay = f"and it writes {x_(tg)} times as many tokens a second."
        else:
            tsay = (f"Here that buys only {100 * (tg - 1):.0f} percent more tokens a second, because on this "
                    "computer each conversation's own cache costs nearly as much to read as it adds; on a GPU, "
                    "where reading the weights dominates, vLLM measured two to four times.")
        with self.voiceover(
            "Where in memory should each conversation's cache go? Nobody knows how long an answer will be. "
            "<bookmark mark='a'/> So servers used to reserve, for every conversation, room for the longest answer "
            f"allowed, here {mx:,} tokens. Most of it sits empty: in our simulated server, on average only "
            f"{used[0]:.0f} percent of the memory holds a token, and it fits {run[0]:.1f} conversations at a "
            "time. In 2023 the vLLM team measured real systems keeping 20 to 38 percent. "
            "<bookmark mark='b'/> Reserving exactly the right length would need the future, and still splinters "
            f"the memory as conversations come and go: {used[1]:.0f} percent. <bookmark mark='c'/> vLLM's answer "
            "came from operating systems: virtual memory. Cut the cache into pages of sixteen tokens, put each "
            "page anywhere, and keep a table of where they are. A conversation takes a page when it needs one. "
            f"<bookmark mark='d'/> Now {used[2]:.0f} percent of the memory holds tokens, and {run[2]:.1f} "
            f"conversations fit at once, {x_(cg)} times as many; " + tsay
        ) as vo:
            self.play(FadeIn(head), FadeIn(maps[0], lag_ratio=0.002), FadeIn(sub[0]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(t2), FadeIn(b1[0]), FadeIn(b2[0]))
            vo.wait_until("b")
            self.play(ReplacementTransform(maps[0], maps[1]), ReplacementTransform(sub[0], sub[1]), run_time=1.2)
            self.play(FadeIn(b1[1]), FadeIn(b2[1]))
            vo.wait_until("c")
            self.play(ReplacementTransform(maps[1], maps[2]), ReplacementTransform(sub[1], sub[2]), run_time=1.2)
            self.play(FadeIn(hc))
            vo.wait_until("d")
            self.play(FadeIn(b1[2]), FadeIn(b2[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def blocks(self):
        p = load("paging")
        bl = np.asarray(p["blocks"], float)
        w = 100 * np.asarray(p["block_waste"])
        g = axes([0, 8.6], [0, max(w) * 1.15], x_length=7.0, y_length=3.8, xlabel=r"page size \ (tokens)",
                 ylabel=r"memory in pages left empty \ (\%)", xticks=list(range(0, 9)), yticks=[0, 10, 20],
                 xfmt=lambda v: f"{2 ** int(v)}", center=[-1.4, -0.2, 0])
        ax = g.ax
        xs = np.log2(bl)
        dots = VGroup(*[Dot(ax.c2p(x, y), radius=0.07, color=PAGEDC) for x, y in zip(xs, w)])
        line = curve(ax, xs, w, PAGEDC, 3)
        k16 = list(bl).index(16)
        mark = DashedLine(ax.c2p(4, 0), ax.c2p(4, w[k16]), color=GREY_B, dash_length=0.06)
        ml = label(rf"vLLM: \ $16$ tokens, \ ${w[k16]:.1f}\%$ empty", font_size=20, color=PAGEDC)
        ml.next_to(ax.c2p(4, w[k16]), UL, buff=0.15)
        f_ = MathTex(r"\text{waste} \approx \frac{b/2}{\bar L}", font_size=36, color=PAGEDC).move_to([4.7, 1.0, 0])
        fl = label(r"half a page per conversation, \\ $\bar L$ its length", font_size=20, color=GREY_A)
        fl.next_to(f_, DOWN, buff=0.2)
        L = float(np.mean(p["lengths"]))
        with self.voiceover(
            "How big should a page be? <bookmark mark='a'/> On average a conversation leaves half its last page "
            f"empty, so the waste is about half a page over the length of a conversation, here {L:.0f} tokens. "
            "<bookmark mark='b'/> Small pages waste little, but make a longer table to look up in every attention "
            f"step. vLLM chose sixteen tokens: for our conversations, {w[k16]:.1f} percent of the memory wasted. "
            f"Pages of 256 would waste {w[-1]:.0f}."
        ) as vo:
            self.play(FadeIn(g), Write(f_), FadeIn(fl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d_, scale=0.5) for d_ in dots], lag_ratio=0.1), Create(line), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(mark), FadeIn(ml))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def prefix(self):
        p = load("paging")
        caps = p["prefix_caps"]
        saved = [100 * x["saved"] for x in p["prefix"]]
        sysn = int(p["prefix_system"])
        # three conversations sharing a system prompt, turn after turn (schematic)
        sp = Rectangle(width=2.2, height=0.42, stroke_width=0, fill_color=GREY_B, fill_opacity=0.6)
        spl = label(rf"system prompt", font_size=18, color=WHITE).move_to(sp)
        convs = VGroup()
        for k, col in enumerate((C.TRUE_P, C.KEY, C.HOT)):
            row = VGroup()
            for j in range(3):
                row.add(Rectangle(width=0.55, height=0.32, stroke_width=0, fill_color=col,
                                  fill_opacity=0.9 if j % 2 == 0 else 0.45))
            row.arrange(RIGHT, buff=0.04)
            convs.add(row)
        convs.arrange(DOWN, buff=0.25)
        tree = VGroup(VGroup(sp, spl), convs).arrange(RIGHT, buff=0.6).move_to([-3.6, 1.0, 0])
        links = VGroup(*[Line(sp.get_right(), r_.get_left(), color=GREY_C, stroke_width=1.5) for r_ in convs])
        tl = label(r"cached once, \ shared by every conversation", font_size=20, color=GREY_A).next_to(tree, UP, buff=0.3)
        tag = schematic_tag(corner=UL)
        b = hbars(saved[1:], [rf"${c // 1024}$k tokens" if c < 10 ** 8 else r"unlimited" for c in caps[1:]],
                  [KVC] * (len(caps) - 1), width=3.6, row_h=0.42, font_size=20, lo=0, hi=100,
                  fmt_v=lambda v: rf"{v:.0f}\%")
        b.move_to([3.6, 0.6, 0])
        btl = label(r"prompt tokens not recomputed, \\ by the memory kept for prefixes", font_size=20,
                    color=GREY_A).next_to(b, UP, buff=0.25)
        tf, ts = float(p["prefix_full_t"]) * 1e3, float(p["prefix_suffix_t"]) * 1e3
        meas = VGroup(label(rf"our model, \ a $256$-token prompt: \ ${tf:.0f}$ ms", font_size=21, color=PREFILLC),
                      label(rf"its first $224$ tokens cached: \ ${ts:.0f}$ ms", font_size=21, color=KVC))
        meas.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-3.4, -1.5, 0])
        hc = history_card(2023, r"Lianmin Zheng et al., \ SGLang", rf"RadixAttention: \ cached prefixes in a tree; \ "
                          rf"up to ${F.SGLANG['gain']}\times$ the throughput", width=4.4, font_size=17,
                          color=KVC).move_to([3.6, -2.3, 0])
        with self.voiceover(
            "Pages make one more thing possible: sharing. <bookmark mark='a'/> Most requests start with the same "
            "words: a system prompt, the instructions, the conversation so far. Their keys and values are the "
            "same every time, so compute them once, keep the pages, and point every request that starts that way "
            "at them. <bookmark mark='b'/> We simulated forty conversations of six turns, all opening with a "
            f"{sysn}-token system prompt. With room for a thousand tokens of prefixes, {saved[1]:.0f} percent of "
            f"the prompt tokens needn't be computed again; with room for everything, {saved[-1]:.0f} percent, "
            "because every turn repeats the conversation before it. <bookmark mark='c'/> On our model, a "
            f"256-token prompt takes {tf:.0f} milliseconds to prefill; with its first 224 tokens already cached, "
            f"{ts:.0f}: {x_(tf / ts)} times faster. SGLang kept these prefixes in a tree in 2023, and since 2024 "
            f"DeepSeek has charged up to {F.DEEPSEEK_CACHE['cut']} percent less for input it finds in its cache."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(tree[0]), FadeIn(tl))
            vo.wait_until("a")
            self.play(Create(links), LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in convs], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(btl), LaggedStart(*[AnimationGroup(FadeIn(r_.name), GrowFromEdge(r_.bar, LEFT),
                                                                FadeIn(r_.val)) for r_ in b], lag_ratio=0.25))
            vo.wait_until("c")
            self.play(FadeIn(meas), FadeIn(hc))
        self.wait(0.3)
        self.clear_scene()
