from __future__ import annotations

import math

import numpy as np

from explainer.cs import *  # noqa: F403
from videos.cs.cs2.common import COST, CTRL, DATA, FUNC, HEAD, INF, NO, PART, YES, fmt, load


def door(label_txt: str, color=GREY_B) -> VGroup:
    r = RoundedRectangle(width=1.1, height=1.7, corner_radius=0.08, stroke_color=color, stroke_width=3,
                         fill_color="#1B2130", fill_opacity=1)
    t = MathTex(label_txt, font_size=40, color=color).move_to(r)
    return VGroup(r, t)


class Chance(VoiceoverScene):
    def construct(self):
        self.card()
        self.monty()
        self.bayes()
        self.linearity()
        self.bounds()

    def card(self):
        card = chapter_card(13, r"Chance", r"How do you reason precisely about what is likely?", part=PART)
        with self.voiceover("Chapter thirteen. Chance."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def monty(self):
        d = load("chance")
        head = label(r"Three doors", font_size=38).to_edge(UP, buff=0.35)
        doors = VGroup(door("1"), door("2"), door("3")).arrange(RIGHT, buff=0.4).move_to(LEFT * 4.0 + UP * 0.6)
        pick = Triangle(color=DATA, fill_opacity=1, stroke_width=0).scale(0.15).rotate(PI).next_to(doors[0], UP, buff=0.15)
        goat = label(r"goat", font_size=24, color=NO).move_to(doors[2]).shift(DOWN * 0.55)
        rules = VGroup(*[label(t, font_size=24, color=GREY_A) for t in (
            r"a car behind one door; \ you pick one",
            r"the host, who knows, opens another, \ always a goat",
            r"stay, \ or switch?",
        )]).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(doors, DOWN, buff=0.4)
        T = d["T"]
        stay, sw = np.asarray(d["stay"]), np.asarray(d["switch"])
        ax = Axes(x_range=[0, T, 1000], y_range=[0, 1, 0.25], x_length=6.0, y_length=4.0, tips=False,
                  axis_config={"color": GREY_C, "font_size": 18},
                  x_axis_config={"numbers_to_include": [1000, 2000, 3000]},
                  y_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1.0]}).move_to(RIGHT * 3.4 + DOWN * 0.2)
        xs = np.arange(len(stay)) * 10 + 1
        ps = VMobject(color=NO, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, stay)])
        pw = VMobject(color=YES, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, sw)])
        ls = label(rf"stay: \ ${d['stay_final']:.3f}$", font_size=26, color=NO).next_to(ax.c2p(T, stay[-1]), RIGHT,
                                                                                         buff=0.1)
        lw = label(rf"switch: \ ${d['switch_final']:.3f}$", font_size=26, color=YES).next_to(ax.c2p(T, sw[-1]), RIGHT,
                                                                                              buff=0.1)
        VGroup(ls, lw).shift(LEFT * 1.6 + UP * 0.25)
        xl = note(rf"${fmt(T)}$ games, simulated: \ the fraction won so far", font_size=20).next_to(ax, DOWN, buff=0.15)
        why = label(r"switching wins exactly when your first pick was wrong: \ $2/3$", font_size=26,
                    color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Probability is counting, divided by counting, and it is where intuition fails most reliably. "
            "<bookmark mark='a'/> A game show. A car is behind one of three doors, goats behind the others. You pick a "
            "door. The host, who knows where the car is, opens a different door, always showing a goat, and offers you "
            "the chance to switch. <bookmark mark='b'/> Most people say it cannot matter: two doors left, fifty-fifty. "
            "Simulate three thousand games. Staying wins about a third of the time. Switching wins about two thirds. "
            "<bookmark mark='c'/> The reason: switching wins exactly when your first pick was wrong, and it was wrong "
            "two times in three. The host's choice gave you information, because it was not random. Whenever a "
            "probability argument feels slippery, list the outcomes, or simulate."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(doors), FadeIn(rules[0]))
            self.play(FadeIn(pick), FadeIn(rules[1]))
            self.play(doors[2][0].animate.set_fill(NO, 0.25), FadeIn(goat), FadeIn(rules[2]))
            vo.wait_until("b")
            self.play(Create(ax), FadeIn(xl))
            self.play(Create(ps), Create(pw), run_time=3.0, rate_func=linear)
            self.play(FadeIn(ls), FadeIn(lw))
            vo.wait_until("c")
            self.play(FadeIn(why))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bayes(self):
        d = load("chance")
        f = d["per10000"]
        head = label(r"Conditional probability, \ and Bayes", font_size=38).to_edge(UP, buff=0.35)
        setup = label(r"a disease affects $1\%$; \ the test catches $99\%$ of cases, \ but flags $5\%$ of the healthy",
                      font_size=26, color=GREY_A).next_to(head, DOWN, buff=0.3)
        # an area diagram of 10,000 people
        W, H = 7.0, 3.6
        o = np.array([-4.6, -2.6, 0])
        sick_w = W * 0.01 * 4  # exaggerated width so the sick column is visible
        well_w = W - sick_w
        sick = Rectangle(width=sick_w, height=H, stroke_width=0, fill_color=NO, fill_opacity=0.25).move_to(
            o + np.array([sick_w / 2, H / 2, 0]))
        well = Rectangle(width=well_w, height=H, stroke_width=0, fill_color=DATA, fill_opacity=0.15).move_to(
            o + np.array([sick_w + well_w / 2, H / 2, 0]))
        sick_pos = Rectangle(width=sick_w, height=H * 0.99, stroke_width=0, fill_color=NO, fill_opacity=0.8).move_to(
            o + np.array([sick_w / 2, H * 0.99 / 2, 0]))
        well_pos = Rectangle(width=well_w, height=H * 0.05 * 3, stroke_width=0, fill_color=HEAD,
                             fill_opacity=0.8).move_to(o + np.array([sick_w + well_w / 2, H * 0.15 / 2, 0]))
        l1 = label(rf"sick: \ {f['sick']}", font_size=22, color=NO).next_to(sick, UP, buff=0.1)
        l2 = label(rf"healthy: \ ${fmt(f['well'])}$", font_size=22, color=DATA).next_to(well, UP, buff=0.1)
        l3 = label(rf"{f['sick_pos']} test positive", font_size=22, color=NO).next_to(sick_pos, LEFT, buff=0.1)
        l4 = label(rf"{f['well_pos']} test positive", font_size=22, color=HEAD).move_to(well_pos)
        cap = note(r"out of $10{,}000$ people \ (column widths exaggerated, heights to scale; \ the yellow strip "
                   r"three times taller)", font_size=18).next_to(VGroup(sick, well), DOWN, buff=0.12)
        q = MathTex(r"P(\text{sick} \mid +) = \frac{99}{99 + 495} = \frac16", font_size=40, color=YES).move_to(
            RIGHT * 4.4 + UP * 0.6)
        rule = MathTex(r"P(A \mid B) = \frac{P(B \mid A)\, P(A)}{P(B)}", font_size=36, color=CTRL).next_to(q, DOWN,
                                                                                                    buff=0.5)
        rl = note(r"Bayes' rule: \ the same count, \ in symbols", font_size=22).next_to(rule, DOWN, buff=0.15)
        with self.voiceover(
            "Conditional probability is the chance of one thing given that another happened, and it is the other half "
            "of the Monty Hall surprise. <bookmark mark='a'/> A disease affects one person in a hundred. A test catches "
            "ninety-nine percent of cases, but also flags five percent of healthy people. You test positive. How "
            "worried should you be? <bookmark mark='b'/> Count ten thousand people. A hundred are sick, and ninety-nine "
            "of them test positive. Nine thousand nine hundred are healthy, and four hundred and ninety-five of them "
            "test positive too. <bookmark mark='c'/> Of the five hundred and ninety-four positives, only ninety-nine "
            "are sick: one in six. Bayes' rule is this count written in symbols. When the thing you are looking for is "
            "rare, false alarms swamp it, which is the daily problem of every spam filter, fraud detector and "
            "intrusion alarm."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(setup))
            vo.wait_until("b")
            self.play(FadeIn(sick), FadeIn(well), FadeIn(l1), FadeIn(l2), FadeIn(cap))
            self.play(GrowFromEdge(sick_pos, DOWN), GrowFromEdge(well_pos, DOWN), FadeIn(l3), FadeIn(l4))
            vo.wait_until("c")
            self.play(Write(q))
            self.play(FadeIn(rule), FadeIn(rl))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def linearity(self):
        d = load("derange")
        head = label(r"Linearity of expectation", font_size=38).to_edge(UP, buff=0.35)
        q = label(r"$n$ hats handed back at random: \ how many people get their own, \ on average?", font_size=28,
                  color=GREY_A).next_to(head, DOWN, buff=0.35)
        ind = MathTex(r"X = X_1 + X_2 + \cdots + X_n,\qquad X_i = \begin{cases} 1 & \text{person } i \text{ gets their "
                      r"own} \\ 0 & \text{otherwise} \end{cases}", font_size=32, color=CTRL).next_to(q, DOWN, buff=0.4)
        e = MathTex(r"\mathbb{E}[X] = \sum_i \mathbb{E}[X_i] = n \cdot \frac1n = 1", font_size=40, color=YES).next_to(
            ind, DOWN, buff=0.45)
        warn = note(r"the $X_i$ are not independent; \ linearity does not care", font_size=22).next_to(e, DOWN,
                                                                                                  buff=0.15)
        sims = d["sims"]
        rows = VGroup(*[label(rf"$n = {s['n']}$: \ average ${s['mean']:.3f}$", font_size=26, color=GREY_A)
                        for s in sims]).arrange(RIGHT, buff=0.6).next_to(warn, DOWN, buff=0.45)
        # the distribution of fixed points against Poisson(1)
        s52 = sims[2]
        ax = Axes(x_range=[-0.5, 6.5, 1], y_range=[0, 0.4, 0.1], x_length=5.0, y_length=1.6, tips=False,
                  axis_config={"color": GREY_C, "font_size": 16},
                  x_axis_config={"numbers_to_include": list(range(7))}).to_edge(DOWN, buff=0.35)
        bars = VGroup(*[Rectangle(width=0.32, height=max(ax.y_length * h / 0.4, 0.005), stroke_width=0,
                                  fill_color=DATA, fill_opacity=0.85).move_to(ax.c2p(k - 0.15, 0), aligned_edge=DOWN)
                        for k, h in enumerate(s52["hist"][:7])])
        pbars = VGroup(*[Rectangle(width=0.32, height=max(ax.y_length * h / 0.4, 0.005), stroke_width=0,
                                   fill_color=HEAD, fill_opacity=0.6).move_to(ax.c2p(k + 0.15, 0), aligned_edge=DOWN)
                         for k, h in enumerate(d["poisson"][:7])])
        al = note(r"52 people, \ simulated \ (blue) \\ against $e^{-1}/k!$ \ (yellow)", font_size=20).next_to(
            ax, LEFT, buff=0.4)
        with self.voiceover(
            "The most useful fact in discrete probability is almost too simple to believe. <bookmark mark='a'/> Back to "
            "the hats. On average, how many people get their own? <bookmark mark='b'/> Write the count as a sum of "
            "indicators: X i is one if person i gets their own hat, and zero otherwise. Each person has a one in n "
            "chance. <bookmark mark='c'/> The expectation of a sum is the sum of the expectations: n times one over n. "
            "One. For every n. <bookmark mark='d'/> The indicators are tangled together, since if one person has the "
            "wrong hat it changes the odds for the others, but linearity holds anyway, with no independence needed. "
            "<bookmark mark='e'/> The simulations agree, and the whole distribution of fixed points is close to the "
            "Poisson law with mean one. Part 16 uses exactly this trick, indicators and linearity, to show that "
            "quicksort makes about two n times the natural logarithm of n comparisons on average."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Write(ind))
            vo.wait_until("c")
            self.play(Write(e))
            vo.wait_until("d")
            self.play(FadeIn(warn))
            vo.wait_until("e")
            self.play(FadeIn(rows, lag_ratio=0.2))
            self.play(Create(ax), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.1),
                      LaggedStart(*[GrowFromEdge(b, DOWN) for b in pbars], lag_ratio=0.1), FadeIn(al))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def bounds(self):
        d = load("chance")
        c = d["coins"]
        head = label(r"How unlikely? \ Three bounds", font_size=38).to_edge(UP, buff=0.35)
        q = label(r"100 fair coins: \ what is the chance of $75$ or more heads?", font_size=28,
                  color=GREY_A).next_to(head, DOWN, buff=0.35)
        rows = VGroup()
        for name, f_, v, col in ((r"Markov", r"P(X \ge a) \le \mathbb{E}X / a", c["markov"], NO),
                                 (r"Chebyshev", r"P(|X - \mu| \ge t) \le \sigma^2 / t^2", c["chebyshev"], HEAD),
                                 (r"exact", r"\textstyle\sum_{k \ge 75} \binom{100}{k} / 2^{100}", c["exact"], YES)):
            rows.add(VGroup(label(name, font_size=28, color=col), MathTex(f_, font_size=30, color=GREY_A),
                            MathTex(f"{v:.3g}".replace("e-07", r"\times 10^{-7}"), font_size=34, color=col)))
        for i, r in enumerate(rows):
            r[0].move_to([-5.0, 0.8 - 0.8 * i, 0], aligned_edge=LEFT)
            r[1].move_to([-0.8, 0.8 - 0.8 * i, 0])
            r[2].move_to([3.6, 0.8 - 0.8 * i, 0], aligned_edge=LEFT)
        need = note(r"Markov needs only the mean; \ Chebyshev also the variance; \ Part 16 adds Chernoff, \ which is "
                    r"exponentially sharper", font_size=22).next_to(rows, DOWN, buff=0.35)
        bd = d["birthday"]
        b23 = [b for b in bd if b["k"] == 23][0]
        union = VGroup(MathTex(r"P(A_1 \cup \cdots \cup A_m) \le \sum P(A_i)", font_size=32, color=CTRL),
                       label(rf"23 people, \ a shared birthday: \ union bound \ ${b23['union']:.3f}$, \ exact "
                             rf"${b23['exact']:.3f}$", font_size=26, color=GREY_A)).arrange(DOWN, buff=0.2).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "Often we cannot compute a probability exactly, but we can bound it, and the bound is what a guarantee is "
            "made of. <bookmark mark='a'/> Toss a hundred fair coins. What is the chance of seventy-five heads or more? "
            "<bookmark mark='b'/> Markov's inequality uses only the average, fifty: the chance is at most fifty over "
            "seventy-five, two thirds. True, and nearly useless. <bookmark mark='c'/> Chebyshev's inequality also uses "
            "the spread, the variance, twenty-five: being twenty-five away from the mean has chance at most twenty-five "
            "over six hundred and twenty-five, four percent. <bookmark mark='d'/> The exact answer is about three in ten "
            "million. Each extra fact about the distribution buys a much sharper bound, and Part 16 adds the Chernoff "
            "bound, which is close to the truth. <bookmark mark='e'/> And the crudest bound of all: the chance that any "
            "of several bad things happens is at most the sum of their chances. With twenty-three people, the "
            "chance that two share a birthday is at most two hundred and fifty-three pairs over three hundred and "
            "sixty-five, sixty-nine percent; the truth is fifty-one. Part 17 uses this to size hash tables."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.1))
            self.play(FadeIn(need))
            vo.wait_until("e")
            self.play(FadeIn(union))
        self.wait(0.3)
        self.clear_scene()
