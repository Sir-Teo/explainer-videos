from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ tipping points, \ adaptation, \ the transition",
             r"What is still being worked out?",
             "Chapter sixteen. Frontier: how large the damage is, who can adapt, and the economics of the transition.",
             lit={2015: r"McGlade and Ekins", 2024: r"Bilal and K\"anzig"}, scale=("world",),
             horizon=("a decade", "a century"))
        self.global_shocks()
        self.transition()
        self.adaptation()

    def global_shocks(self):
        rows = VGroup(
            label(r"chapter twelve: \ a country's own hot year, \ about a point of growth in hot, \ poor places",
                  font_size=21, color=WHITE),
            label(r"Bilal and K\"anzig, \ 2024: \ a year when the whole world is 1\textdegree C warmer, \ world GDP "
                  r"about 12\% lower, \ six years on", font_size=21, color=HEAT),
            label(r"about six times earlier estimates: \ storms, \ heat and drought hit everywhere at once, \ and "
                  r"trade carries them", font_size=20, color=GREY_A),
            label(r"their social cost of carbon: \ from about 800 to over 1,300 dollars a tonne, \ across versions "
                  r"of the paper", font_size=20, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to(DOWN * 0.2)
        head = label(r"how large is the damage?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.FRONTIER48.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The first open question is the size of the damage. <bookmark mark='a'/> Chapter twelve measured what a "
            "country's own unusually hot year does: about a point of growth in hot, poor places. <bookmark "
            "mark='b'/> In 2024 Adrien Bilal and Diego Känzig measured something different: what happens when the "
            "whole world has a warm year. They found world GDP about twelve percent lower some six years after a "
            "global rise of one degree, <bookmark mark='c'/> about six times earlier estimates, because extreme "
            "weather strikes many places at once and trade carries the losses. <bookmark mark='d'/> Their social "
            "cost of carbon runs from about eight hundred to over thirteen hundred dollars a tonne in different "
            "versions of the paper. Others question whether global temperature can be separated from everything "
            "else that moves the world economy. If they are right, every number in this part's dials is too low."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
        self.clear_scene()

    def transition(self):
        D = load("dice")
        O = D["opt"]
        y = np.array(O["year"])
        ax = plane([2025, 2150], [0, 3.6], center=LEFT * 2.2 + DOWN * 0.35, x_length=7.2, y_length=4.4,
                   xticks=[2050, 2075, 2100, 2125, 2150], yticks=[0, 1, 2, 3], xfmt=lambda v: f"{v:.0f}",
                   ylabel=r"percent of world output", yfmt=lambda v: f"{v:.0f}\\%", font_size=14)
        k = y <= 2150
        ab = path(ax, y[k], 100 * np.array(O["abate"])[k], POLICY, 3.2, smooth=False)
        dm = path(ax, y[k], 100 * np.array(O["damage"])[k], OPT, 3.2, smooth=False)
        db = path(ax, y[k], 100 * np.array(D["base"]["damage"])[k], BASE, 3.2, smooth=False)
        i30, i50 = list(y).index(2030), list(y).index(2050)
        side = VGroup(
            label(rf"purple: \ the optimal \\ path's cost of cutting: \\ {100 * O['abate'][i30]:.2f}\% of output \\ in "
                  rf"2030, \ {100 * O['abate'][i50]:.2f}\% in 2050", font_size=17, color=POLICY),
            label(r"green and red: \\ damages with and \\ without the cuts", font_size=17, color=WHITE),
            label(r"McGlade and Ekins, \\ 2015: \ for 2\textdegree, \ most \\ coal, \ half the gas, \\ a third of "
                  r"the oil \\ in reserves stay \\ unburned", font_size=17, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The second is the transition itself. <bookmark mark='a'/> In the model, cutting emissions on the "
            f"optimal path costs about {100 * O['abate'][i30]:.2f} percent of world output in 2030 and "
            f"{100 * O['abate'][i50]:.2f} percent in 2050: small beside the economy, <bookmark mark='b'/> and "
            "smaller than the damage it avoids later. <bookmark mark='c'/> But averages hide who pays. Christophe "
            "McGlade and Paul Ekins estimated in 2015 that to hold warming to two degrees at least cost, more than "
            "eighty percent of the world's coal reserves, half its gas and a third of its oil would have to stay "
            "in the ground: assets on the books of firms and the budgets of governments that would be worth far "
            "less. Who bears those losses, how fast capital can move to clean energy, and what that does to "
            "interest rates and inflation, is the macroeconomics of the transition, and it is being written now."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(ab), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(db), Create(dm), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def adaptation(self):
        H = tables.HEALTH_48.data
        cards = point_cards([
            (r"adaptation works", rf"air conditioning cut \\ the toll of US \\ heat by about {H['ac']}\%", COOL),
            (r"but costs money", r"the hottest countries \\ are among the \\ poorest: \ the ones \\ least able to "
                                 r"adapt", HEAT),
            (r"and is a choice", r"where people live, \\ what farmers grow, \\ what cities build: \\ each priced, "
                                 r"\ or not", POLICY),
            (r"the question", r"how much of the \\ damage is left \\ once people adapt, \\ and who pays \\ for it",
             E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"who can adapt?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.HEALTH_48.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The third is adaptation. <bookmark mark='a'/> It works: chapter twelve's air conditioners cut the "
            f"toll of American heat by about {H['ac']} percent. <bookmark mark='b'/> But it costs money, and the "
            "hottest countries, where chapter twelve's curve falls fastest, are among the poorest, the least able "
            "to pay. <bookmark mark='c'/> And it is a set of choices: where people live, what farmers plant, what "
            "cities build, whether flood risk is priced into insurance and property. <bookmark mark='d'/> How much "
            "damage remains once people adapt, and who pays for the adapting, is the question on which the size "
            "of climate damage, and the fairness of climate policy, now turn."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
