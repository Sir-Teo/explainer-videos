from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


def _synapse(center) -> VGroup:
    """A synapse, drawn: the sending terminal with its vesicles and a pump, the gap with transmitter in it, and the
    receiving cell with four receptors.  ``.receptors``, ``.pump``, ``.dots``."""
    c = np.asarray(center, float)
    term = RoundedRectangle(width=3.6, height=1.7, corner_radius=0.35, color=VOLT, stroke_width=3, fill_color=VOLT,
                            fill_opacity=0.06).move_to(c + UP * 1.75)
    ves = VGroup(*[Circle(radius=0.2, color=VOLT, stroke_width=2).move_to(term.get_center() + np.array([x, y, 0]))
                   for x, y in ((-0.95, 0.15), (-0.3, -0.3), (0.35, 0.2), (0.95, -0.25))])
    for v in ves:
        v.add(*[Dot(v.get_center() + 0.08 * np.array([np.cos(a), np.sin(a), 0]), radius=0.035, color=VOLT)
                for a in (0.5, 2.6, 4.7)])
    post = RoundedRectangle(width=4.0, height=1.3, corner_radius=0.3, color=VOLT, stroke_width=3, fill_color=VOLT,
                            fill_opacity=0.06).move_to(c + DOWN * 1.75)
    rec = VGroup()
    for x in (-1.35, -0.45, 0.45, 1.35):
        base = post.get_top() + np.array([x, 0, 0])
        cup = VMobject(color=CLOCKC, stroke_width=4).set_points_as_corners(
            [base + np.array([-0.2, 0.3, 0]), base + np.array([-0.2, 0.02, 0]), base + np.array([0.2, 0.02, 0]),
             base + np.array([0.2, 0.3, 0])])
        rec.add(cup)
    g = np.random.default_rng(4)
    dots = VGroup(*[Dot(c + np.array([g.uniform(-1.5, 1.5), g.uniform(-0.45, 0.6), 0]), radius=0.06, color=VOLT)
                    for _ in range(12)])
    pump = VGroup(Rectangle(width=0.34, height=0.5, color=SLEEPC, stroke_width=3, fill_color=SLEEPC, fill_opacity=0.3),
                  Arrow(DOWN * 0.45, UP * 0.3, buff=0, color=SLEEPC, stroke_width=4, max_tip_length_to_length_ratio=0.35))
    pump.move_to(term.get_bottom() + RIGHT * 1.45 + DOWN * 0.02)
    out = VGroup(term, ves, post, rec, dots, pump)
    out.receptors, out.pump, out.dots, out.term, out.post = rec, pump, dots, term, post
    return out


