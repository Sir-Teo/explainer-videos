from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403
from videos.psychology.psych44.diagrams import node, three


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.discovery()
        self.bayes_dynamic()

    def card(self):
        card = chapter_card(15, r"Frontier: \ causal discovery, \ Bayes and dynamic fit",
                            r"Can the arrows be found, \ not assumed?", lit={2000: r"Spirtes et al.",
                                                                            2023: r"McNeish \& Wolf"},
                            part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter fifteen. Frontier: causal discovery, Bayes and dynamic fit."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def discovery(self):
        head = heading(r"Causal discovery")
        X, M, Y = node("X", MODEL), node("M", MODEL), node("Y", MODEL)
        VGroup(X, M, Y).arrange(RIGHT, buff=1.0)
        undirected = VGroup(X, M, Y, Line(X.get_right(), M.get_left(), color=MODEL, stroke_width=3),
                            Line(M.get_right(), Y.get_left(), color=MODEL, stroke_width=3)).scale(0.7)
        coll = three("collider", AUTH).scale(0.7)
        left = VGroup(undirected, wrapped_label(r"chain, \ reverse or fork: \ the edges are found, \ their direction "
                                                r"is not", 5.0, 17, MODEL)).arrange(DOWN, buff=0.3)
        right = VGroup(coll, wrapped_label(r"a collider: \ both arrows found, \ because X and Y are independent "
                                           r"until M is known", 5.0, 17, AUTH)).arrange(DOWN, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=1.2).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"algorithms such as PC (Spirtes, \ Glymour and Scheines) test conditional independences and return the "
             r"family of diagrams that fits, \ orienting only what the data force", WHITE),
            (r"they assume every common cause is measured and no independence is a coincidence; \ psychological data, "
             r"\ with latent traits behind everything, \ rarely oblige", AUTH),
            (r"open question: \ how much can discovery add when the variables are themselves noisy measures?", YOU),
        ], 12.4, 20, 0.34).move_to([0, -1.9, 0])
        tag = published_tag(r"Spirtes, Glymour \& Scheines (2000)")
        with self.voiceover(
            "Can the arrows be found, rather than assumed? <bookmark mark='a'/> Take chapter nine's four diagrams. "
            "For the chain, its reverse and the fork, the data reveal the edges but not their direction. "
            "<bookmark mark='b'/> Only the collider is oriented, because X and Y are independent until M is known. "
            "<bookmark mark='c'/> Algorithms such as Peter Spirtes, Clark Glymour and Richard Scheines's PC test "
            "conditional independences, and return the family of diagrams that fits, orienting only what the data "
            "force. <bookmark mark='d'/> They assume every common cause is measured, and that no independence is a "
            "coincidence. Psychological data, with latent traits behind everything, rarely oblige. "
            "<bookmark mark='e'/> An open question: how much can discovery add when the variables are themselves "
            "noisy measures?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            for m, r in zip("cde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def bayes_dynamic(self):
        head = heading(r"Small samples, \ and fit for this model")
        data = (
            (r"Bayesian SEM", r"priors that keep small cross-loadings near zero instead of exactly zero (Muthén and "
                              r"Asparouhov, \ 2012); \ it helps small samples, \ and the priors must be reported "
                              r"and varied", MODEL),
            (r"dynamic fit", r"simulate from this model, \ with a misspecification of a stated size, \ and set the "
                             r"cut-off from the simulation (McNeish and Wolf, \ 2023): \ chapter five's lesson made "
                             r"routine", GOOD),
            (r"open", r"which misspecifications matter for the question being asked, \ and how big is too big?", YOU),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=18, width=3.0), wrapped_label(how, 8.8, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, -0.2, 0])
        tag = published_tag(r"Muthén \& Asparouhov (2012); McNeish \& Wolf (2023)")
        with self.voiceover(
            "Two more frontiers. <bookmark mark='a'/> Bayesian structural equation models put priors on small "
            "cross-loadings, keeping them near zero instead of exactly zero, as Bengt Muthén and Tihomir Asparouhov "
            "proposed in 2012. It helps small samples, and the priors must be reported and varied. "
            "<bookmark mark='b'/> Dynamic fit simulates from this model, with a misspecification of a stated size, and "
            "sets the cut-off from the simulation, as Daniel McNeish and Melissa Wolf proposed. It makes chapter "
            "five's lesson routine. <bookmark mark='c'/> And open: which misspecifications matter for the question "
            "being asked, and how big is too big?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
