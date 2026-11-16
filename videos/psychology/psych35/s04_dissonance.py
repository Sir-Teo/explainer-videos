from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403


class Dissonance(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_theories()
        self.multilab()

    def card(self):
        card = chapter_card(3, r"Dissonance or self-perception", r"Do we change our minds to match what we did?",
                            lit={1959: r"Festinger \& Carlsmith", 1967: r"Bem", 2024: r"Vaidis et al."}, part=PART,
                            scale=("person",), marr=("what", "why"))
        with self.voiceover("Chapter three. Dissonance or self-perception."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def two_theories(self):
        head = heading(r"Two explanations of one result")
        left = VGroup(word_chip(r"dissonance", color=AUTH, font_size=24, width=4.6),
                      wrapped_label(r"holding two clashing cognitions is unpleasant, \ like hunger; \ people reduce "
                                    r"it, \ often by changing the belief that is easiest to change", 4.6, 19, WHITE))
        left.arrange(DOWN, buff=0.25).move_to([-3.4, 1.0, 0])
        right = VGroup(word_chip(r"self-perception", color=CROWD, font_size=24, width=4.6),
                       wrapped_label(r"people often do not know their attitudes directly; \ they infer them from "
                                     r"their own behaviour and its circumstances, \ as an outside observer would", 4.6,
                                     19, WHITE))
        right.arrange(DOWN, buff=0.25).move_to([3.4, 1.0, 0])
        rows = rows_of([
            (r"both predict the one-dollar result: \ an unexplained act, \ and an attitude that moves to match it", WHITE),
            (r"dissonance says the change is driven by an unpleasant arousal; \ self-perception says no arousal is "
             r"needed, \ only inference", MODEL),
            (r"Bem, \ 1967: \ observers heard a tape of a man praising the peg task and were told he was paid "
             r"\$1 or \$20; \ they inferred the attitudes the real participants had reported", CROWD),
            (r"Fazio, \ Zanna and Cooper, \ 1977: \ dissonance for acts far from what a person accepts, \ "
             r"self-perception for acts close to it", YOU),
        ], 12.4, 21, 0.3).move_to([0, -2.0, 0])
        tag = historical_tag(r"Bem (1967); \ Fazio, \ Zanna \& Cooper (1977)")
        with self.voiceover(
            "There are two explanations of the one-dollar result. <bookmark mark='a'/> Dissonance theory says that "
            "holding two clashing thoughts is unpleasant, like hunger, and people reduce it, often by changing the "
            "belief that is easiest to change. <bookmark mark='b'/> Self-perception theory says people often don't "
            "know their attitudes directly. They infer them from their own behaviour and its circumstances, as an "
            "outside observer would. <bookmark mark='c'/> Both predict the one-dollar result: an act with no "
            "outside explanation, and an attitude that moves to match it. <bookmark mark='d'/> They differ on "
            "what drives the change. Dissonance says an unpleasant arousal; self-perception says no arousal is "
            "needed, only inference. <bookmark mark='e'/> In 1967 Bem played observers a tape of a man praising "
            "the peg task, and told them he'd been paid one dollar or twenty. The observers inferred the same "
            "attitudes the real participants had reported. <bookmark mark='f'/> In 1977 Fazio, Zanna and Cooper proposed that each "
            "theory is right in its own range: dissonance for acts far from what a person accepts, self-perception "
            "for acts close to it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            for m, r in zip("cdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def multilab(self):
        head = heading(r"Thirty-nine laboratories")
        A = axes([-0.6, 2.6], [0, 1.0], x_length=5.0, y_length=3.6, xticks=None, yticks=None,
                 ylabel=r"attitude toward the essay's position", center=[-3.6, -0.3, 0], font_size=15)
        b = bars(A.ax, [0, 1, 2], [0.45, 0.62, 0.62], [GREY_B, AUTH, CROWD], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.5, 14, c).next_to(A.ax.c2p(k, 0), DOWN, buff=0.15) for k, (t, c) in
                         enumerate(((r"neutral essay", GREY_B), (r"counter-attitudinal, \ high choice", AUTH),
                                    (r"counter-attitudinal, \ low choice", CROWD)))])
        note = label(r"the pattern reported, \ drawn schematically", font_size=15, color=GREY_B).next_to(A, UP,
                                                                                                    buff=0.1)
        rows = rows_of([
            (r"Vaidis and colleagues, \ 2024: \ a preregistered replication of the classic induced-compliance "
             r"design in 39 laboratories, \ 19 countries, \ 4{,}898 people", WHITE),
            (r"participants wrote an essay against their own view under high or low choice, \ or a neutral essay", CROWD),
            (r"writing the counter-attitudinal essay did shift attitudes, \ compared with a neutral one", MODEL),
            (r"but high choice made no difference: \ the very comparison dissonance theory needs", AUTH),
            (r"the authors concluded that this paradigm may not give robust evidence for dissonance", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = published_tag(r"Vaidis et al.\ (2024)")
        with self.voiceover(
            "Sixty-five years later, the classic design was tested at scale. <bookmark mark='a'/> In 2024 "
            "Vaidis and colleagues ran a preregistered replication of induced compliance in thirty-nine "
            "laboratories in nineteen countries, with four thousand eight hundred and ninety-eight people. "
            "<bookmark mark='b'/> Participants wrote an essay against their own view, under high or low choice, "
            "or a neutral essay. <bookmark mark='c'/> Writing the counter-attitudinal essay did shift attitudes, "
            "compared with writing a neutral one. <bookmark mark='d'/> But high choice made no difference, and "
            "that is the very comparison dissonance theory needs. <bookmark mark='e'/> The authors concluded that "
            "this paradigm may not give robust evidence for cognitive dissonance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[0], DOWN), GrowFromEdge(b[1], DOWN), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(GrowFromEdge(b[2], DOWN), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
