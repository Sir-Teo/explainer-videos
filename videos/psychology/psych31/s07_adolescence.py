from __future__ import annotations

from videos.psychology.psych31.common import *  # noqa: F403


class Adolescence(VoiceoverScene):
    def construct(self):
        self.card()
        self.peers()
        self.dual()
        self.clock_()
        self.excuse()

    def card(self):
        card = chapter_card(6, r"Adolescence", r"Why do teenagers take risks, \ and when?",
                            lit={2004: r"Roenneberg et al.", 2005: r"Gardner \& Steinberg", 2018: r"Steinberg et al."},
                            part=PART, scale=("brain", "person", "group"), marr=("what", "how"))
        with self.voiceover("Chapter six. Adolescence."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def peers(self):
        head = heading(r"Chicken, \ alone and with friends")
        A = axes([-0.5, 2.5], [0, 1.1], x_length=5.6, y_length=3.6, xticks=None, yticks=None,
                 ylabel=r"risky driving", center=[-3.2, -0.3, 0], font_size=16)
        groups = [(r"about 14", 0.0), (r"about 19", 1.0), (r"about 37", 2.0)]
        alone = bars(A.ax, [x - 0.18 for _, x in groups], [0.45, 0.45, 0.42], GREY_B, width=0.32)
        peers = bars(A.ax, [x + 0.18 for _, x in groups], [0.9, 0.7, 0.46], CHILD, width=0.32)
        names = VGroup(*[label(t, font_size=18).next_to(A.ax.c2p(x, 0), DOWN, buff=0.2) for t, x in groups])
        key = legend([(GREY_B, r"alone"), (CHILD, r"two friends watching")], font_size=17).next_to(A, UP, buff=0.1)
        sch = label(r"schematic: \ the pattern, \ not the published values", font_size=16, color=GREY_B)
        sch.next_to(names, DOWN, buff=0.3)
        rows = rows_of([
            (r"Gardner and Laurence Steinberg, \ 2005: \ a driving game in which a light turns yellow and a "
             r"wall may appear; \ the longer you drive on, \ the more you score, \ unless you crash", WHITE),
            (r"early adolescents, \ late adolescents and adults, \ alone or with two friends in the room", AGE),
            (r"alone, \ the three ages took similar risks; \ with friends watching, \ the adolescents took more, \ "
             r"the adults did not", CHILD),
            (r"the risk is in the situation as much as in the teenager", YOU),
        ], 5.6, 21, 0.34).move_to([3.6, -0.2, 0])
        tag = published_tag(r"Gardner \& Steinberg (2005)")
        with self.voiceover(
            "Teenagers crash cars, try drugs and take dares more than children or adults. Why? "
            "<bookmark mark='a'/> In 2005, the psychologists Gardner and Laurence Steinberg used a driving game called Chicken. "
            "A light turns yellow, a wall may appear, and the longer you keep driving, the more points you get, "
            "unless you crash. <bookmark mark='b'/> They tested early adolescents, late adolescents and adults, "
            "either alone or with two friends in the room. <bookmark mark='c'/> Alone, the three ages took similar "
            "risks. With friends watching, the adolescents took more, and the adults didn't. The bars show that "
            "pattern, not the published values. <bookmark mark='d'/> The risk is in the situation as much as in the "
            "teenager."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(names), FadeIn(tag), FadeIn(sch))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(alone), FadeIn(key))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(peers))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def dual(self):
        d = load("adolescence")
        head = heading(r"Two systems, \ two timetables")
        A = axes([10, 30], [0, 1.1], x_length=6.2, y_length=4.4, xticks=[10, 15, 20, 25, 30], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"age", center=[-3.0, -0.4, 0], font_size=16)
        seek = curve(A.ax, d["age"], d["seeking"], CHILD, stroke_width=5)
        reg = curve(A.ax, d["age"], d["regulation"], AGE, stroke_width=5)
        gap = VGroup(*[Line(A.ax.c2p(a, r), A.ax.c2p(a, s), color=LOST, stroke_width=3, stroke_opacity=0.5)
                       for a, s, r in zip(d["age"][::8], d["seeking"][::8], d["regulation"][::8]) if s > r])
        key = legend([(CHILD, r"sensation seeking"), (AGE, r"self-regulation")], font_size=18)
        key.move_to(A.ax.c2p(13.2, 1.0))
        sh = label(r"illustrative curves, \ drawn to the reported peaks", font_size=16, color=GREY_B)
        sh.next_to(A, DOWN, buff=0.1)
        rows = rows_of([
            (r"the dual-systems model: \ reward seeking rises with puberty; \ the control that restrains it "
             r"matures slowly, \ into the twenties", WHITE),
            (r"Steinberg and colleagues, \ 2018: \ more than 5{,}000 people aged 10 to 30 in 11 countries", AGE),
            (r"sensation seeking peaked at 19; \ self-regulation rose until a plateau between 23 and 26", CHILD),
            (r"the gap between them is widest in the mid-to-late teens; \ the patterns were largely similar across countries", LOST),
        ], 5.6, 21, 0.36).move_to([3.6, -0.2, 0])
        tag = published_tag(r"Steinberg et al.\ (2018)")
        with self.voiceover(
            "One account is the dual-systems model. <bookmark mark='a'/> Reward seeking rises with puberty, while "
            "the control that restrains it matures slowly, into the twenties. <bookmark mark='b'/> In 2018 "
            "Steinberg and colleagues tested it in more than five thousand people aged ten to thirty, in eleven "
            "countries across Africa, Asia, Europe and the Americas. <bookmark mark='c'/> Sensation seeking peaked at "
            "nineteen. Self-regulation rose steadily until a plateau between twenty-three and twenty-six. The curves "
            "here are drawn to those peaks. <bookmark mark='d'/> The gap between the two is widest in the mid-to-late "
            "teens, and the age patterns were largely similar across countries, though their sizes varied."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag), FadeIn(sh))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(key))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(seek), Create(reg), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(gap), FadeIn(rows[3]))
        self.clear_scene()

    def clock_(self):
        d = load("adolescence")
        head = heading(r"The adolescent clock runs late")
        rows = rows_of([
            (r"Part 10's chronotypes: \ the hour of mid-sleep on free days moves later through adolescence", PERIOD),
            (rf"Till Roenneberg and colleagues, \ 2004, \ about 25{{,}}000 people aged 8 to 90: \ latest at about "
             rf"{d['late_women']:.1f} in women and {d['late_men']:.0f} in men, \ earlier every year after", WHITE),
            (r"they proposed it as a biological marker of the end of adolescence", AGE),
            (r"Fischer and colleagues, \ 2017, \ twelve years of the American Time Use Survey: \ the "
             r"latest chronotypes again near 19", COHORT),
            (r"the American Academy of Pediatrics, \ 2014: \ middle and high schools should start at 8:30 or "
             r"later", GOOD),
        ], 12.4, 24, 0.4).move_to([0, -0.3, 0])
        tag = published_tag(r"Roenneberg et al.\ (2004); \ Fischer et al.\ (2017)")
        with self.voiceover(
            "Adolescence also shifts the body clock. <bookmark mark='a'/> Part 10 measured chronotype as the hour of "
            "mid-sleep on free days. It moves later through adolescence. <bookmark mark='b'/> Till Roenneberg and "
            "colleagues surveyed about twenty-five thousand people aged eight to ninety and found sleep was latest "
            "at about nineteen and a half in women and about twenty-one in men, and earlier every year after. "
            "<bookmark mark='c'/> They proposed it as a biological marker for the end of adolescence. "
            "<bookmark mark='d'/> In 2017 Fischer and colleagues, using twelve years of the American Time "
            "Use Survey, again found the latest chronotypes near nineteen. <bookmark mark='e'/> In 2014 the American "
            "Academy of Pediatrics recommended that middle and high schools start at eight-thirty or later: a "
            "policy built on a lifespan curve."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def excuse(self):
        head = heading(r"What ``the teenage brain'' explains, \ and excuses")
        rows = rows_of([
            (r"it explains averages: \ more risk with peers, \ later sleep, \ control still maturing into the "
             r"twenties", AGE),
            (r"it does not explain a person: \ the spread within any age is far wider than the gap between ages",
             COHORT),
            (r"teenagers are not simply irrational: \ alone, \ and with time to think, \ their choices look like "
             r"adults'", GOOD),
            (r"a 2014 master's thesis in New Zealand repeated the driving game, \ and did not find adolescents more affected "
             r"by peers than adults", LOST),
            (r"courts have used this research to treat juveniles differently: \ chapter fourteen", YOU),
        ], 12.4, 25, 0.4).move_to([0, -0.3, 0])
        with self.voiceover(
            "So what does the teenage brain explain? <bookmark mark='a'/> It explains averages: more risk with "
            "peers, later sleep, and control still maturing into the twenties. <bookmark mark='b'/> It doesn't "
            "explain a person. The spread within any age is far wider than the gap between ages. "
            "<bookmark mark='c'/> And teenagers aren't simply irrational. Alone, with time to think, their choices "
            "look like adults'. <bookmark mark='d'/> The peer effect itself needs more replication. A 2014 master's "
            "thesis in New Zealand repeated the driving game and did not find adolescents more affected by watching peers "
            "than adults were. <bookmark mark='e'/> Even so, courts have used this research to treat juveniles "
            "differently, which is chapter fourteen."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
