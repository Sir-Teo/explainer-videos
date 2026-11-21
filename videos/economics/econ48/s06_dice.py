from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Dice(VoiceoverScene):
    def construct(self):
        card(self, 5, r"A climate-economy model, \ built", r"How much should the world cut, and how fast?",
             "Chapter five. A climate-economy model, built.", lit={1992: r"Nordhaus's DICE", 2024: r"DICE-2023"},
             scale=("world",), horizon=("a century",))
        self.structure()
        self.paths()
        self.compare()

    def structure(self):
        D = load("dice")
        chain = flow_chain([(r"the Ramsey \\ economy, \ Part 20", GAIN), (r"emissions", CO2),
                            (r"the climate, \\ chapter four", HEAT), (r"damages", LOSS)],
                           notes=[rf"output \${D['output0']:.0f} trillion \\ in 2025, \ capital, \\ saving",
                                  r"$\sigma\,Y\,(1-\mu)$: \ intensity \\ falls 1.5\% a year",
                                  r"carbon, \ forcing, \\ temperature", r"3.1\% of output \\ at 3\textdegree C, \\ "
                                                                             r"rising with $T^2$"],
                           box_w=2.8, font_size=20, note_size=16).move_to(UP * 1.3)
        back = CurvedArrow(chain.boxes[3].get_bottom() + DOWN * 0.9, chain.boxes[0].get_bottom() + DOWN * 0.9,
                           angle=-0.35, color=LOSS, stroke_width=2.4)
        rows = VGroup(
            MathTex(r"Y_t = (1 - \psi T_t^2)\,(1 - \theta_{1,t}\,\mu_t^{2.6})\; A_t K_t^{0.3} L_t^{0.7}", font_size=32,
                    color=THEORY),
            MathTex(r"\max_{\mu_t} \; \sum_t \frac{L_t}{(1+\rho)^t}\; \frac{c_t^{1-\eta}}{1-\eta}", font_size=32,
                    color=THEORY),
            label(r"$\mu$: \ the share of emissions avoided; \ avoiding all of them costs the backstop price, \ "
                  rf"\${D['backstop2050']:.0f} a tonne in 2050", font_size=18, color=GREY_A),
        ).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.45)
        intro = VGroup(
            label(r"DICE: \ the Dynamic Integrated Climate-Economy model", font_size=24, color=WHITE),
            label(r"Nordhaus, \ 1992 \ $\rightarrow$ \ DICE-2016R \ $\rightarrow$ \ DICE-2023, \ Barrage and Nordhaus, "
                  r"\ 2024", font_size=20, color=METAL),
            label(r"rebuilt here in a few hundred lines, \ on chapter four's climate", font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 1.7)
        tag = published_tag(tables.DICE_2023.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 1992 William Nordhaus joined an economy to a climate in a model he called DICE, the dynamic "
            "integrated climate-economy model. The version built here follows its latest form, DICE-2023, by Lint "
            "Barrage and Nordhaus, on the climate of chapter four. <bookmark mark='a'/> The economy is Part twenty's: "
            f"capital, labour and saving, with world output of about {D['output0']:.0f} trillion dollars in 2025. "
            "<bookmark mark='b'/> Output brings emissions, at an intensity that falls about one and a half percent a "
            "year as economies grow cleaner on their own. <bookmark mark='c'/> Emissions warm the climate. <bookmark "
            "mark='d'/> And warming does damage: DICE-2023's estimate is 3.1 percent of world output at three "
            "degrees, rising with the square of the temperature. <bookmark mark='e'/> The damage feeds back into "
            "output. The world can cut emissions by a share mu, at a cost that rises steeply with the share, until "
            f"cutting the last tonne costs the backstop price of {D['backstop2050']:.0f} dollars in 2050. "
            "<bookmark mark='f'/> And a planner chooses how much to cut each year to make the sum of everyone's "
            "discounted well-being, now and in the future, as large as possible."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(intro[0]), run_time=1.0)
            self.play(FadeIn(intro[1]), FadeIn(intro[2]), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(FadeOut(intro), run_time=0.5)
            self.play(Create(back), Write(rows[0]), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("f")
            self.play(Write(rows[1]), run_time=1.5)
        self.clear_scene()

    def paths(self):
        D = load("dice")
        B, O = D["base"], D["opt"]
        axE = plane([2025, 2200], [0, 50], center=LEFT * 3.5 + DOWN * 0.3, x_length=5.2, y_length=4.2,
                    xticks=[2050, 2100, 2150, 2200], yticks=[0, 10, 20, 30, 40, 50], xfmt=lambda v: f"{v:.0f}",
                    ylabel=r"emissions, \ GtCO$_2$ a year", yfmt=lambda v: f"{v:.0f}", font_size=13)
        axT = plane([2025, 2200], [1, 4.5], center=RIGHT * 2.6 + DOWN * 0.3, x_length=5.2, y_length=4.2,
                    xticks=[2050, 2100, 2150, 2200], yticks=[1, 2, 3, 4], xfmt=lambda v: f"{v:.0f}",
                    ylabel=r"warming, \ \textdegree C", yfmt=lambda v: f"{v:.0f}", font_size=13)
        yb = np.array(B["year"])
        k = yb <= 2200
        eb = path(axE, yb[k], np.array(B["E"])[k], BASE, 3.0, smooth=False)
        eo = path(axE, yb[k], np.array(O["E"])[k], OPT, 3.0, smooth=False)
        tb = path(axT, yb[k], np.array(B["T"])[k], BASE, 3.0, smooth=False)
        to = path(axT, yb[k], np.array(O["T"])[k], OPT, 3.0, smooth=False)
        head = VGroup(label(r"red: \ business as usual", font_size=19, color=BASE),
                      label(r"green: \ the optimal path", font_size=19, color=OPT)).arrange(RIGHT, buff=0.8).to_edge(
            UP, buff=0.45)
        notes = VGroup(
            label(rf"2100: \ {B['T2100']:.1f}\textdegree \ against \ {O['T2100']:.1f}\textdegree", font_size=18,
                  color=WHITE).next_to(axT, DOWN, buff=0.5),
            label(rf"optimal: \ {100 * O['mu2050']:.0f}\% cut by 2050, \ {100 * O['mu2100']:.0f}\% by 2100; \ "
                  rf"net zero in {O['zero_year']}", font_size=18, color=OPT).next_to(axE, DOWN, buff=0.5),
        )
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now run it. <bookmark mark='a'/> In red, business as usual: today's policies, which DICE-2023 reckons "
            "cut emissions about five percent, rising slowly. Emissions keep growing for decades, and by 2100 the "
            f"world is {B['T2100']:.1f} degrees warmer than before industry. <bookmark mark='b'/> In green, the path "
            f"a planner would choose: cut {100 * O['mu2030']:.0f} percent of emissions by 2030, "
            f"{100 * O['mu2050']:.0f} by 2050, {100 * O['mu2100']:.0f} by 2100, and reach net zero around "
            f"{O['zero_year']}. <bookmark mark='c'/> Warming peaks at {O['peak_T']:.1f} degrees, against the "
            "unchecked climb. That is the cost-benefit answer, with this model's damages and its modest "
            "discounting, and it misses the Paris Agreement's goal of well below two degrees. Whether it should "
            "is the subject of chapters six to eight."
        ) as vo:
            self.play(FadeIn(axE), FadeIn(axT), FadeIn(tag), FadeIn(head[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(eb), Create(tb), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(head[1]), Create(eo), FadeIn(notes[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(to), FadeIn(notes[0]), run_time=2.5)
        self.clear_scene()

    def compare(self):
        D = load("dice")
        S = load("scc")
        O = D["opt"]
        T = tables.DICE_2023.data
        rows = [
            (r"warming in 2100, \ business as usual", rf"{D['base']['T2100']:.1f}\textdegree", rf"{T['t2100_base']}"
             r"\textdegree \ (from 1765)"),
            (r"warming in 2100, \ optimal", rf"{O['T2100']:.1f}\textdegree", rf"{T['t2100_cb']}\textdegree"),
            (r"emissions cut by 2050, \ optimal", rf"{100 * O['mu2050']:.0f}\%", rf"{T['mu2050']}\%"),
            (r"carbon price in 2050, \ optimal", rf"\${O['price2050']:.0f}", rf"\${T['price2050']}"),
            (r"social cost of carbon, \ business as usual", rf"\${S['ramsey']:.0f}", rf"\${T['scc_base']}"),
            (r"social cost of carbon at 3\%", rf"\${S['by_rate'][S['rates'].index(0.03)]:.0f}",
             rf"\${T['scc_r'][3]}"),
        ]
        hdr = VGroup(label(r"measure", font_size=20, color=GREY_B), label(r"built here", font_size=22, color=OPT),
                     label(r"DICE-2023", font_size=22, color=METAL))
        grid = VGroup(hdr, *[VGroup(label(a, font_size=19, color=WHITE), label(b, font_size=21, color=OPT),
                                    label(c, font_size=21, color=METAL)) for a, b, c in rows])
        grid.arrange(DOWN, buff=0.36).move_to(DOWN * 0.1)
        for r_ in grid:
            r_[0].align_to(np.array([-0.6, 0, 0]), RIGHT)
            r_[1].set_x(1.2)
            r_[2].set_x(4.4)
        head = label(r"the model built here, \ against DICE-2023", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.55)
        foot = label(r"dollars of 2019 a tonne of CO$_2$; \ DICE-2023's social costs are for 2020, \ ours for 2025",
                     font_size=16, color=GREY_A).to_edge(DOWN, buff=0.55)
        tag = published_tag(tables.DICE_2023.tag, corner=DR, font_size=11)
        with self.voiceover(
            "How does a model built in a few hundred lines compare with Nordhaus's? <bookmark mark='a'/> Warming in "
            f"2100 under business as usual: {D['base']['T2100']:.1f} degrees here, {T['t2100_base']} in DICE-2023, "
            "which counts from 1765 and has a hotter baseline. <bookmark mark='b'/> On the optimal path, "
            f"{O['T2100']:.1f} here and {T['t2100_cb']} there. <bookmark mark='c'/> The share of emissions cut by "
            f"2050: {100 * O['mu2050']:.0f} percent here, {T['mu2050']} there. <bookmark mark='d'/> The carbon price "
            f"that delivers it in 2050: {O['price2050']:.0f} dollars a tonne here, {T['price2050']} there. "
            "<bookmark mark='e'/> And the social cost of carbon, the damage a tonne emitted today does over its "
            f"lifetime: {S['ramsey']:.0f} dollars here, {T['scc_base']} there; <bookmark mark='f'/> and at a "
            f"discount rate of three percent, {S['by_rate'][S['rates'].index(0.03)]:.0f} against {T['scc_r'][3]}. "
            "The structure, not the details, does most of the work. Which means that the structure's choices, "
            "above all the discount rate, deserve the closest look."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hdr), FadeIn(foot))
            for mk, r_ in zip("abcdef", grid[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()
