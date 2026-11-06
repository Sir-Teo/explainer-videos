from __future__ import annotations

import random

from videos.philosophy.philosophy13.common import *  # noqa: F403

SICK, WELL, POS = "#F28EC2", "#4A5568", "#FFD166"
CLOTH = {"green": "#5FD38D", "blue": "#6FB7FF", "violet": "#C3A6FF"}


class Update(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Learning from evidence", r"How should credences change when you learn something?",
                            lit=(1763, 1965), part=PART)
        with self.voiceover("Chapter five. Learning from evidence."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rule()
        self.medical()
        self.diachronic()
        self.puzzles()
        self.jeffrey()

    def rule(self):
        head = label(r"Conditionalization: \ cut away what you've ruled out, \ and rescale", font_size=28,
                     color=CONN).to_edge(UP, buff=0.3)
        W, Hh = 6.0, 3.4
        ph, peh, pen = 0.4, 0.8, 0.3
        origin = np.array([-3.4, -0.9, 0])

        def rect(x0, x1, y0, y1, col, op):
            return Rectangle(width=(x1 - x0) * W, height=(y1 - y0) * Hh, stroke_color=WHITE, stroke_width=1.5,
                             fill_color=col, fill_opacity=op).move_to(
                origin + np.array([((x0 + x1) / 2 - 0.5) * W, ((y0 + y1) / 2 - 0.5) * Hh, 0]))
        HE = rect(0, ph, 0, peh, CRED, 0.75)
        HnE = rect(0, ph, peh, 1, CRED, 0.2)
        NE = rect(ph, 1, 0, pen, GREY_B, 0.6)
        NnE = rect(ph, 1, pen, 1, GREY_B, 0.15)
        tags = VGroup(label(r"$H$", font_size=26, color=CRED).next_to(HnE, UP, buff=0.1),
                      label(r"$\lnot H$", font_size=26, color=GREY_B).next_to(NnE, UP, buff=0.1),
                      MathTex(rf"P(H) = {ph}", font_size=24, color=CRED).next_to(HE, DOWN, buff=0.15).shift(
                          LEFT * 0.0),
                      label(r"shaded: \ $E$", font_size=22, color=WHITE).next_to(NE, DOWN, buff=0.15))
        eq = VGroup(
            MathTex(r"P_{\text{new}}(H) = P(H \mid E) = \frac{P(E \mid H)\,P(H)}{P(E)}", font_size=34),
            MathTex(rf"= \frac{{{peh} \times {ph}}}{{{peh} \times {ph} + {pen} \times {1 - ph:.1f}}} = "
                    rf"{peh * ph / (peh * ph + pen * (1 - ph)):.2f}", font_size=32, color=CRED),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, 1.0, 0])
        bayes = history_card(1763, r"Thomas Bayes", r"`An Essay towards solving a Problem in the Doctrine of Chances'",
                             width=5.6, color=HIST).move_to([3.4, -2.2, 0])
        with self.voiceover(
            "Credences must be coherent at each moment. How should they change from one moment to the next? "
            "<bookmark mark='a'/>Draw all the possibilities as a square, with area as credence. H takes four tenths "
            "of it. The evidence E covers most of H and less of not H. <bookmark mark='b'/>Now you learn E, and "
            "nothing else. Cut away every possibility outside E. <bookmark mark='c'/>What remains must have total "
            "credence one, so rescale it, keeping the proportions inside E. That is conditionalization. "
            "<bookmark mark='d'/>The new credence in H is the old conditional credence, which Bayes's theorem "
            "computes from the likelihoods: here, from point four to point six four. <bookmark mark='e'/>Thomas "
            "Bayes's essay, published after his death in 1763, gave the first version of the rule."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(HE, HnE, NE, NnE)), FadeIn(tags))
            vo.wait_until("b")
            self.play(FadeOut(HnE), FadeOut(NnE), FadeOut(tags[2]), FadeOut(tags[3]))
            vo.wait_until("c")
            tot = peh * ph + pen * (1 - ph)
            a1 = peh * ph / tot
            HE2 = rect(0, a1, 0, 1, CRED, 0.75)
            NE2 = rect(a1, 1, 0, 1, GREY_B, 0.6)
            self.play(Transform(HE, HE2), Transform(NE, NE2), tags[0].animate.next_to(HE2, UP, buff=0.1),
                      tags[1].animate.next_to(NE2, UP, buff=0.1), run_time=2)
            vo.wait_until("d")
            self.play(Write(eq[0]))
            self.play(FadeIn(eq[1]))
            vo.wait_until("e")
            self.play(FadeIn(bayes))
        self.clear_scene()

    def medical(self):
        d = load("update")["test"]
        head = label(r"A positive test", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        facts = stack([(r"1\% of people have the disease", SICK),
                       (r"the test catches 90\% of them", WHITE),
                       (r"and flags 9\% of the healthy", WHITE),
                       (r"you test positive: \ how likely is it that you are ill?", BET)], font_size=24,
                      aligned_edge=LEFT).move_to([-4.0, 1.4, 0])
        rnd = random.Random(13)
        idx = list(range(1000))
        rnd.shuffle(idx)
        sick = set(idx[:10])
        sick_pos = set(list(sick)[:9])
        well = [i for i in idx[10:]]
        well_pos = set(well[:89])
        dots = VGroup()
        for i in range(1000):
            r, c = divmod(i, 40)
            dots.add(Square(side_length=0.12, stroke_width=0, fill_color=WELL, fill_opacity=1).move_to(
                [-0.2 + c * 0.17, 2.3 - r * 0.17, 0]))
        sick_anim = [dots[i].animate.set_fill(SICK) for i in sick]
        pos_rings = VGroup(*[Square(side_length=0.17, stroke_color=POS, stroke_width=2).move_to(dots[i])
                             for i in sorted(sick_pos | well_pos)])
        counts = stack([(r"1{,}000 people: \ 10 ill, \ 990 well", WHITE),
                        (rf"positives: \ {d['per_1000']['sick_pos']:.0f} ill \ + \ {d['per_1000']['well_pos']:.0f} "
                         r"well", POS),
                        (rf"$P(\text{{ill}} \mid +) = \dfrac{{9}}{{9 + 89.1}} \approx {100 * d['posterior']:.1f}\%$",
                         CRED)], font_size=24, aligned_edge=LEFT).move_to([-4.0, -1.5, 0])
        foot = label(r"base-rate neglect: \ most doctors asked answered 95\% \ (Casscells et al.\ 1978); \ natural "
                     r"frequencies help \ (Gigerenzer)", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Bayes's theorem is easy to state and hard to feel. <bookmark mark='a'/>One percent of people have a "
            "disease. A test catches ninety percent of those who have it, and wrongly flags nine percent of those "
            "who don't. You test positive. How likely is it that you are ill? <bookmark mark='b'/>Picture a thousand "
            "people. <bookmark mark='c'/>Ten are ill. <bookmark mark='d'/>The test flags nine of the ten, and also "
            "about eighty nine of the nine hundred and ninety who are well. <bookmark mark='e'/>So of roughly ninety "
            "eight positives, nine are ill: about nine percent. <bookmark mark='f'/>When Ward Casscells and colleagues "
            "put a question like this to doctors at Harvard in 1978, the most common answer was ninety five percent. "
            "Ignoring the base rate is one of the commonest errors in reasoning, and Gerd Gigerenzer showed that "
            "counting people, as we just did, makes it far rarer."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(f) for f in facts], lag_ratio=0.4), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(dots, lag_ratio=0.002), FadeIn(counts[0]), run_time=2)
            vo.wait_until("c")
            self.play(*sick_anim)
            vo.wait_until("d")
            self.play(Create(pos_rings, lag_ratio=0.01), run_time=2)
            self.play(FadeIn(counts[1]))
            vo.wait_until("e")
            dim = VGroup(*[dots[i] for i in range(1000) if i not in sick_pos | well_pos])
            self.play(dim.animate.set_opacity(0.25), FadeIn(counts[2]))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()

    def diachronic(self):
        book = load("update")["diachronic"]
        head = label(r"Why conditionalize? \ The diachronic Dutch book", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        setup = stack([(r"today: \ $P(E) = 0.5$, \ \ $P(H \mid E) = 0.6$", CRED),
                       (r"your plan: \ if you learn $E$, \ adopt $P_{\text{new}}(H) = 0.4$ \ (not $0.6$)", INC)],
                      font_size=25).next_to(head, DOWN, buff=0.35)
        bets = stack([
            (r"bet 1, \ today: \ you buy a ticket on $H$, \ called off unless $E$, \ for $0.6$", WHITE),
            (r"bet 2, \ today: \ you buy a ticket paying $0.2$ if $E$, \ for $0.5 \times 0.2 = 0.1$", WHITE),
            (r"bet 3, \ if $E$: \ the bookie buys ticket 1 back at your new price, \ $0.4$", WHITE),
        ], font_size=23, aligned_edge=LEFT).next_to(setup, DOWN, buff=0.35)
        hd = [r"\text{world}", r"\text{bets 1 and 3}", r"\text{bet 2}", r"\text{net}"]
        rows = [[r"E,\ H", r"-0.6 + 0.4", r"+0.2 - 0.1", rf"{book['E&H']:+.1f}"],
                [r"E,\ \lnot H", r"-0.6 + 0.4", r"+0.2 - 0.1", rf"{book['E&~H']:+.1f}"],
                [r"\lnot E", r"0 \ (\text{called off})", r"-0.1", rf"{book['~E']:+.1f}"]]
        grid = ValueGrid(hd, rows, col_w=[1.6, 3.0, 2.4, 1.4], cell_h=0.5, font_size=24).next_to(bets, DOWN,
                                                                                               buff=0.35)
        for r in range(3):
            grid.cell[r][3].set_color(BAD)
        foot = stack([(r"Lewis (via Teller, \ 1973): \ any planned rule other than conditionalization can be booked",
                       GOAL),
                      (r"and by accuracy: \ conditionalizing maximizes expected accuracy \ (Greaves and Wallace, \ 2006)",
                       GREY_A)], font_size=21).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Why must updating go by conditionalization? David Lewis gave a Dutch book across time, first published by "
            "Paul Teller in 1973. <bookmark mark='a'/>Today your credence in E is one half, and your credence in H "
            "given E is point six. But your plan is that, if you learn E, your credence in H will be point four. "
            "<bookmark mark='b'/>The bookie sells you a ticket on H, called off unless E happens, for point six, your "
            "price. He also sells you a ticket that pays point two if E, for point one, again your price. If E "
            "happens, he buys the first ticket back at your new price, point four. <bookmark mark='c'/>Check it. If E "
            "happens, you lose point two on the first ticket and gain point one on the second. If E doesn't, the "
            "first bet is off and you lose the point one you paid for the second. <bookmark mark='d'/>Ten cents lost "
            "in every world. Any rule for updating other than conditionalization can be booked like this. "
            "<bookmark mark='e'/>And there is an accuracy version too: Hilary Greaves and David Wallace showed that "
            "conditionalizing maximizes your expected accuracy."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(setup))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bets], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule))
            for r in range(3):
                self.play(*[FadeIn(grid.cell[r][c]) for c in range(3)], run_time=0.7)
            vo.wait_until("d")
            self.play(*[FadeIn(grid.cell[r][3]) for r in range(3)])
            self.play(FadeIn(foot[0]))
            vo.wait_until("e")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def puzzles(self):
        head = label(r"Two puzzles for strict conditionalization", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        left = VGroup(
            label(r"old evidence \ (Glymour, \ 1980)", font_size=26, color=INC),
            label(r"Mercury's orbit was known before 1915", font_size=22),
            label(r"so $P(E) = 1$, \ and $P(\text{GR} \mid E) = P(\text{GR})$", font_size=22),
            label(r"yet it confirmed general relativity", font_size=22, color=GOAL),
            label(r"replies: \ counterfactual priors; \ learning that GR \textit{entails} $E$", font_size=20,
                  color=GREY_A)).arrange(DOWN, buff=0.22).move_to([-3.4, 0.2, 0])
        right = VGroup(
            label(r"certainty forever", font_size=26, color=INC),
            label(r"after conditionalizing, \ $P(E) = 1$", font_size=22),
            label(r"and no later conditionalizing can lower it", font_size=22),
            label(r"but evidence is rarely certain", font_size=22, color=GOAL),
            label(r"reply: \ Jeffrey's rule \ (next)", font_size=20, color=GREY_A)).arrange(DOWN, buff=0.22).move_to(
            [3.4, 0.2, 0])
        for g in (left, right):
            for m in g:
                if m.width > 6.2:
                    m.width = 6.2
        with self.voiceover(
            "Strict conditionalization has two well-known problems. <bookmark mark='a'/>The first is old evidence, "
            "raised by Clark Glymour. The odd orbit of Mercury was known long before Einstein. So its credence was "
            "already one, and conditioning on it cannot raise the credence of general relativity. Yet it was one of "
            "the theory's great confirmations. Bayesians reply with counterfactual credences, or say that what was "
            "really learned was that the theory entails the orbit. <bookmark mark='b'/>The second: once you "
            "conditionalize on E, its credence is one, and no further conditionalizing can ever lower it. But real "
            "evidence is rarely certain. Richard Jeffrey's rule was designed for that."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(m) for m in left], lag_ratio=0.5), run_time=5)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in right], lag_ratio=0.5), run_time=5)
        self.clear_scene()

    def jeffrey(self):
        j = load("update")["jeffrey"]
        hc = history_card(1965, r"Richard Jeffrey", r"\textit{The Logic of Decision}", width=4.8,
                          color=HIST).to_corner(UL, buff=0.35)
        scene = label(r"inspecting a cloth by candlelight", font_size=26, color=BET).next_to(hc, RIGHT, buff=0.6)
        colours = list(CLOTH)
        t = ValueTracker(0.0)

        def share(c):
            a, b = j["prior"][c], j["post"][c]
            return a + (b - a) * t.get_value()
        base = np.array([-5.0, -2.4, 0])

        def bars():
            g = VGroup()
            for i, c in enumerate(colours):
                h = 3.2 * share(c)
                g.add(Rectangle(width=0.9, height=max(h, 0.01), stroke_width=0, fill_color=CLOTH[c],
                                fill_opacity=0.85).move_to(base + np.array([i * 1.3, h / 2, 0])))
            return g
        bar_g = always_redraw(bars)
        vals = always_redraw(lambda: VGroup(*[DecimalNumber(share(c), num_decimal_places=2, font_size=24,
                                                            color=CLOTH[c]).next_to(bar_g[i], UP, buff=0.1)
                                              for i, c in enumerate(colours)]))
        names = VGroup(*[label(c, font_size=22, color=CLOTH[c]).move_to(base + np.array([i * 1.3, -0.3, 0]))
                         for i, c in enumerate(colours)])
        cap = label(r"$P(\text{colour})$", font_size=24, color=GREY_B).move_to(base + np.array([1.3, 4.3, 0]))
        sold = VGroup(*[MathTex(rf"P(\text{{sold}} \mid \text{{{c}}}) = {j['sold'][c]}", font_size=26,
                                color=CLOTH[c]) for c in colours]).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to(
            [2.6, 1.3, 0])
        rigid = label(r"rigidity: \ these stay fixed", font_size=22, color=GREY_A).next_to(sold, DOWN, buff=0.15)
        rule = MathTex(r"P_{\text{new}}(A) = \sum_i P(A \mid E_i)\, P_{\text{new}}(E_i)", font_size=34).move_to(
            [2.6, -0.6, 0])
        ps = always_redraw(lambda: VGroup(MathTex(r"P(\text{sold}) =", font_size=34, color=BET),
                                          DecimalNumber(sum(j["sold"][c] * share(c) for c in colours),
                                                        num_decimal_places=2, font_size=34, color=BET)).arrange(
            RIGHT, buff=0.2).move_to([2.6, -1.6, 0]))
        foot = label(r"Diaconis and Zabell (1982): \ Jeffrey's rule is the smallest change, \ in relative entropy, \ "
                     r"that fits the glimpse", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Richard Jeffrey's example. <bookmark mark='a'/>You inspect a cloth by candlelight, wondering whether it "
            "will sell. Before you look, your credences in its colour are point three green, point three blue, point "
            "four violet. <bookmark mark='b'/>Your chance of selling it depends on the colour: point four if green or "
            "blue, point eight if violet. So your credence that it sells is point five six. "
            "<bookmark mark='c'/>Then you glimpse it. The glimpse is not a proposition you can state; it just shifts "
            "your colour credences, to point seven green, point two five blue, point zero five violet. "
            "<bookmark mark='d'/>Jeffrey's rule: keep the credences conditional on each colour fixed, and average "
            "them with the new weights. <bookmark mark='e'/>Your credence that it sells falls to point four two. "
            "Strict conditionalization is the special case where one weight goes to one. <bookmark mark='f'/>And, "
            "returning to the geometry of chapter three: Persi Diaconis and Sandy Zabell showed that Jeffrey's rule "
            "is the smallest change in relative entropy that fits the glimpse. Updating is minimal revision."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(scene))
            vo.wait_until("a")
            self.play(FadeIn(bar_g), FadeIn(vals), FadeIn(names), FadeIn(cap))
            vo.wait_until("b")
            self.play(FadeIn(sold), FadeIn(ps))
            vo.wait_until("c")
            self.play(t.animate.set_value(1.0), run_time=3)
            vo.wait_until("d")
            self.play(FadeIn(rule), FadeIn(rigid))
            vo.wait_until("e")
            self.play(Indicate(ps, color=BET))
            vo.wait_until("f")
            self.play(FadeIn(foot))
        self.clear_scene()
