from __future__ import annotations

from videos.psychology.psych45.common import *  # noqa: F403


class Info(VoiceoverScene):
    def construct(self):
        self.card()
        self.derive()
        self.lsat()

    def card(self):
        card = chapter_card(5, r"Information", r"Where does an item tell us the most?", lit={1980: r"Lord"},
                            part=PART, scale=("person",), marr=("what", "how"))
        with self.voiceover("Chapter five. Information."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def derive(self):
        head = heading(r"Fisher information, \ item by item")
        eqs = VGroup(
            MathTex(r"I_i(\theta) = a_i^2\, P_i(\theta)\,\big(1 - P_i(\theta)\big)", font_size=36, color=MODEL),
            MathTex(r"I(\theta) = \sum_i I_i(\theta), \qquad \mathrm{SE}(\hat\theta) \approx \frac{1}{\sqrt{I(\theta)}}",
                    font_size=36, color=GOOD),
        ).arrange(DOWN, buff=0.4).move_to([-3.3, 1.6, 0])
        A = axes([-4, 4], [0, 1.6], x_length=5.6, y_length=2.6, xticks=[-4, -2, 0, 2, 4], yticks=[0, 0.5, 1, 1.5],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"ability $\theta$", ylabel=r"information",
                 center=[-3.3, -1.4, 0], font_size=13)
        th = np.linspace(-4, 4, 200)
        cols = (SYMP, PERSON, GOOD)
        pars = ((1.0, -1.5), (2.5, 0.0), (1.0, 1.5))
        cs = VGroup(*[curve(A.ax, th, a ** 2 * (1 / (1 + np.exp(-a * (th - b)))) * (1 - 1 / (1 + np.exp(-a * (th - b)))),
                            c) for (a, b), c in zip(pars, cols)])
        rows = rows_of([
            (r"an item's information is the Fisher information about $\theta$ in one answer (Part 4's precision, \ "
             r"one item at a time)", WHITE),
            (r"it peaks where the item's difficulty meets the person's ability, \ at height $a^2/4$: \ a steep item "
             r"informs a lot, \ in a narrow range", PERSON),
            (r"information adds across items, \ so a test can be designed: \ put the information where the decisions "
             r"are", GOOD),
            (r"with guessing, \ information falls for low abilities: \ a right answer might be luck", AUTH),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        with self.voiceover(
            "How much does one answer tell us? <bookmark mark='a'/> An item's information is the Fisher information "
            "about ability in a single answer: discrimination squared, times P, times one minus P. "
            "<bookmark mark='b'/> It peaks where the item's difficulty meets the person's ability, at a height of a "
            "squared over four. A steep item informs a lot, in a narrow range. <bookmark mark='c'/> Information adds "
            "across items, and the standard error is one over its square root. So a test can be designed: put the "
            "information where the decisions are. <bookmark mark='d'/> With guessing, information falls for low "
            "abilities, because a right answer might be luck."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eqs[0]), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(cs[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cs[1]), Create(cs[2]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(eqs[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def lsat(self):
        d = load("info")
        head = heading(r"What five easy items can measure")
        A = axes([-6, 4], [0, 0.7], x_length=5.6, y_length=2.4, xticks=[-6, -4, -2, 0, 2, 4], yticks=[0, 0.3, 0.6],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"ability $\theta$",
                 ylabel=r"test information", center=[-3.3, 1.0, 0], font_size=13)
        B = axes([-6, 4], [0, 4], x_length=5.6, y_length=1.8, xticks=[-6, -4, -2, 0, 2, 4], yticks=[0, 2, 4],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"ability $\theta$",
                 ylabel=r"standard error", center=[-3.3, -2.0, 0], font_size=13)
        ti = curve(A.ax, d["th"], d["test"], MODEL, stroke_width=4)
        se = curve(B.ax, d["th"], np.minimum(d["se"], 4), AUTH, stroke_width=4)
        k = int(np.argmax(d["test"]))
        rows = rows_of([
            (rf"the LSAT's five items give most information at $\theta \approx {d['th'][k]:.1f}$, \ far below the "
             rf"average candidate", MODEL),
            (rf"even there, \ the information is only {d['test'][k]:.2f}: \ a standard error of at least "
             rf"{d['se'].min():.1f}, \ more than the spread of the people", AUTH),
            (r"five items can sort a crowd roughly, \ but cannot place one person precisely", WHITE),
            (r"the cure is more items where they are needed: \ which is what an adaptive test does", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{irt.info}; \ the LSAT's two-parameter fit")
        with self.voiceover(
            "Now the law-school items. <bookmark mark='a'/> Their test information peaks near minus one point eight, "
            "far below the average candidate. <bookmark mark='b'/> And even at its peak it's only about zero point "
            "six: a standard error of at least one point three, more than the spread of the people being measured. "
            "<bookmark mark='c'/> Five items can sort a crowd roughly, but can't place one person precisely. "
            "<bookmark mark='d'/> The cure is more items where they're needed. That's what an adaptive test does."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(B))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Create(ti))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(se))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
