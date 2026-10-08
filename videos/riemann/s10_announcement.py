from __future__ import annotations

from explainer import *  # noqa: F403
from videos.riemann.common import RELEASE, gammas, label, note, part_card, region, strip_axes

LEAN = [
    ("theorem ", "riemannZeta_ne_zero_of_seven_eighths_lt_re"),
    ("    {s : ℂ} (hs : (7 / 8 : ℝ) < s.re) :", ""),
    ("    riemannZeta s ≠ 0", ""),
]


def lean_block() -> VGroup:
    mono = dict(font="DejaVu Sans Mono", font_size=24)
    char_w = Text("m", **mono).width  # monospace advance, used for spaces and indentation
    lines = VGroup()
    for a, b in LEAN:
        indent = len(a) - len(a.lstrip(" "))
        row = VGroup(Text(a.strip(), color=C.CHARACTER if a.startswith("theorem") else GREY_A, **mono))
        if b:
            row.add(Text(b, color=C.ZERO_FREE, **mono))
        row.arrange(RIGHT, buff=char_w * 1.15, aligned_edge=DOWN)
        row.indent = indent * char_w * 1.05
        lines.add(row)
    lines.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    for row in lines:
        row.shift(RIGHT * row.indent)
    bg = SurroundingRectangle(lines, color=GREY_C, buff=0.3, corner_radius=0.1, stroke_width=1.5).set_fill("#151a22", opacity=1)
    return VGroup(bg, lines)


def doc_card(title: str, date: str, pages: int, extra: str = "", color=WHITE, width=3.9) -> VGroup:
    box = RoundedRectangle(width=width, height=3.0, corner_radius=0.15, color=color, stroke_width=2).set_fill(color, opacity=0.06)
    t = label(title, font_size=26, color=color)
    t.width = min(t.width, width - 0.4)
    d = label(date, font_size=24, color=GREY_A)
    p = label(rf"{pages} pages", font_size=34)
    content = VGroup(t, d, p)
    if extra:
        content.add(label(extra, font_size=22, color=GREY_B))
    content.arrange(DOWN, buff=0.22).move_to(box)
    return VGroup(box, content)


