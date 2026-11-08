from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


class Paracon(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Living with contradiction", r"Must one contradiction poison everything?",
                            lit=(1979,), part=PART)
        with self.voiceover("Chapter six. Living with contradiction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.proof()
        self.history()
        self.recapture()
        self.dialetheism()

    def proof(self):
        d = load("explosion")
        hc = history_card(r"12th c.", r"William of Soissons; \ later Lewis and Langford (1932)",
                          r"from a contradiction, anything follows", width=7.0, color=HIST).to_corner(UL, buff=0.35)
        lines = [(r"1", r"p \land \lnot p", r"premise"), (r"2", r"p", r"$\land$E, 1"), (r"3", r"\lnot p", r"$\land$E, 1"),
                 (r"4", r"p \lor q", r"$\lor$I, 2"), (r"5", r"q", r"disjunctive syllogism, 4, 3")]
        rows = VGroup()
        for i, (n, f, why) in enumerate(lines):
            y = 1.3 - 0.72 * i
            r = VGroup(label(n, font_size=24, color=GREY_B), MathTex(f, font_size=36), label(why, font_size=22,
                                                                                         color=GREY_A))
            r[0].move_to([-5.6, y, 0])
            r[1].move_to([-4.9 + r[1].width / 2, y, 0])
            r[2].move_to([-2.2 + r[2].width / 2, y, 0])
            rows.add(r)
        verdicts = VGroup()
        for i, row in enumerate(d["rows"]):
            v = tv(row["lp"], 30).move_to([2.6, rows[i + 1].get_y(), 0])
            verdicts.add(v)
        vh = label(r"valid in LP?", font_size=24, color=P.CLAIM).move_to([2.6, 2.0, 0])
        bad = d["rows"][-1]
        cm = label(rf"countermodel: \ ${cm_tex(bad['cm'])}$: \ $p \lor q$ and $\lnot p$ hold, \ $q$ does not",
                   font_size=24, color=BAD).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Why does a contradiction imply everything? The proof was known in the twelfth century, to William of "
            "Soissons, and Lewis and Langford printed it in 1932. <bookmark mark='a'/>Suppose p and not p. Then p. "
            "Then not p. <bookmark mark='b'/>From p, 'p or q', for any q at all. <bookmark mark='c'/>And from 'p or "
            "q' and 'not p', q: disjunctive syllogism. <bookmark mark='d'/>The Reasoner checks each step in LP. "
            "The first three are valid. <bookmark mark='e'/>The last is not: with p both true and false, 'p or q' "
            "and 'not p' both hold, and q may still be false. In a world with true contradictions, ruling out one "
            "disjunct does not hand you the other."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(rows[2]))
            vo.wait_until("b")
            self.play(FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(vh), LaggedStart(*[FadeIn(v, scale=0.6) for v in verdicts[:3]], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(FadeIn(verdicts[3], scale=0.6), FadeIn(cm), Indicate(rows[4], color=BAD))
        self.clear_scene()

    def history(self):
        hcs = VGroup(history_card(1948, r"Stanisław Jaśkowski", r"discussive logic: \ each participant consistent, "
                                  r"\ the discussion not", width=4.3, color=HIST, font_size=20),
                     history_card(1963, r"Newton da Costa", r"the C-systems: \ consistency as an explicit "
                                  r"hypothesis", width=4.3, color=HIST, font_size=20),
                     history_card(1979, r"Graham Priest", r"LP, \ and \textit{dialetheism}: \ some contradictions "
                                  r"are true", width=4.3, color=HIST, font_size=20)).arrange(RIGHT, buff=0.25).to_edge(
            UP, buff=0.5)
        defs = VGroup(VGroup(label(r"paraconsistent:", font_size=28, color=GOAL),
                             label(r"a logic in which a contradiction does not entail everything", font_size=26)
                             ).arrange(RIGHT, buff=0.3),
                      VGroup(label(r"dialetheism:", font_size=28, color=BAD),
                             label(r"the view that some contradictions are actually true", font_size=26)
                             ).arrange(RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([0, -0.8, 0])
        gap = label(r"the first is a claim about logic; \ the second, a claim about the world", font_size=24,
                    color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Logics without explosion were found several times. <bookmark mark='a'/>Stanisław Jaśkowski, in 1948, "
            "modelled a discussion where each participant is consistent but the discussion as a whole is not. "
            "<bookmark mark='b'/>Newton da Costa in Brazil, from 1963, built systems in which consistency is a "
            "hypothesis you add when you are entitled to it. <bookmark mark='c'/>And Graham Priest, in 1979, "
            "defended LP together with a stronger thesis. <bookmark mark='d'/>A logic is paraconsistent if a "
            "contradiction does not entail everything. Dialetheism is the view that some contradictions are in "
            "fact true. <bookmark mark='e'/>The first is a claim about logic. Most people who use paraconsistent "
            "logics, for example to query inconsistent data, reject the second."
        ) as vo:
            for mk, h in zip("abc", hcs):
                if mk != 'a':
                    vo.wait_until(mk)
                self.play(FadeIn(h, shift=DOWN * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(defs))
            vo.wait_until("e")
            self.play(FadeIn(gap))
        self.clear_scene()

    def recapture(self):
        d = load("lpm")
        head = label(r"Classical recapture: \ minimally inconsistent LP \ (Priest 1991)", font_size=30,
                     color=CONN).to_edge(UP, buff=0.45)
        rule = label(r"keep only the LP models of the premises with as few contradictions as possible", font_size=24,
                     color=GREY_A).next_to(head, DOWN, buff=0.25)
        hd = [label(r"argument", font_size=22, color=P.CLAIM), label(r"classical", font_size=22, color=P.CLAIM),
              label(r"LP", font_size=22, color=P.CLAIM), label(r"LP$_m$", font_size=22, color=P.CLAIM)]
        rows = [[MathTex(arg_tex(r["premises"], r["conclusion"]), font_size=30), r["cl"], r["lp"], r["lpm"]]
                for r in d["rows"]]
        grid = ValueGrid(hd, rows, col_w=[5.4, 1.8, 1.2, 1.4], cell_h=0.62, font_size=28).next_to(rule, DOWN, buff=0.5)
        q = label(r"the contradiction about $p$ is quarantined: \ reasoning about $r$ and $q$ is classical again",
                  font_size=24, color=OK).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A paraconsistent reasoner pays for safety with weakness: LP loses modus ponens and disjunctive "
            "syllogism everywhere, even where nothing is contradictory. <bookmark mark='a'/>Priest's repair, in "
            "1991: among the models of the premises, keep only those with as few contradictions as possible. "
            "<bookmark mark='b'/>The Reasoner computes it. Where the premises are consistent, the minimal models are "
            "classical, and disjunctive syllogism and modus ponens come back. <bookmark mark='c'/>A contradiction "
            "about p still does not explode. <bookmark mark='d'/>And in the last row, p is contradictory, but "
            "reasoning about r and q is untouched: from 'r or q' and 'not r', q. <bookmark mark='e'/>The "
            "contradiction is quarantined where it is."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            self.play(FadeIn(grid.head), FadeIn(grid.rows_bg), FadeIn(grid.rule),
                      *[FadeIn(grid.cell[r][c]) for r in range(len(rows)) for c in (0, 1, 2)])
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[r][3], scale=0.6) for r in (0, 1)])
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[r][3], scale=0.6) for r in (2, 3)])
            vo.wait_until("d")
            self.play(FadeIn(grid.cell[4][3], scale=0.6), Create(grid.row_box(4)))
            vo.wait_until("e")
            self.play(FadeIn(q))
        self.clear_scene()

    def dialetheism(self):
        head = label(r"Are any contradictions true?", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        cands = VGroup(label(r"the liar: \ `this sentence is false' \ (Part 8)", font_size=26),
                       label(r"the instant of change: \ as I leave the room, am I in it?", font_size=26),
                       label(r"inconsistent laws: \ a statute that both requires and forbids", font_size=26)
                       ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(head, DOWN, buff=0.6)
        cands.set_x(0)
        obj = VGroup(label(r"Lewis (1982): \ `I decline to defend it': \ non-contradiction affirmed, not argued", font_size=24,
                           color=BAD),
                     label(r"Quine (1970): \ change the logic, \ and you change the subject", font_size=24, color=BAD),
                     label(r"Priest: \ \textit{In Contradiction} (1987): \ the evidence of paradox is the evidence",
                           font_size=24, color=OK)).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(cands, DOWN,
                                                                                                    buff=0.6)
        obj.set_x(0)
        with self.voiceover(
            "Are there true contradictions? Priest's candidates are of three kinds. <bookmark mark='a'/>The liar "
            "sentence, which says of itself that it is false, the subject of Part 8. <bookmark mark='b'/>The instant "
            "of change: at the moment I leave a room, am I in it or not? <bookmark mark='c'/>And bodies of law "
            "that, by accident, both require and forbid the same act. <bookmark mark='d'/>The opposition is less "
            "an argument than a refusal. David Lewis affirmed the law of non-contradiction and, against the "
            "rules of debate, declined to defend it. Quine said that whoever changes the logic changes the subject. Priest's reply, in In "
            "Contradiction, is that the paradoxes are the evidence, and that we should follow it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abc", cands):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(o, shift=RIGHT * 0.15) for o in obj], lag_ratio=0.5), run_time=3)
        self.clear_scene()
