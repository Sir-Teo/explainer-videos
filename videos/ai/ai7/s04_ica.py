from __future__ import annotations

import numpy as np

from explainer.ai import *  # noqa: F403
from videos.ai.ai7.common import PART, VOICE1, VOICE2, card_in, load

MIC = GREY_B
KURT = C.SURPRISE


def wave(t, y, width=4.4, height=0.9, color=WHITE, stroke_width=2.5, n=400) -> VMobject:
    t, y = np.asarray(t)[:n], np.asarray(y)[:n]
    xs = (t - t[0]) / (t[-1] - t[0]) * width - width / 2
    ys = y / max(np.abs(y).max(), 1e-9) * height / 2
    return VMobject(color=color, stroke_width=stroke_width).set_points_as_corners([[a, b, 0] for a, b in zip(xs, ys)])


class ICA(VoiceoverScene):
    def construct(self):
        card_in(self, 3, r"The cocktail party", r"Two voices, two microphones: can we unmix them?",
                "Chapter three. The cocktail party.")
        self.problem()
        self.rotate()
        self.result()

    # ------------------------------------------------------------------
    def problem(self):
        d = load("ica")
        t, S, X, A = np.asarray(d["t"]), np.asarray(d["S"]), np.asarray(d["X"]), np.asarray(d["A"])
        vs = VGroup(wave(t, S[0], color=VOICE1), wave(t, S[1], color=VOICE2)).arrange(DOWN, buff=0.7).move_to([-3.8, 0.6, 0])
        ms = VGroup(wave(t, X[0], color=MIC), wave(t, X[1], color=MIC)).arrange(DOWN, buff=0.7).move_to([3.8, 0.6, 0])
        vl = VGroup(label(r"voice 1", font_size=24, color=VOICE1).next_to(vs[0], UP, buff=0.12),
                    label(r"voice 2", font_size=24, color=VOICE2).next_to(vs[1], UP, buff=0.12))
        ml = VGroup(label(r"microphone 1", font_size=24, color=MIC).next_to(ms[0], UP, buff=0.12),
                    label(r"microphone 2", font_size=24, color=MIC).next_to(ms[1], UP, buff=0.12))
        mix = VGroup(*[Arrow(vs[i].get_right(), ms[j].get_left(), buff=0.25, color=VOICE1 if i == 0 else VOICE2,
                             stroke_width=1.5 + 3 * A[j, i], max_tip_length_to_length_ratio=0.06)
                       for i in range(2) for j in range(2)])
        eq = cmath(r"x", r"=", r"A", r"\,s", colors={r"x": MIC, r"A": GREY_A, r"\,s": VOICE1}, font_size=48)
        eq.to_edge(DOWN, buff=1.0)
        unk = label(r"we hear $x$; \ both $A$ and $s$ are unknown", font_size=26, color=GREY_A).next_to(eq, DOWN, buff=0.2)
        tag = note(r"illustrative signals: \ a tone and a sawtooth", font_size=20).to_corner(UR, buff=0.3)
        h = history_card(1953, r"Colin Cherry", r"how do we follow one voice at a party? \ the cocktail-party "
                         r"problem", width=5.4).move_to([0, 2.6, 0])
        with self.voiceover(
            "In 1953 the psychologist Colin Cherry asked how we manage to follow one voice in a noisy room: the "
            "cocktail party problem. <bookmark mark='a'/> Here's a machine's version. Two people talk at once. "
            "<bookmark mark='b'/> Two microphones each hear a different blend of the two, louder for whoever is "
            "nearer. <bookmark mark='c'/> In symbols, x equals A times s: the sounds we record are a mixing matrix "
            "times the voices. But we know neither the matrix nor the voices. All we have is x."
        ) as vo:
            self.play(FadeIn(h, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(h), Create(vs[0]), Create(vs[1]), FadeIn(vl), FadeIn(tag), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in mix], lag_ratio=0.15), Create(ms[0]), Create(ms[1]),
                      FadeIn(ml), run_time=2.5)
            vo.wait_until("c")
            self.play(Write(eq), FadeIn(unk))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rotate(self):
        d = load("ica")
        X, Xw = np.asarray(d["X"]), np.asarray(d["Xw"])
        th, kurt, ang = np.asarray(d["theta"]), np.asarray(d["kurt"]), np.asarray(d["ang"])
        km = np.asarray(d["kurt_mix"])
        sub = np.arange(0, X.shape[1], 2)

        def scatter(P, center, size=3.0, color=MIC):
            lim = 3.0
            pts = np.clip(P[:, sub].T, -lim, lim) / lim * size / 2
            frame = Square(size + 0.15, stroke_color=GREY_D, stroke_width=1).move_to(center)
            return VGroup(frame, VGroup(*[Dot(np.array([x, y, 0]) + center, radius=0.025, color=color,
                                              fill_opacity=0.75) for x, y in pts]))

        Xc = X - X.mean(1, keepdims=True)
        Xs = Xc / Xc.std()
        left = scatter(Xs * 1.4, np.array([-4.6, 0.6, 0]))
        mid = scatter(Xw, np.array([-0.9, 0.6, 0]))
        ll = label(r"the two microphones, \\ moment by moment", font_size=22, color=GREY_A).next_to(left, DOWN, buff=0.15)
        mlab = label(r"whitened (PCA): \\ uncorrelated, \ still mixed", font_size=22, color=GREY_A).next_to(mid, DOWN, buff=0.15)
        g = axes([0, np.pi, 1], [float(kurt.min()) - 0.1, 0.2, 0.5], x_length=4.2, y_length=2.6,
                 xlabel=r"angle of the unmixing direction", ylabel=r"kurtosis", center=[4.4, 0.9, 0])
        ax = g.ax
        kc = curve(ax, th, kurt, KURT, 3)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(np.pi, 0), color=GREY_C, stroke_width=1.5)
        zl = label(r"a Gaussian: \ $0$", font_size=18, color=GREY_B).next_to(zero, UP, buff=0.05).align_to(zero, RIGHT)
        k = ValueTracker(0)
        c0 = mid[0].get_center()

        def wline():
            a = ang[min(int(round(k.get_value())), len(ang) - 1)]
            u = np.array([np.cos(a), np.sin(a), 0])
            return Line(c0 - 1.6 * u, c0 + 1.6 * u, color=VOICE1, stroke_width=4)

        def wdot():
            a = ang[min(int(round(k.get_value())), len(ang) - 1)]
            return glow_dot(ax.c2p(a, float(np.interp(a, th, kurt))), color=VOICE1, radius=0.07)

        wl = always_redraw(wline)
        wd = always_redraw(wdot)
        kdef = cmath(r"\mathrm{kurt}(y)", r"=", r"\mathbb{E}[y^4] - 3", font_size=34).move_to([4.4, -1.4, 0])
        kn = label(r"$0$ for a bell curve; \ negative for a tone or a sawtooth", font_size=20, color=GREY_A)
        kn.next_to(kdef, DOWN, buff=0.15)
        clt = label(rf"excess kurtosis: \ ${d['kurt_mix'][0]:.2f}$ and ${d['kurt_mix'][1]:.2f}$ "
                    rf"for the whitened mixes, \ ${d['kurt_src'][0]:.2f}$ and ${d['kurt_src'][1]:.2f}$ for the voices",
                    font_size=22, color=C.BITS).to_edge(DOWN, buff=0.35)
        ks = np.asarray(d["kurt_src"])
        if (np.abs(km) < np.abs(ks).min()).all():
            clt_say = (f"The voices have kurtosis {ks[0]:.2f} and {ks[1]:.2f}; the whitened mixtures, {km[0]:.2f} and "
                       f"{km[1]:.2f}, sit closer to zero.")
        else:
            clt_say = (f"Here the voices have kurtosis {ks[0]:.2f} and {ks[1]:.2f}, and the whitened mixtures "
                       f"{km[0]:.2f} and {km[1]:.2f}.")
        unc = label(r"uncorrelated $\neq$ independent: \\ turned by any angle, \\ a white cloud stays white", font_size=24,
                    color=GREY_A).move_to([4.3, 0.8, 0])
        it = label(rf"FastICA: \ ${d['iters']}$ fixed-point steps", font_size=22, color=VOICE1).next_to(g, DOWN, buff=0.1)
        with self.voiceover(
            "Plot the two microphones against each other, moment by moment, and the mixing shows as a slanted, "
            "squashed shape. <bookmark mark='a'/> First, whiten: chapter one's principal components, rescaled to "
            "unit spread. The two outputs are now uncorrelated. But they're still mixed: turn this white cloud by "
            "any angle, and it stays uncorrelated, so correlation alone can never tell us which way is right. "
            "<bookmark mark='b'/> The central limit theorem motivates looking for non-Gaussian directions in "
            "mixtures of independent signals. Here the contrast is excess kurtosis: for a centered, unit-variance "
            "output, the fourth moment minus three. A Gaussian gives zero, though zero alone does not prove "
            "Gaussianity. " + clt_say +
            f" <bookmark mark='c'/> So turn the direction until the output is as far from Gaussian as "
            f"possible. Aapo Hyvärinen's FastICA does it with a fixed-point step; here we record "
            f"{d['iters']} fixed-point steps."
        ) as vo:
            self.play(FadeIn(left), FadeIn(ll), run_time=1.5)
            vo.wait_until("a")
            self.play(TransformFromCopy(left, mid), FadeIn(mlab), run_time=1.8)
            self.play(Rotate(mid[1], angle=0.6, about_point=c0), run_time=1.5)
            self.play(Rotate(mid[1], angle=-0.6, about_point=c0), FadeIn(unc), run_time=1.0)
            vo.wait_until("b")
            self.play(FadeOut(unc))
            self.play(FadeIn(g), Create(kc), Create(zero), FadeIn(zl), FadeIn(kdef), FadeIn(kn))
            self.play(FadeIn(clt))
            vo.wait_until("c")
            self.play(Create(wl), FadeIn(wd))
            self.play(k.animate.set_value(len(ang) - 1), FadeIn(it), run_time=3.0, rate_func=linear)
            wl.clear_updaters()
            wd.clear_updaters()
            self.play(Rotate(VGroup(mid[1], wl), angle=-float(ang[-1]), about_point=c0), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def result(self):
        d = load("ica")
        t, S, Y = np.asarray(d["t"]), np.asarray(d["S"]), np.asarray(d["Y"])
        r_ica, r_pca, r_mic = (np.asarray(d[k]) for k in ("r_ica", "r_pca", "r_mic"))
        tw = VGroup()
        for i, col in enumerate((VOICE1, VOICE2)):
            true = wave(t, S[i], width=6.2, height=1.0, color=col, stroke_width=5).set_stroke(opacity=0.45)
            rec = DashedVMobject(wave(t, Y[i], width=6.2, height=1.0, color=WHITE, stroke_width=2), num_dashes=120)
            tw.add(VGroup(true, rec))
        tw.arrange(DOWN, buff=0.8).move_to([-3.0, 1.0, 0])
        tl = VGroup(label(r"voice 1 (wide) \ and what ICA recovered (dashed)", font_size=22, color=VOICE1).next_to(tw[0], UP, buff=0.12),
                    label(r"voice 2", font_size=22, color=VOICE2).next_to(tw[1], UP, buff=0.12))
        rows = VGroup(
            label(r"correlation, \ one-to-one matching to the two voices:", font_size=24, color=GREY_A),
            label(rf"a microphone: \ ${r_mic.min():.2f}$ and ${r_mic.max():.2f}$", font_size=26, color=MIC),
            label(rf"PCA (whitening): \ ${r_pca.min():.2f}$ and ${r_pca.max():.2f}$", font_size=26, color=GREY_A),
            label(rf"ICA: \ ${r_ica.min():.4f}$ and ${r_ica.max():.4f}$", font_size=26, color=C.BITS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([-3.0, -2.2, 0])
        hist = VGroup(
            history_card(1986, r"J.~H\'erault \& C.~Jutten", r"blind separation with a neural circuit", width=4.6),
            history_card(1995, r"A.~Bell \& T.~Sejnowski", r"infomax ICA; \ in 1997, ICA of natural images gives edge "
                         r"detectors", width=4.6),
            history_card(1999, r"A.~Hyv\"arinen", r"FastICA", width=4.6),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to([4.3, 0.4, 0])
        use = label(r"today: \ cleaning brain recordings; \\ sparse dictionaries of features (Part 30)", font_size=22,
                    color=GREY_A).next_to(hist, DOWN, buff=0.25)
        good = r_ica.min() > 0.99
        verdict = (f"The two outputs follow the voices with correlations of {r_ica.min():.4f} and better. Whitening alone "
                   f"managed only {r_pca.max():.2f}." if good else
                   f"The outputs follow the voices with correlations of {r_ica.min():.2f} and {r_ica.max():.2f}.")
        with self.voiceover(
            "Turn the white cloud to that angle, and read off the two outputs. <bookmark mark='a'/> " + verdict +
            " <bookmark mark='b'/> Independent component analysis grew from Jeanny Hérault and Christian Jutten's "
            "circuits in the 1980s, through Pierre Comon's definition in 1994 and Bell and Sejnowski's infomax. Run "
            "on patches of natural images, it finds edge detectors like those in the visual cortex. Today it cleans "
            "eye blinks out of brain recordings, and its idea, find the directions in which the data is sparse and "
            "independent, is the dictionary learning behind part thirty's sparse autoencoders."
        ) as vo:
            self.play(Create(tw[0][0]), Create(tw[1][0]), FadeIn(tl), run_time=1.5)
            self.play(Create(tw[0][1]), Create(tw[1][1]), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(h, shift=LEFT * 0.2) for h in hist], lag_ratio=0.4), run_time=2.5)
            self.play(FadeIn(use))
        self.wait(0.3)
        self.clear_scene()
