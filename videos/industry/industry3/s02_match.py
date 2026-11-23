from __future__ import annotations

from videos.industry.industry3.common import *  # noqa: F403

ROWS = [("op_margin", "Operating profit per $ of sales", lambda v: f"{100 * v:.0f}¢"),
        ("turnover", "Sales per $ of assets", lambda v: f"${v:.2f}"),
        ("leverage", "Assets per $ of owners' money", lambda v: f"${v:.1f}"),
        ("rd_sales", "Research per $ of sales", lambda v: f"{100 * v:.0f}¢"),
        ("capex_sales", "New equipment per $ of sales", lambda v: f"{100 * v:.0f}¢")]


def table(reveal: bool = False) -> VGroup:
    cards = R["cards"]
    col_w, row_h, x0, y0 = 1.55, 0.62, -1.75, 1.55
    g = VGroup()
    heads = VGroup()
    for i, c in enumerate(cards):
        x = x0 + i * col_w
        lab = TB(c["letter"], 30, I.ACCENT).move_to(np.array([x, y0 + 0.75, 0]))
        if reveal:
            nm = T(name(c["key"]), 15, CO[c["key"]]).move_to(np.array([x, y0 + 0.33, 0]))
            if nm.width > col_w - 0.1:
                nm.scale_to_fit_width(col_w - 0.1)
            lab = VGroup(lab, nm)
        heads.add(lab)
    g.add(heads)
    body = VGroup()
    for r, (key, label, fmt) in enumerate(ROWS):
        y = y0 - 0.25 - r * row_h
        row = VGroup(T(label, 17, I.TEXT).move_to(np.array([x0 - 0.7, y, 0]), aligned_edge=RIGHT))
        for i, c in enumerate(cards):
            row.add(TB(fmt(c[key]), 22, I.TEXT).move_to(np.array([x0 + i * col_w, y, 0])))
        body.add(row)
    g.add(body)
    rules = VGroup(*[Line(np.array([x0 - 4.9, y0 - 0.25 - r * row_h - row_h / 2, 0]),
                          np.array([x0 + 5.5 * col_w, y0 - 0.25 - r * row_h - row_h / 2, 0]), color=I.EDGE,
                          stroke_width=1) for r in range(len(ROWS) - 1)])
    g.add(rules)
    return g


class Match(VoiceoverScene):
    def construct(self):
        card(self, 1, "Six companies, no names", "Can you tell a bank from an airline by its numbers alone?",
             "Chapter one. Six companies, no names.", lit=("dollar", "moat"))
        t = table()
        heads, body, rules = t
        names = VGroup(*[VGroup(Dot(radius=0.07, color=CO[k]), T(f"{name(k)}, {R['six'][k]['kind']}", 18, I.TEXT)
                                ).arrange(RIGHT, buff=0.12) for k in ("cost", "msft", "jpm", "nee", "dal", "lly")])
        names.arrange_in_grid(rows=2, cols=3, buff=(0.5, 0.18)).to_edge(DOWN, buff=0.75)
        head = T("Six real companies, latest annual accounts", 22, I.DIM).to_edge(UP, buff=0.3)
        src = source("Forms 10-K: Costco and Microsoft fiscal 2026, the others 2025; SEC EDGAR; for the bank, profit before "
                     "tax", corner=DR, size=13)
        C = R["cards"]
        with self.voiceover(
            "Start with a game. <bookmark mark='a'/> Here are six real American companies, with their names taken "
            "off. <bookmark mark='b'/> For each, five numbers from its latest accounts. How many cents of operating "
            "profit it keeps from each dollar of sales. <bookmark mark='c'/> How many dollars of sales it makes "
            "from each dollar of things it owns. <bookmark mark='d'/> How many dollars of things it owns for each "
            "dollar its owners put in: the rest is borrowed. <bookmark mark='e'/> And how much of each dollar of "
            "sales goes back into research, and into new buildings and equipment. <bookmark mark='f'/> The six are "
            "a warehouse grocer, Costco; a software company, Microsoft; a bank, JPMorgan Chase; a power company, "
            "NextEra Energy; an airline, Delta; and a drug maker, Eli Lilly. Match them. One clue: company "
            f"{C[1]['letter']} turns over its assets more than three times a year, and company {C[3]['letter']} "
            "owns twelve dollars of things for every dollar of its own. Keep your answers; they are revealed near "
            "the end of this part, by which time you will be able to say why."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h, shift=DOWN * 0.1) for h in heads], lag_ratio=0.12))
            for i, m in enumerate("bcd"):
                vo.wait_until(m)
                self.play(FadeIn(body[i]), *(Create(rules[i]) for _ in [0] if i < len(rules)))
            vo.wait_until("e")
            self.play(FadeIn(body[3]), Create(rules[3]))
            self.play(FadeIn(body[4]))
            vo.wait_until("f")
            self.play(LaggedStart(*[FadeIn(n) for n in names], lag_ratio=0.15), run_time=2)
        self.wait(1.5)
        self.clear_scene()
