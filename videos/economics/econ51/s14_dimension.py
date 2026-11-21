from __future__ import annotations

from videos.economics.econ51.common import *  # noqa: F403

TENSOR = "#9AA3B2"
SMOL = "#C9A0FF"


def _big(n):
    n = int(n)
    if n >= 10 ** 9:
        e = int(np.floor(np.log10(n)))
        return rf"${n / 10 ** e:.1f} \times 10^{{{e}}}$"
    return f"{n:,}".replace(",", "{,}")


class Dimension(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The curse of dimensionality", r"What happens when the state has many parts?",
             "Chapter twelve. The curse of dimensionality.", lit={1957: r"Bellman", 1963: r"Smolyak",
                                                                 2004: r"Krueger and Kubler"},
             scale=("nation", "world"), horizon=("a century",))
        self.curse()
        self.counts()
        self.accuracy()

    def curse(self):
        rows = VGroup(
            label(r"one state, \ 5 points: \ 5", font_size=26, color=WHITE),
            label(r"capital and productivity: \ 25", font_size=26, color=WHITE),
            label(r"+ two income states and a price: \ 625", font_size=26, color=WHITE),
            label(r"ten states: \ 9,765,625".replace(",", "{,}"), font_size=26, color=ERR),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to(LEFT * 1.0)
        quote = label(r"Bellman (1957): \ ``the curse of dimensionality''", font_size=22, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        side = label(r"5 points \\ in each \\ direction", font_size=22, color=GREY_A).to_edge(RIGHT, buff=0.8)
        with self.voiceover(
            "Every method so far had a state with one or two parts: capital, or assets and income. Real models "
            "have more. <bookmark mark='a'/> With five grid points in one direction, a grid has five points. "
            "<bookmark mark='b'/> Add productivity, and it has twenty-five. <bookmark mark='c'/> Add two more "
            "parts and it has six hundred and twenty-five. <bookmark mark='d'/> With ten parts, nearly ten "
            "million, and that with only five points in each direction, far too coarse to be accurate. Bellman "
            "named the problem himself in 1957: the curse of dimensionality."
        ) as vo:
            self.play(FadeIn(quote), FadeIn(side))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def counts(self):
        D = load("dimension")["counts"]
        d = np.array(D["d"])
        ax = plane([0, 21], [0, 15], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.8, y_length=4.6,
                   xticks=[1, 5, 10, 15, 20], yticks=[0, 3, 6, 9, 12, 15], xlabel=r"parts of the state",
                   ylabel=r"grid points, \ $\log_{10}$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        ten = path(ax, d, np.log10(D["tensor5"]), TENSOR, 2.8, smooth=False)
        smo = path(ax, d, np.log10(D["smolyak2"]), SMOL, 2.8, smooth=False)
        side = VGroup(
            label(r"grey: \ every combination \\ of 5 points", font_size=18, color=TENSOR),
            label(r"purple: \ Smolyak's \\ sparse grid, \ level 2", font_size=18, color=SMOL),
            label(rf"20 parts: \\ {_big(D['tensor5'][-1])} \ against \ {_big(D['smolyak2'][-1])}", font_size=18,
                  color=WHITE),
            label(r"exponential \ against \ polynomial", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Smolyak (1963); \ Krueger and Kubler, \ JEDC (2004)", corner=DL, font_size=11)
        with self.voiceover(
            "The way out begins with a Russian mathematician, Sergey Smolyak, in 1963. <bookmark mark='a'/> A full "
            "grid takes every combination of points in every direction, so its size multiplies with each new "
            "part: on a log scale, a straight line up. <bookmark mark='b'/> Smolyak's sparse grid keeps only the "
            "combinations that matter most for smooth functions: many points along each axis, few where several "
            "directions vary at once. Its size grows like the square of the number of parts, not exponentially. "
            f"<bookmark mark='c'/> With twenty parts: {D['smolyak2'][-1]} points, against about a hundred trillion. "
            "Dirk Krueger and Felix Kubler brought the method into economics in 2004."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ten), FadeIn(side[0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(smo), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def accuracy(self):
        D = load("dimension")
        rows = D["interp"]
        sm = [r for r in rows if r["kind"] == "smolyak"]
        tn = [r for r in rows if r["kind"] == "tensor"]
        ax = plane([0.5, 4.2], [-7, 0], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.6, y_length=4.6,
                   xticks=[1, 2, 3, 4], yticks=[-6, -4, -2, 0], xlabel=r"points used, \ $\log_{10}$",
                   ylabel=r"typical error, \ $\log_{10}$", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        cs = path(ax, [np.log10(r["points"]) for r in sm], [np.log10(r["rms"]) for r in sm], SMOL, 2.8,
                  smooth=False)
        ct = path(ax, [np.log10(r["points"]) for r in tn], [np.log10(r["rms"]) for r in tn], TENSOR, 2.8,
                  smooth=False)
        ds = VGroup(*[dot(ax, np.log10(r["points"]), np.log10(r["rms"]), SMOL, 0.08) for r in sm])
        dt = VGroup(*[dot(ax, np.log10(r["points"]), np.log10(r["rms"]), TENSOR, 0.08) for r in tn])
        side = VGroup(
            label(rf"a smooth function \\ of {D['d']} variables, \\ $e^{{-|x|^2/2}}$", font_size=18, color=WHITE),
            label(r"purple: \ Smolyak, \\ levels 1 to 4", font_size=18, color=SMOL),
            label(r"grey: \ the full grid", font_size=18, color=TENSOR),
            label(r"at equal accuracy, \\ Smolyak needs fewer \\ points; \ the saving grows \\ with the "
                  r"dimension", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        foot = label(r"beyond a few dozen dimensions: \ neural networks as the approximation \ (Part 64)",
                     font_size=19, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Does the sparse grid give up accuracy? Test it on a smooth function of four variables, whose value is "
            "known everywhere. <bookmark mark='a'/> The full grid's error falls as points are added. <bookmark "
            "mark='b'/> Smolyak's falls too, and for a given accuracy it uses fewer points: in four dimensions, "
            "roughly a half or a third as many. <bookmark mark='c'/> In ten or twenty dimensions, where the full "
            "grid cannot even be stored, the saving is what makes the problem possible at all. The price is "
            "smoothness: a kink or a strong interaction between the variables erodes the advantage. <bookmark "
            "mark='d'/> Beyond a few dozen dimensions, even sparse grids give out, and the frontier uses neural "
            "networks as the approximation, the subject of Part sixty-four."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(ct), FadeIn(dt), FadeIn(side[2]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(cs), FadeIn(ds), FadeIn(side[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()
