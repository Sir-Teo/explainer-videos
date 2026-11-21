from __future__ import annotations

from videos.economics.econ66.common import *  # noqa: F403


class Games(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Trade wars as games", r"Why are countries tempted into tariff wars, \ and why do trade "
             r"agreements exist?", "Chapter three. Trade wars as games.",
             lit={1948: "the GATT", 2014: "Ossa"}, scale=("nation", "world"), horizon=("a decade",))
        self.optimal()
        self.responses()
        self.agreements()

    def optimal(self):
        B = load("bloc")
        g = np.array(B["grid"])
        Wu = 100 * np.array(B["W_us"])
        Wr = 100 * np.array(B["W_ro"])
        ax = plane([0, 0.6], [-0.6, 0.6], center=LEFT * 1.6 + DOWN * 0.3, x_length=8.6, y_length=4.8,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[-0.6, -0.4, -0.2, 0, 0.2, 0.4, 0.6],
                   xlabel=r"the US tariff on everyone else \ (no retaliation)",
                   ylabel=r"real income, \ \% change", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{v:.1f}".replace("-", "{-}"), font_size=14)
        zero = seg(ax, 0, 0, 0.6, 0, GREY_C, 1.5)
        lu = path(ax, g, Wu[:, 0], US, 3.2)
        lr = path(ax, g, Wr[:, 0], ROW, 3.2)
        opt = vline(ax, B["optimal"], -0.6, 0.6, US)
        olab = label(rf"the optimal tariff: \ {100 * B['optimal']:.0f}\%", font_size=17, color=US).next_to(
            ax.ax.c2p(B["optimal"], 0.55), RIGHT, buff=0.1)
        key = legend_rows([(US, "the United States"), (ROW, "the rest of the world")], font_size=16).next_to(
            ax.ax, RIGHT, buff=0.3).shift(UP * 1.2)
        eq = MathTex(r"t^\ast \approx \frac{1}{\varepsilon^\ast}", font_size=36, color=GREY_A)
        eqn = label(r"$\varepsilon^\ast$: \ how readily \\ foreigners' supply responds", font_size=15, color=GREY_A)
        VGroup(eq, eqn).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(key, DOWN, buff=0.5).align_to(key, LEFT)
        tag = island_tag(r"computed: \ agora.tradewar.two\_bloc \ ($\theta = 4$, \ CEPII flows of 2019, \ "
                         r"deficits purged)", corner=DL, font_size=12)
        with self.voiceover(
            "Start with why a tariff tempts a large country. <bookmark mark='a'/> In the model, the United States "
            "puts a uniform tariff on everyone else, and nobody answers. <bookmark mark='b'/> Its real income "
            "rises at first. The tariff cuts what Americans buy abroad, the world price of those goods falls, and "
            "part of the tariff is paid by foreigners: the terms of trade improve. <bookmark mark='c'/> Up to a "
            f"point: the gain peaks at a tariff of about {100 * B['optimal']:.0f} percent, the optimal tariff, "
            "roughly one over the elasticity of foreign supply. <bookmark mark='d'/> The rest of the world loses "
            "more than America gains. A large country's tariff is a way of taking a slice of other people's "
            "income, at a cost to the world."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(key[0]))
            vo.wait_until("b")
            self.play(Create(lu), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(opt), FadeIn(olab), Write(eq), FadeIn(eqn))
            vo.wait_until("d")
            self.play(Create(lr), FadeIn(key[1]), run_time=2.0)
        self.clear_scene()

    def responses(self):
        B = load("bloc")
        g = np.array(B["grid"])
        ax = plane([0, 0.6], [0, 0.6], center=LEFT * 2.0 + DOWN * 0.3, x_length=5.4, y_length=5.0,
                   xticks=[0, 0.2, 0.4, 0.6], yticks=[0, 0.2, 0.4, 0.6], xlabel=r"the US tariff",
                   ylabel=r"the rest of the world's tariff", xfmt=lambda v: f"{100 * v:.0f}\\%",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        bu = path(ax, B["br_us"], g, US, 3.2, smooth=False)
        br = path(ax, g, B["br_ro"], ROW, 3.2, smooth=False)
        n0, n1 = B["nash"]
        nash = dot(ax, n0, n1, TARIFF, 0.11)
        free = dot(ax, 0, 0, FREE, 0.11)
        nl = label(r"Nash", font_size=18, color=TARIFF).next_to(nash, UR, buff=0.08)
        fl = label(r"free trade", font_size=18, color=FREE).next_to(free, UR, buff=0.08)
        side = VGroup(
            label(r"best responses:", font_size=20, color=GREY_A),
            legend_rows([(US, "America's, to each foreign tariff"), (ROW, "the rest's, to each US tariff")],
                        font_size=16),
            label(rf"at the Nash tariffs \ ({100 * n0:.0f}\%, \ {100 * n1:.0f}\%):", font_size=19, color=TARIFF),
            label(rf"the United States \ {100 * B['nash_us']:+.2f}\%".replace("-", "{-}"), font_size=19, color=US),
            label(rf"the rest of the world \ {100 * B['nash_ro']:+.2f}\%".replace("-", "{-}"), font_size=19,
                  color=ROW),
            label(r"both worse than free trade", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(ax.ax, RIGHT, buff=0.6)
        tag = island_tag(r"computed: \ agora.tradewar.two\_bloc", corner=DL, font_size=12)
        with self.voiceover(
            "But the rest of the world can do the same. <bookmark mark='a'/> For each tariff the other side sets, "
            "find each side's best answer. America's, in blue, is the same whatever the rest does: about "
            f"{100 * n0:.0f} percent. <bookmark mark='b'/> The rest of the world's, in orange, is about the same. "
            "<bookmark mark='c'/> Where the two cross is the Nash equilibrium of the tariff war: each taxing the "
            f"other at about {100 * n0:.0f} percent. <bookmark mark='d'/> And there, America is "
            f"{-100 * B['nash_us']:.2f} percent poorer than at free trade, and the rest of the world "
            f"{-100 * B['nash_ro']:.2f} percent. Each did the best it could given the other, and both lost. It is "
            "Part eleven's prisoners' dilemma, with countries."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(Create(bu), FadeIn(side[1][0]), run_time=1.6)
            vo.wait_until("b")
            self.play(Create(br), FadeIn(side[1][1]), run_time=1.6)
            vo.wait_until("c")
            self.play(FadeIn(nash, scale=1.5), FadeIn(nl), FadeIn(free), FadeIn(fl), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3:]))
        self.clear_scene()

    def agreements(self):
        cards = point_cards([
            (r"the escape", r"a trade agreement is a way out of the dilemma: \ each lowers its tariff because the "
             r"other does \ (reciprocity)", FREE),
            (r"the GATT and the WTO", r"since 1947: \ bound tariffs, \ the same tariff for every member \ (most "
             r"favoured nation), \ and a court for disputes", STATE),
            (r"Ossa's numbers", r"in a model of the world economy, \ Nash tariffs average 63\%, \ and a breakdown "
             r"of cooperation costs 2.9\% of income on average", TARIFF),
            (r"why it held", r"repetition: \ Part 11's folk theorem; \ a deviation today is answered tomorrow", US),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"why trade agreements exist", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        tag = published_tag(r"Bagwell and Staiger, \ AER 89(1) (1999); \ Ossa, \ AER 104(12) (2014)", corner=DL,
                            font_size=12)
        with self.voiceover(
            "This is the modern economic theory of trade agreements, from Kyle Bagwell and Robert Staiger. "
            "<bookmark mark='a'/> Each country lowers its tariff because the other does: reciprocity turns the "
            "prisoners' dilemma into a deal. <bookmark mark='b'/> The General Agreement on Tariffs and Trade, from "
            "1947, and the World Trade Organization after it, added bound tariffs that cannot be raised at will, "
            "the same tariff for every member, and a court for disputes. <bookmark mark='c'/> How much is at stake? "
            "Ralph Ossa computed the Nash tariffs of a model of the world economy: they average sixty-three "
            "percent, and a breakdown of cooperation would cost governments two point nine percent of income on "
            "average. <bookmark mark='d'/> Cooperation held for seventy years for the reason of Part eleven's folk "
            "theorem: the game is repeated, and a deviation today is answered tomorrow."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
