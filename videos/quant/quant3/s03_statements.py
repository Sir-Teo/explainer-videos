from __future__ import annotations

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import CASH, EQUITY, PART, VALUE

IS_C, CF_C, BS_C = VALUE, CASH, QC.IMPLIED

# A toy firm's year.  Start: cash 150, receivables 0, plant 500 | debt 200, equity 450.
# Sales 1000 (200 not yet collected), cash costs 700, depreciation 100: net income 200.
# Capital spending 150, dividends 50.  End: cash 50, receivables 200, plant 550 | debt 200, equity 600.
INCOME = [("sales", "1000"), ("cash costs", "-700"), ("depreciation", "-100"), ("net income", "200")]
CASHFLOW = [("net income", "200"), ("+ depreciation", "100"), ("- rise in receivables", "-200"),
            ("operating cash flow", "100"), ("capital spending", "-150"), ("dividends", "-50"),
            ("change in cash", "-100")]
BALANCE = [("cash", "150", "50"), ("receivables", "0", "200"), ("plant", "500", "550"), ("total assets", "650", "800"),
           ("debt", "200", "200"), ("equity", "450", "600"), ("total claims", "650", "800")]
TOTALS = {"net income", "operating cash flow", "change in cash", "total assets", "total claims"}


def ledger(title, rows, color, width, ncols=1, fs=19, heads=None):
    head = label(title, font_size=fs + 5, color=color)
    lines = VGroup()
    named = {}
    for r in rows:
        name, vals = r[0], r[1:]
        bold = name in TOTALS
        nm = label(rf"\textbf{{{name}}}" if bold else name, font_size=fs, color=WHITE if bold else GREY_A)
        nums = VGroup(*[MathTex(v.replace("-", "-\\,"), font_size=fs + 6, color=WHITE if bold else GREY_A) for v in vals])
        line = VGroup(nm, nums)
        lines.add(line)
        named[name] = line
    lines.arrange(DOWN, aligned_edge=LEFT, buff=0.17)
    head.next_to(lines, UP, buff=0.3).align_to(lines, LEFT)
    if heads:
        hd = VGroup(*[label(h, font_size=fs - 3, color=GREY_B) for h in heads])
    body = VGroup(head, lines)
    box = RoundedRectangle(width=width, height=body.height + 0.5, corner_radius=0.12, stroke_color=color,
                           stroke_width=2, fill_color=color, fill_opacity=0.05)
    box.move_to(body).align_to(head, UP).shift(UP * 0.2)
    left = box.get_left()[0] + 0.25
    for ln in lines:
        ln[0].set_x(left + ln[0].width / 2)
        for k, num in enumerate(ln[1][::-1]):
            num.set_x(box.get_right()[0] - 0.3 - k * 0.95 - num.width / 2)
    head.set_x(left + head.width / 2)
    g = VGroup(box, head, lines)
    if heads:
        for k, h in enumerate(hd[::-1]):
            h.move_to([box.get_right()[0] - 0.3 - k * 0.95 - 0.25, head.get_y(), 0])
        g.add(hd)
    for name in TOTALS:
        if name in named:
            ln = named[name]
            rule = Line([left, ln.get_top()[1] + 0.07, 0], [box.get_right()[0] - 0.25, ln.get_top()[1] + 0.07, 0],
                        stroke_width=1, color=GREY_C)
            g.add(rule)
    g.rows = named
    return g


