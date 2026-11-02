from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant15.common import BAD, DELTA, GOOD, IV, OPT, PART, SPOT, illustration, load


class Digitals(VoiceoverScene):
    def construct(self):
        d = load("digital")
        a = load("asian")
        self.card()
        self.digital(d)
        self.spread(d)
        self.asian(a)

    def card(self):
        c = chapter_card(3, r"Digitals, Asians and lookbacks", r"Which payoffs are easy to price and hard to hedge?",
                         part=PART)
        with self.voiceover("Chapter three. Digitals, Asians and lookbacks."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def digital(self, d):
        S = np.asarray(d["S"])
        g1 = axes([90, 110], [0, 1.05], x_length=5.6, y_length=3.4, xlabel=r"spot", ylabel=r"price of 1 if $S_T > 100$",
                  xticks=[90, 95, 100, 105, 110], yticks=[0, 0.5, 1.0], font_size=15)
        g2 = axes([90, 110], [0, 0.75], x_length=5.6, y_length=3.4, xlabel=r"spot", ylabel=r"delta",
                  xticks=[90, 95, 100, 105, 110], yticks=[0, 0.25, 0.5, 0.75], font_size=15)
        VGroup(g1, g2).arrange(RIGHT, buff=0.9).to_edge(UP, buff=1.0)
        cols = {"a month": GREY_B, "a day": IV, "an hour": BAD}
        L1 = VGroup(*[curve(g1.ax, S, np.asarray(c["price"]), cols[k], stroke_width=2.5) for k, c in d["curves"].items()])
        L2 = VGroup(*[curve(g2.ax, S, np.clip(np.asarray(c["delta"]), 0, 0.75), cols[k], stroke_width=2.5)
                      for k, c in d["curves"].items()])
        leg = legend([(cols[k], rf"{k} to expiry") for k in d["curves"]], font_size=17)
        leg.arrange(RIGHT, buff=0.4).next_to(VGroup(g1, g2), DOWN, buff=0.3)
        mx = d["curves"]["an hour"]["max_delta"]
        foot = wrapped_label(rf"an hour before expiry, the digital's delta at the strike is {mx:.2f} units per unit of payout: "
                             r"for a payout of a million, a hedge of hundreds of thousands of units that flips to zero on a "
                             r"tick. A digital is a smooth price on an impossible hedge", 11.5, 20, GREY_A).to_edge(DOWN, buff=0.45)
        src = illustration(r"cash-or-nothing call struck at 100, volatility 25\%")
        with self.voiceover(
            "A digital pays one if the price ends above the strike, and nothing otherwise. Its price is simple: the "
            "risk-neutral probability of finishing above, discounted. A month from expiry it is a gentle S-curve. "
            "<bookmark mark='a'/> But as expiry nears, the curve steepens into a step, and its slope, the delta, "
            f"spikes at the strike: {mx:.2f} units per unit of payout an hour before expiry. On a payout of a "
            "million, that is a hedge of hundreds of thousands of units, which must flip to zero on a tick. A digital "
            "is a smooth price on an impossible hedge."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(src), Create(L1[0]), Create(L2[0]), FadeIn(leg[0]))
            vo.wait_until("a")
            self.play(Create(L1[1]), Create(L2[1]), FadeIn(leg[1]), run_time=1.5)
            self.play(Create(L1[2]), Create(L2[2]), FadeIn(leg[2]), FadeIn(foot), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()

    def spread(self, d):
        rows = d["spread"]
        tab = VGroup(VGroup(label(r"call spread width", font_size=22, color=GREY_A), label(r"price", font_size=22, color=GREY_A),
                            label(r"largest delta, a day out", font_size=22, color=GREY_A)))
        tab.add(VGroup(label(r"the digital itself", font_size=24), MathTex(f"{d['digital_atm']:.3f}", font_size=28),
                       MathTex(f"{d['curves']['a day']['max_delta']:.3f}", font_size=28, color=BAD)))
        for r in rows:
            tab.add(VGroup(MathTex(rf"\varepsilon = {r['eps']:g}", font_size=28), MathTex(f"{r['price']:.3f}", font_size=28),
                           MathTex(f"{r['max_delta']:.3f}", font_size=28, color=GOOD)))
        xs = [-3.6, 0.6, 4.0]
        for i, row in enumerate(tab):
            for j, cell in enumerate(row):
                cell.move_to([xs[j], 2.4 - 0.62 * i, 0])
        eq = MathTex(r"\text{digital} \le \frac{C(K - \varepsilon) - C(K)}{\varepsilon}", font_size=34, color=OPT)
        eq.to_edge(DOWN, buff=1.2)
        note_ = wrapped_label(r"the seller books the digital as a call spread struck just below: it pays at least as much in "
                              r"every state, costs a little more, and has a delta capped at $1/\varepsilon$ per unit. The "
                              r"width is a trade between that extra cost and a hedge the desk can actually run",
                              11.0, 20, GREY_A).next_to(eq, DOWN, buff=0.25)
        with self.voiceover(
            "Desks do not hedge a digital as a digital. They book it as a tight call spread, long a call just below "
            "the strike and short one at it, scaled by one over the width. <bookmark mark='a'/> The spread pays at "
            "least as much as the digital in every state, so the seller is safe; it costs a little more, and the "
            "wider it is, the more it costs and the gentler its delta. Choosing the width is choosing between a "
            "price the client will pay and a hedge the desk can run."
        ) as vo:
            self.play(FadeIn(tab[:2]), FadeIn(eq))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_) for r_ in tab[2:]], lag_ratio=0.3), FadeIn(note_))
        self.wait(0.4)
        self.clear_scene()

    def asian(self, a):
        rows = a["rows"]
        g = axes([np.log10(500), np.log10(100000)], [-3, 0], x_length=6.2, y_length=4.0,
                 xlabel=r"paths (log scale)", ylabel=r"Monte Carlo error (s.d., log scale)",
                 xticks=[np.log10(v) for v in (1000, 4000, 16000, 64000)], xfmt=lambda u: f"{10 ** u:,.0f}".replace(",", "{,}"),
                 yticks=[-3, -2, -1, 0], yfmt=lambda u: f"10^{{{int(u)}}}", log_x=True, font_size=15)
        g.to_edge(LEFT, buff=0.7).shift(DOWN * 0.2)
        ax = g.ax
        p1 = VGroup(*[Dot(ax.c2p(np.log10(r["n"]), np.log10(r["sd_plain"])), radius=0.07, color=BAD) for r in rows])
        p2 = VGroup(*[Dot(ax.c2p(np.log10(r["n"]), np.log10(r["sd_cv"])), radius=0.07, color=GOOD) for r in rows])
        l1 = VMobject(stroke_color=BAD, stroke_width=2.5).set_points_as_corners([d_.get_center() for d_ in p1])
        l2 = VMobject(stroke_color=GOOD, stroke_width=2.5).set_points_as_corners([d_.get_center() for d_ in p2])
        leg = legend([(BAD, r"plain Monte Carlo"), (GOOD, r"with the geometric Asian as control variate")], font_size=17)
        leg.next_to(g, UP, buff=0.15).align_to(g, LEFT)
        ratio = float(np.median([r["sd_plain"] / r["sd_cv"] for r in rows]))
        side = VGroup(
            wrapped_label(r"an Asian option pays on the average price: cheaper than a vanilla, and hard to manipulate at "
                          r"a single fixing", 4.4, 19, GREY_A),
            MathTex(rf"{a['price']:.2f}\ \ \text{{vs vanilla}}\ {a['vanilla']:.2f}", font_size=30, color=OPT),
            wrapped_label(r"the geometric average is log-normal, so its Asian has a closed form (Kemna and Vorst 1990); "
                          rf"simulate both and correct by the known error: {ratio:.0f} times less noise, as if with "
                          rf"{ratio ** 2:.0f} times the paths", 4.4, 19, WHITE),
            wrapped_label(rf"a lookback pays $S_T - \min S$: {a['lookback_cf']:.1f} watched continuously (Goldman, Sosin "
                          rf"and Gatto 1979), {a['lookback_mc_daily']:.1f} at daily closes, the same BGK effect as barriers",
                          4.4, 19, GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.35)
        src = illustration(r"one-year at-the-money calls, 25\% volatility, daily fixings; 20 independent runs each")
        with self.voiceover(
            "Two more path-dependent payoffs. An Asian option pays on the average price over its life: cheaper than "
            f"a vanilla, {a['price']:.2f} against {a['vanilla']:.2f} here, and hard to push around with a trade at a "
            "single fixing. The arithmetic average has no closed form, so it is simulated. <bookmark mark='a'/> But "
            "the geometric average does: Angelien Kemna and Ton Vorst noticed in 1990 that it is log-normal. Simulate "
            "both on the same paths, and correct the arithmetic estimate by the geometric one's known error. The "
            f"noise falls by a factor of {ratio:.0f}, as if you had run {ratio ** 2:.0f} times as many paths. "
            "<bookmark mark='b'/> And a lookback, which pays the final price minus the lowest one, shows the barrier's "
            "lesson again: watched at daily closes, it is worth less than the continuous formula says."
        ) as vo:
            self.play(FadeIn(g), FadeIn(src), FadeIn(leg[0]), FadeIn(p1), Create(l1), FadeIn(side[0]), FadeIn(side[1]))
            vo.wait_until("a")
            self.play(FadeIn(leg[1]), FadeIn(p2), Create(l2), FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(side[3]))
        self.wait(0.4)
        self.clear_scene()
