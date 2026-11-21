from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403


class Deterrence(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Deterrence measured", r"Do more police mean less crime, and how would we know?",
             "Chapter three. Deterrence measured.", lit={1997: r"Levitt", 2004: r"Di Tella and Schargrodsky",
                                                         2011: r"Draca et al."}, scale=("city",),
             horizon=("a year",))
        self.blocks()
        self.estimates()
        self.experiments()
        self.executions()

    def blocks(self):
        P = load("police")
        lp, lc = np.array(P["log_police"]), np.array(P["log_crime"])
        k = np.arange(0, len(lp), 3)
        ax = plane([-1.0, 3.2], [0.0, 4.6], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.4,
                   xticks=[-1, 0, 1, 2, 3], yticks=[0, 1, 2, 3, 4], xlabel=r"police on the block \ (log)",
                   ylabel=r"crime on the block \ (log)", xfmt=lambda v: f"{v:.0f}".replace("-", "{-}"),
                   yfmt=lambda v: f"{v:.0f}", font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.03, color=POLICE, fill_opacity=0.55) for x, y in zip(lp[k],
                                                                                                          lc[k])])
        a = float(np.mean(lc) - P["naive"] * np.mean(lp))
        fit = seg(ax, -0.8, a - 0.8 * P["naive"], 3.0, a + 3.0 * P["naive"], CRIME, 3.2)
        side = VGroup(
            label(rf"{len(lp):,} Island blocks".replace(",", "{,}"), font_size=18, color=WHITE),
            label(r"the city sends police \\ where it expects crime", font_size=18, color=POLICE),
            label(rf"the slope: \ {say_num(P['naive'])}".replace("minus ", "{-}"), font_size=19, color=CRIME),
            label(rf"the truth planted: \\ {P['elasticity']:.1f}".replace("-", "{-}") + r" \ (more police, \\ "
                  r"less crime)", font_size=18, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Now the evidence. The obvious study compares places. <bookmark mark='a'/> Here are the Island's "
            f"{len(lp):,} city blocks, the police on each against its crime. <bookmark mark='b'/> The city, "
            "sensibly, sends police where it expects crime. <bookmark mark='c'/> So the blocks with the most police "
            "have the most crime: the slope is "
            f"{say_num(P['naive'], 2)}. Read naively, police cause crime. <bookmark mark='d'/> The truth planted in "
            f"the Island is the opposite: each percent more police cuts crime by {abs(P['elasticity']):.1f} percent. "
            "The comparison is ruined because police are not placed at random."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.003), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(fit), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(fit, color=WHITE))
        self.clear_scene()

    def estimates(self):
        P = load("police")
        rows = ((r"compare blocks", P["naive"], P["naive_se"], CRIME),
                (r"follow blocks over time, \\ police counted with error", P["fd_noisy"], P["fd_noisy_se"], HOLD),
                (r"police moved at random", P["experiment"], P["experiment_se"], GAIN))
        ax = plane([-0.8, 1.0], [-0.5, 2.5], center=RIGHT * 1.0 + DOWN * 0.3, x_length=7.6, y_length=4.0,
                   xticks=[-0.75, -0.5, -0.25, 0, 0.25, 0.5, 0.75, 1.0], yticks=[],
                   xlabel=r"estimated elasticity of crime to police",
                   xfmt=lambda v: f"{v:.2f}".replace("-", "{-}"), font_size=14)
        truth = vline(ax, P["elasticity"], -0.5, 2.5, GAIN, 2.4)
        truth_l = label(r"the truth", font_size=16, color=GAIN).next_to(ax.ax.c2p(P["elasticity"], 2.5), UP,
                                                                        buff=0.05)
        zero = vline(ax, 0.0, -0.5, 2.5, GREY_B, 1.4)
        marks = VGroup()
        for i, (nm, b, se, col) in enumerate(rows):
            y = 2.0 - 1.0 * i
            marks.add(VGroup(seg(ax, b - 1.96 * se, y, b + 1.96 * se, y, col, 3.0), dot(ax, b, y, col, 0.09),
                             label(nm, font_size=17, color=col).next_to(ax.ax.c2p(-0.8, y), LEFT, buff=0.2)))
        foot = label(rf"counting errors leave only {100 * P['reliability']:.0f}\% of the measured changes in police "
                     r"real: \ the estimate shrinks toward zero", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.5)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Three ways to estimate it. <bookmark mark='a'/> Comparing blocks: "
            f"{say_num(P['naive'], 2)}, the wrong sign. <bookmark mark='b'/> Following each block over time removes "
            "what is permanent about it, but changes in police from year to year are small, and police are counted "
            f"with error. Here only {100 * P['reliability']:.0f} percent of the measured changes are real; the rest "
            f"is noise, which drags the estimate toward zero: {say_num(P['fd_noisy'], 2)}. <bookmark mark='b2'/> "
            "Aaron Chalfin and Justin McCrary found exactly this in American cities' police counts. <bookmark "
            "mark='c'/> What works is moving police for a reason that has nothing to do with crime. Move them at "
            f"random on the Island, and the estimate is {say_num(P['experiment'], 2)}, close to the truth. <bookmark "
            "mark='d'/> Nobody assigns police at random in a real city. But sometimes history does."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), Create(truth), FadeIn(truth_l), run_time=1.0)
            for mk, m in zip("abc", marks):
                vo.wait_until(mk)
                self.play(FadeIn(m[2]), Create(m[0]), FadeIn(m[1]), run_time=1.2)
                if mk == "b":
                    self.play(FadeIn(foot))
                    vo.wait_until("b2")
                    self.play(Indicate(marks[1], color=WHITE, scale_factor=1.08), Indicate(foot, color=WHITE,
                                                                                           scale_factor=1.0))
            vo.wait_until("d")
            self.play(Indicate(marks[2], color=WHITE, scale_factor=1.05))
        self.clear_scene()

    def experiments(self):
        T = tables.POLICE_49.data
        chain = flow_chain([(rf"July {T['ba_year']}: \\ a bomb at the \\ AMIA in Buenos Aires", LOSS),
                            (r"police guard every \\ Jewish institution, \\ day and night", POLICE),
                            (r"car thefts on \\ those blocks", GAIN), (r"and a block \\ or two away", GREY_B)],
                           notes=[r"85 killed", r"placed by a threat, \\ not by crime", rf"down {T['ba_fall']}\%",
                                  r"no change"], box_w=2.9, font_size=19, note_size=17).move_to(UP * 1.3)
        london = VGroup(
            label(rf"London, \ July {T['london_year']}: \ after the bombings, \ police flood central London",
                  font_size=21, color=POLICE),
            label(rf"crime falls there relative to outer London: \ an elasticity of about "
                  rf"{T['london_lo']:.1f} to {T['london_hi']:.1f}".replace("-", "{-}"), font_size=21, color=GAIN),
            label(r"so a tenth more police, \ three or four percent less crime", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, buff=0.25).move_to(DOWN * 1.9)
        tag = published_tag(tables.POLICE_49.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Two such accidents. <bookmark mark='a'/> In July 1994 a bomb destroyed the AMIA Jewish community centre "
            "in Buenos Aires and killed eighty-five people. <bookmark mark='b'/> The government put police outside "
            "every Jewish institution in the city, day and night, where they were placed by a threat of terror, not "
            "by the crime around them. <bookmark mark='c'/> Rafael Di Tella and Ernesto Schargrodsky counted car "
            f"thefts: on the protected blocks they fell by {T['ba_fall']} percent relative to other blocks. "
            "<bookmark mark='d'/> A block or two away, nothing changed: police deter where they stand. <bookmark "
            "mark='e'/> In July 2005, after the London bombings, police were moved into central London for weeks. "
            "Mirko Draca, Stephen Machin and Robert Witt found crime fell there relative to outer London, <bookmark "
            "mark='f'/> an elasticity of about minus 0.3 to minus 0.4: <bookmark mark='g'/> a tenth more police, "
            "three or four percent less crime. Close to the Island's planted value, which was chosen to match."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]), Indicate(chain.boxes[0], color=WHITE, scale_factor=1.04))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            for mk, r_ in zip("efg", london):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def executions(self):
        M = load("murder")
        ex, rate, south = np.array(M["executions"]), np.array(M["rate"]), np.array(M["south"])
        ax = plane([0, 0.45], [0, 21], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.4,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4], yticks=[0, 5, 10, 15, 20],
                   xlabel=r"executions per conviction, \ 1946--50", ylabel=r"murders per 100{,}000, \ 1950",
                   xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.06, color=LOSS if s else POLICE) for x, y, s in
                       zip(ex, rate, south)])
        S1, S2 = M["simple"], M["controls"]
        side = VGroup(
            label(rf"{M['n']} states, \ 1950", font_size=18, color=WHITE),
            label(rf"red: \ the South, \\ {M['mean_south']:.1f} murders \\ per 100{{,}}000; \\ blue: \ the rest, "
                  rf"{M['mean_north']:.1f}", font_size=17, color=LOSS),
            label(rf"executions, \ alone: \\ {S1['exe']:+.0f} \ (s.e. {S1['exe_se']:.0f})".replace("-", "{-}"),
                  font_size=17, color=E.ACCENT),
            label(rf"with region, \ income, \\ race: \ {S2['exe']:+.0f} \ (s.e. {S2['exe_se']:.0f})".replace("-",
                                                                                                         "{-}"),
                  font_size=17, color=E.ACCENT),
            label(r"the answer follows \\ the controls chosen \\ (Leamer, \ McManus)", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"Maddala (2001), \ after McManus (1985), \ via AER", corner=DL, font_size=12)
        with self.voiceover(
            "The hardest case is the most severe penalty. <bookmark mark='a'/> In 1975 Isaac Ehrlich estimated "
            "from American time series that each execution deterred several murders, and the study was quickly "
            "drawn into the American argument over the death penalty. Here are the 1950 data his critics used: "
            "murders per hundred thousand in forty-four states against executions per conviction. <bookmark "
            "mark='b'/> The southern states, in red, had both more executions and far more murder. <bookmark "
            "mark='c'/> Regress murder on executions and convictions "
            "alone, and executions seem to raise murder. <bookmark mark='d'/> Add region, income and race, and the "
            "estimate shrinks, with an error larger than itself. <bookmark mark='e'/> Edward Leamer and Walter "
            "McManus showed that, with data like these, the deterrent effect of execution can be made large, zero "
            "or negative by the choice of controls: the data cannot settle it. Their lesson, to report how an "
            "answer moves with the assumptions behind it, is one this series follows."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p_) for p_ in pts], lag_ratio=0.03), run_time=2.0)
            for mk, r_ in zip("bcde", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()
