from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Effects(VoiceoverScene):
    def construct(self):
        self.card()
        self.wording()
        self.acquiescence()

    def card(self):
        card = chapter_card(9, r"Question effects", r"Can the same question get different answers?",
                            lit={1941: r"Rugg", 1981: r"Schuman \& Presser"}, part=PART, scale=("person", "society"),
                            marr=("what",))
        with self.voiceover("Chapter nine. Question effects."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def wording(self):
        head = heading(r"Wording and order")
        data = (
            (r"forbid or allow", r"``Should the US forbid public speeches against democracy?'' \ against ``allow'': "
                                 r"more people would not allow than would forbid (Rugg, \ 1941)", PERSON),
            (r"order", r"the same two questions in either order give different answers: \ the first sets the frame "
                       r"for the second (Schuman and Presser)", MODEL),
            (r"anchors", r"the categories offered suggest what is normal: \ a scale of TV hours from ``up to half an "
                         r"hour'' moves answers down", SYMP),
            (r"desirability", r"voting, \ exercise and charity are over-reported; \ drinking under-reported; \ more "
                              r"so face to face than online", AUTH),
        )
        rows = VGroup()
        for name, how, c in data:
            rows.add(VGroup(word_chip(name, color=c, font_size=18, width=3.0), wrapped_label(how, 9.2, 20, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Rugg (1941); \ Schuman \& Presser (1981)")
        with self.voiceover(
            "The same question, asked differently, gets different answers. <bookmark mark='a'/> In 1941 Donald Rugg "
            "asked Americans whether the country should forbid public speeches against democracy, or whether it "
            "should allow them. More people would not allow such speeches than would forbid them, though the "
            "questions are logically the same. <bookmark mark='b'/> Order: the same two questions in either order get "
            "different answers, because the first sets the frame for the second. <bookmark mark='c'/> Anchors: the "
            "categories offered suggest what's normal. A scale of television hours that starts at up to half an hour "
            "moves answers down. <bookmark mark='d'/> And social desirability: voting, exercise and charity are "
            "over-reported, drinking under-reported, more so face to face than online."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def acquiescence(self):
        d = load("acq")
        head = heading(r"Agreeing with everything")
        A = axes([0.3, 4.7], [-0.05, 0.3], x_length=5.4, y_length=3.0, xticks=None, yticks=[0, 0.1, 0.2, 0.3],
                 yfmt=lambda v: f"{v:g}", ylabel=r"correlation of unrelated scales", center=[-3.3, 0.3, 0], font_size=13)
        vals = [d["pos_0"], d["pos_4"], d["bal_0"], d["bal_4"]]
        b = bars(A.ax, [1, 2, 3, 4], vals, [GREY_B, AUTH, GREY_B, GOOD], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.3, 11, GREY_A).next_to(A.ax.c2p(i + 1, -0.05), DOWN, buff=0.1) for i, t in
                         enumerate((r"one-way keys, \ no style", r"one-way keys, \ acquiescence",
                                    r"balanced, \ no style", r"balanced, \ acquiescence"))])
        rows = rows_of([
            (r"Psyche: \ two unrelated traits, \ six items each; \ some people agree with whatever is said, \ a stable "
             r"style (Cronbach, \ 1946)", WHITE),
            (rf"with every item keyed the same way, \ the style adds to both scores: \ they correlate "
             rf"{d['pos_4']:.2f}, \ though the traits do not", AUTH),
            (rf"balance the keys, \ half the items reversed, \ and the style cancels in each sum: "
             rf"{d['bal_4']:.2f}", GOOD),
            (r"a correlation between two questionnaires can be a correlation between two ways of answering", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.styled\_answers}, \ 20{,}000 simulated people")
        with self.voiceover(
            "One habit can manufacture a finding. <bookmark mark='a'/> Psyche makes two unrelated traits, with six "
            "items each, and some people who agree with whatever is said. Lee Cronbach described this response set "
            "in 1946. <bookmark mark='b'/> With every item keyed the same way, the style adds to both scores, and they "
            "correlate about zero point two five, though the traits don't. <bookmark mark='c'/> Balance the keys, with "
            "half the items reversed, and the style cancels in each sum. <bookmark mark='d'/> A correlation between "
            "two questionnaires can be a correlation between two ways of answering."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[2]), FadeIn(b[3]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
