from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.quantum2.common import (corner_wheel, hue, label, ladder, load, mtex, note, phase_img, phasor_chain, plain_axes,
                                    polyline, why)
from videos.quantum2.compute import STAT


class StationaryPhase(VoiceoverScene):
    def construct(self):
        self.family()
        self.cornu()
        self.plane()
        self.euler_lagrange()
        self.numbers()

    # ------------------------------------------------------------------
    def _paths_panel(self, hb, center=LEFT * 3.5 + DOWN * 0.4, n=15):
        s = load("stationary")
        T, g = STAT["T"], STAT["g"]
        ts = s["ts"]
        xcl = s["xcl"]
        ax = plain_axes((0, T), (-1.7, 2.2), 5.6, 4.6).move_to(center)
        tl = MathTex("t", font_size=30, color=C.QTIME).next_to(ax.x_axis.get_end(), RIGHT, buff=0.1)
        xl = MathTex("x", font_size=30, color=C.XPOS).next_to(ax.y_axis.get_end(), UP, buff=0.1)
        aa = np.linspace(-1.4, 1.4, n)
        paths = VGroup()
        for a in aa:
            dS = np.pi**2 * a * a / (4 * T)
            paths.add(polyline(ax, ts[::20], (xcl + a * np.sin(np.pi * ts / T))[::20], color=hue(dS / hb), stroke_width=2.2))
        cl = polyline(ax, ts[::20], xcl[::20], color=C.CLASSICAL, stroke_width=5)
        return ax, VGroup(tl, xl), paths, cl, aa

    def family(self):
        hb = STAT["hbars"][1]
        ax, labs, paths, cl, aa = self._paths_panel(hb)
        cll = label(r"classical", font_size=24, color=C.CLASSICAL).next_to(ax.c2p(1.0, 0.5), UP, buff=0.1)
        q = label(r"if every path counts, why does a ball follow just one?", font_size=32).to_edge(UP, buff=0.3)
        fam = MathTex(r"x_a(t) = x_{\text{cl}}(t) + a\,\sin(\pi t/T)", font_size=30).next_to(ax, DOWN, buff=0.25)
        s = load("stationary")
        sax = plain_axes((-1.6, 1.6), (0, 3.4), 5.4, 3.6).move_to(RIGHT * 3.4 + DOWN * 0.3)
        a = s["a"]
        Sc = polyline(sax, a, s["S"] - float(s["Scl"]), color=C.ACTION, stroke_width=4)
        Sl = MathTex(r"S(a) - S_{\text{cl}}", font_size=30, color=C.ACTION).next_to(sax.c2p(-1.6, 3.4), RIGHT, buff=0.1)
        al = MathTex("a", font_size=30).next_to(sax.x_axis.get_end(), RIGHT, buff=0.1)
        exact = MathTex(r"= \frac{\pi^2 a^2}{4T}", font_size=32, color=C.ACTION).next_to(Sl, RIGHT, buff=0.15)
        dots_ = VGroup(*[Dot(sax.c2p(v, np.pi**2 * v * v / (4 * STAT["T"])), radius=0.06, color=hue(np.pi**2 * v * v / (4 * STAT["T"]) / hb)) for v in aa])
        bottom = label(r"stationary at $a = 0$", font_size=26, color=C.CLASSICAL).next_to(sax.c2p(0, 0), DOWN, buff=0.2)
        units = note(r"$m = g = 1$, $T = 2$; path colors: the arrow $e^{iS/\hbar}$ with $\hbar = 0.08$").to_edge(DOWN, buff=0.15)
        wheel = corner_wheel(corner=UR, buff=0.2, radius=0.25)
        with self.voiceover(
            "If every path counts, why does a thrown ball follow just one? <bookmark mark='a'/> Take a ball thrown "
            "straight up and caught again two seconds later. The classical path is a parabola in time. "
            "<bookmark mark='b'/> Now consider a whole family of other paths with the same start and end, bent by "
            "different amounts a."
        ) as vo:
            self.play(FadeIn(q))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(labs), Create(cl), FadeIn(cll))
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(p) for p in paths], lag_ratio=0.08), FadeIn(fam), FadeIn(units), FadeIn(wheel), run_time=2.5)
        with self.voiceover(
            "For each one, compute the action, the integral of kinetic minus potential energy. <bookmark mark='a'/> "
            "Plotted against a, it's a parabola, smallest at a equals zero: the classical path. <bookmark mark='b'/> "
            "Each path's arrow turns by S over h-bar, and that's its color. Near the bottom, neighboring paths have "
            "almost the same action, so their arrows point the same way. <bookmark mark='c'/> Far from it, the action "
            "changes quickly, and their arrows spin."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(sax), FadeIn(al), Create(Sc), FadeIn(Sl), FadeIn(exact))
            self.play(FadeIn(bottom))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d, scale=0.5) for d in dots_], lag_ratio=0.06))
            vo.wait_until("c")
            self.play(Indicate(VGroup(paths[0], paths[-1], dots_[0], dots_[-1]), color=WHITE))
        self.wait(0.2)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cornu(self):
        s = load("stationary")
        hbars = STAT["hbars"]
        a = s["a"]
        hb_i = 1
        ax, labs, paths, cl, aa = self._paths_panel(hbars[hb_i], center=LEFT * 4.2 + DOWN * 0.6)
        ax_g = VGroup(ax, labs, paths, cl).scale(0.8)
        O = RIGHT * 0.6 + DOWN * 2.2
        unit = 5.2
        chains = [phasor_chain(s[f"arrows_{i}"], origin=O, unit=unit, stroke_width=3, tips=False) for i in range(3)]
        sel = ValueTracker(-1.6)
        T = STAT["T"]

        def pointer():
            i = int(np.clip(np.searchsorted(a, sel.get_value()), 0, len(a) - 1))
            arr = s[f"arrows_{hb_i}"]
            zc = complex(np.sum(arr[:i])) * unit
            p = O + np.array([zc.real, zc.imag, 0])
            d = Dot(p, radius=0.08, color=WHITE)
            v = sel.get_value()
            pth = polyline(ax, s["ts"][::20], (s["xcl"] + v * np.sin(np.pi * s["ts"] / T))[::20], color=WHITE, stroke_width=4)
            return VGroup(d, pth)

        ptr = always_redraw(pointer)
        tot = Arrow(O, O + unit * np.array([s["arrows_1"].sum().real, s["arrows_1"].sum().imag, 0]), buff=0, color=WHITE, stroke_width=5)
        lab = label(r"the arrows of all the paths, tip to tail, in order of $a$", font_size=26, color=GREY_A).to_edge(UP, buff=0.3).shift(RIGHT * 2.2)
        straight = label(r"paths near the classical one:\\ a straight run", font_size=24, color=C.CLASSICAL).move_to(RIGHT * 4.9 + DOWN * 2.3)
        curl = label(r"far paths: tight spirals that cancel", font_size=24, color=GREY_A).move_to(RIGHT * 3.2 + UP * 2.4)
        hbl = [MathTex(r"\hbar = " + f"{h:g}", font_size=34, color=C.HBAR).to_corner(DR, buff=0.5) for h in hbars]
        cornu = note(r"a Cornu (Euler) spiral: the same curve that describes light at the edge of a shadow").to_edge(DOWN, buff=0.15)
        wheel = corner_wheel(corner=UL, buff=0.2, radius=0.25)
        with self.voiceover(
            "Add the arrows tip to tail, in order of a. <bookmark mark='a'/> The middle of the chain, from paths near "
            "the classical one, is a long straight run. <bookmark mark='b'/> The ends curl into tight spirals that go "
            "nowhere: those paths cancel each other out. <bookmark mark='c'/> This curve is a Cornu spiral, the same one "
            "that describes light at the edge of a shadow."
        ) as vo:
            self.play(FadeIn(ax_g), FadeIn(lab), FadeIn(wheel), FadeIn(hbl[1]))
            self.play(Create(chains[1]), run_time=2.5)
            self.add(ptr)
            vo.wait_until("a")
            self.play(sel.animate.set_value(0.0), FadeIn(straight), run_time=2.5, rate_func=linear)
            vo.wait_until("b")
            self.play(sel.animate.set_value(1.6), FadeIn(curl), run_time=2.5, rate_func=linear)
            self.play(GrowArrow(tot))
            vo.wait_until("c")
            self.play(FadeIn(cornu))
        ptr.clear_updaters()
        self.play(FadeOut(ptr), FadeOut(tot), FadeOut(straight), FadeOut(curl))
        with self.voiceover(
            "Now make h-bar smaller. <bookmark mark='a'/> The spirals wind tighter, the straight run shrinks, "
            "<bookmark mark='b'/> and fewer and fewer paths around the classical one survive."
        ) as vo:
            vo.wait_until("a")
            self.play(Transform(chains[1], chains[2]), TransformMatchingTex(hbl[1], hbl[2]), run_time=2.5)
            vo.wait_until("b")
            narrow = label(r"only paths with $|S - S_{\text{cl}}| \lesssim \hbar$ matter", font_size=28, color=C.HBAR).to_edge(UP, buff=0.9).shift(RIGHT * 2.2)
            self.play(FadeIn(narrow))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plane(self):
        s = load("stationary")
        hb = 0.04
        from scipy.ndimage import gaussian_filter
        S = s["map_S"]
        z = np.exp(1j * S / hb)
        # average neighboring arrows (a small blur of the complex field): where they spin, they cancel and go dark
        z = gaussian_filter(z.real, 2.0) + 1j * gaussian_filter(z.imag, 2.0)
        img = phase_img(z[::-1], height=5.6, width=5.6, vmax=1.0, gamma=0.8).move_to(LEFT * 2.6 + DOWN * 0.3)
        fr = Rectangle(width=5.62, height=5.62, stroke_color=GREY_C, stroke_width=1.5).move_to(img)
        al = MathTex("a", font_size=30).next_to(img, DOWN, buff=0.1)
        bl = MathTex("b", font_size=30).next_to(img, LEFT, buff=0.1)
        ctr = Dot(img.get_center(), radius=0.07, color=WHITE)
        cl = label(r"the classical path", font_size=24, color=C.CLASSICAL).next_to(ctr, DOWN, buff=0.15)
        fam = MathTex(r"x(t) = x_{\text{cl}} + a\sin\frac{\pi t}{T} + b\sin\frac{2\pi t}{T}", font_size=30).to_edge(UP, buff=0.4).shift(RIGHT * 3.3)
        txt = VGroup(
            label(r"color = direction of $e^{iS(a, b)/\hbar}$; brightness:\\how well neighboring arrows agree", font_size=26),
            label(r"rings crowd together wherever $S$ changes;", font_size=26),
            label(r"they spread out only where it doesn't:", font_size=26),
            MathTex(r"\frac{\partial S}{\partial a} = \frac{\partial S}{\partial b} = 0", font_size=34, color=C.ACTION),
            label(r"the principle of \textbf{stationary phase}", font_size=28, color=C.ACTION),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT * 3.4 + DOWN * 0.3)
        wheel = corner_wheel(corner=DR, buff=0.2, radius=0.26)
        with self.voiceover(
            "With two ways to bend the path, the picture is a whole plane of arrows. <bookmark mark='a'/> Color each "
            "point by its arrow's direction: <bookmark mark='b'/> the rings crowd together everywhere except at the "
            "center, where the action is stationary. <bookmark mark='c'/> That's the principle of stationary phase."
        ) as vo:
            self.play(FadeIn(fam))
            vo.wait_until("a")
            self.play(FadeIn(img), Create(fr), FadeIn(al), FadeIn(bl), FadeIn(txt[0]), FadeIn(wheel))
            vo.wait_until("b")
            self.play(FadeIn(txt[1]), FadeIn(txt[2]), FadeIn(ctr), FadeIn(cl))
            vo.wait_until("c")
            self.play(Write(txt[3]), FadeIn(txt[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def euler_lagrange(self):
        rows = [
            MathTex(r"S[x + \delta x]", r"=", r"S[x] + \int_0^T\Big(\frac{\partial L}{\partial x}\delta x + \frac{\partial L}{\partial \dot x}\delta\dot x\Big)dt + O(\delta x^2)",
                    font_size=34),
            MathTex(r"\delta S", r"=", r"\int_0^T\Big(\frac{\partial L}{\partial x} - \frac{d}{dt}\frac{\partial L}{\partial\dot x}\Big)\,\delta x\;dt", font_size=36),
            MathTex(r"\delta S = 0 \text{ for every } \delta x", r"\;\Leftrightarrow\;", r"\frac{d}{dt}\frac{\partial L}{\partial\dot x} = \frac{\partial L}{\partial x}",
                    font_size=36),
            MathTex(r"L = \tfrac12 m\dot x^2 - V(x)", r"\;\Rightarrow\;", r"m\ddot x = -V'(x)", font_size=44),
        ]
        rows[3][2].set_color(C.CLASSICAL)
        rows[2][2].set_color(C.ACTION)
        whys = [
            why(rows[0], r"vary the path, keep the ends fixed"),
            why(rows[1], r"integrate by parts ($\delta x = 0$ at both ends)"),
            why(rows[2], r"the Euler--Lagrange equation"),
            why(rows[3], r"Newton's second law"),
        ]
        step = ladder(self, rows, whys, keep=4, top=2.7, x=-2.3, buff=0.55)
        msg = label(r"classical mechanics: the paths whose arrows add up", font_size=30, color=C.CLASSICAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So the paths that survive are those where small changes don't change the action, to first order. "
            "<bookmark mark='a'/> Vary the path by delta x, keeping its ends fixed. <bookmark mark='b'/> Integrate by "
            "parts, and the first-order change in S is the integral of delta x times something. <bookmark mark='c'/> "
            "For that to vanish for every delta x, the something must be zero: the Euler-Lagrange equation. "
            "<bookmark mark='d'/> For L equals one half m x dot squared minus V, it's m x double dot equals minus V "
            "prime. Newton's second law, recovered as the limit of quantum mechanics."
        ) as vo:
            vo.wait_until("a")
            step(0)
            vo.wait_until("b")
            step(1)
            vo.wait_until("c")
            step(2)
            vo.wait_until("d")
            step(3)
            self.play(Create(SurroundingRectangle(rows[3], color=C.CLASSICAL, buff=0.18, corner_radius=0.12)), FadeIn(msg))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def numbers(self):
        n = load("numbers")
        r = float(n["S_ball_over_hbar"])
        m, e = f"{r:.1e}".split("e")
        assert abs(float(m) - 4.7) < 0.05 and int(e) == 30
        import scipy.constants as sc
        turns = np.pi**2 * 1e-3 * (1e-10) ** 2 / (4 * 1.0) / sc.hbar / (2 * np.pi)  # S(a) - S_cl = pi^2 m a^2 / 4T
        assert 3e10 < turns < 5e10
        ball = VGroup(
            label(r"a 1-gram ball, 1 m/s, for 1 second", font_size=30),
            MathTex(r"\frac{S}{\hbar} \approx \frac{\tfrac12(10^{-3})(1)^2(1)\ \text{J s}}{1.05\times 10^{-34}\ \text{J s}} \approx 4.7\times 10^{30}",
                    font_size=34, color=C.ACTION),
            label(r"bend the path by one atom's width ($10^{-10}$ m): $\sim 4\times 10^{10}$ turns of the arrow", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to(LEFT * 3.4 + UP * 0.7)
        elec = VGroup(
            label(r"an electron in an atom", font_size=30),
            MathTex(r"\oint p\,dx \sim h", font_size=36, color=C.HBAR),
            label(r"many paths contribute: quantum", font_size=26, color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to(RIGHT * 3.5 + UP * 0.7)
        if ball.width > 6.6:
            ball.width = 6.6
            ball.move_to(LEFT * 3.4 + UP * 0.7)
        fermat = label(r"Fermat's principle for light rays is the same mathematics: rays are where wave phases are stationary",
                       font_size=26, color=GREY_B).to_edge(DOWN, buff=0.9)
        with self.voiceover(
            "How small is h-bar, really? <bookmark mark='a'/> For a one-gram ball moving at a meter per second for one "
            "second, the action is about four point seven times ten to the thirty h-bars: <bookmark mark='b'/> bending "
            "its path by the width of a single atom turns its arrow some forty billion times. Only the classical path "
            "survives. <bookmark mark='c'/> For an electron in an atom, the action around an orbit is about h itself; "
            "many paths contribute, and the world is quantum. <bookmark mark='d'/> Fermat's principle for light rays is "
            "the same story: rays are where the phases of waves are stationary."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(ball[0]), Write(ball[1]))
            vo.wait_until("b")
            self.play(FadeIn(ball[2]))
            vo.wait_until("c")
            self.play(FadeIn(elec))
            vo.wait_until("d")
            self.play(FadeIn(fermat))
        self.wait(0.4)
        self.clear_scene()
