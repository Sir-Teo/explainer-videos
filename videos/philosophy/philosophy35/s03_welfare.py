from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Welfare(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"What is good for a person?", r"Is a good life a pleasant life?", lit=(1974,),
                            part=PART)
        with self.voiceover("Chapter two. What is good for a person?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.theories()
        self.machine()
        self.sour()

    def theories(self):
        head = label(r"Three theories of well-being \ (Parfit, \ 1984)", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.35)
        rows = [(r"hedonism", r"a life goes well to the extent that it contains pleasure and lacks pain \ (Bentham; \ "
                              r"Crisp)", GOOD),
                (r"desire satisfaction", r"to the extent that one gets what one wants, \ or would want if fully "
                                         r"informed \ (Brandt; \ Railton)", AGG),
                (r"objective list", r"to the extent that it contains goods worth having whether or not one wants them: "
                                    r"\ knowledge, \ friendship, \ achievement \ (Finnis; \ Fletcher)", VIRT),
                (r"the stakes", r"utilitarianism needs a theory of welfare: \ `maximize the good' is only as clear as "
                                r"`good for'", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.4)
        with self.voiceover(
            "Consequentialism needs an account of what makes a life go well. Derek Parfit sorted the answers into "
            "three in 1984. <bookmark mark='a'/>Hedonism: a life goes well to the extent that it contains pleasure and "
            "lacks pain. <bookmark mark='b'/>Desire satisfaction: to the extent that one gets what one wants, or would "
            "want if fully informed. <bookmark mark='c'/>Objective list theories: to the extent that it contains "
            "things worth having whether or not one wants them, like knowledge, friendship and achievement. "
            "<bookmark mark='d'/>The choice matters: the instruction to maximize the good is only as clear as the "
            "theory of what is good for someone."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def machine(self):
        d = load("tetrad")
        sv = d["survey"]
        assert (sv["experience machine: no"], sv["experience machine: yes"]) == (0.769, 0.130)
        hc = history_card(1974, r"Robert Nozick", r"\textit{Anarchy, State, and Utopia}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        q = quote_card(r"Suppose there were an experience machine that would give you any experience you desired. \ "
                       r"\dots\ Should you plug into this machine for life, \ preprogramming your life's experiences?",
                       r"Nozick", r"\textit{Anarchy, State, and Utopia}, \ p.~42", width=9.4,
                       font_size=26).move_to([0, 0.9, 0])
        rows = stack([(r"we want to do things, \ not only to have the experience of doing them", VIRT),
                      (r"we want to be a certain kind of person, \ and to be in contact with reality", VIRT),
                      (r"so hedonism is false, \ if we would not plug in", HARM),
                      (r"De Brigard \ (2010): \ told they are already in a machine, \ many would stay: \ status quo "
                       r"bias?", GREY_A)], font_size=19, buff=0.22).to_edge(DOWN, buff=1.8)
        bars = VGroup()
        for k, (n, col) in enumerate((("experience machine: no", VIRT), ("experience machine: yes", GOOD))):
            w = 5.0 * sv[n]
            b = Rectangle(width=w, height=0.3, stroke_width=0, fill_color=col, fill_opacity=0.7).move_to(
                [-1.5 + w / 2, -3.05 - 0.4 * k, 0])
            bars.add(VGroup(b, label(f"{n.split(': ')[1]}: \\ {100 * sv[n]:.1f}\\%", font_size=16,
                                     color=col).next_to(b, RIGHT, buff=0.15)))
        cap = label(r"PhilPapers 2020: \ would you enter?", font_size=15, color=GREY_A).next_to(bars, LEFT, buff=0.3)
        with self.voiceover(
            "Robert Nozick posed the most famous test of hedonism in 1974. <bookmark mark='a'/>Suppose there were an "
            "experience machine that would give you any experience you desired, indistinguishable from the real "
            "thing. Should you plug in for life? <bookmark mark='b'/>Most people say no. We want to do things, not "
            "only to have the experience of doing them; <bookmark mark='c'/>we want to be a certain kind of person, "
            "and to be in contact with reality. <bookmark mark='d'/>If so, something besides experience matters, and "
            "hedonism is false. In the 2020 survey, seventy seven percent of philosophers would not enter, thirteen "
            "would. <bookmark mark='e'/>Felipe De Brigard turned the case around in 2010: told that their present "
            "life is already in a machine, many people would stay. Perhaps what the case measures is attachment to "
            "the status quo."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcd", rows[:3]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            self.play(FadeIn(cap), *[FadeIn(b) for b in bars])
            vo.wait_until("e")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def sour(self):
        d = load("adaptive")
        head = label(r"Sour grapes: \ adaptive preferences", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ds, cp = d["desire_satisfaction"], d["capability"]
        assert (d["options"], d["steps"], d["cuts"], d["adapt"]) == (10, 60, [[10, 4], [30, 4]], 0.15)
        assert (d["final"]["desire"], d["final"]["capability"], d["lowest_desire"]) == (0.9817, 0.2, 0.3249)
        ax = Axes(x_range=[0, 60, 10], y_range=[0, 1, 0.25], x_length=6.2, y_length=3.8, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True},
                  y_axis_config={"decimal_number_config": {"num_decimal_places": 2}}).move_to([-3.2, -0.6, 0])
        xl = label(r"time", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.42)
        c1 = VMobject(color=AGG, stroke_width=3).set_points_as_corners([ax.c2p(t, v) for t, v in enumerate(ds)])
        c2 = VMobject(color=VIRT, stroke_width=3).set_points_as_corners([ax.c2p(t, v) for t, v in enumerate(cp)])
        l1 = label(r"desire satisfaction", font_size=16, color=AGG).next_to(ax.c2p(60, ds[-1]), UP, buff=0.12).shift(
            LEFT * 1.0)
        l2 = label(r"options open: \ a capability index", font_size=16, color=VIRT).next_to(ax.c2p(60, cp[-1]), UP,
                                                                                             buff=0.12).shift(LEFT * 1.6)
        cuts = VGroup(*[DashedLine(ax.c2p(t, 0), ax.c2p(t, 1), color=HARM, stroke_width=1.5) for t, _ in d["cuts"]])
        cl = VGroup(*[label(r"4 options closed", font_size=14, color=HARM).next_to(ax.c2p(t, 1), UP, buff=0.08)
                      for t, _ in d["cuts"]])
        side = stack([(r"ten options, \ all equally wanted", GREY_A),
                      (r"each step, \ desire for what is out of reach shrinks by 15\%", AGG),
                      (r"after the second loss desire satisfaction falls to 0.32, \ then climbs back to 0.98", AGG),
                      (r"the capability index stays at 0.2", VIRT),
                      (r"Elster \ (1983): \ sour grapes; \ Sen; \ Nussbaum \ (2000): \ count capabilities, \ not "
                       r"only satisfied desires", GOAL)],
                     font_size=18, aligned_edge=LEFT, width=4.8, buff=0.3).move_to([4.1, -0.3, 0])
        with self.voiceover(
            "Desire theories face a problem that Jon Elster named in 1983, after Aesop's fox, who decided that the "
            "grapes he could not reach were sour anyway. <bookmark mark='a'/>The Reasoner models an agent who wants "
            "ten options equally: careers, freedoms, ways to live. At two moments, four of them are closed off. "
            "<bookmark mark='b'/>Desire for what is out of reach fades, by fifteen percent a step. "
            "<bookmark mark='c'/>Each loss knocks desire satisfaction down, after the second to a third, and each "
            "time it climbs back, to point nine eight: the agent comes to want only what she can have. "
            "<bookmark mark='d'/>Yet only two options in ten remain open. <bookmark mark='e'/>Amartya Sen observed "
            "that deprived people often come to terms with their deprivation, so that measures of satisfied desire "
            "can make injustice invisible; with Martha Nussbaum, he proposed counting capabilities, what people are "
            "actually able to do and be, as well. The fox is content, and he is still hungry."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(cuts), FadeIn(cl))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(c1), run_time=2.5)
            self.play(FadeIn(l1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(c2), run_time=1.5)
            self.play(FadeIn(l2), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
