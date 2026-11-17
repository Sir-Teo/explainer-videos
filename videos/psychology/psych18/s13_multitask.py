from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Multitask(VoiceoverScene):
    def construct(self):
        self.card()
        self.driving()
        self.media()

    def card(self):
        card = chapter_card(12, r"Doing two things at once", r"Can you drive and talk?",
                            lit={2001: r"Strayer \& Johnston", 2009: r"Ophir et al."}, part=PART,
                            scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter twelve. Doing two things at once."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def driving(self):
        p = archive.STRAYER_2001.data
        head = heading(r"Driving and talking")
        groups = VGroup()
        for k, (name, col, mult) in enumerate([(r"radio", GREY_B, 1.0), (r"handheld phone", BAD, 2.2),
                                               (r"hands-free phone", BAD, 2.2)]):
            g = VGroup(label(name, font_size=22, color=col),
                       label(r"misses: \ more than doubled" if mult > 1 else r"misses: \ no reliable change",
                             font_size=19, color=col))
            g.arrange(DOWN, buff=0.12)
            groups.add(g)
        groups.arrange(RIGHT, buff=1.0).move_to([0, 1.7, 0])
        boxes = VGroup(*[SurroundingRectangle(g, color=g[0].get_color(), buff=0.18, stroke_width=2) for g in groups])
        rows = rows_of([
            (rf"2001: \ Strayer and Johnston; \ {p['participants']} people track a moving target, \ "
             r"and brake for red lights", WHITE),
            (r"during a phone conversation, \ the share of red lights missed more than doubled", BAD),
            (r"and the lights they did see, \ they reacted to more slowly", BAD),
            (r"hands-free was no better: \ the cost is in the conversation, \ not the hands", ATT),
            (r"listening to the radio, \ or a book on tape, \ did not reliably hurt", GREY_A),
        ], 12.4, 26, 0.3).to_edge(DOWN, buff=0.75)
        tag = published_tag(archive.STRAYER_2001.cite)
        with self.voiceover(
            "The bottleneck has a cost on the road. <bookmark mark='a'/> In 2001 David Strayer and William Johnston "
            f"had {p['participants']} people steer a cursor to follow a moving target, a stand-in for driving, and "
            "brake whenever a red light flashed. <bookmark mark='b'/> During a phone conversation, the share of red "
            "lights they missed more than doubled. <bookmark mark='c'/> And the lights they did catch, they "
            "reacted to more slowly. <bookmark mark='d'/> People using a hands-free phone did no better than people "
            "holding one. The cost lies in the conversation, which competes for the central bottleneck of Chapter "
            "seven, not in the hand on the phone. <bookmark mark='e'/> Listening to the radio didn't reliably hurt. "
            "Later simulator studies by the same group found phone drivers' braking comparable in some measures to "
            "drunk drivers'. Laws that ban handheld phones but allow hands-free ones address the wrong problem."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(groups[0]), FadeIn(boxes[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(groups[1]), FadeIn(boxes[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(groups[2]), FadeIn(boxes[2]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def media(self):
        p = archive.OPHIR_2009.data
        head = heading(r"Does media multitasking damage attention?")
        A = axes([0, 3], [0, 0.6], x_length=5.0, y_length=2.8, xticks=[], yticks=[0, 0.3, 0.6],
                 ylabel=r"effect size, \ $d$", center=[3.4, 0.9, 0], font_size=17)
        ax = A.ax
        bars = VGroup()
        for k, (v, name, col) in enumerate([(None, r"the 2009 study: \ large", BAD),
                                            (p["meta_d"], rf"meta-analysis, \ {p['meta_tests']} tests: \ 0.17", ATT),
                                            (0.0, r"corrected for small-study bias: \ about 0", GOOD)]):
            if v is None:
                arr = Arrow(ax.c2p(k + 0.5, 0), ax.c2p(k + 0.5, 0.6), buff=0, color=col, stroke_width=8,
                            max_tip_length_to_length_ratio=0.12)
                bars.add(VGroup(arr, wrapped_label(name, 1.5, 15, col).next_to(ax.c2p(k + 0.5, 0), DOWN, buff=0.1)))
                continue
            lo, hi = ax.c2p(k + 0.5, 0), ax.c2p(k + 0.5, max(v, 0.004))
            bars.add(VGroup(Rectangle(width=0.8, height=max(hi[1] - lo[1], 0.03), stroke_width=0, fill_color=col,
                                      fill_opacity=0.85).move_to([lo[0], (lo[1] + hi[1]) / 2, 0]),
                            wrapped_label(name, 1.5, 15, col).next_to(lo, DOWN, buff=0.1)))
        rows = rows_of([
            (r"2009: \ Ophir, \ Nass and Wagner: \ heavy media multitaskers were worse at ignoring distractors", WHITE),
            (r"a small study, \ a striking claim, \ wide coverage", GREY_A),
            (rf"2017: \ two replications, \ {p['replication_tests']} tests, \ {p['replication_significant']} in the "
             r"predicted direction", ATT),
            (rf"meta-analysis of {p['meta_studies']} studies: \ $d$ = {p['meta_d']}; \ near zero after bias correction",
             ATT),
            (r"the Ledger: \ contested; \ and correlation could not show cause anyway", CONFLICT),
        ], 6.4, 24, 0.38).to_edge(LEFT, buff=0.55).shift(DOWN * 0.1)
        tag = published_tag(archive.OPHIR_2009.cite)
        with self.voiceover(
            "A popular claim goes further: that constant multitasking with media damages attention itself. "
            "<bookmark mark='a'/> In 2009 Eyal Ophir, Clifford Nass and Anthony Wagner compared students who reported "
            "heavy media multitasking with light ones, and found the heavy multitaskers worse at filtering out "
            "distractors, by a large margin. <bookmark mark='b'/> It was a small study with a striking claim, and it "
            "was widely reported. <bookmark mark='c'/> In 2017 Reza Wiradhany and Mark Nieuwenstein ran two careful "
            "replications: of fourteen tests, five came out in the predicted direction. <bookmark mark='d'/> Their "
            "meta-analysis of twelve studies found a small average effect, which shrank to about nothing after "
            "correcting for the tendency of small studies with big effects to get published. "
            "<bookmark mark='e'/> The Ledger marks the claim contested. And even a solid correlation couldn't say "
            "which way it runs: people who are easily distracted may simply multitask more."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "a":
                    self.play(FadeIn(bars[0]))
                if m == "d":
                    self.play(GrowFromEdge(bars[1][0], DOWN), FadeIn(bars[1][1]), FadeIn(bars[2]))
        self.clear_scene()
