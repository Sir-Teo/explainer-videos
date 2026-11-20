from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


class Social(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Social preferences", r"How much do other people's payoffs matter, and when?",
             "Chapter nine. Social preferences.",
             lit={1999: r"Fehr and Schmidt", 2006: r"Gneezy and List", 2007: r"List"},
             scale=("person", "firm"), horizon=("a day",))
        self.ultimatum()
        self.gift()
        self.dictator()

    def ultimatum(self):
        U = load("social")
        s = np.array(U["s"])
        acc = np.array(U["accept"])
        ax = plane([0, 0.5], [0, 1], center=LEFT * 2.2 + DOWN * 0.4, x_length=6.8, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   xlabel=r"share of the pie offered", ylabel=r"share of responders who accept",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        ln = path(ax, s, acc, PLAN, 3.2, smooth=False)
        oh = np.array(U["offer_hist"], float)
        oh = oh / oh.max() * 0.45
        edges = np.linspace(0, 0.5, 11)
        obars = VGroup()
        for lo, hi, h in zip(edges[:-1], edges[1:], oh):
            if h <= 0:
                continue
            p0, p1 = ax.ax.c2p(lo + 0.004, 0), ax.ax.c2p(hi - 0.004, h)
            obars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=GYM,
                                fill_opacity=0.6).move_to((p0 + p1) / 2))
        eq = MathTex(r"U_i = x_i - \alpha\max(x_j - x_i, 0) - \beta\max(x_i - x_j, 0)", font_size=30,
                     color=THEORY).to_edge(UP, buff=0.4)
        side = VGroup(
            label(r"$\alpha$: \ envy; \ $\beta$: \ guilt", font_size=19, color=WHITE),
            label(r"a responder rejects \\ any offer below \\ $\alpha / (1 + 2\alpha)$", font_size=18, color=PLAN),
            label(rf"{100 * U['reject_20']:.0f}\% would reject 20\%", font_size=18, color=LOSS),
            label(rf"gold: \ proposers' offers; \\ mean {100 * U['mean_offer']:.0f}\%, \ "
                  rf"{100 * U['share_half']:.0f}\% \\ offer half", font_size=18, color=GYM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        game = flow_chain([(r"the proposer \\ offers a share", GYM), (r"the responder \\ accepts", GAIN),
                           (r"or rejects: \\ both get nothing", LOSS)],
                          notes=[r"of a pie of, \\ say, \$10", r"the split stands", r"Part 5 says: \\ never "
                                 r"reject \\ a positive offer"], box_w=3.0, font_size=21, note_size=17)
        game.move_to(UP * 0.3)
        tag = published_tag(tables.SOCIAL_45.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "In the ultimatum game one player proposes how to split a pie, and the other accepts, or rejects and "
            "both get nothing. Part five's agents would offer a crumb, and it would be accepted. In laboratories "
            "around the world, offers are much more generous than that, and low offers are often rejected. "
            "<bookmark mark='a'/> Ernst Fehr and Klaus Schmidt explained this with one change to the agent: people "
            "dislike inequality. Alpha measures how much it hurts to have less than the other player, beta how much "
            "it hurts to have more. <bookmark mark='b'/> A responder with envy alpha prefers nothing to an offer "
            "below alpha over one plus two alpha. On the Island, envy varies from person to person, and this is the "
            f"share who would accept each offer. <bookmark mark='c'/> {100 * U['reject_20']:.0f} percent would turn "
            "down a fifth of the pie. <bookmark mark='d'/> Proposers who know this offer a lot: on average "
            f"{100 * U['mean_offer']:.0f} percent, and those whose guilt beta exceeds a half offer exactly half, "
            "because for them every dollar of advantage hurts more than it pleases."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(game.boxes[0]), FadeIn(game.notes[0]), run_time=1.0)
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a_), FadeIn(b_), FadeIn(n_)) for a_, b_, n_ in
                                    zip(game.arrows, game.boxes[1:], game.notes[1:])], lag_ratio=0.6), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeOut(game), FadeIn(ax), Write(eq), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(ln), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in obars], lag_ratio=0.2), FadeIn(side[3]))
        self.clear_scene()

    def gift(self):
        G = load("social")["gift"]
        hrs = np.array(G["hour"])
        ax = plane([1, hrs[-1]], [0.9, 1.35], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=list(hrs), yticks=[1.0, 1.1, 1.2, 1.3], xlabel=r"hour of the job",
                   ylabel=r"effort, \ relative to the base wage", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=14)
        flat = path(ax, hrs, G["flat"], GREY_B, 3.0, smooth=False)
        gift = path(ax, hrs, G["gift"], GAIN, 3.2)
        side = VGroup(
            label(r"grey: \ paid as advertised", font_size=18, color=GREY_B),
            label(r"green: \ told on arrival \\ they will be paid more", font_size=18, color=GAIN),
            label(r"the extra effort fades \\ within hours \ (the \\ Island's assumption)", font_size=18,
                  color=HOLD),
            label(r"Gneezy and List: \\ in two field jobs, \\ the same pattern", font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.SOCIAL_45.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "If workers reciprocate kindness, an employer might pay more than it must and get more effort back: the "
            "gift exchange behind efficiency wages in Part thirty-eight. Laboratory experiments find it. Does it "
            "survive a real job? <bookmark mark='a'/> Uri Gneezy and John List hired people for one-day jobs, "
            "entering library books into a database and raising money door to door. <bookmark mark='b'/> On "
            "arrival, some were told they would be paid more than advertised. <bookmark mark='c'/> They worked "
            "harder at first, but within a few hours the difference was gone. The Island's workers are built the "
            "same way. <bookmark mark='d'/> Reciprocity is real, but it can be shorter-lived in the field than in "
            "the laboratory, where most sessions last an hour."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(flat), FadeIn(side[0]), run_time=1.2)
            vo.wait_until("a")
            self.play(Indicate(side[0], color=WHITE))
            vo.wait_until("b")
            self.play(Create(gift), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def dictator(self):
        cards = point_cards([
            (r"the dictator game", r"one player splits \\ money with another \\ who has no say", PLAN),
            (r"most give something", r"in the standard \\ game, \ even \\ to a stranger", GAIN),
            (r"List, \ 2007", r"let dictators also \\ take, \ and giving \\ falls sharply", LOSS),
            (r"what it measures", r"preferences, \\ and also the menu \\ and being watched", HOLD),
        ], width=12.8, cols=4, font_size=18).move_to(UP * 0.4)
        fine = label(r"a fine is a price: \ Part 1's day-care fine raised late pickups at six centres; \ a later "
                     r"survey-based \\ study did not find the same effect in its setting. \ Incentives can crowd out "
                     r"motives, \ sometimes.", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.7)
        tag = published_tag(tables.SOCIAL_45.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The simplest measure of generosity is the dictator game. <bookmark mark='a'/> One player divides a sum "
            "of money with an anonymous other, who has no say at all. <bookmark mark='b'/> Most dictators give "
            "something, which looked like direct evidence of altruism. <bookmark mark='c'/> John List changed the "
            "menu: dictators could also take money from the other player. Giving fell sharply, and many took. If "
            "dictators had fixed preferences over the two payoffs, adding options they did not use should not have "
            "changed what they chose. <bookmark mark='d'/> So the game measures preferences, but also what the "
            "menu suggests is appropriate, and the sense of being watched. <bookmark mark='e'/> Social motives also "
            "interact with incentives. In Part one, a fine for late pickup at six Israeli day-care centres was "
            "followed by more late parents, not fewer: a fine is a price. A 2020 replication that put the same "
            "situation to online respondents as a written scenario found the opposite, fines reducing intended "
            "lateness. A survey is not a field experiment, but one striking result should be held as what it is: "
            "one result."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(fine))
        self.clear_scene()
