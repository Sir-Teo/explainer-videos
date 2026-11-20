from __future__ import annotations

from videos.economics.econ45.common import *  # noqa: F403


def hm(minutes: float) -> str:
    h, m = divmod(int(round(minutes)), 60)
    return f"{h}:{m:02d}"


class Field(VoiceoverScene):
    def construct(self):
        card(self, 4, r"In the field: \ runners, \ golfers, \ sellers", r"Do reference points survive real stakes?",
             "Chapter four. In the field: runners, golfers, sellers.",
             lit={2001: r"Genesove and Mayer", 2011: r"Pope and Schweitzer", 2017: r"Allen et al."},
             scale=("person", "market"), horizon=("a day", "a year"))
        self.marathon()
        self.kink()
        self.golf()
        self.condos()

    def marathon(self):
        M = load("marathon")
        e = np.array(M["edges"])
        h = np.array(M["h"]) / 1000
        mid = (e[:-1] + e[1:]) / 2
        top = float(np.ceil(h.max()))
        ax = plane([150, 390], [0, top], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.4, y_length=4.6,
                   xticks=[180, 210, 240, 270, 300, 330, 360], yticks=[0, top / 2, top],
                   xlabel=r"finishing time, \ hours:minutes", ylabel=r"runners per minute, \ thousands",
                   xfmt=lambda v: hm(v), yfmt=lambda v: f"{v:.1f}", font_size=14)
        bars = VGroup()
        for x, y in zip(mid, h):
            if y <= 0:
                continue
            p0, p1 = ax.ax.c2p(x - 0.5, 0), ax.ax.c2p(x + 0.5, y)
            bars.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0, fill_color=GYM,
                               fill_opacity=0.8).move_to((p0 + p1) / 2))
        marks = VGroup(*[vline(ax, m, 0, top, LOSS, 1.4) for m in (180, 210, 240, 270, 300, 330, 360)])
        side = VGroup(
            label(rf"{M['n'] // 1000:,},000 Island \\ runners", font_size=19, color=WHITE),
            label(r"spikes just under \\ every half hour", font_size=19, color=GYM),
            label(r"and gaps just over", font_size=19, color=LOSS),
            label(r"Allen, \ Dechow, \ Pope \\ and Wu: \ millions of \\ real finishes look \\ the same", font_size=18,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.REFERENCE_FIELD.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Laboratory mugs are cheap. Does reference dependence survive when the stakes are hours of training? "
            f"<bookmark mark='a'/> Here are the finishing times of {M['n'] // 1000:,} thousand marathon runners on "
            "the Island, minute by minute. <bookmark mark='b'/> Look just before each half hour: three hours, three "
            "and a half, four. Too many runners finish there. <bookmark mark='c'/> And just after, too few. "
            "<bookmark mark='d'/> Eric Allen, Patricia Dechow, Devin Pope and George Wu found exactly this shape "
            "in nearly ten million real marathon finishing times: runners bunch just under round numbers, most "
            "visibly under three and four hours. Nothing about running changes at four hours. Only the goal does."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.004), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(marks), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def kink(self):
        M = load("marathon")
        mid = np.array(M["mid240"])
        h = np.array(M["h240"]) / 1000
        cf = np.array(M["cf240"]) / 1000
        top = float(np.ceil(h.max() * 2) / 2)
        ax = plane([215, 265], [0, top], center=LEFT * 2.2 + DOWN * 0.4, x_length=7.2, y_length=4.6,
                   xticks=[220, 230, 240, 250, 260], yticks=[0, top / 2, top], xlabel=r"finishing time",
                   ylabel=r"runners per minute, \ thousands", xfmt=lambda v: hm(v), yfmt=lambda v: f"{v:.1f}",
                   font_size=14)
        bars = VGroup()
        for x, y in zip(mid, h):
            p0, p1 = ax.ax.c2p(x - 0.5, 0), ax.ax.c2p(x + 0.5, y)
            col = GYM if 239 <= x < 240 else (LOSS if 240 <= x < 243 else GREY_B)
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.001), stroke_width=0,
                               fill_color=col, fill_opacity=0.8).move_to((p0 + p1) / 2))
        cfl = path(ax, mid, cf, WHITE, 2.4)
        eq = MathTex(r"\text{effort: } k\,(1 + \eta) \;\text{ below the goal},\quad k\,(1 + \eta\lambda) "
                     r"\;\text{ above it}", font_size=26, color=THEORY).to_edge(UP, buff=0.4)
        side = VGroup(
            label(r"white: \ the smooth \\ counterfactual \\ (Part 41's method)", font_size=18, color=WHITE),
            label(rf"gold: \ {M['excess']['240']:.1f} minutes' worth \\ of extra runners", font_size=18, color=GYM),
            label(rf"red: \ {M['missing']['240']:.1f} minutes' worth \\ missing", font_size=18, color=LOSS),
            label(rf"planted: \ the kink \\ moves {M['extra_minutes']:.1f} minutes \\ of runners onto \\ the goal",
                  font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Why the shape? <bookmark mark='a'/> On the Island each runner chooses effort, which is costly. A "
            "minute saved is worth something, plus a gain-loss term around the goal: below four hours each minute "
            "is a gain, above it each minute is a loss, and losses count lambda times more. So the reward for "
            "speed jumps at the goal: a kink, like the jump in a tax rate in Part forty-one. Runners whose natural "
            "time lies just over the goal push to just under it. <bookmark mark='b'/> Fit a smooth curve to the "
            "histogram away from the goal, as Part forty-one did for taxpayers. <bookmark mark='c'/> The excess "
            f"under four hours is about {M['excess']['240']:.1f} minutes' worth of runners, <bookmark mark='d'/> and "
            f"about as many are missing just over it. <bookmark mark='e'/> The planted kink moves "
            f"{M['extra_minutes']:.1f} minutes' worth of runners onto the goal; the estimator recovers most of it. "
            "The size of the bunch is a measure of how much losses outweigh gains."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(bars), run_time=1.2)
            vo.wait_until("a")
            self.play(Write(eq), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cfl), FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]), *[Indicate(b, color=WHITE) for b, x in zip(bars, mid) if 239 <= x < 240])
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def golf(self):
        G = load("golf")
        cv = G["curve"]
        ax = plane([0, 40], [0, 1], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"length of the putt, \ feet",
                   ylabel=r"share holed", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        par = path(ax, cv["feet"], cv["par"], GAIN, 3.0)
        bird = path(ax, cv["feet"], cv["birdie"], PLAN, 3.0)
        mp = VGroup(vline(ax, G["mean_feet_par"], 0, 1, GAIN, 1.8),
                    label(rf"par putts: \ {G['mean_feet_par']:.0f} feet", font_size=15, color=GAIN).next_to(
                        ax.ax.c2p(G["mean_feet_par"], 0.95), LEFT, buff=0.1))
        mb = VGroup(vline(ax, G["mean_feet_birdie"], 0, 1, PLAN, 1.8),
                    label(rf"birdie putts: \ {G['mean_feet_birdie']:.0f} feet", font_size=15, color=PLAN).next_to(
                        ax.ax.c2p(G["mean_feet_birdie"], 0.95), RIGHT, buff=0.1))
        side = VGroup(
            label(r"green: \ putts for par, \\ to avoid a loss", font_size=18, color=GAIN),
            label(r"blue: \ putts for birdie, \\ for a gain", font_size=18, color=PLAN),
            label(r"longer putts \\ go in less often", font_size=18, color=WHITE),
            label(rf"raw gap: \ {100 * G['raw']:.0f} points, \\ mostly distance", font_size=18, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.33).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.REFERENCE_FIELD.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "Golf has a reference point printed on the card: par. A putt for par avoids a loss; a putt for birdie, "
            "one under par, is a gain. <bookmark mark='a'/> On the Island, the share of putts holed falls steeply "
            "with length, for both kinds. <bookmark mark='b'/> And birdie putts are longer on average, because they "
            "usually follow an approach shot, while a par putt often follows a missed birdie putt or a chip. "
            f"<bookmark mark='c'/> So comparing all par putts with all birdie putts gives a gap of "
            f"{100 * G['raw']:.0f} percentage points, which is mostly distance: the selection problem of Part four, "
            "where the comparison groups differ in more than the thing being studied."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(bird), Create(par), FadeIn(side[0]), FadeIn(side[1]),
                      run_time=1.5)
            vo.wait_until("a")
            self.play(FadeIn(side[2]))
            vo.wait_until("b")
            self.play(FadeIn(mp), FadeIn(mb))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
        self.clear_scene()
        self.golf_gap()

    def golf_gap(self):
        G = load("golf")
        cv = G["curve"]
        gap = np.array(cv["par"]) - np.array(cv["birdie"])
        ax = plane([0, 40], [-0.02, 0.06], center=LEFT * 1.8 + DOWN * 0.4, x_length=8.2, y_length=4.6,
                   xticks=[0, 10, 20, 30, 40], yticks=[-0.02, 0, 0.02, 0.04, 0.06], xlabel=r"length of the putt, \ "
                   r"feet", ylabel=r"par minus birdie, \ share holed", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{100 * v:.0f}", font_size=14)
        zero = seg(ax, 0, 0, 40, 0, GREY_B, 1.4)
        bars = VGroup()
        for x, g in zip(cv["feet"], gap):
            p0, p1 = ax.ax.c2p(x - 0.8, 0), ax.ax.c2p(x + 0.8, float(np.clip(g, -0.02, 0.06)))
            h = p1[1] - p0[1]
            bars.add(Rectangle(width=p1[0] - p0[0], height=max(abs(h), 0.002), stroke_width=0, fill_color=GAIN,
                               fill_opacity=0.8).move_to((p0 + p1) / 2))
        planted = VGroup(seg(ax, 0, G["effect"], 40, G["effect"], E.ACCENT, 2.0, dashed=True),
                         label(rf"planted: \ {100 * G['effect']:.1f} points", font_size=15, color=E.ACCENT).next_to(
                             ax.ax.c2p(40, G["effect"]), UP, buff=0.08).shift(LEFT * 0.8))
        side = VGroup(
            label(r"each bar: \ putts of the \\ same length", font_size=18, color=GAIN),
            label(rf"averaged: \ {100 * G['within']:.1f} points", font_size=19, color=E.ACCENT),
            label(r"Pope and Schweitzer: \\ PGA Tour professionals \\ show the same gap", font_size=17,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.REFERENCE_FIELD.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "So compare putts of the same length. <bookmark mark='a'/> Each bar is the difference between par and "
            "birdie putts within one band of distance. At almost every length, par putts go in a little more often. "
            f"<bookmark mark='b'/> Averaged, the gap is {100 * G['within']:.1f} points, close to the planted "
            f"{100 * G['effect']:.1f}. <bookmark mark='c'/> Devin Pope and Maurice Schweitzer did this with millions "
            "of laser-measured putts on the PGA Tour. Professionals, with large sums at stake and years of practice, "
            "hole par putts about two percentage points more often than birdie putts of the same length: they try "
            "harder to avoid a loss than to secure a gain."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), Create(zero), run_time=1.0)
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.08), FadeIn(side[0]),
                      run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(planted), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
        self.clear_scene()

    def condos(self):
        C = load("condos")
        ax = plane([0, 0.4], [-0.02, 0.14], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.4, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4], yticks=[0, 0.04, 0.08, 0.12],
                   xlabel=r"the owner's nominal loss, \ share of the price paid", ylabel=r"asking price above "
                   r"the flat's value", xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%",
                   font_size=14)
        pts = VGroup(*[dot(ax, x, y, SELL, 0.09) for x, y in zip(C["bin_loss"], C["bin_markup"])])
        truth = seg(ax, 0, 0, 0.4, C["m"] * 0.4, GAIN, 2.4, dashed=True)
        up = seg(ax, 0, 0, 0.2, C["upper"] * 0.2, LOSS, 2.0)
        lo = seg(ax, 0, 0, 0.4, C["lower"] * 0.4, PLAN, 2.0)
        side = VGroup(
            label(r"the Island after a \\ fall in flat prices", font_size=19, color=WHITE),
            label(rf"planted: \ ask {C['m']:.1f} of \\ the loss above value", font_size=18, color=GAIN),
            label(rf"estimate missing unseen \\ quality: \ {C['upper']:.2f} \ (too high)", font_size=18, color=LOSS),
            label(rf"controlling for the \\ last sale's residual: \\ {C['lower']:.2f} \ (too low)", font_size=18,
                  color=PLAN),
            label(rf"losers wait {C['weeks_losers']:.0f} weeks \\ to sell; \ others {C['weeks_gainers']:.0f}",
                  font_size=18, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = published_tag(tables.REFERENCE_FIELD.tag + r"; \ the Island", corner=DR, font_size=11)
        with self.voiceover(
            "The last test has the largest stakes: selling a home. After flat prices fall, many owners face a "
            "loss against the price they paid. <bookmark mark='a'/> On the Island, a loss-averse owner asks the "
            f"flat's value plus {C['m']:.1f} of the nominal loss. Each dot is a group of owners, by the size of "
            "their loss. <bookmark mark='b'/> The econometrician never sees a flat's value, only its features, and "
            "a flat that is better than its features is both bought for more, which looks like a bigger loss, and "
            f"listed for more. Ignore that, and the estimate is {C['upper']:.2f}: too high. "
            "<bookmark mark='c'/> Control for how far the last sale price stood above the features' value, and the "
            f"estimate falls to {C['lower']:.2f}: too low, because that residual also contains the owner's luck "
            "when buying. The two estimates bracket the truth. <bookmark mark='d'/> And the owners with losses, "
            f"asking more, wait {C['weeks_losers']:.0f} weeks to sell instead of {C['weeks_gainers']:.0f}. David "
            "Genesove and Christopher Mayer found this in downtown Boston's condominium market from 1990 to 1997: "
            "owners facing a nominal loss asked more, by a quarter to a third of the gap between the expected price "
            "and the price they had paid, got more, and sold more slowly."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), LaggedStart(*[FadeIn(p) for p in pts],
                                                                             lag_ratio=0.2), run_time=1.5)
            vo.wait_until("a")
            self.play(Create(truth), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(up), FadeIn(side[2]))
            vo.wait_until("c")
            self.play(Create(lo), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()
