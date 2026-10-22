from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai31.common import CI, EST, HACK, JUDGE, PART, TRUTH, board_rows, node_box


def quote_card(text: str, who: str, color, width=11.6, font_size=30) -> VGroup:
    """A verbatim quotation (Tex), its source under it, in a dark box with a coloured bar."""
    body = wrapped_label(text, width - 1.0, font_size, WHITE)
    src = label(who, font_size=font_size - 8, color=GREY_B)
    inner = VGroup(body, src).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
    box = RoundedRectangle(width=width, height=inner.height + 0.6, corner_radius=0.14, stroke_color=color,
                           stroke_width=1.8, fill_color="#0B0F17", fill_opacity=0.94)
    bar = Rectangle(width=0.07, height=box.height - 0.28, stroke_width=0, fill_color=color, fill_opacity=1)
    inner.move_to(box).align_to(box, LEFT).shift(RIGHT * 0.45)
    bar.move_to(box.get_left() + RIGHT * 0.15)
    return VGroup(box, bar, inner)


class Hook(VoiceoverScene):
    def construct(self):
        self.series()
        self.wiener()
        self.good()
        self.questions()
        self.plan()

    # ------------------------------------------------------------------
    def series(self):
        smap = series_map(current=PART, done=PART - 1).scale(0.85).move_to(DOWN * 0.15)
        head = label(r"AI, Built: \ thirty-one parts", font_size=40).to_edge(UP, buff=0.35)
        rows, named = board_rows()
        board = scoreboard(rows, max_bits=8.0, row_h=0.36, font_size=20)
        board.scale_to_fit_height(min(board.height, 6.2)).move_to(DOWN * 0.3)
        bhead = label(r"the scoreboard: \ bits per character on one passage", font_size=32).to_edge(UP, buff=0.3)
        q = label(r"Can we trust what we built?", font_size=54, color=JUDGE)
        qbox = BackgroundRectangle(q, color=BACKGROUND, fill_opacity=0.85, buff=0.35)
        with self.voiceover(
            "Thirty parts ago, this series began with a guessing game. Claude Shannon asked people to guess the next "
            "letter of an English sentence, and from their guesses measured how much information English carries. "
            "<bookmark mark='a'/> Since then we have built, piece by piece, the machines that play that game: "
            "counting models, networks, transformers, models that paint and speak, agents that act. Every one of "
            "them, in the end, guesses what comes next. <bookmark mark='b'/> This scoreboard, from Part 1, keeps "
            "score: bits per character on one passage of a detective novel. <bookmark mark='c'/> This is the last "
            "part, and its question is not how to build one more. It is whether we can trust what we built."
        ) as vo:
            self.play(FadeIn(head), FadeIn(smap, lag_ratio=0.02), run_time=2.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[Indicate(smap.cols[k].head, color=C.BITS) for k in range(6)], lag_ratio=0.3),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(FadeOut(smap), ReplacementTransform(head, bhead), FadeIn(board), run_time=1.5)
            vo.wait_until("c")
            self.play(board.animate.set_opacity(0.35), FadeIn(qbox), FadeIn(q, scale=1.1))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def wiener(self):
        hc = history_card(1960, r"Norbert Wiener, \textit{Some Moral and Technical Consequences of Automation}, "
                          r"\textit{Science} $131$", r"a lecture to the AAAS, December 1959; \ checkers programs that "
                          r"learn ``can defeat the programmer''", width=11.6, color=JUDGE).to_edge(UP, buff=0.4)
        q1 = quote_card(r"``It is my thesis that machines can and do transcend some of the limitations of their "
                        r"designers, and that in doing so they may be both effective and dangerous.''",
                        r"N.~Wiener, \textit{Science} (6 May 1960), p.~1355", JUDGE, font_size=28)
        q2 = quote_card(r"``\dots we had better be quite sure that the purpose put into the machine is the purpose "
                        r"which we really desire and not merely a colorful imitation of it.''",
                        r"N.~Wiener, \textit{Science} (6 May 1960), p.~1358", HACK, font_size=28)
        q1.next_to(hc, DOWN, buff=0.35)
        q2.next_to(q1, DOWN, buff=0.3)
        with self.voiceover(
            "The worry is older than the field's successes. In December 1959 the mathematician "
            "Norbert Wiener, who founded cybernetics, gave a lecture that Science printed the next May, under the "
            "title Some Moral and Technical Consequences of Automation. He pointed to the checkers programs of the "
            "day, Arthur Samuel's from Part 2 among them, which had learned to beat the people who programmed them. "
            "<bookmark mark='b'/> His thesis, in his words: machines can and do transcend some of the limitations of "
            "their designers, and in doing so they may be both effective and dangerous. <bookmark mark='c'/> And his "
            "warning. If we use a machine we cannot interfere with once it has started, we had better be quite sure "
            "that the purpose put into the machine is the purpose which we really desire, and not merely a colorful "
            "imitation of it."
        ) as vo:
            self.play(FadeIn(hc, shift=DOWN * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(q1, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(q2, shift=UP * 0.15))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def good(self):
        hc = history_card(1965, r"I.~J.~Good, \textit{Speculations Concerning the First Ultraintelligent Machine}, "
                          r"\textit{Advances in Computers} $6$", r"a statistician who had worked with Alan Turing at "
                          r"Bletchley Park", width=11.6, color=EST).to_edge(UP, buff=0.4)
        q1 = quote_card(r"``Let an ultraintelligent machine be defined as a machine that can far surpass all the "
                        r"intellectual activities of any man however clever. Since the design of machines is one of "
                        r"these intellectual activities, an ultraintelligent machine could design even better "
                        r"machines; there would then unquestionably be an `intelligence explosion' \dots''",
                        r"I.~J.~Good (1965), \S 2", EST, font_size=26)
        q2 = quote_card(r"``Thus the first ultraintelligent machine is the last invention that man need ever make, "
                        r"provided that the machine is docile enough to tell us how to keep it under control.''",
                        r"I.~J.~Good (1965), \S 2", JUDGE, font_size=26)
        q3 = quote_card(r"``\dots is likely to be achieved with the help of a very large artificial neural net.''",
                        r"I.~J.~Good (1965), \S 9, on how it would be built", CI, font_size=26)
        q1.next_to(hc, DOWN, buff=0.3)
        q2.next_to(q1, DOWN, buff=0.25)
        q3.move_to(q2)
        with self.voiceover(
            "Five years later the statistician I. J. Good, who had worked with Alan Turing breaking codes at "
            "Bletchley Park, took the thought further. <bookmark mark='a'/> Let an ultraintelligent machine be "
            "defined as a machine that can far surpass all the intellectual activities of any man, however clever. "
            "Designing machines is one of those activities, so it could design better machines, and there would be "
            "an intelligence explosion. <bookmark mark='b'/> Thus, he wrote, the first ultraintelligent machine is "
            "the last invention that man need ever make, provided that the machine is docile enough to tell us how "
            "to keep it under control. <bookmark mark='c'/> He even guessed how it would be built: most likely with "
            "the help of a very large artificial neural network."
        ) as vo:
            self.play(FadeIn(hc, shift=DOWN * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q1, shift=UP * 0.15))
            vo.wait_until("b")
            self.play(FadeIn(q2, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeOut(q2), FadeIn(q3, shift=UP * 0.15))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def questions(self):
        cols = [
            (r"Wiener: \ is the purpose \\ the one we meant?", HACK,
             [r"reward hacking \ (6)", r"specification gaming"]),
            (r"Good: \ can we keep it \\ under control?", JUDGE,
             [r"oversight \ (7)", r"deception \ (8)", r"monitoring, control \ (9--10)", r"safeguards \ (11)"]),
            (r"Underneath both: \\ how would we know?", TRUTH,
             [r"measurement \ (1)", r"contamination \ (2)", r"arenas, judges \ (3--4)", r"forecasts \ (5)"]),
        ]
        boxes = VGroup()
        for head, col, items in cols:
            h = label(head, font_size=30, color=col)
            rows = VGroup(*[label(t, font_size=24, color=GREY_A) for t in items]).arrange(DOWN, aligned_edge=LEFT,
                                                                                         buff=0.18)
            inner = VGroup(h, rows).arrange(DOWN, buff=0.4)
            box = RoundedRectangle(width=4.2, height=4.6, corner_radius=0.16, stroke_color=col, stroke_width=2,
                                   fill_color=col, fill_opacity=0.06)
            inner.move_to(box).align_to(box, UP).shift(DOWN * 0.35)
            boxes.add(VGroup(box, inner))
        boxes.arrange(RIGHT, buff=0.35).move_to(DOWN * 0.3)
        title = label(r"The questions, then and now", font_size=40).to_edge(UP, buff=0.4)
        with self.voiceover(
            "Their questions are still the questions. <bookmark mark='a'/> Wiener's: is the purpose we put in the "
            "one we meant, or a colorful imitation of it? Today the imitation is called a proxy, and optimizing it "
            "too well is called reward hacking. <bookmark mark='b'/> Good's: can we keep it under control? Today "
            "that is the work of oversight, monitoring and control, and of the safeguards around the most capable "
            "models. <bookmark mark='c'/> And underneath both, a third question: how would we know? That is "
            "measurement, and it is where this part begins."
        ) as vo:
            self.play(FadeIn(title))
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                self.play(FadeIn(boxes[k], shift=UP * 0.2))
        self.wait(0.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def plan(self):
        title = label(rf"Part {PART}: \ Can We Trust It?", font_size=48).to_edge(UP, buff=0.5)
        smap = series_map(current=PART, done=PART - 1).scale(0.8).move_to(DOWN * 0.6)
        obj = objectives_card([
            r"measuring a model honestly: \ error bars, \ contamination, \ arenas, \ judges",
            r"forecasting what comes next, \ and how such forecasts fail",
            r"reward hacking, \ and supervising a model stronger than its supervisor",
            r"the evidence for deception; \ monitoring chains of thought; \ control",
            r"dangerous capabilities and safeguards; \ what a model remembers, \ and privacy",
            r"the open problems; \ then the scoreboard, \ and Shannon's game, \ one last time",
        ], font_size=26)
        with self.voiceover(
            "This is Part 31 of AI, Built, the finale. <bookmark mark='a'/> In this part: measuring a model honestly, "
            "with error bars, without contamination, in arenas and with judges; forecasting what comes next; reward "
            "hacking, and supervising a model stronger than its supervisor; the evidence that models can deceive, and "
            "how they are monitored and controlled; safeguards against misuse, and what a model remembers of its "
            "training data; and the problems still open. Then, one last time, the scoreboard, and Shannon's game. "
            "Wherever we can, we run the experiment ourselves, on this computer."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
