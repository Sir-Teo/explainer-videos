from __future__ import annotations

from videos.economics.econ17.common import *  # noqa: F403

HUTS = ("ana", "bo", "chidi", "dara")


class Kidneys(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Huts and kidneys", r"When everyone already owns something, \ how can swaps make everyone "
             r"better off?", "Chapter nine. Huts and kidneys.",
             lit={1974: r"Shapley and Scarf", 2004: r"Roth, Sönmez and Ünver", 2009: r"the first long chain"},
             scale=("person", "nation"), horizon=("a year",))
        self.huts()
        self.why()
        self.pool()
        self.chains()

    def huts(self):
        h = load("huts")
        pos = {k: np.array([3.0 * np.cos(a), 2.0 * np.sin(a) - 0.3, 0])
               for k, a in zip(HUTS, (PI / 2 + PI / 4, PI / 4, -PI / 4, -PI / 2 - PI / 4))}
        chips = {k: who_chip(k, 0.6, 18).move_to(pos[k]) for k in HUTS}
        prefs = VGroup(*[label(rf"{island.CAST[k].name}: \ " + r" $>$ ".join(island.CAST[x].name + "'s"
                                                                          for x in h["prefs"][k]),
                               font_size=17, color=color_of(k)) for k in HUTS]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).to_corner(UL, buff=0.35).shift(DOWN * 0.5)
        head = label(r"top trading cycles: \ everyone owns a hut, \ and points at the one they like best",
                     font_size=24, color=E.ACCENT).to_edge(UP, buff=0.25)
        def arrow(a, b, color):
            return CurvedArrow(chips[a].get_center() + (pos[b] - pos[a]) * 0.18,
                               chips[b].get_center() - (pos[b] - pos[a]) * 0.18, angle=-0.35, color=color,
                               stroke_width=4)

        first = {k: h["prefs"][k][0] for k in HUTS}
        round1 = VGroup(*[arrow(a, b, color_of(a)) for a, b in first.items()])
        round2 = VGroup(*[arrow(a, b, color_of(a)) for a, b in h["cycles"][1]])
        result = label(r"each cycle swaps, \ and leaves; \ the rest point again", font_size=22,
                       color=STABLE).to_edge(DOWN, buff=0.4)
        tag = published_tag(r"Shapley and Scarf, J.\ Math.\ Econ.\ 1(1) (1974), \ crediting David Gale", corner=DR,
                            font_size=13)
        with self.voiceover(
            "First, a market where everyone already owns something. Four islanders each own a hut, and each ranks "
            "all four huts. <bookmark mark='a'/> David Gale's procedure, which Lloyd Shapley and Herbert Scarf "
            "published in 1974, asks everyone to point at the owner of the hut they like best. "
            "<bookmark mark='b'/> There is always at least one cycle of pointing. Here Ana and Bo point at each "
            "other: Ana gets Bo's hut, Bo gets Ana's, and both leave. <bookmark mark='c'/> Dara's favourite was "
            "Ana's hut, which has gone, so Dara now points at Chidi's, and Chidi points at Dara's: a second cycle, "
            "and they swap too. <bookmark mark='d'/> The result is efficient, no group could do better trading "
            "among themselves, and pointing at your true favourite is always safe."
        ) as vo:
            self.play(FadeIn(head), FadeIn(prefs), *[FadeIn(c) for c in chips.values()], FadeIn(tag))
            vo.wait_until("a")
            self.play(*[Create(a) for a in round1], run_time=1.5)
            vo.wait_until("b")
            self.play(Indicate(round1[0], color=WHITE), Indicate(round1[1], color=WHITE))
            self.play(FadeOut(round1), chips["ana"].animate.set_opacity(0.35), chips["bo"].animate.set_opacity(0.35))
            vo.wait_until("c")
            self.play(*[Create(a) for a in round2], run_time=1.2)
            vo.wait_until("d")
            self.play(FadeIn(result))
        self.clear_scene()

    def why(self):
        k = load("roth")["kidney"]
        rows = VGroup(
            label(r"a healthy person can give a kidney to someone they love: \ if their blood and tissue match",
                  font_size=23),
            label(r"often they don't: \ the donor is willing, \ but can't give to their own patient", font_size=23,
                  color=REJECT),
            label(r"and selling a kidney is illegal almost everywhere: \ no price can help", font_size=23,
                  color=GREY_A),
            label(r"so swap: \ my donor gives to your patient, \ yours to mine", font_size=25, color=KIDNEY),
            label(rf"surgeries at the same time, \ so nobody backs out: \ {k['two_way_rooms']} operating rooms for a "
                  rf"swap of two, \ {k['three_way_rooms']} for three", font_size=22, color=HELD),
            label(r"2004: \ Roth, \ Tayfun Sönmez and Utku Ünver design a clearinghouse for it, \ with New England's "
                  r"surgeons", font_size=22, color=STABLE),
        ).arrange(DOWN, buff=0.36).move_to(UP * 0.1)
        tag = published_tag(r"Roth, Sönmez and Ünver, QJE 119(2) (2004); \ Roth, Nobel lecture (2012)", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Kidneys are the life-and-death version. <bookmark mark='a'/> A healthy person can give a kidney to a "
            "relative or friend with kidney failure, if their blood and tissues are compatible. "
            "<bookmark mark='b'/> Often they are not: the donor is willing, but cannot give to their own patient. "
            "<bookmark mark='c'/> And buying and selling kidneys is illegal almost everywhere, so no price can do "
            "the work. <bookmark mark='d'/> But two such pairs can swap: my donor gives to your patient, and yours "
            "to mine. <bookmark mark='e'/> The operations are done at the same time, so that nobody can back out: "
            "four operating rooms and four surgical teams for a swap between two pairs, and six for three. "
            "<bookmark mark='f'/> In 2004 Roth, Tayfun Sönmez and Utku Ünver designed a clearinghouse for such "
            "swaps, and helped New England's surgeons start one."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def graph(self, kd):
        pairs = sorted(kd["compat"], key=lambda p: int(p[1:]))
        n = len(pairs)
        pos = {p: np.array([2.6 * np.cos(PI / 2 - 2 * PI * i / n), 2.6 * np.sin(PI / 2 - 2 * PI * i / n) - 0.4, 0])
               + LEFT * 2.2 for i, p in enumerate(pairs)}
        nodes = {p: VGroup(Circle(radius=0.33, color=KIDNEY, stroke_width=3, fill_color=BACKGROUND, fill_opacity=1),
                           label(p, font_size=18, color=KIDNEY)).move_to(pos[p]) for p in pairs}
        for p in pairs:
            nodes[p][1].move_to(nodes[p][0])
        edges = {}
        for a, outs in kd["compat"].items():
            for b in outs:
                edges[(a, b)] = Arrow(pos[a], pos[b], buff=0.36, color=GREY_C, stroke_width=2,
                                      max_tip_length_to_length_ratio=0.12)
        return pairs, pos, nodes, edges

    def pool(self):
        kd = load("kidneys")
        pairs, pos, nodes, edges = self.graph(kd)
        g = VGroup(*edges.values(), *nodes.values())
        head = label(r"eight patient--donor pairs: \ an arrow means that donor can give to that patient",
                     font_size=22, color=E.ACCENT).to_edge(UP, buff=0.3)

        def light(sets, color):
            out = []
            for it in sets:
                ps = it["pairs"]
                if it["kind"] == "cycle":
                    for i in range(len(ps)):
                        e = edges.get((ps[i], ps[(i + 1) % len(ps)]))
                        if e is not None:
                            out.append(e.animate.set_color(color).set_stroke(width=5))
                    out += [nodes[p][0].animate.set_fill(color, opacity=0.35) for p in ps]
            return out

        side = VGroup(
            label(rf"swaps of two only: \ {kd['pairs_only']} transplants", font_size=23, color=HELD),
            label(rf"cycles of up to three: \ {kd['cycles']}", font_size=23, color=STABLE),
            label(r"longer cycles need more \\ operating rooms at once", font_size=20, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.6).shift(UP * 0.6)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is a small pool in Agora: eight pairs, each a patient with a willing but incompatible donor. An "
            "arrow from one pair to another means that pair's donor could give to the other's patient. "
            "<bookmark mark='a'/> If only swaps between two pairs are allowed, the best Agora can find is one swap: "
            "two transplants. <bookmark mark='b'/> Allow cycles of three, and two cycles fit: six transplants. "
            "<bookmark mark='c'/> Longer cycles would find more, but need more operating rooms at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(tag), run_time=1.5)
            vo.wait_until("a")
            self.play(*light(kd["best_pairs_only"], HELD), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(*[e.animate.set_color(GREY_C).set_stroke(width=2) for e in edges.values()],
                      *[nodes[p][0].animate.set_fill(BACKGROUND, opacity=1) for p in pairs], run_time=0.6)
            self.play(*light(kd["best_cycles"], STABLE), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def chains(self):
        kd = load("kidneys")
        k = load("roth")["kidney"]
        pairs, pos, nodes, edges = self.graph(kd)
        g = VGroup(*edges.values(), *nodes.values())
        donor = VGroup(Circle(radius=0.33, color=STABLE, stroke_width=3), label(r"giver", font_size=16,
                                                                                color=STABLE))
        donor.move_to(LEFT * 2.2 + DOWN * 0.4)
        donor[1].move_to(donor[0])
        chain = [it for it in kd["best"] if it["kind"] == "chain"][0]["pairs"]
        links = VGroup(Arrow(donor.get_center(), pos[chain[0]], buff=0.36, color=STABLE, stroke_width=5))
        for a, b in zip(chain, chain[1:]):
            links.add(Arrow(pos[a], pos[b], buff=0.36, color=STABLE, stroke_width=5))
        side = VGroup(
            label(r"a chain: \ someone gives a kidney \\ to a stranger, \ asking nothing", font_size=21,
                  color=STABLE),
            label(rf"with one chain: \ all {kd['with_chains']} patients", font_size=23, color=STABLE),
            label(r"a chain needn't be simultaneous: \\ each pair receives before it gives", font_size=20,
                  color=GREY_A),
            label(rf"2009: \ a chain of {k['first_chain_transplants']} transplants; \\ later one of "
                  rf"{k['large_chain_transplants']}", font_size=21, color=KIDNEY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.45)
        tag = published_tag(r"Rees et al., NEJM 360 (2009); \ Roth, Nobel lecture (2012)", corner=DR, font_size=13)
        with self.voiceover(
            "There is one more source. <bookmark mark='a'/> Some people give a kidney to a stranger, asking nothing "
            "in return. Such a gift can start a chain: the giver's kidney goes to one patient, that patient's donor "
            "gives to the next, and so on. <bookmark mark='b'/> In Agora's pool, one chain, with the cycles, gives "
            "a kidney to all eight patients. <bookmark mark='c'/> And a chain need not be done all at once, because "
            "each pair receives a kidney before its donor gives one: if a donor backs out, nobody is left worse off "
            "than before. <bookmark mark='d'/> In 2009 the surgeon Michael Rees reported the first long chain of "
            "this kind, with ten transplants; later chains reached thirty. Many patients have antibodies that rule "
            "out most kidneys, so few cycles exist, and chains are how they are found."
        ) as vo:
            self.play(FadeIn(g), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(donor), FadeIn(side[0]))
            for it in kd["best"]:
                if it["kind"] == "cycle":
                    ps = it["pairs"]
                    self.play(*[edges[(ps[i], ps[(i + 1) % len(ps)])].animate.set_color(KIDNEY).set_stroke(width=4)
                                for i in range(len(ps))], run_time=0.5)
            vo.wait_until("b")
            self.play(*[GrowArrow(a) for a in links], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
