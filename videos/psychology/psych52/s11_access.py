from __future__ import annotations

from videos.psychology.psych52.common import *  # noqa: F403


class Access(VoiceoverScene):
    def construct(self):
        card_section(self, 10, r"Accessibility as psychophysics", r"Who can read this?", scale=("person", "society"))
        self.contrast()
        self.colour()
        self.motor()

    def contrast(self):
        d = load("contrast")
        head = heading(r"Contrast, \ computed")
        sw = VGroup()
        for name, fg, bg, r in zip(d["names"], d["fg"], d["bg"], d["ratio"]):
            box = Rectangle(width=2.0, height=0.62, fill_color=rgb_to_color(np.asarray(bg) / 255), fill_opacity=1,
                            stroke_color=GREY_D, stroke_width=1)
            txt = label(r"Aa", font_size=24, color=rgb_to_color(np.asarray(fg) / 255)).move_to(box)
            ok = r >= 4.5
            sw.add(VGroup(VGroup(box, txt), label(name, font_size=15, color=GREY_A),
                          label(rf"{r:.1f} : 1", font_size=18, color=GOOD if ok else AUTH)).arrange(RIGHT, buff=0.3))
        sw.arrange(DOWN, buff=0.18, aligned_edge=LEFT).move_to([-3.4, -0.2, 0])
        rows = rows_of([
            (r"WCAG's contrast ratio: \ $(L_1 + 0.05)/(L_2 + 0.05)$, \ from each colour's relative luminance; \ 1 to "
             r"21", WHITE),
            (r"normal text needs 4.5 : 1 (level AA): \ the grey 767676 on white just passes, \ at 4.5", GOOD),
            (r"the threshold comes from Part 13: \ contrast sensitivity falls with age and low vision, \ so the margin "
             r"is for them", MODEL),
            (r"red on green has almost no luminance contrast: \ 1.3 : 1, \ and for many colour-blind readers, \ none "
             r"at all", AUTH),
        ], 6.0, 19, 0.36).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{work.contrast\_ratio}")
        with self.voiceover(
            "Accessibility is psychophysics with a standard attached. <bookmark mark='a'/> The web's contrast ratio is "
            "computed from each colour's relative luminance, and runs from one to twenty-one. <bookmark mark='b'/> "
            "Normal text needs four and a half to one. This mid grey on white just passes. <bookmark mark='c'/> The "
            "threshold comes from Part 13. Contrast sensitivity falls with age and with low vision, so the margin is "
            "for them. <bookmark mark='d'/> Red on green has almost no luminance contrast, about one point three, and "
            "for many colour-blind readers, none at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), LaggedStart(*[FadeIn(s_) for s_ in sw], lag_ratio=0.2))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def colour(self):
        rows_section(self, r"Colour-vision deficiency", [
            (r"about one man in twelve and one woman in two hundred of Northern European descent has a red-green "
             r"deficiency (Part 13's cones)", WHITE),
            (r"a chart that separates its lines only by red and green separates nothing for them", AUTH),
            (r"redundant coding: \ colour plus shape, \ position, \ labels or dashes", GOOD),
            (r"palettes chosen to differ in lightness as well as hue survive both deficiency and grey-scale printing",
             MODEL),
        ], "Colour vision differs too. <bookmark mark='a'/> About one man in twelve, and one woman in two hundred, of "
           "Northern European descent has a red-green deficiency, from Part 13's cones. <bookmark mark='b'/> A chart "
           "that separates its lines only by red and green separates nothing for them. <bookmark mark='c'/> The fix "
           "is redundant coding: colour plus shape, position, labels or dashes. <bookmark mark='d'/> And palettes that "
           "differ in lightness as well as hue survive both colour deficiency and printing in grey.")

    def motor(self):
        chips_section(self, r"Size, \ time and motor tolerance", [
            (r"text size", r"acuity falls with age: \ text that can be enlarged, \ and layouts that reflow", PERSON),
            (r"targets", r"Fitts's law for a tremor: \ larger targets and more space between them", MODEL),
            (r"time limits", r"Part 31's slower processing: \ adjustable or no time limits", SYMP),
            (r"other routes", r"keyboard-only use, \ screen readers and captions: \ the same task by another sense",
             GOOD),
        ], "Motor and cognitive tolerances follow the same logic. <bookmark mark='a'/> Acuity falls with age, so text "
           "should be enlargeable, and layouts should reflow. <bookmark mark='b'/> Fitts's law for a hand with a "
           "tremor means larger targets with more space between them. <bookmark mark='c'/> Part 31's slower "
           "processing in later life means adjustable time limits, or none. <bookmark mark='d'/> And other routes, "
           "keyboard-only use, screen readers and captions, give the same task to another sense. Designs that work "
           "at the edges of the population usually work better for everyone.")
