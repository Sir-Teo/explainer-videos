from __future__ import annotations

from scipy import stats

from videos.economics.econ48.common import *  # noqa: F403


class Tails(VoiceoverScene):
    def construct(self):
        card(self, 8, r"Fat tails", r"What if the worst case drives the answer?",
             "Chapter eight. Fat tails.", lit={2009: r"Weitzman", 2021: r"Dietz et al."}, scale=("world",),
             horizon=("a century",))
        self.sensitivity()
        self.truncation()
        self.tipping()

    def sensitivity(self):
        Tt = TRUTH["tails"]
        L = load("tails")
        xs = np.linspace(0.8, 12, 400)
        sd = Tt["spread"]
        thin = stats.norm.pdf(np.log(xs / Tt["median"]) / sd) / (sd * xs)
        fat = stats.t.pdf(np.log(xs / Tt["median"]) / sd, Tt["df"]) / (sd * xs)
        ax = plane([0.5, 12], [0, 0.6], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.6,
                   xticks=[1, 2, 3, 4, 6, 8, 10, 12], yticks=[0, 0.2, 0.4, 0.6],
                   xlabel=r"warming from doubled CO$_2$, \ \textdegree C", ylabel=r"probability density",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        lt = path(ax, xs, thin, COOL, 3.2)
        lf = path(ax, xs, fat, HEAT, 3.2)
        six = vline(ax, 6, 0, 0.6, GREY_B)
        tail = band(ax, xs[xs >= 6], np.zeros(np.sum(xs >= 6)), fat[xs >= 6], HEAT, 0.35)
        side = VGroup(
            label(r"both centred \\ on 3\textdegree, \ the IPCC's \\ best estimate", font_size=18, color=WHITE),
            label(rf"blue: \ thin tails; \\ above 6\textdegree: \ {100 * L['p_above6_thin']:.1f}\%", font_size=18,
                  color=COOL),
            label(rf"red: \ fat tails; \\ above 6\textdegree: \ {100 * L['p_above6_fat']:.1f}\%", font_size=18,
                  color=HEAT),
            label(r"the data on the \\ tail are thin: \\ few past climates \\ are like this one", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Everything so far used one number for the climate's sensitivity, three degrees. Nobody knows it "
            "exactly. <bookmark mark='a'/> Here are two beliefs about it, both centred on three degrees. <bookmark "
            f"mark='b'/> In blue, thin tails: the chance of more than six degrees is {100 * L['p_above6_thin']:.1f} "
            f"percent. <bookmark mark='c'/> In red, fat tails, as Martin Weitzman argued in 2009 the evidence allows: "
            f"the same centre, but a {100 * L['p_above6_fat']:.1f} percent chance of more than six degrees. <bookmark "
            "mark='d'/> Weitzman's point was that the data cannot rule the fat tail out, because so few past "
            "climates resemble one forced this fast, and that the tail, not the centre, may drive what we should "
            "pay to avoid the risk."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(six), run_time=1.0)
            vo.wait_until("b")
            self.play(Create(lt), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lf), FadeIn(tail), FadeIn(side[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def truncation(self):
        L = load("tails")
        tr = np.array(L["truncation"])
        ax = plane([4.5, 20.5], [0, 1.0], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.6, y_length=4.6,
                   xticks=[5, 8, 10, 12, 15, 20], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"the worst warming allowed in the calculation, \ \textdegree C",
                   ylabel=r"certainty-equivalent loss of consumption", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        lt = path(ax, tr, L["thin"], COOL, 3.2, smooth=False)
        lf = path(ax, tr, L["fat"], HEAT, 3.2, smooth=False)
        dt = VGroup(*[dot(ax, x, y, COOL, 0.05) for x, y in zip(tr, L["thin"])])
        df = VGroup(*[dot(ax, x, y, HEAT, 0.05) for x, y in zip(tr, L["fat"])])
        side = VGroup(
            label(r"damages: \ DICE's below \\ 4\textdegree, \ steepening \\ sharply above 6", font_size=18,
                  color=WHITE),
            label(rf"thin tails: \ about \\ {100 * L['thin'][-1]:.0f}\%, \ whatever \\ the cut-off", font_size=18,
                  color=COOL),
            label(rf"fat tails: \ {100 * L['fat'][1]:.0f}\% at 6\textdegree, \\ "
                  rf"{100 * L['fat'][4]:.0f}\% at 10, \\ {100 * L['fat'][-1]:.0f}\% at 20", font_size=18, color=HEAT),
            label(r"the answer is set \\ by an assumption \\ about the extreme", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        inset = plane([0, 20], [0, 1.0], center=LEFT * 1.6 + UP * 0.3, x_length=4.2, y_length=2.4,
                      xticks=[0, 5, 10, 15, 20], yticks=[0, 0.5, 1.0], xlabel=r"warming, \ \textdegree C",
                      ylabel=r"share of output lost", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                      font_size=12)
        Ts = np.linspace(0, 20, 201)
        om = 1 - 1 / (1 + (0.031 / 9) * Ts ** 2 + (Ts / 6.5) ** 7)
        dmg = path(inset, Ts, om, LOSS, 3.0)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Here is the problem with numbers. <bookmark mark='a'/> Let damages follow DICE below four degrees but "
            "steepen sharply above six, as many fear, and let a society that dislikes risk, with a relative risk "
            "aversion of two, ask what sure loss of consumption it would accept in place of the gamble. To compute "
            "it, someone must decide the worst warming the calculation allows. <bookmark mark='b'/> With thin tails "
            f"the answer is about {100 * L['thin'][-1]:.0f} percent whatever the cut-off: the extremes are too "
            f"unlikely to matter. <bookmark mark='c'/> With fat tails it is {100 * L['fat'][1]:.0f} percent if "
            f"nothing above six degrees is allowed, {100 * L['fat'][4]:.0f} at ten, and {100 * L['fat'][-1]:.0f} at "
            "twenty: the answer is whatever the cut-off says. That is Weitzman's dismal theorem in miniature: with "
            "fat tails, expected damage can be dominated by catastrophes whose probability nobody can estimate. "
            "<bookmark mark='d'/> His conclusion was not that the number is infinite, but that climate policy is "
            "partly insurance, against outcomes too bad and too uncertain for a single best guess."
        ) as vo:
            self.play(FadeIn(tag), run_time=0.5)
            vo.wait_until("a")
            self.play(FadeIn(inset), FadeIn(side[0]), run_time=1.0)
            self.play(Create(dmg), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeOut(inset), FadeOut(dmg), run_time=0.6)
            self.play(FadeIn(ax), Create(lt), FadeIn(dt), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(lf), FadeIn(df), FadeIn(side[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def tipping(self):
        T = tables.WEITZMAN_2009.data
        cards = point_cards([
            (r"tipping points", r"ice sheets, \ the \\ Amazon, \ permafrost, \\ ocean currents: \\ changes that "
                                r"feed \\ on themselves", HEAT),
            (r"Dietz et al., \ 2021", rf"eight together raise \\ the social cost of \\ carbon by about \\ "
                                      rf"{T['tipping']}\%", LOSS),
            (r"the tail", rf"about a {T['double']}\% chance \\ they more than \\ double it", LOSS),
            (r"the lesson", r"uncertainty raises \\ the price of carbon, \\ it does not lower it", E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"from fat tails to tipping points", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.WEITZMAN_2009.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Climate scientists point to particular ways the tail could arrive. <bookmark mark='a'/> Tipping points: "
            "the loss of ice sheets, the drying of the Amazon, thawing permafrost releasing its methane, changes in "
            "ocean currents, each a change that feeds on itself once begun. <bookmark mark='b'/> Simon Dietz, James "
            "Rising, Thomas Stoerk and Gernot Wagner put eight of them into an integrated model in 2021. Together "
            f"they raise the social cost of carbon by about {T['tipping']} percent. <bookmark mark='c'/> And there "
            f"is about a {T['double']} percent chance they more than double it. <bookmark mark='d'/> The common "
            "thread: uncertainty about the climate is a reason to price carbon higher, not lower, because the "
            "outcomes we cannot rule out are worse than the ones we expect."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
