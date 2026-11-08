from __future__ import annotations

from videos.philosophy.philosophy4.common import *  # noqa: F403


class Tense(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"The logic of time", r"Is tomorrow's sea battle true today?", lit=(1957,),
                            part=PART)
        with self.voiceover("Chapter eleven. The logic of time."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.prior()
        self.shapes()
        self.branching()
        self.table()

    def prior(self):
        hc = history_card(1957, r"Arthur Prior", r"\textit{Time and Modality}: \ tense logic", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        ops = VGroup(
            VGroup(MathTex(r"\mathsf{F}\,p", font_size=40, color=GOAL), label(r"it will at some time be that $p$",
                                                                              font_size=24)),
            VGroup(MathTex(r"\mathsf{G}\,p", font_size=40, color=GOAL), label(r"it will always be that $p$",
                                                                              font_size=24)),
            VGroup(MathTex(r"\mathsf{P}\,p", font_size=40, color=P.AGENT), label(r"it was at some time that $p$",
                                                                                 font_size=24)),
            VGroup(MathTex(r"\mathsf{H}\,p", font_size=40, color=P.AGENT), label(r"it has always been that $p$",
                                                                                 font_size=24))).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3)
        for r in ops:
            r.arrange(RIGHT, buff=0.5)
        ops.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        ops.move_to([-2.6, -0.5, 0])
        line = NumberLine(x_range=[0, 8, 1], length=5.0, include_numbers=False, color=GREY_B).move_to([3.6, -0.5, 0])
        now = Dot(line.n2p(3), color=WORLD, radius=0.1)
        nl = label(r"now", font_size=22, color=WORLD).next_to(now, DOWN, buff=0.2)
        fut = Arrow(line.n2p(3) + UP * 0.4, line.n2p(7.5) + UP * 0.4, buff=0, color=GOAL, stroke_width=3)
        past = Arrow(line.n2p(3) + UP * 0.8, line.n2p(0.5) + UP * 0.8, buff=0, color=P.AGENT, stroke_width=3)
        with self.voiceover(
            "Arthur Prior, a New Zealand logician, founded tense logic in the 1950s, inspired partly by Diodorus. "
            "<bookmark mark='a'/>Its operators: F p, it will at some time be that p; G p, it will always be that p; "
            "<bookmark mark='b'/>and their mirror images for the past, P and H. <bookmark mark='c'/>In Kripke's "
            "terms, the worlds are moments, and the arrows point to later moments: G is a box over the future, and H "
            "a box over the past, using the arrows backwards."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(ops[0]), FadeIn(ops[1]))
            vo.wait_until("b")
            self.play(FadeIn(ops[2]), FadeIn(ops[3]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(now), FadeIn(nl), GrowArrow(fut), GrowArrow(past))
        self.clear_scene()

    def shapes(self):
        head = label(r"The shape of time, axiom by axiom", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        rows = [(r"\mathsf{G}p \to \mathsf{GG}p", r"transitive: \ later than later is later"),
                (r"\mathsf{G}p \to \mathsf{F}p", r"no last moment"),
                (r"\mathsf{F}p \to \mathsf{FF}p", r"dense: \ between any two moments, another"),
                (r"\mathsf{F}p \land \mathsf{F}q \to \mathsf{F}(p \land q) \lor \mathsf{F}(p \land \mathsf{F}q) \lor "
                 r"\mathsf{F}(\mathsf{F}p \land q)", r"linear: \ no branching into the future")]
        tab = VGroup()
        for f, t in rows:
            tab.add(VGroup(MathTex(f, font_size=32, color=GOAL), label(t, font_size=24, color=GREY_A)))
        for r in tab:
            r.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        tab.arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.5)
        q = label(r"is the future linear? \ physics and free will disagree", font_size=26, color=BAD).to_edge(
            DOWN, buff=0.5)
        with self.voiceover(
            "As with necessity, each axiom fixes a shape of time. <bookmark mark='a'/>'Always in the future p' "
            "implies 'always always p': time is transitive. <bookmark mark='b'/>'Always p' implies 'sometime p': "
            "there is no last moment. <bookmark mark='c'/>Density: between any two moments there is another. "
            "<bookmark mark='d'/>And this long axiom says the future does not branch: of any two future events, one "
            "comes first, or they coincide. <bookmark mark='e'/>Is the future linear? That is exactly Aristotle's "
            "question about the sea battle."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", tab):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(FadeIn(q))
        self.clear_scene()

    def branching(self):
        t0 = Dot([-5.2, -0.2, 0], radius=0.12, color=WORLD)
        t1 = Dot([-1.0, 1.4, 0], radius=0.12, color=OK)
        t2 = Dot([-1.0, -1.8, 0], radius=0.12, color=BAD)
        h1 = Line(t0.get_center(), t1.get_center(), color=OK, stroke_width=4)
        h2 = Line(t0.get_center(), t2.get_center(), color=BAD, stroke_width=4)
        ext1 = DashedLine(t1.get_center(), t1.get_center() + RIGHT * 2.0, color=OK)
        ext2 = DashedLine(t2.get_center(), t2.get_center() + RIGHT * 2.0, color=BAD)
        lb = VGroup(label(r"today", font_size=24, color=GREY_A).next_to(t0, DOWN, buff=0.2),
                    label(r"history $h_1$: \ a sea battle tomorrow", font_size=24, color=OK).next_to(ext1, RIGHT,
                                                                                                buff=0.2),
                    label(r"history $h_2$: \ none", font_size=24, color=BAD).next_to(ext2, RIGHT, buff=0.2))
        rd = VGroup(label(r"Peircean: \ $\mathsf{F}p$ \ = \ on \textit{every} history, a battle", font_size=26,
                          color=P.CLAIM),
                    label(r"Ockhamist: \ $\mathsf{F}p$ is true or false \textit{relative to a history}", font_size=26,
                          color=P.AGENT)).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Prior's answer to Aristotle was to let the future branch. <bookmark mark='a'/>Today, two histories "
            "continue: in one there is a sea battle tomorrow, in the other there is not. <bookmark mark='b'/>Now "
            "'there will be a sea battle' can be read two ways. Prior called them Peircean and Ockhamist, after "
            "Charles Peirce and William of Ockham. The Peircean reading: it will be, on every history. "
            "<bookmark mark='c'/>The Ockhamist reading: the sentence is true or false only relative to a history, a "
            "complete way the future might go."
        ) as vo:
            self.play(FadeIn(t0), Create(h1), Create(h2), FadeIn(t1), FadeIn(t2), Create(ext1), Create(ext2),
                      FadeIn(lb))
            vo.wait_until("a")
            vo.wait_until("b")
            self.play(FadeIn(rd[0]))
            vo.wait_until("c")
            self.play(FadeIn(rd[1]))
        self.clear_scene()

    def table(self):
        d = load("seabattle")
        hd = [label(t, font_size=24, color=P.CLAIM) for t in (r"sentence, today", r"Peircean", r"Ockham: $h_1$",
                                                              r"Ockham: $h_2$")]
        rows = []
        for r in d["rows"]:
            f = MathTex(r["s"].replace("F ", r"\mathsf{F}\,").replace("~", r"\lnot ").replace("|", r"\lor"),
                        font_size=30)
            rows.append([f, tv(r["peirce"]), tv(r["ockham"]["h1"]), tv(r["ockham"]["h2"])])
        grid = ValueGrid(hd, rows, col_w=[3.6, 2.2, 2.2, 2.2], cell_h=0.58, font_size=26).move_to([0, 0.7, 0])
        notes = VGroup(label(r"Peircean: \ `battle' and `no battle' both false today, \ yet `battle or no battle' "
                             r"true: \ Aristotle's reading", font_size=22, color=GREY_A),
                       label(r"Ockhamist: \ bivalence holds on each history; \ what is open is which history is ours",
                             font_size=22, color=GREY_A),
                       label(r"divine foreknowledge and the open future: \ Part 23", font_size=22, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The Reasoner evaluated four sentences today on the two-branch tree. <bookmark mark='a'/>On the "
            "Peircean reading, 'there will be a battle' is false, since one history has none, and 'there will be no "
            "battle' is also false. <bookmark mark='b'/>Their disjunction is false too, but 'there will be: a battle "
            "or none' is true. That is close to Aristotle's own view: the future disjunction is necessary, and "
            "neither disjunct is yet true. <bookmark mark='c'/>On the Ockhamist reading, every sentence has a truth "
            "value on each history: on the first, 'there will be a battle' is true; on the second, false. What is "
            "open is only which history is ours. <bookmark mark='d'/>The choice matters for free will, and for the "
            "old puzzle of divine foreknowledge, which returns in Part 23."
        ) as vo:
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][0]) for r in range(len(rows))])
            vo.wait_until("a")
            self.play(*[FadeIn(grid.cell[r][1]) for r in (0, 1)])
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[r][1]) for r in (2, 3)], FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[r][c]) for r in range(len(rows)) for c in (2, 3)], FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.clear_scene()
