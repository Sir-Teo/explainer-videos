from __future__ import annotations

from videos.psychology.psych27.common import *  # noqa: F403


class Problems(VoiceoverScene):
    def construct(self):
        self.card()
        self.easy_hard()
        self.bet()

    def card(self):
        card = chapter_card(4, r"The easy problems and the hard one", r"What would a theory of consciousness "
                            r"have to explain?", lit={1974: r"Nagel", 1995: r"Chalmers; \ Block"},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter four. The easy problems and the hard one."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def easy_hard(self):
        head = heading(r"Two kinds of question")
        easy = VGroup(label(r"the easy problems", font_size=28, color=SEEN),
                      wrapped_label(r"how the brain discriminates, \ integrates information, \ reports, \ attends, \ "
                                    r"controls behaviour: \ explained by mechanisms, \ like everything in this series",
                                    5.2, 22, WHITE)).arrange(DOWN, buff=0.25)
        hard = VGroup(label(r"the hard problem", font_size=28, color=LOST),
                      wrapped_label(r"why any of that is accompanied by experience: \ why there is something it is "
                                    r"like to see red", 5.2, 22, WHITE)).arrange(DOWN, buff=0.25)
        VGroup(easy, hard).arrange(RIGHT, buff=1.2, aligned_edge=UP).move_to([0, 1.2, 0])
        rows = rows_of([
            (r"Nagel, \ 1974: \ \emph{What is it like to be a bat?} \ Chalmers, \ 1995, \ named the hard problem",
             WHITE),
            (r"Block, \ 1995: \ access consciousness, \ information available for report and reasoning, \ against "
             r"phenomenal consciousness, \ the experience itself", HOT),
            (r"science works on the correlates and on access; \ whether that will reach the hard problem is "
             r"\emph{Philosophy, Built}, \ Part 31", MODEL),
        ], 12.0, 24, 0.34).move_to([0, -1.6, 0])
        tag = historical_tag(r"Nagel (1974); \ Chalmers (1995); \ Block (1995)")
        with self.voiceover(
            "Before the theories, two minutes on what they're trying to explain. <bookmark mark='a'/> David "
            "Chalmers, in 1995, separated the easy problems of consciousness, how the brain discriminates, "
            "integrates information, reports and controls behaviour, which are hard enough but are explained by "
            "mechanisms, like everything else in this series, <bookmark mark='b'/> from the hard problem: why any "
            "of that is accompanied by experience at all. Why there is something it is like to see red, as Thomas "
            "Nagel put it in asking what it is like to be a bat. <bookmark mark='c'/> In the same year Ned Block "
            "distinguished access consciousness, information available for report and reasoning, from phenomenal "
            "consciousness, the experience itself. Experiments can only ever measure the first directly. "
            "<bookmark mark='d'/> Science works on the correlates and on access. Whether that will ever reach the "
            "hard problem is a question for philosophy, and it's Part 31 of Philosophy, Built."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(easy))
            vo.wait_until("b")
            self.play(FadeIn(hard), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def bet(self):
        head = heading(r"A bet made in 1998")
        left = VGroup(label(r"Christof Koch", font_size=28, color=GNW),
                      wrapped_label(r"within 25 years, \ the neural correlates of consciousness will be clearly "
                                    r"described", 4.8, 22, WHITE)).arrange(DOWN, buff=0.25)
        right = VGroup(label(r"David Chalmers", font_size=28, color=IIT),
                       wrapped_label(r"they will not", 4.8, 22, WHITE)).arrange(DOWN, buff=0.25)
        VGroup(left, right).arrange(RIGHT, buff=1.5, aligned_edge=UP).move_to([0, 1.0, 0])
        stake = label(r"the stake: \ a case of fine wine", font_size=24, color=GREY_A).move_to([0, -0.4, 0])
        result = wrapped_label(r"June 2023: \ Koch conceded, \ and paid; \ the adversarial test of chapter nine had "
                               r"just reported, \ with no winner", 11.0, 25, LOST).move_to([0, -1.6, 0])
        tag = historical_tag(r"the Koch--Chalmers wager (1998, \ settled 2023)")
        with self.voiceover(
            "The state of the field can be summed up by a bet. <bookmark mark='a'/> In 1998 the neuroscientist "
            "Christof Koch bet the philosopher David Chalmers that within twenty-five years the neural correlates "
            "of consciousness would be clearly described. Chalmers bet they wouldn't. <bookmark mark='b'/> The stake "
            "was a case of fine wine. <bookmark mark='c'/> In June 2023, at the annual meeting of the field, Koch "
            "conceded and paid up. The adversarial test of chapter nine had just reported its first results, and "
            "neither leading theory had won."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(right))
            vo.wait_until("b")
            self.play(FadeIn(stake))
            vo.wait_until("c")
            self.play(FadeIn(result))
        self.clear_scene()
