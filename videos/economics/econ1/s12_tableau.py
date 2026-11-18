from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403


def quesnay() -> VGroup:
    """Quesnay's zigzag (schematic): three columns, the money passing back and forth between them, halving each
    time."""
    heads = VGroup(label(r"farmers", font_size=22, color=E.HOUSEHOLDS), label(r"landlords", font_size=22,
                                                                             color=E.ACCENT),
                   label(r"artisans", font_size=22, color=E.FIRMS)).arrange(RIGHT, buff=1.5)
    g = VGroup(heads)
    xs = [h.get_x() for h in heads]
    y = heads.get_bottom()[1] - 0.35
    amounts = [1.0, 0.5, 0.25, 0.125, 0.0625]
    lines = VGroup()
    for k, a in enumerate(amounts):
        y0, y1 = y - 0.55 * k, y - 0.55 * (k + 1)
        left_to_right = k % 2 == 0
        a_ = Line([xs[0], y0, 0], [xs[2], y1, 0]) if left_to_right else Line([xs[2], y0, 0], [xs[0], y1, 0])
        a_.set_stroke(GREY_A, 1.5 + 3 * a)
        lines.add(a_)
    g.add(lines)
    g.lines = lines
    return g


def phillips() -> VGroup:
    """Phillips's machine (schematic): tanks of water joined by pipes; the flow is income, the levels are money."""
    tanks = VGroup()
    specs = [(0, 1.0, r"income"), (-1.2, -0.4, r"saving"), (1.2, -0.4, r"taxes"), (0, -1.6, r"spending")]
    for x, y, name in specs:
        t = VGroup(Rectangle(width=1.2, height=0.7, stroke_color="#7EC8F5", stroke_width=2),
                   Rectangle(width=1.16, height=0.3, stroke_width=0, fill_color="#3A78B8", fill_opacity=0.8))
        t[1].move_to(t[0].get_bottom() + UP * 0.17)
        lab = label(name, font_size=18, color=GREY_A).next_to(t, LEFT if x < 0 else RIGHT, buff=0.1)
        tanks.add(VGroup(t, lab).move_to([x, y, 0]))
    pipes = VGroup(*[Line(tanks[0][0].get_bottom(), tanks[k][0].get_top(), color="#3A78B8", stroke_width=4)
                     for k in (1, 2)], Line(tanks[1][0].get_bottom(), tanks[3][0].get_top(), color="#3A78B8",
                                             stroke_width=4),
                     Line(tanks[2][0].get_bottom(), tanks[3][0].get_top(), color="#3A78B8", stroke_width=4))
    back = CurvedArrow(tanks[3][0].get_right() + RIGHT * 0.1, tanks[0][0].get_right() + RIGHT * 0.1, angle=PI / 1.6,
                       color="#3A78B8", stroke_width=3)
    return VGroup(pipes, tanks, back)


