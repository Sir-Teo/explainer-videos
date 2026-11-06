from __future__ import annotations

from videos.philosophy.philosophy12.common import *  # noqa: F403

ORDER = [(0, 1, 2), (0, 2, 1), (2, 0, 1), (2, 1, 0), (1, 2, 0), (1, 0, 2)]


class Cards(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Many minds, one model", r"How do we draw what several people know?", lit=(1962,),
                            part=PART)
        with self.voiceover("Chapter two. Many minds, one model."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.model()
        self.announce()
        self.cheryl()

    def graph(self):
        d = load("cards")
        pos = {w: [2.2 * np.cos(PI / 2 - TAU * i / 6), 2.2 * np.sin(PI / 2 - TAU * i / 6), 0]
               for i, w in enumerate(ORDER)}
        edges = {ag: [(tuple(u), tuple(v)) for u, v in d["edges"][ag]] for ag in "abc"}
        labels = {w: "".join(map(str, w)) for w in ORDER}
        return d, AgentGraph(ORDER, edges, pos, labels, radius=0.42, font_size=26, center=[-3.4, -0.4, 0])

    def model(self):
        d, g = self.graph()
        head = label(r"Three cards: \ 0, \ 1, \ 2", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        key = VGroup(*[VGroup(Line(LEFT * 0.25, RIGHT * 0.25, color=AG[ag], stroke_width=5),
                              label(nm, font_size=21, color=AG[ag])).arrange(RIGHT, buff=0.15)
                       for ag, nm in (("a", r"Ann"), ("b", r"Bob"), ("c", r"Cath"))]).arrange(RIGHT, buff=0.5)
        key.next_to(g, DOWN, buff=0.3)
        world_l = label(r"world 012: \ Ann holds 0, \ Bob 1, \ Cath 2", font_size=20, color=GREY_A).next_to(
            key, DOWN, buff=0.15)
        act = Circle(radius=0.52, color=COMMON, stroke_width=3).move_to(g.world[(0, 1, 2)])
        rows = VGroup()
        for c in d["checks"]:
            rows.add(VGroup(MathTex(c["tex"], font_size=30), mark(c["value"], 30)).arrange(RIGHT, buff=0.4))
        glosses = [r"Ann knows she holds 0", r"she does not know Bob holds 1", r"she knows Bob doesn't hold 0",
                   r"she knows 1 is with Bob or Cath", r"Bob knows Ann knows she lacks 1",
                   r"Bob doesn't know whether Ann knows his card"]
        for r, gl in zip(rows, glosses):
            r.add(label(gl, font_size=19, color=GREY_A).next_to(r, DOWN, buff=0.06, aligned_edge=LEFT))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, -0.3, 0])
        with self.voiceover(
            "Hintikka's logic comes into its own with several agents. <bookmark mark='a'/>Deal three cards, zero, "
            "one and two, to Ann, Bob and Cath. There are six possible deals, six worlds; world zero one two means "
            "Ann holds zero, Bob one, Cath two. <bookmark mark='b'/>Each person sees only her own card, so she cannot "
            "tell apart two deals that give her the same card. Draw one coloured line for each such pair: blue for "
            "Ann, orange for Bob, purple for Cath. <bookmark mark='c'/>Now the Reasoner evaluates, in the actual deal, "
            "zero one two. Ann knows she holds zero. She does not know that Bob holds one: Cath might. She does know "
            "that Bob does not hold zero, and that card one is with Bob or Cath. <bookmark mark='d'/>And the logic "
            "nests. Bob knows that Ann knows she lacks card one. But Bob does not know whether Ann knows his card; in "
            "fact she doesn't, and every world Bob considers possible agrees."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(g.discs), FadeIn(world_l))
            vo.wait_until("b")
            self.play(Create(g.edges), FadeIn(key), run_time=2)
            vo.wait_until("c")
            self.play(Create(act))
            self.play(LaggedStart(*[FadeIn(r) for r in rows[:4]], lag_ratio=0.6), run_time=4)
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[4:]], lag_ratio=0.6), run_time=3)
        self.clear_scene()

    def announce(self):
        d, g = self.graph()
        after = d["after_a0"]
        head = label(r"A public announcement", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        say = label(r"Ann: \ `I hold card 0'", font_size=26, color=AG["a"]).move_to([3.4, 2.1, 0])
        keep = {tuple(w) for w in after["left"]}
        gone = [w for w in ORDER if w not in keep]
        gone_edges = [e for k, e in g.edge.items() if k[1] not in keep or k[2] not in keep]
        rows = VGroup(
            label(r"delete every world where it is false", font_size=23),
            VGroup(label(r"Bob now knows Cath holds 2", font_size=23), mark(after["b_knows_c2"], 28)).arrange(
                RIGHT, buff=0.3),
            VGroup(label(r"Cath now knows Bob holds 1", font_size=23), mark(after["c_knows_b1"], 28)).arrange(
                RIGHT, buff=0.3),
            VGroup(label(r"and it is \textit{common knowledge} that Ann holds 0", font_size=23, color=COMMON),
                   mark(after["common_a0"], 28)).arrange(RIGHT, buff=0.3),
            label(r"announcing changes the model: \ dynamic epistemic logic \ (Plaza 1989)", font_size=21,
                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Now someone speaks. <bookmark mark='a'/>Ann announces, truthfully and to everyone: I hold card zero. "
            "<bookmark mark='b'/>A public announcement deletes every world in which it is false. Four deals vanish, "
            "with their lines. <bookmark mark='c'/>In what is left, Bob knows that Cath holds two, and Cath knows "
            "that Bob holds one. <bookmark mark='d'/>And because everyone heard it, and everyone saw that everyone "
            "heard it, it is common knowledge that Ann holds zero. <bookmark mark='e'/>Speech changes the model. "
            "Jan Plaza wrote down the logic of public announcements in 1989; it is the start of dynamic epistemic "
            "logic, which we will use all through this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(say))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]), *[FadeOut(g.world[w]) for w in gone], *[FadeOut(e) for e in gone_edges])
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def cheryl(self):
        d = load("cheryl")
        head = label(r"Cheryl's birthday", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        who = label(r"Singapore and Asian Schools Math Olympiad, \ 2015", font_size=20, color=GREY_B).next_to(
            head, DOWN, buff=0.12)
        months = ["May", "June", "July", "August"]
        days = sorted({dd for _, dd in d["start"]})
        cells = {}
        grid = VGroup()
        for i, m in enumerate(months):
            ml = label(m, font_size=20, color=AG["A"]).move_to([-5.6, 1.0 - i * 0.62, 0])
            grid.add(ml)
            for mm, dd in d["start"]:
                if mm == m:
                    j = days.index(dd)
                    c = VGroup(RoundedRectangle(width=0.62, height=0.46, corner_radius=0.08, color=GREY_B),
                               label(str(dd), font_size=20)).move_to([-4.6 + j * 0.78, 1.0 - i * 0.62, 0])
                    c[1].move_to(c[0])
                    cells[(m, dd)] = c
                    grid.add(c)
        tell = VGroup(label(r"Albert is told the month", font_size=20, color=AG["A"]),
                      label(r"Bernard is told the day", font_size=20, color=AG["b"])).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.1).move_to(
            [-3.0, -1.7, 0])
        says = VGroup(
            label(r"A: \ `I don't know, \ and I know Bernard doesn't either'", font_size=21, color=AG["A"]),
            label(r"B: \ `Now I know'", font_size=21, color=AG["b"]),
            label(r"A: \ `Then I know too'", font_size=21, color=AG["A"])).arrange(DOWN, aligned_edge=LEFT,
                                                                                 buff=0.5).move_to([3.6, 0.5, 0])
        notes = VGroup(label(r"only May and June hold a unique day \ (19, 18): \ gone", font_size=18, color=GREY_A),
                       label(r"14 is shared by July and August: \ gone", font_size=18, color=GREY_A),
                       label(r"only July has one date left", font_size=18, color=GREY_A))
        for n, s_ in zip(notes, says):
            n.next_to(s_, DOWN, buff=0.1, aligned_edge=LEFT)
        ans = label(rf"the Reasoner: \ {d['after3'][0][0]}~{d['after3'][0][1]}", font_size=26, color=OK).move_to(
            [3.6, -2.4, 0])
        left = [{tuple(w) for w in d[k]} for k in ("start", "after1", "after2", "after3")]

        def drop(a, b):
            return [cells[w].animate.set_opacity(0.15) for w in a - b]
        with self.voiceover(
            "A puzzle that went round the world in 2015 is pure public announcement logic. <bookmark mark='a'/>Cheryl "
            "gives Albert and Bernard ten possible dates for her birthday. She tells Albert only the month, and "
            "Bernard only the day. <bookmark mark='b'/>Albert says: I don't know when it is, but I know that Bernard "
            "doesn't know either. For Albert to be sure of that, his month must contain no day that appears only "
            "once; May and June each contain one, nineteen and eighteen. Those months are deleted. "
            "<bookmark mark='c'/>Bernard says: now I know. So his day is not fourteen, which appears in both July and "
            "August. <bookmark mark='d'/>Albert says: then I know too. Only July has a single date left. "
            "<bookmark mark='e'/>The Reasoner runs the three announcements on the model and is left with one world: "
            "July the sixteenth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(who))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(tell))
            vo.wait_until("b")
            self.play(FadeIn(says[0]), FadeIn(notes[0]))
            self.play(*drop(left[0], left[1]))
            vo.wait_until("c")
            self.play(FadeIn(says[1]), FadeIn(notes[1]))
            self.play(*drop(left[1], left[2]))
            vo.wait_until("d")
            self.play(FadeIn(says[2]), FadeIn(notes[2]))
            self.play(*drop(left[2], left[3]))
            vo.wait_until("e")
            self.play(FadeIn(ans), Indicate(cells[("July", 16)], color=OK, scale_factor=1.3))
        self.clear_scene()

