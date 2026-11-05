from __future__ import annotations

from videos.philosophy.philosophy1.common import *  # noqa: F403

POS = {
    "V": (r"Modern logic", r"Boole, Frege, Russell: `all' carries no commitment to existence; Darapti is invalid"),
    "u1": (r"The tradition", r"universal sentences assume their subjects exist; with no unicorns, `all unicorns "
                             r"\dots' is false"),
    "u2": (r"Presupposition", r"Strawson (1952): with no unicorns, `all unicorns \dots' is neither true nor false"),
    "ns": (r"Accept the conclusion", r"some horses are one-horned: no one"),
}


class Import(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Empty terms", r"Does `all unicorns' assume there are unicorns?", lit=(1854,),
                            part=PART)
        with self.voiceover("Chapter nine. Empty terms."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.empty()
        self.import_()
        self.price()

    def empty(self):
        d = load("unicorn")
        assert d["countermodel"] == []
        V = venn3(radius=1.15, center=[-3.4, -0.4, 0], names=(r"\text{horses}", r"\text{unicorns}",
                                                               r"\text{one-horned}"))
        dar = VGroup(label(r"Darapti:", font_size=28, color=GOAL),
                     label(r"all $M$ are $P$; \ all $M$ are $S$; \ so some $S$ are $P$", font_size=28)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15).to_corner(UR, buff=0.5)
        world = label(r"the countermodel: \ every region empty", font_size=28, color=BAD).next_to(dar, DOWN, buff=0.6)
        world.align_to(dar, LEFT)
        why_ = VGroup(label(r"`all unicorns are horses': \ no unicorn is a non-horse \ $\checkmark$", font_size=24),
                      label(r"`all unicorns are one-horned': \ likewise \ $\checkmark$", font_size=24),
                      label(r"`some horses are one-horned': \ nothing is \ $\times$", font_size=24, color=BAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).next_to(world, DOWN, buff=0.4).align_to(world, LEFT)
        with self.voiceover(
            "The Latin verse names twenty-four moods; our machine passed fifteen. The other nine include Darapti, the "
            "unicorn argument. <bookmark mark='a'/>All M are P; all M are S; so some S are P. <bookmark mark='b'/>"
            "The countermodel the machine finds is the simplest arrangement there is: every region empty. "
            "<bookmark mark='c'/>If there are no unicorns at all, then no unicorn fails to be a horse, and no unicorn "
            "fails to be one-horned: in the modern reading, both premises are true, vacuously. But nothing is a "
            "one-horned horse, so the conclusion is false."
        ) as vo:
            self.play(FadeIn(V))
            vo.wait_until("a")
            self.play(FadeIn(dar))
            vo.wait_until("b")
            self.play(FadeIn(world), *[c.animate.set_stroke(opacity=0.5) for c in V.circles])
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(w, shift=RIGHT * 0.2) for w in why_], lag_ratio=0.4))
        self.clear_scene()

    def import_(self):
        d = load("moods")
        rows = d["rows"]
        cells, idx = VGroup(), {}
        for f in (1, 2, 3, 4):
            for j, r in enumerate([r for r in rows if r["figure"] == f]):
                sq = Square(0.17, stroke_width=0.6, stroke_color=GREY_D, fill_color=GREY_D, fill_opacity=1)
                sq.move_to([-5.7 + j * 0.185, 1.6 - (f - 1) * 0.8, 0])
                cells.add(sq)
                idx[(f, r["mood"])] = sq
        boolean = {(f, m) for f, m, _ in d["boolean"]}
        trad = {(f, m) for f, m, _ in d["traditional"]}
        extra = trad - boolean
        for k in boolean:
            idx[k].set_fill(OK)
        rule = label(r"add one assumption: \ every term names something", font_size=30, color=GOAL).to_edge(UP,
                                                                                                    buff=0.4)
        cnt = label(rf"valid: \ {len(trad)} \ = \ {len(boolean)} \ + \ {len(extra)} that need an inhabited term",
                    font_size=30).move_to([0, -2.0, 0])
        names = sorted(n for f, m, n in d["traditional"] if (f, m) in extra)
        nl = label(r",\ ".join(names), font_size=22, color=GOAL).next_to(cnt, DOWN, buff=0.3)
        with self.voiceover(
            "Now give the machine Aristotle's background assumption: every term names something; no circle is "
            "empty. <bookmark mark='a'/>Rerun all two hundred and fifty-six moods. "
            f"<bookmark mark='b'/>Now {len(trad)} pass: the original {len(boolean)}, and {len(extra)} more, each of "
            "which needs some term to be inhabited. <bookmark mark='c'/>And these twenty-four are exactly the moods "
            "of the medieval verse. The tradition was not careless. It was calculating correctly, under an "
            "assumption it never stated, because it never imagined a logic about things that might not exist."
        ) as vo:
            self.play(FadeIn(rule), FadeIn(cells))
            vo.wait_until("a")
            self.play(Indicate(cells, color=GOAL, scale_factor=1.01))
            vo.wait_until("b")
            self.play(*[idx[k].animate.set_fill(GOAL) for k in extra], FadeIn(cnt))
            vo.wait_until("c")
            self.play(FadeIn(nl))
        self.clear_scene()

    def price(self):
        d = load("unicorn")
        pl = PriceList([(c["key"], c["text"]) for c in d["claims"]], mus=d["mus"], radius=2.3, width=4.6,
                       font_size=24, center=[0, -0.4, 0])
        title = label(r"The Price List: \ the unicorns", font_size=34, color=P.PRICE).to_edge(UP, buff=0.25)
        with self.voiceover(
            "So the opening dispute becomes a Price List of four claims. <bookmark mark='a'/>The two premises are "
            "true. Darapti is valid. And the conclusion is not true. The four are inconsistent; there are four "
            "exits, and three of them have been taken by real logicians."
        ) as vo:
            self.play(FadeIn(title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in pl.cards], lag_ratio=0.3), Create(pl.conflict))

        def show(k):
            name, holders = POS[k]
            return pl.position((k,), name, holders, width=4.0)[0]

        with self.voiceover(
            "Modern logic, from Boole and Frege on, gives up the validity of Darapti: 'all' makes no claim that "
            "anything exists."
        ):
            self.play(*show("V"), run_time=1.2)
        self.play(*pl.reset(), run_time=0.8)
        with self.voiceover(
            "The tradition read universal sentences as asserting that their subjects exist, so that 'all unicorns "
            "are horses' is simply false."
        ):
            self.play(*show("u1"), run_time=1.2)
        self.play(*pl.reset(), run_time=0.8)
        with self.voiceover(
            "And in 1952 Peter Strawson argued for a third view: with no unicorns, 'all unicorns are horses' "
            "presupposes something false, and is neither true nor false. A gap between truth and falsehood: Part 5 "
            "will build logics with exactly such gaps. Calculation did not end this dispute. It located it, "
            "precisely, in the meaning of one word."
        ):
            self.play(*show("u2"), run_time=1.2)
        self.clear_scene()
