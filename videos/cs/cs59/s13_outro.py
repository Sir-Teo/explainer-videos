from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


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
        head = label(rf"Part {PART}: \ Distributed Computing Theory", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"\log^* n", font_size=60, color=HEAD), r"locality", HEAD),
            tile(MathTex(r"n > 3f", font_size=60, color=NO), r"Byzantine agreement", NO),
            tile(MathTex(r"f + 1", font_size=60, color=YES), r"rounds with crashes", YES),
            tile(label(r"flip a coin", font_size=40, color=DATA), r"randomized consensus", DATA),
            tile(label(r"Sperner's triangle", font_size=34, color=LAM), r"topology", LAM),
            tile(label(r"$A + B \to a + b$", font_size=40, color=KERN), r"population protocols", KERN),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. Models of distributed computation, and the faults they allow. Cole and "
            "Vishkin's colouring of a million-node ring in seven rounds, and Linial's proof that log star is "
            "unavoidable. The f plus one round bound for crashes, and the hexagon that shows three processes cannot "
            "survive one liar. Randomized consensus that escapes FLP; the consensus hierarchy of shared objects; the "
            "topological proof that k-set agreement is impossible; failure detectors; and protocols for "
            "populations of anonymous agents. One idea runs through it: in a distributed system, what each process "
            "cannot know limits what all of them can do."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"hardware networks and their topologies", [60]),
            (r"open problems as research", [61]),
            (r"consensus in practice", [38]),
            (r"scale and replication", [39]),
            (r"verifying protocols", [54]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 60's accelerators are networks of processing elements that pass messages to "
            "neighbours. Part 61 gathers this part's open problems with the series' others. And looking back, it is "
            "the theory under Part 38's consensus, Part 39's replication, and the protocols Part 54 checked."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"assume", r"state the fault model: \ crash, \ omission or Byzantine, \ and how many"),
            (r"bound", r"Byzantine tolerance needs $n > 3f$; \ no protocol beats it"),
            (r"time", r"partial synchrony: \ safety always, \ progress once the network settles"),
            (r"randomize", r"coins break symmetry where determinism cannot"),
            (r"gossip", r"epidemic protocols spread state in $O(\log n)$ rounds"),
        ])
        with self.voiceover(
            "In practice. State the fault model: which failures, and how many. For Byzantine faults no protocol can "
            "tolerate a third or more of the processes lying. Use partial synchrony: safety always, progress once "
            "the network settles. Use randomness to break symmetry where determinism cannot. And spread state by "
            "gossip, which reaches everyone in a logarithmic number of rounds."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Prove that one Cole--Vishkin step keeps neighbouring colours different.",
            r"Show that FloodSet with $f$ crashes reaches agreement in $f + 1$ rounds.",
            r"Use the hexagon argument to show that 3 processes cannot tolerate 1 Byzantine fault.",
            r"Prove Sperner's lemma in two dimensions by counting doors.",
            r"\textit{Build.} \ Implement Ben-Or's consensus and measure its rounds against $n$ with split inputs.",
            r"$\bigstar$ \textit{Research.} \ The deterministic LOCAL complexity of maximal independent set.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: implement Ben-Or's randomized consensus and measure how its rounds grow. The last, marked with "
            "a star, is a research problem: matching bounds for maximal independent set in the LOCAL model."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 60, \ Domain-Specific Hardware", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"the roofline: \ arithmetic intensity", HEAD),
            (r"a systolic array, \ gate by gate", YES),
            (r"the TPU and quantization", DATA),
            (r"the Job in hardware", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 60: hardware built for one job. When the free speedups ended, the answer was "
            "specialization. We build a systolic array in Pebble's gate simulator, put it on the roofline, and end "
            "with the Job in hardware."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Lynch, \ \textit{Distributed Algorithms}; \ Attiya and Welch, \ \textit{Distributed Computing}",
             r"Herlihy, \ Kozlov and Rajsbaum, \ \textit{Distributed Computing through Combinatorial Topology}"],
            [r"Cole and Vishkin \ (1986); \ Linial \ (1992); \ Naor and Stockmeyer \ (1995)",
             r"Fischer, \ Lynch and Merritt \ (1986); \ Dolev and Strong \ (1983); \ Ben-Or \ (1983)",
             r"Herlihy and Shavit \ (1999); \ Borowsky and Gafni \ (1993); \ Saks and Zaharoglou \ (2000)",
             r"Chandra and Toueg \ (1996); \ Angluin et al. \ (2006); \ Rozho\v{n} and Ghaffari \ (2020)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
