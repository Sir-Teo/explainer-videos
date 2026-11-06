from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.puzzle()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"The determination of the value of an item must not be based on its price, \ but rather on "
                       r"the utility it yields.", r"Daniel Bernoulli",
                       r"`Exposition of a New Theory on the Measurement of Risk' \ (1738)", width=9.0,
                       font_size=29).next_to(t, DOWN, buff=0.45)
        with self.voiceover(
            "Part 32 asked whether our choices are free. This part asks what it is to choose well, the theory of "
            "rational choice. <bookmark mark='a'/>It begins in 1738, with Daniel Bernoulli: the value of an item must "
            "not be based on its price, but on the utility it yields. <bookmark mark='b'/>From that sentence grew "
            "expected utility theory, the most successful formal theory in the social sciences, and a set of "
            "puzzles it has never fully absorbed."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=PREF, scale_factor=1.03))
        self.clear_scene()

    def puzzle(self):
        head = label(r"Four questions about choice", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"what to maximize", r"money, \ utility, \ or something that cares about risk itself?", PREF),
            (r"under ignorance", r"when probabilities are unknown, \ or expectations do not exist", RISK),
            (r"over time", r"how much to bet, \ and how to bind a future self", MONEY),
            (r"against a predictor", r"does a choice count for what it causes, \ or for what it indicates?", AGENT),
        ]
        g = rows_table(rows, top=1.6, gap=0.55)
        with self.voiceover(
            "Four questions run through it. <bookmark mark='a'/>What should a rational agent maximize: money, "
            "utility, or something that also cares about risk itself? <bookmark mark='b'/>How should it choose when "
            "probabilities are unknown, or when expectations do not exist at all? <bookmark mark='c'/>How much should "
            "it bet over time, and how should it deal with a future self who will want something else? "
            "<bookmark mark='d'/>And when a reliable predictor is involved, does a choice count for what it causes, "
            "or for what it is evidence of? Two of these puzzles, Allais's and Newcomb's, are this part's brick in "
            "the Wall."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"preferences, \ and a money pump, \ built; \ St Petersburg, \ simulated",
            r"the von Neumann--Morgenstern theorem; \ the triangle's parallel lines",
            r"Allais, \ checked against every utility; \ Savage and the sure-thing principle",
            r"Ellsberg and ambiguity; \ risk-weighted utility; \ prospect theory",
            r"the Kelly criterion, \ 1000 paths; \ the Pasadena game's rearrangements",
            r"Newcomb's problem with any predictor; \ the Price List",
            r"evidential against causal decision theory: \ the smoking lesion, \ death in Damascus",
            r"policies; \ Ulysses; \ Good's theorem, \ checked; \ the two envelopes",
        ], font_size=22)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Preferences, with a money pump built, and the St Petersburg game "
            "simulated. <bookmark mark='b'/>The von Neumann–Morgenstern theorem, and the geometry of its "
            "indifference lines. <bookmark mark='c'/>Allais's paradox, checked against every possible utility, and "
            "Savage's foundations. <bookmark mark='d'/>Ellsberg's urn, risk-weighted utility and prospect theory. "
            "<bookmark mark='e'/>The Kelly criterion, with a thousand simulated fortunes, and a game whose "
            "expectation depends on the order you add it up. <bookmark mark='f'/>Newcomb's problem, with a predictor "
            "of any accuracy, and its Price List. <bookmark mark='g'/>Evidential against causal decision theory, on "
            "the smoking lesion and death in Damascus. <bookmark mark='h'/>And choosing policies, Ulysses at the "
            "mast, the value of information, checked on two thousand problems, and the two envelopes."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefgh", range(8)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
