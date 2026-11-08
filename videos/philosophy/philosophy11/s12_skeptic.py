from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Skeptic(VoiceoverScene):
    def construct(self):
        card = chapter_card(11, r"The brain in a vat", r"Do you know you are not dreaming?", lit=(1641,), part=PART)
        with self.voiceover("Chapter eleven. The brain in a vat."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.vat()
        self.closure()
        self.price()

    def vat(self):
        head = label(r"Descartes's demon, \ updated", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        jar = VGroup(RoundedRectangle(width=2.0, height=2.4, corner_radius=0.3, stroke_color=BEL, stroke_width=3,
                                      fill_color=BEL, fill_opacity=0.08),
                     Line([-1.0, 0.7, 0], [1.0, 0.7, 0], color=BEL, stroke_width=2)).move_to([-3.6, 0.0, 0])
        brain = VGroup(*[Circle(radius=0.32, stroke_color=LUCK, stroke_width=2.5, fill_color=LUCK,
                                fill_opacity=0.3).move_to(jar.get_center() + np.array([dx, dy, 0]))
                         for dx, dy in ((-0.28, 0.05), (0.28, 0.05), (0, 0.32), (0, -0.2))])
        comp = VGroup(Rectangle(width=1.8, height=1.2, stroke_color=GREY_B, stroke_width=3),
                      label(r"computer", font_size=20, color=GREY_B)).move_to([1.0, 0.0, 0])
        comp[1].move_to(comp[0])
        wires = VGroup(*[CubicBezier(jar.get_right() + UP * dy, jar.get_right() + RIGHT * 0.8 + UP * (dy + 0.3),
                                     comp[0].get_left() + LEFT * 0.8 + UP * (dy - 0.3), comp[0].get_left() + UP * dy,
                                     color=GREY_C, stroke_width=2) for dy in (-0.3, 0, 0.3)])
        world = VGroup(label(r"it feeds the brain \ every experience you have now:", font_size=22, color=GREY_A),
                       label(r"this screen, \ your hands, \ the room", font_size=22, color=WHITE)).arrange(
            DOWN, buff=0.12).next_to(comp, DOWN, buff=0.35)
        rows = VGroup(label(r"nothing in your experience could tell the two apart", font_size=25, color=LUCK),
                      label(r"Descartes's demon (1641); \ the vat: \ Harman (1973), \ Putnam (1981)", font_size=21,
                            color=GREY_B)).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "The skeptic's question returns, in its modern form. <bookmark mark='a'/>Imagine your brain removed and "
            "kept alive in a vat of nutrients. <bookmark mark='b'/>Its nerve endings are wired to a computer, which "
            "feeds it exactly the experiences you are having now: this screen, your hands, the room around you. "
            "<bookmark mark='c'/>Nothing in your experience could tell the two situations apart. This is Descartes's "
            "evil demon, rebuilt with a laboratory; Gilbert Harman described it in 1973, and Hilary Putnam gave it "
            "its name in 1981. Do you know that you are not a brain in a vat?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(jar), FadeIn(brain))
            vo.wait_until("b")
            self.play(FadeIn(comp), Create(wires), FadeIn(world))
            vo.wait_until("c")
            self.play(FadeIn(rows))
        self.clear_scene()

    def closure(self):
        head = label(r"The closure argument", font_size=32, color=CONN).to_edge(UP, buff=0.35)
        cp = VGroup(label(r"closure: \ if you know $p$, \ and know that $p$ implies $q$, \ you are in a position to "
                          r"know $q$", font_size=24, color=GOAL),
                    MathTex(r"(K p \land K(p \rightarrow q)) \rightarrow K q", font_size=34, color=GOAL)).arrange(
            DOWN, buff=0.2).next_to(head, DOWN, buff=0.35)
        steps = VGroup(
            label(r"1. \ I don't know that I am not a brain in a vat", font_size=25, color=SKEP),
            label(r"2. \ if I know I have hands, \ then I know I am not a brain in a vat \ (closure)", font_size=25),
            label(r"3. \ so I don't know I have hands", font_size=25, color=BAD),
            label(r"and the same for almost everything I believe about the world", font_size=23,
                  color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([0, -1.2, 0])
        with self.voiceover(
            "The skeptic needs only one principle. <bookmark mark='a'/>Closure: if you know p, and you know that p "
            "implies q, then you are in a position to know q. Knowledge extends by known implication. "
            "<bookmark mark='b'/>Now the argument. One: I do not know that I am not a brain in a vat; nothing in my "
            "experience could tell me. <bookmark mark='c'/>Two: having hands implies not being a handless brain in a "
            "vat, and I know it does. So by closure, if I know I have hands, I know I am not a brain in a vat. "
            "<bookmark mark='d'/>Three: so I do not know that I have hands. <bookmark mark='e'/>And the argument "
            "generalizes to almost everything I believe about the world around me."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cp))
            for mk, s_ in zip("bcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s_, shift=RIGHT * 0.1))
        self.clear_scene()

    def price(self):
        d = load("skeptic")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.5, width=4.0, font_size=23,
                       center=[0, -0.4, 0], title=r"The Price List: \ the skeptic's triad")
        assert d["mcs"] == [["S1"], ["S2"], ["S3"]]
        positions = [(("S1",), r"Moore", r"`here is one hand': \ so I do know I'm not envatted (Ch.\ 12)"),
                     (("S2",), r"Dretske, \ Nozick", r"closure fails: \ I know I have hands, \ not that I'm not "
                                                    r"envatted"),
                     (("S3",), r"the skeptic", r"I don't know I have hands")]
        foot = label(r"and contextualism: \ each is true in some context, \ never all three in one (Ch.\ 12)",
                     font_size=22, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Here is the skeptic's argument as a Price List. <bookmark mark='a'/>Three claims, each plausible on its "
            "own: I don't know I'm not a brain in a vat; if I know I have hands, I know I'm not one; I know I have "
            "hands. <bookmark mark='b'/>The Reasoner confirms that the three together are inconsistent, and that "
            "giving up any one of them restores consistency. So there are exactly three positions. "
            "<bookmark mark='c'/>G. E. Moore gives up the first: since I know I have hands, I can know I am not "
            "envatted. <bookmark mark='d'/>Fred Dretske and Robert Nozick give up the second: closure fails, as "
            "sensitivity predicted. <bookmark mark='e'/>The skeptic gives up the third. <bookmark mark='f'/>And a "
            "fourth answer, contextualism, says that each claim is true in some context, though never all three in "
            "one. The next chapter weighs them."
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
                anims, centre = pl.position(mcs, name, who, width=2.6)
                self.play(*anims)
            vo.wait_until("f")
            self.play(*pl.reset())
            self.play(FadeIn(foot))
        self.clear_scene()
