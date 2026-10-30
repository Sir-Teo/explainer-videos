from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai15.common import fmt_int, ATT, HIST, HYB, MIX_C, MIX_SHORT, PART, axes, band, curve, heat_image, load

TF_C, HY_C = C.ATTN, HYB
TASK_NAME = {"needle": r"one needle", "multikey": r"one of four needles", "vartrack": r"a chain of three names"}


class LongContext(VoiceoverScene):
    def construct(self):
        self.card()
        self.needle()
        self.ruler_published()
        self.ruler_ours()
        self.past_window()
        self.today()

    def card(self):
        card = chapter_card(13, r"How long is a context, really?", r"Does a model use everything in its window?", part=PART)
        with self.voiceover("Chapter thirteen. How long is a context, really?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def needle(self):
        g = np.random.default_rng(3)
        img_good = heat_image(np.ones((10, 10)), 3.6, 3.0, color=C.INTERVAL, gamma=1.0).move_to([-3.4, -0.6, 0])
        bad = np.ones((10, 10))
        for i in range(10):
            for j in range(10):
                if j > 5 and 2 <= i <= 7:
                    bad[i, j] = 0.35 + 0.4 * g.random()
        img_bad = heat_image(bad, 3.6, 3.0, color=C.INTERVAL, gamma=1.0).move_to([2.6, -0.6, 0])
        yl = label(r"depth of the needle \\ (top: \ the start)", font_size=18, color=GREY_B).next_to(img_good, LEFT, buff=0.2)
        xl = label(r"length of the haystack $\rightarrow$", font_size=18, color=GREY_B).next_to(img_good, DOWN, buff=0.15)
        xl2 = xl.copy().next_to(img_bad, DOWN, buff=0.15)
        t1 = label(r"passes everywhere", font_size=20, color=C.INTERVAL).next_to(img_good, UP, buff=0.15)
        t2 = label(r"loses the middle of long texts", font_size=20, color=C.INTERVAL).next_to(img_bad, UP, buff=0.15)
        hay = label(r"``\dots \ The best thing to do in San Francisco is eat a sandwich and sit in Dolores Park on a "
                    r"sunny day. \ \dots''", font_size=20, color=GREY_A).to_edge(UP, buff=0.4)
        tag = note(r"illustrative", font_size=16).to_corner(DR, buff=0.3)
        cite_ = cite(r"G.~Kamradt, \textit{Needle in a Haystack} (2023); \ N.~F.~Liu et al., \textit{Lost in the Middle} (2023)",
                     corner=DL, font_size=17)
        with self.voiceover(
            "How do you test a long context? In November 2023 Greg Kamradt hid one sentence, the needle, at a chosen "
            "depth in a long stack of essays, and asked the model about it. <bookmark mark='a'/> Vary the depth and "
            "the length, colour each cell by whether it answered, and you get the needle-in-a-haystack picture that "
            "every long-context model now shows. <bookmark mark='b'/> A weak one goes dark in the middle of long "
            "texts: the lost-in-the-middle effect of Nelson Liu and colleagues, which Part 29 returns to. "
            "<bookmark mark='c'/> But the needle is an easy test: its question repeats its words, so a single "
            "attention head that matches words can find it."
        ) as vo:
            self.play(FadeIn(hay), FadeIn(cite_), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(img_good), FadeIn(yl), FadeIn(xl), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(img_bad), FadeIn(xl2), FadeIn(t2))
            vo.wait_until("c")
            self.play(Indicate(hay, color=C.BITS, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ruler_published(self):
        head = label(r"Harder than a needle", font_size=36).to_edge(UP, buff=0.35)
        w, fs = 4.2, 19
        cards = VGroup(
            history_card(2024, r"RULER \ (Hsieh et al., NVIDIA)", r"13 tasks: \ many needles, \ tracing variables, \ "
                         r"counting words, \ questions; \ of 17 models claiming at least $32$k tokens, \ only half held "
                         r"up at $32$k", color=HIST, width=w, font_size=fs),
            history_card(2025, r"NoLiMa \ (Modarressi et al.)", r"needles that share no words with the question; \ "
                         r"at $32$k tokens, \ 11 of 13 models fell below half their short-text score; \ GPT-4o: \ "
                         r"$99.3\% \to 69.7\%$", color=HIST, width=w, font_size=fs),
            history_card(2025, r"Context rot \ (Hong, Troynikov \& Huber, Chroma)", r"18 models: \ every one less reliable "
                         r"as the input grows, \ even on simple tasks", color=HIST, width=w, font_size=fs),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP)
        if cards.width > 13.4:
            cards.width = 13.4
        cards.next_to(head, DOWN, buff=0.4)
        tw = label(r"the length a model accepts \ $\ne$ \ the length it can use", font_size=30, color=C.BITS)
        tw.next_to(cards, DOWN, buff=0.6)
        with self.voiceover(
            "So the tests got harder. <bookmark mark='a'/> In 2024 Cheng-Ping Hsieh and colleagues at NVIDIA built "
            "RULER: many needles at once, values passed along chains of variables, counting the commonest words, and "
            "questions about the text. Of seventeen models that claimed at least thirty-two thousand tokens, only "
            "half still did well at thirty-two thousand. <bookmark mark='b'/> In 2025 NoLiMa took away the literal "
            "match: the needle and the question share no words. At thirty-two thousand tokens, eleven of thirteen "
            "models fell below half their short-text score. <bookmark mark='c'/> And Chroma's report on context rot "
            "found all eighteen models it tried growing less reliable as the input grew, even on simple tasks. "
            "<bookmark mark='d'/> The length a model accepts is not the length it can use."
        ) as vo:
            self.play(FadeIn(head))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(cards[k], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(tw))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ruler_ours(self):
        r = load("ruler")
        mix = list(r["mixers"])
        tasks = list(r["tasks"])
        Ls = [int(x) for x in r["lengths"]]
        T0 = int(r["T"])
        tables = Group()
        for k in mix:
            A = np.asarray(r[f"acc_{k}"]).mean(0)  # tasks x lengths
            img = heat_image(A, 0.62 * len(Ls), 0.62 * len(tasks), color=MIX_C[k], gamma=1.0)
            vals = VGroup()
            for i in range(len(tasks)):
                for j in range(len(Ls)):
                    c = img.get_corner(UL) + np.array([0.62 * (j + 0.5), -0.62 * (i + 0.5), 0])
                    vals.add(MathTex(f"{100 * A[i, j]:.0f}", font_size=17, color=BLACK if A[i, j] > 0.55 else WHITE).move_to(c))
            t = label(MIX_SHORT[k], font_size=22, color=MIX_C[k]).next_to(img, UP, buff=0.12)
            tables.add(Group(img, SurroundingRectangle(img, buff=0, color=GREY_D, stroke_width=1), vals, t))
        tables.arrange_in_grid(rows=2, cols=2, buff=(1.6, 0.7)).move_to([0.8, -0.35, 0])
        rl = VGroup(*[label(TASK_NAME[t], font_size=17, color=GREY_A) for t in tasks]).arrange(DOWN, aligned_edge=RIGHT, buff=0.38)
        rl.next_to(tables[0][0], LEFT, buff=0.2).align_to(tables[0][0], UP).shift(DOWN * 0.18)
        rl2 = rl.copy().next_to(tables[2][0], LEFT, buff=0.2).align_to(tables[2][0], UP).shift(DOWN * 0.18)
        cl = VGroup(*[MathTex(str(L), font_size=17, color=GREY_B).move_to(tables[2][0].get_corner(DL) + np.array([0.62 * (j + 0.5), -0.22, 0]))
                      for j, L in enumerate(Ls)])
        cl2 = VGroup(*[MathTex(str(L), font_size=17, color=GREY_B).move_to(tables[3][0].get_corner(DL) + np.array([0.62 * (j + 0.5), -0.22, 0]))
                       for j, L in enumerate(Ls)])
        head = label(rf"our RULER: \ trained at ${T0}$ tokens, \ tested up to ${fmt_int(Ls[-1])}$ \ (\% right, \ chance $3\%$)",
                     font_size=24).to_edge(UP, buff=0.3)
        foot = note(rf"two-layer models as in chapter 11, \ keys of $16$; \ {len(r['seeds'])} seeds each, \ averaged; \ "
                    r"filler of random words around the needles; \ columns: \ tokens", font_size=16).to_edge(DOWN, buff=0.2)
        acc = {k: np.asarray(r[f"acc_{k}"]).mean(0) for k in mix}
        nm = {k: MIX_SHORT[k].replace("$", "") for k in mix}
        at_train = {k: float(acc[k][:, 0].mean()) for k in mix}
        far = {k: float(acc[k][:, -1].mean()) for k in mix}
        best_far = max(mix, key=lambda k: far[k])
        worst_drop = max(mix, key=lambda k: at_train[k] - far[k])
        vt = acc
        hard = tasks.index("vartrack")
        a_ = {k: 100 * at_train[k] for k in mix}
        v1 = (f"At the length they trained on, averaged over the three tasks, softmax attention gets {a_['softmax']:.0f} "
              f"percent, the Mamba-2-style model {a_['mamba2']:.0f}, the gated delta rule {a_['gdn']:.0f} and the hybrid "
              f"{a_['hybrid']:.0f}. ")
        v2 = (f"At eight times that length, {nm[best_far]} holds up best, {100 * far[best_far]:.0f} percent; "
              f"{nm[worst_drop]} falls furthest, from {100 * at_train[worst_drop]:.0f} to {100 * far[worst_drop]:.0f}. ")
        hardest = min(range(len(tasks)), key=lambda i: np.mean([acc[k][i, 0] for k in mix]))
        v3 = (f"The hardest task, even at the training length, is {TASK_NAME[tasks[hardest]].replace('$', '')}.")
        with self.voiceover(
            "We can run a small RULER of our own. Four of the last chapter's two-layer models, trained on three tasks "
            f"at {T0} tokens: find one needle in a stream of filler words; find the one of four needles that's asked "
            "for; and follow a chain, A is seven, B equals A, C equals B, what is C? <bookmark mark='a'/> Then we test "
            f"them on longer streams, up to {Ls[-1]:,} tokens. <bookmark mark='b'/> " + v1 + "<bookmark mark='c'/> "
            + v2 + "<bookmark mark='d'/> " + v3
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(rl), FadeIn(rl2), FadeIn(cl), FadeIn(cl2), *[FadeIn(t_[0]) for t_ in tables],
                      *[FadeIn(t_[1]) for t_ in tables], *[FadeIn(t_[3]) for t_ in tables])
            vo.wait_until("b")
            self.play(*[FadeIn(t_[2]) for t_ in tables])
            vo.wait_until("c")
            self.play(Indicate(tables[mix.index(best_far)][3], color=WHITE, scale_factor=1.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def past_window(self):
        r = load("lm")
        bt, bh = np.asarray(r["transformer_by_pos"]), np.asarray(r["hybrid_by_pos"])
        L = bt.shape[1]

        def sm(x, k=32):
            return np.convolve(x, np.ones(k) / k, mode="valid")

        mt, mh = sm(bt.mean(0)), sm(bh.mean(0))
        xs = np.arange(len(mt)) + 16
        lo = math.floor(min(mt.min(), mh.min()) * 2) / 2
        hi = min(math.ceil(max(mt.max(), mh.max()) * 2) / 2, lo + 4)
        g1 = axes([0, L], [lo, hi], x_length=5.6, y_length=3.3, xlabel=r"position, \ read in one go",
                  ylabel=r"loss \ (nats a token)", xticks=[0, 256, 512, 1024], yticks=[lo, hi], center=[-3.5, -0.4, 0])
        ax = g1.ax
        c1 = VGroup(curve(ax, xs, np.clip(mt, lo, hi), TF_C, 3), curve(ax, xs, np.clip(mh, lo, hi), HY_C, 3))
        tr = DashedLine(ax.c2p(256, lo), ax.c2p(256, hi), dash_length=0.06, color=GREY_B, stroke_width=1.5)
        trl = label(r"trained on $256$", font_size=16, color=GREY_B).next_to(tr, UP, buff=0.05)
        gaps = [int(x) for x in r["gaps"]]
        ct, chy = np.asarray(r["transformer_copy"]), np.asarray(r["hybrid_copy"])
        lg = np.log2(gaps)
        g2 = axes([lg[0] - 0.2, lg[-1] + 0.2], [0, 1.0], x_length=5.0, y_length=3.3,
                  xlabel=r"tokens between the two copies", ylabel=r"copied tokens right", xticks=list(lg), yticks=[0, 0.5, 1],
                  xfmt=lambda v: f"{int(round(2 ** v))}", yfmt=lambda v: rf"{int(100 * v)}\%", center=[3.4, -0.4, 0], font_size=17)
        ax2 = g2.ax
        b2 = VGroup(band(ax2, lg, ct.min(0), ct.max(0), TF_C, 0.25), band(ax2, lg, chy.min(0), chy.max(0), HY_C, 0.25))
        c2 = VGroup(curve(ax2, lg, ct.mean(0), TF_C, 3), curve(ax2, lg, chy.mean(0), HY_C, 3))
        w2 = DashedLine(ax2.c2p(math.log2(256 - 48), 0), ax2.c2p(math.log2(256 - 48), 1), dash_length=0.06, color=GREY_B,
                        stroke_width=1.5)
        leg = legend([(TF_C, r"transformer, \ rotary positions"), (HY_C, r"hybrid, \ attention without positions")],
                     font_size=18).to_edge(UP, buff=0.35)
        task = note(r"the copy test: \ $24$ random tokens, \ a stretch of a novel, \ the same $24$ again; \ $3$ seeds, \ "
                    r"band: \ min to max", font_size=16).to_edge(DOWN, buff=0.2)
        far_t, far_h = float(mt[-200:].mean()), float(mh[-200:].mean())
        near_t, near_h = float(mt[100:240].mean()), float(mh[100:240].mean())
        v1 = (f"Past 256, the transformer's loss climbs, from {near_t:.1f} to {far_t:.1f} nats: rotary positions it "
              "never trained on. " if far_t > near_t + 0.3 else
              f"Past 256, the transformer's loss barely moves, {near_t:.1f} to {far_t:.1f}. ")
        v2 = (f"The hybrid's stays near where it was, {near_h:.1f} to {far_h:.1f}: its attention has no positions to "
              "run out of. " if far_h < near_h + 0.3 else
              f"The hybrid's climbs too, {near_h:.1f} to {far_h:.1f}. ")
        gi = gaps.index(max(g_ for g_ in gaps if g_ + 48 > 256)) if any(g_ + 48 > 256 for g_ in gaps) else len(gaps) - 1
        lt, lh = float(ct.mean(0)[-1]), float(chy.mean(0)[-1])
        nt, nh = float(ct.mean(0)[0]), float(chy.mean(0)[0])
        v3 = (f"In the copy test, both copy well when the copies are close: {100 * nt:.0f} and {100 * nh:.0f} percent "
              f"of the tokens. With {gaps[-1]} tokens between them, the transformer gets {100 * lt:.0f} percent and the "
              f"hybrid {100 * lh:.0f}.")
        with self.voiceover(
            "Our two language models from the last chapter were trained on windows of 256 tokens. What happens "
            "past the end? <bookmark mark='a'/> Here is the loss at each position of held-out text a thousand tokens "
            "long, read in one go. " + v1 + "<bookmark mark='b'/> " + v2 + "<bookmark mark='c'/> And a needle the "
            "models can only find by memory: twenty-four random tokens, then a stretch of a novel, then the same "
            "twenty-four again. How many of the repeated tokens does each predict? " + v3
        ) as vo:
            self.play(FadeIn(leg), FadeIn(g1), Create(tr), FadeIn(trl))
            vo.wait_until("a")
            self.play(Create(c1[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(c1[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(g2), FadeIn(task), Create(w2))
            self.play(FadeIn(b2), Create(c2[0]), Create(c2[1]), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def today(self):
        head = label(r"Long contexts in 2026", font_size=36).to_edge(UP, buff=0.35)
        rows = [
            (r"Gemini 1.5 \ (Google, 2024)", r"a million tokens; \ needles found in up to $10$ million, \ in research", HIST),
            (r"Kimi Linear \ (Moonshot, 2025)", r"RULER at $128$k: \ $84.3$, \ against $81.3$ for full attention \ "
             r"($1.4$T tokens each); \ $78.8$ with rotary positions", HYB),
            (r"MRCR v2, \ eight needles \ (OpenAI's test)", r"at $1$M tokens: \ Claude Opus 4.6 $76\%$, \ Claude Sonnet 4.5 "
             r"$18.5\%$ \ (Anthropic, \ February 2026)", C.BITS),
            (r"DeepSeek-V4 \ (2026)", r"$1$M tokens; \ keys and values compressed $4\times$ and $128\times$ \ "
             r"(compressed sparse attention: \ Part 16)", ATT),
        ]
        tbl = VGroup()
        for i, (a, b, c_) in enumerate(rows):
            tbl.add(VGroup(label(a, font_size=21, color=c_), label(b, font_size=19, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.08))
        tbl.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.4)
        if tbl.width > 13.2:
            tbl.width = 13.2
        src = note(r"each figure from its maker's report", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Where does that leave the frontier? <bookmark mark='a'/> Google's Gemini 1.5, in 2024, first offered a "
            "million tokens, and reported finding needles in up to ten million. <bookmark mark='b'/> Kimi Linear's "
            "report gives the strongest evidence for hybrids on long texts: on RULER at 128 thousand tokens, 84.3 "
            "against 81.3 for full attention trained the same way, and only 78.8 when its attention layers use "
            "rotary positions. <bookmark mark='c'/> On OpenAI's harder MRCR test, eight similar requests hidden in "
            "a million tokens, Anthropic reported in February 2026 that Claude Opus 4.6 found 76 percent, where "
            "its predecessor Sonnet 4.5 found 18.5. <bookmark mark='d'/> And DeepSeek-V4 reads a million tokens by "
            "compressing its keys and values, four and a hundred and twenty-eight to one, and choosing among them: "
            "Part 16's subject. These are each maker's own measurements."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(tbl[k], shift=RIGHT * 0.1))
        self.wait(0.3)
        self.clear_scene()
