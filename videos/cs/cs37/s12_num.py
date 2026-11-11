from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (DATA, HEAD, KERN, LAM, NO, PART, WIN, YES, axes, box, grid_table, load, trace)


class Num(VoiceoverScene):
    def construct(self):
        self.card()
        self.problem()
        self.dual()
        self.ascent()
        self.meaning()

    def card(self):
        card = chapter_card(11, r"TCP as optimization", r"What is congestion control maximizing?",
                            lit=(1997, 1999), extra=((1997, r"Kelly: \ charging and rate control"),
                                                     (1998, r"Kelly, Maulloo and Tan"),
                                                     (1999, r"Low and Lapsley")), part=PART)
        with self.voiceover("Chapter eleven. TCP as an optimization algorithm."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def network(self, center):
        n = load("num")
        A = Dot([-2.4, 0, 0], radius=0.1, color=GREY_B)
        B = Dot([0, 0, 0], radius=0.1, color=GREY_B)
        C = Dot([2.4, 0, 0], radius=0.1, color=GREY_B)
        l1 = Line(A, B, color=WIN, stroke_width=6)
        l2 = Line(B, C, color=WIN, stroke_width=6)
        t1 = label(r"link 1, \ $c = 1$", font_size=17, color=WIN).next_to(l1, DOWN, buff=0.12)
        t2 = label(r"link 2, \ $c = 1$", font_size=17, color=WIN).next_to(l2, DOWN, buff=0.12)
        long = CurvedArrow(A.get_center() + UP * 0.25, C.get_center() + UP * 0.25, angle=-0.6, color=KERN)
        a = Arrow(A.get_center() + UP * 0.25 + DOWN * 0.0, B.get_center() + UP * 0.25, buff=0.05, color=DATA,
                  stroke_width=3).shift(UP * 0.25)
        b = Arrow(B.get_center() + UP * 0.25, C.get_center() + UP * 0.25, buff=0.05, color=LAM,
                  stroke_width=3).shift(UP * 0.25)
        ll = label(r"long flow", font_size=17, color=KERN).next_to(long, UP, buff=0.05)
        al = label(r"$a$", font_size=18, color=DATA).next_to(a, UP, buff=0.02)
        bl = label(r"$b$", font_size=18, color=LAM).next_to(b, UP, buff=0.02)
        g = VGroup(l1, l2, A, B, C, t1, t2, long, a, b, ll, al, bl).move_to(center)
        _ = n
        return g

    def problem(self):
        head = label(r"Kelly's question", font_size=36).to_edge(UP, buff=0.3)
        net = self.network([0, 1.3, 0]).scale(1.5)
        eqs = VGroup(
            MathTex(r"\max_{x \ge 0}\ \sum_r U_r(x_r) \qquad \text{subject to}\quad \sum_{r \ni \ell} x_r \le "
                    r"c_\ell \ \text{ for every link } \ell", font_size=34, color=WHITE),
            MathTex(r"U(x) = \log x \ \Rightarrow\ \textbf{proportional fairness}", font_size=32, color=YES),
        ).arrange(DOWN, buff=0.35).next_to(net, DOWN, buff=0.55)
        note1 = wrapped_label(r"each flow $r$ has a utility $U_r$ of its rate; \ each link a capacity; \ choose all "
                              r"rates at once to maximize the total", 12.4, font_size=21,
                              color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So far we have described congestion control as a set of rules. In 1997 and 1998 Frank Kelly, a "
            "mathematician at Cambridge, asked what problem those rules are solving. <bookmark mark='a'/> Take a "
            "network: here, two links in a row, each of capacity one, a long flow that crosses both, and two short "
            "flows that use one each. <bookmark mark='b'/> Give each flow a utility, a concave function of its rate "
            "saying how much it values bandwidth, and choose all the rates at once to maximize total utility, "
            "subject to no link carrying more than its capacity. This is network utility maximization. "
            "<bookmark mark='c'/> With logarithmic utilities, the solution has a name: proportional fairness. A "
            "rate is increased only if the percentage gain to some flows outweighs the percentage loss to others."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(net))
            vo.wait_until("b")
            self.play(Write(eqs[0]), FadeIn(note1))
            vo.wait_until("c")
            self.play(FadeIn(eqs[1]))
        self.wait(0.4)
        self.clear_scene()

    def dual(self):
        head = label(r"Prices on links", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            wrapped_label(r"Attach a price $p_\ell \ge 0$ to each link's constraint \ (the Lagrange multipliers of "
                          r"Part 23's duality):", 12.4, font_size=22, color=WHITE),
            MathTex(r"L(x, p) = \sum_r \log x_r - \sum_\ell p_\ell\Big(\sum_{r \ni \ell} x_r - c_\ell\Big)",
                    font_size=34, color=HEAD),
            wrapped_label(r"\textbf{each flow}, \ seeing only the total price $q_r$ on its own path, \ maximizes "
                          r"$\log x_r - q_r x_r$:", 12.4, font_size=22, color=DATA),
            MathTex(r"x_r = \frac{1}{q_r}, \qquad q_r = \sum_{\ell \in r} p_\ell", font_size=36, color=DATA),
            wrapped_label(r"\textbf{each link}, \ seeing only its own load, \ raises its price when overloaded and "
                          r"lowers it when not:", 12.4, font_size=22, color=WIN),
            MathTex(r"p_\ell \leftarrow \Big[\,p_\ell + \gamma\Big(\sum_{r \ni \ell} x_r - c_\ell\Big)\Big]^+",
                    font_size=36, color=WIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(head, DOWN, buff=0.35)
        for k in (1, 3, 5):
            steps[k].set_x(0)
        with self.voiceover(
            "The problem decomposes, by the duality of Part 23. <bookmark mark='a'/> Attach a price to each link's "
            "capacity constraint: a Lagrange multiplier. <bookmark mark='b'/> The Lagrangian adds, for each link, "
            "its price times its overload. <bookmark mark='c'/> Now look at one flow. Its part of the Lagrangian "
            "is the log of its rate minus its rate times the total price along its path. It can maximize that "
            "alone: <bookmark mark='d'/> its best rate is one over the path price. <bookmark mark='e'/> And look at "
            "one link. It needs to know only its own load: if more is offered than it can carry, it raises its "
            "price a little; if less, it lowers it. <bookmark mark='f'/> This is gradient ascent on the dual "
            "problem. Every flow and every link acts on local information only, and together they converge to the "
            "global optimum."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcdef", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()

    def ascent(self):
        n = load("num")
        two = n["two"]
        head = label(r"Dual ascent, \ running", font_size=36).to_edge(UP, buff=0.3)
        hist = two["history"]
        g = axes([0, hist[-1]["iter"], 500], [0, 1.4, 0.5], x_length=6.6, y_length=3.6, x_label=r"iterations",
                 y_label=r"rate", xticks=range(0, hist[-1]["iter"] + 1, 500), yticks=(0.5, 1.0),
                 fx=lambda v: f"{v:,.0f}").move_to([-3.0, -0.4, 0])
        ax = g.ax
        cols = {"long": KERN, "a": DATA, "b": LAM}
        trs = VGroup(*[trace(ax, [(h["iter"], h["x"][k]) for h in hist], cols[k], width=2.6) for k in ("long", "a")])
        tl = VGroup(label(r"long flow", font_size=17, color=KERN).next_to(trs[0].get_end(), UP, buff=0.08),
                    label(r"each short flow", font_size=17, color=DATA).next_to(trs[1].get_end(), UP, buff=0.08))
        for t in tl:
            t.shift(LEFT * 0.6)
        mm = two["maxmin"]
        rows = [[r"long flow", f"{two['x']['long']:.3f}", f"{mm['long']:.3f}"],
                [r"short flows, \ each", f"{two['x']['a']:.3f}", f"{mm['a']:.3f}"],
                [r"total", f"{two['total']:.3f}", f"{two['total_maxmin']:.3f}"]]
        tab = grid_table([r"", r"proportional", r"max-min"], rows, widths=[2.6, 1.9, 1.6], row_h=0.42,
                         font_size=19, mono_cols=())
        tab.move_to([3.7, 1.0, 0])
        for k in range(1, 4):
            tab.cells[k][1].set_color(YES)
            tab.cells[k][2].set_color(KERN)
        th = n["three"]
        notes = VGroup(
            wrapped_label(rf"prices settle at $p_1 = p_2 = {two['p']['L1']:.2f}$; \ the long flow pays twice, \ so "
                          r"it gets half the rate", 5.6, font_size=19, color=WHITE),
            wrapped_label(rf"three links in a row: \ long flow {th['x']['long']:.2f}, \ each short "
                          rf"{th['x']['a']:.2f} \ (max-min gives {th['maxmin']['long']:.2f} to all)", 5.6,
                          font_size=19, color=GREY_A),
            wrapped_label(r"proportional fairness charges a flow for the resources it uses; \ max-min gives every "
                          r"flow the same, \ and carries less in total", 5.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.7, -1.5, 0])
        with self.voiceover(
            "We ran it on the two-link network. <bookmark mark='a'/> The rates swing at first, as prices overshoot, "
            "and then settle: the long flow at one third, each short flow at two thirds. <bookmark mark='b'/> Both "
            "links end up full, each with price one and a half. The long flow pays both prices, so it gets half "
            "the rate of a short flow. <bookmark mark='c'/> Compare max-min fairness, which raises everyone's rate "
            "together until a link fills: it gives all three a half. Proportional fairness carries more in total, "
            "five thirds against three halves, by charging the long flow for using two links. With three links in a "
            "row, the long flow gets a quarter. Which fairness is right is a question of values, not mathematics; "
            "what the mathematics says is which one a given algorithm is computing."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(Create(trs[0]), Create(trs[1]), run_time=2.5)
            self.play(FadeIn(tl))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]), FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def meaning(self):
        head = label(r"So what is TCP doing?", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            VGroup(box(3.2, 0.7, r"link price $p_\ell$", WIN, font_size=20),
                   wrapped_label(r"the loss rate \ (Reno, \ CUBIC) \ or the queueing delay \ (Vegas, \ FAST)", 7.6,
                                 font_size=21, color=WHITE)).arrange(RIGHT, buff=0.5),
            VGroup(box(3.2, 0.7, r"$x_r = 1/q_r$", DATA, font_size=20),
                   wrapped_label(r"each flow's window responds to the price on its path", 7.6, font_size=21,
                                 color=WHITE)).arrange(RIGHT, buff=0.5),
            VGroup(box(3.2, 0.7, r"utility $U_r$", YES, font_size=20),
                   wrapped_label(r"Reno's AIMD maximizes $\sum_r -\tfrac{3}{2\,\text{RTT}_r^2 x_r}$, \ approximately: \ "
                                 r"the Mathis formula is its first-order condition, \ and RTT unfairness is "
                                 r"written into its utility", 7.6, font_size=21, color=WHITE)).arrange(RIGHT,
                                                                                                    buff=0.5),
            VGroup(box(3.2, 0.7, r"Vegas", KERN, font_size=20),
                   wrapped_label(r"keeps $\alpha$ packets queued per flow: \ exactly proportionally fair, \ $U = "
                                 r"\alpha \log x$ \ (Low, Peterson and Wang, 2002)", 7.6, font_size=21,
                                 color=WHITE)).arrange(RIGHT, buff=0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.5)
        foot = wrapped_label(r"no one designed TCP this way; \ the theory explained afterwards what the engineering "
                             r"had built, \ and now guides new designs", 12.4, font_size=21,
                             color=HEAD).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "And here is the surprise. Real TCPs are this algorithm, in disguise. <bookmark mark='a'/> The price "
            "of a link is something the flows can observe: for Reno and CUBIC, the probability that a packet is "
            "dropped; for delay-based algorithms like Vegas, the time packets spend in the queue. "
            "<bookmark mark='b'/> Each flow adjusts its rate to the total price on its path. "
            "<bookmark mark='c'/> And each algorithm turns out to maximize a particular utility. Reno's, as Steven "
            "Low, Srinivas Kunniyur and Rayadurgam Srikant worked out, is approximately minus three halves over the "
            "round trip squared times the rate: setting its derivative equal to the loss rate gives back the Mathis "
            "formula, and the unfairness to long round trips is built "
            "into the utility itself. <bookmark mark='d'/> Vegas keeps a fixed number of its own packets queued, "
            "and is exactly proportionally fair. <bookmark mark='e'/> No one designed TCP this way. The engineering "
            "came first, and a decade later the theory explained what it had built."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (NO,)
