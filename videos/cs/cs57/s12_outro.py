from __future__ import annotations

from explainer import narration_credit
from explainer.cs import *  # noqa: F403
from videos.cs.cs57.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES


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
        head = label(rf"Part {PART}: \ Learning Theory", font_size=34).to_edge(UP, buff=0.3)
        tiles = Group(
            tile(MathTex(r"m \ge \tfrac{1}{\epsilon}\left(\ln|\mathcal H| + \ln\tfrac1\delta\right)",
                         font_size=40, color=HEAD), r"PAC", HEAD),
            tile(MathTex(r"\sum_{i \le d} \binom{m}{i}", font_size=50, color=YES), r"Sauer--Shelah", YES),
            tile(MathTex(r"(R/\gamma)^2", font_size=56, color=DATA), r"margins", DATA),
            tile(MathTex(r"\sqrt{T \ln N}", font_size=56, color=KERN), r"regret", KERN),
            tile(label(r"parity hides from statistics", font_size=30, color=NO), r"limits", NO),
            tile(label(r"keep four points", font_size=36, color=LAM), r"compression", LAM),
        ).arrange_in_grid(rows=2, cols=3, buff=(0.35, 0.35)).move_to(DOWN * 0.2)
        with self.voiceover(
            "What we built in this part. PAC learning, where a finite class needs examples in proportion to the "
            "logarithm of its size. The VC dimension, the Sauer–Shelah lemma, and the fundamental theorem: a class is "
            "learnable exactly when its VC dimension is finite. Margins, which bound the perceptron's mistakes and "
            "explain boosting, whatever the dimension. Online learning against an adversary, where regret grows like "
            "a square root, and bandits that balance exploring against exploiting. Problems such as sparse parity "
            "that no statistical learner can find quickly. And double descent and compression. One idea runs through "
            "it: learning is possible exactly when the hypotheses are simple enough to be pinned down by the data."
        ):
            self.play(FadeIn(head))
            self.play(LaggedStart(*[FadeIn(t, shift=UP * 0.15) for t in tiles], lag_ratio=0.25), run_time=4.0)
        self.wait(0.5)
        self.clear_scene()

    def payoffs(self):
        card = payoff_card([
            (r"what programs mean", [58]),
            (r"learning in distributed systems", [59]),
            (r"hardware for learning", [60]),
            (r"measuring results honestly", [61]),
            (r"the bridge to \textit{AI, Built}", [61]),
        ], font_size=23)
        with self.voiceover(
            "Where this comes back. Part 58 asks what programs mean, learned ones included. Part 59 studies what many "
            "machines can compute together. Part 60 builds the hardware that trains and runs learned models. And Part "
            "61 asks how to measure a result honestly, and returns to the bridge between this series and AI, Built."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.3), run_time=3.0)
        self.wait(0.5)
        self.clear_scene()

    def practice(self):
        card = practice_card([
            (r"validate", r"hold out data the model never saw; \ never tune on the test set"),
            (r"size", r"more data beats a cleverer model when the model is already flexible"),
            (r"regularize", r"margins, \ weight decay and early stopping control capacity"),
            (r"explore", r"bandits for online choices; \ Thompson sampling is a strong default"),
            (r"distrust", r"a result that looks too good: \ look for leakage first"),
        ])
        with self.voiceover(
            "In practice. Hold out data the model never sees, and never tune on the test set. When the model is "
            "already flexible, more data usually beats a cleverer model. Control capacity with margins, weight decay "
            "and early stopping. Use bandits for online choices; Thompson sampling is a strong default. And when a "
            "result looks too good, look for leakage first."
        ):
            self.play(FadeIn(card.head), LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.rows],
                                                     lag_ratio=0.35), run_time=3.0)
        self.wait(0.3)
        self.clear_scene()

    def problems(self):
        ps = problem_set([
            r"Show that half-planes in the plane have VC dimension 3, \ and axis-aligned rectangles have VC "
            r"dimension 4.",
            r"Prove the Sauer--Shelah lemma by induction on $m + d$.",
            r"Prove Novikoff's bound: \ the perceptron makes at most $(R/\gamma)^2$ mistakes on separable data.",
            r"Show that Hedge with the right learning rate has regret at most $\sqrt{(T/2) \ln N}$.",
            r"\textit{Build.} \ Implement UCB1 and Thompson sampling for Bernoulli arms, \ and compare their regret "
            r"with the Lai--Robbins rate.",
            r"$\bigstar$ \textit{Research.} \ The sample compression conjecture.",
        ], font_size=22)
        with self.voiceover(
            "Six problems, with full solutions in the part's notes. Pause on any of them. The fifth is a build "
            "problem: implement two bandit algorithms and compare their regret with the Lai–Robbins rate. The last, "
            "marked with a star, is a research problem: whether every class of VC dimension d can be compressed to a "
            "number of points proportional to d."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(6.0)
        self.clear_scene()

    def next_time(self):
        nxt = label(r"Next: \ Part 58, \ Semantics", font_size=40).to_edge(UP, buff=0.6)
        items = VGroup(*[label(t, font_size=26, color=c) for t, c in (
            (r"meaning as steps: \ operational semantics", HEAD),
            (r"meaning as mathematics: \ domains and fixed points", YES),
            (r"logical relations and theorems for free", DATA),
            (r"effects, \ dependent types and processes", LAM))]).arrange(DOWN, buff=0.35)
        with self.voiceover(
            "Next time, Part 58: semantics. What does a program mean? Three answers: the steps a machine takes, the "
            "mathematical object a program denotes, and the laws it obeys, with a theorem that writes code's "
            "properties for free."
        ):
            self.play(FadeIn(nxt), LaggedStart(*[FadeIn(i) for i in items], lag_ratio=0.3))
        self.wait(0.5)
        self.clear_scene()

    def references(self):
        card = reference_card(
            [r"Shalev-Shwartz and Ben-David, \ \textit{Understanding Machine Learning}; \ Mohri, \ Rostamizadeh "
             r"and Talwalkar",
             r"Cesa-Bianchi and Lugosi, \ \textit{Prediction, Learning, and Games}; \ Lattimore and Szepesv\'ari, \ "
             r"\textit{Bandit Algorithms}"],
            [r"Valiant \ (1984); \ Vapnik and Chervonenkis \ (1971); \ Littlestone \ (1988)",
             r"Freund and Schapire \ (1997); \ Novikoff \ (1962); \ Lai and Robbins \ (1985)",
             r"Kearns and Valiant \ (1994); \ Belkin et al. \ (2019); \ Bartlett et al. \ (2020)",
             r"Littlestone and Warmuth \ (1986); \ Moran and Yehudayoff \ (2016)"])
        credit = note(rf"narration: \ {narration_credit()}", font_size=18).to_edge(DOWN, buff=0.15)
        with self.voiceover("The books and papers this part follows are on screen and in the notes. Thank you for "
                            "watching."):
            self.play(FadeIn(card), FadeIn(credit))
        self.wait(2.0)


_ = (NO, YES, KERN, LAM, DATA)
