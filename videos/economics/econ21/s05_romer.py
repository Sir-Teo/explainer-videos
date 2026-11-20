from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Romer(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Romer's economy", r"If ideas are invented for profit, \ how fast does the economy grow?",
             "Chapter four. Romer's economy.", lit={1990: r"Romer"}, scale=("firm", "nation"), horizon=("decades",))
        self.sectors()
        self.derive()
        self.path_()
        self.scale()

    def sectors(self):
        boxes = VGroup()
        specs = [(r"research", r"researchers $L_A$ \\ invent designs: \\ $\dot A = \delta L_A A$", RESEARCH),
                 (r"intermediates", r"one monopolist per design \\ rents capital, \\ prices at a markup $1/\alpha$",
                  IDEA),
                 (r"final goods", r"workers $L_Y$ and \\ every design: \\ $Y = L_Y^{1-\alpha}\sum_i x_i^{\alpha}$",
                  OUTPUT)]
        for name, body, col in specs:
            b = RoundedRectangle(width=3.6, height=2.3, corner_radius=0.15, stroke_color=col, stroke_width=3)
            t = VGroup(label(name, font_size=26, color=col), label(body, font_size=19, color=GREY_A)).arrange(
                DOWN, buff=0.2).move_to(b)
            boxes.add(VGroup(b, t))
        boxes.arrange(RIGHT, buff=0.9).move_to(UP * 0.4)
        arrows = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), buff=0.1, color=GREY_B),
                        Arrow(boxes[1].get_right(), boxes[2].get_left(), buff=0.1, color=GREY_B))
        al = VGroup(label(r"patents", font_size=17, color=GREY_B).next_to(arrows[0], UP, buff=0.08),
                    label(r"machines", font_size=17, color=GREY_B).next_to(arrows[1], UP, buff=0.08))
        note_ = label(r"the prize for invention: \ the monopoly profits of a design, \ for ever", font_size=23,
                      color=E.ACCENT).to_edge(DOWN, buff=0.8)
        tag = published_tag(r"Romer, JPE 98(5) (1990): \ S71--S102", corner=DR, font_size=12)
        with self.voiceover(
            "Romer's economy has three sectors. <bookmark mark='a'/> In research, people invent new designs. Each "
            "researcher adds ideas in proportion to the ideas already known, so the stock of designs, A, grows at "
            "delta times the number of researchers. <bookmark mark='b'/> Each design is patented, and one firm makes "
            "the machine it describes. That firm is a monopolist and charges a markup over its cost. "
            "<bookmark mark='c'/> Final goods are made by workers using every design there is, each with "
            "diminishing returns, so more designs mean more output from the same inputs. <bookmark mark='d'/> The "
            "prize for invention is the stream of monopoly profits a design earns. Without the monopoly, nobody "
            "would invent."
        ) as vo:
            self.play(FadeIn(boxes[0]), FadeIn(tag))
            vo.wait_until("b")
            self.play(GrowArrow(arrows[0]), FadeIn(al[0]), FadeIn(boxes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(arrows[1]), FadeIn(al[1]), FadeIn(boxes[2]))
            vo.wait_until("d")
            self.play(FadeIn(note_))
        self.clear_scene()

    def derive(self):
        r = load("romer")
        pr = r["params"]
        rows = VGroup(
            MathTex(r"\pi = \alpha(1-\alpha)\frac{Y}{A}, \qquad V = \frac{\pi}{r}", font_size=40),
            MathTex(r"\underbrace{\delta A\, V}_{\text{a researcher earns}} \;=\; "
                    r"\underbrace{(1-\alpha)\frac{Y}{L_Y}}_{\text{a worker earns}} \;\Rightarrow\; L_Y = "
                    r"\frac{r}{\alpha\delta}", font_size=38),
            MathTex(r"g = \delta L_A = \delta (L - L_Y), \qquad r = \rho + \theta g", font_size=40),
            MathTex(r"g = \frac{\alpha\,\delta L - \rho}{\alpha + \theta}", font_size=56, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.5)
        notes = VGroup(
            label(r"a design's profit, \ and its value at interest rate $r$", font_size=19, color=GREY_B),
            label(r"people move between research and production until the pay is equal", font_size=19,
                  color=GREY_B),
            label(r"the Euler equation of Part 7 sets the interest rate", font_size=19, color=GREY_B),
        )
        for n_, row in zip(notes, rows[:3]):
            n_.next_to(row, DOWN, buff=0.08)
        res = label(rf"island: \ $\delta = {pr['delta']:g}$, \ $\alpha = {pr['alpha']:g}$, \ $\rho = {pr['rho']:g}$, "
                    rf"\ $\theta = {pr['theta']:g}$: \ $g = {pc(r['g'])}$, \ research share {pc(r['share_research'], 0)}, "
                    rf"\ $r = {pc(r['r'])}$", font_size=22, color=IDEA).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The balanced path takes four lines. <bookmark mark='a'/> A design's monopolist earns a profit "
            "proportional to output per design, and a patent is worth that profit divided by the interest rate. "
            "<bookmark mark='b'/> People choose between research and production. A researcher finds delta A designs "
            "a year, each worth V; a production worker earns the marginal product of labour. Setting the two equal "
            "fixes the number of production workers: the interest rate over alpha delta. "
            "<bookmark mark='c'/> Growth is delta times the researchers, everyone not in production, and the "
            "interest rate comes from the Euler equation. <bookmark mark='d'/> Put together: growth equals alpha "
            "delta L, less impatience, over alpha plus theta. <bookmark mark='e'/> On the island, a fifth of the "
            f"people do research and the economy grows {100 * r['g']:.0f} percent a year, with no help from "
            "anywhere: growth is endogenous."
        ) as vo:
            self.play(Write(rows[0]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Write(rows[1]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Write(rows[2]), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(Write(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(res))
        self.clear_scene()

    def path_(self):
        r = load("romer")
        t = np.array(r["t"], float)
        A = np.array(r["A"])
        ax = plane([0, 80], [0, np.log10(6)], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.0, y_length=4.8,
                   xticks=[0, 20, 40, 60, 80], yticks=[0, np.log10(2), np.log10(4)], xlabel=r"years",
                   ylabel=r"designs $A$ \ (log)", yfmt=lambda v: f"{10 ** v:.0f}", font_size=16)
        line = path(ax, t, np.log10(A), color=IDEA, width=4, smooth=False)
        side = VGroup(
            label(r"too little research:", font_size=24, color=E.ACCENT),
            label(r"an inventor keeps a markup, \\ not the whole value of the design", font_size=19, color=GREY_A),
            label(r"and none of the help her idea \\ gives to the next inventor", font_size=19, color=GREY_A),
            label(r"a planner would put more \\ people into research", font_size=19, color=RESEARCH),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        with self.voiceover(
            f"Here is the island's stock of designs on that path: {100 * r['g']:.0f} percent a year, a straight line "
            "on a log scale. <bookmark mark='a'/> Is it enough? No. Left to the market, Romer's economy does too "
            "little research, for two reasons. <bookmark mark='b'/> An inventor collects a monopoly markup, not the "
            "whole value of what her design adds to output. <bookmark mark='c'/> And she collects nothing for the "
            "help her idea gives every future inventor, who stands on her shoulders for free. "
            "<bookmark mark='d'/> A planner who counted both would put more people into research and grow faster. "
            "That is the case for subsidizing research, and chapter fourteen puts a number on it."
        ) as vo:
            self.play(FadeIn(ax), Create(line), run_time=2.5)
            for mk, m in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(m, shift=RIGHT * 0.1))
        self.clear_scene()

    def scale(self):
        r = load("romer")
        sc = r["scale"]
        ax = plane([0, 2.1], [0, 0.07], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.0, y_length=4.8,
                   xticks=[0, 0.5, 1.0, 1.5, 2.0], yticks=[0, 0.02, 0.04, 0.06],
                   xlabel=r"size of the labour force \ (the island $= 1$)", ylabel=r"growth a year",
                   xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        line = path(ax, sc["L"], sc["g"], color=IDEA, width=4, smooth=False)
        dots = VGroup(*[Dot(ax.ax.c2p(float(k), v["g"]), radius=0.08, color=WHITE) for k, v in r["sizes"].items()])
        side = VGroup(
            label(r"the scale effect", font_size=26, color=E.ACCENT),
            label(r"twice the people, \\ more than twice the growth", font_size=20, color=GREY_A),
            label(rf"island $\times 2$: \ {pc(r['sizes']['2']['g'])} a year", font_size=20, color=IDEA),
            label(r"a testable prediction: \\ chapter six tests it", font_size=20, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "The formula has a striking implication. <bookmark mark='a'/> Growth rises with L, the size of the "
            "labour force: the more people, the more researchers, and with ideas non-rival, every one of them "
            "benefits everyone. <bookmark mark='b'/> Double the island's population and, in this model, its growth "
            f"rate rises from {100 * r['g']:.0f} to about {100 * r['sizes']['2']['g']:.0f} percent a year, for ever. "
            "<bookmark mark='c'/> That is the scale effect, and it is a prediction the twentieth century tested."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(line), FadeIn(side[1]), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in dots], lag_ratio=0.3), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
