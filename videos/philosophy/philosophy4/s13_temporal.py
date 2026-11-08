from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


def path(labels, y=0.0, x0=-5.6, dx=1.4, color=WORLD):
    """A run of a system: states left to right, each with the atoms true there."""
    g = VGroup()
    dots = VGroup()
    for i, lab in enumerate(labels):
        d = Circle(radius=0.3, stroke_color=color, stroke_width=2.5, fill_color="#0B0F17", fill_opacity=1).move_to(
            [x0 + i * dx, y, 0])
        t = MathTex(lab if lab else r"\cdot", font_size=22, color=PROP if lab else GREY_C).move_to(d)
        dots.add(VGroup(d, t))
    arrows = VGroup(*[Arrow(dots[i].get_right(), dots[i + 1].get_left(), buff=0.05, color=ACC, stroke_width=2.5,
                            max_tip_length_to_length_ratio=0.25) for i in range(len(labels) - 1)])
    more = MathTex(r"\cdots", font_size=34, color=GREY_B).next_to(dots, RIGHT, buff=0.3)
    g.add(arrows, dots, more)
    g.dots = dots
    return g


class Temporal(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Temporal logic for machines", r"How do you specify what a program must never do?",
                            lit=(1977,), part=PART)
        with self.voiceover("Chapter twelve. Temporal logic for machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.pnueli()
        self.operators()
        self.safety_liveness()
        self.ctl()
        self.automata()

    def pnueli(self):
        hc = history_card(1977, r"Amir Pnueli", r"`The temporal logic of programs': \ Prior's logic, for computers",
                          width=6.6, color=HIST).to_corner(UL, buff=0.35)
        why = VGroup(label(r"a program that runs forever: \ an operating system, a network protocol, a pacemaker",
                           font_size=24),
                     label(r"its correctness is not an output, \ but a pattern of behaviour over time", font_size=26,
                           color=GOAL)).arrange(DOWN, buff=0.3).move_to([0, -0.4, 0])
        award = label(r"Turing Award 1996", font_size=22, color=GREY_A).next_to(hc, RIGHT, buff=0.4)
        with self.voiceover(
            "In 1977 Amir Pnueli, an Israeli computer scientist, saw that Prior's tense logic was exactly what "
            "programmers needed. <bookmark mark='a'/>Many programs are never supposed to stop: an operating system, "
            "a network protocol, a pacemaker. <bookmark mark='b'/>Their correctness is not a final answer but a "
            "pattern of behaviour over time: something bad never happens, something good always eventually happens. "
            "<bookmark mark='c'/>Pnueli received the Turing Award for it in 1996."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(why[0]))
            vo.wait_until("b")
            self.play(FadeIn(why[1]))
            vo.wait_until("c")
            self.play(FadeIn(award))
        self.clear_scene()

    def operators(self):
        head = label(r"Linear temporal logic (LTL): \ formulas about one run", font_size=30, color=CONN).to_edge(
            UP, buff=0.4)
        rows = [(r"\mathsf{X}\,p", r"next state: $p$", ["", "p", "", "", "", ""], 1),
                (r"\mathsf{F}\,p", r"eventually: $p$", ["", "", "", "p", "", ""], 3),
                (r"\mathsf{G}\,p", r"always: $p$", ["p", "p", "p", "p", "p", "p"], None),
                (r"p\ \mathsf{U}\ q", r"$p$ until $q$", ["p", "p", "p", "q", "", ""], 3)]
        grp = VGroup()
        for i, (f, t, labs, hi) in enumerate(rows):
            y = 1.6 - 1.25 * i
            fm_ = MathTex(f, font_size=34, color=GOAL).move_to([-5.6, y, 0])
            tl = label(t, font_size=20, color=GREY_A).next_to(fm_, DOWN, buff=0.08)
            p_ = path(labs, y=y, x0=-3.2, dx=1.3)
            g = VGroup(fm_, tl, p_)
            if hi is not None:
                g.add(SurroundingRectangle(p_.dots[hi], color=GOAL, buff=0.06))
            grp.add(g)
        with self.voiceover(
            "Pnueli's logic speaks about a single run of a system, an infinite sequence of states. "
            "<bookmark mark='a'/>X p: p holds in the next state. <bookmark mark='b'/>F p: p holds eventually, at "
            "some later state. <bookmark mark='c'/>G p: p holds always, at every state. <bookmark mark='d'/>And p "
            "until q: q eventually holds, and p holds at every state before that."
        ) as vo:
            self.play(FadeIn(head))
            for mk, g in zip("abcd", grp):
                vo.wait_until(mk)
                self.play(FadeIn(g, shift=RIGHT * 0.2))
        self.clear_scene()

    def safety_liveness(self):
        two = VGroup(
            VGroup(label(r"safety", font_size=32, color=BAD),
                   label(r"something bad never happens", font_size=24, color=GREY_A),
                   MathTex(r"\mathsf{G}\,\lnot(\mathit{crit}_0 \land \mathit{crit}_1)", font_size=36),
                   label(r"`never two processes in the critical section'", font_size=22, color=GREY_A),
                   label(r"refuted by a finite trace", font_size=22, color=BAD)).arrange(DOWN, buff=0.18),
            VGroup(label(r"liveness", font_size=32, color=OK),
                   label(r"something good eventually happens", font_size=24, color=GREY_A),
                   MathTex(r"\mathsf{G}\,(\mathit{try}_0 \to \mathsf{F}\,\mathit{crit}_0)", font_size=36),
                   label(r"`whoever asks to enter, eventually enters'", font_size=22, color=GREY_A),
                   label(r"refuted only by an infinite run", font_size=22, color=OK)).arrange(DOWN, buff=0.18)).arrange(
            RIGHT, buff=1.4).move_to([0, 0.3, 0])
        thm = label(r"every property of runs is a safety property and a liveness property combined \ (Alpern and "
                    r"Schneider 1985)", font_size=22, color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Two kinds of property matter most, as Leslie Lamport observed in 1977. <bookmark mark='a'/>Safety: "
            "something bad never happens. For example, two processes are never in their critical sections at the "
            "same time. A safety violation can be shown with a finite trace: here is the moment it went wrong. "
            "<bookmark mark='b'/>Liveness: something good eventually happens. Whoever asks to enter the critical "
            "section eventually gets in. A liveness violation needs an infinite run, one where the waiting never "
            "ends. <bookmark mark='c'/>Bowen Alpern and Fred Schneider proved in 1985 that every property of runs is "
            "a combination of the two."
        ) as vo:
            self.play(FadeIn(two[0]))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(two[1]))
            vo.wait_until("c")
            self.play(FadeIn(thm))
        self.clear_scene()

    def ctl(self):
        hcs = VGroup(history_card(1981, r"Clarke \& Emerson; \ Queille \& Sifakis", r"model checking: \ decide a "
                                  r"temporal formula on a finite state graph, by machine", width=7.2, color=HIST),
                     label(r"Turing Award 2007", font_size=22, color=GREY_A)).arrange(RIGHT, buff=0.4).to_edge(UP,
                                                                                                         buff=0.4)
        rows = VGroup(
            VGroup(MathTex(r"\mathsf{AG}\,\varphi", font_size=36, color=GOAL),
                   label(r"on all paths, always", font_size=24)),
            VGroup(MathTex(r"\mathsf{EF}\,\varphi", font_size=36, color=GOAL),
                   label(r"on some path, eventually: \ $\varphi$ is reachable", font_size=24)),
            VGroup(MathTex(r"\mathsf{EG}\,\varphi", font_size=36, color=GOAL),
                   label(r"some path stays in $\varphi$ forever", font_size=24))).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.3)
        for r in rows:
            r.arrange(RIGHT, buff=0.5)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        rows.move_to([-3.4, -0.4, 0])
        fix = VGroup(MathTex(r"\mathsf{EF}\,\varphi = \mu Z.\ \varphi \lor \mathsf{EX}\,Z", font_size=32),
                     label(r"least fixed point: \ add predecessors until nothing changes", font_size=22,
                           color=GREY_A),
                     MathTex(r"\mathsf{EG}\,\varphi = \nu Z.\ \varphi \land \mathsf{EX}\,Z", font_size=32),
                     label(r"greatest fixed point: \ remove states that cannot continue", font_size=22,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.65, -0.4, 0])
        with self.voiceover(
            "In 1981 Edmund Clarke and Allen Emerson, and independently Jean-Pierre Queille and Joseph Sifakis, "
            "turned this into an algorithm called model checking, and shared the Turing Award for it in 2007. "
            "<bookmark mark='a'/>Their logic, CTL, can also quantify over paths. AG phi: on every path, always phi. "
            "EF phi: on some path, eventually phi; that is, a phi-state is reachable. EG phi: some path stays in phi "
            "forever. <bookmark mark='b'/>Each is computed as a fixed point on the finite graph of the system's "
            "states. EF grows a set backwards from the target until nothing changes; EG shrinks a set until every "
            "state left can continue. Both are in the Reasoner, and the next chapter runs them on a real protocol."
        ) as vo:
            self.play(FadeIn(hcs))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(fix))
        self.clear_scene()

    def automata(self):
        hc = history_card(1986, r"Vardi \& Wolper", r"model checking with automata on infinite words", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        steps = VGroup(
            label(r"1. \ negate the property: \ `some request is never granted'", font_size=22),
            MathTex(r"\lnot\,\mathsf{G}(\mathit{try} \to \mathsf{F}\,\mathit{crit}) \;\equiv\; "
                    r"\mathsf{F}(\mathit{try} \land \mathsf{G}\,\lnot\mathit{crit})", font_size=30, color=BAD),
            label(r"2. \ build an automaton for the violating runs \ (B\"uchi 1962)", font_size=22),
            label(r"3. \ run it alongside the system: \ the product graph", font_size=22),
            VGroup(label(r"4. \ search for a reachable cycle through an accepting state", font_size=22, color=GOAL),
                   label(r"found: \ a counterexample run; \ none: \ the property holds", font_size=22,
                         color=GOAL)).arrange(DOWN, aligned_edge=LEFT, buff=0.1)).arrange(DOWN, aligned_edge=LEFT,
                                                                                          buff=0.22)
        steps.move_to([-2.9, -0.4, 0])
        q0 = Circle(radius=0.38, color=WORLD, stroke_width=3).move_to([4.4, 1.2, 0])
        q1 = VGroup(Circle(radius=0.38, color=BAD, stroke_width=3), Circle(radius=0.3, color=BAD,
                                                                             stroke_width=2)).move_to([4.4, -1.4, 0])
        l0 = MathTex(r"q_0", font_size=26).move_to(q0)
        l1 = MathTex(r"q_1", font_size=26).move_to(q1)
        e01 = Arrow(q0.get_bottom(), q1.get_top(), buff=0.05, color=ACC)
        el = MathTex(r"\mathit{try} \land \lnot\mathit{crit}", font_size=22, color=ACC).next_to(e01, RIGHT,
                                                                                               buff=0.1)
        s0 = Arc(radius=0.25, start_angle=-PI / 6, angle=4 * PI / 3, color=ACC, stroke_width=2).move_to(
            q0.get_top() + UP * 0.2)
        s1 = Arc(radius=0.25, start_angle=PI + PI / 6, angle=4 * PI / 3, color=ACC, stroke_width=2).move_to(
            q1.get_bottom() + DOWN * 0.2)
        sl0 = MathTex(r"\top", font_size=22, color=ACC).next_to(s0, UP, buff=0.05)
        sl1 = MathTex(r"\lnot\mathit{crit}", font_size=22, color=ACC).next_to(s1, DOWN, buff=0.05)
        acc = label(r"accepting: \ visited forever", font_size=20, color=BAD).next_to(q1, LEFT, buff=0.3)
        with self.voiceover(
            "Linear temporal logic has its own algorithm, found by Moshe Vardi and Pierre Wolper in 1986. "
            "<bookmark mark='a'/>Negate the property. 'Every request is eventually granted' becomes 'some request is "
            "never granted'. <bookmark mark='b'/>Build an automaton that reads a run of the system and accepts "
            "exactly the runs that violate the property. Here it waits, jumps when a request arrives that is not yet "
            "granted, and accepts if it can stay forever where the grant never comes. Such automata on infinite "
            "words were invented by Julius Büchi in 1962, to prove a logic decidable. <bookmark mark='c'/>Run the "
            "automaton alongside the system, and search the combined graph for a reachable cycle through an "
            "accepting state. If there is one, it is a counterexample run; if not, the property holds. SPIN works "
            "exactly this way."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2]), Create(q0), FadeIn(l0), Create(q1), FadeIn(l1), GrowArrow(e01), FadeIn(el),
                      Create(s0), Create(s1), FadeIn(sl0), FadeIn(sl1), FadeIn(acc))
            vo.wait_until("c")
            self.play(FadeIn(steps[3]))
            self.play(FadeIn(steps[4]))
        self.clear_scene()
