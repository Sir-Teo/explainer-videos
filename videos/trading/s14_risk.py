from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import (
    FACTS, fmt_int, label, load, node, note, schematic_tag, server_box, show_part, source, tagged,
)


class Risk(VoiceoverScene):
    def construct(self):
        show_part(self, 5, r"Staying alive", r"risk, determinism, and the research loop")
        self.gate()
        self.knight()
        self.lessons()

    # ------------------------------------------------------------------
    def gate(self):
        checks = [r"order size $\le$ limit", r"price within a band around fair value", r"position after fill $\le$ limit",
                  r"orders per second $\le$ limit", r"capital and credit $\le$ limit", r"kill switch: off"]
        rows = VGroup(*[VGroup(Square(0.32, stroke_color=C.RISK, stroke_width=2),
                               label(t, font_size=24)).arrange(RIGHT, buff=0.2) for t in checks])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16)
        box = SurroundingRectangle(rows, buff=0.3, color=C.RISK, corner_radius=0.12, stroke_width=3)
        gate = VGroup(box, rows).move_to(RIGHT * 0.3 + DOWN * 0.2)
        gl = label(r"risk checks: inline, automatic, on every order", font_size=28, color=C.RISK).next_to(gate, UP, buff=0.2)
        strat = node(r"strategy", C.OURS, width=2.0, height=0.9).move_to(LEFT * 5.4 + DOWN * 0.2)
        exch = node(r"exchange", C.TRADE, width=2.0, height=0.9).move_to(RIGHT * 5.6 + DOWN * 0.2)
        a1 = Arrow(strat.get_right(), gate.get_left(), buff=0.1, color=C.ORDER, stroke_width=3)
        a2 = Arrow(gate.get_right(), exch.get_left(), buff=0.1, color=C.ORDER, stroke_width=3)
        rule = note(r"required for U.S. broker-dealers since 2010: SEC Rule 15c3-5, the Market Access Rule", font_size=22,
                    color=GREY_A).to_edge(DOWN, buff=0.35)
        tag = schematic_tag()
        with self.voiceover(
            "The last stage before an order leaves is the one that keeps the firm alive. <bookmark mark='g'/> Every "
            "order passes through risk checks: is it too big? Is its price far from where we think the stock is "
            "worth? Would it push our position past its limit? Are we sending too many orders too fast? Would it use "
            "more capital than we have? And is the kill switch on? <bookmark mark='l'/> Because they run on every "
            "order, they have to be fast, and some firms build them into the same hardware as the reflexes. And they "
            "have to be independent of the strategy: the strategy is the thing they protect us from. <bookmark mark='r'/> In "
            "the United States, any broker with direct access to the market has been required to have such automated "
            "controls since 2010."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(strat), FadeIn(exch))
            vo.wait_until("g")
            self.play(FadeIn(gate), FadeIn(gl), GrowArrow(a1), GrowArrow(a2))
            for k in range(len(rows)):
                ck = MathTex(r"\checkmark", font_size=30, color=C.PNL_UP).move_to(rows[k][0])
                self.play(FadeIn(ck), run_time=0.25)
            vo.wait_until("l")
            good = Dot(strat.get_right(), radius=0.1, color=C.ORDER)
            self.add(good)
            self.play(MoveAlongPath(good, Line(strat.get_right(), exch.get_left())), run_time=1.0, rate_func=linear)
            self.remove(good)
            bad = VGroup(Dot(radius=0.14, color=C.PNL_DOWN), label(r"buy 1{,}000{,}000", font_size=20, color=C.PNL_DOWN))
            bad[1].next_to(bad[0], UP, buff=0.08)
            bad.move_to(strat.get_right() + UP * 0.35)
            self.play(bad.animate.move_to(gate.get_left() + UP * 0.35 + LEFT * 0.3), run_time=0.8)
            x = Cross(rows[0][0], stroke_color=C.PNL_DOWN, stroke_width=6).scale(1.4)
            self.play(Create(x), FadeOut(bad, scale=0.5))
            vo.wait_until("r")
            self.play(FadeIn(rule))
        self.clear_scene()

    # ------------------------------------------------------------------
    def knight(self):
        F = FACTS
        ttl = label(r"Knight Capital, August 1, 2012", font_size=40).to_edge(UP, buff=0.35)
        sub = label(r"then about 10\% of all U.S. stock trading", font_size=24, color=GREY_A).next_to(ttl, DOWN, buff=0.1)
        servers = VGroup(*[server_box(str(i + 1), color=C.PNL_UP if i < 7 else C.PNL_DOWN, width=1.2, height=0.85, font_size=20)
                           for i in range(F["knight_servers"])]).arrange(RIGHT, buff=0.18).move_to(UP * 1.15)
        notes = VGroup(
            label(r"new code installed on 7 of 8 servers", font_size=24, color=C.PNL_UP),
            label(r"server 8 still had \emph{Power Peg}: dead code, unused since 2003", font_size=24, color=C.PNL_DOWN),
        ).arrange(DOWN, buff=0.1).next_to(servers, DOWN, buff=0.3)
        src = source(r"SEC order against Knight Capital Americas, Release 34-70694 (2013)", font_size=18)
        with self.voiceover(
            "What happens without those checks? The most famous answer is Knight Capital, then one of the largest "
            "market makers in America, handling about a tenth of all U.S. stock trading. <bookmark mark='s'/> In late "
            "July 2012, Knight installed new code on the eight servers of its order router. A technician missed one. "
            "<bookmark mark='p'/> Server number eight still had a piece of old code called Power Peg, unused since "
            "2003, and the new code reused a flag that, on that one server, switched Power Peg back on."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(sub), FadeIn(src))
            vo.wait_until("s")
            self.play(LaggedStart(*[FadeIn(s, shift=UP * 0.2) for s in servers], lag_ratio=0.1), FadeIn(notes[0]))
            vo.wait_until("p")
            self.play(Indicate(servers[7], color=C.PNL_DOWN), FadeIn(notes[1]))
        emails = label(rf"8:01 a.m.: the first of {F['knight_emails']} automated e-mails saying ``Power Peg disabled''",
                       font_size=24, color=GREY_A).next_to(notes, DOWN, buff=0.35)
        with self.voiceover(
            "<bookmark mark='e'/> On the morning of August 1st, starting at 8:01, Knight's systems sent ninety-seven "
            "automated e-mails mentioning Power Peg. They weren't designed as alerts, and nobody acted on them."
        ) as vo:
            vo.wait_until("e")
            self.play(FadeIn(emails))
        self.clear_scene()

        # the 45 minutes
        minutes = ValueTracker(0)
        T = F["knight_minutes"]
        clock = always_redraw(lambda: label(rf"9:{30 + int(minutes.get_value()):02d} a.m." if minutes.get_value() < 30
                                            else rf"10:{int(minutes.get_value()) - 30:02d} a.m.", font_size=44,
                                            color=C.LATENCY).to_edge(UP, buff=0.5))
        execs = always_redraw(lambda: label(rf"executions: {fmt_int(F['knight_execs'] * minutes.get_value() / T)}",
                                            font_size=30, color=C.TRADE).move_to(UP * 1.6))
        bar_w = 5.0

        def bars():
            f = minutes.get_value() / T
            lw, sw = bar_w * f, bar_w * f * F["knight_short"] / F["knight_long"]
            g = VGroup(
                Rectangle(width=max(lw, 0.01), height=0.7, stroke_width=0, fill_color=C.BID, fill_opacity=0.85)
                .move_to(LEFT * 0.05 + RIGHT * 0, aligned_edge=LEFT).shift(UP * 0.3),
                Rectangle(width=max(sw, 0.01), height=0.7, stroke_width=0, fill_color=C.ASK, fill_opacity=0.85)
                .move_to(LEFT * 0.05, aligned_edge=RIGHT).shift(UP * 0.3),
            )
            g[0].align_to(ORIGIN, LEFT)
            g[1].align_to(ORIGIN, RIGHT)
            g.add(label(rf"long \${F['knight_long'] / 1e9 * f:.2f} billion", font_size=26, color=C.BID).next_to(g[0], DOWN, buff=0.15).align_to(ORIGIN, LEFT).shift(RIGHT * 0.3),
                  label(rf"short \${F['knight_short'] / 1e9 * f:.2f} billion", font_size=26, color=C.ASK).next_to(g[1], DOWN, buff=0.15).align_to(ORIGIN, RIGHT).shift(LEFT * 0.3))
            return g

        pos = always_redraw(bars)
        axis = Line(UP * 0.85, DOWN * 0.3, color=GREY_B, stroke_width=2).shift(UP * 0.3)
        what = label(rf"server 8 kept sending child orders for {F['knight_parent']} customer orders, never counting the fills",
                     font_size=24, color=GREY_A).to_edge(DOWN, buff=1.4)
        fix = label(r"the attempted fix, removing the new code from the 7 good servers, made it worse", font_size=24,
                    color=C.PNL_DOWN).next_to(what, DOWN, buff=0.15)
        with self.voiceover(
            "<bookmark mark='o'/> At 9:30, server eight began working on 212 small customer orders, and for each one, "
            "it sent child orders to the market, again and again, because the code that counted how many shares had "
            "already been bought had been moved years earlier. <bookmark mark='g'/> Nothing stopped it. <bookmark "
            "mark='f'/> The engineers, trying to find the problem live, removed the new code from the seven good "
            "servers, which activated Power Peg on those too. <bookmark mark='t'/> In forty-five minutes: four million "
            "executions in 154 stocks, 397 million shares, a 3.5 billion dollar long position in eighty stocks, and a "
            "3.15 billion dollar short position in seventy-four."
        ) as vo:
            vo.wait_until("o")
            self.add(clock, execs, pos)
            even = note(r"totals from the SEC's order; growth over the 45 minutes drawn evenly", font_size=20).to_corner(DR, buff=0.3)
            self.play(FadeIn(axis), FadeIn(what), FadeIn(even))
            vo.wait_until("g")
            self.play(minutes.animate.set_value(20), run_time=max(vo.until("f") - 0.2, 1.0), rate_func=linear)
            self.play(FadeIn(fix))
            self.play(minutes.animate.set_value(T), run_time=max(vo.until("t") - 0.2, 1.0), rate_func=linear)
        clock.clear_updaters()
        execs.clear_updaters()
        pos.clear_updaters()
        loss = VGroup(label(r"loss", font_size=36, color=GREY_A),
                      MathTex(rf"\${F['knight_loss'] / 1e6:.0f}\ \text{{million}}", font_size=72, color=C.PNL_DOWN),
                      label(r"in 45 minutes", font_size=30, color=GREY_A)).arrange(DOWN, buff=0.15).move_to(DOWN * 2.3)
        loss.add_background_rectangle(color=BACKGROUND, opacity=0.95, buff=0.15)
        with self.voiceover(
            "<bookmark mark='l'/> Unwinding those positions cost Knight 460 million dollars, more than the firm could "
            "survive on its own. Within days it needed a rescue, and within a year it had been merged away."
        ) as vo:
            vo.wait_until("l")
            self.play(FadeOut(what), FadeOut(fix), FadeIn(loss, scale=1.1))
        self.clear_scene()

    # ------------------------------------------------------------------
    def lessons(self):
        F = FACTS
        missing = VGroup(
            label(r"what the SEC found missing", font_size=32, color=C.RISK),
            label(r"\textbullet\ no automated, firm-wide capital limit wired to order entry", font_size=26),
            label(rf"\textbullet\ a \${F['knight_limit_33'] / 1e6:.0f} million limit on the account that filled up, "
                  r"connected to nothing that could stop orders", font_size=26),
            label(r"\textbullet\ position monitoring that relied on people watching a screen", font_size=26),
            label(r"\textbullet\ no second technician checking deployments; no procedure for incidents", font_size=26),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(UP * 0.9)
        today = VGroup(
            label(r"what the industry does now", font_size=32, color=C.PNL_UP),
            label(r"inline limits on every order \quad kill switches \quad reconciling every fill against the "
                  r"exchange's copy \quad automated, rehearsed deployments", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "<bookmark mark='m'/> The SEC's findings read like a checklist of everything in that risk gate. There was "
            "no automated, firm-wide capital limit connected to order entry. The account that filled up with unwanted "
            "shares had a two-million-dollar limit, but it wasn't wired to anything that could stop the orders. Position "
            "monitoring depended on people watching a screen. Nobody double-checked the deployment, and there was no "
            "plan for an incident. <bookmark mark='t'/> Today's top firms treat these as part of the trading system "
            "itself: limits on every order, kill switches, every fill reconciled against the exchange's own record, "
            "and deployments rehearsed and automated, so that a mistake costs seconds, not a company."
        ) as vo:
            vo.wait_until("m")
            self.play(LaggedStart(*[FadeIn(m, shift=RIGHT * 0.15) for m in missing], lag_ratio=0.35), run_time=4)
            vo.wait_until("t")
            self.play(FadeIn(today))
        self.clear_scene()
