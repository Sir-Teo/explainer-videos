from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant18.common import BAD, GOOD, PART, ZERO, ask, grid_fn, illustration, load, surf3d_axes

KCOL = [QC.SPOT, QC.GAIN, QC.DELTA, QC.IMPLIED, QC.LOSS]


class Gilts(VoiceoverScene, ThreeDScene):
    def construct(self):
        L = load("ldi")
        self.card()
        self.setup_()
        self.arithmetic()
        self.spiral(L)
        self.surface(L)
        self.bank(L)

    def card(self):
        c = chapter_card(17, r"September 2022: gilts and LDI", r"How does a hedge become a fire sale?", lit=(2022,),
                         part=PART)
        with self.voiceover("Chapter seventeen. September 2022: British gilts, and the pension funds' hedges."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def setup_(self):
        boxes = VGroup()
        items = [(r"defined-benefit pension fund", r"promises paid for decades: liabilities with a duration of 20 years or "
                                                   r"more, valued off long gilt yields", ZERO),
                 (r"LDI fund (liability-driven investment)", r"holds long gilts bought with borrowed money (repo) and "
                                                             r"interest rate swaps: gilt exposure several times its cash",
                  QC.SPOT),
                 (r"the hedge", r"an approximate interest-rate and inflation hedge; the scheme, leveraged pool and collateral accounts have different cash-flow needs", GOOD)]
        for t, b, col in items:
            boxes.add(VGroup(label(t, font_size=24, color=col), wrapped_label(b, 11.0, 20, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12))
        boxes.arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(UP, buff=0.7)
        warn = wrapped_label(r"Higher yields can reduce liability present value immediately while also creating urgent margin calls. Lower liability PV does not supply cash to meet them", 11.0, 22, BAD).next_to(boxes, DOWN, buff=0.5)
        with self.voiceover(
            "Defined-benefit pension liabilities have long interest-rate and often inflation exposures. Leveraged LDI uses gilts, repo and swaps to hedge selected sensitivities while leaving capital for other assets. <bookmark mark='a'/> A pension scheme's funding position, an LDI pool's net asset value and its available collateral are different measures. A hedge can reduce the scheme's rate mismatch while remaining exposed to basis and liquidity risk. <bookmark mark='b'/> Higher yields can lower liability present value immediately, yet the hedge may face cash margin calls immediately too. The liability revaluation does not produce the cash needed to meet those calls."
        ) as vo:
            self.play(FadeIn(boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(boxes[1]), FadeIn(boxes[2]))
            vo.wait_until("b")
            self.play(FadeIn(warn))
        self.wait(0.4)
        self.clear_scene()

    def arithmetic(self):
        rows = [cmath(r"\frac{\Delta\,\text{NAV}}{\text{NAV}}", r"\approx", r"-\,L \times D \times \Delta y", font_size=44,
                      colors={r"\frac{\Delta\,\text{NAV}}{\text{NAV}}": BAD}),
                cmath(r"\Delta y_{\rm linear\ zero}", r"=", r"\frac{1}{L\,D} = \frac{1}{3 \times 20} = 1.67\ \text{points}",
                      font_size=42, colors={r"\Delta y_{\rm linear\ zero}": BAD}),
                cmath(r"3 \times 20 \times 1.30\%", r"\approx", r"78\%\ \text{of initial NAV: linear estimate}", font_size=42,
                      colors={r"3 \times 20 \times 1.30\%": BAD})]
        whys = [why(r"a pool with leverage $L$ (gilt exposure over its own cash) in gilts of duration $D$: chapter 6, "
                    r"multiplied by the leverage"),
                why(r"zero-NAV extrapolation of a first-order formula, not an exact solvency threshold or a measured collateral buffer"),
                why(r"the 30-year gilt yield rose 130 bp in three trading days to 28 September 2022, three times "
                    r"any earlier move of that length (Bank of England)")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.2, buff=0.7, edge=6.9)
        with self.voiceover(
            "Multiply a fixed-cash-flow bond's local modified-duration loss by asset-to-NAV leverage. With leverage three and duration twenty, the first-order NAV change is minus sixty times the yield change in decimal units. <bookmark mark='a'/> Extrapolating that tangent reaches zero at one-point-six-seven percentage points. This is not an exact default threshold or a complete margin model: convexity, hedge structure, financing and cash transfers matter. <bookmark mark='b'/> The Bank of England reports that thirty-year nominal gilt yields rose a hundred thirty basis points in three trading days to September twenty-eighth, 2022. Applying our illustrative tangent gives a seventy-eight-percent initial-NAV loss estimate, not an observed return of any specific fund."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
        self.add(illustration(r"illustrative pool: leverage 3, duration 20; the move: Bank of England Quarterly Bulletin "
                              r"(2023)"))
        self.wait(0.4)
        self.clear_scene()

    def spiral(self, L):
        runs = L["runs"]
        keys = list(runs)
        g1 = axes([0, 30], [0, 350], x_length=5.8, y_length=3.8, xlabel=r"round of selling",
                  ylabel=r"total rise in yields, bp", xticks=[0, 10, 20, 30], yticks=[0, 100, 200, 300], font_size=13)
        g2 = axes([0, 30], [0, 1], x_length=5.8, y_length=3.8, xlabel=r"round of selling", ylabel=r"pool's NAV",
                  xticks=[0, 10, 20, 30], yticks=[0, 0.5, 1], font_size=13)
        VGroup(g1, g2).arrange(RIGHT, buff=0.8).shift(DOWN * 0.5)
        l1, l2 = VGroup(), VGroup()
        for k, col in zip(keys, KCOL):
            r = runs[k]
            dy, nav = np.asarray(r["dy_bp"]), np.asarray(r["nav"])
            x = np.arange(len(dy))
            if len(x) < 2:
                x, dy, nav = np.array([0, 1]), np.r_[dy, dy], np.r_[nav, nav]
            l1.add(VGroup(curve(g1.ax, x, dy, col, stroke_width=3),
                          Dot(g1.ax.c2p(x[-1], dy[-1]), radius=0.06, color=col)))
            l2.add(VGroup(curve(g2.ax, x, nav, col, stroke_width=3), Dot(g2.ax.c2p(x[-1], nav[-1]), radius=0.06,
                                                                         color=col)))
        leg = legend([(c_, rf"impact {float(k):.1f} bp per 1\% of the pool sold") for k, c_ in zip(keys, KCOL)],
                     font_size=16).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.4)
        if leg.width > 13:
            leg.scale_to_fit_width(13)
        fin = {k: (runs[k]["dy_bp"][-1], runs[k]["nav"][-1]) for k in keys}
        with self.voiceover(
            f"This illustrative model starts with a fifty-basis-point shock, leverage three and constant duration twenty. After each local price loss, it sells assets to restore a specified NAV-to-duration buffer; sales generate another yield rise. Price impact is measured per percent of the then-current remaining asset pool sold. <bookmark mark='a'/> With zero impact the final recorded shock stays fifty basis points. At impact zero-point-five it reaches {fin[keys[1]][0]:.0f}, and at one it reaches {fin[keys[2]][0]:.0f}. <bookmark mark='b'/> At impact two, the thirty-round record ends at {fin[keys[4]][0]:.0f} basis points and {100 * fin[keys[4]][1]:.0f} percent of initial NAV. That path hits the iteration limit; it does not prove an infinite runaway or give a converged equilibrium. The model stops earlier for a small incremental shock or nonpositive NAV, and floors displayed NAV at zero. These are numerical assumptions, not a fitted history of the gilt crisis."
        ) as vo:
            self.play(FadeIn(g1), FadeIn(g2), FadeIn(leg))
            self.play(Create(l1[0]), Create(l2[0]))
            vo.wait_until("a")
            self.play(Create(l1[1]), Create(l2[1]), Create(l1[2]), Create(l2[2]), run_time=2)
            vo.wait_until("b")
            self.play(Create(l1[3]), Create(l2[3]), Create(l1[4]), Create(l2[4]), run_time=3)
        self.add(illustration(r"the House's \texttt{rates.ldi\_spiral}: leverage 3, duration 20, a 50 bp shock; "
                              r"illustrative, not a model of any fund"))
        self.wait(0.4)
        self.clear_scene()

    def surface(self, L):
        sh, kk, Z = np.asarray(L["shocks"], float), np.asarray(L["impacts"], float), np.asarray(L["surf"], float)
        f = grid_fn(sh, kk, Z)
        ax = surf3d_axes([10, 150, 20], [0, 2, 0.5], [0, 3200, 800], x_length=6.2, y_length=4.4, z_length=3.4)
        ax.shift(RIGHT * 0.9 + DOWN * 0.3)
        surf = Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=(10, 150), v_range=(0, 2), resolution=(14, 20),
                       fill_opacity=0.85, stroke_width=0.3, stroke_color=GREY_D, checkerboard_colors=False)
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.SPOT, 0), (QC.DELTA, 1000), (QC.LOSS, 3000)], axis=2)
        key = VGroup(
            label(r"initial shock 10--150 bp (across); impact 0--2 bp per 1\% of remaining assets sold (back)", font_size=17, color=GREY_A),
            label(r"final recorded yield rise, bp (up); full 15 by 21 grid; all values retained, up to 3000 bp", font_size=17, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "This surface retains all three hundred fifteen cached combinations of initial shock and impact, with bilinear interpolation between grid nodes. Its full vertical range reaches about three thousand basis points; the earlier four-hundred-basis-point cap is removed. <bookmark mark='a'/> Large values expose the limitations of repeatedly applying a local constant-duration model, its zero-NAV floor and its thirty-round stopping rule. The surface is a numerical stress illustration, not calibrated crisis probabilities or a forecast of feasible market clearing. It shows why leverage, liquidation and market depth must be modeled together, while realistic price and liquidity dynamics need a richer model."
        ) as vo:
            self.play(Create(ax), FadeIn(key))
            self.play(Create(surf), run_time=3)
            vo.wait_until("a")
            self.move_camera(theta=-140 * DEGREES, run_time=6)
        self.wait(0.3)
        self.move_camera(phi=0, theta=-90 * DEGREES, zoom=1.0, run_time=0.5)
        self.clear_scene()
        self.set_camera_orientation(phi=0, theta=-90 * DEGREES, gamma=0, zoom=1.0, frame_center=ORIGIN)

    def bank(self, L):
        p = L["published"]
        cc = crisis_card(r"28 September -- 14 October 2022", r"The Bank of England steps in",
                         r"to restore orderly markets, the Bank bought long-dated gilts for a strictly limited period, "
                         r"widened on 11 October to index-linked gilts; the pools used the time to raise cash and cut "
                         r"leverage, and the purchases ended on schedule",
                         stats=[(rf"\pounds {p['boe_bought_bn']}\,\text{{bn}}", r"bought in all"),
                                (rf"\pounds {p['conventional_bn']}\,\text{{bn}}", r"conventional gilts"),
                                (rf"\pounds {p['index_linked_bn']}\,\text{{bn}}", r"index-linked"),
                                (rf"{p['y30_rise_bp_3days']}\ \text{{bp}}", r"30-year yield, three days")],
                         width=7.4, font_size=22).to_edge(LEFT, buff=0.5)
        after = VGroup(
            wrapped_label(r"Higher yields improved aggregate scheme funding measures, but leveraged pools still faced urgent liquidity needs. This does not establish every scheme or pool was solvent", 4.8, 20, GREY_A),
            wrapped_label(r"2023 resilience guidance: at least around 250 bp market-stress buffer, plus an arrangement-specific operational buffer",
                          4.8, 20, GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        credit = illustration(r"Bank of England: market notices and Quarterly Bulletin (2023); Financial Policy Committee")
        with self.voiceover(
            "The Bank of England's temporary purchases ran from September twenty-eighth to October fourteenth, 2022. The published total was nineteen-point-three billion pounds: twelve-point-one conventional and seven-point-two index-linked. <bookmark mark='a'/> Higher yields improved aggregate pension funding measures because liabilities fell substantially, but leveraged pools still faced urgent cash needs. That does not certify every scheme or pool as solvent throughout. <bookmark mark='b'/> The 2023 resilience guidance calls for a market-stress buffer of at least around two hundred fifty basis points, with an additional arrangement-specific operational buffer. Collateral readiness, governance and timely access to cash matter alongside the rate hedge."
        ) as vo:
            self.play(FadeIn(cc), FadeIn(credit))
            vo.wait_until("a")
            self.play(FadeIn(after[0]))
            vo.wait_until("b")
            self.play(FadeIn(after[1]))
        self.play(FadeOut(credit), run_time=0.3)
        q = ask(r"A scheme can have improved funding while its LDI pool must sell. What would reduce forced-sale pressure?")
        with self.voiceover('A scheme can have improved funding while its LDI pool must sell. What would reduce forced-sale pressure?'):
            self.play(FadeIn(q))
        self.wait(2.5)
        self.clear_scene()
        q.to_edge(UP, buff=0.6)
        answer = wrapped_label(r"Accessible liquid collateral, lower leverage, stress-tested buffers and reliable cash-transfer processes can buy time; valuation gains on liabilities alone cannot meet margin calls.", 11.8, 26, GOOD).move_to(ORIGIN)
        with self.voiceover("Accessible liquid collateral, lower leverage, stress-tested buffers and reliable cash-transfer processes can buy time. Valuation gains on liabilities alone cannot meet margin calls."):
            self.play(FadeIn(q), FadeIn(answer))
        self.clear_scene()
