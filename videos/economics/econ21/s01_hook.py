from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.lamps()
        self.unrecorded()
        self.question()
        self.romer()
        self.title()
        self.objectives()

    def lamps(self):
        l_ = load("light")
        rows = [r for r in l_["rows"] if r["device"] in ("open fire", "Neolithic lamp", "Babylonian lamp")
                or (r["device"] == "candle" and r["tech"] == "tallow" and r["year"] == 1800)]
        bars = VGroup()
        top = max(r["hours"] for r in rows)
        for i, r in enumerate(rows):
            w = 7.0 * r["hours"] / top
            y = 1.2 - i * 1.0
            bar = Rectangle(width=w, height=0.55, stroke_width=0, fill_color=LIGHT, fill_opacity=0.85).move_to(
                [-2.6 + w / 2, y, 0])
            name = label(rf"{r['device']}, \ {r['tech']}", font_size=20, color=GREY_A).next_to(bar, LEFT, buff=0.25)
            name.align_to([-2.85, 0, 0], RIGHT)
            when = label(r["printed"].replace("-", "--").replace("B.C.", "BC"), font_size=17,
                         color=GREY_B).next_to(name, DOWN, buff=0.05).align_to(name, RIGHT)
            val = label(rf"{r['hours']:g} hours", font_size=20, color=LIGHT).next_to(bar, RIGHT, buff=0.15)
            bars.add(VGroup(bar, name, when, val))
        head = label(r"hours of work to buy 1{,}000 lumen-hours of light \ (about an hour of a 75-watt bulb)",
                     font_size=22, color=GREY_A).to_edge(UP, buff=0.5)
        tag = published_tag(tables.NORDHAUS_LIGHT.tag + r"; \ " + r"in Bresnahan and Gordon (eds), \emph{The "
                            r"Economics of New Goods}", corner=DR, font_size=12)
        with self.voiceover(
            "In the early 1990s the economist William Nordhaus set out to measure something no statistical agency "
            "had ever recorded: the price of light. Not the price of candles or of bulbs, but of light itself, "
            "measured in lumen-hours, and paid for in hours of work. <bookmark mark='a'/> To make a thousand "
            "lumen-hours, about an hour of light from an ordinary 75-watt bulb, a family round an open fire had to "
            "gather wood for about fifty-eight hours. <bookmark mark='b'/> A Neolithic lamp burning animal fat cost "
            "about fifty. <bookmark mark='c'/> A Babylonian lamp burning sesame oil, around 1750 BC, about "
            f"{l_['babylon']:.1f}. <bookmark mark='d'/> And in 1800, a tallow candle, {l_['tallow_1800']:.2f} hours "
            "of work. Three and a half thousand years of progress had made light about eight times cheaper."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), *[FadeIn(b_[1]) for b_ in bars], *[FadeIn(b_[2]) for b_ in bars])
            for mk, b_ in zip("abcd", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b_[0], LEFT), FadeIn(b_[3]))
        self.clear_scene()

    def unrecorded(self):
        l_ = load("light")
        rows = VGroup(
            label(r"price indexes followed candles, \ lamp oil, \ gas, \ bulbs: \ the goods, \ not the light", font_size=25,
                  color=GREY_A),
            label(r"each new technology entered the index late, \ and its fall was missed", font_size=25,
                  color=LIGHT),
            label(rf"Nordhaus: \ since 1800 the traditional indexes overstated the price of light \\ by a factor of "
                  rf"900 to 1{{,}}600 \ ({100 * l_['bias']:.1f}\% a year)", font_size=25, color=WEDGE),
            label(r"so real wages and real output were understated too", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(tables.NORDHAUS_LIGHT.tag + r", \ section 1.5", corner=DR, font_size=12)
        with self.voiceover(
            "What happened next is the subject of this part's game, so hold it for a moment. Here is why Nordhaus "
            "bothered. <bookmark mark='a'/> The price indexes in the national accounts followed the things people "
            "bought: candles, lamp oil, gas, bulbs. <bookmark mark='b'/> Each new way of making light entered the "
            "index late, and the fall in the price of light that it brought was missed. "
            "<bookmark mark='c'/> Nordhaus calculated that between 1800 and the 1990s the traditional indexes "
            "overstated the rise in the price of light by a factor of nine hundred to sixteen hundred, about "
            f"{100 * l_['bias']:.1f} percent a year. <bookmark mark='d'/> If light is typical of new goods, real "
            "wages and real output have grown much faster than the statistics say. And the source of that growth was "
            "not more capital. It was better ideas about how to make light."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(rows[0], shift=UP * 0.1))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"what is an idea, \ economically, \ and why does it change growth theory?", font_size=27,
                  color=IDEA),
            label(r"why do some countries use the world's ideas so much better than others?", font_size=27,
                  color=WEDGE),
            label(r"and do institutions, \ geography or culture decide it?", font_size=27, color=INST),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "Part twenty ended with a residual: half of American growth, and most of the gap between rich and poor "
            "countries, unexplained by capital and schooling. This part's question: where does the growth that "
            "capital cannot explain come from? <bookmark mark='a'/> What is an idea, economically, and why does it "
            "change growth theory? <bookmark mark='b'/> Why do some countries use the world's ideas so much better "
            "than others? <bookmark mark='c'/> And what decides it: institutions, geography or culture?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()

    def romer(self):
        hc = history_card(1990, r"Paul Romer", r"\emph{Endogenous Technological Change}, \ Journal of Political "
                          r"Economy", color=IDEA, width=11.0, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"a lamp can light one room at a time", font_size=30, color=LIGHT),
            label(r"the idea of a lamp can be used by everyone at once", font_size=30, color=IDEA),
            label(r"growth theory built on that difference: \ Nobel prize, \ 2018", font_size=24, color=GREY_A),
        ).arrange(DOWN, buff=0.45).next_to(hc, DOWN, buff=0.7)
        tag = published_tag(r"Romer, JPE 98(5) (1990): \ S71--S102", corner=DR, font_size=12)
        with self.voiceover(
            "The theory starts from one observation. <bookmark mark='a'/> A lamp can light one room at a time. "
            "<bookmark mark='b'/> The idea of a lamp, its design, can be used by everyone at once, and using it does "
            "not use it up. <bookmark mark='c'/> In 1990 Paul Romer built a theory of growth on that difference, "
            "and in 2018 he shared the Nobel prize for it, with William Nordhaus."
        ) as vo:
            self.play(FadeIn(hc, shift=UP * 0.2), FadeIn(tag))
            for mk, r in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def title(self):
        l_ = load("light")
        mini = plane([1800, 1995], [np.log10(0.0001), np.log10(10)], x_length=4.2, y_length=1.6)
        logo = VGroup(log_path(mini, l_["frontier_years"], l_["frontier"], LIGHT, width=4))
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 21 \ $\cdot$ \ Growth II: \ Ideas and Institutions", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part twenty-one: growth, part two. Ideas and institutions."):
            self.play(Create(logo), run_time=1.4)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act V \ $\cdot$ \ The Long Run", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"the price of light; \ rival and non-rival goods; \ why ideas bring increasing returns",
            r"AK and learning by doing; \ Romer's economy derived; \ creative destruction",
            r"are ideas getting harder to find? \ diffusion; \ misallocation",
            r"institutions, \ borders as experiments, \ geography, \ disease and culture",
            r"directed technical change; \ patents; \ a dial on research; \ fewer people",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "This part continues Act Five. <bookmark mark='a'/> You'll see what happened to the price of light, "
            "and why ideas, unlike lamps, bring increasing returns. <bookmark mark='b'/> You'll meet growth that "
            "never ends, derive Romer's economy, and watch creative destruction on a quality ladder. "
            "<bookmark mark='c'/> You'll ask whether ideas are getting harder to find, why they cross borders "
            "slowly, and how much output is lost when capital and workers sit in the wrong firms. "
            "<bookmark mark='d'/> Then institutions, borders that act as experiments, and the rival claims of "
            "geography, disease and culture. <bookmark mark='e'/> And the direction of technical change, patents "
            "and prizes, a dial on the return to research, and what happens to growth when populations shrink."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
        self.clear_scene()
