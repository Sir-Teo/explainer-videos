from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Confidence(VoiceoverScene):
    def construct(self):
        self.card()
        self.balance()
        self.folded()

    def card(self):
        card = chapter_card(11, r"Confidence", r"Where does the feeling of being sure come from?",
                            lit={1979: r"Vickers", 2009: r"Kiani \& Shadlen", 2010: r"Pleskac \& Busemeyer",
                                 2016: r"Sanders et al."},
                            part=PART, scale=("mind", "neuron"), marr=("what",))
        with self.voiceover("Chapter eleven. Confidence."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def balance(self):
        head = heading(r"The balance of evidence")
        A = axes([0, 1.0], [0, 2.2], x_length=5.6, y_length=3.6, xticks=[0, 0.5, 1.0], yticks=[0, 1, 2],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", xlabel=r"time, \ s", ylabel=r"evidence",
                 center=[-3.3, -0.2, 0], font_size=16)
        rng = np.random.default_rng(31)
        dt = 0.005
        x = np.zeros((2, 1))
        traj = [[0.0], [0.0]]
        drift = np.array([2.6, 0.6])
        while x.max() < 2.0 and len(traj[0]) < 400:
            x = np.maximum(x + (drift * dt)[:, None] + np.sqrt(dt) * rng.standard_normal((2, 1)), 0)
            traj[0].append(float(x[0, 0]))
            traj[1].append(float(x[1, 0]))
        t = np.arange(len(traj[0])) * dt
        win = int(np.argmax([traj[0][-1], traj[1][-1]]))
        lines = VGroup(*[VMobject(color=c, stroke_width=3).set_points_as_corners(
            [A.ax.c2p(float(tt), float(v)) for tt, v in zip(t, tr)]) for tr, c in zip(traj, (MODEL, LOST))])
        bound = DashedLine(A.ax.c2p(0, 2.0), A.ax.c2p(1.0, 2.0), color=BOUND, stroke_width=2)
        te = float(t[-1])
        gap = DoubleArrow(A.ax.c2p(te, traj[1 - win][-1]), A.ax.c2p(te, traj[win][-1]), buff=0, color=WHITE,
                          stroke_width=3, tip_length=0.15)
        gl = label(r"the gap: \ confidence", font_size=18, color=WHITE).next_to(gap, RIGHT, buff=0.1)
        key = legend([(MODEL, r"for ``right''"), (LOST, r"for ``left''")], font_size=17).move_to(A.ax.c2p(0.25, 1.75))
        assert win == 0 and te < 1.0
        rows = rows_of([
            (r"Vickers, \ 1979: \ when one accumulator wins the race, \ the other's level says how close it was: "
             r"\ the balance of evidence", WHITE),
            (r"Kiani \& Shadlen, \ 2009: \ monkeys offered a small sure reward chose it most when evidence was weak, "
             r"\ and LIP neurons carried that confidence", MODEL),
            (r"Pleskac \& Busemeyer, \ 2010: \ evidence keeps arriving after the answer; \ confidence reads it, \ "
             r"and so do changes of mind", EVIDENCE),
        ], 5.4, 22, 0.36).move_to([3.7, 0.0, 0])
        tag = published_tag(r"Vickers (1979); \ Kiani \& Shadlen (2009); \ Pleskac \& Busemeyer (2010)")
        with self.voiceover(
            "You felt more sure about the first cloud of dots than the second. Where does that feeling come from? "
            "<bookmark mark='a'/> In a race, Douglas Vickers suggested in 1979, the answer is in the loser. When one "
            "accumulator reaches its bound, how far behind the other is tells you how close the race was. That gap, "
            "the balance of evidence, is confidence. <bookmark mark='b'/> In 2009 Roozbeh Kiani and Michael "
            "Shadlen gave monkeys a third option: a small reward that was certain. The monkeys took it most when the "
            "evidence was weak, as if they knew when they were unsure, and the same LIP neurons carried that "
            "confidence in their firing. <bookmark mark='c'/> And Timothy Pleskac and Jerome Busemeyer argued in "
            "2010 that evidence keeps arriving after the answer is given. Confidence reads it, which is why people "
            "sometimes change their minds a moment after choosing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(bound))
            self.play(Create(lines), FadeIn(key), run_time=3)
            vo.wait_until("a")
            self.play(GrowFromCenter(gap), FadeIn(gl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def folded(self):
        d = load("confidence")
        head = heading(r"The folded X")
        A = axes([0, 3.4], [0.3, 0.8], x_length=5.6, y_length=3.6, xticks=[0, 1, 2, 3], yticks=[0.3, 0.5, 0.7],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"strength of the evidence \ (drift)",
                 ylabel=r"confidence, \ share of the bound", center=[-3.3, -0.2, 0], font_size=16)
        cc = curve(A.ax, d["v"], d["conf_correct"], MODEL, 3)
        ce = curve(A.ax, d["v"], d["conf_error"], LOST, 3)
        dots = VGroup(scatter(A.ax, d["v"], d["conf_correct"], MODEL, 0.06, 1),
                      scatter(A.ax, d["v"], d["conf_error"], LOST, 0.06, 1))
        key = legend([(MODEL, r"correct answers"), (LOST, r"errors")], font_size=17).move_to(A.ax.c2p(0.9, 0.37))
        assert d["conf_correct"][-1] > d["conf_correct"][0] and d["conf_error"][-1] < d["conf_error"][0] - 0.2
        assert np.all(d["conf_correct"] > d["conf_error"])
        rows = rows_of([
            (r"Psyche's race, \ 3{,}000 trials at each strength: \ confidence on correct answers rises with the "
             r"evidence; \ on errors it falls", MODEL),
            (r"an error on an easy trial is a fluke, \ and it feels like one", LOST),
            (r"Sanders, \ Hangya \& Kepecs, \ 2016: \ people's confidence shows the same folded X", WHITE),
            (r"Part 12's meta-$d'$ \ (Maniscalco \& Lau, \ 2012) \ measures how well confidence tracks accuracy; "
             r"\ here is a mechanism that could produce it", EVIDENCE),
        ], 5.4, 22, 0.36).move_to([3.7, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.race\_confidence}; \ Sanders et al. (2016)")
        with self.voiceover(
            "The balance of evidence makes a distinctive prediction. <bookmark mark='a'/> Run Psyche's race at many "
            "strengths of evidence and average its confidence. On correct answers, confidence rises with the "
            "strength of the evidence. On errors it falls. <bookmark mark='b'/> An error on an easy trial is a "
            "fluke: the loser was nearly at the bound too, and it feels like a fluke. <bookmark mark='c'/> In 2016 "
            "Joshua Sanders, Balázs Hangya and Adam Kepecs found the same folded X in people's confidence. "
            "<bookmark mark='d'/> Part 12 measured how well confidence tracks accuracy, with meta d prime. Here is "
            "a mechanism that could produce it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cc), Create(ce), FadeIn(dots), FadeIn(key), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
