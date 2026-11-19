from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403


class Maximize(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Do firms maximize profit?", r"Business people say they set prices by rules of thumb; does the "
             r"theory survive?", "Chapter nine. Do firms maximize profit?", lit={1953: r"Friedman's billiard player"},
             scale=("firm", "market"), horizon=("a decade",))
        self.hall_hitch()
        self.as_if()
        self.survival()

    def hall_hitch(self):
        hc = history_card(1939, r"Oxford: \ Robert Hall and Charles Hitch", r"they ask businessmen how they set "
                          r"prices: \ estimate average cost at a ``normal'' output, \ add a margin, \ and stick to "
                          r"it", color=CAP, width=11.4, font_size=25).move_to(UP * 1.8)
        rows = VGroup(
            label(r"``full-cost pricing'': \ nobody mentioned marginal revenue or marginal cost", font_size=26),
            label(r"such a rule maximizes profit only by accident, \ they argued", font_size=26, color=CAP),
            label(r"the ``marginalist controversy'': \ if firms don't compute marginal cost, \\ what use is a theory "
                  r"that assumes they equate it to price?", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.35).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Hall and Hitch, Oxford Economic Papers 2 (1939) 12--45", corner=DR, font_size=14)
        with self.voiceover(
            "Everything so far assumed the firm maximizes profit. In 1939 two Oxford economists, Robert Hall and "
            "Charles Hitch, went and asked. <bookmark mark='a'/> They put questions to the heads of a few dozen "
            "firms about how they set prices, and the answer was a rule of thumb: estimate average cost at a normal "
            "level of output, add a conventional margin, and stick to the price. <bookmark mark='b'/> Nobody "
            "talked about marginal revenue or marginal cost. A rule like that, they argued, would maximize profit "
            "only by accident. <bookmark mark='c'/> It started what was called the marginalist controversy: if "
            "firms don't compute marginal cost, what use is a theory that assumes they set it equal to price?"
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def as_if(self):
        c1 = history_card(1950, r"Armen Alchian: \ ``Uncertainty, Evolution, and Economic Theory''",
                          r"whatever firms intend, \ the market keeps the ones that happen to make profits: \ "
                          r"survival does the maximizing", color=COST, width=11.4, font_size=24)
        c2 = history_card(1953, r"Milton Friedman: \ ``The Methodology of Positive Economics''",
                          r"an expert billiard player doesn't solve the equations of mechanics, \ but his shots are "
                          r"predicted well by assuming he does: \ judge a theory by its predictions, \ not by its "
                          r"assumptions", color=PRICE, width=11.4, font_size=24)
        g = VGroup(c1, c2).arrange(DOWN, buff=0.4).move_to(UP * 0.3)
        head = label(r"the defence: \ does it matter what firms think they are doing?", font_size=30,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        foot = label(r"the objection that remains: \ selection is slow, \ noisy, \ and needs competition", font_size=25,
                     color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"Alchian, JPE 58(3) (1950); Friedman, \emph{Essays in Positive Economics} (1953), p.\ 21",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Two answers came from Chicago and Los Angeles. <bookmark mark='a'/> In 1950 Armen Alchian argued that "
            "it doesn't matter what firms intend. In a competitive market, the firms that happen to make profits "
            "survive and grow, and the rest disappear. Survival does the maximizing. <bookmark mark='b'/> In 1953 "
            "Milton Friedman added his famous billiard player. An expert player doesn't solve the equations of "
            "mechanics before each shot, but his shots are well predicted by assuming that he does. Judge a theory, "
            "Friedman said, by its predictions, not by the realism of its assumptions. <bookmark mark='c'/> The "
            "objection that remains is that selection is slow and noisy, and works only where competition is fierce. "
            "We can watch it work on the Island."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(c1, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(c2, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def survival(self):
        s = load("selection")
        pct = np.array(s["pct"])
        months = np.array(s["months"])
        ax = plane([0, 120], [0, 1.0], center=LEFT * 2.6 + DOWN * 0.3, x_length=7.4, y_length=5.0,
                   xticks=[0, 24, 48, 72, 96, 120], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"months",
                   ylabel=r"markup over cost", font_size=17, yfmt=lambda v: f"{100 * v:.0f}\\%")
        a = ax.ax
        def band(lo, hi, i0, i1, op):
            m_, l_, h_ = months[i0:i1 + 1], lo[i0:i1 + 1], hi[i0:i1 + 1]
            return Polygon(*[a.c2p(m, v) for m, v in zip(m_, l_)], *[a.c2p(m, v) for m, v in zip(m_[::-1], h_[::-1])],
                           stroke_width=0, fill_color=COST, fill_opacity=op)

        cuts = np.linspace(0, len(months) - 1, 13).astype(int)
        bands = VGroup(*[VGroup(band(pct[0], pct[4], i0, i1, 0.15), band(pct[1], pct[3], i0, i1, 0.3))
                         for i0, i1 in zip(cuts[:-1], cuts[1:])])
        med = VMobject(stroke_color=COST, stroke_width=3).set_points_as_corners(
            [a.c2p(m, v) for m, v in zip(months, pct[2])])
        start = VGroup(Line(a.c2p(0, pct[0][0]), a.c2p(0, pct[4][0]), color=COST, stroke_width=8),
                       label(r"month 0: \ markups all over", font_size=18, color=COST).next_to(
                           a.c2p(0, 0.85), RIGHT, buff=0.15))
        best = DashedLine(a.c2p(0, s["best"]), a.c2p(120, s["best"]), color=PRICE, stroke_width=2.5).set_z_index(3)
        bl = label(r"the profit-maximizing markup: \ 50\%", font_size=19, color=PRICE).next_to(a.c2p(96, s["best"]),
                                                                                              UP, buff=0.1)
        bl.add_background_rectangle(color=BACKGROUND, opacity=0.8, buff=0.05).set_z_index(4)
        side = VGroup(
            label(r"200 yards, \ each pricing at cost \\ plus a habitual markup, \ 0--100\%", font_size=23),
            label(r"none of them computes anything", font_size=22, color=GREY_A),
            label(r"three losing months and a yard closes; \\ a newcomer copies a profitable one, \\ "
                  r"with small variations", font_size=22),
            label(rf"{s['total_closed']} closures in ten years", font_size=23, color=HOLD),
            label(rf"the middle half of markups: \\ {100 * pct[1][0]:.0f}--{100 * pct[3][0]:.0f}\% at first, \ "
                  rf"{100 * pct[1][-1]:.0f}--{100 * pct[3][-1]:.0f}\% after ten years", font_size=22, color=COST),
            label(r"the market converges on the maximizing \\ markup, \ slowly, \ with losses on the way",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"simulated: the Island (seeded)", corner=DR, font_size=15)
        with self.voiceover(
            "Here's Alchian's argument, run. <bookmark mark='a'/> Two hundred yards each price at cost plus a "
            "habitual markup, drawn at random between nothing and a hundred percent. None of them computes "
            "anything. Each faces demand with an elasticity of minus three, so the markup that maximizes profit is "
            "fifty percent. <bookmark mark='b'/> A yard that loses money three months running closes, and a "
            "newcomer copies a profitable yard, with small variations. <bookmark mark='c'/> Over ten years, four "
            "hundred and seventy-nine yards close. <bookmark mark='d'/> And the markups of the survivors close in on "
            "fifty percent: the middle half of them runs from twenty-two to seventy-five percent at the start, and "
            "from forty-six to fifty-seven after ten years. <bookmark mark='e'/> The market ends up near where "
            "maximizing firms would be, though nobody maximized. But it took years, and nearly five hundred failures."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(best), FadeIn(bl))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(side[1]), FadeIn(start))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), FadeOut(start[1]))
            self.play(LaggedStart(*[FadeIn(b_) for b_ in bands], lag_ratio=0.5), Create(med), run_time=5,
                      rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
            vo.wait_until("e")
            self.play(FadeIn(side[5]))
        self.clear_scene()
