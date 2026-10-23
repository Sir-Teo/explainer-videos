from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import CI, EST, HACK, JUDGE, PART, PRIVATE, TRUTH, load


def problem_card(title: str, can: str, cannot: str, color, width=6.3, font_size=21) -> VGroup:
    """An open problem: what we can do today, and what we can't yet."""
    t = label(title, font_size=font_size + 4, color=color)
    a = wrapped_label(r"\textbf{can:} \ " + can, width - 0.5, font_size, GREY_A)
    b = wrapped_label(r"\textbf{not yet:} \ " + cannot, width - 0.5, font_size, WHITE)
    body = VGroup(t, a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.14)
    if body.width > width - 0.35:
        body.width = width - 0.35
    box = RoundedRectangle(width=width, height=body.height + 0.4, corner_radius=0.14, stroke_color=color,
                           stroke_width=1.8, fill_color="#0B0F17", fill_opacity=0.94)
    return VGroup(box, body.move_to(box))


class OpenProblems(VoiceoverScene):
    def construct(self):
        self.card()
        self.measuring()
        self.aligning()
        self.securing()
        self.honest()

    def card(self):
        card = chapter_card(13, r"Open problems", r"What don't we know how to do yet?", lit=(2026,), part=PART)
        with self.voiceover("Chapter thirteen. Open problems."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def row(self, cards):
        g = VGroup(*cards).arrange_in_grid(rows=2, cols=2, buff=(0.3, 0.3), cell_alignment=UL)
        if g.width > 13.4:
            g.width = 13.4
        if g.height > 6.0:
            g.height = 6.0
        return g.move_to(DOWN * 0.45)

    # ------------------------------------------------------------------
    def measuring(self):
        fc = load("forecast")
        later = fc["later"]
        miss = later[-1]["actual"] / later[-1]["pred"]
        head = label(r"Measuring", font_size=38, color=TRUTH).to_edge(UP, buff=0.4)
        cards = self.row([
            problem_card(r"tests a model can't spot", r"build harder, \ more realistic evaluations; \ filter out the "
                         r"implausible ones", r"know that behaviour on a test is behaviour in deployment, \ once models "
                         r"can tell them apart", JUDGE),
            problem_card(r"measuring what matters", r"track benchmarks, \ stitch them together, \ time tasks in human "
                         r"hours", r"keep up: \ most benchmarks saturate within years or months; \ the task rulers stop "
                         r"at about sixteen hours", TRUTH),
            problem_card(r"forecasting", r"fit trends, \ and backtest them", rf"know when a trend will bend: \ our "
                         rf"backtest was too low by ${miss:.0f}\times$ within fifteen months", EST),
        ])
        with self.voiceover(
            "What doesn't work yet? First, measurement. <bookmark mark='a'/> We can build harder and more realistic tests, but once a model "
            "can tell a test from the real thing, we can't be sure that what it does in one it does in the other. "
            "<bookmark mark='b'/> We can track benchmarks and stitch them together, but most saturate within a few "
            "years, or months, and the best ruler for long tasks already runs out at about sixteen hours. "
            "<bookmark mark='c'/> And we can fit trends and backtest them, but not know in advance when a trend will "
            f"bend: our own backtest came in {miss:.0f} times too low within fifteen months."
        ) as vo:
            full = [c_.copy() for c_ in cards]
            for c_ in cards:
                c_.fade(0.8)
            self.play(FadeIn(head), FadeIn(cards))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(Transform(cards[k], full[k]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def aligning(self):
        w = load("w2s")
        aw = float(w["agree_wrong"].mean()) * 100
        head = label(r"Aligning and overseeing", font_size=38, color=HACK).to_edge(UP, buff=0.4)
        cards = self.row([
            problem_card(r"saying what we mean", r"patch the hacks we find; \ shape rewards safely; \ inoculate",
                         r"write an objective that cannot be gamed by something smarter than its author", HACK),
            problem_card(r"overseeing the stronger", r"recover part of the gap with a weak supervisor; \ debate helps "
                         r"weak judges", rf"show it works across a large gap; \ our students copied their supervisor's "
                         rf"mistakes ${aw:.0f}\%$ of the time", C.NEURAL),
            problem_card(r"finding deception", r"catch planted backdoors with probes; \ read chains of thought",
                         r"detect deception that arises on its own, \ in a model that may hide its reasoning", JUDGE),
            problem_card(r"understanding the model", r"find features and circuits \ (Part 30)", r"account for most of "
                         r"what a frontier model computes, \ well enough to certify it", CI),
        ])
        with self.voiceover(
            "Second, alignment and oversight. <bookmark mark='a'/> We patch the reward hacks we find, but we can't "
            "write an objective that something smarter than its author can't game. <bookmark mark='b'/> A weak "
            "supervisor recovers part of the gap, and debate helps weak judges, but nobody has shown either working "
            f"across a large gap; our own students copied their supervisor's mistakes {aw:.0f} percent of the time. "
            "<bookmark mark='c'/> Probes catch deception we planted, but we have no reliable test for deception that "
            "arises on its own, in a model that can hide its reasoning. <bookmark mark='d'/> And interpretability, "
            "Part 30, finds features and circuits, but cannot yet account for most of what a frontier model computes."
        ) as vo:
            full = [c_.copy() for c_ in cards]
            for c_ in cards:
                c_.fade(0.8)
            self.play(FadeIn(head), FadeIn(cards))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(Transform(cards[k], full[k]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def securing(self):
        dps = load("dpsgd")
        dp = dps["dp"]
        cost = dp["held"] - dps["plain"][-1]["held"]
        head = label(r"Securing", font_size=38, color=PRIVATE).to_edge(UP, buff=0.4)
        cards = self.row([
            problem_card(r"robustness", r"layered classifiers, \ thousands of hours of red-teaming", r"a defense that "
                         r"provably holds against an attacker who adapts", PRIVATE),
            problem_card(r"privacy", r"differential privacy with a guarantee, \ at a billion parameters",
                         rf"privacy at the frontier without the cost: \ our tiny model lost ${cost:.2f}$ bits per "
                         r"character", PRIVATE),
            problem_card(r"eliciting what it knows", r"ask, \ probe, \ train for honesty", r"get a model to report what "
                         r"it knows when it would rather not \ (ARC, 2021)", EST),
            problem_card(r"verifying from outside", r"publish frameworks and system cards; \ laws that require them",
                         r"check a developer's claims about training and capability without trusting the developer",
                         TRUTH),
        ])
        with self.voiceover(
            "Third, security. <bookmark mark='a'/> Layered classifiers and thousands of hours of red-teaming raise "
            "the bar, but no defense of a language model has been shown to hold against an attacker who adapts. "
            "<bookmark mark='b'/> Differential privacy gives a real guarantee, at a cost in accuracy that is still too "
            "high for the frontier. <bookmark mark='c'/> We don't know how to get a model to tell us what it knows when "
            "it would rather not, the problem the Alignment Research Center called eliciting latent knowledge. "
            "<bookmark mark='d'/> And outsiders can read frameworks and system cards, but cannot yet check a "
            "developer's claims without trusting the developer."
        ) as vo:
            full = [c_.copy() for c_ in cards]
            for c_ in cards:
                c_.fade(0.8)
            self.play(FadeIn(head), FadeIn(cards))
            for k, m in enumerate("abcd"):
                vo.wait_until(m)
                self.play(Transform(cards[k], full[k]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def honest(self):
        lines = VGroup(
            label(r"None of these is hopeless.", font_size=40),
            label(r"Each has people working on it, \ and partial answers that work today.", font_size=30, color=GREY_A),
            label(r"None is solved.", font_size=40, color=HACK),
        ).arrange(DOWN, buff=0.5)
        with self.voiceover(
            "None of these is hopeless; each has people working on it, and partial answers that work today, many of "
            "which we ran in this part. <bookmark mark='a'/> And none of them is solved. That is the honest state of "
            "the art in October 2026, and the reason the question in this part's title is still a question."
        ) as vo:
            self.play(FadeIn(lines[0]), FadeIn(lines[1]))
            vo.wait_until("a")
            self.play(FadeIn(lines[2], scale=1.1))
        self.wait(0.6)
        self.clear_scene()
