from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403

XT, YT = 12.0, 18.0     # fish across to 12, coconuts up to 18


def plane(center=LEFT * 3.4 + DOWN * 0.25):
    from explainer.ai.viz import axes

    return axes([0, XT], [0, YT], x_length=5.4, y_length=6.2, xticks=[0, 4, 8, 12], yticks=[0, 4, 8, 12, 16],
                xlabel=r"fish", ylabel=r"coconuts", font_size=19, center=center)


def tag_card(name: str, price: str, kcal: str, per: str, color) -> VGroup:
    box = RoundedRectangle(width=3.6, height=1.85, corner_radius=0.12, stroke_color=color, stroke_width=2.5,
                           fill_color=color, fill_opacity=0.07)
    t = VGroup(label(name, font_size=30, color=color), label(price, font_size=26),
               label(kcal, font_size=23, color=GREY_A), label(per, font_size=23, color=CAL)).arrange(DOWN, buff=0.08)
    t.move_to(box)
    return VGroup(box, t)


class PlayIt(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Play it: \ a week of food on \$21", r"If a staple gets dearer, do you buy less of it?",
             "Chapter one. Play it: a week of food on twenty-one dollars.", lit=("households",),
             horizon=("a day",))
        self.setup_week()
        self.ask()
        self.reveal()

    def lines(self, ax, c_price):
        p = load("playit")
        a = ax.ax
        budget = Line(a.c2p(p["m"] / p["pf"], 0), a.c2p(0, p["m"] / c_price), color=BUDGET if c_price == p["c0"]
                      else NEWB, stroke_width=3.5)
        return budget

    def setup_week(self):
        p = load("playit")
        ax = plane()
        a = ax.ax
        cal = Line(a.c2p(0, p["need"] / p["cs"]), a.c2p(XT, (p["need"] - p["cf"] * XT) / p["cs"]), color=CAL,
                   stroke_width=3.5)
        cal_l = label(r"14{,}000 calories", font_size=19, color=CAL).next_to(a.c2p(10.5, 3.2), UP, buff=0.12)
        budget = self.lines(ax, p["c0"])
        bud_l = label(r"\$21", font_size=21, color=BUDGET).next_to(a.c2p(1.2, 16.0), RIGHT, buff=0.1)
        f0, s0 = p["before"]
        fed = Polygon(a.c2p(0, p["need"] / p["cs"]), a.c2p(0, p["m"] / p["c0"]), a.c2p(f0, s0), stroke_width=0,
                      fill_color=CAL, fill_opacity=0.22)
        fed_l = label(r"affordable \\ and fed", font_size=16, color=CAL).move_to(a.c2p(1.05, 11.1))
        best = Dot(a.c2p(f0, s0), radius=0.11, color=CHOICE)
        best_l = label(rf"{f0:.1f} fish, \ {s0:.1f} coconuts", font_size=20).next_to(best, RIGHT, buff=0.15)
        tags = VGroup(
            tag_card(r"coconut", rf"\${p['c0']:.2f}", r"1{,}400 calories",
                     rf"{p['kcal_per_dollar']['coconut0']:,.0f} calories a dollar".replace(",", "{,}"), COCO),
            tag_card(r"fish", rf"\${p['pf']:.2f}", r"700 calories, \ and taste",
                     rf"{p['kcal_per_dollar']['fish']:.0f} calories a dollar", FISHC),
        ).arrange(RIGHT, buff=0.35).to_edge(RIGHT, buff=0.35).to_edge(UP, buff=0.5)
        rule = VGroup(label(r"a week's food: \ \$21", font_size=30, color=BUDGET),
                      label(r"you must eat 14{,}000 calories, \\ 2{,}000 a day", font_size=28, color=CAL),
                      label(r"you'd rather eat fish; \\ coconuts are the cheap way to be full", font_size=26,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(tags, DOWN, buff=0.45)
        rule.align_to(tags, LEFT)
        best_rule = label(r"so: as much fish as the calories allow", font_size=27, color=E.ACCENT).next_to(
            rule, DOWN, buff=0.4).align_to(rule, LEFT)
        tag = island_tag(r"the Island's poorest households", corner=DR, font_size=15)
        with self.voiceover(
            "A game first. You run a household on the Island, one of its poorest. <bookmark mark='a'/> You have "
            "twenty-one dollars for a week's food, and the household must eat fourteen thousand calories, two "
            "thousand a day, or go hungry. <bookmark mark='b'/> The market sells two foods. A coconut costs one "
            "dollar twenty and brings fourteen hundred calories. A fish costs two dollars and brings seven hundred, "
            "and it tastes far better. Per dollar, coconuts give more than three times as many calories. "
            "<bookmark mark='c'/> Here is the week on the plane of Part five: fish across, coconuts up. The yellow "
            "line is what twenty-one dollars buys. The green line is fourteen thousand calories; bundles above it "
            "keep you fed. <bookmark mark='d'/> So you can choose anything in this green sliver: affordable, and "
            "enough to eat. <bookmark mark='e'/> You'd like as much fish as possible, so you go to the sliver's "
            "far corner, where the money and the calories run out together: about six and a half fish and seven "
            "coconuts."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(ax), FadeIn(rule[0]))
            vo.wait_until("a")
            self.play(FadeIn(rule[1]))
            vo.wait_until("b")
            self.play(FadeIn(tags, shift=DOWN * 0.15), FadeIn(rule[2]))
            vo.wait_until("c")
            self.play(Create(budget), FadeIn(bud_l))
            self.play(Create(cal), FadeIn(cal_l))
            vo.wait_until("d")
            self.play(FadeIn(fed), FadeIn(fed_l))
            vo.wait_until("e")
            self.play(FadeIn(best, scale=1.6), FadeIn(best_l), FadeIn(best_rule))
        self.ax, self.budget, self.cal, self.fed, self.best = ax, budget, cal, fed, best
        self.keep = VGroup(ax, budget, bud_l, cal, cal_l, fed, fed_l, best, best_l, tag)
        self.side = VGroup(tags, rule, best_rule)

    def ask(self):
        p = load("playit")
        a = self.ax.ax
        new = self.lines(self.ax, p["c1"])
        new_l = label(rf"\${p['m']:.0f} at \${p['c1']:.2f}", font_size=19, color=NEWB).next_to(
            a.c2p(p["m"] / p["pf"], 0), UP, buff=0.5).shift(RIGHT * 0.2)
        f1, s1 = p["after"]
        fed1 = Polygon(a.c2p(0, p["need"] / p["cs"]), a.c2p(0, p["m"] / p["c1"]), a.c2p(f1, s1), stroke_width=0,
                       fill_color=CAL, fill_opacity=0.22)
        stage = game_stage(6.3, 5.2, center=RIGHT * 3.45 + DOWN * 0.3)
        q = VGroup(label(r"coconuts go up: \ \$1.20 $\to$ \$1.50", font_size=27, color=NEWB),
                   label(r"fish stay at \$2; \ you still have \$21", font_size=22, color=GREY_A),
                   label(r"next week, \ do you buy \\ \emph{more} coconuts or \emph{fewer}?", font_size=30)).arrange(
            DOWN, buff=0.35)
        q.move_to(stage.box.get_center() + UP * 0.6)
        ring = countdown().next_to(q, DOWN, buff=0.45)
        with self.voiceover(
            "Now the price of coconuts rises, from one dollar twenty to one fifty. Fish stay at two dollars, and "
            "you still have twenty-one. <bookmark mark='a'/> The budget line swings in: you can afford fewer "
            "coconuts than before. <bookmark mark='b'/> Pause the film and decide. Next week, do you buy more "
            "coconuts, or fewer?"
        ) as vo:
            self.play(FadeOut(self.side), FadeIn(stage), FadeIn(q[0]), FadeIn(q[1]))
            vo.wait_until("a")
            self.play(TransformFromCopy(self.budget, new), FadeIn(new_l), Transform(self.fed, fed1))
            vo.wait_until("b")
            self.play(FadeIn(q[2]), FadeIn(ring))
        self.add(ring[1])
        self.play(ring.t.animate.set_value(0.0), run_time=5.0, rate_func=linear)
        self.play(FadeOut(stage), FadeOut(q), FadeOut(ring))
        self.new, self.new_l = new, new_l

    def reveal(self):
        p = load("playit")
        a = self.ax.ax
        f0, s0 = p["before"]
        f1, s1 = p["after"]
        old_cost = s0 * p["c1"] + f0 * p["pf"]
        short = old_cost - p["m"]
        save = p["pf"] - 0.5 * p["c1"]
        best1 = Dot(a.c2p(f1, s1), radius=0.11, color=GIFF)
        move = arrow_between(self.ax, (f0, s0), (f1, s1), GIFF, width=5, buff=0.13)
        res = VGroup(
            label(rf"coconuts \ {s0:.1f} $\to$ {s1:.1f}: \ \emph{{more}}", font_size=34, color=GIFF),
            label(rf"fish \ {f0:.1f} $\to$ {f1:.1f}", font_size=30, color=FISHC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        steps = VGroup(
            label(rf"last week's basket now costs \${old_cost:.2f}: \\ \${short:.2f} more than you have",
                  font_size=25),
            label(rf"drop a fish: \ save \$2, \ lose 700 calories", font_size=25, color=FISHC),
            label(rf"win them back: \ half a coconut, \ \${0.5 * p['c1']:.2f}", font_size=25, color=COCO),
            label(rf"each swap saves \${save:.2f}: \ make {short / save:.2f} of them", font_size=25, color=E.ACCENT),
            label(rf"$\Rightarrow$ \ {short / save:.2f} fewer fish, \ {0.5 * short / save:.2f} more coconuts",
                  font_size=27, color=GIFF),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28)
        moral = label(r"dearer coconuts made you poorer, \\ and poverty pushes you to the cheapest calories",
                      font_size=26, color=E.ACCENT)
        col = VGroup(res, steps, moral).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        col.to_edge(RIGHT, buff=0.45).shift(UP * 0.15)
        if col.width > 6.6:
            col.width = 6.6
        with self.voiceover(
            "Here's what the arithmetic says. <bookmark mark='a'/> You buy more coconuts: from about six point "
            "eight to seven point six, while fish fall from six point four to four point eight. "
            "<bookmark mark='b'/> Why? At the new price, last week's basket costs twenty-three dollars and four "
            "cents: two dollars and four cents more than you have. <bookmark mark='c'/> You must save money "
            "without going hungry. Dropping a fish saves two dollars but loses seven hundred calories, "
            "<bookmark mark='d'/> and winning those calories back takes half a coconut, seventy-five cents even at "
            "the new price. <bookmark mark='e'/> So each swap saves a dollar twenty-five, and you need about one "
            "point six of them: one point six fewer fish, and point eight more coconuts. "
            "<bookmark mark='f'/> The higher price didn't make coconuts more attractive. It made you poorer, and "
            "being poorer pushed you toward the cheapest calories you could find. That is exactly what Marshall "
            "described, and what Hunan's households did."
        ) as vo:
            vo.wait_until("a")
            self.play(GrowArrow(move), FadeIn(best1, scale=1.6), FadeIn(res))
            vo.wait_until("b")
            self.play(FadeIn(steps[0]))
            vo.wait_until("c")
            self.play(FadeIn(steps[1]))
            vo.wait_until("d")
            self.play(FadeIn(steps[2]))
            vo.wait_until("e")
            self.play(FadeIn(steps[3]), FadeIn(steps[4]))
            vo.wait_until("f")
            self.play(FadeIn(moral, shift=UP * 0.1))
        self.clear_scene()
