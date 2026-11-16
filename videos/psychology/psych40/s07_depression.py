from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Depression(VoiceoverScene):
    def construct(self):
        self.card()
        self.cognition()

    def card(self):
        card = chapter_card(6, r"Depression and thought", r"Is depression a way of thinking?",
                            lit={1967: r"Beck", 1978: r"Abramson et al.", 1991: r"Nolen-Hoeksema"}, part=PART,
                            scale=("person",), marr=("what",))
        with self.voiceover("Chapter six. Depression and thought."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def cognition(self):
        head = heading(r"Three cognitive accounts")
        tri = VGroup(*[word_chip(t, color=c, font_size=18, width=2.6) for t, c in (
            (r"the self", PERSON), (r"the world", SYMP), (r"the future", MODEL))])
        tri[0].move_to([-3.8, 1.6, 0])
        tri[1].move_to([-5.2, -0.3, 0])
        tri[2].move_to([-2.4, -0.3, 0])
        edges = VGroup(*[Line(tri[i].get_center(), tri[j].get_center(), color=GREY_D, buff=0.35)
                         for i, j in ((0, 1), (1, 2), (2, 0))])
        lt = label(r"Beck's negative triad", font_size=15, color=GREY_A).move_to([-3.8, -1.3, 0])
        rows = rows_of([
            (r"depression's symptoms span mood, \ interest, \ sleep, \ appetite, \ energy, \ concentration, \ guilt "
             r"and thoughts of death; \ Part 39 showed how varied the combinations are", WHITE),
            (r"Beck, \ 1967: \ a negative view of the self, \ the world and the future, \ kept going by biased "
             r"interpretation", PERSON),
            (r"attributional style: \ explaining bad events as caused by oneself, \ lasting and pervasive; \ the "
             r"1978 reformulation of helplessness", SYMP),
            (r"rumination: \ dwelling on one's distress and its causes, \ which prolongs low mood", MODEL),
            (r"cognitive therapy targets these, \ with evidence of benefit; \ whether the thoughts cause depression "
             r"or come with it is harder to show", YOU),
        ], 6.4, 19, 0.34).move_to([3.2, -0.2, 0])
        tag = historical_tag(r"Beck (1967); \ Abramson, \ Seligman \& Teasdale (1978)")
        with self.voiceover(
            "Now sadness. <bookmark mark='a'/> Depression's symptoms span mood, interest, sleep, appetite, energy, "
            "concentration, guilt and thoughts of death, and Part 39 showed how varied the combinations are. "
            "<bookmark mark='b'/> In 1967 Aaron Beck described a negative triad: a negative view of the self, the "
            "world and the future, kept going by biased interpretation. <bookmark mark='c'/> In 1978 the helplessness "
            "theory was reformulated around attributional style: explaining bad events as caused by oneself, as "
            "lasting, and as pervasive. <bookmark mark='d'/> And rumination: dwelling on one's distress and its "
            "causes, which prolongs low mood. <bookmark mark='e'/> Cognitive therapy targets these, with evidence of "
            "benefit. Whether such thoughts cause depression, or simply come with it, is harder to show."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(tri), Create(edges), FadeIn(lt))
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
