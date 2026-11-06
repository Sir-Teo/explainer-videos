from __future__ import annotations

from videos.philosophy.philosophy42.common import *  # noqa: F403


class Goodhart(VoiceoverScene):
    def construct(self):
        card = chapter_card(1, r"Goodhart's law", r"What happens when a measure becomes a target?", lit=(1975, 2018), part=PART)
        with self.voiceover("Chapter one. Goodhart's law."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.history()
        self.scatter()
        self.curves()
        self.quantilize()
        self.ml()

    def history(self):
        head = history_card(1975, r"Charles Goodhart", r"``Problems of Monetary Management''", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"Goodhart \ (1975)", r"any observed statistical regularity will tend to collapse once pressure is placed upon it for control purposes", PROXYC),
                (r"Campbell \ (1976)", r"the more a quantitative social indicator is used for decisions, \ the more it is corrupted, \ and corrupts", RISK),
                (r"Strathern \ (1997)", r"`when a measure becomes a target, \ it ceases to be a good measure'", HUMAN),
                (r"Manheim and Garrabrant \ (2018)", r"four kinds: \ regressional, \ extremal, \ causal and adversarial", TRUEV)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Start with the simplest way to tell a machine what we want: give it a number to maximize. <bookmark "
            "mark='a'/>In 1975 the economist Charles Goodhart observed that any statistical regularity a government "
            "relies on tends to collapse once it is used as a target: the money supply stopped predicting inflation "
            "once the Bank of England tried to control it. <bookmark mark='b'/>The psychologist Donald Campbell said "
            "the same of social indicators: the more they are used to make decisions, the more they are corrupted. "
            "<bookmark mark='c'/>Marilyn Strathern gave the law its popular form: when a measure becomes a target, it "
            "ceases to be a good measure. <bookmark mark='d'/>David Manheim and Scott Garrabrant sorted the ways it "
            "happens into four. Regressional: the proxy contains noise, and selecting hard on the proxy selects the "
            "noise. Extremal: the relation between proxy and goal changes in regions never seen before. Causal: "
            "intervening on the proxy breaks its link to the goal. Adversarial: other agents game the proxy. The "
            "Reasoner computes the first."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def scatter(self):
        g = load("goodhart")
        s = g["scatter"]
        V = np.array(s["V"])
        head = label(r"Two worlds: \ the proxy is the true value plus an error", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        panels, notes = VGroup(), VGroup()
        tops = {}
        for i, (kind, title, col) in enumerate((("light", r"Gaussian error", TRUEV), ("heavy", r"heavy-tailed error",
                                                                                         PROXYC))):
            U = np.array(s[kind])
            ax = Axes(x_range=[-6, 12, 3], y_range=[-3.5, 3.5, 1], x_length=5.6, y_length=4.4,
                      axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
                      x_axis_config={"numbers_to_include": [-3, 0, 3, 6, 9]},
                      y_axis_config={"numbers_to_include": [-3, -2, -1, 1, 2, 3]}).move_to([-3.4 + 6.8 * i, -0.5, 0])
            xl = label(r"proxy $U = V + E$", font_size=17, color=GREY_A).next_to(ax, DOWN, buff=0.12)
            yl = label(r"true value $V$", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
            tl = label(title, font_size=22, color=col).next_to(yl, RIGHT, buff=0.6)
            inside = (U > -6) & (U < 12) & (np.abs(V) < 3.5)
            dots = VGroup(*[Dot(ax.c2p(u, v), radius=0.025, color=GREY_B, fill_opacity=0.6)
                            for u, v in zip(U[inside][::2], V[inside][::2])])
            order = np.argsort(-U)[:10]
            tops[kind] = float(V[order].mean())
            hi = VGroup(*[Dot(ax.c2p(min(U[k], 11.8), V[k]), radius=0.07, color=col) for k in order])
            beyond = int((U >= 12).sum())
            n0 = label(rf"top 10 by proxy: \ mean true value {tops[kind]:.2f}", font_size=18, color=col)
            n0.next_to(ax, DOWN, buff=0.55)
            if beyond:
                n0 = VGroup(n0, label(rf"{beyond} points lie beyond the right edge, \ drawn at it", font_size=15,
                                      color=GREY_B).next_to(n0, DOWN, buff=0.12))
            panels.add(VGroup(ax, xl, yl, tl, dots, hi))
            notes.add(n0)
        assert tops["light"] > 2.0 and tops["heavy"] < 1.0
        with self.voiceover(
            "The Reasoner builds two worlds. <bookmark mark='a'/>In each, fifteen hundred candidates have a true "
            "value, drawn from a bell curve, that we cannot see. We see only a proxy: the true value plus an error. "
            "In the first world the error is Gaussian, like the true value. <bookmark mark='b'/>In the second it is "
            "heavy-tailed: usually small, occasionally enormous. Both proxies are honest on average; neither is "
            "biased. <bookmark mark='c'/>Now optimize: take the ten candidates with the highest proxy. In the "
            "Gaussian world they are genuinely good, with a mean true value above two. <bookmark mark='d'/>In the "
            "heavy-tailed world the top of the proxy is crowded by error outliers, whose true values are close to "
            "average. The harder you select, the more of what you select is error."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(panels[0][0]), FadeIn(panels[0][1:4]), FadeIn(panels[0][4]))
            vo.wait_until("b")
            self.play(Create(panels[1][0]), FadeIn(panels[1][1:4]), FadeIn(panels[1][4]))
            vo.wait_until("c")
            self.play(FadeIn(panels[0][5], scale=1.5), FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(panels[1][5], scale=1.5), FadeIn(notes[1]))
        self.clear_scene()

    def curves(self):
        g = load("goodhart")
        ns = g["ns"]
        L, H = g["light"]["true"], g["heavy"]["true"]
        assert g["heavy"]["peak_n"] == 8 and g["light"]["peak_n"] == ns[-1]
        head = label(r"Optimization pressure \ (best of $N$) \ against true value", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        ax = Axes(x_range=[0, 13, 1], y_range=[-0.25, 3.0, 0.5], x_length=8.6, y_length=4.8,
                  axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
                  y_axis_config={"numbers_to_include": [0, 0.5, 1.0, 1.5, 2.0, 2.5],
                                 "decimal_number_config": {"num_decimal_places": 1}}).move_to([-1.6, -0.4, 0])
        ticks = VGroup(*[label(rf"{2 ** k:,}", font_size=14, color=GREY_B).next_to(ax.c2p(k, -0.25), DOWN, buff=0.15)
                         for k in (0, 3, 6, 9, 12, 13)])
        xl = label(r"candidates compared, \ $N$ \ (log scale)", font_size=17, color=GREY_A).next_to(ticks, DOWN,
                                                                                                    buff=0.15)
        yl = label(r"true value of the proxy's pick", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.05).align_to(
            ax, LEFT)
        xs = [math.log2(n) for n in ns]
        light = VMobject(color=TRUEV, stroke_width=4).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, L)])
        heavy = VMobject(color=PROXYC, stroke_width=4).set_points_as_corners([ax.c2p(x, y) for x, y in zip(xs, H)])
        ld = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=TRUEV) for x, y in zip(xs, L)])
        hd = VGroup(*[Dot(ax.c2p(x, y), radius=0.05, color=PROXYC) for x, y in zip(xs, H)])
        side = stack([(rf"Gaussian error: \ {L[-1]:.2f} at $N = 8{{,}}192$, \ still rising", TRUEV),
                      (rf"heavy tails: \ peak {g['heavy']['peak']:.2f} at $N = 8$, \ then back to {abs(H[-1]):.2f}", PROXYC),
                      (rf"meanwhile the pick's proxy score climbs to {g['heavy']['proxy'][-1]:.0f}", RISK),
                      (r"the shape of the error, \ not its size, \ decides", GOAL)],
                     font_size=19, buff=0.32, aligned_edge=LEFT)
        for s0 in side:
            if s0.width > 4.3:
                s0.width = 4.3
        side.move_to([4.6, 0.2, 0])
        with self.voiceover(
            "Now turn up the pressure. <bookmark mark='a'/>Compare N candidates and take the one with the best "
            "proxy, for N from one to eight thousand, three thousand trials each, and record the true value of the "
            "pick. <bookmark mark='b'/>With Gaussian error, more pressure always helps: the true value keeps rising, "
            "to two point seven at eight thousand candidates, though always below the proxy, which it trails by "
            "half. <bookmark mark='c'/>With heavy-tailed error the curve bends over. The true value peaks at about "
            "point six when only eight candidates are compared, and then falls back to zero, the average of doing "
            "nothing at all. <bookmark mark='d'/>Meanwhile the proxy score of the pick climbs into the hundreds. "
            "The optimizer reports ever better results while delivering nothing. <bookmark mark='e'/>The two worlds "
            "had proxies with the same correlation near the middle. What decided the outcome was the shape of the "
            "error's tail, which is exactly what a few examples cannot reveal."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(ticks), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.wait(0.5)
            vo.wait_until("b")
            self.play(Create(light), FadeIn(ld), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(heavy), FadeIn(hd), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[2]), Indicate(hd[-4:], color=RISK, scale_factor=1.6))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def quantilize(self):
        d = load("quantilize")
        rows = d["rows"]
        assert d["best_q"] == 0.25 and round(d["best_true"], 2) == 0.65 and rows[0]["top"] == 1 and rows[-1]["q"] == 1.0
        head = label(r"Mild optimization: \ a quantilizer \ (Taylor, \ 2016)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        ax = Axes(x_range=[0, len(rows), 1], y_range=[-0.1, 0.8, 0.2], x_length=9.0, y_length=4.2,
                  axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
                  x_axis_config={"include_ticks": False},
                  y_axis_config={"numbers_to_include": [0, 0.2, 0.4, 0.6],
                                 "decimal_number_config": {"num_decimal_places": 1}}).move_to([-1.0, -0.2, 0])
        names = [r"best 1", r"top 4", r"top 16", r"top 64", r"top 256", r"top 1,024", r"top 2,048", r"all 4,096"]
        bars, vals, labs = VGroup(), VGroup(), VGroup()
        for i, (r0, nm) in enumerate(zip(rows, names)):
            h = r0["true"]
            col = GOAL if r0["q"] == d["best_q"] else (RISK if i == 0 else PROXYC)
            b = Rectangle(width=0.7, height=max(abs(h) * 4.2 / 0.9, 0.02), fill_color=col, fill_opacity=0.8,
                          stroke_width=0)
            b.move_to(ax.c2p(i + 0.5, 0), DOWN if h >= 0 else UP)
            bars.add(b)
            vals.add(label(f"{h:.2f}", font_size=17, color=col).next_to(b, UP if h >= 0 else DOWN, buff=0.08))
            labs.add(label(nm, font_size=15, color=GREY_A).next_to(ax.c2p(i + 0.5, -0.1), DOWN, buff=0.12))
        yl = label(r"mean true value of the choice", font_size=17, color=GREY_A).next_to(ax, UP, buff=0.05).align_to(
            ax, LEFT)
        xl = label(r"choose at random among the proxy's top \dots \ \ (of 4,096; \ heavy-tailed error)", font_size=17,
                   color=GREY_A).next_to(labs, DOWN, buff=0.2)
        side = stack([(r"argmax: \ the outlier", RISK), (r"a quarter: \ most of the real gain", GOAL),
                      (r"everything: \ no optimization at all", PROXYC)], font_size=19, buff=0.3, aligned_edge=LEFT)
        side.move_to([5.2, 0.6, 0])
        with self.voiceover(
            "Is there a safer way to optimize? Jessica Taylor proposed one in 2016: the quantilizer. <bookmark "
            "mark='a'/>Instead of taking the single best candidate by the proxy, choose at random among the top "
            "fraction. The Reasoner tries it on four thousand and ninety six candidates in the heavy-tailed world. "
            "<bookmark mark='b'/>The argmax, the single best, has a true value near zero: it is almost always an "
            "outlier of the error. <bookmark mark='c'/>Choosing at random among the top quarter gives point six five, "
            "most of what is really there to be had. <bookmark mark='d'/>And choosing among everyone gives zero "
            "again: no optimization at all. Between doing nothing and optimizing to the limit lies a region where a "
            "proxy is useful. Limiting how hard a system optimizes is one of the few general defences against "
            "Goodhart's law; the penalty that keeps a fine-tuned language model close to its starting point is a "
            "relative of the same idea."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(yl), FadeIn(labs), FadeIn(xl))
            vo.wait_until("a")
            self.wait(0.3)
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[0], DOWN), FadeIn(vals[0]), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(*[GrowFromEdge(b, DOWN) for b in bars[1:7]], *[FadeIn(v) for v in vals[1:7]], FadeIn(side[1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(bars[7], DOWN), FadeIn(vals[7]), FadeIn(side[2]))
        self.clear_scene()

    def ml(self):
        head = label(r"Goodhart in machine learning", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"reward models", r"Gao, \ Schulman and Hilton \ (2023): \ optimizing a learned reward model raises the true reward, \ then lowers it", PROXYC),
                (r"the leash", r"RLHF penalizes divergence from the original model \ (Ziegler et al., \ 2019; \ Ouyang et al., \ 2022): \ mild optimization", TRUEV),
                (r"catastrophic Goodhart", r"Kwa, \ Thomas and Garriga-Alonso \ (2024): \ with heavy-tailed reward error, \ the leash alone can fail", RISK),
                (r"the lesson", r"a proxy is safe only within the range where it was checked: \ pressure carries you outside it", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "This is not only a toy. <bookmark mark='a'/>Leo Gao, John Schulman and Jacob Hilton trained language "
            "models against a learned reward model and measured a separate gold-standard reward. As optimization "
            "proceeded, the gold reward rose, peaked and fell, while the proxy reward kept rising: the curve the "
            "Reasoner just drew. <bookmark mark='b'/>Training from human feedback therefore keeps the model on a "
            "leash: a penalty for moving too far from the original model, as in the methods of Daniel Ziegler and "
            "colleagues and Long Ouyang and colleagues. That is mild optimization. <bookmark mark='c'/>Thomas Kwa, "
            "Drake Thomas and Adrià Garriga-Alonso showed that when the reward model's errors are heavy-tailed, the "
            "leash alone may not prevent the collapse. <bookmark mark='d'/>The general lesson: a proxy is trustworthy "
            "only in the region where it has been checked, and optimization pressure is precisely what carries a "
            "system outside that region."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
