from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


def tracks(kind: str, center):
    """A schematic trolley case: the main track to five, a branch or a bridge."""
    c = np.array(center)
    g = VGroup()
    g.add(Line(c + LEFT * 2.2, c + RIGHT * 2.0, color=GREY_B, stroke_width=3))
    five = VGroup(*[Dot(c + RIGHT * (1.2 + 0.18 * i), radius=0.07, color=HARM) for i in range(5)])
    g.add(five)
    trolley = RoundedRectangle(width=0.5, height=0.3, corner_radius=0.06, color=KANT, fill_opacity=0.7).move_to(
        c + LEFT * 1.9 + UP * 0.2)
    g.add(trolley)
    if kind in ("switch", "loop"):
        br = Line(c + LEFT * 0.6, c + LEFT * 0.0 + DOWN * 0.9, color=GREY_B, stroke_width=3)
        br2 = Line(c + DOWN * 0.9, c + RIGHT * 1.6 + DOWN * 0.9, color=GREY_B, stroke_width=3)
        g.add(br, br2, Dot(c + RIGHT * 0.9 + DOWN * 0.9, radius=0.08, color=HARM))
        if kind == "loop":
            g.add(Line(c + RIGHT * 1.6 + DOWN * 0.9, c + RIGHT * 2.0, color=GREY_B, stroke_width=3))
    if kind == "footbridge":
        g.add(Line(c + LEFT * 0.3 + UP * 0.9, c + RIGHT * 0.7 + UP * 0.9, color=GREY_B, stroke_width=4),
              Dot(c + RIGHT * 0.2 + UP * 1.05, radius=0.11, color=HARM))
    return g


