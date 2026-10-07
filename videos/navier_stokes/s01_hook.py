from __future__ import annotations

from explainer import *  # noqa: F403
from videos.navier_stokes.common import cylinder_movie, frame_rect, label, move_movie, ns_system


class Hook(VoiceoverScene):
    def construct(self):
        movie = cylinder_movie("cyl_re150", width=config.frame_width, alpha=0.0)
        movie.move_to(ORIGIN)
        self.add(movie)

        with self.voiceover(
            "This is a computer simulation of fluid flowing past a cylinder. Notice the swirls peeling off, alternating between "
            "the top and the bottom, one after another, in a perfectly rhythmic pattern."
        ) as vo:
            self.play(movie.fade(1.0, run_time=2.5))

        name = label(r"a K\'arm\'an vortex street", font_size=40).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "This pattern is called a Kármán vortex street. You can see it in the clouds downwind of islands, and it's why a "
            "telephone wire hums in the wind."
        ) as vo:
            self.play(FadeIn(name, shift=UP * 0.2))

        system = ns_system(font_size=52).move_to(DOWN * 1.55)
        title = label(r"The Navier--Stokes equations", font_size=36, color=GREY_A).next_to(system, UP, buff=0.3)
        with self.voiceover(
            "Every swirl here, every detail of this flow, comes from a single set of equations, written down two centuries ago: "
            "<bookmark mark='eq'/> the Navier–Stokes equations."
        ) as vo:
            self.play(FadeOut(name), move_movie(movie, center=UP * 1.95, width=11.0, run_time=2.0))
            border = frame_rect(movie)
            self.play(Create(border), run_time=0.8)
            vo.wait_until("eq")
            self.play(Write(system), run_time=2.5)
            self.play(FadeIn(title))

        uses = VGroup(*[label(t, font_size=30, color=GREY_A) for t in
                        ["weather", "ocean currents", "blood flow", "aircraft", "your coffee"]])
        uses.arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "They govern <bookmark mark='a'/> the weather, <bookmark mark='b'/> ocean currents, <bookmark mark='c'/> the blood in your "
            "arteries, <bookmark mark='d'/> the air over an airplane's wing, <bookmark mark='e'/> and the cream swirling in your coffee."
        ) as vo:
            for i, m in enumerate("abcde"):
                vo.wait_until(m)
                self.play(FadeIn(uses[i], shift=UP * 0.15), run_time=0.6)

        fma = MathTex(r"F = m\,a", font_size=64, color=YELLOW)
        fma_box = SurroundingRectangle(fma, color=YELLOW, buff=0.2, corner_radius=0.1)
        fma_g = VGroup(fma, fma_box).next_to(system, RIGHT, buff=0.5)
        with self.voiceover(
            "At first glance they look intimidating. But the core idea is something you already know. They are nothing more than "
            "Newton's second law, <bookmark mark='f'/> F equals m a, applied to every tiny parcel of fluid."
        ) as vo:
            self.play(FadeOut(uses), system.animate.shift(LEFT * 1.4), title.animate.shift(LEFT * 1.4))
            fma_g.next_to(system, RIGHT, buff=0.6)
            vo.wait_until("f")
            self.play(Write(fma), Create(fma_box))

        prize = MathTex(r"\$1{,}000{,}000", font_size=48, color=YELLOW).to_edge(DOWN, buff=0.35).shift(LEFT * 2.0)
        ai = label(r"$+$ an AI-generated proof (2026)?", font_size=32, color=GREY_A).next_to(prize, RIGHT, buff=0.5)
        with self.voiceover(
            "By the end of this video, we'll have derived every one of these terms from scratch, and every symbol will feel not "
            "just familiar, but inevitable. Along the way, we'll see why these innocent-looking equations hide one of the great "
            "problems in mathematics, <bookmark mark='m'/> with a million-dollar prize attached, <bookmark mark='ai'/> and one that an "
            "AI system, in September 2026, claimed to have cracked."
        ) as vo:
            vo.wait_until("m")
            self.play(FadeIn(prize, shift=UP * 0.2))
            vo.wait_until("ai")
            self.play(FadeIn(ai, shift=UP * 0.2))

        self.play(FadeOut(VGroup(system, title, fma_g, prize, ai, border)), movie.fade(0.25, run_time=1.0))
        card = VGroup(
            label(r"The Navier--Stokes Equations", font_size=64),
            label(r"derived from scratch, and visualized", font_size=36, color=GREY_A),
        ).arrange(DOWN, buff=0.35)
        card.add_background_rectangle(opacity=0.6, buff=0.4)
        self.play(FadeIn(card, scale=1.05), move_movie(movie, center=ORIGIN, width=config.frame_width, run_time=1.5))
        self.wait(2.5)
        movie.rate = 0
        self.play(FadeOut(card), movie.fade(0.0, run_time=1.0))
        self.remove(movie)
