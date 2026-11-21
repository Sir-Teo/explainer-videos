from __future__ import annotations

from videos.economics.econ49.common import *  # noqa: F403

LOW_COLS = {"South Korea": "#C9A0FF", "China": "#F25F5C", "Japan": "#7FD1B9", "United States": "#7EC8F5"}


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ fertility and the marriage market", r"What is still being worked out?",
             "Chapter sixteen. Frontier: fertility and the marriage market.",
             lit={2011: r"Wei and Zhang", 2023: r"Doepke et al."}, scale=("household", "nation"),
             horizon=("a decade", "a century"))
        self.lowest()
        self.new_era()
        self.sex_ratio()

    def lowest(self):
        F = load("fertility")
        ax = plane([1990, 2025], [0, 3.0], center=LEFT * 2.0 + DOWN * 0.35, x_length=7.8, y_length=4.4,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0],
                   ylabel=r"children per woman", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", font_size=14)
        rep = DashedLine(ax.ax.c2p(1990, 2.1), ax.ax.c2p(2025, 2.1), color=GREY_B, stroke_width=1.4)
        lines = VGroup()
        for e, col in LOW_COLS.items():
            d = F["series"][e]
            yy = [y for y in d["year"] if y >= 1990]
            vv = [v for y, v in zip(d["year"], d["value"]) if y >= 1990]
            lines.add(path(ax, yy, vv, col, 3.2, smooth=False))
        keys = VGroup(*[label(e, font_size=15, color=c) for e, c in LOW_COLS.items()]).arrange(DOWN, aligned_edge=LEFT,
                                                                                            buff=0.12)
        side = VGroup(
            keys,
            label(rf"South Korea, \ {F['last_year']}: \\ {F['korea_last']:.2f} \ (a generation \\ shrinks by "
                  rf"{100 * (1 - F['korea_last'] / 2.1):.0f}\% \\ in each turn)", font_size=17,
                  color=LOW_COLS["South Korea"]),
            label(r"subsidies for births \\ have moved it little", font_size=17, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"UN World Population Prospects, \ via Our World in Data", corner=DL, font_size=12)
        with self.voiceover(
            "The first open question is how low fertility will go, and why. <bookmark mark='a'/> Since 1990, "
            "children per woman in four large economies. Becker's model predicts a fall as women's time grows "
            "dearer, <bookmark mark='b'/> but not this: South Korea, at "
            f"{F['korea_last']:.2f} children per woman in {F['last_year']}, where each generation is about "
            f"{100 * (1 - F['korea_last'] / 2.1):.0f} percent smaller than the one before. <bookmark mark='c'/> "
            "Governments in East Asia and Europe now pay for births, with limited success. Why the fall is so deep "
            "in some rich countries and not others is one of the field's live questions."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(rep), FadeIn(keys), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(ln) for ln in lines[1:]], lag_ratio=0.3), run_time=3.0)
            vo.wait_until("b")
            self.play(Create(lines[0]), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def new_era(self):
        cards = point_cards([
            (r"the old pattern", r"across rich countries \\ in 1980: \ more women \\ at work, \ fewer \\ children",
             HOLD),
            (r"the new one", r"now: \ more women \\ at work, \ more \\ children", GAIN),
            (r"what changed", r"childcare, \ fathers \\ who share the work, \\ flexible jobs, \\ norms", CHILD),
            (r"the open question", r"which of these \\ policy can move, \\ and how much", E.ACCENT),
        ], width=12.8, cols=4, font_size=18).move_to(DOWN * 0.2)
        head = label(r"fertility and work: \ a new era", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.6)
        tag = published_tag(tables.FRONTIER49.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The second is a reversal. <bookmark mark='a'/> In 1980, across rich countries, the more women worked, "
            "the fewer children were born, as Becker's model of the price of time predicts. <bookmark mark='b'/> "
            "Today the relation runs the other way: the rich countries where more women work have more children. "
            "<bookmark mark='c'/> Matthias Doepke, Anne Hannusch, Fabian Kindermann and Michèle Tertilt argue that "
            "what now matters is whether work and children can be combined: childcare, fathers who share the work "
            "at home, flexible jobs, and the norms that govern all three. <bookmark mark='d'/> How much of that "
            "policy can change, and how fast, is open."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(cards.cards[0], shift=UP * 0.1))
            vo.wait_until("a")
            self.play(Indicate(cards.cards[0], color=WHITE, scale_factor=1.04))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()

    def sex_ratio(self):
        T = tables.FRONTIER49.data
        M = load("marriage")
        chain = flow_chain([(r"more boys \\ than girls born", MEN), (r"a harder marriage \\ market for sons", WOMEN),
                            (r"parents of sons \\ save to compete", CHILD), (r"China's household \\ saving rises",
                                                                           GAIN)],
                           notes=[r"preference for sons, \\ one-child policy", r"chapter five's \\ more-men case",
                                  r"a house, \ wealth: \\ a better match", rf"about {T['saving_share']}\% of the \\ "
                                  r"rise, 1990--2007"], box_w=2.9, font_size=19, note_size=17).move_to(UP * 1.2)
        isl = label(rf"the Island, \ a fifth more men: \ married men {100 * M['eq']['married_share_men']:.0f}\% "
                    rf"$\to$ {100 * M['more_men']['married_share_men']:.0f}\%", font_size=21,
                    color=MEN).move_to(DOWN * 1.4)
        foot = label(r"the marriage market reaches into the national accounts", font_size=24,
                     color=E.ACCENT).next_to(isl, DOWN, buff=0.4)
        tag = published_tag(r"Wei and Zhang, \ JPE (2011)", corner=DR, font_size=11)
        with self.voiceover(
            "The third joins the family to the whole economy. <bookmark mark='a'/> Where parents preferred sons, "
            "and could choose, more boys than girls were born; in China the one-child policy sharpened it. "
            "<bookmark mark='b'/> A generation later, young men outnumber young women, and, as in chapter five's "
            "Island with more men, many will not marry. <bookmark mark='c'/> Shang-Jin Wei and Xiaobo Zhang found "
            "that parents of sons save more to improve their sons' chances, with a house or wealth, and that "
            "families without sons save more too, to keep up. <bookmark mark='d'/> They estimate this can explain "
            f"about {T['saving_share']} percent of the rise in China's household saving from 1990 to 2007. "
            "<bookmark mark='e'/> On the Island, a fifth more men cuts the share of men who marry from "
            f"{100 * M['eq']['married_share_men']:.0f} to {100 * M['more_men']['married_share_men']:.0f} percent. "
            "<bookmark mark='f'/> Becker's marriage market, it turns out, reaches into the national accounts and "
            "the world's trade balances."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]), Indicate(chain.boxes[0], color=WHITE, scale_factor=1.04))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            vo.wait_until("e")
            self.play(FadeIn(isl, shift=UP * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(foot, shift=UP * 0.1))
        self.clear_scene()
