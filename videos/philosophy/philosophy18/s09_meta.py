from __future__ import annotations

from videos.philosophy.philosophy18.common import *  # noqa: F403


class Meta(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"The pessimistic meta-induction", r"Were our predecessors' theories just as good?",
                            lit=(1902, 1981), part=PART)
        with self.voiceover("Chapter eight. The pessimistic meta-induction."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.graveyard()
        self.price()
        self.brick()

    def graveyard(self):
        d = load("meta")
        hc = history_card(1981, r"Larry Laudan", r"`A Confutation of Convergent Realism'", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        ths = sorted(d["theories"], key=lambda t: t["to"])
        lo, hi = -400, 1950
        ax = NumberLine(x_range=[lo, hi, 200], length=9.4, include_numbers=False, color=GREY_B).move_to(
            [-1.9, -3.1, 0])
        yrs = VGroup(*[label(f"{y}" if y > 0 else f"{-y} BCE", font_size=14, color=GREY_A).next_to(
            ax.n2p(y), DOWN, buff=0.1) for y in (-400, 0, 400, 800, 1200, 1600, 1950)])
        bars = VGroup()
        top = 1.4
        for i, t in enumerate(ths):
            y = top - i * 0.36
            a, b = ax.n2p(max(t["from"], lo)), ax.n2p(t["to"])
            r = Rectangle(width=max(b[0] - a[0], 0.05), height=0.24, stroke_width=0, fill_color=REAL,
                          fill_opacity=0.6).move_to([(a[0] + b[0]) / 2, y, 0])
            nm = label(t["name"], font_size=15, color=WHITE).next_to(r, RIGHT, buff=0.12)
            bars.add(VGroup(r, nm))
        side = label(r"each was empirically successful; \ each is now rejected; \ their central terms do not refer",
                     font_size=19, color=BAD).next_to(hc, RIGHT, buff=0.4).shift(DOWN * 0.1)
        if side.width > 6.0:
            side.width = 6.0
        with self.voiceover(
            "Larry Laudan answered the no-miracles argument with history. <bookmark mark='a'/>Here are twelve of "
            "the theories on his list, each drawn across the years it was accepted: the crystalline spheres of "
            "ancient astronomy, humoral medicine, phlogiston, caloric, the vital force, the optical and "
            "electromagnetic aethers, and more. <bookmark mark='b'/>Each was empirically successful in its day; "
            "each is now rejected; and their central terms, phlogiston, caloric, the aether, refer to nothing. "
            "<bookmark mark='c'/>The pessimistic meta-induction draws the inference: most successful theories of "
            "the past were false, so ours probably are too. Henri Poincaré had already noticed, in 1902, the "
            "ephemeral nature of scientific theories, and called it the bankruptcy of science that the man of the "
            "world sees."
        ) as vo:
            self.play(FadeIn(hc), Create(ax), FadeIn(yrs))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b, shift=RIGHT * 0.2) for b in bars], lag_ratio=0.12), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(side))
            vo.wait_until("c")
            self.play(*[b[0].animate.set_fill(BAD, opacity=0.6) for b in bars])
        self.clear_scene()

    def price(self):
        d = load("meta")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["R1"], ["R2"], ["R3"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.9, font_size=21,
                       center=[0, -0.5, 0], title=r"The Price List: \ the realism trilemma")
        positions = [(("R1",), r"anti-realists", r"van Fraassen; \ Laudan: \ success is evidence of empirical "
                                                 r"adequacy, \ not truth"),
                     (("R2",), r"selective realism", r"Kitcher \ (1993); \ Psillos \ (1999): \ the parts that did the "
                                                     r"work were kept; \ only idle posits died"),
                     (("R3",), r"Fahrbach \ (2011)", r"most science ever done is recent; \ our theories have survived "
                                                     r"far more testing")]
        with self.voiceover(
            "The debate is a Price List. <bookmark mark='a'/>Predictive success is good evidence of approximate "
            "truth. Many past theories were successful, and are false. And our best theories are in no better "
            "position than theirs were. <bookmark mark='b'/>Together the three are inconsistent; any two can stand. "
            "<bookmark mark='c'/>Anti-realists give up the first: success is evidence only that a theory gets the "
            "observable phenomena right. <bookmark mark='d'/>Selective realists, like Philip Kitcher and Stathis "
            "Psillos, give up the second in its strong form: the parts of past theories that actually did the "
            "predictive work were retained, and only idle posits like the aether died. "
            "<bookmark mark='e'/>And Ludwig Fahrbach gives up the third: the number of scientists and papers has "
            "doubled every fifteen to twenty years, so most science ever done is recent, and our best theories "
            "have survived far more testing than any before them."
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
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def brick(self):
        w = wall(upto=18, current=18).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(18, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        rows = card[1][1]
        with self.voiceover(
            "This is the eighteenth brick in the Wall. <bookmark mark='a'/>The dream: evidence fixes theory, and "
            "success certifies truth. <bookmark mark='b'/>The wall: underdetermination, empirically equivalent "
            "rivals and the auxiliaries of every test, joined to the pessimistic meta-induction, which turns "
            "history against the inference from success to truth. <bookmark mark='c'/>What it forces: realism has "
            "a price. Either settle for empirical adequacy, or say precisely which parts of a theory success "
            "vindicates. The next two chapters take each option."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(Indicate(w.brick[18], color=P.CONCL, scale_factor=1.08), FadeIn(card[0]), FadeIn(card[1][0]),
                      FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()
