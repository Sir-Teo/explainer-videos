from __future__ import annotations

from videos.psychology.psych4.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.experiment()
        self.nine()
        self.dilemma()
        self.objectives()

    def experiment(self):
        head = heading(r"2011: \ a memory experiment, with one step moved")

        def step(text, color, w=2.7):
            t = wrapped_label(text, w - 0.4, 26, WHITE)
            return VGroup(panel(w, 1.25, color=color), t)

        usual = VGroup(step(r"see a list of words", GREY_B), step(r"practise half of them", SIG), step(r"memory test", GREY_B))
        usual.arrange(RIGHT, buff=0.9).move_to([0.6, 1.35, 0])
        bem = VGroup(step(r"see a list of words", GREY_B), step(r"memory test", GREY_B), step(r"practise half of them", SIG))
        bem.arrange(RIGHT, buff=0.9).move_to([0.6, -0.75, 0])
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=4)
                          for row in (usual, bem) for a, b in zip(row, row[1:])])
        l1 = label(r"the usual order", font_size=26, color=GREY_A).next_to(usual, LEFT, buff=0.35)
        l2 = label(r"Bem's order", font_size=26, color=SIG).next_to(bem, LEFT, buff=0.35)
        VGroup(usual, bem, arrows, l1, l2).move_to([0, 0.3, 0])
        claim = VGroup(
            label(r"reported: \ the words practised \emph{afterwards} were remembered better \emph{in the test}",
                  font_size=30, color=WHITE),
            label(r"the computer chose which words to practise only after the test was over", font_size=26,
                  color=GREY_A),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.75)
        src = published_tag(archive.BEM_2011.cite)
        with self.voiceover(
            "In 2011 one of psychology's leading journals published a memory experiment with one step moved. "
            "<bookmark mark='a'/> You know the ordinary version. People see a list of words. They practise some "
            "of them. Then they're tested, and the practised words are remembered better. Nobody doubts that. "
            "<bookmark mark='b'/> In this version the test comes first. People see the words and are tested on "
            "them. Only then does a computer pick, at random, which words they'll practise. "
            "<bookmark mark='c'/> And the report was that the words people would practise later were remembered "
            "better in the test they'd already taken. The practice worked backwards in time. The author was "
            "Daryl Bem, a respected social psychologist at Cornell, and he called the paper Feeling the Future."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(l1), LaggedStart(*[FadeIn(s_) for s_ in usual], lag_ratio=0.5), FadeIn(arrows[:2]),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(l2), LaggedStart(*[FadeIn(s_) for s_ in bem], lag_ratio=0.5), FadeIn(arrows[2:]),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(claim[0], shift=UP * 0.15))
            self.play(FadeIn(claim[1]))
        self.clear_scene()

    def nine(self):
        d = archive.BEM_2011.data
        head = heading(r"Not one experiment: \ nine")
        cards = VGroup()
        for i in range(d["experiments"]):
            ok = i < d["significant"]
            box = RoundedRectangle(width=1.15, height=1.5, corner_radius=0.1, stroke_color=SIG if ok else GREY_C,
                                   stroke_width=3, fill_color="#131A28", fill_opacity=1)
            num = label(rf"{i + 1}", font_size=36, color=WHITE).move_to(box).shift(UP * 0.25)
            mark = label(r"$p < .05$" if ok else r"n.s.", font_size=20, color=SIG if ok else GREY_B)
            mark.move_to(box).shift(DOWN * 0.42)
            cards.add(VGroup(box, num, mark))
        cards.arrange(RIGHT, buff=0.2).move_to([0, 1.2, 0])
        facts = VGroup(
            big_number(rf"{fmt_int(d['participants_more_than'])}+", r"participants", WHITE, 60, 3.0),
            big_number(rf"{d['significant']} of the {d['experiments']}", r"statistically significant", SIG, 60, 3.4),
            big_number(rf"$d = {r2(d['mean_d'])}$", r"the average size of the effect", TRUTH, 60, 3.6),
        ).arrange(RIGHT, buff=0.9, aligned_edge=UP).move_to([0, -1.5, 0])
        src = published_tag(archive.BEM_2011.cite)
        with self.voiceover(
            f"And it wasn't one experiment. It was {d['experiments']}, <bookmark mark='a'/> with more than a "
            "thousand participants between them. Each took a well-established effect and ran it backwards, so "
            f"that the cause came after the response. <bookmark mark='b'/> {d['significant']} of the "
            f"{d['experiments']} gave a statistically significant result. <bookmark mark='c'/> The effects were "
            f"small, about {d['mean_d']} of a standard deviation on average, but they were there, experiment after "
            "experiment. And here is what made the paper impossible to wave away. The designs were ordinary. The "
            "statistics were the ones in every textbook. The paper had passed peer review at one of the field's "
            "leading journals. By the standards the field applied to everything else, this was a "
            "well-supported finding."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c[0]) for c in cards], *[FadeIn(c[1]) for c in cards], lag_ratio=0.08),
                      FadeIn(facts[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c[2]) for c in cards], lag_ratio=0.15), FadeIn(facts[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(facts[2], shift=UP * 0.15))
        self.clear_scene()

    def dilemma(self):
        head = heading(r"Two possibilities, and no third")
        left = VGroup(panel(5.6, 2.5, color=GREY_B),
                      VGroup(label(r"People can feel the future.", font_size=34, color=WHITE),
                             wrapped_label(r"Then physics has a great deal to revise.", 4.8, 26, GREY_A)).arrange(
                          DOWN, buff=0.25))
        right = VGroup(panel(5.6, 2.5, color=BAD),
                       VGroup(wrapped_label(r"The field's ordinary methods can produce evidence for something "
                                            r"that is not there.", 4.9, 32, WHITE),
                              wrapped_label(r"Then how much else did they produce?", 4.8, 26, BAD)).arrange(
                           DOWN, buff=0.25))
        for g in (left, right):
            g[1].move_to(g[0])
        doors = VGroup(left, right).arrange(RIGHT, buff=0.6).move_to([0, 1.0, 0])
        observer = VGroup(
            label(r"Kant's third objection: \ the observer disturbs", font_size=28, color=KANT),
            label(r"Part 2: the experimenter. \ \ Part 3: the person reporting on themselves.", font_size=26,
                  color=GREY_A),
            label(r"Today: the scientist, looking at the data and hoping.", font_size=30, color=WHITE),
        ).arrange(DOWN, buff=0.16).move_to([0, -1.6, 0])
        q = label(r"When should a finding be believed?", font_size=42, color=P.ACCENT).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "So there were two possibilities. <bookmark mark='a'/> Either people really can feel the future, in "
            "which case physics has some explaining to do. <bookmark mark='b'/> Or the methods that every "
            "psychologist had been trained to use can produce good-looking evidence for a thing that isn't there. "
            "And if they can do it for precognition, they can do it for anything. Most psychologists took the "
            "second door, and it was the more frightening one. "
            "<bookmark mark='c'/> This is Kant's third objection in its last form. The observer disturbs what is "
            "observed. In Part 2 the observer was the experimenter, leaking the answer. In Part 3 it was the "
            "person reporting on themselves. Today it's the scientist, who looks at the data hoping to see "
            "something, and has a hundred small decisions to make along the way. <bookmark mark='d'/> So the "
            "question for this part is the plainest one in science. When should a finding be believed?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(right, shift=UP * 0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(o, shift=UP * 0.1) for o in observer], lag_ratio=0.7), run_time=9.0)
            vo.wait_until("d")
            self.play(FadeIn(q, shift=UP * 0.2))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 4", font_size=34, color=GREY_B), label(r"The Evidence", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"how big an effect is, \ what a p-value says, \ and what it does not",
            r"power: \ why small studies miss real effects and overstate the ones they find",
            r"forking paths, on you: \ make nothing significant, honestly",
            r"the file drawer, \ and what a filtered literature looks like",
            r"one hundred studies run again, \ and what it showed",
            r"the repairs, \ and how to tell which findings to trust",
        ], color=P.ACCENT, font_size=32, width=13.2)
        with self.voiceover(
            "Part four: the evidence. <bookmark mark='a'/> We start with the vocabulary: how big an effect is, "
            "what a p-value actually says, and the things it's often taken to say and doesn't. "
            "<bookmark mark='b'/> Then power, which explains why small studies miss real effects, and exaggerate "
            "the ones they find. <bookmark mark='c'/> Then you'll take a dataset with nothing in it and, "
            "without cheating, make it significant. <bookmark mark='d'/> We'll put a thousand laboratories to "
            "work on one question, and see what the published record looks like when only the successes are "
            "printed. <bookmark mark='e'/> Then the moment the field tested itself, by running a hundred of its "
            "own studies again. <bookmark mark='f'/> And last, what was done about it, and how you can tell which "
            "findings deserve your trust. That's also what the Ledger is for."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mark_, r in zip("bcdef", obj.rows[1:]):
                vo.wait_until(mark_)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
