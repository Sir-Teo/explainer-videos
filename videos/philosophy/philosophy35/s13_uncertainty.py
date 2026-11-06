from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Uncertainty(VoiceoverScene):
    def construct(self):
        card = chapter_card(12, r"Moral uncertainty", r"What should you do if you do not know which theory is true?",
                            lit=(2020,), part=PART)
        with self.voiceover("Chapter twelve. Moral uncertainty."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.mec()
        self.normalize()
        self.parliament()
        self.information()

    def mec(self):
        head = label(r"Maximize expected choiceworthiness", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"\mathrm{EC}(a) \;=\; \sum_{T} P(T)\, \mathrm{CW}_T(a)", font_size=40, color=AGG).move_to(
            [0, 1.4, 0])
        rows = stack([(r"you have credences in moral theories, \ as in empirical ones", GREY_A),
                      (r"each theory scores each option: \ its choiceworthiness", GOOD),
                      (r"act on the expectation: \ the analogue of Part 33's expected utility", AGG),
                      (r"MacAskill, \ Bykvist and Ord, \ \textit{Moral Uncertainty} \ (2020)", HIST),
                      (r"the hard part: \ comparing one theory's units with another's", BAD)], font_size=20,
                     buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "This part has shown that each theory gets some cases wrong. So you may well be uncertain which is true. "
            "<bookmark mark='a'/>Then you have credences in moral theories, as in empirical hypotheses. "
            "<bookmark mark='b'/>Each theory scores each option by how choiceworthy it is. <bookmark mark='c'/>One "
            "proposal is to maximize expected choiceworthiness, the analogue of expected utility from Part 33. "
            "<bookmark mark='d'/>William MacAskill, Krister Bykvist and Toby Ord developed it in Moral Uncertainty, "
            "in 2020. <bookmark mark='e'/>The hard part is comparing one theory's units with another's: how many "
            "utilitarian lives is one deontological violation worth?"
        ) as vo:
            self.play(FadeIn(head), Write(f))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def normalize(self):
        d = load("uncertainty")
        head = label(r"The answer depends on the exchange rate", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["credence"] == {"utilitarian": 0.6, "deontological": 0.4}
        two = d["two"]
        r = two["results"]
        assert (r["raw"]["choice"], r["range"]["choice"], r["variance"]["choice"]) == ("do nothing", "push", "push")
        th = two["theories"]
        hd = [r"\text{theory}", r"\text{credence}", r"\text{push}", r"\text{do nothing}"]
        cells = [[label(t, font_size=18, color=GOOD if t == "utilitarian" else DUTY),
                  label(f"{d['credence'][t]:g}", font_size=18), label(f"{th[t][0]:+d}", font_size=18),
                  label(f"{th[t][1]:+d}", font_size=18)] for t in ("utilitarian", "deontological")]
        grid = ValueGrid(hd, cells, col_w=[3.0, 1.8, 1.6, 2.2], cell_h=0.55, font_size=17).move_to([-2.4, 1.0, 0])
        hd2 = [r"\text{comparison}", r"\mathrm{EC}(\text{push})", r"\mathrm{EC}(\text{nothing})", r"\text{choice}"]
        cells2 = [[label(nm, font_size=17, color=GREY_A), label(f"{r[k]['scores'][0]:.2f}", font_size=17),
                   label(f"{r[k]['scores'][1]:.2f}", font_size=17),
                   label(r[k]["choice"], font_size=17, color=OK if r[k]["choice"] == "push" else DUTY)]
                  for nm, k in ((r"raw numbers", "raw"), (r"range normalized", "range"),
                                (r"variance normalized", "variance"))]
        grid2 = ValueGrid(hd2, cells2, col_w=[3.0, 2.0, 2.2, 2.0], cell_h=0.55, font_size=17).move_to([-2.4, -1.6, 0])
        side = stack([(r"the footbridge: \ push saves four net lives; \ the deontologist calls it a grave wrong", GREY_A),
                      (r"on the raw scale the grave wrong dominates: \ do nothing", DUTY),
                      (r"rescale each theory to the same spread, \ and push wins", GOOD),
                      (r"fanaticism: \ a theory with huge stakes can swamp the rest, \ however unlikely", BAD)],
                     font_size=18, aligned_edge=LEFT, width=4.2, buff=0.3).move_to([4.6, -0.3, 0])
        with self.voiceover(
            "The Reasoner tries it on the footbridge. <bookmark mark='a'/>Credence point six in a utilitarian theory, "
            "for which pushing saves four lives net, and point four in a deontological theory, for which pushing is "
            "a grave wrong, scored minus a hundred. <bookmark mark='b'/>Taking the numbers at face value, the grave "
            "wrong dominates: minus thirty seven point six for pushing, so do nothing. <bookmark mark='c'/>But nothing "
            "fixed the deontologist's scale. Rescale each theory to the same range, or to the same variance across "
            "the options, as MacAskill and his co-authors suggest, and pushing wins. <bookmark mark='d'/>The verdict "
            "depends on the exchange rate between theories, and a theory that announces enormous stakes can swamp "
            "all the others however little you believe it: the problem of fanaticism, which returns in Part 36."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for row in grid.cell for c in row])
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(grid2.head), Create(grid2.rule), *[FadeIn(c) for c in grid2.cell[0]], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(c) for k in (1, 2) for c in grid2.cell[k]], FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def parliament(self):
        d = load("uncertainty")
        head = label(r"A third option, \ and a moral parliament", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        r = d["three"]["results"]
        assert [r[k]["choice"] for k in ("raw", "range", "variance")] == ["shout a warning"] * 3
        assert r["plurality"]["choice"] == "push"
        rows = stack([(r"add an option both theories accept: \ shout a warning that saves two of the five", GOOD),
                      (r"every form of expected choiceworthiness now chooses it: \ raw, \ range, \ variance", AGG),
                      (r"a parliament that just votes \ (seats in proportion to credence, \ each for its favourite): "
                       r"\ the utilitarian majority pushes", BAD),
                      (r"Bostrom \ (2009); \ Newberry and Ord \ (2021): \ let the delegates bargain, \ and compromise "
                       r"options win", DUTY),
                      (r"uncertainty rewards looking for acts that many theories can accept", GOAL)], font_size=20,
                     buff=0.3).move_to([0, -0.2, 0])
        with self.voiceover(
            "Often there are more than two options. <bookmark mark='a'/>Add one that both theories can accept: shout "
            "a warning that saves two of the five. <bookmark mark='b'/>Now every version of expected choiceworthiness "
            "chooses it, raw, range normalized or variance normalized. <bookmark mark='c'/>A different proposal is a "
            "moral parliament, in which each theory gets seats in proportion to your credence. If the delegates "
            "simply vote for their favourites, the utilitarian majority pushes. <bookmark mark='d'/>Nick Bostrom, "
            "and Toby Newberry and Toby Ord, proposed instead that the delegates bargain, which favours "
            "compromises like the warning. <bookmark mark='e'/>The practical lesson of moral uncertainty is to look "
            "for acts that many theories can accept."
        ) as vo:
            self.play(FadeIn(head))
            for mk, x in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(x))
        self.clear_scene()

    def information(self):
        d = load("moralinfo")
        head = label(r"The value of moral information", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        v, rg, raw = d["variance"], d["range"], d["raw"]
        assert (v["at_0.6"], v["now_at_0.6"], v["peak_p"], v["peak"]) == (0.8, 0.2, 0.5, 1.0)
        assert (rg["at_0.6"], rg["peak_p"]) == (0.4, 0.5) and (raw["peak_p"], raw["peak"], raw["at_0.6"]) == (0.96, 3.84,
                                                                                                             2.4)
        f = MathTex(r"\mathrm{VOI}(p) \;=\; \mathbb{E}_T\big[\max_a \mathrm{CW}_T(a)\big] \;-\; "
                    r"\max_a \mathbb{E}_T\big[\mathrm{CW}_T(a)\big]", font_size=32, color=AGG).next_to(head, DOWN,
                                                                                                    buff=0.3)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 1, 0.25], x_length=5.8, y_length=3.4, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15, "include_numbers": True,
                               "decimal_number_config": {"num_decimal_places": 2}}).move_to([-3.4, -1.1, 0])
        xl = label(r"credence in the utilitarian theory", font_size=16, color=GREY_A).next_to(ax.x_axis, DOWN,
                                                                                              buff=0.42)
        cv = VMobject(color=GOOD, stroke_width=3).set_points_as_corners([ax.c2p(p, y) for p, y in zip(d["p"],
                                                                                                    v["voi"])])
        cr = VMobject(color=DUTY, stroke_width=3).set_points_as_corners([ax.c2p(p, y) for p, y in zip(d["p"],
                                                                                                    rg["voi"])])
        lv = label(r"variance-normalized", font_size=15, color=GOOD).next_to(ax.c2p(0.5, 1.0), RIGHT, buff=0.15)
        lr = label(r"range-normalized", font_size=15, color=DUTY).next_to(ax.c2p(0.5, 0.5), UP, buff=0.12)
        mk6 = DashedLine(ax.c2p(0.6, 0), ax.c2p(0.6, 1), color=GREY_A, stroke_width=1.5)
        dot = Dot(ax.c2p(0.6, 0.8), radius=0.07, color=WHITE)
        side = stack([(r"the footbridge again: \ push, \ or do nothing", GREY_A),
                      (r"credence 0.6, \ variance scales: \ choose now, \ 0.2; \ learn first, \ 1.0", GOOD),
                      (r"so the information is worth 0.8: \ four times the best choice now", GOOD),
                      (r"never negative; \ largest where you are most torn, \ at 0.5", AGG),
                      (r"raw scales: \ largest at credence 0.96, \ where the verdict flips", HARM),
                      (r"when theories disagree about large stakes, \ finding out can matter more than any one "
                       r"choice", GOAL)],
                     font_size=18, aligned_edge=LEFT, width=5.0, buff=0.26).move_to([3.9, -1.0, 0])
        with self.voiceover(
            "If moral uncertainty is real, moral inquiry has a value, like any other information. "
            "<bookmark mark='a'/>How much would it be worth to learn which theory is true before acting on the "
            "footbridge? Use the value of information from Part 33: the expected value of choosing after you learn, "
            "minus the value of choosing now. <bookmark mark='b'/>With the scales matched by variance and a "
            "credence of point six, choosing now is worth point two, and choosing after learning is worth one. "
            "<bookmark mark='c'/>So the information is worth point eight, four times what the best choice now is "
            "worth. <bookmark mark='d'/>The value is never negative, and it is largest where you are most torn, at "
            "even credence. <bookmark mark='e'/>On the raw scales the peak moves to a credence of ninety six percent, "
            "where the grave wrong and the four lives just balance. <bookmark mark='f'/>The lesson holds for anyone "
            "who must act under moral uncertainty, a government, a hospital or a machine: when theories disagree "
            "about large stakes, finding out which is true can matter more than any single choice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(f), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(lv), Create(mk6), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(dot), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(cr), FadeIn(lr), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
        self.clear_scene()
