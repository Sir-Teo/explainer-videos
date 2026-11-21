from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403

PROBLEMS = [
    r"Olson: \ a policy worth $B$ = 100 to a group, \ won with probability $E/(E+1)$. \ Find each member's effort and "
    r"the group's total for $n$ = 4 and $n$ = 25. \ At what size does the group give up?",
    r"Tullock: \ five players compete for a prize of 100. \ Find each one's spending in equilibrium and the share of "
    r"the prize dissipated. \ What if one player's spending counts double?",
    r"Rent seeking: \ a quota raises a price from 2 to 6 on demand $q = 10 - p$. \ Find the triangle and the "
    r"rectangle, \ and the social cost if the rectangle is competed away.",
    r"Agency: \ office is worth $W$ = 0.2 a term, \ rents up to 1, \ $\delta$ = 0.6. \ Find the rents voters must "
    r"tolerate. \ How high must $W$ be for them to tolerate none?",
    r"Close elections: \ explain why a regression discontinuity needs the density of the margin to be smooth at "
    r"zero, \ and what bunching just above zero would mean.",
    r"Persuasion: \ a channel reaches 40\% of homes against 10\%, \ and a party's share is 52\% against 51\%. \ Find "
    r"the persuasion rate.",
    r"The franchise: \ explain why the elite democratizes when crises are rare but not when they are frequent.",
    r"$\bigstar$ \ Two groups lobby with stakes per head $v_s$ and $v_l$ in a Tullock contest. \ Derive the "
    r"efforts and the probability the small group wins.",
]


