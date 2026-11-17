from __future__ import annotations

import numpy as np

from videos.psychology.psych6.common import *  # noqa: F403

SEROTONIN = "#5BD18B"


def badge(n: int, at, color=None) -> VGroup:
    color = color or P.ACCENT
    c = Circle(radius=0.21, color=color, stroke_width=3, fill_color="#05070B", fill_opacity=1).move_to(at)
    return VGroup(c, label(rf"{n}", font_size=24, color=color).move_to(c))


class Transmitters(VoiceoverScene):
    def construct(self):
        self.card()
        self.cast()
        self.lock()
        self.sites()

    def card(self):
        card = chapter_card(2, r"Transmitters, and where the drugs act", r"Which chemicals, and how does a drug "
                            r"interfere?", lit=(), part=PART, scale=("molecule", "neuron"), marr=("tissue",))
        with self.voiceover(
            "Chapter two. Transmitters, and where the drugs act."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def cast(self):
        head = heading(r"Seven transmitters, \ one line each")
        items = [
            (r"glutamate", EXC, r"the accelerator: \ nearly every fast excitatory synapse"),
            (r"GABA", INH, r"the brake: \ most fast inhibition"),
            (r"acetylcholine", DATA, r"nerve to muscle; \ in the brain, attention"),
            (r"dopamine", RULE, r"movement, motivation, learning from reward"),
            (r"serotonin", SEROTONIN, r"mood, sleep, appetite, and a long list besides"),
            (r"noradrenaline", THRESH, r"alertness and alarm"),
            (r"the opioids", LEAK, r"pain, and relief from it"),
        ]
        rows = VGroup()
        for name, col, what in items:
            n = label(name, font_size=36, color=col)
            w = label(what, font_size=31, color=WHITE)
            rows.add(VGroup(n, w))
        y = 2.0
        for i, r in enumerate(rows):
            if i == 2:
                y -= 0.4
            r[0].move_to([-3.6, y, 0], aligned_edge=RIGHT)
            r[1].move_to([-3.1, y, 0], aligned_edge=LEFT)
            y -= 0.78
        rows.shift(RIGHT * 0.6)
        b1 = Brace(VGroup(rows[0], rows[1]), LEFT, color=GREY_B, buff=0.2)
        b1_l = wrapped_label(r"the wiring: \ cell to cell, fast", 2.3, 26, GREY_A).next_to(b1, LEFT, buff=0.15)
        b2 = Brace(VGroup(*rows[2:]), LEFT, color=GREY_B, buff=0.2)
        b2_l = wrapped_label(r"the broadcast: \ few cells, wide reach, slow", 2.3, 26, GREY_A).next_to(
            b2, LEFT, buff=0.15)
        g = VGroup(rows, b1, b1_l, b2, b2_l)
        if g.width > 13.6:
            g.width = 13.6
        g.move_to([0, -0.35, 0])
        end = label(r"every line here is too simple", font_size=28, color=P.ACCENT).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "More than a hundred transmitters are known. Seven will carry us through this series. "
            "<bookmark mark='a'/> Two of them do most of the wiring. Glutamate is the brain's accelerator: "
            "nearly every fast excitatory synapse uses it. GABA is the brake: most fast inhibition. Between "
            "them they account for the great majority of the synapses you have. <bookmark mark='b'/> The rest "
            "work differently. Acetylcholine is what Loewi found at the heart, and it's what your nerves "
            "release onto your muscles. In the brain it has to do with attention. <bookmark mark='c'/> "
            "Dopamine: movement, motivation, and, as Part 17 will show, learning from reward. Serotonin: mood, "
            "sleep, appetite, and a long list besides. Noradrenaline: alertness and alarm. The opioids: pain, "
            "and relief from it. <bookmark mark='d'/> For each of these, the cells that make it are few, a "
            "small cluster deep in the brain, but their axons reach almost everywhere. They don't pass a "
            "message from one cell to the next. They broadcast, and what they change is how the circuits that "
            "receive them behave. <bookmark mark='e'/> One line each, and every line is too simple. We'll "
            "earn the detail as the series goes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.15), FadeIn(rows[1], shift=RIGHT * 0.15), FadeIn(b1),
                      FadeIn(b1_l))
            vo.wait_until("b")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.15))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in rows[3:]], lag_ratio=0.9), run_time=11.0)
            vo.wait_until("d")
            self.play(FadeIn(b2), FadeIn(b2_l))
            vo.wait_until("e")
            self.play(FadeIn(end))
        self.clear_scene()

    def _receptor(self, x, y, col, opened, odd=False):
        gap = 0.36 if opened else 0.06
        halves = VGroup(*[Rectangle(width=0.5, height=1.2, color=VOLT, stroke_width=3, fill_color="#1A2130",
                                    fill_opacity=1).move_to([x + s * (0.25 + gap / 2), y, 0]) for s in (-1, 1)])
        mem = VGroup(Line([x - 1.5, y, 0], [x - 0.5 - gap / 2, y, 0], color=GREY_C, stroke_width=7),
                     Line([x + 0.5 + gap / 2, y, 0], [x + 1.5, y, 0], color=GREY_C, stroke_width=7))
        cup = Arc(radius=0.3, start_angle=PI, angle=PI, color=VOLT, stroke_width=3).move_arc_center_to(
            [x, y + 0.86, 0])
        lig = VGroup(Circle(radius=0.2, color=col, stroke_width=0, fill_color=col, fill_opacity=1).move_to(
            [x, y + 0.82, 0]))
        if odd:
            lig.add(Square(side_length=0.24, color=col, stroke_width=0, fill_color=col, fill_opacity=1).move_to(
                [x + 0.2, y + 1.08, 0]))
        g = VGroup(mem, halves, cup, lig)
        if opened:
            flow = Arrow([x, y + 0.45, 0], [x, y - 1.05, 0], color=EXC, stroke_width=5, buff=0,
                         max_tip_length_to_length_ratio=0.16)
            g.add(flow)
        else:
            g.add(VGroup(Line([x - 0.2, y - 0.95, 0], [x + 0.2, y - 0.75, 0], color=GREY_B, stroke_width=4),
                         Line([x - 0.2, y - 0.75, 0], [x + 0.2, y - 0.95, 0], color=GREY_B, stroke_width=4)))
        g.lig = lig
        return g

    def lock(self):
        head = heading(r"A receptor recognizes a shape")
        y = 1.3
        cols = [(-4.5, EXC, True, False, r"the transmitter", r"fits, \ and the channel opens", r""),
                (0.0, MODEL, True, True, r"an agonist", r"another molecule that fits and opens it",
                 r"nicotine, \ morphine"),
                (4.5, BAD, False, True, r"an antagonist", r"fits, opens nothing, \ and keeps the transmitter out",
                 r"curare, \ naloxone")]
        panels = VGroup()
        for x, col, opened, odd, name, what, ex in cols:
            r = self._receptor(x, y, col, opened, odd).scale(1.2)
            txt = VGroup(label(name, font_size=34, color=col), wrapped_label(what, 4.1, 28, WHITE))
            if ex:
                txt.add(label(ex, font_size=28, color=GREY_A))
            txt.arrange(DOWN, buff=0.12).next_to(r, DOWN, buff=0.25)
            panels.add(VGroup(r, txt))
        lines = VGroup(
            wrapped_label(r"curare: \ the nerve fires, the muscle never hears it", 6.2, 28, GREY_A),
            wrapped_label(r"naloxone: \ pushes an opioid off its receptors within minutes", 6.2, 28, P.ACCENT),
        ).arrange(RIGHT, buff=0.6, aligned_edge=UP).to_edge(DOWN, buff=0.35)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "Now, drugs. A receptor recognizes its transmitter by shape, the way a lock recognizes a key. "
            "<bookmark mark='a'/> The transmitter fits, and the channel opens. <bookmark mark='b'/> But other "
            "molecules can have the right shape too. A molecule that fits the receptor and opens it, as the "
            "transmitter would, is called an agonist. Nicotine is one, at a receptor for acetylcholine. "
            "Morphine is one, at the receptors for your own opioids. <bookmark mark='c'/> A molecule that fits "
            "and does nothing is an antagonist. It just sits there, and while it sits there, the real "
            "transmitter can't get in. <bookmark mark='d'/> Curare, the arrow poison of South American "
            "hunters, is an antagonist at the receptor on muscle. The nerve fires, the acetylcholine is "
            "released, and the muscle never hears it. <bookmark mark='e'/> And antagonists save lives. "
            "Naloxone fits the opioid receptor tightly and opens nothing. Given to someone who has stopped "
            "breathing after an overdose, it pushes the drug off its receptors within minutes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(panels[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(panels[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(panels[2], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(lines[0]))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
        self.clear_scene()

    def sites(self):
        head = heading(r"Six places for a drug to act")
        cx = -4.2
        axon = VGroup(Line([cx - 0.4, 2.9, 0], [cx - 0.4, 1.85, 0], color=VOLT, stroke_width=4),
                      Line([cx + 0.4, 2.9, 0], [cx + 0.4, 1.85, 0], color=VOLT, stroke_width=4))
        bulb = RoundedRectangle(width=3.4, height=1.9, corner_radius=0.5, color=VOLT, stroke_width=4,
                                fill_color="#111722", fill_opacity=1).move_to([cx, 0.95, 0])
        post = RoundedRectangle(width=4.2, height=1.5, corner_radius=0.4, color=VOLT, stroke_width=4,
                                fill_color="#111722", fill_opacity=1).move_to([cx, -1.45, 0])
        ves = VGroup(*[VGroup(Circle(radius=0.2, color=EXC, stroke_width=3).move_to([cx + dx, y, 0]),
                              Dot([cx + dx, y, 0], radius=0.05, color=EXC))
                       for dx, y in ((-0.9, 1.35), (0.0, 1.45), (0.9, 1.35), (-0.45, 0.45), (0.5, 0.42))])
        rx = [-1.2, -0.4, 0.4, 1.2]
        recs = VGroup(*[Rectangle(width=0.3, height=0.34, color=EXC, stroke_width=3, fill_color="#111722",
                                  fill_opacity=1).move_to([cx + x, -0.72, 0]) for x in rx])
        pump = Rectangle(width=0.18, height=0.46, stroke_width=0, fill_color=INH, fill_opacity=1).move_to(
            [cx + 1.7, 0.45, 0])
        free = VGroup(*[Dot([cx + x, -0.25 + 0.08 * ((i * 7) % 3 - 1), 0], radius=0.05, color=EXC)
                        for i, x in enumerate(np.linspace(-1.3, 1.3, 9))])
        back = CurvedArrow([cx + 1.45, -0.25, 0], [cx + 1.95, 0.4, 0], angle=PI / 2.5, color=INH, stroke_width=3,
                           tip_length=0.14)
        drawing = VGroup(axon, bulb, post, ves, recs, pump, free, back)
        marks = VGroup(badge(1, [cx - 1.25, 2.1, 0]), badge(2, [cx - 1.95, 0.2, 0]), badge(3, [cx - 1.2, -1.25, 0]),
                       badge(4, [cx - 0.4, -1.25, 0]), badge(5, [cx + 0.4, -1.25, 0]), badge(6, [cx + 2.35, 0.1, 0]))
        VGroup(drawing, marks).scale(1.25).move_to([-3.9, -0.4, 0])
        entries = [
            (r"the supply", r"L-DOPA, \ the raw material for dopamine"),
            (r"the release", r"botulinum toxin stops vesicles fusing"),
            (r"the receptor, opened", r"agonists: \ nicotine, morphine"),
            (r"the receptor, blocked", r"antagonists: \ caffeine, antipsychotics, naloxone"),
            (r"the receptor, helped", r"benzodiazepines, and in part alcohol, at GABA's"),
            (r"the clearing", r"SSRIs, cocaine; \ nerve agents block the enzyme"),
        ]
        rows = VGroup()
        for i, (where, what) in enumerate(entries, 1):
            b = badge(i, ORIGIN)
            t = VGroup(label(where, font_size=30, color=P.ACCENT), label(what, font_size=27, color=WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.05)
            rows.add(VGroup(b, t).arrange(RIGHT, buff=0.25))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.27).move_to([3.3, -0.3, 0])
        keep_in_frame(rows)
        tag = note(r"schematic").to_corner(DR, buff=0.2)
        with self.voiceover(
            "A drug doesn't have to act at the receptor. Go back through the steps of the synapse, and every "
            "one of them is a place to interfere. <bookmark mark='a'/> The supply. In Parkinson's disease the "
            "cells that make dopamine die. L-DOPA is the raw material, given so that the cells that remain "
            "can make more. <bookmark mark='b'/> The release. Botulinum toxin stops vesicles of acetylcholine "
            "from fusing, and the muscle goes slack. <bookmark mark='c'/> The receptor, opened by an agonist. "
            "<bookmark mark='d'/> Or blocked by an antagonist. Caffeine is one: it blocks the receptor for "
            "adenosine, a chemical that builds up while you're awake and makes you sleepy. The antipsychotic "
            "drugs block a receptor for dopamine. <bookmark mark='e'/> A receptor can also be helped. The "
            "benzodiazepines, and in part alcohol, bind beside GABA on its receptor and make it work better. "
            "More brake. <bookmark mark='f'/> And the clearing. Block the pump that takes serotonin back up, "
            "and it lingers in the cleft: that's an SSRI. Block the pump for dopamine: that's cocaine. Block "
            "the enzyme that destroys acetylcholine, and muscles can't stop contracting: that's a nerve "
            "agent. <bookmark mark='g'/> Most of psychopharmacology is on this one diagram. Chapter thirteen "
            "comes back to it, and asks what these drugs do to a person."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(drawing))
            for i, mark_ in enumerate("abcdef"):
                vo.wait_until(mark_)
                self.play(FadeIn(marks[i], scale=1.5), FadeIn(rows[i], shift=RIGHT * 0.15))
            vo.wait_until("g")
            self.play(Indicate(marks, color=WHITE, scale_factor=1.15))
        self.clear_scene()
