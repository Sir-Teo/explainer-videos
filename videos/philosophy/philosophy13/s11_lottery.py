from __future__ import annotations

from videos.philosophy.philosophy13.common import *  # noqa: F403

TICKET, WIN = "#4A5A70", "#FFD166"


class Lottery(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"The lottery and the preface", r"When does high credence make a belief?",
                            lit=(1961, 2017), part=PART)
        with self.voiceover("Chapter ten. The lottery and the preface."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.lockean()
        self.lottery()
        self.preface()
        self.price()
        self.stable()
        self.statistical()

    def lockean(self):
        head = label(r"Belief and credence", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"Parts 11 and 12: \ belief is all or nothing", WHITE),
            (r"this part: \ credence comes in degrees", WHITE),
            (r"how are they related?", GOAL),
        ], font_size=27, buff=0.3).next_to(head, DOWN, buff=0.5)
        thesis = MathTex(r"\text{believe } A \iff C(A) \geq t", font_size=44, color=CRED).next_to(rows, DOWN,
                                                                                               buff=0.6)
        tl = label(r"the Lockean thesis \ (Foley), \ with a threshold such as $t = 0.99$", font_size=24,
                   color=GREY_A).next_to(thesis, DOWN, buff=0.3)
        with self.voiceover(
            "We now have two pictures of the mind. <bookmark mark='a'/>In Parts 11 and 12, belief was all or "
            "nothing. <bookmark mark='b'/>In this part, credence comes in degrees. <bookmark mark='c'/>How are they "
            "related? <bookmark mark='d'/>The obvious answer: to believe is to have a high enough credence. Believe A "
            "just when your credence in A reaches some threshold, say point nine nine. Richard Foley called this the "
            "Lockean thesis, after Locke's talk of degrees of assent. It runs into two famous paradoxes."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(Write(thesis), FadeIn(tl))
        self.clear_scene()

    def lottery(self):
        d = load("lottery")["lottery"]
        hc = history_card(1961, r"Henry Kyburg", r"\textit{Probability and the Logic of Rational Belief}",
                          width=6.2, color=HIST).to_corner(UL, buff=0.35)
        tickets = VGroup()
        for i in range(d["n"]):
            r, c = divmod(i, 50)
            tickets.add(Rectangle(width=0.1, height=0.16, stroke_width=0, fill_color=TICKET, fill_opacity=1).move_to(
                [-6.2 + c * 0.135, 1.2 - r * 0.2, 0]))
        rows = stack([
            (rf"1{{,}}000 tickets, \ exactly one wins", WHITE),
            (rf"ticket 1 loses: \ credence {d['p_each_loses']} \ $\geq 0.99$: \ believe it", OK),
            (r"ticket 2 loses: \ believe it. \ \ \dots \ \ ticket 1000 loses: \ believe it", OK),
            (r"closure: \ believe that \textit{every} ticket loses", INC),
            (rf"but credence in that is {d['p_all_lose']:.0f}: \ you know some ticket wins", BAD),
        ], font_size=23, aligned_edge=LEFT, width=5.6).move_to([3.9, -0.6, 0])
        winner = tickets[617]
        with self.voiceover(
            "The lottery paradox, from Henry Kyburg in 1961. <bookmark mark='a'/>A fair lottery has a thousand "
            "tickets, and exactly one will win. <bookmark mark='b'/>Your credence that ticket one loses is point nine "
            "nine nine, over the threshold, so you believe it. <bookmark mark='c'/>Likewise for ticket two, and for "
            "every ticket up to a thousand. <bookmark mark='d'/>If rational belief is closed under conjunction, you "
            "believe that every ticket loses. <bookmark mark='e'/>But your credence in that is zero. You know that "
            "some ticket wins."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(tickets, lag_ratio=0.001), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(tickets[0].animate.set_fill(OK), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(tickets.animate.set_fill(OK), FadeIn(rows[2]), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(winner.animate.set_fill(WIN).scale(1.6), FadeIn(rows[4]))
        self.clear_scene()

    def preface(self):
        d = load("lottery")["preface"]
        head = label(r"The preface \ (Makinson, \ 1965)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 300, 50], y_range=[0, 1, 0.5], x_length=6.4, y_length=3.4, tips=False,
                  axis_config={"color": GREY_C, "include_numbers": True, "font_size": 18}).move_to([-2.8, -0.8, 0])
        xl = label(r"claims in the book", font_size=20, color=GREY_B).next_to(ax, DOWN, buff=0.35)
        curve = ax.plot(lambda n: d["each"] ** n, x_range=[0, 300], color=CRED, stroke_width=3)
        cl = MathTex(r"0.99^{n}", font_size=30, color=CRED).next_to(ax.c2p(60, 0.55), RIGHT, buff=0.1)
        end = Dot(ax.c2p(300, d["all"]), color=BAD, radius=0.08)
        el = MathTex(rf"{d['all']:.3f}", font_size=26, color=BAD).next_to(end, UP, buff=0.12)
        rows = stack([
            (rf"an author believes each of her {d['n']} claims, \ each at credence {d['each']}", WHITE),
            (r"if they are independent, \ the chance that all are true:", GREY_A),
            (rf"${d['each']}^{{{d['n']}}} \approx {d['all']:.3f}$", BAD),
            (r"so her preface says: \ `surely some errors remain'", BET),
            (r"and that is rational too", GOAL),
            (r"unlike the lottery: \ no statistics, \ just a long, \ careful book", GREY_A),
        ], font_size=23, aligned_edge=LEFT, width=5.6).move_to([3.7, -0.3, 0])
        with self.voiceover(
            "David Makinson's preface paradox, from 1965, needs no lottery. <bookmark mark='a'/>An author has "
            "checked each of the three hundred claims in her book carefully, and believes each one, with credence "
            "point nine nine. <bookmark mark='b'/>If the claims are independent, the chance that all three hundred "
            "are true is point nine nine to the three hundredth, <bookmark mark='c'/>about five percent. "
            "<bookmark mark='d'/>So in the preface she writes, as authors do, that errors surely remain. "
            "<bookmark mark='e'/>That is rational too. Yet the preface contradicts the conjunction of the book's "
            "claims. <bookmark mark='f'/>And unlike the lottery, nothing here is a matter of statistics: just a long, "
            "careful book."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(curve), FadeIn(cl), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(end), FadeIn(el), FadeIn(rows[2]))
            for mk, r in zip("def", rows[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def price(self):
        d = load("lottery")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.5, width=4.0, font_size=23,
                       center=[0, -0.4, 0], title=r"The Price List: \ the lottery triad")
        assert d["mcs"] == [["L1"], ["L2"], ["L3"]]
        positions = [(("L1",), r"high credence is not enough", r"statistical evidence alone does not justify belief "
                                                                r"(Nelkin; \ Smith)"),
                     (("L2",), r"Kyburg, \ Foley", r"believe each claim, \ not their conjunction"),
                     (("L3",), r"Christensen", r"belief need not be consistent; \ only credences must cohere")]
        with self.voiceover(
            "The Reasoner sets out the lottery as a Price List. <bookmark mark='a'/>Three claims. A credence of point "
            "nine nine or more suffices for belief. Rational belief is closed under conjunction. Never believe what "
            "you know to be false. <bookmark mark='b'/>Together they are inconsistent, and dropping any one restores "
            "consistency. <bookmark mark='c'/>Give up the first: high credence is not enough for belief. Dana Nelkin "
            "and Martin Smith argue that purely statistical evidence never justifies outright belief: you do not "
            "believe your ticket will lose; you only think it very likely. <bookmark mark='d'/>Give up the second, "
            "with Kyburg and Foley: believe each claim without believing their conjunction. "
            "<bookmark mark='e'/>Or give up the third, with David Christensen: belief need not be consistent, since "
            "only credences must obey logic's laws. <bookmark mark='f'/>A fourth answer keeps a version of all "
            "three, by making the threshold depend on the situation."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cde", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=2.8)
                self.play(*anims)
            vo.wait_until("f")
            self.play(*pl.reset())
        self.clear_scene()

    def stable(self):
        d = load("lottery")["stable"]
        probs = d["probs"]
        hc = history_card(2017, r"Hannes Leitgeb", r"\textit{The Stability of Belief}", width=4.8,
                          color=HIST).to_corner(UL, buff=0.35)
        defn = MathTex(r"A \text{ is stable} \iff P(A \mid B) > \tfrac12 \text{ for every } B \text{ consistent with } A",
                       font_size=30, color=CRED).next_to(hc, DOWN, buff=0.4).set_x(0)
        eq = label(r"equivalently: \ every world in $A$ is more probable than all the worlds outside $A$ together",
                   font_size=21, color=GREY_A).next_to(defn, DOWN, buff=0.2)
        names = list(probs)
        base = np.array([-4.8, -2.7, 0])
        bars = VGroup()
        for i, w in enumerate(names):
            h = 4.0 * probs[w]
            b = Rectangle(width=0.9, height=h, stroke_width=0, fill_color=CRED, fill_opacity=0.85).move_to(
                base + np.array([i * 1.2, h / 2, 0]))
            v = MathTex(f"{probs[w]:.2f}", font_size=22, color=CRED).next_to(b, UP, buff=0.08)
            n = MathTex(rf"w_{i + 1}", font_size=24).next_to(b, DOWN, buff=0.12)
            bars.add(VGroup(b, v, n))
        brackets = VGroup()
        for k, s in enumerate(d["sets"]):
            left = bars[0][0].get_left() + LEFT * 0.08
            right = bars[len(s) - 1][0].get_right() + RIGHT * 0.08
            y = -2.7 - 0.55 - k * 0.22
            brackets.add(Line(np.array([left[0], y, 0]), np.array([right[0], y, 0]), color=[OK, COH, BET, GREY_B][k],
                              stroke_width=4))
        notes = stack([
            (r"stable sets here: \ $\{w_1\} \subset \{w_1, w_2\} \subset \{w_1, w_2, w_3\} \subset W$", WHITE),
            (r"believe the propositions that contain a chosen stable set:", WHITE),
            (r"then belief is closed under conjunction, \ \textit{and} Lockean", OK),
            (r"with the threshold set by the stable set itself", GREY_A),
            (r"a fair lottery: \ no stable set but $W$, \ so believe no ticket loses", BET),
        ], font_size=22, aligned_edge=LEFT, width=6.6).move_to([3.4, -1.3, 0])
        with self.voiceover(
            "That fourth answer is Hannes Leitgeb's stability theory. <bookmark mark='a'/>Call a proposition stable "
            "if it stays more likely than not however you conditionalize, on anything consistent with it. "
            "Equivalently, every world in it is more probable than all the worlds outside it put together. "
            "<bookmark mark='b'/>Take four worlds with these probabilities. <bookmark mark='c'/>The Reasoner finds "
            "the stable sets: the first world alone; the first two; the first three; and everything. They are "
            "nested, as Leitgeb proved they must be. <bookmark mark='d'/>Now believe exactly the propositions that "
            "contain one chosen stable set. <bookmark mark='e'/>Then belief is closed under conjunction, and it is "
            "also Lockean, <bookmark mark='f'/>with the threshold set by the probability of the stable set you chose. "
            "<bookmark mark='g'/>In a fair lottery, all worlds are equally likely, and the only stable set is "
            "everything. So you believe of no ticket that it loses. The threshold for belief is not fixed; it moves "
            "with the shape of your credences."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Write(defn), FadeIn(eq))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(LaggedStart(*[Create(b) for b in brackets], lag_ratio=0.4), FadeIn(notes[0]), run_time=2.5)
            for mk, r in zip("defg", notes[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def statistical(self):
        head = label(r"Naked statistical evidence", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([
            (r"1{,}000 people at a concert; \ only 10 paid", WHITE),
            (r"you were there: \ the chance you didn't pay is 0.99", WHITE),
            (r"should the court find against you on that alone?", BET),
            (r"most say no: \ a version of L.\ J.\ Cohen's gatecrasher \ (1977)", GOAL),
            (r"yet an eyewitness who is right 95\% of the time would do", WHITE),
            (r"the same gap as the lottery: \ probability is not the whole of justified belief, \ or of knowledge",
             GREY_A),
        ], font_size=24, buff=0.3, width=12.4).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "The lottery has a twin in the law. <bookmark mark='a'/>A thousand people attend a concert; only ten "
            "paid. <bookmark mark='b'/>You were there, so the chance that you didn't pay is ninety nine percent. "
            "<bookmark mark='c'/>Should a court find against you on that evidence alone? <bookmark mark='d'/>Almost "
            "everyone says no. This is a version of Jonathan Cohen's gatecrasher case. <bookmark mark='e'/>Yet an eyewitness who "
            "is right ninety five percent of the time would be enough. <bookmark mark='f'/>It is the same gap as the "
            "lottery: high probability is not the whole of justified belief, or of knowledge, as Part 11's safety "
            "condition suggested."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
