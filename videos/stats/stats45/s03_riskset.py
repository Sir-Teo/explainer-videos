from __future__ import annotations

import numpy as np

from videos.stats.stats45.common import *  # noqa: F403


class RiskSets(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.points()
        self.bayes()
        self.minimax()
        self.theorem()

    def card(self):
        card = chapter_card(2, r"Risk sets", r"A whole decision problem in one picture", part=PART)
        with self.voiceover("Chapter two. Risk sets: a whole decision problem in one picture."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def problem(self):
        d = load("decision")
        px = np.asarray(d["px"])
        tab = table_rows([[r"heads $x$", "0", "1", "2", "3"],
                          [r"fair: \ $p = 0.5$"] + [f"{v:.3f}" for v in px[0]],
                          [r"biased: \ $p = 0.8$"] + [f"{v:.3f}" for v in px[1]]], font_size=28, col_buff=0.7, row_buff=0.28,
                         colors=[GREY_A, MLEC, INADC]).move_to([0, 1.7, 0])
        loss = table_rows([[r"loss", r"say fair", r"say biased"], [r"fair", "0", "1"], [r"biased", "2", "0"]], font_size=28,
                          col_buff=0.8, row_buff=0.25, colors=[GREY_A, MLEC, INADC]).move_to([-3.2, -1.3, 0])
        side = fit_rows(VGroup(
            label(r"a rule: \ an answer for each $x \in \{0, 1, 2, 3\}$", font_size=26),
            label(r"$2^4 = 16$ non-randomized rules", font_size=26, color=S.ACCENT),
            label(r"each has two risks: \ $R(\text{fair}, \delta)$ and $R(\text{biased}, \delta)$", font_size=26, color=MMC),
        ), 6.0, 0.35, [3.2, -1.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> A problem small enough to see whole. A coin is either fair or biased, landing heads with "
            "probability point eight. We toss it three times and count the heads; here are the chances of each count under "
            "both states. <bookmark mark='b'/> We must say fair or biased. Calling a fair coin biased costs one; missing a "
            "biased coin costs two. <bookmark mark='c'/> A rule assigns an answer to each of the four possible counts, "
            "<bookmark mark='d'/> so there are sixteen rules, <bookmark mark='e'/> and each has just two risks, one for each "
            "state of nature: a point in the plane."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(loss))
            vo.wait_until("c")
            self.play(FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(side[1]))
            vo.wait_until("e")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def _axes(self):
        A = axes([0, 1.05], [0, 2.1], x_length=6.6, y_length=5.0, xlabel=r"$R(\text{fair}, \delta)$", ylabel=r"$R(\text{biased}, \delta)$",
                 xticks=[0, 0.25, 0.5, 0.75, 1], yticks=[0, 0.5, 1, 1.5, 2], center=[-2.7, 0.0, 0])
        return A

    def points(self):
        d = load("decision")
        A = self._axes()
        rs = RiskSet(A.ax, d["R"])
        dots = rs.rule_dots(MLEC, radius=0.08)
        hull = rs.hull(MLEC, 0.18)
        low = rs.lower(d["lower"], ADMC, 6)
        adm = rs.rule_dots(highlight=d["admissible"], hcolor=ADMC, radius=0.1)
        adm = VGroup(*[adm[i] for i in d["admissible"]])
        side = fit_rows(VGroup(
            label(r"blue: \ the 16 rules", font_size=22, color=MLEC),
            label(r"shaded: \ randomized rules, \ the convex hull", font_size=22, color=GREY_A),
            label(r"green: \ the lower-left edge, \ the admissible rules", font_size=22, color=ADMC),
            label(r"its corners: \ ``say biased if $x \ge c$'', \ $c = 0, \ldots, 4$", font_size=22, color=ADMC),
            label(r"up and to the right: \ dominated", font_size=22, color=INADC),
        ), 4.4, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Here are the sixteen rules as points: across, the risk when the coin is fair; up, the risk "
            "when it is biased. The rule that always says fair sits at the top left; always biased, at the bottom right. "
            "<bookmark mark='b'/> Flip a coin to choose between two rules, and you get any point on the segment between "
            "them, so the randomized rules fill the convex hull. <bookmark mark='c'/> Smaller is better in both directions, "
            "so only the lower-left edge matters: every point above or to the right of it is dominated by a point on it. "
            "<bookmark mark='d'/> Its corners are the five threshold rules: say biased when the number of heads is at least "
            "c. <bookmark mark='e'/> Rules such as saying biased after zero heads but fair after three sit far inside, "
            "dominated many times over."
        ) as vo:
            self.play(FadeIn(A), FadeIn(exact_tag(r"exact: \ binomial probabilities")))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.08), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(hull), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(low), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(adm), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def bayes(self):
        d = load("decision")
        A = self._axes()
        rs = RiskSet(A.ax, d["R"])
        base = VGroup(rs.hull(MLEC, 0.15), rs.rule_dots(MLEC, radius=0.07), rs.lower(d["lower"], ADMC, 5))
        cols = {"0.25": S.ALT, "0.5": BAYESC, "0.75": MMC}
        lines, hits = {}, {}
        for k, c in cols.items():
            b = d["bayes"][k]
            lines[k] = rs.bayes_line(float(k), b["risk"], c, 3)
            hits[k] = Dot(A.ax.c2p(*b["point"]), radius=0.13, color=c)
        side = fit_rows(VGroup(
            label(r"prior $\pi$ on fair: \ risk $\pi R_1 + (1 - \pi) R_2$", font_size=22),
            label(r"level sets: \ lines of slope $-\pi/(1 - \pi)$", font_size=22, color=GREY_A),
            label(r"slide the line down until it touches the set", font_size=22, color=S.ACCENT),
            label(r"$\pi = 0.25, \ 0.5, \ 0.75$: \ thresholds $c = 1, \ 2, \ 3$", font_size=22, color=BAYESC),
            label(r"Bayes rules: \ likelihood-ratio thresholds", font_size=22, color=ADMC),
        ), 4.4, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Now put a prior on the states: probability pi that the coin is fair. The Bayes risk of a "
            "rule is pi times its first risk plus one minus pi times its second. <bookmark mark='b'/> Rules with equal Bayes "
            "risk lie on a straight line, and changing the Bayes risk slides the line parallel to itself. <bookmark "
            "mark='c'/> So the Bayes rule is found by sliding the line down until it first touches the risk set: a "
            "supporting line. <bookmark mark='d'/> With a quarter on fair, it touches the threshold rule c equals one; with "
            "a half, c equals two; with three quarters, c equals three. <bookmark mark='e'/> Every Bayes rule here is a "
            "threshold on the number of heads, which is a threshold on the likelihood ratio, as Neyman and Pearson will "
            "explain in Part forty-six."
        ) as vo:
            self.play(FadeIn(A), FadeIn(base))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(lines["0.5"]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(hits["0.5"]), Create(lines["0.25"]), FadeIn(hits["0.25"]), Create(lines["0.75"]), FadeIn(hits["0.75"]),
                      FadeIn(side[3]), run_time=2.0)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def minimax(self):
        d = load("decision")
        A = self._axes()
        rs = RiskSet(A.ax, d["R"])
        base = VGroup(rs.hull(MLEC, 0.15), rs.rule_dots(MLEC, radius=0.07), rs.lower(d["lower"], ADMC, 5))
        diag = rs.diagonal(GREY_B, 2)
        v = d["minimax"]
        mm = Dot(A.ax.c2p(v, v), radius=0.14, color=MMC)
        sq = Polygon(A.ax.c2p(0, 0), A.ax.c2p(v, 0), A.ax.c2p(v, v), A.ax.c2p(0, v), stroke_color=MMC, stroke_width=2, fill_opacity=0)
        lf = d["least_favourable"]
        sup = rs.bayes_line(lf, v, MMC, 3, dashed=True)
        w = np.asarray(d["weights"])
        side = fit_rows(VGroup(
            label(r"minimax: \ the first square $[0, t]^2$ to touch", font_size=22),
            label(rf"on the diagonal: \ $R_1 = R_2 = {v:.3f}$", font_size=22, color=MMC),
            label(rf"mix $c = 3$ and $c = 2$ \ with weights {w[1]:.2f}, \ {w[3]:.2f}", font_size=22, color=MMC),
            label(rf"its slope: \ least favourable $\pi = {lf:.3f}$", font_size=22, color=S.ACCENT),
            label(r"minimax = Bayes for that prior", font_size=22, color=ADMC),
        ), 4.4, 0.42, [4.4, 0.3, 0])
        with self.voiceover(
            f"<bookmark mark='a'/> The minimax rule minimizes the larger of the two risks. Grow a square from the origin "
            f"until it first meets the risk set. <bookmark mark='b'/> It meets the lower edge on the diagonal, where the two "
            f"risks are equal, at {say(v, 3)}: an equalizer rule. <bookmark mark='c'/> That point lies between two corners, "
            f"so the minimax rule randomizes: it uses the threshold three about a quarter of the time and the threshold two "
            f"about three quarters of the time; in effect, with exactly two heads it flips a biased coin of its own. "
            f"<bookmark mark='d'/> The edge's supporting line there has a slope, and that slope is a prior: "
            f"{say(lf, 2)} on fair, the least favourable prior. <bookmark mark='e'/> The minimax rule is the Bayes rule for "
            f"the prior that makes the statistician's job hardest."
        ) as vo:
            self.play(FadeIn(A), FadeIn(base))
            vo.wait_until("a")
            self.play(Create(diag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(sq), FadeIn(mm), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Indicate(base[1][1], color=MMC), Indicate(base[1][3], color=MMC), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(sup), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def theorem(self):
        d = load("decision")
        rows = [
            cmath(r"\inf_\delta \sup_\theta R(\theta, \delta)", r"=", r"\sup_\pi \inf_\delta r(\pi, \delta)", font_size=34),
            cmath(r"\pi^* \text{ least favourable}", r":", r"\text{the prior attaining the sup}", font_size=32),
            cmath(r"\delta \text{ Bayes for } \pi, \ R \text{ constant}", r"\Rightarrow", r"\delta \text{ is minimax}", font_size=32),
            cmath(r"\text{here}", r":", rf"\text{{both sides}} = {d['minimax']:.4f}; \ \text{{the binomial's flat rule, \ the same way}}", font_size=30),
        ]
        rows[0][-1].set_color(MMC)
        rows[2][-1].set_color(ADMC)
        whys = [why(r"von Neumann (1928); \ Wald (1950)"), why(r"nature's best strategy"), why(r"the equalizer trick"), why(r"chapter 1, \ proved")]
        with self.voiceover(
            "<bookmark mark='a'/> What the picture shows is von Neumann's minimax theorem, which Wald extended to statistics: "
            "the best worst-case risk equals the largest Bayes risk that any prior can force. <bookmark mark='b'/> A prior "
            "attaining it is least favourable: nature's best strategy in the game. <bookmark mark='c'/> And it gives the "
            "practical recipe: a Bayes rule whose risk is constant is minimax, because its worst case equals its average, "
            "and no rule can beat that average everywhere. <bookmark mark='d'/> In our coin problem both sides equal the same "
            "number, and chapter one's flat binomial rule is minimax for exactly this reason: it is Bayes for a Beta prior "
            "and its risk is constant."
        ) as vo:
            step = ladder(self, rows, whys, keep=4, top=2.6, x=-0.9, buff=0.85, edge=6.9)
            for k, m_ in enumerate("abcd"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()
