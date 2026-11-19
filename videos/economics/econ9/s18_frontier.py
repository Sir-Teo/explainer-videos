from __future__ import annotations

from videos.economics.econ9.common import *  # noqa: F403

KEYS = ("ana", "bo", "chidi", "dara", "crusoe", "friday")
CYC = ("#F6C453", "#7BD88F", "#7EC8F5")


def hut(width=0.75, color="#6B5B45"):
    body = Square(side_length=width, stroke_color="#A89276", stroke_width=2, fill_color=color, fill_opacity=0.85)
    roof = Polygon(body.get_corner(UL) + LEFT * 0.08, body.get_corner(UR) + RIGHT * 0.08,
                   body.get_top() + UP * width * 0.45, stroke_color="#A89276", stroke_width=2, fill_color="#4F4334",
                   fill_opacity=0.9)
    return VGroup(body, roof)


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ hard equilibria, \ and markets without money", r"Can equilibria always be found "
             r"in time, and what if goods can't be divided?", "Chapter sixteen. Frontier: hard equilibria, and "
             "markets without money.", lit={2011: r"Budish's course market"}, scale=("market",))
        self.hard()
        self.huts()
        self.courses()

    def hard(self):
        cards = VGroup(
            history_card(1994, r"Christos Papadimitriou", r"PPAD: \ problems whose answer is guaranteed by a parity "
                         r"argument, \ like the doors of Sperner's triangle", color=HOLD, width=5.8, font_size=21),
            history_card(2006, r"Daskalakis, Goldberg and Papadimitriou; \ Chen and Deng",
                         r"finding a Nash equilibrium is as hard as any problem in PPAD", color=HOLD, width=5.8,
                         font_size=21),
        ).arrange(RIGHT, buff=0.35).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"Scarf's walk always ends, \ but it can be very long: \ exponential in the worst case",
                  font_size=24),
            label(r"so is there a fast algorithm for every economy? \ probably not:", font_size=25, color=E.ACCENT),
            label(r"for some kinds of markets, \ finding a competitive equilibrium \\ is as hard as Nash's problem "
                  r"(Chen, Dai, Du and Teng, 2009)", font_size=23, color=HOLD),
            label(r"if a computer can't find the equilibrium in reasonable time, \\ should we expect a market to?",
                  font_size=25, color=CC),
        ).arrange(DOWN, buff=0.35).next_to(cards, DOWN, buff=0.55)
        tag = published_tag(r"Papadimitriou, JCSS 48(3) (1994); Daskalakis et al., SIAM J.\ Comput.\ (2009); Chen, "
                            r"Dai, Du and Teng, FOCS (2009)", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier has two questions about this part. The first is computational. Scarf's walk always "
            "ends, but on bad problems it can take a number of steps that grows exponentially with their size. "
            "<bookmark mark='a'/> In 1994 Christos Papadimitriou defined a class of problems, called PPAD, whose "
            "solutions are guaranteed to exist by exactly the argument of Sperner's doors: follow the path and "
            "you must arrive. <bookmark mark='b'/> In 2006 Constantinos Daskalakis, Paul Goldberg and "
            "Papadimitriou, and then Xi Chen and Xiaotie Deng, proved that finding a Nash equilibrium of a game, "
            "the subject of Part eleven, is as hard as anything in that class. <bookmark mark='c'/> And for some "
            "kinds of markets, finding a competitive equilibrium is just as hard. <bookmark mark='d'/> Which raises "
            "a question economists are still arguing about: if no computer can find an equilibrium in reasonable "
            "time, why should we expect a market to?"
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(cards[0], shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(cards[1], shift=UP * 0.2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def huts(self):
        h = load("huts")
        n = len(h["names"])
        centre = LEFT * 3.0 + DOWN * 0.2
        R = 2.3
        pos = [centre + R * np.array([np.cos(PI / 2 + 2 * PI * k / n), np.sin(PI / 2 + 2 * PI * k / n), 0])
               for k in range(n)]
        huts = VGroup()
        for k in range(n):
            hk = hut().move_to(pos[k])
            who = islander(KEYS[k], 0.45).next_to(hk, DOWN, buff=0.05)
            nm = label(h["names"][k], font_size=17, color=island.CAST[KEYS[k]].color).next_to(who, DOWN, buff=0.02)
            huts.add(VGroup(hk, who, nm))
        side = VGroup(
            label(r"six islanders, \ each owning a hut; \ no money", font_size=22),
            label(r"Shapley and Scarf (1974): \ is there an allocation \\ no group would undo?", font_size=22),
            label(r"top trading cycles (David Gale): \ each points to the owner \\ of the hut they like best; \ "
                  r"trade around every cycle; \ repeat", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.45).shift(UP * 1.2)
        results = VGroup()
        for k, rd in enumerate(h["rounds"]):
            cyc = [" $\\to$ ".join(h["names"][i] for i in c + [c[0]]) if len(c) > 1 else
                   rf"{h['names'][c[0]]} keeps {('his' if KEYS[c[0]] in ('bo', 'crusoe', 'friday') else 'her')} own"
                   for c in rd["cycles"]]
            results.add(label(rf"round {k + 1}: \ " + r"; \ ".join(cyc), font_size=20, color=CYC[k % 3]))
        results.add(label(r"in the core: \ no group can do better on its own; \\ and nobody gains by lying about "
                          r"their ranking (Roth, 1982)", font_size=21, color=CC))
        results.arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(side, DOWN, buff=0.35).align_to(side, LEFT)

        def arrows(rd, color):
            g = VGroup()
            for i, j in rd["pointing"].items():
                i, j = int(i), int(j)
                if i == j:
                    g.add(Circle(radius=0.55, color=color, stroke_width=3).move_to(huts[i][0]))
                else:
                    g.add(CurvedArrow(huts[i][0].get_center(), huts[j][0].get_center(), angle=-0.4, color=color,
                                      stroke_width=3, tip_length=0.18))
            return g

        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "The second question is older. Everything in this part assumed goods can be divided, and traded for "
            "money. What if they can't? <bookmark mark='a'/> Six islanders each own a hut, and each ranks all six. "
            "There is no money. <bookmark mark='b'/> In 1974 Lloyd Shapley and Herbert Scarf asked whether there is "
            "always a way to swap huts that no group would undo. <bookmark mark='c'/> There is, and David Gale's "
            "method finds it. Everyone points at the owner of the hut they like best. <bookmark mark='d'/> Follow "
            "the arrows and there is always a cycle: here Ana points to Chidi's hut, Chidi to Bo's, and Bo to Ana's. "
            "They swap around the cycle and leave. <bookmark mark='e'/> The rest point again among the huts that "
            "are left: Dara and Crusoe swap. <bookmark mark='f'/> And Friday keeps his own. "
            "<bookmark mark='g'/> The result is in the core: no group can do better trading among themselves. And, "
            "as Alvin Roth later showed, nobody can gain by lying about their ranking. A version of this idea now "
            "helps arrange chains of kidney donations."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(x, shift=UP * 0.1) for x in huts], lag_ratio=0.15), FadeIn(tag),
                      run_time=1.8)
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            a1 = arrows(h["rounds"][0], CYC[0])
            self.play(FadeIn(side[2]), LaggedStart(*[Create(a_) for a_ in a1], lag_ratio=0.15), run_time=2)
            vo.wait_until("d")
            gone = [i for c in h["rounds"][0]["cycles"] for i in c]
            self.play(FadeIn(results[0]), *[huts[i].animate.set_opacity(0.3) for i in gone], FadeOut(a1))
            vo.wait_until("e")
            a2 = arrows(h["rounds"][1], CYC[1])
            self.play(LaggedStart(*[Create(a_) for a_ in a2], lag_ratio=0.2), FadeIn(results[1]))
            gone2 = [i for c in h["rounds"][1]["cycles"] for i in c]
            self.play(*[huts[i].animate.set_opacity(0.3) for i in gone2], FadeOut(a2))
            vo.wait_until("f")
            a3 = arrows(h["rounds"][2], CYC[2])
            self.play(Create(a3), FadeIn(results[2]))
            vo.wait_until("g")
            self.play(FadeIn(results[3]))
        self.clear_scene()

    def courses(self):
        hc = history_card(2011, r"Eric Budish", r"``approximate competitive equilibrium from equal incomes'': \ give "
                          r"every student the same budget of fake money, \ let them buy seats in courses, \ find "
                          r"prices that nearly clear every class", color=E.ACCENT, width=11.6, font_size=23
                          ).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"courses come in whole seats, \ and students want bundles of them: \ no exact equilibrium need "
                  r"exist", font_size=23),
            label(r"Budish proved an approximate one does, \ with small differences in budgets to break ties",
                  font_size=23),
            label(r"used at the Wharton School as Course Match \ (Budish, Cachon, Kessler and Othman, 2017)",
                  font_size=23, color=CC),
            label(r"a competitive equilibrium, \ computed on purpose, \ as a fair and efficient way to share",
                  font_size=24, color=E.ACCENT),
            label(r"markets by design: \ Parts 16 and 17", font_size=22, color=GREY_A),
        ).arrange(DOWN, buff=0.35).next_to(hc, DOWN, buff=0.55)
        tag = published_tag(r"Budish, JPE 119(6) (2011); Budish et al., Operations Research 65(2) (2017)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "And the theory of this part has come back as a tool. <bookmark mark='a'/> Places in university "
            "courses are scarce, come in whole seats, and students want bundles of them, so there may be no exact "
            "equilibrium at all. In 2011 Eric Budish proposed giving every student the same budget of artificial "
            "money, letting them buy seats, and finding prices at which every class nearly clears. "
            "<bookmark mark='b'/> He proved that such an approximate equilibrium always exists, if budgets differ "
            "by tiny amounts to break ties. <bookmark mark='c'/> The Wharton School adopted it to allocate its "
            "courses, under the name Course Match. <bookmark mark='d'/> A competitive equilibrium, computed on "
            "purpose, as a fair and efficient way to share what can't be divided. <bookmark mark='e'/> Designing "
            "markets like that is the subject of Parts sixteen and seventeen."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
