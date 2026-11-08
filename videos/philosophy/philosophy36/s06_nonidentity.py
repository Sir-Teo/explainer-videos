from __future__ import annotations

from videos.philosophy.philosophy36.common import *  # noqa: F403


class NonIdentity(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Person-affecting views", r"Can an outcome be worse if it is worse for no one?",
                            lit=(1973, 1984), part=PART)
        with self.voiceover("Chapter five. Person-affecting views."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.asymmetry()
        self.neutral()
        self.benatar()
        self.depletion()
        self.girl()
        self.hmv()

    def asymmetry(self):
        q = quote_card(r"We are in favour of making people happy, \ but neutral about making happy people.",
                       r"Jan Narveson", r"``Moral Problems of Population'' \ (1973)", width=9.0,
                       font_size=30).move_to([0, 1.6, 0])
        rows = [(r"the person-affecting restriction", r"an outcome can be worse only if it is worse for someone", POP),
                (r"the asymmetry", r"we have strong reason not to create a miserable life, \ but none to create a "
                                   r"happy one \ (McMahan, \ 1981)", RISK),
                (r"its appeal", r"it avoids the repugnant conclusion at a stroke: \ merely possible people make no "
                                r"claims", WELL),
                (r"its puzzle", r"if a happy life is not good for the one who would live it, \ why is a miserable "
                                r"life bad for hers?", GOAL)]
        g = rows_table(rows, top=0.1, gap=0.32, width=7.6, x_text=-1.6, label_size=19, text_size=19)
        with self.voiceover(
            "Many people find the whole question odd. <bookmark mark='a'/>Jan Narveson put the intuition in 1973: we "
            "are in favour of making people happy, but neutral about making happy people. <bookmark mark='b'/>Behind "
            "it is a person-affecting restriction: an outcome can be worse only if it is worse for someone. "
            "<bookmark mark='c'/>It comes with an asymmetry, so named by Jeff McMahan in 1981: we have strong reason "
            "not to create a life that would be miserable, but no comparable reason to create one that would be "
            "happy. <bookmark mark='d'/>The view avoids the repugnant conclusion at a stroke, since people who would "
            "merely be possible make no claims on us. <bookmark mark='e'/>But it has a puzzle at its heart: if a happy "
            "life is not good for the person who would live it, why is a miserable life bad for the person who "
            "would live that one?"
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            for mk, r in zip("bcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def neutral(self):
        d = load("neutrality")
        head = label(r"Neutrality cannot be a range \ (Broome, \ 2004)", font_size=30, color=CONN).to_edge(UP,
                                                                                                        buff=0.3)
        assert (d["base"], d["levels"], d["count"]) == (10.0, [2, 4, 6, 8], 6)
        base_y = -1.4
        A = parfit_bars([(1, 10)], -6.0, base_y, unit_w=0.7, unit_h=0.2, color=WELL)
        A4 = VGroup(parfit_bars([(1, 10)], -3.2, base_y, unit_w=0.7, unit_h=0.2, color=WELL),
                    parfit_bars([(1, 4)], -2.45, base_y, unit_w=0.7, unit_h=0.2, color=POP))
        A8 = VGroup(parfit_bars([(1, 10)], -0.4, base_y, unit_w=0.7, unit_h=0.2, color=WELL),
                    parfit_bars([(1, 8)], 0.35, base_y, unit_w=0.7, unit_h=0.2, color=POP))
        names = VGroup(label(r"A", font_size=20, color=GOAL).next_to(A, DOWN, buff=0.15),
                       label(r"A + someone at 4", font_size=18, color=GOAL).next_to(A4, DOWN, buff=0.15),
                       label(r"A + the same person at 8", font_size=18, color=GOAL).next_to(A8, DOWN, buff=0.15))
        rel = VGroup(MathTex(r"\sim", font_size=40, color=FUT).move_to([-4.2, 0.0, 0]),
                     MathTex(r"\sim", font_size=40, color=FUT).move_to([-1.3, 0.0, 0]))
        side = stack([(r"neutrality: \ adding someone at any level in a range is equally as good as not", FUT),
                      (r"then $A \sim A_4$ and $A \sim A_8$, \ so by transitivity $A_4 \sim A_8$", FUT),
                      (r"but $A_8$ is better than $A_4$: \ the same people, \ one of them better off", BAD),
                      (r"levels 2, \ 4, \ 6, \ 8: \ all 6 pairs contradict", GOAL),
                      (r"so neutrality holds at one level at most: \ a critical level", RISK)],
                     font_size=18, aligned_edge=LEFT, width=5.0, buff=0.28).move_to([4.3, 0.0, 0])
        with self.voiceover(
            "John Broome, in Weighing Lives, of 2004, argued that the intuition of neutrality cannot be quite what "
            "it seems. <bookmark mark='a'/>Neutrality says that adding a person at any level within a range of good "
            "lives is equally as good as not adding her. <bookmark mark='b'/>Then A, a world of one person, is "
            "equally as good as A plus someone at four, and equally as good as A plus the same person at eight. By "
            "transitivity, those two are equally good. <bookmark mark='c'/>But the second is plainly better than the "
            "first: the same people, with one of them better off. <bookmark mark='d'/>The Reasoner tries a range of "
            "four levels, two, four, six and eight; every one of the six pairs gives a contradiction. "
            "<bookmark mark='e'/>So neutrality can hold at one level at most, which is a critical-level view, with "
            "the sadistic conclusion that comes with it. Broome concluded that the intuition, however attractive, "
            "cannot be right as it stands, and that vagueness in betterness may explain its pull."
        ) as vo:
            self.play(FadeIn(head), GrowFromEdge(A, DOWN), FadeIn(names[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(A4, DOWN), FadeIn(names[1]), FadeIn(rel[0]))
            self.play(GrowFromEdge(A8, DOWN), FadeIn(names[2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(rel[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def benatar(self):
        head = label(r"Better never to have been? \ (Benatar, \ 2006)", font_size=30, color=CONN).to_edge(UP,
                                                                                                         buff=0.3)
        hd = [r"", r"\text{if the person exists}", r"\text{if she never exists}"]
        cells = [[label(r"pain", font_size=20, color=RISK), label(r"present: \ bad", font_size=19, color=BAD),
                  label(r"absent: \ good, \ though no one enjoys it", font_size=19, color=OK)],
                 [label(r"pleasure", font_size=20, color=WELL), label(r"present: \ good", font_size=19, color=OK),
                  label(r"absent: \ not bad, \ for no one is deprived", font_size=19, color=GREY_A)]]
        grid = ValueGrid(hd, cells, col_w=[2.0, 4.0, 5.6], cell_h=0.7, font_size=17).move_to([0, 0.8, 0])
        side = stack([(r"never existing beats existing on pain, \ and ties on pleasure", BAD),
                      (r"so coming into existence is always a harm: \ antinatalism", BAD),
                      (r"the asymmetry of this chapter, \ pushed to its limit", FUT),
                      (r"replies: \ the absence of pleasure is a loss if anything is; \ or the asymmetry was wrong",
                       GREY_A)],
                     font_size=19, aligned_edge=LEFT, width=10.4, buff=0.22).move_to([0, -1.8, 0])
        with self.voiceover(
            "David Benatar took the asymmetry to its limit in Better Never to Have Been, of 2006. "
            "<bookmark mark='a'/>Compare a person's existing with her never existing. If she exists, her pains are "
            "bad and her pleasures good. If she never exists, the absence of her pains is good, even though no one "
            "enjoys it, while the absence of her pleasures is not bad, because no one is deprived of them. "
            "<bookmark mark='b'/>Never existing then wins on pain and ties on pleasure, however good the life. "
            "<bookmark mark='c'/>So coming into existence is always a harm, and it would be better if no more people "
            "were born: antinatalism. <bookmark mark='d'/>Most philosophers reject the conclusion, and so must "
            "reject a premise: either the absence of pleasure is a loss if the absence of pain is a gain, or the "
            "asymmetry of this chapter was wrong from the start."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for row in grid.cell for c in row])
            for mk, r in zip("bcd", (side[0], VGroup(side[1], side[2]), side[3])):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def depletion(self):
        d = load("nonidentity")
        rows = {r["policy"]: r for r in d["rows"]}
        head = label(r"The non-identity problem \ (Parfit, \ 1984): \ depletion", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert (d["now_people"], d["later_people"], d["harmed_by_depletion"]) == (100, 1000, 0)
        assert (rows["depletion"]["total"], rows["conservation"]["total"]) == (41000, 60000)
        assert d["total_prefers"] == "conservation"
        hd = [r"\text{policy}", r"\text{we gain, each}", r"\text{people in 300 years}", r"\text{their welfare}",
              r"\text{total}"]
        cells = [[label(n, font_size=18, color=RISK if n == "depletion" else WELL),
                  label(f"{rows[n]['now']}", font_size=18), label(r"a different 1000", font_size=17, color=GREY_A),
                  label(f"{rows[n]['later']}", font_size=18), label(f"{rows[n]['total']:,}", font_size=18,
                                                                    color=GOAL)] for n in ("depletion", "conservation")]
        grid = ValueGrid(hd, cells, col_w=[2.6, 2.4, 3.2, 2.2, 1.8], cell_h=0.55, font_size=16).move_to([0, 0.9, 0])
        side = stack([(r"which people are born depends on when their parents meet: \ different policies, \ different "
                       r"people", FUT),
                      (r"is anyone worse off under depletion than they would otherwise be? \ the Reasoner checks each "
                       r"person: \ 0", POP),
                      (r"the narrow person-affecting view: \ so depletion is not worse", RISK),
                      (r"almost everyone thinks it is: \ the total view agrees, \ 41,000 against 60,000", WELL)],
                     font_size=19, aligned_edge=LEFT, width=10.4, buff=0.25).move_to([0, -1.6, 0])
        with self.voiceover(
            "Parfit's non-identity problem tests the restriction hardest. <bookmark mark='a'/>A society chooses "
            "between depleting its resources and conserving them. Depletion gives each of us a little more, ten "
            "units, and in three centuries the people alive are worse off, at forty. Conservation gives us nothing "
            "extra, and the people then are at sixty. <bookmark mark='b'/>But which people are born depends on who "
            "meets whom, and when; a policy this large changes all of that. After three centuries, the two policies "
            "lead to entirely different people. <bookmark mark='c'/>So is anyone worse off under depletion than they "
            "would otherwise have been? The Reasoner checks each person: we are better off; the later people would "
            "not have existed at all, and their lives are worth living. The count is zero. "
            "<bookmark mark='d'/>A narrow person-affecting view must say depletion is not worse. "
            "<bookmark mark='e'/>Almost everyone thinks it is, and the total view agrees: forty one thousand against "
            "sixty thousand."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for row in grid.cell for c in row])
            for mk, r in zip("bcde", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def girl(self):
        head = label(r"Wide and narrow", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the fourteen-year-old girl", r"Parfit: \ she chooses to have a child now, \ who will have a worse "
                                                r"start than the child she would have at twenty-five; \ the child she "
                                                r"has is not worse off than otherwise, \ for otherwise it would not "
                                                r"exist", RISK),
                (r"wide person-affecting views", r"compare the people who exist in each outcome by their places, \ "
                                                 r"not their identities \ (Parfit; \ Hare): \ depletion is worse for "
                                                 r"`the future generation'", POP),
                (r"Parfit's Q", r"if the same number would live either way, \ it is worse if those who live are worse "
                                r"off: \ his \textit{same number quality claim}", WELL),
                (r"climate", r"every large policy is a non-identity case: \ our emissions decide who will exist", FUT)]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.0, x_text=-1.8, label_size=19, text_size=19)
        with self.voiceover(
            "Parfit's best-known example is personal. <bookmark mark='a'/>A fourteen-year-old girl chooses to have a "
            "child now, rather than in ten years, when she could give a child a far better start. The child she has "
            "is not worse off than it would otherwise have been, because otherwise it would not have existed; yet her "
            "choice seems regrettable. <bookmark mark='b'/>Wide person-affecting views compare the people in each "
            "outcome by their places rather than their identities: whoever her child is, her first child is worse "
            "off. <bookmark mark='c'/>Parfit's own principle Q says that if the same number of people would live "
            "either way, it is worse if those who live are worse off than those who would have lived. "
            "<bookmark mark='d'/>The problem is not academic. Every large policy, on climate above all, changes who "
            "will exist, so the people it will harm are, strictly, people it creates."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def hmv(self):
        d = load("hmv")
        head = label(r"Harm minimization \ (Meacham, \ 2012)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["depletion_harm"], d["conservation_harm"], d["A_harm"], d["Z_harm"]) == (20000, 1000, 0, 997.5)
        assert (d["choose_depletion_case"], d["choose_AZ"]) == ("conservation", "A")
        rows = [(r"counterparts", r"match the people of different outcomes one to one, \ by their places", POP),
                (r"harm", r"a person is harmed by how much better her counterpart does in another outcome; \ a good "
                          r"life with no counterpart harms no one", RISK),
                (r"the rule", r"choose the outcome with the least total harm", GOAL)]
        g = rows_table(rows, top=1.7, gap=0.32, width=8.6, x_text=-2.4, label_size=19, text_size=19)
        hd = [r"\text{case}", r"\text{outcome}", r"\text{total harm}", r"\text{verdict}"]
        cells = [[label(r"depletion", font_size=18, color=FUT), label(r"deplete", font_size=18),
                  label(r"1000 later people $\times$ 20 = 20,000", font_size=18), label(r"", font_size=18)],
                 [label(r"", font_size=18), label(r"conserve", font_size=18),
                  label(r"100 of us $\times$ 10 = 1,000", font_size=18), label(r"conserve", font_size=18, color=OK)],
                 [label(r"A against Z", font_size=18, color=FUT), label(r"Z", font_size=18),
                  label(r"A's 10 counterparts $\times$ 99.75 = 997.5", font_size=18), label(r"", font_size=18)],
                 [label(r"", font_size=18), label(r"A", font_size=18), label(r"0", font_size=18),
                  label(r"A", font_size=18, color=OK)]]
        grid = ValueGrid(hd, cells, col_w=[2.4, 1.8, 5.6, 1.8], cell_h=0.48, font_size=17).move_to([0, -1.1, 0])
        foot = label(r"the price: \ verdicts depend on which outcomes are on the menu", font_size=18,
                     color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Can a person-affecting view be made to work? Christopher Meacham proposed one in 2012. "
            "<bookmark mark='a'/>Match the people of different outcomes one to one, by their places, so that the "
            "first child born in one outcome is the counterpart of the first child born in the other. "
            "<bookmark mark='b'/>A person is harmed by how much better her counterpart fares in another outcome; a "
            "good life with no counterpart harms no one. <bookmark mark='c'/>Choose the outcome with the least total "
            "harm. <bookmark mark='d'/>The Reasoner runs it on depletion. The thousand later people of depletion are "
            "each harmed by twenty, against their counterparts at sixty: twenty thousand. Under conservation, the "
            "hundred of us lose ten each: a thousand. Conserve: the non-identity problem is answered. "
            "<bookmark mark='e'/>And on A against Z: in Z, the ten people who stand in the places of A's ten are "
            "harmed by ninety nine point seven five each, while in A no one is harmed. Choose A: no repugnant "
            "conclusion. The price is that the verdict can change when an outcome is added to the menu, which a "
            "ranking of outcomes should never do."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for k in range(2) for c in grid.cell[k]])
            vo.wait_until("e")
            self.play(*[FadeIn(c) for k in range(2, 4) for c in grid.cell[k]], FadeIn(foot))
        self.clear_scene()
