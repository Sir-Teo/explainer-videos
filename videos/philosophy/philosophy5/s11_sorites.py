from __future__ import annotations

from videos.philosophy.philosophy5.common import *  # noqa: F403


class Sorites(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"The heap", r"When does a heap stop being a heap?", lit=(-340,), part=PART)
        with self.voiceover("Chapter ten. The heap."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.eubulides()
        self.formal()
        self.check()
        self.everywhere()
        self.brick()

    def eubulides(self):
        hc = history_card(r"4th c.\ BCE", r"Eubulides of Miletus", r"the heap \ (\textit{sōritēs}), \ the bald man "
                          r"\ (\textit{phalakros})", width=6.6, color=HIST).to_corner(UL, buff=0.35)
        rng = np.random.default_rng(3)
        grains = VGroup()
        piles = [1, 2, 3, 10, 40, 160]
        xs = [-5.4, -3.9, -2.4, -0.6, 1.7, 4.6]
        for k, x in zip(piles, xs):
            g = VGroup()
            w = 0.06 + 0.0045 * k
            hmax = min(1.3, 0.03 * k)
            for _ in range(k):
                dx = float(np.clip(rng.normal(0, w), -2.2 * w, 2.2 * w))
                y = -1.6 + max(0.0, 1 - abs(dx) / (2.2 * w)) * hmax * rng.uniform(0, 1) ** 0.6
                g.add(Dot([x + dx, y, 0], radius=0.035, color=HALF))
            grains.add(g)
        nums = VGroup(*[label(str(k), font_size=22, color=GREY_A).move_to([x, -2.3, 0]) for k, x in zip(piles, xs)])
        qs = VGroup(label(r"one grain is not a heap", font_size=26),
                    label(r"adding one grain to a non-heap never makes a heap", font_size=26),
                    label(r"so a million grains are not a heap", font_size=26, color=BAD)).arrange(
            DOWN, buff=0.22).move_to([0, 1.1, 0])
        with self.voiceover(
            "In the fourth century before our era, Eubulides of Miletus, a logician of the Megarian school, posed "
            "a series of puzzles. <bookmark mark='a'/>One grain of sand is not a heap. Two grains are not a heap. "
            "<bookmark mark='b'/>Adding a single grain to something that is not a heap never makes it a heap. "
            "<bookmark mark='c'/>So, one grain at a time, a million grains are not a heap. "
            "<bookmark mark='d'/>The Greek for heap, sōros, gave the puzzle its name: the sorites. Its twin is "
            "the bald man, losing his hairs one by one. Chrysippus, the Stoic, is said to have advised falling "
            "silent as the questions approached the boundary."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(qs[0]), FadeIn(grains[0]), FadeIn(grains[1]), FadeIn(nums[:2]))
            vo.wait_until("b")
            self.play(FadeIn(qs[1]), LaggedStart(*[FadeIn(g) for g in grains[2:]], lag_ratio=0.4), FadeIn(nums[2:]))
            vo.wait_until("c")
            self.play(FadeIn(qs[2]))
        self.clear_scene()

    def formal(self):
        n = 11
        heads = men_row([None] * n, width=11.6, r=0.24, y=1.2)
        idx = VGroup(*[MathTex(rf"B_{{{i}}}", font_size=24, color=GREY_A).next_to(h, DOWN, buff=0.18)
                       for i, h in enumerate(heads)])
        arrows = VGroup(*[CurvedArrow(heads[i].get_top() + UP * 0.1, heads[i + 1].get_top() + UP * 0.1,
                                      angle=-PI / 2.4, color=CONN, stroke_width=2.5, tip_length=0.12)
                          for i in range(n - 1)])
        prem = VGroup(MathTex(r"B_0", font_size=40, color=OK), label(r"man 0, with no hair, is bald", font_size=24),
                      MathTex(r"B_i \to B_{i+1} \quad (i = 0, \dots, n-1)", font_size=40, color=CONN),
                      label(r"tolerance: \ one more hair never makes the difference", font_size=24),
                      MathTex(r"\lnot B_n", font_size=40, color=BAD),
                      label(r"man $n$, with a full head, is not bald", font_size=24)).arrange_in_grid(
            3, 2, buff=(0.6, 0.3), col_alignments="rl").move_to([0, -1.6, 0])
        with self.voiceover(
            "Here is the bald man, made precise. <bookmark mark='a'/>Line up men by the number of hairs, and let "
            "B i say that man i is bald. <bookmark mark='b'/>Man zero has no hair, and is bald. "
            "<bookmark mark='c'/>Tolerance: for each i, if man i is bald, so is man i plus one. One hair never "
            "makes the difference. <bookmark mark='d'/>And man n, with a full head, is not bald. "
            "<bookmark mark='e'/>Modus ponens, applied n times, carries baldness down the line, all the way to the "
            "man who plainly is not bald."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(h) for h in heads], lag_ratio=0.08), FadeIn(idx))
            vo.wait_until("b")
            self.play(FadeIn(prem[0]), FadeIn(prem[1]), heads[0].face.animate.set_stroke(OK).set_fill(OK, 0.3))
            vo.wait_until("c")
            self.play(FadeIn(prem[2]), FadeIn(prem[3]))
            vo.wait_until("d")
            self.play(FadeIn(prem[4]), FadeIn(prem[5]), heads[-1].face.animate.set_stroke(BAD).set_fill(BAD, 0.3))
            vo.wait_until("e")
            for i in range(n - 1):
                self.play(Create(arrows[i]), heads[i + 1].face.animate.set_stroke(OK).set_fill(OK, 0.3),
                          run_time=0.35)
            self.play(Indicate(heads[-1], color=BAD, scale_factor=1.5))
        self.clear_scene()

    def check(self):
        d = load("sorites")
        s = d["small"]
        names = [r"B_0"] + [rf"B_{i} \to B_{{{i + 1}}}" for i in range(s["n"])] + [rf"\lnot B_{s['n']}"]
        rows = VGroup(*[MathTex(t, font_size=32) for t in names]).arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        rows.move_to([-4.0, -0.2, 0])
        marks = VGroup(*[label(r"drop it: \ consistent $\checkmark$", font_size=22, color=OK).next_to(r, RIGHT, buff=0.6)
                         for r in rows])
        all_ = label(rf"all {s['premises']} together: \ unsatisfiable", font_size=26, color=BAD).next_to(rows, UP,
                                                                                                    buff=0.4)
        all_.align_to(rows, LEFT)
        big = VGroup(label(rf"{d['big']['n'] + 1} men, \ {d['big']['premises']} premises", font_size=30, color=GOAL),
                     label(r"CDCL (Part 2): \ unsatisfiable", font_size=26, color=BAD),
                     label(rf"and each of the {d['big']['premises']} is needed:", font_size=26, color=OK),
                     label(r"drop any one, \ and a model exists", font_size=26, color=OK),
                     label(r"a minimal inconsistent set: \ the cutoff could be anywhere", font_size=24,
                           color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.3, -0.2, 0])
        with self.voiceover(
            "The Reasoner can check this exactly. <bookmark mark='a'/>With six men, there are seven premises. "
            "Together they are unsatisfiable. <bookmark mark='b'/>Drop any one of them, and the rest have a model. "
            "Drop a conditional, and the model draws the line exactly there. <bookmark mark='c'/>With a hundred and "
            f"one men, there are {d['big']['premises']} premises. The SAT solver from Part 2 finds them "
            "unsatisfiable, and then confirms that every single premise is needed. <bookmark mark='d'/>So the "
            "sorites is a minimal inconsistent set, and the trouble is that the line it forces us to draw could be "
            "anywhere. Nothing in the meaning of 'bald' picks a place."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(rows), FadeIn(all_))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.15))
            vo.wait_until("c")
            self.play(FadeIn(big[:4]))
            vo.wait_until("d")
            self.play(FadeIn(big[4]))
        self.clear_scene()

    def everywhere(self):
        head = label(r"Vagueness is the rule, \ not the exception", font_size=32, color=CONN).to_edge(UP, buff=0.5)
        words = [r"heap", r"bald", r"tall", r"red", r"child", r"rich", r"alive", r"species", r"mountain",
                 r"cloud", r"reasonable doubt", r"a person"]
        ws = VGroup(*[label(w, font_size=28, color=GOAL) for w in words]).arrange_in_grid(3, 4, buff=(0.9, 0.45))
        ws.next_to(head, DOWN, buff=0.6)
        law = label(r"the law draws lines by fiat: \ adulthood at 18, \ not at `mature enough'", font_size=24,
                    color=GREY_A).next_to(ws, DOWN, buff=0.6)
        tol = label(r"Crispin Wright (1975): \ tolerance seems built into the meaning of such words", font_size=24,
                    color=GREY_A).next_to(law, DOWN, buff=0.25)
        with self.voiceover(
            "This is not a curiosity about sand. <bookmark mark='a'/>Almost every word we use is vague in this way: "
            "tall, red, child, rich, alive, species, mountain, cloud, reasonable doubt, and even person. "
            "<bookmark mark='b'/>The law, which needs lines, draws them by fiat: you are an adult at eighteen, not "
            "when you are mature enough. <bookmark mark='c'/>And Crispin Wright argued in 1975 that tolerance is "
            "part of what such words mean: we learn 'red' by looking, and a difference too small to see cannot "
            "make the difference between red and not red."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(w, scale=0.8) for w in ws], lag_ratio=0.12), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(law))
            vo.wait_until("c")
            self.play(FadeIn(tol))
        self.clear_scene()

    def brick(self):
        w = wall(upto=5, current=5).scale(0.42).move_to([-3.65, -0.2, 0])
        wc = wall_card(5, width=6.4, font_size=22).move_to([3.3, -0.2, 0])
        q = label(r"three ways out: \ a sharp cutoff, \ a gap, \ or a new logic \ (Chapters 11--13)", font_size=24,
                  color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "This is the fifth brick in the Wall. <bookmark mark='a'/>The dream: sharp concepts for a vague world, "
            "a logic in which every sentence is simply true or false. The wall: tolerance, bivalence and classical "
            "logic cannot all be kept. <bookmark mark='b'/>What it forces is a choice. Either there is a sharp "
            "cutoff after all, or some sentences fall into a gap, or we reason with a different logic. The next "
            "three chapters price each option."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(wc))
            vo.wait_until("b")
            self.play(FadeIn(q))
        self.clear_scene()
