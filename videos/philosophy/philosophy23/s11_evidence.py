from __future__ import annotations

from videos.philosophy.philosophy23.common import *  # noqa: F403


class Evidence(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"The evidential problem of evil", r"Does evil make God improbable?",
                            lit=(1979, 1984), part=PART)
        with self.voiceover("Chapter ten. The evidential problem of evil."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rowe()
        self.bayes()
        self.price()
        self.theodicies()

    def rowe(self):
        hc = history_card(1979, r"William Rowe", r"`The Problem of Evil and Some Varieties of Atheism'", width=7.2,
                          color=HIST).to_corner(UL, buff=0.3)
        steps = stack([(r"1. \ there exist instances of intense suffering which an omnipotent, \ omniscient being "
                        r"could have prevented without losing some greater good", WHITE),
                       (r"2. \ an omniscient, \ wholly good being would prevent any such suffering", ABS),
                       (r"3. \ so there does not exist such a being", BAD)], font_size=21, aligned_edge=LEFT,
                      width=12.2, buff=0.35).move_to([0, 0.5, 0])
        fawn = label(r"the fawn: \ trapped in a forest fire caused by lightning, \ burned, \ dying slowly, \ unseen",
                     font_size=20, color=WARM).to_edge(DOWN, buff=0.9)
        why = label(r"premise 1 is supported, \ not proved: \ we can see no good that this serves", font_size=19,
                    color=GREY_A).next_to(fawn, DOWN, buff=0.15)
        with self.voiceover(
            "William Rowe's evidential argument does not claim a contradiction. <bookmark mark='a'/>There exist "
            "instances of intense suffering which an omnipotent, omniscient being could have prevented without "
            "thereby losing some greater good. <bookmark mark='b'/>An omniscient, wholly good being would prevent any "
            "such suffering, unless it could not. <bookmark mark='c'/>So there is no such being. "
            "<bookmark mark='d'/>His example: in a distant forest, lightning strikes a tree; a fawn is trapped in the "
            "fire, horribly burned, and dies after days of agony, unseen by anyone. <bookmark mark='e'/>Rowe does not "
            "claim to prove premise one. He argues that it is reasonable to believe it, because we can see no good "
            "that the fawn's suffering serves."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abc", steps):
                vo.wait_until(mk)
                self.play(FadeIn(r))
            vo.wait_until("d")
            self.play(FadeIn(fawn))
            vo.wait_until("e")
            self.play(FadeIn(why))
        self.clear_scene()

    def bayes(self):
        d = load("rowe")
        head = label(r"Rowe as Bayes", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        f = MathTex(r"P(G \mid E) = \frac{P(E \mid G)\, P(G)}{P(E \mid G)\, P(G) + P(E \mid \lnot G)\, P(\lnot G)}",
                    font_size=34, color=ABS).next_to(head, DOWN, buff=0.35)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[0, 0.6, 0.1], x_length=5.6, y_length=2.8,
                  axis_config={"color": GREY_B, "font_size": 17}, x_axis_config={"include_numbers": True},
                  y_axis_config={"include_numbers": True}).move_to([-3.0, -1.2, 0])
        pts = VGroup(*[Dot(ax.c2p(r["p_e_given_god"], r["posterior"]), radius=0.08, color=DIV) for r in d["rows"]])
        curve = ax.plot(lambda x: d["prior"] * x / (d["prior"] * x + (1 - d["prior"]) * d["p_e_given_not"]),
                        x_range=[0.01, 1], color=DIV, stroke_width=3)
        xl = label(r"$P(E \mid G)$", font_size=19, color=GREY_A).next_to(ax.x_axis, RIGHT, buff=0.1)
        yl = label(r"$P(G \mid E)$", font_size=19, color=GREY_A).next_to(ax.y_axis, UP, buff=0.1)
        rows = stack([(r"$E$: \ suffering like the fawn's, \ with no good we can see", WHITE),
                      (r"prior " + f"{d['prior']}" + r"; \ $P(E \mid \lnot G) = " + f"{d['p_e_given_not']}" + r"$",
                       GREY_A),
                      (r"if $P(E \mid G) = 0.05$: \ the posterior falls to " + f"{d['rows'][0]['posterior']}", BAD),
                      (r"if $P(E \mid G)$ is near $P(E \mid \lnot G)$: \ almost no change", OK),
                      (r"everything turns on $P(E \mid G)$", GOAL)], font_size=20, aligned_edge=LEFT,
                     width=5.4).move_to([3.9, -1.1, 0])
        with self.voiceover(
            "The evidential argument is naturally Bayesian. <bookmark mark='a'/>Let E be the evidence: suffering like "
            "the fawn's, with no good we can see that it serves. The probability of God given E depends on how "
            "probable E is if God exists, compared with how probable it is if God does not. "
            "<bookmark mark='b'/>Start from a prior of one half, and say E is very probable without God: nine in ten. "
            "<bookmark mark='c'/>If E is improbable given God, five in a hundred, the posterior falls to about one "
            "in twenty. <bookmark mark='d'/>If E is about as probable given God as without, the posterior barely "
            "moves. <bookmark mark='e'/>Everything turns on one number: the probability of unexplained suffering if "
            "there is a God."
        ) as vo:
            self.play(FadeIn(head), Write(f))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(curve), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pts[0]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(p) for p in pts[1:]], lag_ratio=0.2), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def price(self):
        d = load("evil")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["G"], ["B"], ["S"], ["N"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.9, width=3.7, font_size=19,
                       center=[0, -0.5, 0], title=r"The Price List: \ the fawn")
        positions = [(("G",), r"Rowe", r"there is no God: \ evidential atheism"),
                     (("B",), r"van Inwagen \ (2006)", r"no line is sharp: \ God may permit some pointless evil"),
                     (("S",), r"theodicy", r"we can see goods it serves: \ freedom, \ soul-making, \ natural law"),
                     (("N",), r"skeptical theism", r"goods beyond our ken would be invisible to us: \ Wykstra, \ "
                                                   r"Bergmann")]
        with self.voiceover(
            "The debate is a Price List. <bookmark mark='a'/>God exists. A perfect being would permit no evil that "
            "serves no greater good. The fawn's agony serves no greater good that we can see. And if an evil served "
            "a greater good, we would probably see it. <bookmark mark='b'/>All four cannot hold. "
            "<bookmark mark='c'/>Rowe gives up God. <bookmark mark='d'/>Peter van Inwagen gives up the second claim: "
            "for any amount of evil God permits, slightly less would have served as well, so there is no sharp line, "
            "and God may permit some evils that serve nothing in particular. <bookmark mark='e'/>Theodicists deny "
            "the third: we can see the goods, such as freedom, soul-making, and regular natural laws. "
            "<bookmark mark='f'/>Skeptical theists, following Stephen Wykstra and Michael Bergmann, deny the fourth. "
            "If God's reasons concern goods beyond our ken, we would not expect to see them; our failing to see a "
            "reason is no evidence that there is none."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def theodicies(self):
        head = label(r"Skeptical theism's price", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"CORNEA", r"Wykstra \ (1984): \ `I see no reason' supports `there is none' \ only if I would see one "
                        r"if there were", ABS),
            (r"the cost", r"if we cannot judge God's reasons, \ can we judge any of God's purposes? \ moral "
                          r"paralysis?", BAD),
            (r"the symmetry", r"goods beyond our ken, \ and evils beyond our ken: \ the skeptic's ignorance cuts "
                              r"both ways", GREY_A),
            (r"the quantity", r"Draper \ (1989): \ the pattern of pleasure and pain fits indifference better than "
                              r"design", NAT),
            (r"where it stands", r"no knock-down argument on either side; \ the debate is now about likelihoods",
             GOAL),
        ]
        g = rows_table(rows, top=1.9, gap=0.45, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Skeptical theism has its own price. <bookmark mark='a'/>Wykstra's condition, CORNEA: the claim that I see "
            "no reason supports the claim that there is none only if I would see a reason if there were one. "
            "<bookmark mark='b'/>But if we cannot judge God's reasons here, can we judge them anywhere? Critics fear a "
            "moral paralysis: we could never be confident that preventing a harm is good. <bookmark mark='c'/>And the "
            "ignorance cuts both ways: there may be evils beyond our ken as well as goods. "
            "<bookmark mark='d'/>Paul Draper argued that the overall pattern of pleasure and pain in nature is far "
            "more probable on the hypothesis of indifference than on theism. <bookmark mark='e'/>No knock-down "
            "argument stands on either side. The debate is now about likelihoods, exactly where the Bayesian picture "
            "put it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
