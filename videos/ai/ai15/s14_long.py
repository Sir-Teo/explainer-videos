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
        img_good = heat_image(np.ones((10, 10)), 4.4, 3.6, color=C.INTERVAL, gamma=1.0).move_to([-2.4, -0.6, 0])
        bad = np.ones((10, 10))
        for i in range(10):
            for j in range(10):
                if j > 5 and 2 <= i <= 7:
                    bad[i, j] = 0.35 + 0.4 * g.random()
        img_bad = heat_image(bad, 4.4, 3.6, color=C.INTERVAL, gamma=1.0).move_to([3.3, -0.6, 0])
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
            self.play(FadeIn(hay), FadeIn(cite_), FadeIn(tag), FadeIn(img_good), FadeIn(yl), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(t1), Indicate(img_good, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(img_bad), FadeIn(xl2), FadeIn(t2))
            vo.wait_until("c")
            self.play(Indicate(hay, color=C.BITS, scale_factor=1.02))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ruler_published(self):
        head = label(r"Harder than a needle", font_size=36).to_edge(UP, buff=0.35)
        w, fs = 4.3, 26
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
        cards.next_to(head, DOWN, buff=0.7)
        tw = label(r"the length a model accepts \ $\ne$ \ the length it can use", font_size=34, color=C.BITS)
        tw.next_to(cards, DOWN, buff=0.7)
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
            veils = VGroup(*[Rectangle(width=c_.width + 0.08, height=c_.height + 0.08, stroke_width=0,
                                       fill_color=BACKGROUND, fill_opacity=0.82).move_to(c_) for c_ in cards])
            self.play(FadeIn(head), FadeIn(cards), FadeIn(veils))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeOut(veils[k]))
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
            self.play(FadeIn(head), FadeIn(foot), FadeIn(rl), FadeIn(rl2), FadeIn(cl), FadeIn(cl2),
                      *[FadeIn(t_[0]) for t_ in tables], *[FadeIn(t_[1]) for t_ in tables], *[FadeIn(t_[3]) for t_ in tables])
            vo.wait_until("a")
            self.play(Indicate(VGroup(cl, cl2), color=WHITE, scale_factor=1.1))
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
        lt_, ht_ = np.array([sm(x) for x in bt]), np.array([sm(x) for x in bh])
        xs = np.arange(len(mt)) + 16
        lo = math.floor(min(mt.min(), mh.min()) * 2) / 2
        hi = min(math.ceil(max(mt.max(), mh.max()) * 2) / 2, lo + 4)
        g1 = axes([0, L], [lo, hi], x_length=7.8, y_length=4.2, xlabel=r"position, \ read in one go",
                  ylabel=r"loss on the next token \ (nats, \ average of $12$ held-out windows, \ $3$ seeds)",
                  xticks=[0, 256, 512, 768, 1024], yticks=[lo, (lo + hi) / 2, hi], center=[-2.2, -0.4, 0])
        ax = g1.ax
        b1 = VGroup(band(ax, xs, np.clip(lt_.min(0), lo, hi), np.clip(lt_.max(0), lo, hi), TF_C, 0.2),
                    band(ax, xs, np.clip(ht_.min(0), lo, hi), np.clip(ht_.max(0), lo, hi), HY_C, 0.2))
        c1 = VGroup(curve(ax, xs, np.clip(mt, lo, hi), TF_C, 3), curve(ax, xs, np.clip(mh, lo, hi), HY_C, 3))
        tr = DashedLine(ax.c2p(256, lo), ax.c2p(256, hi), dash_length=0.06, color=GREY_B, stroke_width=1.5)
        trl = label(r"trained on $256$", font_size=18, color=GREY_B).next_to(tr, UP, buff=0.05)
        leg = legend([(TF_C, r"transformer, \ rotary positions"), (HY_C, r"hybrid, \ attention without positions")],
                     font_size=20).move_to([4.6, 1.8, 0])
        ct, chy = np.asarray(r["transformer_copy"]), np.asarray(r["hybrid_copy"])
        none = max(float(ct.max()), float(chy.max())) < 0.05
        cl = label(r"the copy test: \\ $24$ random tokens, \ a stretch of a novel, \\ the same $24$ again", font_size=21,
                   color=GREY_A)
        cv = label(rf"copied right: \ transformer ${100 * ct.mean(0)[0]:.0f}\%$, \ hybrid ${100 * chy.mean(0)[0]:.0f}\%$ \\ "
                   rf"(copies {r['gaps'][0]} tokens apart)", font_size=21, color=WHITE)
        cg = VGroup(cl, cv).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        if cg.width > 4.6:
            cg.width = 4.6
        cg.move_to([4.55, -0.9, 0])
        far_t, far_h = float(mt[-200:].mean()), float(mh[-200:].mean())
        near_t, near_h = float(mt[100:240].mean()), float(mh[100:240].mean())
        v1 = (f"Past 256, the transformer's loss climbs, from {near_t:.2f} to {far_t:.2f} nats: rotary positions it "
              "never trained on. " if far_t > near_t + 0.1 else
              f"Past 256, the transformer's loss barely moves, {near_t:.2f} to {far_t:.2f}. ")
        v2 = (f"The hybrid's stays near where it was, {near_h:.2f} to {far_h:.2f}: its attention has no positions to "
              "run out of. " if far_h < near_h + 0.1 else
              f"The hybrid's climbs too, {near_h:.2f} to {far_h:.2f}. ")
        v3 = ("But neither can find a needle: given twenty-four random tokens, a stretch of a novel and the same "
              "twenty-four again, neither predicts the repeat, even sixteen tokens apart. Models this small, trained "
              "this briefly, never formed Part 13's induction heads; that is why the tests before used small models "
              "trained for the task." if none else
              f"And in the copy test, twenty-four random tokens repeated after a stretch of a novel, the transformer "
              f"predicts {100 * ct.mean(0)[0]:.0f} percent of the repeat and the hybrid {100 * chy.mean(0)[0]:.0f}, when "
              f"the copies are {r['gaps'][0]} tokens apart.")
        with self.voiceover(
            "Our two language models from the last chapter were trained on windows of 256 tokens. What happens "
            "past the end? <bookmark mark='a'/> Here is the loss at each position of held-out text a thousand tokens "
            "long, read in one go. " + v1 + "<bookmark mark='b'/> " + v2 + "<bookmark mark='c'/> " + v3
        ) as vo:
            self.play(FadeIn(leg), FadeIn(g1), Create(tr), FadeIn(trl))
            vo.wait_until("a")
            self.play(FadeIn(b1[0]), Create(c1[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(b1[1]), Create(c1[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(cg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def today(self):
        head = label(r"Long contexts in 2026", font_size=36).to_edge(UP, buff=0.35)
        rows = [
            (r"Gemini 1.5 \ (Google, 2024)", r"a million tokens; \ needles found in up to $10$ million, \ in research", HIST),
            (r"Kimi Linear \ (Moonshot, 2025)", r"RULER at $128$k: \ $84.3$, \ against $81.3$ for full attention \ "
             r"($1.4$T tokens each); \\ $78.8$ with rotary positions", HYB),
            (r"MRCR v2, \ eight needles \ (OpenAI's test)", r"at $1$M tokens: \ Claude Opus 4.6 $76\%$, \ Claude Sonnet 4.5 "
             r"$18.5\%$ \\ (Anthropic, \ February 2026)", C.BITS),
            (r"DeepSeek-V4 \ (2026)", r"$1$M tokens; \ keys and values compressed $4\times$ and $128\times$ \\ "
             r"(compressed sparse attention: \ Part 16)", ATT),
        ]
        tbl = VGroup()
        for i, (a, b, c_) in enumerate(rows):
            lines_ = VGroup(*[label(b_.strip(), font_size=25, color=GREY_A) for b_ in b.split(r"\\")]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
            tbl.add(VGroup(label(a, font_size=30, color=c_), lines_).arrange(DOWN, aligned_edge=LEFT, buff=0.14))
        tbl.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.45)
        if tbl.width > 13.2:
            tbl.width = 13.2
        if tbl.height > 6.3:
            tbl.height = 6.3
        tbl.next_to(head, DOWN, buff=0.45)
        src = note(r"each figure from its maker's report", font_size=16).to_corner(DR, buff=0.25)
        with self.voiceover(
            "Where does that leave the frontier? <bookmark mark='a'/> Google's Gemini 1.5, in 2024, offered a "
            "million tokens, and reported finding needles in up to ten million. <bookmark mark='b'/> Kimi Linear's "
            "report gives evidence for hybrids on long texts: on RULER at 128 thousand tokens, 84.3 "
            "against 81.3 for full attention trained the same way, and only 78.8 when its attention layers use "
            "rotary positions. <bookmark mark='c'/> On OpenAI's harder MRCR test, eight similar requests hidden in "
            "a million tokens, Anthropic reported in February 2026 that Claude Opus 4.6 found 76 percent, where "
            "its predecessor Sonnet 4.5 found 18.5. <bookmark mark='d'/> And DeepSeek-V4 reads a million tokens by "
            "compressing its keys and values, four and a hundred and twenty-eight to one, and choosing among them: "
            "Part 16's subject. These are each maker's own measurements."
        ) as vo:
            veils = VGroup(*[Rectangle(width=r_.width + 0.1, height=r_.height + 0.08, stroke_width=0,
                                       fill_color=BACKGROUND, fill_opacity=0.82).move_to(r_) for r_ in tbl])
            self.play(FadeIn(head), FadeIn(src), FadeIn(tbl), FadeIn(veils))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeOut(veils[k]))
        self.wait(0.3)
        self.clear_scene()
