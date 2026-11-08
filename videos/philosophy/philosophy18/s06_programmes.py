from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Programmes(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Programmes, anarchy and problems", r"What makes one research tradition better?",
                            lit=(1970, 1977), part=PART)
        with self.voiceover("Chapter five. Programmes, anarchy and problems."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.lakatos()
        self.planets()
        self.feyerabend()

    def lakatos(self):
        hc = history_card(1970, r"Imre Lakatos", r"`Falsification and the Methodology of Scientific Research "
                                                r"Programmes'", width=7.4, color=HIST).to_corner(UL, buff=0.3)
        core = Circle(radius=0.9, color=REAL, fill_opacity=0.25).move_to([-3.4, -0.9, 0])
        belt = Annulus(inner_radius=0.95, outer_radius=1.9, color=THEORY, fill_opacity=0.15).move_to(core)
        cl = label(r"hard core", font_size=19, color=REAL).move_to(core)
        bl = label(r"protective belt", font_size=17, color=THEORY).move_to(core.get_center() + DOWN * 1.45)
        hits = VGroup(*[Arrow(core.get_center() + 3.0 * np.array([np.cos(a), np.sin(a), 0]),
                              core.get_center() + 1.95 * np.array([np.cos(a), np.sin(a), 0]), buff=0, color=DATA,
                              stroke_width=3) for a in (0.4, 1.9, 3.3, 4.9)])
        side = stack([(r"hard core: \ never given up \ (Newton's three laws and gravitation)", REAL),
                      (r"protective belt: \ auxiliary hypotheses, \ adjusted when anomalies strike", THEORY),
                      (r"progressive: \ adjustments predict \textit{novel} facts, \ some confirmed", OK),
                      (r"degenerating: \ adjustments only accommodate, \ after the fact", BAD),
                      (r"rational to stay with a degenerating programme? \ for a while: \ no instant rationality", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=6.2).move_to([3.4, -0.7, 0])
        with self.voiceover(
            "Imre Lakatos tried to reconcile Popper's falsificationism with Kuhn's history. "
            "<bookmark mark='a'/>The unit of appraisal is not a theory but a research programme. At its centre is a "
            "hard core that scientists decide never to give up, such as Newton's laws of motion and gravitation. "
            "<bookmark mark='b'/>Around it is a protective belt of auxiliary hypotheses, which absorb the impact of "
            "anomalies. <bookmark mark='c'/>A programme is progressive if its adjustments predict novel facts, and "
            "some of the predictions are confirmed. <bookmark mark='d'/>It is degenerating if its adjustments only "
            "accommodate facts already known. <bookmark mark='e'/>There is no instant rationality: a degenerating "
            "programme can recover, so judgements are made in hindsight."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(core), FadeIn(cl), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(belt), FadeIn(bl), LaggedStart(*[GrowArrow(h) for h in hits], lag_ratio=0.2),
                      FadeIn(side[1]))
            for mk, r in zip("cde", side[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def planets(self):
        head = label(r"Two anomalies, \ one programme", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Uranus \ (1845--46)", r"its orbit wanders; \ Le Verrier and Adams posit an outer planet; \ Galle finds "
                                     r"Neptune within about $1^\circ$ of Le Verrier's position", OK),
            (r"the lesson", r"an auxiliary hypothesis that predicted a novel fact: \ progressive", OK),
            (r"Mercury \ (1859)", r"its perihelion advances too fast \ (38 arcseconds a century; \ later 43); \ Le "
                                  r"Verrier posits Vulcan, \ inside Mercury's orbit", BAD),
            (r"the lesson", r"Vulcan was never found; \ general relativity explained the 43 seconds \ (1915)", BAD),
            (r"for Lakatos", r"the same move, \ two fates: \ only hindsight tells progress from degeneration", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.8, x_text=-2.6)
        with self.voiceover(
            "The history of Newtonian astronomy shows both kinds of move. <bookmark mark='a'/>In the 1840s Uranus "
            "wandered from its predicted orbit. Urbain Le Verrier and John Couch Adams posited an unseen outer "
            "planet, and in 1846 Johann Galle found Neptune within about a degree of Le Verrier's position. "
            "<bookmark mark='b'/>An auxiliary hypothesis predicted a novel fact: progress. "
            "<bookmark mark='c'/>In 1859 Le Verrier found that Mercury's perihelion advances faster than Newton "
            "allows, by thirty-eight arcseconds a century, later refined to forty-three, and proposed another "
            "planet, Vulcan, inside Mercury's orbit. "
            "<bookmark mark='d'/>Vulcan was never found. In 1915 Einstein's general relativity explained the "
            "forty-three seconds exactly. <bookmark mark='e'/>The same methodological move had two fates, and only "
            "hindsight distinguished them."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def feyerabend(self):
        head = label(r"Anarchy, \ and problem solving", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Feyerabend \ (1975)", r"\textit{Against Method}: \ every methodological rule has been broken by some "
                                     r"great advance; \ `anything goes'", BAD),
            (r"his example", r"Galileo defended Copernicus with rhetoric, \ propaganda and a telescope no one trusted",
             GREY_A),
            (r"Laudan \ (1977)", r"\textit{Progress and its Problems}: \ science aims to solve problems; \ a tradition "
                                 r"progresses if it solves more, \ and more important ones", OK),
            (r"truth set aside", r"progress without convergence to truth: \ a theme the realism debate takes up", ANTI),
            (r"Feyerabend's point", r"not that method is useless, \ but that no single method is mandatory", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6, x_text=-2.6)
        with self.voiceover(
            "Two more voices completed the debate. <bookmark mark='a'/>Paul Feyerabend, Lakatos's friend, argued in "
            "Against Method that every methodological rule has been broken by some great advance, and that the only "
            "universal principle is: anything goes. <bookmark mark='b'/>His case study was Galileo, who defended "
            "Copernicus with rhetoric, propaganda, and a telescope whose images few trusted. "
            "<bookmark mark='c'/>Larry Laudan proposed that science aims at solving problems, empirical and "
            "conceptual, and that a research tradition progresses when it solves more problems, and more important "
            "ones. <bookmark mark='d'/>On this view progress does not require approaching the truth, a theme the "
            "realism debate takes up next. <bookmark mark='e'/>And Feyerabend's real point was not that method is "
            "useless, but that no single method is mandatory."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
