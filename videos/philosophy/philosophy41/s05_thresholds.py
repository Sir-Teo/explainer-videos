from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Thresholds(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Moving the thresholds", r"Can separate thresholds make the groups equal?", lit=(2016, 2017), part=PART)
        with self.voiceover("Chapter four. Moving the thresholds."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.groupwise()
        self.cost()
        self.ledger()
        self.beyond()

    def cost(self):
        head = label(r"The cost of fairness", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Corbett-Davies et al. \ (2017)", r"if the aim is to minimize crime and detention together, \ the best rule is a single threshold on a calibrated score", EXPL),
                (r"so", r"equalizing error rates means detaining some lower-risk people and releasing some higher-risk ones", BAD),
                (r"Hardt, \ Price and Srebro \ (2016)", r"`equal opportunity': \ equal true-positive rates, \ by post-processing, \ with randomized thresholds where needed", FAIRC),
                (r"the lesson", r"every fairness constraint has a price in accuracy or in someone's outcome: \ the price must be chosen", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Each choice has a measurable cost. <bookmark mark='a'/>Sam Corbett-Davies and colleagues showed in 2017 "
            "that if the aim is to minimize crime and detention together, the best rule is a single threshold on a "
            "calibrated score. <bookmark mark='b'/>So equalizing error rates means detaining some lower-risk people "
            "and releasing some higher-risk ones, and that harms someone too. <bookmark mark='c'/>Hardt, Price and "
            "Srebro defined equal opportunity as equal true-positive rates, achieved by post-processing, with "
            "randomized thresholds where needed. <bookmark mark='d'/>Every fairness constraint has a price, in "
            "accuracy or in someone's outcome, and someone must choose which price to pay."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def beyond(self):
        head = label(r"Beyond thresholds", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"fair training", r"constraints added during learning \ (Zafar et al., \ 2017; \ Agarwal et al., \ 2018)", FAIRC),
                (r"better data", r"many disparities come from measurement: \ arrests are not offences, \ costs are not needs", EXPL),
                (r"multicalibration", r"Hébert-Johnson et al. \ (2018): \ calibration on every identifiable subgroup at once", PRIV),
                (r"the impossibility stays", r"no algorithm escapes the identity; \ it only chooses where the errors fall", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Fairness can also be built in earlier. <bookmark mark='a'/>Constraints can be added during training, as "
            "in methods by Muhammad Bilal Zafar and colleagues in 2017 and Alekh Agarwal and colleagues in 2018. "
            "<bookmark mark='b'/>Many disparities come from what is measured: arrests are not offences, and health "
            "costs are not health needs, as the Obermeyer study found. <bookmark mark='c'/>Úrsula Hébert-Johnson and "
            "colleagues defined multicalibration in 2018: calibration on every identifiable subgroup at once. "
            "<bookmark mark='d'/>But no algorithm escapes the identity; each only chooses where the errors fall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def groupwise(self):
        g = load("thresholds")
        F_, P_ = g["fpr"], g["ppv"]
        assert abs(F_["A"]["fpr"] - F_["B"]["fpr"]) < 0.01 and abs(P_["A"]["ppv"] - P_["B"]["ppv"]) < 0.01
        head = label(r"A threshold for each group", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{goal}", r"\text{group}", r"\text{threshold}", r"\text{FPR}", r"\text{FNR}", r"\text{PPV}",
              r"\text{labelled high}"]
        cells = []
        for goal, D0, tag in (("fpr", F_, r"equal false positives"), ("ppv", P_, r"equal precision")):
            for gname in "AB":
                r0 = D0[gname]
                hit = {"fpr": "fpr", "ppv": "ppv"}[goal]
                cells.append([label(tag if gname == "A" else r"", font_size=18, color=FAIRC if goal == "fpr" else EXPL),
                              label(gname, font_size=19, color=GA if gname == "A" else GB),
                              label(f"{r0['t']:.2f}", font_size=19)] +
                             [label(f"{r0[k]:.2f}", font_size=19, color=GOAL if k == hit else WHITE)
                              for k in ("fpr", "fnr", "ppv")] +
                             [label(f"{r0['selected'] * 100:.0f}\\%", font_size=19, color=GREY_A)])
        grid = ValueGrid(hd, cells, col_w=[3.4, 1.0, 1.6, 1.3, 1.3, 1.3, 2.2], cell_h=0.55, font_size=17).move_to([0, 1.0, 0])
        foot = stack([(r"equal false positives \ (20\%): \ false negatives nearly equal, \ precision 0.55 against 0.74",
                       FAIRC),
                      (r"equal precision \ (0.70): \ false positives 4\% against 30\%", EXPL),
                      (r"group-specific thresholds treat people differently by group: \ disparate treatment, \ in law",
                       BAD)], font_size=20, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "If one threshold cannot satisfy both criteria, try one threshold for each group. <bookmark "
            "mark='a'/>Choose them so that both groups have a false-positive rate of twenty percent: the thresholds "
            "are point three nine for A and point five eight for B. False negatives come out nearly equal too, but "
            "precision does not: point five five in A, point seven four in B. A high-risk label now means less for "
            "group A. <bookmark mark='b'/>Choose them instead for equal precision of point seven: then group A's "
            "false-positive rate is four percent and group B's thirty. <bookmark mark='c'/>And thresholds that depend "
            "on group raise their own problem: treating people differently because of their group is disparate "
            "treatment, which anti-discrimination law forbids in many settings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c0) for rw in grid.cell[:2] for c0 in rw], FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(c0) for rw in grid.cell[2:] for c0 in rw], FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def ledger(self):
        g = load("thresholds")
        pols = [("single", r"one threshold, \ 0.5", WHITE), ("fpr", r"equal false positives", FAIRC),
                ("ppv", r"equal precision", EXPL), ("selected", r"equal selection \ (30\%)", PRIV)]
        n = sum(g["single"][x][k] for x in "AB" for k in ("tp", "fp", "fn", "tn"))
        errs, cells = [], []
        for key, name, col in pols:
            fp = g[key]["A"]["fp"] + g[key]["B"]["fp"]
            fn = g[key]["A"]["fn"] + g[key]["B"]["fn"]
            errs.append((fp, fn))
        e0 = sum(errs[0])
        assert n == 40000 and all(sum(e) >= e0 for e in errs) and e0 == 11160
        assert [sum(e) - e0 for e in errs] == [0, 585, 168, 932]
        for (key, name, col), (fp, fn) in zip(pols, errs):
            acc = 1 - (fp + fn) / n
            cells.append([label(name, font_size=19, color=col), label(f"{acc * 100:.1f}\\%", font_size=19),
                          label(f"{fp:,}", font_size=19, color=RESP), label(f"{fn:,}", font_size=19, color=FAIRC),
                          label("0" if fp + fn == e0 else f"+{fp + fn - e0:,}", font_size=19, color=GOAL)])
        head = label(r"The ledger of four policies \ (40,000 people)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        grid = ValueGrid([r"\text{policy}", r"\text{accuracy}", r"\text{innocent, labelled high}",
                          r"\text{reoffenders missed}", r"\text{extra errors}"], cells,
                         col_w=[3.3, 1.7, 3.2, 2.8, 1.9], cell_h=0.6, font_size=17).move_to([0, 1.3, 0])
        sa, sb = g["selected"]["A"], g["selected"]["B"]
        foot = stack([(r"the single threshold on a calibrated score makes the fewest errors", WHITE),
                      (r"equal precision costs least in total, \ but misses 980 more reoffenders", EXPL),
                      (rf"equal selection reverses the gap: \ false-positive rates {sa['fpr'] * 100:.0f}\% in A, \ "
                       rf"{sb['fpr'] * 100:.0f}\% in B", PRIV),
                      (r"each column is a burden on different people: \ choosing the policy is choosing who bears it", GOAL)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The Reasoner keeps a ledger of what each policy costs, for its forty thousand people. <bookmark "
            "mark='a'/>One threshold at point five, the same for everyone, is the most accurate: seventy-two point "
            "one percent. It labels four thousand three hundred and seventy-five innocent people high risk, and "
            "misses six thousand seven hundred and eighty-five who reoffend. On a calibrated score, no other policy "
            "makes fewer errors. <bookmark mark='b'/>Equal false-positive rates cost five hundred and eighty-five "
            "extra errors. Equal precision costs only one hundred and sixty-eight, but it misses nine hundred and "
            "eighty more people who go on to reoffend. <bookmark mark='c'/>Equal selection rates, demographic parity, "
            "cost the most, nine hundred and thirty-two errors, and they reverse the original gap: now group A's "
            "false-positive rate is nineteen percent and group B's fourteen. <bookmark mark='d'/>The columns are "
            "burdens on different people: innocent people detained, victims of crimes that were not prevented. No "
            "policy is free, and choosing among them is choosing who bears which cost."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c0) for c0 in grid.cell[0]], FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(c0) for rw in grid.cell[1:3] for c0 in rw], FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(c0) for c0 in grid.cell[3]], FadeIn(foot[2]))
            vo.wait_until("d")
            self.play(FadeIn(foot[3]), Indicate(grid.column(2), color=RESP, scale_factor=1.05),
                      Indicate(grid.column(3), color=FAIRC, scale_factor=1.05))
        self.clear_scene()
