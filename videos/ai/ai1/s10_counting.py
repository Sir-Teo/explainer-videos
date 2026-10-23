from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai1.common import ALPHA27, MONO, PART, load, plain_axes, polyline


class Counting(VoiceoverScene):
    def construct(self):
        self.card()
        self.samples()
        self.rule()
        self.curves()
        self.sparsity()
        self.laplace()
        self.reading()
        self.writing()
        self.lesson()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(9, r"Learning by counting, and Laplace's rule",
                            r"How far can you get by remembering what came next?", lit=(1948,), part=PART)
        with self.voiceover("Chapter nine. So far, our models have only counted. How far can counting go?") as vo:
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def samples(self):
        s = load("samples")["samples"]
        rows = [
            ("0", r"every symbol equally likely", s["0"]),
            ("1", r"letter frequencies", s["1"]),
            ("2", r"$1$ letter of context", s["2"]),
            ("3", r"$2$ letters", s["3"]),
            ("5", r"$4$ letters", s["5"]),
            ("7", r"$6$ letters", s["7"]),
            ("w2", r"words, $1$ word of context", s["w2"]),
        ]
        head = label(r"Text written by counting models of the $30$ books", font_size=34).to_edge(UP, buff=0.35)
        src = cite(r"after C.~E.~Shannon, \textit{A Mathematical Theory of Communication} (1948), \S 3; \ "
                   r"sampled here, seed $1948$")
        lines = VGroup()
        for key, name, txt in rows:
            t = txt[:62]
            if len(txt) > 62:
                t = t.rsplit(" ", 1)[0] if " " in t[40:] else t
            n = label(name, font_size=22, color=C.CONTEXT)
            body = Text(t, font=MONO, font_size=20, color=WHITE if key in ("5", "7", "w2") else GREY_A)
            lines.add(VGroup(n, body))
        for g in lines:
            g[0].move_to([-4.6, 0, 0], aligned_edge=RIGHT).shift(RIGHT * 0.0)
            g[1].next_to(g[0], RIGHT, buff=0.35)
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.45)
        for g in lines:
            g[0].align_to(lines[0][0], RIGHT)
            g[1].next_to(g[0], RIGHT, buff=0.35)
        lines.set_x(0)
        if lines.width > 13.4:
            lines.width = 13.4
        six = " ".join(s["7"].split()[:5])
        with self.voiceover(
            "In 1948, Shannon showed what counting can do by letting counting models write. <bookmark mark='a'/> "
            "With every symbol equally likely, you get noise. <bookmark mark='b'/> With the right letter "
            "frequencies, still noise, but with the right texture. <bookmark mark='c'/> Pick each letter by what "
            "followed the previous one in our books, and syllables appear. <bookmark mark='d'/> With two letters of "
            "context, short words. <bookmark mark='e'/> With four, mostly real words. <bookmark mark='f'/> With "
            f"six, phrases: {six}. <bookmark mark='g'/> Count whole words instead, and you get something that almost "
            "scans."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, mark in enumerate("abcdefg"):
                vo.wait_until(mark)
                g = lines[k]
                self.play(FadeIn(g[0]), AddTextLetterByLetter(g[1], time_per_char=0.012), run_time=1.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rule(self):
        head = label(r"The counting model", font_size=38).to_edge(UP, buff=0.5)
        f = mtex(r"q(c \mid \text{context}) = \frac{n(\text{context},\, c)}{n(\text{context})}", font_size=48)
        f.next_to(head, DOWN, buff=0.6)
        lt, bg = load("letters"), load("bigram")
        qi, ui = ALPHA27.index("q"), ALPHA27.index("u")
        n_q = int(lt["counts"][qi])
        n_qu = int(round(float(bg["joint"][qi, ui]) * int(lt["n"])))
        ex = mtex(r"q(\texttt{u} \mid \texttt{q}) = " + rf"\frac{{{n_qu:,}}}{{{n_q:,}}}".replace(",", "{,}"),
                  font_size=36, color=GREY_A)
        ex.next_to(f, DOWN, buff=0.5)
        cap = label(r"what followed this context in the books, as a fraction of the times it appeared", font_size=26,
                    color=GREY_A).next_to(ex, DOWN, buff=0.4)
        mle = label(r"(this is the \textit{maximum likelihood} estimate: Chapter 11)", font_size=24, color=GREY_B)
        mle.next_to(cap, DOWN, buff=0.3)
        with self.voiceover(
            "The rule behind all of these is simple. <bookmark mark='a'/> The probability of the next symbol, given "
            "a context, is the number of times it followed that context in the books, divided by the number of "
            "times the context appeared. <bookmark mark='b'/> It's the most natural estimate there is, and in "
            "chapter eleven we'll see why it's also the best one, for the books themselves."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(f))
            self.play(FadeIn(ex), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(mle))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def curves(self):
        d = load("orders")
        rows = d["rows"]
        ks = np.array([r["order"] for r in rows])
        plug = np.array([r["plugin"] for r in rows])
        test = np.array([r["test"] for r in rows])
        best = int(d["best"])
        sh27 = [float(v) for v in d["shannon_27"]]
        ax = plain_axes([0, 14, 2], [0, 5, 1], 9.6, 5.0).shift(DOWN * 0.45 + LEFT * 0.6)
        xl = VGroup(*[MathTex(str(k), font_size=24, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.15)
                      for k in range(0, 15, 2)])
        yl = VGroup(*[MathTex(str(v), font_size=24, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.15)
                      for v in range(0, 6)])
        axl = VGroup(label(r"letters of context $k$", font_size=24, color=GREY_A).next_to(ax, DOWN, buff=0.5),
                     label(r"bits per letter", font_size=24, color=GREY_A).next_to(ax.c2p(0, 5), UP, buff=0.15))
        c_plug = polyline(ax, ks, plug, color=C.COUNTING, stroke_width=4)
        c_test = polyline(ax, ks, test, color=C.SURPRISE, stroke_width=4)
        d_plug = VGroup(*[Dot(ax.c2p(k, v), radius=0.05, color=C.COUNTING) for k, v in zip(ks, plug)])
        d_test = VGroup(*[Dot(ax.c2p(k, v), radius=0.05, color=C.SURPRISE) for k, v in zip(ks, test)])
        l_plug = label(r"on the books it counted", font_size=24, color=C.COUNTING).next_to(ax.c2p(10, plug[10]), DOWN,
                                                                                            buff=0.3)
        l_test = label(r"on the Falcon passage: \ new text", font_size=24, color=C.SURPRISE)
        l_test.move_to(ax.c2p(7.0, 3.7))
        best_d = Dot(ax.c2p(best, test[best]), radius=0.09, color=WHITE)
        best_l = label(rf"best: \ $k = {best}$, \ ${test[best]:.2f}$ bits", font_size=24).next_to(best_d, UP, buff=0.25)
        sh = sh27[:3]
        sh_d = VGroup(*[Cross(scale_factor=0.08, stroke_color=C.HUMAN, stroke_width=3).move_to(ax.c2p(k - 1, v))
                        for k, v in zip(range(0, 3), sh) if k >= 1])
        sh_l = label(r"$\times$ \ Shannon's 1951 estimates, from printed tables", font_size=22, color=C.HUMAN)
        sh_l.to_corner(UR, buff=0.5).shift(DOWN * 0.6)
        uni = DashedLine(ax.c2p(0, 4.755), ax.c2p(14, 4.755), color=GREY_C, stroke_width=1.5)
        uni_l = label(r"$\log_2 27$: \ no knowledge", font_size=20, color=GREY_B).next_to(ax.c2p(14, 4.755), UP, buff=0.08)
        uni_l.align_to(uni, RIGHT)
        tag = computed_tag()
        with self.voiceover(
            "So let's score the counting models. For each amount of context, from no letters to fourteen, measure "
            "the bits per letter. <bookmark mark='a'/> First on the very books it counted. More context, fewer bits, "
            f"all the way down to {plug[-1]:.2f} bits per letter at {ks[-1]} letters. Our numbers for no context and "
            f"one letter of context, {plug[0]:.2f} and {plug[1]:.2f}, <bookmark mark='b'/> land next to the "
            f"estimates Shannon made in 1951 from printed tables, {sh27[1]:.2f} and {sh27[2]:.2f}."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(axl), Create(uni), FadeIn(uni_l), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(c_plug), FadeIn(d_plug), run_time=2.0)
            self.play(FadeIn(l_plug))
            vo.wait_until("b")
            self.play(FadeIn(sh_d), FadeIn(sh_l))
        with self.voiceover(
            "But on new text, the Falcon passage, <bookmark mark='a'/> the story is different. More context helps at "
            f"first: <bookmark mark='b'/> the best is {best} letters of context, at {test[best]:.2f} bits per letter. "
            "Beyond that, it gets worse"
            + (f", and with {ks[-1]} letters of context it's worse than knowing nothing but letter frequencies."
               if test[-1] > test[0] else f", up to {test[-1]:.2f} bits with {ks[-1]} letters of context.")
        ) as vo:
            vo.wait_until("a")
            self.play(Create(c_test), FadeIn(d_test), run_time=2.0)
            self.play(FadeIn(l_test))
            vo.wait_until("b")
            self.play(FadeIn(best_d, scale=1.5), FadeIn(best_l))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sparsity(self):
        d = load("orders")
        rows = d["rows"]
        seen = np.array([r["seen_frac"] for r in rows])
        nctx = np.array([r["contexts"] for r in rows])
        ks = np.arange(len(rows))
        head = label(r"Why: \ the books run out of examples", font_size=36).to_edge(UP, buff=0.4)
        ax = plain_axes([0, 14, 2], [0, 1, 0.25], 6.4, 3.6).shift(LEFT * 3.2 + DOWN * 0.5)
        xl = VGroup(*[MathTex(str(k), font_size=22, color=GREY_B).next_to(ax.c2p(k, 0), DOWN, buff=0.12)
                      for k in range(0, 15, 2)])
        yl = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(0, v), LEFT, buff=0.12)
                      for t, v in (("0", 0), ("50\\%", 0.5), ("100\\%", 1))])
        c = polyline(ax, ks, seen, color=C.CONTEXT, stroke_width=4)
        t = label(r"contexts in the passage that\\ ever occur in the books", font_size=22, color=C.CONTEXT)
        t.next_to(ax, UP, buff=0.2)
        xlab = label(r"letters of context $k$", font_size=22, color=GREY_A).next_to(ax, DOWN, buff=0.45)
        kL = int(ks[-1])
        e20 = kL * np.log10(27)
        facts = VGroup(
            mtex(rf"27^{{{kL}}} \approx 10^{{{e20:.0f}}} \ \text{{possible contexts}}", font_size=32),
            label(rf"the books contain ${nctx[kL] / 1e6:.1f}$ million of them", font_size=28, color=GREY_A),
            label(r"an unseen context: \ $q = \frac{0}{0}$; \ an unseen letter: \ $q = 0$, \ surprise $= \infty$",
                  font_size=26, color=C.SURPRISE),
        ).arrange(DOWN, buff=0.35).move_to(RIGHT * 3.4 + DOWN * 0.2)
        if facts.width > 6.8:
            facts.width = 6.8
        # contexts multiply: every 2-letter context, then the 4-letter contexts inside one of them, then all of those
        g = load("ctxgrid")
        seen2, grid4 = np.asarray(g["seen2"]), np.asarray(g["grid4"])
        G, cx, cy = 4.0, 3.5, -0.55
        cell = G / 27
        dark, lit = ManimColor("#1A2030"), ManimColor(C.CONTEXT)

        def grid27(mask, size, center):
            c = size / 27
            return VGroup(*[Square(side_length=c, stroke_width=0, fill_color=lit if mask[i, j] else dark, fill_opacity=1)
                            .move_to([center[0] - size / 2 + (j + 0.5) * c, center[1] + size / 2 - (i + 0.5) * c, 0])
                            for i in range(27) for j in range(27)])

        g2 = grid27(seen2, G, (cx, cy))
        ti, hi = ALPHA27.index("t"), ALPHA27.index("h")
        th = g2[ti * 27 + hi]
        sub = grid27(grid4[ti * 27:(ti + 1) * 27, hi * 27:(hi + 1) * 27], G, (cx, cy))
        dens = grid4.reshape(243, 3, 243, 3).mean(axis=(1, 3))[..., None] ** 0.6  # 3 x 3 pooling, shaded by how many are seen
        rgb = (dens * np.array(lit.to_rgb()) + (1 - dens) * np.array(dark.to_rgb())) * 255
        img = ImageMobject(rgb.astype(np.uint8)).set_resampling_algorithm(RESAMPLING_ALGORITHMS["bilinear"])
        img.height = G
        img.move_to([cx, cy, 0])
        home = np.array([cx - G / 2 + (hi + 0.5) * cell, cy + G / 2 - (ti + 0.5) * cell, 0])
        l2 = label(rf"$2$ letters: \ $27^2 = 729$ contexts; \ the books have ${100 * g['frac2']:.0f}\%$", font_size=26,
                   color=C.CONTEXT).next_to(g2, UP, buff=0.2)
        lth = label(r"\texttt{th} then $2$ more: \ $27^2$ again", font_size=26, color=C.CONTEXT).next_to(g2, UP, buff=0.2)
        l4 = label(rf"$4$ letters: \ $27^4 = 531{{,}}441$; \ the books have ${100 * g['frac4']:.0f}\%$", font_size=26,
                   color=C.CONTEXT).next_to(g2, UP, buff=0.2)
        with self.voiceover(
            "The reason is that contexts multiply. <bookmark mark='a'/> Of all the five-letter contexts in the Falcon "
            f"passage, {100 * seen[5]:.0f} percent appear somewhere in the books. Of the {kL}-letter contexts, only "
            f"{100 * seen[kL]:.0f} percent do. <bookmark mark='b'/> There are about ten to the {e20:.0f} possible "
            f"{kL}-letter contexts, and the books contain {nctx[kL] / 1e6:.1f} million of them. <bookmark mark='c'/> A "
            "context the books never saw gives the model nothing to go on, and a letter never seen after it would get "
            "probability zero: infinite surprise."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(t), FadeIn(xlab),
                      LaggedStart(*[FadeIn(q) for q in g2], lag_ratio=0.002), FadeIn(l2), run_time=1.6)
            vo.wait_until("a")
            self.play(Create(c), run_time=2.0)
            vo.wait_until("b")
            others = VGroup(*[q for q in g2 if q is not th])
            self.play(FadeOut(others), th.animate.scale(27).move_to([cx, cy, 0]), ReplacementTransform(l2, lth),
                      run_time=1.4)
            self.play(FadeIn(sub, lag_ratio=0.002), FadeOut(th), run_time=1.0)
            self.play(sub.animate.scale(1 / 27).move_to(home), FadeIn(img), ReplacementTransform(lth, l4), run_time=1.6)
            self.remove(sub)
            self.play(FadeOut(img), FadeOut(l4), FadeIn(facts[0]), FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(FadeIn(facts[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def laplace(self):
        """Laplace's rule of succession, add-one and add-alpha smoothing, and what alpha costs at each context length."""
        sm = load("smoothing")
        A = np.asarray(sm["alphas"], float)
        orders = [int(o) for o in sm["orders"]]
        lap = list(A).index(1.0)
        head = label(r"Laplace's rule of succession (1814)", font_size=36).to_edge(UP, buff=0.35)
        rows = [
            cmath(r"P(\text{next success})", r"=", r"\frac{\int_0^1 \theta^{s+1} (1-\theta)^{n-s}\, d\theta}"
                  r"{\int_0^1 \theta^{s} (1-\theta)^{n-s}\, d\theta}", font_size=34),
            cmath(r"P(\text{next success})", r"=", r"\frac{s + 1}{n + 2}", font_size=38),
            cmath(r"q(c \mid \text{ctx})", r"=", r"\frac{n(\text{ctx}, c) + 1}{n(\text{ctx}) + 27}", font_size=36),
            cmath(r"q_\alpha(c \mid \text{ctx})", r"=", r"\frac{n(\text{ctx}, c) + \alpha}{n(\text{ctx}) + 27\alpha}",
                  font_size=36, colors={r"q_\alpha(c \mid \text{ctx})": C.BITS}),
        ]
        whys = [why(r"every chance $\theta$ equally likely beforehand; \ $s$ successes in $n$ trials"),
                why(r"Euler's beta integral"), why(r"$27$ outcomes: \ add one to every count"),
                why(r"add $\alpha$: \ a prior less sure that anything can happen")]
        step = ladder(self, rows, whys, keep=2, top=2.2, x=-1.8, buff=0.5, edge=6.9)
        sun = label(r"Laplace: \ $5{,}000$ years of sunrises, \ $1{,}826{,}213$ days $\Rightarrow$ odds of "
                    r"$1{,}826{,}214$ to $1$ on tomorrow", font_size=24, color=GREY_A).to_edge(DOWN, buff=0.4)
        src = cite(r"P.-S.~Laplace, \textit{Essai philosophique sur les probabilit\'es} (1814)", corner=DR)
        with self.voiceover(
            "The patch is older than computers. In 1814 Pierre-Simon Laplace asked: if something has happened s "
            "times in n tries, how likely is it next time? <bookmark mark='a'/> Suppose that, before looking, every "
            "chance between zero and one was equally plausible. Weigh each chance by how well it explains what you "
            "saw, <bookmark mark='b'/> and the answer is s plus one, over n plus two. <bookmark mark='c'/> His "
            "example was the sunrise: five thousand years of it, 1,826,213 days, gives odds of 1,826,214 to one "
            "that the sun rises tomorrow. <bookmark mark='d'/> For our 27 symbols, the same reasoning says: add one "
            "to every count. Nothing ever gets probability zero. <bookmark mark='e'/> Add alpha instead of one, and "
            "you have the smoothing that keeps our curves finite, with alpha chosen on held-out text."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            step(0)
            vo.wait_until("a")
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            self.play(FadeIn(sun))
            vo.wait_until("d")
            self.play(FadeOut(sun), FadeOut(src))
            step(2)
            vo.wait_until("e")
            step(3)
        self.wait(0.3)
        self.clear_scene()
        # how much alpha matters, at each context length
        cols = dict(zip(orders, (GREY_B, C.COUNTING, C.SURPRISE, C.BITS)))
        T = {o: np.asarray(sm[f"test_{o}"]) for o in orders}
        V = {o: np.asarray(sm[f"valid_{o}"]) for o in orders}
        lo_y = min(float(T[o].min()) for o in orders) - 0.2
        hi_y = min(4.75, max(float(T[o].max()) for o in orders) + 0.1)
        a = axes([-4, 1], [lo_y, hi_y], x_length=7.4, y_length=4.4, xlabel=r"$\alpha$ \ (log scale)",
                 ylabel=r"bits per letter on the Falcon passage", xticks=[-4, -3, -2, -1, 0, 1],
                 yticks=[round(v, 1) for v in np.arange(np.ceil(lo_y * 2) / 2, hi_y, 0.5)],
                 xfmt=lambda v: f"10^{{{int(v)}}}", center=[-2.2, -0.45, 0], font_size=20)
        ax = a.ax
        lx = np.log10(A)
        lines = VGroup(*[curve(ax, lx, np.minimum(T[o], hi_y), cols[o], 3.5) for o in orders])
        best = {o: int(np.argmin(V[o])) for o in orders}
        marks = VGroup()
        for o in orders:
            marks.add(Dot(ax.c2p(lx[best[o]], T[o][best[o]]), radius=0.07, color=cols[o]))
            marks.add(Square(0.16, stroke_color=cols[o], stroke_width=2.5).move_to(ax.c2p(0, min(T[o][lap], hi_y))))
        lapl = DashedLine(ax.c2p(0, lo_y), ax.c2p(0, hi_y), color=GREY_B, stroke_width=1.5)
        lapt = label(r"Laplace: \ $\alpha = 1$", font_size=20, color=GREY_B).next_to(ax.c2p(0, hi_y), UP, buff=0.08)
        names = VGroup(*[label(rf"${o}$ letter{'s' if o > 1 else ''} of context", font_size=22, color=cols[o])
                         for o in orders]).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        key = VGroup(names, label(r"$\bullet$ \ $\alpha$ chosen on held-out text", font_size=20, color=GREY_A),
                     label(r"$\square$ \ Laplace's add-one", font_size=20, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT,
                                                                                                buff=0.18)
        key.move_to([4.6, 0.6, 0])
        ol = orders[-1]
        un = float(sm[f"unseen_pair_{ol}"])
        tag = computed_tag()
        cost = T[ol][lap] - T[ol][best[ol]]
        short = orders[0]
        short_said = ("For one letter of context, Laplace's rule is as good as anything"
                      if abs(T[short][lap] - T[short][best[short]]) < 0.005 else
                      f"For one letter of context, Laplace's rule costs {T[short][lap] - T[short][best[short]]:.3f} bits")
        with self.voiceover(
            "How much does alpha matter? <bookmark mark='a'/> Here is every alpha from a ten-thousandth to ten, at "
            f"four context lengths, scored on the Falcon passage. <bookmark mark='b'/> {short_said}: its contexts "
            f"are seen millions of times. <bookmark mark='c'/> With {ol} letters of context, {100 * un:.0f} percent of "
            "the passage's letters come after a context where the books never showed that letter, and most contexts "
            "were seen only a few times. Adding one to every count drowns the evidence: Laplace's rule costs "
            f"{cost:.2f} bits per letter more than the alpha chosen on held-out text, {A[best[ol]]:.2f}. "
            "Good smoothing is a question about what you haven't seen. Part 7 answers it properly."
        ) as vo:
            self.play(FadeIn(a), FadeIn(tag), Create(lapl), FadeIn(lapt))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(l_) for l_ in lines], lag_ratio=0.3), FadeIn(key), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(marks[0:2]))
            vo.wait_until("c")
            self.play(FadeIn(marks[2:]))
            self.play(Indicate(marks[-1], color=WHITE, scale_factor=1.6))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reading(self):
        """Learning by counting, as it reads: four context lengths scored on the Falcon passage against text counted."""
        d = load("seen")
        A = np.asarray(d["amounts"], float)
        orders = [int(o) for o in d["orders"]]
        B = {o: np.asarray(d[f"bits_{o}"]) for o in orders}
        cols = dict(zip(orders, (GREY_B, C.COUNTING, C.SURPRISE, C.BITS)))
        lx = np.log10(A)
        ax = plain_axes([3, 7.5, 1], [2, 5, 1], 8.4, 4.6).shift(DOWN * 0.4 + LEFT * 1.3)
        xl = VGroup(*[MathTex(t, font_size=22, color=GREY_B).next_to(ax.c2p(v, 2), DOWN, buff=0.12)
                      for t, v in ((r"10^3", 3), (r"10^4", 4), (r"10^5", 5), (r"10^6", 6), (r"10^7", 7))])
        yl = VGroup(*[MathTex(str(v), font_size=22, color=GREY_B).next_to(ax.c2p(3, v), LEFT, buff=0.12) for v in (2, 3, 4, 5)])
        axl = VGroup(label(r"letters of the books counted \ (log scale)", font_size=22, color=GREY_A).next_to(xl, DOWN, buff=0.15),
                     label(r"bits per letter on the Falcon passage", font_size=22, color=GREY_A).next_to(ax.c2p(3, 5), UP, buff=0.15)
                     .align_to(ax, LEFT))
        uni = DashedLine(ax.c2p(3, 4.755), ax.c2p(7.5, 4.755), color=GREY_C, stroke_width=1.5)
        uni_l = label(r"$\log_2 27$: \ no knowledge", font_size=20, color=GREY_B).next_to(ax.c2p(7.5, 4.755), UP, buff=0.08)
        uni_l.align_to(uni, RIGHT)
        t = ValueTracker(float(lx[0]))

        def upto(o):
            x_ = t.get_value()
            pts = [(a_, b_) for a_, b_ in zip(lx, B[o]) if a_ <= x_ + 1e-9]
            if x_ > pts[-1][0] and len(pts) < len(lx):
                i = len(pts)
                f_ = (x_ - lx[i - 1]) / (lx[i] - lx[i - 1])
                pts.append((x_, B[o][i - 1] + f_ * (B[o][i] - B[o][i - 1])))
            pts = pts if len(pts) > 1 else pts * 2
            return VMobject(color=cols[o], stroke_width=4).set_points_as_corners([ax.c2p(a_, b_) for a_, b_ in pts])

        lines = VGroup(*[always_redraw(lambda o=o: upto(o)) for o in orders])
        names = VGroup(*[label(rf"${o}$ letter{'s' if o > 1 else ''} of context", font_size=22, color=cols[o]) for o in orders])
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_corner(UR, buff=0.5).shift(DOWN * 0.7)

        def best_at(i):
            return min(orders, key=lambda o: B[o][i])

        lead = [best_at(i) for i in range(len(A))]
        assert lead[0] == orders[0]  # the narration says the shortest context starts ahead
        takes = [(i, lead[i]) for i in range(1, len(A)) if lead[i] != lead[i - 1]]  # where the lead changes hands
        crown = always_redraw(lambda: Star(n=5, outer_radius=0.1, color=WHITE, fill_opacity=1).move_to(  # on the best curve
            ax.c2p(t.get_value(), min(float(np.interp(t.get_value(), lx, B[o])) for o in orders))))
        o_long = orders[-1]
        words = {3: "three", 5: "five", 8: "eight"}

        def amount(n):
            return {1000: "a thousand", 3000: "three thousand", 10_000: "ten thousand", 30_000: "thirty thousand",
                    100_000: "a hundred thousand", 300_000: "three hundred thousand", 1_000_000: "a million",
                    3_000_000: "three million"}.get(int(n), f"{n:,.0f}")

        ending = (f"{words[o_long]} letters is still behind, at {B[o_long][-1]:.2f}: it would need far more text "
                  "than we have." if lead[-1] != o_long else f"{words[o_long]} letters finally leads.")
        with self.voiceover(
            "And how does a counting model learn? It reads, and counts. Here are four of them, with one, three, five "
            "and eight letters of context, scored on the Falcon passage as they count more and more of the books. "
            f"<bookmark mark='a'/> After a thousand letters, one letter of context is best, {B[orders[0]][0]:.2f} bits: "
            "a short context is seen often enough to count quickly, while longer ones have hardly met any of their "
            "contexts."
        ) as vo:
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(axl), Create(uni), FadeIn(uni_l), FadeIn(names))
            self.add(lines, crown)
            vo.wait_until("a")
        for i, o in takes:  # one short line each time the lead changes hands
            with self.voiceover(f"At {amount(A[i])} letters, {words.get(o, str(o))} letters of context take the lead."):
                self.play(t.animate.set_value(float(lx[i])), run_time=2.5, rate_func=linear)
                self.play(Indicate(names[orders.index(o)], color=cols[o]))
        with self.voiceover(
            f"With all {A[-1] / 1e6:.0f} million letters, {ending} The more you can count, the longer the context "
            "worth using."
        ):
            self.play(t.animate.set_value(float(lx[-1])), run_time=2.5, rate_func=linear)
        self.wait(0.5)
        self.remove(lines, crown)
        self.clear_scene()

    # ------------------------------------------------------------------
    def writing(self):
        """The five-letter model's own writing at checkpoints of its reading; copied stretches in red."""
        w, seen = load("writing"), load("seen")
        amounts = [int(a) for a in w["amounts"]]
        A = [int(a) for a in seen["amounts"]]
        assert int(w["context"]) == 5 and all(a in A for a in amounts)
        bits = [float(seen["bits_5"][A.index(a)]) for a in amounts]
        L = int(w["copy_len"])
        n_show = 44
        shown, share = [], []
        for a in amounts:
            t_ = w["samples"][str(a)][:n_show]
            t_ = t_.rsplit(" ", 1)[0] if " " in t_[30:] else t_
            m_ = w["mask"][str(a)][:len(t_)]
            shown.append((t_, m_))
            share.append(m_.count("1") / len(t_))
        head = label(r"The $5$-letter model, writing as it reads", font_size=34).to_edge(UP, buff=0.4)
        hdr = VGroup(label(r"letters read", font_size=22, color=GREY_B), label(r"what it writes", font_size=22, color=GREY_B),
                     label(r"copied", font_size=22, color=C.SURPRISE), label(r"bits", font_size=22, color=C.COUNTING))
        X1, X2, X3, X4 = -4.25, -3.95, 4.55, 6.45  # right edge of col 1, left of col 2, right of cols 3 and 4
        ys = [1.75 - 0.95 * k for k in range(len(amounts))]
        rows = VGroup()
        for k, (a, (t_, m_)) in enumerate(zip(amounts, shown)):
            n_ = label(rf"${a:,}$".replace(",", "{,}"), font_size=26, color=C.CONTEXT)
            n_.move_to([X1, ys[k], 0], aligned_edge=RIGHT)
            body = data_text(t_, font=MONO, font_size=20, color=WHITE)
            glyphs = [c for c in t_ if not c.isspace()]
            flags = [f for c, f in zip(t_, m_) if not c.isspace()]
            assert len(glyphs) == len(body.submobjects)
            for g_, f in zip(body.submobjects, flags):
                g_.set_color(C.SURPRISE if f == "1" else WHITE)
            body.move_to([X2, ys[k], 0], aligned_edge=LEFT)
            cp = MathTex(rf"{100 * share[k]:.0f}\%", font_size=28, color=C.SURPRISE).move_to([X3, ys[k], 0], aligned_edge=RIGHT)
            bt = MathTex(f"{bits[k]:.2f}", font_size=28, color=C.COUNTING).move_to([X4, ys[k], 0], aligned_edge=RIGHT)
            rows.add(VGroup(n_, body, cp, bt))
        hdr[0].move_to([X1, ys[0] + 0.75, 0], aligned_edge=RIGHT)
        hdr[1].move_to([X2, ys[0] + 0.75, 0], aligned_edge=LEFT)
        hdr[2].move_to([X3, ys[0] + 0.75, 0], aligned_edge=RIGHT)
        hdr[3].move_to([X4, ys[0] + 0.75, 0], aligned_edge=RIGHT)
        grid_ = VGroup(hdr, rows)
        if grid_.width > 13.4:
            grid_.scale_to_fit_width(13.4)
        key = label(rf"red: \ inside a stretch of ${L}$ letters or more, copied word for word from what it read; \ "
                    r"bits: \ on the Falcon passage", font_size=20, color=GREY_B).to_edge(DOWN, buff=0.35)
        if key.width > 13.2:
            key.scale_to_fit_width(13.2)
        late = share[2:]
        nothing = ("nothing is copied" if max(late) == 0 else
                   (f"at most {100 * max(late):.0f} percent is copied" if max(late) >= 0.01 else "almost nothing is copied"))
        recite = "it can only recite: " if share[0] > 0.5 else "it mostly invents, but "
        with self.voiceover(
            "Here's the five-letter model writing, as it reads, from the same start and with the same dice each "
            f"time. <bookmark mark='a'/> After a thousand letters {recite}{100 * share[0]:.0f} percent "
            f"of what it writes, in red, is copied word for word, in stretches of {L} letters or more, from the "
            f"little it has read. <bookmark mark='b'/> After ten thousand, {100 * share[1]:.0f} percent. "
            f"<bookmark mark='c'/> From a hundred thousand on, {nothing}: it strings real-looking words together "
            f"on its own, <bookmark mark='d'/> and its score on the Falcon passage goes from {bits[0]:.2f} bits per "
            f"letter to {bits[-1]:.2f}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][0]), AddTextLetterByLetter(rows[0][1], time_per_char=0.02), FadeIn(rows[0][2]),
                      run_time=1.2)
            vo.wait_until("b")
            self.play(FadeIn(rows[1][0]), AddTextLetterByLetter(rows[1][1], time_per_char=0.02), FadeIn(rows[1][2]),
                      run_time=1.2)
            vo.wait_until("c")
            for r in rows[2:]:
                self.play(FadeIn(r[0]), AddTextLetterByLetter(r[1], time_per_char=0.015), FadeIn(r[2]), run_time=1.0)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r[3], shift=LEFT * 0.1) for r in rows], lag_ratio=0.25), run_time=1.5)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lesson(self):
        a = label(r"memorizing the books $\ne$ predicting new text", font_size=40, color=C.BITS)
        b = label(r"the gap between them is \textit{generalization}", font_size=32, color=GREY_A)
        c = label(r"counting can't tell that \texttt{the dog barked} and \texttt{the hound barked} are alike",
                  font_size=28, color=GREY_A)
        g = VGroup(a, b, c).arrange(DOWN, buff=0.45).move_to(UP * 0.6)
        pay = payoff_card([(r"smoothing, done properly", [7]), (r"generalization", [8]),
                           (r"sharing strength between similar contexts", [3, 9])], font_size=24, title=r"")
        pay.next_to(g, DOWN, buff=0.7)
        with self.voiceover(
            "This is the first appearance of the central problem of machine learning. <bookmark mark='a'/> A model "
            "can fit the data it learned from almost perfectly, and still guess badly on new data. The gap between "
            "the two is called generalization. <bookmark mark='b'/> And counting has a deeper limit: every context "
            "is its own island. It can't tell that the dog barked and the hound barked are alike, so it can't "
            "borrow what it learned about one for the other. <bookmark mark='c'/> Better smoothing comes in part "
            "seven, generalization in part eight, and models that share what they learn between similar contexts, "
            "with vectors and networks, in parts three and nine."
        ) as vo:
            self.play(FadeIn(a))
            vo.wait_until("a")
            self.play(FadeIn(b))
            vo.wait_until("b")
            self.play(FadeIn(c))
            vo.wait_until("c")
            self.play(FadeIn(pay))
        self.wait(0.5)
        self.clear_scene()
