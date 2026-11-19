from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403


class Curves(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Cost curves from the technology", r"Where do the textbook's U-shaped cost curves come from?",
             "Chapter five. Cost curves from the technology.", scale=("firm",), horizon=("a day", "a year"))
        self.short_run()
        self.averages()
        self.envelope()

    def short_run(self):
        c = load("curves")
        qs = np.array(c["qs"])
        ax = plane([0, 16], [0, 30000], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[0, 4, 8, 12, 16], yticks=[0, 10000, 20000, 30000], xlabel=r"boats a month",
                   ylabel=r"\$ a month", font_size=17, yfmt=lambda v: f"{v / 1000:.0f}k")
        fc = path(ax, qs, np.full_like(qs, c["fc"]), color=CAP, width=3, smooth=False)
        vc = path(ax, qs, c["vc"], color=LAB, width=3, yr=(0, 30000))
        tc = path(ax, qs, c["tc"], color=COST, width=3.5, yr=(0, 30000))
        names = VGroup(label(r"fixed: \ 4 slipways, \ \$1{,}600", font_size=19, color=CAP).next_to(
            ax.ax.c2p(10, c["fc"]), UP, buff=0.08),
            label(r"variable: \ shipwrights", font_size=19, color=LAB).next_to(ax.ax.c2p(9.5, 18000), RIGHT,
                                                                                 buff=0.1),
            label(r"total", font_size=19, color=COST).next_to(ax.ax.c2p(8.6, 22000), LEFT, buff=0.15))
        side = VGroup(
            label(r"the short run: \ four slipways, \ already rented", font_size=24),
            label(r"fixed cost: \ paid whatever is built", font_size=23, color=CAP),
            label(r"variable cost: \ shipwrights, \ more of them \\ for each extra boat", font_size=23, color=LAB),
            label(r"with capital fixed, diminishing returns \\ make each extra boat dearer", font_size=23,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "The cost function was the long run, where every input can change. In the short run some can't. "
            "<bookmark mark='a'/> Suppose Crusoe has rented four slipways for the year. Their sixteen hundred dollars "
            "a month is a fixed cost: paid whether he builds no boats or ten. <bookmark mark='b'/> Shipwrights are "
            "the variable cost, and with the slipways fixed, diminishing returns mean each extra boat needs more "
            "extra labour than the last. <bookmark mark='c'/> Total cost is the sum: it starts at the fixed cost and "
            "curves upward."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(fc), FadeIn(names[0]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(vc), FadeIn(names[1]), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("c")
            self.play(Create(tc), FadeIn(names[2]))
        self.clear_scene()

    def averages(self):
        c = load("curves")
        qs = np.array(c["qs"])
        ax = plane([0, 16], [0, 4000], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[0, 4, 8, 12, 16], yticks=[0, 1000, 2000, 3000, 4000], xlabel=r"boats a month",
                   ylabel=r"\$ a boat", font_size=17)
        atc = path(ax, qs, c["atc"], color=ATC, width=3.5, yr=(0, 4000))
        avc = path(ax, qs, c["avc"], color=AVC, width=3, yr=(0, 4000))
        mc = path(ax, qs, c["mc"], color=MC, width=3, yr=(0, 4000))
        P = Dot(ax.ax.c2p(c["atc_min_q"], c["atc_min"]), radius=0.09, color=E.ACCENT)
        names = VGroup(label(r"average total", font_size=19, color=ATC).next_to(ax.ax.c2p(1.2, 3300), RIGHT,
                                                                               buff=0.1),
                       label(r"average variable", font_size=19, color=AVC).next_to(ax.ax.c2p(14, c["avc"][-20]), UP,
                                                                                  buff=0.1),
                       label(r"marginal", font_size=19, color=MC).next_to(ax.ax.c2p(12.5, 3500), LEFT, buff=0.1))
        side = VGroup(
            label(r"per boat: \ average total, \ average variable", font_size=24),
            label(r"marginal cost: \ the cost of one more boat", font_size=24, color=MC),
            label(rf"marginal cost cuts average total cost \\ at its lowest point: \ {c['atc_min_q']:.1f} boats, "
                  rf"\\ \${c['atc_min']:,.0f} a boat".replace(",", "{,}"), font_size=24, color=E.ACCENT),
            label(r"below the average, \ the next boat pulls it down; \\ above, \ it pushes it up", font_size=22,
                  color=GREY_A),
            label(r"the U: \ fixed cost spread thin, \ then \\ diminishing returns", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Divide by output to get costs per boat. <bookmark mark='a'/> Average total cost falls at first, as the "
            "fixed cost of the slipways is spread over more boats, then rises as diminishing returns take over: the "
            "textbook's U. Average variable cost, the shipwrights alone, rises from the start. "
            "<bookmark mark='b'/> Marginal cost is the cost of one more boat. <bookmark mark='c'/> It cuts average "
            "total cost at the bottom of the U: three point six boats a month, at eight hundred and ninety-four "
            "dollars a boat. <bookmark mark='d'/> That isn't a coincidence. When the next boat costs less than the "
            "average, building it pulls the average down; when it costs more, it pushes the average up. So the "
            "average is lowest where the two are equal. <bookmark mark='e'/> The U shape is the two forces of this "
            "chapter in one picture."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(atc), FadeIn(names[0]), Create(avc), FadeIn(names[1]), run_time=2)
            vo.wait_until("b")
            self.play(Create(mc), FadeIn(names[2]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(P, scale=0.5), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def envelope(self):
        c = load("curves")
        qs = np.array(c["qs"])
        ax = plane([0, 16], [0, 2500], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.6, y_length=5.0,
                   xticks=[0, 4, 8, 12, 16], yticks=[0, 500, 1000, 1500, 2000, 2500], xlabel=r"boats a month",
                   ylabel=r"\$ a boat", font_size=17)
        srs = VGroup(*[path(ax, qs, c["srs"][k], color=ATC, width=2.2, yr=(0, 2500)) for k in ("1", "2", "4", "8",
                                                                                                "16")])
        labs = VGroup(*[label(rf"{k} slipways", font_size=15, color=ATC) for k in ("1", "2", "4", "8", "16")])
        for k, lb in zip(("1", "2", "4", "8", "16"), labs):
            v = np.array(c["srs"][k])
            j = int(np.argmin(v))
            lb.next_to(ax.ax.c2p(qs[j], v[j]), DOWN, buff=0.08)
        lr = path(ax, qs, c["lr_ac"], color=COST, width=4, yr=(0, 2500))
        side = VGroup(
            label(r"one short-run curve for each \\ number of slipways", font_size=24, color=ATC),
            label(r"the long run can choose the slipways: \\ its average cost is the lower envelope", font_size=24,
                  color=COST),
            label(r"with decreasing returns it rises; \\ with constant returns it would be flat", font_size=22,
                  color=GREY_A),
            label(r"short run: \ what you have; \\ long run: \ what you can choose", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now let the number of slipways change. <bookmark mark='a'/> Each choice gives its own short-run average "
            "cost curve: one, two, four, eight, sixteen slipways. <bookmark mark='b'/> In the long run Crusoe can "
            "pick the best number for each output, so the long-run average cost is the lower envelope of all the "
            "short-run curves. Each short-run curve touches it at exactly one output, the one for which that many "
            "slipways is right. <bookmark mark='c'/> Here the envelope slopes up, because of decreasing returns. With "
            "constant returns it would be flat; with increasing returns, falling. <bookmark mark='d'/> The short run "
            "is what you have; the long run is what you can choose."
        ) as vo:
            self.play(FadeIn(ax))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s_) for s_ in srs], lag_ratio=0.3), FadeIn(labs), FadeIn(side[0]),
                      run_time=3)
            vo.wait_until("b")
            self.play(Create(lr), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
