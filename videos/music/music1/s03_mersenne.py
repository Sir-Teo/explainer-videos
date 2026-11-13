from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from videos.music.music1.common import (FORCE, FREQ, GOOD, HIST, MASS, PART, RATIO, STR, TUNE, clip, load, ring, say,
                                        window)


def bench(width=8.6) -> VGroup:
    """A string on a test bench: fixed at the left, a tuning peg at the right."""
    a, b = np.array([-width / 2, 0, 0]), np.array([width / 2, 0, 0])
    s = Line(a, b, color=STR, stroke_width=3.5)
    post = Polygon(a + [-0.12, -0.3, 0], a + [0.12, -0.3, 0], a, stroke_width=0, fill_color=GREY_A, fill_opacity=1)
    peg = VGroup(Circle(radius=0.2, stroke_color=GREY_A, stroke_width=2, fill_color=GREY_D, fill_opacity=1),
                 Line(UP * 0.2, DOWN * 0.2, color=GREY_A, stroke_width=3)).move_to(b + RIGHT * 0.2)
    g = VGroup(s, post, peg)
    g.string, g.peg, g.a, g.b = s, peg, a, b
    return g


class Mersenne(SoundScene):
    def construct(self):
        self.card()
        self.knobs()
        self.laws()
        self.experiment()
        self.worked()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(2, r"What sets the pitch", r"Length, and what else?", lit=(1589, 1636, 1638), part=PART)
        with self.voiceover("Chapter two. What sets the pitch."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def knobs(self):
        d = load("mersenne")
        f1 = d["string"]["f1"]
        bn = bench().shift(UP * 2.75)
        knobs = VGroup(label(r"length \ $L$", font_size=28, color=RATIO), label(r"tension \ $T$", font_size=28, color=FORCE),
                       label(r"mass per metre \ $\mu$", font_size=28, color=MASS))
        panels = VGroup()
        specs = [("length", r"length", [0.45, 1.05], [100, 280], [0.5, 0.75, 1.0], [130, 196, 262], RATIO,
                  lambda x: f1 / x),
                 ("tension", r"tension, \ $\times$", [0.6, 4.4], [100, 280], [1, 2, 3, 4], [130, 196, 262], FORCE,
                  lambda x: f1 * np.sqrt(x)),
                 ("mass", r"mass, \ $\times$", [0.8, 4.4], [50, 150], [1, 2, 4], [65, 131], MASS,
                  lambda x: f1 / np.sqrt(x))]
        dots, laws = {}, {}
        for key, xl, xr, yr, xt, yt, col, law in specs:
            g = axes(xr, yr, x_length=3.3, y_length=2.7, xlabel=xl, ylabel=r"hertz", xticks=xt, yticks=yt, font_size=20)
            panels.add(g)
        panels.arrange(RIGHT, buff=0.75).move_to(DOWN * 1.55)
        for (key, xl, xr, yr, xt, yt, col, law), g in zip(specs, panels):
            dots[key] = VGroup(*[Dot(g.ax.c2p(p["x"], p["hz"]), radius=0.07, color=col) for p in d["sweep"][key]])
            xs = np.linspace(xr[0] + 0.03, xr[1] - 0.03, 80)
            laws[key] = curve(g.ax, xs, np.clip(law(xs), yr[0], yr[1]), col, stroke_width=2.5)
        for kn, g in zip(knobs, panels):
            kn.next_to(g, UP, buff=0.45)
        with self.voiceover(
            "Anyone who has tuned a guitar knows three ways to change the note of a string. Press it against a fret, "
            "and it gets shorter. <bookmark mark='a'/> Turn the peg, and it gets tighter. <bookmark mark='b'/> Or "
            "pick a thicker string. Three knobs: length, tension, and the mass of each metre of string. Let us turn "
            "them one at a time on our simulated string and measure what comes out."
        ) as vo:
            self.play(FadeIn(bn), FadeIn(knobs[0]), FadeIn(panels[0]))
            vo.wait_until("a")
            self.play(FadeIn(knobs[1]), FadeIn(panels[1]), Rotate(bn.peg, PI, run_time=1.0))
            vo.wait_until("b")
            self.play(FadeIn(knobs[2]), FadeIn(panels[2]))

        def run(key, text, stops=None, widths=None, pull=None):
            c = clip(f"mersenne.{key}")
            names = sorted(k for k in c.events if len(k) == 2 and k[0] in "ltm")
            with self.listen(c) as snd:
                window(snd, text)
                for i, ev in enumerate(names):
                    snd.wait_until(ev)
                    stop = stops[i] if stops else 1.0
                    if widths:
                        bn.string.set_stroke(width=widths[i])
                    if pull:
                        bn.peg.rotate(PI / 2)
                    a_, b_ = bn.string.get_start(), bn.string.get_end()
                    lens = Lens(a_, a_ + (b_ - a_) * stop, amp=0.2, color=TUNE)
                    snd.show(lens)
                    nxt = snd.time_of(names[i + 1]) if i + 1 < len(names) else None
                    snd.drive(lens, ring(at=snd.time_of(ev), rate=2.2, stop_at=nxt))
                    idx = [j for j, p in enumerate(d["sweep"][key])
                           if abs(p["x"] - (stops[i] if stops else pull[i] if pull else widths_x[i])) < 1e-6]
                    for j in idx:
                        self.add(dots[key][j])

        widths_x = [1.0, 4.0]
        with self.voiceover("Length first: the whole string, three quarters, two thirds, a half."):
            self.play(Indicate(knobs[0], color=RATIO))
        run("length", r"shorter", stops=[1.0, 0.75, 2 / 3, 0.5])
        with self.voiceover(
            "The measured points fall on a curve: <bookmark mark='a'/> one over the length. That is the monochord "
            "again. Now tension: the same string, pulled with twice the force, three times, four times."
        ) as vo:
            self.play(FadeIn(dots["length"]))
            vo.wait_until("a")
            self.play(Create(laws["length"]))
        run("tension", r"tighter", pull=[1.0, 2.0, 3.0, 4.0])
        with self.voiceover(
            "It takes four times the tension to go up one octave. <bookmark mark='a'/> The pitch grows as the square "
            "root of the tension, which is exactly what Vincenzo Galilei found with his weights. Last, the mass: the "
            "same length and the same tension, but a string four times as heavy."
        ) as vo:
            self.play(FadeIn(dots["tension"]))
            vo.wait_until("a")
            self.play(Create(laws["tension"]))
        run("mass", r"heavier", widths=[3.5, 7.0])
        with self.voiceover(
            "An octave lower. <bookmark mark='a'/> The pitch falls as the square root of the mass. That is why the "
            "bass strings of a guitar or a piano are wound with wire: it makes them heavy without making them long."
        ) as vo:
            self.play(FadeIn(dots["mass"]))
            vo.wait_until("a")
            self.play(Create(laws["mass"]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def laws(self):
        card = history_card(1636, r"Marin Mersenne, \ \textit{Harmonie universelle}",
                            r"a friar in Paris, and the man through whom the scientists of Europe wrote to one another",
                            width=5.6).to_corner(UL, buff=0.45)
        rows = VGroup(
            MathTex(r"f \;\propto\; \frac{1}{L}", font_size=48),
            MathTex(r"f \;\propto\; \sqrt{T}", font_size=48),
            MathTex(r"f \;\propto\; \frac{1}{\sqrt{\mu}}", font_size=48),
        ).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * 3.6 + UP * 1.3)
        for r, col in zip(rows, (RATIO, FORCE, MASS)):
            r.set_color(col)
        law = MathTex(r"f", r"=", r"\frac{1}{2L}", r"\sqrt{\frac{T}{\mu}}", font_size=64).move_to(DOWN * 1.9 + RIGHT * 1.2)
        law[2].set_color(RATIO), law[3].set_color(FORCE)
        box = SurroundingRectangle(law, color=GOOD, buff=0.25, corner_radius=0.12, stroke_width=2)
        name = label(r"Mersenne's laws", font_size=30, color=GOOD).next_to(box, UP, buff=0.15)
        half = label(r"the $\tfrac{1}{2}$ came later, \ with calculus \ (Taylor, 1713)", font_size=24, color=GREY_A)
        half.next_to(box, DOWN, buff=0.2)
        # a string long and slack enough to count: its slow swing, and a tally
        long = StringView(width=5.6, scale=0.45, stroke_width=3).move_to(LEFT * 3.6 + DOWN * 1.6)
        tr = ValueTracker(0.0)
        xs_ = np.linspace(0, 1, 60)
        long.add_updater(lambda m: m.set_shape(np.sin(np.pi * xs_) * np.cos(2 * PI * 0.8 * tr.get_value())))
        tally = Integer(0, font_size=54, color=TUNE).next_to(long, DOWN, buff=0.75)
        tally.add_updater(lambda m: m.set_value(int(0.8 * tr.get_value())))
        cap = label(r"a string long and slack enough to count", font_size=24, color=GREY_A).next_to(long, UP, buff=0.75)
        with self.voiceover(
            "These three rules are called Mersenne's laws. Marin Mersenne was a friar in Paris, and in 1636 he "
            "published them in a book called Universal Harmony. <bookmark mark='a'/> Frequency goes as one over the "
            "length, as the square root of the tension, and as one over the square root of the mass per unit length. "
            "Galileo printed the same thing two years later. <bookmark mark='b'/> Mersenne did something else nobody "
            "had done. He made strings so long and slack that he could count their swings by eye, then used his own "
            "laws to scale up, and so put the first actual number, vibrations per second, on a musical note."
        ) as vo:
            self.play(FadeIn(card, shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in rows], lag_ratio=0.5), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(long), FadeIn(cap), FadeIn(tally), run_time=0.6)
            self.play(tr.animate.set_value(vo.remaining() + 0.1), run_time=vo.remaining() + 0.1, rate_func=linear)
        long.clear_updaters()
        tally.clear_updaters()
        self.play(FadeOut(long), FadeOut(cap), FadeOut(tally), run_time=0.5)
        with self.voiceover(
            "Put together, with the constant that makes it an equation: <bookmark mark='a'/> the frequency is one "
            "over twice the length, times the square root of tension over mass per unit length. "
            "<bookmark mark='b'/> Mersenne had the proportions. The factor of one half had to wait for calculus."
        ) as vo:
            vo.wait_until("a")
            self.play(Write(law), Create(box), FadeIn(name))
            vo.wait_until("b")
            self.play(FadeIn(half))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def experiment(self):
        d = load("mersenne")
        e = d["exponents"]
        tab = d["table"]
        lo, hi = 1.5, 3.2
        g = axes([lo, hi], [lo, hi], x_length=5.0, y_length=4.4, xlabel=r"$\frac{1}{2L}\sqrt{T/\mu}$ \ (hertz)",
                 ylabel=r"pitch measured from the motion (hertz)", xticks=[2, 3], yticks=[2, 3], font_size=20,
                 xfmt=lambda v: rf"10^{{{int(v)}}}", yfmt=lambda v: rf"10^{{{int(v)}}}")
        g.move_to(LEFT * 3.5 + DOWN * 0.2)
        diag = Line(g.ax.c2p(lo, lo), g.ax.c2p(hi, hi), color=GREY_C, stroke_width=1.5)
        pts = VGroup(*[Dot(g.ax.c2p(np.log10(r["law"]), np.log10(r["hz"])), radius=0.06, color=FREQ) for r in tab])
        fit = VGroup(
            label(rf"{d['strings']} random strings, \ simulated", font_size=28, color=GREY_A),
            MathTex(r"f = C \, L^{a} \, T^{b} \, \mu^{c}", font_size=44),
            MathTex(rf"a = {e['L']:.3f}", font_size=40, color=RATIO),
            MathTex(rf"b = {e['T']:+.3f}".replace("+", r"\phantom{-}"), font_size=40, color=FORCE),
            MathTex(rf"c = {e['mu']:.3f}", font_size=40, color=MASS),
            MathTex(rf"C = {d['constant']:.3f}", font_size=40, color=GOOD),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(RIGHT * 3.6 + UP * 0.3)
        told = label(r"what the simulation was told: \ Newton's law, for each small piece of string", font_size=26,
                     color=TUNE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Do the laws hold for our string? Here is the test. We made up "
            f"{d['strings']} strings with random lengths, tensions and masses, simulated each one, and measured its "
            "pitch from the motion alone, by asking after how long the motion repeats. <bookmark mark='a'/> Plotted "
            "against the formula, every string lands on the diagonal. <bookmark mark='b'/> And if we let a computer "
            "fit the powers, without telling it what to expect, "
            f"<bookmark mark='c'/> it finds {say(e['L'], 3)} for the length, {say(e['T'], 3)} for the tension, "
            f"{say(e['mu'], 3)} for the mass, and a constant of {say(d['constant'], 3)}."
        ) as vo:
            self.play(FadeIn(g), Create(diag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p, scale=0.5) for p in pts], lag_ratio=0.05), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(fit[0]), FadeIn(fit[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(r) for r in fit[2:]], lag_ratio=0.6), run_time=4.0)
        with self.voiceover(
            "Minus one, a half, minus a half, and one half. The formula was never typed into the simulation. "
            "<bookmark mark='a'/> All it was given is Newton's second law, applied to each small piece of the string. "
            "So Mersenne's laws must follow from Newton's. In two chapters we will see how."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(told, shift=UP * 0.2))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        g = load("mersenne")["guitar"]
        title = label(r"A worked example: \ a guitar's top string", font_size=36).to_edge(UP, buff=0.45)
        given = VGroup(
            MathTex(rf"L = {g['L'] * 1000:.0f}\ \text{{mm}}", font_size=38, color=RATIO),
            MathTex(rf"\mu = {g['mu_g_per_m']:.2f}\ \text{{g/m}}", font_size=38, color=MASS),
            MathTex(rf"f = {g['hz']:.1f}\ \text{{Hz}} \quad (\text{{E}}_4)", font_size=38, color=FREQ),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(LEFT * 4.2 + UP * 1.0)
        solve = MathTex(r"T", r"=", r"\mu \,(2 L f)^2", r"=", rf"{g['T']:.0f}\ \text{{N}}", font_size=50)
        solve.move_to(RIGHT * 2.2 + UP * 1.4)
        solve[0].set_color(FORCE), solve[4].set_color(FORCE)
        kg = label(rf"the weight of {g['kgf']:.1f} kilograms", font_size=32, color=FORCE).next_to(solve, DOWN, buff=0.3)
        ask = pause_card(r"To raise this string a whole octave with the peg alone, \\ how much tension would it take?",
                         width=9.0).move_to(DOWN * 1.6)
        ans = MathTex(rf"4 \times {g['T']:.0f}\ \text{{N}} = {g['octave_T']:.0f}\ \text{{N}}", font_size=44, color=FORCE)
        ans2 = label(rf"the weight of {g['octave_kgf']:.0f} kilograms on a wire a quarter of a millimetre thick: "
                     r"\ it breaks first", font_size=28, color=GREY_A)
        VGroup(ans, ans2).arrange(DOWN, buff=0.25).move_to(DOWN * 1.7)
        with self.voiceover(
            "One worked example, with a real string. The top string of a guitar is steel, a quarter of a millimetre "
            "thick. <bookmark mark='a'/> It is "
            f"{say(g['L'] * 1000)} millimetres long, a metre of it weighs {say(g['mu_g_per_m'], 1)} grams, and it is "
            f"tuned to the E above middle C, {say(g['hz'], 1)} hertz. <bookmark mark='b'/> Solve the law for the "
            f"tension, and you get {say(g['T'])} newtons: the weight of about {say(g['kgf'])} kilograms, hanging "
            "from that one thin wire."
        ) as vo:
            wire = bench(7.0).move_to(DOWN * 2.2)
            wire.string.set_stroke(width=2)
            wtag = label(r"steel, \ 0.25 mm", font_size=24, color=GREY_A).next_to(wire.string, UP, buff=0.2)
            self.play(FadeIn(title), FadeIn(wire), FadeIn(wtag))
            vo.wait_until("a")
            self.play(FadeIn(given))
            vo.wait_until("b")
            self.play(Write(solve), run_time=1.5)
            self.play(FadeIn(kg))
        with self.voiceover(
            "Now you predict. Suppose you wanted this string an octave higher, and all you did was turn the peg. "
            "How much tension would that take?"
        ):
            self.play(FadeOut(wire), FadeOut(wtag), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"Four times as much: {say(g['octave_T'])} newtons, about {say(g['octave_kgf'])} kilograms. The wire "
            "breaks long before that. <bookmark mark='a'/> This is why the six strings of a guitar differ in "
            "thickness and not much in tension: each one carries roughly the same load, and the mass does the "
            "work. So we have the law. What we do not have is the reason. For that we need to watch a string move."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(ans), FadeIn(ans2))
            vo.wait_until("a")
        self.wait(0.3)
        self.clear_scene()