class Announcement(VoiceoverScene):
    def construct(self):
        self.card()
        self.release()
        self.family()
        self.theorem()
        self.band()
        self.lean()

    def card(self):
        c = part_card(3, r"The quasi-Riemann claim", r"what was released, and what it says")
        self.play(FadeIn(c, shift=UP * 0.2))
        self.wait(1.8)
        self.play(FadeOut(c))

    # ------------------------------------------------------------------
    def release(self):
        date = label(rf"{RELEASE['date']}, about 6 p.m.\ Eastern", font_size=34, color=C.DIM).to_edge(UP, buff=0.5)
        head = label(r"OpenAI posts a public collection: \texttt{github.com/openai/math}", font_size=36).next_to(date, DOWN, buff=0.3)
        stats = VGroup(
            VGroup(MathTex(str(RELEASE["manuscripts"]), font_size=72, color=YELLOW), label(r"manuscripts", font_size=28)),
            VGroup(MathTex(str(RELEASE["families"]), font_size=72, color=YELLOW), label(r"families of results", font_size=28)),
            VGroup(MathTex(r"\sim" + f"{RELEASE['problems']:,}".replace(",", "{,}"), font_size=72, color=YELLOW),
                   label(r"problems posed", font_size=28)),
        )
        for s in stats:
            s.arrange(DOWN, buff=0.2)
        stats.arrange(RIGHT, buff=1.3).move_to(UP * 0.1)
        model = label(r"all produced by an \emph{unreleased} internal OpenAI model", font_size=30, color=GREY_A).next_to(stats, DOWN, buff=0.5)
        proc = VGroup(
            label(rf"most results: one fixed procedure, about {RELEASE['hours_per_result']} hours of ChatGPT Pro thinking each, on average",
                  font_size=27),
            label(r"named exceptions: \textbf{the zero-free region for zeta}, \ and the Hodge conjecture for CM abelian varieties",
                  font_size=25, color=C.ZERO_FREE),
        ).arrange(DOWN, buff=0.22).to_edge(DOWN, buff=0.55)
        src = note(r"source: the repository's README", font_size=20).to_corner(DR, buff=0.2)

        with self.voiceover(
            "Now, to the news. <bookmark mark='d'/> On the evening of October sixth, 2026, OpenAI posted a public collection "
            "of <bookmark mark='a'/> 722 mathematical manuscripts, <bookmark mark='b'/> grouped into 372 families of results, "
            "<bookmark mark='c'/> drawn from about four thousand research problems that the model was posed. <bookmark mark='m'/> "
            "All of it was produced by an unreleased internal model."
        ) as vo:
            vo.wait_until("d")
            self.play(FadeIn(date), FadeIn(head))
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(stats[i], shift=UP * 0.2), run_time=0.8)
            vo.wait_until("m")
            self.play(FadeIn(model))
        with self.voiceover(
            "According to OpenAI, most results came from the same fixed procedure, averaging about three hours of ChatGPT Pro "
            "thinking per result. <bookmark mark='e'/> They name two exceptions, and one of them is the subject of this video: "
            "the work on a zero-free region for the zeta function."
        ) as vo:
            self.play(FadeIn(proc[0]), FadeIn(src))
            vo.wait_until("e")
            self.play(FadeIn(proc[1]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def family(self):
        head = label(r"Family 003: \ \textbf{The quasi-Riemann hypothesis}", font_size=40).to_edge(UP, buff=0.5)
        cards = VGroup(
            doc_card(r"\textbf{A Zero-Free Half-Plane}\\$\Real(s) > 7/8$", "September 30, 2026", RELEASE["pages_78"],
                     "the main result", color=C.ZERO_FREE),
            doc_card(r"\textbf{Alternate proof}\\$\Real(s) > 11/12$", "October 5, 2026", RELEASE["pages_1112"],
                     r"write-up human-edited\\for readability", color=YELLOW),
            doc_card(r"\textbf{Uniform exclusion of}\\\textbf{Landau--Siegel zeros}", "October 1, 2026", RELEASE["pages_siegel"],
                     "", color=C.DANGER),
        ).arrange(RIGHT, buff=0.45).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Family number three is called 'The quasi-Riemann hypothesis', and it contains three manuscripts. "
            "<bookmark mark='a'/> A 199-page paper proving the line at seven eighths. <bookmark mark='b'/> A 49-page alternate "
            "proof of a weaker line, at eleven twelfths, whose write-up, OpenAI says, was edited by humans for readability. "
            "<bookmark mark='c'/> And a nine-page paper that rules out Landau–Siegel zeros directly."
        ) as vo:
            self.play(FadeIn(head))
            for i, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(cards[i], shift=UP * 0.2), run_time=0.9)
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def theorem(self):
        thm = VGroup(
            label(r"\textbf{Theorem} (claimed, OpenAI 2026)", font_size=36, color=C.ZERO_FREE),
            label(r"Every Dirichlet $L$-function, including the Riemann zeta function,\\has no zeros with $\Real(s) > \tfrac78$.",
                  font_size=36),
            label(r"The same holds for every finite-order Hecke $L$-function over $\mathbb{Q}(\sqrt{-3})$.", font_size=30, color=GREY_A),
            note(r"(the pole of $\zeta$ at $s = 1$ is, of course, allowed)", font_size=24),
        ).arrange(DOWN, buff=0.35)
        box = SurroundingRectangle(thm, color=C.ZERO_FREE, buff=0.35, corner_radius=0.12)
        with self.voiceover(
            "Here is the main theorem, as claimed. <bookmark mark='a'/> Every Dirichlet L-function, including the Riemann zeta "
            "function, has no zeros with real part greater than seven eighths. <bookmark mark='b'/> The same holds for a family "
            "of L-functions built on a number system called the Eisenstein integers, which we'll meet in a moment."
        ) as vo:
            self.play(FadeIn(thm[0]), Create(box))
            vo.wait_until("a")
            self.play(FadeIn(thm[1]))
            vo.wait_until("b")
            self.play(FadeIn(thm[2:]))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def band(self):
        g = strip_axes(t_max=60, x_length=4.4, y_length=6.0).move_to(LEFT * 4.35 + DOWN * 0.4)
        ax = g.ax
        dots = VGroup(*[Dot(ax.c2p(0.5, t), radius=0.05, color=C.ZERO) for t in gammas(13)])
        right = region(ax, 7 / 8, 1.35, 0, 60, opacity=0.33)
        left = region(ax, -0.35, 1 / 8, 0, 60, opacity=0.33)
        l78 = DashedLine(ax.c2p(7 / 8, 0), ax.c2p(7 / 8, 60), color=C.ZERO_FREE, stroke_width=3)
        l18 = DashedLine(ax.c2p(1 / 8, 0), ax.c2p(1 / 8, 60), color=C.ZERO_FREE, stroke_width=3)
        t78 = MathTex(r"\frac78", font_size=34, color=C.ZERO_FREE).next_to(ax.c2p(7 / 8, 60), UP, buff=0.1)
        t18 = MathTex(r"\frac18", font_size=34, color=C.ZERO_FREE).next_to(ax.c2p(1 / 8, 60), UP, buff=0.1)
        notes = VGroup(
            label(r"no zeros with $\Real(s) > \tfrac78$ \ (the theorem)", font_size=29, color=C.ZERO_FREE, tex_environment="flushleft"),
            label(r"so none with $\Real(s) < \tfrac18$ \ (the mirror symmetry)", font_size=29, color=C.ZERO_FREE, tex_environment="flushleft"),
            label(r"every nontrivial zero lies in the band $\tfrac18 \le \Real(s) \le \tfrac78$,\\the same band at \emph{every} height",
                  font_size=29, tex_environment="flushleft"),
            label(r"the Riemann hypothesis needs the single line $\Real(s) = \tfrac12$", font_size=29, color=C.ZERO, tex_environment="flushleft"),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(RIGHT * 2.75 + UP * 0.2)
        with self.voiceover(
            "Picture it on the critical strip. <bookmark mark='r'/> No zeros to the right of seven eighths, <bookmark mark='l'/> "
            "and by the mirror symmetry, none to the left of one eighth either. <bookmark mark='b'/> So every nontrivial zero is "
            "confined to a band around the critical line, the same band at every height. <bookmark mark='n'/> That's not the "
            "Riemann hypothesis, which demands the single line at one half. But no band of fixed width like this was ever known "
            "before."
        ) as vo:
            self.play(FadeIn(g), FadeIn(dots))
            vo.wait_until("r")
            self.play(FadeIn(right), Create(l78), FadeIn(t78), FadeIn(notes[0]))
            vo.wait_until("l")
            self.play(FadeIn(left), Create(l18), FadeIn(t18), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(FadeIn(notes[2]))
            vo.wait_until("n")
            self.play(FadeIn(notes[3]), Indicate(g.crit, color=C.ZERO))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lean(self):
        code = lean_block().move_to(UP * 0.6)
        head = label(r"The formal statement, in Lean (from the release)", font_size=34).next_to(code, UP, buff=0.5)
        read = label(r"``if the real part of $s$ is greater than $\tfrac78$, then $\zeta(s) \ne 0$''", font_size=32, color=GREY_A)
        read.next_to(code, DOWN, buff=0.45)
        lean_is = note(r"Lean: a programming language in which a computer checks every logical step of a proof", font_size=26)
        lean_is.next_to(read, DOWN, buff=0.4)
        nxt = label(r"So how could you possibly prove such a thing?", font_size=38, color=YELLOW).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The release also comes with a formal proof in Lean, <bookmark mark='l'/> a programming language in which a computer "
            "checks every logical step. <bookmark mark='s'/> Here is the formal statement for zeta: if the real part of s is "
            "greater than seven eighths, then zeta of s is not zero. We'll come back to what has and hasn't been checked."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code))
            vo.wait_until("l")
            self.play(FadeIn(lean_is))
            vo.wait_until("s")
            self.play(FadeIn(read))
        with self.voiceover(
            "So how could you possibly prove such a thing? <bookmark mark='o'/> The 49-page version comes with a readable outline, "
            "and its strategy turns out to be surprisingly concrete. Let's walk through it."
        ) as vo:
            vo.wait_until("o")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()
