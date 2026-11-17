from __future__ import annotations

from videos.psychology.psych48.common import *  # noqa: F403


class Sloppy(VoiceoverScene):
    def construct(self):
        self.card()
        self.ridge()
        self.tradeoff()

    def card(self):
        card = chapter_card(5, r"Parameters that trade off", r"Can two parameters explain the same thing?",
                            lit=(), part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter five. Parameters that trade off."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def ridge(self):
        d = load("surface")
        head = heading(r"The likelihood surface")
        ll = d["ll"]
        top = ll.max()
        a, b = d["alpha"], d["beta"]
        cell_w, cell_h = 5.6 / len(b), 4.0 / len(a)
        grid = VGroup()
        for i in range(len(a)):
            for j in range(len(b)):
                v = float(np.clip((ll[i, j] - top + 12) / 12, 0, 1))
                grid.add(Rectangle(width=cell_w, height=cell_h, stroke_width=0,
                                   fill_color=interpolate_color(ManimColor("#14181F"), ManimColor(PERSON), v),
                                   fill_opacity=1).move_to([-5.9 + (j + 0.5) * cell_w, -1.9 + (i + 0.5) * cell_h, 0]))
        i0, j0 = np.unravel_index(ll.argmax(), ll.shape)
        best = Dot([-5.9 + (j0 + 0.5) * cell_w, -1.9 + (i0 + 0.5) * cell_h, 0], radius=0.08, color=WHITE)
        xl = label(r"inverse temperature $\beta$ (0.5 to 15)", font_size=13, color=GREY_A).next_to(grid, DOWN, buff=0.12)
        yl = label(r"learning rate $\alpha$ (0 to 1)", font_size=13, color=GREY_A).rotate(PI / 2).next_to(grid, LEFT,
                                                                                                         buff=0.12)
        rows = rows_of([
            (r"the log-likelihood of Psyche's 200 choices at every learning rate and inverse temperature; \ bright "
             r"is likely", WHITE),
            (r"the bright region is a curved ridge, \ not a peak: \ a lower learning rate with a higher temperature "
             r"explains the data almost as well", MODEL),
            (r"the two trade off: \ fast learning with noisy choice, \ or slow learning with sharp choice", PERSON),
            (r"so a group difference in one parameter can be a difference in the other: \ compare people on both, \ "
             r"or fix one by design", AUTH),
        ], 5.6, 18, 0.36).move_to([3.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.tradeoff\_surface}")
        with self.voiceover(
            "Why is one parameter recovered better than another? Look at the whole likelihood. "
            "<bookmark mark='a'/> Here is the log-likelihood of Psyche's two hundred choices at every combination "
            "of learning rate and inverse temperature. Bright is likely. <bookmark mark='b'/> The bright region is a "
            "curved ridge, not a peak. A lower learning rate with a higher temperature explains the data almost as "
            "well. <bookmark mark='c'/> The two trade off: fast learning with noisy choice, or slower learning with "
            "sharper choice. <bookmark mark='d'/> So a difference between groups in one parameter can really be a "
            "difference in the other. Compare people on both, or pin one down by design."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid), FadeIn(xl), FadeIn(yl), FadeIn(best))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def tradeoff(self):
        d = load("tradeoff")
        head = heading(r"The ridge, \ in repeated fits")
        A = axes([0.1, 0.6], [2, 10], x_length=5.0, y_length=3.2, xticks=[0.2, 0.3, 0.4, 0.5], yticks=[3, 5, 7, 9],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"fitted learning rate",
                 ylabel=r"fitted inverse temperature", center=[-3.5, 0.3, 0], font_size=12)
        dots = scatter(A.ax, d["alpha"], d["beta"], MODEL, radius=0.06)
        true = Dot(A.ax.c2p(0.3, 5.0), radius=0.1, color=GOOD)
        tl = label(r"the truth", font_size=13, color=GOOD).next_to(true, UR, buff=0.05)
        rows = rows_of([
            (r"one learner (0.3 and 5), \ simulated 40 times, \ fitted each time", WHITE),
            (rf"the two estimates are negatively correlated, \ $r = {d['r']:.2f}$: \ when one comes out high, \ the "
             rf"other tends to come out low", AUTH),
            (r"a fast learner who chooses noisily and a slow one who chooses sharply produce similar choices", PERSON),
            (r"so report them together, \ compare people on what is well determined, \ or design tasks (more "
             r"reversals) that pull them apart", YOU),
        ], 6.4, 19, 0.36).move_to([3.3, -0.1, 0])
        tag = psyche_tag(r"\texttt{fit.fit}, \ 40 simulations")
        with self.voiceover(
            "The ridge shows up in repeated fits too. <bookmark mark='a'/> Take one learner, simulate it forty times, "
            "and fit it each time. <bookmark mark='b'/> The two estimates are negatively correlated: when one comes "
            "out high, the other tends to come out low. <bookmark mark='c'/> A fast learner who chooses noisily and a "
            "slow one who chooses sharply produce similar choices. <bookmark mark='d'/> So report the two together, "
            "compare people on what's well determined, or design tasks, with more reversals, that pull them apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(dots), FadeIn(true), FadeIn(tl))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
