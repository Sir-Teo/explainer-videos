from __future__ import annotations

import numpy as np

from videos.psychology.psych4.common import *  # noqa: F403


class Repairs(VoiceoverScene):
    def construct(self):
        self.card()
        self.prereg()
        self.many_labs()
        self.absence()

    def card(self):
        card = chapter_card(10, r"The repairs", r"What does a procedure look like that closes the forks?",
                            lit={2014: r"Many Labs 1"}, part=PART, scale=("group", "culture"), marr=("what",))
        with self.voiceover(
            "Chapter ten. The repairs."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def prereg(self):
        d = archive.SCHEEL_2021.data
        head = heading(r"Preregistration: \ decide before you look")

        def step(text, color, w=2.25):
            box = RoundedRectangle(width=w, height=0.95, corner_radius=0.1, color=color, stroke_width=3,
                                   fill_color="#111722", fill_opacity=1)
            return VGroup(box, wrapped_label(text, w - 0.3, 24, WHITE).move_to(box))

        before = VGroup(step(r"hypothesis", TRUTH), step(r"sample size, stopping rule", TRUTH),
                        step(r"the one analysis", TRUTH)).arrange(RIGHT, buff=0.2)
        after = VGroup(step(r"collect the data", NULLC), step(r"run the plan", NULLC),
                       step(r"anything else: ``exploratory''", NULLC, 2.7)).arrange(RIGHT, buff=0.2)
        line = VGroup(before, after).arrange(RIGHT, buff=0.9).move_to([0, 1.55, 0])
        if line.width > 13.4:
            line.width = 13.4
        lock = DashedLine([0, 0, 0], [0, 1.7, 0], color=SIG, stroke_width=4)
        lock.move_to([(before.get_right()[0] + after.get_left()[0]) / 2, 1.55, 0])
        lock_l = label(r"time-stamped, public, fixed", font_size=22, color=SIG).next_to(lock, UP, buff=0.08)
        rr = wrapped_label(r"A registered report goes one step further: \ the journal reviews the plan, and "
                           r"commits to publish the result whatever it turns out to be.", 12.4, 28, P.ACCENT)
        rr.next_to(line, DOWN, buff=0.5)
        unit = 5.2
        bars = VGroup()
        for i, (name, n, share, color) in enumerate((
                (r"ordinary reports", d["standard_n"], d["standard_positive"], ORIG),
                (r"registered reports", d["registered_n"], d["registered_positive"], REP))):
            y = -1.75 - 0.75 * i
            bar = Rectangle(width=unit * share, height=0.46, stroke_width=0, fill_color=color, fill_opacity=0.9)
            bar.move_to([-1.6 + unit * share / 2, y, 0])
            nm = label(rf"{name} \ ({n} papers)", font_size=26, color=WHITE).next_to([-1.6, y, 0], LEFT, buff=0.2)
            val = label(pct(share), font_size=30, color=color).next_to(bar, RIGHT, buff=0.15)
            bars.add(VGroup(nm, bar, val))
        bcap = label(r"papers whose first hypothesis was supported", font_size=24, color=GREY_A)
        bcap.next_to(bars, DOWN, buff=0.22)
        src = published_tag(archive.SCHEEL_2021.cite)
        with self.voiceover(
            "Honesty wasn't enough, so the repair had to be a procedure, and the first one is almost "
            "embarrassingly simple. <bookmark mark='a'/> Before you collect any data, write down the "
            "hypothesis, the number of people and the rule for stopping, and the one analysis that will test "
            "it. <bookmark mark='b'/> Put that somewhere public with a date on it. <bookmark mark='c'/> Then "
            "collect the data and run the plan. You can still do anything else you like with the data, and "
            "you should. You just label it exploratory, so that a reader knows which result was a test and "
            "which was a search. Every fork from chapter four is closed, because the path was chosen before "
            "there was a result to steer by. That's preregistration. <bookmark mark='d'/> It closes the forks "
            "but not the file drawer, so a second idea goes further. In a registered report, the journal "
            "reviews the plan before the data exist, and commits to print the result whatever it is. "
            f"<bookmark mark='e'/> Does it change anything? Among {d['standard_n']} ordinary papers in "
            f"psychology, {100 * d['standard_positive']:.0f} per cent reported that their first hypothesis was "
            f"supported. Among {d['registered_n']} registered reports, "
            f"{100 * d['registered_positive']:.0f} per cent. The two sets of papers didn't test the same "
            "hypotheses, so part of that gap may be in what people chose to test. But ninety-six per cent "
            "was never believable. No science is right that often."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.15) for s_ in before], lag_ratio=0.6), run_time=4.0)
            vo.wait_until("b")
            self.play(Create(lock), FadeIn(lock_l))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s_, shift=RIGHT * 0.15) for s_ in after], lag_ratio=0.6), run_time=4.0)
            vo.wait_until("d")
            self.play(FadeIn(rr, shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(src), LaggedStart(*[FadeIn(b_) for b_ in bars], lag_ratio=0.7), FadeIn(bcap),
                      run_time=5.0)
        self.clear_scene()

    def many_labs(self):
        d = archive.MANY_LABS.data
        m1, m2 = d["ml1"], d["ml2"]
        head = heading(r"Many laboratories, one protocol")
        ok, weak, bad = STATUS_COLOR["replicated"], STATUS_COLOR["contested"], STATUS_COLOR["failed"]
        t1 = VGroup(*[Square(0.46, stroke_width=0, fill_opacity=1, fill_color=(
            ok if i < m1["replicated"] else weak if i < m1["replicated"] + m1["weak"] else bad))
            for i in range(m1["effects"])]).arrange(RIGHT, buff=0.1)
        g1 = VGroup(
            label(rf"2014: \ {m1['effects']} findings, \ {m1['samples']} laboratories, \ "
                  rf"{fmt_int(m1['participants'])} people", font_size=28, color=WHITE),
            t1,
            label(rf"{m1['replicated']} held, \ {m1['weak']} weakly, \ {m1['failed']} did not", font_size=26,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        t2 = VGroup(*[Square(0.4, stroke_width=0, fill_opacity=1, fill_color=(
            ok if i < m2["replicated"] else bad)) for i in range(m2["effects"])]).arrange_in_grid(2, 14, buff=0.1)
        g2 = VGroup(
            label(rf"2018: \ {m2['effects']} findings, \ {m2['samples']} samples, \ "
                  rf"{fmt_int(m2['participants'])} people, \ {m2['countries']} countries", font_size=26, color=WHITE),
            t2,
            label(rf"{m2['replicated']} held, \ {m2['effects'] - m2['replicated']} did not", font_size=26,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        left = VGroup(g1, g2).arrange(DOWN, aligned_edge=LEFT, buff=0.55)
        left.move_to([-6.75, -0.1, 0], aligned_edge=LEFT)
        unit = 4.2
        eff = VGroup()
        for i, (name, v, color) in enumerate(((r"as first printed", m2["median_d_original"], ORIG),
                                              (r"across the laboratories", m2["median_d_replication"], REP))):
            bar = Rectangle(width=unit * v, height=0.5, stroke_width=0, fill_color=color, fill_opacity=0.9)
            row = VGroup(label(name, font_size=24, color=GREY_A), VGroup(bar, label(rf"$d = {v:.2f}$", font_size=28,
                                                                                   color=color)).arrange(RIGHT, buff=0.15))
            row.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
            eff.add(row)
        eff.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        right = VGroup(label(r"the median effect, 2018", font_size=28, color=WHITE), eff).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25)
        right.move_to([max(left.get_right()[0] + 0.6, 2.0), 0.9, 0], aligned_edge=LEFT)
        lesson = wrapped_label(r"Whether a finding held depended on the finding, and hardly at all on the "
                               r"laboratory, the country or the sample.", 4.5, 27, P.ACCENT)
        lesson.next_to(right, DOWN, buff=0.5).align_to(right, LEFT)
        keep_in_frame(VGroup(right, lesson))
        src = published_tag(archive.MANY_LABS.cite)
        with self.voiceover(
            "The second repair answers the critics of chapter nine. If one replication settles nothing, run "
            "many. <bookmark mark='a'/> In the first Many Labs project, thirty-six laboratories "
            f"all ran the same thirteen experiments, from one shared protocol, on more than six "
            f"thousand people. {m1['replicated']} of the thirteen findings held. One held weakly. "
            f"{m1['failed']} didn't hold at all, and you'll meet those two in the Ledger. <bookmark mark='b'/> "
            f"The second project was larger: {m2['effects']} findings, {m2['samples']} samples, more than "
            f"fifteen thousand people in {m2['countries']} countries. {m2['replicated']} held. "
            f"<bookmark mark='c'/> And the size again. The median effect as first printed was "
            f"{m2['median_d_original']:.2f}. Across the laboratories it was {m2['median_d_replication']:.2f}. "
            "<bookmark mark='d'/> But the most useful result is a quieter one. When a replication fails, the "
            "usual defence is that something about the new sample was different: the culture, the language, "
            "the students. With dozens of samples you can check. And whether a finding held depended on the "
            "finding, and hardly at all on where it was run. The ones that worked, worked nearly everywhere. "
            "The ones that failed, failed nearly everywhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(g1[0]), FadeIn(t1, lag_ratio=0.1), run_time=2.0)
            self.play(FadeIn(g1[2]))
            vo.wait_until("b")
            self.play(FadeIn(g2[0]), FadeIn(t2, lag_ratio=0.05), run_time=2.0)
            self.play(FadeIn(g2[2]))
            vo.wait_until("c")
            self.play(FadeIn(right[0]), LaggedStart(*[FadeIn(r_) for r_ in eff], lag_ratio=0.7), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(lesson, shift=UP * 0.15))
        self.clear_scene()

    def absence(self):
        d = load("absence")
        sm = d["small_study"]
        head = heading(r"How to say that nothing is there")
        A = axes([-0.5, 0.5], [0, 3], x_length=9.0, y_length=3.0, xticks=[-0.4, -0.2, 0, 0.2, 0.4],
                 xfmt=lambda v: f"{v:+.1f}" if abs(v) > 1e-9 else "0", yticks=[], xlabel=r"effect ($d$)",
                 center=[-1.9, -0.75, 0])
        ax = A.ax
        band = Rectangle(width=ax.c2p(d["bound"], 0)[0] - ax.c2p(-d["bound"], 0)[0], height=3.0, stroke_width=0,
                         fill_color=TRUTH, fill_opacity=0.16).move_to(ax.c2p(0, 1.5))
        band_l = label(r"too small to matter", font_size=22, color=TRUTH).next_to(band, UP, buff=0.08)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, 3), color=GREY_B, stroke_width=2)

        def interval(lo, hi, y, color, text):
            lo, hi = max(lo, -0.5), min(hi, 0.5)
            ln = Line(ax.c2p(lo, y), ax.c2p(hi, y), color=color, stroke_width=7)
            dot = Dot(ax.c2p(d["est"], y), radius=0.1, color=color)
            caps = VGroup(*[Line(ax.c2p(v, y) + DOWN * 0.13, ax.c2p(v, y) + UP * 0.13, color=color, stroke_width=4)
                            for v in (lo, hi)])
            t = label(text, font_size=24, color=color).next_to(ln, UP, buff=0.14)
            return VGroup(ln, caps, dot, t)

        small = interval(*sm["ci95"], 2.0, ORIG, rf"{d['n_small']} people: \ ``not significant''")
        large = interval(*d["ci95"], 0.8, REP, rf"{fmt_int(d['n_large'])} people: \ ``not significant''")
        side = VGroup(
            VGroup(label(rf"{d['n_small']} people", font_size=30, color=ORIG),
                   wrapped_label(rf"could be $-{abs(sm['ci95'][0]):.2f}$, could be $+{sm['ci95'][1]:.2f}$: \ no "
                                 r"news", 4.4, 25, WHITE),
                   label(rf"evidence for ``nothing'': \ {sm['bf01']:.1f} to 1", font_size=24, color=GREY_A),
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(rf"{fmt_int(d['n_large'])} people", font_size=30, color=REP),
                   wrapped_label(r"anything large enough to matter is ruled out", 4.4, 25, WHITE),
                   label(rf"evidence for ``nothing'': \ {d['bf01']:.0f} to 1", font_size=24, color=GREY_A),
                   ).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([4.75, -0.2, 0])
        keep_in_frame(side)
        tag = note(r"computed: two illustrative studies with the same estimate; \ the bound and the comparison "
                   r"effect are choices").to_corner(DR, buff=0.2)
        with self.voiceover(
            "One more repair, and it's the one the replicators needed most. A replication that comes out "
            "not significant: what has it shown? <bookmark mark='a'/> Here are two studies. Both estimate the "
            "effect at about zero. Both are not significant. <bookmark mark='b'/> The first had a hundred "
            f"people. Its margin of error runs from minus {abs(sm['ci95'][0]):.2f} to plus "
            f"{sm['ci95'][1]:.2f}. A medium effect in either direction would fit comfortably. This study "
            "hasn't found nothing. It has found out nothing. <bookmark mark='c'/> The second had ten thousand. "
            "<bookmark mark='d'/> Now decide, before looking, how small an effect would be too small to care "
            "about; say a tenth of a standard deviation either way. The whole margin of error sits inside that "
            "band. That's an equivalence test, and it turns the absence of evidence into evidence of absence: "
            "whatever is there is too small to matter. <bookmark mark='e'/> There's a second way to say it. "
            "Ask how much better the data are predicted by no effect than by an effect of the size Bem "
            f"reported. For the large study, about {d['bf01']:.0f} to one in favour of nothing. For the small "
            f"one, {sm['bf01']:.1f} to one, which is no evidence at all. That ratio is a Bayes factor. Parts "
            "43 and 48 take both tools apart. For now, remember the picture: not significant is two different "
            "results, and only the width of the bar tells you which."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(small[2]), FadeIn(large[2]))
            vo.wait_until("b")
            self.play(Create(small[0]), FadeIn(small[1]), FadeIn(small[3]), FadeIn(side[0][0]), FadeIn(side[0][1]))
            vo.wait_until("c")
            self.play(Create(large[0]), FadeIn(large[1]), FadeIn(large[3]), FadeIn(side[1][0]))
            vo.wait_until("d")
            self.play(FadeIn(band), FadeIn(band_l), FadeIn(side[1][1]))
            vo.wait_until("e")
            self.play(FadeIn(side[1][2]), FadeIn(side[0][2]))
        self.clear_scene()
