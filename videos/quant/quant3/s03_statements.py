from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant3.common import CASH, DEBT, EQUITY, PART, VALUE, load

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


STEP_CODE = [
    "def step(firm, sales, cost_ratio=0.7, credit=0.2, dep_rate=0.05, ...):",
    "    collected = (1 - write_off) * firm.receivables",
    "    firm.receivables = credit * sales            # unpaid sales",
    "    firm.cash += (1 - credit) * sales + collected",
    "    dep = dep_rate * firm.plant",
    "    firm.plant += capex - dep",
    "    ni = sales - costs - dep - interest - lost - taxes",
    "    firm.cash -= costs + capex + interest + taxes + div",
    "    firm.equity += ni - div                       # clean surplus",
    "    assert abs(firm.assets() - firm.claims()) < 1e-9",
    "    cfo = ni + dep - d_receivables                # indirect method",
    "    return dict(net_income=ni, cfo=cfo, accruals=ni - cfo, ...)",
]


class Statements(VoiceoverScene):
    def construct(self):
        st = load("statements")
        self.card()
        self.ledgers()
        self.running(st)
        self.lab(st)
        self.identities(st)

    def card(self):
        c = chapter_card(3, r"The three statements, running", r"What did the firm earn, and where did the cash go?",
                         part=PART)
        with self.voiceover("Chapter three. The three statements, running."):
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
            "Every listed company publishes three statements. Here is a toy firm's year. <bookmark mark='a'/> The income "
            "statement: sales of a thousand, two hundred not yet paid by customers, seven hundred of cash costs, a hundred of "
            "depreciation as the machines wear. Net income, two hundred. <bookmark mark='b'/> The cash flow statement starts "
            "from net income, adds back depreciation, which used no cash, and subtracts the unpaid two hundred: operations brought "
            "in only a hundred. After a hundred and fifty of new machines and fifty of dividends, cash fell by a hundred. "
            "<bookmark mark='c'/> The balance sheet is two snapshots of what the firm owns and who has a claim on it. And the "
            "three are one set of books. <bookmark mark='d'/> The fall in cash is the change in the cash line. "
            "<bookmark mark='e'/> Profit less dividends is the rise in equity; receivables and plant move too. "
            "<bookmark mark='f'/> And both sides still balance: double-entry bookkeeping."
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

    def running(self, st):
        R = {k: np.asarray(v) for k, v in st["rows"].items()}
        n = len(R["sales"])
        q = ValueTracker(0)
        unit = 0.0021

        def stack(parts, x, title):
            g = VGroup()
            y = -2.2
            for v, col in parts:
                h = max(v * unit, 0.004)
                g.add(Rectangle(width=1.3, height=h, stroke_width=0, fill_color=col, fill_opacity=0.85)
                      .move_to([x, y + h / 2, 0]))
                y += h
            g.add(label(title, font_size=20, color=GREY_A).move_to([x, -2.55, 0]))
            return g

        def books():
            i = int(np.clip(round(q.get_value()), 0, n - 1))
            a = stack([(R["cash"][i], CF_C), (R["receivables"][i], QC.LOSS), (R["plant"][i], BS_C)], -5.2, r"assets")
            c = stack([(R["debt"][i], DEBT), (R["equity"][i], EQUITY)], -3.6, r"claims")
            ok = MathTex(rf"{R['assets'][i]:,.1f} = {R['debt'][i] + R['equity'][i]:,.1f}".replace(",", "{,}"),
                         font_size=26, color=QC.GAIN).move_to([-4.4, -3.05, 0])
            qt = label(rf"quarter {i + 1} of {n}", font_size=22, color=GREY_B).move_to([-4.4, 3.2, 0])
            return VGroup(a, c, ok, qt)

        bk = always_redraw(books)
        leg = legend([(CF_C, r"cash"), (QC.LOSS, r"receivables"), (BS_C, r"plant"), (DEBT, r"debt"),
                      (EQUITY, r"equity")], font_size=17).to_corner(UL, buff=0.35).shift(DOWN * 0.5)
        g = axes([1, n], [-40, 140], x_length=6.6, y_length=3.6, xlabel=r"quarter", ylabel=r"per quarter",
                 xticks=[1, 5, 10, 15, 20], yticks=[0, 50, 100], font_size=17).move_to(RIGHT * 2.9 + UP * 0.6)
        ax = g.ax
        tq = np.arange(1, n + 1)
        l_ni = tracing(ax, tq, R["net_income"], q, IS_C)
        l_cf = tracing(ax, tq, R["cfo"], q, CF_C)
        lg = legend([(IS_C, r"net income"), (CF_C, r"operating cash flow")], font_size=19).next_to(g, DOWN, buff=0.2)
        cum_gap = float(np.sum(R["accruals"]))
        note_ = wrapped_label(rf"over five years: earnings {R['net_income'].sum():,.0f}, cash from operations "
                              rf"{R['cfo'].sum():,.0f}; accruals {cum_gap:,.0f}".replace(",", "{,}"), 6.4, 21, GREY_A)
        note_.next_to(lg, DOWN, buff=0.2)
        with self.voiceover(
            "Now run the machine: the House's accounting simulator takes the toy firm through twenty quarters. Sales grow with "
            "noise; a fifth are on credit, collected next quarter, a few percent never; the firm pays costs, interest and tax, "
            "buys plant and pays out a quarter of its profit. <bookmark mark='a'/> On the left, the balance sheet: both columns "
            "move every quarter, and the totals stay equal to the cent, because every entry is posted twice. "
            "<bookmark mark='b'/> On the right, net income in gold and operating cash flow in green: close, never the same. The "
            "gap is the accruals."
        ) as vo:
            self.play(FadeIn(leg), FadeIn(g), FadeIn(lg))
            vo.wait_until("a")
            self.add(bk, l_ni, l_cf)
            self.play(q.animate.set_value(n - 1), run_time=12, rate_func=linear)
            vo.wait_until("b")
            self.play(FadeIn(note_))
        bk.clear_updaters()
        l_ni.clear_updaters()
        l_cf.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def lab(self, st):
        card = lab_card(r"one quarter of double-entry bookkeeping", STEP_CODE,
                        source="explainer/quant/house/fundamentals.py (excerpt)", width=7.4, font_size=16)
        card.to_edge(LEFT, buff=0.3).to_edge(UP, buff=0.3)
        L, H = st["lab"], st["credit_heavy"]
        pp = desk_question(r"Pause and predict: sales double, but nine-tenths are on credit. Does cash go up or "
                           r"down this quarter?", width=4.9, font_size=21).to_edge(RIGHT, buff=0.3).shift(UP * 1.6)
        ans = VGroup(MathTex(rf"\text{{net income}}\ {H['net_income']:+.0f}", font_size=30, color=IS_C),
                     MathTex(rf"\text{{operating cash flow}}\ {H['cfo']:+.0f}", font_size=30, color=QC.LOSS),
                     label(r"profitable, and running out of cash", font_size=22, color=GREY_A))
        ans.arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(pp, DOWN, buff=0.4)
        with self.voiceover(
            "Here is the House's code for one quarter, cut to the lines that matter: credit sales become receivables, "
            "depreciation moves plant into expense, earnings less payout go to equity, and an assertion stops the program if the "
            f"books ever fail to balance. <bookmark mark='a'/> On sales of {L['sales']:.0f}: net income {L['net_income']:.0f}, "
            f"operating cash flow {L['cfo']:.0f}. <bookmark mark='b'/> Pause and predict: sales double, nine tenths on credit. "
            f"Does cash go up or down? <bookmark mark='c'/> Down: profit {H['net_income']:.0f}, cash flow {H['cfo']:.0f}. "
            "Growth on credit eats cash."
        ) as vo:
            self.play(FadeIn(card, shift=UP * 0.2))
            vo.wait_until("a")
            lab_run(self, card, [f"step(Firm(), sales={L['sales']:.0f})",
                                 f"net income {L['net_income']:.1f}  cfo {L['cfo']:.1f}  accruals {L['accruals']:.1f}",
                                 f"assets {L['assets']:.1f} = claims {L['debt'] + L['equity']:.1f}   ok"])
            vo.wait_until("b")
            self.play(FadeIn(pp))
            vo.wait_until("c")
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    def identities(self, st):
        R = {k: np.asarray(v) for k, v in st["rows"].items()}
        ni = R["net_income"][-4:].sum()
        sales = R["sales"][-4:].sum()
        A = R["assets"][-1]
        E = R["equity"][-1]
        rows = [
            cmath(r"\Delta\text{Cash} + \Delta\text{AR} + \Delta\text{Plant}", r"=", r"\Delta\text{Debt} + \Delta E",
                  font_size=36),
            cmath(r"\Delta E = NI - \text{Div}", r",", r"\quad \Delta\text{Plant} = \text{Capex} - \text{Dep}",
                  font_size=36),
            cmath(r"\Delta\text{Cash}", r"=", r"\underbrace{NI + \text{Dep} - \Delta\text{AR}}_{\text{operating cash flow}}"
                  r" - \text{Capex} - \text{Div} + \Delta\text{Debt}", font_size=36),
            cmath(r"\frac{NI}{E}", r"=", r"\frac{NI}{S}\cdot\frac{S}{A}\cdot\frac{A}{E}", font_size=40),
            cmath(rf"{100 * ni / E:.1f}\%", r"=", rf"{100 * ni / sales:.1f}\% \times {sales / A:.2f} \times {A / E:.2f}",
                  font_size=36),
        ]
        whys = [why(r"take differences of assets $=$ claims, quarter to quarter"),
                why(r"clean surplus, and plant rolled forward"),
                why(r"substitute and solve for cash: the cash flow statement, by the indirect method"),
                why(r"multiply and divide: DuPont's split of return on equity into margin, turnover and leverage"),
                why(r"the toy firm's last four quarters")]
        step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.7, edge=6.9)
        with self.voiceover(
            "Two identities fall out. Difference the balance sheet from one quarter to the next. <bookmark mark='a'/> Equity "
            "moves by earnings less dividends; plant by spending less depreciation. <bookmark mark='b'/> Solve for cash, and you "
            "have derived the cash flow statement by the indirect method. <bookmark mark='c'/> And return on equity is margin "
            "times asset turnover times leverage, DuPont's split: does the firm earn by pricing, efficiency or borrowing? "
            "<bookmark mark='d'/> For the toy firm's last year: these three numbers."
            " Notice that the toy firm's earnings and its cash were not the same number. The gap has a name, and a price: accruals."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            step(4)
        self.wait(0.4)
        self.clear_scene()
