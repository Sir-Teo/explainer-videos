from __future__ import annotations

import numpy as np

from videos.psychology.psych2.common import *  # noqa: F403

# the six designs, in the order of the film: (key, name, the study, why it is fooled)
DESIGNS = [
    ("testing", r"Testing", r"one group, tested before and after", r"the second test is easier than the first"),
    ("history", r"History", r"before and after, in a lab that changed its keyboards",
     r"something else happened in between"),
    ("maturation", r"Maturation", r"children, tested two years apart", r"people change on their own"),
    ("regression", r"Regression", r"the slowest at a quick screening, tested again",
     r"an extreme score is partly luck, and luck does not repeat"),
    ("selection", r"Selection", r"volunteers against everyone else", r"the groups differed before the game"),
    ("attrition", r"Attrition", r"randomized, but only finishers are counted", r"who drops out is not random"),
]


class Threats(VoiceoverScene):
    def construct(self):
        self.card()
        self.rail()
        self.regression()
        self.confound()
        self.sound()

    def card(self):
        card = chapter_card(4, r"Six ways to fool yourself", r"How many wrong designs find that a useless game "
                            r"works?", lit={1963: r"Campbell \& Stanley's threats to validity"}, part=PART,
                            scale=("group",), marr=("what",))
        with self.voiceover(
            "Chapter four. Six ways to fool yourself."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rail(self):
        d = load("threats")
        ds = d["designs"]
        head = heading(r"One useless game, six studies", font_size=34)
        rail = effect_rail(-50, 10, length=6.0, ticks=[-40, -30, -20, -10, 0, 10], font_size=20)
        rail.move_to([3.85, -3.05, 0])
        x0 = rail.x(0)
        zero = Line([x0, rail.axis.get_y() + 0.05, 0], [x0, 2.75, 0], color=TRUTH, stroke_width=3)
        zlab = label(r"the truth: \ 0", font_size=24, color=TRUTH).next_to(zero, UP, buff=0.06)
        names, details, marks = VGroup(), VGroup(), VGroup()
        for i, (key, name, study, why_) in enumerate(DESIGNS):
            y = 2.3 - 0.9 * i
            e = ds[key]
            nm = label(name, font_size=32, color=BIAS).move_to([-6.85, y, 0], aligned_edge=LEFT)
            t = VGroup(label(study, font_size=24, color=WHITE), label(why_, font_size=21, color=GREY_B))
            t.arrange(DOWN, aligned_edge=LEFT, buff=0.04).move_to([-4.6, y, 0], aligned_edge=LEFT)
            if t.get_right()[0] > 0.6:
                t.scale_to_fit_width(5.2).move_to([-4.6, y, 0], aligned_edge=LEFT)
            m = estimate_mark(rail, y, e["effect"], e["lo"], e["hi"], BIAS)
            v = label(rf"${e['effect']:.0f}$", font_size=30, color=BIAS).next_to(m, LEFT, buff=0.15)
            names.add(nm)
            details.add(t)
            marks.add(VGroup(m, v))
        head.to_edge(UP, buff=0.25)
        tag = simulated_tag(rf"simulated: the Pool, {d['n']} people a study; \ the game's true effect is zero")
        with self.voiceover(
            "The single group measured twice is one of a family. In 1963 Donald Campbell and Julian Stanley "
            "listed the ways a study can find an effect that isn't there, and gave them names that are still "
            "used. Let's run each of them on the Pool, with the same useless game. The green line is the truth: "
            "zero. <bookmark mark='a'/> Testing we've seen. The second test is easier than the first. "
            f"{abs(ds['testing']['effect']):.0f} milliseconds. <bookmark mark='b'/> History. Between the two "
            "tests, something else happened to everybody. Here, the laboratory bought faster keyboards. "
            "<bookmark mark='c'/> Maturation. The subjects were changing anyway. Test children two years apart, "
            f"and the game appears to take {abs(ds['maturation']['effect']):.0f} milliseconds off their "
            "reactions. They grew. <bookmark mark='d'/> Regression, which gets a picture of its own in a moment. "
            "<bookmark mark='e'/> Selection. Compare people who chose to play with people who didn't. In the "
            "Pool, the ones who sign up for things are younger and quicker to begin with. "
            f"{abs(ds['selection']['effect']):.0f} milliseconds, and the game hasn't been opened yet. "
            "<bookmark mark='f'/> And attrition. Even a proper experiment goes wrong if people leave it "
            "unevenly. Here the slowest players got bored and quit, and only the finishers were measured. "
            "<bookmark mark='g'/> Six studies, six effects, every interval clear of zero, and nothing there."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rail), FadeIn(tag))
            ghosts = VGroup(*[nm.copy().set_color(GREY_C) for nm in names])
            self.play(LaggedStart(*[FadeIn(g_, shift=RIGHT * 0.15) for g_ in ghosts], lag_ratio=0.25), run_time=4.0)
            self.play(Create(zero), FadeIn(zlab))
            for mark, g_, nm, t, m in zip("abcdef", ghosts, names, details, marks):
                vo.wait_until(mark)
                self.play(ReplacementTransform(g_, nm), FadeIn(t, shift=RIGHT * 0.15))
                self.play(FadeIn(m, shift=LEFT * 0.2))
            vo.wait_until("g")
            self.play(LaggedStart(*[Indicate(m[1], color=WHITE, scale_factor=1.25) for m in marks], lag_ratio=0.15),
                      run_time=2.5)
        self.clear_scene()

    def regression(self):
        d = load("threats")
        e = d["designs"]["regression"]
        head = heading(r"Regression to the mean")
        rng = np.random.default_rng(12)
        n = 220
        true = rng.normal(0, 1.0, n)
        first = np.clip(true + rng.normal(0, 0.75, n), -3.3, 3.3)
        second = np.clip(true + rng.normal(0, 0.75, n), -3.3, 3.3)
        A = axes([-3.6, 3.6], [-3.6, 3.6], x_length=5.6, y_length=5.0, xlabel=r"first test (slower $\rightarrow$)",
                 ylabel=r"second test", center=[-3.5, -0.45, 0])
        ax = A.ax
        cut = np.sort(first)[-22]
        sel = first >= cut
        dots = VGroup(*[Dot(ax.c2p(a, b), radius=0.045, color=P.POOL).set_opacity(0.8) for a, b in zip(first, second)])
        diag = DashedLine(ax.c2p(-3.4, -3.4), ax.c2p(3.4, 3.4), color=GREY_B, stroke_width=2)
        dlab = label(r"no change", font_size=22, color=GREY_B).move_to(ax.c2p(-0.6, -3.0))
        band = Rectangle(width=ax.c2p(3.5, 0)[0] - ax.c2p(cut, 0)[0], height=5.0, stroke_width=0, fill_color=BIAS,
                         fill_opacity=0.14).move_to([(ax.c2p(3.5, 0)[0] + ax.c2p(cut, 0)[0]) / 2, ax.c2p(0, 0)[1], 0])
        chosen = VGroup(*[dots[i] for i in np.flatnonzero(sel)])
        m1, m2 = first[sel].mean(), second[sel].mean()
        mean_pt = Dot(ax.c2p(m1, m2), radius=0.12, color=WHITE)
        drop = Arrow(ax.c2p(m1, m1), ax.c2p(m1, m2), buff=0.02, color=BIAS, stroke_width=5,
                     max_tip_length_to_length_ratio=0.25)
        text = VGroup(
            wrapped_label(r"A score is the person plus the day.", 5.6, 30, WHITE),
            wrapped_label(r"Pick the slowest on one test, and you have picked slow people \emph{and} bad days.",
                          5.6, 30, WHITE),
            wrapped_label(r"The bad days do not come back. \ The group ``improves'', untreated.", 5.6, 30, BIAS),
            label(rf"in the Pool: \ ${e['effect']:.0f}$ ms from nothing", font_size=30, color=BIAS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([3.7, 0.0, 0])
        ill = note(r"illustrative scatter; \ the number is the Pool's").to_corner(DR, buff=0.3)
        with self.voiceover(
            "Regression to the mean deserves a picture, because it fools professionals. <bookmark mark='a'/> "
            "Give people a quick test twice. Each dot is a person: first score across, second score up. A score "
            "is partly the person, and partly the day they were having. <bookmark mark='b'/> Now do what a "
            "training programme naturally does: pick the people who need it most. The slowest tenth on the first "
            "test. <bookmark mark='c'/> You've picked slow people. But you've also picked people who were having "
            "a bad day, because a bad day is one of the ways to land in that corner. <bookmark mark='d'/> Test "
            "them again, and the bad days don't repeat. As a group, they're closer to average, with no treatment "
            f"at all. <bookmark mark='e'/> In the Pool that alone is worth {abs(e['effect']):.0f} milliseconds. "
            "Francis Galton found this in the heights of parents and children in the eighteen-eighties, and it's "
            "the reason that almost any remedy given to the worst cases seems to work."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(dots, lag_ratio=0.01), Create(diag), FadeIn(dlab), FadeIn(text[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(band), chosen.animate.set_color(BIAS).set_opacity(1))
            vo.wait_until("c")
            self.play(FadeIn(text[1], shift=LEFT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(mean_pt), GrowArrow(drop), FadeIn(text[2], shift=LEFT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(text[3], shift=LEFT * 0.15))
        self.clear_scene()

    def node(self, text, color, pos, w=3.0) -> VGroup:
        t = label(text, font_size=30, color=color)
        box = RoundedRectangle(width=max(w, t.width + 0.6), height=0.95, corner_radius=0.2, stroke_color=color,
                               stroke_width=2.5, fill_color=CARD_FILL, fill_opacity=1)
        return VGroup(box, t).move_to(pos)

    def confound(self):
        head = heading(r"What all six have in common")
        game = self.node(r"played the game", TREAT, [-3.6, -1.3, 0])
        rt = self.node(r"faster reactions", P.RESP, [3.6, -1.3, 0])
        third = self.node(r"young, quick, and keen", BIAS, [0, 1.5, 0], w=4.0)
        claim = Arrow(game.get_right(), rt.get_left(), buff=0.12, color=GREY_B, stroke_width=5)
        q = label(r"?", font_size=54, color=GREY_B).next_to(claim, UP, buff=0.1)
        a1 = Arrow(third.get_bottom() + LEFT * 0.9, game.get_top(), buff=0.12, color=BIAS, stroke_width=5)
        a2 = Arrow(third.get_bottom() + RIGHT * 0.9, rt.get_top(), buff=0.12, color=BIAS, stroke_width=5)
        word = VGroup(label(r"a confound:", font_size=36, color=BIAS),
                      label(r"something that goes with the treatment, and moves the outcome by itself", font_size=30))
        word.arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.7)
        alts = VGroup(*[label(t, font_size=24, color=BIAS) for t in (
            r"practice", r"new keyboards", r"growing up", r"a bad day", r"who stayed")])
        alts.arrange(RIGHT, buff=0.5).next_to(third, UP, buff=0.3)
        with self.voiceover(
            "All six have the same shape. <bookmark mark='a'/> The claim is an arrow: the game causes faster "
            "reactions. <bookmark mark='b'/> But in each study there was a third thing, which came along with "
            "the game and could move the reaction times by itself. In the volunteer study, being young and "
            "keen. <bookmark mark='c'/> In the others: practice, new keyboards, growing up, a bad day, who "
            "stayed to the end. <bookmark mark='d'/> That third thing is called a confound. And the list of "
            "possible confounds has no end, because it includes everything you didn't think to measure. So you "
            "can't beat them one at a time. You need a way to beat all of them at once, including the ones "
            "nobody has thought of. There is one, and it's the next chapter."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(game), FadeIn(rt), GrowArrow(claim), FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(third, shift=DOWN * 0.2), GrowArrow(a1), GrowArrow(a2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(a, shift=DOWN * 0.1) for a in alts], lag_ratio=0.5), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(word, shift=UP * 0.15))
        self.clear_scene()

    def sound(self):
        d = load("threats")
        e = d["designs"]["randomized"]
        head = heading(r"And the randomized experiment, 500 times")
        edges, counts = np.asarray(d["edges"]), np.asarray(d["hist_randomized"])
        A = axes([-12, 12], [0, float(counts.max()) * 1.15], x_length=9.0, y_length=3.8,
                 xlabel=r"effect reported (ms)", xticks=[-10, -5, 0, 5, 10], center=[-1.2, -0.45, 0])
        ax = A.ax
        bars = hist(ax, edges, counts, CTRL, 0.75)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, float(counts.max()) * 1.1), color=TRUTH, stroke_width=3)
        zlab = label(r"the truth: \ 0", font_size=24, color=TRUTH).next_to(zero, UP, buff=0.06)
        facts = VGroup(
            label(rf"mean of 500 studies: \ ${signed(e['mean'])}$ ms", font_size=30, color=CTRL),
            label(rf"``significant'' in {100 * e['share_significant']:.0f}\% of them", font_size=30, color=WHITE),
            label(r"as advertised: \ 5\%", font_size=26, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([5.0, 0.4, 0])
        if facts.get_right()[0] > 6.9:
            facts.shift(LEFT * (facts.get_right()[0] - 6.9))
        tag = simulated_tag(rf"simulated: the Pool, {d['n']} people a study")
        with self.voiceover(
            "For comparison, here is the design from the last chapter, with one addition that we'll come to: who "
            "plays and who doesn't is decided by shuffling. <bookmark mark='a'/> Five hundred studies of the "
            "useless game. Any one of them misses zero by a few milliseconds, one way or the other. "
            f"<bookmark mark='b'/> But they're centred on the truth. <bookmark mark='c'/> And "
            f"{100 * e['share_significant']:.0f} per cent of them come out significant by the usual test, which "
            "is the false-alarm rate that test promises, and Part 4 explains. An unsound design is wrong on "
            "average. A sound one is wrong only by chance, and by an amount it can tell you."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bars, lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(zero), FadeIn(zlab), FadeIn(facts[0]))
            vo.wait_until("c")
            self.play(FadeIn(facts[1]), FadeIn(facts[2]))
        self.clear_scene()
