from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403
from videos.psychology.psych58.s01_hook import tiles


class Sparse(VoiceoverScene):
    def construct(self):
        card_section(self, 3, r"Sparse coding", r"Why edges?", marr=("how",))
        self.objective()
        self.compare()
        self.caveats()

    def objective(self):
        rows_section(self, r"The objective, \ written out", [
            (r"describe each patch $x$ as a sum of basis functions: \ $x \approx D a$", WHITE),
            (r"minimize \ $\tfrac{1}{2}\lVert x - D a\rVert^2 + \lambda \sum_i |a_i|$: \ fit well, \ with few "
             r"active units", MODEL),
            (r"for each patch, \ find the code $a$ (a few steps of shrinkage, \ ISTA); \ then nudge $D$ to fit "
             r"better; \ repeat", PERSON),
            (r"$\lambda$ sets the price of activity: \ too low and the units stay spread out; \ too high and the "
             r"fit is poor", AUTH),
            (r"Olshausen and Field ran this on whitened photographs in 1996: \ localized, \ oriented, \ band-pass "
             r"units, \ like V1's simple cells", GOOD),
        ], "Why edges? Here's the objective, written out. <bookmark mark='a'/> Describe each patch x as a sum of "
           "basis functions: D times a code a. <bookmark mark='b'/> Minimize the squared error plus lambda times the "
           "sum of the absolute values of the code. Fit well, with few active units. <bookmark mark='c'/> For each "
           "patch, find the code with a few steps of shrinkage, an algorithm called ISTA. Then nudge the basis "
           "functions to fit better, and repeat. <bookmark mark='d'/> Lambda sets the price of activity. Too low, "
           "and the units stay spread out. Too high, and the fit is poor. <bookmark mark='e'/> Olshausen and Field "
           "ran this on whitened photographs in 1996, and got localized, oriented, band-pass units, like V1's "
           "simple cells.", tag=published_tag(r"Olshausen \& Field (1996)"))

    def compare(self):
        d = load("sparse")
        head = heading(r"Sparse, \ against the principal components")
        left = tiles(d["D"], height=3.4, center=[-4.4, 0.6, 0])
        right = tiles(d["pcs"], height=3.4, center=[-0.6, 0.6, 0])
        ll = label(r"sparse code", font_size=15, color=GOOD).next_to(left, DOWN, buff=0.12)
        rl = label(r"principal components", font_size=15, color=CROWD).next_to(right, DOWN, buff=0.12)
        A = axes([0.4, 3.6], [0, 1.0], x_length=3.0, y_length=2.0, xticks=None, yticks=[0, 0.5, 1.0],
                 yfmt=lambda v: f"{v:g}", ylabel=r"localized", center=[4.6, 1.1, 0], font_size=11)
        vals = [np.median(d["loc"]), np.median(d["pca_loc"]), np.median(d["rand_loc"])]
        cols = [GOOD, CROWD, GREY_B]
        bs = VGroup(*[bars(A.ax, [i + 1], [v], c, width=0.6) for i, (v, c) in enumerate(zip(vals, cols))])
        nm = VGroup(*[label(t, font_size=11, color=c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.08) for i, (t, c) in
                      enumerate(zip([r"sparse", r"PCA", r"random"], cols))])
        rows = rows_of([
            (r"the same patches, \ two codes: \ sparse units are small and oriented; \ principal components are "
             r"global ripples, \ like a Fourier basis", WHITE),
            (rf"share of each unit's energy in its strongest 3 by 3 spot: \ {vals[0]:.2f} sparse, \ {vals[1]:.2f} "
             rf"for components, \ {vals[2]:.2f} for random patterns", GOOD),
            (r"PCA only decorrelates; \ sparseness asks for independent causes, \ and edges are what images are "
             r"made of", MODEL),
        ], 12.4, 19, 0.3).move_to([0, -2.4, 0])
        tag = psyche_tag(r"\texttt{efficient.localization}").to_corner(UR, buff=0.3)
        with self.voiceover(
            "Is it the sparseness that matters? Compare two codes for the same patches. <bookmark mark='a'/> The "
            "sparse units are small and oriented. The principal components, which only decorrelate, are global "
            "ripples, like a Fourier basis. <bookmark mark='b'/> Measure how much of each unit's energy sits in its "
            "strongest three by three spot. The sparse code: about zero point eight. The components and random "
            "patterns: about zero point two five. <bookmark mark='c'/> Decorrelation alone gives ripples. Sparseness "
            "asks for independent causes, and edges are what images are made of."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(left), FadeIn(ll), FadeIn(right), FadeIn(rl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(A), FadeIn(nm), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bs],
                                                                            lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def caveats(self):
        chips_section(self, r"How far it goes", [
            (r"replicated", r"independent component analysis gives the same filters (Bell and Sejnowski, \ 1997); \ "
                            r"so do many later methods, \ and deep networks' first layers", GOOD),
            (r"other senses", r"the same objective on sounds gives cochlear-like filters (Lewicki, \ 2002)", MODEL),
            (r"not exact", r"measured V1 fields are rounder and more varied than the model's (Ringach, \ 2002)", AUTH),
            (r"Psyche's images", r"synthetic dead leaves, \ not a licensed photograph set: \ the result is the "
                                 r"same in kind, \ and the fields are smaller", YOU),
        ], "How far does it go? <bookmark mark='a'/> It's replicated. Independent component analysis gives the same "
           "filters, as Anthony Bell and Terrence Sejnowski showed in 1997, and so do many later methods, including "
           "the first layers of deep networks. <bookmark mark='b'/> The same objective applied to sounds gives "
           "filters like the cochlea's, as Michael Lewicki showed in 2002. <bookmark mark='c'/> But it isn't exact. "
           "Measured V1 fields are rounder and more varied than the model's, as Dario Ringach found. "
           "<bookmark mark='d'/> And a note on Psyche: its images are synthetic dead leaves, not a licensed set of "
           "photographs. The result is the same in kind, and the fields come out smaller.")
