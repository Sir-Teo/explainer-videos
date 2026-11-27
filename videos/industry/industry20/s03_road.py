from __future__ import annotations

from videos.industry.industry20.common import *  # noqa: F403


class Road(VoiceoverScene):
    def construct(self):
        card(self, 2, "From molecule to medicine", "What happens between an idea and a pill on the shelf?",
             "Chapter two. From molecule to medicine. What happens between an idea in a laboratory and a pill on a "
             "pharmacy shelf?", lit=("make",))
        self.timeline()
        self.funnel()

    def timeline(self):
        O = R["odds"]
        phases = O["phases"]
        x = -5.6
        scale = 10.8 / sum(y for _, y, _ in phases)
        cols = [BIO, LAB, PRICE, BRAND]
        blocks = VGroup()
        for (name, yrs, _), col in zip(phases, cols):
            w = yrs * scale
            b = Rectangle(width=w, height=0.8, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to([x + w / 2, 0.4, 0])
            b.grow = LEFT
            lab = VGroup(tx(name, 16, "#0E1117", bold=True), tx(f"{yrs:.1f} years", 14, "#0E1117")).arrange(DOWN, buff=0.04).move_to(b)
            if lab.width > w - 0.1:
                lab.scale_to_fit_width(w - 0.1)
            blocks.add(VGroup(b, lab))
            x += w
        pre = VGroup(draw.molecule("CH4").scale(0.8), tx("before: the laboratory and animals", 14, GREY_A)).arrange(DOWN, buff=0.1).move_to([-4.6, 2.3, 0])
        who = VGroup(tx("Phase I: a small group; is it safe?", 15, BIO),
                     tx("Phase II: patients; does it work at all?", 15, LAB),
                     tx("Phase III: large trials; does it work, and safely, against the alternatives?", 15, PRICE),
                     tx("review: the FDA reads the evidence", 15, BRAND)).arrange(DOWN, aligned_edge=LEFT, buff=0.1).move_to([0, -1.7, 0])
        tot = tx(f"{O['years']:.1f} years on average from the first human test to approval", 18, WHITE, bold=True).next_to(blocks, UP, buff=0.35).shift(RIGHT * 1.5)
        src = source("BIO, Informa and QLS, Clinical Development Success Rates 2011-2020 (2021): average phase durations", size=12)
        beat(self,
             "A medicine starts as a molecule that does something useful to a target in the body, found in a laboratory "
             "and tested in cells and animals. Then come the human trials. <bookmark mark='a'/> Phase one gives the drug to "
             f"a small group to see if it is safe: on average {phases[0][1]:.1f} years. <bookmark mark='b'/> Phase two "
             f"tries it in patients to see if it works at all: {phases[1][1]:.1f} years. <bookmark mark='c'/> Phase three, "
             "the longest and most expensive, tests it in large trials, against the best existing treatment or a placebo: "
             f"{phases[2][1]:.1f} years. <bookmark mark='d'/> Then the regulator, America's Food and Drug Administration, "
             f"reviews the evidence: {phases[3][1]:.1f} years. <bookmark mark='e'/> From the first person to approval: "
             f"{O['years']:.1f} years on average, for the drugs that make it.",
             base=[pre, src], steps=[[blocks[0], who[0]], [blocks[1], who[1]], [blocks[2], who[2]], [blocks[3], who[3]], tot])

    def funnel(self):
        O = R["odds"]
        reach = O["reach"]
        labels = ["start Phase I", "start Phase II", "start Phase III", "submitted to the FDA", "approved"]
        rows = VGroup()
        for i, (lab, p) in enumerate(zip(labels, reach)):
            n = 100 * p
            dots = VGroup(*[draw.capsule(0.26, BRAND if i < 4 else LAB).move_to([-1.6 + 0.29 * (k % 25), 2.25 - 1.0 * i - 0.17 * (k // 25), 0])
                            for k in range(int(round(n)))])
            t = tx(f"{lab}: {n:.0f}", 16, WHITE, bold=True).move_to([-3.8, 2.0 - 1.0 * i, 0], aligned_edge=RIGHT)
            rows.add(VGroup(t, dots))
        src = source("BIO, Informa and QLS, Clinical Development Success Rates 2011-2020: phase transition success rates", size=12)
        beat(self,
             "Now follow a hundred candidate drugs into the clinic. <bookmark mark='a'/> A hundred begin Phase one. "
             f"<bookmark mark='b'/> About {100 * reach[1]:.0f} pass into Phase two. <bookmark mark='c'/> Only about "
             f"{100 * reach[2]:.0f} survive Phase two, where most drugs are shown not to work well enough. "
             f"<bookmark mark='d'/> About {100 * reach[3]:.0f} finish Phase three and are submitted to the regulator, "
             f"<bookmark mark='e'/> and about {100 * reach[4]:.0f} are approved. Ninety-two of every hundred drugs tested "
             "in people never reach a patient as a medicine. Each of the failures still cost money, years and the "
             "volunteers' and patients' time, and each taught the company something about the disease. "
             "But only the eight earn anything back.",
             base=[src], steps=list(rows))
