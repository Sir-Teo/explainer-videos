from __future__ import annotations

from videos.philosophy.philosophy33.common import *  # noqa: F403


class Dynamic(VoiceoverScene):
    def construct(self):
        card = chapter_card(13, r"Ulysses and the sirens", r"How should you choose when your future self will want "
                                                            r"something else?", lit=(1956, 1990), part=PART)
        with self.voiceover("Chapter thirteen. Ulysses and the sirens."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.sirens()
        self.choosers()
        self.discount()
        self.hammond()

    def sirens(self):
        d = load("ulysses")
        head = label(r"A decision tree with a changing chooser", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        now = d["now"]
        assert now == {"past the sirens, free": 3, "past the sirens, bound": 2.5, "home": 1, "wrecked": 0}
        root = np.array([-5.6, 0.0, 0])
        mids = {"stay home": np.array([-2.2, 2.0, 0]), "sail bound": np.array([-2.2, 0.0, 0]),
                "sail free": np.array([-2.2, -2.0, 0])}
        later = np.array([0.8, -2.0, 0])
        leaves = {"home": np.array([1.2, 2.0, 0]), "past the sirens, bound": np.array([1.2, 0.0, 0]),
                  "past the sirens, free": np.array([4.0, -1.1, 0]), "wrecked": np.array([4.0, -2.9, 0])}
        sq = Square(0.4, color=AGENT, fill_opacity=0.5).move_to(root)
        sq2 = Square(0.4, color=RISK, fill_opacity=0.5).move_to(later)
        tl = label(r"now", font_size=16, color=AGENT).next_to(sq, DOWN, buff=0.15)
        tl2 = label(r"hearing the sirens", font_size=16, color=RISK).next_to(sq2, DOWN, buff=0.15)
        br = VGroup()
        for nm, p in mids.items():
            br.add(VGroup(Line(root, p, color=AGENT), label(nm, font_size=17, color=AGENT).next_to(
                p, UP, buff=0.12)))
        leaf = VGroup()
        for nm in ("home", "past the sirens, bound"):
            src = mids["stay home"] if nm == "home" else mids["sail bound"]
            leaf.add(VGroup(Line(src, leaves[nm], color=GREY_B),
                            label(f"{nm}: \\ {now[nm]}", font_size=17, color=GOAL).next_to(leaves[nm], RIGHT,
                                                                                            buff=0.1)))
        free = VGroup(Line(mids["sail free"], later, color=GREY_B),
                      Line(later, leaves["past the sirens, free"], color=GREY_B),
                      Line(later, leaves["wrecked"], color=GREY_B),
                      label(r"past the sirens, \ free: \ 3", font_size=17, color=GOAL).next_to(
                          leaves["past the sirens, free"], RIGHT, buff=0.1),
                      label(r"wrecked: \ 0", font_size=17, color=BAD).next_to(leaves["wrecked"], RIGHT, buff=0.1))
        note = label(r"values are Ulysses's preferences now; \ hearing the sirens, \ he will prefer the rocks",
                     font_size=17, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Choices are spread over time, and the chooser can change. <bookmark mark='a'/>Ulysses must sail past "
            "the sirens, whose song makes sailors steer onto the rocks. Now, he can stay home, sail bound to the "
            "mast, or sail free. <bookmark mark='b'/>Ranked by his present preferences: sailing past free is best, "
            "three; past but bound, two and a half, since the ropes hurt; home, one. <bookmark mark='c'/>If he sails "
            "free, a second choice comes later, when he hears the song: sail on, or steer to the sirens. "
            "<bookmark mark='d'/>Now he ranks the wreck lowest. But he knows that when he hears the song he will "
            "prefer it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sq), FadeIn(tl))
            vo.wait_until("a")
            self.play(Create(br))
            vo.wait_until("b")
            self.play(FadeIn(leaf))
            vo.wait_until("c")
            self.play(FadeIn(sq2), FadeIn(tl2), Create(free[:3]), FadeIn(free[3:]))
            vo.wait_until("d")
            self.play(FadeIn(note), Indicate(free[4], color=BAD))
        self.clear_scene()

    def choosers(self):
        d = load("ulysses")
        head = label(r"Three ways to choose", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        assert d["naive"] == "wrecked" and d["sophisticated"] == "past the sirens, bound"
        assert d["soph_plan"] == "sail bound" and d["resolute"] == "past the sirens, free"
        rows = [(r"naive", r"plans the best path, \ sail free and sail on, \ hears the song, \ re-chooses: \ "
                           r"wrecked \ (0)", BAD),
                (r"sophisticated", r"predicts his later choice and plans by backward induction: \ sail free leads to "
                                   r"the rocks, \ so sail bound \ (2.5)", EVID),
                (r"resolute", r"McClennen \ (1990): \ adopts the best plan and carries it out, \ even against his "
                              r"preference at the time: \ free and past \ (3)", AGENT),
                (r"the question", r"is resolve rational, \ or only something to wish for? \ the ropes are "
                                  r"precommitment: \ savings locks, \ Ulysses contracts in medicine", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6)
        with self.voiceover(
            "Decision theorists distinguish three choosers. <bookmark mark='a'/>The naive chooser plans the best "
            "path, sailing free and sailing on, then hears the song, chooses again with his new preferences, and is "
            "wrecked. <bookmark mark='b'/>The sophisticated chooser predicts what his later self will do, and plans "
            "by backward induction: sailing free leads to the rocks, so he has himself bound, and gets two and a "
            "half. <bookmark mark='c'/>Edward McClennen defended a third, the resolute chooser, in 1990: adopt the "
            "best plan and carry it out, even when the moment comes and you would rather not. He sails free and "
            "sails on, and gets three. <bookmark mark='d'/>Is resoluteness rational, or something we can only wish "
            "for? The sophisticated chooser's ropes are precommitment: the device behind savings plans that lock "
            "money away, and behind the Ulysses contracts of psychiatry, in which a patient asks in advance to be "
            "treated despite a later refusal."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def discount(self):
        d = load("discount")
        head = label(r"Why preferences change: \ hyperbolic discounting", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        assert d["hyp_switch_day"] == 9 and d["exp_consistent"] and d["exp_pick"][0] == "sooner"
        rows = d["rows"]
        assert rows[0]["hyp_sooner"] == 100.0 and rows[0]["hyp_later"] == 25.0
        assert rows[30]["hyp_sooner"] == 3.2258 and rows[30]["hyp_later"] == 4.1667
        ax = Axes(x_range=[0, 30, 5], y_range=[0, 2.2, 1], x_length=7.4, y_length=4.0, tips=False,
                  axis_config={"color": GREY_B, "font_size": 16}, x_axis_config={"include_numbers": True}
                  ).move_to([-2.0, -0.6, 0])
        xl = label(r"days until the \$100", font_size=17, color=GREY_A).next_to(ax.x_axis, DOWN, buff=0.4)
        yl = label(r"present value \ (log scale)", font_size=17, color=GREY_A).next_to(ax.y_axis, UP, buff=0.12)
        ylabs = VGroup(*[label(str(10 ** k), font_size=15, color=GREY_A).next_to(ax.c2p(0, k), LEFT, buff=0.1)
                         for k in range(3)])

        def curve(key, col):
            return VMobject(color=col, stroke_width=3).set_points_smoothly(
                [ax.c2p(r["t"], math.log10(r[key])) for r in rows])
        hs, hl = curve("hyp_sooner", MONEY), curve("hyp_later", CAUSE)
        cl1 = label(r"\$100", font_size=16, color=MONEY).next_to(ax.c2p(0, 2.0), RIGHT, buff=0.15)
        cl2 = label(r"\$150, \ 5 days later", font_size=16, color=CAUSE).next_to(
            ax.c2p(30, math.log10(rows[30]["hyp_later"])), UP, buff=0.12).shift(LEFT * 0.6)
        cross = Dot(ax.c2p(9, 1.0), radius=0.09, color=WHITE)
        cl = label(r"day 9: \ a tie", font_size=16, color=WHITE).next_to(cross, UR, buff=0.08)
        f = VGroup(MathTex(r"\text{hyperbolic: } \frac{x}{1 + t}", font_size=26, color=MONEY),
                   MathTex(r"\text{exponential: } x\,(0.9)^t", font_size=26, color=GREY_A)).arrange(
            DOWN, buff=0.25, aligned_edge=LEFT)
        side = stack([(r"\$100 on day $t$, \ or \$150 on day $t + 5$", GREY_A),
                      (r"from more than 9 days away: \ wait for the \$150", CAUSE),
                      (r"up close: \ take the \$100", MONEY),
                      (r"exponential discounting never reverses: \ \$100 from every distance", GREY_A),
                      (r"Strotz \ (1956); \ Ainslie \ (1975)", HIST)], font_size=18, aligned_edge=LEFT, width=4.2,
                     buff=0.25)
        VGroup(f, side).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to([4.5, -0.3, 0])
        with self.voiceover(
            "One source of such changes is the way we discount the future. <bookmark mark='a'/>Choose between a "
            "hundred dollars on some day, and a hundred and fifty five days later. <bookmark mark='b'/>Discount "
            "hyperbolically, dividing by one plus the delay in days, as experiments by George Ainslie and others "
            "suggest people do. From more than nine days away the later hundred and fifty is worth more. "
            "<bookmark mark='c'/>But as the day approaches the two curves cross: at nine days they tie, and up close "
            "the hundred dollars now wins. The plan made a month ahead is abandoned. <bookmark mark='d'/>Exponential "
            "discounting, multiplying by point nine for each day, ranks the pair the same way from every distance; "
            "Robert Strotz showed in 1956 that it is the only discounting that never reverses. "
            "<bookmark mark='e'/>A hyperbolic discounter is a sequence of selves with different preferences, and "
            "faces Ulysses's problem every day."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(ylabs))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Write(f[0]))
            self.play(Create(hs), Create(hl), FadeIn(cl1), FadeIn(cl2), run_time=2)
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(cross), FadeIn(cl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(Write(f[1]), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def hammond(self):
        head = label(r"Consistency over time, \ and independence", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"Hammond \ (1988)", r"an agent who is consequentialist at every node \ and dynamically "
                                      r"consistent \ must satisfy independence", PREF),
                (r"so", r"Allais's and Buchak's agents face a choice: \ be sophisticated and pay to avoid "
                        r"information, \ or be resolute, \ or abandon a plan", RISK),
                (r"Machina \ (1989)", r"non-expected-utility agents should not be consequentialist: \ what might "
                                      r"have happened can rationally matter", EVID),
                (r"the link", r"independence, \ the sure-thing principle and dynamic consistency stand or fall "
                              r"together", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.6)
        with self.voiceover(
            "Dynamic choice turns into an argument about expected utility itself. <bookmark mark='a'/>Peter Hammond "
            "proved in 1988 that an agent who judges each choice only by its consequences from that point on, and "
            "never plans what it will not carry out, must satisfy independence. <bookmark mark='b'/>So Allais's and "
            "Buchak's agents face a dilemma: be sophisticated, and sometimes pay to avoid information or to bind "
            "themselves; be resolute; or abandon plans. <bookmark mark='c'/>Mark Machina replied in 1989 that such "
            "agents need not be consequentialist: what might have happened, the risk already borne, can rationally "
            "matter. <bookmark mark='d'/>Independence, the sure-thing principle and consistency over time stand or "
            "fall together. The next chapter shows the price in one of them: information that hurts."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
