from __future__ import annotations

import numpy as np

from videos.psychology.psych2.common import *  # noqa: F403


class Shuffle(VoiceoverScene):
    def construct(self):
        self.card()
        self.peirce()
        self.balance()
        self.yardstick()

    def card(self):
        card = chapter_card(5, r"Shuffling the cards", r"Who should decide who gets the treatment?",
                            lit={1884: r"Peirce \& Jastrow shuffle a deck", 1935: r"Fisher's \emph{Design of "
                                 r"Experiments}"}, part=PART, scale=("group",), marr=("what",))
        with self.voiceover(
            "Chapter five. Shuffling the cards."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def peirce(self):
        pj = archive.PEIRCE_JASTROW_1884.data
        hc = history_card(1884, r"Charles Peirce and Joseph Jastrow, Johns Hopkins", r"can a person feel a "
                          r"difference in pressure too small to be sure of?", color=P.ARCHIVE, width=10.6,
                          font_size=28).to_edge(UP, buff=0.35)
        # the apparatus, in outline: a finger under a balance beam, a screen, an operator with a deck
        beam = Line([-5.6, -0.6, 0], [-2.4, -0.6, 0], color=GREY_A, stroke_width=5)
        fulcrum = Triangle(stroke_width=0, fill_color=GREY_B, fill_opacity=1).scale(0.22).move_to([-4.0, -0.82, 0])
        pan = VGroup(Line([-2.6, -0.6, 0], [-2.6, -1.3, 0], color=GREY_A, stroke_width=2),
                     Rectangle(width=0.9, height=0.12, stroke_width=0, fill_color=GREY_A, fill_opacity=1)
                     .move_to([-2.6, -1.36, 0]))
        weight = Rectangle(width=0.45, height=0.3, stroke_width=0, fill_color=P.ACCENT, fill_opacity=1)
        weight.move_to([-2.6, -1.15, 0])
        finger = RoundedRectangle(width=1.3, height=0.34, corner_radius=0.16, stroke_width=0, fill_color=P.HUMAN,
                                  fill_opacity=0.9).move_to([-5.9, -0.36, 0])
        screen = Rectangle(width=0.14, height=2.3, stroke_width=0, fill_color=GREY_C, fill_opacity=1)
        screen.move_to([-4.75, -0.45, 0])
        s_lab = label(r"a screen", font_size=22, color=GREY_B).next_to(screen, UP, buff=0.1)
        subj = label(r"the subject", font_size=24, color=P.HUMAN).move_to([-6.0, -1.0, 0])
        oper = label(r"the operator", font_size=24, color=GREY_A).move_to([-1.2, -1.1, 0])
        rig = VGroup(beam, fulcrum, pan, weight, finger, screen, s_lab, subj, oper)
        # the deck
        rng = np.random.default_rng(1884)
        colors = [RED_CARD] * 12 + [BLACK_CARD] * 13
        rng.shuffle(colors)
        deck = VGroup(*[card(c, 0.25, 0.4) for c in colors]).arrange_in_grid(rows=1, buff=0.04)
        deck.move_to([3.15, 0.6, 0])
        d_lab = label(r"a pack of 25: \ 12 red, 13 black, well shuffled", font_size=26).next_to(deck, UP, buff=0.2)
        rule = VGroup(
            VGroup(card(RED_CARD, 0.3, 0.44), label(r"heavier first, then lighter", font_size=26)).arrange(RIGHT, buff=0.25),
            VGroup(card(BLACK_CARD, 0.3, 0.44), label(r"lighter first, then heavier", font_size=26)).arrange(RIGHT, buff=0.25),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(deck, DOWN, buff=0.3).align_to(deck, LEFT)
        conf = label(r"the subject answers, and rates his confidence: \ 0, 1, 2 or 3", font_size=24, color=GREY_A)
        conf.next_to(rule, DOWN, buff=0.22).align_to(deck, LEFT)
        keep_in_frame(conf)
        quote = quote_card(r"Any possible psychological guessing of what change the operator was likely to select "
                           r"was avoided.", r"Peirce and Jastrow, \emph{On small differences in sensation} (1884)",
                           width=12.4, font_size=26).to_edge(DOWN, buff=0.75)
        src = historical_tag(archive.PEIRCE_JASTROW_1884.cite)
        assert pj["trials_per_pack"] == 25
        with self.voiceover(
            "Baltimore, 1884, twenty years before Hans. The philosopher Charles Peirce and his student Joseph "
            "Jastrow want to know whether a person can feel a difference in pressure so small that they'd swear "
            "they were guessing. <bookmark mark='a'/> The subject rests a fingertip under a balance. Behind a "
            "screen, the operator adds a little weight and takes it off, or takes it off and adds it, and the "
            "subject says which. <bookmark mark='b'/> But who decides the order? If the operator chooses, he'll "
            "fall into a pattern, as you did with your coin, and the subject may pick the pattern up. So they "
            "took the choice away from both of them. <bookmark mark='c'/> A pack of twenty-five playing cards, "
            "shuffled. Red: heavier first. Black: lighter first. The operator turns a card and does what it "
            "says. <bookmark mark='d'/> In their words: any possible psychological guessing of what change the "
            "operator was likely to select was avoided. <bookmark mark='e'/> A screen so the subject can't read "
            "the operator, and a deck so that nobody can predict the next trial. As far as anyone has found, it "
            "is the first randomized experiment in any science. Agriculture and medicine took up the idea forty "
            "and sixty years later."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(src))
            vo.wait_until("a")
            self.play(FadeIn(rig))
            self.play(weight.animate(rate_func=there_and_back).shift(UP * 0.5), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(d_lab), LaggedStart(*[FadeIn(c_, shift=DOWN * 0.15) for c_ in deck], lag_ratio=0.06),
                      run_time=3.0)
            self.play(FadeIn(rule), FadeIn(conf))
            vo.wait_until("d")
            self.play(FadeIn(quote, shift=UP * 0.2))
        self.clear_scene()

    def balance(self):
        d = load("balance")
        ss, eye = d["self_selected"], d["by_eye"]
        head = heading(rf"Shuffle {d['n']} people into two groups, {fmt_int(d['shuffles'])} times")
        edges = np.asarray(d["edges"])
        top = float(max(d["hist_age"].max(), d["hist_keen"].max())) * 1.15
        A = axes([-1.0, 1.0], [0, top], x_length=8.4, y_length=3.7,
                 xlabel=r"difference between the two groups, in standard deviations", xticks=[-1, -0.5, 0, 0.5, 1],
                 center=[1.6, -0.2, 0])
        ax = A.ax
        h_age = hist(ax, edges, d["hist_age"], CTRL, 0.6)
        h_keen = hist(ax, edges, d["hist_keen"], P.ACCENT, 0.45)
        leg = legend([(CTRL, r"age (measured)"), (P.ACCENT, r"eagerness (never measured)")], font_size=24)
        leg.next_to(ax.c2p(1.0, top), DL, buff=0.1)
        zero = DashedLine(ax.c2p(0, 0), ax.c2p(0, top), color=TRUTH, stroke_width=2)

        def flag(x, lines, color, up, label_x=None):
            p0 = ax.c2p(x, 0)
            ln = Line(p0, p0 + UP * up, color=color, stroke_width=4)
            t = VGroup(*[label(t_, font_size=24, color=color) for t_ in lines]).arrange(DOWN, aligned_edge=RIGHT,
                                                                                     buff=0.06)
            anchor = np.array([ax.c2p(x if label_x is None else label_x, 0)[0], ln.get_end()[1], 0])
            t.next_to(anchor, LEFT, buff=0.15).align_to(anchor, UP)
            return VGroup(ln, keep_in_frame(t))

        left_most = min(ss["speed"], eye["speed"])
        f_self = flag(ss["speed"], (r"people choose their group:", rf"${ss['speed']:.2f}$ SD in speed"), BIAS, 2.9,
                      left_most)
        f_eye = flag(eye["speed"], (r"the experimenter chooses,", rf"``at random'': \ ${eye['speed']:.2f}$ SD"),
                     "#F2A65A", 1.5, left_most)
        facts = VGroup(
            label(rf"the shuffle: \ centred on 0, \ spread ${d['sd_keen']:.2f}$", font_size=30, color=TRUTH),
            MathTex(rf"\sqrt{{4 / n}} = {d['theory_sd']:.2f}", font_size=34, color=GREY_A),
        ).arrange(RIGHT, buff=0.6).to_edge(DOWN, buff=0.75)
        tag = simulated_tag()
        with self.voiceover(
            "What does a shuffle buy when the units are people? Take two hundred from the Pool, and deal them "
            "into two groups by shuffling. Then compare the groups on something, say age. <bookmark mark='a'/> Do "
            "it five thousand times. The difference between the groups is sometimes a little positive, "
            "sometimes a little negative, and centred on zero. <bookmark mark='b'/> Now the important part. Do "
            "the same for eagerness, which no experimenter measured, or even knew about. Same picture. The "
            "shuffle balances what you measured, what you didn't, and what you've never heard of, all at once. "
            "That's the answer to the endless list of confounds. <bookmark mark='c'/> Compare the alternatives. "
            "Let people choose their own group, and the groups differ in speed by "
            f"{abs(ss['speed']):.1f} standard deviations before anything is done. <bookmark mark='d'/> Let the "
            "experimenter assign them, trying to be fair but with a slight eye for who looks alert: "
            f"{abs(eye['speed']):.1f}. <bookmark mark='e'/> And the shuffle gives a second thing that neither of "
            "those can. Its spread is known in advance. With n people it's the square root of four over n. Chance "
            "is the one cause of a difference whose size you can calculate."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(h_age, lag_ratio=0.03), Create(zero), FadeIn(leg[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(h_keen, lag_ratio=0.03), FadeIn(leg[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(f_self, shift=DOWN * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(f_eye, shift=DOWN * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(facts, shift=UP * 0.15))
        self.clear_scene()

    def yardstick(self):
        d = load("balance")
        st = d["study"]
        head = heading(r"The deck that assigns is the deck that judges")
        edges, counts = np.asarray(d["null_edges"]), np.asarray(d["null_hist"])
        top = float(counts.max()) * 1.15
        A = axes([-14, 14], [0, top], x_length=8.6, y_length=3.6, xticks=[-10, -5, 0, 5, 10],
                 xlabel=r"difference between the groups if the game did nothing (ms)", center=[-2.0, -0.55, 0])
        ax = A.ax
        bars = hist(ax, edges, counts, GREY_B, 0.6)
        obs = Line(ax.c2p(st["effect"], 0), ax.c2p(st["effect"], top * 0.95), color=TREAT, stroke_width=5)
        mirror = DashedLine(ax.c2p(-st["effect"], 0), ax.c2p(-st["effect"], top * 0.95), color=TREAT, stroke_width=2)
        obs_lab = label(rf"${st['effect']:.1f}$", font_size=28, color=TREAT).next_to(obs, UP, buff=0.08)
        rng = np.random.default_rng(1935)
        centres = (edges[:-1] + edges[1:]) / 2
        deals = rng.choice(centres, size=7, p=counts / counts.sum()) + rng.uniform(-0.3, 0.3, 7)
        hand = [RED_CARD] * 8 + [BLACK_CARD] * 8
        cards = VGroup(*[card(c, 0.3, 0.44) for c in hand]).arrange(RIGHT, buff=0.07)
        cards.next_to(A, UP, buff=0.25).set_x(ax.c2p(0, 0)[0])
        c_lab = label(r"deal again", font_size=24, color=GREY_A).next_to(cards, LEFT, buff=0.3)
        drops = VGroup(*[Dot(ax.c2p(v, top * 0.06), radius=0.08, color=WHITE) for v in deals])
        asked = VGroup(label(rf"this study: \ ${st['effect']:.1f}$ ms", font_size=34, color=TREAT),
                       label(r"the game, or the shuffle?", font_size=28, color=WHITE))
        asked.arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        steps = VGroup(
            wrapped_label(r"1. \ Suppose the game did nothing: every score would be the same whichever group its "
                          r"owner had landed in.", 4.4, 25, WHITE),
            wrapped_label(r"2. \ Reshuffle the labels 20,000 times and take the difference each time.", 4.4, 25,
                          WHITE),
            wrapped_label(rf"3. \ A difference this large turns up {100 * st['p_randomization']:.1f}\% of the time.",
                          4.4, 25, TREAT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([4.75, -0.35, 0])
        asked.next_to(steps, UP, buff=0.4).align_to(steps, LEFT)
        truth = label(rf"the effect planted in the Pool: \ ${st['true']:.0f}$ ms; \ {100 * d['coverage']:.0f}\% of "
                      rf"400 such intervals contain it", font_size=26, color=TRUTH).to_edge(DOWN, buff=0.75)
        tag = simulated_tag()
        with self.voiceover(
            "Here is that second gift at work. Give the game a real effect this time: in the Pool it now takes "
            f"eight milliseconds off. A randomized study of two hundred people finds a difference of "
            f"{abs(st['effect']):.1f}. Is that the game, or the luck of the shuffle? <bookmark mark='a'/> Ask "
            "what the shuffle alone can do. Suppose the game did nothing. Then each person's score would have "
            "been the same in either group, and the only thing that made the groups differ was the deal. "
            "<bookmark mark='b'/> So deal again. Shuffle the labels twenty thousand times, keeping every score "
            "where it is, and look at the differences. <bookmark mark='c'/> A difference as large as the real "
            f"one comes up about {100 * st['p_randomization']:.0f} times in a hundred. That's all a p value is, "
            "and the Statistics series builds this test in its tenth part. <bookmark mark='d'/> Notice what "
            "made it legitimate. We could reshuffle because the assignment really was a shuffle. If people had "
            "chosen their own groups, there'd be nothing to redo. Randomization is what gives the statistics "
            "something to stand on, and Ronald Fisher made that the foundation of experimental design in 1935."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            self.play(FadeIn(asked, shift=LEFT * 0.15), Create(obs), FadeIn(obs_lab))
            vo.wait_until("a")
            self.play(FadeIn(steps[0], shift=LEFT * 0.15), FadeIn(cards, lag_ratio=0.05), FadeIn(c_lab))
            for k in range(len(deals)):
                rng.shuffle(hand)
                self.play(*[c_.animate.set_fill(col) for c_, col in zip(cards, hand)], run_time=0.45)
                self.play(FadeIn(drops[k], shift=DOWN * 0.3), run_time=0.35)
            vo.wait_until("b")
            self.play(FadeIn(steps[1], shift=LEFT * 0.15), FadeOut(drops), FadeIn(bars, lag_ratio=0.05),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(Create(mirror), FadeIn(steps[2], shift=LEFT * 0.15), Indicate(obs, color=TREAT))
            vo.wait_until("d")
            self.play(FadeIn(truth, shift=UP * 0.15))
        self.clear_scene()
