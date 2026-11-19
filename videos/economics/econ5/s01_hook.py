from __future__ import annotations

from videos.economics.econ5.common import *  # noqa: F403


def receipt_glyph(scale: float = 1.0, color=BUDGET) -> VGroup:
    """A till receipt with a zigzag foot: the part's emblem."""
    w, h = 1.3 * scale, 1.8 * scale
    teeth = 7
    pts = [np.array([-w / 2, h / 2, 0]), np.array([w / 2, h / 2, 0]), np.array([w / 2, -h / 2, 0])]
    for k in range(teeth * 2 + 1):
        x = w / 2 - w * k / (teeth * 2)
        y = -h / 2 + (0.12 * scale if k % 2 else 0)
        pts.append(np.array([x, y, 0]))
    paper = Polygon(*pts, stroke_color=color, stroke_width=4, fill_color=color, fill_opacity=0.08)
    lines = VGroup(*[Line(np.array([-w / 2 + 0.18 * scale, h / 2 - (0.32 + 0.24 * k) * scale, 0]),
                          np.array([w / 2 - (0.18 + (0.35 if k % 2 else 0.1)) * scale,
                                    h / 2 - (0.32 + 0.24 * k) * scale, 0]),
                          stroke_color=color, stroke_width=3) for k in range(5)])
    g = VGroup(paper, lines)
    g.paper, g.lines = paper, lines
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.receipt()
        self.history()
        self.samuelson()
        self.question()
        self.title()
        self.objectives()

    def receipt(self):
        rows = [(r"week 1", r"fish \ 3 @ \$4", r"coconuts \ 8 @ \$3"),
                (r"week 2", r"fish \ 6 @ \$2", r"coconuts \ 6 @ \$4"),
                (r"week 3", r"fish \ 4 @ \$6", r"coconuts \ 6 @ \$2")]
        paper = RoundedRectangle(width=5.4, height=3.4, corner_radius=0.08, stroke_color=GREY_B, stroke_width=2,
                                 fill_color="#F7F3E3", fill_opacity=0.06).move_to(LEFT * 3.2 + DOWN * 0.1)
        head = label(r"Bo's receipts from the Island market", font_size=24, color=WHO["bo"]).next_to(
            paper.get_top(), DOWN, buff=0.3)
        lines = VGroup()
        for wk, f, c in rows:
            lines.add(VGroup(label(wk, font_size=22, color=GREY_B), label(f, font_size=22, color=FISHC),
                             label(c, font_size=22, color=COCO)).arrange(RIGHT, buff=0.35))
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.4)
        total = label(r"each week: \ \$36", font_size=22, color=GREY_A).next_to(lines, DOWN, buff=0.4)
        asks = VGroup(
            label(r"does Bo like fish?", font_size=28, color=FISHC),
            label(r"does he like it more than coconuts?", font_size=28),
            label(r"is he even consistent?", font_size=28, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.7).shift(UP * 0.4)
        tag = island_tag(r"simulated: the Island", corner=DR, font_size=15)
        with self.voiceover(
            "Here are three weeks of a man's shopping. Bo buys fish and coconuts at the Island market, and spends "
            "the same thirty-six dollars every week. <bookmark mark='a'/> Prices change from week to week, and so do "
            "his purchases. <bookmark mark='b'/> What can you tell about what Bo wants? Does he like fish? More than "
            "coconuts? <bookmark mark='c'/> And a stranger question: is he consistent? Could any single set of "
            "tastes have produced these three choices? By the end of this part you'll be able to answer that from "
            "a receipt, and you'll know exactly what the answer means."
        ) as vo:
            self.play(FadeIn(paper), FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in lines], lag_ratio=0.4), FadeIn(total))
            vo.wait_until("b")
            self.play(FadeIn(asks[0]))
            self.play(FadeIn(asks[1]))
            vo.wait_until("c")
            self.play(FadeIn(asks[2]))
        self.clear_scene()

    def history(self):
        cards = VGroup(
            history_card(r"1871", r"Jevons, \emph{The Theory of Political Economy}",
                         r"value comes from utility, and what matters is the last unit's: marginal utility",
                         color=GREY_B, width=4.1, font_size=20),
            history_card(r"1881--1906", r"Edgeworth draws indifference curves; Pareto keeps only the ranking",
                         r"utility as a number you can measure gives way to an order: better, worse, the same",
                         color=IC, width=4.1, font_size=20),
            history_card(r"1934", r"Hicks and Allen, ``A Reconsideration of the Theory of Value''",
                         r"demand theory rebuilt on the marginal rate of substitution alone, with no measurable "
                         r"utility", color=BUDGET, width=4.1, font_size=20),
        ).arrange(RIGHT, buff=0.25, aligned_edge=UP).move_to(UP * 0.5)
        foot = label(r"each step needed less from the inside of people's heads", font_size=27,
                     color=E.ACCENT).to_edge(DOWN, buff=0.7)
        head = label(r"How economists explained what people buy", font_size=34).to_edge(UP, buff=0.6)
        with self.voiceover(
            "For most of its history, economics answered with a theory of the inside of people's heads. "
            "<bookmark mark='a'/> In 1871 Stanley Jevons explained value by utility, and by the utility of the last "
            "unit bought: marginal utility. <bookmark mark='b'/> Francis Edgeworth drew the first indifference "
            "curves in 1881, and by 1906 Vilfredo Pareto had seen that only the ranking mattered: better, worse, or "
            "the same, with no need to measure how much. <bookmark mark='c'/> In 1934 John Hicks and Roy Allen "
            "rebuilt the theory of demand on that ranking alone. <bookmark mark='d'/> Each step asked less about "
            "what goes on inside people."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c_ in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def samuelson(self):
        t = tables.SAMUELSON_1938.data
        who = history_card(r"1938", r"Paul Samuelson, 22, \ ``A Note on the Pure Theory of Consumer's Behaviour''",
                           r"\emph{Economica}: start from what can be observed, the choices people make at given "
                           r"prices and incomes", color=E.ACCENT, width=8.6, font_size=24)
        who.to_edge(UP, buff=0.5)
        q = quote_card(t["vestiges"], r"Samuelson (1938)", width=9.0, font_size=32, color=E.ACCENT)
        q.next_to(who, DOWN, buff=0.45)
        chain = flow_chain([(r"choices at prices and incomes", E.ACCENT), (r"consistency axioms", GREY_A),
                            (r"tastes, recovered", PASS)], box_w=3.4, box_h=0.8, buff=0.8, font_size=23)
        chain.next_to(q, DOWN, buff=0.5)
        tag = published_tag(r"Samuelson, Economica NS 5(17) (1938); Moscati (2019) on what he meant", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Then, in 1938, a twenty-two-year-old graduate of the University of Chicago, then at Harvard, went "
            "further. <bookmark mark='a'/> Paul Samuelson proposed to build the theory of the consumer from what "
            "can actually be observed: the choices people make, at the prices and incomes they face. "
            "<bookmark mark='b'/> He wrote of dropping off the last vestiges of the utility analysis. "
            "<bookmark mark='c'/> If choices obey a few rules of consistency, perhaps tastes can be read off them, "
            "and nothing inside anyone's head needs to be assumed. Historians now argue about how far he really "
            "meant to go. But the programme he started would, thirty years later, produce a test that runs on a "
            "grocery receipt."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(who, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(Indicate(who, color=E.ACCENT, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(chain.boxes[0]))
            self.play(GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]))
            self.play(GrowArrow(chain.arrows[1]), FadeIn(chain.boxes[2]))
        self.clear_scene()

    def question(self):
        q = label(ASK, font_size=42, color=E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what does ``rational'' assume, \ and what does it not?", font_size=30, color=WHITE),
            label(r"can a list of purchases be inconsistent, \ and how inconsistent?", font_size=30, color=VIOL),
            label(r"how much of someone's tastes can you recover from it?", font_size=30, color=PASS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.8)
        with self.voiceover(
            "So this part asks: can you tell what someone wants from what they buy? <bookmark mark='a'/> What does "
            "it mean to call a choice rational, and what does that not assume? <bookmark mark='b'/> Can a list of "
            "purchases be inconsistent, and if so, by how much? <bookmark mark='c'/> And how much of a person's "
            "tastes can you recover from the list?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        logo = receipt_glyph(0.9)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 5 \ $\cdot$ \ What People Want", font_size=34, color=E.ACCENT)
        g = VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part five: what people want."):
            self.play(Create(logo.paper), LaggedStart(*[Create(x) for x in logo.lines], lag_ratio=0.2),
                      run_time=1.4)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act II \ $\cdot$ \ Choosing", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"choose a bundle on eleven budgets yourself, \ and keep your choices for later",
            r"preferences, \ utility as a label, \ and the shapes of wanting",
            r"the budget, \ the tangency, \ corners, \ kinks, \ and the tax credit people bunch at",
            r"revealed preference: \ Samuelson, \ Houthakker, \ Afriat, \ and your own consistency score",
            r"what rationality does not assume, \ how consistent people are, \ and machines that choose",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part opens Act Two, on choosing. <bookmark mark='a'/> You'll choose a bundle on eleven budgets "
            "yourself, and keep your answers. <bookmark mark='b'/> We'll build preferences, utility and the shapes "
            "they take. <bookmark mark='c'/> We'll find the best bundle on a budget, including the corners and "
            "kinks real budgets have, and the tax credit thousands of Americans bunch at. <bookmark mark='d'/> Then "
            "revealed preference, from Samuelson to Afriat, and your own consistency score. "
            "<bookmark mark='e'/> And finally what rationality does and doesn't assume, how consistent children, "
            "students, Dutch households and even a language model are, and what the frontier is doing with it."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
