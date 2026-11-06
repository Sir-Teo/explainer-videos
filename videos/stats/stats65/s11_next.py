from __future__ import annotations

from videos.stats.stats65.common import *  # noqa: F403


class WhereNext(LectureMixin, VoiceoverScene):
    def construct(self):
        self.card_voiceover("Chapter ten. Where to go next.", 10, r"Where to go next", r"Beyond the series")
        self.books()
        self.problems_left()
        self.journals()
        self.replicate()
        self.habits()

    def books(self):
        self.list_voiceover(
            "<bookmark mark='a'/> A reading list beyond the series, one book for each direction. <bookmark mark='b'/> For "
            "theory: Aad van der Vaart's Asymptotic Statistics, and Martin Wainwright's High-Dimensional Statistics. "
            "<bookmark mark='c'/> For modelling: Andrew Gelman and colleagues' Bayesian Data Analysis, and Trevor Hastie, "
            "Robert Tibshirani and Jerome Friedman's Elements of Statistical Learning. <bookmark mark='d'/> For causes: "
            "Miguel Hernan and James Robins's Causal Inference: What If, and Guido Imbens and Donald Rubin's book. <bookmark "
            "mark='e'/> And for the frontier: Anastasios Angelopoulos, Rina Foygel Barber and Stephen Bates's book on "
            "conformal prediction, and the arXiv's statistics listings, every morning.",
            [(r"beyond the series:", GREY_A),
             (r"theory: \ van der Vaart; \ Wainwright", S.EST),
             (r"modelling: \ Gelman et al.; \ Hastie, \ Tibshirani \& Friedman", S.KEPT),
             (r"causes: \ Hern\'an \& Robins; \ Imbens \& Rubin", S.ALT),
             (r"the frontier: \ Angelopoulos, \ Barber \& Bates; \ arXiv stat", S.ACCENT)],
            buff=0.42, font_size=25, head_size=32)

    def journals(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> Where the field talks. <bookmark mark='b'/> The Annals of Statistics, the Journal of the "
            "Royal Statistical Society, Biometrika and the Journal of the American Statistical Association, for methods and "
            "theory. <bookmark mark='c'/> Applied journals in every science, where the methods meet their data and often "
            "fail in instructive ways. <bookmark mark='d'/> And the machine-learning conferences, where much of the frontier "
            "of Parts fifty-six to sixty-four now appears first.",
            [(r"\text{methods, \ theory}", r":", r"\text{Annals, \ JRSS, \ Biometrika, \ JASA}", 40),
             (r"\text{applications}", r":", r"\text{every science's journals}", 40),
             (r"\text{machine learning}", r":", r"\text{NeurIPS, \ ICML, \ COLT}", 40),
             (r"\text{preprints}", r":", r"\text{arXiv stat and math.ST}", 40)],
            [r"the core", r"where methods meet data", r"the fast frontier", r"daily"],
            colors=[(0, S.EST)])

    def habits(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> And four habits, the degree's in summary. <bookmark mark='b'/> Ask what the data could "
            "have been, not only what they are: the sampling distribution is the subject. <bookmark mark='c'/> Say what is "
            "assumed, and test what can be tested by simulation before trusting it. <bookmark mark='d'/> Prefer designs that "
            "make assumptions true over models that hope they are. And report what you find, including the broken rows.",
            [(r"\text{ask}", r":", r"\text{what could the data have been?}", 40),
             (r"\text{say}", r":", r"\text{what is assumed}", 40),
             (r"\text{simulate}", r":", r"\text{before trusting}", 40),
             (r"\text{prefer}", r":", r"\text{design over hope; \ report everything}", 40)],
            [r"Part 8", r"every part", r"the Board", r"the dissertation"],
            colors=[(3, S.ACCENT)])

    def problems_left(self):
        self.list_voiceover(
            "<bookmark mark='a'/> The open problems the last ten parts left, as a menu for a real dissertation. <bookmark "
            "mark='b'/> Inference after selection with learned models, and conditional guarantees beyond the marginal. "
            "<bookmark mark='c'/> Anytime-valid inference for complex models, and adaptive experiments with honest "
            "intervals. <bookmark mark='d'/> Robustness to shift and contamination at once, and transport with estimated "
            "maps. <bookmark mark='e'/> Causal inference with learned adjustment sets, interference at scale, privacy beyond "
            "the mean, and statistics with models in every loop. <bookmark mark='f'/> And this dissertation's own: weights "
            "estimated on the same data, and a bound that sees the scores.",
            [(r"open, \ from Parts 56--65:", GREY_A),
             (r"selection with learned models; \ conditional guarantees", S.EST),
             (r"anytime-valid inference for complex models", S.KEPT),
             (r"shift and contamination together; \ estimated transport", S.ALT),
             (r"learned adjustment; \ interference; \ privacy; \ models in the loop", S.PRIOR),
             (r"this thesis: \ cross-fitted weights; \ a score-aware bound", S.ACCENT)],
            buff=0.38, font_size=25, head_size=32)

    def replicate(self):
        self.lad_voiceover(
            "<bookmark mark='a'/> The best way to keep learning, after a course like this one. <bookmark mark='b'/> Pick "
            "a paper you admire, and replicate its main table: its simulations, then its data analysis. <bookmark "
            "mark='c'/> You will find the choices the paper did not report, the tuning it needed, and, now and then, a "
            "result that does not reproduce. Each is a lesson no textbook gives. <bookmark mark='d'/> Then change one "
            "assumption and run it again. That is how most of this series' Board rows were made, and how most "
            "dissertations begin.",
            [(r"\text{pick}", r":", r"\text{a paper you admire}", 40),
             (r"\text{replicate}", r":", r"\text{its table, \ then its data}", 40),
             (r"\text{you will find}", r":", r"\text{unreported choices}", 40),
             (r"\text{then}", r":", r"\text{change one assumption}", 40)],
            [r"practice", r"reproduction", r"the hidden forks", r"a question is born"],
            colors=[(3, S.ACCENT)])
