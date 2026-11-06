from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


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
        head = label(rf"Part {PART}: \ Keeping It Running", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"1 - \prod (1 - A_i)", font_size=48, color=HEAD), r"availability composes", HEAD),
            tile(MathTex(r"b = \tfrac{f \cdot 30\,\mathrm{d}}{w}", font_size=50, color=YES), r"burn-rate alerts", YES),
            tile(label(r"retries $+$ jitter, \ under a budget", font_size=36, color=NO), r"overload", NO),
            tile(label(r"eject, \ shed, \ hedge", font_size=40, color=KERN), r"defences", KERN),
            tile(MathTex(r"\tfrac{2\gamma^i}{\gamma + 1}", font_size=56, color=DATA), r"sketches that do not lie",
                 DATA),
            tile(label(r"break it on purpose", font_size=38, color=LAM), r"chaos engineering", LAM),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Availability that multiplies in series and is rescued in parallel, until "
            "a common cause breaks the independence it relies on. An error budget, and alerts derived from it that "
            "page quickly for real trouble and stay quiet for blips. Retries that can hold a system in collapse long "
            "after the trigger, and the backoff, jitter and budgets that prevent it. Breakers, bulkheads, shedding, "
            "ejection and hedges. Metrics, sketches, traces and profiles that do not lie, and load generators that "
            "do. And the Job's own service, broken on purpose, kept within its objective. One idea runs through it: "
            "reliability is not hoped for, it is measured and paid for."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"rendering pipelines and their frame budgets", [51]),
            (r"proving protocols and configurations correct", [54]),
            (r"trusting the software we deploy", [55]),
            (r"the second review: \ the whole machine at once", [56]),
            (r"distributed algorithms and their limits", [59]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 51 renders frames against a sixteen-millisecond budget, an objective of its "
            "own. Part 54 proves protocols and configurations correct before they ship. Part 55 asks whether the "
            "software we deploy can be trusted at all. Part 56, the second review, runs the whole machine at once. "
            "And Part 59 returns to the theory of distributed algorithms and what they cannot do."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"define", r"SLOs in users' terms, \ and an error budget everyone agrees to spend"),
            (r"alert", r"on budget burn over two windows, \ not on causes or single metrics"),
            (r"retry", r"with timeouts, \ jitter and a budget; \ never in every layer"),
            (r"measure", r"latency with histograms or sketches, \ from intended send times"),
            (r"learn", r"blameless post-mortems; \ chaos experiments with a small blast radius"),
        ])
        with self.voiceover(
            "In practice. Define objectives in the terms your users feel, and an error budget the whole team agrees "
            "to spend. Alert on how fast the budget is burning, over a long and a short window, rather than on "
            "every symptom. Retry with timeouts, jitter and a budget, and never at every layer at once. Measure "
            "latency with histograms or sketches, from the time a request should have been sent. And learn from "
            "failure: blameless post-mortems, and chaos experiments that start with a small blast radius."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"A request needs five services of 99.95\% each, \ and each has two replicas. \ What is its "
            r"availability, \ and what if 10\% of each service's downtime is common-mode?",
            r"Derive the burn-rate threshold that pages when 5\% of a 30-day budget is spent in 6 hours, \ and the "
            r"time to detect a burn rate of 10.",
            r"Show that with $L$ layers each retrying $r$ times, \ a failing backend sees $(r+1)^L$ attempts, \ and "
            r"that a 10\% retry budget bounds it by $1.1^L$.",
            r"Prove DDSketch's guarantee: \ every value in bucket $i$ is within relative error $\alpha$ of "
            r"$2\gamma^i / (\gamma + 1)$.",
            r"\textit{Build.} \ Add a circuit breaker and a retry budget to a client, \ and measure goodput through a "
            r"capacity drop.",
            r"$\bigstar$ \textit{Research.} \ The exact set of triggers a retrying server cannot recover from.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: add a circuit breaker and a retry budget to a client, and measure what they do through a drop "
            "in capacity. The last, marked with a star, is a research problem: derive, rather than simulate, the "
            "triggers from which a retrying server cannot recover."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 51, \ Light and Pixels", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"perspective as linear algebra plus one division", HEAD),
            (r"rasterization, \ and why $1/w$", YES),
            (r"sampling, \ aliasing and mipmaps", DATA),
            (r"a path tracer whose noise falls as $1/\sqrt{N}$", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 51, which opens the last act: light and pixels. A picture is millions of samples of "
            "light. Projecting triangles onto a screen is linear algebra plus one division; getting the samples "
            "right is Nyquist again; and the physics of light is one integral equation, which our own path tracer "
            "solves one bounced ray at a time."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Beyer, \ Jones, \ Petoff and Murphy, \textit{Site Reliability Engineering}; \ \textit{The Site "
             r"Reliability Workbook}",
             r"Nygard, \textit{Release It!}; \ Gregg, \textit{Systems Performance}; \ Jain, \textit{The Art of "
             r"Computer Systems Performance Analysis}"],
            [r"Bronson et al. \ (2021); \ Huang et al. \ (2017, \ 2022); \ Brooker \ (2015)",
             r"Sigelman et al. \ (2010, \ Dapper); \ Masson, \ Rim and Lee \ (2019, \ DDSketch)",
             r"Schroeder, \ Wierman and Harchol-Balter \ (2006); \ Cook \ (1998)",
             r"Basiri et al. \ (2016, \ chaos engineering)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
