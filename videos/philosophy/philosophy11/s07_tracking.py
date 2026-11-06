from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Tracking(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Tracking the truth", r"Would you believe it if it were false?", lit=(1981,),
                            part=PART)
        with self.voiceover("Chapter six. Tracking the truth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.conditions()
        self.barns()
        self.vat()

    def conditions(self):
        sp = load("spheres")["coins"]
        hc = history_card(1981, r"Robert Nozick", r"\textit{Philosophical Explanations}, \ ch.\ 3", width=5.4,
                          color=HIST).to_corner(UL, buff=0.35)
        conds = VGroup(
            MathTex(r"1.\ \ p", font_size=32),
            MathTex(r"2.\ \ B_S\,p", font_size=32),
            MathTex(r"3.\ \ \lnot p \;\Box\!\!\rightarrow\; \lnot B_S\,p", font_size=32, color=GOAL),
            MathTex(r"4.\ \ p \;\Box\!\!\rightarrow\; B_S\,p", font_size=32, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.25).move_to([-4.4, 0.0, 0])
        gloss = label(r"3: \ if $p$ were false, \ S would not believe it", font_size=21, color=GOAL).next_to(
            conds, DOWN, buff=0.3)
        sv = SpheresView(sp, "p", center=[2.6, 0.3, 0], step=1.4, angles={"nine coins": PI * 0.75,
                                                                          "jones hired": PI * 0.25},
                         names={"actual": "actual", "nine coins": "Smith has nine coins",
                                "jones hired": "Jones is hired"})
        lg = legend().next_to(sv, DOWN, buff=0.5)
        close = sv.disc(1, color=GOAL, opacity=0.06)
        verdict = label(r"the closest world where $p$ is false: \ Smith still believes $p$ \ $\Rightarrow$ \ "
                        r"insensitive: \ no knowledge", font_size=22, color=BAD).to_edge(DOWN, buff=0.35)
        v = sp["verdicts"][0]
        assert not v["sensitive"] and v["closest_not_p"] == ["nine coins"]
        with self.voiceover(
            "In 1981 Robert Nozick proposed that knowledge is belief that tracks the truth. <bookmark mark='a'/>S "
            "knows p when p is true, S believes it, and two counterfactuals hold. <bookmark mark='b'/>The third "
            "condition, now called sensitivity: if p were false, S would not believe p. The fourth: if p were true, "
            "S would believe it. <bookmark mark='c'/>To evaluate a counterfactual we look at the closest worlds where "
            "its antecedent holds. Here are Gettier's coins as the Reasoner models them. The actual world is at the "
            "centre, with nearby alternatives on the first ring: green where the belief is true, red where it is "
            "false, circled in white where Smith believes it. <bookmark mark='d'/>The closest world where the belief "
            "is false is the one where Smith has nine coins in his pocket. There Smith still believes it, for "
            "exactly the same reasons. So the belief is insensitive, and Nozick's analysis says, correctly, that "
            "Smith does not know."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(conds[0]), FadeIn(conds[1]))
            vo.wait_until("b")
            self.play(FadeIn(conds[2]), FadeIn(gloss))
            self.play(FadeIn(conds[3]))
            vo.wait_until("c")
            self.play(FadeIn(sv), FadeIn(lg))
            vo.wait_until("d")
            self.play(FadeIn(close), Indicate(sv.dot["nine coins"], color=BAD, scale_factor=1.6))
            self.play(FadeIn(verdict))
        self.clear_scene()

    def barns(self):
        sp = load("spheres")["barns"]
        v = {r["p"]: r for r in sp["verdicts"]}
        assert not v["barn"]["sensitive"] and v["red barn"]["sensitive"]
        head = label(r"Barn County, \ with Kripke's twist: \ every facade is green", font_size=30,
                     color=CONN).to_edge(UP, buff=0.3)
        ang = {"green facade": PI * 0.78, "green barn": PI * 0.22, "empty field": -PI * 0.5, "red facade": PI * 0.5}
        nm = {"red barn": "the red barn", "green facade": "a green facade", "green barn": "a green barn",
              "empty field": "an empty field", "red facade": "a red facade"}
        a = SpheresView(sp, "barn", center=[-3.5, -0.2, 0], step=0.75, angles=ang, names=nm, font_size=16)
        b = SpheresView(sp, "red barn", center=[3.5, -0.2, 0], step=0.75, angles=ang, names=nm, font_size=16)
        ta = label(r"`there is a barn'", font_size=26, color=BEL).next_to(a, UP, buff=0.2)
        tb = label(r"`there is a red barn'", font_size=26, color=BEL).next_to(b, UP, buff=0.2)
        va = label(r"closest not-barn: \ a facade, \ believed: \ insensitive", font_size=20, color=BAD).next_to(
            a, DOWN, buff=0.25)
        vb = label(r"closest not-red-barn: \ believed nowhere: \ sensitive", font_size=20, color=OK).next_to(
            b, DOWN, buff=0.25)
        abom = label(r"Henry knows there is a red barn, \ but not that there is a barn", font_size=26,
                     color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Sensitivity also gets Barn County right: had Henry been looking at a facade, he would still have "
            "believed there was a barn, so he does not know. But Saul Kripke, in lectures that circulated for "
            "decades, added a twist. <bookmark mark='a'/>Suppose every facade in the county is green, and the one "
            "real barn Henry looks at is red. Henry believes two things: there is a barn, and there is a red barn. "
            "<bookmark mark='b'/>The Reasoner checks the first. The closest world where there is no barn is one where "
            "he looks at a green facade, and there he still believes there is a barn. Insensitive. "
            "<bookmark mark='c'/>Now the second. The closest worlds where there is no red barn show a green facade or "
            "a green barn, and in neither does he believe he sees a red barn. A red facade would fool him, but no one "
            "has ever made one: that world is far away. Sensitive. <bookmark mark='d'/>So, on Nozick's analysis, "
            "Henry knows that there is a red barn, but does not know that there is a barn. Keith DeRose called "
            "sentences like this abominable conjunctions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(b), FadeIn(ta), FadeIn(tb))
            vo.wait_until("b")
            self.play(Indicate(a.dot["green facade"], color=BAD, scale_factor=1.6), FadeIn(va))
            vo.wait_until("c")
            self.play(Indicate(b.dot["green facade"], color=OK, scale_factor=1.6),
                      Indicate(b.dot["green barn"], color=OK, scale_factor=1.6), FadeIn(vb))
            vo.wait_until("d")
            self.play(FadeIn(abom))
        self.clear_scene()

    def vat(self):
        sp = load("spheres")["biv"]
        v = {r["p"]: r for r in sp["verdicts"]}
        assert v["hands"]["sensitive"] and not v["not_biv"]["sensitive"]
        head = label(r"Sensitivity, \ hands, \ and the vat", font_size=32, color=CONN).to_edge(UP, buff=0.3)
        ang = {"lost hands": PI * 0.75, "envatted": PI * 0.25}
        nm = {"normal": "you", "lost hands": "no hands", "envatted": "envatted"}
        a = SpheresView(sp, "hands", center=[-3.5, -0.3, 0], step=1.1, angles=ang, names=nm)
        b = SpheresView(sp, "not_biv", center=[3.5, -0.3, 0], step=1.1, angles=ang, names=nm)
        ta = label(r"`I have hands'", font_size=26, color=BEL).next_to(a, UP, buff=0.2)
        tb = label(r"`I am not a brain in a vat'", font_size=26, color=BEL).next_to(b, UP, buff=0.2)
        va = label(r"sensitive: \ without hands, \ I'd see none", font_size=21, color=OK).next_to(a, DOWN,
                                                                                               buff=0.25)
        vb = label(r"insensitive: \ envatted, \ I'd believe the same", font_size=21, color=BAD).next_to(
            b, DOWN, buff=0.25)
        foot = label(r"I know I have hands, \ but not what obviously follows: \ closure fails \ (Chapter 11)",
                     font_size=24, color=GOAL).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The deepest consequence concerns skepticism. <bookmark mark='a'/>Take two of my beliefs: I have hands, "
            "and I am not a brain in a vat. <bookmark mark='b'/>The first is sensitive: if I had lost my hands, I "
            "would see that I had none. <bookmark mark='c'/>The second is not. If I were a brain in a vat, fed the "
            "same experiences, I would believe I was not one. <bookmark mark='d'/>So on Nozick's view I know that I "
            "have hands, but not that I am not a brain in a vat, even though the first obviously implies the second. "
            "Knowledge is not closed under known implication. Nozick accepted this, and thought it was the truth in "
            "skepticism. We return to it in chapter eleven."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a), FadeIn(b), FadeIn(ta), FadeIn(tb))
            vo.wait_until("b")
            self.play(Indicate(a.dot["lost hands"], color=OK, scale_factor=1.6), FadeIn(va))
            vo.wait_until("c")
            self.play(Indicate(b.dot["envatted"], color=BAD, scale_factor=1.6), FadeIn(vb))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