class Outro(VoiceoverScene):
    def construct(self):
        self.answer()
        self.recap()
        self.problems()
        self.references()
        self.next_part()

    def answer(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).move_to(UP * 2.2)
        a = wrapped_label(r"Because small groups organize and large ones do not; \ because chasing privileges is "
                          r"rewarded; \ because voters cannot watch everything, \ and elites cannot promise. \ What "
                          r"helps is what makes the hidden visible and the powerful accountable: \ audits, \ "
                          r"published accounts, \ elections, \ and rules.", 11.6, 25, WHITE)
        a.next_to(q, DOWN, buff=0.5)
        F = load("film")
        mini = plane([1900, 2025], [0, 1], x_length=4.2, y_length=1.3)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, DEM, 2.4, smooth=False).next_to(a, DOWN, buff=0.35)
        with self.voiceover(
            "So: why do governments so often choose policies that economists can show are wasteful? <bookmark "
            "mark='a'/> Because small groups with a lot at stake organize, and large groups with a little at stake "
            "do not. Because chasing a privilege is rewarded, so resources are spent winning it. Because voters "
            "cannot watch everything their agents do, and elites cannot credibly promise to give up what they hold. "
            "What helps is whatever makes the hidden visible and the powerful accountable: audits, published "
            "accounts, competitive elections, and rules that take the most tempting decisions out of reach."
        ) as vo:
            self.play(FadeIn(q, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(a, shift=UP * 0.1), run_time=2)
            self.play(Create(logo), run_time=1.5)
        self.clear_scene()

    def recap(self):
        R, S, K, Tl, V, Se, M, F, W, Tx, C, P_ = (load(x) for x in (
            "roads", "sugar", "tokens", "tullock", "voting", "senate", "mayors", "franchise", "wgi", "tax",
            "conflict", "persuasion"))
        items = [
            (r"roads: \ audits cut missing spending by about 8 points; \ meetings barely moved it", AUDIT),
            (rf"sugar: \ twice the world price; \ about \${S['per_farm'] / 1000:,.0f},000 a farm against "
             rf"\${S['per_person']:.0f} a head".replace(",", "{,}"), FEW),
            (rf"build or lobby: \ everyone ends with {K['nash_payoff']:.0f}, \ not {K['best_payoff']:.0f}", LOBBY),
            (rf"rent seeking: \ ten players spend {100 * Tl['dissipated'][8]:.0f}\% of the prize", LOSS),
            (r"voters: \ swing groups and organized groups get more", VOTER),
            (rf"close Senate races: \ winning is worth {Se['jump']:.1f} points next time", VOTER),
            (rf"agency: \ lame ducks take more; \ first-term mayors {100 * M['fewer']:.0f}\% less", POL),
            (r"measurement: \ core samples, \ share prices, \ parking tickets, \ surveys", AUDIT),
            (r"the franchise: \ the vote as a promise that cannot be withdrawn", ELITE),
            (rf"state capacity: \ poor states collect {Tx['median_poorest']:.0f}\% of GDP, \ rich "
             rf"{Tx['median_richest']:.0f}\%", DEM),
            (rf"conflict: \ rain as an instrument, \ {say_num(C['iv'])} against a planted {say_num(C['truth'])}",
             CORRUPT),
            (r"media: \ persuasion rates; \ cycles: \ unemployment timed to elections", MANY),
        ]
        rows = VGroup(*[label(rf"{n + 1}.\ \ {txt}", font_size=28, color=col) for n, (txt, col) in enumerate(items)])
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        head = label(r"Part 47, \ in twelve lines", font_size=42).to_edge(UP, buff=0.3)
        if rows.width > 13.2:
            rows.width = 13.2
        room = head.get_bottom()[1] - 0.35 + 3.75
        if rows.height > room:
            rows.scale_to_fit_height(room)
        rows.next_to(head, DOWN, buff=0.35)
        del R, V, F, W, P_
        with self.voiceover(
            "Part forty-seven in twelve lines. <bookmark mark='a'/> Audits cut the money missing from Indonesia's "
            "roads; meetings did little. America's sugar program costs each consumer a few dollars and pays each "
            "farm a fortune, so it survives. When tokens can build or lobby, everyone lobbies and everyone is "
            "poorer. In a contest for a prize, competitors spend nearly all of it. Parties court swing voters and "
            "organized groups. In close Senate races, winning is worth about seven points next time. Politicians "
            "who cannot run again take more. Corruption can be measured with core samples, share prices, parking "
            "tickets and surveys, each with its own blind spots. Extending the vote is how an elite makes a promise "
            "it cannot take back. Poor states collect little tax. Rain shows that poverty breeds conflict. And "
            "media persuade, and governments time the economy to elections, unless the decision is delegated."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r_, shift=RIGHT * 0.15) for r_ in rows], lag_ratio=0.8), run_time=40.0)
        self.clear_scene()

    def problems(self):
        ps = problem_set(PROBLEMS, font_size=19, width=13.0)
        with self.voiceover(
            "The problems. Olson's group effort; Tullock's contest; the triangle and the rectangle; the threshold "
            "of the agency model; what a regression discontinuity at a close election assumes; a persuasion rate; "
            "the franchise; and a starred derivation of the contest between a small and a large group. Full "
            "solutions are in the part's notes."
        ):
            self.play(FadeIn(ps.head), FadeIn(ps.rows[0], shift=UP * 0.1), run_time=0.8)
            self.play(LaggedStart(*[FadeIn(r) for r in ps.rows[1:]], lag_ratio=0.4), run_time=6)
        self.wait(4)
        self.clear_scene()

    def references(self):
        rc = reference_card(
            [r"Mancur Olson, \emph{The Logic of Collective Action} (1965)",
             r"Torsten Persson and Guido Tabellini, \emph{Political Economics} (2000)",
             r"Daron Acemoglu and James Robinson, \emph{Economic Origins of Dictatorship and Democracy} (2006)",
             r"Timothy Besley and Torsten Persson, \emph{Pillars of Prosperity} (2011)"],
            [r"Tullock (1967); \ Stigler (1971); \ Barro (1973); \ Krueger (1974); \ Nordhaus (1975)",
             r"Ferejohn (1986); \ Grossman and Helpman (1994); \ Goldberg and Maggi (1999); \ Fisman (2001)",
             r"Lee, \ Moretti and Butler (2004); \ Reinikka and Svensson (2004); \ Miguel et al. (2004)",
             r"Olken (2007); \ Fisman and Miguel (2007); \ DellaVigna and Kaplan (2007); \ Lee (2008)",
             r"Ferraz and Finan (2011); \ Cattaneo et al. (2015); \ Acemoglu et al. (2019); \ Funke et al. (2023)"])
        with self.voiceover(
            "The reading: Mancur Olson's Logic of Collective Action; Torsten Persson and Guido Tabellini's graduate "
            "text, Political Economics; Daron Acemoglu and James Robinson's Economic Origins of Dictatorship and "
            "Democracy; and Timothy Besley and Torsten Persson's Pillars of Prosperity. Then the papers, from "
            "Tullock's rectangle to the economics of populism."
        ):
            self.play(FadeIn(rc))
        self.wait(1.5)
        self.clear_scene()

    def next_part(self):
        hc = history_card(1980, r"Simon and Ehrlich", r"bet on the prices of five metals over ten years; \ in 1990 "
                          r"Ehrlich mails Simon a cheque for \$576.07, \ though over many other decades he would have "
                          r"won", color=E.ACCENT, width=10.4, font_size=24)
        nxt = VGroup(label(r"Next: \ Part 48 \ $\cdot$ \ Act IX, \ The Fields", font_size=30, color=GREY_B),
                     label(r"Environment and Climate", font_size=46),
                     label(r"what is a tonne of carbon dioxide worth, \ and what does the answer turn on?",
                           font_size=24, color=E.ACCENT)).arrange(DOWN, buff=0.22)
        head = label(r"from failures of government \ to failures of markets the size of the planet", font_size=26,
                     color=GREY_A).to_edge(UP, buff=0.5)
        VGroup(hc, nxt).arrange(DOWN, buff=0.6).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Next time, the environment and the climate. <bookmark mark='a'/> In 1980 the economist Julian Simon "
            "offered the biologist Paul Ehrlich a bet: pick any raw materials, and in ten years their real prices "
            "will be lower. Ehrlich picked five metals. In 1990 he mailed Simon a cheque for five hundred and "
            "seventy-six dollars and seven cents, though over many other ten-year spans he would have won. "
            "<bookmark mark='b'/> Part forty-eight asks what a tonne of carbon dioxide is worth, and what the "
            "answer turns on."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(hc, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.1))
        self.wait(9.5)
