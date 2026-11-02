from __future__ import annotations

import numpy as np

from explainer.quant import *  # noqa: F403
from videos.quant.quant2.common import ro, CCP, GAIN, LOSS, PART, TRADE, lab, load, node

C_ = {r"G": GREY_B, r"B": QC.IDEA, r"M": CCP}
LAYERS = [(r"defaulter's margin", TRADE), (r"defaulter's default fund", QC.IDEA), (r"CCP's own capital", CCP),
          (r"survivors' default fund", LOSS), (r"assessments", QC.CRISIS)]


def row(*parts, fs=36):
    return cmath(*parts, colors=C_, font_size=fs)


class Clearing(VoiceoverScene):
    def construct(self):
        n = load("netting")
        dz = load("duffie_zhu")
        w = load("waterfall")
        self.card()
        self.novation()
        self.graph(n)
        self.proof(n)
        self.duffie_zhu(dz)
        self.waterfall(w)

    def card(self):
        c = chapter_card(6, r"Clearing: novation, netting, the waterfall", r"Who guarantees that you get paid?",
                         lit=(2008,), part=PART)
        with self.voiceover("Chapter six. Clearing: novation, netting, and the default waterfall."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    def novation(self):
        a, b = node(r"buyer A", TRADE), node(r"seller B", TRADE)
        VGroup(a, b).arrange(RIGHT, buff=5.0).shift(UP * 1.6)
        ab = DoubleArrow(a.get_right(), b.get_left(), buff=0.1, color=GREY_B, stroke_width=3)
        before = label(r"before: A is exposed to B failing, and B to A", font_size=24, color=GREY_A).next_to(VGroup(a, b), UP, buff=0.3)
        a2, c, b2 = node(r"buyer A", TRADE), node(r"CCP", CCP, width=2.0), node(r"seller B", TRADE)
        VGroup(a2, c, b2).arrange(RIGHT, buff=2.0).shift(DOWN * 1.2)
        ac = DoubleArrow(a2.get_right(), c.get_left(), buff=0.1, color=CCP, stroke_width=3)
        cb = DoubleArrow(c.get_right(), b2.get_left(), buff=0.1, color=CCP, stroke_width=3)
        after = label(r"after novation: each faces only the clearing house", font_size=24, color=CCP).next_to(c, DOWN, buff=0.4)
        with self.voiceover(
            "A trade is a promise between two strangers; if one fails, the other is exposed. <bookmark mark='a'/> A central "
            "counterparty replaces the trade by two, buyer with clearing house and clearing house with seller, so everyone "
            "faces one closely watched counterparty. Since 2008 regulators have pushed standardized derivatives into clearing."
        ) as vo:
            self.play(FadeIn(a), FadeIn(b), GrowFromCenter(ab), FadeIn(before))
            vo.wait_until("a")
            self.play(TransformFromCopy(a, a2), TransformFromCopy(b, b2), FadeIn(c))
            self.play(GrowFromCenter(ac), GrowFromCenter(cb), FadeIn(after))
        self.wait(0.4)
        self.clear_scene()

    def graph(self, n):
        M = np.asarray(n["matrix"], float) / 1e9
        N = M.shape[0]
        R = 2.6
        centre = LEFT * 2.6 + DOWN * 0.2
        pos = [centre + R * np.array([np.cos(2 * np.pi * k / N + 0.3), np.sin(2 * np.pi * k / N + 0.3), 0])
               for k in range(N)]
        dots = VGroup(*[Dot(p, radius=0.08, color=TRADE) for p in pos])
        vmax = M.max()
        gross = VGroup()
        for i in range(N):
            for j in range(N):
                if M[i, j] > 0.02:
                    gross.add(Line(pos[i], pos[j], stroke_width=0.6 + 3.5 * M[i, j] / vmax, color=GREY_B,
                                   stroke_opacity=0.35))
        Y = M - M.T
        bil = VGroup()
        ym = np.abs(Y).max()
        for i in range(N):
            for j in range(N):
                if Y[i, j] > 0.02:
                    bil.add(Arrow(pos[i], pos[j], buff=0.1, stroke_width=0.8 + 4 * Y[i, j] / ym, color=QC.IDEA,
                                  max_tip_length_to_length_ratio=0.06, tip_length=0.12, stroke_opacity=0.7))
        net = np.asarray(n["net_position"], float) / 1e9
        hub = VGroup(Circle(radius=0.35, color=CCP, fill_opacity=0.25), label(r"CCP", font_size=20)).move_to(centre)
        mul = VGroup()
        nm = np.abs(net).max()
        for i in range(N):
            if abs(net[i]) > 0.005:
                a, b = (pos[i], centre) if net[i] > 0 else (centre, pos[i])
                mul.add(Arrow(a, b, buff=0.4, stroke_width=1 + 5 * abs(net[i]) / nm, color=CCP,
                              max_tip_length_to_length_ratio=0.1, tip_length=0.15))
        vals = [n["gross"], n["bilateral"], n["multilateral"]]
        tot = ValueTracker(vals[0] / 1e9)
        counter = ro(r"\text{to settle: }\$", lambda: tot.get_value(), digits=1, font_size=34,
                          unit=r"\,\text{bn}").to_edge(RIGHT, buff=0.7).shift(UP * 2.2)
        steps = VGroup(label(rf"{n['trades']:,} trades among {N} members, gross".replace(",", "{,}"), font_size=22,
                             color=GREY_B),
                       label(r"bilateral: each pair nets", font_size=22, color=QC.IDEA),
                       label(r"multilateral: each member nets against the CCP", font_size=22, color=CCP))
        steps.arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(counter, DOWN, buff=0.5).align_to(counter, LEFT)
        dtcc = wrapped_label(r"NSCC (DTCC) says its netting cuts the value of payments to be exchanged by an "
                             r"average of 98\% each day", 5.4, 20, GREY_A).next_to(steps, DOWN, buff=0.5).align_to(steps, LEFT)
        keep_in_frame(VGroup(counter, steps, dtcc), 0.4)
        src = note(r"simulated day: heavy-tailed trade sizes, a few busy members; DTCC, NSCC overview page", font_size=16)
        src.to_edge(DOWN, buff=0.15)
        with self.voiceover(
            f"The second gift is netting. A simulated day: {n['trades']:,} trades among {N} members. Settled one by one, "
            f"{vals[0] / 1e9:.1f} billion dollars. <bookmark mark='a'/> Let each pair net: opposite lines cancel, "
            f"{vals[1] / 1e9:.1f} billion. <bookmark mark='b'/> Now pull every arrow into the clearing house: each member "
            f"settles only its net position, {vals[2] / 1e9:.1f} billion, {100 * n['saved']:.0f} percent less. "
            "<bookmark mark='c'/> The real clearing house for American stocks says its netting removes ninety-eight percent "
            "of payments on an average day."
        ) as vo:
            self.play(FadeIn(dots), Create(gross), FadeIn(counter), FadeIn(steps[0]), FadeIn(src), run_time=2)
            vo.wait_until("a")
            self.play(ReplacementTransform(gross, bil), tot.animate.set_value(vals[1] / 1e9), FadeIn(steps[1]),
                      run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(hub), ReplacementTransform(bil, mul), tot.animate.set_value(vals[2] / 1e9),
                      FadeIn(steps[2]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(dtcc))
        counter.clear_updaters()
        self.wait(0.4)
        self.clear_scene()

    def proof(self, n):
        rows = [
            row(r"G", r"=", r"\sum_{i,j} x_{ij},\qquad", r"B", r"=", r"\sum_{i<j} |x_{ij} - x_{ji}|"),
            row(r"|x_{ij} - x_{ji}| \le x_{ij} + x_{ji}", r"\Rightarrow", r"B", r"\le", r"G"),
            row(r"n_i = \sum_j (x_{ij} - x_{ji}),\qquad", r"M", r"=", r"\sum_i n_i^+"),
            row(r"n_i^+ \le \sum_j (x_{ij} - x_{ji})^+", r"\Rightarrow", r"M", r"\le", r"B"),
            row(r"\sum_i n_i", r"=", r"0"),
        ]
        whys = [why(r"gross; bilateral: each pair settles only the difference", font_size=20),
                why(r"the triangle inequality, pair by pair", font_size=20),
                why(r"a member's net position; the CCP collects only net debts", font_size=20),
                why(r"the positive part of a sum is at most the sum of positive parts", font_size=20),
                why(r"every dollar owed is a dollar owed to someone: the CCP itself is flat", font_size=20)]
        for r_ in rows:
            r_.scale(0.9)
        step = ladder(self, rows, whys, keep=5, top=2.9, x=-0.6, align_index=None, buff=0.42, edge=6.9)
        card = lab_card(r"netting", [
            "def netting(payer, receiver, amount, n):",
            "    M = np.zeros((n, n))",
            "    np.add.at(M, (payer, receiver), amount)",
            "    bilateral = np.abs(np.triu(M - M.T, 1)).sum()",
            "    net = M.sum(axis=1) - M.sum(axis=0)",
            "    return M.sum(), bilateral, net[net > 0].sum()",
        ], source="explainer/quant/house/funding.py", width=6.6).to_corner(UL, buff=0.4)
        q = desk_question(r"A owes B 10, B owes C 10, C owes A 10. What moves through a CCP?", r"nothing: every "
                          r"net position is zero", width=5.4, font_size=21).to_corner(DR, buff=0.3)
        with self.voiceover(
            "Netting can only help, and here is why. Gross is the sum of every obligation; bilateral settles only each pair's "
            "difference. <bookmark mark='a'/> The difference of two amounts is at most their sum, the triangle inequality "
            "pair by pair, so bilateral is at most gross. <bookmark mark='b'/> Through a clearing house each member settles "
            "only its net position, what it owes everyone less what everyone owes it. <bookmark mark='c'/> The positive part "
            "of a sum is at most the sum of the positive parts, so a member's net debt is at most its bilateral debts added "
            "up: multilateral is at most bilateral. <bookmark mark='d'/> And the net positions sum to zero: every dollar owed "
            "is owed to someone, so the clearing house is flat. <bookmark mark='e'/> The House's code is six lines, and on the "
            "simulated day it prints the three numbers you just watched. A question: A owes B ten, B owes C ten, C owes A "
            "ten. What moves through a clearing house? <bookmark mark='z'/> Nothing. Each owes ten and is owed ten, "
            "so every net position is zero and not a dollar moves. Clearing nets the promises; settlement is when "
            "they are kept."
        ) as vo:
            for i, mk in enumerate("abcd"):
                step(i)
                vo.wait_until(mk)
            step(4)
            vo.wait_until("e")
            self.play(*[FadeOut(m) for m in self.mobjects])
            self.play(FadeIn(card))
            lab(self, card, ["netting(payer, receiver, amount, 25)",
                             f"({n['gross'] / 1e9:.2f}e9, {n['bilateral'] / 1e9:.2f}e9, {n['multilateral'] / 1e9:.2f}e9)"])
            q.answer.set_opacity(0)
            self.play(FadeIn(q))
            vo.wait_until("z")
            self.play(q.answer.animate.set_opacity(1))
        self.wait(1.0)
        self.clear_scene()

    def duffie_zhu(self, dz):
        Ns, Ks = np.asarray(dz["N"]), np.asarray(dz["K"])
        G = np.asarray(dz["gain_mc"])
        cell = 0.42
        grid = VGroup()
        for i, N in enumerate(Ns):
            for j, K in enumerate(Ks):
                v = float(np.clip(G[i, j] / 0.15, -1, 1))
                col = interpolate_color(ManimColor(BACKGROUND), ManimColor(GAIN if v > 0 else LOSS), min(abs(v) + 0.15, 1))
                grid.add(Square(cell, stroke_width=0.5, stroke_color=GREY_D, fill_color=col, fill_opacity=1)
                         .move_to([i * cell, j * cell, 0]))
        grid.move_to(LEFT * 3.2 + DOWN * 0.3)
        o = grid[0].get_center()
        bound = VMobject(color=QC.IDEA, stroke_width=4).set_points_as_corners(
            [o + np.array([(nm - Ns[0]) / 5 * cell, j * cell, 0]) for j, nm in enumerate(dz["N_min"])
             if nm <= Ns[-1]])
        xl = label(r"members $N$ (5 to 50)", font_size=20, color=GREY_A).next_to(grid, DOWN, buff=0.2)
        yl = label(r"asset classes $K$ (1 to 10)", font_size=20, color=GREY_A).rotate(PI / 2).next_to(grid, LEFT, buff=0.2)
        leg = legend([(GAIN, r"a CCP for one class lowers exposure"), (LOSS, r"it raises exposure"),
                      (QC.IDEA, r"the formula's boundary")], font_size=19).next_to(grid, UP, buff=0.3)
        rows = VGroup(
            MathTex(r"\text{bilateral, } K \text{ classes: } (N-1)\sqrt{K}\,\tfrac{\sigma}{\sqrt{2\pi}}", font_size=28),
            MathTex(r"\text{one class cleared: } \big[(N-1)\sqrt{K-1} + \sqrt{N-1}\,\big]\tfrac{\sigma}{\sqrt{2\pi}}",
                    font_size=28),
            MathTex(r"\text{helps iff } N - 1 > \big(\sqrt{K} - \sqrt{K-1}\big)^{-2}", font_size=30, color=QC.IDEA),
            MathTex(rf"K = 10:\ N \ge {int(np.ceil(dz['N_min'][-1] + 1e-9))}", font_size=28, color=QC.IDEA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4).shift(UP * 0.3)
        src = note(r"Duffie and Zhu (2011), \textit{Review of Asset Pricing Studies}: iid normal exposures; "
                   r"Monte Carlo cells against the formula", font_size=16).to_edge(DOWN, buff=0.15)
        with self.voiceover(
            "Can clearing ever make things worse? Duffie and Zhu showed that it can. Before clearing, two dealers net all their "
            "trades with each other, across every asset class. Move one class to a clearing house and that class nets across "
            "all members, but it no longer offsets the other classes bilaterally. <bookmark mark='a'/> With independent "
            "exposures the arithmetic is clean: the expected positive part of a sum of K normals grows like the square root of "
            "K, so bilateral exposure grows with the root of the classes, and the cleared class with the root of the members. "
            "<bookmark mark='b'/> Compare the two, and clearing one class lowers exposure only if the number of members minus "
            "one exceeds one over the gap between root K and root K minus one, squared. With ten classes that is "
            f"{int(np.ceil(dz['N_min'][-1] + 1e-9))} members. The Monte Carlo grid agrees with the formula cell by cell: green "
            "where clearing helps, red where it hurts."
        ) as vo:
            self.play(FadeIn(grid), FadeIn(xl), FadeIn(yl), FadeIn(leg), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(Write(rows[2]), FadeIn(rows[3]), Create(bound))
        self.wait(0.4)
        self.clear_scene()

    def waterfall(self, w):
        sizes = [w["big_im"], w["big_df"], w["skin"], w["df_total"] - w["big_df"], w["df_total"]]
        H = 5.2
        scale = H / sum(sizes)
        col = VGroup()
        y = -2.9
        for (name, c), s in zip(LAYERS, sizes):
            h = max(s * scale, 0.12)
            r_ = Rectangle(width=1.8, height=h, stroke_width=1, stroke_color=GREY_D, fill_color=c, fill_opacity=0.75)
            r_.move_to([-3.5, y + h / 2, 0])
            col.add(VGroup(r_, label(name, font_size=19, color=c).next_to(r_, LEFT, buff=0.2)))
            y += h
        named = np.asarray(w["layers_named"], float)
        sig = w["named_sigmas"]
        liquid = VGroup()
        cur = VGroup()
        reach = w["reach"]
        stats = VGroup(
            label(rf"in $10^5$ simulated days of Student-$t$ shocks, the worst-hit member's loss:", font_size=20),
            MathTex(rf"\text{{beyond its margin: }}{100 * reach[0]:.1f}\%", font_size=26, color=TRADE),
            MathTex(rf"\text{{into the CCP's capital: }}{100 * reach[2]:.1f}\%", font_size=26, color=CCP),
            MathTex(rf"\text{{into survivors' money: }}{100 * reach[3]:.1f}\%", font_size=26, color=LOSS),
            MathTex(rf"\text{{assessments: }}{100 * reach[4]:.2f}\%", font_size=26, color=QC.CRISIS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(RIGHT, buff=0.4).shift(UP * 0.8)
        pfmi = wrapped_label(r"cover 2 (CPMI--IOSCO principles): a systemically important CCP holds enough to survive "
                             r"the default of its two largest members in extreme but plausible markets", 5.6, 19,
                             GREY_A).next_to(stats, DOWN, buff=0.4).align_to(stats, LEFT)
        with self.voiceover(
            "If a member defaults, who pays? The waterfall: the defaulter's margin, its default-fund contribution, the "
            "clearing house's own capital, then the survivors' default fund, and finally assessments on them. "
            f"<bookmark mark='a'/> Pour in five stress days, {sig[0]} to {sig[4]} standard deviations against the biggest "
            "member: small shocks stop in its own margin. <bookmark mark='b'/> Over a hundred thousand fat-tailed days, the "
            f"worst-hit member's loss beats its margin on {100 * reach[0]:.0f} percent of days but reaches survivors' money on "
            f"{100 * reach[3]:.1f} percent. Systemically important clearing houses must survive their two largest members "
            "failing at once: cover two."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(c_) for c_ in col], lag_ratio=0.3, run_time=4))
            vo.wait_until("a")
            for k in range(len(sig)):
                taken = named[k][:5]
                parts = VGroup()
                for layer, amt in zip(col, taken):
                    if amt <= 0:
                        continue
                    r_ = layer[0]
                    h = r_.height * min(amt / max(sizes[list(col).index(layer)], 1e-9), 1)
                    parts.add(Rectangle(width=1.8, height=h, stroke_width=0, fill_color=QC.CRISIS, fill_opacity=0.8)
                              .move_to(r_.get_bottom() + UP * h / 2))
                lbl = MathTex(rf"{sig[k]}\sigma", font_size=30, color=QC.CRISIS).next_to(col, RIGHT, buff=0.4)
                self.play(FadeIn(parts, shift=DOWN * 0.4), FadeIn(lbl), run_time=0.9)
                self.play(FadeOut(parts), FadeOut(lbl), run_time=0.4)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in stats], lag_ratio=0.3), FadeIn(pfmi))
        self.wait(0.4)
        self.clear_scene()
