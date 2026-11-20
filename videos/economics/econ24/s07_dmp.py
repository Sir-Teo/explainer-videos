from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403


class DMP(VoiceoverScene):
    def construct(self):
        card(self, 6, r"The Diamond--Mortensen--Pissarides model", r"How many jobs will firms open, \ and how much "
             r"unemployment results?", "Chapter six. The Diamond-Mortensen-Pissarides model.",
             lit={1985: r"Pissarides", 1994: r"Mortensen and Pissarides", 2000: r"Pissarides's book"},
             scale=("firm", "market"), horizon=("a month", "years"))
        self.values()
        self.curves()
        self.beveridge()
        self.dynamics()

    def values(self):
        d = load("dmp")
        rows = VGroup(
            label(r"a firm may open a vacancy, \ at a cost $c$ a month; \ it is filled at rate $q(\theta)$",
                  font_size=23, color=JOB),
            MathTex(r"r\,\mathcal{V} = -c + q(\theta)\,(\mathcal{J} - \mathcal{V})", font_size=40, color=JOB),
            label(r"a filled job produces $p$, \ pays $w$, \ and breaks up at rate $s$", font_size=23, color=MATCH),
            MathTex(r"r\,\mathcal{J} = p - w - s\,\mathcal{J} \quad\Longrightarrow\quad \mathcal{J} = \frac{p - w}{r + s}",
                    font_size=40, color=MATCH),
            label(r"free entry: \ firms open vacancies until one is worth nothing, \ $\mathcal{V} = 0$", font_size=23,
                  color=GREY_A),
            MathTex(r"\frac{c}{q(\theta)} \;=\; \frac{p - w}{r + s} \qquad \text{(job creation)}", font_size=46,
                    color=E.ACCENT),
            label(r"expected cost of hiring \ $=$ \ value of the worker hired", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, buff=0.28).move_to(UP * 0.05)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now the model that Peter Diamond, Dale Mortensen and Christopher Pissarides built in the 1980s, the "
            "one central banks still use for the labour market. Start with firms. "
            "<bookmark mark='a'/> A firm may open a vacancy, at a cost c each month it stays open. It is filled at "
            "rate q of theta, which falls as the market gets tighter. The value of the vacancy, times the interest "
            "rate, is the cost this month plus the chance of filling it times what a filled job is worth. "
            "<bookmark mark='b'/> A filled job produces p a month, pays the wage w, and breaks up at rate s. Its "
            "value is the profit flow over r plus s. <bookmark mark='c'/> Anyone may open a vacancy, so firms keep "
            "opening them until one more is worth nothing. <bookmark mark='d'/> Then the expected cost of hiring, "
            "c over q, the cost per month times the expected months to fill it, equals the value of the worker "
            "hired. That is the job-creation condition."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), FadeIn(rows[3]))
            vo.wait_until("c")
            self.play(FadeIn(rows[4]))
            vo.wait_until("d")
            self.play(FadeIn(rows[5]), FadeIn(rows[6]))
        del d
        self.clear_scene()

    def curves(self):
        d = load("dmp")
        st, cv = d["steady"], d["curves"]
        ax = plane([0, 4], [0.85, 1.05], center=LEFT * 2.2 + DOWN * 0.3, x_length=7.2, y_length=5.0,
                   xticks=[0, 1, 2, 3, 4], yticks=[0.85, 0.9, 0.95, 1.0, 1.05], xlabel=r"tightness $\theta = V/U$",
                   ylabel=r"wage $w$ \ (output per worker $p = 1$)", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.2f}", font_size=16)
        jc = path(ax, cv["theta"], cv["jc"], color=JOB, width=4, yr=(0.85, 1.05))
        wc = path(ax, cv["theta"], cv["wc"], color=WAGE, width=4, yr=(0.85, 1.05))
        eq = dot(ax, st["theta"], st["w"], color=E.ACCENT, r=0.1)
        side = VGroup(
            label(r"job creation: \\ $w = p - (r+s)\,c / q(\theta)$", font_size=21, color=JOB),
            label(r"the wage curve \ (chapter 7): \\ $w = (1-\beta)\,b + \beta\,(p + c\,\theta)$", font_size=21,
                  color=WAGE),
            label(rf"the Island: \ $\theta^* = {st['theta']:.2f}$, \\ $w^* = {st['w']:.3f}$", font_size=23,
                  color=E.ACCENT),
            label(rf"$p = 1$, \ $b = {d['b']:g}$, \ $\beta = \eta = {d['beta']:g}$, \\ $s = {d['s']:g}$ a month, \ "
                  rf"$c = {d['c']:g}$", font_size=18, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Draw it. Across the bottom, tightness; up the side, the wage. <bookmark mark='a'/> Job creation slopes "
            "down: the tighter the market, the longer a vacancy takes to fill, so the dearer hiring is, and the "
            "lower the wage at which it still pays to open one. <bookmark mark='b'/> The wage curve slopes up: the "
            "wage is bargained, as the next chapter derives, and in a tight market a worker who walks away finds "
            "another job sooner, so the worker can ask for more. <bookmark mark='c'/> Where they cross, the "
            f"Island's labour market settles: about {st['theta']:.1f} vacancies for every unemployed worker, and a "
            f"wage of {st['w']:.3f} out of output of one. <bookmark mark='d'/> These are the Island's planted "
            "parameters: benefits worth four-tenths of output, a three percent chance each month that a job ends, "
            "and the cost of keeping a vacancy open."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(jc), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(wc), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(eq), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def beveridge(self):
        d = load("dmp")
        st = d["steady"]
        ax = plane([0, 10], [0, 12], center=LEFT * 2.2 + DOWN * 0.3, x_length=6.4, y_length=5.0,
                   xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 3, 6, 9, 12], xlabel=r"unemployment $u$, \ \%",
                   ylabel=r"vacancies $v$, \ \%", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=16)
        th = np.exp(np.linspace(np.log(0.15), np.log(8), 120))
        uu = d["s"] / (d["s"] + d["A"] * th ** (1 - d["eta"]))
        bc = path(ax, 100 * uu, 100 * th * uu, color=TIGHT, width=4, xr=(0, 10), yr=(0, 12))
        ray = seg(ax, 0, 0, 12 / st["theta"], 12, color=JOB, width=3)
        eq = dot(ax, 100 * st["u"], 100 * st["v"], color=E.ACCENT, r=0.1)
        side = VGroup(
            label(r"flows balance: \\ $u = \dfrac{s}{s + f(v/u)}$ \ \ the Beveridge curve", font_size=21,
                  color=TIGHT),
            label(r"tightness from the last picture: \\ $v = \theta^* u$", font_size=21, color=JOB),
            label(rf"unemployment {pc(st['u'])}, \\ vacancies {pc(st['v'])}", font_size=24, color=E.ACCENT),
            label(rf"job finding {100 * st['f']:.0f}\% a month; \\ a vacancy filled at {100 * st['q']:.0f}\% a month",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now bring back chapter one's tub. <bookmark mark='a'/> Unemployment is steady when separations equal "
            "job finding, and job finding depends on vacancies per unemployed worker. Every pair of unemployment "
            "and vacancies that balances the flows lies on a downward-sloping curve: the model's Beveridge curve. "
            "<bookmark mark='b'/> The last picture fixed tightness, the ratio of vacancies to unemployment: a ray "
            "from the origin. <bookmark mark='c'/> Where the ray crosses the curve, the Island has "
            f"{100 * st['u']:.1f} percent unemployment and {100 * st['v']:.1f} percent vacancies at the same "
            "time, for ever, in a perfectly steady economy. <bookmark mark='d'/> Each month about "
            f"{100 * st['f']:.0f} percent of the unemployed find jobs, and each vacancy has about a "
            f"{100 * st['q']:.0f} percent chance of being filled. That answers the part's question, in one model: "
            "both exist at once because finding each other takes time."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(bc), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(ray), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowFromCenter(eq), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def dynamics(self):
        pa = load("path")
        months = np.arange(len(pa["u"]))
        ax = plane([-3, 36], [3.45, 3.7], center=LEFT * 2.0 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[0, 6, 12, 18, 24, 30, 36], yticks=[3.45, 3.5, 3.55, 3.6, 3.65, 3.7],
                   xlabel=r"months after productivity falls 3\%", ylabel=r"unemployment, \ \%",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}", font_size=16)
        pre = seg(ax, -3, 100 * pa["u_old"], 0, 100 * pa["u_old"], color=WORKER, width=4)
        line_ = path(ax, months, 100 * np.array(pa["u"]), color=WORKER, width=4)
        new = seg(ax, 0, 100 * pa["u_new"], 36, 100 * pa["u_new"], color=GREY_B, width=2, dashed=True)
        side = VGroup(
            label(rf"tightness jumps at once: \\ {pa['theta_old']:.2f} $\to$ {pa['theta_new']:.2f}", font_size=21,
                  color=TIGHT),
            label(rf"unemployment follows: \\ half-way in {pa['half_life']:.1f} months", font_size=21, color=WORKER),
            label(rf"from {pc(pa['u_old'], 2)} to {pc(pa['u_new'], 2)}: \\ a 3\% fall in productivity \\ adds "
                  rf"{100 * (pa['u_new'] - pa['u_old']):.2f} points", font_size=21, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "What happens in a slump? Suppose productivity falls three percent, for good. "
            "<bookmark mark='a'/> Vacancies can be opened or closed overnight, so tightness jumps at once to its "
            f"new level: from {pa['theta_old']:.2f} to {pa['theta_new']:.2f}. <bookmark mark='b'/> Unemployment is "
            "a stock, so it follows more slowly, at the rate s plus f: half the way in under a month, because the "
            "flows are so fast. <bookmark mark='c'/> And look at the scale. A three percent fall in productivity, "
            "large by the standards of the business cycle, raises the Island's unemployment by less than a tenth of a point. "
            "In a real recession, American unemployment rises by several points. Hold on to that; it is chapter "
            "nine's puzzle."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(pre), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(new))
            vo.wait_until("b")
            self.play(Create(line_), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()
