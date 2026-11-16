from __future__ import annotations

from videos.psychology.psych44.common import *  # noqa: F403
from videos.psychology.psych44.diagrams import arrow, node


class Full(VoiceoverScene):
    def construct(self):
        self.card()
        self.structure()
        self.attenuation()
        self.omega()

    def card(self):
        card = chapter_card(6, r"Measurement and structure", r"What is the correlation between two traits, \ not two "
                            r"tests?", lit=(), part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter six. Measurement and structure."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def structure(self):
        head = heading(r"Two layers")
        f1, f2 = node(r"F1", MODEL, latent=True, r=0.5), node(r"F2", SYMP, latent=True, r=0.5)
        f1.move_to([-4.6, 0.8, 0])
        f2.move_to([-1.6, 0.8, 0])
        xs = VGroup(*[node(f"x{i + 1}", GREY_A, r=0.25) for i in range(6)]).arrange(RIGHT, buff=0.25).move_to([-3.1, -1.2, 0])
        arrs = VGroup(*[arrow(f1 if i < 3 else f2, xs[i], color=MODEL if i < 3 else SYMP) for i in range(6)])
        reg = arrow(f1, f2, color=YOU, text=r"$\beta$")
        rows = rows_of([
            (r"the measurement model: \ each latent variable and its indicators, \ with their errors", MODEL),
            (r"the structural model: \ arrows between the latent variables themselves, \ a regression among things "
             r"never observed", YOU),
            (r"because the errors are modelled, \ the structural arrows are free of measurement error: \ Part 3's "
             r"correction for attenuation, \ done inside the model", GOOD),
        ], 6.0, 20, 0.42).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "A full structural equation model has two layers. <bookmark mark='a'/> The measurement model: each latent "
            "variable and its indicators, with their errors. <bookmark mark='b'/> The structural model: arrows "
            "between the latent variables themselves, a regression among things never observed. "
            "<bookmark mark='c'/> Because the errors are modelled, the structural arrows are free of measurement error. "
            "It's Part 3's correction for attenuation, done inside the model."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(f1, f2, xs)), FadeIn(arrs))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(reg))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def attenuation(self):
        d = load("attenuation")
        head = heading(r"Attenuation, \ undone")
        A = axes([0.3, 3.7], [0, 0.6], x_length=5.0, y_length=3.0, xticks=None, yticks=[0, 0.25, 0.5],
                 yfmt=lambda v: f"{v:g}", ylabel=r"correlation", center=[-3.4, 0.5, 0], font_size=13)
        b = bars(A.ax, [1, 2, 3], [d["true"], d["sum_r"], d["latent_r"]], [GREY_B, AUTH, GOOD], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.6, 16, c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.15) for i, (t, c) in
                         enumerate(((r"the truth", GREY_B), (r"sum scores", AUTH), (r"latent, \ from the CFA", GOOD)))])
        rows = rows_of([
            (r"Psyche: \ two traits correlated 0.5, \ each measured by three items with loadings 0.6, \ in 500 people", WHITE),
            (rf"the sum scores have reliability (alpha) {d['alpha']:.2f}, \ and correlate only {d['sum_r']:.2f}", AUTH),
            (rf"the two-factor model recovers {d['latent_r']:.2f}: \ the relation between the traits, \ not the tests", GOOD),
            (r"the correction is only as good as the measurement model: \ if the items measure something else too, \ "
             r"it corrects the wrong thing", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{sem.fit\_cfa}, \ 500 simulated people")
        with self.voiceover(
            "Here is the correction at work. <bookmark mark='a'/> Psyche makes two traits that correlate zero point "
            "five, each measured by three items with loadings of zero point six, in five hundred people. "
            "<bookmark mark='b'/> The sum scores have a reliability of about zero point six, and correlate only about "
            "zero point three. <bookmark mark='c'/> The two-factor model recovers about zero point five: the relation "
            "between the traits, not the tests. <bookmark mark='d'/> The correction is only as good as the "
            "measurement model. If the items measure something else as well, it corrects the wrong thing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(b[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def omega(self):
        d = load("omega")
        head = heading(r"Reliability, \ from the loadings")
        eq = MathTex(r"\omega = \frac{(\sum_j \lambda_j)^2}{(\sum_j \lambda_j)^2 + \sum_j \theta_j}", font_size=40,
                     color=MODEL).move_to([-3.6, 1.4, 0])
        A = axes([0.3, 3.7], [0, 1], x_length=5.0, y_length=2.4, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{v:g}", ylabel=r"reliability", center=[-3.6, -1.2, 0], font_size=13)
        xs = np.array([1, 2, 3])
        bo = bars(A.ax, xs - 0.17, d["omega"], [MODEL] * 3, width=0.3)
        ba = bars(A.ax, xs + 0.17, d["alpha"], [GREY_B] * 3, width=0.3)
        names = VGroup(*[label(t, font_size=15, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.12)
                         for i, t in enumerate((r"visual", r"verbal", r"speed"))])
        key = VGroup(label(r"omega", font_size=14, color=MODEL), label(r"alpha", font_size=14, color=GREY_B)).arrange(
            RIGHT, buff=0.4).next_to(A, UP, buff=0.05)
        rows = rows_of([
            (r"the factor model gives each test's true-score share directly: \ McDonald's omega", MODEL),
            (rf"for Holzinger and Swineford's three factors, \ omega and alpha agree: \ {d['omega'][0]:.2f}, "
             rf"{d['omega'][1]:.2f} and {d['omega'][2]:.2f}", WHITE),
            (rf"they agree only when the loadings are alike; \ with loadings 0.9, 0.8, 0.3 and 0.2, \ alpha is "
             rf"{d['cong_alpha']:.2f} and omega {d['cong_omega']:.2f}: \ alpha understates", AUTH),
            (r"Part 3's alpha assumed equal loadings; \ the CFA tests that assumption instead of making it", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{sem.fit\_cfa}; \ Holzinger \& Swineford's tests")
        with self.voiceover(
            "The loadings also say how reliable a scale is. <bookmark mark='a'/> The share of a sum score that is true "
            "score is the squared sum of the loadings, over that plus the error variances. It's McDonald's omega. "
            "<bookmark mark='b'/> For Holzinger and Swineford's three factors, omega and Part 3's alpha agree. "
            "<bookmark mark='c'/> But they agree only when the loadings are alike. With loadings of zero point nine, "
            "eight, three and two, alpha is about zero point six and omega about zero point six seven. Alpha "
            "understates. <bookmark mark='d'/> Alpha assumed equal loadings. The factor model tests that assumption "
            "instead of making it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(A), FadeIn(names), FadeIn(key), FadeIn(bo), FadeIn(ba))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
