from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403


def floor(tidy: bool, seed: int = 62):
    """A plant floor seen from above: looms in rows, with yarn piled in the aisles and red marks for defects when
    untidy; clear aisles, labelled racks and few defects when tidy."""
    rng = np.random.default_rng(seed)
    g = VGroup()
    looms = VGroup()
    for r in range(4):
        for c in range(6):
            looms.add(RoundedRectangle(width=0.7, height=0.42, corner_radius=0.06, stroke_color=GREY_B,
                                       stroke_width=1.4, fill_color=GREY_E, fill_opacity=0.8).move_to(
                [c * 1.0 - 2.5, r * 0.85 - 1.3, 0]))
    g.add(looms)
    clutter = VGroup()
    n = 6 if tidy else 46
    for _ in range(n):
        x, y = rng.uniform(-3.0, 3.0), rng.uniform(-1.75, 1.75)
        clutter.add(Circle(radius=rng.uniform(0.04, 0.09), stroke_width=0, fill_color=WORK,
                           fill_opacity=0.75).move_to([x, y, 0]))
    defects = VGroup(*[Cross(scale_factor=0.08, stroke_color=COST, stroke_width=3).move_to(
        looms[k].get_center() + np.array([0.18, 0.08, 0])) for k in rng.choice(24, 2 if tidy else 9, replace=False)])
    g.add(clutter, defects)
    if tidy:
        racks = VGroup(*[Rectangle(width=0.5, height=1.6, stroke_color=PLANT, stroke_width=1.6).move_to(
            [3.35, y, 0]) for y in (0.9, -0.9)])
        g.add(racks)
    frame = RoundedRectangle(width=7.4, height=4.2, corner_radius=0.15, stroke_color=GREY_C, stroke_width=1.6)
    g.add(frame)
    return g


class Hook(VoiceoverScene):
    def construct(self):
        self.story()
        self.floors()
        self.question()
        self.title()
        self.objectives()

    def story(self):
        cards = VGroup(
            history_card(2008, r"textile plants near Mumbai", r"large, \ family-run firms making cotton fabric; \ "
                         r"economists offer free management consulting to a randomly chosen group of them",
                         color=PLANT, width=11.2, font_size=21),
            history_card(r"+17\%", r"productivity in the first year", r"in the treated plants, \ from better quality, "
                         r"\ more efficient production and less inventory; \ within three years the treated firms "
                         r"open more plants", color=GAIN, width=11.2, font_size=21),
            history_card(r"free", r"the practices had been free to adopt all along", r"recording defects, \ counting "
                         r"stock, \ keeping the floor clear; \ why had the owners not done it?", color=MGR, width=11.2,
                         font_size=21),
        ).arrange(DOWN, buff=0.35).move_to(UP * 0.3)
        tag = published_tag(r"Bloom, \ Eifert, \ Mahajan, \ McKenzie and Roberts, \ Quarterly Journal of Economics "
                            r"128(1) (2013)", corner=DL, font_size=12)
        with self.voiceover(
            "In 2008 a group of economists, Nicholas Bloom, Benn Eifert, Aprajit Mahajan, David McKenzie and John "
            "Roberts, offered free management consulting to large textile firms near Mumbai: family businesses "
            "weaving cotton fabric. They chose at random which plants would get it. <bookmark mark='a'/> The "
            "treated plants recorded their defects, counted their stock and cleared their floors. Within a year "
            "their productivity was seventeen percent higher, from better quality, more efficient production and "
            "less inventory, and within three years the treated firms had opened more plants. <bookmark mark='b'/> "
            "None of it needed a new machine. The practices had been free to adopt all along. So why had the owners "
            "not adopted them?"
        ) as vo:
            self.play(FadeIn(cards[0], shift=UP * 0.1), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[1], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(cards[2], shift=UP * 0.1))
        self.clear_scene()

    def floors(self):
        before = floor(False).scale(0.82).to_edge(LEFT, buff=0.4).shift(DOWN * 0.2)
        after = floor(True).scale(0.82).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.2)
        hb = label(r"before: \ yarn in the aisles, \ defects unrecorded", font_size=21, color=COST).next_to(
            before, UP, buff=0.3)
        ha = label(r"after: \ racks, \ clear aisles, \ defects logged and fixed", font_size=21, color=PLANT).next_to(
            after, UP, buff=0.3)
        head = label(r"one of the Island's weaving plants, \ seen from above", font_size=26, color=E.ACCENT).to_edge(
            UP, buff=0.4)
        tag = island_tag(r"the Island: \ an illustration", corner=DR, font_size=12)
        with self.voiceover(
            "The Island has textile plants too. <bookmark mark='a'/> Here is one, seen from above: twenty-four "
            "looms, yarn piled in the aisles where workers trip over it, and defects that nobody records, so the "
            "same machine makes the same fault every day. <bookmark mark='b'/> And here is the same plant after a "
            "few months of the practices: racks for the yarn, clear aisles, every defect logged and traced to its "
            "loom. Nothing here costs much. This part asks why firms differ so much in how they are run, whether "
            "it matters, and what happens inside them: how they hire, pay and promote, how they are financed and "
            "governed, and how they are organized."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(before), FadeIn(hb))
            vo.wait_until("b")
            self.play(FadeIn(after), FadeIn(ha))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"why do some plants produce twice as much as others from the same inputs?", font_size=26,
                  color=PLANT),
            label(r"can management be measured, \ and does it cause productivity?", font_size=26, color=MGR),
            label(r"how should a firm hire, \ pay and promote?", font_size=26, color=WORK),
            label(r"why are chief executives paid so much, \ and who watches them?", font_size=26, color=CEO),
            label(r"and what do debt, \ buyouts, \ hierarchies and mergers do to a firm?", font_size=26, color=FIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "The question: why are some firms so much better run than others, and can it be taught? <bookmark "
            "mark='a'/> Why do some plants produce twice as much as others from the same inputs? <bookmark "
            "mark='b'/> Can management be measured, and does it cause productivity? <bookmark mark='c'/> How should "
            "a firm hire, pay and promote? <bookmark mark='d'/> Why are chief executives paid so much, and who "
            "watches them? <bookmark mark='e'/> And what do debt, buyouts, hierarchies and mergers do to a firm?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        g = floor(True).scale(0.45)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 62 \ $\cdot$ \ Inside the Firm", font_size=34, color=E.ACCENT)
        VGroup(g, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part sixty-two: inside the firm."):
            self.play(FadeIn(g), run_time=1.4)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act XI \ $\cdot$ \ Economics at Work", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"productivity dispersion, \ and how management is measured and tested",
            r"personnel economics: \ piece rates, \ sorting, \ promotion and the Peter principle",
            r"executive pay, \ capital structure, \ agency and governance",
            r"private equity, \ hierarchies of knowledge, \ working from home",
            r"culture and relational contracts, \ and mergers that destroy value",
        ], color=E.ACCENT, font_size=28, width=13.0)
        with self.voiceover(
            "Part sixty-one went inside the platforms. This part goes inside any firm. By the end you will know "
            "<bookmark mark='a'/> how much productivity differs across firms, and how management was measured and "
            "then tested by experiment; <bookmark mark='b'/> what personnel economics says about pay, sorting and "
            "promotion; <bookmark mark='c'/> why executives are paid what they are, how firms choose their debt, "
            "and how owners control managers; <bookmark mark='d'/> what private equity, hierarchies and working "
            "from home do to a firm; <bookmark mark='e'/> and why culture is so hard to copy, and why so many "
            "mergers destroy value."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
