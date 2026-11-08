from __future__ import annotations

from videos.philosophy.philosophy1.common import *  # noqa: F403
from explainer.philosophy.reasoner import syllogism as sy


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.unicorns()
        self.series()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"The only way to rectify our reasonings is to make them as tangible as those of the "
                       r"mathematicians, so that we can find our error at a glance, and when there are disputes among "
                       r"persons, we can simply say: let us calculate, without further ado, to see who is right.",
                       r"Leibniz, \textit{The Art of Discovery} (1685)", r"trans.\ Wiener, \textit{Leibniz: "
                       r"Selections} (1951)", width=11.2, font_size=28)
        with self.voiceover(
            "Around 1685, the philosopher and mathematician Gottfried Wilhelm Leibniz wrote down a dream. "
            "<bookmark mark='a'/>The only way to rectify our reasonings, he said, is to make them as tangible as "
            "those of the mathematicians, so that we can find our error at a glance; and when there are disputes "
            "among persons, we can simply say: let us calculate, without further ado, to see who is right. "
            "<bookmark mark='b'/>In Latin, one word: calculemus. This series takes the dream literally."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2), run_time=1.5)
            vo.wait_until("a")
            self.play(t.animate.scale(0.55).to_edge(UP, buff=0.35), FadeIn(q, shift=UP * 0.2))
            vo.wait_until("b")
            cal = label(r"\textit{calculemus}", font_size=60, color=GOAL).to_edge(DOWN, buff=0.6)
            self.play(Write(cal))
        self.clear_scene()

    def unicorns(self):
        mood = (3, "AAI")
        assert sy.valid(mood, existential=True) and not sy.valid(mood)
        prem = VGroup(label(r"All unicorns are one-horned.", font_size=36),
                      label(r"All unicorns are horses.", font_size=36),
                      label(r"So some horses are one-horned.", font_size=36, color=GOAL)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.3)
        bar = Line(LEFT * 3.2, RIGHT * 3.2, color=GREY_B).next_to(prem[1], DOWN, buff=0.17).align_to(prem, LEFT)
        arg = VGroup(prem, bar).move_to([0, 1.3, 0])
        q = label(r"valid?", font_size=40, color=GREY_A).next_to(arg, RIGHT, buff=0.6)
        left = VGroup(label(r"Traditional syllogistic:", font_size=26, color=HIST),
                      label(r"valid \ (\textit{Darapti})", font_size=34, color=OK)).arrange(DOWN, buff=0.15)
        right = VGroup(label(r"Boole, Frege, modern logic:", font_size=26, color=HIST),
                       label(r"invalid", font_size=34, color=BAD)).arrange(DOWN, buff=0.15)
        both = VGroup(left, right).arrange(RIGHT, buff=2.4).move_to([0, -1.2, 0])
        key = label(r"the difference, exactly: \ do `all' sentences assume their subjects exist?", font_size=28,
                    color=GOAL).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Here is a dispute that ran for two thousand years. <bookmark mark='a'/>All unicorns are one-horned. All "
            "unicorns are horses. So some horses are one-horned. <bookmark mark='b'/>Is the argument valid? "
            "<bookmark mark='c'/>In traditional syllogistic, with unicorns assumed to exist, the form is valid: "
            "medieval students learned it under the name Darapti. <bookmark mark='d'/>In modern classical logic, "
            "which allows an empty class of unicorns, it is invalid."
        ) as vo:
            self.play(FadeIn(prem[0], shift=RIGHT * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(prem[1], shift=RIGHT * 0.2), Create(bar))
            self.play(FadeIn(prem[2], shift=RIGHT * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(FadeIn(left, shift=UP * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(right, shift=UP * 0.2))
        with self.voiceover(
            "Who is right? Leibniz's answer would have been: let us calculate. <bookmark mark='a'/>In Chapter nine we "
            "will check this argument against every possible arrangement of unicorns, horses and one-horned things, "
            "and find exactly where the two sides part company. It is not that one side reasons badly. It is that "
            "they mean different things by 'all'. <bookmark mark='b'/>That is the kind of thing calculation can do "
            "for philosophy: not end the argument, but show precisely what it is about."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(key, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(Indicate(key, color=GOAL))
        self.clear_scene()

    def series(self):
        m = series_map(current=1, done=0)
        with self.voiceover(
            "This is a series in forty-two parts about the whole of philosophy, told as one story: how far can "
            "Leibniz's dream go? <bookmark mark='a'/>We start with logic, and build it until it hits the limits of "
            "proof. <bookmark mark='b'/>Then knowledge and belief, science and causation; <bookmark mark='c'/>what "
            "there is, from possible worlds to quantum mechanics; meaning, mind and free will; "
            "<bookmark mark='d'/>and then value: choice, ethics, justice and democracy, and finally the machines we "
            "are now building that reason, and what we want from them."
        ) as vo:
            self.play(FadeIn(m), run_time=2)
            for mk, acts in (("a", (1, 2)), ("b", (3, 4)), ("c", (5, 6)), ("d", (7, 8))):
                vo.wait_until(mk)
                self.play(*[Indicate(m.cols[k].head, color=GOAL) for k in acts])
        self.clear_scene()
        w = wall(upto=0).scale(0.48).move_to([-3.3, 0.0, 0])
        wl = label(r"The Wall", font_size=30, color=P.WALL).next_to(w, UP, buff=0.3)
        tb = VGroup(label(r"The Reasoner", font_size=30, color=CONN),
                    label(r"a toolbox we build, part by part", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12)
        pr = VGroup(label(r"The Price List", font_size=30, color=P.PRICE),
                    label(r"every way out of a contradiction", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.12)
        right = VGroup(tb, pr).arrange(DOWN, buff=0.8).move_to([3.6, 0.2, 0])
        with self.voiceover(
            "Three devices carry the story. <bookmark mark='a'/>The Reasoner: a toolbox of programs we build, "
            "part by part, each one checking a piece of philosophy by calculation. <bookmark mark='b'/>The Wall: "
            "philosophy's sharpest results are impossibility theorems, and each part lays one brick where "
            "calculation stops. <bookmark mark='c'/>And the Price List: when plausible claims contradict each "
            "other, every position in the debate is a choice of what to give up, and the machine can list those "
            "choices exactly."
        ) as vo:
            self.play(FadeIn(tb[0]), FadeIn(pr[0]), FadeIn(wl))
            vo.wait_until("a")
            self.play(FadeIn(tb[1], shift=LEFT * 0.2), Indicate(tb[0], color=CONN))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in w], lag_ratio=0.01), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(pr[1], shift=LEFT * 0.2), Indicate(pr[0], color=P.PRICE))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"the first philosophers: from myth to argument",
            r"what an argument is: validity, soundness and form",
            r"Zeno's race, Socrates' question, Plato's squares",
            r"Aristotle's logic: all 256 moods, checked by machine",
            r"Mohist, Nyāya and Stoic logic",
            r"Llull's wheels, Leibniz's numbers, and the Yijing in binary",
            r"what this logic cannot say",
        ], font_size=27)
        with self.voiceover(
            "This first part follows the dream from its beginnings. <bookmark mark='a'/>The first philosophers, and "
            "what changed when people began to give reasons instead of stories. What an argument is. "
            "<bookmark mark='b'/>Zeno's race, Socrates' question, Plato's squares. <bookmark mark='c'/>Aristotle's "
            "logic, all two hundred and fifty-six of its argument forms, checked by machine; and the logics of "
            "China and India. <bookmark mark='d'/>Then the people who first dreamed of mechanical reasoning: Ramon "
            "Llull with his wheels, and Leibniz with his numbers and his binary. And finally, what this first logic "
            "could not say, which is where Part 2 begins."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0], shift=RIGHT * 0.2))
            for mk, idx in (("a", [1]), ("b", [2]), ("c", [3, 4]), ("d", [5, 6])):
                vo.wait_until(mk)
                self.play(LaggedStart(*[FadeIn(card.rows[i], shift=RIGHT * 0.2) for i in idx], lag_ratio=0.3))
        self.clear_scene()
