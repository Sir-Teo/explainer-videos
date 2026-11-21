from __future__ import annotations

from videos.economics.econ52.common import *  # noqa: F403


class Wealth(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The wealth distribution", r"What does the simple model miss at the top?",
             "Chapter six. The wealth distribution.", lit={1998: r"Krusell and Smith", 2011: r"Benhabib, Bisin, Zhu"},
             scale=("household", "nation"), horizon=("a century",))
        self.gap()
        self.why()
        self.fixes()
        self.tails()

    def _bars(self, W, upto):
        ax = plane([0, 4.6], [0, 80], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.4, y_length=4.8, xticks=[],
                   yticks=[0, 20, 40, 60, 80], ylabel=r"share of all wealth, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        groups = [(r"US data", W["data"]["top1"], W["data"]["top10"], DATA)]
        names = {"Aiyagari": r"Aiyagari", "patience": r"+ patience", "returns 6": r"+ returns, \ 6 pts",
                 "returns 8": r"+ returns, \ 8 pts"}
        cols = {"Aiyagari": MANY, "patience": RICH, "returns 6": DIST, "returns 8": DIST}
        for m in W["models"]:
            groups.append((names[m["name"]], m["top1"], m["top10"], cols[m["name"]]))
        out = VGroup()
        for i, (nm, t1, t10, col) in enumerate(groups[:upto]):
            x = 0.5 + 0.9 * i
            p0, p1 = ax.ax.c2p(x - 0.36, 0), ax.ax.c2p(x - 0.02, t1)
            q0, q1 = ax.ax.c2p(x + 0.02, 0), ax.ax.c2p(x + 0.36, t10)
            b1 = Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.01), stroke_width=0, fill_color=col,
                           fill_opacity=0.95).move_to((p0 + p1) / 2)
            b2 = Rectangle(width=q1[0] - q0[0], height=max(q1[1] - q0[1], 0.01), stroke_width=1.5, stroke_color=col,
                           fill_color=col, fill_opacity=0.25).move_to((q0 + q1) / 2)
            v1 = label(f"{t1:.0f}", font_size=15, color=WHITE).next_to(b1, UP, buff=0.06)
            v2 = label(f"{t10:.0f}", font_size=15, color=GREY_A).next_to(b2, UP, buff=0.06)
            nmo = label(nm, font_size=15, color=col).next_to(ax.ax.c2p(x, 0), DOWN, buff=0.2)
            out.add(VGroup(b1, b2, v1, v2, nmo))
        return ax, out

    def gap(self):
        W = load("wealth")
        ax, groups = self._bars(W, 2)
        key = VGroup(label(r"solid: \ the top 1\%", font_size=18, color=WHITE),
                     label(r"outlined: \ the top 10\%", font_size=18, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_edge(RIGHT, buff=0.5).shift(UP * 2.2)
        side = VGroup(
            label(rf"data: \ the top 1\% \\ hold {W['data']['top1']:.1f}\%", font_size=20, color=DATA),
            label(rf"the model: \ {W['models'][0]['top1']:.1f}\%", font_size=20, color=MANY),
            label(r"precautionary saving \\ makes a middle class \\ of savers, \ not a \\ class of the very rich",
                  font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        tag = data_tag(rf"Federal Reserve, \ Distributional Financial Accounts, \ {W['date'][:4]} Q2, \ via FRED",
                       corner=DL, font_size=12)
        with self.voiceover(
            "How well does this economy match the distribution of wealth in the data? <bookmark mark='a'/> In the "
            "Federal Reserve's distributional accounts for the United States, the richest one percent of "
            f"households hold {W['data']['top1']:.1f} percent of all wealth, and the richest tenth "
            f"{W['data']['top10']:.0f} percent. <bookmark mark='b'/> In Aiyagari's economy, the top one percent "
            f"hold {W['models'][0]['top1']:.1f} percent. <bookmark mark='c'/> The model gets a spread of wealth, "
            "but not the very rich. Saving against bad luck builds a buffer of a few years' income, and then "
            "stops: once the buffer is full, there is no reason to keep accumulating. The rich in the data are not "
            "buffer-stock savers."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(key), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(groups[0], shift=UP * 0.1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(groups[1], shift=UP * 0.1), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def why(self):
        A = load("aiyagari")
        a = np.array(A["a"])
        ap = np.array(A["ap"])
        ax = plane([0, 200], [-0.3, 0.3], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.0, y_length=4.6,
                   xticks=[0, 50, 100, 150, 200], yticks=[-0.3, -0.15, 0, 0.15, 0.3], xlabel=r"wealth",
                   ylabel=r"saving next year, \ share of wealth", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}".replace("-", "{-}"), font_size=14)
        cols = (POOR, MANY, RICH)
        idx = [0, 3, ap.shape[1] - 1]
        sel = a > 0.5
        curves = VGroup(*[path(ax, a[sel], ap[sel, j] / a[sel] - 1, col, 2.6, xr=(0, 200), yr=(-0.3, 0.3))
                          for j, col in zip(idx, cols)])
        zero = seg(ax, 0, 0, 200, 0, GREY_B, 1.4, dashed=True)
        s_top = ap[:, -1] / np.maximum(a, 1e-9) - 1
        cross = float(a[np.where((a > 1) & (s_top < 0))[0][0]])
        cdot = dot(ax, cross, 0, RICH, 0.1)
        clab = label(rf"even the luckiest: \\ from about {cross:.0f}", font_size=16, color=RICH).next_to(
            cdot, UP, buff=0.2)
        side = VGroup(
            label(r"orange: \ lowest wage", font_size=18, color=POOR),
            label(r"green: \ middle wage", font_size=18, color=MANY),
            label(r"blue: \ highest wage", font_size=18, color=RICH),
            label(r"above some wealth, \\ even the luckiest \\ household runs \\ its wealth down", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Here is why. The curves show how much each household adds to its wealth in a year, as a share of what "
            "it has. <bookmark mark='a'/> A poor household with a low wage runs its wealth down; <bookmark "
            "mark='b'/> one with a high wage builds it up quickly. <bookmark mark='c'/> But above some level, "
            "every curve falls below zero: even the luckiest household runs its wealth down. The interest rate is "
            "below the rate of time preference, so wealth for its own sake is not worth keeping. Nothing in the "
            "model lets fortunes grow without limit, and so nothing produces the long upper tail of the data."
        ) as vo:
            self.play(FadeIn(ax), Create(zero))
            for mk, c_, s_ in zip("ab", curves[:1], side[:1]):
                vo.wait_until(mk)
                self.play(Create(c_), FadeIn(s_), run_time=1.4)
            vo.wait_until("b")
            self.play(Create(curves[1]), FadeIn(side[1]), Create(curves[2]), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(cdot, scale=1.5), FadeIn(clab), FadeIn(side[3], shift=UP * 0.1))
        self.clear_scene()

    def fixes(self):
        W = load("wealth")
        ax, groups = self._bars(W, 5)
        b = W["betas"]
        side = VGroup(
            label(rf"patience: \ discount factors \\ {b[0]}, \ {b[1]} and {b[2]}", font_size=18, color=RICH),
            label(rf"returns: \ {100 * W['business_share']:.0f}\% of households \\ at a time earn a few \\ points more "
                  r"on wealth", font_size=18, color=DIST),
            label(r"returns: \ same interest rate \\ and wages, \ not re-cleared", font_size=15, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3).shift(UP * 0.4)
        tag = published_tag(r"Krusell and Smith (1998); \ Benhabib, \ Bisin and Zhu (2011, 2015)", corner=DR,
                            font_size=12)
        r6, r8 = W["models"][2], W["models"][3]
        with self.voiceover(
            "Three fixes have been tried. <bookmark mark='a'/> The first gives households different patience: "
            "Krusell and Smith let the discount factor itself drift between values. With three permanent types "
            f"here, the top one percent hold {W['models'][1]['top1']:.1f} percent: better, but nowhere near. "
            "<bookmark mark='b'/> The second, after Jess Benhabib, Alberto Bisin and Shenghao Zhu, gives some "
            "households, at some times, a higher return on their wealth: think of an owner whose business takes "
            f"off. If {100 * W['business_share']:.0f} percent of households at a time earn six points more, the top "
            f"one percent hold {r6['top1']:.1f} percent; <bookmark mark='c'/> if they earn eight points more, "
            f"{r8['top1']:.1f} percent. <bookmark mark='d'/> Returns that compound for the lucky few make fortunes "
            "that grow until the luck ends, and that is what the data's upper tail looks like. The third fix, not "
            "shown, gives the best-paid a small chance of extraordinary earnings."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(groups[:2]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(groups[2], shift=UP * 0.1), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(groups[3], shift=UP * 0.1), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(groups[4], shift=UP * 0.1))
            vo.wait_until("d")
            self.play(Indicate(groups[4][0], color=WHITE), Indicate(groups[0][0], color=WHITE))
        self.clear_scene()

    def tails(self):
        W = load("wealth")
        ax = plane([0, 9], [-7, -2], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.0, y_length=4.8,
                   xticks=[0, 3, 6, 9], yticks=[-7, -6, -5, -4, -3, -2], xlabel=r"log wealth",
                   ylabel=r"log share of households richer", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        lines = VGroup()
        for tl, col in zip(W["tails"], (DIST, INDIRECT)):
            if "log_a" in tl:
                lines.add(path(ax, tl["log_a"], tl["log_tail"], col, 3.0, smooth=False))
        t0 = W["tail_base"]
        base = path(ax, t0.get("log_a", []), t0.get("log_tail", []), MANY, 3.0, smooth=False) if "log_a" in t0 \
            else VMobject()
        d_alpha = W["data"]["alpha"]
        r6, r8 = W["models"][2], W["models"][3]
        side = VGroup(
            label(r"a Pareto tail is a straight line here; \\ its slope is minus the exponent", font_size=18,
                  color=WHITE),
            label(rf"green: \ Aiyagari, \ steep: \ exponent {W['models'][0]['alpha']:.1f}", font_size=18,
                  color=MANY),
            label(rf"purple: \ 6 points, \ {r6['alpha']:.1f}", font_size=18, color=DIST),
            label(rf"gold: \ 8 points, \ {r8['alpha']:.1f}", font_size=18, color=INDIRECT),
            label(rf"the data's top shares imply {d_alpha:.1f}", font_size=19, color=DATA),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        foot = label(r"the tail is very sensitive to how large and lasting the lucky returns are", font_size=20,
                     color=E.ACCENT).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "On a log-log plot of how many households are richer than each level of wealth, a Pareto tail is a "
            "straight line, and the flatter the line, the fatter the tail. <bookmark mark='a'/> Aiyagari's economy "
            f"has a steep, thin tail: an exponent of about {W['models'][0]['alpha']:.0f}. <bookmark mark='b'/> With "
            f"returns six points higher for the lucky, about {r6['alpha']:.1f}; <bookmark mark='c'/> with eight "
            f"points, about {r8['alpha']:.1f}. The data's top shares imply {d_alpha:.1f}. <bookmark mark='d'/> "
            "Notice how sensitive the tail is: two points of extra return move the top one percent's share from "
            f"{r6['top1']:.0f} to {r8['top1']:.0f} percent. A model can match the top this way, but only by "
            "choosing returns that must then be measured, and measuring returns to private wealth is hard."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(base), FadeIn(side[1]))
            vo.wait_until("b")
            if len(lines) > 0:
                self.play(Create(lines[0]), FadeIn(side[2]))
            vo.wait_until("c")
            if len(lines) > 1:
                self.play(Create(lines[1]), FadeIn(side[3]), FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
