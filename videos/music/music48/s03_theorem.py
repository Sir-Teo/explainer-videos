from __future__ import annotations

import numpy as np

from videos.music.music48.common import *  # noqa: F403


class Theorem(SoundScene):
    def construct(self):
        chapter(self, 2, r"The sampling theorem", r"How can samples hold everything between them?")
        self.statement()
        self.sincs()
        self.proof()
        self.truncation()
        self.history()

    # ------------------------------------------------------------------
    def statement(self):
        items = [
            (r"if a signal contains no frequency at or above $B$, \ samples taken $2B$ times a second determine it completely", WHITE),
            (r"not approximately: \ exactly, \ at every instant between the samples too", WHITE),
            (r"$f_s / 2$ is the Nyquist frequency; \ a signal must stay below it", WHITE),
            (r"it sounds impossible: \ infinitely many curves pass through any set of dots", TUNE),
            (r"but only one of them contains no frequency above $f_s/2$", GREY_A),
        ]
        rows_scene(self, r"a theorem that sounds impossible", items,
                   "Here is the theorem. If a signal contains no frequency at or above some limit B, then samples taken two B "
                   "times a second determine it completely. <bookmark mark='b'/> Not approximately: exactly, at every instant "
                   "between the samples too. <bookmark mark='c'/> Half the sample rate is called the Nyquist frequency; the "
                   "signal must stay below it. <bookmark mark='d'/> It sounds impossible: infinitely many curves pass through any "
                   "set of dots. <bookmark mark='e'/> But an infinite, exact sample sequence uniquely determines the strictly band-limited signal under the theorem's assumptions; a finite set of displayed points alone does not.",
                   marks="bcde")

    # ------------------------------------------------------------------
    def sincs(self):
        d = load("sampling")
        fs = d["fs"]
        n = np.array(d["n"])
        x = np.array(d["x"])
        ax = frame_axes(width=11.6, height=3.4, xlo=0.4, xhi=3.6, ylo=-1.3, yhi=1.3, center=DOWN * 0.3)
        keep = [(k, v) for k, v in zip(n, x) if 0.4 <= k / fs <= 3.6]
        st = stems([k / fs for k, _ in keep], [v for _, v in keep], ax.to, color=TUNE)
        tt = np.linspace(0.4, 3.6, 500)
        sinc_curves = VGroup()
        for k, v in keep[::1]:
            sinc_curves.add(curve(tt, v * np.sinc(fs * tt - k), ax.to, color=BLUE, width=1.5).set_stroke(opacity=0.55))
        from explainer.music.monochord import digital as DG
        total = DG.sinc_interp(x, fs, tt)
        tot = curve(tt, total, ax.to, color=WHITE, width=4)
        head = label(r"one sinc for every sample; \ their sum is the signal", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        eq = MathTex(r"x(t) = \sum_n x[n]\,\operatorname{sinc}(f_s t - n), \qquad \operatorname{sinc}(u) = \frac{\sin \pi u}{\pi u}", font_size=34).next_to(head, DOWN, buff=0.25)
        with self.voiceover(
            "Here is how the one curve is built. <bookmark mark='a'/> Take the samples of a signal that stays below the "
            "Nyquist frequency. <bookmark mark='b'/> At each sample, place a sinc function: sine of pi u over pi u, scaled by "
            "the sample's value. Each sinc is one at its own sample and exactly zero at every other sample. "
            "<bookmark mark='c'/> Add them all up. The sum passes through every sample, because only one sinc is non-zero "
            "there, and between the samples it is the original signal, with an error of "
            f"{say(d['max_err_full'], 3)} here, and that only because we used thirty-three samples instead of infinitely many."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(st))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in sinc_curves], lag_ratio=0.15), run_time=3.0)
            vo.wait_until("c")
            self.play(Create(tot), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def proof(self):
        W = 11.0
        def spec(y, color, centers, label_text, tag_color=GREY_A):
            ax = Line([-W / 2, y, 0], [W / 2, y, 0], color=GREY_B, stroke_width=1.5)
            g = VGroup(ax)
            for c in centers:
                pts = [[c - 0.9, y, 0], [c - 0.9, y + 0.2, 0], [c, y + 0.9, 0], [c + 0.9, y + 0.2, 0], [c + 0.9, y, 0]]
                g.add(Polygon(*pts, stroke_color=color, stroke_width=2, fill_color=color, fill_opacity=0.35))
            g.add(label(label_text, font_size=17, color=tag_color).move_to([-W / 2, y + 1.15, 0], aligned_edge=LEFT))
            return g
        a = spec(1.0, TUNE, [0.0], r"the signal's spectrum: \ nothing above $B$")
        b = spec(-1.2, BLUE, [-4.0, 0.0, 4.0], r"the samples' spectrum: \ copies every $f_s$, \ separate when $f_s > 2B$")
        box = Rectangle(width=4.0, height=1.0, stroke_color=WHITE, stroke_width=3).move_to([0, -0.78, 0])
        lp = label(r"keep only the middle copy: \ an ideal low-pass, \ whose impulse response is the sinc", font_size=18, color=WHITE).to_edge(DOWN, buff=0.4)
        ticks = VGroup(*[label(t, font_size=15, color=GREY_A).move_to([v, -1.5, 0]) for t, v in ((r"$-f_s$", -4.0), (r"$0$", 0.0), (r"$f_s$", 4.0))])
        head = label(r"why it works", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Why does it work? Think in frequencies, as Part 3 taught. <bookmark mark='a'/> The signal's spectrum has nothing "
            "above B. <bookmark mark='b'/> Sampling multiplies the signal by a train of spikes, and the spectrum of the samples "
            "is the signal's spectrum copied again and again, once every f s. If f s is more than twice B, the copies do not "
            "touch. <bookmark mark='c'/> Then keep only the middle copy with an ideal low-pass filter, and you have the "
            "original spectrum, so the original signal. The ideal low-pass filter's response to a single spike is exactly the "
            "sinc, which is why the sum of sincs works."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(a))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(ticks))
            vo.wait_until("c")
            self.play(Create(box), FadeIn(lp))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def truncation(self):
        d = load("sampling")
        e = d["taps_error"]
        keys = list(e)
        bars = VGroup()
        x0 = -3.5
        for i, k in enumerate(keys):
            v = e[k]
            h = 0.5 * (np.log10(v) + 5)
            y = -1.8
            bars.add(VGroup(Rectangle(width=0.9, height=max(h, 0.05), stroke_width=0, fill_color=TUNE, fill_opacity=0.85).move_to([x0 + 1.4 * i, y + h / 2, 0]),
                            label(k, font_size=19, color=WHITE).move_to([x0 + 1.4 * i, y - 0.3, 0]),
                            label(f"{v:.1e}".replace("e-0", r"e-"), font_size=15, color=GREY_A).move_to([x0 + 1.4 * i, y + h + 0.25, 0])))
        axl = label(r"samples used for each output point", font_size=17, color=GREY_A).move_to([x0 + 3.5, -2.6, 0])
        yl = label(r"largest error \ (log scale)", font_size=17, color=GREY_A).move_to([x0 - 1.6, 0.5, 0])
        head = label(r"a real filter uses finitely many samples", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        ks = keys
        with self.voiceover(
            "A real converter cannot add up infinitely many sincs: it uses a window of nearby samples. How much does that "
            f"cost? <bookmark mark='a'/> With {ks[0]} samples, the largest error is {say(e[ks[0]], 2)}, a quarter of the "
            f"signal. With {ks[2]}, {say(e[ks[2]], 2)}. With {ks[4]}, {say(e[ks[4]], 4)}. With {ks[5]}, about four in a "
            "hundred thousand. Every doubling buys accuracy, and a real interpolation filter uses enough to put the error "
            "below the noise. The theorem is exact; its engineering is a trade-off you can measure."
        ) as vo:
            self.play(FadeIn(head), FadeIn(axl), FadeIn(yl), FadeIn(ghost(bars, 0.15)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"Edmund Whittaker \ (1915): \ the interpolating series of sincs, \ as a problem in pure mathematics", WHITE),
            (r"Harry Nyquist \ (1928): \ a channel of bandwidth $B$ carries at most $2B$ independent pulses a second", WHITE),
            (r"Vladimir Kotelnikov \ (1933) \ and Claude Shannon \ (1949): \ the theorem for communication, \ with proof", WHITE),
            (r"the same idea runs through every digital camera, \ telephone and scanner", TUNE),
            (r"its fine print is the rest of this part: \ the signal must really be band-limited", GREY_A),
        ]
        rows_scene(self, r"many fathers", items,
                   "The theorem has many fathers. <bookmark mark='b'/> Edmund Whittaker found the series of sincs in 1915, as "
                   "pure mathematics. <bookmark mark='c'/> Harry Nyquist showed in 1928 that a channel of bandwidth B carries at "
                   "most two B independent pulses a second. <bookmark mark='d'/> Vladimir Kotelnikov in 1933 and Claude Shannon "
                   "in 1949 stated it for communication, with proof. <bookmark mark='e'/> The same idea runs through every "
                   "digital camera, telephone and scanner. <bookmark mark='f'/> Its fine print is the rest of this part: the "
                   "signal must really contain nothing above the Nyquist frequency.", marks="bcdef")
