from __future__ import annotations

import numpy as np

from explainer.music import *  # noqa: F403
from explainer.music.monochord.physics import pluck_shape
from videos.music.music1.common import (BAD, FORCE, FREQ, GOOD, HIST, LIMIT, PART, RATIO, STR, TIME, TUNE, clip, load,
                                        ring, say, window)

X = np.linspace(0, 1, 121)


class Frontier(SoundScene):
    def construct(self):
        self.card()
        self.stretch()
        self.glide()
        self.energy()
        self.open()

    # ------------------------------------------------------------------
    def card(self):
        card = chapter_card(12, r"Frontier: \ when the string stretches", r"Where does the linear string stop being true?",
                            lit=(1883, 1945, 2009), part=PART)
        with self.voiceover("Chapter twelve. The frontier: when the string stretches."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def stretch(self):
        d = load("nonlinear")
        hard = d["runs"]["hard"]
        s = StringView(width=10.0, scale=1.5).move_to(UP * 1.0)
        flat = Line(s.p(0), s.p(1), color=GREY_C, stroke_width=2)
        tri = pluck_shape(X, 1.0, 0.25, 1.0)
        longer = label(r"longer than the straight string: \ so it is stretched, \ so it is tighter", font_size=28,
                       color=LIMIT).move_to(UP * 3.3)
        eq = MathTex(r"T", r"\;\longrightarrow\;", r"T\,\Bigl(1 + \gamma\!\int_0^L\! \bigl(\tfrac{\partial u}{\partial x}\bigr)^2 dx\Bigr)",
                     font_size=44).move_to(DOWN * 1.3)
        eq[0].set_color(FORCE), eq[2].set_color(LIMIT)
        who = label(r"Kirchhoff, 1883; \ Carrier, 1945", font_size=24, color=HIST).next_to(eq, DOWN, buff=0.25)
        num = label(rf"our wire, pulled aside {hard['height_mm']:.0f} mm: \ the tension rises by "
                    rf"{100 * (hard['tension_start'] - 1):.0f}\%", font_size=30, color=TUNE).move_to(DOWN * 3.1)
        with self.voiceover(
            "Every result in this part rested on one quiet assumption: that the tension of the string is a "
            "constant. It is not. <bookmark mark='a'/> A string pulled aside is longer than a straight one. A longer "
            "string is a stretched string, and a stretched string is tighter. <bookmark mark='b'/> Kirchhoff put "
            "this into the equation in 1883: the tension grows with the total amount of slope along the string. "
            f"<bookmark mark='c'/> For a gentle pluck the correction is nothing. But pull our steel wire aside by "
            f"{say(hard['height_mm'])} millimetres and its tension goes up by "
            f"{say(100 * (hard['tension_start'] - 1))} percent."
        ) as vo:
            self.play(FadeIn(s), FadeIn(flat))
            vo.wait_until("a")
            s.set_shape(tri)
            self.play(FadeIn(longer))
            vo.wait_until("b")
            self.play(Write(eq), FadeIn(who))
            vo.wait_until("c")
            self.play(FadeIn(num))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def glide(self):
        d = load("nonlinear")
        soft, hard = d["runs"]["soft"], d["runs"]["hard"]
        ymax = max(hard["cents"]) * 1.15
        g = axes([0, 2.6], [-5, ymax], x_length=8.4, y_length=4.0, xlabel=r"seconds after the pluck", font_size=20,
                 ylabel=r"pitch above the string's own note (cents)", xticks=[0, 1, 2], yticks=[0, 25, 50, 75])
        g.move_to(LEFT * 1.6 + DOWN * 0.5)
        zero = DashedLine(g.ax.c2p(0, 0), g.ax.c2p(2.6, 0), color=GREY_D, stroke_width=1.5, dash_length=0.08)
        ch = curve(g.ax, hard["times"], hard["cents"], BAD, stroke_width=3.5)
        cs = curve(g.ax, soft["times"], soft["cents"], GOOD, stroke_width=3.5)
        ce = DashedVMobject(curve(g.ax, hard["times"], hard["estimate_cents"], GREY_B, stroke_width=2), num_dashes=40)
        leg = VGroup(label(rf"a soft pluck, \ {soft['height_mm']:.0f} mm", font_size=26, color=GOOD),
                     label(rf"a hard pluck, \ {hard['height_mm']:.0f} mm", font_size=26, color=BAD),
                     label(r"estimate: \ $\sqrt{\text{average tension}}$", font_size=24, color=GREY_B)
                     ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(RIGHT * 4.7 + UP * 0.9)
        with self.voiceover(
            "Tighter means higher. So the pitch of a string depends, a little, on how hard you play it, and it "
            "changes while the note dies away. Here is the simulation with Kirchhoff's term switched on: first a "
            "soft pluck, then a hard one, made equally loud so that only the pitch differs."
        ):
            plucks = VGroup()
            for h_, col in ((0.1, GOOD), (1.0, BAD)):
                v_ = StringView(width=3.4, scale=0.9, color=col, stroke_width=3)
                v_.set_shape(h_ * pluck_shape(X, 1.0, 0.11, 1.0))
                plucks.add(v_)
            plucks.arrange(DOWN, buff=0.9).move_to(RIGHT * 4.9 + DOWN * 1.6)
            self.play(FadeIn(g), Create(zero), FadeIn(leg[:2]), FadeIn(plucks))
        head = Line(g.ax.c2p(0, -5), g.ax.c2p(0, ymax), color=WHITE, stroke_width=1.5)
        for key, cv in (("soft", cs), ("hard", ch)):
            c = clip(f"nonlinear.{key}")
            with self.listen(c) as snd:
                window(snd, rf"a {key} pluck")
                self.add(cv)
                h = head.copy()
                snd.show(h)
                snd.drive(h, lambda m, t: m.set_x(g.ax.c2p(min(max(t, 0), 2.6), 0)[0]))
        with self.voiceover(
            f"The hard pluck starts {say(hard['start_cents'])} cents sharp, most of a semitone, and slides down to "
            "the true note as it fades. You know this sound: it is the twang of any slack string hit too hard. "
            f"<bookmark mark='a'/> The obvious estimate, the square root of the average tension, predicts "
            f"{say(hard['estimate_cents'][0])} cents. The simulation gives more, because the string is tightest "
            "exactly when it is most bent. The linear theory of this part is a theory of quiet strings."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(ce), FadeIn(leg[2]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def energy(self):
        d = load("nonlinear")
        drift = d["energy_drift"]
        expo = int(np.floor(np.log10(drift)))
        H = MathTex(r"E", r"=", r"\sum_i \; \tfrac{1}{2}\,\mu h\, \dot u_i^{\,2}", r"\;+\;",
                    r"\tfrac{1}{2}\,\frac{T}{h}\,(u_{i+1} - u_i)^2", font_size=44).move_to(UP * 1.9)
        H[2].set_color(TIME), H[4].set_color(FORCE)
        tags = VGroup(label(r"motion", font_size=24, color=TIME).next_to(H[2], DOWN, buff=0.2),
                      label(r"stretch", font_size=24, color=FORCE).next_to(H[4], DOWN, buff=0.2))
        res = VGroup(label(rf"over {d['steps']:,} steps of the ideal string, \ the energy changes by at most".replace(",", "{,}"),
                           font_size=28, color=GREY_A),
                     MathTex(rf"{drift / 10 ** expo:.0f} \times 10^{{{expo}}}", font_size=54, color=GOOD),
                     label(r"of itself", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.2).move_to(DOWN * 0.7)
        why_ = label(r"a scheme that keeps a positive energy exactly \ cannot blow up", font_size=30, color=TUNE)
        why_.move_to(DOWN * 2.6)
        with self.voiceover(
            "There is a second frontier, in the computer. How do you know a simulation of a violent, nonlinear "
            "string will not simply explode? <bookmark mark='a'/> The modern answer is energy. Our bead scheme has "
            "a quantity, the energy of motion plus the energy of stretch, that it conserves exactly. "
            f"<bookmark mark='b'/> Over {say(d['steps'])} steps it wanders by a few parts in ten to the "
            f"{abs(expo)}: rounding error. <bookmark mark='c'/> A scheme that keeps a positive energy exactly cannot "
            "blow up, and physical models of instruments are now designed that way: energy first, then the scheme."
        ) as vo:
            beads = StringView(width=9.0, scale=0.7, stroke_width=2).move_to(DOWN * 0.6)
            shape_ = pluck_shape(np.linspace(0, 1, 25), 1.0, 0.3, 1.0)
            beads.set_shape(shape_)
            dots = VGroup(*[Dot(beads.p(i / 24, shape_[i]), radius=0.06, color=STR) for i in range(1, 24)])
            self.play(FadeIn(beads), FadeIn(dots), run_time=0.6)
            vo.wait_until("a")
            self.play(Write(H), FadeIn(tags), run_time=1.6)
            vo.wait_until("b")
            self.play(FadeOut(beads), FadeOut(dots), run_time=0.4)
            self.play(FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(why_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        d = load("nonlinear")
        t = d["third_mode"]
        expo = int(np.floor(np.log10(max(t["stretching"], 1e-300))))
        head = label(r"What this model still cannot do", font_size=36, color=LIMIT).to_edge(UP, buff=0.4)
        s = StringView(width=6.0, scale=0.9).move_to(LEFT * 3.6 + UP * 1.5)
        s.set_shape(pluck_shape(X, 1.0, 1 / 3, 1.0))
        node = Dot(s.p(1 / 3, 1.0), radius=0.08, color=HIST)
        lab = label(r"plucked at a third: \ mode 3 is missing", font_size=24, color=GREY_A).next_to(s, DOWN, buff=0.3)
        exp = VGroup(label(r"on a real string (Legge \& Fletcher, 1984)", font_size=26, color=HIST),
                     label(r"the missing mode grows back within a tenth of a second", font_size=26),
                     label(r"in our model, with stretching", font_size=26, color=TUNE),
                     MathTex(rf"\frac{{|a_3|}}{{|a_1|}} \;<\; 10^{{{expo + 1}}}", font_size=40, color=TUNE),
                     label(r"it stays missing", font_size=26)).arrange(DOWN, buff=0.16).move_to(RIGHT * 3.4 + UP * 1.2)
        with self.voiceover(
            "And here is where our model stops. Pluck a string a third of the way along and, by chapter eight, its "
            "third mode is missing. <bookmark mark='a'/> In 1984 Katherine Legge and Neville Fletcher measured real "
            "strings and found that the missing mode comes back: within about a tenth of a second it has grown to "
            "an amplitude you can hear. <bookmark mark='b'/> In our simulation, even with stretching, it never "
            "does. Stretching changes the tension everywhere at once, and that cannot pass energy from one mode to "
            "another. A real bridge that gives a little can."
        ) as vo:
            self.play(FadeIn(head), FadeIn(s), FadeIn(node), FadeIn(lab))
            vo.wait_until("a")
            self.play(FadeIn(exp[:2]))
            vo.wait_until("b")
            self.play(FadeIn(exp[2:]))
        opens = VGroup(
            label(r"open, and active", font_size=26, color=GREY_B),
            label(r"strings that hit things: \ a sitar's curved bridge, \ a slapped bass, \ a buzzing fret", font_size=26),
            label(r"the two directions a string can swing in, \ and how they trade energy (whirling)", font_size=26),
            label(r"schemes that stay stable through a collision \ (Bilbao, Torin \& Chatziioannou, 2015; "
                  r"\ Issanchou et al., 2017)", font_size=24, color=GREY_A),
            label(r"$\bigstar$ \ Build a string against a curved bridge, \ with an exact energy balance, \ and "
                  r"compare it with a tanpura", font_size=26, color=TUNE),
        ).arrange(DOWN, buff=0.2, aligned_edge=LEFT).move_to(DOWN * 2.0)
        with self.voiceover(
            "So the frontier of the vibrating string, three hundred years after Taylor, is contact. "
            "<bookmark mark='a'/> Strings that touch things as they move: the curved bridge that gives a sitar its "
            "buzz, a slapped bass, a fret that rattles. <bookmark mark='b'/> A string also swings in two directions "
            "at once, and nonlinearity makes them trade energy, so the motion whirls. <bookmark mark='c'/> Writing "
            "simulations of these that are provably stable is work of the last ten years. "
            "<bookmark mark='d'/> This part's research problem is one of them, and we will need it in Part 34, when "
            "the series builds a tanpura."
        ) as vo:
            self.play(FadeOut(lab), FadeIn(opens[0]))
            for mark, o in zip("abcd", opens[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(o, shift=RIGHT * 0.2), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
