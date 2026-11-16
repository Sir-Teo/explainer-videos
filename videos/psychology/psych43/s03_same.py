from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403


class Same(VoiceoverScene):
    def construct(self):
        self.card()
        self.kinds()
        self.protocols()

    def card(self):
        card = chapter_card(2, r"What counts as the same study", r"Direct or conceptual?",
                            lit={2014: r"Brandt et al.", 2018: r"Zwaan et al."}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter two. What counts as the same study."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def kinds(self):
        head = heading(r"Two kinds of replication")
        left = VGroup(word_chip(r"direct", color=GOOD, font_size=22, width=3.4),
                      wrapped_label(r"the same procedure, \ materials and analysis, \ in a new sample: \ it tests "
                                    r"whether the finding was real", 5.0, 20, WHITE))
        right = VGroup(word_chip(r"conceptual", color=SYMP, font_size=22, width=3.4),
                       wrapped_label(r"a different procedure for the same idea: \ it tests whether the idea is general, "
                                     r"\ but a failure is easy to explain away", 5.0, 20, WHITE))
        for g in (left, right):
            g.arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"Brandt and colleagues, \ 2014: \ a recipe for a convincing replication: \ define the effect, \ follow "
             r"the original closely, \ get high power, \ report everything, \ and compare with the original", PERSON),
            (r"Zwaan and colleagues, \ 2018: \ ``making replication mainstream'', \ answering the objections that "
             r"replications are pointless or hostile", MODEL),
        ], 12.4, 21, 0.36).move_to([0, -1.9, 0])
        tag = published_tag(r"Brandt et al.\ (2014); \ Zwaan et al.\ (2018)")
        with self.voiceover(
            "What counts as the same study? <bookmark mark='a'/> A direct replication repeats the procedure, the "
            "materials and the analysis in a new sample. It tests whether the finding was real. "
            "<bookmark mark='b'/> A conceptual replication tests the same idea another way. It asks whether the idea "
            "is general, but a failure is easy to explain away. <bookmark mark='c'/> In 2014 Mark Brandt and "
            "colleagues wrote a recipe for a convincing replication: define the effect, follow the original closely, "
            "get high power, report everything, and compare with the original. <bookmark mark='d'/> In 2018 Rolf "
            "Zwaan and colleagues argued for making replication mainstream, and answered the objections that "
            "replications are pointless, or hostile."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            for m, r in zip("cd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def protocols(self):
        head = heading(r"The two protocols")
        rows = rows_of([
            (r"verbal overshadowing: \ a film of a robbery, \ then 20 minutes of a filler task, \ then five minutes "
             r"describing the robber's face or listing countries and capitals, \ then a line-up", GOOD),
            (r"the original authors helped write it; \ a first version, \ with the description straight after the "
             r"film, \ had the order of the original's study changed by mistake, \ and became a second report", GREY_A),
            (r"ego depletion: \ cross out every e in a text, \ with or without demanding extra rules, \ then a "
             r"conflict task whose response-time variability is the measure of self-control", AUTH),
            (r"its protocol followed a single study, \ chosen because it could be run identically by computer in every "
             r"lab", YOU),
        ], 12.4, 21, 0.42).move_to([0, -0.3, 0])
        tag = published_tag(r"Alogna et al.\ (2014); \ Hagger et al.\ (2016)")
        with self.voiceover(
            "Both replications followed fixed protocols, written with the original authors. <bookmark mark='a'/> "
            "Verbal overshadowing: a film of a robbery, then twenty minutes of a filler task, then five minutes "
            "describing the robber's face, or listing countries and their capitals, and then a line-up. "
            "<bookmark mark='b'/> A first version, with the description straight after the film, had changed "
            "the order of the original study by mistake, and became a second report. <bookmark mark='c'/> Ego "
            "depletion: cross out every letter e in a text, with or without demanding extra rules, and then a "
            "conflict task, where the variability of response times measures self-control. <bookmark mark='d'/> Its "
            "protocol followed a single earlier study, chosen because a computer could run it identically in every "
            "lab."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
