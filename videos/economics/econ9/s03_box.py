from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403

E1881 = tables.EDGEWORTH_1881.data


def ana_curve(box, b, u, width=2.5, opacity=1.0):
    xs = np.linspace(0.05, b["X"][0], 300)
    return box.curve(xs, ge.cd_indifference(b["aA"], u, xs), color=ANA, width=width).set_stroke(opacity=opacity)


def bo_curve(box, b, u, width=2.5, opacity=1.0):
    X = b["X"]
    xs = np.linspace(0.0, X[0] - 0.05, 300)
    return box.curve(xs, X[1] - ge.cd_indifference(b["aB"], u, X[0] - xs), color=BO, width=width
                     ).set_stroke(opacity=opacity)


def u_cd(a, x):
    return a * np.log(x[0]) + (1 - a) * np.log(x[1])


class EdgeworthBox(VoiceoverScene):
    def construct(self):
        card(self, 2, r"The Edgeworth box", r"Which ways of sharing the goods can trade reach, and when does it "
             r"stop?", "Chapter two. The Edgeworth box.", lit={1881: r"Edgeworth's contract curve"})
        self.build()
        self.maps()
        self.lens()
        self.contract()

    def build(self):
        b = load("box")
        box = box_from(b, center=LEFT * 2.6 + DOWN * 0.1, width=6.2, height=5.4)
        w = Dot(box.c2p(*b["eA"]), radius=0.1, color=WHITE)
        wl = label(r"$\omega$: \ where they start", font_size=21).next_to(w, UP, buff=0.12)
        other = Dot(box.c2p(5.0, 5.0), radius=0.08, color=GREY_B)
        side = VGroup(
            label(r"Ana's bundle: \ measured from the bottom left", font_size=23, color=ANA),
            label(r"Bo's: \ from the top right, \ upside down", font_size=23, color=BO),
            label(r"each point: \ one way to share \\ 10 fish and 10 baskets", font_size=23),
            label(r"the box in this form came later, \\ from Pareto and Bowley", font_size=20, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is the picture economists draw for two people and two goods. <bookmark mark='a'/> Ana's fish are "
            "measured across from the bottom-left corner, and her coconuts up. <bookmark mark='b'/> Bo's are "
            "measured from the top-right corner, the other way round: his fish leftwards, his coconuts down. "
            "<bookmark mark='c'/> Because the box is exactly ten fish wide and ten baskets tall, every point in it "
            "is one way of sharing all the goods between them. <bookmark mark='d'/> Here is where they start: Ana "
            "with eight fish and one and a half baskets, so Bo with two fish and eight and a half. "
            "<bookmark mark='e'/> The idea is Edgeworth's, from 1881; the box in this form was drawn later, by "
            "Pareto and by Bowley."
        ) as vo:
            self.play(Create(box.frame), FadeIn(box.ticks), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(box.names[0]), FadeIn(box.names[2]), FadeIn(box.names[4]), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(box.names[1]), FadeIn(box.names[3]), FadeIn(box.names[5]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(other), FadeIn(side[2]))
            self.play(other.animate.move_to(box.c2p(2.0, 7.0)), run_time=1.2)
            self.play(FadeOut(other))
            vo.wait_until("d")
            self.play(FadeIn(w, scale=0.5), FadeIn(wl))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def maps(self):
        b = load("box")
        box = box_from(b, center=LEFT * 2.6 + DOWN * 0.1, width=6.2, height=5.4)
        w = Dot(box.c2p(*b["eA"]), radius=0.09, color=WHITE)
        ua0 = u_cd(b["aA"], b["eA"])
        ub0 = u_cd(b["aB"], b["eB"])
        A = VGroup(*[ana_curve(box, b, ua0 + d, width=2.2, opacity=0.65) for d in (-0.4, 0.4, 0.8, 1.2)])
        B = VGroup(*[bo_curve(box, b, ub0 + d, width=2.2, opacity=0.65) for d in (-0.4, 0.4, 0.8, 1.2)])
        A0, B0 = ana_curve(box, b, ua0, width=3.5), bo_curve(box, b, ub0, width=3.5)
        side = VGroup(
            label(r"Ana's indifference curves: \\ bundles she likes equally; \\ she prefers curves further up and "
                  r"right", font_size=22, color=ANA),
            label(r"Bo's: \ the same, \ seen from his corner; \\ he prefers curves further down and left",
                  font_size=22, color=BO),
            label(r"through $\omega$: \ what each has without trade", font_size=22),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.45)
        with self.voiceover(
            "Now their tastes. <bookmark mark='a'/> These are Ana's indifference curves, as in Part five: bundles "
            "she likes equally well. She bows toward her own corner, and she prefers curves further from it, up "
            "and to the right. <bookmark mark='b'/> Bo's curves are the same kind of thing seen from his corner: he "
            "prefers curves further down and to the left, nearer to Ana's corner, because they give him more. "
            "<bookmark mark='c'/> The two curves through the starting point matter most. They show what each "
            "already has, without trading at all."
        ) as vo:
            self.play(FadeIn(box), FadeIn(w))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(c) for c in A], lag_ratio=0.2), FadeIn(side[0]), run_time=2)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(c) for c in B], lag_ratio=0.2), FadeIn(side[1]), run_time=2)
            vo.wait_until("c")
            self.play(FadeOut(A), FadeOut(B), Create(A0), Create(B0), FadeIn(side[2]))
        self.clear_scene()

    def lens(self):
        b = load("box")
        box = box_from(b, center=LEFT * 2.6 + DOWN * 0.1, width=6.2, height=5.4)
        w = Dot(box.c2p(*b["eA"]), radius=0.09, color=WHITE)
        ua0 = u_cd(b["aA"], b["eA"])
        ub0 = u_cd(b["aB"], b["eB"])
        A0, B0 = ana_curve(box, b, ua0, width=3), bo_curve(box, b, ub0, width=3)
        L = lens_region(box, b)
        pts = VGroup()
        for k, v in b["play"].items():
            col = (CORE if v["on_cc"] else CC) if (v["ana_gains"] and v["bo_gains"]) else HOLD
            d = Dot(box.c2p(*v["xA"]), radius=0.08, color=col)
            pts.add(VGroup(d, label(k, font_size=20, color=col).next_to(d, UR, buff=0.05)))
        side = VGroup(
            label(r"the lens: \ every point inside \\ makes both better off than $\omega$", font_size=23,
                  color=LENS),
            label(r"trades A and B are inside", font_size=23, color=CC),
            label(r"C is below Bo's curve: \ he refuses; \\ D is below Ana's: \ she refuses", font_size=22,
                  color=HOLD),
            label(r"from A, \ a new lens: \ more to gain", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.45)
        xa = b["play"]["A"]["xA"]
        A1 = ana_curve(box, b, u_cd(b["aA"], xa), width=2.2, opacity=0.8)
        B1 = bo_curve(box, b, u_cd(b["aB"], np.subtract(b["X"], xa)), width=2.2, opacity=0.8)
        with self.voiceover(
            "Between those two curves lies a lens. <bookmark mark='a'/> Every point inside it puts Ana on a higher "
            "curve than her starting one and Bo on a higher curve than his. Any trade that lands in the lens, both "
            "will accept. <bookmark mark='b'/> Here are the trades of Play it. A and B are in the lens. "
            "<bookmark mark='c'/> C lies below Bo's starting curve, so he refuses it; D lies below Ana's, so she "
            "does. <bookmark mark='d'/> And from A, the curves through the new point make a new, smaller lens. "
            "There is still something both could gain."
        ) as vo:
            self.play(FadeIn(box), FadeIn(w), FadeIn(A0), FadeIn(B0))
            vo.wait_until("a")
            self.play(FadeIn(L), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(pts[0]), FadeIn(pts[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[2]), FadeIn(pts[3]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(A1), Create(B1), FadeIn(side[3]))
        self.clear_scene()

    def contract(self):
        b = load("box")
        box = box_from(b, center=LEFT * 2.6 + DOWN * 0.1, width=6.2, height=5.4)
        w = Dot(box.c2p(*b["eA"]), radius=0.09, color=WHITE)
        ua0 = u_cd(b["aA"], b["eA"])
        ub0 = u_cd(b["aB"], b["eB"])
        A0, B0 = ana_curve(box, b, ua0, width=2.5, opacity=0.7), bo_curve(box, b, ub0, width=2.5, opacity=0.7)
        L = lens_region(box, b, opacity=0.15)
        cc = box.curve(b["cc_x"], b["cc_y"], color=CC, width=4)
        lo, hi = b["lens"]
        xs_in = np.linspace(lo, hi, 120)
        cc_in = box.curve(xs_in, ge.contract_curve(ge.Trader((b["aA"], 1 - b["aA"]), b["eA"]),
                                                   ge.Trader((b["aB"], 1 - b["aB"]), b["eB"]), xs_in),
                          color=CORE, width=7)
        xt = np.array([4.7, float(ge.contract_curve(ge.Trader((b["aA"], 1 - b["aA"]), b["eA"]),
                                                    ge.Trader((b["aB"], 1 - b["aB"]), b["eB"]), 4.7))])
        tA = ana_curve(box, b, u_cd(b["aA"], xt), width=3)
        tB = bo_curve(box, b, u_cd(b["aB"], np.subtract(b["X"], xt)), width=3)
        tp = Dot(box.c2p(*xt), radius=0.08, color=CC)
        side = VGroup(
            label(r"where the curves just touch, \\ no swap helps one without hurting the other: \\ "
                  r"\emph{Pareto efficient}", font_size=22, color=CC),
            MathTex(r"MRS_{\text{Ana}} = MRS_{\text{Bo}}", font_size=34, color=CC),
            label(r"all such points: \ the contract curve \\ (Edgeworth's name for it, 1881)", font_size=22,
                  color=CC),
            label(r"inside the lens: \ where trade can end", font_size=23, color=CORE),
            label(r"efficient is not fair: \\ Ana's corner and Bo's are efficient too", font_size=21,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Edgeworth, Mathematical Psychics (1881), p.\ 21", corner=DR, font_size=14)
        with self.voiceover(
            "When does it stop? <bookmark mark='a'/> At a point where Ana's curve and Bo's just touch. There the "
            "lens has shrunk to nothing: any swap that raises one of them lowers the other. Such a point is called "
            "Pareto efficient, after Vilfredo Pareto. <bookmark mark='b'/> Touching curves have the same slope, so "
            "at such a point Ana and Bo value a fish at the same number of coconuts: their marginal rates of "
            "substitution are equal. <bookmark mark='c'/> The efficient points form a line from Ana's corner to "
            "Bo's, which Edgeworth named in 1881: which locus, he wrote, it is here proposed to call the contract "
            "curve. <bookmark mark='d'/> The stretch of it inside the lens is where voluntary trade can end. Where "
            "exactly depends on how they bargain. <bookmark mark='e'/> And note what efficiency doesn't say. The "
            "corners are on the contract curve too: everything to Ana, or everything to Bo, is efficient. "
            "Efficient is not the same as fair."
        ) as vo:
            self.play(FadeIn(box), FadeIn(w), FadeIn(A0), FadeIn(B0), FadeIn(L), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(tA), Create(tB), FadeIn(tp), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(cc), FadeIn(side[2]), FadeOut(tA), FadeOut(tB), run_time=2)
            vo.wait_until("d")
            self.play(Create(cc_in), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), Indicate(box.names[0], color=ANA), Indicate(box.names[1], color=BO))
        self.clear_scene()
