from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Errors(VoiceoverScene):
    def construct(self):
        self.card()
        self.data()
        self.variability()

    def card(self):
        card = chapter_card(7, r"Fast errors and slow errors", r"Why are some mistakes quick and others slow?",
                            lit={1978: r"Ratcliff", 1998: r"Ratcliff \& Rouder", 2008: r"Ratcliff \& McKoon"},
                            part=PART, scale=("mind",), marr=("how",))
        with self.voiceover("Chapter seven. Fast errors and slow errors."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def data(self):
        d = load("selective")
        head = heading(r"Errors minus correct answers, \ median time")
        diff = 1000 * d["err_minus_correct"]
        A = axes([-0.5, 1.5], [-120, 400], x_length=5.4, y_length=4.4, xticks=[], yticks=[-100, 0, 100, 200, 300, 400],
                 yfmt=lambda v: f"{v:+.0f}" if v else "0", ylabel=r"error minus correct, \ ms", center=[-3.4, -0.2, 0],
                 font_size=16)
        zero = DashedLine(A.ax.c2p(-0.5, 0), A.ax.c2p(1.5, 0), color=GREY_C)
        assert diff.min() > -120 and diff.max() < 400
        rng = np.random.default_rng(4)
        jit = 0.18 * (rng.random(len(diff)) - 0.5)
        sp = scatter(A.ax, 0 + jit, diff[:, 0], SPEED, 0.08, 1)
        ac = scatter(A.ax, 1 + jit, diff[:, 1], CAREFUL, 0.08, 1)
        names = VGroup(label(r"``be fast''", font_size=20, color=SPEED).next_to(A.ax.c2p(0, -120), DOWN, buff=0.15),
                       label(r"``be accurate''", font_size=20, color=CAREFUL).next_to(A.ax.c2p(1, -120), DOWN,
                                                                                       buff=0.15))
        tags = VGroup(label(r"errors slower", font_size=17, color=GREY_B).next_to(A.ax.c2p(-0.45, 360), RIGHT,
                                                                                  buff=0.05),
                      label(r"errors faster", font_size=17, color=GREY_B).next_to(A.ax.c2p(-0.45, -95), RIGHT,
                                                                                  buff=0.05))
        nf, ns, n = d["fast_errors_speed"], d["slow_errors_accuracy"], len(diff)
        assert nf > n / 2 and ns > n / 2
        rows = rows_of([
            (r"the diffusion model of chapter five, \ started halfway, \ gives errors and correct answers the "
             r"same time", WHITE),
            (rf"told to be fast, \ {nf} of {n} people made their errors faster than their correct answers", SPEED),
            (rf"told to be accurate, \ {ns} of {n} made them slower", CAREFUL),
            (r"the same people, \ the same words: \ a model with four numbers cannot do both", LOST),
        ], 5.4, 23, 0.36).move_to([3.7, 0.0, 0])
        tag = psyche_tag(r"open data: \ Wagenmakers et al. (2008); \ medians per person")
        with self.voiceover(
            "Chapter five ended with a puzzle. With the start halfway between the bounds, the model gives errors "
            "and correct answers exactly the same time. <bookmark mark='a'/> Here is the difference, error minus "
            "correct, for each of the seventeen people, in each kind of block. <bookmark mark='b'/> Told to be fast, "
            f"{nf} of them made their errors faster than their correct answers. <bookmark mark='c'/> Told to be "
            f"accurate, {ns} made them slower. <bookmark mark='d'/> Same people, same words, and the pattern flips "
            "with the instruction. Four numbers can't do that."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(zero), FadeIn(names), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(sp), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(ac), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def variability(self):
        d = load("variability")
        head = heading(r"Trials are not all alike")
        cases = [r"no variability", r"drift varies", r"start varies"]
        A = axes([0, 3], [0.2, 0.38], x_length=6.0, y_length=3.4, xticks=[], yticks=[0.2, 0.25, 0.3, 0.35],
                 yfmt=lambda v: f"{1000 * v:.0f}", ylabel=r"mean decision time, \ ms", center=[-3.2, 0.3, 0],
                 font_size=16)
        bc = VGroup(*[bars(A.ax, [k + 0.32], [v], MODEL, 0.3) for k, v in enumerate(d["mean_correct"])])
        be = VGroup(*[bars(A.ax, [k + 0.68], [v], LOST, 0.3) for k, v in enumerate(d["mean_error"])])
        cl = VGroup(*[label(c, font_size=18, color=GREY_A).next_to(A.ax.c2p(k + 0.5, 0.2), DOWN, buff=0.12)
                      for k, c in enumerate(cases)])
        key = legend([(MODEL, r"correct"), (LOST, r"errors")], font_size=17).move_to(A.ax.c2p(0.5, 0.365))
        mc, me = d["mean_correct"], d["mean_error"]
        assert abs(mc[0] - me[0]) < 0.012 and me[1] > mc[1] + 0.02 and me[2] < mc[2] - 0.015
        pics = VGroup()
        for k, (txt, c) in enumerate(((r"some trials weak: \ they wander long, \ and err", DRIFT),
                                      (r"some starts near the wrong bound: \ quick slips", EVIDENCE))):
            pics.add(wrapped_label(txt, 1.8, 17, c).next_to(A.ax.c2p(k + 1.5, 0.2), DOWN, buff=0.55))
        rows = rows_of([
            (r"Ratcliff, \ 1978: \ the drift itself varies from trial to trial \ (attention, \ the item): "
             r"\ errors come mostly from weak trials, \ which are slow", DRIFT),
            (r"Ratcliff \& Rouder, \ 1998: \ the start varies too: \ a start near the wrong bound makes a fast "
             r"mistake", EVIDENCE),
            (r"a low bound lets start variability show: \ fast errors under speed; \ a wide bound lets drift "
             r"variability show: \ slow errors under accuracy", BOUND),
            (r"with variability in drift, \ start and $t_0$, \ seven numbers: \ the standard full diffusion model",
             MODEL),
        ], 5.4, 21, 0.32).move_to([3.7, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.simulate}: \ 60{,}000 trials per case; \ $v = 1$, \ $a = 1.2$")
        with self.voiceover(
            "The answer is that trials aren't all alike. <bookmark mark='a'/> In 1978 Ratcliff already let the "
            "drift vary from trial to trial, because attention wanders and some items are harder than others. "
            "Errors then come mostly from the weak trials, which wander for a long time before going wrong, so "
            "errors are slow. <bookmark mark='b'/> Twenty years later Ratcliff and Jeffrey Rouder let the starting "
            "point vary as well. Now some trials begin near the wrong bound and slip across it quickly, so errors "
            "are fast. Psyche's simulations show both: equal times with no variability, slow errors when the drift "
            "varies, fast errors when the start does. <bookmark mark='c'/> And the instruction decides which shows. "
            "A low bound, under speed, makes a starting offset matter a great deal: fast errors. A wide bound, under "
            "accuracy, washes out the start and leaves the weak trials: slow errors. <bookmark mark='d'/> With "
            "variability in drift, start and non-decision time, the model has seven numbers. That's the standard "
            "full diffusion model, and it fits both patterns at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(cl), FadeIn(key), FadeIn(bc[0]), FadeIn(be[0]))
            vo.wait_until("a")
            self.play(FadeIn(bc[1]), FadeIn(be[1]), FadeIn(pics[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bc[2]), FadeIn(be[2]), FadeIn(pics[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
