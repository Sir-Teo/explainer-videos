from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Demarcation(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Demarcation revisited", r"What makes astrology not a science?", lit=(1934, 1983),
                            part=PART)
        with self.voiceover("Chapter fourteen. Demarcation revisited."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.criteria()
        self.cluster()
        self.strings()

    def criteria(self):
        head = label(r"One criterion after another", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"verifiability", r"the Vienna Circle: \ meaningful iff verifiable \ (Chapter 1: \ Church)", BAD),
            (r"falsifiability", r"Popper \ (1934): \ scientific iff it forbids something \ (Part 15)", REAL),
            (r"its trouble", r"astrology makes falsifiable predictions, \ and they fail; \ is it then bad science, \ "
                             r"not non-science?", BAD),
            (r"Kuhn \ (1970)", r"science is marked by puzzle-solving: \ astrology had no puzzles to solve", THEORY),
            (r"Lakatos", r"a degenerating research programme, \ like Freudian or Marxist theory as he saw them", THEORY),
            (r"Laudan \ (1983)", r"`The Demise of the Demarcation Problem': \ no necessary and sufficient conditions "
                                 r"exist; \ ask instead whether a claim is well supported", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.6, x_text=-2.6)
        with self.voiceover(
            "Where does science end? <bookmark mark='a'/>The Vienna Circle answered with verifiability, which "
            "Church's argument emptied. <bookmark mark='b'/>Karl Popper answered with falsifiability: a theory is "
            "scientific if it forbids something, so that some observation could refute it. "
            "<bookmark mark='c'/>The trouble is that astrology does make falsifiable predictions, and they fail. "
            "By Popper's test it is science, only bad science. <bookmark mark='d'/>Kuhn proposed instead that "
            "science is marked by normal puzzle-solving, and astrology never had puzzles to solve. "
            "<bookmark mark='e'/>Lakatos called pseudosciences degenerating research programmes, and so classed "
            "Freudian and Marxist theory as he saw them. <bookmark mark='f'/>In 1983 Larry Laudan declared the "
            "problem dead: there are no necessary and sufficient conditions for being science, and we should ask "
            "of each claim whether it is well supported."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def cluster(self):
        head = label(r"Demarcation as a cluster concept", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        feats = [r"testability", r"track record", r"self-correction", r"peer criticism", r"coherence with other "
                 r"sciences", r"methodological transparency", r"progress over time"]
        rows_x = [(-4.8, 1.2), (-1.6, 1.2), (1.6, 1.2), (4.8, 1.2), (-3.2, 0.2), (0.0, 0.2), (3.2, 0.2)]
        chips = VGroup()
        for t, (x, y) in zip(feats, rows_x):
            c = VGroup(RoundedRectangle(width=2.9, height=0.6, corner_radius=0.15, color=OK, stroke_width=2),
                       label(t, font_size=17, color=OK))
            if c[1].width > 2.7:
                c[1].width = 2.7
            c[1].move_to(c[0])
            chips.add(c.move_to([x, y, 0]))
        rows = stack([
            (r"Pigliucci and Boudry \ (2013): \ science is a family-resemblance concept, \ like `game'", REAL),
            (r"no single feature is necessary; \ enough of them together make the difference", WHITE),
            (r"the stakes are practical: \ courts \ (\textit{Daubert}, \ 1993), \ creationism in schools \ "
             r"(\textit{McLean v. Arkansas}, \ 1982), \ medicine, \ climate", BAD),
            (r"and new cases: \ string theory's testability; \ machine-learned models nobody understands", GOAL),
        ], font_size=20, width=12.6).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The problem did not stay dead. <bookmark mark='a'/>Massimo Pigliucci and Maarten Boudry revived it in "
            "2013 with a different logic: being scientific is a cluster concept, like Wittgenstein's game. There "
            "are many marks: testability, a track record, self-correction, criticism by peers, coherence with "
            "other sciences, transparency of method, progress over time. <bookmark mark='b'/>None is necessary, "
            "but enough of them together make the difference. <bookmark mark='c'/>The stakes are practical. Courts "
            "must decide what counts as scientific evidence, as the United States Supreme Court did in Daubert in "
            "1993, and whether creationism may be taught as science, as a federal court decided in McLean versus "
            "Arkansas. <bookmark mark='d'/>And new cases keep arriving: whether string theory is testable, and "
            "whether a machine-learned model that predicts well but that no one understands is a scientific theory."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(c) for c in chips], lag_ratio=0.15), run_time=2.5)
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def strings(self):
        hc = history_card(2013, r"Richard Dawid", r"\textit{String Theory and the Scientific Method}", width=6.6,
                          color=HIST).to_corner(UL, buff=0.35)
        rows = [
            (r"the situation", r"string theory makes no prediction testable at accessible energies, \ after fifty "
                               r"years", BAD),
            (r"no alternatives", r"despite great effort, \ no other theory unifies gravity and quantum fields as well",
             THEORY),
            (r"unexpected coherence", r"it explains things it was not built for: \ black-hole entropy, \ "
                                      r"dualities", THEORY),
            (r"meta-induction", r"theories supported by such arguments have tended to be confirmed later", THEORY),
            (r"the critics", r"Ellis and Silk \ (2014): \ `defend the integrity of physics': \ without testability "
                             r"it is not science", BAD),
            (r"the Bayesian reading", r"non-empirical evidence can raise a probability, \ by shrinking the space of "
                                      r"alternatives", GOAL),
        ]
        g = rows_table(rows, top=1.3, gap=0.4, width=8.6, x_text=-2.6, label_size=20)
        with self.voiceover(
            "The demarcation question became urgent in fundamental physics. <bookmark mark='a'/>String theory has "
            "made no prediction testable at energies we can reach, after fifty years of work. "
            "<bookmark mark='b'/>Richard Dawid argued that it can still be confirmed, without new data, by three "
            "arguments. No alternatives: despite great effort, nothing else unifies gravity with quantum fields as "
            "well. <bookmark mark='c'/>Unexpected explanatory coherence: it explains things it was not designed "
            "for, like the entropy of black holes. <bookmark mark='d'/>And a meta-inductive argument: theories "
            "supported in these ways have tended to be confirmed later. <bookmark mark='e'/>George Ellis and Joseph "
            "Silk replied in Nature with a call to defend the integrity of physics: without testability, it is not "
            "science. <bookmark mark='f'/>Read in Bayesian terms, as Part 13 would, Dawid's arguments are evidence "
            "about the space of alternatives, and evidence of that kind can raise a probability. Whether it is "
            "enough is the old question in a new place."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
