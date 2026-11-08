from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403

LEVEL = {"calm": 0, "hurt": 2, "soothed": 1}


class Function(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Minds as machine tables", r"Is pain a role that anything could play?", lit=(1967,),
                            part=PART)
        with self.voiceover("Chapter three. Minds as machine tables."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.table()
        self.lockstep()
        self.varieties()
        self.ramsey()

    def table(self):
        hc = history_card(1967, r"Hilary Putnam", r"`Psychological Predicates'", width=5.2, color=HIST).to_corner(
            UL, buff=0.3)
        T = M.TABLE
        hd = [r"\text{state} \backslash \text{input}"] + [rf"\text{{{i}}}" for i in M.INPUTS]
        cells = []
        for s in M.STATES:
            row = [label(s, font_size=19, color=MIND)]
            for i in M.INPUTS:
                opts = T[(s, i)]
                txt = r"; \ ".join(f"{p:g}: {n}, {o}" for p, n, o in opts)
                row.append(label(txt, font_size=14, color=GREY_A))
            cells.append(row)
        grid = ValueGrid(hd, cells, col_w=[1.7, 3.6, 3.0, 3.6], cell_h=0.6, font_size=18).move_to([0, 0.0, 0])
        foot = stack([(r"pain \ = \ the state that is caused by damage, \ causes wincing, \ and is relieved by aspirin",
                       FUNC),
                      (r"defined by its relations, \ not by what it is made of", GOAL)], font_size=21,
                     buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "In 1967 Putnam proposed that pain is a functional state: a state defined by what causes it and what it "
            "causes, like a state of a machine defined by its machine table. <bookmark mark='a'/>Here is a small "
            "probabilistic machine table for a pain role. Three states: calm, hurt and soothed. Three inputs: a "
            "bump, nothing, or an aspirin. Each entry gives the chances of the next state and the output. A bump "
            "makes a calm creature hurt, nine times in ten, and it says ouch. Hurt and given aspirin, it is usually "
            "soothed, and sighs. <bookmark mark='b'/>On this view, the hurt state is the pain: whatever state is "
            "caused by damage, causes wincing and saying ouch, and is relieved by aspirin. "
            "<bookmark mark='c'/>It is defined by its relations to inputs, outputs and other states, not by what it is "
            "made of."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(3):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def lockstep(self):
        d = load("realizers")
        head = label(r"One role, \ two substrates, \ built", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["steps"] == 1000 and d["agree"] == 1000
        assert d["outputs"] == {"carry on": 468, "say ouch": 282, "sigh": 70, "wince": 180}
        trace = [r for r in d["trace"] if 9 <= r["t"] <= 17]
        assert len(trace) == 9 and trace[1]["input"] == "bump" and trace[1]["output"] == "say ouch"
        # neural panel
        units = VGroup(*[Circle(radius=0.36, color=PHYS, fill_opacity=0.1).move_to([-5.0 + 1.0 * k, 0.6, 0])
                         for k in range(3)])
        ulab = VGroup(*[label(s, font_size=15, color=GREY_A).next_to(u, DOWN, buff=0.12) for s, u in
                        zip(M.STATES, units)])
        ntitle = label(r"threshold units", font_size=20, color=PHYS).next_to(units, UP, buff=0.35)
        # hydraulic panel
        tank = Rectangle(width=1.4, height=2.2, color=PHYS).move_to([4.2, 0.6, 0])
        water = Rectangle(width=1.36, height=0.01, stroke_width=0, fill_color=PHYS, fill_opacity=0.6).align_to(
            tank, DOWN).set_x(4.2)
        ticks = VGroup(*[label(f"{v} L", font_size=14, color=GREY_A).move_to(
            [tank.get_left()[0] - 0.4, tank.get_bottom()[1] + 0.95 * v, 0]) for v in (0, 1, 2)])
        htitle = label(r"a water tank", font_size=20, color=PHYS).next_to(tank, UP, buff=0.35)
        inp = label(r"input", font_size=20, color=BEHAV).move_to([0, 1.6, 0])
        out = label(r"output", font_size=20, color=BEHAV).move_to([0, -0.4, 0])
        foot = stack([(r"1000 steps, \ the same inputs and random draws: \ outputs agree 1000 times out of 1000", OK),
                      (r"`carry on' 468, \ `say ouch' 282, \ `wince' 180, \ `sigh' 70 \ --- in both", GREY_A),
                      (r"physically, \ the two states never look alike: \ a pattern of units, \ a level of water",
                       GOAL)], font_size=20, aligned_edge=LEFT, width=12.0, buff=0.2).to_edge(DOWN, buff=0.35)

        def set_state(state):
            k = M.STATES.index(state)
            anims = [u.animate.set_fill(opacity=0.85 if j == k else 0.1) for j, u in enumerate(units)]
            h = 0.01 + 0.95 * LEVEL[state]
            anims.append(water.animate.stretch_to_fit_height(h).align_to(tank, DOWN))
            return anims

        with self.voiceover(
            "The Reasoner builds the same role twice. <bookmark mark='a'/>Once in a network of threshold units: the "
            "state is which of three units is on, and a unit for each table entry fires only when the state, the "
            "input and the random draw all match it. <bookmark mark='b'/>And once in water: the state is the level in "
            "a tank, empty for calm, one litre for soothed, two for hurt, and the table is a set of valves. "
            "<bookmark mark='c'/>Feed them the same inputs and the same random draws. A bump: the units switch to "
            "hurt, the tank fills to two litres, and both say ouch. Aspirin: both are soothed, and both sigh. "
            "<bookmark mark='d'/>Over a thousand steps the outputs agree a thousand times out of a thousand: carry "
            "on four hundred and sixty-eight times, ouch two hundred and eighty-two, wince a hundred and eighty, "
            "sigh seventy, in both. <bookmark mark='e'/>Yet physically the two never look alike: a pattern of "
            "electrical units in one, a level of water in the other. If pain is the role, both are in pain, or "
            "neither is. That is functionalism's promise, and, as the next chapters show, its problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(units), FadeIn(ulab), FadeIn(ntitle), *set_state("calm"))
            vo.wait_until("b")
            self.play(Create(tank), FadeIn(htitle), FadeIn(ticks))
            vo.wait_until("c")
            cur_in = cur_out = None
            for r in trace:
                ni = label(r["input"], font_size=22, color=BEHAV).next_to(inp, DOWN, buff=0.15)
                no = label(rf"`{r['output']}' \ (both)", font_size=22, color=BEHAV).next_to(out, DOWN, buff=0.15)
                state = {"units 100": "calm", "units 010": "hurt", "units 001": "soothed"}[r["neural"]]
                assert f"{LEVEL[state]} litres" == r["hydraulic"]
                anims = set_state(state)
                if cur_in is None:
                    anims += [FadeIn(inp), FadeIn(out), FadeIn(ni), FadeIn(no)]
                else:
                    anims += [Transform(cur_in, ni), Transform(cur_out, no)]
                self.play(*anims, run_time=0.8)
                if cur_in is None:
                    cur_in, cur_out = ni, no
            vo.wait_until("d")
            self.play(FadeIn(foot[0]), FadeIn(foot[1]))
            vo.wait_until("e")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def varieties(self):
        head = label(r"Functionalism, \ and its varieties", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"machine functionalism", r"Putnam \ (1967): \ mental states are states of a probabilistic automaton",
             FUNC),
            (r"analytic functionalism", r"Lewis \ (1972), \ Armstrong \ (1968): \ folk psychology defines the roles; \ "
                                        r"science finds what plays them", MIND),
            (r"the Ramsey--Lewis method", r"write the theory with mental terms as variables: \ pain is whatever occupies "
                                          r"the pain place in it", SYM),
            (r"role or realizer?", r"is pain the role, \ or the physical state that plays it in us?", PHYS),
            (r"the worries ahead", r"the Chinese room, \ Blockhead, \ the China brain: \ can the role be played with "
                                   r"no one home?", BAD),
        ]
        g = rows_table(rows, top=1.6, gap=0.45)
        with self.voiceover(
            "Functionalism came in several forms. <bookmark mark='a'/>Putnam's machine functionalism identified mental "
            "states with states of a probabilistic automaton. <bookmark mark='b'/>David Lewis and David Armstrong "
            "took the roles from ordinary psychology, the platitudes everyone knows about pain and belief, and left "
            "it to science to find what plays them. <bookmark mark='c'/>Lewis gave a method, after Ramsey: write down "
            "the whole theory, replace each mental term by a variable, and define pain as whatever occupies the pain "
            "place. <bookmark mark='d'/>That leaves a choice. Is pain the role itself, or the physical state that "
            "plays the role in us? <bookmark mark='e'/>And it leaves a worry, which the next three chapters press: "
            "could the role be played with no one home?"
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def ramsey(self):
        d = load("ramsey")
        head = label(r"The Ramsey--Lewis definition, \ counted", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        b, tk, th, wk = d["brain"], d["tank"], d["thermostat"], d["weak"]
        assert (b["candidates"], b["realizations"]) == (1806, 1) and b["found"][0]["hurt"] == ["h1", "h2", "h3"]
        assert (tk["candidates"], tk["realizations"], th["candidates"], th["realizations"]) == (6, 1, 6, 0)
        assert wk["without aspirin"]["realizations"] == 1 and wk["bumps only"]["realizations"] == 2
        f1 = MathTex(r"T(\text{calm},\ \text{hurt},\ \text{soothed})", font_size=30, color=MIND)
        f2 = MathTex(r"\exists x\, \exists y\, \exists z\;\; T(x, y, z)", font_size=30, color=FUNC)
        f3 = MathTex(r"\text{pain} \;=\; \text{the } y \text{ such that } \exists x\, \exists z\;\; T(x, y, z)",
                     font_size=30, color=GOAL)
        fs = VGroup(f1, f2, f3).arrange(DOWN, buff=0.3).move_to([0, 1.9, 0])
        fl = VGroup(label(r"the folk theory, \ all its platitudes", font_size=17, color=GREY_A).next_to(f1, LEFT, 0.4),
                    label(r"its Ramsey sentence", font_size=17, color=GREY_A).next_to(f2, LEFT, buff=0.4))
        col = {"calm": PHYS, "hurt": FEEL, "soothed": FUNC}
        micro = ["c1", "c2", "h1", "h2", "h3", "s1", "s2"]
        xs = {m: -3.6 + 1.2 * k for k, m in enumerate(micro)}
        dots = {m: VGroup(Dot([xs[m], -0.35, 0], radius=0.13, color=GREY_B),
                          MathTex(m[0] + "_" + m[1], font_size=22, color=GREY_A).move_to([xs[m], -0.8, 0]))
                for m in micro}
        dl = label(r"a `brain' of seven microstates", font_size=18, color=GREY_A).move_to([0, 0.25, 0])
        blobs = VGroup()
        for t, ms in b["found"][0].items():
            g = VGroup(*[dots[m] for m in ms])
            blobs.add(VGroup(SurroundingRectangle(g, color=col[t], buff=0.15, corner_radius=0.15),
                             label(t, font_size=18, color=col[t]).next_to(g, DOWN, buff=0.35)))
        res = label(rf"1 of {b['candidates']} assignments makes $T$ true: \ pain $= h_1 \vee h_2 \vee h_3$",
                    font_size=20, color=FEEL).move_to([0, -2.15, 0])
        hd = [r"\text{system and theory}", r"\text{states}", r"\text{assignments}", r"\text{make } T \text{ true}"]
        rows = [(r"the `brain', \ the whole theory", b), (r"a water tank, \ the whole theory", tk),
                (r"a thermostat, \ the whole theory", th),
                (r"the `brain', \ without the aspirin platitudes", {**wk["without aspirin"], "states": 7}),
                (r"the `brain', \ the bump platitudes only", {**wk["bumps only"], "states": 7})]
        cells = [[label(a, font_size=18, color=WHITE), label(str(r["states"]), font_size=19, color=GREY_A),
                  label(str(r["candidates"]), font_size=19, color=GREY_A),
                  label(str(r["realizations"]), font_size=21,
                        color=OK if r["realizations"] == 1 else BAD)] for a, r in rows]
        grid = ValueGrid(hd, cells, col_w=[5.6, 1.4, 2.2, 2.4], cell_h=0.55, font_size=19).move_to([0, -0.2, 0])
        foot = stack([(r"one: \ the terms name \quad none: \ nothing here is in pain \quad two: \ calm and soothed "
                       r"swap, \ and the terms fail to name", GOAL),
                      (r"a realization is a partition the dynamics respects: \ a bisimulation quotient \ (Part 4)",
                       GREY_A)], font_size=19, buff=0.18).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The Ramsey–Lewis method can be carried out, and counted. <bookmark mark='a'/>Take the folk theory of "
            "the pain role as a list of platitudes: from calm, a bump leads to hurt and ouch, or now and then "
            "leaves it calm; from hurt, aspirin leads to soothed and a sigh; and so on, every entry of the table. Replace the "
            "three mental terms by variables, and close them off: there exist x, y and z such that the platitudes "
            "hold of them. That is the theory's Ramsey sentence. Pain is defined as the y that does the job. "
            "<bookmark mark='b'/>Now take a brain with seven microstates, more states than the theory has terms. "
            "<bookmark mark='c'/>The Reasoner tries every way of grouping the seven into three kinds and naming the "
            "kinds calm, hurt and soothed: one thousand eight hundred and six assignments. Exactly one makes the "
            "theory true. Pain is the disjunction of three microstates, h one, h two or h three, multiply realized "
            "inside a single brain. <bookmark mark='d'/>The water tank has one realization out of six. A thermostat "
            "with three states, the same inputs and the same outputs, has none: nothing in it is in pain. And the "
            "theory matters. Leave out the aspirin platitudes and the brain still has one realization. Keep only the "
            "bump platitudes and it has two: calm and soothed can be swapped. <bookmark mark='e'/>Lewis held that "
            "the terms name only if the role is uniquely occupied; with two occupants, the theory does not say which "
            "state is calm. And a realization, in general, is a grouping of states that the dynamics respects, what "
            "Part 4 called a bisimulation: functional equivalence is bisimilarity, up to the grain the theory "
            "describes."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(f1), FadeIn(fl[0]))
            self.play(TransformFromCopy(f1, f2), FadeIn(fl[1]))
            self.play(FadeIn(f3))
            vo.wait_until("b")
            self.play(fs.animate.scale(0.8).move_to([0, 2.3, 0]), FadeOut(fl))
            self.play(FadeIn(dl), *[FadeIn(v) for v in dots.values()])
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(x[0]) for x in blobs], lag_ratio=0.3),
                      *[FadeIn(x[1]) for x in blobs])
            for t, ms in b["found"][0].items():
                for m in ms:
                    dots[m][0].set_color(col[t])
            self.play(FadeIn(res))
            vo.wait_until("d")
            self.play(FadeOut(VGroup(fs, dl, blobs, res, *dots.values())))
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(len(rows)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.5)
            vo.wait_until("e")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()
