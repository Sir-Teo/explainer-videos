from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.occupancy()
        self.four()
        self.trial()

    def card(self):
        card = chapter_card(13, r"In practice: \ drugs at the synapse", r"How is a drug for the mind studied, and "
                            r"what does it do?", lit=(), part=PART, scale=("molecule", "person"), marr=("tissue",))
        with self.voiceover(
            "Chapter thirteen. In practice: drugs at the synapse."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def occupancy(self):
        head = heading(r"The first measurement: \ how tightly does it bind?")
        A = axes([-2, 3], [0, 1.05], x_length=7.0, y_length=4.0, xticks=[-2, -1, 0, 1, 2, 3], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{10 ** v:g}", yfmt=lambda v: f"{v:.1f}",
                 xlabel=r"concentration of the drug (in units of $K_d$)", ylabel=r"fraction of receptors occupied",
                 center=[-3.0, -0.6, 0])
        ax = A.ax
        lg10 = np.linspace(-2, 3, 200)
        conc = 10 ** lg10
        shift = 10.0
        alone = trace(ax, lg10, conc / (conc + 1.0), EXC)
        blocked = trace(ax, lg10, conc / (conc + shift), INH)
        half = VGroup(DashedLine(ax.c2p(-2, 0.5), ax.c2p(0, 0.5), color=GREY_C, stroke_width=2),
                      DashedLine(ax.c2p(0, 0), ax.c2p(0, 0.5), color=GREY_C, stroke_width=2),
                      Dot(ax.c2p(0, 0.5), radius=0.08, color=THRESH))
        half_l = label(r"half occupied at $K_d$", font_size=24, color=THRESH).next_to(ax.c2p(0, 0.5), UL, buff=0.08)
        arrow = Arrow(ax.c2p(0.08, 0.5), ax.c2p(0.95, 0.5), color=INH, stroke_width=4, buff=0,
                      max_tip_length_to_length_ratio=0.2)
        arrow_l = label(r"$\times 10$", font_size=26, color=INH).next_to(arrow, DOWN, buff=0.06)
        side = VGroup(
            label(r"occupied $\;=\; \dfrac{[D]}{[D] + K_d}$", font_size=34, color=EXC),
            wrapped_label(r"$K_d$: \ the concentration that fills half the receptors. \ Smaller means tighter.", 4.8,
                          27, WHITE),
            wrapped_label(r"add a competing antagonist: \ the same curve, moved to the right", 4.8, 27, INH),
            label(r"shift $\;=\; 1 + \dfrac{[B]}{K_B}$", font_size=31, color=INH),
            wrapped_label(r"thousands of compounds are screened this way before one reaches an animal", 4.8, 26,
                          P.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).move_to([4.2, -0.4, 0])
        keep_in_frame(side)
        tag = psyche_tag(r"computed: the law of mass action")
        with self.voiceover(
            "Suppose your job is to study a drug for the mind. Your first question is the plainest one. How "
            "much of it sticks, and to what? <bookmark mark='a'/> Drug molecules and receptors meet at "
            "random, bind, and come apart again. At a steady state, the fraction of receptors occupied "
            "depends on the concentration in one simple way. <bookmark mark='b'/> Plot it on a scale where "
            "each step is ten times more drug, and you get this S-curve. The concentration that fills half "
            "the receptors is called the dissociation constant, and it measures how tightly the drug binds. "
            "The smaller it is, the tighter. <bookmark mark='c'/> Now add an antagonist that competes for "
            "the same site. The curve keeps its shape and slides to the right. It takes more of the first "
            "drug to reach the same occupancy: here, ten times more. The size of that shift is how an "
            "antagonist is measured. <bookmark mark='d'/> Laboratories run this measurement on thousands of "
            "compounds, against dozens of receptors, before one of them is ever given to an animal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Write(side[0]))
            vo.wait_until("b")
            self.play(Create(alone), run_time=3.0)
            self.play(FadeIn(half), FadeIn(half_l), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(blocked), GrowArrow(arrow), FadeIn(arrow_l), FadeIn(side[2]), run_time=2.5)
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4], shift=UP * 0.1))
        self.clear_scene()

    def four(self):
        head = heading(r"Four families of drug, \ each at one place on the synapse")
        data = [
            (r"SSRIs", "#5BD18B", r"block the pump that clears serotonin", r"depression, anxiety",
             r"the pump is blocked within hours; \ the benefit takes weeks"),
            (r"benzodiazepines", INH, r"help GABA's receptor: \ more brake", r"anxiety, seizures, sleep",
             r"tolerance, \ and dependence"),
            (r"stimulants", RULE, r"block or reverse the pumps for dopamine and noradrenaline",
             r"attention deficit, narcolepsy", r"the pump that cocaine blocks; \ dose and speed differ"),
            (r"antipsychotics", THRESH, r"block a receptor for dopamine", r"psychosis",
             r"the same receptor serves movement: \ tremor and stiffness"),
        ]
        cols = [(-6.7, 2.6), (-3.75, 4.0), (0.55, 2.8), (3.6, 3.3)]
        heads = VGroup(*[label(t, font_size=26, color=GREY_B).move_to([x, 2.45, 0], aligned_edge=LEFT)
                         for t, (x, _) in zip((r"family", r"at the synapse", r"given for", r"the catch"), cols)])
        rows = VGroup()
        y = 1.75
        for name, col, what, use, catch in data:
            cells = VGroup(label(name, font_size=31, color=col), wrapped_label(what, cols[1][1], 28, WHITE),
                           wrapped_label(use, cols[2][1], 28, GREY_A), wrapped_label(catch, cols[3][1], 28, DATA))
            for c, (x, _) in zip(cells, cols):
                c.move_to([x, y, 0], aligned_edge=UL)
            rows.add(cells)
            y -= max(c.height for c in cells) + 0.4
        table = VGroup(heads, rows)
        if table.height > 5.2:
            table.scale_to_fit_height(5.2)
        table.move_to([0, 0.0, 0])
        end = wrapped_label(r"What a drug does at a synapse is the first link in a long chain. \ Knowing it is "
                            r"not knowing why a person feels better.", 13.0, 28, P.ACCENT).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Now the drugs that are actually prescribed. Four families, and each acts at one of the six "
            "places from chapter two. <bookmark mark='a'/> The SSRIs block the pump that clears serotonin "
            "from the cleft. They're given for depression and anxiety. And here's a puzzle. The pump is "
            "blocked within hours of the first dose. The benefit, when it comes, takes weeks. So whatever "
            "these drugs do for mood, it isn't simply topping up a chemical. The slow part must be the brain "
            "adapting to the change. <bookmark mark='b'/> The benzodiazepines help GABA's receptor, which "
            "means more brake everywhere: calm, sleep, an end to a seizure. And the brain adapts to that "
            "too, which is tolerance, and then dependence. <bookmark mark='c'/> The stimulants block or "
            "reverse the pumps for dopamine and noradrenaline. That's the same pump that cocaine blocks. "
            "What differs is the dose, and how fast the drug arrives. <bookmark mark='d'/> The "
            "antipsychotics block a receptor for dopamine. But that receptor also serves the control of "
            "movement, and so the older drugs cause tremor and stiffness. <bookmark mark='e'/> Notice what "
            "each catch has in common. A drug reaches every synapse that uses its target, not only the ones "
            "you wanted. And what it does at the synapse is only the first link in a long chain. Knowing "
            "the first link isn't knowing why a person feels better. That question waits for the parts on "
            "disorder and treatment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(heads))
            for k, mark_ in enumerate("abcd"):
                vo.wait_until(mark_)
                self.play(LaggedStart(*[FadeIn(c, shift=RIGHT * 0.1) for c in rows[k]], lag_ratio=0.5), run_time=5.0)
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()

    def trial(self):
        d = archive.TURNER_2008.data
        head = heading(r"Does it work? \ Parts 2 and 4, in an industry")
        steps = VGroup(
            wrapped_label(r"random assignment to drug or placebo; \ nobody knows who has which", 5.8, 30, WHITE),
            wrapped_label(r"a snag: \ side effects tell people which they got", 5.8, 30, DATA),
            wrapped_label(r"a plan registered with the regulator before the trial starts", 5.8, 30, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-3.6, 0.4, 0])
        keep_in_frame(steps)
        x0, yb, h = 1.9, -1.9, 3.3
        bars = VGroup()
        for i, (name, v, col) in enumerate(((r"as registered", d["positive_fda"], MODEL),
                                            (r"as published", d["positive_published"], BAD))):
            b = Rectangle(width=1.5, height=h * v, stroke_width=0, fill_color=col, fill_opacity=0.85)
            b.move_to([x0 + 2.4 * i, yb + h * v / 2, 0])
            bars.add(VGroup(b, label(pct(v), font_size=40, color=col).next_to(b, UP, buff=0.1),
                            label(name, font_size=26, color=col).next_to([x0 + 2.4 * i, yb, 0], DOWN, buff=0.15)))
        bars_h = wrapped_label(rf"{d['trials']} trials of {d['drugs']} antidepressants: \ the share with a positive "
                               r"result", 5.4, 26, GREY_A).move_to([x0 + 1.2, 2.3, 0])
        end = wrapped_label(r"The drugs do something. \ The published record made them look better than the "
                            r"registered one. \ That is the file drawer of Part 4, measured.", 13.0, 28, P.ACCENT)
        end.to_edge(DOWN, buff=0.75)
        src = published_tag(archive.TURNER_2008.cite)
        with self.voiceover(
            "And then the question that matters to a patient. Does it work? You already know how that has to "
            "be answered, from Part 2. <bookmark mark='a'/> People are assigned at random to the drug or to "
            "a placebo, and neither they nor the staff know which. <bookmark mark='b'/> There's a snag, and "
            "it's Part 2's lesson again. These drugs have side effects. People who feel them can guess that "
            "they got the real thing, and the blind is partly broken. <bookmark mark='c'/> And from Part 4: "
            "the plan is registered with the regulator before the trial starts. Which makes a check "
            f"possible. <bookmark mark='d'/> In 2008 Erick Turner and colleagues took {d['trials']} trials "
            f"of {d['drugs']} antidepressants, as registered with the American regulator, and compared them "
            "with what had been published. By the regulator's own analysis, "
            f"{100 * d['positive_fda']:.0f} percent of the trials were positive. In the published "
            f"literature, it looked like {100 * d['positive_published']:.0f} percent. Nearly every positive "
            "trial had been published. Most of the others had not, or had been written up as successes. "
            "<bookmark mark='e'/> The drugs do something. But the record a doctor could read made them look "
            "better than the record the regulator held. That's the file drawer of Part 4, measured, in a "
            "field where the stakes are someone's treatment. The people who do this work, pharmacologists, "
            "trial statisticians, regulators, use everything in these first six parts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for k, mark_ in enumerate("abc"):
                vo.wait_until(mark_)
                self.play(FadeIn(steps[k], shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(bars_h))
            self.play(LaggedStart(*[FadeIn(b, shift=UP * 0.1) for b in bars], lag_ratio=0.8), run_time=7.0)
            vo.wait_until("e")
            self.play(FadeIn(end, shift=UP * 0.1))
        self.clear_scene()
