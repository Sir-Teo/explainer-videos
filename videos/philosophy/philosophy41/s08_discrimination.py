from __future__ import annotations

from videos.philosophy.philosophy41.common import *  # noqa: F403


class Discrimination(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"What makes discrimination wrong?", r"When is treating groups differently unjust?", lit=(1971, 2008), part=PART)
        with self.voiceover("Chapter seven. What makes discrimination wrong?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.law()
        self.unaware()
        self.wrong()
        self.cases()
        self.insurance()

    def law(self):
        head = history_card(1971, r"\textit{Griggs v. Duke Power}", r"disparate impact", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"disparate treatment", r"deciding differently because of a protected characteristic", RESP),
                (r"disparate impact", r"\textit{Griggs v. Duke Power} \ (1971): \ a neutral rule with unequal effects must be justified by business necessity", FAIRC),
                (r"statistical discrimination", r"Phelps \ (1972); \ Arrow \ (1973): \ using group averages as evidence about individuals, \ even without animus", EXPL),
                (r"proxies", r"zip codes and purchase histories stand in for race: \ removing the variable does not remove the information", BAD)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The law of discrimination supplies two concepts. <bookmark mark='a'/>Disparate treatment is deciding "
            "differently because of a protected characteristic such as race or sex. <bookmark mark='b'/>Disparate "
            "impact, from the Supreme Court's Griggs versus Duke Power of 1971, holds that a neutral rule with "
            "unequal effects, like a diploma requirement, must be justified by business necessity. <bookmark "
            "mark='c'/>Economists Edmund Phelps and Kenneth Arrow described statistical discrimination in the early "
            "1970s: using group averages as evidence about individuals, even without any animus. <bookmark "
            "mark='d'/>Machine learning makes the last point acute: removing a protected variable does not remove the "
            "information, because zip codes and purchase histories stand in for it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def wrong(self):
        head = label(r"What makes discrimination wrong?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"harm", r"discrimination wrongs by worsening people's lives, \ especially the already disadvantaged \ (Lippert-Rasmussen, \ 2014)", RESP),
                (r"demeaning", r"Hellman \ (2008): \ \textit{When Is Discrimination Wrong?}: \ when it expresses that some count for less", FAIRC),
                (r"disrespect", r"Eidelson \ (2015): \ failing to treat people as individuals, \ the authors of their own lives", EXPL),
                (r"for algorithms", r"a model has no attitudes: \ harm and disrespect-as-practice survive; \ demeaning needs a social meaning", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Philosophers disagree about why discrimination is wrong. <bookmark mark='a'/>On harm-based views, such "
            "as Kasper Lippert-Rasmussen's, it wrongs people by making their lives worse, especially those already "
            "disadvantaged. <bookmark mark='b'/>Deborah Hellman's When Is Discrimination Wrong?, of 2008, answers: "
            "when it demeans, expressing that some people count for less. <bookmark mark='c'/>Benjamin Eidelson's "
            "Discrimination and Disrespect, of 2015, locates the wrong in failing to treat people as individuals, the "
            "authors of their own lives. <bookmark mark='d'/>For algorithms the views come apart: a model has no "
            "attitudes, so harm-based and practice-based accounts apply directly, while the expressive account needs "
            "to ask what a system's use means in its society."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def cases(self):
        head = label(r"Audits in practice", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Gender Shades \ (2018)", r"error rates up to 34.7\% for darker-skinned women, \ under 1\% for lighter-skinned men; \ vendors improved after publication", PRIV),
                (r"health \ (2019)", r"replacing cost with a direct measure of need raised the share of Black patients flagged for extra care from 17.7\% to 46.5\%", FAIRC),
                (r"hiring law", r"New York City's Local Law 144 \ (2023): \ bias audits of automated hiring tools", EXPL),
                (r"lending", r"US fair-lending law applies disparate impact to credit models", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Audits show what can be done. <bookmark mark='a'/>Gender Shades, by Buolamwini and Gebru in 2018, found "
            "error rates of up to thirty five percent for darker-skinned women and under one percent for "
            "lighter-skinned men, and the vendors' systems improved after publication. <bookmark mark='b'/>In the "
            "health study, replacing the cost target with a direct measure of illness would raise the share of Black "
            "patients flagged for extra care from about eighteen percent to forty seven. <bookmark mark='c'/>New York "
            "City's Local Law 144, in force since 2023, requires bias audits of automated hiring tools. <bookmark "
            "mark='d'/>And American fair-lending law applies disparate impact to credit models."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def unaware(self):
        u = load("unaware")
        sel, base, zr = u["selected"], u["base"], u["rate_by_zone"]
        assert sel["B"] - sel["A"] > base["B"] - base["A"]
        assert round(sel["A"] * 100) == 20 and round(sel["B"] * 100) == 80
        head = label(r"Fairness through unawareness, \ tested", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        y0, sc = -2.4, 4.6
        bars = VGroup()
        for i, (gname, col) in enumerate((("A", GA), ("B", GB))):
            x0 = -5.0 + i * 3.4
            for j, (val, c0, nm) in enumerate(((base[gname], GREY_B, r"reoffend"), (sel[gname], col, r"labelled high"))):
                x = x0 + j * 1.25
                r = Rectangle(width=0.9, height=max(val * sc, 0.02), fill_color=c0, fill_opacity=0.8,
                              stroke_width=0).move_to([x, y0 + val * sc / 2, 0])
                v = label(f"{val * 100:.0f}\\%", font_size=20, color=c0).next_to(r, UP, buff=0.08)
                t = label(nm, font_size=15, color=GREY_A).move_to([x, y0 - 0.3, 0])
                bars.add(VGroup(r, v, t))
            bars.add(label(rf"group {gname}", font_size=22, color=col).move_to([x0 + 0.62, y0 - 0.75, 0]))
        axis = Line([-5.7, y0, 0], [-0.1, y0, 0], color=GREY_C, stroke_width=1.5)
        side = stack([(r"the model never sees the group", WHITE),
                      (r"it sees a neighbourhood that matches the group 4 times in 5", PRIV),
                      (rf"reoffence by neighbourhood: \ {zr['0'] * 100:.0f}\% and {zr['1'] * 100:.0f}\%", GREY_A),
                      (r"rule: \ label the riskier neighbourhood high risk", EXPL),
                      (r"the gap in labels is wider than the gap in behaviour", BAD)],
                     font_size=20, buff=0.3, aligned_edge=LEFT)
        for s0 in side:
            if s0.width > 5.6:
                s0.width = 5.6
        side.move_to([3.3, 0.0, 0])
        with self.voiceover(
            "A common first answer is to leave the group out of the model: fairness through unawareness. The "
            "Reasoner tests it. <bookmark mark='a'/>Its model never sees the group. It sees only a neighbourhood, "
            "and the neighbourhood matches the group four times in five, as residential segregation often does. "
            "<bookmark mark='b'/>In one neighbourhood, thirty-four percent go on to reoffend; in the other, "
            "forty-six. <bookmark mark='c'/>The model labels the riskier neighbourhood high risk. It labels twenty "
            "percent of group A and eighty percent of group B, though the groups' actual rates are twenty-nine and "
            "fifty percent. <bookmark mark='d'/>Removing the variable did not remove the group; with only a coarse "
            "proxy to go on, the model leaned on it harder, and widened the gap. To check a model for discrimination, "
            "you must collect exactly the variable that unawareness throws away."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), *[FadeIn(bars[k]) for k in (0, 3)], FadeIn(bars[2]), FadeIn(bars[5]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1:]),
                      GrowFromEdge(bars[4][0], DOWN), FadeIn(bars[4][1:]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]), Indicate(bars[4], color=BAD, scale_factor=1.05))
        self.clear_scene()

    def insurance(self):
        head = label(r"Prediction and solidarity: \ insurance", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"actuarial fairness", r"each pays a premium matching their own expected cost: \ the calibrated score, \ priced", EXPL),
                (r"Test-Achats \ (2011)", r"the EU Court of Justice banned sex as a factor in insurance premiums, \ from December 2012", BAD),
                (r"GINA \ (2008)", r"US law bars the use of genetic information in health insurance and in employment", RESP),
                (r"solidarity", r"insurance pools risk on purpose: \ some differences in risk are not ours to pay for \ (Part 38)", FAIRC)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Insurance shows the same conflict with money attached. <bookmark mark='a'/>Actuarial fairness says each "
            "person should pay a premium matching their own expected cost. That is calibration, priced: a young man "
            "pays more for car insurance because young men crash more. <bookmark mark='b'/>In 2011, in the "
            "Test-Achats case, the European Court of Justice ruled that sex may not be used to set insurance "
            "premiums, from December 2012, even where it predicts. <bookmark mark='c'/>In the United States, the "
            "Genetic Information Nondiscrimination Act of 2008 bars genetic information from health insurance and "
            "employment decisions, though not from life insurance. <bookmark mark='d'/>Behind these laws is a "
            "different idea of what insurance is for. Insurance pools risk on purpose, so that people do not bear "
            "alone the costs of risks they did not choose. That is the luck egalitarian's thought from Part 38: a "
            "predictive variable that tracks brute luck may be one that fairness forbids us to price."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
