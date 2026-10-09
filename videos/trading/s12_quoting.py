from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.trading.common import Plot, label, load, mtex, node, note, real_tag, schematic_tag, tagged

SKEW = 0.8  # cents of reservation-price shift per 100-share lot of inventory (gamma * sigma^2 * tau)
HALF = 1.5  # half-spread, cents
CAP = 5  # lots


def simulate(mid: np.ndarray, dt: float, seed=7, A=1.5, k=0.8):
    """Avellaneda-Stoikov quoting against a real mid-price path; fills are random, with intensity A exp(-k delta)
    as in the paper (delta = distance of the quote from the mid, cents)."""
    rng = np.random.default_rng(seed)
    q, out = 0, []
    for s in mid:
        r = s - q * SKEW
        bid, ask = r - HALF, r + HALF
        fb = fa = False
        if q < CAP and rng.random() < A * np.exp(-k * max(s - bid, 0)) * dt:
            q += 1
            fb = True
        if q > -CAP and rng.random() < A * np.exp(-k * max(ask - s, 0)) * dt:
            q -= 1
            fa = True
        out.append((s, r, bid, ask, q, fb, fa))
    return np.array(out, float)


class Quoting(VoiceoverScene):
    def construct(self):
        self.inventory()
        self.formula()
        self.slider()
        self.real_path()

    # ------------------------------------------------------------------
    def inventory(self):
        meter = NumberLine(x_range=[-5, 5, 1], length=8, include_numbers=True, font_size=24, color=GREY_B).shift(DOWN * 0.5)
        ml = label(r"inventory, in lots of 100 shares", font_size=26, color=C.INVENTORY).next_to(meter, DOWN, buff=0.5)
        q = ValueTracker(0)
        ptr = always_redraw(lambda: Triangle(fill_color=C.INVENTORY, fill_opacity=1, stroke_width=0).scale(0.16).rotate(PI)
                            .next_to(meter.n2p(q.get_value()), UP, buff=0.05))
        risk = VGroup(label(r"long 500 shares of a \$183 stock:", font_size=28),
                      label(r"every 1-cent move against you costs \$5,", font_size=28, color=C.PNL_DOWN),
                      label(r"wiping out the profit of 10 round trips", font_size=28, color=C.PNL_DOWN)).arrange(DOWN, buff=0.1)
        risk.to_edge(UP, buff=0.6)
        tag = schematic_tag()
        with self.voiceover(
            "With a fair value in hand, the market maker has to decide exactly where to quote. And there's a "
            "complication we skipped: inventory. <bookmark mark='m'/> Every time a seller hits your bid, you own more "
            "stock. <bookmark mark='l'/> Get hit five times in a row and you're long five hundred shares. <bookmark "
            "mark='r'/> Now every cent the price falls costs you five dollars: the profit from ten round trips at a "
            "half-cent each, gone in a single tick. A market maker wants to be a middleman, not an investor."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("m")
            self.play(Create(meter), FadeIn(ml), FadeIn(ptr))
            vo.wait_until("l")
            for v in range(1, 6):
                self.play(q.animate.set_value(v), run_time=0.35)
            vo.wait_until("r")
            self.play(FadeIn(risk))
        ptr.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def formula(self):
        f1 = MathTex(r"r", r"=", r"s", r"-", r"q", r"\,\gamma", r"\sigma^2", r"(T-t)", font_size=60)
        f1[0].set_color(C.OURS)
        f1[2].set_color(C.MID)
        f1[4].set_color(C.INVENTORY)
        f1[6].set_color(C.KERNEL)
        f1[7].set_color(C.LATENCY)
        f2 = MathTex(r"\delta^{\mathrm{ask}} + \delta^{\mathrm{bid}}", r"=", r"\gamma\sigma^2(T-t)", r"+",
                     r"\tfrac{2}{\gamma}\ln\!\left(1+\tfrac{\gamma}{k}\right)", font_size=48)
        VGroup(f1, f2).arrange(DOWN, buff=0.7).shift(UP * 0.8)
        cite = label(r"Avellaneda \& Stoikov, \emph{High-frequency trading in a limit order book} (2008)", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.35)
        legend = VGroup(
            label(r"$r$: the reservation price, where you center your quotes", font_size=24, color=C.OURS),
            label(r"$s$: fair value (the mid)\quad $q$: inventory\quad $\gamma$: risk aversion", font_size=24),
            label(r"$\sigma$: volatility\quad $T-t$: time left to hold\quad $k$: how fast fills dry up away from the mid",
                  font_size=24),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 2008, Marco Avellaneda and Sasha Stoikov worked out the optimal answer for a simple model of this "
            "problem. <bookmark mark='r'/> Don't center your quotes on the fair value s. Center them on a reservation "
            "price r, <bookmark mark='q'/> shifted against your inventory q: the more you own, the lower you go. The "
            "shift grows with your risk aversion, gamma, with the volatility, sigma squared, and with how long you "
            "expect to be stuck holding it. <bookmark mark='s'/> And the width of the spread has two parts: the same "
            "risk term, plus a term that depends on how quickly the chance of a fill falls off as you quote farther "
            "from the mid."
        ) as vo:
            self.play(FadeIn(cite))
            vo.wait_until("r")
            self.play(Write(f1[:3]))
            vo.wait_until("q")
            self.play(Write(f1[3:]))
            self.play(Indicate(f1[4], color=C.INVENTORY))
            vo.wait_until("s")
            self.play(Write(f2), FadeIn(legend))
        self.clear_scene()

    # ------------------------------------------------------------------
    def slider(self):
        axis = NumberLine(x_range=[-6, 6, 1], length=6.5, rotation=PI / 2, include_ticks=True, color=GREY_B).shift(LEFT * 2.0)
        al = label(r"price (cents from fair value)", font_size=22, color=GREY_A).next_to(axis, UP, buff=0.2)
        q = ValueTracker(0)
        sig = ValueTracker(1.0)

        def y(v):
            return axis.n2p(v)[1]

        def quotes():
            qq, ss = q.get_value(), sig.get_value()
            r = -qq * SKEW * ss ** 2
            h = HALF * (0.5 + 0.5 * ss ** 2)
            g = VGroup()
            s_line = DashedLine([-3.6, y(0), 0], [-0.4, y(0), 0], color=C.MID, dash_length=0.08)
            r_line = Line([-3.6, y(r), 0], [-0.4, y(r), 0], color=C.OURS, stroke_width=3)
            bid = Rectangle(width=2.6, height=0.3, fill_color=C.BID, fill_opacity=0.7, stroke_width=0).move_to([-2.0, y(r - h), 0])
            ask = Rectangle(width=2.6, height=0.3, fill_color=C.ASK, fill_opacity=0.7, stroke_width=0).move_to([-2.0, y(r + h), 0])
            g.add(s_line, r_line, bid, ask,
                  label(r"$s$", font_size=26, color=C.MID).next_to(s_line, LEFT, buff=0.1),
                  label(r"$r$", font_size=26, color=C.OURS).next_to(r_line, RIGHT, buff=0.1),
                  label(r"our bid", font_size=22, color=C.BID).next_to(bid, RIGHT, buff=0.15).shift(RIGHT * 0.3),
                  label(r"our ask", font_size=22, color=C.ASK).next_to(ask, RIGHT, buff=0.15).shift(RIGHT * 0.3))
            return g

        qs = always_redraw(quotes)
        readout = always_redraw(lambda: VGroup(
            label(rf"inventory $q$ = {q.get_value():+.1f} lots", font_size=28, color=C.INVENTORY),
            label(rf"volatility $\sigma$: {sig.get_value():.1f}$\times$", font_size=28, color=C.KERNEL),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to(RIGHT * 3.8 + UP * 1.0))
        msg = VGroup(label(r"long: lower both quotes, so you're likelier to sell", font_size=24, color=GREY_A),
                     label(r"short: raise them, so you're likelier to buy", font_size=24, color=GREY_A),
                     label(r"volatile: widen the spread", font_size=24, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        msg.move_to(RIGHT * 3.8 + DOWN * 1.2)
        tag = schematic_tag()
        with self.voiceover(
            "Here's what that does. <bookmark mark='z'/> With no inventory, the quotes sit symmetrically around fair "
            "value. <bookmark mark='l'/> As you get longer, both quotes slide down: your ask becomes more attractive, "
            "so you're likelier to sell, and your bid less attractive, so you're less likely to buy more. <bookmark "
            "mark='s'/> Short, and they slide up. <bookmark mark='v'/> And when volatility rises, the spread widens: "
            "the same inventory is now more dangerous to hold."
        ) as vo:
            self.play(FadeIn(tag), Create(axis), FadeIn(al))
            vo.wait_until("z")
            self.add(qs, readout)
            vo.wait_until("l")
            self.play(q.animate.set_value(3), FadeIn(msg[0]), run_time=2)
            vo.wait_until("s")
            self.play(q.animate.set_value(-3), FadeIn(msg[1]), run_time=2.5)
            vo.wait_until("v")
            self.play(q.animate.set_value(0), run_time=1)
            self.play(sig.animate.set_value(1.6), FadeIn(msg[2]), run_time=2)
        qs.clear_updaters()
        readout.clear_updaters()
        self.clear_scene()

    # ------------------------------------------------------------------
    def real_path(self):
        r = load("race")["minute"]["SPY"]
        t = np.array(r["t"], float) / 1e9
        m = np.array(r["mid"], float)
        dt = 0.2
        grid = np.arange(0, 60, dt)
        idx = np.clip(np.searchsorted(t, grid, side="right") - 1, 0, None)
        mid = m[idx]
        sim = simulate(mid, dt)
        s, rr, bid, ask, q, fb, fa = sim.T
        assert 30 < (mid.max() - mid.min()) < 70 and np.abs(q).max() <= CAP
        lo, hi = mid.min() - 8, mid.max() + 8
        top = Plot((0, 60), (lo, hi), width=11, height=3.3, x_ticks=[0, 15, 30, 45, 60],
                   x_fmt=lambda v: rf"{int(v)}\,\mathrm{{s}}", y_ticks=[]).shift(UP * 1.05)
        bot = Plot((0, 60), (-CAP - 0.5, CAP + 0.5), width=11, height=1.6, x_ticks=[], y_ticks=[-5, 0, 5],
                   y_fmt=lambda v: f"{int(v):+d}" if v else "0").shift(DOWN * 2.35)
        band = VGroup(top.line(grid, bid, C.BID, 2.5), top.line(grid, ask, C.ASK, 2.5))
        midl = top.line(grid, mid, C.MID, 3)
        inv = bot.line(np.repeat(grid, 2)[1:], np.repeat(q, 2)[:-1], C.INVENTORY, 3)
        fills = VGroup(*[Dot(top.c2p(grid[i], bid[i]), radius=0.05, color=C.TRADE) for i in np.nonzero(fb)[0]],
                       *[Dot(top.c2p(grid[i], ask[i]), radius=0.05, color=C.TRADE) for i in np.nonzero(fa)[0]])
        ttl = label(r"SPY's real mid-price, 11:00 to 11:01 a.m.; quotes and fills simulated as in the paper", font_size=26)
        ttl.to_edge(UP, buff=0.2)
        il = label(r"inventory (lots)", font_size=22, color=C.INVENTORY).next_to(bot, LEFT, buff=0.15).shift(UP * 0.6)
        swing = mid.max() - mid.min()
        assert 40 <= swing <= 50 and np.abs(q).max() <= 3
        with self.voiceover(
            "<bookmark mark='p'/> Here's the strategy running against a real minute of SPY, with its fills drawn at "
            f"random the way the paper models them. The price swings through {swing:.0f} cents. <bookmark mark='q'/> "
            "The quotes ride along with it, and lean against the inventory. <bookmark mark='i'/> The inventory "
            "wanders, but it never runs away, because in this model whether you get filled has nothing to do with "
            "where the price goes next. That's the skeleton of a real quoting engine. But real fills are not random. "
            "As we're about to see on real data, you tend to get filled exactly when the price is about to move "
            "against you."
        ) as vo:
            self.play(FadeIn(ttl), FadeIn(real_tag()))
            vo.wait_until("p")
            self.play(Create(top.x_axis), FadeIn(top.x_labels), Create(midl), run_time=2)
            vo.wait_until("q")
            self.play(Create(band), run_time=2)
            self.play(FadeIn(fills))
            vo.wait_until("i")
            self.play(Create(bot), FadeIn(il), Create(inv), run_time=2)
        self.clear_scene()
