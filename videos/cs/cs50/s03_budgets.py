from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace

RULE_NAMES = {
    "error rate > 0.1% over 10 minutes": r"errors $>$ 0.1\% over 10 min",
    "error rate > 0.1% over 36 hours": r"errors $>$ 0.1\% over 36 h",
    "burn > 14.4 over 1 hour": r"burn $>$ 14.4 over 1 h",
    "multiple burn rates": r"multiple burn rates",
    "multiwindow, multi-burn-rate": r"multiwindow, \ multi-burn-rate",
}


def mins(m: float) -> str:
    return rf"{m:.0f} min" if m < 120 else rf"{m / 60:.1f} h"


def defn(title, body, col, w=4.0, h=2.2):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.12, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.35, font_size=20, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.15).move_to(frame)
    return VGroup(frame, t, b)


class Budgets(VoiceoverScene):
    def construct(self):
        self.card()
        self.terms()
        self.budget()
        self.burn()
        self.rules()

    def card(self):
        card = chapter_card(2, r"SLOs and error budgets", r"How unreliable may we be, \ and when should someone wake?",
                            lit=(2016, 2018), extra=((2016, r"Beyer et al.: \ \textit{Site Reliability Engineering}"),
                                                     (2018, r"\textit{The Site Reliability Workbook}")), part=PART)
        with self.voiceover("Chapter two. Objectives, and the budget for failing to meet them."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def terms(self):
        s = load("slo")
        sli = 1 - s["budget"]["final"] * (1 - s["slo"])
        head = label(r"Indicator, \ objective, \ agreement", font_size=36).to_edge(UP, buff=0.3)
        boxes = VGroup(
            defn(r"SLI: \ indicator", r"a measured ratio: \ good events over valid events, \ such as requests "
                 r"answered correctly within 300 ms", DATA),
            defn(r"SLO: \ objective", rf"a target for the SLI over a window: \ {100 * s['slo']:.1f}\% over 30 days; "
                 r"\ an engineering choice", HEAD),
            defn(r"SLA: \ agreement", r"a contract with customers, \ with refunds when it is broken; \ set looser "
                 r"than the SLO", NO),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.4)
        line = NumberLine(x_range=[99.0, 100.0, 0.1], length=11.0, color=GREY_C, include_numbers=False,
                          tick_size=0.06).move_to(DOWN * 1.2)
        nums = VGroup(*[label(rf"{v:.1f}\%", font_size=16, color=GREY_B).next_to(line.n2p(v), DOWN, buff=0.15)
                        for v in (99.0, 99.2, 99.4, 99.6, 99.8, 100.0)])

        def mark(v, txt, col, up=True):
            tick = Line(line.n2p(v) + DOWN * 0.2, line.n2p(v) + UP * 0.2, color=col, stroke_width=4)
            t = label(txt, font_size=18, color=col)
            t.next_to(tick, UP if up else DOWN, buff=0.12 if up else 0.5)
            return VGroup(tick, t)
        m_sla = mark(99.5, r"SLA 99.5\% \ (illustrative)", NO)
        m_slo = mark(100 * s["slo"], r"SLO", HEAD)
        dot = Dot(line.n2p(99.0), radius=0.11, color=YES)
        m_sli = label(rf"this month's SLI: \ {100 * sli:.3f}\%", font_size=18, color=YES).next_to(
            line.n2p(100 * sli), DOWN, buff=0.55).align_to(line, RIGHT)
        foot = wrapped_label(r"between the SLO and perfection lies the room to change things", 12.0, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Reliability needs three words. <bookmark mark='a'/> An indicator, the SLI, is something measured: of the "
            "valid requests, the fraction that were good, say answered correctly within three hundred milliseconds. "
            "<bookmark mark='b'/> An objective, the SLO, is the target for that indicator over a window: here "
            "ninety-nine point nine percent over thirty days. It is an engineering choice, and it should be what users "
            "actually notice. <bookmark mark='c'/> An agreement, the SLA, is a contract with consequences, refunds "
            "when it is broken, and so it is set looser than the objective. <bookmark mark='d'/> In our synthetic "
            "month the indicator came in at ninety-nine point nine four five percent. It met the objective, and the "
            "gap between the objective and perfection is not waste. It is room to change things."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(nums))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]))
            vo.wait_until("b")
            self.play(FadeIn(boxes[1]), FadeIn(m_slo))
            vo.wait_until("c")
            self.play(FadeIn(boxes[2]), FadeIn(m_sla))
            vo.wait_until("d")
            self.play(FadeIn(dot))
            self.play(dot.animate.move_to(line.n2p(100 * sli)), FadeIn(m_sli), run_time=1.5)
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def budget(self):
        s = load("slo")
        used = s["budget"]["used_hourly"]
        per = s["budget"]["per_incident"]
        inc = {i["name"]: i for i in s["incidents"]}
        month_min = load("nines")["rows"][2]["per_month_min"]
        head = label(r"The error budget, \ draining", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 30, 5], [0, 1, 0.25], x_length=8.6, y_length=4.1, x_label=r"day of the month",
                 xticks=range(0, 31, 5), yticks=(0, 0.25, 0.5, 0.75, 1.0), fy=lambda v: rf"{100 * v:.0f}\%")
        g.next_to(head, DOWN, buff=0.5).to_edge(LEFT, buff=0.9)
        ax = g.ax
        ylab = label(r"share of the month's budget spent", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.12)
        ylab.align_to(ax, LEFT)
        T = ValueTracker(0)
        pts = [(h / 24, u) for h, u in enumerate(used)]
        curve = always_redraw(lambda: trace(ax, pts[:max(2, int(T.get_value()) + 1)], HEAD, width=3))
        H, TW = 4.1, 0.9
        tank = Rectangle(width=TW, height=H, stroke_color=GREY_B, stroke_width=2).move_to(
            [ax.get_right()[0] + 1.6, ax.get_center()[1], 0])
        fill = always_redraw(lambda: Rectangle(
            width=TW - 0.08, height=max(0.01, (H - 0.08) * (1 - used[min(len(used) - 1, int(T.get_value()))])),
            stroke_width=0, fill_color=YES, fill_opacity=0.8).align_to(tank, DOWN).shift(UP * 0.04).set_x(
            tank.get_x()))
        tank_l = label(r"left", font_size=18, color=YES).next_to(tank, UP, buff=0.12)
        tags, stops = VGroup(), []
        for name, txt, where in (("outage", r"outage: \ 25 min at 25\%", (4.5, 0.45)),
                                 ("degradation", r"degradation: \ 6 h at 1.2\%", (11.5, 0.65)),
                                 ("slow leak", r"slow leak: \ 3 days at 0.2\%", (22.5, 0.8))):
            i = inc[name]
            d = (i["start_min"] + i["minutes"] / 2) / 1440
            h_end = min(len(used) - 1, (i["start_min"] + i["minutes"]) // 60 + 1)
            stops.append(h_end)
            t = VGroup(label(txt, font_size=16, color=GREY_A),
                       label(rf"{100 * per[name]:.1f}\% of the budget", font_size=16, color=NO)).arrange(
                DOWN, buff=0.05).move_to(ax.c2p(*where))
            ptr = Line(t.get_bottom() + DOWN * 0.05, ax.c2p(d, used[min(len(used) - 1, int(d * 24) + 1)]) + UP * 0.08,
                       color=GREY_C, stroke_width=1.5)
            tags.add(VGroup(t, ptr))
        final = s["budget"]["final"]
        blips = sum(per[n] for n in ("blip", "second blip", "third blip"))
        bg = final - sum(per.values())
        summary = wrapped_label(rf"spent: \ {100 * final:.1f}\%; \ three blips {100 * blips:.1f}\%, \ background "
                                rf"errors {100 * bg:.1f}\%", 3.4, font_size=18, color=WHITE).next_to(
            tank, DOWN, buff=0.3)
        if summary.get_right()[0] > 6.8:
            summary.shift(LEFT * (summary.get_right()[0] - 6.8))
        defn_ = wrapped_label(rf"budget $= (1 - \text{{SLO}}) \times$ requests: \ one bad request in a thousand, \ "
                              rf"or {month_min:.1f} minutes of total outage a month", 4.0, font_size=18,
                              color=HEAD).move_to(ax.c2p(0.8, 0.93), aligned_edge=LEFT)
        foot = wrapped_label(r"while budget remains, \ ship; \ when it is spent, \ freeze risky launches and fix "
                             r"reliability \ (an error-budget policy)", 12.6, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "The objective turns into a resource. <bookmark mark='a'/> The error budget is the unreliability the "
            "objective allows: one bad request in a thousand, or the equivalent of forty-three minutes of total "
            "outage a month. <bookmark mark='b'/> Here is our synthetic month, spending it. Background errors trickle "
            "steadily. On day eight, a twenty-five minute outage at a quarter of requests takes fourteen and a half "
            "percent in one bite. On day fourteen a six-hour degradation takes ten percent. From day twenty a slow "
            "leak, only two errors in a thousand, quietly takes almost nineteen percent over three days. "
            "<bookmark mark='c'/> The month ends with fifty-five percent spent. <bookmark mark='d'/> The budget is "
            "the contract between the people who ship features and the people who carry the pager: while budget "
            "remains, ship; when it is gone, freeze risky launches and spend the effort on reliability."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(ylab), FadeIn(tank), FadeIn(tank_l))
            self.add(curve, fill)
            vo.wait_until("a")
            self.play(FadeIn(defn_))
            vo.wait_until("b")
            prev = 0
            for h, t in zip(stops, tags):
                self.play(T.animate.set_value(h), run_time=max(0.5, 14 * (h - prev) / len(used)), rate_func=linear)
                self.play(FadeIn(t), run_time=0.6)
                prev = h
            self.play(T.animate.set_value(len(used) - 1), run_time=max(0.5, 14 * (len(used) - 1 - prev) / len(used)),
                      rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(summary))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def burn(self):
        s = load("slo")
        th = s["thresholds"]
        head = label(r"Burn rate, \ and the thresholds it implies", font_size=36).to_edge(UP, buff=0.3)
        eq = MathTex(r"b = \frac{\text{error rate}}{1 - \text{SLO}}",
                     r"\qquad \text{budget lasts } \frac{30\text{ days}}{b}",
                     r"\qquad \text{page at } b = \frac{f \times 720\text{ h}}{w}", font_size=32)
        eq[0].set_color(HEAD)
        eq[1].set_color(DATA)
        eq[2].set_color(YES)
        eq.next_to(head, DOWN, buff=0.35)
        g = axes([0, 30, 10], [0, 1, 0.5], x_length=5.6, y_length=3.6, x_label=r"days",
                 xticks=(0, 10, 20, 30), yticks=(0, 0.5, 1.0), fy=lambda v: rf"{100 * v:.0f}\%")
        g.next_to(eq, DOWN, buff=0.5).to_edge(LEFT, buff=0.9)
        ax = g.ax
        rates = (1.0, 2.0, 6.0, th[0]["burn"])
        cols = (GREY_A, DATA, LAM, NO)
        fan, fan_l = VGroup(), VGroup()
        for b, col in zip(rates, cols):
            ln = Line(ax.c2p(0, 0), ax.c2p(30 / b, 1), color=col, stroke_width=3)
            fan.add(ln)
            fan_l.add(label(rf"$b = {b:g}$", font_size=17, color=col).next_to(ln.get_end(), UP, buff=0.08))
        fan_l[2].shift(RIGHT * 0.25 + UP * 0.08)
        fan_l[3].shift(LEFT * 0.3 + UP * 0.08)
        rows = []
        for t in th:
            w = rf"{t['window_h']} h" if t["window_h"] < 48 else rf"{t['window_h'] // 24} days"
            rows.append([rf"{100 * t['share']:.0f}\%", w, rf"{t['burn']:.1f}", rf"{100 * t['error_rate']:.2f}\%",
                         t["action"]])
        tab = grid_table([r"budget $f$", r"in window $w$", r"burn $b$", r"error rate", r"then"], rows,
                         widths=[1.3, 1.5, 1.1, 1.3, 1.0], row_h=0.48, font_size=19, mono_cols=())
        tab.next_to(g, RIGHT, buff=0.6).align_to(g, UP).shift(DOWN * 0.3)
        for r in range(1, 4):
            tab.cells[r][4].set_color(NO if rows[r - 1][4] == "page" else HEAD)
        note_ = wrapped_label(r"from \textit{The Site Reliability Workbook} \ (2018): \ 2\% of a month's budget in an "
                              r"hour is worth waking someone; \ 10\% over three days is worth a ticket", 6.0,
                              font_size=18, color=GREY_A).next_to(tab, DOWN, buff=0.35).align_to(tab, LEFT)
        with self.voiceover(
            "When should the budget wake someone up? <bookmark mark='a'/> Measure the burn rate: the error rate "
            "divided by the rate the objective allows. A burn rate of one spends the budget in exactly thirty days; "
            "a burn rate of b spends it in thirty days over b. <bookmark mark='b'/> Two lasts fifteen days; six, five "
            "days; fourteen point four, just over two days. <bookmark mark='c'/> Now turn it around. To page when a "
            "share f of the month's budget has gone within a window w, the threshold is f times seven hundred and "
            "twenty hours, over w. <bookmark mark='d'/> The Site Reliability Workbook's choices: two percent in an "
            "hour gives fourteen point four, and pages; five percent in six hours gives six, and pages; ten percent "
            "in three days gives one, and opens a ticket for working hours."
        ) as vo:
            self.play(FadeIn(head), Write(eq[0]))
            vo.wait_until("a")
            self.play(Write(eq[1]), FadeIn(g))
            self.play(Create(fan[0]), FadeIn(fan_l[0]))
            vo.wait_until("b")
            for ln, lb in zip(fan[1:], fan_l[1:]):
                self.play(Create(ln), FadeIn(lb), run_time=0.7)
            vo.wait_until("c")
            self.play(Write(eq[2]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*tab.cells[0]), tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(1, 4)], lag_ratio=0.5),
                      FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def rules(self):
        s = load("slo")
        per = s["budget"]["per_incident"]
        head = label(r"Five alerting rules on one month", font_size=36).to_edge(UP, buff=0.3)
        cols = [("blip", r"3 blips", rf"{100 * max(per[n] for n in ('blip', 'second blip', 'third blip')):.1f}\% "
                 r"each"), ("outage", r"outage", rf"{100 * per['outage']:.1f}\%"),
                ("degradation", r"degradation", rf"{100 * per['degradation']:.1f}\%"),
                ("slow leak", r"slow leak", rf"{100 * per['slow leak']:.1f}\%")]
        W = [3.5, 1.35, 1.35, 1.5, 1.5, 0.95, 1.15, 1.35]
        xs = [-6.35 + sum(W[:k]) + W[k] / 2 for k in range(len(W))]
        rh, y0 = 0.68, 2.3
        hdr = VGroup()
        for k, (_, nm, sh) in enumerate(cols):
            hdr.add(VGroup(label(nm, font_size=17, color=WHITE), label(sh, font_size=16, color=NO)).arrange(
                DOWN, buff=0.04).move_to([xs[k + 1], y0, 0]))
        for k, nm in ((5, r"pages"), (6, r"needless"), (7, r"outage alert ends")):
            t = wrapped_label(nm, W[k] - 0.1, font_size=16, color=GREY_B).move_to([xs[k], y0, 0])
            hdr.add(t)
        hdr.add(label(r"rule", font_size=17, color=GREY_B).move_to([xs[0], y0, 0]))
        rule = Line([-6.35, y0 - 0.38, 0], [-6.35 + sum(W), y0 - 0.38, 0], color=GREY_D, stroke_width=1.5)
        rows = VGroup()
        for r, row in enumerate(s["rules"]):
            y = y0 - 0.8 - r * rh
            g = VGroup(label(RULE_NAMES[row["rule"]], font_size=18, color=WHITE).move_to([xs[0], y, 0]).align_to(
                [-6.3, 0, 0], LEFT))
            for k, (key, _, _) in enumerate(cols):
                d = row["per_incident"][key]
                significant = per[key] >= 0.02
                if d["detected"]:
                    col = YES if d["by"] == "page" else HEAD
                    txt = mins(d["delay_min"]) + (r" \ ticket" if d["by"] == "ticket" else "")
                elif significant:
                    col, txt = NO, r"missed"
                else:
                    col, txt = GREY_D, r"quiet"
                box = Rectangle(width=W[k + 1] - 0.1, height=rh - 0.1, stroke_width=0, fill_color=col,
                                fill_opacity=0.35 if (d["detected"] or significant) else 0.5).move_to([xs[k + 1], y, 0])
                t = label(txt, font_size=17, color=WHITE).move_to(box)
                if t.width > box.width - 0.08:
                    t.width = box.width - 0.08
                g.add(VGroup(box, t))
            reset = row["per_incident"]["outage"].get("reset_min")
            g.add(label(rf"{row['pages']}", font_size=18, color=WHITE).move_to([xs[5], y, 0]),
                  label(rf"{row['needless']}", font_size=18, color=NO if row["needless"] else YES).move_to(
                      [xs[6], y, 0]),
                  label(rf"+{mins(reset)}" if reset is not None else r"--", font_size=18,
                        color=YES if reset is not None and reset < 60 else HEAD).move_to([xs[7], y, 0]))
            rows.add(g)
        legend = label(r"times: \ from the start of an incident to its alert; \ green pages, \ yellow tickets, \ "
                       r"red missed", font_size=18, color=GREY_A).move_to([0, y0 - 0.8 - 5 * rh, 0]).align_to(
            [-6.3, 0, 0], LEFT)
        hl = SurroundingRectangle(rows[4], color=YES, buff=0.06, stroke_width=2)
        mw = wrapped_label(r"multiwindow: \ the long window must burn \textit{and} a short one, \ a twelfth of its "
                           r"length \ (5 min for 1 h, \ 30 min for 6 h), \ so the page stops soon after the errors do",
                           12.4, font_size=19, color=WHITE).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "We scored five alerting rules from the Workbook on this month, counting an incident as worth a page if it "
            "costs at least two percent of the budget. <bookmark mark='a'/> Paging whenever the error rate exceeds "
            "the objective over ten minutes catches everything at once, and pages twenty times, including for blips "
            "that cost half a percent. <bookmark mark='b'/> A thirty-six-hour window is quiet for blips, but slow to "
            "notice and slower to stop: it keeps paging for a day and a half after the outage. "
            "<bookmark mark='c'/> A single fast burn threshold misses the degradation and the leak entirely. "
            "<bookmark mark='d'/> Two burn rates, with a ticket for the slowest, catch all three significant "
            "incidents, but the six-hour window keeps the page firing for six hours. <bookmark mark='e'/> The cure "
            "is a second, short window that must agree: the alert ends half an hour after the outage does. That last "
            "rule is the Workbook's recommendation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hdr), Create(rule))
            for mk, g in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(g, shift=RIGHT * 0.1))
                if mk == "a":
                    self.play(FadeIn(legend))
            self.play(Create(hl), FadeIn(mw))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, LAM)
