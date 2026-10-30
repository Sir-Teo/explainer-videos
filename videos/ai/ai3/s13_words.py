from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai3.common import HIST, MONO, chapter, load


class Words(VoiceoverScene):
    def construct(self):
        chapter(self, 12, r"Word vectors from counting", r"Can a computer learn what words mean by counting?",
                "Chapter twelve. Word vectors, from counting.", lit=(1990,))
        self.history()
        self.table()
        self.neighbours()
        self.directions()
        self.analogy()

    # ------------------------------------------------------------------
    def history(self):
        cards = VGroup(
            history_card(1954, r"Zellig Harris, \ \textit{Distributional Structure}",
                         r"words that occur in the same contexts tend to have similar meanings", color=HIST, width=4.3,
                         font_size=30),
            history_card(1957, r"J.~R.~Firth",
                         r"``You shall know a word by the company it keeps''", color=HIST, width=4.3, font_size=30),
            history_card(1990, r"S.~Deerwester, \ S.~Dumais et al., \ latent semantic analysis",
                         r"an SVD of a word-by-document table: \ search that finds \textit{car} for \textit{automobile}",
                         color=HIST, width=4.3, font_size=30),
        ).arrange(RIGHT, buff=0.2, aligned_edge=UP).move_to(DOWN * 0.3)
        head = label(r"Meaning from company", font_size=40).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Part 1's counting model treated every word as an island. The fix is an old idea from linguistics. "
            "<bookmark mark='a'/> In 1954 Zellig Harris argued that words in the same contexts tend to mean similar "
            "things. <bookmark mark='b'/> In 1957 John Firth: you shall know a word by the company it keeps. "
            "<bookmark mark='c'/> In 1990 Scott Deerwester, Susan Dumais and colleagues made it an algorithm: count "
            "words in documents, take the SVD, and search by meaning rather than spelling."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(cards[2], shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        w = load("words")
        T = np.asarray(w["top300"])
        v = np.clip(T / np.percentile(T[T > 0], 99), 0, 1) ** 0.6
        dark, lit = np.array(ManimColor("#121826").to_rgb()), np.array(ManimColor(C.CONTEXT).to_rgb())
        rgb = ((v[..., None] * lit + (1 - v[..., None]) * dark) * 255).astype(np.uint8)
        img = ImageMobject(rgb).set_resampling_algorithm(RESAMPLING_ALGORITHMS["nearest"])
        img.height = 4.6
        img.move_to([-3.3, -0.5, 0])
        vocab = list(w["vocab"])
        ticks = VGroup(data_text(" ".join(vocab[:4]) + " …", font=MONO, font_size=20, color=GREY_A).next_to(img, UP, buff=0.12))
        cap = label(r"the $300$ commonest words, \\ of the $10{,}000$", font_size=24, color=GREY_B).next_to(img, DOWN, buff=0.15)
        P = C.CONTEXT
        pmi = cmath(r"\mathrm{PMI}(w, c)", "=", r"\log \frac{P(w, c)}{P(w)\,P(c)}", colors={r"\mathrm{PMI}(w, c)": P},
                    font_size=46).move_to([3.3, 1.4, 0])
        what = label(r"how much more often $w$ and $c$ meet \\ than if words were scattered at random", font_size=26,
                     color=GREY_A).next_to(pmi, DOWN, buff=0.3)
        keep = label(r"keep the positive part: \ $\max(\mathrm{PMI}, 0)$", font_size=28, color=P).next_to(what, DOWN, buff=0.35)
        counts = label(rf"${w['n_words'] / 1e6:.2f}$ million words; \ pairs within $4$ words of each other", font_size=26,
                       color=GREY_A)
        ex_rows = VGroup(*[MathTex(rf"\mathrm{{PMI}}(\texttt{{{a}}}, \texttt{{{b}}}) = {v:.2f}", font_size=28, color=P)
                           for a, b, n_, v in w["show_pairs"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        ex_rows.next_to(keep, DOWN, buff=0.35)
        counts.to_edge(UP, buff=0.45)
        with self.voiceover(
            "We'll do it with the thirty novels. <bookmark mark='a'/> Take the ten thousand commonest words and count "
            "how often each pair turns up within four words: a hundred million cells, from "
            f"{w['n_words'] / 1e6:.2f} million words of text. <bookmark mark='b'/> Then turn counts into surprise, "
            "Part 1's way: the log of how many times more often two words meet than by chance, the pointwise mutual "
            "information. Keep its positive part. <bookmark mark='c'/> Monday and morning: "
            f"{w['show_pairs'][0][3]:.2f}. The and of meet {int(w['show_pairs'][-1][2]):,} times, but they meet "
            f"everything: {w['show_pairs'][-1][3]:.2f}."
        ) as vo:
            self.play(FadeIn(counts))
            vo.wait_until("a")
            self.play(FadeIn(img), FadeIn(ticks), FadeIn(cap))
            vo.wait_until("b")
            self.play(Write(pmi))
            self.play(FadeIn(what))
            self.play(FadeIn(keep))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in ex_rows], lag_ratio=0.3))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def neighbours(self):
        w = load("words")
        nb = w["neighbours"]
        s = np.asarray(w["s"])
        show = ["monday", "three", "dog", "ship"]
        say = {x: [y for y, _ in nb[x][:3]] for x in show}
        perez_in = "perezvon" in [y for y, _ in nb["dog"][:5]]
        pq_in = "pequod" in [y for y, _ in nb["ship"][:5]]
        if perez_in and pq_in:
            extra = " Perezvon is a dog in The Brothers Karamazov, and the Pequod is Ahab's ship."
        elif perez_in:
            extra = " Perezvon is a dog in The Brothers Karamazov."
        elif pq_in:
            extra = " The Pequod is Ahab's ship."
        else:
            extra = ""
        head = label(r"Keep the table's $100$ strongest directions: \ $100$ numbers per word", font_size=32)
        head.to_edge(UP, buff=0.4)
        cols = VGroup()
        for word in show:
            title = data_text(word, font=MONO, font_size=30, color=C.BITS)
            rows = VGroup()
            for x, sim in nb[word][:5]:
                bar = Rectangle(width=1.6 * sim, height=0.22, stroke_width=0, fill_color=C.CONTEXT, fill_opacity=0.85)
                rows.add(VGroup(data_text(x, font=MONO, font_size=22, color=WHITE), bar).arrange(RIGHT, buff=0.12))
            rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
            cols.add(VGroup(title, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.3))
        cols.arrange(RIGHT, buff=0.55, aligned_edge=UP).next_to(head, DOWN, buff=0.6)
        if cols.width > 13.2:
            cols.width = 13.2
        perez = label((r"Perezvon: \ a dog in \textit{The Brothers Karamazov}" if perez_in else "")
                      + (r"; \ the Pequod: \ Ahab's ship" if pq_in else ""), font_size=26, color=GREY_A)
        perez.to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Keep the table's hundred strongest directions, with the SVD. <bookmark mark='a'/> Every word gets a hundred "
            "numbers. <bookmark mark='b'/> Words that keep the same company end up close. Monday: "
            f"{', '.join(say['monday'])}. Three: {', '.join(say['three'])}. Dog: {', '.join(say['dog'])}. Ship: "
            f"{', '.join(say['ship'])}.{extra} Nobody gave it a dictionary."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c[0]) for c in cols], lag_ratio=0.2))
            vo.wait_until("b")
            for c in cols:
                self.play(LaggedStart(*[AnimationGroup(FadeIn(r[0]), GrowFromEdge(r[1], LEFT)) for r in c[1]],
                                      lag_ratio=0.2), run_time=1.2)
            self.play(FadeIn(perez))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def directions(self):
        """Meaning arriving direction by direction: neighbours from the first k of the 100 SVD directions."""
        w = load("words")
        E = np.asarray(w["E"], float)
        vocab = list(w["vocab"])
        idx = {x: i for i, x in enumerate(vocab)}
        ks = [2, 5, 10, 25, 100]
        assert E.shape[1] == ks[-1]

        def near(word, k, n=5):
            e = E[:, :k] / np.linalg.norm(E[:, :k], axis=1, keepdims=True)
            sim = e @ e[idx[word]]
            return [vocab[i] for i in np.argsort(-sim)[1:n + 1]]

        words = ["three", "ship", "father", "monday"]
        final = {x: set(near(x, ks[-1], 10)) for x in words}  # each word's 10 nearest, with all 100 directions
        nb = {(x, k): near(x, k) for x in words for k in ks}
        settle = {x: next((k for k in ks if sum(y in final[x] for y in nb[(x, k)]) >= 3), ks[-1]) for x in words}
        hits0 = sum(sum(y in final[x] for y in nb[(x, ks[0])]) for x in words)
        days = "monday tuesday wednesday thursday friday saturday sunday".split()
        proper = lambda w_: w_.capitalize() if w_ in days else w_  # noqa: E731

        def column(k, word):  # a fixed pitch, so the rows line up across columns
            return VGroup(*[data_text(y, font=MONO, font_size=26, color=C.BITS if y in final[word] else GREY_B)
                            .move_to(DOWN * 0.52 * i) for i, y in enumerate(nb[(word, k)])])

        heads = VGroup(*[data_text(x, font=MONO, font_size=32, color=WHITE) for x in words]).arrange(RIGHT, buff=1.9)
        heads.move_to([0, 1.5, 0])
        cols = VGroup(*[column(ks[0], x).next_to(h_, DOWN, buff=0.45) for x, h_ in zip(words, heads)])
        t = ValueTracker(ks[0])
        cnt = always_redraw(lambda: label(rf"keeping the first ${int(round(t.get_value()))}$ of the $100$ directions",
                                          font_size=30, color=C.CONTEXT).to_edge(UP, buff=0.45))
        sub = label(r"each word's $5$ nearest neighbours; \ highlighted: \ among its $10$ nearest with all $100$",
                    font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        if sub.width > 13.0:
            sub.scale_to_fit_width(13.0)
        order = sorted(words, key=lambda x: settle[x])
        with self.voiceover(
            "How many directions does meaning need? Keep only the strongest few. <bookmark mark='a'/> With "
            f"{ks[0]}, only {hits0} of these twenty neighbours are final ones. <bookmark mark='b'/> With {ks[1]}, "
            f"<bookmark mark='c'/> {ks[2]}, <bookmark mark='d'/> {ks[3]}, <bookmark mark='e'/> and all {ks[-1]}. "
            f"{order[0]} settles first, with {settle[order[0]]} directions; {order[3]} needs {settle[order[3]]}. The "
            "strongest directions carry the broad patterns; finer meanings live further down."
        ) as vo:
            self.add(cnt)
            self.play(FadeIn(heads), FadeIn(sub))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cols], lag_ratio=0.15))
            for k, mark in zip(ks[1:], "bcde"):
                vo.wait_until(mark)
                new = VGroup(*[column(k, x).next_to(h_, DOWN, buff=0.45) for x, h_ in zip(words, heads)])
                self.play(FadeOut(cols), FadeIn(new), t.animate.set_value(k), run_time=1.0)  # words cross-fade, never morph
                cols = new
        self.wait(0.3)
        self.remove(cnt)
        self.clear_scene()

    # ------------------------------------------------------------------
    def analogy(self):
        w = load("words")
        an = w["analogies"]
        first = an["france:paris::england"][0]
        mk = an["man:king::woman"][:2]
        land_say = ("The nearest word to where you land is London." if first == "london" else
                    f"The nearest word to where you land is {first}.")
        at = w["analogy_test"]
        pu = w["purity"]
        xy = np.asarray(w["analogy_xy"])
        xy = xy / np.abs(xy).max() * 2.6
        pts = [np.array([x, y, 0]) + DOWN * 0.3 for x, y in xy]
        names = ["france", "paris", "england", "london"]
        cols = [C.TRUE_P, C.BITS, C.TRUE_P, C.BITS]
        dots = VGroup(*[glow_dot(p, color=c, radius=0.09) for p, c in zip(pts, cols)])
        labs = VGroup(*[data_text(n, font=MONO, font_size=28, color=c).next_to(p, UP if k % 2 else DOWN, buff=0.18)
                        for k, (n, p, c) in enumerate(zip(names, pts, cols))])
        step = Arrow(pts[0], pts[1], buff=0.12, color=C.BITS, stroke_width=5)
        again = Arrow(pts[2], pts[2] + (pts[1] - pts[0]), buff=0.12, color=C.BITS, stroke_width=5)
        land = DashedLine(pts[2] + (pts[1] - pts[0]), pts[3], color=GREY_B, stroke_width=2)
        head = label(r"Directions mean something too", font_size=34).to_edge(UP, buff=0.4)
        near = an["france:paris::england"][:5]
        res = VGroup(label(r"the words nearest to where you land:", font_size=24, color=GREY_A),
                     *[data_text(f"{k + 1}. {wd}", font=MONO, font_size=24, color=C.BITS if k == 0 else WHITE)
                       for k, wd in enumerate(near)]).arrange(DOWN, aligned_edge=LEFT, buff=0.1).to_corner(DR, buff=0.3)
        k2 = label(rf"\texttt{{man}} : \texttt{{king}} :: \texttt{{woman}} : \ \texttt{{{mk[0]}}}, \ "
                   rf"\texttt{{{mk[1]}}}, \ \ldots", font_size=28, color=GREY_A)
        k2.move_to([-6.6, 0.4, 0], aligned_edge=LEFT)
        score = label(rf"on ${at['all']['n']}$ such questions from the books: \ ${100 * at['all']['acc']:.0f}\%$ right",
                      font_size=26, color=C.BITS).next_to(k2, DOWN, buff=0.2).align_to(k2, LEFT)
        tag = label(r"drawn on the plane of the two steps", font_size=22, color=GREY_B).to_corner(UR, buff=0.45)
        with self.voiceover(
            "Directions mean something too. <bookmark mark='a'/> Step from France to Paris, then take the same step "
            f"from England. <bookmark mark='b'/> {land_say} Man is to king as woman is to: {mk[0]}, then {mk[1]}. "
            f"<bookmark mark='c'/> On {at['all']['n']} such questions built from the books, man and woman, dog and dogs, "
            f"walk and walked, the nearest word is right {100 * at['all']['acc']:.0f} percent of the time, out of ten "
            "thousand candidates. And of each category word's five nearest neighbours, animals, colours, numbers and so "
            f"on, {100 * pu['purity']:.0f} percent share its category, against {100 * pu['chance']:.0f} percent by "
            "chance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(dots[0]), FadeIn(labs[0]), FadeIn(dots[2]), FadeIn(labs[2]))
            vo.wait_until("a")
            self.play(FadeIn(dots[1]), FadeIn(labs[1]), GrowArrow(step))
            self.play(TransformFromCopy(step, again), run_time=1.3)
            vo.wait_until("b")
            self.play(Create(land), FadeIn(dots[3]), FadeIn(labs[3]), FadeIn(res))
            self.play(FadeIn(k2))
            vo.wait_until("c")
            self.play(FadeIn(score))
        self.wait(0.3)
        self.clear_scene()
