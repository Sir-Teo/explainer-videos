from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs44.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


def tile(content, caption, color, TW=3.6, TH=2.3):
    frame = RoundedRectangle(width=TW + 0.3, height=TH + 0.75, corner_radius=0.15, stroke_color=GREY_D,
                             stroke_width=1.5, fill_color=BG, fill_opacity=1)
    if content.width > TW:
        content.scale_to_fit_width(TW)
    if content.height > TH:
        content.scale_to_fit_height(TH)
    content.move_to(frame.get_center() + UP * 0.25)
    cap = label(caption, font_size=22, color=color).move_to(frame.get_bottom() + UP * 0.3)
    return Group(frame, content, cap)


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.payoffs()
        self.practice()
        self.problems()
        self.next_time()
        self.references()

    def recap(self):
        head = label(rf"Part {PART}: \ People and Products", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"a + b \log_2\!\left(\tfrac{D}{W}+1\right)", font_size=44, color=HEAD), r"Fitts's law", HEAD),
            tile(MathTex(r"a + b\,H", font_size=60, color=DATA), r"Hick--Hyman", DATA),
            tile(MathTex(r"\frac{L_1+0.05}{L_2+0.05}", font_size=56, color=YES), r"contrast", YES),
            tile(MathTex(r"1-(1-L)^n", font_size=56, color=LAM), r"how many users", LAM),
            tile(MathTex(r"n \approx \frac{16\sigma^2}{\delta^2}", font_size=52, color=KERN), r"sample size", KERN),
            tile(MathTex(r"(1-\rho^2)\,\sigma^2", font_size=56, color=NO), r"CUPED", NO),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Fitts's law, out of a noisy channel of corrected movements, and Hick's "
            "law, out of the entropy of a choice. Predictions of task time from a few operators. Colour as "
            "formulas, and this series' own palette checked for contrast and for colour-blind viewers. The number "
            "of users a usability study needs, and why the famous five can be too few. The A/B test and its "
            "sample size, the false winners that come from looking every day, a sequential test that is safe to "
            "look at, and CUPED, which removes the variance a user's past already explains. One idea runs through "
            "it: people can be measured, but measuring them well takes the same care as any other experiment."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"experiments on infrastructure: \ canaries and rollouts", [45, 50]),
            (r"logging events at scale for analysis", [46]),
            (r"ranking and its evaluation", [47]),
            (r"glyphs, \ colour and the GPU", [51]),
            (r"learning theory's view of generalization", [57]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Parts 45 and 50 run experiments on infrastructure itself, as canaries and "
            "staged rollouts. Part 46 builds the pipelines that log every event these experiments analyse. Part 47 "
            "ranks search results and measures whether the ranking helps. Part 51 draws glyphs and colour on the "
            "GPU. And Part 57 asks the deeper version of this part's statistical questions: when does what we "
            "measured on some people generalize to the rest?"
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"interfaces", r"big targets near the pointer; \ edges and corners for frequent actions"),
            (r"perception", r"respond within 0.1 s, \ show progress past 1 s, \ let people leave past 10 s"),
            (r"colour", r"contrast of 4.5 to 1 for text; \ never colour alone; \ check a colour-blind view"),
            (r"research", r"test with a few users, \ often; \ fix, \ then test again"),
            (r"experiments", r"fix the sample size in advance, \ or use a sequential test; \ check the split"),
        ])
        with self.voiceover(
            "In practice. Make frequent targets big and close, and use the screen's edges and corners. Respond "
            "within a tenth of a second, show progress after a second, and let people do something else after "
            "ten. Give text a contrast of at least four and a half to one, never use colour as the only signal, "
            "and look at your design through a colour-blind simulation. Test with a few users, often, fixing what "
            "they find between rounds. And fix an experiment's sample size before it starts, or use a sequential "
            "test, and always check that the split is the one you asked for."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Derive Fitts's law from submovements whose endpoint error is proportional to the distance they cover, "
            r"\ and say what sets the slope $b$.",
            r"Show that the best yes/no questioning for a menu with item probabilities $p_i$ needs between $H$ and "
            r"$H + 1$ questions on average.",
            r"Derive $n \approx 16\sigma^2/\delta^2$ per arm for $\alpha = 0.05$ and power 0.8, \ and the sample size "
            r"for a 5\% lift on a 5\% conversion rate.",
            r"Prove that CUPED's estimator is unbiased and that its variance is $(1-\rho^2)$ times the plain one, \ "
            r"for the optimal $\theta$.",
            r"\textit{Build.} \ Simulate daily peeking with a Bonferroni correction over 30 looks, \ and compare its "
            r"power with the mixture SPRT.",
            r"$\bigstar$ \textit{Research.} \ An always-valid sequential test for experiments with interference.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: correct for daily peeking the old-fashioned way, by dividing alpha among thirty looks, and "
            "compare its power with the sequential test. The last, marked with a star, is a research problem: a "
            "sequential test that stays valid when the people in an experiment affect each other."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 45, \ The Cloud", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"a computer rented by the second, \ in a building the size of a stadium", HEAD),
            (r"power, \ cooling and the economics of a datacentre", KERN),
            (r"microVMs, \ containers and bin packing", DATA),
            (r"control loops that make what is match what should be", YES))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 45, and the start of Act Nine: the cloud. A modern application rents its computer by "
            "the second, from a building the size of a stadium. Underneath sit power and cooling budgets, virtual "
            "machines shrunk to micro-VMs, containers placed by bin packing, and control loops that keep making "
            "what is match what should be."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Norman, \textit{The Design of Everyday Things}; \ Card, \ Moran and Newell, \textit{The Psychology of "
             r"Human-Computer Interaction}",
             r"MacKenzie, \textit{Human-Computer Interaction}; \ Kohavi, \ Tang and Xu, \textit{Trustworthy Online "
             r"Controlled Experiments}"],
            [r"Fitts \ (1954); \ Hick \ (1952); \ Hyman \ (1953); \ Meyer et al. \ (1988)",
             r"Nielsen and Landauer \ (1993); \ Machado, \ Oliveira and Fernandes \ (2009); \ Ottosson \ (2020)",
             r"Deng et al. \ (2013, \ CUPED); \ Johari et al. \ (2017); \ Ugander et al. \ (2013)",
             r"Athey et al. \ (2019); \ Warner \ (1965); \ WCAG 2.2"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
