from __future__ import annotations

import numpy as np

from videos.psychology.psych4.common import *  # noqa: F403


class Effect(VoiceoverScene):
    def construct(self):
        self.card()
        self.pictures()
        self.units()
        self.significant()

    def card(self):
        card = chapter_card(1, r"How big is big?", r"What does an effect of 0.22 look like?", lit=(), part=PART,
                            scale=("group",), marr=("what",))
        with self.voiceover(
            "Chapter one. How big is big?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def pictures(self):
        d = load("effects")
        head = heading(r"An effect size: \ the difference, in units of how much people vary")
        x, pdf = np.asarray(d["x"]), np.asarray(d["pdf"])
        panels = VGroup()
        specs = [(r"small", d["rows"]["0.2"], SIZE["0.2"]), (r"medium", d["rows"]["0.5"], SIZE["0.5"]),
                 (r"large", d["rows"]["0.8"], SIZE["0.8"])]
        for i, (name, row, color) in enumerate(specs):
            A = axes([-3.5, 4.5], [0, 0.45], x_length=4.0, y_length=2.3, xticks=[], yticks=[],
                     center=[-4.5 + 4.5 * i, 0.95, 0])
            ax = A.ax
            base = curve(ax, x, pdf, NULLC, stroke_width=3)
            moved = curve(ax, x + row["d"], pdf, color, stroke_width=3)
            title = label(rf"{name}: \ $d = {row['d']:.1f}$", font_size=34, color=color).next_to(A, UP, buff=0.1)
            facts = VGroup(
                label(rf"overlap \ {pct(row['overlap'])}", font_size=30, color=WHITE),
                label(r"a treated person beats an untreated one", font_size=22, color=GREY_A),
                label(rf"{pct(row['superiority'])} of the time", font_size=30, color=color),
                label(rf"people needed per group: \ {row['n_for_80']}", font_size=26, color=GREY_A),
            ).arrange(DOWN, buff=0.13).next_to(A, DOWN, buff=0.25)
            g = VGroup(A, base, moved, title, facts)
            g.plot, g.facts = VGroup(A, base, moved, title), facts
            panels.add(g)
        bem = d["bem"]
        line = label(rf"Bem's average effect, $d = {r2(bem['d'])}$: \ overlap {pct(bem['overlap'])}; \ a coin that "
                     rf"lands heads {pct(bem['superiority'])} of the time", font_size=28, color=TRUTH)
        line.to_edge(DOWN, buff=0.65)
        intro = VGroup(
            label(r"$d \;=\; \dfrac{\text{difference between the groups}}{\text{how much people differ (one SD)}}$",
                  font_size=48, color=WHITE),
            label(r"Part 2's game: \ $\dfrac{8 \text{ ms}}{24 \text{ ms}} = 0.33$", font_size=40, color=TRUTH),
        ).arrange(DOWN, buff=0.6).move_to([0, 0.2, 0])
        tag = note(r"computed: two normal curves of equal spread; \ ``people needed'' is for an 80\% chance of "
                   r"detection").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Before we can ask whether a finding is real, we need a way to say how big it is. A difference of "
            "eight milliseconds means nothing until you know how much people vary. So divide the difference by "
            "the standard deviation. That's the effect size, written d, and it's the one number you should ask "
            "for whenever someone reports a finding. <bookmark mark='a'/> By a rough convention due to Jacob "
            "Cohen, d of point two is small. The two groups overlap almost completely. Pick one person from each "
            f"group, and the treated one comes out ahead {100 * d['rows']['0.2']['superiority']:.0f} times in a "
            "hundred, against fifty by chance. <bookmark mark='b'/> Point five is medium: "
            f"{100 * d['rows']['0.5']['superiority']:.0f} times in a hundred. <bookmark mark='c'/> Point eight is "
            "large, and you can see the gap with the naked eye. Look at the bottom line of each panel: the smaller "
            "the effect, the more people you need to have a decent chance of seeing it, and the number climbs "
            f"fast. <bookmark mark='d'/> Bem's effect was {bem['d']}. If it were real, it would be a coin that "
            f"lands heads {100 * bem['superiority']:.0f} times in a hundred."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            self.wait(4.0)
            self.play(FadeIn(intro[0], shift=UP * 0.15))
            self.wait(3.0)
            self.play(FadeIn(intro[1], shift=UP * 0.15))
            for m, g in zip("abc", panels):
                vo.wait_until(m)
                if m == "a":
                    self.play(FadeOut(intro), run_time=0.5)
                self.play(FadeIn(g.plot), run_time=1.0)
                self.play(LaggedStart(*[FadeIn(f) for f in g.facts], lag_ratio=0.4), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(line, shift=UP * 0.15))
        self.clear_scene()

    def units(self):
        from explainer.psychology import evidence as E

        bem = archive.BEM_2011.data["mean_d"]
        head = heading(r"One effect, four ways of saying it")
        cols = [r"difference, $d$", r"correlation, $r$", r"variation explained", r"higher group wins"]
        xs = [-3.9, -0.9, 2.1, 5.1]
        heads = VGroup(*[label(c, font_size=26, color=GREY_A).move_to([x, 1.9, 0]) for c, x in zip(cols, xs)])
        rule = Line([-6.6, 1.5, 0], [6.6, 1.5, 0], color=GREY_D, stroke_width=2)
        rows = VGroup()
        specs = [(0.2, r"small", SIZE["0.2"]), (0.5, r"medium", SIZE["0.5"]), (0.8, r"large", SIZE["0.8"]),
                 (bem, r"Bem", KANT)]
        for i, (d, name, color) in enumerate(specs):
            y = 0.85 - 0.95 * i
            r = E.d_to_r(d)
            cells = [rf"{d:.2f}", r2(r), pct(r * r, 1), pct(E.superiority(d))]
            row = VGroup(label(name, font_size=30, color=color).move_to([-6.1, y, 0]))
            for c, x in zip(cells, xs):
                row.add(label(c, font_size=38, color=color).move_to([x, y, 0]))
            rows.add(row)
        end = label(r"``Variation explained'' makes every effect in psychology look small. \ Say which unit you "
                    r"are using.", font_size=27, color=P.ACCENT).to_edge(DOWN, buff=0.6)
        tag = note(r"computed: two groups of equal size").to_corner(DR, buff=0.2)
        r_med, r_bem = E.d_to_r(0.5), E.d_to_r(bem)
        with self.voiceover(
            "You'll meet the same effect in other clothes, so here's the dictionary. <bookmark mark='a'/> A "
            "difference between two groups can be restated as a correlation between which group you're in and "
            f"how you score. A medium difference, half a standard deviation, is a correlation of "
            f"{r_med:.2f}. <bookmark mark='b'/> Square the correlation and you get the share of the variation "
            f"between people that the group accounts for: {100 * r_med * r_med:.0f} per cent. "
            "<bookmark mark='c'/> And it's the same effect that lets the higher group win sixty-four "
            "contests in a hundred. Six per cent sounds like nothing. Sixty-four to thirty-six sounds like an "
            "edge. They're one number. <bookmark mark='d'/> Bem's effect, in this dictionary: a correlation "
            f"of {r_bem:.2f}, about one per cent of the variation, fifty-six contests in a hundred. Keep that "
            "row in mind. To tell fifty-six from fifty reliably takes a great many observations, and his nine "
            "experiments shared about a thousand people between them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(heads[0]), FadeIn(rule),
                      *[FadeIn(VGroup(r_[0], r_[1])) for r_ in rows[:3]])
            vo.wait_until("a")
            self.play(FadeIn(heads[1]), *[FadeIn(r_[2]) for r_ in rows[:3]])
            vo.wait_until("b")
            self.play(FadeIn(heads[2]), *[FadeIn(r_[3]) for r_ in rows[:3]])
            vo.wait_until("c")
            self.play(FadeIn(heads[3]), *[FadeIn(r_[4]) for r_ in rows[:3]])
            self.play(FadeIn(end))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.15))
        self.clear_scene()

    def significant(self):
        d = load("effects")
        head = heading(r"``Significant'' is not ``large''")
        ns, ps = d["ns"], d["p_small"]
        logp = [max(np.log10(p), -8) for p in ps]
        A = axes([0, len(ns) - 1], [-8, 0], x_length=7.4, y_length=3.9, xticks=list(range(len(ns))),
                 yticks=[-8, -6, -4, -2, 0], xfmt=lambda v: fmt_int(ns[int(round(v))]),
                 yfmt=lambda v: r"1" if v == 0 else rf"10^{{{int(v)}}}", xlabel=r"people in each group",
                 ylabel=r"p-value", center=[-2.6, -0.45, 0])
        ax = A.ax
        thr = DashedLine(ax.c2p(0, np.log10(0.05)), ax.c2p(len(ns) - 1, np.log10(0.05)), color=SIG, stroke_width=3)
        thr_l = label(r"$p = .05$", font_size=24, color=SIG).next_to(thr, UP, buff=0.05).align_to(thr, LEFT).shift(
            RIGHT * 0.3)
        line = curve(ax, list(range(len(ns))), logp, WHITE, stroke_width=3)
        dots = VGroup(*[Dot(ax.c2p(i, lp), radius=0.08, color=(SIG if p < 0.05 else GREY_B))
                        for i, (lp, p) in enumerate(zip(logp, ps))])
        side = VGroup(
            label(rf"the same effect throughout: \ $d = {d['small_d']}$", font_size=28, color=TRUTH),
            wrapped_label(rf"an overlap of {pct(E_overlap(d['small_d']))}: \ far too small to matter to anyone",
                          5.0, 26, GREY_A),
            wrapped_label(rf"``significant'' once there are {fmt_int(d['n_sig_small'])} people in each group",
                          5.0, 28, SIG),
            wrapped_label(r"A p-value mixes the size of the effect with the size of the sample. \ Ask for both "
                          r"separately.", 5.0, 28, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.3, 0.1, 0])
        tag = note(r"computed").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Now the commonest confusion in reading research. A result is called significant, and people hear "
            "important. <bookmark mark='a'/> Take one fixed effect, a twentieth of a standard deviation. It's far "
            "too small to matter to anyone. <bookmark mark='b'/> Test it with twenty people a group, and the "
            "p-value is nowhere near point oh five. With a hundred, still nothing. <bookmark mark='c'/> But keep "
            f"adding people. At about three thousand in each group it crosses the line, and with a hundred "
            "thousand the p-value has twenty-eight zeros after the decimal point. The effect never changed. "
            "<bookmark mark='d'/> So a p-value isn't a measure of how big or how important something is. It mixes "
            "the size of the effect with the size of the sample. A tiny effect in a huge study and a big effect in "
            "a small study can give the same p. Always ask for the two things separately: how big, and how sure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(thr), FadeIn(thr_l), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(p_) for p_ in dots], lag_ratio=0.5), run_time=9.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()


def E_overlap(d: float) -> float:
    from explainer.psychology import evidence
    return evidence.overlap(d)
