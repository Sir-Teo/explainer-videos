from __future__ import annotations

from videos.economics.econ18.common import *  # noqa: F403


def state_card(title, s, u, color, w=5.4):
    rows = VGroup(label(title, font_size=24, color=color))
    for who in ("Ana", "Bo"):
        x, y = s[who]
        rows.add(VGroup(islander(who.lower(), 0.5),
                        label(rf"{who}: \ {x:g} fish, \ {y:g} fruit \ $\Rightarrow$ \ utility {u[who]:g}",
                              font_size=21)).arrange(RIGHT, buff=0.2))
    tx, ty = s["Ana"][0] + s["Bo"][0], s["Ana"][1] + s["Bo"][1]
    rows.add(label(rf"in all: \ {tx:g} fish, \ {ty:g} fruit", font_size=19, color=GREY_A))
    rows.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
    box = RoundedRectangle(width=w, height=rows.height + 0.5, corner_radius=0.15, stroke_color=color, stroke_width=2)
    rows.move_to(box)
    return VGroup(box, rows)


class Pareto(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Pareto and its limits", r"If a change helps some and hurts others, \ can we still call it an "
             r"improvement?", "Chapter nine. Pareto and its limits.",
             lit={1939: r"Kaldor and Hicks", 1941: r"Scitovsky", 1970: r"Sen's liberal"}, scale=("person", "nation"),
             horizon=("a year",))
        self.compensation()
        self.reversal()
        self.liberal()

    def compensation(self):
        rows = VGroup(
            label(r"Pareto: \ if a change helps someone and hurts nobody, \ it is better", font_size=25, color=WELF),
            label(r"almost no policy passes: \ a tariff cut, \ a new road, \ a vaccine mandate all have losers",
                  font_size=23, color=GREY_A),
            label(r"Kaldor and Hicks, \ 1939: \ call it better if the winners \emph{could} compensate the losers",
                  font_size=24, color=MONEY),
            label(r"whether or not they do", font_size=23, color=HOLD),
            label(r"this is the test behind every cost-benefit analysis: \ gains exceed losses, \ in money",
                  font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Kaldor, EJ 49(195) (1939); \ Hicks, EJ 49(196) (1939)", corner=DR, font_size=13)
        with self.voiceover(
            "If comparing people is an ethical choice, perhaps we can avoid it. <bookmark mark='a'/> Vilfredo "
            "Pareto's criterion needs no comparison: a change that helps someone and hurts nobody is better. "
            "<bookmark mark='b'/> But almost no policy passes it. A tariff cut, a new road, a vaccine mandate: each "
            "has losers. <bookmark mark='c'/> In 1939 Nicholas Kaldor and John Hicks proposed a weaker test. Call a "
            "change an improvement if the winners could compensate the losers and still come out ahead, "
            "<bookmark mark='d'/> whether or not they actually do. <bookmark mark='e'/> That is the test behind every "
            "cost-benefit analysis: the gains, in money, exceed the losses."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def reversal(self):
        sc = load("pareto")["scitovsky"]
        one = state_card(r"state 1", sc["s1"], sc["u1"], RULE).move_to(LEFT * 3.5 + UP * 1.55)
        two = state_card(r"state 2", sc["s2"], sc["u2"], MONEY).move_to(RIGHT * 3.5 + UP * 1.55)
        a12 = CurvedArrow(one.get_top() + RIGHT * 1.2, two.get_top() + LEFT * 1.2, angle=-TAU / 8, color=WELF)
        a21 = CurvedArrow(two.get_bottom() + LEFT * 1.2, one.get_bottom() + RIGHT * 1.2, angle=-TAU / 8, color=CYCLE)
        (a1, f1), (b1, g1) = sc["split_12"]
        (a2, f2), (b2, g2) = sc["split_21"]
        go = VGroup(
            label(r"from 1 to 2: \ Bo gains, \ Ana loses", font_size=21, color=WELF),
            label(rf"share state 2's goods: \ Ana {a1:.2f} fish, \ {f1:.2f} fruit \ ($\ge 6$); \ "
                  rf"Bo {b1:.2f}, \ {g1:.2f} \ ($> 6$)", font_size=18, color=GREY_A),
            label(r"the test says: \ better", font_size=21, color=WELF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        back = VGroup(
            label(r"from 2 back to 1: \ Ana gains, \ Bo loses", font_size=21, color=CYCLE),
            label(rf"share state 1's goods: \ Ana {a2:.2f} fish, \ {f2:.2f} fruit \ ($\ge 4$); \ "
                  rf"Bo {b2:.2f}, \ {g2:.2f} \ ($\ge 21$)", font_size=18, color=GREY_A),
            label(r"the test says: \ better \ again", font_size=21, color=CYCLE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        VGroup(go, back).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to(DOWN * 1.75)
        foot = label(r"Scitovsky, \ 1941: \ the test can approve a move and its reversal; \ and compensation unpaid "
                     r"is not compensation", font_size=20, color=E.ACCENT).to_edge(DOWN, buff=0.22)
        tag = agora_tag(corner=UR, font_size=14)
        with self.voiceover(
            "Tibor Scitovsky found the trouble in 1941. Agora rebuilds his example with two islanders whose "
            "utility is their fish times their fruit. <bookmark mark='a'/> In state one, Ana has six fish and one "
            "fruit, Bo the reverse; each scores six. In state two, Ana has one fish and four fruit, scoring four, "
            "and Bo has seven and three, scoring twenty-one. <bookmark mark='b'/> Moving from one to two, Bo gains "
            "and Ana loses. Could Bo compensate her? Share state two's goods so that Ana still scores six and Bo "
            "more than six: yes, so the test calls the move better. <bookmark mark='c'/> Now move back, from two to "
            "one. Ana gains, Bo loses. Could Ana compensate Bo? Share state one's goods so that Bo keeps his "
            "twenty-one and Ana her four: yes again. <bookmark mark='d'/> The test approves a move, and approves "
            "undoing it. The reason is that prices, and so the value of the goods, change with who holds them. And "
            "compensation that is never paid is not compensation."
        ) as vo:
            self.play(FadeIn(one), FadeIn(two), FadeIn(tag))
            vo.wait_until("b")
            self.play(Create(a12), FadeIn(go))
            vo.wait_until("c")
            self.play(Create(a21), FadeIn(back))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def liberal(self):
        lp = load("pareto")["liberal"]
        name = {"n": r"nobody reads it", "p": r"the prude reads it", "l": r"the lewd reads it"}
        pos = {"n": UP * 1.6, "p": LEFT * 3.2 + DOWN * 1.4, "l": RIGHT * 3.2 + DOWN * 1.4}
        nodes = {k: label(v, font_size=24, color=WHITE).move_to(pos[k] + DOWN * 0.2) for k, v in name.items()}
        edges = [("n", "p", r"the prude's own choice", RULE), ("l", "n", r"the lewd's own choice", RULE),
                 ("p", "l", r"Pareto: \ both agree", WELF)]
        arrows = VGroup()
        for a, b, t, c in edges:
            ar = Arrow(nodes[a].get_center(), nodes[b].get_center(), buff=0.55, color=c, stroke_width=4)
            tl = label(rf"{t}: \ beats", font_size=17, color=c).move_to(ar.get_center())
            off = ar.get_center() - ORIGIN + DOWN * 0.2
            tl.shift(off / max(np.linalg.norm(off), 1e-6) * 0.55)
            arrows.add(VGroup(ar, tl))
        prefs = VGroup(
            label(r"the prude: \ nobody, \ then the prude, \ then the lewd", font_size=19, color=GREY_A),
            label(r"the lewd: \ the prude, \ then the lewd, \ then nobody", font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UL, buff=0.35)
        foot = label(r"Sen, \ 1970: \ a little liberty and Pareto together can leave no best choice", font_size=23,
                     color=CYCLE).to_edge(DOWN, buff=0.4)
        tag = published_tag(r"Sen, JPE 78(1) (1970)", corner=DR, font_size=13)
        with self.voiceover(
            "Sen found a deeper limit in 1970, with one copy of a scandalous book. <bookmark mark='a'/> The prude "
            "would rather nobody read it, but would rather read it than let the lewd. The lewd most wants the prude "
            "to read it, and would rather read it than see it go unread. <bookmark mark='b'/> "
            "Grant each a little liberty: whether you read a book is your own business. The prude doesn't want to "
            "read it, so nobody reading beats the prude reading. <bookmark mark='c'/> The lewd wants to read it, so "
            "the lewd reading beats nobody reading. <bookmark mark='d'/> But both prefer the prude reading to the "
            "lewd reading, so by Pareto that beats it too. <bookmark mark='e'/> The three judgments go round in a "
            "circle. Liberty for two people over their own affairs, plus the Pareto principle, can leave no best "
            "choice at all."
        ) as vo:
            self.play(*[FadeIn(n) for n in nodes.values()], FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(prefs))
            for mk, ar in zip("bcd", arrows):
                vo.wait_until(mk)
                self.play(GrowArrow(ar[0]), FadeIn(ar[1]))
            vo.wait_until("e")
            self.play(FadeIn(foot), *[Indicate(a[0], color=CYCLE) for a in arrows])
        self.clear_scene()
