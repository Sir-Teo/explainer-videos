from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Lob(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Agents that reason about themselves", r"Can a reasoner trust its own proofs?", lit=(1955, 2014), part=PART)
        with self.voiceover("Chapter six. Agents that reason about themselves."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.lob()
        self.frames()
        self.obstacle()
        self.combat()

    def lob(self):
        head = history_card(1955, r"Martin Löb", r"``Solution of a Problem of Leon Henkin''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"Henkin \ (1952)", r"a sentence that says `I am provable': \ is it provable?", HUMAN),
                (r"Löb's theorem", r"if PA proves `if PA proves $\varphi$, \ then $\varphi$', \ then PA proves $\varphi$: \ $\Box(\Box\varphi \to \varphi) \to \Box\varphi$", LOBC),
                (r"Gödel II", r"take $\varphi$ false: \ a consistent PA cannot prove its own consistency \ (Part 7)", RISK),
                (r"the moral", r"a system that trusts its own proofs, \ in general, \ proves everything", GOAL)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The last technical chapter returns to Part 7. <bookmark mark='a'/>In 1952 Leon Henkin asked about a "
            "sentence that says of itself, I am provable. Is it provable? <bookmark mark='b'/>Martin Löb answered in "
            "1955: yes, and much more. If Peano arithmetic proves that the provability of a sentence implies its "
            "truth, then it proves the sentence itself. In the notation of modal logic, box of box phi implies phi, "
            "implies box phi. <bookmark mark='c'/>Take phi to be a falsehood, and this is Gödel's second "
            "incompleteness theorem: a consistent system cannot prove its own consistency. <bookmark mark='d'/>The "
            "moral is strange. A system can trust its own proofs about a sentence only if it already proves that "
            "sentence. A reasoner cannot, in general, certify its own reliability."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def frames(self):
        rows = load("lob")["rows"]
        assert [r["lob_valid"] for r in rows] == [1, 3, 19, 219] and all(r["agree"] == r["frames"] for r in rows)
        head = label(r"Löb's axiom on every frame with up to four worlds", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        ax_ = MathTex(r"\Box(\Box p \to p) \to \Box p", font_size=40, color=LOBC).next_to(head, DOWN, buff=0.35)
        hd = [r"\text{worlds}", r"\text{frames}", r"\text{L\"ob valid}", r"\text{strict partial orders}",
              r"\textbf{4}\text{ valid (transitive)}", r"\textbf{T}\text{ valid (reflexive)}"]
        cells = [[label(str(r["n"]), font_size=20), label(f"{r['frames']:,}", font_size=20),
                  label(str(r["lob_valid"]), font_size=20, color=LOBC),
                  label(str(r["strict_partial_orders"]), font_size=20, color=LOBC),
                  label(f"{r['four_valid']:,}", font_size=20, color=GREY_A),
                  label(f"{r['T_valid']:,}", font_size=20, color=GREY_A)] for r in rows]
        grid = ValueGrid(hd, cells, col_w=[1.4, 1.6, 1.9, 3.0, 3.0, 2.8], cell_h=0.58, font_size=18).move_to([0, 0.0, 0])
        # a tiny GL frame and a reflexive point
        def frame(points, edges, x0, col):
            ds = VGroup(*[Dot([x0 + px, py, 0], radius=0.09, color=col) for px, py in points])
            es = VGroup(*[Arrow(ds[a].get_center(), ds[b].get_center(), buff=0.12, color=col, stroke_width=3,
                                max_tip_length_to_length_ratio=0.25) for a, b in edges])
            return VGroup(ds, es)
        gl = frame([(0, 0), (1.0, 0.5), (2.0, 0)], [(0, 1), (1, 2), (0, 2)], -4.6, LOBC).shift(DOWN * 2.6)
        refl = VGroup(Dot([2.8, -2.6, 0], radius=0.09, color=RISK),
                      Arc(radius=0.28, start_angle=-0.3, angle=1.6 * PI, color=RISK).move_to([2.8, -2.32, 0]))
        cap = VGroup(label(r"a strict order: \ Löb holds", font_size=18, color=LOBC).next_to(gl, DOWN, buff=0.15),
                     label(r"one reflexive world: \ Löb fails", font_size=18, color=RISK).next_to(refl, DOWN,
                                                                                                    buff=0.2))
        with self.voiceover(
            "The Reasoner checks what Löb's axiom means, using the possible-worlds semantics of Part 4. <bookmark "
            "mark='a'/>Read box as true in every world the current one can see. For every frame with up to four "
            "worlds, sixty five thousand, five hundred and thirty six of them at four, and every way of making p "
            "true or false, it tests the axiom. <bookmark mark='b'/>The axiom holds on exactly one, three, nineteen "
            "and two hundred and nineteen frames: precisely the strict partial orders, relations that are "
            "transitive and never let a world see itself. <bookmark mark='c'/>For comparison, the axiom four holds on "
            "the transitive frames, and T on the reflexive ones. <bookmark mark='d'/>A single world that sees itself "
            "already breaks Löb's axiom. Robert Solovay proved in 1976 that the logic of these frames, GL, is exactly "
            "what Peano arithmetic can prove about its own provability. The Reasoner's finite check is the shadow "
            "of that theorem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax_))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(VGroup(*rw[:2])) for rw in grid.cell])
            vo.wait_until("b")
            self.play(*[FadeIn(VGroup(*rw[2:4])) for rw in grid.cell], FadeIn(gl), FadeIn(cap[0]))
            vo.wait_until("c")
            self.play(*[FadeIn(VGroup(*rw[4:])) for rw in grid.cell])
            vo.wait_until("d")
            self.play(FadeIn(refl), FadeIn(cap[1]))
        self.clear_scene()

    def obstacle(self):
        head = label(r"The Löbian obstacle", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"tiling agents", r"Yudkowsky and Herreshoff \ (2013): \ an agent that builds a successor wants `if it proves an action safe, \ it is safe'", ROBOT),
                (r"the obstacle", r"by Löb, \ trusting a successor in its own system is trusting its own proofs: \ only weaker successors can be trusted", RISK),
                (r"logical induction", r"Garrabrant et al. \ (2016): \ computable probabilities for mathematical sentences that come to trust themselves", LOBC),
                (r"embedded agency", r"Demski and Garrabrant \ (2019): \ an agent is part of the world it reasons about, \ and smaller than it", TRUEV)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Why does this matter for machines? <bookmark mark='a'/>Eliezer Yudkowsky and Marcello Herreshoff "
            "considered an agent that designs its own successor. Before handing over, it wants to know: if my "
            "successor proves an action is safe, the action is safe. <bookmark mark='b'/>But if the successor reasons "
            "in the same system, that is exactly the self-trust Löb's theorem forbids. The agent can certify only "
            "successors that reason in weaker systems, and trust decays with each generation: the Löbian obstacle. "
            "<bookmark mark='c'/>One response replaces proof with probability. Scott Garrabrant and colleagues "
            "constructed logical induction, a computable way of assigning probabilities to mathematical sentences "
            "that eventually comes to trust its own future beliefs. <bookmark mark='d'/>Abram Demski and Garrabrant "
            "gathered these puzzles under the name embedded agency: a real agent is not outside the world it models, "
            "like the players in Part 33's decision theories, but part of it, and smaller than it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def combat(self):
        d = load("combat")
        bots, T = d["bots"], d["table"]
        assert T["FairBot|FairBot"] == "C" and T["PrudentBot|CooperateBot"] == "D"
        head = label(r"Löbian cooperation \ (Barasz et al., \ 2014)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        defs = VGroup(
            MathTex(r"\textsf{FairBot}(X) = C \iff \Box\big(X(\textsf{FairBot}) = C\big)", font_size=28, color=LOBC),
            MathTex(r"\textsf{PrudentBot}(X) = C \iff \Box\big(X(\textsf{PrudentBot}) = C\big) \wedge "
                    r"\Box_{+1}\big(X(\textsf{DefectBot}) = D\big)", font_size=26, color=ROBOT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(head, DOWN, buff=0.3)
        short = {"CooperateBot": r"CooperateBot", "DefectBot": r"DefectBot", "FairBot": r"FairBot",
                 "PrudentBot": r"PrudentBot"}
        hd = [r"\text{row plays column}"] + [rf"\text{{{short[b]}}}" for b in bots]
        cells = []
        for X in bots:
            row = [label(short[X], font_size=19, color=GREY_A)]
            for Y in bots:
                v = T[f"{X}|{Y}"]
                row.append(label(v, font_size=24, color=TRUEV if v == "C" else RISK))
            cells.append(row)
        grid = ValueGrid(hd, cells, col_w=[3.2, 2.5, 2.3, 2.1, 2.4], cell_h=0.6, font_size=18).move_to([0, -1.2, 0])
        proof = MathTex(r"\varphi = \text{`both cooperate'}:\quad \vdash \Box\varphi \to \varphi\ \ "
                        r"\Longrightarrow\ \ \vdash \varphi \quad (\text{L\"ob})", font_size=26, color=GOAL).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Löb's theorem also has a happy consequence, in Part 34's prisoner's dilemma. <bookmark mark='a'/>Let "
            "programs play, each able to read the other's code. FairBot cooperates with you if and only if it can "
            "prove that you cooperate with it. <bookmark mark='b'/>What happens when FairBot meets FairBot? Each "
            "waits for a proof about the other, which seems to be an endless regress. <bookmark mark='c'/>Löb's "
            "theorem cuts it. Let phi be the sentence, both cooperate. By their code, if phi is provable then phi is "
            "true, and this is itself provable; so by Löb, phi is provable, and they cooperate. The Reasoner "
            "evaluates every pairing in the provability logic it just checked. <bookmark mark='d'/>FairBot "
            "cooperates with itself and with CooperateBot, and defects against DefectBot. PrudentBot also demands "
            "a proof that you would defect against DefectBot, so it exploits the unconditional CooperateBot, yet "
            "cooperates with FairBot and with itself. Mihaly Barasz, Patrick LaVictoire and colleagues called this "
            "robust cooperation; Andrew Critch extended it to agents with bounded resources. Reasoners that can "
            "read each other can cooperate where the players of Part 34 could not."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(defs[0]))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(rw[0]) for rw in grid.cell])
            vo.wait_until("c")
            self.play(FadeIn(proof), FadeIn(grid.cell[2][3]))
            vo.wait_until("d")
            self.play(FadeIn(defs[1]), *[FadeIn(c0) for rw in grid.cell for c0 in rw[1:]])
        self.clear_scene()
