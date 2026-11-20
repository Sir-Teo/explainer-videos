from __future__ import annotations

from videos.economics.econ44.common import *  # noqa: F403


class Innovation(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Competition and innovation", r"Does competition spur invention, or starve it?",
             "Chapter eight. Competition and innovation.",
             lit={1942: r"Schumpeter", 1962: r"Arrow", 2005: r"Aghion et al."}, scale=("firm", "market"),
             horizon=("a decade",))
        self.debate()
        self.arrow()
        self.stepwise()
        self.inverted()

    def debate(self):
        steps = flow_chain([(r"Schumpeter, \ 1942", LOSS), (r"Arrow, \ 1962", PATIENT)],
                           notes=[r"large firms with market \\ power can afford research \\ and keep its rewards",
                                  r"a monopolist gains less \\ from a new process: \\ it replaces its own profit"],
                           box_w=3.4, font_size=22, note_size=18).move_to(UP * 0.6)
        foot = label(r"two forces, \ pulling in opposite directions", font_size=22,
                     color=E.ACCENT).to_edge(DOWN, buff=1.0)
        tag = published_tag(tables.INNOVATION.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Is competition good for innovation? Two great economists disagreed. <bookmark mark='a'/> Joseph "
            "Schumpeter argued in 1942 that large firms with market power do most invention: they can afford "
            "laboratories and keep the rewards. <bookmark mark='b'/> Kenneth Arrow argued in 1962 that a monopolist "
            "gains less from a new process than a competitor does, because it is already earning a monopoly "
            "profit, which the invention merely replaces. <bookmark mark='c'/> Both forces are real."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(steps.boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(steps.notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()

    def arrow(self):
        I = load("innovation")
        N = TRUTH["innovation"]
        A = I["arrow"]
        vals = [(r"a monopolist", A["monopoly"], LOSS), (r"an innovator among \\ competitors", A["competitive"],
                                                          PATIENT), (r"society", A["planner"], GAIN)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(vals):
            y = 0.9 - 1.15 * k
            w = v * 0.35
            r = Rectangle(width=w, height=0.62, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([-0.4 + w / 2, y, 0]))
            bars.add(VGroup(label(nm, font_size=19, color=col).next_to(np.array([-0.55, y, 0]), LEFT, buff=0.1), r,
                            label(f"{v:.0f}", font_size=21, color=WHITE).next_to(r, RIGHT, buff=0.15)))
        head = label(rf"what a cost cut from {N['c']:.0f} to {N['c_new']:.0f} is worth \ (demand $P$ = "
                     rf"{N['a']:.0f} $-$ $Q$)", font_size=24, color=E.ACCENT).to_edge(UP, buff=0.5)
        foot = label(r"the replacement effect: \ the monopolist is already earning most of what the invention brings",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = published_tag(tables.INNOVATION.tag, corner=DR, font_size=11)
        with self.voiceover(
            f"Arrow's case in numbers. A new process cuts unit cost from {N['c']:.0f} to {N['c_new']:.0f}. "
            f"<bookmark mark='a'/> A monopolist's profit rises by {A['monopoly']:.0f}. <bookmark mark='b'/> A firm "
            "in a competitive industry that invents it can undercut its rivals and take the whole market at a "
            f"price just below the old cost, gaining {A['competitive']:.0f}. <bookmark mark='c'/> Society gains "
            f"{A['planner']:.0f}, more than either, because no inventor captures all the benefit. "
            "<bookmark mark='d'/> The monopolist's incentive is the weakest: it replaces a profit it already has."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(b_[0]) for b_ in bars])
            for mk, b_ in zip("abc", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b_[1], LEFT), FadeIn(b_[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def stepwise(self):
        N = TRUTH["innovation"]
        states = VGroup()
        for k, (nm, sub, col) in enumerate(((r"neck and neck", r"each earns $(1-\Delta)\pi_1$", PATIENT),
                                            (r"one leads", r"the leader earns $\pi_1$, \\ the laggard nothing",
                                             FIRM1))):
            box = RoundedRectangle(width=4.0, height=1.5, corner_radius=0.12, stroke_color=col, stroke_width=2.4,
                                   fill_color="#141821", fill_opacity=1)
            t1 = label(nm, font_size=24, color=col).move_to(box.get_top() + DOWN * 0.38)
            t2 = label(sub, font_size=18, color=GREY_A).next_to(t1, DOWN, buff=0.15)
            states.add(VGroup(box, t1, t2))
        states.arrange(RIGHT, buff=2.4).move_to(UP * 0.8)
        a1 = CurvedArrow(states[0].get_top() + RIGHT * 0.8, states[1].get_top() + LEFT * 0.8, angle=-TAU / 6,
                         color=PATIENT, stroke_width=2.4)
        a2 = CurvedArrow(states[1].get_bottom() + LEFT * 0.8, states[0].get_bottom() + RIGHT * 0.8, angle=-TAU / 6,
                         color=FIRM1, stroke_width=2.4)
        l1 = label(r"either innovates: \ escape", font_size=18, color=PATIENT).next_to(a1, UP, buff=0.1)
        l2 = label(rf"the laggard innovates \\ or imitates (rate {N['h']}): \ catch up", font_size=18,
                   color=FIRM1).next_to(a2, DOWN, buff=0.1)
        foot = label(r"more competition ($\Delta$ up): \ level firms run harder to escape; \ laggards see less "
                     r"reward for catching up", font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.45)
        tag = published_tag(tables.INNOVATION.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Philippe Aghion and his coauthors put both forces in one model of step-by-step innovation. "
            "<bookmark mark='a'/> An industry is either neck and neck, where the two firms' products are equal "
            "and competition, measured by delta, eats into their profits, <bookmark mark='b'/> or one firm leads "
            "and earns the leader's profit, while the laggard earns nothing. <bookmark mark='c'/> Level firms "
            "innovate to escape competition and become the leader. <bookmark mark='d'/> Laggards innovate, or "
            "imitate, to catch up. <bookmark mark='e'/> Tougher competition makes level firms run harder, the "
            "escape-competition effect, but leaves a laggard less to gain from catching up, Schumpeter's effect."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(states[0]), FadeIn(states[1]), run_time=1.2)
            vo.wait_until("a")
            self.play(Indicate(states[0], color=WHITE, scale_factor=1.04))
            vo.wait_until("b")
            self.play(Indicate(states[1], color=WHITE, scale_factor=1.04))
            vo.wait_until("c")
            self.play(Create(a1), FadeIn(l1))
            vo.wait_until("d")
            self.play(Create(a2), FadeIn(l2))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def inverted(self):
        I = load("innovation")
        ax = plane([0, 1], [0, 1.1], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"competition, \ $\Delta$", ylabel=r"innovation across all industries",
                   xfmt=lambda v: f"{v:.2f}", yfmt=lambda v: f"{v:.2f}", font_size=14)
        ln = path(ax, I["delta"], I["innovation"], GAIN, 3.4)
        n0 = path(ax, I["delta"], np.array(I["n0"]) / 1.4, PATIENT, 2.0)
        nm = path(ax, I["delta"], np.array(I["nm"]) / 1.4, FIRM1, 2.0)
        pk = VGroup(vline(ax, I["peak"], 0, 1.1, GAIN), dot(ax, I["peak"], I["peak_value"], GAIN, 0.09))
        side = VGroup(
            label(r"teal: \ level firms' \\ effort rises \\ (rescaled)", font_size=18, color=PATIENT),
            label(r"gold: \ laggards' \\ effort falls \\ (rescaled)", font_size=18, color=FIRM1),
            label(rf"green: \ the total \\ peaks at $\Delta$ = {I['peak']:.1f}", font_size=18, color=GAIN),
            label(r"Aghion et al.: \ British \\ industries' patents \\ trace an inverted U", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.INNOVATION.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Solve the model on the Island for every level of competition. <bookmark mark='a'/> Level firms' "
            "innovation rises with competition. <bookmark mark='b'/> Laggards' falls. <bookmark mark='c'/> And "
            "because tougher competition also means more industries spend time with a leader and a laggard, "
            "total innovation first rises and then falls: an inverted U, peaking at moderate competition. "
            "<bookmark mark='d'/> In 2005 Aghion, Nicholas Bloom, Richard Blundell, Rachel Griffith and Peter "
            "Howitt found that shape in the patents of British industries. Neither Schumpeter nor Arrow was simply "
            "right; the answer depends on where an industry starts."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(n0), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(nm), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(pk), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
