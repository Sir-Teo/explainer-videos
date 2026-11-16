from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Designs(VoiceoverScene):
    def construct(self):
        self.card()
        self.registered()
        self.others()

    def card(self):
        card = chapter_card(7, r"Designs that remove the filter", r"Can the filter be prevented rather than corrected?",
                            lit=(), part=PART, scale=("society",), marr=("how",))
        with self.voiceover("Chapter seven. Designs that remove the filter."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def registered(self):
        head = heading(r"Accept the question, \ not the answer")
        A = axes([0.3, 2.7], [0, 1.05], x_length=4.0, y_length=3.0, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"first hypothesis supported", center=[-3.8, 0.3, 0],
                 font_size=12)
        b = bars(A.ax, [1, 2], [0.96, 0.44], [AUTH, GOOD], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.6, 12, c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, (t, c) in
                         enumerate(((r"standard articles", AUTH), (r"registered reports", GOOD)))])
        rows = rows_of([
            (r"a registered report is reviewed and accepted before the data exist: \ the question and the method are "
             r"judged, \ and the paper is published whatever it finds", WHITE),
            (r"Scheel, \ Schijen and Lakens, \ 2021: \ 96\% of standard psychology articles supported their first "
             r"hypothesis; \ 44\% of registered reports did", PERSON),
            (r"Part 43's row: \ the gap is what filtering predicts, \ though registered reports may also ask riskier "
             r"questions", MODEL),
            (r"for a literature, \ the cure is the denominator: \ every study that was run, \ visible", YOU),
        ], 6.4, 19, 0.36).move_to([3.3, -0.1, 0])
        tag = published_tag(r"Scheel, \ Schijen \& Lakens (2021)")
        with self.voiceover(
            "The filter can be prevented. <bookmark mark='a'/> A registered report is reviewed and accepted before "
            "the data exist. The question and the method are judged, and the paper is published whatever it finds. "
            "<bookmark mark='b'/> In 2021 Anne Scheel, Mitchell Schijen and Daniel Lakens compared them with standard "
            "articles. Ninety-six percent of standard articles supported their first hypothesis. Forty-four percent "
            "of registered reports did. <bookmark mark='c'/> That's Part 43's row. The gap is what filtering predicts, "
            "though registered reports may also ask riskier questions. <bookmark mark='d'/> For a literature, the "
            "cure is the denominator: every study that was run, visible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def others(self):
        head = heading(r"Three more designs")
        items = [
            (r"trial registries", r"every clinical trial registered before it starts, \ with its outcome named: \ the "
                                  r"pile Turner could count", SYMP),
            (r"multi-site protocols", r"one protocol, \ many labs, \ all results reported (Part 43): \ no lab can file "
                                      r"its null away", MODEL),
            (r"sequential designs", r"looks at the data planned in advance, \ with boundaries that keep the error rate "
                                    r"(Part 4's peeking, \ made honest), \ or Bayesian stopping rules", PERSON),
        ]
        rows = VGroup()
        for name, what, col in items:
            rows.add(VGroup(word_chip(name, col, 21, width=4.2), wrapped_label(what, 7.8, 21, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to([0, 0.2, 0])
        foot = wrapped_label(r"each works by making the decision to report independent of the result", 12.0, 22,
                             YOU).to_edge(DOWN, buff=0.7)
        with self.voiceover(
            "Three more designs do the same. <bookmark mark='a'/> Trial registries: every clinical trial registered "
            "before it starts, with its outcome named. That's the pile Turner could count. <bookmark mark='b'/> "
            "Multi-site protocols: one protocol, many labs, and every result reported, as in Part 43. No lab can file "
            "its null away. <bookmark mark='c'/> And sequential designs: looks at the data planned in advance, with "
            "boundaries that keep the error rate. That's Part 4's peeking, made honest. Each works by making the "
            "decision to report independent of the result."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            self.play(FadeIn(foot))
        self.clear_scene()
