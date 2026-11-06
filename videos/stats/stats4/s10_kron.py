from __future__ import annotations

import numpy as np

from videos.stats.stats4.common import *  # noqa: F403

from videos.stats.stats4.s01_hook import heatmap


class Kron(VoiceoverScene):
    def construct(self):
        self.card()
        self.definition()
        self.vec()
        self.eig()
        self.field()

    def card(self):
        card = chapter_card(9, r"Kronecker products and vec", r"Structured covariances for space and time", lit=(),
                            part=PART)
        with self.voiceover("Chapter nine. Kronecker products and vec."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def definition(self):
        d = load("kron")
        K, T, Sp = np.asarray(d["K"]), np.asarray(d["T"]), np.asarray(d["Sp"])
        f = MathTex(r"A \otimes B", r"=", r"\begin{pmatrix} a_{11}B & \cdots & a_{1n}B \\ \vdots & & \vdots \\ a_{m1}B & "
                    r"\cdots & a_{mn}B \end{pmatrix}", font_size=34).to_edge(UP, buff=0.4)
        hs = heatmap(Sp, size=0.5, pos_color=SPACE).move_to([-4.6, -0.8, 0])
        ht = heatmap(T, size=0.5, pos_color=EIG).move_to([-2.2, -0.8, 0])
        hk = heatmap(K, size=0.42, pos_color=FIT).move_to([2.8, -0.8, 0])
        ls = label(r"2 sites", font_size=22, color=SPACE).next_to(hs, DOWN, buff=0.2)
        lt = label(r"3 times (AR(1))", font_size=22, color=EIG).next_to(ht, DOWN, buff=0.2)
        lk = label(r"site $\otimes$ time: \ $6 \times 6$", font_size=22, color=FIT).next_to(hk, DOWN, buff=0.2)
        ox = MathTex(r"\otimes", font_size=40).move_to([-3.4, -0.8, 0])
        eq = MathTex(r"=", font_size=40).move_to([0.0, -0.8, 0])
        props = label(r"$(A \otimes B)^{-1} = A^{-1} \otimes B^{-1}$, \ $\det$ and eigenvalues factor: \ big covariances, "
                      r"small work", font_size=24, color=S.ACCENT).to_edge(DOWN, buff=0.35)
        intro = label('A covariance with space and time structure', font_size=36)
        with self.voiceover(
            "Measurements in space and time have covariances with structure. <bookmark mark='a'/> The Kronecker "
            "product of A and B replaces each entry of A by that entry times the whole of B. "
            "<bookmark mark='b'/> Take a correlation between two measuring sites, <bookmark mark='c'/> and a "
            "correlation between three times that decays with the gap. <bookmark mark='d'/> Their Kronecker product "
            "is a six by six covariance for every site at every time, a pattern of blocks within blocks. "
            "<bookmark mark='e'/> Its inverse, determinant and eigenvalues all factor into those of the small "
            "pieces, which is what makes the spatial and longitudinal models of Parts 25 and 39 computable."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Write(f))
            vo.wait_until("b")
            self.play(FadeIn(hs), FadeIn(ls))
            vo.wait_until("c")
            self.play(FadeIn(ox), FadeIn(ht), FadeIn(lt))
            vo.wait_until("d")
            self.play(FadeIn(eq), FadeIn(hk), FadeIn(lk))
            vo.wait_until("e")
            self.play(FadeIn(props))
        self.clear_scene()

    def vec(self):
        d = load("kron")
        rows = [
            cmath(r"\operatorname{vec}(B)", r"=", r"\text{the columns of } B \text{, stacked}", font_size=34),
            cmath(r"\operatorname{vec}(ABC)", r"=", r"(C^\top \otimes A)\,\operatorname{vec}(B)", font_size=38),
            cmath(r"AXB = C", r"\iff", r"(B^\top \otimes A)\operatorname{vec}(X) = \operatorname{vec}(C)", font_size=34),
        ]
        rows[1][2].set_color(FIT)
        whys = [why(r"a matrix as one long vector"), why(r"the identity everything rests on"),
                why(r"a matrix equation as an ordinary linear system")]
        chk = MathTex(rf"\text{{checked: max error }} {d['err']:.1e}", font_size=26, color=SIM).to_edge(DOWN, buff=0.6)
        intro = label('Stack the columns', font_size=36)
        with self.voiceover(
            "The Kronecker product's partner is vec. <bookmark mark='a'/> Vec of a matrix stacks its columns into "
            "one long vector. <bookmark mark='b'/> And then a product of three matrices, unpacked, is a Kronecker "
            "product acting on the middle one: vec of A B C equals C transpose Kronecker A, times vec of B. "
            "<bookmark mark='c'/> That turns any linear matrix equation into an ordinary system of equations, and "
            "it's the bridge between matrix calculus and ordinary calculus in the next chapter."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.4, x=-0.8, buff=0.7, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
                if m == "b":
                    self.play(FadeIn(chk))
        self.clear_scene()

    def eig(self):
        e = load("extras")["kron_eig"]
        rows = [
            cmath(r"(A \otimes B)(\mathbf u \otimes \mathbf v)", r"=", r"(A\mathbf u) \otimes (B\mathbf v)", r"=",
                  r"\lambda\mu\, (\mathbf u \otimes \mathbf v)", font_size=32),
            cmath(r"\operatorname{eig}(A \otimes B)", r"=", r"\{\lambda_i \mu_j\}", font_size=36),
            cmath(r"\det(A_{m\times m} \otimes B_{n\times n})", r"=", r"(\det A)^n (\det B)^m", font_size=34),
        ]
        rows[1][2].set_color(EIG)
        whys = [why(r"the mixed-product rule"), why(r"all $mn$ products"), why(r"multiply them all")]
        chk = MathTex(r"\text{site} \otimes \text{time: } " + ", ".join(f"{v:.3f}" for v in e["kron"]), font_size=24, color=SIM)
        chk2 = MathTex(rf"\text{{products of the small eigenvalues: max difference }} {e['err']:.0e}", font_size=24, color=SIM)
        VGroup(chk, chk2).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.6)
        intro = label('Eigenvalues of a Kronecker product', font_size=36)
        with self.voiceover(
            "Why do Kronecker structures make big problems small? <bookmark mark='a'/> If u is an eigenvector of A "
            "and v of B, the Kronecker product of u and v is an eigenvector of A Kronecker B, with the product of "
            "the eigenvalues. <bookmark mark='b'/> So the eigenvalues of a Kronecker product are all the products of "
            "the small matrices' eigenvalues: an mn-dimensional problem solved with an m-dimensional one and an "
            "n-dimensional one. <bookmark mark='c'/> The determinant follows. For the site-time covariance, the six "
            "eigenvalues match the products exactly."
        ) as vo:
            self.play(FadeIn(intro))
            step = ladder(self, rows, whys, keep=3, top=2.6, x=-0.6, buff=0.6, edge=6.9)
            for k, m in enumerate("abc"):
                vo.wait_until(m)
                if k == 0:
                    self.play(FadeOut(intro), run_time=0.25)
                step(k, transform=False)
            self.play(FadeIn(chk), FadeIn(chk2))
        self.clear_scene()

    def field(self):
        e = load("extras3")["field"]
        a, b = np.asarray(e["a"]), np.asarray(e["b"])
        limit = max(3.2, np.ceil(max(np.abs(a).max(), np.abs(b).max())))
        A = axes([0, 60], [-limit, limit], x_length=10.0, y_length=3.6, xlabel=r"time", xticks=[0, 20, 40, 60],
                 yticks=[-2, 0, 2], center=[0, -0.8, 0])
        ax = A.ax
        ca = curve(ax, np.arange(60), a, SPACE, 3)
        cb = curve(ax, np.arange(60), b, EIG, 3)
        leg = legend([(SPACE, r"site 1"), (EIG, r"site 2")], font_size=22).move_to([5.2, 1.6, 0])
        f = MathTex(r"\mathbf x = (L_{\text{site}} \otimes L_{\text{time}})\,\mathbf z", r",\qquad",
                    r"\mathrm{Cov}\,\mathbf x = \Sigma_{\text{site}} \otimes \Sigma_{\text{time}}", font_size=32).to_edge(UP, buff=0.4)
        sub = label(rf"AR(1) in time, \ $\rho = 0.9$; \ sites correlated $0.7$ \ (this draw: {e['corr']:.2f})", font_size=22,
                    color=GREY_B).next_to(f, DOWN, buff=0.15)
        intro = label('Simulating a space--time field', font_size=36)
        with self.voiceover(
            "And Kronecker structure makes simulation cheap too. <bookmark mark='a'/> The Cholesky factor of a "
            "Kronecker product is the Kronecker product of the Cholesky factors. Multiply a vector of independent "
            "normals by it, and you get a draw with exactly the space-time covariance. <bookmark mark='b'/> Here are "
            "two sites over sixty time steps: each series wanders smoothly, because neighbouring times are "
            "correlated, and the two sites move together, because the sites are. Part 39 fits models like this to "
            "real measurements."
        ) as vo:
            self.play(FadeIn(intro))
            vo.wait_until("a")
            self.play(FadeOut(intro), run_time=0.25)
            self.play(Write(f), FadeIn(sub))
            vo.wait_until("b")
            self.play(FadeIn(A), Create(ca), Create(cb), FadeIn(leg), run_time=3.0)
        self.clear_scene()
