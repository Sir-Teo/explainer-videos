from __future__ import annotations

from videos.economics.econ68.common import *  # noqa: F403


class Question(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Finding a question", r"What makes a question worth a dissertation?",
             "Chapter one. Finding a question.", lit={1963: "Vickrey", 2003: "London", 2007: "Stockholm"},
             scale=("city",), horizon=("a year",))
        self.tests()
        self.literature()

    def tests(self):
        cards = point_cards([
            (r"important", r"congestion wastes time and fuel, \ and the toll moves money from drivers to transit: \ "
             r"who gains and who pays matters to millions", TOLL),
            (r"answerable", r"public data on crossings, \ entries, \ miles and bus speeds, \ before and after a "
             r"date set by law", DATA),
            (r"not yet answered", r"the charge is new, \ and the official figure compares entries with a "
             r"projection: \ other comparisons are open", TRUE),
            (r"yours to answer", r"a design you can defend, \ a model small enough to check, \ a counterfactual "
             r"someone needs", MODEL),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"three tests for a question, \ and a fourth", font_size=30, color=E.ACCENT).to_edge(UP,
                                                                                                    buff=0.5)
        with self.voiceover(
            "A dissertation question has to pass three tests, and a fourth. <bookmark mark='a'/> It must be "
            "important: congestion wastes time and fuel, and this toll moves money from drivers to the subway, so "
            "who gains and who pays matters to millions. <bookmark mark='b'/> It must be answerable: the transit "
            "authority publishes crossings, entries, miles driven and bus speeds, before and after a date fixed by "
            "law. <bookmark mark='c'/> It must not be answered already: the charge is new, and the official figure "
            "compares entries with a projection, so other comparisons are open. <bookmark mark='d'/> And it must be "
            "yours: a design you can defend, a model small enough to check, a counterfactual someone needs."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def literature(self):
        L = tables.LITERATURE_68.data
        line = NumberLine(x_range=[1955, 2030, 10], length=11.6, include_numbers=False, color=GREY_B).move_to(
            DOWN * 0.4)
        ticks = VGroup(*[label(str(y), font_size=15, color=GREY_B).next_to(line.n2p(y), DOWN, buff=0.15)
                         for y in (1960, 1970, 1980, 1990, 2000, 2010, 2020)])
        events = [(L["vickrey"], r"Vickrey: \\ price roads by time and place", MODEL, UP),
                  (L["singapore"], r"Singapore: \\ a licence to enter", DATA, DOWN),
                  (L["london"], r"London: \\ a daily charge", CTRL, UP),
                  (L["stockholm"], r"Stockholm: \\ a trial, \ a vote, \ a tax", TRUE, DOWN),
                  (2025, r"New York: \\ \$9 by day, \ \$2.25 by night", TOLL, UP)]
        marks = VGroup()
        for y, txt, col, side in events:
            d = Dot(line.n2p(y), radius=0.09, color=col)
            t = label(txt, font_size=17, color=col).next_to(d, side, buff=0.55 if side is DOWN else 0.35)
            marks.add(VGroup(d, Line(d.get_center(), t.get_edge_center(-side), stroke_color=col, stroke_width=1.4),
                             t))
        page = label(r"the literature in one page: \ prices cut traffic where they were tried; \ the open "
                     r"questions are who pays, \ how traffic moves in time and space, \ and how long the effect "
                     r"lasts", font_size=19, color=GREY_A)
        page.scale_to_fit_width(min(page.width, 12.4)).to_edge(DOWN, buff=0.4)
        tag = published_tag(r"Vickrey, \ \emph{AER} 53(2) (1963); \ the schemes' official histories", corner=UL,
                            font_size=12)
        with self.voiceover(
            "Then the literature, in one page. <bookmark mark='a'/> In 1963 William Vickrey argued that roads and "
            "transit should be priced by time and place, like electricity. <bookmark mark='b'/> Singapore sold "
            "licences to enter its centre from 1975. <bookmark mark='c'/> London began a daily charge in 2003. "
            "<bookmark mark='d'/> Stockholm ran a trial in 2006, put it to a vote, and kept it from 2007. <bookmark "
            "mark='e'/> New York is the newest case. Where prices were tried, traffic fell; the open questions are "
            "who pays, how traffic moves in time and space, and how long the effect lasts. A good question sits "
            "exactly there."
        ) as vo:
            self.play(Create(line), FadeIn(ticks), FadeIn(tag))
            for mk, m in zip("abcde", marks):
                vo.wait_until(mk)
                self.play(FadeIn(m, shift=UP * 0.05))
            self.play(FadeIn(page))
        self.clear_scene()
