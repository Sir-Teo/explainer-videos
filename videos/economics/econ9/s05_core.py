from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403
from videos.economics.econ9.s03_box import ana_curve, bo_curve, u_cd


def box_traders(b):
    return (ge.Trader((b["aA"], 1 - b["aA"]), b["eA"]), ge.Trader((b["aB"], 1 - b["aB"]), b["eB"]))


def segment(box, A, B, lo, hi, color=CORE, width=7):
    xs = np.linspace(lo, hi, 80)
    return box.curve(xs, ge.contract_curve(A, B, xs), color=color, width=width)


class Core(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The core, \ and Edgeworth's conjecture", r"With many traders, how much room is left for "
             r"bargaining?", "Chapter four. The core, and Edgeworth's conjecture.",
             lit={1963: r"Debreu and Scarf's limit theorem"})
        self.two()
        self.coalition()
        self.shrink()
        self.theorem()

    def two(self):
        b = load("box")
        A, B = box_traders(b)
        box = box_from(b, center=LEFT * 2.6 + DOWN * 0.1, width=6.2, height=5.4)
        w = Dot(box.c2p(*b["eA"]), radius=0.09, color=WHITE)
        cc = box.curve(b["cc_x"], b["cc_y"], color=CC, width=3)
        core = segment(box, A, B, *b["lens"])
        E_ = Dot(box.c2p(*b["xA"]), radius=0.09, color=WHITE)
        side = VGroup(
            label(r"the \emph{core}: \ allocations that no group \\ can improve on by trading among themselves",
                  font_size=23, color=CORE),
            label(r"two traders: \ the groups are Ana, \ Bo, \ and both", font_size=22),
            label(r"Ana alone blocks anything worse than $\omega$ for her; \\ so does Bo; \ together they block "
                  r"anything inefficient", font_size=21, color=GREY_A),
            label(r"what's left: \ the contract curve inside the lens", font_size=23, color=CORE),
            label(rf"Ana's fish: \ anywhere from {b['lens'][0]:.2f} to {b['lens'][1]:.2f}", font_size=23,
                  color=CORE),
            label(r"the price equilibrium is one point in it", font_size=22, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).to_edge(RIGHT, buff=0.45)
        tag = island_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Where trade ends between two people depends on how they bargain. Here's a way to say exactly how much "
            "it can depend on. <bookmark mark='a'/> Call an allocation blocked if some group of traders could do "
            "better for all its members by trading only among themselves. The core is everything that isn't "
            "blocked. <bookmark mark='b'/> With two traders there are three groups: Ana, Bo, and the pair. "
            "<bookmark mark='c'/> Ana on her own blocks anything worse for her than not trading; so does Bo; and the "
            "two together block anything inefficient. <bookmark mark='d'/> What's left is the contract curve inside "
            "the lens. <bookmark mark='e'/> Ana could end up with as few as two point oh seven fish or as many as "
            "five point five nine, and more or fewer coconuts to match. <bookmark mark='f'/> The price equilibrium "
            "is one point in this stretch, but nothing about two people bargaining picks it out."
        ) as vo:
            self.play(FadeIn(box), FadeIn(w), FadeIn(cc), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Create(core), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
            vo.wait_until("f")
            self.play(FadeIn(E_, scale=0.5), FadeIn(side[5]))
        self.clear_scene()

    def coalition(self):
        b = load("box")
        c = load("core")
        A, B = box_traders(b)
        X = np.array(b["X"])
        box = box_from(b, center=LEFT * 3.2 + DOWN * 0.1, width=5.6, height=5.0)
        w = Dot(box.c2p(*b["eA"]), radius=0.08, color=WHITE)
        cc = box.curve(b["cc_x"], b["cc_y"], color=CC, width=2.5)
        ex = c["example"]
        P = Dot(box.c2p(ex["x"], ex["y"]), radius=0.1, color=HOLD)
        Pl = label(r"a deal good for Bo", font_size=19, color=HOLD).next_to(P, DR, buff=0.1)
        ia = ana_curve(box, b, u_cd(b["aA"], [ex["x"], ex["y"]]), width=2.2)
        ib = bo_curve(box, b, u_cd(b["aB"], X - np.array([ex["x"], ex["y"]])), width=2.2)
        people = VGroup(islander("ana", 0.8), islander("ana", 0.8), islander("bo", 0.8), islander("bo", 0.8)
                        ).arrange(RIGHT, buff=0.35).to_edge(RIGHT, buff=1.2).shift(UP * 2.4)
        ring = SurroundingRectangle(VGroup(people[0], people[1], people[2]), color=CORE, buff=0.15,
                                    corner_radius=0.15)
        side = VGroup(
            label(r"now two Anas and two Bos, \ each pair as before", font_size=22),
            label(r"the same deal offered to each pair", font_size=22, color=HOLD),
            label(r"two Anas and one Bo pool what they own \\ and trade among themselves:", font_size=22,
                  color=CORE),
            label(r"the Bo gets exactly what the deal gave him; \\ both Anas get more than the deal gave them",
                  font_size=22, color=CORE),
            label(r"the deal is blocked: \ it is no longer in the core", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(people, DOWN, buff=0.45).to_edge(RIGHT, buff=0.4)
        with self.voiceover(
            "Now let the market grow. <bookmark mark='a'/> Make two copies of each trader: two Anas, each with "
            "eight fish and one and a half baskets, and two Bos. <bookmark mark='b'/> Take a deal in the old core, "
            "but near the end that's good for Bo, and offer it to both pairs. <bookmark mark='c'/> Two Anas and one "
            "Bo can now pool what they have and trade among themselves. They have eighteen fish and eleven and a "
            "half baskets between them, and only one Bo to satisfy. <bookmark mark='d'/> They can give that Bo "
            "exactly what the deal gave him, and still leave both Anas better off than the deal did. "
            "<bookmark mark='e'/> So the deal is blocked. With more traders, there are more groups that can walk "
            "away and do better, and the core gets smaller."
        ) as vo:
            self.play(FadeIn(box), FadeIn(w), FadeIn(cc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_, shift=UP * 0.1) for p_ in people], lag_ratio=0.2), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(P, scale=0.5), FadeIn(Pl), Create(ia), Create(ib), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(ring), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]), P.animate.set_opacity(0.3))
        self.clear_scene()

    def shrink(self):
        b = load("box")
        c = load("core")
        A, B = box_traders(b)
        box = box_from(b, center=LEFT * 2.6 + DOWN * 0.1, width=6.2, height=5.4)
        w = Dot(box.c2p(*b["eA"]), radius=0.08, color=WHITE)
        cc = box.curve(b["cc_x"], b["cc_y"], color=CC, width=2.5)
        E_ = Dot(box.c2p(*b["xA"]), radius=0.09, color=WHITE)
        segs = {r: segment(box, A, B, *c["intervals"][str(r)][:2]) for r in c["reps"]}
        table = VGroup(VGroup(label(r"copies of each", font_size=21, color=GREY_A),
                              label(r"Ana's fish in the core", font_size=21, color=GREY_A)))
        for r in c["reps"]:
            lo, hi = c["intervals"][str(r)][:2]
            table.add(VGroup(label(f"{r}", font_size=22, color=CORE), label(rf"{lo:.2f} to {hi:.2f}", font_size=22,
                                                                              color=CORE)))
        for row in table:
            row[1].next_to(row[0], RIGHT, buff=0.5)
        table.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        for row in table[1:]:
            row[0].move_to([table[0][0].get_center()[0], row[0].get_center()[1], 0])
            row[1].move_to([table[0][1].get_center()[0], row[1].get_center()[1], 0])
        table.add(label(rf"competitive equilibrium: \ {c['xw']:.2f}", font_size=22, color=WHITE).next_to(
            table, DOWN, buff=0.3).align_to(table, LEFT))
        table.to_edge(RIGHT, buff=0.6).shift(UP * 0.4)
        tag = agora_tag(corner=DR, font_size=15)
        cur = segs[c["reps"][0]]
        with self.voiceover(
            "Agora can find the core for any number of copies, by checking every group that could form. "
            "<bookmark mark='a'/> With one of each, it's the whole stretch inside the lens. <bookmark mark='b'/> "
            "With two of each, it's already less than a third as long. <bookmark mark='c'/> Three, five, ten: "
            "<bookmark mark='d'/> with twenty copies of each, Ana's fish in the core run only from three point "
            "seven five to three point eight three. <bookmark mark='e'/> And the one allocation that survives every "
            "replication is the competitive equilibrium: three point seven nine fish. As the economy grows, the room "
            "for bargaining vanishes, and only the price outcome is left."
        ) as vo:
            self.play(FadeIn(box), FadeIn(w), FadeIn(cc), FadeIn(tag), FadeIn(table[0]))
            vo.wait_until("a")
            self.play(Create(cur), FadeIn(table[1]))
            vo.wait_until("b")
            self.play(Transform(cur, segs[c["reps"][1]]), FadeIn(table[2]))
            vo.wait_until("c")
            for k, r in enumerate(c["reps"][2:-1]):
                self.play(Transform(cur, segs[r]), FadeIn(table[3 + k]), run_time=0.9)
            vo.wait_until("d")
            self.play(Transform(cur, segs[c["reps"][-1]]), FadeIn(table[len(c["reps"])]))
            vo.wait_until("e")
            self.play(FadeIn(E_, scale=0.5), FadeIn(table[-1]))
        self.clear_scene()

    def theorem(self):
        q = quote_card(r"($\alpha$) Contract without competition is indeterminate, ($\beta$) Contract with "
                       r"\emph{perfect} competition is perfectly determinate, ($\gamma$) Contract with more or less "
                       r"perfect competition is less or more indeterminate.",
                       r"F.\ Y.\ Edgeworth, \emph{Mathematical Psychics} (1881), p.\ 20", width=11.6, font_size=25,
                       color=CC).to_edge(UP, buff=0.4)
        cards = VGroup(
            history_card(1963, r"G\'erard Debreu and Herbert Scarf", r"``A Limit Theorem on the Core of an "
                         r"Economy'': \ replicate the traders and the core shrinks to the competitive allocations",
                         color=CORE, width=5.8, font_size=21),
            history_card(1964, r"Robert Aumann", r"``Markets with a Continuum of Traders'': \ with no trader "
                         r"large, \ the core and the competitive allocations are the same", color=CORE, width=5.8,
                         font_size=21),
        ).arrange(RIGHT, buff=0.35).next_to(q, DOWN, buff=0.4)
        moral = label(r"why take prices as given? \ because in a large market, \ nobody can do better by not "
                      r"taking them", font_size=25, color=E.ACCENT).to_edge(DOWN, buff=0.5)
        tag = published_tag(r"Edgeworth (1881); Debreu and Scarf, IER 4(3) (1963); Aumann, Econometrica 32 (1964)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Edgeworth saw this in 1881. Contract without competition, he wrote, is indeterminate; contract with "
            "perfect competition is perfectly determinate; and contract with more or less perfect competition is "
            "less or more indeterminate. <bookmark mark='a'/> It took eighty-two years to prove in general. In "
            "1963 Gerard Debreu and Herbert Scarf showed that as an economy is replicated, the core shrinks to its "
            "competitive allocations. <bookmark mark='b'/> A year later Robert Aumann showed that in a market where "
            "no trader is large, a continuum of traders, the core and the competitive allocations are exactly the "
            "same. <bookmark mark='c'/> That answers a question left open since Part two: why should anyone take "
            "prices as given? Because in a large market no group of traders, of any size, can do better by "
            "refusing to."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(moral))
        self.clear_scene()
