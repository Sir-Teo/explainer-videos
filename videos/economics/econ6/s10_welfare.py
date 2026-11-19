from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403

CVC, EVC, CSC = SUB, HICKS, E.ACCENT     # compensating variation, equivalent variation, Marshall's surplus


class Welfare(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Welfare in dollars", r"What is a price change worth to the people it hits?",
             "Chapter eight. Welfare in dollars.")
        self.cv_ev()
        self.areas()
        self.tax()

    def cv_ev(self):
        b = load("bo")
        w = load("welfare")
        ax = goods_axes(center=LEFT * 3.1 + DOWN * 0.3, top=14, x_length=5.8, y_length=5.8,
                        ticks=(0, 2, 4, 6, 8, 10, 12, 14))
        a = ax.ax
        xs = np.array(b["xs"])
        ic0 = curve(ax, xs, np.array(b["ic0"]), color=IC, width=3, top=14)
        ic1 = curve(ax, xs, np.array(b["ic1"]), color=IC, width=3, top=14)
        old = budget_line(ax, 6, 10)
        new = budget_line(ax, 10, 10, color=NEWB)
        mcv = b["m"] - w["cv"]
        mev = b["m"] + w["ev"]
        cvl = DashedVMobject(budget_line(ax, mcv / b["p1"], mcv / b["py"], color=CVC), num_dashes=30)
        evl = DashedVMobject(budget_line(ax, mev / b["p0"], mev / b["py"], color=EVC), num_dashes=30)
        side = VGroup(
            label(r"fish \$10 $\to$ \$6: \ what is it worth to Bo?", font_size=27),
            VGroup(label(rf"compensating variation: \ \${w['cv']:.2f}", font_size=27, color=CVC),
                   label(r"\emph{after} the fall, \ the most you could take from him \\ and leave him as well off as "
                         r"before", font_size=21, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(rf"equivalent variation: \ \${w['ev']:.2f}", font_size=27, color=EVC),
                   label(r"\emph{instead of} the fall, \ what you'd have to give him \\ to make him as well off as "
                         r"the fall would", font_size=21, color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.1),
            label(r"two honest answers to one question: \\ they differ because the dollars are counted \\ at "
                  r"different prices", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Economists keep asking what a price change is worth: a tax, a tariff, a subsidy, a new railway. The "
            "answer should be in dollars, so it can be added up and compared with the cost. <bookmark mark='a'/> "
            "Bo again: fish fall from ten dollars to six, and he moves to a higher indifference curve. What is that "
            "worth to him? <bookmark mark='b'/> One answer: after the fall, how much money could you take away from "
            "him and leave him exactly as well off as before? That's the compensating variation, the same fifteen "
            "dollars eighty-four as Hicks's compensation in chapter three. <bookmark mark='c'/> Another answer: "
            "suppose the fall never happens. How much would you have to give him to make him as well off as the fall "
            "would have? That's the equivalent variation, twenty-one dollars fifty-two. <bookmark mark='d'/> Both "
            "are honest. They differ because one counts the dollars at the new prices and the other at the old, and "
            "for Bo, whose income matters to how much fish he buys, those dollars are worth different amounts."
        ) as vo:
            self.play(FadeIn(ax), Create(ic0), Create(old), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(new), Create(ic1))
            vo.wait_until("b")
            self.play(Create(cvl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(evl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def areas(self):
        w = load("welfare")
        from explainer.ai.viz import axes

        ps = np.array(w["ps"])
        ax = axes([0, 11], [4, 12], x_length=6.4, y_length=5.2, xticks=[0, 2, 4, 6, 8, 10], yticks=[4, 6, 8, 10, 12],
                  xlabel=r"fish bought", ylabel=r"price of fish (\$)", font_size=18, center=LEFT * 2.9 + DOWN * 0.3)
        a = ax.ax

        def dcurve(q, col, width=4):
            return VMobject(stroke_color=col, stroke_width=width).set_points_smoothly(
                [a.c2p(x, p) for x, p in zip(q, ps) if x <= 11])

        def region(q, col, q_left=None):
            """The area between q_left (or the price axis) and q, between the two prices."""
            k = (ps >= w["p1"]) & (ps <= w["p0"])
            right = [a.c2p(x, p) for x, p in zip(q[k], ps[k])]
            if q_left is None:
                left = [a.c2p(0, w["p0"]), a.c2p(0, w["p1"])]
            else:
                left = [a.c2p(x, p) for x, p in zip(q_left[k][::-1], ps[k][::-1])]
            return Polygon(*right, *left, stroke_width=0, fill_color=col, fill_opacity=0.55)

        mar, h0, h1 = np.array(w["marshall"]), np.array(w["hicks0"]), np.array(w["hicks1"])
        cm, c0, c1 = dcurve(mar, MARSH), dcurve(h0, CVC), dcurve(h1, EVC)
        lines = VGroup(DashedLine(a.c2p(0, w["p0"]), a.c2p(11, w["p0"]), color=GREY_C, stroke_width=1.5),
                       DashedLine(a.c2p(0, w["p1"]), a.c2p(11, w["p1"]), color=GREY_C, stroke_width=1.5))
        def at(q, p):
            return a.c2p(q[int(np.argmin(abs(ps - p)))], p)

        names = VGroup(label(r"Marshall", font_size=19, color=MARSH).next_to(at(mar, 5.0), RIGHT, buff=0.1),
                       label(r"Hicks, old curve", font_size=19, color=CVC).next_to(at(h0, 11.5), LEFT, buff=0.1),
                       label(r"Hicks, new curve", font_size=19, color=EVC).next_to(at(h1, 11.5), RIGHT, buff=0.1))
        side = VGroup(
            label(r"the area to the left of a demand curve, \\ between the two prices \ (each adds a slice):",
                  font_size=23),
            label(rf"Hicks at the old utility: \ CV \ \${w['cv']:.2f}", font_size=25, color=CVC),
            label(rf"Marshall: \ consumer's surplus \ \${w['cs']:.2f}", font_size=25, color=CSC),
            label(rf"Hicks at the new utility: \ EV \ \${w['ev']:.2f}", font_size=25, color=EVC),
            label(r"Willig (1976): \ the gap is about \\ $\eta \cdot \mathrm{CS} / 2m$ \ of the surplus", font_size=24,
                  color=E.ACCENT),
            label(rf"Bo: \ $\eta = 1$, \ CS $= \${w['cs']:.0f}$, \ $m = \${w['m']:.0f}$: \\ about "
                  rf"{100 * w['willig_bo']:.0f}\% \ (exactly {100 * w['cv_gap_bo']:.0f}\%)", font_size=22,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            "The two answers have a picture, and it brings back Marshall's consumer's surplus from Part two. "
            "<bookmark mark='a'/> Three demand curves for fish: Marshall's ordinary curve, and Hicks's compensated "
            "curves at Bo's old and new satisfaction. <bookmark mark='b'/> The compensating variation is exactly "
            "the area to the left of the old compensated curve, between the two prices. By Shephard's lemma, "
            "that area is the change in the expenditure function. <bookmark mark='c'/> The ordinary consumer's "
            "surplus, the area to the left of Marshall's curve, lies in between. <bookmark mark='d'/> And the "
            "equivalent variation is the area to the left of the new compensated curve. <bookmark mark='e'/> In 1976 "
            "Robert Willig showed how far apart they can be: the gap is roughly the income elasticity times the "
            "surplus as a share of income, halved. For Bo, a big price change that's worth almost a third of his "
            "income, that's about fifteen percent. For most price changes it's a few percent, and Marshall's "
            "surplus, which you can measure from an ordinary demand curve, is good enough. Willig titled the paper "
            "consumer's surplus without apology."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(lines), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(cm), Create(c0), Create(c1), FadeIn(names))
            vo.wait_until("b")
            self.play(FadeIn(region(h0, CVC)), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(region(mar, CSC, h0)), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(region(h1, EVC, mar)), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
        self.clear_scene()

    def tax(self):
        w = load("welfare")
        t = w["tax"]
        from explainer.ai.viz import axes

        pt = np.array(w["tax_pt"])
        ax = axes([3, 9], [0.8, 2.2], x_length=5.6, y_length=4.8, xticks=[3, 5, 7, 9], yticks=[1.0, 1.4, 1.8, 2.2],
                  xlabel=r"coconuts a week", ylabel=r"price (\$)", font_size=18, yfmt=lambda v: f"{v:.1f}",
                  center=LEFT * 3.3 + DOWN * 0.35)
        a = ax.ax
        mid = w["taxes"][1]
        p0, p1 = t["price"], t["price"] + mid["t"]
        mar = VMobject(stroke_color=MARSH, stroke_width=4).set_points_smoothly(
            [a.c2p(x, p) for x, p in zip(w["tax_marshall"], pt) if 3 <= x <= 9 and 0.8 <= p <= 2.2])
        hic = VMobject(stroke_color=CVC, stroke_width=4).set_points_smoothly(
            [a.c2p(x, p) for x, p in zip(w["tax_hicks"], pt) if 3 <= x <= 9 and 0.8 <= p <= 2.2])
        x1m = float(np.interp(p1, pt, w["tax_marshall"]))
        # the compensated quantity at the taxed price
        hp = np.array(w["tax_hicks"])
        x1h = float(hp[int(np.argmin(abs(pt - p1)))])
        x0 = w["x0"]
        tri_m = Polygon(a.c2p(x1m, p1), a.c2p(x0, p0), a.c2p(x1m, p0), stroke_width=0, fill_color=CSC,
                        fill_opacity=0.5)
        tri_h = Polygon(a.c2p(x1h, p1), a.c2p(x0, p0), a.c2p(x1h, p0), stroke_width=0, fill_color=CVC,
                        fill_opacity=0.5)
        wedge = VGroup(DashedLine(a.c2p(3, p0), a.c2p(9, p0), color=GREY_C, stroke_width=1.5),
                       DashedLine(a.c2p(3, p1), a.c2p(9, p1), color=GREY_C, stroke_width=1.5),
                       label(rf"tax {100 * mid['t']:.0f}\textcent", font_size=19, color=GREY_A).move_to(
                           a.c2p(8.2, (p0 + p1) / 2)))
        rows = VGroup(
            label(rf"a {100 * mid['t']:.0f}-cent tax on a \${p0:.2f} coconut", font_size=26, color=COCO),
            label(rf"demand $x = {t['alpha']:.0f}p + {t['delta']:g}m + {t['c']:.0f}$; \ income elasticity "
                  rf"{w['eta']:.2f}", font_size=21, color=GREY_A),
            label(rf"loss: \ CS \${mid['cs']:.2f}, \ CV \${mid['cv']:.2f}: \ {100 * mid['cv_gap']:.1f}\% apart",
                  font_size=24),
            label(rf"deadweight loss: \ Marshall \${mid['dwl_marshall']:.2f}, \ exact \${mid['dwl_exact']:.2f}",
                  font_size=24, color=E.ACCENT),
            label(rf"{100 * mid['dwl_error']:.0f}\% too big: \ a small difference \\ between two big numbers",
                  font_size=24, color=E.ACCENT),
            label(r"Hausman (1981): \ integrate Roy's identity \\ back to the expenditure function", font_size=23,
                  color=CVC),
            MathTex(r"e(p, k) = k\,e^{\delta p} - \frac{1}{\delta}\Big(\alpha p + \frac{\alpha}{\delta} + c\Big)",
                    font_size=30, color=CVC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"simulated: the Island's coconut demand", corner=DR, font_size=13)
        with self.voiceover(
            "Where the approximation can mislead is the cost of a tax. <bookmark mark='a'/> Put a sixty-cent tax "
            "on the Island's coconuts, on an ordinary straight demand curve that shifts with income. "
            "<bookmark mark='b'/> The household's loss, measured by Marshall's surplus, is three dollars sixty; "
            "exactly, it's three dollars seventy-two. Three percent apart: Willig's rule holds. "
            "<bookmark mark='c'/> But the number that matters for tax policy is the deadweight loss: the loss beyond "
            "the revenue the government collects. Marshall's triangle says seventy-two cents; the exact triangle, "
            "under the compensated curve, says sixty-one. Seventeen percent too big, because the deadweight loss "
            "is a small difference between two big numbers, and small errors in each become a large error in the "
            "difference. <bookmark mark='d'/> Jerry Hausman's fix, in 1981: from an estimated demand curve, solve "
            "Roy's identity backwards for the expenditure function. For a straight demand curve it has a closed "
            "form, and exact welfare is no harder to compute than the approximation."
        ) as vo:
            self.play(FadeIn(ax), Create(mar), FadeIn(tag), FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(wedge), Create(hic))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(tri_m), FadeIn(rows[3]))
            self.play(FadeIn(tri_h), FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5]), Write(rows[6]))
        self.clear_scene()
