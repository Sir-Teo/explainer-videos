from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Hunger(VoiceoverScene):
    def construct(self):
        self.card()
        self.signals()
        self.settling()
        self.defended()
        self.regain()

    def card(self):
        card = chapter_card(2, r"Hunger as control", r"Why does lost weight come back?",
                            lit={1940: r"Hetherington \& Ranson", 1994: r"leptin", 1999: r"ghrelin",
                                 2011: r"Hall et al."},
                            part=PART, scale=("molecule", "brain", "person"), marr=("what", "tissue"))
        with self.voiceover("Chapter two. Hunger as control."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def signals(self):
        head = heading(r"The loop's signals")
        hyp = Circle(radius=0.9, color=WANT, fill_opacity=0.15).move_to([-3.4, 0.3, 0])
        hyp_l = label(r"hypothalamus", font_size=20, color=WANT).move_to(hyp)
        fat = RoundedRectangle(corner_radius=0.15, width=1.8, height=0.8, color=BODY, fill_opacity=0.15).move_to(
            [-5.6, -2.2, 0])
        gut = RoundedRectangle(corner_radius=0.15, width=1.8, height=0.8, color=EXTR, fill_opacity=0.15).move_to(
            [-1.2, -2.2, 0])
        fat_l = label(r"fat", font_size=20, color=BODY).move_to(fat)
        gut_l = label(r"stomach", font_size=20, color=EXTR).move_to(gut)
        a1 = Arrow(fat.get_top(), hyp.get_left() + DOWN * 0.3, color=BODY, buff=0.1, stroke_width=3)
        a2 = Arrow(gut.get_top(), hyp.get_right() + DOWN * 0.3, color=EXTR, buff=0.1, stroke_width=3)
        l1 = label(r"leptin: \ stores are full", font_size=17, color=BODY).next_to(fat, DOWN, buff=0.15)
        l2 = label(r"ghrelin: \ time to eat", font_size=17, color=EXTR).next_to(gut, DOWN, buff=0.15)
        rows = rows_of([
            (r"1940s and 1950s: \ lesions in one part of a rat's hypothalamus make it overeat and grow obese; \ in "
             r"another, \ it stops eating", WANT),
            (r"1994: \ the gene for leptin, \ a hormone made by fat; \ mice without it eat without limit", BODY),
            (r"1999: \ ghrelin, \ a hormone from the stomach that rises before meals", EXTR),
            (r"leptin cures the rare people born without it, \ but not ordinary obesity: \ most people with more fat "
             r"already have more leptin", LOST),
        ], 5.6, 22, 0.34).move_to([3.5, -0.1, 0])
        tag = published_tag(r"Hetherington \& Ranson (1940); \ Zhang et al.\ (1994); \ Kojima et al.\ (1999)")
        with self.voiceover(
            "Hunger is the loop everyone knows from the inside. <bookmark mark='a'/> In the 1940s and 1950s, small "
            "lesions in one part of a rat's hypothalamus made it overeat until it was obese, and lesions in a nearby "
            "part made it stop eating. The brain had a controller. <bookmark mark='b'/> In 1994 Jeffrey Friedman's "
            "laboratory found one of its sensors: the gene for leptin, a hormone made by fat cells, which tells the "
            "brain how full the stores are. Mice without it eat without limit. <bookmark mark='c'/> In 1999 a "
            "Japanese group found a signal in the other direction, ghrelin, made in the stomach, which rises before "
            "meals. <bookmark mark='d'/> Leptin seemed like a cure for obesity, and for the few people born unable "
            "to make it, it is. But most people with more fat already have more leptin. The controller is not "
            "short of a signal; it defends a different level."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hyp), FadeIn(hyp_l))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(hyp))
            vo.wait_until("b")
            self.play(FadeIn(fat), FadeIn(fat_l), GrowArrow(a1), FadeIn(l1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(gut), FadeIn(gut_l), GrowArrow(a2), FadeIn(l2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def settling(self):
        d = load("weight")
        head = heading(r"Derivation: \ a diet as a loop")
        eqs = VGroup(
            MathTex(r"\rho\,\frac{dW}{dt} = I - E(W)", font_size=38),
            MathTex(r"E(W) = E_0 + a\,(W - W_0)", font_size=34),
            MathTex(r"\text{cut } c: \ \Delta W_\infty = \frac{c}{a}, \quad \tau = \frac{\rho}{a}", font_size=34),
        ).arrange(DOWN, buff=0.4)
        rows = rows_of([
            (r"$\rho$: \ about 7{,}700 kcal in a kilogram of body tissue; \ $a$: \ about 24 kcal a day more "
             r"burned for each extra kilogram", WHITE),
            (rf"cut 500 kcal a day: \ the static rule promises {d['static_loss']:.0f} kg in 300 days, \ and more for "
             r"ever after", LOST),
            (rf"the loop: \ weight heads for a settling point {d['settle_steady']:.0f} kg lower, \ with a time "
             rf"constant of {d['settle_tau']:.0f} days; \ {d['settle_loss']:.0f} kg in 300 days", BODY),
        ], 5.6, 21, 0.3)
        right = VGroup(eqs, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, -0.1, 0])
        A = axes([0, 1100], [55, 82], x_length=5.8, y_length=3.8, xticks=[0, 365, 730, 1095], yticks=[60, 70, 80],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"days", ylabel=r"weight, \ kg",
                 center=[-3.4, -0.2, 0], font_size=16)
        diet = Rectangle(width=abs(A.ax.c2p(400, 0)[0] - A.ax.c2p(100, 0)[0]), height=3.8 * 0.98, stroke_width=0,
                         fill_color=GREY_D, fill_opacity=0.35).move_to([(A.ax.c2p(100, 0)[0] + A.ax.c2p(400, 0)[0]) / 2,
                                                                         A.ax.c2p(0, 68.5)[1], 0])
        dl = label(r"diet", font_size=16, color=GREY_B).next_to(diet, UP, buff=0.05)
        cs = curve(A.ax, d["day"], np.maximum(d["static"], 55.0), LOST, 3)
        cw = curve(A.ax, d["day"], d["settle"], BODY, 4)
        key = legend([(LOST, r"3{,}500 kcal a pound"), (BODY, r"the loop")], font_size=16).move_to(A.ax.c2p(860, 81))
        tag = psyche_tag(r"\texttt{drive.body\_weight}, \ \texttt{static\_rule}; \ Hall et al.\ (2011)")
        with self.voiceover(
            "Put weight into the same kind of equation. <bookmark mark='a'/> Body mass changes with the difference "
            "between energy in and energy out, divided by the energy stored in a kilogram of tissue. Energy out "
            "rises with weight: a heavier body burns more. <bookmark mark='b'/> A kilogram of tissue holds about "
            "seventy-seven hundred kilocalories, and Kevin Hall and his colleagues' models put the extra burn at "
            "roughly twenty-four kilocalories a day for each extra kilogram. <bookmark mark='c'/> The old rule of "
            "thumb, thirty-five hundred kilocalories to a pound, ignores the loop. Cut five hundred kilocalories a "
            f"day and it promises {d['static_loss']:.0f} kilograms in three hundred days, and more for ever. "
            "<bookmark mark='d'/> The loop says otherwise. As weight falls, the body burns less, so loss slows and "
            f"weight heads for a settling point {d['settle_steady']:.0f} kilograms lower, with a time constant of "
            f"nearly a year. After three hundred days it has lost {d['settle_loss']:.0f}, not {d['static_loss']:.0f}. "
            "And when the diet ends, weight drifts back, because nothing holds it at the new level."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(diet), FadeIn(dl))
            vo.wait_until("a")
            self.play(Write(eqs[0]), Write(eqs[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(Create(cs), FadeIn(key[0]), FadeIn(rows[1]), FadeIn(eqs[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(Create(cw), FadeIn(key[1]), FadeIn(rows[2]), run_time=2.0)
        self.clear_scene()

    def defended(self):
        d = load("weight")
        head = heading(r"A weight that defends itself")
        A = axes([0, 1100], [55, 82], x_length=5.8, y_length=3.8, xticks=[0, 365, 730, 1095], yticks=[60, 70, 80],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"days", ylabel=r"weight, \ kg",
                 center=[-3.4, -0.2, 0], font_size=16)
        cw = curve(A.ax, d["day"], d["settle"], BODY, 3)
        cd = curve(A.ax, d["day"], d["defend"], WANT, 4)
        key = legend([(BODY, r"settling point"), (WANT, r"defended set point")], font_size=16).move_to(
            A.ax.c2p(820, 62))
        eq = VGroup(MathTex(r"I = I_0 + h\,(s - W)^+", font_size=30),
                    MathTex(r"E = E_0 + a\,(W - W_0) - g\,(s - W)^+", font_size=30)).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.2)
        rows = rows_of([
            (r"below the set point $s$, \ hunger rises \ ($h$, \ more eaten) \ and the body economizes \ ($g$, "
             r"\ less burned)", WANT),
            (rf"the loop is stiffer: \ the same diet loses {d['defend_loss']:.1f} kg, \ not {d['settle_loss']:.0f}",
             WHITE),
            (rf"by the diet's end the dieter eats {d['defend_intake_gap']:.0f} kcal a day more than planned, "
             rf"\ and burns {d['defend_out_gap']:.0f} less than at the start", LOST),
            (r"when the diet stops, \ the lost weight returns within months", WANT),
        ], 5.6, 21, 0.3)
        right = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.body\_weight}: \ $h = 60$, \ $g = 25$ kcal a day per kg; \ illustrative")
        with self.voiceover(
            "Now let the body defend a set point. <bookmark mark='a'/> Below it, two things happen. Hunger rises, "
            "so more is eaten. And the body economizes, burning less than its size alone would predict; physiologists "
            "call it adaptive thermogenesis. <bookmark mark='b'/> The loop becomes stiffer. The same diet, kept just "
            f"as faithfully, now loses only {d['defend_loss']:.1f} kilograms. <bookmark mark='c'/> By the end, the "
            f"dieter eats about {d['defend_intake_gap']:.0f} kilocalories a day more than the plan, without "
            f"deciding to, and burns about {d['defend_out_gap']:.0f} fewer than at the start. "
            "<bookmark mark='d'/> And when the diet stops, the lost weight returns within months. The numbers for "
            "hunger and economy here are illustrative, not measured, but the shape is the point: a defended loop "
            "makes willpower fight a controller."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(cw), FadeIn(key[0]), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cd), FadeIn(key[1]), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def regain(self):
        head = heading(r"Set point, \ or settling point?")
        rows = rows_of([
            (r"after large weight loss, \ people burn less than their new size predicts, \ and are hungrier: "
             r"\ measured in controlled studies, \ and still present years later in some", WANT),
            (r"but weight is not held at one value for life: \ it drifts with food, \ age and surroundings, \ "
             r"like a settling point", BODY),
            (r"the current view mixes the two: \ defence against loss is stronger than defence against gain", WHITE),
            (r"motivation enters through the loop: \ hunger is the controller's way of making food worth more",
             EXTR),
        ], 12.2, 27, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Leibel, \ Rosenbaum \& Hirsch (1995); \ Hall et al.\ (2011); \ Fothergill et al.\ "
                            r"(2016)")
        with self.voiceover(
            "Is there really a set point? <bookmark mark='a'/> After large weight loss, people burn less energy "
            "than their new size predicts, and feel hungrier. That has been measured in controlled studies since "
            "the 1990s, and in a follow-up of contestants from a televised weight-loss competition it was still "
            "there six years later. <bookmark mark='b'/> But weight isn't fixed at one value for life. It drifts "
            "with what food is around, with age, with surroundings, more like a settling point than a set point. "
            "<bookmark mark='c'/> The current view mixes the two: the body defends against loss more strongly than "
            "against gain. <bookmark mark='d'/> And this is where motivation enters. Hunger is the controller's way "
            "of making food worth more. The rest of this part is about that worth."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
