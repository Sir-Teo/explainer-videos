from __future__ import annotations

from videos.economics.econ30.common import *  # noqa: F403


class ZLB(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The zero lower bound and forward guidance", r"What can a central bank do when its rate is "
             r"already zero?", "Chapter twelve. The zero lower bound and forward guidance.",
             lit={2003: r"Eggertsson and Woodford", 2012: r"Del Negro, \ Giannoni and Patterson"},
             scale=("nation",), horizon=("a quarter", "three years"))
        self.trap()
        self.guidance()
        self.puzzle()

    def _axes(self, lo, hi):
        return plane([0, 11], [lo, hi], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.8, y_length=4.8,
                     xticks=[0, 2, 4, 6, 8, 10], yticks=[v for v in (-8, -4, 0, 4, 8, 12, 16) if lo <= v <= hi],
                     xlabel=r"quarters", ylabel=r"percent", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                     font_size=15)

    def trap(self):
        Z = load("zlb")
        p = Z["paths"]["0"]
        q = np.array(p["q"])
        ax = self._axes(-9, 5)
        zero = seg(ax, 0, 0, 11, 0, GREY_D, 1.5)
        shock = Rectangle(width=ax.ax.c2p(Z["T"], 0)[0] - ax.ax.c2p(0, 0)[0], height=4.8, fill_color=COST,
                          fill_opacity=0.10, stroke_width=0).move_to(ax.ax.c2p(Z["T"] / 2, -2))
        x = path(ax, q, p["x"], OUTPUT, 3.5, smooth=False)
        pi = path(ax, q, p["pi"], INFL, 3.5, smooth=False)
        i = path(ax, q, p["i"], RATE, 2.5, smooth=False)
        side = VGroup(
            label(rf"the natural rate falls to {Z['rn_low']:.0f}\% \\ for {Z['T']} quarters \ (shaded)", font_size=19,
                  color=COST),
            label(r"pink: \ the policy rate, \ stuck at zero", font_size=19, color=RATE),
            label(rf"green: \ output gap, \ {p['x'][0]:.1f}\%", font_size=19, color=OUTPUT),
            label(rf"red: \ inflation, \ {p['pi'][0]:.1f}\% a year", font_size=19, color=INFL),
            label(r"falling prices raise the real rate, \\ which deepens the slump", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Eggertsson and Woodford, \ \emph{Brookings Papers} (2003:1); \ the Island", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Suppose fear grips the Island and the natural rate of interest falls to minus two percent for six "
            "quarters. <bookmark mark='a'/> The central bank should cut its rate below zero, but it cannot: people "
            "would hold cash instead. <bookmark mark='b'/> Its rate sits at zero. <bookmark mark='c'/> Output "
            f"falls {abs(p['x'][0]):.1f} percent below its natural level, <bookmark mark='d'/> and prices fall at "
            f"{abs(p['pi'][0]):.1f} percent a year. <bookmark mark='e'/> Falling prices make the real interest rate "
            "higher, which deepens the slump: the liquidity trap of Part twenty-seven, now with expectations. "
            "Gauti Eggertsson and Michael Woodford worked out this case in 2003, and the numbers in the model are "
            "far larger than anything seen in 2009, which is itself a puzzle."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(shock), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(i), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(x), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(Create(pi), FadeIn(side[3]), run_time=1.5)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def guidance(self):
        Z = load("zlb")
        ps = Z["paths"]
        ax = self._axes(-7, 17)
        zero = seg(ax, 0, 0, 11, 0, GREY_D, 1.5)
        cols = {"0": GREY_B, "1": CB, "2": OUTPUT, "3": E.ACCENT}
        lines = {k: path(ax, ps[k]["q"], np.clip(ps[k]["x"], -7, 17), cols[k], 3, smooth=False) for k in ps}
        x0, x1 = ax.ax.c2p(0, 0)[0], ax.ax.c2p(Z["T"], 0)[0]
        shock = Rectangle(width=x1 - x0, height=4.8, fill_color=COST, fill_opacity=0.10, stroke_width=0).move_to(
            ax.ax.c2p(Z["T"] / 2, 5))
        low = label(r"the natural rate is low", font_size=16, color=COST).move_to(ax.ax.c2p(Z["T"] / 2, 15.5))
        edge = DashedLine(ax.ax.c2p(Z["T"], -7), ax.ax.c2p(Z["T"], 17), color=CB, stroke_width=2)
        arrow = Arrow(ax.ax.c2p(Z["T"], 12), ax.ax.c2p(Z["T"] + 3, 12), color=CB, buff=0, stroke_width=4,
                      max_tip_length_to_length_ratio=0.2)
        promise = label(r"the promise: \\ zero for longer", font_size=16, color=CB).next_to(arrow, UP, buff=0.1)
        side = VGroup(
            label(r"forward guidance: \\ promise to keep the rate \\ at zero \emph{after} the shock", font_size=19,
                  color=CB),
            label(r"output gap on impact:", font_size=19, color=GREY_A),
            *[label(rf"{'no promise' if k == '0' else '+' + k + ' quarter' + ('s' if k != '1' else '')}: \ "
                    rf"{ps[k]['x'][0]:+.1f}\%", font_size=19, color=cols[k]) for k in ps],
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "What can a central bank do at zero? It can talk. <bookmark mark='a'/> Promise to keep the rate at "
            "zero for a while after the natural rate has recovered, <bookmark mark='p'/> when the economy would "
            "otherwise call for higher rates. That future stimulus raises expected output and inflation, and pulls "
            "the economy up today. <bookmark mark='b'/> In the model the effect is enormous. With no promise, output "
            f"is {abs(ps['0']['x'][0]):.1f} percent below normal. <bookmark mark='c'/> Promise one extra quarter at "
            f"zero, and the slump almost disappears: {say_num(ps['1']['x'][0], 1)} percent. "
            f"<bookmark mark='d'/> Two quarters, and it becomes a boom of {ps['2']['x'][0]:.1f} percent; "
            f"<bookmark mark='e'/> three, {ps['3']['x'][0]:.0f} percent. No central bank has ever seen a promise "
            "work like that."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(side[0]), FadeIn(shock), FadeIn(low),
                      run_time=0.6)
            vo.wait_until("a")
            self.play(Create(edge))
            vo.wait_until("p")
            self.play(GrowArrow(arrow), FadeIn(promise))
            vo.wait_until("b")
            self.play(FadeOut(arrow), FadeOut(promise), FadeOut(low), Create(lines["0"]), FadeIn(side[1]),
                      FadeIn(side[2]))
            for mk, k in zip("cde", ("1", "2", "3")):
                vo.wait_until(mk)
                self.play(Create(lines[k]), FadeIn(side[2 + int(k)]))
        self.clear_scene()

    def puzzle(self):
        Z = load("zlb")
        rows = Z["fg"]["rows"]
        hs = [r["h"] for r in rows]
        ax = plane([0, 13], [0, 11], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.8, y_length=4.8,
                   xticks=[0, 2, 4, 6, 8, 10, 12], yticks=[0, 2, 4, 6, 8, 10],
                   xlabel=r"how far ahead the cut is promised, \ quarters", ylabel=r"today's output gap, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=15)
        bars = VGroup()
        for r in rows:
            p0, p1 = ax.ax.c2p(r["h"] - 0.35, 0), ax.ax.c2p(r["h"] + 0.35, min(r["x0"], 11))
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], fill_color=CB, fill_opacity=0.85,
                               stroke_width=0).move_to((p0 + p1) / 2))
        last = rows[-1]
        side = VGroup(
            label(r"promise a one-point cut \\ for one quarter, \ $h$ quarters ahead", font_size=19, color=CB),
            label(rf"$h = 1$: \ output today \ {rows[0]['x0']:+.2f}\%", font_size=19, color=GREY_A),
            label(rf"$h = {last['h']}$: \ {last['x0']:+.1f}\%, \\ with inflation {last['pi0']:+.0f} points",
                  font_size=19, color=INFL),
            label(r"the further away the promise, \\ the bigger its effect today", font_size=19, color=HOLD),
            label(r"Del Negro, \ Giannoni and Patterson: \\ the forward guidance puzzle", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Del Negro, \ Giannoni and Patterson, \ FRBNY Staff Report 574 (2012); \ McKay, \ "
                            r"Nakamura and Steinsson, \ \emph{AER} 106(10) (2016); \ Gabaix, \ \emph{AER} 110(8) "
                            r"(2020)", corner=DR, font_size=12)
        with self.voiceover(
            "Too good to be true? <bookmark mark='a'/> Ask the model a cleaner question: promise to cut the rate by "
            "one point for one quarter, h quarters from now. <bookmark mark='b'/> A cut one quarter ahead raises "
            f"today's output by {rows[0]['x0']:.2f} percent. <bookmark mark='c'/> A cut promised three years ahead "
            f"raises it by {last['x0']:.0f} percent, with inflation up {last['pi0']:.0f} points: "
            "<bookmark mark='d'/> the further away the promise, the bigger its effect today, because every quarter "
            "in between passes the stimulus back. <bookmark mark='e'/> Marco Del Negro, Marc Giannoni and "
            "Christina Patterson called this the forward guidance puzzle. Real promises are not that powerful. The "
            "repairs give households reasons not to look so far ahead: borrowing limits and income risk, as "
            "Alisdair McKay, Emi Nakamura and Jón Steinsson showed, or limited attention to distant news, as Xavier "
            "Gabaix proposed."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.6)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars[1:]], lag_ratio=0.3), FadeIn(side[2]),
                      run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        del hs
        self.clear_scene()
