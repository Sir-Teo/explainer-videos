from __future__ import annotations

from videos.economics.econ56.common import *  # noqa: F403

LINES = [
    r"A continuum of households have $u(c) = c^{1-\gamma}/(1 - \gamma)$ with $\gamma = 3$, \ discount at $\beta = "
    r"0.96$, \ face idiosyncratic labour-income risk \ (log efficiency an AR(1) with persistence 0.9 and shocks of "
    r"s.d. 0.2), \ cannot borrow, \ and save only in capital, \ rented to firms with $Y = K^{0.36}$ and $\delta = "
    r"0.08$.",
    r"(a) \ Show that in a stationary equilibrium $r < \rho \equiv 1/\beta - 1$. \quad (13 marks)",
    r"(b) \ Compute the equilibrium, \ and compare its capital with an economy without income risk. "
    r"\quad (12 marks)",
]


class Macro4(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Macro: \ why $r$ lies below the rate of time preference", r"Why does a precautionary "
             r"economy hold so much capital?", "Question eight. Macroeconomics: why the interest rate lies below "
             "the rate of time preference.", lit={1993: r"Huggett", 1994: r"Aiyagari",
                                                  2000: r"Chamberlain and Wilson"},
             scale=("household", "nation"), horizon=("a decade",))
        self.statement()
        self.proof()
        self.picture()
        self.marks()

    def statement(self):
        paper = exam_paper(8, "macro", r"Aiyagari's economy", LINES).move_to(UP * 0.5)
        with self.voiceover(
            "Question eight. Households with constant relative risk aversion of three and a discount factor of "
            "0.96 face income risk they cannot insure, cannot borrow, and save in capital that firms rent. "
            "<bookmark mark='a'/> Part a: show that the equilibrium interest rate is below the rate of time "
            "preference, one over beta minus one. <bookmark mark='b'/> Part b: compute the equilibrium, and compare "
            "its capital with an economy without risk. Pause: what happens to a household's savings if the "
            "interest rate equals the rate of time preference?"
        ) as vo:
            self.play(FadeIn(paper.box), FadeIn(paper.head), FadeIn(paper[1][1]), FadeIn(paper.rows[0]))
            for mk, r_ in zip("ab", paper.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        pause(self, 7.0)
        self.clear_scene()

    def proof(self):
        M = load("macro4")
        tag = part_tag(8, "a, b", "macro")
        rows = steps([
            (r"u'(c_t) \ \ge\ \beta(1 + r)\,\mathbb{E}_t\, u'(c_{t+1}), \ \ \text{with equality unless } a_{t+1} = 0",
             r"the Euler inequality: \ the borrowing limit may bind"),
            (r"\beta(1 + r) \ge 1 \ \Rightarrow\ u'(c_t) \ge \mathbb{E}_t\, u'(c_{t+1}):\ \text{a nonnegative "
             r"supermartingale}", r"so it converges, \ almost surely"),
            (r"\text{income keeps moving} \ \Rightarrow\ c_t \text{ settles only if } a_t \to \infty",
             r"Chamberlain and Wilson: \ assets drift without bound"),
            (r"A(r) \to \infty \text{ as } r \uparrow \rho, \quad K(r) < \infty \ \Rightarrow\ r^* < \rho",
             r"supply explodes, \ demand does not: \ they cross below $\rho$", GAIN),
            (rf"r^* = {100 * M['r']:.2f}\% < \rho = {100 * M['rho']:.2f}\%, \qquad K = {M['K']:.2f} > K(\rho) = "
             rf"{M['K_rep']:.2f}", r"(b) \ precautionary saving: \ more capital than with no risk", GAIN),
        ])
        rows.move_to(DOWN * 0.1)
        boxes = [answer_box(rows[3][0]), answer_box(rows[4][0])]
        with self.voiceover(
            "Part a. <bookmark mark='a'/> Each household's Euler equation holds with equality unless it is at the "
            "borrowing limit, where it holds as an inequality. <bookmark mark='b'/> Suppose the interest rate were "
            "at least the rate of time preference. Then marginal utility is a nonnegative supermartingale, and "
            "such a process converges. <bookmark mark='c'/> But income never stops moving, so consumption can "
            "only settle down if wealth grows without bound; Gary Chamberlain and Charles Wilson proved it. "
            "<bookmark mark='d'/> So the capital households want to hold explodes as the rate approaches rho, "
            "while the capital firms want stays finite: the two curves can only cross below rho. <bookmark "
            f"mark='e'/> Part b. Solved, the equilibrium rate is {100 * M['r']:.2f} percent, against a rate of time "
            f"preference of {100 * M['rho']:.2f}; and capital is {M['K']:.2f}, against {M['K_rep']:.2f} in an "
            "economy without risk, where the rate would equal rho. Uninsurable risk makes people save more than "
            "they would like, and the economy holds more capital as a result."
        ) as vo:
            self.play(FadeIn(tag))
            for k, (mk, r_) in enumerate(zip("abcde", rows)):
                vo.wait_until(mk)
                self.play(FadeIn(r_[0], shift=RIGHT * 0.1), FadeIn(r_[1]))
                if k == 3:
                    self.play(Create(boxes[0]))
                if k == 4:
                    self.play(Create(boxes[1]))
        self.clear_scene()

    def picture(self):
        M = load("macro4")
        rs, sup, dem = np.array(M["rs"]), np.array(M["supply"]), np.array(M["demand"])
        ax = plane([0, 40], [-0.012, 0.05], center=LEFT * 1.4 + DOWN * 0.3, x_length=8.6, y_length=5.4,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 0.02, 0.04], xlabel=r"capital $K$",
                   ylabel=r"interest rate $r$", xfmt=lambda x: f"{x:.0f}",
                   yfmt=lambda y: f"{100 * y:.0f}\\%" if y else "0", font_size=15)
        rho = DashedLine(ax.ax.c2p(0, M["rho"]), ax.ax.c2p(40, M["rho"]), color=GREY_B, stroke_width=2)
        rl = label(rf"$\rho = {100 * M['rho']:.2f}\%$", font_size=18, color=GREY_B).next_to(ax.ax.c2p(40, M["rho"]),
                                                                                         RIGHT, buff=0.1)
        keep = sup <= 40
        sl = path(ax, sup[keep], rs[keep], MACRO, 3.0, smooth=True)
        dl = path(ax, dem, rs, MICRO, 3.0)
        eq = dot(ax, M["K"], M["r"], GAIN)
        rep = dot(ax, M["K_rep"], M["rho"], WHITE)
        side = VGroup(
            label(r"orange: \ what households save", font_size=19, color=MACRO),
            label(r"blue: \ what firms demand", font_size=19, color=MICRO),
            label(rf"green: \ equilibrium, \\ $r = {100 * M['r']:.2f}\%$, \ $K = {M['K']:.2f}$", font_size=19,
                  color=GAIN),
            label(rf"white: \ no risk, \\ $r = \rho$, \ $K = {M['K_rep']:.2f}$", font_size=19, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"computed: \ Part 52's Aiyagari economy", corner=DR, font_size=13)
        with self.voiceover(
            "The picture, Aiyagari's own. <bookmark mark='a'/> The capital households want to hold rises with "
            "the interest rate, and bends up toward the dashed line at rho, which it never crosses. <bookmark "
            "mark='b'/> The capital firms want falls with the rate. <bookmark mark='c'/> They cross below rho. "
            "<bookmark mark='d'/> Without risk, supply would be a horizontal line at rho, and capital would be "
            "where demand meets it."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(rho), FadeIn(rl), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(sl), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(dl), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(rep), FadeIn(side[3]))
        self.clear_scene()

    def marks(self):
        mc = marks_card([
            r"writing $\beta(1 + r) = 1$ from a representative household's Euler equation",
            r"the Euler equation without the inequality at the borrowing limit",
            r"holding the wage fixed as $r$ changes: \ firms pay $w(r)$, \ and households' income moves with it",
            r"`assets grow without bound' with no reason: \ name the convergence argument",
        ]).move_to(UP * 0.2)
        take = label(r"uninsurable risk and a borrowing limit: \ more saving, \ more capital, \ a lower rate",
                     font_size=23, color=E.ACCENT).next_to(mc, DOWN, buff=0.45)
        with self.voiceover(
            "Where marks are lost. <bookmark mark='a'/> Writing the representative household's steady state, "
            "beta times one plus r equals one. <bookmark mark='b'/> Dropping the inequality at the limit. "
            "<bookmark mark='c'/> Holding the wage fixed as the rate changes. <bookmark mark='d'/> And asserting "
            "that assets explode without saying why. <bookmark mark='e'/> The idea to keep, from Part fifty-two: "
            "uninsurable risk and a borrowing limit mean more saving, more capital and a lower interest rate."
        ) as vo:
            self.play(FadeIn(mc.box), FadeIn(mc.head))
            for mk, r_ in zip("abcd", mc.rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(take, shift=UP * 0.1))
        self.clear_scene()
