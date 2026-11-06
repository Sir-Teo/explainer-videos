from __future__ import annotations

from videos.philosophy.philosophy30.common import *  # noqa: F403


def node(tex, col, at):
    t = MathTex(tex, font_size=34, color=col)
    c = Circle(radius=0.42, color=col, fill_opacity=0.12).move_to(at)
    return VGroup(c, t.move_to(at))


class Exclusion(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"Causal exclusion", r"If the physical is causally complete, \ what does the mind do?",
                            lit=(1998,), part=PART)
        with self.voiceover("Chapter eight. Causal exclusion."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.argument()
        self.premises()
        self.wall_brick()
        self.price()
        self.autonomy()

    def argument(self):
        hc = history_card(1998, r"Jaegwon Kim", r"\textit{Mind in a Physical World}", width=5.4, color=HIST).to_corner(
            UL, buff=0.3)
        M_ = node(r"M", MIND, [-3.0, 1.0, 0])
        Ms = node(r"M^*", MIND, [3.0, 1.0, 0])
        P_ = node(r"P", PHYS, [-3.0, -1.4, 0])
        Ps = node(r"P^*", PHYS, [3.0, -1.4, 0])
        sup1 = DashedLine(P_.get_top(), M_.get_bottom(), color=GREY_B)
        sup2 = DashedLine(Ps.get_top(), Ms.get_bottom(), color=GREY_B)
        st = VGroup(label(r"realizes", font_size=15, color=GREY_B).next_to(sup1, LEFT, buff=0.1),
                    label(r"realizes", font_size=15, color=GREY_B).next_to(sup2, RIGHT, buff=0.1))
        mm = Arrow(M_.get_right(), Ms.get_left(), buff=0.1, color=MIND)
        mp = Arrow(M_.get_right(), Ps.get_left(), buff=0.1, color=MIND)
        pp = Arrow(P_.get_right(), Ps.get_left(), buff=0.1, color=PHYS)
        tags = VGroup(label(r"my wanting water", font_size=16, color=MIND).next_to(M_, LEFT, buff=0.2),
                      label(r"its neural realizer", font_size=16, color=PHYS).next_to(P_, LEFT, buff=0.2),
                      label(r"my arm moving", font_size=16, color=PHYS).next_to(Ps, RIGHT, buff=0.2))
        foot = label(r"$P$ already suffices for $P^*$: \ what is left for $M$ to do?", font_size=22,
                     color=GOAL).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Jaegwon Kim turned supervenience against the non-reductive physicalist. <bookmark mark='a'/>Suppose a "
            "mental event M, my wanting water, causes a physical event P star, my arm reaching for the glass. "
            "<bookmark mark='b'/>M is realized by some neural event P. <bookmark mark='c'/>But the physical world is "
            "causally closed: P star has a sufficient physical cause, and P is the obvious candidate. "
            "<bookmark mark='d'/>So what is left for M to do? Either M is P, or M's causal work is pre-empted by P, "
            "or the arm's motion has two sufficient causes, which would have to be so for every mental cause there "
            "ever was. Kim called the conclusion the exclusion problem."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(M_), FadeIn(Ps), GrowArrow(mp), FadeIn(tags[0]), FadeIn(tags[2]))
            vo.wait_until("b")
            self.play(FadeIn(P_), Create(sup1), FadeIn(st[0]), FadeIn(tags[1]))
            vo.wait_until("c")
            self.play(GrowArrow(pp))
            vo.wait_until("d")
            self.play(mp.animate.set_opacity(0.2), Indicate(pp, color=PHYS), FadeIn(foot))
        self.clear_scene()

    def premises(self):
        head = label(r"The argument, \ step by step", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        steps = [
            (r"1. \ distinctness", r"$M \neq P$: \ mental properties are not physical properties", MIND),
            (r"2. \ mental causation", r"$M$ causes $P^*$", MIND),
            (r"3. \ closure", r"every physical event with a cause has a sufficient physical cause: \ $P$", PHYS),
            (r"4. \ exclusion", r"no event has two sufficient causes, \ unless it is overdetermined", SYM),
            (r"5. \ no overdetermination", r"mental causes do not systematically overdetermine their effects", SYM),
            (r"so", r"1 to 5 are inconsistent: \ something has to go", BAD),
        ]
        g = rows_table(steps, top=1.7, gap=0.42)
        with self.voiceover(
            "Laid out, the argument has five steps. <bookmark mark='a'/>One: distinctness. The mental property is "
            "not the physical property that realizes it; that is what non-reductive physicalism says. "
            "<bookmark mark='b'/>Two: mental causation. My wanting water causes my arm to move. "
            "<bookmark mark='c'/>Three: closure. Every physical event that has a cause has a sufficient physical "
            "cause. <bookmark mark='d'/>Four: exclusion. No event has more than one sufficient cause, unless it is "
            "overdetermined, like a man shot by two firing-squad marksmen at once. <bookmark mark='e'/>Five: mental "
            "causes do not systematically overdetermine their effects. <bookmark mark='f'/>Together, the five are "
            "inconsistent. Kim concluded that the only way to keep mental causation is to reduce the mental to the "
            "physical."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def wall_brick(self):
        w = wall(upto=30, current=30).scale(0.44).to_edge(LEFT, buff=0.3).shift(DOWN * 0.3)
        card = wall_card(30, width=6.2, font_size=22).to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "This is the thirtieth brick in the Wall. <bookmark mark='a'/>The dream was a mind that is both physical, "
            "fully part of the natural world, and causally its own, making a difference that is not just the "
            "difference its physical basis makes. Kim's exclusion argument says you cannot have both. "
            "<bookmark mark='b'/>What it forces is a choice: reduce the mental, accept overdetermination, or let the "
            "mind be an epiphenomenon, a side effect that does nothing."
        ) as vo:
            self.play(FadeIn(w))
            vo.wait_until("a")
            self.play(FadeIn(card), Indicate(w.brick[30], color=P.CONCL, scale_factor=1.06))
            vo.wait_until("b")
            self.wait(0.5)
        self.clear_scene()

    def price(self):
        d = load("exclusion")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert sorted(d["mcs"]) == [["C"], ["D"], ["K"], ["O"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.4, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ the mind--body tetrad")
        positions = [(("D",), r"reductive physicalism", r"mental properties are physical: \ Kim; \ the identity "
                                                          r"theory"),
                     (("C",), r"epiphenomenalism", r"the mind is caused but causes nothing: \ Huxley; \ Jackson "
                                                   r"\ (1982)"),
                     (("K",), r"interactionist dualism", r"some physical events have only mental causes: \ Descartes; "
                                                         r"\ Popper and Eccles"),
                     (("O",), r"harmless overdetermination", r"mental and physical causes overlap without competing: "
                                                             r"\ Bennett \ (2003)")]
        with self.voiceover(
            "Four claims cannot all be true. <bookmark mark='a'/>Mental events are not physical events. Mental events "
            "cause physical events. Every physical event that has a cause has a sufficient physical cause. And the "
            "effects of mental causes are not systematically overdetermined. <bookmark mark='b'/>Something has to "
            "give. <bookmark mark='c'/>The reductive physicalist gives up the first: mental properties are physical "
            "properties after all, Kim's own conclusion. <bookmark mark='d'/>The epiphenomenalist gives up the "
            "second: the mind is caused but causes nothing, as Thomas Huxley held of consciousness, and Frank Jackson "
            "in 1982 of qualia. <bookmark mark='e'/>The interactionist dualist gives up the third: some physical "
            "events have mental causes and no sufficient physical ones, as Descartes held, and in the twentieth "
            "century Karl Popper and John Eccles. <bookmark mark='f'/>And some give up the fourth: Karen Bennett "
            "argued in 2003 that the overdetermination is harmless, because the mental cause is realized by the "
            "physical one, and the two do not compete."
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

    def autonomy(self):
        d = load("proportional")
        head = label(r"The autonomy reply: \ proportional causes", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hc = history_card(1992, r"Stephen Yablo", r"`Mental Causation', \ \textit{Philosophical Review}", width=5.4,
                          color=HIST).to_corner(UL, buff=0.3)
        q = {r["cause"]: r for r in d["rows"]}
        assert d["peck"]["scarlet"] == 0.95 and d["peck"]["teal"] == 0.05
        assert (q["red"]["difference"], q["red"]["info"], q["red"]["cause_bits"]) == (0.9, 0.7136, 1.0)
        assert (q["scarlet"]["difference"], q["scarlet"]["info"]) == (0.54, 0.3686)
        assert (q["the exact shade"]["info"], q["the exact shade"]["cause_bits"]) == (0.7136, 2.585)
        assert q["coloured"]["info"] == 0.0
        hexes = {"scarlet": "#FF2400", "crimson": "#DC143C", "maroon": "#A0303A", "teal": "#2A9D8F",
                 "navy": "#3355AA", "olive": "#8A8A2A"}
        sw = VGroup()
        for k, (name, red) in enumerate(M.SHADES):
            x = -4.5 + 1.8 * k
            sq = Square(side_length=0.9, fill_color=hexes[name], fill_opacity=1, stroke_width=0).move_to([x, 1.2, 0])
            sw.add(VGroup(sq, label(name, font_size=17, color=GREY_A).next_to(sq, DOWN, buff=0.12),
                          MathTex(rf"{d['peck'][name]:.2f}", font_size=24,
                                  color=OK if red else GREY_B).next_to(sq, DOWN, buff=0.5)))
        pl = label(r"Sophie, \ trained to peck at red: \ chance of a peck", font_size=19, color=BEHAV).move_to(
            [0, 2.1, 0])
        br = Brace(VGroup(*sw[:3]), DOWN, buff=1.0, color=FEEL)
        bl = label(r"red: \ supervenes on the shade", font_size=17, color=FEEL).next_to(br, DOWN, buff=0.1)
        hd = [r"\text{candidate cause}", r"\text{values}", r"\text{difference made}",
              r"\text{bits about pecking}", r"\text{bits of cause}"]
        order = ["red", "scarlet", "the exact shade", "coloured"]
        cells = [[label(r"`" + n + "'" if n != "the exact shade" else n, font_size=19,
                        color=FEEL if n == "red" else WHITE),
                  label(str(q[n]["values"]), font_size=19, color=GREY_A),
                  label(f"{q[n]['difference']:.2f}" if q[n]["difference"] is not None else r"---", font_size=19,
                        color=GREY_A),
                  label(f"{q[n]['info']:.3f}", font_size=19, color=OK if q[n]["info"] > 0.7 else GREY_A),
                  label(f"{q[n]['cause_bits']:.2f}", font_size=19, color=GREY_A)] for n in order]
        grid = ValueGrid(hd, cells, col_w=[3.0, 1.4, 2.6, 2.9, 2.2], cell_h=0.55, font_size=19).move_to([0, -0.3, 0])
        gl = label(r"each cause's values set by intervention, \ with equal chances", font_size=16,
                   color=GREY_A).next_to(grid, DOWN, buff=0.2)
        concl = stack([(r"`red' is proportional: \ all the difference the shade makes, \ with one bit", FEEL),
                       (r"realization-insensitive: \ had it been another red, \ she would still have pecked", OK),
                       (r"so too a thirst realized by $P$: \ another realizer, \ the same reach for the glass", MIND),
                       (r"Kim: \ the realizer still does all the producing; \ the debate goes on", BAD)],
                      font_size=21, aligned_edge=LEFT, width=12.4, buff=0.3).move_to([0, -0.4, 0])
        with self.voiceover(
            "There is a fifth answer, which questions the exclusion principle itself. <bookmark mark='a'/>Stephen "
            "Yablo, in 1992, imagined Sophie, a pigeon trained to peck at red. Shown scarlet, she pecks. Was it the "
            "scarlet that caused it, or the red? Red supervenes on the exact shade, as the mental supervenes on the "
            "physical. <bookmark mark='b'/>The Reasoner puts six shades in front of her. Three are reds, and she "
            "pecks at them ninety five times in a hundred; at the others, five. <bookmark mark='c'/>Now compare "
            "candidate causes, in James Woodward's interventionist way: set the cause's value by intervention, with "
            "equal chances, and see what difference it makes to the pecking. Red against not red makes a "
            "difference of ninety points, and carries 0.714 bits about the peck. Scarlet against not scarlet makes "
            "only fifty four points, 0.369 bits, because some non-scarlets are red. The exact shade carries the same "
            "0.714 bits as red, but needs 2.58 bits of cause to do it: most of its detail makes no difference. And "
            "being coloured, which every shade is, makes none. <bookmark mark='d'/>Red is the proportional cause: "
            "it carries all the difference the shade makes, and nothing that makes none. <bookmark mark='e'/>It is "
            "also realization-insensitive, in the terms of Christian List and Peter Menzies in 2009: had the red "
            "been a different red, she would still have pecked. <bookmark mark='f'/>So too, they argue, for a thirst "
            "realized by a neural state P: had it been realized differently, I would still have reached for the "
            "glass, so the thirst, not the exact neural state, is the difference-maker, and the exclusion principle "
            "fails for causes at different grains. <bookmark mark='g'/>Kim replied that the realizer still does all "
            "the producing; proportionality is about which description explains best, not about what makes the arm "
            "move. That disagreement is where the debate stands."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc))
            vo.wait_until("b")
            self.play(FadeOut(hc), FadeIn(pl), LaggedStart(*[FadeIn(x) for x in sw], lag_ratio=0.15))
            self.play(GrowFromCenter(br), FadeIn(bl))
            vo.wait_until("c")
            self.play(FadeOut(VGroup(pl, sw, br, bl)))
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(gl))
            for r in range(len(order)):
                self.play(*[FadeIn(c) for c in grid.cell[r]], run_time=0.6)
            vo.wait_until("d")
            self.play(Indicate(VGroup(*grid.cell[0]), color=FEEL, scale_factor=1.04))
            vo.wait_until("e")
            self.play(FadeOut(VGroup(grid.head, grid.rule, gl, *[c for row in grid.cell for c in row])))
            self.play(FadeIn(concl[0]), FadeIn(concl[1]))
            vo.wait_until("f")
            self.play(FadeIn(concl[2]))
            vo.wait_until("g")
            self.play(FadeIn(concl[3]))
        self.clear_scene()
