from __future__ import annotations

import numpy as np

from videos.stats.stats43.common import *  # noqa: F403


class BorelCantelli(VoiceoverScene):
    def construct(self):
        self.card()
        self.lemmas()
        self.runs()
        self.monkey()
        self.zero_one()
        self.hewitt()

    def card(self):
        card = chapter_card(5, r"Borel--Cantelli and the 0--1 laws", r"What happens infinitely often?", lit=(1909,), part=PART)
        with self.voiceover("Chapter five. Borel–Cantelli and the zero–one laws: what happens infinitely often?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def lemmas(self):
        rows = [
            cmath(r"\{A_n \text{ i.o.}\}", r"=", r"\textstyle\bigcap_{n} \bigcup_{m \ge n} A_m: \ \text{infinitely many } A_m \text{ happen}", font_size=32),
            cmath(r"\text{BC I}", r":", r"\textstyle\sum P(A_n) < \infty \Rightarrow P(A_n \text{ i.o.}) = 0 \ \ \big(P \le \sum_{m \ge n} P(A_m) \to 0\big)", font_size=30),
            cmath(r"\text{BC II}", r":", r"A_n \text{ independent}, \ \textstyle\sum P(A_n) = \infty \Rightarrow P(A_n \text{ i.o.}) = 1", font_size=30),
            cmath(r"\text{proof}", r":", r"P\big(\textstyle\bigcap_{m \ge n} A_m^c\big) = \prod (1 - P(A_m)) \le e^{-\sum_{m \ge n} P(A_m)} = 0", font_size=30),
        ]
        rows[1][-1].set_color(GOODC)
        rows[2][-1].set_color(S.ACCENT)
        whys = [why(r"the limsup of events"), why(r"no independence needed"), why(r"the converse"), why(r"$1 - x \le e^{-x}$")]
        with self.voiceover(
            "<bookmark mark='a'/> An event happens infinitely often if, however far out you start, it happens again: the "
            "intersection over n of the unions from n on. That event is in the sigma-algebra, so it has a probability. "
            "<bookmark mark='b'/> The first Borel–Cantelli lemma: if the probabilities have a finite sum, the event happens "
            "only finitely often, almost surely. The proof is one line: the probability of a union from n on is at most "
            "the tail of a convergent series. <bookmark mark='c'/> The second lemma is a converse, for independent events: "
            "if the probabilities sum to infinity, the event happens infinitely often, almost surely. <bookmark mark='d'/> "
            "Its proof: the chance that none happens from n on is a product of one minus each probability, at most e to the "
            "minus their sum, which is zero."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def runs(self):
        d = load("runs")
        rows_ = d["rows"]
        A = axes([4, 20], [0, 24], x_length=7.4, y_length=4.4, xlabel=r"$\log_2 n$ \ (tosses)", ylabel=r"the longest run of heads",
                 xticks=[4, 8, 12, 16, 20], yticks=[0, 8, 16, 24], center=[-2.5, 0.2, 0])
        ax = A.ax
        lx = [r["log2"] for r in rows_]
        bnd = band(ax, np.array(lx), np.array([r["lo"] for r in rows_]), np.array([r["hi"] for r in rows_]), LAWC, 0.25)
        mean = VGroup(polyline(ax, lx, [r["mean"] for r in rows_], LAWC, 3),
                      *[Dot(ax.c2p(a, r["mean"]), radius=0.06, color=LAWC) for a, r in zip(lx, rows_)])
        diag = DashedLine(ax.c2p(4, 4), ax.c2p(20, 20), color=LIMC, stroke_width=2.5)
        last = rows_[-1]
        side = fit_rows(VGroup(
            label(r"$A_n$: \ a run of $r_n$ heads starts at toss $n$; \ $P(A_n) = 2^{-r_n}$", font_size=22),
            label(r"$r_n = (1 + \varepsilon)\log_2 n$: \ $\sum n^{-1-\varepsilon} < \infty$: \ finitely often", font_size=22, color=GOODC),
            label(r"$r_n = (1 - \varepsilon)\log_2 n$: \ the sum diverges: \ infinitely often", font_size=22, color=S.ACCENT),
            label(rf"so the longest run $\approx \log_2 n$: \ {last['mean']:.1f} in $2^{{20}}$ tosses", font_size=22, color=LAWC),
            label(r"Erd\H{o}s \& R\'enyi (1970)", font_size=20, color=GREY_B),
        ), 4.6, 0.42, [4.45, 0.4, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> Here is the pair at work. Toss a fair coin n times: how long is the longest run of heads? "
            f"Let A n be the event that a run of length r n starts at toss n; it has probability two to the minus r n. "
            f"<bookmark mark='b'/> If r n is a little more than log base two of n, the probabilities sum like one over n to "
            f"the one plus epsilon, which converges, so such runs happen only finitely often. <bookmark mark='c'/> If r n is "
            f"a little less, the sum diverges, and an argument with independent blocks of tosses shows that such runs keep "
            f"happening. <bookmark mark='d'/> So the longest run grows like log base two of n, the gold line. Simulated coins "
            f"agree: about {say(last['mean'], 1)} in a million tosses, against twenty for log base two. <bookmark mark='e'/> "
            f"Paul Erdős and Alfréd Rényi proved it in 1970; it is also why a run of seven heads in a hundred tosses is no "
            f"evidence of a biased coin."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"simulated: 200 sequences at each $n$")))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), Create(diag))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(bnd), Create(mean), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def monkey(self):
        rows = fit_rows(VGroup(
            label(r"a monkey types forever, \ one of 27 keys at random each second", font_size=26),
            label(r"$A_k$: \ the $k$-th block of 9 keys spells \texttt{statistic}: \ $P(A_k) = 27^{-9} \approx 1.3 \times 10^{-13}$", font_size=26, color=GREY_A),
            label(r"the blocks are independent and $\sum_k P(A_k) = \infty$", font_size=26, color=S.ACCENT),
            label(r"BC II: \ the word appears infinitely often, \ with probability one", font_size=26, color=GOODC),
            label(r"(expected wait for the first: \ about $27^9$ blocks of nine seconds, \ some 2.2 million years)", font_size=22, color=GREY_B),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Borel's own illustration was a typing monkey. Give it twenty-seven keys and let it type one "
            "at random each second, forever. <bookmark mark='b'/> Cut the stream into blocks of nine keys; each block spells "
            "the word statistic with probability twenty-seven to the minus nine, about one in eight trillion. <bookmark "
            "mark='c'/> The blocks are independent and the probabilities sum to infinity, <bookmark mark='d'/> so by the "
            "second lemma the word appears infinitely often, with probability one. <bookmark mark='e'/> The first appearance, "
            "block by block, takes on average some two million years. Almost sure is not soon."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def zero_one(self):
        rows = [
            cmath(r"\mathcal T", r"=", r"\textstyle\bigcap_n \sigma(X_n, X_{n+1}, \ldots): \ \text{events no finite set of } X\text{'s can change}", font_size=28),
            cmath(r"\text{Kolmogorov}", r":", r"X_1, X_2, \ldots \text{ independent} \ \Rightarrow \ P(A) \in \{0, 1\} \ \ \forall A \in \mathcal T", font_size=30),
            cmath(r"\text{proof}", r":", r"A \in \mathcal T \Rightarrow A \perp A \Rightarrow P(A) = P(A)^2", font_size=32),
            cmath(r"\text{in } \mathcal T", r":", r"\{\textstyle\sum X_n \text{ converges}\}, \ \{\limsup \bar X_n \le c\}, \ \{X_n > 1 \text{ i.o.}\}", font_size=30),
        ]
        rows[1][-1].set_color(S.ACCENT)
        whys = [why(r"the tail $\sigma$-algebra"), why(r"the 0--1 law"), why(r"independent of itself"), why(r"so these are 0 or 1")]
        with self.voiceover(
            "<bookmark mark='a'/> The tail sigma-algebra holds the events that no finite number of the variables can "
            "affect: what happens from n on, for every n. <bookmark mark='b'/> Kolmogorov's zero–one law: for independent "
            "variables, every tail event has probability zero or one. <bookmark mark='c'/> The proof is a gem: a tail event "
            "is independent of the first n variables for every n, so, by pi–lambda, of all of them; but it is determined by "
            "all of them, so it is independent of itself, and its probability equals its own square. <bookmark mark='d'/> "
            "So whether a random series converges, whether running means stay below a level, whether something happens "
            "infinitely often: each is either almost certain or almost impossible. The law never says which; the next "
            "chapter does."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def hewitt(self):
        rows = fit_rows(VGroup(
            label(r"Hewitt--Savage (1955): \ i.i.d.\ $X_n$, \ events unchanged by permuting finitely many: \ 0 or 1", font_size=26),
            label(r"$\{S_n = 0 \text{ infinitely often}\}$ for a random walk: \ not a tail event, \ but symmetric", font_size=26, color=GREY_A),
            label(r"so a simple random walk returns to zero infinitely often \ or only finitely often, \ surely", font_size=26, color=S.ACCENT),
            label(r"in one dimension: \ infinitely often \ (P\'olya 1921: \ also in two, \ not in three)", font_size=26, color=GOODC),
        ), 12.4, 0.6, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Edwin Hewitt and Leonard Savage extended the law in 1955: for independent and identically "
            "distributed variables, any event unchanged by permuting finitely many of them has probability zero or one. "
            "<bookmark mark='b'/> The event that a random walk returns to zero infinitely often is not a tail event, since "
            "changing the first step changes every partial sum, but it is symmetric. <bookmark mark='c'/> So the walk "
            "returns infinitely often almost surely, or only finitely often almost surely. <bookmark mark='d'/> George "
            "Pólya showed in 1921 which: a walk on the line or the plane returns forever; in three dimensions it eventually "
            "wanders off. Part forty-four takes walks further."
        ) as vo:
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
