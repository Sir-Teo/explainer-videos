from __future__ import annotations

from videos.economics.econ58.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ weights and wellbeing", r"Should a dollar count the same for everyone, \ and must "
             r"everything be dollars?", "Chapter fifteen. Frontier: weights and wellbeing.",
             lit={2021: r"the WELLBY", 2023: r"weights in Circular A-4"}, scale=("person", "nation"),
             horizon=("a decade",))
        self.weights()
        self.open_()

    def weights(self):
        F = tables.FRONTIER58.data
        V = tables.VALUES_58.data
        x = np.linspace(0.25, 4.0, 60)
        w = appraisal.distributional_weights(x, 1.0, F["eps"])
        ax = plane([0, 4], [0, 7], center=LEFT * 2.8 + DOWN * 0.5, x_length=6.4, y_length=4.6,
                   xticks=[0, 0.5, 1, 2, 3, 4], yticks=[0, 1, 2, 4, 6], xlabel=r"income $\div$ the median",
                   ylabel=r"weight on a dollar", xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        cv = path(ax, x, np.minimum(w, 7.0), SAFE, 3.0)
        one = DashedLine(ax.ax.c2p(0, 1), ax.ax.c2p(4, 1), color=GREY_C, stroke_width=1.2)
        half = appraisal.distributional_weights(0.5, 1.0, F["eps"])
        two = appraisal.distributional_weights(2.0, 1.0, F["eps"])
        pts = VGroup(dot(ax, 0.5, half, SAFE, 0.08), dot(ax, 2.0, two, SAFE, 0.08))
        pl = VGroup(label(f"{half:.2f}", font_size=18, color=SAFE).next_to(pts[0], RIGHT, buff=0.1),
                    label(f"{two:.2f}", font_size=18, color=SAFE).next_to(pts[1], UP, buff=0.1))
        side = VGroup(
            MathTex(r"\omega(y) = \left(\frac{\tilde y}{y}\right)^{\varepsilon}, \quad \varepsilon = 1.4",
                    font_size=30, color=WHITE),
            label(r"OMB's 2023 circular allowed such weights; \ rescinded in 2025", font_size=19, color=GREY_A),
            label(r"the Green Book permits them, \ as a sensitivity", font_size=19, color=GREY_A),
            label(rf"a WELLBY \ (one point of life satisfaction for a year): \\ \pounds{V['wellby']:,} \ "
                  rf"(\pounds{V['wellby_lo']:,} to \pounds{V['wellby_hi']:,}, \ 2019 prices)".replace(",", "{,}"),
                  font_size=19, color=BEN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        if side.width > 6.2:
            side.width = 6.2
            side.to_edge(RIGHT, buff=0.3)
        tag = published_tag(tables.FRONTIER58.tag, corner=DL, font_size=12)
        q1 = label(r"should a dollar count the same, \ whoever gets it?", font_size=32, color=E.ACCENT).move_to(
            UP * 0.3)
        with self.voiceover(
            "Two questions at the edge of the method. The first: should a dollar count the same whoever gets it? "
            "Standard cost-benefit analysis says yes, and leaves the distribution to the tax system. <bookmark "
            "mark='a'/> The alternative is to weight each dollar by how much it means to the person who receives "
            "it: the median income over theirs, to a power. <bookmark mark='b'/> With the power at one point four, "
            f"a dollar to a household at half the median counts {half:.2f} times, and one at twice the median "
            f"{two:.2f} times. <bookmark mark='c'/> America's 2023 circular allowed such weights, and the circular "
            "was rescinded two years later; Britain's Green Book permits them as a sensitivity. <bookmark mark='d'/> "
            "The second question: must everything be turned into dollars at all? Since 2021 Britain's Treasury has "
            "allowed appraisals to count wellbeing directly, in WELLBYs, one point of life satisfaction on a scale "
            f"of ten for one person for a year, valued at {V['wellby']:,} pounds at 2019 prices, if the effect on "
            "wellbeing has been measured by a credible experiment."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(q1, shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeOut(q1), run_time=0.5)
            self.play(FadeIn(ax), Create(one), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(cv), FadeIn(pts), FadeIn(pl), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def open_(self):
        cards = point_cards([
            (r"open models", r"tax-benefit calculators published as open code, \ so that anyone can score a "
             r"reform, \ and check a score", TRAV),
            (r"machine-learned demand", r"traffic and take-up predicted from data on many past projects: \ the "
             r"outside view, \ automated, \ and still to be scored", SAFE),
            (r"appraisal and evaluation joined", r"projects evaluated after they open, \ against the forecasts "
             r"that justified them, \ and published", BEN),
            (r"what remains hard", r"values without markets, \ the rate for centuries, \ the behaviour of people "
             r"who know they are being scored", COST),
        ], width=12.6, cols=2, font_size=21).move_to(DOWN * 0.2)
        head = label(r"what remains open", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Three developments, and what remains hard. <bookmark mark='a'/> Tax and benefit calculators are being "
            "published as open code, so that anyone can score a reform and check an official score. <bookmark "
            "mark='b'/> Demand forecasts learned from data on many past projects automate Kahneman's outside "
            "view, and they too will need a record. <bookmark mark='c'/> And evaluation after the fact is spreading: "
            "England's road agency, for one, evaluates its larger schemes a year and five years after they open, "
            "against the forecasts that justified them. <bookmark mark='d'/> What remains hard is what this part "
            "found hard: values without markets, "
            "the rate at which to weigh the centuries, and the behaviour of people who know they are being scored."
        ) as vo:
            self.play(FadeIn(head))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
