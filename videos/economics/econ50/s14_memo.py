from __future__ import annotations

from videos.economics.econ50.common import *  # noqa: F403

PAPER = "#161B24"


def page(n, title, lines, color, width=12.4, font_size=21):
    head = VGroup(label(rf"{n}", font_size=30, color=color), label(title, font_size=27, color=color)).arrange(
        RIGHT, buff=0.3)
    body = VGroup(*[wrapped_label(t, width - 1.2, font_size, WHITE) for t in lines]).arrange(
        DOWN, aligned_edge=LEFT, buff=0.26)
    inner = VGroup(head, body).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
    box = RoundedRectangle(width=width, height=inner.height + 0.8, corner_radius=0.12, stroke_color=color,
                           stroke_width=1.6, fill_color=PAPER, fill_opacity=1.0)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.5)
    g = VGroup(box, inner)
    g.head, g.body = head, body
    return g


def _pct(x):
    return f"{100 * x:.0f}\\%"


class Memo(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The memo", r"Four pages, \ two minutes, \ one decision",
             "Chapter twelve. The memo.", lit={2021: r"the payments"}, scale=("nation",),
             horizon=("a year", "a generation"))
        self.letterhead()
        self.pages()
        self.oral()
        self.revisited()

    def letterhead(self):
        rows = VGroup(
            label(r"To: \ the Minister of Finance", font_size=24, color=GREY_A),
            label(r"From: \ the Island's economist", font_size=24, color=GREY_A),
            label(r"Re: \ a monthly child allowance", font_size=26, color=WHITE),
            label(r"Page 1, \ the decision; \ 2, \ what it does; \ 3, \ what it costs and is worth; \ 4, \ what we "
                  r"do not know", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        box = SurroundingRectangle(rows, buff=0.5, corner_radius=0.12, color=GREY_B, stroke_width=1.4)
        with self.voiceover(
            "Now the memo itself, four pages, as the minister asked. <bookmark mark='a'/> A memo is not a paper. "
            "It begins with the decision, not the method; every number carries its range; and it separates what "
            "the analysis shows from what the minister must judge. <bookmark mark='b'/> Page one, the decision. "
            "Page two, what the policy does. Page three, what it costs and what it is worth. Page four, what we do "
            "not know."
        ) as vo:
            self.play(Create(box), FadeIn(rows[:3]))
            vo.wait_until("a")
            self.play(Indicate(rows[2], color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def pages(self):
        I, Fn, O, B, D, T = (load(x) for x in ("island", "fan", "options", "budget", "deciles", "tornado"))
        old = 100 * O["old"]["poverty"]
        fall_hi = 1 - Fn["new"][0] / Fn["old"]
        fall_lo = 1 - Fn["new"][-1] / Fn["old"]
        h = O["hybrid"][0]
        p1 = page(1, r"The decision", [
            rf"\textbf{{Bottom line.}} \ The allowance would cut child poverty on the Island by about a fifth "
            rf"({_pct(fall_lo)} to {_pct(fall_hi)} across the plausible range), \ at about \${I['per_child']:,.0f} "
            r"a child a year.".replace(",", "{,}"),
            r"\textbf{Two designs.} \ The full allowance does most for the poorest if parents keep working, \ as "
            r"the evidence so far suggests; \ at the central elasticity it slightly raises deep poverty. \ Keeping "
            r"the old credit's work requirement and paying only the extra unconditionally costs a quarter less, \ "
            rf"leaves {100 * h['poverty']:.1f}\% instead of {100 * I['new']['child_poverty']:.1f}\% of children "
            rf"poor, \ lowers deep poverty to {100 * h['deep']:.1f}\%, \ and is safe if parents respond more.",
            r"\textbf{Recommendation.} \ If cutting child poverty is the priority, \ pay the full allowance, \ "
            r"automatically and monthly, \ with a staggered start that measures the work response; \ fall back to "
            r"the second design if many parents leave work.",
        ], NEW)
        p2 = page(2, r"What it does", [
            rf"Child poverty: \ {old:.1f}\% $\to$ {100 * I['new']['child_poverty']:.1f}\% \ (with no response, \ "
            rf"{100 * I['static_child_poverty']:.1f}\%; \ at the dial's top, \ {100 * Fn['new'][-1]:.1f}\%).",
            rf"Work: \ about {I['exits']:.0f} of 40,000 parents stop \ ({100 * I['exit_share']:.1f}\%); \ "
            rf"between 0 and {Fn['exits'][-1]:,.0f} across the dial.".replace("40,000", "40{,}000").replace(
                "1,391", "1{,}391"),
            rf"Deep poverty: \ {100 * Fn['deep_old']:.1f}\% $\to$ {100 * I['new']['deep']:.1f}\%; \ it rises if "
            rf"the elasticity exceeds about {Fn['deep_cross']:.2f}.",
            rf"Who gains: \ the poorest tenth, \ +\${D['mean_gain'][0]:,.0f} a year; \ the middle, \ "
            rf"\$1,400--1,800; \ the richest tenth, \ +\${D['mean_gain'][-1]:,.0f}.".replace(",", "{,}"),
        ], CHILD)
        p3 = page(3, r"What it costs, \ and what it is worth", [
            rf"Cost: \ \${I['cost'] / 1e6:.0f} million a year on the Island; \ families' responses add "
            rf"{100 * B['fe_share']:.1f}\%; \ take-up below 100\% lowers it, \ by missing the poorest.",
            rf"Value per dollar: \ {B['rows'][0]['mvpf']:.2f} with nothing repaid later; \ "
            rf"{B['rows'][3]['mvpf']:.2f} if a quarter is repaid in children's later taxes, \ "
            rf"{B['rows'][6]['mvpf']:.2f} if half.",
            rf"If paid for by a top surtax: \ {B['rows'][2]['mvpf']:.2f} to {B['rows'][1]['mvpf']:.2f} of value "
            r"per dollar taken with nothing repaid; \ the case then rests on the weight you give to poor children's "
            r"incomes, \ which is your judgment, \ not an economic finding.",
        ], BUDGET)
        p4 = page(4, r"What we do not know", [
            r"How parents respond to a permanent allowance: \ the 2021 payments were temporary, \ Canada is not "
            r"the Island, \ and the simulation's elasticities are assumed.",
            r"What the children gain over decades: \ the best evidence is a century old, \ and the newest trial "
            r"found no gains by age four.",
            r"How many of the poorest would claim it, \ and what a staggered start would cost in fairness.",
            r"Each of these moves the answer more than any number on page three.",
        ], HOLD)
        tag = island_tag(corner=DR, font_size=13)
        say = [
            ("Page one, the decision. <bookmark mark='a1'/> The bottom line: the allowance would cut child poverty "
             f"on the Island by about a fifth, between {100 * fall_lo:.0f} and {100 * fall_hi:.0f} percent across "
             f"the plausible range, at about {I['per_child']:,.0f} dollars a child a year. <bookmark mark='a2'/> "
             "There are two designs worth considering. The full allowance does most for the poorest families if "
             "parents keep working, as the evidence so far suggests, although at the central elasticity it "
             "slightly raises deep poverty. The second keeps the old credit's work requirement and pays only the "
             "extra amount unconditionally: it costs a quarter less, leaves "
             f"{100 * h['poverty']:.1f} percent of children poor rather than {100 * I['new']['child_poverty']:.1f}, "
             "lowers deep poverty, and is safe if parents respond more than expected. <bookmark mark='a3'/> The "
             "recommendation: if "
             "cutting child poverty is the priority, pay the full allowance, automatically and monthly, starting "
             "in some places before others so that the work response is measured, and fall back to the second "
             "design if many parents leave work."),
            ("Page two, what it does. <bookmark mark='b1'/> Child poverty falls from "
             f"{old:.1f} to {100 * I['new']['child_poverty']:.1f} percent; with no response it would be "
             f"{100 * I['static_child_poverty']:.1f}, and at the top of the dial {100 * Fn['new'][-1]:.1f}. "
             f"<bookmark mark='b2'/> About {I['exits']:.0f} of forty thousand parents stop working, between none "
             f"and {Fn['exits'][-1]:,.0f} across the dial. <bookmark mark='b3'/> Deep poverty rises slightly at "
             "the central value, and more if the response is stronger. <bookmark mark='b4'/> The gains are largest "
             "for the poorest tenth and smallest for the richest."),
            (f"Page three. <bookmark mark='c1'/> The cost: {I['cost'] / 1e6:.0f} million dollars a year on the "
             "Island, barely changed by families' responses, and lower if take-up is incomplete, but only by "
             "missing the families it is for. <bookmark mark='c2'/> The value per dollar: one with nothing repaid "
             "later, more if children's later taxes repay part of the cost. <bookmark mark='c3'/> If it is paid for "
             "by a surtax and nothing is repaid, it delivers sixty to seventy-five cents of value per dollar taken, "
             "and the case rests on the weight the government gives to poor children's incomes: the minister's "
             "judgment, stated as such."),
            ("Page four, what we do not know. <bookmark mark='d1'/> How parents respond to a permanent allowance. "
             "<bookmark mark='d2'/> What the children gain over decades: the best evidence is a century old, and "
             "the newest trial found no gains by age four. <bookmark mark='d3'/> How many of the poorest would "
             "claim it. <bookmark mark='d4'/> Each of these moves the answer more than any number on page three."),
        ]
        for pg, s_, marks in zip((p1, p2, p3, p4), say, (("a1", "a2", "a3"), ("b1", "b2", "b3", "b4"),
                                                          ("c1", "c2", "c3"), ("d1", "d2", "d3", "d4"))):
            pg.move_to(ORIGIN)
            if pg.height > 7.4:
                pg.scale_to_fit_height(7.4)
            with self.voiceover(s_) as vo:
                self.play(FadeIn(pg[0]), FadeIn(pg.head), FadeIn(tag))
                for mk, ln in zip(marks, pg.body):
                    vo.wait_until(mk)
                    self.play(FadeIn(ln, shift=UP * 0.08))
            self.play(FadeOut(pg), run_time=0.6)
        thumbs = VGroup(*[page(n, t, [], c, width=2.9, font_size=14) for n, t, c in
                          ((1, r"decision", NEW), (2, r"what it does", CHILD), (3, r"cost, \ value", BUDGET),
                           (4, r"unknowns", HOLD))]).arrange(RIGHT, buff=0.3)
        with self.voiceover("Four pages: the decision, what it does, what it costs and is worth, and what we do "
                            "not know."):
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.1) for t in thumbs], lag_ratio=0.3), run_time=2.0)
        self.clear_scene()

    def oral(self):
        lines = VGroup(
            label(r"It would cut child poverty by about a fifth, \ for about 1,500 dollars a child a year."
                  .replace("1,500", "1{,}500"), font_size=24, color=WHITE),
            label(r"Few parents would stop working, \ unless they respond far more than in 2021 or in Canada.",
                  font_size=24, color=WHITE),
            label(r"Whether it is worth it depends on two things: \ what the children repay later, \ and how much",
                  font_size=24, color=WHITE),
            label(r"you value a dollar to a poor child.", font_size=24, color=WHITE),
            label(r"If that is your priority, \ do it, \ automatically, \ and measure as you go.", font_size=24,
                  color=NEW),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to(DOWN * 0.2)
        head = label(r"the two-minute version, \ in the minister's corridor", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        with self.voiceover(
            "And the oral version, for the two minutes in a corridor when the minister has not read the memo. "
            "<bookmark mark='a'/> Minister: it would cut child poverty by about a fifth, for about fifteen hundred "
            "dollars a child a year. <bookmark mark='b'/> Few parents would stop working, unless they respond far "
            "more than they did in 2021 or in Canada. <bookmark mark='c'/> Whether it is worth it depends on two "
            "things: what the children repay later, which nobody yet knows, and how much you value a dollar to a "
            "poor child, which only you can decide. <bookmark mark='d'/> If that is your priority, do it, pay it "
            "automatically, and measure as you go."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lines[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(lines[1], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(lines[2], shift=UP * 0.1), FadeIn(lines[3], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(lines[4], shift=UP * 0.1))
        self.clear_scene()

    def revisited(self):
        O = load("options")
        a, h = O["allowance"], O["hybrid"]
        rows = [
            (r"yes, \ as designed", rf"poverty {100 * a[0]['poverty']:.1f}\% \ ({100 * a[1]['poverty']:.1f}\% at "
                                    rf"0.5); \ \${a[0]['per_child']:,.0f} a child".replace(",", "{,}"), NEW),
            (r"yes, \ keep a work requirement", rf"poverty {100 * h[0]['poverty']:.1f}\% \ "
                                                rf"({100 * h[1]['poverty']:.1f}\% at 0.5); \ "
                                                rf"\${h[0]['per_child']:,.0f} a child".replace(",", "{,}"), WORK),
            (r"yes, \ but smaller", r"cost and gains shrink together; \ the value per dollar barely moves", CHILD),
            (r"no", r"right if a poor child's dollar counts for little more than a taxpayer's, \ or if the money "
                    r"has a better use", LOSS),
        ]
        g = VGroup()
        for n, t, c in rows:
            g.add(VGroup(label(n, font_size=22, color=c), label(t, font_size=19, color=WHITE)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1))
        g.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 0.3)
        head = label(r"your advice from chapter four, \ revisited", font_size=28, color=E.ACCENT).to_edge(UP,
                                                                                                         buff=0.5)
        foot = label(r"the analysis does not choose for you: \ it prices each choice", font_size=22,
                     color=E.ACCENT).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Now your advice from chapter four. <bookmark mark='a'/> Yes, as designed: child poverty falls to "
            f"{100 * a[0]['poverty']:.1f} percent at the central elasticity, but only to {100 * a[1]['poverty']:.1f} "
            "if parents respond twice as strongly. <bookmark mark='b'/> Yes, with a work requirement kept for the "
            f"old credit: {100 * h[0]['poverty']:.1f} percent, almost whatever parents do, for a quarter less "
            "money; it does less for the families with no earnings at all. <bookmark mark='c'/> Yes, but smaller: "
            "the cost and the gains shrink together, and the value per dollar barely moves. <bookmark mark='d'/> "
            "And no: the right answer if a poor child's dollar counts for little more than a taxpayer's, or if the "
            "money has a use with a higher value per dollar. <bookmark mark='e'/> The analysis does not choose for "
            "you. It tells you what each choice buys."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r_ in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
