from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai11.common import OPT_COLORS, PART, SCHED_COLORS, bits_axes, growing, lag, load, step_counter, takeaway_card

CON, COS, WSD, EMA, SF = (SCHED_COLORS[k] for k in ("constant", "cosine", "wsd", "ema", "sf"))


class ScheduleFree(VoiceoverScene):
    def construct(self):
        self.card()
        self.average()
        self.ema()
        self.derive()
        self.measure()
        self.takeaway()

    def card(self):
        c = chapter_card(14, r"Without a schedule", r"Can averaging replace the decay?", part=PART)
        with self.voiceover("Chapter fourteen. Without a schedule."):
            self.play(FadeIn(c[0], shift=UP * 0.2), FadeIn(c[1]))
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def average(self):
        d = load("noise")
        from videos.ai.ai11.s04_sgd import B_COLORS, loss_axes

        ax, cont, star = loss_axes(d, center=(-3.3, 0.2), width=5.8)
        w1, w2 = np.asarray(d["w1"]), np.asarray(d["w2"])
        cl = np.asarray(d["cloud1"])
        cl = cl[(cl[:, 0] > w1[0]) & (cl[:, 0] < w1[-1]) & (cl[:, 1] > w2[0]) & (cl[:, 1] < w2[-1])]
        dots = VGroup(*[Dot(ax.c2p(*p), radius=0.022, color=B_COLORS[1], fill_opacity=0.6) for p in cl])
        avg = np.cumsum(cl, 0) / np.arange(1, len(cl) + 1)[:, None]
        ap = VMobject(color=WHITE, stroke_width=3).set_points_as_corners([ax.c2p(*p) for p in avg[5:]])
        ad = Dot(ax.c2p(*avg[-1]), radius=0.08, color=WHITE)
        gap_cloud = float(np.sqrt(((cl - d["w_star"]) ** 2).sum(1).mean()))
        gap_avg = float(np.sqrt(((avg[-1] - d["w_star"]) ** 2).sum()))
        cap = label(rf"the cloud: \ typically ${gap_cloud:.2f}$ from the best weights; \ its average: \ ${gap_avg:.3f}$",
                    font_size=20, color=GREY_A).next_to(ax, DOWN, buff=0.15)
        eqs = VGroup(cmath(r"\bar\theta_k", "=", r"\frac{1}{k}\sum_{i \le k} \theta_i", font_size=36),
                     cmath(r"\bar\theta_k", r"\leftarrow", r"\beta\,\bar\theta_{k-1} + (1 - \beta)\,\theta_k", font_size=36,
                           colors={r"\beta\,\bar\theta_{k-1} + (1 - \beta)\,\theta_k": EMA}))
        eqs.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([3.3, 1.2, 0])
        notes = VGroup(label(r"Polyak \& Juditsky (1992), \ Ruppert (1988): \ the running mean", font_size=20, color=GREY_A),
                       label(r"an exponential moving average (EMA): \ forgets the start", font_size=20, color=EMA))
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, DOWN, buff=0.15).align_to(e_, LEFT)
        keep_in_frame(VGroup(eqs, notes))
        with self.voiceover(
            "Go back to Chapter three's cloud. The walker never settles, but the cloud is centred on the answer. "
            "<bookmark mark='a'/> So don't take the last position: take the average of all of them. David Ruppert, "
            "and Boris Polyak with Anatoli Juditsky, proved around 1990 that this averaged walker converges as fast "
            f"as anything can. Here the cloud's points are typically {gap_cloud:.2f} from the best weights; their "
            f"running average ends {gap_avg:.3f} away. <bookmark mark='b'/> Deep learning uses a version that forgets "
            "the start: an exponential moving average of the weights."
        ) as vo:
            self.play(Create(cont), FadeIn(star), lag([FadeIn(p) for p in dots], lag_ratio=0.003), run_time=2)
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(notes[0]))
            self.play(Create(ap), FadeIn(ad), FadeIn(cap), run_time=2)
            vo.wait_until("b")
            self.play(Write(eqs[1]), FadeIn(notes[1]))
        self.wait(0.3)
        self.clear_scene()

    def ema(self):
        s = load("schedule")
        sd = list(s["seeds"])[0]
        const, ema = np.asarray(s[f"const_{sd}"]), np.asarray(s[f"ema_{sd}"])
        S = int(max(s["lengths"]))
        cos = np.asarray(s[f"cos_{S}_{sd}"])
        wsd = np.asarray(s[f"wsdcurve_{S}_{sd}"])
        allv = np.concatenate([const[const[:, 0] >= 1000, 1], ema[ema[:, 0] >= 1000, 1], cos[cos[:, 0] >= 1000, 1]])
        lo, hi = float(allv.min()) - 0.02, float(allv.max()) + 0.02
        g = bits_axes([1000, S], [lo, hi], x_length=7.4, y_length=4.4, center=[-2.3, -0.4, 0], x_step=1000,
                      y_step=round((hi - lo) / 4, 3), yfmt=lambda v: f"{v:.2f}")
        ax = g.ax
        sel = lambda c: c[c[:, 0] >= 1000]  # noqa: E731
        lines = [curve(ax, sel(const)[:, 0], sel(const)[:, 1], CON, 2.5), curve(ax, sel(ema)[:, 0], sel(ema)[:, 1], EMA, 3.5),
                 curve(ax, sel(cos)[:, 0], np.clip(sel(cos)[:, 1], lo, hi), COS, 2.5),
                 curve(ax, wsd[:, 0], np.clip(wsd[:, 1], lo, hi), WSD, 3)]
        lg = VGroup(label(r"the constant-rate run", font_size=22, color=CON),
                    label(r"an EMA of its weights, \ $\beta = 0.998$", font_size=22, color=EMA),
                    label(rf"cosine to ${S:,}$".replace(",", "{,}"), font_size=22, color=COS),
                    label(r"its cool-down branch", font_size=22, color=WSD)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
        lg.move_to([4.6, 1.4, 0])
        e_end, c_end = float(ema[-1, 1]), float(const[-1, 1])
        w_end = float(wsd[-1, 1])
        res = label(rf"at step ${S:,}$: \\ raw ${c_end:.3f}$, \ EMA ${e_end:.3f}$, \ cool-down ${w_end:.3f}$".replace(",", "{,}"),
                    font_size=22, color=WHITE).next_to(lg, DOWN, buff=0.45).align_to(lg, LEFT)
        keep_in_frame(res)
        tag = note(r"the same runs as Chapter 13, \ seed $0$; \ held-out bits on $20{,}000$ characters").to_corner(DL, buff=0.2)
        gain = c_end - e_end
        share = gain / max(1e-9, c_end - w_end)
        said1 = (f"The averaged weights are better than the raw ones by {gain:.3f} bits at the end: "
            f"{share:.0%} of what the cool-down gained, without touching the learning rate. "
            if gain > 0 else
            f"Here the average is no better than the raw weights, {e_end:.3f} against {c_end:.3f}. ")
        with self.voiceover(
            "Apply it to Chapter thirteen's constant-rate run: keep an average of the weights with a memory of about "
            "five hundred steps, and score the average instead. <bookmark mark='a'/> "
            + said1
            + "Averaging and decaying are two ways of removing the same noise."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag), Create(lines[0]), FadeIn(lg[0]), Create(lines[2]), FadeIn(lg[2]),
                      Create(lines[3]), FadeIn(lg[3]))
            vo.wait_until("a")
            self.play(Create(lines[1]), FadeIn(lg[1]), run_time=2)
            self.play(FadeIn(res))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def derive(self):
        hist = history_card(2024, r"Aaron Defazio, Xingyu Yang, \dots, Ashok Cutkosky \ (Meta and others)",
                            r"\textit{The Road Less Scheduled}: \ schedule-free SGD and AdamW. \ Won AlgoPerf's "
                            r"self-tuning track", width=6.4).to_corner(UL, buff=0.35)
        cl = {r"y_t": SF, r"x_t": WHITE, r"z_t": OPT_COLORS["adam"]}
        rows = VGroup(
            cmath(r"y_t", "=", r"(1 - \beta)\, z_t + \beta\, x_t", colors=cl, font_size=34),
            cmath(r"z_{t+1}", "=", r"z_t - \gamma\, \nabla \ell(y_t)", colors=cl, font_size=34),
            cmath(r"x_{t+1}", "=", r"(1 - c_{t+1})\, x_t + c_{t+1}\, z_{t+1}", r",\quad c_{t+1} = \frac{\gamma_t^2}{\sum_{i \le t}\gamma_i^2}",
                  colors=cl, font_size=34),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(hist, DOWN, buff=0.45).align_to(hist, LEFT)
        notes = VGroup(label(r"where the gradient is taken: \ between the two", font_size=20, color=SF),
                       label(r"a fast walker, \ never decayed (Adam-scaled in practice)", font_size=20, color=OPT_COLORS["adam"]),
                       label(r"its running average: \ the model that is used", font_size=20, color=WHITE))
        for n_, r_ in zip(notes, rows):
            n_.next_to(r_, RIGHT, buff=0.35)
            keep_in_frame(n_)
        ends = label(r"$\beta = 0$: \ plain averaging; \ $\beta = 1$: \ gradients at the average itself; \ in practice "
                     r"$\beta = 0.9$", font_size=22, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "In 2024 Aaron Defazio and colleagues turned averaging into an optimizer with no schedule at all. "
            "<bookmark mark='a'/> Keep two sets of weights: a fast walker z, stepped at a constant rate, "
            "<bookmark mark='b'/> and its running average x, which is the model you use. <bookmark mark='c'/> The "
            "trick is where the gradient is taken: at y, a point between the two. With beta at zero it is plain "
            "averaging; at one, the gradient is taken at the average itself; nine tenths works in practice. "
            "Schedule-free AdamW won the self-tuning track of AlgoPerf in 2024, about eight percent faster than the "
            "baseline, with no learning-rate schedule to tune."
        ) as vo:
            self.play(FadeIn(hist, shift=RIGHT * 0.2), Write(rows[1]))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(Write(rows[2]), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(Write(rows[0]), FadeIn(notes[0]), FadeIn(ends))
        self.wait(0.3)
        self.clear_scene()

    def measure(self):
        s = load("schedule")
        seeds = list(s["seeds"])
        Ls = list(s["lengths"])
        S = max(Ls)
        sf = [np.asarray(s[f"sf_{sd}"]) for sd in seeds]
        allv = np.concatenate([c[c[:, 0] >= 500, 1] for c in sf])
        lo, hi = float(allv.min()) - 0.04, float(allv.max()) + 0.04
        g = bits_axes([0, S], [lo, hi], x_length=7.0, y_length=4.4, center=[-2.6, -0.4, 0], x_step=1000,
                      y_step=round((hi - lo) / 4, 3), yfmt=lambda v: f"{v:.2f}")
        ax = g.ax
        t = ValueTracker(0)
        live = [growing(ax, c[:, 0], np.clip(c[:, 1], lo, hi), t, SF, 3) for c in sf[:1]]
        mean = lambda key: float(np.mean([s[f"{key}_{sd}"] for sd in seeds]))  # noqa: E731
        # every number on the same 20,000 held-out characters the curves are scored on
        cos20 = {S_: float(np.mean([np.asarray(s[f"cos_{S_}_{sd}"])[-1, 1] for sd in seeds])) for S_ in Ls}
        wsd20 = {S_: mean(f"wsdquick_{S_}") for S_ in Ls}
        sf_at = {S_: float(np.mean([np.interp(S_, c[:, 0], c[:, 1]) for c in sf])) for S_ in Ls}
        pts = VGroup()
        for S_ in Ls:
            for v, col in ((cos20[S_], COS), (wsd20[S_], WSD)):
                if lo < v < hi:
                    pts.add(Dot(ax.c2p(S_, v), radius=0.08, color=col))
        cnt = step_counter(t, ax.get_corner(UR), DL)
        rows = VGroup(label(r"held-out bits, \ mean of $2$ seeds", font_size=20, color=GREY_A))
        for S_ in Ls:
            rows.add(label(rf"${S_:,}$: \ schedule-free ${sf_at[S_]:.3f}$, \ cosine ${cos20[S_]:.3f}$, \ "
                           rf"WSD ${wsd20[S_]:.3f}$".replace(",", "{,}"), font_size=20, color=WHITE))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to([3.9, 1.2, 0])
        keep_in_frame(rows)
        lg = VGroup(label(r"schedule-free AdamW, \ one run, \ scored anytime", font_size=20, color=SF),
                    label(r"dots: \ cosine runs and cool-downs at each length", font_size=20, color=GREY_A))
        lg.arrange(DOWN, aligned_edge=LEFT, buff=0.1).next_to(rows, DOWN, buff=0.4).align_to(rows, LEFT)
        note_ = note(r"every number here on the same $20{,}000$ held-out characters").to_corner(DL, buff=0.2)
        mb = float(s["sf_best"])
        gaps = [sf_at[S_] - min(cos20[S_], wsd20[S_]) for S_ in Ls]
        if all(gp < -0.01 for gp in gaps):
            verdict = (f"one schedule-free run beats the best scheduled run at every length, by {-max(gaps):.3f} to "
                       f"{-min(gaps):.3f} bits.")
        elif all(abs(gp) <= 0.01 for gp in gaps):
            verdict = "at every length, one schedule-free run matches the best scheduled run trained for that length."
        elif gaps[-1] < gaps[0]:
            verdict = "it trails the scheduled runs early on, and closes most of the gap by the longest length."
        else:
            verdict = ("on our model it trails the tuned schedules at every length, by "
                       f"{min(gaps):.3f} to {max(gaps):.3f} bits.")
        edge = " Its best rate was at the edge of our grid, so it might do a little better." if bool(s["sf_edge"]) else ""
        Sm = max(Ls)
        f_sf, f_cos, f_wsd = mean("sffinal"), mean(f"cosfinal_{Sm}"), mean(f"wsdfinal_{Sm}")
        with self.voiceover(
            "Does it work here? Schedule-free AdamW on our character model, its learning rate chosen from four "
            f"multiples of AdamW's, the best being {mb:g} times. One run of {S:,} steps, scored as it goes, against "
            "the scheduled runs of Chapter thirteen, each trained for one length. <bookmark mark='a'/> The verdict: "
            f"{verdict} <bookmark mark='e'/>{edge} <bookmark mark='b'/> Checked on all our held-out text at "
            f"{Sm:,} steps: schedule-free {f_sf:.3f} bits, cosine {f_cos:.3f}, warmup–stable–decay {f_wsd:.3f}."
        ) as vo:
            self.play(FadeIn(g), FadeIn(lg), FadeIn(note_))
            self.add(*live, cnt)
            self.play(t.animate.set_value(S), FadeIn(pts), run_time=5.0, rate_func=linear)
            for m_ in live + [cnt]:
                m_.clear_updaters()
            vo.wait_until("a")
            self.play(lag([FadeIn(r_) for r_ in rows], lag_ratio=0.25), run_time=2)
            vo.wait_until("b")
            self.play(Indicate(rows[-1], color=WHITE))
        self.wait(0.3)
        self.clear_scene()

    def takeaway(self):
        t = takeaway_card(r"Averaging is a schedule",
                          r"The mean of a noisy walk sits near the bottom of its cloud. \ An EMA of the weights, \ and "
                          r"schedule-free's interpolation, \ remove the noise a decay would.",
                          r"Next: \ when training blows up")
        with self.voiceover(
            "So averaging the weights removes the same noise a decaying schedule does, and schedule-free methods "
            "build that in. Next: what happens when training doesn't just wander, but blows up."
        ):
            self.play(FadeIn(t[0], shift=UP * 0.2))
            self.play(FadeIn(t[1]))
        self.wait(0.3)
        self.clear_scene()
