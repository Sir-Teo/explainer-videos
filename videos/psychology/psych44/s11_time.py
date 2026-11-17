from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403
from videos.psychology.psych44.diagrams import arrow, node


class Time(VoiceoverScene):
    def construct(self):
        self.card()
        self.growth()
        self.panel()
        self.within()

    def card(self):
        card = chapter_card(10, r"Latent variables over time", r"Who changes, \ and does one change drive another?",
                            lit={2015: r"Hamaker et al."}, part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter ten. Latent variables over time."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def growth(self):
        head = heading(r"Growth curves")
        I, S = node(r"start", MODEL, latent=True, r=0.5), node(r"slope", GOOD, latent=True, r=0.5)
        I.move_to([-4.8, 1.2, 0])
        S.move_to([-1.8, 1.2, 0])
        ys = VGroup(*[node(f"t{t}", GREY_A, r=0.3) for t in range(4)]).arrange(RIGHT, buff=0.45).move_to([-3.3, -1.0, 0])
        ai = VGroup(*[arrow(I, y, color=MODEL) for y in ys])
        as_ = VGroup(*[arrow(S, y, color=GOOD, text=str(t)) for t, y in enumerate(ys)])
        rows = rows_of([
            (r"two latent variables per person: \ where they start, \ and how fast they change", WHITE),
            (r"the loadings are fixed, \ not estimated: \ 1, 1, 1, 1 for the start; \ 0, 1, 2, 3 for the slope", MODEL),
            (r"the variance of the slope says whether people differ in change; \ its correlation with the start, \ "
             r"whether the high fall back or pull ahead", GOOD),
            (r"the same model as the mixed model of Part 31's growth curves, \ written as a diagram", PERSON),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "Measure the same people four times. <bookmark mark='a'/> A growth-curve model gives each person two latent "
            "variables: where they start, and how fast they change. <bookmark mark='b'/> The loadings are fixed, not "
            "estimated: one, one, one, one for the start, and zero, one, two, three for the slope. "
            "<bookmark mark='c'/> The variance of the slope says whether people differ in how they change. Its "
            "correlation with the start says whether the high fall back or pull ahead. <bookmark mark='d'/> It's the "
            "same model as the mixed model behind Part 31's growth curves for children, written as a diagram."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(I, S, ys)))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(ai))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(as_))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def panel(self):
        head = heading(r"The cross-lagged panel")
        xs = VGroup(*[node(f"x{t + 1}", PERSON, r=0.3) for t in range(3)]).arrange(RIGHT, buff=1.4)
        ys = VGroup(*[node(f"y{t + 1}", SYMP, r=0.3) for t in range(3)]).arrange(RIGHT, buff=1.4)
        grid = VGroup(xs, ys).arrange(DOWN, buff=1.4).move_to([-3.3, 0.2, 0])
        auto = VGroup(*[arrow(a, b, color=GREY_A) for g in (xs, ys) for a, b in zip(g[:-1], g[1:])])
        cross = VGroup(*[arrow(xs[t], ys[t + 1], color=AUTH) for t in range(2)],
                       *[arrow(ys[t], xs[t + 1], color=AUTH) for t in range(2)])
        rows = rows_of([
            (r"two traits measured at three waves, \ say, \ loneliness and low mood", WHITE),
            (r"each predicts itself next time (grey), \ and each predicts the other (red), \ controlling for the past", AUTH),
            (r"if x at one wave predicts y at the next better than y predicts x, \ x ``drives'' y: \ thousands of papers "
             r"read it so", PERSON),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "Now two traits, measured at three waves. Say, loneliness and low mood. <bookmark mark='a'/> The "
            "cross-lagged panel model lets each predict itself next time. <bookmark mark='b'/> And each predict the "
            "other, controlling for the past. <bookmark mark='c'/> If loneliness at one wave predicts low mood at the "
            "next, it is read as a driver. Thousands of papers read it that way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(auto))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(cross))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def within(self):
        d = load("panel")
        head = heading(r"Between people, \ or within?")
        A = axes([0.3, 2.7], [-0.04, 0.16], x_length=4.6, y_length=3.0, xticks=None, yticks=[0, 0.05, 0.1, 0.15],
                 yfmt=lambda v: f"{v:g}", ylabel=r"cross-lagged effect", center=[-3.4, 0.4, 0], font_size=13)
        b = bars(A.ax, [1, 2], [d["clpm"], d["within"]], [AUTH, GOOD], width=0.6)
        eb = VGroup(*[Line(A.ax.c2p(x, v - 1.96 * s), A.ax.c2p(x, v + 1.96 * s), color=WHITE, stroke_width=2)
                      for x, v, s in ((1, d["clpm"], d["clpm_se"]), (2, d["within"], d["within_se"]))])
        names = VGroup(*[wrapped_label(t, 2.0, 12, c).next_to(A.ax.c2p(i + 1, -0.04), DOWN, buff=0.12) for i, (t, c) in
                         enumerate(((r"cross-lagged panel", AUTH), (r"within each person", GOOD)))])
        rows = rows_of([
            (rf"Psyche: \ {num(d['n'])} people, \ {d['waves']} waves; \ stable differences in the two traits, \ "
             rf"correlated {d['trait_r']}, \ and no within-person effect of one on the other at all", WHITE),
            (rf"the cross-lagged panel finds one: \ {d['clpm']:.2f}, \ about {d['clpm'] / d['clpm_se']:.0f} standard "
             rf"errors from zero", AUTH),
            (rf"within each person, \ the effect is {d['within']:.2f}: \ none", GOOD),
            (r"Hamaker, \ Kuiper and Grasman, \ 2015: \ the random-intercept model separates the stable person from "
             r"the wave-to-wave change; \ the cross-lag is about change", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"stable traits, \ no cross effects, \ simulated")
        tag2 = published_tag(r"Hamaker, Kuiper \& Grasman (2015)").next_to(tag, UP, buff=0.1, aligned_edge=RIGHT)
        with self.voiceover(
            "Here is the catch. <bookmark mark='a'/> Psyche makes two thousand people, measured four times. They differ "
            "stably in the two traits, and the stable parts correlate. But within any one person, neither trait does "
            "anything to the other. <bookmark mark='b'/> The cross-lagged panel finds an effect anyway, about eleven "
            "standard errors from zero, because the past score is a noisy stand-in for the stable trait. "
            "<bookmark mark='c'/> Within each person, the effect is nothing. <bookmark mark='d'/> Ellen Hamaker, Rebecca "
            "Kuiper and Raoul Grasman made the point in 2015. A random-intercept model separates the stable person "
            "from the wave-to-wave change, and a claim about one trait driving another is a claim about change."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]), FadeIn(eb[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]), FadeIn(eb[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
