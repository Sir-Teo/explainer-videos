from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

LINES = [
    r"A seller offers quality $q$ at cost $q^2/2$. \ A buyer of type $\theta$ who buys $q$ for $t$ gets "
    r"$\theta q - t$, \ or 0 by not buying. \ The seller knows the distribution of $\theta$ but not the buyer's "
    r"type, \ and offers a menu $\{(q, t)\}$.",
    r"(a) \ $\theta = 1$ with probability $\tfrac23$ and $\theta = 2$ with probability $\tfrac13$. \ Find the "
    r"optimal menu and the high type's information rent. \quad (14 marks)",
    r"(b) \ $\theta$ is uniform on $[1, 2]$. \ Find $q(\theta)$ and $t(\theta)$. \quad (11 marks)",
]


class Micro4(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Micro: \ screening", r"How should a seller design a menu for buyers it cannot tell apart?",
             "Question four. Microeconomics: screening.", lit={1978: r"Mussa and Rosen", 1984: r"Maskin and Riley"},
             scale=("person", "firm"), horizon=("a year",))
        self.statement()
        self.two()
        self.continuum()
        self.picture()
        self.marks()

    def statement(self):
        paper = exam_paper(4, "micro", r"screening", LINES).move_to(UP * 0.5)
        with self.voiceover(
            "Question four. A seller can make any quality q at a cost of q squared over two. A buyer of type theta "
            "values quality at theta per unit. The seller cannot see the type, so it offers a menu of qualities "
            "and prices, and lets each buyer choose. <bookmark mark='a'/> Part a: two types, a low type of one "
            "with probability two thirds and a high type of two. <bookmark mark='b'/> Part b: types spread "
            "uniformly between one and two. Pause, and decide which constraints bind."
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("ab", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 7.0)
        self.clear_scene()

    def two(self):
        M = load("micro4")
        tag = part_tag(4, "a", "micro")
        rows = steps([
            (r"\text{IR}_L:\ q_L - t_L \ge 0, \qquad \text{IC}_H:\ 2q_H - t_H \ge 2q_L - t_L",
             r"the two that bind: \ the low type's participation, \ the high type's incentive"),
            (r"t_L = q_L, \qquad t_H = 2q_H - q_L", r"both bind, \ so substitute"),
            (r"\Pi = \tfrac23\big(q_L - \tfrac12 q_L^2\big) + \tfrac13\big(2q_H - q_L - \tfrac12 q_H^2\big)",
             r"the seller's expected profit"),
            (rf"q_H = 2, \qquad \tfrac23\,(1 - q_L) = \tfrac13 \ \Rightarrow\ q_L = {M['q_l']:.1f}",
             r"no distortion at the top; \ the bottom is cut to shrink the high type's rent", GAIN),
            (rf"t_L = {M['t_l']:.1f}, \ \ t_H = {M['t_h']:.1f}, \ \ \text{{rent}} = (2 - 1)\,q_L = {M['rent']:.1f}, "
             rf"\ \ \Pi = {M['profit']:.2f}", r"first best: \ $q = \theta$, \ profit 1.00"),
            (r"\text{check: } q_L - t_L = 0 \ge q_H - t_H = -1.5, \qquad 2q_H - t_H = 0.5 \ge 0",
             r"the low type's incentive and the high type's participation hold"),
        ], math_size=28, buff=0.28)
        rows.move_to(DOWN * 0.1)
        box = answer_box(rows[3][0])
        with self.voiceover(
            "Part a. <bookmark mark='a'/> Four constraints, and the art is knowing which bind. The low type must be "
            "willing to buy; the high type must not want the low type's item. <bookmark mark='b'/> Both bind at "
            "the optimum: the low type pays its full value, and the high type pays its value less what it could "
            "get by pretending. <bookmark mark='c'/> Substitute, and profit depends on the two qualities alone. "
            "<bookmark mark='d'/> The high type gets the efficient quality, two: no distortion at the top. The low "
            f"type's quality is cut to {M['q_l']:.1f}, because every unit it gets raises the rent the high type can "
            f"claim. <bookmark mark='e'/> Prices {M['t_l']:.1f} and {M['t_h']:.1f}; the high type keeps a rent of "
            f"{M['rent']:.1f}; profit {M['profit']:.2f}, against 1.00 if the seller could see types. <bookmark "
            "mark='f'/> And check the two constraints you ignored: they hold."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if mk == "d":
                    self.play(Create(box))
        self.clear_scene()

    def continuum(self):
        M = load("micro4")
        tag = part_tag(4, "b", "micro")
        rows = steps([
            (r"U(\theta) = \theta q(\theta) - t(\theta), \qquad U'(\theta) = q(\theta), \qquad U(1) = 0",
             r"the envelope theorem, \ and the lowest type's participation"),
            (r"\Pi = \int_1^2 \Big[\Big(\theta - \frac{1 - F(\theta)}{f(\theta)}\Big) q - \frac{q^2}{2}\Big]"
             r" f\, d\theta",
             r"integrate the rent by parts"),
            (r"q(\theta) = \theta - (2 - \theta) = 2\theta - 2",
             r"maximize pointwise: \ virtual type times $q$, \ less cost", GAIN),
            (r"t(\theta) = \theta\,q(\theta) - \int_1^\theta q(s)\,ds = \theta^2 - 1",
             r"the price that makes each type choose its own item"),
            (rf"\Pi = {M['profit_c']:.3f} \quad (\text{{first best }} {M['first_best_c']:.3f})",
             r"and $q$ increases with $\theta$, \ so the menu is incentive compatible"),
        ])
        rows.move_to(DOWN * 0.1)
        box = answer_box(rows[2][0])
        with self.voiceover(
            "Part b. <bookmark mark='a'/> With a continuum, use the envelope theorem: a buyer's surplus rises with "
            "type at the rate of the quality it buys, and the lowest type gets nothing. <bookmark mark='b'/> "
            "Integrating the rents by parts turns profit into virtual surplus: quality times the virtual type, "
            "theta minus one minus F over f, less cost. <bookmark mark='c'/> Maximize type by type: quality is "
            "two theta minus two, efficient only at the top, zero at the bottom. <bookmark mark='d'/> Prices follow "
            "from the envelope condition: theta squared minus one. <bookmark mark='e'/> Profit is two thirds, "
            "against seven sixths if types were visible; and since quality rises with type, no one wants another "
            "type's item."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, r_ in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if mk == "c":
                    self.play(Create(box))
        self.clear_scene()

    def picture(self):
        M = load("micro4")
        th, q, rent = np.array(M["theta"]), np.array(M["q"]), np.array(M["rent_c"])
        axl = plane([1, 2], [0, 2.2], center=LEFT * 3.3 + DOWN * 0.4, x_length=5.2, y_length=4.6,
                    xticks=[1, 1.5, 2], yticks=[0, 1, 2], xlabel=r"type $\theta$", ylabel=r"quality $q$",
                    xfmt=lambda x: f"{x:.1f}", yfmt=lambda y: f"{y:.0f}", font_size=15)
        fb = path(axl, th, th, GREY_B, 2.4)
        sb = path(axl, th, q, MICRO, 3.0)
        two = VGroup(dot(axl, 1, M["q_l"], EST), dot(axl, 2, M["q_h"], EST))
        two_fb = dot(axl, 1, 1, GREY_B)
        axr = plane([1, 2], [0, 1.2], center=RIGHT * 2.8 + DOWN * 0.4, x_length=4.6, y_length=4.6,
                    xticks=[1, 1.5, 2], yticks=[0, 0.5, 1.0], xlabel=r"type $\theta$",
                    ylabel=r"information rent $U(\theta)$", xfmt=lambda x: f"{x:.1f}", yfmt=lambda y: f"{y:.1f}",
                    font_size=15)
        rl = path(axr, th, rent, GAIN, 3.0)
        rarea = band(axr, th, np.zeros_like(th), rent, GAIN, 0.2)
        key = VGroup(label(r"grey: \ first best, \ $q = \theta$", font_size=18, color=GREY_B),
                     label(r"blue: \ the continuum, \ $2\theta - 2$", font_size=18, color=MICRO),
                     label(r"gold: \ the two-type menu", font_size=18, color=EST)).arrange(DOWN, aligned_edge=LEFT,
                                                                                           buff=0.12)
        key.next_to(axl, UP, buff=0.15)
        with self.voiceover(
            "The picture. <bookmark mark='a'/> In grey, the quality each type would get if the seller could see "
            "it. <bookmark mark='b'/> In blue, the screening menu: below it everywhere except the top, and zero at "
            "the bottom. <bookmark mark='c'/> In gold, the two-type answer, the same shape in two points. <bookmark "
            "mark='d'/> On the right, the rent each type keeps, theta minus one squared: the price of the "
            "seller's ignorance, paid to everyone but the lowest type."
        ) as vo:
            self.play(FadeIn(axl), FadeIn(key))
            vo.wait_until("a")
            self.play(Create(fb), FadeIn(two_fb))
            vo.wait_until("b")
            self.play(Create(sb), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(two))
            vo.wait_until("d")
            self.play(FadeIn(axr), FadeIn(rarea), Create(rl), run_time=1.5)
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"binding the wrong pair: \ the high type's participation and the low type's incentive are slack",
            r"distorting the top: \ the high type's quality is efficient",
            r"in the continuum, \ transfers without the rent integral",
            r"never checking that $q(\theta)$ increases: \ if the virtual type does not, \ the menu must pool",
        ]).move_to(UP * 0.2)
        take = label(r"efficiency at the top, \ distortion below, \ rent to everyone but the bottom", font_size=23,
                     color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> Binding the wrong pair of constraints. <bookmark "
            "mark='b'/> Distorting the top. <bookmark mark='c'/> Writing transfers without the rent. <bookmark "
            "mark='d'/> And never checking that quality rises with type; when the virtual type does not, the "
            "answer pools types together, and an answer that misses that loses the hardest marks. <bookmark "
            "mark='e'/> The idea to keep, from Parts ten, thirteen and fourteen: efficiency at the top, distortion "
            "below, a rent for everyone but the bottom."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()
