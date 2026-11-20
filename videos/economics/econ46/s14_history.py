from __future__ import annotations

from videos.economics.econ46.common import *  # noqa: F403


class History(VoiceoverScene):
    def construct(self):
        card(self, 12, r"History that persists", r"Can a rule abolished two centuries ago still make people poor?",
             "Chapter twelve. History that persists.", lit={2008: r"Nunn", 2010: r"Dell", 2011: r"Nunn and Wantchekon"},
             scale=("district", "continent"), horizon=("centuries",))
        self.mita()
        self.island()
        self.why()
        self.slaves()

    def mita(self):
        T = tables.HISTORY_46.data
        chain = flow_chain([(rf"{T['start']}: \ the \emph{{mita}}", HIST), (r"forced labour \\ in the mines", LOSS),
                            (r"only inside \\ a boundary", HIST), (rf"abolished \\ {T['end']}", GREY_B)],
                           notes=[r"Spanish Peru \\ and Bolivia", r"silver at Potos\'i, \\ mercury at \\ Huancavelica",
                                  r"drawn by colonial \\ administrators", r"two centuries ago"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 1.0)
        res = VGroup(
            label(rf"inside the old boundary today: \ household consumption about {T['consumption']}\% lower",
                  font_size=21,
                  color=LOSS),
            label(rf"and children's stunting about {T['stunting']} points higher", font_size=21, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.HISTORY_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            f"In {T['start']} the Spanish rulers of Peru imposed the mita. <bookmark mark='a'/> Villages had to "
            "send one in seven of their adult men to work in the silver mines of Potosí and the mercury mines of "
            "Huancavelica, under brutal conditions. <bookmark mark='b'/> The obligation applied only to villages "
            "inside a boundary drawn by colonial administrators; villages just outside were exempt. <bookmark "
            f"mark='c'/> The mita was abolished in {T['end']}, more than two centuries ago. <bookmark mark='d'/> "
            "Melissa Dell compared districts just inside the old boundary with districts just outside it, with the "
            "same altitude, soils and ethnic make-up. Inside, household consumption today is about "
            f"{T['consumption']} percent lower, and children are about {T['stunting']} points more likely to be "
            "stunted."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]), FadeIn(chain.notes[0]),
                      FadeIn(chain.notes[1]))
            for k, mk in zip((1, 2), "bc"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(r_, shift=UP * 0.1) for r_ in res], lag_ratio=0.6), run_time=2.0)
        self.clear_scene()

    def island(self):
        M = load("mita")
        h = M["bandwidth"]
        ax = plane([-150, 150], [4.0, 5.8], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.2, y_length=4.8,
                   xticks=[-150, -100, -50, 0, 50, 100, 150], yticks=[4.0, 4.4, 4.8, 5.2, 5.6],
                   xlabel=r"distance to the old boundary, \ km \ (inside on the left)", ylabel=r"log consumption",
                   xfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", yfmt=lambda v: f"{v:.1f}",
                   font_size=13)
        cut = vline(ax, 0, 4.0, 5.8, WHITE)
        pts = VGroup(*[dot(ax, x, y, HIST if x < 0 else CONTROL, 0.075) for x, y in zip(M["mids"], M["means"])])
        win = Rectangle(width=(ax.ax.c2p(h, 0) - ax.ax.c2p(-h, 0))[0],
                        height=(ax.ax.c2p(0, 5.8) - ax.ax.c2p(0, 4.0))[1],
                        stroke_width=0, fill_color=E.ACCENT, fill_opacity=0.08).move_to(ax.ax.c2p(0, 4.9))
        fi = seg(ax, -h, np.polyval(M["fit_in"], -h), 0, np.polyval(M["fit_in"], 0), HIST, 3.2)
        fo = seg(ax, 0, np.polyval(M["fit_out"], 0), h, np.polyval(M["fit_out"], h), CONTROL, 3.2)
        side = VGroup(
            label(rf"the Island: \ {TRUTH['mita']['n']:,} districts".replace(",", "{,}"), font_size=18, color=WHITE),
            label(r"dots: \ averages in \\ 10 km bins", font_size=18, color=GREY_A),
            label(rf"lines: \ local linear fits \\ within {h:.0f} km", font_size=18, color=E.ACCENT),
            label(rf"the jump: \ {M['jump']:+.3f} \\ (planted {M['effect']:+.2f})".replace("-", "{-}"), font_size=19,
                  color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "The Island has an old boundary too, with a planted effect. <bookmark mark='a'/> Each dot is the "
            "average log consumption of districts in a ten-kilometre band, inside the old boundary on the left. "
            "Consumption rises gently from left to right everywhere, as land gets lower and closer to the coast. "
            f"<bookmark mark='b'/> Fit a line on each side, using only districts within {h:.0f} kilometres of the "
            f"boundary. <bookmark mark='c'/> The gap between the lines at the boundary is {say_num(M['jump'], 3)} "
            f"in logs, close to the planted {say_num(M['effect'])}. A regression discontinuity across a line on a "
            "map works like the one across a cutoff in a score: neighbours on either side are compared, and "
            "whatever changes smoothly with distance cancels out."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(cut), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.05), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(win), Create(fi), Create(fo), FadeIn(side[2]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def why(self):
        cards = point_cards([
            (r"land", r"large estates formed \\ outside the \\ boundary, \ where \\ labour was free \\ to hire", HIST),
            (r"roads", r"their owners \\ lobbied for roads \\ that still reach \\ markets", TOWN),
            (r"inside", r"smallholders, \ fewer \\ roads, \ more \\ subsistence \\ farming today", LOSS),
            (r"a caution", r"Part 19: \ maps \\ regressed on maps \\ can find history \\ in noise", HOLD),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"why would it last?", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.HISTORY_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "How does a labour rule abolished in 1812 lower incomes today? Dell's answer is land. <bookmark "
            "mark='a'/> Large estates, haciendas, formed mostly outside the boundary, where they did not have to "
            "compete with the mita for workers. <bookmark mark='b'/> Their owners had the political connections to "
            "get roads built, and those roads still carry farmers' produce to market. <bookmark mark='c'/> Inside "
            "the boundary, there are fewer roads, and more families farm only to feed themselves. <bookmark "
            "mark='d'/> A caution from Part nineteen: studies that regress one map on another can find "
            "persistence in what is really spatial noise. A discontinuity at a boundary, comparing near "
            "neighbours, is much less exposed to that problem, which is why Dell's design is so admired."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def slaves(self):
        chain = flow_chain([(r"slaves taken, \\ by country, \\ 1400--1900", HIST), (r"income today", LOSS),
                            (r"instrument: \\ sailing distance \\ to the markets", TRIAL), (r"trust today", HIST)],
                           notes=[r"from shipping \\ and census records", r"the most raided \\ are the poorest",
                                  r"Nunn, \ 2008", r"Nunn and \\ Wantchekon, \ 2011"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.7)
        foot = label(r"people from the groups raided most report less trust in neighbours, \ relatives and "
                     r"government", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.9)
        tag = published_tag(tables.HISTORY_46.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The largest example is Africa's slave trades. <bookmark mark='a'/> Nathan Nunn assembled shipping "
            "and census records to estimate how many people were taken from each part of Africa over five "
            "centuries. <bookmark mark='b'/> The countries from which the most slaves were taken are the poorest "
            "today. <bookmark mark='c'/> That could be because poorer places were raided more, so he used the "
            "sailing distance from each country to the slave markets of the Americas and the Indian Ocean as an "
            "instrument, and the relationship survived. <bookmark mark='d'/> With Leonard Wantchekon he found one "
            "channel: people from the ethnic groups raided most heavily trust others less today, a belief passed "
            "down from a time when neighbours and even relatives might sell you."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            self.play(FadeIn(foot))
        self.clear_scene()
