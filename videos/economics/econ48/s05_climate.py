from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Climate(VoiceoverScene):
    def construct(self):
        card(self, 4, r"The largest externality", r"How do emissions become warming?",
             "Chapter four. The largest externality.", lit={1958: r"Keeling at Mauna Loa", 2021: r"IPCC AR6"},
             scale=("world",), horizon=("a century",))
        self.emissions()
        self.equations()
        self.fit_air()
        self.fit_heat()

    def emissions(self):
        C = load("climate")
        yr = np.array(C["year"])
        fos, land = np.array(C["fossil"]), np.array(C["land"])
        ax = plane([1850, 2026], [0, 48], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.4, y_length=4.6,
                   xticks=[1850, 1900, 1950, 2000], yticks=[0, 10, 20, 30, 40], xfmt=lambda v: f"{v:.0f}",
                   ylabel=r"billion tonnes of CO$_2$ a year", yfmt=lambda v: f"{v:.0f}", font_size=14)
        lower = band(ax, yr, np.zeros_like(fos), fos, CO2, 0.55)
        upper = band(ax, yr, fos, fos + land, FISH, 0.45)
        side = VGroup(
            label(r"gold: \ fossil fuels \\ and cement", font_size=18, color=CO2),
            label(r"green: \ land use, \\ mostly forests cleared", font_size=18, color=FISH),
            label(rf"{C['year'][-1]}: \ {C['fossil_2025']:.0f} billion \\ tonnes from fossil fuels", font_size=19,
                  color=WHITE),
            label(r"each tonne warms \\ everyone, \ for centuries, \\ and its emitter \\ pays nothing for it",
                  font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Global Carbon Budget (2026), \ via Our World in Data", corner=DL, font_size=12)
        with self.voiceover(
            "Part fifteen met externalities: costs that fall on people who did not choose them. Climate change is "
            "the largest there is. <bookmark mark='a'/> Here are the world's emissions of carbon dioxide from fossil "
            f"fuels and cement since 1850, from the Global Carbon Budget: {C['fossil_2025']:.0f} billion tonnes in "
            f"{C['year'][-1]}. <bookmark mark='b'/> On top, emissions from changing the use of land, mostly from "
            "clearing forests. <bookmark mark='c'/> Every tonne mixes into the whole atmosphere within a year or "
            "two, and a good part of it stays for centuries. So every tonne warms everyone, for a very long time, "
            "and whoever emits it pays nothing for that. To put a price on it, economists need to know how a tonne "
            "becomes warming, and what warming costs. The first half is physics, and it fits in four equations."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(lower), FadeIn(side[0]), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(upper), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def equations(self):
        eqs = VGroup(
            MathTex(r"R_{i,t} = R_{i,t-1}\, e^{-1/\tau_i} + a_i E_t", font_size=34, color=WHITE),
            MathTex(r"C_t = 278 + \tfrac{1}{2.124} \textstyle\sum_i R_{i,t}", font_size=34, color=WHITE),
            MathTex(r"F_t = k \cdot 5.35 \ln\!\frac{C_t}{278} \;-\; b\,\mathrm{SO}_{2,t}", font_size=34,
                    color=WHITE),
            MathTex(r"c\,\Delta T = F - \lambda T - \gamma\,(T - T_{\mathrm{deep}}), \quad "
                    r"c_{\mathrm{deep}}\,\Delta T_{\mathrm{deep}} = \gamma\,(T - T_{\mathrm{deep}})",
                    font_size=30, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(LEFT * 1.4 + UP * 0.35)
        notes = VGroup(
            label(r"carbon: \ four reservoirs, \ some \\ emptying in years, \ one never", font_size=17, color=CO2),
            label(r"concentration, \ parts per million", font_size=17, color=CO2),
            label(r"forcing: \ CO$_2$ and other gases warm; \\ sulphur from coal cools", font_size=17, color=HEAT),
            label(r"temperature: \ the surface and \\ the deep ocean", font_size=17, color=HEAT),
        )
        for n_, e_ in zip(notes, eqs):
            n_.next_to(e_, RIGHT, buff=0.5).align_to(np.array([3.2, 0, 0]), LEFT)
        foot = label(r"$\lambda = 5.35 \ln 2 / \mathrm{ECS}$, \ with ECS $= 3$\textdegree C, \ the IPCC's best "
                     r"estimate", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = published_tag(r"IPCC AR5 impulse response (Joos et al. 2013); \ AR6 (2021)", corner=DR, font_size=11)
        with self.voiceover(
            "<bookmark mark='a'/> First, carbon. Each year's emissions are shared among four reservoirs in the "
            "atmosphere's exchange with the oceans and the land. Some of the extra carbon is taken up within years, "
            "some within centuries, and about a fifth stays for millennia. These fractions and timescales are the "
            "IPCC's. <bookmark mark='b'/> Second, the concentration: pre-industrial air held 278 parts per million, "
            "and every 2.1 billion tonnes of carbon left in the air adds one more. <bookmark mark='c'/> Third, "
            "forcing: the extra energy trapped, rising with the logarithm of the concentration, scaled up for the "
            "other greenhouse gases, and reduced by the sulphur pollution from coal, which reflects sunlight. "
            "<bookmark mark='d'/> Fourth, temperature: the surface warms until it sheds the extra energy, while the "
            "deep ocean slowly soaks up heat. How much warming a doubling of carbon dioxide finally brings, the "
            "equilibrium climate sensitivity, is set at three degrees, the IPCC's best estimate."
        ) as vo:
            self.play(FadeIn(tag))
            for mk, e_, n_ in zip("abcd", eqs, notes):
                vo.wait_until(mk)
                self.play(Write(e_), FadeIn(n_), run_time=1.5)
            self.play(FadeIn(foot))
        self.clear_scene()

    def fit_air(self):
        C = load("climate")
        yr = np.array(C["year"])
        ax = plane([1950, 2026], [300, 440], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.4, y_length=4.6,
                   xticks=[1960, 1980, 2000, 2020], yticks=[300, 340, 380, 420], xfmt=lambda v: f"{v:.0f}",
                   ylabel=r"CO$_2$, \ parts per million", yfmt=lambda v: f"{v:.0f}", font_size=14)
        keep = yr >= 1950
        model = path(ax, yr[keep], np.array(C["ppm"])[keep], MODEL, 3.2, smooth=False)
        obs = VGroup(*[dot(ax, y, v, OBS, 0.045) for y, v in zip(C["obs_year"], C["obs_ppm"])])
        side = VGroup(
            label(r"dots: \ Mauna Loa, \\ every year since 1959", font_size=18, color=OBS),
            label(r"line: \ the model, \ fed \\ only the emissions", font_size=18, color=MODEL),
            label(rf"fitted: \ the sinks work \\ {1 / C['speed']:.1f} times faster than \\ the IPCC pulse; \ "
                  rf"{100 * C['land_weight']:.0f}\% \\ of land-use emissions count", font_size=17, color=GREY_A),
            label(rf"error: \ {C['ppm_rmse']:.1f} ppm", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"NOAA Global Monitoring Laboratory (Scripps before 1974); \ Global Carbon Budget", corner=DL,
                       font_size=12)
        with self.voiceover(
            "Does it work? <bookmark mark='a'/> The dots are the yearly concentration at Mauna Loa in Hawaii, where "
            f"Charles Keeling began measuring in 1958: {C['ppm_2025']:.0f} parts per million in 2025. <bookmark "
            "mark='b'/> The line is the model, fed nothing but the emissions since 1750. <bookmark mark='c'/> Two "
            "numbers were fitted to the dots: how fast the reservoirs take up carbon, since the IPCC's response is "
            "for a single pulse added to today's air, and how much of the uncertain emissions from land use to "
            f"count, {100 * C['land_weight']:.0f} percent. <bookmark mark='d'/> The model misses the record by "
            f"{C['ppm_rmse']:.1f} parts per million on average."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in obs], lag_ratio=0.03), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(model), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def fit_heat(self):
        C = load("climate")
        yr = np.array(C["year"])
        ax = plane([1850, 2026], [-0.5, 1.8], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.4, y_length=4.6,
                   xticks=[1850, 1900, 1950, 2000], yticks=[-0.5, 0, 0.5, 1.0, 1.5], xfmt=lambda v: f"{v:.0f}",
                   ylabel=r"warming since 1850--1900, \ \textdegree C",
                   yfmt=lambda v: f"{v:+.1f}".replace("-", "{-}") if v else "0", font_size=14)
        obs = path(ax, C["obs_temp_year"], C["obs_temp"], OBS, 2.0, smooth=False)
        model = path(ax, yr, C["temp"], MODEL, 3.4, smooth=False)
        side = VGroup(
            label(r"gold: \ HadCRUT5, \\ the thermometers", font_size=18, color=OBS),
            label(r"green: \ the model", font_size=18, color=MODEL),
            label(rf"fitted: \ other gases add \\ {100 * (C['ghg_scale'] - 1):.0f}\% to CO$_2$'s forcing; \\ "
                  rf"sulphur cools {C['aerosol']:.2f} W/m$^2$ \\ per 100 Mt a year", font_size=17, color=GREY_A),
            label(rf"2016--2025: \ model {C['decade_model']:.2f}\textdegree, \\ thermometers "
                  rf"{C['decade_obs']:.2f}\textdegree", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Met Office Hadley Centre and CRU, \ HadCRUT5; \ CEDS sulphur via Our World in Data",
                       corner=DL, font_size=12)
        with self.voiceover(
            "<bookmark mark='a'/> And the temperature. In gold, the world's average surface temperature from "
            "HadCRUT5, measured from its level in 1850 to 1900. The wiggles are weather: El Niño years, volcanoes. "
            "<bookmark mark='b'/> In green, the model. <bookmark mark='c'/> Two more numbers were fitted here, with "
            "the sensitivity held at three degrees: how much the other greenhouse gases add to carbon dioxide's "
            f"forcing, {100 * (C['ghg_scale'] - 1):.0f} percent, and how much the sulphur from burning coal cools, "
            "which is part of why the record flattened in the middle of the century. <bookmark mark='d'/> Over the "
            f"last ten years the model is {C['decade_model']:.2f} degrees warmer than the pre-industrial level, "
            f"and the thermometers {C['decade_obs']:.2f}. That is the physics of the next chapter's economy."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(obs), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(model), FadeIn(side[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()
