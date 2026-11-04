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
                 (r"the hedge", r"when yields fall, liabilities rise and so does the LDI fund; when yields rise, both "
                                r"fall. The pension fund is hedged", GOOD)]
        for t, b, col in items:
            boxes.add(VGroup(label(t, font_size=24, color=col), wrapped_label(b, 11.0, 20, GREY_A)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.12))
        boxes.arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(UP, buff=0.7)
        warn = wrapped_label(r"but leverage means a rise in yields calls for collateral in cash, today; the falling "
                             r"liability saves money only over decades", 11.0, 22, BAD).next_to(boxes, DOWN, buff=0.5)
        with self.voiceover(
            "British defined-benefit pension funds owe pensions for decades ahead, and the value of those promises "
            "moves with long gilt yields. To hedge, most used liability-driven investment funds, which hold long gilts "
            "bought with borrowed money, and interest rate swaps. <bookmark mark='a'/> Leverage let a pension fund "
            "hedge its whole liability with a fraction of its assets. When yields fall, liabilities rise, and so does "
            "the hedge. <bookmark mark='b'/> But when yields rise, the leveraged positions need more collateral, in "
            "cash, at once; the matching fall in the liability saves money only over decades."
        ) as vo:
            self.play(FadeIn(boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(boxes[1]), FadeIn(boxes[2]))
            vo.wait_until("b")
            self.play(FadeIn(warn))
        self.wait(0.4)
        self.clear_scene()

    def arithmetic(self):
        rows = [cmath(r"\frac{\Delta\,\text{NAV}}{\text{NAV}}", r"=", r"-\,L \times D \times \Delta y", font_size=44,
                      colors={r"\frac{\Delta\,\text{NAV}}{\text{NAV}}": BAD}),
                cmath(r"\Delta y^{\dagger}", r"=", r"\frac{1}{L\,D} = \frac{1}{3 \times 20} = 1.67\ \text{points}",
                      font_size=42, colors={r"\Delta y^{\dagger}": BAD}),
                cmath(r"3 \times 20 \times 1.30\%", r"=", r"78\%\ \text{of NAV, in three days}", font_size=42,
                      colors={r"3 \times 20 \times 1.30\%": BAD})]
        whys = [why(r"a pool with leverage $L$ (gilt exposure over its own cash) in gilts of duration $D$: chapter 6, "
                    r"multiplied by the leverage"),
                why(r"the yield rise that wipes out the pool: its buffer. Leverage of three and a duration of twenty "
                    r"leave under two points"),
                why(r"the 30-year gilt yield rose 130 bp in three trading days to 28 September 2022, three times "
                    r"any earlier move of that length (Bank of England)")]
        step = ladder(self, rows, whys, keep=3, top=2.9, x=-1.2, buff=0.7, edge=6.9)
        with self.voiceover(
            "Chapter six's arithmetic, multiplied by leverage. A pool with three times leverage in gilts of duration "
            "twenty loses three times twenty times the yield change, as a fraction of its cash. "
            "<bookmark mark='a'/> So a rise of one point sixty-seven wipes it out. That was the buffer, and many pools "
            "held less. <bookmark mark='b'/> On the twenty-third of September 2022 the government announced large "
            "unfunded tax cuts. By the twenty-eighth, the thirty-year gilt yield had risen a hundred and thirty basis "
            "points in three trading days: three times any earlier move of that length, by the Bank of England's "
            "count. Three times twenty times one point three is seventy-eight percent of a pool's cash."
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
            l1.add(VGroup(curve(g1.ax, x, np.clip(dy, 0, 350), col, stroke_width=3),
                          Dot(g1.ax.c2p(x[-1], min(dy[-1], 350)), radius=0.06, color=col)))
            l2.add(VGroup(curve(g2.ax, x, nav, col, stroke_width=3), Dot(g2.ax.c2p(x[-1], nav[-1]), radius=0.06,
                                                                         color=col)))
        leg = legend([(c_, rf"impact {float(k):.1f} bp per 1\% of the pool sold") for k, c_ in zip(keys, KCOL)],
                     font_size=16).arrange(RIGHT, buff=0.3).to_edge(UP, buff=0.4)
        if leg.width > 13:
            leg.scale_to_fit_width(13)
        fin = {k: (runs[k]["dy_bp"][-1], runs[k]["nav"][-1]) for k in keys}
        with self.voiceover(
            "Now the spiral, simulated with the House's model of a leveraged pool. A fifty basis point shock cuts the "
            "pool's net asset value. To rebuild its buffer the manager sells gilts and repays borrowing; if those sales "
            "push yields up, the next round of losses follows, and the next. <bookmark mark='a'/> With no price impact, "
            "the shock stays fifty basis points. With half a basis point of impact for every percent of the pool sold, "
            f"it becomes {fin[keys[1]][0]:.0f}. With one, {fin[keys[2]][0]:.0f}. <bookmark mark='b'/> With two, the "
            f"selling never catches up: yields rise {fin[keys[4]][0]:.0f} basis points and the pool is left with "
            f"{100 * fin[keys[4]][1]:.0f} percent of its value. The amplification is not proportional to the impact; "
            "past a point it runs away."
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
        Zc = np.clip(Z, 0, 400)
        f = grid_fn(sh, kk, Zc)
        ax = surf3d_axes([10, 150, 20], [0, 2, 0.5], [0, 400, 100], x_length=6.2, y_length=4.4, z_length=3.4)
        ax.shift(RIGHT * 0.9 + DOWN * 0.3)
        surf = Surface(lambda u, v: ax.c2p(u, v, f(u, v)), u_range=(10, 150), v_range=(0, 2), resolution=(20, 20),
                       fill_opacity=0.85, stroke_width=0.3, stroke_color=GREY_D, checkerboard_colors=False)
        surf.set_fill_by_value(axes=ax, colorscale=[(QC.SPOT, 0), (QC.DELTA, 150), (QC.LOSS, 350)], axis=2)
        key = VGroup(label(r"initial shock, bp (across); price impact (back); final rise, bp (up, capped at 400)",
                           font_size=18, color=GREY_A)).to_corner(UL, buff=0.3)
        self.set_camera_orientation(phi=65 * DEGREES, theta=-60 * DEGREES, zoom=0.85)
        self.add_fixed_in_frame_mobjects(key)
        self.remove(key)
        with self.voiceover(
            "Map it over every combination of initial shock and price impact. On the near edge, with little impact, "
            "the final move is the shock. <bookmark mark='a'/> Toward the back the surface lifts gently, and then rears "
            "up into a cliff: large shocks in a market that cannot absorb the selling. In September 2022 the shock was "
            "large, and everyone was selling the same long gilts at once."
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
            wrapped_label(r"the pension funds were solvent: higher yields cut their liabilities more than their assets. "
                          r"Their problem was cash, not value", 4.8, 20, GREY_A),
            wrapped_label(r"since then UK regulators expect LDI pools to withstand a rise of at least 250 bp in yields",
                          4.8, 20, GOOD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5)
        with self.voiceover(
            "On the twenty-eighth of September the Bank of England announced it would buy long gilts, for a strictly "
            "limited time, to restore orderly markets. It bought nineteen point three billion pounds by the fourteenth "
            "of October: twelve point one billion of conventional gilts and seven point two of index-linked. "
            "<bookmark mark='a'/> The striking thing is that the pension funds were solvent throughout: higher yields "
            "shrank their liabilities more than their assets. They ran short of cash, not of value. "
            "<bookmark mark='b'/> Since then, British regulators have expected these pools to survive a jump of at "
            "least two hundred and fifty basis points."
        ) as vo:
            self.play(FadeIn(cc))
            vo.wait_until("a")
            self.play(FadeIn(after[0]))
            vo.wait_until("b")
            self.play(FadeIn(after[1]))
        q = ask(r"the funds were solvent but had to sell. What would have let them wait?")
        with self.voiceover("They were solvent, and still had to sell. What would have let them wait?"):
            self.play(FadeIn(q))
        self.add(illustration(r"Bank of England: market notices and Quarterly Bulletin (2023); Financial Policy Committee"))
        self.wait(0.5)
        self.clear_scene()
