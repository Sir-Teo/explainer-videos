from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Looking(VoiceoverScene):
    def construct(self):
        self.card()
        self.fantz()
        self.habituate()
        self.voe()
        self.goldilocks()

    def card(self):
        card = chapter_card(2, r"Looking as an instrument", r"What does a long look measure?",
                            lit={1961: r"Fantz", 1985: r"Baillargeon et al.", 2012: r"Kidd et al."},
                            part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter two. Looking as an instrument."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def fantz(self):
        head = heading(r"Fantz's looking chamber")
        box = Rectangle(width=4.6, height=2.6, color=GREY_B, stroke_width=3).move_to([-3.6, 0.4, 0])
        kid = baby(0.45).move_to([-3.6, -0.3, 0])
        left = Circle(radius=0.45, color=WHITE).move_to([-4.8, 1.2, 0])
        bulls = VGroup(*[Circle(radius=r, color=WHITE, stroke_width=3) for r in (0.45, 0.3, 0.15)]).move_to(
            [-2.4, 1.2, 0])
        face_ = VGroup(Circle(radius=0.45, color=WHITE), Dot([-0.15, 0.1, 0], radius=0.06),
                       Dot([0.15, 0.1, 0], radius=0.06), Arc(radius=0.18, start_angle=-2.4, angle=1.7)).move_to(
            [-4.8, 1.2, 0])
        eye = DashedLine(kid.get_top(), [-3.6, 1.5, 0], color=LOOK)
        rows = rows_of([
            (r"Robert Fantz, \ late 1950s: \ an infant lies in a chamber; \ two pictures hang above; \ an observer "
             r"watches the reflections in the infant's eyes through a peephole", WHITE),
            (r"time each look: \ if the infant looks longer at one picture, \ it can tell them apart, \ and "
             r"prefers one", LOOK),
            (r"newborns and young infants looked longer at patterns, \ such as a face, \ a bull's-eye or "
             r"stripes, \ than at plain fields", OBJ),
            (r"later studies disagree on whether faces beat other patterns so early; \ the method survived the "
             r"argument", GREY_A),
        ], 5.8, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = historical_tag(r"Fantz (1961)")
        with self.voiceover(
            "The way in came from a simple observation: infants can't answer, but they can look, and looking can be "
            "timed. <bookmark mark='a'/> In the late 1950s Robert Fantz built a looking chamber. An infant lay "
            "inside, two pictures hung above, and an observer watched through a peephole for the reflection of a "
            "picture in the infant's eyes. <bookmark mark='b'/> Time each look. If the infant looks longer at one "
            "picture, it can tell them apart, and prefers one. <bookmark mark='c'/> Newborns and young infants "
            "looked longer at patterns, such as a face, a bull's-eye or stripes, than at plain fields. "
            "<bookmark mark='d'/> Later studies disagree on whether faces beat other patterns so early. But the "
            "method survived the argument, and became developmental psychology's main instrument."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Create(box), FadeIn(kid))
            vo.wait_until("a")
            self.play(FadeIn(face_), FadeIn(bulls), Create(eye), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def habituate(self):
        d = load("habituation")
        head = heading(r"Habituation, \ and recovery")
        A = axes([0, 11], [0, 22], x_length=6.0, y_length=3.6, xticks=[1, 4, 7], yticks=[0, 5, 10, 15, 20],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"trial", ylabel=r"look \ (seconds)",
                 center=[-3.2, -0.2, 0], font_size=16)
        n = int(d["criterion"])
        t, lk = np.asarray(d["trial"])[:n], np.asarray(d["looks"])[:n]
        famb = bars(A.ax, t, lk, LOOK, width=0.6)
        crit = DashedLine(A.ax.c2p(0.5, d["first3"] / 2), A.ax.c2p(n + 0.5, d["first3"] / 2), color=GREY_B)
        cl = label(r"half the first three", font_size=15, color=GREY_B).next_to(crit, UP, buff=0.06).align_to(crit,
                                                                                                           RIGHT)
        test = VGroup(bars(A.ax, [n + 2], [d["familiar"]], GREY_B, width=0.6),
                      bars(A.ax, [n + 3], [d["novel"]], OBJ, width=0.6))
        tl = VGroup(label(r"same", font_size=16, color=GREY_B).next_to(A.ax.c2p(n + 2, 0), DOWN, buff=0.15),
                    label(r"new", font_size=16, color=OBJ).next_to(A.ax.c2p(n + 3, 0), DOWN, buff=0.15))
        rows = rows_of([
            (r"show the same display again and again: \ looks get shorter as the infant learns it", LOOK),
            (rf"the usual criterion: \ three looks in a row under half the first three; \ here, \ after trial {n}",
             WHITE),
            (r"then a test: \ the same display again, \ or a new one; \ a longer look at the new one means the "
             r"infant noticed the difference", OBJ),
            (r"Psyche: \ interest falls as a memory of the display builds; \ a new display restores part of it",
             MODEL),
        ], 5.6, 21, 0.32).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{develop.habituation}")
        with self.voiceover(
            "The most useful version of looking is habituation. <bookmark mark='a'/> Show the same display again "
            "and again, and the looks get shorter as the infant learns it. <bookmark mark='b'/> Laboratories use a "
            f"criterion: three looks in a row shorter than half the first three. Here it's met after trial {n}. "
            "<bookmark mark='c'/> Then comes the test: the same display again, or a new one. A longer look at the "
            "new one means the infant noticed the difference. <bookmark mark='d'/> Psyche's version: interest falls "
            "as a memory of the display builds, and a new display restores part of it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in famb], lag_ratio=0.2), FadeIn(rows[0]),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(Create(crit), FadeIn(cl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(test), FadeIn(tl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def voe(self):
        head = heading(r"Violation of expectation")
        rows = rows_of([
            (r"show an event that is possible, \ and one that would be impossible if the infant knew some fact "
             r"about the world", WHITE),
            (r"if the infant looks longer at the impossible one, \ perhaps it expected otherwise", OBJ),
            (r"the trouble: \ a longer look can mean surprise, \ novelty, \ familiarity, \ or simply more to look "
             r"at; \ which way a preference points depends on how long the infant was familiarized", LOST),
            (r"so looking studies need controls for each low-level difference, \ and the interpretation of a "
             r"long look is always an inference", LOOK),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        with self.voiceover(
            "Looking also powers the most used design in infant cognition, violation of expectation. "
            "<bookmark mark='a'/> Show an event that is possible, and one that would be impossible if the infant "
            "knew some fact about the world. <bookmark mark='b'/> If the infant looks longer at the impossible one, "
            "perhaps it expected otherwise. <bookmark mark='c'/> The trouble is that a longer look can mean "
            "surprise, but also novelty, a preference for the familiar, or simply that there is more to look at. "
            "And which way a preference points depends on how long the infant was familiarized beforehand. "
            "<bookmark mark='d'/> So looking studies need controls for every low-level difference, and reading a "
            "long look as knowledge is always an inference. This is Part 3's question, what does an instrument "
            "measure, in its hardest form."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def goldilocks(self):
        d = load("goldilocks")
        head = heading(r"The Goldilocks effect")
        A = axes([0, 4], [0, 0.45], x_length=5.8, y_length=3.4, xticks=[0, 1, 2, 3, 4], yticks=[0, 0.1, 0.2, 0.3, 0.4],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"surprisal of the event \ (bits)",
                 ylabel=r"chance of looking away", center=[-3.2, -0.3, 0], font_size=16)
        s, r = np.asarray(d["surprisal"]), np.asarray(d["rate"])
        ok = np.isfinite(r)
        dots = scatter(A.ax, s[ok], r[ok], LOOK, radius=0.07)
        cv = curve(A.ax, s[ok], r[ok], LOOK, 3)
        best = DashedLine(A.ax.c2p(d["best"], 0), A.ax.c2p(d["best"], 0.45), color=GOOD, stroke_width=2)
        rows = rows_of([
            (r"Celeste Kidd, \ Steven Piantadosi and Richard Aslin, \ 2012: \ 7- and 8-month-olds watched objects "
             r"pop out of three boxes, \ in sequences of varied predictability", WHITE),
            (r"an ideal learner gave each event a surprisal; \ infants were most likely to look away from events "
             r"that were very predictable, \ or very surprising", LOOK),
            (r"attention seeks the middle: \ things neither too simple nor too complex, \ where there is most to "
             r"learn", GOOD),
            (r"Psyche's observer, \ built with that U-shaped rule, \ an assumption shaped after the result, \ not "
             r"fitted to its data", MODEL),
        ], 5.6, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{develop.goldilocks}: \ a Dirichlet-multinomial learner")
        with self.voiceover(
            "Looking is not only a measure. It's a choice the infant makes about what to learn from. "
            "<bookmark mark='a'/> In 2012 Celeste Kidd, Steven Piantadosi and Richard Aslin showed seven- and "
            "eight-month-olds objects popping out of three boxes, in sequences of varied predictability. "
            "<bookmark mark='b'/> An ideal learner model gave each event a surprisal, how unexpected it was. "
            "Infants were most likely to look away from events that were very predictable, or very surprising. "
            "<bookmark mark='c'/> Attention seeks the middle: things neither too simple nor too complex, where "
            "there is most to learn. They called it the Goldilocks effect. <bookmark mark='d'/> Psyche's observer "
            "here is built with that U-shaped rule. It's an assumption shaped after the result, not a fit to the "
            "data; what Psyche adds is the learner that measures surprisal."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots), Create(cv), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(best), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