class Tableau(VoiceoverScene):
    def construct(self):
        card(self, 10, r"The economy as plumbing", r"How do the parts of an economy connect?",
             "Chapter ten. The economy as plumbing.", lit={1758: r"Quesnay's \emph{Tableau}", 1949: r"Phillips's "
                                                                                                    r"machine"},
             scale=("nation",), horizon=("a year",))
        self.history()
        self.ours()
        self.map()

    # ------------------------------------------------------------------
    def history(self):
        qc = history_card(1758, r"Fran\c{c}ois Quesnay, \ physician to Louis XV", r"the \emph{Tableau "
                          r"\'economique}: \ the economy as a circulation, like the blood", color=E.ACCENT, width=6.0,
                          font_size=22)
        pc = history_card(1949, r"Bill Phillips, \ a student at the London School of Economics",
                          r"a machine of tanks and pipes, \ water for money; \ about a dozen were built",
                          color="#7EC8F5", width=6.0, font_size=22)
        VGroup(qc, pc).arrange(RIGHT, buff=0.5, aligned_edge=UP).to_edge(UP, buff=0.35)
        z = quesnay().scale(0.85).next_to(qc, DOWN, buff=0.45)
        m = phillips().scale(0.8).next_to(pc, DOWN, buff=0.45)
        tag = note(r"both drawn schematically", font_size=18, color=GREY_B).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Markets don't stand alone. What a household earns in one market it spends in another, and the money "
            "goes round. <bookmark mark='a'/> In 1758 François Quesnay, a physician at the court of Louis the "
            "Fifteenth, drew the French economy as a circulation, like the blood. In his zigzag table, the money "
            "spent by each class of society becomes the income of another, and is spent again. "
            "<bookmark mark='b'/> In 1949 Bill Phillips, a New Zealand engineer who had become a student of "
            "economics at the London School of Economics, built the same idea out of plastic tanks and pipes. "
            "Water stood for money. It flowed from income into spending, leaked into saving and taxes, and came "
            "back as investment and government spending. About a dozen of these machines were built, and they "
            "were used to teach economics for years."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(qc, shift=UP * 0.2), FadeIn(tag))
            self.play(FadeIn(z.submobjects[0]), LaggedStart(*[Create(x) for x in z.lines], lag_ratio=0.5),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(pc, shift=UP * 0.2))
            self.play(FadeIn(m, lag_ratio=0.2), run_time=2.5)
        self.clear_scene()

    def ours(self):
        t = tableau_map()
        head = label(r"The Tableau: \ the series map, \ sealed", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.12)
        t.scale(0.92).next_to(head, DOWN, buff=0.2)
        order = sorted(PIPES, key=lambda p: p[4])
        with self.voiceover(
            "This series has its own version, and it is the map of the course. <bookmark mark='a'/> Five tanks: "
            "households, firms, banks, the government, and the rest of the world. <bookmark mark='b'/> Ten pipes "
            "between them: spending and goods, labour, saving and loans, money, taxes and public spending, trade "
            "and the flows of capital. <bookmark mark='c'/> Today every pipe is sealed, and each is labelled with the "
            "part that opens it. Part two opens the first two, the market for goods. Money opens in Part "
            "twenty-five, the banks in twenty-six, the treasury in thirty-two, trade in thirty-five. "
            "<bookmark mark='d'/> By the end, most pipes will be flowing. What is still sealed will be the list of "
            "open problems."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(s, scale=0.9) for s in t.tanks], lag_ratio=0.25), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in t.pipes], lag_ratio=0.15), run_time=3)
            vo.wait_until("c")
            for key, *_ in order[:2]:
                self.play(Indicate(t.pipe[key].label, color=E.ACCENT, scale_factor=1.15), run_time=0.8)
            vo.wait_until("d")
            flows = VGroup(*[flowing(t.paths[k], GREY_B, n=3, period=4.0, radius=0.04) for k in ("spending", "goods")])
            self.add(flows)
            self.wait(2.0)
        for f in flows:
            f.clear_updaters()
        self.clear_scene()

    def map(self):
        m = series_map(current=PART, font_size=19, height=7.6)
        with self.voiceover(
            "And here is the whole course: sixty-eight parts in twelve acts. <bookmark mark='a'/> Act one asks the "
            "question and sets up the tools: prices, measurement, evidence. Acts two to four are microeconomics: "
            "choice, markets, games, and markets that fail and are designed. <bookmark mark='b'/> Acts five and "
            "six are the long run and the short: growth, money, banks, the business cycle and crises. "
            "<bookmark mark='c'/> Then the world economy, work and the state, and the fields of economics, ending "
            "with the degree's capstone in Part fifty. <bookmark mark='d'/> Then the graduate core, economics at "
            "work, and the research frontier, ending with a dissertation in Part sixty-eight."
        ) as vo:
            self.play(FadeIn(m, lag_ratio=0.01), run_time=2)
            for mark, idx in zip("abcd", ((0, 1, 2, 3), (4, 5), (6, 7, 8), (9, 10, 11))):
                vo.wait_until(mark)
                self.play(*[Indicate(m.acts[i].head, color=E.ACCENT, scale_factor=1.12) for i in idx], run_time=1.2)
        self.clear_scene()
