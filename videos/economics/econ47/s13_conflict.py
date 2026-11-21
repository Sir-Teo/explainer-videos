from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403


class Conflict(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Conflict", r"Does poverty cause war, and do resources make it worse?",
             "Chapter eleven. Conflict.", lit={1995: r"Sachs and Warner", 2004: r"Miguel, Satyanath and Sergenti"},
             scale=("nation",), horizon=("a year", "decades"))
        self.problem()
        self.island()
        self.resources()

    def problem(self):
        chain = flow_chain([(r"poor growth", LOSS), (r"civil conflict", CORRUPT), (r"rain", AUDIT),
                            (r"growth, \ and only \\ through growth, \\ conflict", E.ACCENT)],
                           notes=[r"$\rightarrow$ conflict?", r"$\rightarrow$ poor growth too", r"moves farm output \\ "
                                  r"in Africa", r"an instrument"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.9)
        res = label(r"41 African countries, \ 1981--99: \ a 5\% fall in growth raised the risk of civil conflict "
                    r"\\ the next year by up to 10 points, \ nearly half", font_size=21, color=E.ACCENT).to_edge(
            DOWN, buff=0.9)
        tag = published_tag(tables.CONFLICT_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Poor countries have far more civil wars than rich ones. <bookmark mark='a'/> Does poverty cause war? "
            "<bookmark mark='b'/> Or does war cause poverty? Both, surely, which is why a simple correlation proves "
            "nothing. <bookmark mark='c'/> Edward Miguel, Shanker Satyanath and Ernest Sergenti looked for "
            "something that moves incomes but not conflict directly, and found it in the rain: in Africa, where "
            "most farming depends on it, a dry year means a poor year. <bookmark mark='d'/> Using rainfall as an "
            "instrument for growth, as in Part four, they found that a fall in growth of five percent raised the "
            "risk of civil conflict in the following year by up to ten percentage points, nearly half."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]), run_time=1.0)
            for k, mk in enumerate("abc"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("d")
            self.play(FadeIn(res))
        self.clear_scene()

    def island(self):
        C = load("conflict")
        Tc = TRUTH["conflict"]
        rows = [(r"the truth", C["truth"], GREY_B), (r"least squares", C["ols"], LOSS),
                (r"rainfall as \\ the instrument", C["iv"], AUDIT)]
        ax = plane([0, 3], [-3.0, 0], center=LEFT * 2.0 + UP * 0.3, x_length=6.6, y_length=4.2, xticks=[],
                   yticks=[-3, -2, -1, 0], ylabel=r"change in the probability of conflict, \ per unit of growth",
                   yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0", font_size=13)
        bars = VGroup()
        for i, (nm, v, col) in enumerate(rows):
            p0, p1 = ax.ax.c2p(0.5 + i - 0.3, 0), ax.ax.c2p(0.5 + i + 0.3, v)
            r = Rectangle(width=p1[0] - p0[0], height=abs(p1[1] - p0[1]), stroke_width=0, fill_color=col,
                          fill_opacity=0.85).move_to((p0 + p1) / 2)
            bars.add(VGroup(r, label(nm, font_size=14, color=WHITE).next_to(ax.ax.c2p(0.5 + i, -3.0), DOWN, buff=0.1),
                            label(rf"{v:+.2f}".replace("-", "{-}"), font_size=16, color=WHITE).next_to(r, DOWN,
                                                                                                buff=0.05)))
        err = Line(ax.ax.c2p(2.5, C["iv"] - 1.96 * C["iv_se"]), ax.ax.c2p(2.5, min(C["iv"] + 1.96 * C["iv_se"], 0)),
                   color=WHITE, stroke_width=2)
        side = VGroup(
            label(rf"the Island: \ {Tc['countries']} countries, \\ {Tc['years']} years", font_size=18, color=WHITE),
            label(rf"growth is measured \\ with error of \\ {100 * Tc['error_sd']:.0f} points", font_size=18,
                  color=HOLD),
            label(r"the error drags \\ least squares \\ toward zero", font_size=18, color=LOSS),
            label(rf"rain is unrelated to \\ the error: \ first-stage \\ F = {C['F']:.0f}", font_size=18, color=AUDIT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            f"The Island has {Tc['countries']} countries followed for {Tc['years']} years, with the planted "
            "effect: a fall in growth of five points raises the risk of conflict by ten. <bookmark mark='a'/> In "
            "grey, the truth. <bookmark mark='b'/> Growth in poor countries is measured badly, here with an error "
            f"of {100 * Tc['error_sd']:.0f} points, and that drags a least-squares estimate toward zero: "
            f"{say_num(C['ols'])}. <bookmark mark='c'/> Rainfall moves true growth, and has nothing to do with the "
            f"statistician's errors, so the instrumental estimate recovers the effect: {say_num(C['iv'])}, with a "
            f"standard error of {C['iv_se']:.2f}. <bookmark mark='d'/> An instrument is only as good as its "
            "assumption: that rain affects conflict only through incomes. And later work found the link between "
            "rain and growth in Africa weaker after 2000, so the instrument itself has grown weaker."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), *[FadeIn(b[1]) for b in bars], run_time=1.0)
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0][0], UP), FadeIn(bars[0][2]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1][0], UP), FadeIn(bars[1][2]), FadeIn(side[1]), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[2][0], UP), FadeIn(bars[2][2]), Create(err), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(Indicate(bars[2], color=WHITE))
        self.clear_scene()

    def resources(self):
        cards = point_cards([
            (r"the finding", r"Sachs and Warner: \\ resource exporters \\ in 1971 grew more \\ slowly to 1989", LOSS),
            (r"the politics", r"rents to fight over, \\ and states that \\ need no taxpayers", CORRUPT),
            (r"the economics", r"a strong currency \\ crowds out other \\ exports: \ the \\ Dutch disease", FEW),
            (r"the caveat", r"measured by reserves, \\ not exports, \ the \\ curse weakens; \\ Norway, \ Botswana",
             GAIN),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"the resource curse", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.CONFLICT_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Natural resources can make conflict worse. <bookmark mark='a'/> In 1995 Jeffrey Sachs and Andrew "
            "Warner found that countries whose exports were mostly natural resources in 1971 grew more slowly over "
            "the next two decades, even with other influences on growth held fixed. <bookmark mark='b'/> The "
            "political reasons: oil and diamonds are rents worth fighting over, and a state that lives on them "
            "needs no taxpayers, so it answers to none. <bookmark mark='c'/> The economic reason, the Dutch "
            "disease: resource exports strengthen the currency and crowd out other exports. <bookmark mark='d'/> "
            "But the curse is not a law. Measured by reserves rather than exports, it weakens, and Norway and "
            "Botswana turned resources into prosperity, through institutions that came first."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
