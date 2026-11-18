from __future__ import annotations

from videos.economics.econ1.common import *  # noqa: F403

GREEN, RED, BLUE = "#4CAF6E", "#E5484D", "#8EC5FF"


def martian_view(seed: int = 1991) -> VGroup:
    """Simon's telescope view (schematic): firms as green areas with faint divisions, market transactions as red lines
    between them, lines of authority in pale blue inside them."""
    rng = np.random.default_rng(seed)
    firms = VGroup()
    centres = []
    for k in range(9):
        x, y = rng.uniform(-5.6, 5.6), rng.uniform(-2.3, 2.3)
        if any(np.hypot(x - a, y - b) < 2.1 for a, b in centres):
            continue
        centres.append((x, y))
        w, h = rng.uniform(1.4, 2.6), rng.uniform(1.0, 1.8)
        blob = Ellipse(width=w, height=h, stroke_color=GREEN, stroke_width=1.5, fill_color=GREEN, fill_opacity=0.55)
        blob.move_to([x, y, 0]).rotate(rng.uniform(0, PI))
        div = Line(blob.get_center() + LEFT * w * 0.3, blob.get_center() + RIGHT * w * 0.3, color="#2E7D4F",
                   stroke_width=1).rotate(rng.uniform(0, PI))
        boss = Dot(blob.get_center(), radius=0.04, color=BLUE)
        lines = VGroup(*[Line(boss.get_center(), blob.get_center() + np.array([np.cos(a) * w * 0.32,
                                                                                np.sin(a) * h * 0.32, 0]),
                              color=BLUE, stroke_width=1.2) for a in np.linspace(0, TAU, 5, endpoint=False)])
        firms.add(VGroup(blob, div, lines, boss))
    trades = VGroup()
    for i in range(len(centres)):
        for j in range(i + 1, len(centres)):
            if rng.uniform() < 0.32:
                a, b = firms[i][0], firms[j][0]
                trades.add(Line(a.get_center(), b.get_center(), color=RED, stroke_width=1.6).set_z_index(-1))
    g = VGroup(trades, firms)
    g.firms, g.trades = firms, trades
    return g


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Frontier: how much of the economy is a market?", r"If prices coordinate so well, \ why is "
             r"so much of the economy run by command?", "Chapter thirteen. Frontier: how much of the economy is a "
             "market?", lit={1937: r"Coase: why firms exist"}, scale=("firm", "market", "nation"),
             horizon=("a decade",))
        self.coase()
        self.martian()
        self.open_()

    # ------------------------------------------------------------------
    def coase(self):
        hc = history_card(1937, r"Ronald Coase, \ ``The Nature of the Firm''",
                          r"if the price system coordinates so well, \ why are there firms at all, \ inside which "
                          r"nobody uses prices?", color=E.FIRMS, width=8.6, font_size=26).to_edge(UP, buff=0.5)
        ans = VGroup(label(r"his answer: \ using the market has costs", font_size=30, color=WHITE),
                     label(r"finding a supplier, \ bargaining, \ writing and enforcing contracts", font_size=24,
                           color=GREY_A),
                     label(r"a firm grows until doing one more thing inside it \ costs as much as buying it",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22).next_to(hc, DOWN, buff=0.6)
        with self.voiceover(
            "Here's where the part's question stops being settled. <bookmark mark='a'/> In 1937 a young British "
            "economist, Ronald Coase, asked something nobody had asked properly. If the price system coordinates "
            "so well, why are there firms at all? Inside a firm, nobody uses prices. A worker moves from one "
            "department to another because a manager says so. <bookmark mark='b'/> His answer was that using the "
            "market has costs: finding a supplier, bargaining, writing a contract and enforcing it. "
            "<bookmark mark='c'/> So a firm grows until doing one more thing inside it costs as much as buying it "
            "outside. It took decades for economists to take this seriously, and it won Coase a Nobel prize in "
            "1991."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(ans[0]), FadeIn(ans[1]))
            vo.wait_until("c")
            self.play(FadeIn(ans[2]))
        self.clear_scene()

    def martian(self):
        s = tables.SIMON_1991.data
        view = martian_view().scale(0.86).move_to(DOWN * 0.55)
        head = label(r"Herbert Simon, 1991: \ a visitor from Mars, with a telescope", font_size=30,
                     color=GREY_A).to_edge(UP, buff=0.3)
        key = VGroup(VGroup(Square(0.22, stroke_width=0, fill_color=GREEN, fill_opacity=0.7),
                            label(r"firms", font_size=20, color=GREEN)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.3, color=RED, stroke_width=3),
                            label(r"market transactions", font_size=20, color=RED)).arrange(RIGHT, buff=0.1),
                     VGroup(Line(ORIGIN, RIGHT * 0.3, color=BLUE, stroke_width=3),
                            label(r"lines of authority", font_size=20, color=BLUE)).arrange(RIGHT, buff=0.1))
        key.arrange(RIGHT, buff=0.5).next_to(head, DOWN, buff=0.2)
        msg = VGroup(label(rf"``{s['message']}''", font_size=30, color=WHITE),
                     label(rf"not \ ``{s['not']}''", font_size=24, color=GREY_B)).arrange(DOWN, buff=0.12)
        msg.add_background_rectangle(color=BACKGROUND, opacity=0.85, buff=0.15).move_to(UP * 0.3)
        tag = note(r"schematic", font_size=18, color=GREY_B).to_corner(UR, buff=0.3)
        src = published_tag(tables.SIMON_1991.tag, corner=DL, font_size=16)
        with self.voiceover(
            "In 1991 Herbert Simon put the same question as a picture. <bookmark mark='a'/> A visitor from Mars "
            "approaches the Earth with a telescope that shows social structures. Firms show up as solid green "
            "areas, with faint lines marking out their divisions. <bookmark mark='b'/> Market transactions show as "
            "red lines between the firms. <bookmark mark='c'/> And inside the firms are pale blue lines: the lines "
            "of authority, from bosses to workers. <bookmark mark='d'/> Most people, Simon pointed out, work inside "
            "the green areas. So the message the visitor sends home would describe large green areas "
            "interconnected by red lines, not a network of red lines connecting green spots. On this view, we live "
            "in an organizational economy as much as a market one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(src), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f[0:2]) for f in view.firms], lag_ratio=0.15), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(t) for t in view.trades], lag_ratio=0.1), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(f[2:]) for f in view.firms], lag_ratio=0.1), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(msg, shift=UP * 0.1))
        self.clear_scene()

    def open_(self):
        items = [
            (r"where the line falls", r"what decides which transactions happen inside firms and which between them, "
             r"and why the line moves (Parts 8, 14, 62)", E.FIRMS),
            (r"markets built on purpose", r"platforms, clearinghouses and auctions are designed: \ markets that are "
             r"also organizations (Parts 17, 44, 61)", E.DEMAND),
            (r"Hayek's problem, again", r"if a firm or a computer could gather what millions know, would prices still "
             r"be needed? \ the old calculation debate, with new tools (Parts 9, 64, 65)", TIN),
        ]
        pc = point_cards(items, width=12.8, cols=3, font_size=22).move_to(UP * 0.3)
        head = heading(r"What is open")
        star = label(r"$\star$ \ research problem: \ measure how much of one country's economy runs through markets, "
                     r"and how much through firms; \ what data would you need?", font_size=22,
                     color=E.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So here is what's open. <bookmark mark='a'/> First, where the line between firm and market falls, and "
            "why it moves: why some companies make their own parts and others buy everything, and why that changes "
            "over time. <bookmark mark='b'/> Second, the markets that are now built on purpose: a ride-hailing "
            "platform, a kidney exchange, an advertising auction. They're markets and organizations at once, and "
            "economists design them. <bookmark mark='c'/> And third, Hayek's problem again. His argument was that "
            "no planner could gather what millions of people know. With enough data and enough computing, could a "
            "firm, or a government, do it after all? That was argued fiercely in the 1930s, and it's being argued "
            "again. <bookmark mark='d'/> The research problem at the end of this part asks you to measure, for one "
            "country, how much of its economy runs through markets and how much through organizations, and to "
            "work out what data you would need."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c in zip("abc", pc.cards):
                vo.wait_until(mark)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("d")
            self.play(FadeIn(star))
        self.clear_scene()
