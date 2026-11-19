from __future__ import annotations

from videos.economics.econ15.common import *  # noqa: F403

YOU = "#7BD88F"


def chip(text, color, w=1.6, font_size=26) -> VGroup:
    box = RoundedRectangle(width=w, height=0.75, corner_radius=0.12, stroke_color=color, stroke_width=3,
                           fill_color=BACKGROUND, fill_opacity=1)
    t = label(text, font_size=font_size, color=color).move_to(box)
    return VGroup(box, t)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ the shared pot", r"Four islanders, \ twenty shells each, \ one pot that grows. "
             r"\ How many shells do you put in?", "Chapter one. Play it: the shared pot.",
             lit={1979: r"Marwell and Ames", 1995: r"Ledyard's survey"}, scale=("person", "community"),
             horizon=("a day",))
        self.rules()
        self.reveal()
        self.dilemma()

    def rules(self):
        p = load("playit")
        stage = game_stage(12.0, 5.8, center=DOWN * 0.2)
        rules = VGroup(
            label(rf"you and three other islanders each hold {p['endowment']:.0f} shells", font_size=24),
            label(r"each of you, in secret, puts some shells into a shared pot", font_size=24),
            label(rf"the pot is multiplied by {p['multiplier']:.1f} \ and shared equally among all four", font_size=24,
                  color=POT),
            label(r"you keep whatever you didn't put in, \ plus your quarter of the pot", font_size=24),
            label(r"how many do you put in?", font_size=27, color=E.ACCENT),
        ).arrange(DOWN, buff=0.24).move_to(stage.box.get_center() + UP * 1.0)
        chips = VGroup(*[chip(rf"{g}", YOU) for g in p["gives"] if True]).arrange(RIGHT, buff=0.45).next_to(
            rules, DOWN, buff=0.4)
        who = VGroup(*[islander(k, 0.6) for k in ("ana", "bo", "chidi", "dara")]).arrange(RIGHT, buff=0.35).move_to(
            stage.box.get_corner(DR) + LEFT * 1.9 + UP * 0.7)
        ring = countdown().next_to(chips, DOWN, buff=0.35)
        with self.voiceover(
            "This time you are one of four islanders, and each of you holds twenty shells. Each of you, in secret, "
            "puts some of your shells into a shared pot. The pot is then multiplied by one point six, and shared "
            "equally among all four, whoever put in what. You keep whatever you didn't put in, plus your quarter of "
            "the pot. How many shells do you put in: none, five, ten, or all twenty? Pause, and choose."
        ):
            self.play(FadeIn(stage), FadeIn(rules[0]), FadeIn(who))
            self.play(FadeIn(rules[1]), FadeIn(rules[2]), run_time=1.5)
            self.play(FadeIn(rules[3]), FadeIn(rules[4]),
                      LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in chips], lag_ratio=0.2), run_time=2)
            self.play(FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.clear_scene()

    def reveal(self):
        p = load("playit")
        others = np.array(p["others"])
        ax = plane([0, 60], [0, 46], center=LEFT * 2.8 + DOWN * 0.3, x_length=6.4, y_length=4.6,
                   xticks=[0, 20, 40, 60], yticks=[0, 10, 20, 30, 40], xlabel=r"what the other three put in, \ in all",
                   ylabel=r"your shells at the end", font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        cols = [YOU, DEMAND, SOCIAL, POT]
        lines = VGroup(*[path(ax, others, r["pay_curve"], color=c, width=3, smooth=False)
                         for r, c in zip(p["rows"], cols)])
        labs = VGroup(*[label(rf"you give {r['give']}", font_size=15, color=c).next_to(
            a.c2p(60, r["pay_curve"][-1]), RIGHT, buff=0.1) for r, c in zip(p["rows"], cols)])
        side = VGroup(
            label(r"each shell you put in costs you 1 \\ and returns 0.4 to you", font_size=21, color=SOCIAL),
            label(r"so whatever the others do, \\ giving less leaves you with more", font_size=21, color=YOU),
            label(r"but each shell you give \\ is worth 1.6 to the four together", font_size=21, color=POT),
            label(rf"if all give everything: \ {p['all_give']:.0f} each; \\ if none give: \ {p['none_give']:.0f} each",
                  font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is what you end up with, against what the other three put in, for each of your choices. "
            "<bookmark mark='a'/> Each shell you put in costs you one shell, and comes back to you as a quarter of "
            "one point six: four tenths of a shell. <bookmark mark='b'/> So whatever the others do, the fewer you "
            "give, the more you end with. The four lines never cross, and giving nothing is always on top. "
            "<bookmark mark='c'/> But each shell you give is worth one point six to the four of you together. "
            "<bookmark mark='d'/> If everyone gives everything, each of you ends with thirty-two shells. If nobody "
            "gives anything, each ends with the twenty they started with."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(lines), FadeIn(labs), run_time=2)
            for mk, r in zip("abcd", side):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
                if mk == "b":
                    self.play(Indicate(lines[0], color=YOU), Indicate(labs[0]))
        self.clear_scene()

    def dilemma(self):
        rows = VGroup(
            label(r"what is best for each \ is worst for all: \ a prisoner's dilemma with four players", font_size=25,
                  color=E.ACCENT),
            label(r"the extra 0.6 of every shell you give \ lands on the other three: \ a spillover", font_size=24,
                  color=POT),
            label(r"so the pot is a public good, \ and the shells you keep are free riding", font_size=24,
                  color=SOCIAL),
            label(r"in laboratories since the 1970s, \ people give about half at first", font_size=24, color=GREY_A),
            label(r"what happens next, \ round after round, \ is chapter seven", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Marwell and Ames (1979); \ Ledyard, in the Handbook of Experimental Economics (1995)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "This is part eleven's prisoner's dilemma, with four players. <bookmark mark='a'/> What is best for each "
            "of you is worst for all of you. <bookmark mark='b'/> The reason is a spillover: of the one point six "
            "that each shell becomes, only four tenths come back to you. The rest lands on the other three, and you "
            "are not paid for it. <bookmark mark='c'/> The pot is a public good, and keeping your shells is free "
            "riding on the others. <bookmark mark='d'/> Economists have run this game in laboratories since the "
            "1970s. On a first play, people put in about half. <bookmark mark='e'/> What happens when they play "
            "again, and again, is chapter seven."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
