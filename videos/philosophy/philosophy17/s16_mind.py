from __future__ import annotations

from videos.philosophy.philosophy17.common import *  # noqa: F403


class Mind(VoiceoverScene):
    def construct(self):
        card = chapter_card(15, r"Causation and the mind", r"Can a thought move an arm?", lit=(1992, 1998),
                            part=PART)
        with self.voiceover("Chapter fifteen. Causation and the mind."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.argument()
        self.price()
        self.pigeon()

    def argument(self):
        hc = history_card(1998, r"Jaegwon Kim", r"\textit{Mind in a Physical World}", width=5.6,
                          color=HIST).to_corner(UL, buff=0.3)
        pos = {"M": [-3.0, 0.6, 0], "M*": [1.0, 0.6, 0], "P": [-3.0, -1.4, 0], "P*": [1.0, -1.4, 0]}
        g = CausalGraph(pos, [("P", "P*"), ("M", "P*")], radius=0.45, font_size=22,
                        colors={"M": CAUSE, "M*": CAUSE, "P": EFFECT, "P*": EFFECT})
        sup = VGroup(*[DashedLine(np.array(pos[a]) + DOWN * 0.45, np.array(pos[b]) + UP * 0.45, color=GREY_B)
                       for a, b in (("M", "P"), ("M*", "P*"))])
        sl = label(r"supervenes on", font_size=16, color=GREY_B).next_to(sup[0], LEFT, buff=0.1)
        notes = stack([(r"$M$: \ a wish for water; \ \ $P^*$: \ the arm reaching for the glass", WHITE),
                       (r"the brain state $P$ realizes $M$, \ and is already sufficient for $P^*$", EFFECT),
                       (r"so what is left for $M$ to do?", BAD),
                       (r"`the problem of causal exclusion'", GOAL)], font_size=21).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Part 30 will ask what minds are; this chapter asks one causal question about them. "
            "<bookmark mark='a'/>I want water, and my arm reaches for the glass. Surely the wish caused the "
            "movement. <bookmark mark='b'/>But the wish is realized by a brain state, on which it supervenes; and "
            "that brain state, by the causal closure of physics, was already sufficient for the arm's motion. "
            "<bookmark mark='c'/>So what is left for the wish to do? <bookmark mark='d'/>Jaegwon Kim pressed this "
            "as the problem of causal exclusion, against everyone who holds that minds are physical but not "
            "reducible to physics."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(g.node["M"]), FadeIn(g.node["P*"]), GrowArrow(g.edge[("M", "P*")]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(g.node["P"]), FadeIn(g.node["M*"]), Create(sup), FadeIn(sl),
                      GrowArrow(g.edge[("P", "P*")]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(g.edge[("M", "P*")].animate.set_color(BAD), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.clear_scene()

    def price(self):
        d = load("mind")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mcs"] == [["K1"], ["K2"], ["K3"], ["K4"], ["K5"]]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=3.0, width=3.5, font_size=18,
                       center=[0, -0.5, 0], title=r"The Price List: \ causal exclusion")
        positions = [(("K2",), r"Kim", r"reductive physicalism: \ the wish \textit{is} the brain state, \ so it "
                                       r"causes by being physical"),
                     (("K1",), r"epiphenomenalism", r"Huxley \ (1874): \ the mind is the steam-whistle, \ not the "
                                                    r"engine"),
                     (("K3",), r"interactionist dualism", r"Descartes; \ Lowe \ (2000): \ physics is not causally "
                                                          r"closed"),
                     (("K5",), r"Sider \ (2003)", r"what is so bad about overdetermination? \ accept it"),
                     (("K4",), r"Bennett; \ Woodward", r"a cause and its realizer are not rivals: \ exclusion applies "
                                                       r"only to independent causes")]
        with self.voiceover(
            "Kim's argument is a Price List with five claims. <bookmark mark='a'/>Mental events cause physical "
            "events. Mental events are not physical events. Physics is closed: every physical event with a cause "
            "has a sufficient physical cause. Exclusion: no event has two distinct sufficient causes unless it is "
            "overdetermined. And the mind does not systematically overdetermine behaviour. "
            "<bookmark mark='b'/>The five are inconsistent; drop any one and the rest are fine. "
            "<bookmark mark='c'/>Kim dropped the second: the wish is the brain state, and causes by being "
            "physical. <bookmark mark='d'/>Thomas Huxley dropped the first: consciousness is like the steam whistle "
            "on a locomotive, which accompanies the work but does none of it. <bookmark mark='e'/>Dualists, from "
            "Descartes to Jonathan Lowe, drop closure. <bookmark mark='f'/>Theodore Sider asked what is so bad "
            "about overdetermination, and accepted it. <bookmark mark='g'/>And Karen Bennett, and interventionists "
            "following Woodward, reject exclusion as stated: a cause and the state that realizes it are not "
            "competitors, so the principle applies only to independent causes."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who) in zip("cdefg", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def pigeon(self):
        d = load("mind")["pigeon"]
        hc = history_card(1992, r"Stephen Yablo", r"`Mental Causation'", width=4.8, color=HIST).to_corner(UL,
                                                                                                    buff=0.3)
        shades = [("scarlet", "#FF2400"), ("crimson", "#DC143C"), ("maroon", "#B03060"), ("navy", "#3050C0"),
                  ("sky", "#87CEEB")]
        sw = VGroup()
        for i, (n, c) in enumerate(shades):
            sq = Square(side_length=0.8, stroke_color=WHITE, stroke_width=2, fill_color=c, fill_opacity=0.9)
            t = label(n, font_size=17, color=GREY_A).next_to(sq, DOWN, buff=0.12)
            sw.add(VGroup(sq, t))
        sw.arrange(RIGHT, buff=0.35).move_to([0.8, 0.4, 0])
        brace_r = Brace(VGroup(*sw[:3]), UP, color=SUZY)
        red = label(r"red: \ the pigeon pecks", font_size=19, color=SUZY).next_to(brace_r, UP, buff=0.1)
        rows = stack([(r"trained to peck at red; \ shown scarlet; \ it pecks", WHITE),
                      (r"`scarlet' as the cause: \ of " + f"{d['shade_alts']}" + r" other shades, \ only " +
                       f"{d['shade_diff']}" + r" would change the outcome", BAD),
                      (r"`red' as the cause: \ " + f"{d['color_diff']}" + r" of " + f"{d['color_alts']}" +
                       r" alternative changes it: \ \textit{proportional}", OK),
                      (r"the mental may be the better cause than its realizer, \ as red is than scarlet \ "
                       r"(List and Menzies, \ 2009)", GOAL),
                      (r"the interventionist question: \ which variable, \ when wiggled, \ makes the difference?", GREY_A)],
                     font_size=20, width=12.0).next_to(sw, DOWN, buff=0.5)
        with self.voiceover(
            "Stephen Yablo's pigeon makes the interventionist reply vivid. <bookmark mark='a'/>A pigeon is trained "
            "to peck at red things. It is shown a scarlet patch, and pecks. <bookmark mark='b'/>What caused the "
            "peck: the patch's being scarlet, or its being red? <bookmark mark='c'/>Take scarlet as the cause. Of "
            "the four other shades it might have been, only two would have changed the outcome; crimson and maroon "
            "would have been pecked as well. <bookmark mark='d'/>Take red as the cause. Its alternative, not red, "
            "always changes the outcome. Red is the proportional cause: neither too specific nor too general. "
            "<bookmark mark='e'/>Christian List and Peter Menzies argued that mental states can stand to their "
            "realizers as red stands to scarlet: the higher-level state is the better cause, and exclusion runs "
            "the other way. <bookmark mark='f'/>Which description of a cause is correct becomes Woodward's "
            "question: which variable, when wiggled, makes the difference?"
        ) as vo:
            self.play(FadeIn(hc), LaggedStart(*[FadeIn(s) for s in sw], lag_ratio=0.15))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(sw[0], color=WHITE))
            vo.wait_until("b")
            self.play(GrowFromCenter(brace_r), FadeIn(red))
            for mk, r in zip("cdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
