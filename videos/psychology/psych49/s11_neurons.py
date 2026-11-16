from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Neurons(VoiceoverScene):
    def construct(self):
        self.card()
        self.popvec()
        self.manifold()

    def card(self):
        card = chapter_card(10, r"Populations of neurons", r"How do many noisy cells code one movement?", lit=(),
                            part=PART, scale=("cell", "brain"), marr=("how",))
        with self.voiceover("Chapter ten. Populations of neurons."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def popvec(self):
        d = load("popvec")
        head = heading(r"The population vector")
        A = axes([0, 270], [0, 50], x_length=5.6, y_length=3.0, xticks=[4, 32, 64, 128, 256], yticks=[0, 20, 40],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: rf"{v:.0f}^\circ", xlabel=r"neurons recorded",
                 ylabel=r"average error in direction", center=[-3.3, 0.3, 0], font_size=12)
        c = curve(A.ax, d["n"], d["error_deg"], MODEL, stroke_width=4)
        dots = VGroup(*[Dot(A.ax.c2p(n, e), radius=0.07, color=MODEL) for n, e in zip(d["n"], d["error_deg"])])
        rows = rows_of([
            (r"1982: \ Apostolos Georgopoulos and colleagues found motor-cortex neurons broadly tuned to the "
             r"direction of an arm movement: \ each fires most for one direction, \ less for others", WHITE),
            (r"each neuron votes for its preferred direction, \ weighted by how much it fires; \ the sum of votes points "
             r"the way the arm moves", MODEL),
            (rf"Psyche's noisy cosine-tuned neurons: \ 4 cells miss by {d['error_deg'][0]:.0f}$^\circ$ on average, \ "
             rf"256 by {d['error_deg'][-1]:.0f}$^\circ$", PERSON),
            (r"no single cell is precise; \ the population is", GOOD),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{neurodata.population\_vector\_error}")
        tag2 = published_tag(r"Georgopoulos et al.\ (1982)").to_corner(DL, buff=0.3)
        with self.voiceover(
            "Below the voxel are the neurons. <bookmark mark='a'/> In 1982 Apostolos Georgopoulos and colleagues "
            "found motor-cortex neurons broadly tuned to the direction of an arm movement. Each fires most for one "
            "direction, and less for others. <bookmark mark='b'/> Let each neuron vote for its preferred direction, "
            "weighted by how much it fires, and the sum of the votes points the way the arm moves. "
            "<bookmark mark='c'/> With Psyche's noisy neurons, four cells miss by more than forty degrees on average, "
            "and two hundred and fifty-six by about six. <bookmark mark='d'/> No single cell is precise. The "
            "population is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(tag2), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(c), FadeIn(dots))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def manifold(self):
        d = load("manifold")
        head = heading(r"A hundred neurons, \ two dimensions")
        v = np.asarray(d["var_share"])[:8]
        A = axes([0.3, 8.7], [0, 0.8], x_length=4.4, y_length=2.8, xticks=list(range(1, 9)), yticks=[0, 0.25, 0.5, 0.75],
                 xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{100 * y:.0f}\\%", xlabel=r"principal component",
                 ylabel=r"share of variance", center=[-4.3, 0.6, 0], font_size=12)
        b = bars(A.ax, list(range(1, 9)), v, [MODEL, MODEL] + [GREY_B] * 6, width=0.6)
        P = np.asarray(d["pcs"])
        P = P / np.abs(P).max() * 1.4
        traj = VMobject(stroke_color=PERSON, stroke_width=2).set_points_smoothly(
            [np.array([0.2 + p[0], 0.6 + p[1], 0]) for p in P[::3]])
        frame = Square(3.2, stroke_color=GREY_D, stroke_width=1).move_to([0.2, 0.6, 0])
        flab = label(r"activity, \ first two components", font_size=14, color=GREY_A).next_to(frame, DOWN, buff=0.1)
        rows = rows_of([
            (r"a hundred neurons during slow, \ wandering reaches: \ a hundred numbers at every moment", WHITE),
            (rf"two components hold {100 * (v[0] + v[1]):.0f}\% of the variance; \ the rest is noise", MODEL),
            (r"the activity lives on a ring: \ the direction of the movement; \ a neural manifold", PERSON),
            (r"in real recordings the manifolds are low-dimensional too, \ and their dynamics, \ not single cells, \ "
             r"are what models of the motor cortex now explain", YOU),
        ], 4.4, 18, 0.32).move_to([4.6, -0.1, 0])
        tag = psyche_tag(r"\texttt{neurodata.manifold}")
        with self.voiceover(
            "Populations also have shapes. <bookmark mark='a'/> A hundred neurons, recorded during slow, wandering "
            "reaches: a hundred numbers at every moment. <bookmark mark='b'/> Principal components show that two "
            "dimensions hold over ninety percent of the variance. The rest is noise. <bookmark mark='c'/> Plotted in "
            "those two dimensions, the activity lives on a ring, the direction of the movement. It's called a neural "
            "manifold. <bookmark mark='d'/> In real recordings the manifolds are low-dimensional too, and their "
            "dynamics, not single cells, are what models of the motor cortex now try to explain."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(frame), FadeIn(flab), Create(traj), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
