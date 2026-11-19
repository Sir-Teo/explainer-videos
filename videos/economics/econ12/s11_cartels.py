from __future__ import annotations

from videos.economics.econ12.common import *  # noqa: F403

WAR = "#F2788F"
PRICE = "#F2C14E"


class Cartels(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Cartels in the data", r"What do real cartels look like, \ and how are they broken?",
             "Chapter nine. Cartels in the data.", lit={1983: r"Porter's railroad cartel", 1993: r"amnesty for the "
             r"first"}, scale=("firm", "market", "nation"), horizon=("a week", "a decade"))
        self.railroad()
        self.wars()
        self.overcharge()
        self.leniency()

    def railroad(self):
        hc = history_card(1880, r"the Joint Executive Committee", r"a cartel of the railroads carrying grain from "
                          r"Chicago to the Atlantic coast: \\ legal at the time, \ and it set its rates in the open", color=CARTEL, width=11.6, font_size=24).to_edge(UP, buff=0.45)
        rows = VGroup(
            label(r"Robert Porter (1983): \ the weekly rates from 1880 to 1886 \ switch between two regimes",
                  font_size=24),
            label(r"long spells at a collusive rate, \ broken by price wars, \ then back again", font_size=24,
                  color=WAR),
            label(r"were the wars punishments for cheating? \ but punishment that works should never be needed",
                  font_size=24, color=GREY_A),
            label(r"Green and Porter (1984): \ wars can happen with nobody cheating", font_size=25,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Porter, Bell Journal 14(2) (1983); \ Green and Porter, Econometrica 52(1) (1984)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "Cartels have not always been illegal. From 1879 the railroads carrying grain from Chicago to the "
            "Atlantic coast ran an open cartel, the Joint Executive Committee, which set their rates in the "
            "open. <bookmark mark='a'/> In 1983 Robert Porter studied its weekly rates from 1880 to 1886, "
            "and found that they switched between two regimes. <bookmark mark='b'/> Long spells at a collusive rate "
            "were broken by price wars, and then the rate went back up. <bookmark mark='c'/> Were the wars "
            "punishments for cheating? The theory of the last chapter says a cartel that punishes well is never "
            "cheated, so its punishments should never be seen. <bookmark mark='d'/> Edward Green and Porter had "
            "an answer: price wars can happen even when nobody cheats."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def wars(self):
        g = load("greenporter")
        P = np.array(g["P"])
        war = np.array(g["war"], bool)
        T = len(P)
        ax = plane([0, T], [0, 8.5], center=LEFT * 2.6 + DOWN * 0.3, x_length=7.4, y_length=4.6,
                   xticks=[0, 100, 200, 300], yticks=[0, 2, 4, 6, 8], xlabel=r"season", ylabel=r"market price",
                   font_size=16, xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        shade = VGroup()
        k = 0
        while k < T:
            if war[k]:
                j = k
                while j < T and war[j]:
                    j += 1
                shade.add(Polygon(a.c2p(k, 0), a.c2p(j, 0), a.c2p(j, 8.5), a.c2p(k, 8.5), stroke_width=0,
                                  fill_color=WAR, fill_opacity=0.25))
                k = j
            else:
                k += 1
        line = VMobject(stroke_color=PRICE, stroke_width=2).set_points_as_corners(
            [a.c2p(t, float(np.clip(p, 0, 8.5))) for t, p in enumerate(P)])
        trig = DashedLine(a.c2p(0, g["trigger"]), a.c2p(T, g["trigger"]), color=WHITE, stroke_width=1.5)
        tl = label(r"trigger", font_size=15).next_to(a.c2p(T, g["trigger"]), RIGHT, buff=0.1)
        side = VGroup(
            label(r"two firms see only the price, \\ which also moves with demand they can't see", font_size=21),
            label(r"the deal: \ produce the cartel's quantity, \\ but if the price ever falls below the trigger, \\ "
                  r"produce Cournot's for six seasons", font_size=21, color=CARTEL),
            label(rf"nobody ever cheats; \ yet {g['n_wars']} wars in {T} seasons, \\ {100 * g['share_war']:.0f}\% of "
                  r"the time at war", font_size=22, color=WAR),
            label(r"every war began with a bad season for demand, \\ not with a cheat", font_size=21, color=GREY_A),
            label(r"the wars are the price of keeping everyone honest", font_size=22, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = agora_tag(corner=DR, font_size=15)
        with self.voiceover(
            "Here is their idea in Agora. <bookmark mark='a'/> Two firms cannot see each other's output, only the "
            "market price, and the price also moves with demand they cannot see. <bookmark mark='b'/> They agree to "
            "produce the cartel's quantity, and that if the price ever falls below a trigger, both will produce "
            "Cournot's quantity for six seasons, then return to the deal. <bookmark mark='c'/> Nobody ever cheats. "
            "Yet over three hundred seasons there are ten price wars, and the market spends a fifth of its time at "
            "war. <bookmark mark='d'/> Every war began with a bad season for demand, which looked like cheating. "
            "<bookmark mark='e'/> The wars are what it costs to keep everyone honest: without them, cheating could "
            "hide behind bad luck. Porter's estimates for the railroads were consistent with wars of this kind."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("b")
            self.play(Create(trig), FadeIn(tl), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(line), FadeIn(shade), FadeIn(side[2]), run_time=4)
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def overcharge(self):
        L = load("lysine")
        lo, hi = L["overcharge_musd"]
        slo, shi = L["sales_musd"]
        plo, phi = L["overcharge_pct"]
        rows = VGroup(
            label(r"an overcharge: \ what buyers paid, \ minus what they would have paid without the cartel",
                  font_size=24),
            label(r"the price without the cartel is never seen: \ it must be estimated", font_size=24, color=GREY_A),
            label(rf"lysine, \ 1992--95: \ sales of \${slo} to {shi} million in America; \ an overcharge of \${lo} to "
                  rf"{hi} million", font_size=23, color=PRICE),
            label(rf"so prices {plo} to {phi} percent above the competitive level \ (Connor's estimate)",
                  font_size=24, color=CARTEL),
            label(r"and the price war before the cartel? \ below cost: \ not a fair benchmark either", font_size=23,
                  color=HOLD),
            label(r"how big are overcharges in general? \ chapter 14's dial", font_size=24, color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).move_to(UP * 0.1)
        tag = published_tag(r"Connor, Choices 13(3) (1998), p.\ 17", corner=DR, font_size=13)
        with self.voiceover(
            "What did the lysine cartel cost its buyers? <bookmark mark='a'/> The overcharge is what buyers paid "
            "minus what they would have paid without the cartel. <bookmark mark='b'/> The second price is never "
            "seen, so it must be estimated, which is where economists earn their fees in court. "
            "<bookmark mark='c'/> Connor put American sales of lysine during the conspiracy at four hundred and "
            "ninety-five to five hundred and fifty million dollars, and the overcharge to direct buyers at "
            "sixty-five to a hundred and forty million. <bookmark mark='d'/> That makes prices twelve to "
            "twenty-eight percent above the competitive level. <bookmark mark='e'/> Notice what the benchmark cannot "
            "be: the price war of 1991 and 1992, when prices were below cost, was no more competitive than the "
            "cartel. <bookmark mark='f'/> How large overcharges are across hundreds of cartels is chapter fourteen's "
            "dial."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0]))
            for mk, r in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def leniency(self):
        le = load("leniency")
        lam = np.array(le["lam"])
        ax = plane([0, 1], [0, 105], center=LEFT * 3.0 + DOWN * 0.3, x_length=5.8, y_length=4.6,
                   xticks=[0, 0.5, 0.8, 1], yticks=[0, 20, 50, 100], xlabel=r"share of the fine forgiven to the "
                   r"first to confess", ylabel=r"expected fine", font_size=16, xfmt=lambda v: f"{v:.1f}",
                   yfmt=lambda v: f"{v:.0f}")
        a = ax.ax
        conf = path(ax, lam, le["confess"], color=COMPETE, width=3.5, smooth=False)
        sil = path(ax, lam, le["silent"], color=CARTEL, width=3.5, smooth=False)
        cl = label(r"confess first", font_size=16, color=COMPETE).next_to(a.c2p(0.3, 88), RIGHT, buff=0.05)
        sl = label(r"stay silent", font_size=16, color=CARTEL).next_to(a.c2p(0.05, 20), UP, buff=0.08)
        cut = DashedLine(a.c2p(le["threshold"], 0), a.c2p(le["threshold"], 100), color=WHITE, stroke_width=1.5)
        side = VGroup(
            label(rf"each member: \ stay silent \\ (the law finds the cartel with chance {le['caught']:.1f}), \\ or "
                  r"confess", font_size=21),
            label(r"if a rival confesses first, \ you pay in full \\ whatever you do", font_size=21, color=GREY_A),
            label(rf"forgive the first confessor more than \\ {100 * le['threshold']:.0f}\% of the fine, \ and "
                  r"confessing \\ becomes the dominant choice", font_size=21, color=COMPETE),
            label(r"a prisoner's dilemma, \ built on purpose", font_size=23, color=E.ACCENT),
            label(r"United States, \ August 1993: \ automatic amnesty \\ for the first to report \ (before, \ about "
                  r"one \\ application a year); \ Europe followed in 1996", font_size=20, color=LEADER),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.35)
        tag = published_tag(r"U.S. Department of Justice, Corporate Leniency Policy (1993); \ the game: \ Agora",
                            corner=DR, font_size=13)
        with self.voiceover(
            "How are cartels broken now? With a game. <bookmark mark='a'/> Each member of a cartel can stay silent, "
            "and hope the authorities don't find it, which on the Island happens with a chance of one in five, or "
            "confess. <bookmark mark='b'/> If a rival confesses first, you pay the full fine whatever you do. "
            "<bookmark mark='c'/> So if the first to confess is forgiven more than eighty percent of the fine, "
            "confessing beats silence whatever the others do. <bookmark mark='d'/> It is a prisoner's dilemma, "
            "built on purpose. <bookmark mark='e'/> In August 1993 the American Justice Department made amnesty "
            "automatic for the first firm to report a cartel it was not yet investigating. Under the older policy it "
            "had received about one application a year. The European Commission followed with a leniency notice in "
            "1996, and most competition authorities now have one."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), Create(sil), FadeIn(sl))
            vo.wait_until("b")
            self.play(FadeIn(side[1]))
            vo.wait_until("c")
            self.play(Create(conf), FadeIn(cl), Create(cut), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()
