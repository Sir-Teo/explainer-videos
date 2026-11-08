from __future__ import annotations

from videos.philosophy.philosophy31.common import *  # noqa: F403


class IIT(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"Integrated information", r"Is consciousness a system's irreducible cause-effect "
                                                           r"structure?", lit=(2004,), part=PART)
        with self.voiceover("Chapter ten. Integrated information."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.axioms()
        self.cuts()
        self.states()
        self.networks()

    def axioms(self):
        hc = history_card(2004, r"Giulio Tononi", r"`An Information Integration Theory of Consciousness'", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        hd = [r"\text{experience is \dots}", r"\text{so its substrate must \dots}"]
        rows = [(r"intrinsic: \ it exists for itself", r"have cause-effect power on itself"),
                (r"specific: \ this one, \ not another", r"specify one cause-effect state"),
                (r"unitary: \ one whole, \ not separate parts", r"be irreducible to its parts: \ $\Phi > 0$"),
                (r"definite: \ just these contents", r"be the maximum of $\Phi$ among overlapping candidates"),
                (r"structured: \ distinctions and relations", r"unfold a cause-effect structure")]
        cells = [[label(a, font_size=18, color=FEEL), label(b, font_size=18, color=FUNC)] for a, b in rows]
        grid = ValueGrid(hd, cells, col_w=[5.6, 6.6], cell_h=0.62, font_size=20).move_to([0, -0.6, 0])
        foot = label(r"IIT 4.0 \ (Albantakis et al., \ 2023): \ axioms of experience, \ postulates of physics",
                     font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Integrated information theory, due to Giulio Tononi, runs in the opposite direction from the others. "
            "It starts from experience itself. <bookmark mark='a'/>Every experience, it says, is intrinsic: it "
            "exists for itself. So its physical substrate must have cause-effect power on itself. "
            "<bookmark mark='b'/>Every experience is specific, this one and not another. So the substrate must "
            "specify one cause-effect state. <bookmark mark='c'/>Every experience is unified: you do not have one "
            "experience of the left half of the room and another of the right. So the substrate must be irreducible "
            "to its parts; a measure of that irreducibility is called phi. <bookmark mark='d'/>Every experience is "
            "definite, with just these contents, so the substrate is the set of elements with the most phi. "
            "<bookmark mark='e'/>And every experience is structured, so the substrate must unfold a structure of "
            "causes and effects. The theory's fourth version, of 2023, then says: the experience is that "
            "structure."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(grid.head), Create(grid.rule))
            for mk, r in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
            self.play(FadeIn(foot))
        self.clear_scene()

    def cuts(self):
        d = load("phi")
        head = label(r"Cutting a system, \ computed \ (a simplified $\Phi$)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        cuts = d["loop_cuts"]
        assert d["loop_state"] == [1, 1, 1]
        assert [(c["A"], c["ei"]) for c in cuts] == [([0], 1.0), ([1], 2.585), ([2], 2.0)]
        names = [r"\text{OR}", r"\text{AND}", r"\text{XOR}"]
        pos = [np.array([-3.6, 1.0, 0]), np.array([-5.0, -1.2, 0]), np.array([-2.2, -1.2, 0])]
        nodes = VGroup(*[VGroup(Circle(radius=0.45, color=FUNC, fill_opacity=0.15),
                                MathTex(n, font_size=22, color=FUNC)).move_to(p) for n, p in zip(names, pos)])
        state = VGroup(*[MathTex(r"1", font_size=22, color=SIG).next_to(nodes[k], UP if k == 0 else DOWN, buff=0.12)
                         for k in range(3)])
        edges = VGroup()
        for i in range(3):
            for j in range(3):
                if i != j:
                    a, b = pos[j], pos[i]
                    v = (b - a) / np.linalg.norm(b - a)
                    nrm = np.array([-v[1], v[0], 0]) * 0.08
                    edges.add(Arrow(a + v * 0.48 + nrm, b - v * 0.48 + nrm, buff=0, color=GREY_B, stroke_width=2,
                                    max_tip_length_to_length_ratio=0.12))
        lines = [DashedLine([-5.6, 0.25, 0], [-1.6, 0.25, 0], color=BAD),
                 DashedLine([-4.4, 1.6, 0], [-4.0, -2.0, 0], color=BAD),
                 DashedLine([-2.8, 1.6, 0], [-3.2, -2.0, 0], color=BAD)]
        hd = [r"\text{cut off}", r"\text{information lost}", r"\text{per element}"]
        cells = [[label(["OR", "AND", "XOR"][c["A"][0]], font_size=20, color=FUNC),
                  label(f"{c['ei']:.3f} bits", font_size=20, color=GREY_A),
                  label(f"{c['norm']:.3f}", font_size=20, color=OK if k == 0 else GREY_A)]
                 for k, c in enumerate(cuts)]
        grid = ValueGrid(hd, cells, col_w=[1.8, 2.6, 2.0], cell_h=0.6, font_size=19).move_to([3.4, 0.6, 0])
        res = stack([(r"the weakest cut: \ OR off on its own", OK),
                     (r"$\Phi = 1$ bit: \ the whole says more about its past than its parts do", GOAL)], font_size=19,
                    width=6.0, buff=0.18).move_to([3.4, -1.8, 0])
        foot = label(r"IIT 2.0 style \ (Balduzzi and Tononi, \ 2008), \ bipartitions only: \ not IIT 4.0's $\Phi$",
                     font_size=17, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Phi can be computed exactly for tiny systems, and the Reasoner does, with a simplified measure in the "
            "style of the theory's second version, labelled as such. <bookmark mark='a'/>Three logic gates, OR, "
            "AND and XOR, each reading the other two, all now in state one. <bookmark mark='b'/>Given that present "
            "state, the whole system constrains its own past: only some earlier states could have produced it. "
            "<bookmark mark='c'/>Now cut the system in two, and let each part constrain its own past, treating "
            "inputs across the cut as noise. The information lost is how much more the whole says about its past "
            "than the parts say separately. Cutting off the OR gate loses one bit. Cutting off AND loses two point "
            "five eight. Cutting off XOR, two. <bookmark mark='d'/>Phi is the information lost across the weakest "
            "cut, here one bit. The system is irreducible: no way of cutting it loses nothing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(nodes), Create(edges), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(state), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for k in range(3):
                self.play(Create(lines[k]), *[FadeIn(c) for c in grid.cell[k]], run_time=0.8)
                if k < 2:
                    self.play(FadeOut(lines[k]), run_time=0.4)
            vo.wait_until("d")
            self.play(FadeOut(lines[2]), Create(lines[0]), FadeIn(res))
        self.clear_scene()

    def states(self):
        d = load("states")
        head = label(r"$\Phi$ depends on the state, \ not only the wiring", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        rows = d["rows"]
        assert [r["pasts"] for r in rows] == [1, 1, 0, 0, 2, 2, 1, 1]
        assert [r["phi"] for r in rows] == [1.0, 1.0, None, None, 1.585, 1.0, 1.0, 1.0]
        hd = [r"\text{state (OR, AND, XOR)}", r"\text{possible pasts}", r"\Phi"]
        cells = [[MathTex(r"(" + r",\,".join(str(v) for v in r["state"]) + r")", font_size=24, color=SIG),
                  label(str(r["pasts"]), font_size=20, color=GREY_A),
                  label(f"{r['phi']:g}" if r["phi"] is not None else r"---", font_size=20,
                        color=OK if r["phi"] else GREY_B)] for r in rows]
        grid = ValueGrid(hd, cells, col_w=[3.6, 2.6, 1.6], cell_h=0.5, font_size=19).move_to([-2.6, -0.4, 0])
        side = stack([(r"two of the eight states have no past at all: \ the system can never get into them", GREY_A),
                      (r"in state $(1,0,0)$ its parts lose more: \ $\Phi = 1.585$", OK),
                      (r"on IIT, \ a change of state with the same wiring is a change of experience, \ and even "
                       r"inactive elements contribute", GOAL)], font_size=19, aligned_edge=LEFT, width=5.0,
                     buff=0.3).move_to([3.8, -0.3, 0])
        with self.voiceover(
            "Phi belongs to a system in a state, not just to its wiring. <bookmark mark='a'/>The Reasoner computes "
            "it for the loop in each of its eight states. <bookmark mark='b'/>Two of them have no possible past: "
            "no state leads to them, so once running the system never gets into them, and phi is undefined there. "
            "<bookmark mark='c'/>In five of the rest phi is one bit; in the state one, zero, zero, the parts lose "
            "more, and phi is one point five eight. <bookmark mark='d'/>For IIT that is a prediction: the same "
            "wiring in a different state is a different experience, and elements that are switched off still "
            "contribute, because what matters is what the system could have done."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            for r in range(8):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.35)
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def networks(self):
        d = load("phi")["networks"]
        head = label(r"$\Phi$ for four small systems", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        order = ["two separate pairs", "a feedforward chain", "OR, AND, XOR loop", "a ring of four XORs"]
        assert [d[k]["phi"] for k in order] == [0.0, 0.0, 1.0, 1.0]
        pics = VGroup()
        for k, name in enumerate(order):
            n = d[name]["n"]
            ins = d[name]["inputs"]
            cx = -5.1 + 3.4 * k
            rad = 0.75
            pts = [np.array([cx + rad * np.cos(PI / 2 + i * TAU / n), 0.9 + rad * np.sin(PI / 2 + i * TAU / n), 0])
                   for i in range(n)]
            g = VGroup(*[Dot(p, radius=0.11, color=FUNC) for p in pts])
            for i, src in enumerate(ins):
                for j in src:
                    if j == i:
                        continue
                    v = pts[i] - pts[j]
                    if np.linalg.norm(v) < 1e-6:
                        continue
                    v = v / np.linalg.norm(v)
                    g.add(Arrow(pts[j] + v * 0.13, pts[i] - v * 0.13, buff=0, color=GREY_B, stroke_width=2,
                                max_tip_length_to_length_ratio=0.2))
            t = label(name, font_size=18, color=WHITE).move_to([cx, -0.4, 0])
            ph = MathTex(rf"\Phi = {d[name]['phi']:g}", font_size=30,
                         color=OK if d[name]["phi"] > 0 else GREY_B).move_to([cx, -1.0, 0])
            pics.add(VGroup(g, t, ph))
        foot = stack([(r"separate parts: \ a cut loses nothing \quad a feedforward chain: \ cut at the source", GREY_A),
                      (r"loops make $\Phi$: \ on IIT, \ only systems that feed back on themselves can be conscious",
                       GOAL)], font_size=20, buff=0.22).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The same measure on four systems. <bookmark mark='a'/>Two separate pairs of gates, each pair copying "
            "back and forth: cut between the pairs and nothing is lost. Phi is zero: two systems, not one. "
            "<bookmark mark='b'/>A feedforward chain, each gate copying the one before: cut it at the source and "
            "nothing is lost either. Phi is zero. <bookmark mark='c'/>The loop of three gates: one bit. And a ring "
            "of four XOR gates, each reading its two neighbours: one bit. <bookmark mark='d'/>The pattern is the "
            "theory's central claim. Only systems whose parts feed back on each other have phi, and so, on IIT, "
            "only such systems can be conscious. A feedforward system, however intelligent its behaviour, has none. "
            "The next chapter turns that claim against the theory."
        ) as vo:
            self.play(FadeIn(head))
            for mk, k in zip("abc", (0, 1, 2)):
                vo.wait_until(mk)
                self.play(FadeIn(pics[k]))
                if k == 2:
                    self.play(FadeIn(pics[3]))
            self.play(FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(FadeIn(foot[1]))
        self.clear_scene()
