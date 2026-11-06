from __future__ import annotations

from videos.philosophy.philosophy37.common import *  # noqa: F403


class Debunk(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Evolutionary debunking", r"Could evolved values track an independent truth?",
                            lit=(2006,), part=PART)
        with self.voiceover("Chapter eight. Evolutionary debunking."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.dilemma()
        self.analogy()
        self.replies()
        self.selective()

    def dilemma(self):
        hc = history_card(2006, r"Sharon Street", r"``A Darwinian Dilemma for Realist Theories of Value''", width=6.6,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [(r"the premise", r"natural selection has shaped our evaluative tendencies: \ care for kin, \ "
                                 r"reciprocity, \ outrage at cheats", MIND),
                (r"horn one", r"if evaluative truth is independent of those pressures, \ it would be a coincidence if "
                              r"our values tracked it", BAD),
                (r"horn two", r"if the truth is tied to them, \ the realist must explain how: \ and the simplest "
                              r"explanation needs no independent truth", BAD),
                (r"the conclusion", r"realism is in trouble; \ Street's constructivism is not", EXPR)]
        g = rows_table(rows, top=1.0, gap=0.45, width=8.2, x_text=-2.0)
        with self.voiceover(
            "Sharon Street posed a dilemma for realists in 2006. <bookmark mark='a'/>Natural selection has shaped our "
            "evaluative tendencies: to care for our children and kin, to return favours, to be outraged by cheats. "
            "<bookmark mark='b'/>If the evaluative truths are independent of those pressures, it would be a "
            "remarkable coincidence if our values tracked them: selection rewarded fitness, not truth. "
            "<bookmark mark='c'/>If instead the truth is related to those pressures, the realist must say how, and "
            "the simplest account, that we value what helped our ancestors survive, needs no independent truth at "
            "all. <bookmark mark='d'/>Either way, Street argued, realism is in trouble, while her constructivism, on "
            "which values are made by valuers, is not."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def analogy(self):
        d = load("debunk")
        head = label(r"The dilemma, \ as an analogy", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert (d["n"], d["corr_fitness"], d["corr_independent"], d["corr_third_factor"]) == (200, 0.832, -0.023, 0.68)
        panels = VGroup()
        specs = [("fitness", d["fitness"], r"against fitness: \ $r = 0.83$", MIND),
                 ("t_indep", d["t_indep"], r"against an independent truth: \ $r = -0.02$", BAD),
                 ("t_third", d["t_third"], r"against a truth tied to fitness: \ $r = 0.68$", REAL)]
        for k, (key, ys, title, col) in enumerate(specs):
            ax = Axes(x_range=[-3, 3, 1], y_range=[0, 1, 0.5], x_length=3.6, y_length=2.6, tips=False,
                      axis_config={"color": GREY_B, "stroke_width": 1.5}).move_to([-4.4 + 4.4 * k, -0.2, 0])
            dots = VGroup(*[Dot(ax.c2p(max(-3, min(3, x)), a), radius=0.03, color=col)
                            for x, a in zip(ys, d["approval"])])
            t = label(title, font_size=16, color=col).next_to(ax, UP, buff=0.15)
            panels.add(VGroup(ax, dots, t))
        yl = label(r"vertical: \ evolved share approving of an act", font_size=16, color=GREY_A).to_edge(DOWN, buff=1.0)
        foot = label(r"an analogy: \ 200 kinds of act, \ approval evolving by the replicator equation; \ it models the "
                     r"argument's structure, \ not our history", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The Reasoner runs the dilemma as an analogy, which models only its structure. <bookmark mark='a'/>Two "
            "hundred kinds of act each have a fitness effect. A population's approval of each act evolves by the "
            "replicator equation of Part 19: approval of fitness-enhancing acts spreads. After four hundred "
            "generations, approval correlates with fitness at point eight three. <bookmark mark='b'/>Now suppose the "
            "moral truth about each act is independent of fitness. Then evolved approval correlates with it at minus "
            "point zero two: no better than chance. That is Street's first horn. <bookmark mark='c'/>Suppose instead "
            "the truth is tied to fitness by some third factor, for instance that survival and flourishing are good, "
            "and that what helps them is often good too. Then approval correlates with the truth at point six eight, "
            "and tracking fitness tracks value, roughly. <bookmark mark='d'/>The analogy shows exactly where the "
            "argument turns: on whether there is a reason, independent of our values, to link fitness and value."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot), FadeIn(yl))
            for mk, p in zip("abc", panels):
                vo.wait_until(mk)
                self.play(Create(p[0]), FadeIn(p[2]))
                self.play(LaggedStart(*[FadeIn(x) for x in p[1]], lag_ratio=0.004, run_time=1.5))
            vo.wait_until("d")
            self.wait(0.5)
        self.clear_scene()

    def replies(self):
        head = label(r"Third factors, \ and companions again", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"third factor", r"Enoch \ (2010); \ Wielenberg \ (2010); \ Copp \ (2008): \ survival is good, \ so "
                                  r"selection for survival roughly tracks the good", REAL),
                (r"Street's reply", r"that assumption is itself an evaluative judgment shaped by selection: \ it cannot "
                                    r"vouch for itself", ANTI),
                (r"Joyce \ (2006)", r"\textit{The Evolution of Morality}: \ the genealogy undermines justification, \ "
                                    r"even if it cannot prove falsity", ANTI),
                (r"over-generalization", r"the same argument threatens our beliefs about logic and mathematics: \ "
                                         r"companions in guilt, \ chapter four", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The replies follow the analogy's fork. <bookmark mark='a'/>David Enoch, Erik Wielenberg and David Copp "
            "offered third factors: survival and flourishing are good, so selection for them roughly tracks the "
            "good. <bookmark mark='b'/>Street answered that the link is itself an evaluative judgment shaped by "
            "selection, and cannot vouch for itself. <bookmark mark='c'/>Richard Joyce's The Evolution of Morality, of "
            "2006, argued that the genealogy undermines our justification even if it cannot show our moral beliefs "
            "false. <bookmark mark='d'/>And critics note that the same argument threatens our beliefs about logic "
            "and mathematics, which were also useful to believe: the companions in guilt of chapter four, again."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def selective(self):
        head = label(r"Debunking selectively", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the strategy", r"debunk only some intuitions: \ those best explained by evolutionary or cultural pressures unrelated to truth", MIND),
                (r"Singer \ (2005)", r"intuitions against pushing the man are by-products of our evolved aversion to personal violence: \ discount them", BAD),
                (r"de Lazari-Radek and Singer \ (2012)", r"impartial benevolence survives, \ since it is no product of selection for kin and allies", REAL),
                (r"Kahane \ (2011)", r"selective debunking needs a premise about which intuitions are reliable: \ it cannot be global and still leave anything standing", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Some philosophers use debunking selectively. <bookmark mark='a'/>Debunk only the intuitions best "
            "explained by pressures unrelated to truth. <bookmark mark='b'/>Peter Singer argued in 2005 that our "
            "reluctance to push the man from the footbridge is a by-product of an evolved aversion to up-close "
            "personal violence, and should be discounted. <bookmark mark='c'/>Katarzyna de Lazari-Radek and Singer "
            "argued in 2012 that impartial benevolence survives the test, since no selection for kin and allies would "
            "produce concern for everyone. <bookmark mark='d'/>Guy Kahane replied in 2011 that a selective debunking "
            "argument needs a premise about which intuitions are reliable, and that the more global the argument, the "
            "less it leaves standing to judge with."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
