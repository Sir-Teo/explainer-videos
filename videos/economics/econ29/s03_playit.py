from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403

LETTERS = "ABCDEF"
# the order the panels are shown in: a fixed shuffle, so the leader is not first
SHOW = ("GDPC1", "HOANBS", "A011RA3Q086SBEA", "PCECC96", "OPHNFB", "A008RA3Q086SBEA")


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 2, r"Play it: \ which one turns first?", r"Six series around a recession. \ Which one leads?",
             "Chapter two. Play it: which one turns first?", lit={2007: r"Leamer"}, scale=("nation",),
             horizon=("a quarter", "two years"))
        self.choose()
        self.reveal()
        self.lesson()

    def _panels(self, labelled: bool):
        P = load("play")
        q = np.array(P["q"])
        S = P["series"]
        grid = VGroup()
        for n, key in enumerate(SHOW):
            s = S[key]
            avg = np.array(s["avg"])
            lo = min(-12.0, np.floor(avg.min() / 4) * 4)
            hi = max(4.0, np.ceil(avg.max() / 4) * 4)
            ax = plane([-8, 8], [lo, hi], x_length=3.6, y_length=1.9, xticks=[-8, 0, 8],
                       yticks=[lo, 0, hi], xfmt=lambda v: f"{v:+.0f}" if v else "0",
                       yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=13)
            zero = seg(ax, -8, 0, 8, 0, GREY_D, 1.2)
            peak = DashedLine(ax.ax.c2p(0, lo), ax.ax.c2p(0, hi), color=GREY_C, stroke_width=1.5)
            col = SERIES_COLORS[key] if labelled else GREY_A
            line = path(ax, q, avg, col, 3, smooth=False)
            name = label(rf"{LETTERS[n]}: \ {s['name']}" if labelled else LETTERS[n], font_size=19,
                         color=col).next_to(ax, UP, buff=0.08)
            grid.add(VGroup(ax, zero, peak, line, name))
        grid.arrange_in_grid(rows=2, cols=3, buff=(0.55, 0.55)).move_to(DOWN * 0.15)
        return grid

    def choose(self):
        P = load("play")
        grid = self._panels(False)
        note_ = label(r"average of the 10 recessions from 1953 to 2007; \ quarters from the NBER's peak (dashed); "
                      r"\ \% from each series' own trend growth, \ 0 at the peak", font_size=16,
                      color=GREY_B).to_edge(UP, buff=0.25)
        ring = countdown().scale(0.6).to_corner(DR, buff=0.4)
        tag = data_tag(r"BEA and BLS, \ via FRED", corner=DL, font_size=12)
        del P
        with self.voiceover(
            "Your turn. Here are six American series around the peak of a business cycle, the quarter the NBER says "
            "the expansion ended, marked by the dashed line. <bookmark mark='a'/> Each is the average over the ten "
            "recessions from 1953 to 2007, measured as a percentage from where the series stood at the peak, with "
            "its normal growth taken out. <bookmark mark='b'/> They include real output, consumer spending, "
            "business investment, housing investment, hours worked and output per hour, in some order. "
            "<bookmark mark='c'/> Which one turns down first, well before the recession begins? Pause, and choose a "
            "letter."
        ) as vo:
            self.play(FadeIn(note_), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in grid], lag_ratio=0.25), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        P = load("play")
        S = P["series"]
        grid = self._panels(True)
        lead = S["A011RA3Q086SBEA"]
        k = SHOW.index("A011RA3Q086SBEA")
        box = SurroundingRectangle(grid[k], color=HOUSING, buff=0.08, stroke_width=3)
        note_ = label(rf"{LETTERS[k]}: \ housing investment peaks about {-lead['peak_q']} quarters before the peak, "
                      rf"\ and is {abs(lead['drop']):.0f}\% below that a year after it", font_size=20,
                      color=HOUSING).to_edge(UP, buff=0.25)
        tag = data_tag(r"BEA and BLS, \ via FRED", corner=DL, font_size=12)
        order = [S[k_]["name"] for k_ in P["order"]]
        del order
        with self.voiceover(
            f"<bookmark mark='a'/> The answer is {LETTERS[k]}: housing investment. On average it reached its high "
            f"about {-lead['peak_q']} quarters before the peak of the cycle, and fell "
            f"{abs(lead['drop']):.0f} percent below that high within a year after it. <bookmark mark='b'/> Output, "
            "hours and business investment turn together, about two quarters before the peak, and business "
            "investment then falls furthest and longest. <bookmark mark='c'/> Consumer spending flattens a little "
            "earlier. "
            "<bookmark mark='d'/> And output per hour does something interesting: it stalls well before the peak, "
            "dips as the recession starts, and then recovers while hours are still falling."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(box), FadeIn(note_))
            vo.wait_until("b")
            self.play(*[Indicate(grid[SHOW.index(x)][3], color=WHITE, scale_factor=1.0)
                        for x in ("GDPC1", "HOANBS", "A008RA3Q086SBEA")])
            vo.wait_until("c")
            self.play(Indicate(grid[SHOW.index("PCECC96")][3], color=WHITE, scale_factor=1.0))
            vo.wait_until("d")
            self.play(Indicate(grid[SHOW.index("OPHNFB")][3], color=WHITE, scale_factor=1.0))
        self.clear_scene()

    def lesson(self):
        rows = VGroup(
            label(r"Leamer, \ 2007: \ ``Housing \emph{is} the business cycle''", font_size=27, color=HOUSING),
            label(r"housing is the spending most sensitive to interest rates, \ and to credit", font_size=23,
                  color=GREY_A),
            label(r"it turns first because monetary policy and credit conditions turn first", font_size=23,
                  color=GREY_A),
            label(r"a model driven only by technology has no reason for houses to lead", font_size=23,
                  color=TECH),
            label(r"keep this clue: \ it comes back in chapter eleven, \ and in Parts 30 and 31", font_size=23,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Leamer, \ ``Housing IS the Business Cycle'', \ Jackson Hole Symposium (2007); \ NBER "
                            r"WP 13428", corner=DR, font_size=12)
        with self.voiceover(
            "In 2007, at the Federal Reserve's Jackson Hole symposium, Edward Leamer gave a paper with the title "
            "Housing Is the Business Cycle. <bookmark mark='a'/> Housing is the kind of spending most sensitive to "
            "interest rates and to credit. <bookmark mark='b'/> It turns first because monetary policy and credit "
            "conditions turn first. <bookmark mark='c'/> Keep that in mind, because the model this part builds is "
            "driven by technology alone, and in a world driven only by technology there is no reason for houses to "
            "lead. <bookmark mark='d'/> It is a clue, and it comes back in chapter eleven, and in the next two parts."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
