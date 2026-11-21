from __future__ import annotations

from videos.economics.econ63.common import *  # noqa: F403

POS = {"A": LEFT * 2.0 + UP * 1.3, "B": RIGHT * 2.0 + UP * 1.3, "C": RIGHT * 2.0 + DOWN * 1.3,
       "D": LEFT * 2.0 + DOWN * 1.3}


def bank_node(name, assets, color=BANK):
    c = Circle(radius=0.48, stroke_color=color, stroke_width=2.4, fill_color=color, fill_opacity=0.15)
    t = VGroup(label(name, font_size=28, color=WHITE), label(rf"has {assets:g}", font_size=15, color=GREY_A)).arrange(
        DOWN, buff=0.05)
    return VGroup(c, t.move_to(c))


def tiny_net(kind, n=10, r=0.8, color=BANK):
    pts = [r * np.array([np.cos(2 * PI * k / n + PI / 2), np.sin(2 * PI * k / n + PI / 2), 0]) for k in range(n)]
    dots = VGroup(*[Dot(p, radius=0.06, color=SHOCK if k == 0 else color) for k, p in enumerate(pts)])
    if kind == "ring":
        lines = VGroup(*[Line(pts[k], pts[(k + 1) % n], stroke_width=1.6, color=color) for k in range(n)])
    else:
        lines = VGroup(*[Line(pts[i], pts[j], stroke_width=0.8, color=color)
                         for i in range(n) for j in range(i + 1, n)])
    return VGroup(lines, dots)


