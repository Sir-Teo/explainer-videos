from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403


def _g_model(center):
    g = Circle(radius=0.42, color=G, stroke_width=4).move_to(center + np.array([0, 1.0, 0]))
    gl = label(r"$g$", font_size=28, color=G).move_to(g)
    boxes = VGroup(*[Square(0.45, color=WHITE, stroke_width=2).move_to(center + np.array([-1.5 + 0.75 * i, -0.7, 0]))
                     for i in range(5)])
    arrows = VGroup(*[Arrow(g.get_bottom(), b.get_top(), buff=0.05, color=G, stroke_width=3,
                            max_tip_length_to_length_ratio=0.15) for b in boxes])
    return VGroup(arrows, g, gl, boxes)


def _network(center):
    ang = np.linspace(np.pi / 2, np.pi / 2 + 2 * np.pi, 6)[:-1]
    pts = [center + 1.15 * np.array([np.cos(a), np.sin(a), 0]) for a in ang]
    nodes = VGroup(*[Square(0.45, color=WHITE, stroke_width=2).move_to(p) for p in pts])
    edges = VGroup()
    for i in range(5):
        for j in range(i + 1, 5):
            w = 3 if (j - i) in (1, 4) else 1.5
            edges.add(Line(pts[i], pts[j], color=VERB, stroke_width=w, buff=0.25))
    return VGroup(edges, nodes)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.networks()
        self.genes()
        self.machines()
        self.open_()

    def card(self):
        card = chapter_card(15, r"Frontier: \ networks, \ genes and machines", r"What is open?",
                            lit={2018: r"Lee et al.", 2019: r"Kan et al.; \ Chollet", 2022: r"Howe et al."},
                            part=PART, scale=("gene", "mind", "person"), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: networks, genes and machines."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def networks(self):
        head = heading(r"One cause, \ or a web?")
        gm = _g_model(np.array([-3.4, 1.5, 0]))
        nw = _network(np.array([3.4, 1.55, 0]))
        cap = VGroup(label(r"a common cause", font_size=18, color=G).next_to(gm, DOWN, buff=0.25),
                     label(r"a network of abilities", font_size=18, color=VERB).next_to(nw, DOWN, buff=0.25))
        rows = rows_of([
            (r"chapter five: \ a common cause, \ sampling and mutualism all make a positive manifold, \ and a "
             r"one-factor test could not tell them apart", MODEL),
            (r"Kan, \ van der Maas and Levine, \ 2019: \ on standard test batteries, \ network models, \ with "
             r"abilities linked directly, \ fitted the correlations better than models with $g$", VERB),
            (r"McFarland, \ 2020: \ the networks' advantage came from fitting partial correlations; \ Kan and "
             r"colleagues replied that standard software cannot compare the two fairly: \ how to compare them is "
             r"still being worked out", G),
            (r"the decisive evidence is not a better fit but a different prediction: \ train one ability, \ and "
             r"see whether only its neighbours move, \ or everything", YOU),
        ], 12.4, 20, 0.28).move_to([0, -1.85, 0])
        tag = published_tag(r"Kan et al.\ (2019); \ McFarland (2020)")
        with self.voiceover(
            "Three frontiers. The first is what the positive manifold is. <bookmark mark='a'/> Chapter five built "
            "three worlds, a common cause, sampling and mutualism, that all make a positive manifold, and a "
            "one-factor test couldn't tell them apart. <bookmark mark='b'/> In 2019 Kan, van der Maas and Levine "
            "fitted network models, in which abilities are linked directly to one another, to standard test "
            "batteries, and found they fitted the correlations better than models with g. <bookmark mark='c'/> In "
            "2020 McFarland argued that the networks' advantage came from fitting partial correlations rather than "
            "ordinary ones. Kan and colleagues replied that standard software can't compare the two kinds of model "
            "fairly. How to compare them is still being worked out. "
            "<bookmark mark='d'/> The decisive evidence won't be a better fit, but a different prediction. Train "
            "one ability, and see whether only its neighbours move, or everything does: chapter five's experiment, "
            "run on people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(gm), FadeIn(nw), FadeIn(cap))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def genes(self):
        head = heading(r"Genes, \ measured directly")
        A = axes([-0.6, 1.6], [0, 1.1], x_length=4.0, y_length=3.6, xticks=None, yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{v:g}", ylabel=r"effect of the score (population = 1)", center=[-4.4, -0.2, 0],
                 font_size=14)
        b = bars(A.ax, [0, 1], [1.0, 0.53], [G, VERB], width=0.6)
        nm = VGroup(label(r"between families", font_size=16, color=G).next_to(A.ax.c2p(0, 0), DOWN, buff=0.2),
                    label(r"within families", font_size=16, color=VERB).next_to(A.ax.c2p(1, 0), DOWN, buff=0.2))
        rows = rows_of([
            (r"Lee and colleagues, \ 2018: \ a genome-wide study of educational attainment in about 1.1 "
             r"million people; \ a polygenic score explained 11 to 13\% of the variance in education, \ and 7 to "
             r"10\% in cognitive performance", WHITE),
            (r"Howe and colleagues, \ 2022: \ 178{,}000 siblings in 19 cohorts: \ within families, \ the "
             r"genetic associations with education shrank by about 47\%", VERB),
            (r"part of what a score predicts between families runs through the families: \ their homes, \ "
             r"their neighbourhoods, \ and parents' genes acting on children's environments", G),
            (r"so a polygenic score is not yet a measure of a child's potential, \ and should not be sold as one",
             LOST),
        ], 7.4, 20, 0.34).move_to([2.6, -0.3, 0])
        tag = published_tag(r"Lee et al.\ (2018); \ Howe et al.\ (2022)")
        with self.voiceover(
            "The second frontier is genes, measured directly rather than inferred from twins. "
            "<bookmark mark='a'/> In 2018 Lee and colleagues ran a genome-wide study of educational "
            "attainment in about 1.1 million people. A polygenic score built from it explained eleven to thirteen "
            "percent of the variance in education, and seven to ten percent in cognitive performance. "
            "<bookmark mark='b'/> In 2022 Howe and colleagues compared a hundred and seventy-eight "
            "thousand siblings in nineteen cohorts. Within families, the genetic associations with education shrank "
            "by about forty-seven percent. <bookmark mark='c'/> So part of what a score predicts between families "
            "runs through the families themselves: their homes, their neighbourhoods, and parents' genes acting on "
            "their children's environments. <bookmark mark='d'/> A polygenic score isn't yet a measure of a child's "
            "potential, and shouldn't be sold as one."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(nm))
            vo.wait_until("a")
            self.play(FadeIn(b[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(b[1]), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def machines(self):
        d = load("matrices")
        head = heading(r"Intelligence in machines")
        panel = matrix_panel(d["grid2"], cell=0.62).move_to([-4.3, 0.2, 0])
        rows = rows_of([
            (r"Fran\c{c}ois Chollet, \ 2019: \ a skill is not intelligence, \ since enough training data buys any "
             r"skill; \ intelligence is how efficiently a system acquires new skills, \ from little experience and "
             r"the priors it starts with", WHITE),
            (r"his Abstraction and Reasoning Corpus: \ grid puzzles, \ like matrix items, \ each with its own rule "
             r"and only a few examples, \ built on priors children have: \ objects, \ counting, \ symmetry", G),
            (r"Spearman's question, \ asked of machines: \ does a system good at one benchmark tend to be good at "
             r"all of them, \ and is that one ability or many?", MODEL),
            (r"Part 3's lesson carries over: \ a benchmark is a measurement, \ and needs reliability, \ validity "
             r"and fresh items it has not seen", YOU),
        ], 7.6, 20, 0.34).move_to([2.6, -0.3, 0])
        tag = published_tag(r"Chollet (2019)")
        with self.voiceover(
            "The third frontier is machines. <bookmark mark='a'/> In 2019 François Chollet argued that a skill isn't "
            "intelligence, since enough training data can buy any skill. Intelligence, he proposed, is how "
            "efficiently a system acquires new skills, from little experience and the priors it starts with. "
            "<bookmark mark='b'/> His Abstraction and Reasoning Corpus is a set of grid puzzles, like matrix items, "
            "each with its own rule and only a few examples, built on priors young children have: objects, counting, "
            "symmetry. <bookmark mark='c'/> And Spearman's question can be asked of machines. Does a system that's "
            "good at one benchmark tend to be good at all of them, and is that one ability or many? "
            "<bookmark mark='d'/> Part 3's lesson carries over: a benchmark is a measurement, and it needs "
            "reliability, validity, and fresh items that the system hasn't seen."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(panel))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def open_(self):
        head = heading(r"Open questions")
        rows = rows_of([
            (r"is $g$ a cause, \ a sampling summary, \ or a web of abilities that grew together?", G),
            (r"what rose in the Flynn effect, \ and why is it reversing?", COHORT),
            (r"how much of a genetic association runs through families, \ and how much through the child?", VERB),
            (r"can a test be built that is invariant across cultures, \ and what would it measure?", MODEL),
            (r"what is the right measure of intelligence in a machine?", YOU),
        ], 12.4, 26, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "So the open questions. <bookmark mark='a'/> Is g a cause, a sampling summary, or a web of abilities "
            "that grew together? <bookmark mark='b'/> What rose in the Flynn effect, and why is it reversing? "
            "<bookmark mark='c'/> How much of a genetic association runs through families, and how much through "
            "the child? <bookmark mark='d'/> Can a test be built that's invariant across cultures, and what would it "
            "measure? <bookmark mark='e'/> And what is the right measure of intelligence in a machine?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