class Synapse(VoiceoverScene):
    def construct(self):
        self.card()
        self.four()
        self.caffeine()
        self.gap()

    def card(self):
        card = chapter_card(9, r"Four ways to change a synapse", r"Where does a drug act?", lit=(), part=PART,
                            scale=("molecule", "neuron"), marr=("how", "tissue"))
        with self.voiceover(
            "Chapter nine. Four ways to change a synapse."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def four(self):
        head = heading(r"A drug has four places to act")
        syn = _synapse([-4.6, -0.25, 0])
        r = syn.receptors
        labs = VGroup(label(r"sending cell", font_size=24, color=GREY_A).next_to(syn.term, UP, buff=0.08),
                      label(r"receiving cell", font_size=24, color=GREY_A).next_to(syn.post, DOWN, buff=0.08))
        m1 = VGroup(Dot(r[0].get_center() + DOWN * 0.02, radius=0.13, color=DRUG),
                    label(r"1", font_size=28, color=DRUG).next_to(r[0], UP, buff=0.1))
        m2 = VGroup(Square(side_length=0.26, stroke_width=0, fill_color=OPP, fill_opacity=1).move_to(r[1].get_center()
                                                                                                    + DOWN * 0.02),
                    label(r"2", font_size=28, color=OPP).next_to(r[1], UP, buff=0.1))
        m3 = VGroup(Cross(syn.pump[0], stroke_color=BAD, stroke_width=5, scale_factor=1.3),
                    label(r"3", font_size=28, color=BAD).next_to(syn.pump, RIGHT, buff=0.12))
        m4 = VGroup(label(r"$+$", font_size=44, color=LIGHTC).move_to(r[3].get_center() + UP * 0.02),
                    label(r"4", font_size=28, color=LIGHTC).next_to(r[3], UP, buff=0.1))
        items = [
            (r"1. \ mimic the transmitter", DRUG, r"nicotine, at acetylcholine's receptors; \ morphine, at the receptors for "
                                                  r"the body's own opioids"),
            (r"2. \ block the receptor", OPP, r"caffeine, at adenosine's receptors; \ naloxone, at the opioid receptors: \ "
                                              r"it reverses an overdose in minutes"),
            (r"3. \ keep the transmitter in the gap", BAD, r"the commonest antidepressants block the pump that takes "
                                                           r"serotonin back; \ cocaine does it for dopamine"),
            (r"4. \ turn the receptor up", LIGHTC, r"alcohol, and the sedatives called benzodiazepines, \ at the receptors "
                                                   r"for GABA, the brain's main signal for inhibition"),
        ]
        rows = VGroup()
        for name, col, what in items:
            rows.add(VGroup(label(name, font_size=33, color=col), wrapped_label(what, 7.6, 29, WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([2.85, -0.25, 0])
        keep_in_frame(rows)
        tag = note(r"a diagram; \ the drugs' actions as the textbooks give them").to_corner(DR, buff=0.3)
        with self.voiceover(
            "A drug that changes the mind has to change the brain, and for nearly all of them that means "
            "changing a synapse. Here's Part 6's synapse again. <bookmark mark='a'/> The sending cell "
            "releases a transmitter into the gap. The transmitter binds to receptors on the receiving "
            "cell. And then it's cleared away, mostly by pumps that carry it back into the cell it came "
            "from. That gives a drug four places to act. <bookmark mark='b'/> One. It can mimic the "
            "transmitter, and switch the receptor on by itself. Nicotine does that, at the receptors for "
            "acetylcholine. Morphine does it at the receptors for the body's own opioids. "
            "<bookmark mark='c'/> Two. It can sit in the receptor and do nothing, which keeps the "
            "transmitter out. Caffeine does that, at the receptors for adenosine. Naloxone does it at the "
            "opioid receptors, which is how it reverses an overdose within minutes. <bookmark mark='d'/> "
            "Three. It can keep the transmitter in the gap, by blocking the pump. The commonest "
            "antidepressants do that for serotonin. Cocaine does it for dopamine. <bookmark mark='e'/> "
            "Four. It can leave the transmitter alone and turn the receptor up, so that the same signal "
            "counts for more. Alcohol does that, among other things, and so do the sedatives called "
            "benzodiazepines. Their receptor is the one for GABA, the brain's main signal for inhibition."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(syn.term), FadeIn(syn[1]), FadeIn(syn.post), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(syn.dots, lag_ratio=0.1), run_time=1.5)
            self.play(FadeIn(syn.receptors, lag_ratio=0.2), run_time=1.5)
            self.wait(1.5)
            self.play(FadeIn(syn.pump))
            for mark_, m, row in zip("bcde", (m1, m2, m3, m4), rows):
                vo.wait_until(mark_)
                self.play(FadeIn(m, scale=1.4), FadeIn(row, shift=RIGHT * 0.15))
        self.clear_scene()

    def caffeine(self):
        s, c = load("sleep"), load("dose")
        t = s["t"]
        k = (t >= 72 + s["rise"]) & (t <= 72 + s["bed"])
        hours, S = t[k], s["S"][k]
        level = np.interp(hours - 72, c["caf_t"], c["caf"]) / c["caf_peak"]
        felt = S * (1 - 0.55 * level)
        head = heading(r"Caffeine covers the gauge")
        A = axes([78, 96], [0, 0.75], x_length=7.4, y_length=4.2, xticks=[], yticks=[],
                 xlabel=r"a waking day; \ coffee at 8:00, 13:00 and 16:00", ylabel=r"", center=[-3.05, -0.35, 0])
        ax = A.ax
        A.add(hour_labels(ax, [80, 84, 88, 92, 96], 0))
        real = curve(ax, hours, S, SLEEPC, stroke_width=4.5)
        read = curve(ax, hours, felt, DRUG, stroke_width=4.5)
        cups = VGroup(*[Triangle(color=DRUG, fill_color=DRUG, fill_opacity=1).scale(0.1).rotate(PI).move_to(ax.c2p(72 + h, 0.04))
                        for h in (8, 13, 16)])
        rl = label(r"the pressure to sleep", font_size=27, color=SLEEPC).next_to(ax.c2p(86.5, float(np.interp(86.5, hours, S))),
                                                                                 UL, buff=0.1)
        fl = label(r"the pressure as the brain reads it", font_size=27, color=DRUG).move_to(ax.c2p(90.2, 0.13))
        rows = rows_of([
            (r"adenosine builds up through the waking day; \ its receptors are how the brain reads the pressure", SLEEPC),
            (r"caffeine blocks them: \ the pressure climbs as before, \ and is not read", DRUG),
            (r"no energy is given, \ and no sleep is paid off", WHITE),
            (r"when the caffeine clears, \ the pressure is all still there", THRESH),
        ], 4.9, 28, 0.28).move_to([4.4, -0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: Psyche; \ the size of the masking is an illustration")
        with self.voiceover(
            "Take caffeine, because you probably have. Chapter four said that one carrier of sleep "
            "pressure is adenosine, building up in the brain through the waking day. Adenosine's "
            "receptors are how the brain reads the pressure. <bookmark mark='a'/> Caffeine blocks them. "
            "So the pressure goes on climbing exactly as before, and the brain can't read it. "
            "<bookmark mark='b'/> That's the whole trick. Caffeine doesn't give you energy, and it "
            "doesn't pay off any sleep. It covers the gauge. <bookmark mark='c'/> And when the caffeine "
            "has cleared, the pressure is all still there, which is the slump you know. The size of the "
            "effect in this picture is an illustration. The logic isn't."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(real), FadeIn(rl), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(cups, lag_ratio=0.3), Create(read), FadeIn(fl), FadeIn(rows[1]), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def gap(self):
        head = heading(r"Where a drug starts is not where it ends")
        line = Line([-5.6, 0.9, 0], [5.6, 0.9, 0], color=GREY_B, stroke_width=3)
        marks = VGroup()
        for x, name in ((-4.6, r"the first dose"), (-2.2, r"hours"), (0.6, r"days"), (4.2, r"weeks")):
            marks.add(VGroup(Line([x, 0.78, 0], [x, 1.02, 0], color=GREY_B, stroke_width=3),
                             label(name, font_size=27, color=GREY_A).next_to([x, 0.78, 0], DOWN, buff=0.12)))
        a = VGroup(Dot([-2.2, 0.9, 0], radius=0.13, color=DRUG),
                   wrapped_label(r"the pump is blocked", 3.2, 30, DRUG).next_to([-2.2, 1.05, 0], UP, buff=0.2))
        b = VGroup(Dot([4.2, 0.9, 0], radius=0.13, color=THRESH),
                   wrapped_label(r"mood lifts, \ if it lifts", 3.2, 30, THRESH).next_to([4.2, 1.05, 0], UP, buff=0.2))
        q = label(r"what happens in between is not settled", font_size=29, color=BAD).move_to([1.0, 2.55, 0])
        rows = rows_of([
            (r"``this drug raises this chemical, \ so the chemical was too low'' does not follow; \ for depression that "
             r"simple story has not held up well", WHITE),
            (r"the receptor tells you where a drug starts. \ The rest is Parts 40 to 42", THRESH),
        ], 12.2, 30, 0.3).move_to([0, -1.75, 0])
        tag = note(r"a diagram").to_corner(DR, buff=0.3)
        with self.voiceover(
            "One warning, before the arithmetic. Knowing where a drug acts isn't knowing what it does to "
            "a mind. <bookmark mark='a'/> An antidepressant of the common kind blocks its pump within "
            "hours of the first dose. <bookmark mark='b'/> If mood lifts, it lifts after weeks. "
            "<bookmark mark='c'/> Something slow happens in between, and what it is hasn't been settled. "
            "<bookmark mark='d'/> So the tidy story, this drug raises this chemical, so this chemical "
            "must have been too low, doesn't follow. For depression, that simple story hasn't held up "
            "well, and the argument belongs to Parts 40 and 42. For today: the receptor tells you where "
            "a drug starts. It doesn't tell you where it ends."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(line), FadeIn(marks))
            vo.wait_until("a")
            self.play(FadeIn(a, scale=1.2))
            vo.wait_until("b")
            self.play(FadeIn(b, scale=1.2))
            vo.wait_until("c")
            self.play(FadeIn(q))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            self.wait(6.0)
            self.play(FadeIn(rows[1], shift=UP * 0.1))
        self.clear_scene()