class Banks(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Financial networks", r"When banks owe each other, \ does linking them spread a loss or "
             r"absorb it?", "Chapter eight. Financial networks.", lit={2001: r"Eisenberg and Noe",
                                                                       2015: r"Acemoglu et al."},
             scale=("firm", "world"), horizon=("a day",))
        self.clearing()
        self.contagion()
        self.lessons()

    def clearing(self):
        Bx = load("banks")["example"]
        names, L, assets, pay = Bx["names"], np.array(Bx["L"]), Bx["assets"], Bx["payments"]
        nodes = {nm: bank_node(nm, a).move_to(POS[nm] + LEFT * 2.2) for nm, a in zip(names, assets)}
        arrows = VGroup()
        tags = VGroup()
        for i, a in enumerate(names):
            for j, b in enumerate(names):
                if L[i, j] > 0:
                    s, e = nodes[a][0].get_center(), nodes[b][0].get_center()
                    u = (e - s) / np.linalg.norm(e - s)
                    perp = np.array([-u[1], u[0], 0]) * 0.12
                    ar = Arrow(s + u * 0.5 + perp, e - u * 0.5 + perp, buff=0, stroke_width=3, color=GREY_B,
                               tip_length=0.18)
                    arrows.add(ar)
                    tags.add(label(rf"owes {L[i, j]:g}", font_size=16, color=GREY_A).next_to(ar.get_center(),
                                                                                             perp * 6 + UP * 0.01,
                                                                                             buff=0.08))
        rule = label(r"each bank pays $\min(\text{what it owes}, \ \text{what it has} + \text{what it is paid})$",
                     font_size=21, color=WHITE)
        rows = VGroup(
            label(rf"A owes 8 but has 2: \ it pays {pay[0]:g}", font_size=20, color=SHOCK),
            label(rf"B receives {pay[0]:g}, \ pays its 6 in full", font_size=20, color=GAIN),
            label(rf"C receives 6, \ has 1: \ pays {pay[2]:g} of 8, \ shared", font_size=20, color=SHOCK),
            label(rf"A gets {L[2, 0] / L[2].sum() * pay[2]:g} back from C: \ hence {pay[0]:g}", font_size=20,
                  color=GREY_A),
            label(r"the clearing vector: \ a fixed point; \ Eisenberg and Noe", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        side = VGroup(rule, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.35)
        if side.width > 6.6:
            side.width = 6.6
            side.to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"Eisenberg and Noe, \ Management Science 47(2) (2001)", corner=DL, font_size=12)
        with self.voiceover(
            "Banks lend to each other, so a bank's ability to pay depends on whether its debtors pay it. <bookmark "
            "mark='a'/> Four banks. A owes B eight; B owes C six; C owes four to A and four to D. Each also has some "
            "money of its own. <bookmark mark='b'/> The rule, from Larry Eisenberg and Thomas Noe: each bank pays "
            "what it owes if it can, and otherwise everything it has, shared among its creditors in proportion. "
            f"<bookmark mark='c'/> A owes eight and has two; it pays what it can, {pay[0]:g}. <bookmark mark='d'/> "
            "B receives that, adds its own three, and pays its six in full. <bookmark mark='e'/> C receives six, "
            f"has one of its own, and can pay only {pay[2]:g} of the eight it owes, half to A and half to D. "
            f"<bookmark mark='f'/> But that payment is part of what A has: so A's {pay[0]:g} depends on C's "
            f"{pay[2]:g}, which depends on B's, which depends on A's. <bookmark mark='g'/> The payments are a fixed "
            "point, the clearing vector, and Eisenberg and Noe showed how to find it: start from full payment and "
            "lower it until everyone's books balance."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(*[FadeIn(n) for n in nodes.values()], *[GrowArrow(a) for a in arrows], FadeIn(tags))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            for k, mk in enumerate("cdefg"):
                vo.wait_until(mk)
                anims = [FadeIn(rows[k], shift=RIGHT * 0.1)]
                if k == 0:
                    anims.append(nodes["A"][0].animate.set_stroke(SHOCK))
                if k == 2:
                    anims.append(nodes["C"][0].animate.set_stroke(SHOCK))
                self.play(*anims)
        self.clear_scene()

    def contagion(self):
        C = load("banks")["contagion"]
        sh = np.array(C["shocks"])
        ax = plane([0, 20], [0, 10.5], center=RIGHT * 2.0 + DOWN * 0.4, x_length=6.6, y_length=4.6,
                   xticks=[0, 5, 10, 15, 20], yticks=[0, 2, 4, 6, 8, 10], xlabel=r"loss at one bank",
                   ylabel=r"banks that default", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        rg = path(ax, sh, C["ring"]["defaults"], LINK, 3.4, smooth=False)
        cp = path(ax, sh, C["complete"]["defaults"], SHOCK, 3.4, smooth=False)
        ri = tiny_net("ring", color=LINK).move_to(LEFT * 4.8 + UP * 1.4)
        ci = tiny_net("complete", color=SHOCK).move_to(LEFT * 4.8 + DOWN * 1.5)
        rl = label(r"a ring: \ each owes the next", font_size=17, color=LINK).next_to(ri, DOWN, buff=0.15)
        cl = label(r"complete: \ each owes all the others", font_size=17, color=SHOCK).next_to(ci, DOWN, buff=0.15)
        thr = next(s for s, d in zip(sh, C["complete"]["defaults"]) if d == 10)
        concl = label(r"robust yet fragile: \ small shocks are shared, \ large ones reach everyone", font_size=21,
                      color=E.ACCENT).to_edge(UP, buff=0.4)
        tag = published_tag(r"Acemoglu, \ Ozdaglar and Tahbaz-Salehi, \ AER 105(2) (2015); \ the Island: \ "
                            r"agora.network.contagion", corner=DL, font_size=12)
        with self.voiceover(
            "Is it safer for banks to owe each other a little, or a lot to one? Daron Acemoglu, Asuman Ozdaglar and "
            "Alireza Tahbaz-Salehi worked it out. Ten banks, each owing ten in total, each with a cushion of one. "
            "<bookmark mark='a'/> In a ring, each bank owes the next. <bookmark mark='b'/> A loss at one bank "
            "passes to the next in line, and each extra unit of loss topples one more bank. <bookmark mark='c'/> "
            "In a complete network, each bank owes a little to all the others. <bookmark mark='d'/> Small losses "
            "are shared nine ways and absorbed: only the bank that was hit fails. <bookmark mark='e'/> But past a "
            f"threshold, a loss of about {thr:.0f} here, the same links carry it to everyone, and all ten fail at "
            "once. <bookmark mark='f'/> Robust yet fragile: the dense network is the safest for small shocks and "
            "the most dangerous for large ones."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(ri), FadeIn(rl))
            vo.wait_until("b")
            self.play(Create(rg), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(ci), FadeIn(cl))
            vo.wait_until("d")
            self.play(Create(cp), run_time=1.5)
            vo.wait_until("e")
            self.play(Indicate(cp, color=WHITE, scale_factor=1.0))
            vo.wait_until("f")
            self.play(FadeIn(concl))
        self.clear_scene()

    def lessons(self):
        head = label(r"what regulators took from it", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.4)
        cards = point_cards([
            (r"15 September 2008", r"Lehman Brothers is allowed to fail; \ the next day the government rescues AIG, "
             r"\ which owed too many others too much", SHOCK),
            (r"clearing houses", r"since 2009, \ standard derivatives must pass through central counterparties: \ "
             r"a star network, \ built on purpose", BANK),
            (r"who owes whom", r"supervisors collect the exposures between large banks, \ to see the network "
             r"before the shock", LINK),
            (r"the catch", r"a star is only as safe as its centre; \ the clearing house must never fail", GDP),
        ], cols=2, width=12.8, font_size=20).next_to(head, DOWN, buff=0.45)
        tag = published_tag(r"Elliott, \ Golub and Jackson, \ AER 104(10) (2014); \ G20 Pittsburgh statement (2009)",
                            corner=DL, font_size=12)
        with self.voiceover(
            "The theory arrived with the crisis that needed it. <bookmark mark='a'/> On the fifteenth of September "
            "2008 Lehman Brothers was allowed to fail. The next day the American government rescued the insurer "
            "AIG, which had sold protection to too many banks to be let go. <bookmark mark='b'/> Afterwards, the "
            "leaders of the G20 agreed that standard derivatives should pass through central counterparties: "
            "clearing houses that stand between every buyer and seller, a star network built on purpose. <bookmark "
            "mark='c'/> Supervisors now collect who owes whom among the largest banks, to see the network before "
            "the shock. <bookmark mark='d'/> And the catch, from chapter four: a star is only as safe as its "
            "centre. And Matthew Elliott, Benjamin Golub and Matthew Jackson showed the same two-sidedness in the "
            "number of counterparties: spreading exposures first connects the network and lets cascades travel, "
            "then, as it grows, insures the banks against one another."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                self.play(FadeIn(cards.cards[k], shift=UP * 0.1))
        self.clear_scene()