class Trolley(VoiceoverScene):
    def construct(self):
        card = chapter_card(8, r"The trolley problem", r"Why may you turn the trolley, but not push the man?",
                            lit=(1967, 1985), part=PART)
        with self.voiceover("Chapter eight. The trolley problem."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.cases()
        self.dde()
        self.price()
        self.machine()

    def cases(self):
        d = load("trolley")
        head = label(r"Foot \ (1967), \ Thomson \ (1976, \ 1985)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        sv = d["survey"]
        assert (sv["switch"], sv["don't switch"], sv["push"], sv["don't push"]) == (0.634, 0.133, 0.22, 0.562)
        t1 = tracks("switch", [-3.4, 0.9, 0])
        t2 = tracks("footbridge", [3.0, 0.9, 0])
        l1 = label(r"switch: \ turn the trolley onto the one", font_size=19, color=GREY_A).next_to(t1, DOWN, buff=0.3)
        l2 = label(r"footbridge: \ push a large man into its path", font_size=19, color=GREY_A).next_to(t2, DOWN,
                                                                                                   buff=0.3)

        def bar(x, y, share, txt, col):
            w = 4.0 * share
            r = Rectangle(width=w, height=0.28, stroke_width=0, fill_color=col, fill_opacity=0.75).move_to(
                [x + w / 2, y, 0])
            return VGroup(r, label(f"{txt}: \\ {100 * share:.1f}\\%", font_size=15, color=col).next_to(r, RIGHT,
                                                                                                   buff=0.12))
        b1 = VGroup(bar(-5.4, -1.6, sv["switch"], "switch", GOOD), bar(-5.4, -2.0, sv["don't switch"],
                                                                       "don't switch", DUTY))
        b2 = VGroup(bar(1.0, -1.6, sv["push"], "push", GOOD), bar(1.0, -2.0, sv["don't push"], "don't push", DUTY))
        cap = label(r"PhilPapers 2020, \ what ought one do?", font_size=15, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Philippa Foot introduced the case in 1967, and Judith Jarvis Thomson gave it its modern form. "
            "<bookmark mark='a'/>A runaway trolley will kill five people on the track ahead. You can switch it onto a "
            "side track, where it will kill one. Most people think you may. <bookmark mark='b'/>Now you stand on a "
            "footbridge beside a large man. Pushing him onto the track would stop the trolley and save the five, "
            "and he would die. Most people think you may not. <bookmark mark='c'/>In the 2020 survey, sixty three "
            "percent of philosophers would switch, and thirteen would not. Twenty two percent would push, and fifty "
            "six would not. One death against five, either way; why the difference?"
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(t1), FadeIn(l1))
            vo.wait_until("b")
            self.play(FadeIn(t2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(b1), FadeIn(b2), FadeIn(cap))
        self.clear_scene()

    def dde(self):
        d = load("trolley")
        head = label(r"The doctrine of double effect", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["rows"]
        assert [(r["case"], r["utilitarian"], r["double_effect"]) for r in rows] == [
            ("switch", "permissible", "permissible"), ("footbridge", "permissible", "impermissible"),
            ("loop", "permissible", "impermissible"), ("trapdoor", "permissible", "impermissible")]
        hd = [r"\text{case}", r"\text{the one's death is}", r"\text{utilitarian}", r"\text{double effect}"]
        cells = [[label(r["case"], font_size=18, color=WHITE), label(r["harm_is"], font_size=18, color=HARM),
                  label(r["utilitarian"], font_size=17, color=GOOD),
                  label(r["double_effect"], font_size=17, color=OK if r["double_effect"] == "permissible" else BAD)]
                 for r in rows]
        grid = ValueGrid(hd, cells, col_w=[2.2, 3.4, 2.6, 2.8], cell_h=0.55, font_size=17).move_to([0, 0.6, 0])
        rule = label(r"Aquinas: \ a harm may be foreseen as a side effect of a good act, \ never intended as a means",
                     font_size=19, color=DUTY).next_to(grid, UP, buff=0.35)
        foot = stack([(r"the loop \ (Thomson, \ 1985): \ the one's body stops the trolley, \ yet many judge "
                       r"switching still permissible", BAD),
                      (r"the trapdoor: \ no push, \ yet his fall is the means: \ intuitions follow personal force \ "
                       r"(Greene et al., \ 2009)", HARM)], font_size=18, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The traditional answer is the doctrine of double effect, which goes back to Thomas Aquinas. "
            "<bookmark mark='a'/>A harm may be accepted as a foreseen side effect of a good act, but never intended "
            "as a means to the good. <bookmark mark='b'/>In the switch case the one's death is a side effect: if he "
            "escaped, so much the better. In the footbridge case it is the means: his body stops the trolley. "
            "Utilitarianism permits both acts; double effect only the first. <bookmark mark='c'/>But in Thomson's "
            "loop case, the side track loops back, and the one's body is what stops the trolley; many still judge "
            "switching permissible. <bookmark mark='d'/>And if a trapdoor drops the man onto the track at the flick of "
            "a switch, people object less than to a push, though his fall is equally a means. Joshua Greene and "
            "colleagues found in 2009 that intuitions track personal force, which seems morally irrelevant."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rule))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), *[FadeIn(c) for k in range(2) for c in grid.cell[k]])
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[2]], FadeIn(foot[0]))
            vo.wait_until("d")
            self.play(*[FadeIn(c) for c in grid.cell[3]], FadeIn(foot[1]))
        self.clear_scene()

    def price(self):
        d = load("tetrad")
        claims = [(c["key"], c["text"]) for c in d["claims"]]
        assert d["mus"] == [["NODIFF", "ONLY", "PUSH", "SWITCH"]]
        assert sorted(d["mcs"]) == [["NODIFF"], ["ONLY"], ["PUSH"], ["SWITCH"]]
        sv = d["survey"]
        pl = PriceList(claims, mus=[tuple(m) for m in d["mus"]], radius=2.6, width=3.8, font_size=19,
                       center=[0, -0.6, 0], title=r"The Price List: \ the trolley")
        positions = [(("SWITCH",), r"don't switch", r"Thomson \ (2008)", sv["don't switch"],
                      r"PhilPapers 2020"),
                     (("PUSH",), r"push", r"Singer; \ Greene", sv["push"], r"PhilPapers 2020"),
                     (("ONLY",), r"another difference", r"redirecting a threat \ (Thomson, \ 1985); \ Kamm", None,
                      r""),
                     (("NODIFF",), r"means matter", r"double effect; \ Kant's humanity formula", None, r"")]
        with self.voiceover(
            "Four claims cannot all be true. <bookmark mark='a'/>Turning the trolley is permissible. Pushing the man "
            "is not. The cases differ only in that the one is used as a means. And harming as a means rather than as "
            "a side effect makes no moral difference. <bookmark mark='b'/>Something has to give. "
            "<bookmark mark='c'/>Thomson herself, in 2008, came to deny the first: you may not switch either. Thirteen "
            "percent of philosophers agree. <bookmark mark='d'/>Peter Singer and Joshua Greene deny the second: push, "
            "with twenty two percent. <bookmark mark='e'/>Others find a different difference: Thomson's early view "
            "that switching redirects an existing threat while pushing creates a new one, or Frances Kamm's subtler "
            "principles. <bookmark mark='f'/>And defenders of double effect and of Kant's humanity formula deny the "
            "fourth: using a person as a means is a distinct wrong."
        ) as vo:
            self.play(FadeIn(pl.title))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in pl.cards], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(Create(pl.conflict))
            first = True
            for mk, (mcs, name, who, share, note) in zip("cdef", positions):
                vo.wait_until(mk)
                if not first:
                    self.play(*pl.reset())
                first = False
                anims, centre = pl.position(mcs, name, who, share=share, share_note=note, width=3.0)
                self.play(*anims)
        self.clear_scene()

    def machine(self):
        head = label(r"Forty million decisions \ (Awad et al., \ 2018)", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"the Moral Machine", r"an online game: \ a driverless car must choose whom to spare; \ 40 million "
                                       r"decisions from 233 countries and territories", AGG),
                (r"near-universal", r"spare humans over animals, \ more lives over fewer, \ the young over the old",
                 GOOD),
                (r"varies by culture", r"the preference for sparing the young was weaker in an `Eastern' cluster of "
                                       r"countries", VIRT),
                (r"the caution", r"what people prefer is not what is right: \ and the dilemmas are rare on real roads",
                 HARM),
                (r"the lesson", r"intuitions are data for a theory, \ not the theory itself: \ Part 37 asks what they "
                                r"are evidence of", GOAL)]
        g = rows_table(rows, top=1.6, gap=0.45, width=8.4)
        with self.voiceover(
            "The trolley went global. <bookmark mark='a'/>The Moral Machine, an online game run by Edmond Awad and "
            "colleagues, asked people to choose whom a driverless car should spare; it gathered forty million "
            "decisions from two hundred and thirty three countries and territories, published in 2018. "
            "<bookmark mark='b'/>Some preferences were nearly universal: spare humans over animals, more lives over "
            "fewer, the young over the old. <bookmark mark='c'/>Others varied: the preference for sparing the young "
            "was weaker in a cluster of East Asian and Islamic countries. <bookmark mark='d'/>The authors cautioned "
            "that what people prefer is not thereby right, and such dilemmas are rare on real roads. "
            "<bookmark mark='e'/>Intuitions are data for a moral theory, not the theory itself; Part 37 asks what "
            "they are evidence of."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
