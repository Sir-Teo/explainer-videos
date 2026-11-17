from __future__ import annotations

import numpy as np

from videos.psychology.psych13.common import *  # noqa: F403


def stripes(pale, dark, w: float = 2.4, h: float = 3.0, n: int = 6) -> VGroup:
    g = VGroup()
    sh = h / n
    for i in range(n):
        c = pale if i % 2 == 0 else dark
        g.add(Rectangle(width=w, height=sh, stroke_width=0, fill_color=ManimColor.from_rgb(np.clip(c, 0, 1)),
                        fill_opacity=1).move_to([0, h / 2 - sh / 2 - i * sh, 0]))
    return g


class Dress(VoiceoverScene):
    def construct(self):
        self.card()
        self.constancy()
        self.dress()
        self.why()

    def card(self):
        card = chapter_card(11, r"Constancy and the dress", r"How can one picture have two colours?",
                            lit={2015: r"the dress"}, part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter eleven. Constancy, and the dress."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def constancy(self):
        head = heading(r"The light changes; \ the colour stays")
        from explainer.psychology.psyche import vision as V
        rows = rows_of([
            (r"the light from a surface is its reflectance times the illuminant", WHITE),
            (r"a white page under a warm lamp sends yellowish light, \ under a blue sky bluish light, \ yet it looks "
             r"white in both", LIGHT),
            (r"to see the surface, \ the visual system must estimate the light and discount it", CENTRE),
            (r"the simplest way, \ von Kries, \ 1905: \ scale each cone type's signal by its response to the light "
             r"itself", GREY_A),
        ], 7.0, 27, 0.34).move_to([2.6, -0.2, 0])
        keep_in_frame(rows)
        eq = MathTex(r"L' = \frac{L}{L_{\text{light}}},\quad M' = \frac{M}{M_{\text{light}}},\quad S' = \frac{S}{S_{\text{light}}}",
                     font_size=32).next_to(rows, DOWN, buff=0.35)
        warm = V.srgb(V.to_xyz(V.planck(2856)), None)
        cool = V.srgb(V.to_xyz(V.planck(12000)), None)
        pw = swatch(warm, 1.4).move_to([-4.6, 0.9, 0])
        pc = swatch(cool, 1.4).move_to([-4.6, -1.0, 0])
        lw = label(r"a warm lamp", font_size=22, color=GREY_A).next_to(pw, LEFT, buff=0.15)
        lc = label(r"a blue sky", font_size=22, color=GREY_A).next_to(pc, LEFT, buff=0.15)
        tag = psyche_tag(r"computed: \ a white surface under two lights")
        with self.voiceover(
            "There's a third problem colour has to solve. <bookmark mark='a'/> The light coming from a surface is "
            "its reflectance multiplied by the light falling on it. <bookmark mark='b'/> So a white page under a "
            "warm lamp sends your eye yellowish light, and under a blue sky, bluish light. Yet it looks white in "
            "both. That's colour constancy. <bookmark mark='c'/> To see the surface, the visual system has to "
            "estimate the light, and discount it. <bookmark mark='d'/> The simplest way, proposed by Johannes von "
            "Kries in 1905, is to divide each cone type's signal by its response to the light itself. Adaptation, "
            "from chapter three, does something like this automatically."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(pw), FadeIn(pc), FadeIn(lw), FadeIn(lc))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r))
            self.play(FadeIn(eq))
        self.clear_scene()

    def dress(self):
        d = load("dress")
        head = heading(r"February 2015: \ the dress")
        orig = stripes(d["pale"], d["dark"]).move_to([-4.6, 0.25, 0])
        warm = stripes(d["pale_warm"], d["dark_warm"]).move_to([0, 0.25, 0])
        cool = stripes(d["pale_cool"], d["dark_cool"]).move_to([4.6, 0.25, 0])
        lo = label(r"the pixels", font_size=24, color=GREY_A).next_to(orig, UP, buff=0.2)
        lw = wrapped_label(r"assume a warm light, \ discount it: \ blue and black", 3.6, 24, SCONE).next_to(warm, UP, buff=0.2)
        lc = wrapped_label(r"assume a cool, \ bluish light: \ white and gold", 3.6, 24, LIGHT).next_to(cool, UP, buff=0.2)
        a1 = Arrow(orig.get_right(), warm.get_left(), buff=0.2, color=GREY_B)
        a2 = CurvedArrow(orig.get_bottom() + DOWN * 0.1, cool.get_bottom() + DOWN * 0.1, angle=PI / 5, color=GREY_B)
        cap = wrapped_label(r"one image, \ two assumed illuminants, \ two dresses", 12.0, 28, WHITE).to_edge(DOWN, buff=0.8)
        tags = VGroup(note(r"a stand-in swatch with colours like the photograph's; \ not the photograph").to_corner(DL, buff=0.3),
                      psyche_tag(r"computed: \ von Kries under a 3000 K and a 12000 K light"))
        with self.voiceover(
            "In February 2015 a photograph of a striped dress went around the world, because people couldn't agree "
            "on its colours. Some saw blue and black. Others, just as sure, saw white and gold. "
            "<bookmark mark='a'/> Here is a swatch with colours like the photograph's: a pale, washed-out blue, and "
            "a dark golden brown. Not the photograph itself, but the same problem. <bookmark mark='b'/> Suppose your "
            "visual system assumes the dress is lit by warm, yellowish light. Discount that, and the pale stripes "
            "become distinctly blue, and the dark ones nearly black. <bookmark mark='c'/> Suppose instead it assumes "
            "the dress is in cool, bluish light, in shade under a blue sky. Discount that, and the pale stripes "
            "become white, and the dark ones gold. The image is genuinely ambiguous about the light, and the two "
            "answers both make sense."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags))
            vo.wait_until("a")
            self.play(FadeIn(orig), FadeIn(lo))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(warm), FadeIn(lw))
            vo.wait_until("c")
            self.play(Create(a2), FadeIn(cool), FadeIn(lc), FadeIn(cap))
        self.clear_scene()

    def why(self):
        d = load("dress")
        head = heading(r"Who saw what, \ and why")
        bb, wg, br, ot = d["survey"]
        bar = share_bar([bb, wg, br, ot], [SCONE, LIGHT, "#8B6B4A", GREY_C], width=11.0, height=0.7,
                        names=[rf"blue-black {pct(bb)}", rf"white-gold {pct(wg)}", "", ""],
                        font_size=24).move_to([0, 1.6, 0])
        rest = label(rf"blue-brown {pct(br)}, \ other {pct(ot)}", font_size=22, color="#C9A27E")
        rest.next_to(bar.parts[2], DOWN, buff=0.15).align_to(bar, RIGHT)
        rows = rows_of([
            (rf"Lafer-Sousa, \ Hermann and Conway, \ 2015: \ about {num(d['n'])} people online", WHITE),
            (r"the authors' account: \ those who saw white and gold were discounting a bluish light; \ more of them "
             r"were older, \ and more were women", LIGHT),
            (r"Wallisch, \ 2017, \ two surveys of 8{,}084 and 5{,}333: \ people who assumed the dress was in shadow saw "
             r"white and gold more often", GREY_A),
            (r"why people differ in what they assume about the light is less settled, \ and the effects are modest", GREY_B),
            (r"perception is a bet about the world: \ Part 14", YOU),
        ], 12.4, 26, 0.3).move_to([0, -1.2, 0])
        tag = published_tag(r"Lafer-Sousa, Hermann \& Conway (2015); \ Wallisch (2017)")
        with self.voiceover(
            "Who saw what? <bookmark mark='a'/> Rosa Lafer-Sousa, Katherine Hermann and Bevil Conway surveyed about "
            "fourteen hundred people online. Fifty-seven percent saw blue and black, thirty percent white and gold, "
            "and eleven percent blue and brown. <bookmark mark='b'/> Their account is that the white and gold group "
            "were discounting a bluish light, and they were more often older, and more often women. "
            "<bookmark mark='c'/> In 2017 Pascal Wallisch ran two much larger surveys and asked people how they "
            "thought the dress was lit. Those who assumed it was in shadow saw white and gold more often. "
            "<bookmark mark='d'/> Why people differ in their assumptions about light, whether age, or how much time "
            "they spend in daylight, is less settled, and the effects found are modest. <bookmark mark='e'/> But the "
            "lesson is the one Part 14 is built on. Seeing a colour is a bet about the world, and different brains "
            "can place different bets on the same picture."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(bar), FadeIn(rest), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
