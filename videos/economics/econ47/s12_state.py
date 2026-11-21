from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403

DEM_COLS = {"Spain": "#F2C14E", "Chile": "#F25F5C", "South Korea": "#7EC8F5", "Poland": "#C9A0FF",
            "Taiwan": "#7FD1B9", "Indonesia": "#E8A0B4", "Ghana": "#C8B273"}


class State(VoiceoverScene):
    def construct(self):
        card(self, 10, r"State capacity and democracy", r"What lets a state act, and does democracy make it richer?",
             "Chapter ten. State capacity and democracy.",
             lit={2009: r"Besley and Persson", 2019: r"Acemoglu, Naidu, Restrepo and Robinson"}, scale=("nation",),
             horizon=("decades",))
        self.capacity()
        self.taxes()
        self.transitions()
        self.growth()

    def capacity(self):
        cards = point_cards([
            (r"fiscal capacity", r"the power to \\ tax: \ registers, \\ withholding, \\ inspectors", AUDIT),
            (r"legal capacity", r"courts and \\ property rights \\ that hold", DEM),
            (r"investments", r"built in advance, \\ by governments \\ that expect to \\ benefit", ELITE),
            (r"what helps", r"common threats, \\ stable politics, \\ inclusive \\ institutions", GAIN),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"Besley and Persson: \ the state as an investment", font_size=30, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        tag = published_tag(tables.STATE_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Most of this part has been about states that do the wrong thing. Timothy Besley and Torsten Persson "
            "asked why many states cannot do much at all. <bookmark mark='a'/> To tax, a state needs registers of "
            "firms and people, withholding at source, inspectors: fiscal capacity. <bookmark mark='b'/> To protect "
            "property and enforce contracts, it needs courts that work: legal capacity. <bookmark mark='c'/> Both "
            "must be built in advance, by governments that will not necessarily be the ones to use them. <bookmark "
            "mark='d'/> So states invest when there is a common interest, such as a war that threatens everyone, "
            "when politics is stable, and when institutions include enough people that whoever rules next will "
            "not turn the capacity against them. The two capacities reinforce each other."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Circumscribe(cards.cards[0], color=WHITE, buff=0.05))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def taxes(self):
        T = load("tax")
        ax = plane([2.8, 5.3], [0, 45], center=LEFT * 1.9 + DOWN * 0.35, x_length=8.0, y_length=4.8,
                   xticks=[3, 4, 5], yticks=[0, 10, 20, 30, 40],
                   xlabel=r"GDP per head, \ 2021 dollars at PPP \ (log scale)",
                   ylabel=r"central government tax revenue, \ \% of GDP",
                   xfmt=lambda v: f"{10 ** v:,.0f}".replace(",", "{,}"), yfmt=lambda v: f"{v:.0f}", font_size=13)
        pts = VGroup(*[dot(ax, x, min(y, 45), AUDIT, 0.045) for x, y in zip(T["x"], T["y"]) if 2.8 <= x <= 5.3])
        fit = seg(ax, 2.9, T["intercept"] + T["slope"] * 2.9, 5.2, T["intercept"] + T["slope"] * 5.2, E.ACCENT, 2.6)
        side = VGroup(
            label(rf"{T['n']} countries, \\ latest year", font_size=18, color=WHITE),
            label(rf"poorest quarter: \\ median {T['median_poorest']:.0f}\% of GDP", font_size=18, color=AUDIT),
            label(rf"richest quarter: \\ median {T['median_richest']:.0f}\%", font_size=18, color=GAIN),
            label(r"central government only: \\ social contributions \\ and local taxes \\ are left out",
                  font_size=17, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"World Bank, \ WDI: \ GC.TAX.TOTL.GD.ZS, \ NY.GDP.PCAP.PP.KD", corner=DL, font_size=12)
        with self.voiceover(
            "One trace of fiscal capacity is how much a state collects. <bookmark mark='a'/> Here is tax revenue "
            f"as a share of GDP for {T['n']} countries, from the World Bank's data, against income. <bookmark "
            f"mark='b'/> In the poorest quarter of countries the median central government collects "
            f"{T['median_poorest']:.0f} percent of GDP; <bookmark mark='c'/> in the richest quarter, "
            f"{T['median_richest']:.0f} percent. <bookmark mark='d'/> These are central government taxes only; "
            "add social insurance contributions and local taxes, and rich countries collect much more. Poor "
            "states cannot tax much of their economies, which are informal and paid in cash, and so cannot pay "
            "for the schools, roads and courts that would make them richer."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.005), FadeIn(side[0]), Create(fit),
                      run_time=2.5)
            for mk, r_ in zip("bcd", side[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def transitions(self):
        D = load("democracy")
        ax = plane([1960, 2026], [0, 1], center=LEFT * 1.7 + DOWN * 0.35, x_length=8.6, y_length=4.6,
                   xticks=[1960, 1970, 1980, 1990, 2000, 2010, 2020], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   ylabel=r"V-Dem's electoral democracy index", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}",
                   font_size=14)
        lines, names = VGroup(), VGroup()
        for c, d in D["democratized"].items():
            ys = [y for y in d["year"] if y >= 1960]
            vs = [v for y, v in zip(d["year"], d["value"]) if y >= 1960]
            col = DEM_COLS[c]
            lines.add(path(ax, ys, vs, col, 2.6, smooth=False))
            names.add(label(rf"{c}, \ {d['transition']}", font_size=14, color=col))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(RIGHT, buff=0.4)
        tag = data_tag(r"V-Dem Institute, \ Democracy Report v16 (2026), \ via Our World in Data", corner=DL,
                       font_size=12)
        with self.voiceover(
            "Does democracy itself make a country richer? <bookmark mark='a'/> Here are seven countries that "
            "became democracies in the last third of the twentieth century, by the V-Dem project's index: Spain "
            "after Franco, Chile after Pinochet, South Korea, Poland, Taiwan, Ghana and Indonesia. <bookmark "
            "mark='b'/> Each jumps within a few years from the bottom of the scale to near the top. Comparing their "
            "incomes before and after is not enough, because countries often democratize in a crisis, and grow "
            "for many other reasons."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.25), FadeIn(names), run_time=4.0)
            vo.wait_until("b")
            self.play(*[Indicate(ln, color=WHITE) for ln in lines])
        self.clear_scene()

    def growth(self):
        T = tables.FRANCHISE_47.data
        rows = VGroup(
            label(r"Acemoglu, \ Naidu, \ Restrepo \\ and Robinson, \ 2019: \\ 175 countries, \ 1960--2010",
                  font_size=19, color=WHITE),
            label(r"compare countries that \\ democratize with similar \\ ones that do not, \ allowing \\ for "
                  r"the slump that \\ often comes first", font_size=19, color=GREY_A),
            label(rf"GDP per head about \\ {T['growth']}\% higher {T['years']} years \\ after a democratization",
                  font_size=21, color=DEM),
            label(r"through investment, \\ schooling, \ public goods, \\ reforms \ and less unrest", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        head = label(r"democracy does cause growth", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        ax = plane([0, 30], [0, 25], center=LEFT * 2.4 + DOWN * 0.4, x_length=6.6, y_length=4.4,
                   xticks=[0, 5, 10, 15, 20, 25, 30], yticks=[0, 5, 10, 15, 20, 25],
                   xlabel=r"years after democratizing",
                   ylabel=r"GDP per head, \ \% above similar countries that did not",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.0f}", font_size=14)
        ts = np.linspace(0, 30, 61)
        g = T["growth"] * (1 - np.exp(-ts / 15.0)) / (1 - np.exp(-T["years"] / 15.0))
        sketch = path(ax, ts, g, DEM, 3.2, smooth=True)
        pin = dot(ax, T["years"], T["growth"], E.ACCENT, 0.09)
        pin_l = label(rf"about {T['growth']}\% after {T['years']} years", font_size=17, color=E.ACCENT).next_to(
            pin, UL, buff=0.1)
        note = label(r"a sketch of the shape: \ gradual, \ not the published estimates year by year",
                     font_size=14, color=GREY_B).next_to(ax, DOWN, buff=0.55)
        tag = published_tag(tables.FRANCHISE_47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Daron Acemoglu, Suresh Naidu, Pascual Restrepo and James Robinson tried to make the comparison fair. "
            "<bookmark mark='a'/> They used a panel of countries from 1960, <bookmark mark='b'/> comparing those "
            "that democratized with similar countries that did not, and allowing for the economic slump that often "
            f"comes just before a transition. <bookmark mark='c'/> They found GDP per head about {T['growth']} "
            f"percent higher {T['years']} years after a democratization, with similar answers from other methods. "
            "<bookmark mark='d'/> Democracies, they argue, invest more, school more of their people, provide more "
            "public goods, reform more, and suffer less unrest. The gains come slowly, which is part of why democracy "
            "is hard to defend in its first years."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1), FadeIn(ax), FadeIn(note))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
                if mk == "c":
                    self.play(Create(sketch), run_time=2.5)
                    self.play(FadeIn(pin), FadeIn(pin_l))
        self.clear_scene()
