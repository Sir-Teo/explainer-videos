from __future__ import annotations

from videos.economics.econ48.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.wager()
        self.prices()
        self.question()
        self.title()
        self.objectives()

    def wager(self):
        T = tables.BET_1980.data
        chain = flow_chain([(r"1980: \ Ehrlich \\ picks five metals", METAL), (r"Simon bets their \\ prices will fall",
                                                                              GAIN),
                            (r"1990: \ all five \\ are cheaper", GAIN), (r"Ehrlich mails \\ a cheque", LOSS)],
                           notes=[r"chromium, \ copper, \\ nickel, \ tin, \ tungsten", rf"\${T['each']} of each, \\ "
                                  rf"\${T['stake']:,} in all".replace(",", "{,}"), r"after inflation",
                                  rf"for \${T['cheque']:.2f}"], box_w=2.8, font_size=20, note_size=17)
        chain.move_to(UP * 1.2)
        sides = VGroup(
            VGroup(label(r"Paul Ehrlich, \ biologist", font_size=22, color=LOSS),
                   label(r"more people, \ fixed resources: \\ scarcity, \ so prices rise", font_size=19,
                         color=GREY_A)).arrange(DOWN, buff=0.12),
            VGroup(label(r"Julian Simon, \ economist", font_size=22, color=GAIN),
                   label(r"scarcity raises prices, \\ which call forth substitutes, \\ discovery, \ invention",
                         font_size=19, color=GREY_A)).arrange(DOWN, buff=0.12),
        ).arrange(RIGHT, buff=2.2).move_to(DOWN * 1.9)
        tag = published_tag(tables.BET_1980.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 1980 the economist Julian Simon offered anyone a bet. Pick any raw materials you like; if their "
            "prices, after inflation, are higher in ten years' time, I pay; if lower, you pay. <bookmark mark='z'/> "
            "The biologist Paul Ehrlich, who had warned that a growing population would run the world short of food "
            "and materials, took it, with two colleagues. "
            "<bookmark mark='a'/> Ehrlich chose five metals: chromium, copper, nickel, tin and tungsten. "
            f"<bookmark mark='b'/> On paper he bought {T['each']} dollars' worth of each, {T['stake']:,} dollars in "
            "all. <bookmark mark='c'/> On the twenty-ninth of September 1990 the bet was settled. All five metals were "
            "cheaper in real terms. <bookmark mark='d'/> In October Ehrlich mailed Simon a cheque for "
            "five hundred and seventy-six dollars and seven cents. <bookmark mark='e'/> Behind the bet were two "
            "views of scarcity. Ehrlich's: more people and fixed resources, so prices must rise. <bookmark mark='f'/> "
            "Simon's: scarcity raises prices, and high prices call forth substitutes, discovery and invention, which "
            "push them down again."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(sides[1], shift=UP * 0.1), run_time=1.0)
            vo.wait_until("z")
            self.play(FadeIn(sides[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(FadeIn(chain.boxes[0]), FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(Indicate(sides[0], color=WHITE, scale_factor=1.05))
            vo.wait_until("f")
            self.play(Indicate(sides[1], color=WHITE, scale_factor=1.05))
        self.clear_scene()

    def prices(self):
        M = load("metals")
        yr = np.array(M["year"])
        i80 = int(np.where(yr == 1980)[0][0])
        keep = (yr >= 1970) & (yr <= 2000)
        ax = plane([1970, 2000], [0, 260], center=LEFT * 1.8 + DOWN * 0.35, x_length=8.2, y_length=4.6,
                   xticks=[1970, 1980, 1990, 2000], yticks=[0, 50, 100, 150, 200, 250],
                   ylabel=r"real price, \ 1980 = 100", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        win = shade(ax, [(1980, 1990)], 0, 260, color=RECESS, opacity=0.6)
        lines = VGroup()
        for k, col in (("copper", COPPER), ("nickel", NICKEL), ("tin", TIN)):
            v = np.array(M["index"][k])
            v = 100 * v / v[i80]
            lines.add(path(ax, yr[keep], v[keep], col, 3.0, smooth=False))
        hundred = DashedLine(ax.ax.c2p(1970, 100), ax.ax.c2p(2000, 100), color=GREY_B, stroke_width=1.4)
        ch = M["change_8090"]
        side = VGroup(
            label(r"three of the five metals \\ the World Bank prices", font_size=18, color=WHITE),
            label(rf"copper: \ {100 * ch['copper']:+.0f}\%".replace("-", "{-}"), font_size=19, color=COPPER),
            label(rf"nickel: \ {100 * ch['nickel']:+.0f}\%".replace("-", "{-}"), font_size=19, color=NICKEL),
            label(rf"tin: \ {100 * ch['tin']:+.0f}\%".replace("-", "{-}"), font_size=19, color=TIN),
            label(rf"the bundle, \ 1980--90: \\ {100 * M['bundle_8090']:+.0f}\%".replace("-", "{-}"), font_size=21,
                  color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"World Bank, \ Commodity Price Data (the Pink Sheet); \ US CPI (BLS via FRED)", corner=DL,
                       font_size=12)
        with self.voiceover(
            "Here are three of Ehrlich's metals, the ones the World Bank prices, from its monthly price data, "
            "deflated by America's consumer prices. <bookmark mark='a'/> The grey band is the decade of the bet. "
            f"<bookmark mark='b'/> Copper fell {100 * abs(ch['copper']):.0f} percent in real terms, nickel "
            f"{100 * abs(ch['nickel']):.0f}, <bookmark mark='c'/> and tin, whose producers' cartel collapsed in "
            f"1985, {100 * abs(ch['tin']):.0f}. An equal bundle of the three lost "
            f"{100 * abs(M['bundle_8090']):.0f} percent. <bookmark mark='d'/> Simon won. But look at the years before "
            "1980 and after 1990: the same prices rose as often as they fell. Chapters one and two ask whether Simon "
            "was right, or lucky."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(win), Create(hundred), FadeIn(side[0]), run_time=1.0)
            self.play(*[Create(ln) for ln in lines], run_time=3.0)
            vo.wait_until("a")
            self.play(Indicate(win, color=WHITE, scale_factor=1.0))
            vo.wait_until("b")
            self.play(FadeIn(side[1]), FadeIn(side[2]), Indicate(lines[0], color=WHITE),
                      Indicate(lines[1], color=WHITE))
            vo.wait_until("c")
            self.play(FadeIn(side[3]), FadeIn(side[4]), Indicate(lines[2], color=WHITE))
            vo.wait_until("d")
            self.play(Indicate(side[4], color=WHITE))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 34, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"are we running out of things, \ and what do prices say?", font_size=26, color=METAL),
            label(r"why are fish and the air used up, \ and what stops it?", font_size=26, color=FISH),
            label(r"what does warming cost, \ and how should the future be weighed?", font_size=26, color=HEAT),
            label(r"which policies work: \ taxes, \ permits, \ clubs, \ new technology?", font_size=26,
                  color=POLICY),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.42).next_to(q, DOWN, buff=0.6)
        with self.voiceover(
            "Simon's argument works for metals, because metals have prices. This part is about the things that do "
            "not. Its question: what is a tonne of carbon dioxide worth, and what does the answer turn on? "
            "<bookmark mark='a'/> Are we running out of things, and what do prices tell us? <bookmark mark='b'/> Why "
            "are fish and the air used up, when metals are not? <bookmark mark='c'/> What does warming cost, and how "
            "should the future be weighed against the present? <bookmark mark='d'/> And which policies work: taxes, "
            "permits, clubs of countries, new technology?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        F = load("film")
        mini = plane([1850, 2025], [0, 1], x_length=4.2, y_length=1.4)
        v = np.array(F["v"])
        v = (v - v.min()) / (v.max() - v.min())
        logo = path(mini, F["t"], v, HEAT, 2.6, smooth=False)
        tt = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 48 \ $\cdot$ \ Environment and Climate", font_size=34, color=E.ACCENT)
        VGroup(logo, tt, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part forty-eight: environment and climate."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(tt), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act IX \ $\cdot$ \ The Fields", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"exhaustible resources and Hotelling's rule; \ the bet, \ rerun; \ the fishery",
            r"the climate in four equations, \ fitted to the record; \ a climate-economy model, \ built",
            r"the social cost of carbon, \ your discount rate, \ and fat tails",
            r"taxes, \ permits, \ clubs, \ learning curves; \ damages measured; \ electricity",
            r"three dials; \ the people who use this; \ the frontier",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> Resources that run out and the rule for their prices; the bet, "
            "rerun for every decade; and the fishery, a resource that renews itself but is overused anyway. "
            "<bookmark mark='b'/> The climate in four equations, fitted to the record of the air and the "
            "thermometers, and a climate-economy model built on it. <bookmark mark='c'/> The social cost of carbon, "
            "with the discount rate chosen by you, and the problem of fat tails. <bookmark mark='d'/> Taxes, permits, "
            "clubs of countries and learning curves; damages measured from the data; and the markets for "
            "electricity. <bookmark mark='e'/> Three dials, the people who use these ideas, and the frontier."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
