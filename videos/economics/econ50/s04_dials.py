from __future__ import annotations

from videos.economics.econ7.s15_dials import dial_rows, status_head
from videos.economics.econ50.common import *  # noqa: F403


class Dials(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Who responds, \ and how much", r"Which numbers decide the answer?",
             "Chapter three. Who responds, and how much: the dials the memo runs on.",
             lit={2002: r"Gruber and Saez", 2011: r"Chetty et al.", 2020: r"Hendren and Sprung-Keyser"},
             scale=("household", "nation"), horizon=("a year", "a decade"))
        self.which()
        self.labour()
        self.eti()
        self.mvpf()

    def which(self):
        rows = VGroup(
            label(r"how many parents stop working \ $\to$ \ the elasticity of participation", font_size=24,
                  color=WORK),
            label(r"what paying for it costs \ $\to$ \ the elasticity of taxable income", font_size=24, color=BUDGET),
            label(r"what a dollar buys \ $\to$ \ the marginal value of public funds", font_size=24, color=NEW),
            label(r"how many eligible families claim it \ $\to$ \ take-up \ (chapter five)", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        head = label(r"the numbers the answer depends on", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.7)
        with self.voiceover(
            "Which numbers decide the answer? Not all of economics: a memo should name the handful that matter "
            "and give each its range. <bookmark mark='a'/> How many parents stop working when the reward falls: "
            "the elasticity of participation. <bookmark mark='b'/> What raising the money costs, if it comes from "
            "a tax on top incomes: the elasticity of taxable income. <bookmark mark='c'/> And the yardstick for "
            "what a dollar of spending buys: the marginal value of public funds. <bookmark mark='d'/> A fourth, "
            "how many eligible families actually claim the payment, has no dial of its own yet; chapter five "
            "takes it up."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()

    def _show(self, dial, title, lo, hi, ticks, unit, say, marks, fmt="{:.2f}"):
        head = status_head(dial, title)
        frame, rows = dial_rows(dial, lo, hi, ticks, unit, top=2.1, step=0.56, fmt=fmt)
        meaning = wrapped_label(tex_safe(dial.meaning), 11.2, 15, GREY_A).to_edge(DOWN, buff=0.4)
        tag = published_tag(r"explainer.economics.dials, \ checked 2026-11-20", corner=DR, font_size=12)
        with self.voiceover(say) as vo:
            self.play(FadeIn(head), FadeIn(frame), FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip(marks, rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("z")
            self.play(FadeIn(meaning), Indicate(head[1], color=WHITE))
        self.clear_scene()

    def labour(self):
        self._show(dials.DIALS["labour_supply"], r"the elasticity of labour supply", 0.0, 1.4,
                   [0, 0.25, 0.5, 0.75, 1.0, 1.25], r"percent change in hours or in working, \ per percent of pay",
                   "The first dial, from Part thirty-eight. Raj Chetty and his co-authors pulled together the "
                   "quasi-experimental estimates: for hours, when a change in pay is permanent, about 0.3. <bookmark "
                   "mark='a'/> For whether to work at all, the margin that matters here, about 0.25. <bookmark "
                   "mark='b'/> For a temporary change in pay, larger for hours, about a half, <bookmark mark='c'/> "
                   "and the same quarter for participation. <bookmark mark='d'/> And where hours are free to move, "
                   "as for Uber's drivers, more than one. <bookmark mark='z'/> The memo takes 0.25 as its central "
                   "value for parents' participation, and runs everything from zero to a half. A quarter means "
                   "that a ten percent smaller reward for working moves two and a half percent of those at the "
                   "margin out of work.", "abcd")

    def eti(self):
        E_ = load("economy")
        self._show(dials.DIALS["eti"], r"the elasticity of taxable income", 0.0, 1.2,
                   [0, 0.25, 0.5, 0.75, 1.0], r"percent change in reported income, \ per percent of $1 - t$",
                   "The second, from Part forty-one: how much reported income falls when the top tax rate rises. "
                   "Martin Feldstein, from the 1986 reform, at least one. <bookmark mark='a'/> Jonathan Gruber and "
                   "Emmanuel Saez, across several reforms, about 0.4. <bookmark mark='b'/> Peter Diamond and Saez's "
                   "mid-range value, a quarter. <bookmark mark='z'/> Why it matters for a child allowance: if the "
                   "money comes from a surtax on the highest incomes, at a combined top rate of forty percent, each "
                   "dollar of revenue costs top earners about "
                   f"{E_['mcpf'][0]:.2f}, {E_['mcpf'][1]:.2f} or {E_['mcpf'][2]:.2f} dollars, for elasticities of "
                   "0.1, a quarter and 0.4, because reported incomes shrink.", "ab")

    def mvpf(self):
        self._show(dials.DIALS["mvpf"], r"the marginal value of public funds", 0.0, 2.5,
                   [0, 0.5, 1.0, 1.5, 2.0, 2.5], r"dollars of benefit per dollar of net cost",
                   "The third, from Part forty-two: the marginal value of public funds, what recipients would pay "
                   "for a policy divided by what it costs the government in the end. Nathaniel Hendren and Ben "
                   "Sprung-Keyser's survey of 133 American policies: for those aimed at adults, mostly between a "
                   "half and two. <bookmark mark='a'/> The Island's unemployment insurance at its best, one. "
                   "<bookmark mark='b'/> The Island's earned income tax credit, a little above one. <bookmark "
                   "mark='z'/> Their striking finding was about children: policies that invest in children's "
                   "health and education often return so much in later taxes that they cost the government "
                   "nothing in the end. Whether a cash allowance does the same is one of the memo's open questions.",
                   "ab")
