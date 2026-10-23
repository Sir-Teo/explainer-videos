from __future__ import annotations

import math

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai21.common import DATA, NOISE, PART, Panel, load, take_away

COL = {r"x_0": DATA, r"\varepsilon": NOISE, r"\bar\alpha_t": C.BITS}


class Forward(VoiceoverScene):
    def construct(self):
        self.card()
        self.chain()
        self.closed_form()
        self.check()
        self.posterior()

    def card(self):
        card = chapter_card(1, r"Destroying data slowly", r"How do you turn data into noise, in a way that can be undone?",
                            part=PART, lit=(2015,))
        with self.voiceover("Chapter one. Destroying data slowly."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def chain(self):
        f = load("forward")
        frames, keep = np.asarray(f["frames"]), [int(k) for k in f["keep"]]
        T = int(f["T"])
        pn = Panel(6.4, center=[-3.2, -0.2, 0], xlim=(-3.2, 3.4), ylim=(-3.0, 2.6))
        dots = pn.dots(frames[0], DATA, radius=0.022)
        cnt = label(r"step $0$", font_size=26, color=GREY_A).next_to(pn, UP, buff=0.15)
        d = definition_card(r"the forward process", VGroup(
            MathTex(r"q(x_t \mid x_{t-1}) = \mathcal N\big(\sqrt{1-\beta_t}\; x_{t-1},\ \beta_t I\big)", font_size=30),
            label(r"shrink a little, \ add a little noise; \ $t = 1, \dots, T$", font_size=22, color=GREY_A),
            label(rf"DDPM's choice: \ $T = {T:,}$, \ $\beta_t$ from ${f['beta'][0]:g}$ to ${f['beta'][-1]:g}$".replace(",", "{,}"),
                  font_size=22, color=GREY_A),
            label(r"nothing in it is learned", font_size=22, color=C.BITS)).arrange(DOWN, aligned_edge=LEFT, buff=0.18),
            width=6.0).move_to([3.4, 0.4, 0])
        cite_ = cite(r"Sohl-Dickstein et al.\ (2015); \ Ho, Jain \& Abbeel (2020)", corner=DR)
        with self.voiceover(
            "Annealed Langevin, at the end of Part 20, needs the score at every level of noise. Where do the levels "
            "come from? From a process that destroys the data on purpose. <bookmark mark='a'/> Take every point, "
            "shrink it a little towards the origin, and add a little Gaussian noise. <bookmark mark='b'/> Do it a "
            "thousand times. The shrinking keeps the spread from growing; the noise erases the letters, a little at "
            "each step, until only a round bell of noise is left. <bookmark mark='c'/> That is the forward process. "
            "It has no parameters: nothing in it is learned."
        ) as vo:
            self.play(FadeIn(pn), FadeIn(dots), FadeIn(cnt), FadeIn(cite_))
            vo.wait_until("a")
            self.play(FadeIn(d, shift=UP * 0.2))
            vo.wait_until("b")
            for k in range(1, len(frames)):
                col = interpolate_color(ManimColor(DATA), ManimColor(NOISE), k / (len(frames) - 1))
                c2 = label(rf"step ${keep[k]:,}$".replace(",", "{,}"), font_size=26, color=GREY_A).move_to(cnt)
                self.play(*pn.move(dots, frames[k], color=col), Transform(cnt, c2),
                          run_time=0.45)
            vo.wait_until("c")
            self.play(Indicate(d.body[-1], color=C.BITS))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def closed_form(self):
        rows = [
            cmath(r"x_t", r"=", r"\sqrt{1-\beta_t}\; x_{t-1} + \sqrt{\beta_t}\; \varepsilon_t", font_size=34),
            cmath(r"x_t", r"=", r"\sqrt{(1-\beta_t)(1-\beta_{t-1})}\; x_{t-2} + \sqrt{(1-\beta_t)\beta_{t-1}}\; "
                  r"\varepsilon_{t-1} + \sqrt{\beta_t}\; \varepsilon_t", font_size=30),
            cmath(r"x_t", r"=", r"\sqrt{(1-\beta_t)(1-\beta_{t-1})}\; x_{t-2} + \sqrt{1 - (1-\beta_t)(1-\beta_{t-1})}\; "
                  r"\varepsilon", font_size=30),
            cmath(r"x_t", r"=", r"\sqrt{\bar\alpha_t}\;", r"x_0", r"+", r"\sqrt{1-\bar\alpha_t}\;", r"\varepsilon",
                  r",\qquad \bar\alpha_t = \prod_{s \le t} (1-\beta_s)", colors=COL, font_size=34),
        ]
        whys = [why(r"one step"), why(r"substitute the step before"),
                why(r"independent Gaussians: \ their variances add"), why(r"repeat, \ all the way down to $x_0$")]
        step = ladder(self, rows, whys, keep=4, top=2.6, x=-3.6, buff=0.55, edge=6.8)
        box = theorem_card(r"one jump", MathTex(r"q(x_t \mid x_0) = \mathcal N\big(\sqrt{\bar\alpha_t}\, x_0,\ "
                                                 r"(1-\bar\alpha_t)\, I\big)", font_size=32),
                           who=r"any step $t$, \ without the $t - 1$ steps before it", width=7.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "You don't have to run the thousand steps to know where a point ends up. Write one step: the point "
            "shrunk, plus fresh noise. <bookmark mark='a'/> Substitute the step before it. <bookmark mark='b'/> The "
            "two noises are independent Gaussians, so their sum is one Gaussian whose variance is the sum of theirs. "
            "<bookmark mark='c'/> Keep going down to the clean point, and the whole chain collapses into a single "
            "jump: the data shrunk by the square root of alpha bar, plus noise of variance one minus alpha bar, "
            "where alpha bar is the product of all the shrink factors. <bookmark mark='d'/> So training can sample "
            "any noise level at once, without simulating the chain."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            step(3)
            vo.wait_until("d")
            self.play(FadeIn(box, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def check(self):
        f = load("forward")
        rows = f["checks"]
        abar = np.asarray(f["abar"])
        T = int(f["T"])
        g = axes([0, T], [0, 1.05], x_length=6.4, y_length=3.8, xlabel=r"step $t$", ylabel=r"measured on the chain",
                 xticks=[0, 250, 500, 750, 1000], yticks=[0, 0.5, 1], center=[-2.6, -0.3, 0])
        ts = np.arange(1, T + 1)
        c1 = curve(g.ax, ts[::5], np.sqrt(abar[::5]), DATA, 3)
        c2 = curve(g.ax, ts[::5], 1 - abar[::5], NOISE, 3)
        d1 = VGroup(*[Dot(g.ax.c2p(r["t"], r["slope"]), radius=0.07, color=WHITE).set_stroke(DATA, 2) for r in rows])
        d2 = VGroup(*[Dot(g.ax.c2p(r["t"], r["resid"]), radius=0.07, color=WHITE).set_stroke(NOISE, 2) for r in rows])
        lg = VGroup(label(r"$\sqrt{\bar\alpha_t}$: \ how much of $x_0$ is left", font_size=22, color=DATA),
                    label(r"$1 - \bar\alpha_t$: \ the noise's variance", font_size=22, color=NOISE),
                    label(r"dots: \ $20{,}000$ points run through all the steps", font_size=22, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).move_to([3.6, 1.6, 0])
        r5 = next(r for r in rows if r["t"] == 500)
        worst = max(max(abs(r["slope"] - r["slope_pred"]), abs(r["resid"] - r["resid_pred"])) for r in rows)
        sw_ok = all(r["sw_chain"] < 1.5 * r["sw_floor"] + 0.005 for r in rows)
        tab = VGroup(label(r"the chain's points against one jump's:", font_size=22, color=GREY_A),
                     *[label(rf"step ${r['t']:,}$: \ ${r['sw_chain']:.3f}$ \ (two jumps: ${r['sw_floor']:.3f}$)".replace(",", "{,}"),
                             font_size=20, color=WHITE) for r in rows]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        tab.move_to([3.6, -1.4, 0])
        man, ex = f"{float(f['abar_T']):.1e}".split("e")
        man, ex = float(man), -int(ex)
        left = math.sqrt(float(f["abar_T"]))
        verdict = ("and whole clouds agree as well as two independent jumps agree with each other."
                   if sw_ok else "and whole clouds agree nearly as well as two independent jumps do.")
        with self.voiceover(
            "Check it on our letters. Run twenty thousand points through all thousand steps, and at "
            f"{len(rows)} moments regress where they are on where they started. <bookmark mark='a'/> The slope should be the square root "
            f"of alpha bar: at step 500 it is {r5['slope']:.3f}, the formula says {r5['slope_pred']:.3f}. "
            f"<bookmark mark='b'/> The leftover variance should be one minus alpha bar: {r5['resid']:.3f} against "
            f"{r5['resid_pred']:.3f}. The largest gap anywhere is {worst:.3f}, <bookmark mark='c'/> {verdict} "
            f"After all thousand steps, alpha bar is {man:.1f} times ten to the minus {ex}: what is left of a point "
            f"is {left:.4f} of it."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg[2]))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(lg[0]), LaggedStart(*[FadeIn(x, scale=1.5) for x in d1], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(lg[1]), LaggedStart(*[FadeIn(x, scale=1.5) for x in d2], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(tab))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def posterior(self):
        rows = [
            cmath(r"q(x_{t-1} \mid x_t, x_0)", r"\propto", r"q(x_t \mid x_{t-1})\; q(x_{t-1} \mid x_0)", font_size=34),
            cmath(r"q(x_{t-1} \mid x_t, x_0)", r"=", r"\mathcal N\big(\tilde\mu_t,\ \tilde\beta_t I\big)", font_size=34),
            cmath(r"\tilde\mu_t", r"=", r"\frac{\sqrt{\bar\alpha_{t-1}}\,\beta_t}{1-\bar\alpha_t}\; x_0 + "
                  r"\frac{\sqrt{1-\beta_t}\,(1-\bar\alpha_{t-1})}{1-\bar\alpha_t}\; x_t, \qquad "
                  r"\tilde\beta_t = \frac{1-\bar\alpha_{t-1}}{1-\bar\alpha_t}\, \beta_t", font_size=30),
        ]
        whys = [why(r"Bayes: \ the step forward, \ times the jump to $t-1$"),
                why(r"two Gaussians in $x_{t-1}$: \ complete the square"), why(r"a blend of the clean point and the noisy one")]
        step = ladder(self, rows, whys, keep=3, top=2.7, x=-1.0, buff=0.6, edge=6.8)
        vp = VGroup(label(r"in continuous time:", font_size=24, color=GREY_A),
                    MathTex(r"x_t = \alpha_t\, x_0 + \sigma_t\, \varepsilon, \qquad \alpha_t^2 + \sigma_t^2 = 1", font_size=32),
                    label(r"variance preserving; \ ours: \ $\alpha_t = \cos(\pi t/2)$, \ $\sigma_t = \sin(\pi t/2)$, \ $t \in [0, 1]$",
                          font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15).move_to([0, -1.25, 0])
        ta = take_away(r"Given the clean point, every step back is a Gaussian we can write down. \ The model must do it "
                       r"without the clean point.")
        with self.voiceover(
            "One more fact, and the model's job is defined. Run a step backwards, and suppose you knew the clean "
            "point. <bookmark mark='a'/> Bayes says the previous point's distribution is the forward step times the "
            "jump to step t minus one: both Gaussian in the previous point, so completing the square gives a "
            "Gaussian, <bookmark mark='b'/> whose mean blends the clean point and the noisy one. <bookmark mark='c'/> "
            "In continuous time, write alpha for the shrink and sigma for the noise: their squares add to one. Ours "
            "is a quarter circle, cosine and sine, the forward process of Part 5's Ornstein-Uhlenbeck chapter run on "
            "a clock. <bookmark mark='d'/> Every step back is a known Gaussian, if you know where you started. The "
            "model has to manage without."
        ) as vo:
            step(0)
            vo.wait_until("a")
            step(1)
            vo.wait_until("b")
            step(2)
            vo.wait_until("c")
            self.play(FadeIn(vp, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(ta, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()
