from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class Media(VoiceoverScene):
    def construct(self):
        card(self, 12, r"Media and persuasion", r"Can a news channel move an election?",
             "Chapter twelve. Media and persuasion.", lit={2007: r"DellaVigna and Kaplan", 2020: r"Autor et al."},
             scale=("town", "nation"), horizon=("an election",))
        self.fox()
        self.rate()
        self.polarization()

    def fox(self):
        T = tables.MEDIA_47.data
        chain = flow_chain([(r"a new channel, \\ 1996", VOTER), (r"cable systems add it \\ town by town", AUDIT),
                            (r"compare towns \\ with and without", AUDIT), (r"the vote, \\ 1996 to 2000", POL)],
                           notes=[r"Fox News", r"by 2000, \ some \\ towns had it, \\ others not",
                                  r"the timing had \\ little to do \\ with politics", rf"Republican share \\ "
                                                                                      rf"+{T['vote_lo']} to "
                                                                                      rf"{T['vote_hi']} points"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.8)
        tag = published_tag(tables.MEDIA_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Do the media change minds, or only tell people what they already think? <bookmark mark='a'/> In 1996 "
            "a new cable channel, Fox News, was launched. <bookmark mark='b'/> Cable companies added it town by "
            "town, and by the 2000 election some towns had it and others did not. <bookmark mark='c'/> Stefano "
            "DellaVigna and Ethan Kaplan argued that which towns got it early had little to do with their "
            "politics, and compared the change in the Republican vote between 1996 and 2000 in towns with the "
            f"channel and without. <bookmark mark='d'/> The Republican share rose by {T['vote_lo']} to "
            f"{T['vote_hi']} points more where Fox had arrived. In a country where one presidential election that "
            "year was decided by a few hundred votes, that is not small."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
        self.clear_scene()

    def rate(self):
        P_ = load("persuasion")
        T = tables.MEDIA_47.data
        eq = MathTex(r"f = \frac{y_T - y_C}{e_T - e_C}\cdot\frac{1}{1 - y_C}", font_size=46, color=THEORY).move_to(
            UP * 1.9)
        rows = VGroup(
            label(r"$y$: \ the share who vote for the party, \ with ($T$) and without ($C$) the message", font_size=21,
                  color=WHITE),
            label(r"$e$: \ the share who receive the message", font_size=21, color=WHITE),
            label(rf"an Island town: \ $y$ = {P_['yT']:.3f} against {P_['yC']:.3f}; \ $e$ = {P_['eT']:.2f} against "
                  rf"{P_['eC']:.2f} \ $\Rightarrow$ \ $f$ = {100 * P_['rate']:.0f}\%", font_size=21, color=VOTER),
            label(rf"Fox News: \ {T['pers_lo']} to {T['pers_hi']}\% of viewers who were not already Republican, \ "
                  r"depending on the audience measure", font_size=21, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(eq, DOWN, buff=0.45)
        dy, de = P_["yT"] - P_["yC"], P_["eT"] - P_["eC"]
        work = MathTex(rf"f = \frac{{{dy:.3f}}}{{{de:.2f}}}\cdot\frac{{1}}{{1 - {P_['yC']:.2f}}} = {dy / de:.2f}"
                       rf"\times {1 / (1 - P_['yC']):.0f} = {P_['rate']:.2f}", font_size=34,
                       color=VOTER).next_to(rows, DOWN, buff=0.45)
        tag = published_tag(tables.MEDIA_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "A small change in votes can hide a large effect on the people who watched. DellaVigna and Kaplan "
            "turned their estimate into a persuasion rate. <bookmark mark='a'/> Take the difference in the vote "
            "between places with and without the message, <bookmark mark='b'/> divide by the difference in how many "
            "people received it, and divide again by the share who were not already voting that way. <bookmark "
            f"mark='c'/> In an Island town where the party's share is 50.4 percent against 50.0, and 30 percent of "
            f"homes get the channel against 20, the persuasion rate is {100 * P_['rate']:.0f} percent. <bookmark "
            f"mark='d'/> For Fox News, between {T['pers_lo']} and {T['pers_hi']} percent of viewers who were not "
            "already Republican were persuaded, depending on how the audience is measured, and 3 to 8 percent "
            "with the broadest measures. Persuasion rates like these turn up in studies of advertising, canvassing "
            "and news alike."
        ) as vo:
            self.play(FadeIn(tag), Write(eq), run_time=1.5)
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
                if mk == "a":
                    self.play(Indicate(eq[0][2:7], color=WHITE))
                if mk == "c":
                    self.play(Write(work), run_time=2.0)
        self.clear_scene()

    def polarization(self):
        chain = flow_chain([(r"the China shock: \\ Part 36", FEW), (r"jobs lost in \\ exposed districts", LOSS),
                            (r"moderates voted out, \\ 2002 to 2010", POL), (r"more polarized \\ Congress", LOBBY)],
                           notes=[r"imports after 2001", r"manufacturing \\ towns", r"replaced from \\ both sides",
                                  r"and a larger \\ audience for Fox"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.8)
        foot = label(r"Autor, \ Dorn, \ Hanson and Majlesi, \ 2020: \ strong though not definitive evidence; \ "
                     r"polarization did not begin with China", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.MEDIA_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Economic shocks move politics too. <bookmark mark='a'/> Part thirty-six measured the China shock: the "
            "surge of Chinese imports into the United States after 2001. <bookmark mark='b'/> David Autor, David "
            "Dorn, Gordon Hanson and Kaveh Majlesi followed it into elections. In the congressional districts most "
            "exposed, where factories closed, <bookmark mark='c'/> voters removed moderate representatives between "
            "2002 and 2010, replacing them with more conservative Republicans in mostly white districts and more "
            "liberal Democrats elsewhere. <bookmark mark='d'/> Exposed areas also watched more Fox News. The "
            "authors call the evidence strong though not definitive, and note that American polarization did not "
            "begin with China. But a trade shock, with no politics in it, left a political mark."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(foot), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
        self.clear_scene()
