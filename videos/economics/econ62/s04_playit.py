from __future__ import annotations

from videos.economics.econ62.common import *  # noqa: F403

ORDER = ("record and act on defects", "count and cut inventory", "a faster loom", "pay for performance")
NAMES = ("A", "B", "C", "D")
SHORT = (r"record and act \\ on defects", r"count and cut \\ inventory", r"a faster \\ loom", r"pay for \\ performance")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Play it: \ four practices and a budget", r"Which pays the most for each dollar it costs?",
             "Chapter three. Play it: four practices and a budget.", scale=("firm",), horizon=("a year",))
        self.stage()
        self.reveal()

    def stage(self):
        P = load("practices")
        T = P["table"]
        rows = VGroup()
        for n, key in zip(NAMES, ORDER):
            t = T[key]
            what = (rf"output +{100 * t['output']:.0f}\%" if t["output"] else
                    rf"inventory {-100 * t['inventory']:.0f}\%".replace("-", "{-}"))
            rows.add(label(rf"{n} \ \ {key}: \ costs \${t['cost']:.0f} thousand; \ {what} if it works; \ works "
                           rf"{100 * t['p']:.0f}\% of the time", font_size=21,
                           color=(PLANT, OWN, GREY_A, WORK)[NAMES.index(n)]))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(UP * 0.3)
        if rows.width > 13.0:
            rows.width = 13.0
        facts = label(rf"one Island plant: \ revenue \${P['revenue'] / 1000:.0f} million a year, \ inventory worth "
                      r"\$1.5 million carried at 12\% a year; \ value over three years", font_size=20,
                      color=GREY_A).to_edge(UP, buff=0.5)
        if facts.width > 13.0:
            facts.width = 13.0
        tag = island_tag(r"the Island: \ agora.org.practices; \ effects and odds planted", corner=DL, font_size=12)
        with self.voiceover(
            "Your turn. You own one of the Island's weaving plants, with eight million dollars of sales a year, and "
            "you can afford one change. <bookmark mark='a'/> A: record every defect and act on it, for sixty "
            "thousand dollars of consultants' and managers' time; it raises output eight percent when it works. "
            "<bookmark mark='b'/> B: count your stock and cut it, for forty thousand, freeing a third of the "
            "inventory. <bookmark mark='c'/> C: a faster loom, six hundred thousand dollars, ten percent more "
            "output, and almost sure to work. <bookmark mark='d'/> D: pay workers for performance, a hundred and "
            "fifty thousand to design and run, six percent more output, but it works only sixty percent of the "
            "time. <bookmark mark='e'/> Which pays the most for each dollar it costs, over three years?"
        ) as vo:
            self.play(FadeIn(facts), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.15))
            vo.wait_until("e")
        ring = countdown().scale(0.6).next_to(rows, DOWN, buff=0.5)
        self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=7.0, rate_func=linear)
        self.play(FadeOut(ring), Indicate(rows[0], color=WHITE, scale_factor=1.03))
        self.wait(0.5)
        self.clear_scene()

    def reveal(self):
        P = load("practices")
        R = P["rows"]
        vals = [R[k]["per_dollar"] for k in ORDER]
        ax = plane([-0.6, 3.6], [-1, 5.5], center=LEFT * 2.9 + DOWN * 0.4, x_length=6.4, y_length=4.6, xticks=[],
                   yticks=[-1, 0, 1, 2, 3, 4, 5], ylabel=r"net value over three years, \ per dollar spent",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=14)
        cols = (PLANT, OWN, COST, WORK)
        b = bars(ax, range(4), vals, cols, width=0.55)
        zero = seg(ax, -0.6, 0, 3.6, 0, GREY_C, 1.2)
        labs = VGroup(*[label(rf"{n}: \ {s_}", font_size=14, color=c).next_to(ax.ax.c2p(k, -1), DOWN, buff=0.1)
                        for k, (n, s_, c) in enumerate(zip(NAMES, SHORT, cols))])
        vl = VGroup(*[label(f"{v:+.2f}".replace("-", "{-}"), font_size=15, color=c).next_to(
            x, UP if v >= 0 else DOWN, buff=0.06) for v, c, x in zip(vals, cols, b)])
        side = VGroup(
            label(rf"A: \ \${R[ORDER[0]]['mean_net']:.0f} thousand net, \ {R[ORDER[0]]['per_dollar']:.1f} per dollar",
                  font_size=20, color=PLANT),
            label(rf"B: \ \${R[ORDER[1]]['mean_net']:.0f} thousand, \ {R[ORDER[1]]['per_dollar']:.1f} per dollar",
                  font_size=20, color=OWN),
            label(rf"C: \ loses \${-R[ORDER[2]]['mean_net']:.0f} thousand over three years", font_size=20, color=COST),
            label(rf"D: \ {R[ORDER[3]]['per_dollar']:.2f} per dollar, \ and a wide spread", font_size=20, color=WORK),
            label(r"the cheap practices pay most: \ the Mumbai plants' lesson", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        if side.width > 6.0:
            side.width = 6.0
            side.to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ 20,000 draws of each practice's luck and size".replace(",", "{,}"),
                         corner=DL, font_size=12)
        with self.voiceover(
            "Here is what each change is worth over three years, per dollar it costs. <bookmark mark='a'/> A, "
            f"recording and acting on defects, returns {vals[0]:.1f} dollars of net value for every dollar: about "
            f"{R[ORDER[0]]['mean_net']:.0f} thousand dollars. <bookmark mark='b'/> B, cutting inventory, "
            f"{vals[1]:.1f} per dollar. <bookmark mark='c'/> C, the loom, the most visible investment, loses money "
            "over three years: it pays back eventually, but slowly. <bookmark mark='d'/> D, pay for performance, "
            f"returns {vals[3]:.2f} per dollar on average, with a wide spread: incentive schemes fail as often as "
            "they work if they are badly designed, as chapter five will show. <bookmark mark='e'/> So A. The cheap, "
            "dull practices pay most, which is exactly what the Mumbai experiment found, and exactly why it is "
            "puzzling that so many owners had not adopted them."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(labs), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[k], DOWN if vals[k] >= 0 else UP), FadeIn(vl[k]), FadeIn(side[k]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
