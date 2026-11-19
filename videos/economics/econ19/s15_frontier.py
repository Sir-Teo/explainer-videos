from __future__ import annotations

from videos.economics.econ19.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 13, r"Frontier: \ deep roots and persistence", r"Does the distant past still decide which countries "
             r"are rich, \ and how would we know?", "Chapter thirteen. Frontier: deep roots and persistence.",
             lit={2009: r"Spolaore and Wacziarg", 2013: r"Ashraf and Galor", 2019: r"Kelly"},
             scale=("nation", "world"), horizon=("a century",))
        self.roots()
        self.noise()
        self.open_q()

    def roots(self):
        rows = VGroup(
            label(r"if the escape spread from north-western Europe, \ who caught it first, \ and why?", font_size=24),
            label(r"Comin, \ Easterly and Gong, \ 2010: \ technology in 1500, \ and even 1000 BC, \ predicts income "
                  r"today", font_size=21, color=TECH),
            label(r"Spolaore and Wacziarg, \ 2009: \ populations more distant in ancestry from the leaders \\ "
                  r"adopted new ideas later: \ barriers of language and custom", font_size=21, color=EDU),
            label(r"Ashraf and Galor, \ 2013: \ genetic diversity and income, \ a hump", font_size=21, color=POP),
            label(r"sharply criticized, \ by anthropologists and geneticists, \ for what such data can mean",
                  font_size=21, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Comin, Easterly and Gong, AEJ Macro 2(3) (2010); \ Spolaore and Wacziarg, QJE 124(2) "
                            r"(2009); \ Ashraf and Galor, AER 103(1) (2013)", corner=DR, font_size=11)
        with self.voiceover(
            "The frontier asks how deep the roots of the escape go. <bookmark mark='a'/> If it spread out from "
            "north-western Europe, who caught it first, and why? <bookmark mark='b'/> Diego Comin, William Easterly "
            "and Erick Gong found that the technologies a region used in 1500, and even in 1000 BC, predict its "
            "income today. <bookmark mark='c'/> Enrico Spolaore and Romain Wacziarg found that populations more "
            "distant in ancestry from the leaders adopted new ideas later, and read it as a barrier of language and "
            "custom to the spread of know-how, not as anything in the genes themselves. <bookmark mark='d'/> "
            "Quamrul Ashraf and Oded Galor went further, relating a country's genetic diversity to its income. "
            "<bookmark mark='e'/> That paper was sharply criticized by anthropologists and geneticists for what such "
            "data can and cannot mean."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def noise(self):
        nz = load("noise")
        bars = plane([-0.6, 1.6], [0, 0.7], center=LEFT * 3.0 + DOWN * 0.5, x_length=5.0, y_length=4.4,
                     yticks=[0, 0.05, 0.2, 0.4, 0.6], ylabel=r"share called significant", font_size=17,
                     yfmt=lambda v: f"{v:g}")
        vals = [(nz["independent"]["reject"], r"no spatial \\ pattern", GREY_B),
                (nz["smooth"]["reject"], r"smooth \\ patterns", DEATH)]
        bg = VGroup()
        for k, (v, name, c) in enumerate(vals):
            r = Polygon(bars.ax.c2p(k - 0.3, 0), bars.ax.c2p(k + 0.3, 0), bars.ax.c2p(k + 0.3, v), bars.ax.c2p(k - 0.3, v),
                        stroke_width=0, fill_color=c, fill_opacity=0.85)
            bg.add(VGroup(r, label(rf"{100 * v:.0f}\%", font_size=22, color=WHITE).next_to(r, UP, buff=0.08),
                          label(name, font_size=18, color=GREY_A).next_to(bars.ax.c2p(k, 0), DOWN, buff=0.12)))
        five = DashedLine(bars.ax.c2p(-0.6, 0.05), bars.ax.c2p(1.6, 0.05), color=E.ACCENT, stroke_width=2)
        rows = VGroup(
            label(r"Morgan Kelly, \ 2019: \ many persistence studies regress \\ one map on another", font_size=21),
            label(rf"Agora: \ {nz['n_sites']} places, \ two unrelated random maps, \ {nz['reps']} times", font_size=21,
                  color=GREY_A),
            label(rf"with no pattern, \ {100 * nz['independent']['reject']:.0f}\% look significant, \ as they should",
                  font_size=21, color=GREY_B),
            label(rf"with smooth patterns, \ {100 * nz['smooth']['reject']:.0f}\% do", font_size=22, color=DEATH),
            label(r"nearby places are not independent evidence: \\ standard errors must allow for space", font_size=21,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35).shift(UP * 0.4)
        for r in rows:
            if r.width > 6.4:
                r.width = 6.4
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "There is also a warning about method. <bookmark mark='a'/> Morgan Kelly noticed that many persistence "
            "studies regress one map on another: a medieval pattern against a modern one. Nearby places resemble "
            "each other, in both. <bookmark mark='b'/> Agora shows what that does. Take "
            f"{nz['n_sites']} places, draw two random maps that have nothing to do with each other, regress one on "
            f"the other, and repeat {nz['reps']} times. <bookmark mark='c'/> If the maps have no spatial pattern, "
            f"about {100 * nz['independent']['reject']:.0f} percent of the regressions look significant, as they "
            "should. <bookmark mark='d'/> If each map varies smoothly over space, like most real ones, about "
            f"{100 * nz['smooth']['reject']:.0f} percent do. <bookmark mark='e'/> Nearby places are not independent "
            "pieces of evidence, and standard errors that pretend they are can find deep roots in pure noise."
        ) as vo:
            self.play(FadeIn(bars), Create(five), FadeIn(rows[0]), FadeIn(tag))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(bg[0], shift=UP * 0.1), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(bg[1], shift=UP * 0.1), FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()

    def open_q(self):
        head = label(r"open questions", font_size=32, color=E.ACCENT).to_edge(UP, buff=0.5)
        qs = VGroup(
            label(r"was the escape inevitable once ideas could spread, \ or an accident of one island?", font_size=23),
            label(r"how much did empire, \ slavery and colonial trade contribute to it?", font_size=23),
            label(r"can poor countries today repeat it faster, \ and with what? \ (part 46)", font_size=23),
            label(r"will growth continue if populations shrink, \ as Kremer's logic suggests it may not?",
                  font_size=23),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Some questions remain open. <bookmark mark='a'/> Was the escape inevitable once ideas could spread, or "
            "an accident of one island? <bookmark mark='b'/> How much did empire, slavery and colonial trade "
            "contribute to it? <bookmark mark='c'/> Can poor countries repeat it faster today, and with what? Part "
            "forty-six takes that up. <bookmark mark='d'/> And if more people meant more ideas, what happens to "
            "growth when populations begin to shrink?"
        ) as vo:
            self.play(FadeIn(head), FadeIn(qs[0]))
            for mk, q in zip("bcd", qs[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(q, shift=RIGHT * 0.15))
        self.clear_scene()
