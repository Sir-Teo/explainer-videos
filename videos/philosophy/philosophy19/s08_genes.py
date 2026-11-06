from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Genes(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Genes, organisms and adaptation", r"Is the organism a vehicle for its genes?",
                            lit=(1976, 1979), part=PART)
        with self.voiceover("Chapter seven. Genes, organisms and adaptation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.selfish()
        self.spandrels()
        self.adaptationism()
        self.systems()

    def selfish(self):
        hc = history_card(1976, r"Richard Dawkins", r"\textit{The Selfish Gene}", width=5.0, color=HIST).to_corner(
            UL, buff=0.35)
        rep = VGroup(RoundedRectangle(width=2.6, height=0.8, corner_radius=0.15, color=GENE, stroke_width=3),
                     label(r"replicator", font_size=20, color=GENE)).move_to([-4.2, 0.4, 0])
        veh = VGroup(Ellipse(width=3.6, height=2.4, color=ORG, stroke_width=3),
                     label(r"vehicle \ / \ interactor", font_size=18, color=ORG)).move_to([-4.2, -1.2, 0])
        rep[1].move_to(rep[0])
        veh[1].move_to(veh[0].get_bottom() + UP * 0.35)
        rep.move_to(veh[0].get_center() + UP * 0.25)
        rows = stack([(r"genes are the replicators: \ copied with high fidelity, \ potentially immortal", GENE),
                      (r"organisms are vehicles built by genes to make more genes", ORG),
                      (r"Hull \ (1980): \ replicators are copied; \ \textit{interactors} meet the environment", GROUP),
                      (r"the extended phenotype \ (1982): \ a beaver's dam is a gene's effect too", ALT),
                      (r"a perspective, \ not a new fact: \ the same models, \ different bookkeeping", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=6.6).move_to([3.0, -0.4, 0])
        with self.voiceover(
            "Richard Dawkins popularized the gene's-eye view in 1976. <bookmark mark='a'/>Genes are the true "
            "replicators: copied with high fidelity, and potentially immortal through their copies. "
            "<bookmark mark='b'/>Organisms are vehicles that genes build in order to make more copies of themselves. "
            "<bookmark mark='c'/>The philosopher David Hull refined the distinction: replicators are what gets "
            "copied; interactors are what meets the environment and so determines which replicators get copied. "
            "<bookmark mark='d'/>Dawkins extended the idea outward: a beaver's dam is part of the phenotype of "
            "beaver genes, as much as its teeth. <bookmark mark='e'/>Critics and defenders agree on one point: the "
            "gene's-eye view is a perspective that keeps the same books in a different way, not a new empirical "
            "discovery."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(veh), FadeIn(rep))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def spandrels(self):
        hc = history_card(1979, r"Stephen Jay Gould and Richard Lewontin", r"`The Spandrels of San Marco'",
                          width=6.8, color=HIST).to_corner(UL, buff=0.3)
        base = np.array([-4.4, -1.6, 0])
        arches = VGroup(*[Arc(radius=1.0, start_angle=0, angle=PI, arc_center=base + RIGHT * 2.0 * i + UP * 1.0,
                              color=GREY_B, stroke_width=4) for i in range(2)])
        pillars = VGroup(*[Line(base + RIGHT * x, base + RIGHT * x + UP * 1.0, color=GREY_B, stroke_width=4)
                           for x in (-1.0, 1.0, 3.0)])
        top = Line(base + LEFT * 1.0 + UP * 2.2, base + RIGHT * 3.0 + UP * 2.2, color=GREY_B, stroke_width=4)
        span = Polygon(base + RIGHT * 1.0 + UP * 1.0, base + RIGHT * 0.2 + UP * 2.2, base + RIGHT * 1.8 + UP * 2.2,
                       color=GOAL, fill_opacity=0.5, stroke_width=0)
        sl = label(r"a spandrel", font_size=18, color=GOAL).next_to(span, UP, buff=0.4)
        rows = stack([(r"spandrels: \ the spaces left between arches, \ later decorated", GOAL),
                      (r"they look designed for the paintings, \ but are by-products of the architecture", WHITE),
                      (r"adaptationism tells `just-so stories': \ every trait an optimal adaptation", BAD),
                      (r"alternatives: \ by-products, \ drift, \ developmental constraint, \ history", GENE),
                      (r"Gould and Vrba \ (1982): \ \textit{exaptations}: \ feathers before flight", ORG)],
                     font_size=20, aligned_edge=LEFT, width=6.4).move_to([3.2, -0.5, 0])
        with self.voiceover(
            "Stephen Jay Gould and Richard Lewontin attacked what they called the adaptationist programme. "
            "<bookmark mark='a'/>Their image came from the cathedral of San Marco in Venice. Where a dome rests on "
            "arches, triangular spaces are left between them: spandrels, which were later filled with mosaics. "
            "<bookmark mark='b'/>The spandrels look as if they were designed to hold the paintings, but they are "
            "by-products of the architecture. <bookmark mark='c'/>Biologists, they argued, too often tell just-so "
            "stories in which every trait is an optimal adaptation. <bookmark mark='d'/>Traits can also be by-products, "
            "results of drift, or consequences of developmental constraint and history. <bookmark mark='e'/>Gould "
            "and Elisabeth Vrba added exaptation: a trait that evolved for one role and was co-opted for another, as "
            "feathers apparently evolved before flight."
        ) as vo:
            self.play(FadeIn(hc), Create(pillars), Create(arches), Create(top))
            vo.wait_until("a")
            self.play(FadeIn(span), FadeIn(sl), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def systems(self):
        head = label(r"Beyond the gene's-eye view", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"developmental systems", r"Oyama \ (1985): \ genes are one resource among many; \ no privileged "
                                       r"information carrier", GROUP),
            (r"niche construction", r"organisms change their own selective environments: \ earthworms make soil", ORG),
            (r"parity", r"Griffiths and Gray \ (1994): \ treat genetic and non-genetic causes evenly", GENE),
            (r"the reply", r"genes are special: \ replicated with digital fidelity, \ and selected for their effects",
             ALT),
            (r"Chapter 10", r"whether genes carry `information' is the crux", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.4, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Others push further against the gene's-eye view. <bookmark mark='a'/>Developmental systems theory, "
            "from Susan Oyama, holds that genes are one developmental resource among many, alongside cell "
            "structures, hormones and environments, with no privileged role as carriers of information. "
            "<bookmark mark='b'/>Niche construction emphasizes that organisms alter their own selective "
            "environments, as earthworms make the soil they live in. <bookmark mark='c'/>Paul Griffiths and Russell "
            "Gray urged parity: treat genetic and non-genetic causes evenly. <bookmark mark='d'/>The reply is that "
            "genes are special: copied with something like digital fidelity, and selected for their effects. "
            "<bookmark mark='e'/>Whether genes carry information in a special sense is the crux, and chapter ten "
            "takes it up with the genetic code itself."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def adaptationism(self):
        head = label(r"Three adaptationisms \ (Godfrey-Smith, \ 2001)", font_size=30, color=CONN).to_edge(
            UP, buff=0.35)
        rows = [
            (r"empirical", r"selection is a powerful and ubiquitous cause: \ most traits are adaptations", GENE),
            (r"explanatory", r"the big questions, \ apparent design and fit, \ are answered only by selection", ORG),
            (r"methodological", r"assume adaptation first: \ it is the best way to find out what is going on", GROUP),
            (r"the lesson", r"Gould and Lewontin's critique bites on the first, \ less on the other two", GOAL),
            (r"optimality models", r"testable: \ Parker's dung flies stay on a dropping for the time that maximizes "
                                   r"matings", OK),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Peter Godfrey-Smith untangled the debate by distinguishing three adaptationisms. "
            "<bookmark mark='a'/>Empirical adaptationism is a claim about nature: selection is powerful and "
            "ubiquitous, so most traits are adaptations. <bookmark mark='b'/>Explanatory adaptationism says that "
            "the deepest questions in biology, about apparent design and the fit of organisms to their "
            "environments, are answered by selection alone, however common other causes may be. "
            "<bookmark mark='c'/>Methodological adaptationism is advice: look for adaptation first, because that "
            "is the best way to discover what is going on. <bookmark mark='d'/>Gould and Lewontin's critique bites "
            "hardest on the first. <bookmark mark='e'/>And adaptationist hypotheses can be tested. Geoffrey Parker "
            "predicted, with an optimality model, how long male dung flies should stay on a cowpat waiting for "
            "females, and the flies stayed close to the predicted time."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
