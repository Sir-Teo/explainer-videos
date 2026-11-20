from __future__ import annotations

from videos.economics.econ41.common import *  # noqa: F403


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Play it: \ set the top rate from three numbers", r"What rate raises the most from the top?",
             "Chapter three. Play it: set the top rate from three numbers.", lit={2001: r"Saez", 2011: r"Diamond and "
                                                                                                     r"Saez"},
             scale=("person", "nation"), horizon=("a year",))
        self.ask()
        self.reveal()
        self.curves()

    def ask(self):
        P = load("top")
        nums = VGroup()
        for sym, val, nm, col in ((r"$a$", f"{P['a']:.2f}", r"the shape of the top: \\ the mean income above \\ any "
                                                             r"top threshold is \\ $a/(a-1)$ times it", TOP),
                                  (r"$e$", "0.25", r"how much top incomes \\ fall when the share \\ kept falls 1\%: "
                                                   r"\ 0.25\%", RATE),
                                  (r"$g$", "0", r"the value society puts \\ on one more dollar for \\ a top earner: \ "
                                                r"none", WORKER)):
            box = RoundedRectangle(width=3.9, height=2.6, corner_radius=0.12, stroke_color=col, stroke_width=2.2,
                                   fill_color="#141821", fill_opacity=1)
            big = label(rf"{sym} = {val}", font_size=40, color=col).move_to(box.get_top() + DOWN * 0.6)
            sm = label(nm, font_size=17, color=GREY_A).next_to(big, DOWN, buff=0.25)
            nums.add(VGroup(box, big, sm))
        nums.arrange(RIGHT, buff=0.35).move_to(UP * 0.6)
        opts = VGroup(*[label(o, font_size=26, color=WHITE) for o in (r"A: \ 37\%", r"B: \ 50\%", r"C: \ 72\%",
                                                                        r"D: \ 90\%")]).arrange(RIGHT, buff=0.9)
        opts.next_to(nums, DOWN, buff=0.55)
        head = label(r"Your turn: \ what top rate raises the most revenue?", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.35)
        ring = countdown().scale(0.6).next_to(opts, DOWN, buff=0.35)
        tag = data_tag(r"$a$ from Piketty and Saez's 2022 top shares", corner=DR, font_size=12)
        with self.voiceover(
            "Your turn. Three numbers decide how high the top income tax rate should be, if the goal is to raise "
            "as much as possible from the top. <bookmark mark='a'/> The first, a, describes the shape of the top "
            "of the distribution: the average income above any high threshold is a over a minus one times the "
            "threshold. In America's tax records for 2022, a is "
            f"{P['a']:.2f}. <bookmark mark='b'/> The second, e, is how much top incomes shrink when the share they "
            "keep falls by one percent: a common middle estimate is a quarter of a percent. <bookmark mark='c'/> The "
            "third, g, is the value society puts on giving top earners one more dollar; set it to zero, to find the "
            "rate that raises the most. <bookmark mark='d'/> Which rate is it: thirty-seven percent, the current "
            "federal top rate; fifty; seventy-two; or ninety? Pause, and choose."
        ) as vo:
            for n_ in nums:
                n_.set_opacity(0.3)
            self.play(FadeIn(head), FadeIn(tag), FadeIn(nums, lag_ratio=0.2), run_time=1.5)
            for mk, n_ in zip("abc", nums):
                vo.wait_until(mk)
                self.play(n_.animate.set_opacity(1.0), Indicate(n_[1], scale_factor=1.15))
            vo.wait_until("d")
            self.play(FadeIn(opts), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=8.0, rate_func=linear)
        self.play(FadeOut(ring))
        self.keep = (head, nums, opts, tag)

    def reveal(self):
        P = load("top")
        head, nums, opts, tag = self.keep
        eq = MathTex(r"t^{*} = \frac{1 - g}{1 - g + a\, e} = \frac{1}{1 + " + f"{P['a']:.2f}" + r" \times 0.25} = "
                     + f"{100 * P['rates']['0.25']:.0f}" + r"\%", font_size=40, color=E.ACCENT)
        eq.next_to(opts, DOWN, buff=0.35)
        hl = SurroundingRectangle(opts[2], color=GAIN, buff=0.12)
        foot = label(rf"Diamond and Saez (2011), \ with $a$ = 1.5: \ {100 * P['ds_rate']:.0f}\%; \ all taxes on top "
                     r"income combined, \ not only the federal rate", font_size=18, color=GREY_A).to_edge(DOWN,
                                                                                                 buff=0.8)
        with self.voiceover(
            "The answer is C. <bookmark mark='a'/> The formula, derived in chapter six, is one minus g over one minus "
            f"g plus a times e: with these numbers, {100 * P['rates']['0.25']:.0f} percent. <bookmark mark='b'/> "
            "Peter Diamond and Emmanuel Saez, with a of one and a half, got seventy-three. That is the rate on all "
            "taxes on top incomes combined, federal, state and payroll, and it is the most that can be raised, not "
            "necessarily the best rate: any positive weight on top earners' welfare, or a larger elasticity, "
            "lowers it."
        ) as vo:
            self.play(Create(hl))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def curves(self):
        P = load("top")
        taus = np.array(P["taus"])
        cols = (GAIN, TOP, RATE, LOSS)
        es = list(P["curves"])
        ax = plane([0, 1], [0, 1.4], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0, 0.5, 1.0], xlabel=r"top rate",
                   ylabel=r"revenue from the top bracket", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        lines = VGroup(*[path(ax, taus, P["curves"][e], c, 3.0, yr=(0, 1.4)) for e, c in zip(es, cols)])
        peaks = VGroup(*[dot(ax, P["rates"][e], float(np.max(P["curves"][e])), c, 0.08) for e, c in zip(es, cols)])
        side = VGroup(*[label(rf"$e$ = {float(e):g}: \ the top at {100 * P['rates'][e]:.0f}\%", font_size=19, color=c)
                        for e, c in zip(es, cols)])
        side.add(label(rf"with $g$ = 0.25 \ (and $e$ = 0.25): \\ {100 * P['rates_g']['0.25']:.0f}\%", font_size=18,
                       color=WORKER))
        side.arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = data_tag(rf"computed: \ $a$ = {P['a']:.2f}, \ from Piketty and Saez's 2022 top shares", corner=DR,
                       font_size=12)
        with self.voiceover(
            "The answer moves with the elasticity, which is the hard number to pin down. Here is the revenue from "
            "the top bracket against its rate, with the shape of the top fixed. <bookmark mark='a'/> With an "
            f"elasticity of a tenth, the top of the curve is at {100 * P['rates']['0.1']:.0f} percent; "
            f"<bookmark mark='b'/> a quarter, {100 * P['rates']['0.25']:.0f}; <bookmark mark='c'/> a half, "
            f"{100 * P['rates']['0.5']:.0f}; <bookmark mark='d'/> one, {100 * P['rates']['1.0']:.0f}. "
            "<bookmark mark='e'/> And if society values top earners' extra dollars at a quarter of the average, the "
            f"best rate falls to {100 * P['rates_g']['0.25']:.0f} percent. Chapter eight asks what the elasticity "
            "really is."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(lines[1]), run_time=1.5)
            for mk, k in zip("abcd", range(4)):
                vo.wait_until(mk)
                anims = [FadeIn(peaks[k], scale=1.4), FadeIn(side[k])]
                if k != 1:
                    anims.append(Create(lines[k]))
                self.play(*anims)
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
