from __future__ import annotations

import numpy as np

from videos.psychology.psych2.common import *  # noqa: F403


class Within(VoiceoverScene):
    def construct(self):
        self.card()
        self.noise()
        self.pairing()
        self.order()
        self.squares()

    def card(self):
        card = chapter_card(6, r"Between people and within them", r"What if each person could be their own control?",
                            lit=(), part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter six. Between people, and within them."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def noise(self):
        d = load("within")
        head = heading(r"A real effect, and the people it has to be seen through")
        unit = 0.085
        eff = Rectangle(width=abs(d["effect"]) * unit, height=0.55, stroke_width=0, fill_color=TREAT, fill_opacity=0.9)
        sd = Rectangle(width=2 * d["sd"] * unit, height=0.55, stroke_width=0, fill_color=P.POOL, fill_opacity=0.7)
        rows = VGroup(
            VGroup(label(r"the game's effect", font_size=30, color=TREAT), eff,
                   label(rf"{abs(d['effect']):.0f} ms", font_size=34, color=TREAT)),
            VGroup(label(r"how much people differ ($\pm 1$ SD)", font_size=30, color=P.POOL), sd,
                   label(rf"$\pm${d['sd']:.0f} ms", font_size=34, color=P.POOL)),
        )
        for r in rows:
            r[1].move_to([-0.6 + r[1].width / 2, 0, 0])
            r[0].next_to(r[1], UP, buff=0.1).align_to(r[1], LEFT)
            r[2].next_to(r[1], RIGHT, buff=0.25)
        rows.arrange(DOWN, buff=0.6, aligned_edge=LEFT).move_to([-1.2, 1.3, 0])
        need = VGroup(
            label(r"for an 80\% chance of detecting it:", font_size=30, color=GREY_A),
            label(rf"{d['n_between_per_group']} people in each group", font_size=52, color=WHITE),
            label(rf"{d['n_between_total']} in all; \ checked on the Pool: \ detected in "
                  rf"{100 * d['sim_power_between']:.0f}\% of 400 studies", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.9)
        tag = simulated_tag()
        with self.voiceover(
            "Randomized groups get the answer right on average. But they can be slow about it. "
            f"<bookmark mark='a'/> Suppose the game really does take {abs(d['effect']):.0f} milliseconds off a "
            "reaction time. <bookmark mark='b'/> People differ from one another by far more than that: about "
            f"{d['sd']:.0f} milliseconds either way. So in a comparison of two groups, the effect has to be seen "
            "through all the ordinary differences between people, which are three times its size. "
            f"<bookmark mark='c'/> The arithmetic says you need {d['n_between_per_group']} people in each group "
            "to have four chances in five of detecting it. That's the price of comparing different people, and "
            "it's why so many small experiments find nothing, or find something that isn't there. We come back to "
            "that in Part 4."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0][0]), GrowFromEdge(rows[0][1], LEFT), FadeIn(rows[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1][0]), GrowFromEdge(rows[1][1], LEFT), FadeIn(rows[1][2]))
            vo.wait_until("c")
            self.play(FadeIn(need, shift=UP * 0.15))
        self.clear_scene()

    def pairing(self):
        d = load("within")
        head = heading(r"Each person, with the game and without")
        edges = np.asarray(d["edges"])
        top = float(d["hist_within"].max()) * 1.12
        A = axes([-40, 24], [0, top], x_length=8.6, y_length=3.7, xticks=[-40, -30, -20, -10, 0, 10, 20],
                 xlabel=r"effect reported by a study of 40 people (ms)", center=[-2.1, -0.45, 0])
        ax = A.ax
        hb = hist(ax, edges, d["hist_between"], P.POOL, 0.55)
        hw = hist(ax, edges, d["hist_within"], P.ACCENT, 0.7)
        truth = DashedLine(ax.c2p(d["effect"], 0), ax.c2p(d["effect"], top), color=TRUTH, stroke_width=3)
        tlab = label(rf"the truth: \ ${d['effect']:.0f}$", font_size=22, color=TRUTH).next_to(truth, UP, buff=0.06)
        leg = legend([(P.POOL, rf"two groups of 20: \ spread {d['sd_between']:.1f} ms"),
                      (P.ACCENT, rf"40 people, each both ways: \ spread {d['sd_within']:.1f} ms")], font_size=22)
        leg.move_to([4.7, 1.5, 0])
        if leg.get_right()[0] > 6.95:
            leg.shift(LEFT * (leg.get_right()[0] - 6.95))
        why_ = VGroup(
            label(rf"a person's two sessions correlate {d['rho']:.2f}", font_size=26, color=WHITE),
            wrapped_label(r"subtract a person from themselves, and what made them differ from everyone else is gone",
                          4.4, 24, GREY_A),
            label(rf"about {d['n_within_sim']} people, not {d['n_between_total']}", font_size=34, color=P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(leg, DOWN, buff=0.45).align_to(leg, LEFT)
        tag = simulated_tag()
        with self.voiceover(
            "There's a way round it, when the treatment allows. Don't compare different people. Compare each "
            "person with themselves: one session with the game, one without. <bookmark mark='a'/> Here are three "
            "hundred studies of forty people done the first way, as two groups of twenty. They scatter widely "
            "round the truth. <bookmark mark='b'/> And three hundred done the second way, each person measured "
            f"both ways. The same forty people, and the estimates are more than "
            f"{int(d['sd_between'] / d['sd_within'])} times as tight. <bookmark mark='c'/> "
            f"The reason is that a person is very like themselves. In the Pool, two sessions of the same person "
            f"correlate {d['rho']:.2f}. Subtract one from the other, and nearly everything that made that person "
            f"different from everybody else cancels. <bookmark mark='d'/> For the same four chances in five, "
            f"about {d['n_within_sim']} people do the work of {d['n_between_total']}. This is why so much of "
            "experimental psychology, from Donders on, is done within the person."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(truth), FadeIn(tlab), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(hb, lag_ratio=0.05), FadeIn(leg[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(hw, lag_ratio=0.05), FadeIn(leg[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(why_[0]), FadeIn(why_[1]))
            vo.wait_until("d")
            self.play(FadeIn(why_[2], shift=UP * 0.15))
        self.clear_scene()

    def order(self):
        d = load("within")
        head = heading(r"The price: \ whatever comes second is not the same person")
        edges = np.asarray(d["edges"])
        top = float(d["hist_within"].max()) * 1.12
        A = axes([-40, 24], [0, top], x_length=8.6, y_length=3.3, xticks=[-40, -30, -20, -10, 0, 10, 20],
                 xlabel=r"effect reported (ms)", center=[-2.1, -1.0, 0])
        ax = A.ax
        hu = hist(ax, edges, d["hist_unbalanced"], BIAS, 0.7)
        hw = hist(ax, edges, d["hist_within"], P.ACCENT, 0.7)
        truth = DashedLine(ax.c2p(d["effect"], 0), ax.c2p(d["effect"], top), color=TRUTH, stroke_width=3)
        tlab = label(rf"the truth: \ ${d['effect']:.0f}$", font_size=22, color=TRUTH).next_to(truth, UP, buff=0.06)

        def session(text, color):
            t = label(text, font_size=24, color=WHITE)
            box = RoundedRectangle(width=1.9, height=0.55, corner_radius=0.1, stroke_width=0, fill_color=color,
                                   fill_opacity=0.55)
            return VGroup(box, t)

        plain = VGroup(session(r"no game", CTRL), MathTex(r"\rightarrow", font_size=36, color=GREY_B),
                       session(r"game", TREAT)).arrange(RIGHT, buff=0.2)
        half1 = plain.copy()
        half2 = VGroup(session(r"game", TREAT), MathTex(r"\rightarrow", font_size=36, color=GREY_B),
                       session(r"no game", CTRL)).arrange(RIGHT, buff=0.2)
        bad = VGroup(label(r"everyone:", font_size=24, color=BIAS), plain).arrange(RIGHT, buff=0.3)
        good = VGroup(label(r"half, by shuffle:", font_size=24, color=P.ACCENT), half1,
                      label(r"the other half:", font_size=24, color=P.ACCENT), half2).arrange(RIGHT, buff=0.3)
        bad.move_to([-1.6, 2.35, 0])
        good.scale_to_fit_width(12.8).move_to([0, 1.55, 0])
        notes = VGroup(
            label(rf"control first for all: \ ${d['mean_unbalanced']:.1f}$ ms", font_size=28, color=BIAS),
            label(rf"practice ({d['practice_first_retest']:.0f} ms) is credited to the game", font_size=24,
                  color=GREY_A),
            label(rf"counterbalanced: \ ${d['mean_within']:.1f}$ ms", font_size=28, color=P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([4.75, -0.9, 0])
        if notes.get_right()[0] > 6.95:
            notes.shift(LEFT * (notes.get_right()[0] - 6.95))
        tag = simulated_tag()
        with self.voiceover(
            "It has a price. The two sessions happen in some order, and the second session isn't taken by quite "
            "the same person: they've done the task before. <bookmark mark='a'/> Suppose everyone does the "
            "session without the game first, and the session with it second. <bookmark mark='b'/> Then the "
            f"practice from the first session is counted as the game's doing. The studies agree with one another "
            f"beautifully, on {abs(d['mean_unbalanced']):.0f} milliseconds, and the truth is "
            f"{abs(d['effect']):.0f}. Precisely wrong. <bookmark mark='c'/> The repair is called "
            "counterbalancing. Half the people, chosen by shuffle, take the game first, and half take it second. "
            "Practice still happens, but now it helps each condition equally, and cancels. <bookmark mark='d'/> "
            "Back on the truth. Some things can't be counterbalanced, of course. You can't untrain a person, or "
            "give back a memory. Then it has to be two groups."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(truth), FadeIn(tlab), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bad, shift=DOWN * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(hu, lag_ratio=0.05), FadeIn(notes[0]), FadeIn(notes[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(good, shift=DOWN * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(hw, lag_ratio=0.05), FadeIn(notes[2]), run_time=2.0)
        self.clear_scene()

    def square(self, rows, cell=0.62, title="", sub="", color=WHITE) -> VGroup:
        letters = "ABCD"
        cells = VGroup()
        for i, row in enumerate(rows):
            for j, c in enumerate(row):
                sq = Square(side_length=cell, stroke_color=BACKGROUND, stroke_width=3, fill_color=COND[int(c)],
                            fill_opacity=0.85).move_to([j * cell, -i * cell, 0])
                cells.add(VGroup(sq, label(letters[int(c)], font_size=26, color=BLACK).move_to(sq)))
        t = label(title, font_size=28, color=color).next_to(cells, UP, buff=0.3)
        s = wrapped_label(sub, 4.0, 22, GREY_A).next_to(cells, DOWN, buff=0.3)
        g = VGroup(cells, t, s)
        g.cells = cells
        return g

    def squares(self):
        d = load("within")
        head = heading(r"Four conditions: \ in what order?")
        cyc = self.square(d["cyclic"], title=r"a Latin square", sub=r"each condition once in each position; \ but B "
                          r"comes straight after A in three rows of four")
        wil = self.square(d["williams"], title=r"a Williams square", sub=r"and each condition follows every other "
                          r"exactly once", color=P.ACCENT)
        cnt = VGroup(label(rf"{d['orders_complete']}", font_size=72, color=WHITE),
                     label(r"possible orders", font_size=28, color=GREY_A),
                     wrapped_label(r"complete counterbalancing: \ one group of people for each", 3.6, 22, GREY_A))
        cnt.arrange(DOWN, buff=0.15)
        g = VGroup(cnt, cyc, wil).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, -0.2, 0])
        axes_ = VGroup(label(r"position in the session $\rightarrow$", font_size=20, color=GREY_B),
                       label(r"group of people $\downarrow$", font_size=20, color=GREY_B))
        axes_[0].next_to(cyc.cells, UP, buff=0.04).align_to(cyc.cells, LEFT)
        axes_[1].rotate(0).next_to(cyc.cells, LEFT, buff=0.12)
        axes_[0].set_opacity(0)  # the titles sit there; the row label is enough
        with self.voiceover(
            "With two conditions there are two orders. With four conditions there are twenty-four, "
            "<bookmark mark='a'/> and running all of them takes twenty-four groups of people. "
            "<bookmark mark='b'/> A Latin square does it with four. Each row is the order one group follows, and "
            "every condition turns up once in every position, so practice and fatigue fall evenly. But look at "
            "this one: B comes straight after A in three rows of the four, and never after C. If A leaves "
            "something behind, it's B that gets it. "
            "<bookmark mark='c'/> A Williams square fixes that too. Each condition appears once in each "
            "position, and each one follows every other exactly once. Four groups, and both kinds of order "
            "effect are balanced. This is a small piece of combinatorics that every within-person experiment "
            "in the series will lean on."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cnt, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(cyc[1]), FadeIn(axes_[1]), LaggedStart(*[FadeIn(c) for c in cyc.cells], lag_ratio=0.05),
                      run_time=2.5)
            self.play(FadeIn(cyc[2]))
            vo.wait_until("c")
            self.play(FadeIn(wil[1]), LaggedStart(*[FadeIn(c) for c in wil.cells], lag_ratio=0.05), run_time=2.5)
            self.play(FadeIn(wil[2]))
        self.clear_scene()
