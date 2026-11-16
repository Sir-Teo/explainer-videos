from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403
from videos.psychology.psych44.diagrams import arrow, node

NAMES = ["visual", "cubes", "lozenges", "paragraph", "sentence", "words", "addition", "dots", "capitals"]


def cfa_diagram(color_f=(MODEL, SYMP, GOOD), loadings=None) -> VGroup:
    facs = VGroup(*[node(t, c, latent=True, r=0.62) for t, c in zip(("visual", "verbal", "speed"), color_f)])
    facs.arrange(RIGHT, buff=2.2).move_to([0, 1.2, 0])
    for f in facs:
        f[1].scale(0.85)
    obs = VGroup(*[node(f"x{i + 1}", GREY_A, r=0.27) for i in range(9)]).arrange(RIGHT, buff=0.3).move_to([0, -0.9, 0])
    arrs = VGroup()
    for i in range(9):
        t = None if loadings is None else f"{loadings[i]:.2f}"
        arrs.add(arrow(facs[i // 3], obs[i], color=color_f[i // 3], text=None))
        if t:
            arrs[-1].add(label(t, font_size=11, color=color_f[i // 3]).move_to(
                0.55 * facs[i // 3].get_center() + 0.45 * obs[i].get_center() + LEFT * 0.12))
    cov = VGroup(*[ArcBetweenPoints(facs[a].get_top(), facs[b].get_top(), angle=-PI / 3, color=GREY_B,
                                    stroke_width=2) for a, b in ((0, 1), (1, 2), (0, 2))])
    return VGroup(facs, obs, arrs, cov)


class Cfa(VoiceoverScene):
    def construct(self):
        self.card()
        self.model()
        self.identify()

    def card(self):
        card = chapter_card(3, r"The factor model, \ confirmed", r"What does the diagram claim?",
                            lit={1939: r"Holzinger \& Swineford", 1969: r"Jöreskog"}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter three. The factor model, confirmed."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def model(self):
        head = heading(r"Nine tests, \ three factors")
        dg = cfa_diagram().scale(1.05).next_to(head, DOWN, buff=0.3)
        eq = MathTex(r"\Sigma = \Lambda\,\Phi\,\Lambda^{\top} + \Theta", font_size=40, color=MODEL)
        rows = rows_of([
            (r"Holzinger and Swineford, \ 1939: \ 301 children in two schools took nine tests: \ three visual, \ three "
             r"verbal, \ three of speed", WHITE),
            (r"the confirmatory model says each test measures one factor, \ and nothing else: \ the missing arrows are "
             r"the claim", MODEL),
        ], 12.4, 21, 0.3)
        eq.next_to(dg, DOWN, buff=0.2)
        rows.next_to(eq, DOWN, buff=0.25)
        tag = historical_tag(r"Holzinger \& Swineford (1939)")
        with self.voiceover(
            "Now the factor model. <bookmark mark='a'/> In 1939 Karl Holzinger and Frances Swineford gave nine tests "
            "to three hundred and one children in two schools: three visual, three verbal, and three of speed. "
            "<bookmark mark='b'/> A confirmatory model says each test measures one factor and nothing else, and the "
            "factors may correlate. The missing arrows are the claim. <bookmark mark='c'/> The implied covariance "
            "matrix is lambda phi lambda transpose, plus theta: loadings, factor covariances, and each test's own "
            "error variance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(dg))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq))
        self.clear_scene()

    def identify(self):
        head = heading(r"Identification: \ counting")
        rows = rows_of([
            (r"a factor has no units: \ fix one loading per factor to 1 (or its variance to 1) to give it a scale", WHITE),
            (r"knowns: \ the 9 variances and 36 covariances, \ 45 in all", PERSON),
            (r"unknowns: \ 6 free loadings, \ 3 factor variances, \ 3 factor covariances, \ 9 error variances: \ 21", MODEL),
            (r"degrees of freedom: \ 45 minus 21 = 24 testable constraints; \ a factor needs at least three indicators "
             r"to be identified on its own", GOOD),
            (r"a model with more unknowns than knowns cannot be estimated at all; \ one with exactly as many fits "
             r"perfectly, \ and tests nothing", YOU),
        ], 12.4, 26, 0.55).move_to([0, -0.2, 0])
        with self.voiceover(
            "Before estimating, count. <bookmark mark='a'/> A factor has no units of its own, so fix one loading per "
            "factor to one, or its variance to one, to give it a scale. <bookmark mark='b'/> The knowns are the nine "
            "variances and thirty-six covariances: forty-five in all. <bookmark mark='c'/> The unknowns are six free "
            "loadings, three factor variances, three factor covariances, and nine error variances: twenty-one. "
            "<bookmark mark='d'/> That leaves twenty-four degrees of freedom: twenty-four testable constraints. A "
            "factor needs at least three indicators to be identified on its own. <bookmark mark='e'/> A model with "
            "more unknowns than knowns can't be estimated at all, and one with exactly as many fits perfectly, and "
            "tests nothing."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
