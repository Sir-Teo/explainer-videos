from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.interference()
        self.longterm()
        self.privacy()

    def card(self):
        self.chapter(13, r"Frontier: \ measuring people, \ carefully", r"What can an experiment not see?", lit=(2013, 2019), extra=((2013, r"Ugander et al.: \ graph cluster randomization"),
                                   (2019, r"Athey et al.: \ surrogate indices")), part=PART, said="Chapter thirteen, the frontier. What can an experiment not see?")

    def interference(self):
        r = load("interference")
        lim, amp = r["limited"], r["ample"]
        head = label(r"When units are not independent", font_size=36).to_edge(UP, buff=0.3)
        # a marketplace: buyers on the left, a fixed shelf of items on the right
        buyers = VGroup(*[Dot(radius=0.07, color=HEAD if k % 2 else GREY_B) for k in range(40)]).arrange_in_grid(
            rows=5, cols=8, buff=0.18).move_to([-4.3, 1.0, 0])
        shelf = VGroup(*[Square(0.2, stroke_color=YES, fill_color=YES, fill_opacity=0.6) for _ in range(12)]
                       ).arrange_in_grid(rows=3, cols=4, buff=0.12).move_to([-0.6, 1.0, 0])
        bl = label(r"buyers: \ treated \ (yellow) \ and control", font_size=17, color=GREY_B).next_to(buyers, DOWN,
                                                                                                buff=0.2)
        sl = label(r"limited supply", font_size=17, color=YES).next_to(shelf, DOWN, buff=0.2)
        arrows = VGroup(*[Arrow(buyers[k].get_center(), shelf[k % 12].get_center(), buff=0.1, stroke_width=1.5,
                                color=HEAD, max_tip_length_to_length_ratio=0.05) for k in range(1, 24, 2)])
        rows = [[r"limited supply", f"{100 * lim['ab_estimate']:+.1f}", f"{100 * lim['true_global']:+.1f}"],
                [r"ample supply", f"{100 * amp['ab_estimate']:+.1f}", f"{100 * amp['true_global']:+.1f}"]]
        tab = grid_table([r"marketplace", r"A/B estimate \ (points)", r"launch to all \ (points)"], rows,
                         widths=[2.6, 2.6, 2.6], row_h=0.5, font_size=19, mono_cols=())
        tab.move_to([3.6, 1.0, 0])
        tab.cells[1][1].set_color(NO)
        tab.cells[1][2].set_color(YES)
        lines = VGroup(
            wrapped_label(rf"treated buyers are {100 * (lim['q'][1] - lim['q'][0]):.0f} points keener; \ with "
                          r"limited supply every extra sale to them is a sale a control buyer lost", 12.4,
                          font_size=20, color=WHITE),
            wrapped_label(r"fixes: \ randomize whole markets, \ cities or time slots \ (switchbacks); \ in social "
                          r"networks, \ clusters of friends \ (Ugander et al., \ 2013)", 12.4, font_size=20,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Every test in this part assumed that what happens to one user does not depend on what happens to "
            "another. Marketplaces break that. <bookmark mark='a'/> We simulated ten thousand buyers and three "
            "thousand items. The treatment makes buyers six points keener. <bookmark mark='b'/> But supply is "
            "limited, so every extra item a treated buyer takes is one a control buyer cannot have. "
            f"<bookmark mark='c'/> The A/B test reports a lift of {100 * lim['ab_estimate']:.1f} points. Launch the "
            f"treatment to everyone, and sales rise by {100 * lim['true_global']:.1f}: almost nothing, because "
            "supply was the limit all along. With ample supply the two agree. <bookmark mark='d'/> The fixes "
            "randomize whole units that do not interact: entire cities, or alternating time slots, called "
            "switchbacks, and in social networks, clusters of friends, as Johan Ugander and colleagues proposed in "
            "2013. Designing experiments under interference is an active field."
        ) as vo:
            self.play(FadeIn(head), FadeIn(buyers), FadeIn(shelf), FadeIn(bl), FadeIn(sl))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.1), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def longterm(self):
        head = label(r"Effects that take years", font_size=36).to_edge(UP, buff=0.3)
        x0, y0 = -6.0, -0.6
        axis = Arrow([x0, y0, 0], [6.2, y0, 0], buff=0, color=GREY_C, stroke_width=2)
        segs = [(r"two-week test", 0.0, 1.2, HEAD), (r"what we care about: \ a year of retention", 1.2, 12.0, LAM)]
        bars = VGroup()
        for t, a, b, c in segs:
            r = Rectangle(width=b - a, height=0.45, stroke_width=0, fill_color=c, fill_opacity=0.7).move_to(
                [x0 + (a + b) / 2, y0 + 0.4, 0])
            bars.add(VGroup(r, label(t, font_size=18, color=c).next_to(r, UP, buff=0.1)))
        lines = VGroup(
            wrapped_label(r"novelty fades and habits form: \ a short test can mislead about the long run", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"\textbf{surrogate indices} \ (Athey, \ Chetty, \ Imbens and Kang, \ 2019): \ predict the "
                          r"long-term outcome from short-term signals learned on past experiments", 12.4,
                          font_size=21, color=YES),
            wrapped_label(r"\textbf{holdouts}: \ keep a few users on the old product for months, \ and measure the "
                          r"accumulated effect of many launches", 12.4, font_size=21, color=HEAD),
            wrapped_label(r"open: \ when is a surrogate valid, \ and how wrong can it be?", 12.4, font_size=21,
                          color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A second limit is time. <bookmark mark='a'/> A test runs for two weeks; what a company cares about, "
            "whether people are still using the product next year, takes a year to see. Novelty fades, habits "
            "form, and a short test can point the wrong way. <bookmark mark='b'/> One answer is the surrogate index "
            "of Susan Athey, Raj Chetty, Guido Imbens and Hyunseung Kang: learn, from many past experiments, how "
            "short-term signals predict the long-term outcome, and use that prediction as the metric. "
            "<bookmark mark='c'/> Another is a long-running holdout: a few users kept on the old product for "
            "months, against whom the accumulated effect of many launches is measured. <bookmark mark='d'/> When a "
            "surrogate can be trusted, and how wrong it can be, are open questions."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(axis), FadeIn(bars[0]))
            vo.wait_until("a")
            self.play(FadeIn(bars[1]), FadeIn(lines[0]))
            for mk, ln in zip("bcd", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    def privacy(self):
        self.ask(r"Each answer is randomized: no single one can be trusted. \\ The overall rate is...", [r"unknowable",
                 r"still estimable"], 1,
                 say="Each person flips a coin before answering, so no single answer can be trusted. Can we still learn the overall rate?",
                 reveal="Yes: the noise is known, so it can be subtracted on average.")
        pr = load("privacy")
        head = label(r"Measuring without looking", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(*[label(t, font_size=21, color=c) for t, c in (
            (rf"with probability {pr['p_truth']:.2f}: \ answer truthfully", YES),
            (rf"otherwise: \ flip a coin and answer that", HEAD),
            (r"any single answer is deniable", DATA),
            (r"the population's rate is still recoverable", LAM))]).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        steps.to_edge(LEFT, buff=0.6).shift(UP * 1.0)
        rows = [[f"{r['n']:,}", f"{100 * r['err_plain']:.2f}", f"{100 * r['err_private']:.2f}"] for r in pr["rows"]]
        tab = grid_table([r"people", r"error, \ honest survey \ (points)", r"error, \ randomized"], rows,
                         widths=[1.8, 3.2, 2.6], row_h=0.45, font_size=19, mono_cols=())
        tab.to_edge(RIGHT, buff=0.5).shift(UP * 1.0)
        eq = MathTex(r"\hat r = \frac{\bar a - (1-p)/2}{p}", font_size=36, color=WHITE).next_to(steps, DOWN, buff=0.5)
        lines = VGroup(
            wrapped_label(rf"Warner \ (1965); \ in today's terms, \ local differential privacy with "
                          rf"$\varepsilon = {pr['epsilon']:.2f}$: \ the price is about one and a half times the error",
                          12.4, font_size=20, color=WHITE),
            wrapped_label(r"deployed: \ Google's RAPPOR \ (2014), \ Apple's keyboard and emoji statistics \ (2016), \ "
                          r"the 2020 US Census \ (central, \ not local)", 12.4, font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A third limit is privacy: some things should be measured without anyone being watched. "
            "<bookmark mark='a'/> The oldest trick is Stanley Warner's randomized response, from 1965. Ask a "
            "sensitive question. Each person answers truthfully three times in four, and otherwise flips a coin "
            "and gives that answer instead. <bookmark mark='b'/> No single answer reveals anything certain, but "
            "the rate in the population can be recovered by undoing the known noise. <bookmark mark='c'/> The "
            "price is precision: with a true rate of twenty percent, the private estimate's error is about one and "
            "a half times that of an honest survey of the same size, at every size we tried. In today's language "
            f"this is local differential privacy, with epsilon of about {pr['epsilon']:.1f}. "
            "<bookmark mark='d'/> Google's RAPPOR used it for browser statistics in 2014, Apple for keyboard "
            "statistics in 2016, and the 2020 United States Census applied differential privacy centrally to its "
            "published tables."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(steps[0]), FadeIn(steps[1]))
            vo.wait_until("b")
            self.play(FadeIn(steps[2]), FadeIn(steps[3]), FadeIn(eq))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()




_ = (DATA, KERN, LAM, NO, YES)