class Statements(VoiceoverScene):
    def construct(self):
        self.card()
        self.ledgers()
        self.accruals()
        self.xbrl()

    def card(self):
        c = chapter_card(2, r"The three statements", r"What did the firm earn, and where did the cash go?", part=PART)
        with self.voiceover("Chapter two. The three statements."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def ledgers(self):
        inc = ledger(r"Income statement", INCOME, IS_C, 3.7)
        cf = ledger(r"Cash flow statement", CASHFLOW, CF_C, 4.5)
        bs = ledger(r"Balance sheet", BALANCE, BS_C, 4.6, heads=[r"start", r"end"])
        books = VGroup(inc, cf, bs).arrange(RIGHT, buff=0.22, aligned_edge=UP)
        books.scale_to_fit_width(13.4).move_to(UP * 0.35)
        top = label(r"one year of a toy firm", font_size=24, color=GREY_B).to_edge(UP, buff=0.3)
        sub = VGroup(label(r"a flow: over the year", font_size=18, color=GREY_B).next_to(inc, DOWN, buff=0.15),
                     label(r"a flow: over the year", font_size=18, color=GREY_B).next_to(cf, DOWN, buff=0.15),
                     label(r"two snapshots: a stock", font_size=18, color=GREY_B).next_to(bs, DOWN, buff=0.15))

        def hl(ledger_, name, color=YELLOW):
            return SurroundingRectangle(ledger_.rows[name], buff=0.06, color=color, stroke_width=2.5)

        def flow(a, b, color, run_time=1.6):
            path = ArcBetweenPoints(a.get_right() + RIGHT * 0.05, b.get_left() + LEFT * 0.05, angle=-PI / 5)
            trail = path.copy().set_stroke(color, width=3, opacity=0.8)
            dot = Dot(radius=0.09, color=color).move_to(path.get_start())
            self.play(Create(trail), MoveAlongPath(dot, path), run_time=run_time)
            return VGroup(trail, dot)

        identity = MathTex(r"\text{assets}", r"=", r"\text{debt}", r"+", r"\text{equity}", r"\qquad 800 = 200 + 600",
                           font_size=34).to_edge(DOWN, buff=0.35)
        identity[0].set_color(BS_C)
        identity[4].set_color(EQUITY)
        with self.voiceover(
            "Every listed company publishes three statements. Here is a toy firm's year. "
            "<bookmark mark='a'/> The income statement says what it earned. It sold a thousand dollars of goods, "
            "though two hundred of that has not yet been paid by its customers. It spent seven hundred in cash on "
            "costs, and its machines wore out by a hundred, which the accountants charge as depreciation. Net "
            "income: two hundred. <bookmark mark='b'/> The cash flow statement says where the cash went. It starts "
            "from net income, adds back the depreciation, because no cash left the building for it, and subtracts "
            "the two hundred the customers still owe. The operations brought in only a hundred in cash. Then the "
            "firm spent a hundred and fifty on new machines and paid fifty in dividends. Cash fell by a hundred. "
            "<bookmark mark='c'/> The balance sheet is two snapshots: what the firm owns, and who has a claim on "
            "it, at the start of the year and at the end. And the three are one set of books. <bookmark mark='d'/> "
            "The fall in cash from the second statement is the change in the cash line. <bookmark mark='e'/> The "
            "profit from the first, less the dividends, is the rise in the owners' equity. The receivables grew by "
            "the unpaid sales, the plant by the new machines less the wear. <bookmark mark='f'/> And both sides "
            "still balance: everything the firm owns is claimed by its lenders or its owners. That identity is "
            "double-entry bookkeeping, written down in Venice by Luca Pacioli in 1494."
        ) as vo:
            self.play(FadeIn(top))
            vo.wait_until("a")
            self.play(FadeIn(inc), FadeIn(sub[0]))
            self.play(Create(hl(inc, "net income")))
            vo.wait_until("b")
            ni_flow = flow(inc.rows["net income"], cf.rows["net income"], IS_C)
            self.play(FadeIn(cf), FadeIn(sub[1]))
            vo.wait_until("c")
            self.play(FadeIn(bs), FadeIn(sub[2]))
            vo.wait_until("d")
            c_flow = flow(cf.rows["change in cash"], bs.rows["cash"], CF_C)
            self.play(Create(hl(bs, "cash", CF_C)))
            vo.wait_until("e")
            low = sub[1].get_bottom()[1] - 0.15
            gap = (cf[0].get_right()[0] + bs[0].get_left()[0]) / 2
            ni, eqr = inc.rows["net income"], bs.rows["equity"]
            path = VMobject().set_points_as_corners([
                [inc[0].get_right()[0] - 0.3, ni.get_bottom()[1] - 0.05, 0], [inc[0].get_right()[0] - 0.3, low, 0],
                [gap, low, 0], [gap, eqr.get_y(), 0],
                eqr.get_left() + LEFT * 0.02])
            trail = path.copy().set_stroke(IS_C, width=3, opacity=0.8)
            dot = Dot(radius=0.09, color=IS_C).move_to(path.get_start())
            self.play(Create(trail), MoveAlongPath(dot, path), run_time=2)
            self.play(Create(hl(bs, "equity", IS_C)), Create(hl(bs, "receivables", GREY_B)),
                      Create(hl(bs, "plant", GREY_B)))
            vo.wait_until("f")
            self.play(FadeOut(sub), FadeIn(identity))
            self.play(Indicate(bs.rows["total assets"]), Indicate(bs.rows["total claims"]))
        self.wait(0.4)
        self.clear_scene()

    def accruals(self):
        eq = cmath(r"\text{earnings}", r"=", r"\text{cash flow}", r"+", r"\text{accruals}", font_size=46,
                   colors={r"\text{earnings}": IS_C, r"\text{cash flow}": CF_C, r"\text{accruals}": QC.LOSS})
        nums = MathTex(r"200", r"=", r"100", r"+", r"100", font_size=46).next_to(eq, DOWN, buff=0.3)
        for k in range(5):
            nums[k].set_x(eq[k].get_x())
        VGroup(eq, nums).to_edge(UP, buff=0.9)
        judg = VGroup(
            label(r"accruals are judgments:", font_size=26, color=GREY_A),
            label(r"when a sale counts as made", font_size=24, color=GREY_A),
            label(r"how fast a machine wears out", font_size=24, color=GREY_A),
            label(r"what an unpaid bill is likely to fetch", font_size=24, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(nums, DOWN, buff=0.7).to_edge(LEFT, buff=1.2)
        sloan = wrapped_label(r"Sloan (1996): the accrual part of earnings persists less than the cash part, yet "
                              r"prices treated them alike; firms with high accruals then returned less", 5.6, 23,
                              QC.IDEA).next_to(nums, DOWN, buff=0.7).to_edge(RIGHT, buff=0.9)
        with self.voiceover(
            "So earnings and cash are different numbers. The difference has a name: accruals. Here earnings of two "
            "hundred are a hundred of cash plus a hundred of accruals, mostly the sales not yet collected. "
            "<bookmark mark='a'/> Accruals are where accounting needs judgment: when a sale counts as made, how fast "
            "a machine wears out, what an unpaid bill will really fetch. Cash is harder to bend. "
            "<bookmark mark='b'/> In 1996 Richard Sloan showed that the accrual part of earnings is less "
            "persistent than the cash part, that prices did not tell the two apart, and that the firms with the "
            "most accruals went on to return less. An accounting identity had become a trading signal. We will "
            "measure it in chapter eight."
        ) as vo:
            self.play(Write(eq), FadeIn(nums))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(j) for j in judg], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(sloan))
        self.wait(0.4)
        self.clear_scene()

    def xbrl(self):
        fact = VGroup(
            label(r"one fact in a filing", font_size=24, color=GREY_B),
            MathTex(r"\texttt{us-gaap:NetIncomeLoss}", font_size=34, color=IS_C),
            MathTex(r"\text{value } 200 \quad \text{unit USD} \quad \text{period: the fiscal year}", font_size=30),
            MathTex(r"\text{filed: the day the 10-K reached the SEC}", font_size=30, color=QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        box = SurroundingRectangle(fact, buff=0.35, color=GREY_C, corner_radius=0.12)
        card_ = VGroup(box, fact).to_edge(UP, buff=0.8)
        rules = VGroup(
            wrapped_label(r"Since 2009 the SEC has required filings tagged in XBRL, phased in from the largest firms "
                          r"to all by 2011: every number machine-readable, with its period and its filing date.",
                          9.4, 24, GREY_A),
            wrapped_label(r"An annual report can arrive 60 to 90 days after the year it describes; numbers are "
                          r"later restated.  A backtest may use a number only from the day it was filed.", 9.4, 24,
                          QC.HOUSE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(card_, DOWN, buff=0.6)
        with self.voiceover(
            "Analysts once typed these numbers in by hand. Since 2009 the Securities and Exchange Commission has "
            "required American companies to file them in a machine-readable language, XBRL, phased in from the "
            "largest firms to all of them by 2011. <bookmark mark='a'/> Each number is a tagged fact: what it is, "
            "the value, the unit, the period it covers, and the filing it came in. <bookmark mark='b'/> That last "
            "date is the one a quant cares about. A firm's year ends on the thirty-first of December, but its "
            "annual report can arrive two or three months later, and some numbers are restated years after that. "
            "A backtest that uses December's numbers in December has read the future. The House stores every "
            "number with the day it became public."
        ) as vo:
            self.play(Create(box), FadeIn(fact[0]), FadeIn(rules[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in fact[1:]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]), Indicate(fact[3], color=QC.HOUSE))
        self.wait(0.4)
        self.clear_scene()
