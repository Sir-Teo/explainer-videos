from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403

CORNERS = [("t", r"it is", r"\textit{asti}"), ("f", r"it is not", r"\textit{nāsti}"),
           ("b", r"it both is and is not", r"\textit{ubhaya}"), ("n", r"it neither is nor is not", r"\textit{anubhaya}")]


class Corners(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"The four corners", r"What if a question has four possible answers, or none?",
                            lit=(150,), part=PART)
        with self.voiceover("Chapter four. The four corners."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.tetralemma()
        self.mapping()
        self.fifth()
        self.caution()

    def corner_cards(self, center=ORIGIN, w=3.6, h=1.3, dx=2.3, dy=1.1, with_values=False):
        cards = VGroup()
        pos = [UL, UR, DR, DL]
        for (v, en, skt), p in zip(CORNERS, pos):
            box = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=VAL_COLOR[v] if with_values
                                   else P.CLAIM, stroke_width=2.5, fill_color="#0B0F17", fill_opacity=0.9)
            t = VGroup(label(en, font_size=26), label(skt, font_size=22, color=GREY_B)).arrange(DOWN, buff=0.1)
            c = VGroup(box, t.move_to(box)).move_to(np.asarray(center, float) + np.array([p[0] * dx, p[1] * dy, 0]))
            c.box, c.value = box, v
            cards.add(c)
        return cards

    def tetralemma(self):
        hc = history_card(r"c.\ 150", r"Nāgārjuna", r"\textit{Mūlamadhyamakakārikā}, \ the Middle Way", width=6.0,
                          color=HIST).to_corner(UL, buff=0.35)
        cards = self.corner_cards(center=[0, -0.4, 0])
        q = label(r"`Does the Tathāgata exist after death?'", font_size=28, color=GOAL).next_to(hc, DOWN, buff=0.35)
        q.set_x(0)
        unans = label(r"the Buddha sets aside all four: \ one of the `unanswered questions'", font_size=24,
                      color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Indian logic had four values long before Belnap. <bookmark mark='a'/>In the early Buddhist texts, "
            "and then in Nāgārjuna's Fundamental Verses on the Middle Way, around the second century, a question "
            "is answered at four corners: the catuṣkoṭi. <bookmark mark='b'/>It is. It is not. It both is and is "
            "not. It neither is nor is not. <bookmark mark='c'/>Asked whether the Tathāgata, the Buddha, exists "
            "after death, the Buddha of the sutras sets aside all four. These are the unanswered questions."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in cards], lag_ratio=0.35), run_time=3)
            vo.wait_until("c")
            self.play(*[c.animate.set_opacity(0.4) for c in cards], FadeIn(unans))
        self.clear_scene()

    def mapping(self):
        cards = self.corner_cards(center=[0, -0.2, 0], w=3.4, dx=2.0)
        vals = VGroup(*[VGroup(vmob(c.value, 40), label({"t": r"told true", "f": r"told false", "b": r"told both",
                                                         "n": r"told neither"}[c.value], font_size=20,
                                                        color=GREY_A)).arrange(DOWN, buff=0.08) for c in cards])
        for v, c in zip(vals, cards):
            v.next_to(c, RIGHT if c.get_x() > 0 else LEFT, buff=0.3)
        head = label(r"Priest (2010), \ `The logic of the catuṣkoṭi': \ the four corners are FDE's four values",
                     font_size=26, color=CONN).to_edge(UP, buff=0.45)
        pt = label(r"each corner is \textit{one} value, \ not a claim about the others", font_size=24,
                   color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 2010 Graham Priest gave the corners a precise reading. <bookmark mark='a'/>They are the four values "
            "of the last chapter. 'It is' is T, true only. 'It is not' is F. 'Both' is B, and 'neither' is N. "
            "<bookmark mark='b'/>On this reading the catuṣkoṭi is not a muddle about contradiction. It is an "
            "exhaustive list of the possibilities in a logic that allows gaps and gluts, and the same logic a "
            "database needs when its sources conflict."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards))
            vo.wait_until("a")
            for c, v in zip(cards, vals):
                self.play(c.box.animate.set_stroke(VAL_COLOR[c.value], width=3), FadeIn(v), run_time=0.7)
            vo.wait_until("b")
            self.play(FadeIn(pt))
        self.clear_scene()

    def fifth(self):
        d = load("corners")
        cards = self.corner_cards(center=[-3.2, 0.6, 0], w=2.9, h=1.1, dx=1.6, dy=0.75, with_values=True)
        e = VGroup(Circle(radius=0.42, stroke_color=EMPTY, stroke_width=3, fill_color=EMPTY, fill_opacity=0.5),
                   MathTex(r"\mathbf{E}", font_size=34, color=WHITE)).move_to(cards.get_center())
        el = label(r"the fifth value: \ emptiness, \textit{śūnyatā}", font_size=24, color=GREY_A).next_to(cards, DOWN,
                                                                                                    buff=0.3)
        rule = label(r"E infects: \ any compound with an E part is E", font_size=24, color=GOAL).next_to(el, DOWN,
                                                                                                  buff=0.2)
        hd = [label(r"inference", font_size=22, color=P.CLAIM), label(r"FDE", font_size=22, color=P.CLAIM),
              label(r"FDE + E", font_size=22, color=P.CLAIM)]
        rows = [[MathTex(arg_tex(r["premises"], r["conclusion"]), font_size=28), r["fde"], r["fde_e"]] for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[3.4, 1.3, 1.6], cell_h=0.55, font_size=26).move_to([3.6, 0.4, 0])
        bad = next(r for r in d["rows"] if not r["fde_e"])
        cm = label(rf"$p \models p \lor q$ fails: \ ${cm_tex(bad['cm'])}$, \ so $p \lor q$ is E", font_size=24,
                   color=BAD).next_to(grid, DOWN, buff=0.35)
        with self.voiceover(
            "But the Buddha rejected all four corners, and Nāgārjuna does the same, again and again. How can every "
            "value fail? <bookmark mark='a'/>Priest's answer is a fifth value, outside the four, for questions whose "
            "presuppositions are empty: emptiness, śūnyatā. <bookmark mark='b'/>In the simplest version it "
            "behaves like Bochvar's meaningless value: any compound with an empty part is empty. <bookmark mark='c'/>The Reasoner adds it "
            "and rechecks the inferences of FDE. Most survive. <bookmark mark='d'/>One does not: from p, infer p or "
            "q. If q is empty, so is the disjunction, and it is not designated. Adding a disjunct can drag a "
            "truth into emptiness."
        ) as vo:
            self.play(FadeIn(cards))
            vo.wait_until("a")
            self.play(FadeIn(e, scale=0.5), FadeIn(el))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][c]) for r in range(len(rows)) for c in (0, 1, 2)])
            vo.wait_until("d")
            self.play(FadeIn(cm))
        self.clear_scene()

    def caution(self):
        q = quote_card(r"Neither from itself nor from another, \ nor from both, \ nor without a cause, \ does "
                       r"anything whatever, anywhere arise.", r"Nāgārjuna, \textit{Mūlamadhyamakakārikā} I.1",
                       r"trans.\ Garfield, \textit{The Fundamental Wisdom of the Middle Way} (1995)", width=10.6,
                       font_size=28).move_to([0, 1.3, 0])
        reads = VGroup(label(r"a logic of four or five values \ (Priest; Garfield and Priest 2003)", font_size=24),
                       label(r"a method of refutation: \ each corner is reduced to absurdity \ (\textit{prasaṅga})",
                             font_size=24),
                       label(r"rhetoric for the limits of concepts \ (Robinson 1957; Jayatilleke 1963)", font_size=24)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(q, DOWN, buff=0.6)
        moral = label(r"the formal reading does not settle the interpretation, \ but it shows the corners are "
                      r"consistent", font_size=24, color=GOAL).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is the first verse of Nāgārjuna's work, a tetralemma about causation. <bookmark mark='a'/>Nothing "
            "arises from itself, from another, from both, or from no cause. <bookmark mark='b'/>How to read such "
            "verses is disputed. Priest and Jay Garfield read them as logic with four or five values. Others read "
            "the corners as a method of refutation, each reduced to absurdity in turn, or as a rhetoric for the "
            "limits of concepts. <bookmark mark='c'/>The formal reading does not settle the interpretation. What it "
            "does show is that the four corners, and the rejection of all four, can be stated without inconsistency."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in reads], lag_ratio=0.4))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()
