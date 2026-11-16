from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403
from videos.psychology.psych44.diagrams import arrow, node


class Mediation(VoiceoverScene):
    def construct(self):
        self.card()
        self.recipe()
        self.trap()
        self.fixes()

    def card(self):
        card = chapter_card(8, r"Mediation", r"Does the treatment work through the mechanism?",
                            lit={1986: r"Baron \& Kenny", 2010: r"Bullock et al."}, part=PART, scale=("person",),
                            marr=("how",))
        with self.voiceover("Chapter eight. Mediation."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def recipe(self):
        head = heading(r"The recipe")
        X, M, Y = node(r"X", PERSON), node(r"M", MODEL), node(r"Y", GOOD)
        X.move_to([-5.2, -0.6, 0])
        M.move_to([-3.4, 1.0, 0])
        Y.move_to([-1.6, -0.6, 0])
        a = arrow(X, M, color=MODEL, text=r"$a$")
        b = arrow(M, Y, color=GOOD, text=r"$b$")
        c = arrow(X, Y, color=GREY_A, text=r"$c'$")
        rows = rows_of([
            (r"X is a treatment, \ M a proposed mechanism, \ Y the outcome", WHITE),
            (r"regress M on X for $a$; \ regress Y on M and X for $b$ and the direct effect $c'$", MODEL),
            (r"the indirect effect is $a \times b$, \ with a bootstrap interval; \ Baron and Kenny, \ 1986, \ wrote the "
             r"recipe, \ cited tens of thousands of times", PERSON),
            (r"the trap: \ X can be randomized, \ but M is not; \ the regression of Y on M is an observational one", AUTH),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Baron \& Kenny (1986)")
        with self.voiceover(
            "A treatment works. Through what? <bookmark mark='a'/> X is the treatment, M a proposed mechanism, Y the "
            "outcome. <bookmark mark='b'/> Regress M on X for the path a. Regress Y on M and X for the path b, and the "
            "direct effect. <bookmark mark='c'/> The indirect effect is a times b, with a bootstrap interval. Reuben "
            "Baron and David Kenny wrote the recipe in 1986, and it's been cited tens of thousands of times. "
            "<bookmark mark='d'/> Here's the trap. X can be randomized, but M is not. The regression of Y on M is an "
            "observational one, with every confound that brings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(VGroup(X, M, Y)))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(a), FadeIn(b), FadeIn(c))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def trap(self):
        d = load("mediation")
        head = heading(r"A mechanism that is not there")
        X, M, Y = node(r"X", PERSON), node(r"M", MODEL), node(r"Y", GOOD)
        U = node(r"U", AUTH, latent=True, r=0.4)
        X.move_to([-5.4, -1.0, 0])
        M.move_to([-3.4, 0.6, 0])
        Y.move_to([-1.4, -1.0, 0])
        U.move_to([-2.4, 2.2, 0])
        a = arrow(X, M, color=MODEL, text=r"$a = 0.5$")
        u1, u2 = arrow(U, M, color=AUTH), arrow(U, Y, color=AUTH)
        none = label(r"no arrow from M to Y", font_size=14, color=GREY_B).move_to([-3.4, -1.6, 0])
        A = axes([-0.1, 0.35], [0, 2], x_length=5.4, y_length=1.0, xticks=[0, 0.1, 0.2, 0.3], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"indirect effect $a\times b$", center=[3.4, -2.2, 0], font_size=12)
        ci = Line(A.ax.c2p(d["lo"], 1), A.ax.c2p(d["hi"], 1), color=AUTH, stroke_width=6)
        pt = Dot(A.ax.c2p(d["indirect"], 1), radius=0.08, color=AUTH)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, 2), color=GOOD, stroke_width=2)
        z_l = label(r"the truth", font_size=12, color=GOOD).next_to(A.ax.c2p(0, 2), UP, buff=0.05)
        rows = rows_of([
            (r"Psyche: \ X randomized; \ X raises M; \ M does nothing to Y; \ an unmeasured U raises both M and Y", WHITE),
            (rf"the recipe finds an indirect effect of {d['indirect']:.2f}, \ 95\% interval {d['lo']:.2f} to "
             rf"{d['hi']:.2f}: \ a mechanism, \ significant, \ and false", AUTH),
            (r"randomizing X protects the total effect, \ not the split into paths", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, 1.0, 0])
        tag = psyche_tag(rf"\texttt{{sem.mediation}}, \ {500} simulated people")
        with self.voiceover(
            "Watch the trap close. <bookmark mark='a'/> Psyche runs an experiment. X is randomized, and X raises M. "
            "But M does nothing at all to Y. An unmeasured trait, U, raises both M and Y. <bookmark mark='b'/> The "
            "recipe finds an indirect effect of about zero point one seven, with an interval well clear of zero. A "
            "mechanism, significant, and false. <bookmark mark='c'/> Randomizing X protects the total effect, not its "
            "split into paths."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(VGroup(X, M, Y, U)), FadeIn(a), FadeIn(none))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(u1), FadeIn(u2))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(A), FadeIn(zero), FadeIn(z_l), FadeIn(ci), FadeIn(pt))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def fixes(self):
        head = heading(r"What would show a mechanism")
        data = (
            (r"manipulate M", r"a second experiment that moves the mechanism directly, \ and watches Y", GOOD),
            (r"design in parallel", r"the treatment with and without the mechanism blocked", MODEL),
            (r"sensitivity", r"how strong would a confound of M and Y have to be to erase the indirect effect?", SYMP),
            (r"say less", r"``consistent with mediation'', \ never ``explained by'', \ from one randomized X", YOU),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=18, width=3.0), wrapped_label(how, 8.8, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.38).move_to([0, 0.4, 0])
        foot = wrapped_label(r"Bullock, \ Green and Ha, \ 2010: \ ``Yes, \ but what's the mechanism? \ (Don't "
                             r"expect an easy answer)''; \ glucose as the mediator of self-control is this chapter's "
                             r"Ledger row", 12.4, 20, PERSON).move_to([0, -2.5, 0])
        tag = published_tag(r"Bullock, Green \& Ha (2010)")
        with self.voiceover(
            "So what would show a mechanism? <bookmark mark='a'/> Manipulate M: a second experiment that moves the "
            "mechanism directly, and watches Y. <bookmark mark='b'/> Or design in parallel: the treatment with and "
            "without the mechanism blocked. <bookmark mark='c'/> At least, a sensitivity analysis: how strong would a "
            "confound of M and Y have to be to erase the indirect effect? <bookmark mark='d'/> Or say less: "
            "consistent with mediation, never explained by, from one randomized X. <bookmark mark='e'/> John Bullock, "
            "Donald Green and Shang Ha made the case in 2010, under the title: yes, but what's the mechanism? Don't "
            "expect an easy answer. This chapter's Ledger row is a mediator that failed when it was manipulated."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
