from __future__ import annotations

from videos.economics.econ67.common import *  # noqa: F403

GROUPS = [
    (r"design-based", ("RCT", "IV", "RD", "DiD", "event study"), TRUE),
    (r"structural and calibrated", ("structural", "calibration"), STATE),
    (r"regressions", ("regression",), FIRST),
    (r"reviews and meta-analyses", ("review", "meta-analysis"), PUB),
    (r"laboratories and surveys", ("lab", "survey"), ROW),
    (r"history and reconstruction", ("narrative", "reconstruction"), GREY_B),
]
STATUS_COL = {"settled within a range": TRUE, "depends on the setting": PUB, "contested": FAIL,
              "not identified": GREY_B}
SHORT = {"return_capital_poor": r"the return to capital in poor countries", "risk_aversion": r"risk aversion",
         "neutral_rate": r"the neutral interest rate", "ai_productivity_decade": r"AI's productivity, \ next decade",
         "school_effects": r"what schools add"}


class Audit(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Structure, \ design, \ and the Dials audited", r"What kinds of evidence has this series "
             r"used, \ and how much of it is settled?", "Chapter eight. Structure, design, and the Dials audited.",
             scale=("world",), horizon=("a century",))
        self.camps()
        self.kinds()
        self.status()

    def camps(self):
        left = point_cards([
            (r"design", r"find variation as good as random; \ estimate one effect cleanly; \ say little beyond the "
             r"sample \ (Parts 4, 38, 46)", TRUE),
        ], width=6.0, cols=1, font_size=19)
        right = point_cards([
            (r"structure", r"write down the choices that produce the data; \ estimate their parameters; \ predict "
             r"policies never tried \ (Parts 44, 51, 54)", STATE),
        ], width=6.0, cols=1, font_size=19)
        pair = VGroup(left, right).arrange(RIGHT, buff=0.5).move_to(UP * 0.9)
        rows = VGroup(
            label(r"the trade: \ credibility against reach", font_size=22, color=E.ACCENT),
            label(r"the reconciliation: \ use a design's estimates as targets a model must match \ (Part 54)",
                  font_size=20, color=GREY_A),
            label(r"or ask the model what a design would have found \ (the Island, \ throughout)", font_size=20,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(pair, DOWN, buff=0.6)
        with self.voiceover(
            "The turn left economics with two camps, and this series has worked in both. <bookmark mark='a'/> "
            "Design: find variation that is as good as random, a lottery, a border, a cutoff, and estimate one "
            "effect cleanly, without saying much beyond the sample. <bookmark mark='b'/> Structure: write down the "
            "choices that generate the data, estimate their parameters, and predict the effects of policies never "
            "tried. <bookmark mark='c'/> The trade is credibility against reach. <bookmark mark='d'/> The "
            "reconciliation, where there is one, is to use a design's clean estimates as targets the model must "
            "match, as in Part fifty-four, or to ask the model what a design would have found, as the Island has "
            "done all series."
        ) as vo:
            self.play(FadeIn(left.cards[0], shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(right.cards[0], shift=UP * 0.1))
            vo.wait_until("c")
            self.play(FadeIn(rows[0]))
            vo.wait_until("d")
            self.play(FadeIn(rows[1]), FadeIn(rows[2]))
        self.clear_scene()

    def kinds(self):
        A = load("audit")
        bd = A["by_design"]
        vals = [sum(bd.get(k, 0) for k in ks) for _, ks, _ in GROUPS]
        tot = sum(vals)
        ax = plane([0, 6], [0, 130], center=LEFT * 1.0 + DOWN * 0.1, x_length=9.0, y_length=4.4, xticks=[],
                   yticks=[0, 40, 80, 120], ylabel=r"estimates in the Dials", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        b = bars(ax, [0.5 + k for k in range(6)], vals, [c for _, _, c in GROUPS], width=0.7)
        nums = VGroup(*[label(f"{v}", font_size=17, color=c).next_to(bb, UP, buff=0.06)
                        for bb, v, (_, _, c) in zip(b, vals, GROUPS)])
        xl = VGroup(*[label(n_, font_size=14, color=c).next_to(ax.ax.c2p(0.5 + k, 0), DOWN, buff=0.15)
                      for k, (n_, _, c) in enumerate(GROUPS)])
        for x in xl:
            if x.width > 1.4:
                x.scale_to_fit_width(1.4)
        head = label(rf"{A['n_dials']} Dials, \ {A['n_estimates']} estimates, \ {A['n_film']} of them computed in "
                     r"these films", font_size=24, color=E.ACCENT).to_edge(UP, buff=0.45)
        tag = published_tag(r"the Dials' records: \ explainer/economics/dials.py", corner=DL, font_size=12)
        with self.voiceover(
            "The series kept its own ledger. Every number that a part treated as a measurement of something in the "
            f"world went into a Dial, with its source and its design. <bookmark mark='a'/> There are now "
            f"{A['n_dials']} Dials holding {A['n_estimates']} estimates, {A['n_film']} of them computed in these "
            f"films. <bookmark mark='b'/> By kind: {vals[0]} come from designs, trials, instruments, "
            f"discontinuities, differences in differences and event studies; {vals[1]} from structural or "
            f"calibrated models; {vals[2]} from plain regressions. <bookmark mark='c'/> The rest are reviews and "
            "meta-analyses, laboratories and surveys, and reconstructions of history. Both camps, and the plain "
            f"regression that neither camp admires, carry the series about equally: no kind is more than "
            f"{100 * max(vals) / tot:.0f} percent of the record."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(xl), FadeIn(tag), FadeIn(head))
            vo.wait_until("a")
            self.play(Indicate(head, color=WHITE, scale_factor=1.03))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in b[:3]], lag_ratio=0.3), FadeIn(nums[:3]),
                      run_time=1.8)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(bb, DOWN) for bb in b[3:]], lag_ratio=0.3), FadeIn(nums[3:]),
                      run_time=1.5)
        self.clear_scene()

    def status(self):
        A = load("audit")
        st = A["statuses"]
        order = ["settled within a range", "depends on the setting", "contested", "not identified"]
        tot = sum(st.values())
        bar = VGroup()
        x0 = -6.2
        for s_ in order:
            w = 12.4 * st.get(s_, 0) / tot
            r = Rectangle(width=w, height=0.75, fill_color=STATUS_COL[s_], fill_opacity=0.8, stroke_width=0)
            r.move_to([x0 + w / 2, 2.2, 0])
            bar.add(r)
            x0 += w
        labs = VGroup()
        for r, s_ in zip(bar, order):
            t = label(rf"{s_}: \ {st.get(s_, 0)}", font_size=15, color=STATUS_COL[s_])
            if s_ == "not identified":
                t.next_to(r, UP, buff=0.12).shift(LEFT * 0.6)
            else:
                t.next_to(r, DOWN, buff=0.12)
            labs.add(t)
        wide = A["widest"][:5]
        rows = VGroup(*[label(rf"{SHORT.get(w_['key'], tex_safe(w_['name']))}: \ largest estimate "
                              rf"{w_['spread']:.0f} times the smallest", font_size=19, color=GREY_A)
                        for w_ in wide]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        wh = label(r"the widest disagreements:", font_size=21, color=FAIL)
        VGroup(wh, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(labs, DOWN, buff=0.6).to_edge(
            LEFT, buff=0.9)
        tag = published_tag(r"the Dials' records: \ explainer/economics/dials.py", corner=DL, font_size=12)
        settled = st.get("settled within a range", 0)
        with self.voiceover(
            "And how much is settled? Each Dial carries a status, set when its part was written. <bookmark "
            f"mark='a'/> {settled} of the {tot} are settled within a range: the evidence agrees about the "
            f"size. {st.get('depends on the setting', 0)} depend on the setting, which is a finding, not a failure: "
            "the effect really differs from place to place. <bookmark mark='b'/> "
            f"{st.get('contested', 0)} are contested, and {st.get('not identified', 0)} are not identified at all "
            "with the data we have. <bookmark mark='c'/> The widest disagreements: the return to capital in poor "
            f"countries, where the largest estimate is {wide[0]['spread']:.0f} times the smallest; risk aversion, the "
            "neutral interest rate, the productivity effect of AI, and what schools add. These are the questions "
            "where the next economics has the most to do."
        ) as vo:
            self.play(FadeIn(tag), *[GrowFromEdge(r, LEFT) for r in bar], run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(labs[0]), FadeIn(labs[1]))
            vo.wait_until("b")
            self.play(FadeIn(labs[2]), FadeIn(labs[3]))
            vo.wait_until("c")
            self.play(FadeIn(wh), LaggedStart(*[FadeIn(r_) for r_ in rows], lag_ratio=0.3), run_time=2.0)
        self.clear_scene()
