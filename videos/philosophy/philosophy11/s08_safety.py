from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Safety(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Safety", r"Could you easily have been wrong?", lit=(2000,), part=PART)
        with self.voiceover("Chapter seven. Safety."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.safety()
        self.chute()
        self.table()

    def safety(self):
        sp = load("spheres")["clock"]
        head = label(r"Safety: \ not easily wrong", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        who = label(r"Sosa (1999); \ Williamson (2000); \ Pritchard (2005)", font_size=22, color=GREY_B).next_to(
            head, DOWN, buff=0.2)
        f = MathTex(r"\text{safe} \iff \text{in every nearby world where } S \text{ believes } p,\ p \text{ is true}",
                    font_size=32, color=GOAL).next_to(who, DOWN, buff=0.3)
        sv = SpheresView(sp, "eight", center=[-2.6, -1.3, 0], step=1.3,
                         angles={"7:58": PI * 0.8, "8:03": PI * 0.2},
                         names={"8:00": "8:00", "7:58": "two minutes earlier", "8:03": "three minutes later"})
        disc = sv.disc(1, color=KNOW, opacity=0.1)
        dl = label(r"the nearby worlds", font_size=20, color=KNOW).next_to(disc, LEFT, buff=0.1)
        rows = VGroup(label(r"Russell's stopped clock:", font_size=24, color=WHITE),
                      label(r"glance two minutes earlier, \ and you believe `8:00' \ falsely", font_size=22,
                            color=BAD),
                      label(r"unsafe: \ no knowledge", font_size=24, color=BAD),
                      label(r"sensitivity asks about the \textit{closest} world where $p$ is false;", font_size=21,
                            color=GREY_A),
                      label(r"safety asks about \textit{every nearby} world where S believes $p$", font_size=21,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([3.4, -1.3, 0])
        v = sp["verdicts"][0]
        assert not v["safe"]
        with self.voiceover(
            "A rival condition turns Nozick's counterfactual around. <bookmark mark='a'/>Ernest Sosa, in 1999, and "
            "Timothy Williamson and Duncan Pritchard after him, proposed safety: your belief is safe if, in every "
            "nearby world where you believe it, it is true. You could not easily have been wrong. "
            "<bookmark mark='b'/>Run it on Russell's stopped clock. In the actual world you glance at eight. "
            "<bookmark mark='c'/>The nearby worlds are those where you glanced a little earlier or later. "
            "<bookmark mark='d'/>There you still believe it is eight o'clock, and you are wrong. The belief is unsafe, "
            "and is not knowledge. <bookmark mark='e'/>Notice the difference in what the two conditions examine. "
            "Sensitivity looks at the closest world where p is false, however far away that is. Safety looks only "
            "at nearby worlds, but at every one in which you believe p."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(who), Write(f))
            vo.wait_until("b")
            self.play(FadeIn(sv))
            vo.wait_until("c")
            self.play(FadeIn(disc), FadeIn(dl))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), Indicate(sv.dot["7:58"], color=BAD, scale_factor=1.6))
            self.play(FadeIn(rows[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
        self.clear_scene()

    def chute(self):
        sp = load("spheres")["chute"]
        bv = load("spheres")["biv"]
        head = label(r"Where they disagree", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        a = SpheresView(sp, "basement", center=[-3.5, -0.4, 0], step=2.0, angles={"snags": PI * 0.3},
                        names={"falls": "it falls", "snags": "it snags (never has)"})
        b = SpheresView(bv, "not_biv", center=[3.5, -0.4, 0], step=1.0,
                        angles={"lost hands": PI * 0.75, "envatted": PI * 0.25},
                        names={"normal": "you", "lost hands": "no hands", "envatted": "envatted"})
        da = Circle(radius=1.0, stroke_color=KNOW, stroke_width=2, fill_color=KNOW, fill_opacity=0.1).move_to(
            a.center_pt)
        db = Circle(radius=1.35, stroke_color=KNOW, stroke_width=2, fill_color=KNOW, fill_opacity=0.1).move_to(
            b.center_pt)
        ta = VGroup(label(r"Sosa's garbage chute", font_size=25, color=GOAL),
                    label(r"`the bag is in the basement'", font_size=21, color=BEL)).arrange(DOWN, buff=0.1).next_to(
            a, UP, buff=0.15)
        tb = VGroup(label(r"the vat again", font_size=25, color=GOAL),
                    label(r"`I am not a brain in a vat'", font_size=21, color=BEL)).arrange(DOWN, buff=0.1).next_to(
            b, UP, buff=0.15)
        va = VGroup(label(r"insensitive: \ snagged, \ I'd still believe it", font_size=20, color=BAD),
                    label(r"safe: \ no nearby world where I'm wrong", font_size=20, color=OK)).arrange(
            DOWN, buff=0.1).next_to(a, DOWN, buff=0.2)
        vb = VGroup(label(r"insensitive", font_size=20, color=BAD),
                    label(r"safe: \ the vat is far away", font_size=20, color=OK)).arrange(DOWN, buff=0.1).next_to(
            b, DOWN, buff=0.2)
        r1 = sp["verdicts"][0]
        r2 = {r["p"]: r for r in bv["verdicts"]}["not_biv"]
        assert not r1["sensitive"] and r1["safe"] and not r2["sensitive"] and r2["safe"]
        with self.voiceover(
            "The two conditions come apart, and the Reasoner finds where. <bookmark mark='a'/>Sosa's own example: on "
            "my way to the elevator I drop a bag of rubbish down the chute of my high-rise. A moment later I believe "
            "it is in the basement. It is. <bookmark mark='b'/>Is the belief sensitive? The closest world where the "
            "bag is not in the basement is one where it snagged on the way down, which has never happened, and there "
            "I would still believe it reached the bottom. Insensitive. But in every nearby world where I believe it, "
            "it is true. Safe. Surely I know where my rubbish is. <bookmark mark='c'/>And the vat: I would believe I "
            "was not a brain in a vat even if I were one, so the belief is insensitive. But the vat world is far "
            "away. In every nearby world where I believe I am not envatted, I am not. Safe. "
            "<bookmark mark='d'/>So safety, unlike sensitivity, lets me know that I am not a brain in a vat. The "
            "anti-skeptical premise becomes knowledge, and closure survives."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(ta))
            vo.wait_until("b")
            self.play(FadeIn(da), FadeIn(va))
            vo.wait_until("c")
            self.play(FadeIn(b), FadeIn(tb), FadeIn(db), FadeIn(vb))
            vo.wait_until("d")
            self.play(Indicate(vb[1], color=OK))
        self.clear_scene()

    def table(self):
        sps = load("spheres")
        head = label(r"Two checkers, \ seven beliefs", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        cases = [("coins", "p", r"Gettier's coins"), ("clock", "eight", r"the stopped clock"),
                 ("barns", "barn", r"Barn County: \ `a barn'"), ("lottery", "lose", r"`my ticket will lose'"),
                 ("chute", "basement", r"the garbage chute"), ("biv", "not_biv", r"`I'm not envatted'"),
                 ("biv", "hands", r"`I have hands'")]
        hd = [label(r"belief", font_size=21, color=P.CLAIM), label(r"true", font_size=21, color=P.CLAIM),
              label(r"sensitive", font_size=21, color=P.CLAIM), label(r"safe", font_size=21, color=P.CLAIM),
              label(r"intuition", font_size=21, color=P.CLAIM)]
        intuit = {"coins": False, "clock": False, "barns": False, "lottery": False, "chute": True, "not_biv": None,
                  "hands": True}
        rows = []
        for key, p, name in cases:
            v = {r["p"]: r for r in sps[key]["verdicts"]}[p]
            k = p if key == "biv" else key
            rows.append([label(name, font_size=20), mark(v["true"], 24), mark(v["sensitive"], 24),
                         mark(v["safe"], 24),
                         label({True: r"knows", False: r"doesn't", None: r"disputed"}[intuit[k]], font_size=20,
                               color={True: OK, False: BAD, None: GOAL}[intuit[k]])])
        grid = ValueGrid(hd, rows, col_w=[4.0, 1.3, 1.8, 1.3, 1.8], cell_h=0.52, font_size=20).move_to([0, 0.0, 0])
        foot = VGroup(label(r"the lottery: \ odds of a million to one, \ yet both say you don't know it will lose",
                            font_size=22, color=GREY_A),
                      label(r"knowledge is not high probability: \ the losing ticket could easily have won",
                            font_size=22, color=GOAL)).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the scorecard, every entry computed from the models. <bookmark mark='a'/>Gettier's coins, the "
            "stopped clock and Barn County: true beliefs, neither sensitive nor safe, and both conditions agree with "
            "the verdict that they are not knowledge. <bookmark mark='b'/>The lottery: you hold one ticket in a "
            "million and believe it will lose. You are almost certainly right, yet it seems you do not know it, and "
            "both conditions agree: a different ball dropping is a very small change to the world. Knowledge is not "
            "just high probability. <bookmark mark='c'/>The garbage chute and the vat are where they part: "
            "sensitivity says no, safety says yes, and intuition, at least about the rubbish, sides with safety. "
            "<bookmark mark='d'/>Neither checker is the final word. But safety has become the most widely accepted "
            "anti-luck condition, usually as a necessary condition on knowledge, not a definition of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(3)], lag_ratio=0.5), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*grid.cell[3])), FadeIn(foot))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(4, 7)], lag_ratio=0.5),
                      run_time=3)
            vo.wait_until("d")
            self.play(Indicate(VGroup(*[grid.cell[r][3] for r in range(7)]), color=KNOW))
        self.clear_scene()
