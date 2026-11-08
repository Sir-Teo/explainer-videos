from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Utility(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"The greatest happiness", r"Is the right act the one that does the most good?",
                            lit=(1789, 1863, 1874), part=PART)
        with self.voiceover("Chapter one. The greatest happiness."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.bentham()
        self.ledger()
        self.mill()
        self.sidgwick()
        self.levels()

    def bentham(self):
        q = quote_card(r"Nature has placed mankind under the governance of two sovereign masters, \ pain and "
                       r"pleasure. \ It is for them alone to point out what we ought to do.", r"Jeremy Bentham",
                       r"\textit{An Introduction to the Principles of Morals and Legislation} \ (1789)", width=9.6,
                       font_size=27).move_to([0, 1.5, 0])
        rows = stack([(r"intensity, \ duration, \ certainty, \ propinquity", GOOD),
                      (r"fecundity: \ pleasures that lead to more; \ purity: \ pleasures not followed by pain", GOOD),
                      (r"extent: \ the number of people affected", AGG),
                      (r"each to count for one, \ and none for more than one", GOAL)], font_size=21,
                     buff=0.25).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "In 1789 Jeremy Bentham opened his Principles of Morals and Legislation with a famous sentence. "
            "<bookmark mark='a'/>Nature has placed mankind under the governance of two sovereign masters, pain and "
            "pleasure; it is for them alone to point out what we ought to do. <bookmark mark='b'/>He listed the "
            "dimensions by which to measure a pleasure or a pain: its intensity, duration, certainty and nearness; "
            "<bookmark mark='c'/>its fecundity, the further pleasures it brings, and its purity, freedom from "
            "following pains; <bookmark mark='d'/>and its extent, how many people it reaches. <bookmark mark='e'/>Each "
            "person counts for one, and no one for more than one: the egalitarian core of utilitarianism."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            for mk, r in zip("bcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def ledger(self):
        d = load("felicific")
        head = label(r"A felicific ledger, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        acts = d["acts"]
        names = list(acts)
        assert [acts[a]["total"] for a in names] == [26.47, -21.91] and d["best"] == names[0]
        hd = [r"\text{who}", r"\text{intensity}", r"\text{hours}", r"\text{certainty}", r"\text{days away}",
              r"\text{value}"]
        grids = VGroup()
        for k, a in enumerate(names):
            cells = [[label(r["who"], font_size=16, color=GREY_A), label(f"{r['intensity']:+d}", font_size=17,
                                                                        color=GOOD if r["intensity"] > 0 else HARM),
                      label(str(r["hours"]), font_size=17), label(f"{r['certainty']:g}", font_size=17),
                      label(str(r["delay"]), font_size=17), label(f"{r['value']:+.2f}", font_size=17, color=WHITE)]
                     for r in acts[a]["rows"]]
            g = ValueGrid(hd, cells, col_w=[3.0, 1.5, 1.2, 1.5, 1.6, 1.5], cell_h=0.42, font_size=15)
            t = label(a, font_size=19, color=GOAL if k == 0 else HARM)
            tot = label(f"total: \\ {acts[a]['total']:+.2f}", font_size=19, color=GOAL if k == 0 else HARM)
            grids.add(VGroup(t, g, tot).arrange(DOWN, buff=0.15, aligned_edge=LEFT))
        grids.arrange(DOWN, buff=0.35).move_to([0, -0.4, 0])
        note = label(r"value = intensity $\times$ hours $\times$ certainty $\times\ 0.99^{\text{days}}$", font_size=17,
                     color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The Reasoner keeps Bentham's ledger for a small decision. <bookmark mark='a'/>You promised to help a "
            "friend move house, but a concert has come up. Keeping the promise costs you four mildly unpleasant "
            "hours, gives your friend four better ones, and, more remotely and less certainly, strengthens the "
            "friendship. <bookmark mark='b'/>Going to the concert gives you three good hours, costs your friend four "
            "bad ones, and probably damages the friendship. <bookmark mark='c'/>Multiply intensity by duration and "
            "certainty, discount for distance in time, and add: plus twenty six against minus twenty two. "
            "<bookmark mark='d'/>Keep the promise. The calculation is crude, and the numbers are invented; Bentham's "
            "claim is that the structure of moral reasoning is exactly this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(grids[0]))
            vo.wait_until("b")
            self.play(FadeIn(grids[1]))
            vo.wait_until("c")
            self.play(Indicate(grids[0][2], color=WHITE), Indicate(grids[1][2], color=WHITE))
            vo.wait_until("d")
            self.wait(0.5)
        self.clear_scene()

    def mill(self):
        hc = history_card(1863, r"John Stuart Mill", r"\textit{Utilitarianism}", width=4.6, color=HIST).to_corner(
            UL, buff=0.3)
        q = quote_card(r"It is better to be a human being dissatisfied than a pig satisfied; \ better to be Socrates "
                       r"dissatisfied than a fool satisfied.", r"Mill", r"\textit{Utilitarianism}, \ chapter 2",
                       width=9.0, font_size=27).move_to([0, 0.6, 0])
        rows = stack([(r"higher and lower pleasures differ in quality, \ not only in amount", GOOD),
                      (r"the test: \ the preference of those who have known both", GREY_A),
                      (r"critics: \ either quality reduces to quantity, \ or something besides pleasure matters",
                       HARM)], font_size=20, buff=0.25).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Bentham said that, quantity of pleasure being equal, pushpin is as good as poetry. John Stuart Mill, in "
            "Utilitarianism of 1863, disagreed. <bookmark mark='a'/>It is better to be a human being dissatisfied "
            "than a pig satisfied; better to be Socrates dissatisfied than a fool satisfied. "
            "<bookmark mark='b'/>Pleasures differ in quality as well as quantity, <bookmark mark='c'/>and the judges "
            "of quality are those who have known both kinds. <bookmark mark='d'/>His critics replied that either "
            "quality comes down to quantity after all, or Mill has admitted that something besides pleasure "
            "matters, which is the next chapter's question."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(q))
            for mk, r in zip("bcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def sidgwick(self):
        hc = history_card(1874, r"Henry Sidgwick", r"\textit{The Methods of Ethics}", width=5.0,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [(r"three methods", r"egoism, \ intuitionism, \ and utilitarianism: \ the three ways of deciding what "
                                   r"one ought to do", GREY_A),
                (r"the point of view of the universe", r"the good of any one individual is of no more importance "
                                                       r"than the equal good of any other", AGG),
                (r"the dualism of practical reason", r"egoism and utilitarianism are both rational, \ and can "
                                                     r"conflict: \ Sidgwick could find no way to reconcile them", HARM),
                (r"esoteric morality", r"perhaps a utilitarian society should not teach utilitarianism: \ rules may "
                                       r"do more good than calculation \ (rule utilitarianism, \ Harsanyi, \ Hooker)",
                 DUTY)]
        g = rows_table(rows, top=1.3, gap=0.45, width=7.6, x_text=-1.4)
        with self.voiceover(
            "Henry Sidgwick's Methods of Ethics, of 1874, is the most careful statement of the theory. "
            "<bookmark mark='a'/>He compared three methods of deciding what one ought to do: egoism, the "
            "intuitionism of common sense, and utilitarianism. <bookmark mark='b'/>From the point of view of the "
            "universe, he wrote, the good of any one individual is of no more importance than the equal good of any "
            "other. <bookmark mark='c'/>But he could not show that egoism is irrational: both seemed to be rational, "
            "and they conflict, the dualism of practical reason. <bookmark mark='d'/>And he saw that a utilitarian "
            "society might do best not to teach utilitarianism, if fixed rules produce more good than calculation. "
            "Rule utilitarianism, later defended by Harsanyi and by Brad Hooker, grew from that thought."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def levels(self):
        d = load("levels")
        head = label(r"Rules or calculation? \ Two levels", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ns = d["noises"]
        c0, c5 = d["curves"]["0.0"], d["curves"]["0.5"]
        assert (d["mu"], d["sd"], d["threshold"], d["ideal"]) == (-1.0, 1.0, 2.0, 0.083)
        assert (c0["act_below_rule_at"], c5["act_below_rule_at"]) == (0.9, 0.5)
        two = dict(zip(ns, c5["two_level"]))
        assert two[1.5] > 0 > two[1.6]
        # the axes run from -0.25 to 0.1; drawn shifted up by 0.25 so that the horizontal axis sits at the bottom
        ax = Axes(x_range=[0, 2, 0.5], y_range=[0, 0.35, 0.05], x_length=6.0, y_length=3.9, tips=False,
                  axis_config={"color": GREY_B, "font_size": 15}).move_to([-3.3, -0.6, 0])

        def pt(x, y):
            return ax.c2p(x, y + 0.25)

        xn = VGroup(*[label(f"{v:g}", font_size=15, color=GREY_B).next_to(pt(v, -0.25), DOWN, buff=0.12)
                      for v in (0, 0.5, 1, 1.5, 2)])
        yn = VGroup(*[label(f"{v:g}", font_size=15, color=GREY_B).next_to(pt(0, v), LEFT, buff=0.12)
                      for v in (-0.2, -0.1, 0, 0.1)])
        xl = label(r"noise in the agent's estimates", font_size=16, color=GREY_A).next_to(xn, DOWN, buff=0.15)
        yl = label(r"value per promise case, \ against always keeping", font_size=16, color=GREY_A).next_to(
            ax, UP, buff=0.12).align_to(ax, LEFT)

        def curve(ys, col, dashed=False):
            m = VMobject(color=col, stroke_width=3).set_points_as_corners([pt(x, y) for x, y in zip(ns, ys)])
            return DashedVMobject(m, num_dashes=40) if dashed else m

        rule = DashedLine(pt(0, 0), pt(2, 0), color=DUTY, stroke_width=2.5)
        rl = label(r"rule: \ always keep", font_size=15, color=DUTY).next_to(pt(2, 0), UP, buff=0.1).shift(
            LEFT * 0.7)
        act0, act5, two5 = curve(c0["act"], GOOD), curve(c5["act"], HARM), curve(c5["two_level"], VIRT)
        ideal = Dot(pt(0, d["ideal"]), radius=0.07, color=WHITE)
        l0 = label(r"act, \ unbiased", font_size=15, color=GOOD).next_to(pt(1.25, c0["act"][12]), LEFT,
                                                                           buff=0.15)
        l5 = label(r"act, \ self-serving bias 0.5", font_size=15, color=HARM).next_to(pt(1.05, -0.215), LEFT,
                                                                                       buff=0.0)
        lt = label(r"two-level, \ same bias", font_size=15, color=VIRT).next_to(pt(1.0, c5["two_level"][10]),
                                                                                UP, buff=0.12)
        x0 = Dot(pt(0.9, 0), radius=0.06, color=GOOD)
        x5 = Dot(pt(0.5, 0), radius=0.06, color=HARM)
        side = stack([(r"200,000 promise cases: \ breaking is worth $D \sim N(-1, 1)$", GREY_A),
                      (r"the act utilitarian breaks when its estimate of $D$ is positive: \ perfectly informed, \ "
                       r"it gains 0.083 a case \ (the white dot)", GOOD),
                      (r"unbiased, \ it falls below the rule at noise 0.9", GOOD),
                      (r"with a self-serving bias of 0.5, \ at noise 0.5", HARM),
                      (r"Hare \ (1981): \ keep the rule unless the case for breaking exceeds 2: \ above the rule up "
                       r"to noise 1.5", VIRT),
                      (r"Hooker \ (2000): \ the code whose internalization by nearly all would be best", DUTY),
                      (r"Smart: \ why keep a rule you know is worse here? \ ``rule worship''", HARM)],
                     font_size=17, aligned_edge=LEFT, width=5.0, buff=0.24).move_to([3.9, -0.35, 0])
        with self.voiceover(
            "Sidgwick's worry can be made precise. <bookmark mark='a'/>The Reasoner generates two hundred thousand "
            "cases in which an agent has made a promise. Breaking it has a true net value, usually negative: on "
            "average minus one, with spread one. <bookmark mark='b'/>A perfectly informed act utilitarian breaks "
            "exactly when breaking is better, and gains point zero eight three per case over someone who always keeps "
            "her word. But real agents estimate, with noise. <bookmark mark='c'/>As the noise grows, the act "
            "utilitarian's mistakes mount, and once the noise reaches point nine it does worse than the plain rule. "
            "<bookmark mark='d'/>Add a self-serving bias of half a unit, the familiar discovery that breaking this "
            "particular promise would be for the best, and it falls below the rule at a noise of only point five. "
            "<bookmark mark='e'/>R. M. Hare's Moral Thinking, of 1981, proposed two levels. In everyday life, follow "
            "well-chosen intuitive rules; think critically, like an archangel, only in calm reflection or when the "
            "case for an exception is overwhelming. The two-level thinker here breaks a promise only when its "
            "estimated gain exceeds two, and stays above the rule until the noise passes one and a half. "
            "<bookmark mark='f'/>Brad Hooker's rule consequentialism, of 2000, goes further: an act is right if it "
            "is allowed by the code whose internalization by nearly everyone would have the best consequences. "
            "<bookmark mark='g'/>The old objection, pressed by J. J. C. Smart, who called it rule worship: if the rule "
            "exists for the sake of the good, why keep it when you know that breaking it is better?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(side[0]), Create(ax), FadeIn(xn), FadeIn(yn), FadeIn(xl), FadeIn(yl))
            self.play(Create(rule), FadeIn(rl))
            vo.wait_until("b")
            self.play(FadeIn(ideal), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(act0), run_time=1.5)
            self.play(FadeIn(l0), FadeIn(x0), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(act5), run_time=1.5)
            self.play(FadeIn(l5), FadeIn(x5), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(Create(two5), run_time=1.5)
            self.play(FadeIn(lt), FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(side[5]))
            vo.wait_until("g")
            self.play(FadeIn(side[6]))
        self.clear_scene()
