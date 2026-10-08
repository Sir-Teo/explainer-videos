from __future__ import annotations

import numpy as np

from explainer import *  # noqa: F403
from videos.riemann.common import RELEASE, gammas, label, note, part_card, polyline, region, strip_axes


def check_row(mark: str, color, text: str, font_size=28) -> VGroup:
    sym = {"yes": r"\checkmark", "no": r"\times", "wait": r"\cdots"}[mark]
    m = MathTex(sym, font_size=40, color=color)
    t = label(text, font_size=font_size, tex_environment="flushleft")
    return VGroup(m, t).arrange(RIGHT, buff=0.35, aligned_edge=UP)


def quote(text: str, who: str, color=WHITE, width=5.6) -> VGroup:
    q = label(text, font_size=28, color=color, tex_environment="flushleft")
    w = label(who, font_size=22, color=GREY_B, tex_environment="flushleft")
    g = VGroup(q, w).arrange(DOWN, buff=0.18, aligned_edge=LEFT)
    bar = Line(g.get_corner(UL) + LEFT * 0.2, g.get_corner(DL) + LEFT * 0.2, color=color, stroke_width=3)
    return VGroup(bar, g)


class Status(VoiceoverScene):
    def construct(self):
        self.card()
        self.verification()
        self.reactions()
        self.meaning()
        self.limits()

    def card(self):
        c = part_card(4, r"Is it right, and what does it mean?", r"status as of October 7, 2026")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.8)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def verification(self):
        head = label(r"Where things stand (October 7, 2026, one day after the release)", font_size=34).to_edge(UP, buff=0.5)
        rows = VGroup(
            check_row("no", C.DANGER, r"peer review: none yet --- the manuscripts were posted directly to GitHub"),
            check_row("wait", YELLOW, r"outside experts: checking of the human-readable proof has only just begun"),
            check_row("yes", C.ZERO_FREE, r"a Lean formalization of the $\tfrac78$ theorem (zeta, every Dirichlet $L$, and\\"
                                          r"the Eisenstein family) and of the Landau--Siegel bound, posed as\\"
                                          r"``comparator challenges'' that allow only Lean's three standard axioms"),
            check_row("yes", C.ZERO_FREE, rf"the Lean library behind it: about {RELEASE['lean_lines'] // 1000},000 lines\\"
                                          rf"(overall, {RELEASE['formalized_manuscripts']} of the {RELEASE['manuscripts']} manuscripts "
                                          r"have formalized main results)"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.5)
        caveat = quote(r"``Some of the unformalized results could have issues.''", r"--- OpenAI, in the repository's README",
                       color=GREY_A).to_edge(DOWN, buff=0.45)

        with self.voiceover(
            "So, is it right? As of October seventh, one day after the release: <bookmark mark='a'/> the manuscripts have not "
            "been peer reviewed. They were posted straight to GitHub. <bookmark mark='b'/> Outside mathematicians have only just "
            "begun to work through the human-readable proof."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1], shift=RIGHT * 0.2))
        with self.voiceover(
            "The strongest evidence is the formal proof. <bookmark mark='l'/> OpenAI's Lean library states the seven-eighths "
            "theorem for zeta, for every Dirichlet L-function, and for the Eisenstein family, plus the Landau–Siegel bound. "
            "Each is set up as a challenge for an independent checking tool, which allows only Lean's standard axioms, so no step "
            "can simply be assumed. <bookmark mark='s'/> The part of the library behind this result runs to about 137,000 lines. "
            "<bookmark mark='c'/> OpenAI itself cautions that results without a formalization could have issues."
        ) as vo:
            vo.wait_until("l")
            self.play(FadeIn(rows[2], shift=RIGHT * 0.2))
            vo.wait_until("s")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(caveat))
        self.wait(0.5)
        self.clear_scene()

        buys = VGroup(
            label(r"\textbf{What a checked Lean proof buys}", font_size=32, color=C.ZERO_FREE),
            label(r"if it compiles as claimed, the theorem is true \emph{as stated},\\for the standard library's definition of "
                  r"$\zeta$: no gap can hide in the logic", font_size=28),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        not_buys = VGroup(
            label(r"\textbf{What it doesn't}", font_size=32, color=YELLOW),
            label(r"human understanding of \emph{why} it works ---\\and someone still has to read the statement\\"
                  r"and confirm it says what we think", font_size=28),
        ).arrange(DOWN, buff=0.25, aligned_edge=LEFT)
        VGroup(buys, not_buys).arrange(DOWN, buff=0.8, aligned_edge=LEFT).move_to(ORIGIN)
        with self.voiceover(
            "What does a formal proof buy you? <bookmark mark='b'/> If it compiles as claimed, the theorem is true exactly as "
            "stated, for the standard library's definition of zeta. No gap can hide in the logic. <bookmark mark='n'/> What it "
            "doesn't give you is understanding: why it works, and what else the method can do. That's what the human reading is "
            "for."
        ) as vo:
            vo.wait_until("b")
            self.play(FadeIn(buys, shift=UP * 0.2))
            vo.wait_until("n")
            self.play(FadeIn(not_buys, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reactions(self):
        head = label(r"Early reactions", font_size=38).to_edge(UP, buff=0.5)
        qs = VGroup(
            quote(r"``Big, big, big, big props for quasiriemann and no Siegel zeroes''", r"Levent Alp\"oge, mathematician, on X",
                  color=C.ZERO_FREE),
            quote(r"``We should ask for receipts.''", r"Andrew Sutherland (MIT), on the release as a whole, to \emph{Scientific American}",
                  color=YELLOW),
            quote(r"criticized the breakneck pace at which AI is harvesting open problems", r"Terence Tao (UCLA), on Mastodon (paraphrased)",
                  color=GREY_A),
            quote(r"``My view is that this is great for mathematics.''", r"Daniel Litt (Toronto), to \emph{Fortune}", color=C.PRIME),
        )
        qs.arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "The reactions came fast. <bookmark mark='a'/> The mathematician Levent Alpöge wrote: big, big, big, big props for "
            "quasi-Riemann and no Siegel zeroes. <bookmark mark='b'/> Others focused on the process. Andrew Sutherland of MIT "
            "said, of the release as a whole, 'We should ask for receipts.' <bookmark mark='c'/> Terence Tao criticized the "
            "breakneck pace at which AI is harvesting open problems, <bookmark mark='d'/> while Daniel Litt called it great for "
            "mathematics."
        ) as vo:
            self.play(FadeIn(head))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(qs[i], shift=UP * 0.15), run_time=0.8)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def meaning(self):
        head = label(r"If it holds up", font_size=40, color=C.ZERO_FREE).to_edge(UP, buff=0.5)
        fl = dict(font_size=29, tex_environment="flushleft")
        items = VGroup(
            label(r"$\bullet$ \ the first zero-free half-plane of fixed width,\\\phantom{$\bullet$ \ }130 years after the prime number theorem", **fl),
            label(r"$\bullet$ \ primes up to $x$, in any progression: error at most about $x^{7/8}$", **fl),
            label(r"$\bullet$ \ the Landau--Siegel ghost is gone; ineffective theorems become effective", **fl),
            label(r"$\bullet$ \ Vinogradov's conjecture, deterministic square roots mod $p$, Euler's idoneal numbers", **fl),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "If it holds up, what does it mean? <bookmark mark='a'/> It's the first zero-free region of fixed width, 130 years "
            "after the prime number theorem. <bookmark mark='b'/> The error in counting primes, in any arithmetic progression, "
            "drops to at most about x to the seven eighths. <bookmark mark='c'/> The Landau–Siegel ghost is gone, <bookmark mark='d'/> "
            "and with it come all those consequences."
        ) as vo:
            self.play(FadeIn(head))
            for i, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(FadeIn(items[i], shift=RIGHT * 0.2), run_time=0.8)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def limits(self):
        g = strip_axes(t_max=60, x_length=5.0, y_length=6.2).move_to(LEFT * 3.7 + DOWN * 0.2)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(0.5, t), radius=0.05, color=C.ZERO) for t in gammas(13)])
        band = region(ax, 1 / 8, 7 / 8, 0, 60, color=YELLOW, opacity=0.12)
        outside = VGroup(region(ax, 7 / 8, 1.35, 0, 60, opacity=0.3), region(ax, -0.35, 1 / 8, 0, 60, opacity=0.3))
        band_l = label(r"still allowed\\by the theorem", font_size=24, color=YELLOW).move_to(ax.c2p(0.5, 52))
        band_l.add_background_rectangle(opacity=0.8, buff=0.05)
        cmp = VGroup(
            label(r"\textbf{What it does not do}", font_size=34, color=YELLOW),
            label(r"the Riemann hypothesis needs the single line $\Real(s) = \tfrac12$", font_size=28),
            MathTex(r"x = 10^{24}:\qquad x^{7/8} = 10^{21} \quad\text{vs.}\quad \sqrt{x} = 10^{12}", font_size=36),
            label(r"a factor of a billion still separates them", font_size=28, color=GREY_A),
            label(r"the paper itself: ``The Riemann hypothesis remains open.''", font_size=28, color=C.ZERO),
        ).arrange(DOWN, buff=0.4).move_to(RIGHT * 3.0 + UP * 0.2)
        assert np.isclose((1e24) ** (7 / 8), 1e21) and np.isclose(np.sqrt(1e24), 1e12)
        with self.voiceover(
            "What it doesn't do is just as important. <bookmark mark='r'/> The Riemann hypothesis asks for the single line at one "
            "half. <bookmark mark='b'/> Between one eighth and seven eighths, there's still a wide band where, as far as this "
            "theorem knows, zeros could roam. <bookmark mark='x'/> In prime terms: at ten to the twenty-four, an error of x to the "
            "seven eighths is ten to the twenty-one, while the square root is ten to the twelve, <bookmark mark='f'/> a factor of "
            "a billion apart. <bookmark mark='o'/> As the paper itself says, the Riemann hypothesis remains open."
        ) as vo:
            self.play(FadeIn(g), FadeIn(dots), FadeIn(outside))
            vo.wait_until("r")
            self.play(FadeIn(cmp[:2]), Indicate(g.crit, color=C.ZERO))
            vo.wait_until("b")
            self.play(FadeIn(band), FadeIn(band_l))
            vo.wait_until("x")
            self.play(FadeIn(cmp[2]))
            vo.wait_until("f")
            self.play(FadeIn(cmp[3]))
            vo.wait_until("o")
            self.play(FadeIn(cmp[4]))
        self.wait(0.5)
        self.clear_scene()

        close = label(r"A machine-written argument, built from a century of human tools,\\may have moved one of mathematics' most "
                      r"stubborn walls.\\The coming weeks of checking will tell.", font_size=36)
        with self.voiceover(
            "Still, it's a remarkable moment. A machine-written argument, assembled from tools that number theorists built over "
            "the last century, may have moved one of the most stubborn walls in mathematics. The coming weeks of checking will "
            "tell."
        ) as vo:
            self.play(FadeIn(close, shift=UP * 0.2), run_time=1.5)
        self.wait(1.0)
        self.clear_scene()
