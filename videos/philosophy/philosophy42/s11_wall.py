from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Wall(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"The Wall, complete", r"What do forty-two impossibilities have in common?", lit=(1931, 2018), part=PART)
        with self.voiceover("Chapter ten. The Wall, complete."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.build()
        self.kinds()
        self.lesson()
        self.price()
        self.bets()

    def build(self):
        outline = wall(upto=0).scale(0.62).move_to([0, 0.4, 0])
        full = wall(upto=42, current=42).scale(0.62).move_to([0, 0.4, 0])
        card = wall_card(42, width=9.6, font_size=22).to_edge(DOWN, buff=0.25)
        courses = [VGroup(*[full.brick[p] for p in range(r * 7 + 1, r * 7 + 8)]) for r in range(6)]
        with self.voiceover(
            "Every part of this series has added one brick to a wall. <bookmark mark='a'/>Each brick is a dream of "
            "settling some question by calculation, and the theorem that stops it. <bookmark mark='b'/>Zeno and "
            "Meno, Cook and Levin, Church and Turing, Gödel and the liar; Hume, Bertrand, Gettier and Goodman's "
            "grue; Bell, Kripke, the hard problem; Arrow, Sen and Arrhenius; the paradox of taste and the fairness "
            "theorem. <bookmark mark='c'/>The forty second brick is this part's: the dream of specifying what we "
            "want and then optimizing it, stopped by Goodhart's law, by the theorem that behaviour does not fix "
            "values, and by the Löbian obstacle to an agent certifying itself. What it forces is judgment that "
            "stays in the loop."
        ) as vo:
            self.play(FadeIn(outline))
            vo.wait_until("a")
            for c in courses[:2]:
                self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in c], lag_ratio=0.12), run_time=1.2)
            vo.wait_until("b")
            for c in courses[2:]:
                self.play(LaggedStart(*[FadeIn(b, shift=DOWN * 0.15) for b in c], lag_ratio=0.12), run_time=1.2)
            vo.wait_until("c")
            self.play(full.animate.scale(0.75).to_edge(UP, buff=0.3), FadeOut(outline))
            self.play(FadeIn(card), Indicate(full.brick[42], color=P.CONCL, scale_factor=1.15))
        self.clear_scene()

    def kinds(self):
        d = load("wall")
        K, kind = d["kinds"], d["kind"]
        assert sum(d["counts"].values()) == 41
        colors = {"A": LOBC, "B": HUMAN, "C": RISK, "D": ROBOT, "E": TRUEV}
        w = wall(upto=42, current=42).scale(0.56).to_edge(LEFT, buff=0.3).shift(UP * 0.3)
        head = label(r"What the bricks force", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        legend = VGroup()
        for k in "ABCDE":
            sw = Square(side_length=0.28, stroke_width=0, fill_color=colors[k], fill_opacity=0.85)
            t = label(rf"{K[k]['name']} \ ({d['counts'][k]})", font_size=19, color=colors[k])
            legend.add(VGroup(sw, t).arrange(RIGHT, buff=0.18))
        sw = Square(side_length=0.28, stroke_width=0, fill_color=P.CONCL, fill_opacity=0.85)
        legend.add(VGroup(sw, label(r"the capstone: \ alignment \ (42)", font_size=19, color=P.CONCL)).arrange(
            RIGHT, buff=0.18))
        legend.arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(UP * 0.4)
        foot = label(r"every kind ends in the same place: \ a choice that calculation can inform but not make",
                     font_size=21, color=GOAL).to_edge(DOWN, buff=0.4)
        anims = {k: [] for k in "ABCDE"}
        for p in range(1, 42):
            k = kind[str(p)]
            anims[k].append(w.brick[p][0].animate.set_fill(colors[k], opacity=0.85))
        with self.voiceover(
            "Read together, the bricks fall into five kinds. <bookmark mark='a'/>In eight, proof and calculation "
            "run out: Gödel, Turing, Cook and Levin, the liar, the frame problem. <bookmark mark='b'/>In seven, "
            "evidence underdetermines: Hume's induction, Bertrand's priors, Markov equivalence, no free lunch. "
            "<bookmark mark='c'/>In seven, no way of aggregating meets every condition: Arrow, Sen, Arrhenius, the "
            "prisoner's dilemma, the fairness theorem. <bookmark mark='d'/>In eight, facts do not fix meaning, "
            "mind or value: Frege's puzzle, Kripkenstein, the hard problem, Hume's law, taste. <bookmark "
            "mark='e'/>And in eleven, a paradox forces a new concept: Zeno, the sorites, Gettier, fission. "
            "<bookmark mark='f'/>The last brick touches several kinds at once. And every kind ends in the same "
            "place: a choice that calculation can inform, sharpen and price, but cannot make for us."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w))
            for mk, k in zip("abcde", "ABCDE"):
                vo.wait_until(mk)
                self.play(*anims[k], FadeIn(legend["ABCDE".index(k)]))
            vo.wait_until("f")
            self.play(FadeIn(legend[5]), Indicate(w.brick[42], color=P.CONCL, scale_factor=1.15))
            self.play(FadeIn(foot))
        self.clear_scene()

    def price(self):
        d = load("alignment")
        claims = [(c0["key"], c0["text"]) for c0 in d["claims"]]
        assert d["mus"] == [["GOODHART", "PROXY", "SAFE", "STRONG"]] and len(d["mcs"]) == 4
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.5, width=3.6, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ alignment")
        positions = [(("PROXY",), r"learn the target", r"inverse RL; \ assistance games; \ feedback \ (chapters 3, \ 4)"),
                     (("STRONG",), r"optimize mildly", r"quantilizers; \ KL penalties; \ limited agency \ (chapter 1)"),
                     (("GOODHART",), r"harden the proxy", r"adversarial testing; \ oversight; \ interpretability"),
                     (("SAFE",), r"contain the result", r"corrigibility; \ monitoring; \ control \ (chapter 4)")]
        with self.voiceover(
            "The field's own Price List has four claims. <bookmark mark='a'/>What we can write down is only a proxy "
            "for what we want. Strong optimizers will optimize what we write down. Under strong optimization a proxy "
            "and its target come apart. And the result will be what we want. <bookmark mark='b'/>They cannot all "
            "be true, and every research programme in alignment denies one. <bookmark mark='c'/>Learn the target "
            "instead of writing it: inverse reinforcement learning, assistance games, learning from feedback, which "
            "runs into the no-free-lunch theorem. <bookmark mark='d'/>Optimize mildly: quantilizers, penalties for "
            "drifting from a base model, systems with limited agency. <bookmark mark='e'/>Harden the proxy so it "
            "holds under pressure: adversarial testing, scalable oversight, interpretability. <bookmark "
            "mark='f'/>Or accept that the result may not be what we want, and contain it: corrigibility, monitoring "
            "and control. Each position pays a price this series has met before."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c0) for c0 in pl.cards], lag_ratio=0.35))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def bets(self):
        head = label(r"The philosophical bets of artificial intelligence", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"mind as computation", r"the right computations suffice for thought \ (Part 30), \ and perhaps for experience \ (Part 31)", ROBOT),
                (r"meaning from use", r"statistics of text carry meaning \ (Part 28: \ the distributional hypothesis)", HUMAN),
                (r"induction", r"a learner's inductive bias fits our world \ (Part 15: \ no free lunch)", TRUEV),
                (r"preference", r"comparisons reveal a single reward; \ raters aggregate like Borda \ (Parts 37, \ 39)", PROXYC)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Artificial intelligence is already making philosophical bets, whether or not it says so. <bookmark "
            "mark='a'/>That the right computations suffice for thought, the functionalism of Part 30, and perhaps for "
            "experience, the open question of Part 31. <bookmark mark='b'/>That the statistics of text carry meaning: "
            "the distributional hypothesis of Part 28, against the grounding objections. <bookmark mark='c'/>That a "
            "learner's inductive bias fits the world it will meet, the bet that Part 15's no-free-lunch theorem says "
            "every learner makes. <bookmark mark='d'/>And that human comparisons reveal a single reward that can be "
            "aggregated across people, which Parts 37 and 39 showed is a substantive, and contestable, assumption. "
            "Knowing the bets is the first step to hedging them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def lesson(self):
        head = label(r"What the Wall is not", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"not skepticism", r"every brick came with escapes: \ each Price List named the positions that pay its price", TRUEV),
                (r"not relativism", r"the escapes are few, \ and their prices are exact: \ choosing is constrained", HUMAN),
                (r"not a failure", r"the theorems are achievements of calculation: \ only calculation could prove its own limits", LOBC),
                (r"the lesson", r"calculation does not replace judgment; \ it shows exactly where judgment is needed, \ and what it will cost", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "It is easy to misread the Wall. <bookmark mark='a'/>It is not a counsel of skepticism. Every brick came "
            "with its escapes: each Price List named the positions that give up one claim and pay its price, and "
            "serious people hold each of them. <bookmark mark='b'/>Nor is it relativism. The escapes are few, and "
            "their prices are exact; once you know them, choosing is constrained, and some choices are better argued "
            "than others. <bookmark mark='c'/>Nor is it a failure of calculation. Gödel's theorems, Arrow's theorem "
            "and the fairness theorem are among its greatest achievements: only calculation could have proved its own "
            "limits. <bookmark mark='d'/>The lesson is a division of labour. Calculation does not replace judgment. "
            "It shows exactly where judgment is needed, and what each judgment will cost."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
