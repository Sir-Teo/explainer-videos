from __future__ import annotations

from videos.psychology.psych22.common import *  # noqa: F403

PROBLEMS = [
    r"Show that the generalized context model with one exemplar per category, \ placed at the category's mean, \ "
    r"is a prototype model, \ and find an item of the 5-4 structure on which the two must disagree.",
    r"For centred points $X$, \ prove that $-\tfrac{1}{2} J D^{(2)} J = X X^\top$, \ and say what a negative "
    r"eigenvalue of $B$ tells you about the dissimilarities.",
    r"Show that $\int_0^\infty s\, e^{-s} \max(0,\ 1 - d/s)\, ds = e^{-d}$, \ and find the gradient when sizes are "
    r"uniform on $[0, L]$.",
    r"In the contrast model, \ show that $S(a, b) - S(b, a) = (\beta - \alpha)\,[f(A - B) - f(B - A)]$, \ and say "
    r"when the asymmetry vanishes.",
    r"Show that no examples from 1 to 100 can separate \emph{multiples of 10} from \emph{ending in 0}, \ and say "
    r"what decides between them.",
    r"With \texttt{explainer.psychology.opendata}: \ rerun Tversky's sign count on Rothkopf's table with "
    r"prominence measured by the number of dashes instead of the length.",
    r"$\star$ \ Prototype and exemplar models often predict the same accuracies. \ Design a study whose outcome "
    r"they must predict differently.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.recap()
        self.score()
        self.payoffs()
        self.problems()
        self.references()
        self.next_part()

    def recap(self):
        items = [
            (r"few concepts have definitions; \ membership is graded, \ and typical members come first", CAT_A),
            (r"a prototype is the average member; \ it is recognised though never seen", PROTO),
            (r"exemplar models remember every member and sum the similarities, \ with attention to what matters",
             EXEMPLAR),
            (r"the six problems are learned in an order that attention which learns can explain", MODEL),
            (r"scaling turns confusions into a map: \ Ekman's colour circle, \ Rothkopf's Morse code", SPACE),
            (r"generalization falls exponentially with distance, \ because the region of a consequence is "
             r"uncertain", MODEL),
            (r"similarity is not distance: \ it is asymmetric, \ and built from features", PROTO),
            (r"knowledge is a network, \ not a tree; \ priming is real, \ and small", CAT_B),
            (r"concepts are theories: \ the pizza, \ the raccoon, \ the size principle", CAT_A),
            (r"meaning can be read from company, \ biases included, \ but company is not grounding", LOST),
        ]
        rows = VGroup(*[label(rf"{k + 1}.\ \ {t_}", font_size=30, color=col) for k, (t_, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        head = label(r"Part 22, \ in ten lines", font_size=42).to_edge(UP, buff=0.35)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.4 + 3.7
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.4)
        with self.voiceover(
            "Part twenty-two in ten lines. <bookmark mark='a'/> Few everyday concepts have definitions: membership "
            "is graded, and typical members come first. A prototype is the average member, and people recognise it "
            "though they have never seen it. Exemplar models remember every member and add up the similarities, "
            "paying attention to the features that matter. The six problems of Shepard, Hovland and Jenkins are "
            "learned in an order that an attention which learns can explain. Scaling turns confusions into a map, "
            "like Ekman's colour circle and Rothkopf's Morse code. Generalization falls exponentially with distance "
            "in that map, because the region of a consequence is uncertain. But similarity is not distance: it is "
            "asymmetric, and built from features. Knowledge is a network, not a tree, and priming through it is "
            "real, and small. Concepts are also theories, as the pizza, the raccoon and the size principle show. And "
            "meaning can be read from the company words keep, prejudices included, though company is not grounding."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in rows[1:]], lag_ratio=0.9), run_time=45.0)
        self.clear_scene()

    def score(self):
        board = wager_board((
            (r"a law of generalization derived from uncertainty; \ exemplar, \ attention and Bayesian models fitted "
             r"to open data",
             STATUS_COLOR["replicated"]),
            (r"the six problems run in 1961 and again in 1994, \ the second set of data open to refit",
             STATUS_COLOR["replicated"]),
            (r"similarity read from confusions and choices, \ never from asking people what a concept is",
             STATUS_COLOR["replicated"]),
        ))
        with self.voiceover(
            "Kant's wager. <bookmark mark='a'/> The first objection, that mathematics can't apply to the mind, met a "
            "law of generalization derived from uncertainty, and models of exemplars, attention and inference fitted "
            "to open data. <bookmark mark='b'/> The second, that the mind can't be experimented on, met the six "
            "problems, run in 1961 and again in 1994, with the second set of data open for anyone to refit. "
            "<bookmark mark='c'/> And the third, that looking inward disturbs what you look at, met similarity read "
            "from confusions and choices, never from asking people what their concepts are."
        ) as vo:
            self.play(FadeIn(board.head), *[FadeIn(r_.objection) for r_ in board.rows])
            for m, r_ in zip("abc", board.rows):
                vo.wait_until(m)
                self.play(Indicate(r_.objection, color=KANT), FadeIn(r_.reply, shift=LEFT * 0.2))
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"language: \ words, \ rules and the past tense", [23]),
            (r"essences and kinds in the infant mind", [30]),
            (r"what is a disorder: \ categories or dimensions", [39]),
            (r"scaling, \ surveys and choice", [46]),
            (r"model mimicry: \ when behaviour cannot choose", [48]),
            (r"designing for minds: \ navigation and card sorts", [52]),
            (r"minds and machines: \ the geometry of embeddings", [60]),
        ], font_size=29)
        with self.voiceover(
            "Where this comes back. <bookmark mark='a'/> Language, with words, rules and the past tense, is the next "
            "part. Essences and kinds in the infant mind are Part 30. Whether a disorder is a category or a dimension "
            "is Part 39. Scaling, surveys and choice are Part 46. Model mimicry, when behaviour can't choose between "
            "two theories, is Part 48. Designing for minds, with navigation and card sorts, is Part 52. And the "
            "geometry of machine embeddings is Part 60."
        ) as vo:
            self.play(FadeIn(card.head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.2) for r_ in card.rows], lag_ratio=0.5), run_time=12.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=23)
        with self.voiceover(
            "Seven problems, with full solutions in this part's README. <bookmark mark='a'/> One shows that a "
            "prototype model is a special exemplar model. One proves the double-centring identity. One does Shepard's "
            "integral. One finds the contrast model's asymmetry. One finds two concepts in the number game that no "
            "example can tell apart. One reruns Tversky's count with a different measure of prominence. And the last, "
            "with the star, asks you to design a study on which prototype and exemplar models must disagree. Pause "
            "here if you'd like to try them."
        ) as vo:
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0]), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in ps.rows[1:]], lag_ratio=0.3), run_time=5.0)
        self.wait(4.0)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"G. L. Murphy, \emph{The Big Book of Concepts} (2002)",
             r"E. E. Smith \& D. L. Medin, \emph{Categories and Concepts} (1981)",
             r"E. Margolis \& S. Laurence (eds), \emph{Concepts: Core Readings} (1999)"],
            [r"E. Rosch (1975); \ E. Rosch et al.\ (1976); \ M. I. Posner \& S. W. Keele (1968)",
             r"D. L. Medin \& M. M. Schaffer (1978); \ R. M. Nosofsky (1986); \ J. K. Kruschke (1992)",
             r"R. N. Shepard, \ C. I. Hovland \& H. M. Jenkins (1961); \ R. M. Nosofsky et al.\ (1994)",
             r"R. N. Shepard (1987); \ A. Tversky (1977); \ J. B. Tenenbaum \& T. L. Griffiths (2001)",
             r"A. M. Collins \& M. R. Quillian (1969); \ A. M. Collins \& E. F. Loftus (1975); \ K. A. Hutchison et "
             r"al.\ (2013)",
             r"G. L. Murphy \& D. L. Medin (1985); \ F. C. Keil (1989); \ S. A. Gelman \& E. M. Markman (1986)",
             r"T. K. Landauer \& S. T. Dumais (1997); \ A. Caliskan et al.\ (2017); \ R. Marjieh et al.\ (2024)"])
        with self.voiceover(
            "The books and papers behind this part are listed here and in the README. Gregory Murphy's The Big Book "
            "of Concepts is the field's best guide, honest about what each theory can and can't do."
        ):
            self.play(FadeIn(card))
        self.wait(2.0)
        self.clear_scene()

    def next_part(self):
        hm = homunculus_map(done=PART, height=6.2).move_to([-3.7, 0.1, 0])
        tally = label(r"Act V: \ thinking", font_size=27, color=P.MECH)
        tally.next_to(hm, DOWN, buff=0.15)
        keep_in_frame(tally)
        nxt = VGroup(label(r"Part 23", font_size=32, color=GREY_B), label(r"Language", font_size=40),
                     wrapped_label(r"\emph{Colorless green ideas sleep furiously.} \ How does a child who hears a "
                                   r"finite number of sentences come to understand an infinite number?", 6.0, 28,
                                   GREY_A)).arrange(DOWN, buff=0.3)
        nxt.move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Today's concepts were mostly words: bird, game, fep. <bookmark mark='a'/> Next time, the words "
            "themselves. <bookmark mark='b'/> Colorless green ideas sleep furiously. The sentence is new to you, it "
            "means nothing, and yet you know it is English. How does a child who hears a finite number of sentences "
            "come to understand an infinite number? It's Part 23: language."
        ) as vo:
            self.play(FadeIn(hm), FadeIn(tally))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.5)
        self.clear_scene()
