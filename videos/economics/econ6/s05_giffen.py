from __future__ import annotations

from videos.economics.econ6.common import *  # noqa: F403


class Giffen(VoiceoverScene):
    def construct(self):
        card(self, 4, r"When demand slopes up: \ Giffen behaviour", r"Who buys more of a good when it gets dearer, "
             r"and how would you ever know?", "Chapter four. When demand slopes up: Giffen behaviour.")
        self.legend()
        self.zones()
        self.experiment()
        self.hunan()
        self.island()

    def legend(self):
        c1 = history_card(r"1895", r"Marshall, citing Sir Robert Giffen",
                          r"the poorest labourers eat more bread when bread is dearer; no data, no reference",
                          color=GIFF, width=4.2, font_size=21)
        c2 = history_card(r"1947", r"George Stigler looks for Giffen's claim",
                          r"and cannot find it anywhere in Giffen's writings; Britain's bread and wheat were not Giffen either",
                          color=GREY_B, width=4.2, font_size=21)
        c3 = history_card(r"1999", r"Sherwin Rosen, ``Potato Paradoxes''",
                          r"the textbook example, potatoes in the Irish famine, fails: the blight destroyed the crop, "
                          r"so the Irish could not have eaten more", color=GREY_B, width=4.2, font_size=21)
        cards = VGroup(c1, c2, c3).arrange(RIGHT, buff=0.3, aligned_edge=UP).move_to(UP * 0.3)
        foot = label(r"a market's price and quantity can't both rise after a harvest fails: \ look at households, "
                     r"\ and change the price yourself", font_size=24, color=E.ACCENT).to_edge(DOWN, buff=0.6)
        head = label(r"A hundred years without a Giffen good", font_size=34).to_edge(UP, buff=0.45)
        tag = published_tag(r"Stigler, JPE (1947); Rosen, JPE (1999); as discussed by Jensen and Miller (2008)",
                            corner=DR, font_size=13)
        with self.voiceover(
            "First, the history of a rumour. <bookmark mark='a'/> Marshall gave Giffen as his source in 1895, but "
            "no reference and no numbers. <bookmark mark='b'/> In 1947 George Stigler went looking for the claim in "
            "Giffen's writings and couldn't find it; and the evidence on bread and wheat in Britain didn't show "
            "demand sloping up. <bookmark mark='c'/> The example in most textbooks became the potato in the "
            "Irish famine of the eighteen-forties. In 1999 Sherwin Rosen argued that it couldn't be right: the price "
            "of potatoes rose because blight destroyed the crop, so the Irish could not have eaten more potatoes, "
            "whatever they wanted. <bookmark mark='d'/> That's the deeper problem. In a whole market, price and "
            "quantity move together for many reasons; Part four's identification problem again. To see a demand "
            "curve slope up, you need households, and a price that someone changes on purpose."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c_ in zip("abc", cards):
                vo.wait_until(mk)
                self.play(FadeIn(c_, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def zones(self):
        d = load("diet")
        from explainer.ai.viz import axes

        ps, s = np.array(d["ps"]), np.array(d["s"])
        zones = d["zones"]
        dax = axes([0, 12], [0.4, 2.4], x_length=6.0, y_length=5.4, xticks=[0, 2, 4, 6, 8, 10, 12],
                   yticks=[0.5, 1.0, 1.5, 2.0], xlabel=r"coconuts bought a week", ylabel=r"price of a coconut (\$)",
                   font_size=18, yfmt=lambda v: f"{v:.1f}", center=LEFT * 2.8 + DOWN * 0.3)
        a = dax.ax
        segs = VGroup()
        for zname in ("standard", "subsistence", "deprived"):
            idx = [i for i, z in enumerate(zones) if z == zname]
            pts = [a.c2p(s[i], ps[i]) for i in idx if s[i] <= 12]
            segs.add(VMobject(stroke_color=ZONE[zname], stroke_width=5).set_points_as_corners(pts))
        # where the zones meet, at $21 a week
        p_lo = float(ps[[i for i, z in enumerate(zones) if z == "subsistence"][0]])
        p_hi = float(ps[[i for i, z in enumerate(zones) if z == "subsistence"][-1]])
        names = VGroup(
            label(r"standard: \ calories to spare; \\ demand slopes down", font_size=25, color=IC),
            label(r"subsistence: \ the calorie line binds; \\ demand slopes \emph{up}", font_size=25, color=GIFF),
            label(r"deprived: \ every dollar on coconuts; \\ demand slopes down again", font_size=25, color=GREY_B),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.5).shift(UP * 1.0)
        marks = VGroup(
            DashedLine(a.c2p(0, p_lo), a.c2p(12, p_lo), color=GREY_D, stroke_width=1.5),
            DashedLine(a.c2p(0, p_hi), a.c2p(12, p_hi), color=GREY_D, stroke_width=1.5))
        rule = VGroup(label(rf"middle zone: \ $\varepsilon = \dfrac{{r}}{{1-r}} = {d['giffen']:.2f}$ \ at \$1.20",
                            font_size=26, color=GIFF),
                      label(r"$r$: \ fish calories per dollar \\ over coconut calories per dollar", font_size=22,
                            color=GREY_A)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        rule.next_to(names, DOWN, buff=0.45).align_to(names, LEFT)
        hh = label(r"the Play-it household, \$21 a week", font_size=22, color=GREY_A).next_to(dax, UP, buff=0.1)
        tag = agora_tag(r"computed: Agora's subsistence diet", corner=DR, font_size=14)
        with self.voiceover(
            "Theory first, with the household from Play it. Hold its twenty-one dollars fixed and let the price of "
            "coconuts run from very cheap to very dear. <bookmark mark='a'/> When coconuts are cheap, the household "
            "eats enough with money to spare, chooses by taste, and its demand slopes down like anyone's. "
            f"<bookmark mark='b'/> Past about {money_words(p_lo)}, the calorie line starts to bind, and the household is "
            "pinned where money and calories run out together. From there, every rise in the price of coconuts "
            f"means fewer fish and more coconuts: demand slopes up. <bookmark mark='c'/> Past {money_words(p_hi)} "
            "the household has no fish left to give up; it spends everything on coconuts, "
            "and a higher price can only mean fewer. <bookmark mark='d'/> In the middle zone the elasticity has a "
            "simple form. It depends only on how many calories a dollar buys in each food: the fewer the fish give "
            "relative to coconuts, the stronger the effect. At a dollar twenty it's nought point four three. "
            "Jensen and Miller's own figures make the same point: in Hunan a yuan bought fourteen hundred calories "
            "of rice and three hundred and thirty of pork."
        ) as vo:
            self.play(FadeIn(dax), FadeIn(hh), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(segs[0]), FadeIn(names[0]))
            vo.wait_until("b")
            self.play(Create(segs[1]), FadeIn(names[1]), FadeIn(marks[0]))
            vo.wait_until("c")
            self.play(Create(segs[2]), FadeIn(names[2]), FadeIn(marks[1]))
            vo.wait_until("d")
            self.play(FadeIn(rule))
        self.clear_scene()

    def experiment(self):
        t = tables.JENSEN_MILLER_2008.data
        flow = flow_chain([(r"April: \ survey 1, \ no vouchers", GREY_A),
                           (r"June--Oct: \ vouchers \\ (Sept: survey 2)", GIFF),
                           (r"December: \ survey 3, \ vouchers gone", GREY_A)], box_w=3.7, box_h=1.2, buff=0.55,
                          font_size=22).to_edge(UP, buff=0.7)
        reg = MathTex(r"\%\Delta\,\text{rice}_{it} = \beta\;\%\Delta\,\text{price}_{it} + "
                      r"\text{county}\times\text{round} + \cdots", font_size=36).next_to(flow, DOWN, buff=0.6)
        notes = VGroup(
            label(r"each household gives two changes: \ the price falls, \ then returns", font_size=24),
            label(r"$\beta$: \ the price elasticity; \ Giffen if $\beta > 0$", font_size=24, color=GIFF),
            label(r"the theory says: \ look among the poor, \ but not the poorest", font_size=24, color=E.ACCENT),
            label(r"their sorting variable: \ the share of calories from rice before the vouchers", font_size=24,
                  color=COCO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).next_to(reg, DOWN, buff=0.55)
        tag = published_tag(r"Jensen and Miller, AER (2008), section III", corner=DR, font_size=14)
        with self.voiceover(
            "That's the theory Jensen and Miller took to Hunan and Gansu. <bookmark mark='a'/> They surveyed every "
            "household three times: in April, before anyone knew about vouchers; in September, after three months "
            "with them; and in December, after they had ended. <bookmark mark='b'/> For each household, two changes "
            "in its rice consumption, matched with two changes in its price, and compared only with other "
            "households in the same town at the same time. The coefficient is the price elasticity, and it is "
            "positive if demand slopes up. <bookmark mark='c'/> And the theory told them where to look: among "
            "households poor enough to depend on rice, but not so poor that they eat nothing else. "
            "<bookmark mark='d'/> They sorted households by the share of their calories that came from rice before "
            "the experiment began."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(flow.boxes[0]))
            vo.wait_until("a")
            self.play(LaggedStart(GrowArrow(flow.arrows[0]), FadeIn(flow.boxes[1]),
                                  GrowArrow(flow.arrows[1]), FadeIn(flow.boxes[2]), lag_ratio=0.4), run_time=3)
            vo.wait_until("b")
            self.play(Write(reg), FadeIn(notes[0]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.clear_scene()

    def hunan(self):
        h = tables.JENSEN_MILLER_2008.data["hunan"]
        loc = tables.JENSEN_MILLER_2008.data["hunan_local"]
        g = tables.JENSEN_MILLER_2008.data["gansu"]
        rows = [("all households", h["full"], GREY_A), (r"rice $\le$ 80\% of calories", h["share_le_080"], GIFF),
                (r"rice $>$ 80\% of calories", h["share_gt_080"], IC),
                (r"rice 60--80\% of calories", h["share_060_080"], GIFF)]
        x0, x1, lo, hi = -2.0, 2.7, -1.4, 1.2

        def X(v):
            return x0 + (x1 - x0) * (v - lo) / (hi - lo)

        top, step = 1.9, 0.85
        zero = DashedLine([X(0), top + 0.5, 0], [X(0), top - step * 3 - 0.5, 0], color=GREY_B, stroke_width=2)
        zl = label(r"0", font_size=20, color=GREY_B).next_to(zero, DOWN, buff=0.08)
        grp = VGroup()
        for k, (name, (b, se, n), col) in enumerate(rows):
            y = top - step * k
            ci = Line([X(b - 1.96 * se), y, 0], [X(b + 1.96 * se), y, 0], color=col, stroke_width=4)
            dot = Dot([X(b), y, 0], radius=0.1, color=col)
            nm = label(name, font_size=24, color=WHITE).move_to([x0 - 0.3, y, 0], aligned_edge=RIGHT)
            val = label(rf"{b:+.2f} \ ({n})", font_size=20, color=col).next_to(dot, UP, buff=0.1)
            grp.add(VGroup(nm, ci, dot, val))
        axis_l = label(r"price elasticity of rice, \ 95\% intervals \ (household changes)", font_size=19,
                       color=GREY_B).move_to([X(0), top - step * 3 - 0.95, 0])
        head = label(r"Hunan: \ table 3 of Jensen and Miller", font_size=30, color=GIFF).to_edge(UP, buff=0.35)
        side = VGroup(
            label(rf"meat-eaters: \ meat {h['meat_over_50g'][0]:+.2f} \\ per 1\% on rice", font_size=24, color=FISHC),
            label(rf"a kernel-weighted curve: \\ positive from {loc['positive_from']:.2f} to {loc['positive_to']:.2f}"
                  rf" \\ of calories, \ peak {loc['peak']:.2f} at {loc['peak_at']:.2f}", font_size=24, color=GIFF),
            label(r"Gansu: \ weaker; \ little meat \\ to give up, \ and wheat \\ eaten in many forms", font_size=24,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.3).shift(DOWN * 0.1)
        tag = published_tag(r"Jensen and Miller, AER (2008), tables 3 and 6, figure 2", corner=DR, font_size=14)
        with self.voiceover(
            "Here is what they found in Hunan. <bookmark mark='a'/> Across all households the elasticity was "
            "positive, nought point two two, but not significant: the interval runs well below zero. "
            "<bookmark mark='b'/> Among households getting less than eighty percent of their calories from rice, "
            "it was nought point four five, and clearly positive. <bookmark mark='c'/> Among the very poorest, who "
            "ate almost nothing but rice, it was minus nought point six one: they had nothing to give up, and "
            "simply ate less when rice cost more. <bookmark mark='d'/> Between sixty and eighty percent, nought "
            "point six four. <bookmark mark='e'/> The mechanism showed too: households that ate meat cut it sharply "
            "when rice got dearer. A smoothed curve across calorie shares rose and fell, an inverted U, positive "
            "for nearly two thirds of the sample. In Gansu the evidence was weaker, and the authors said why: "
            "families there ate almost no meat to give up, and wheat came in many forms that could substitute for "
            "one another. <bookmark mark='f'/> One honest caution, which they raised themselves: searching across "
            "many cut-offs for a positive number is a forking path, Part four's warning. What protects them is that "
            "the theory picked the place to look before the data did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(zero), FadeIn(zl), FadeIn(axis_l), FadeIn(tag))
            for mk, r in zip("abcd", grp):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.2))
            vo.wait_until("e")
            self.play(LaggedStart(*[FadeIn(s_) for s_ in side], lag_ratio=0.6), run_time=4)
            vo.wait_until("f")
            self.play(Indicate(grp[1], color=E.ACCENT), Indicate(grp[3], color=E.ACCENT))
        self.clear_scene()

    def island(self):
        v = load("vouchers")
        from explainer.ai.viz import axes

        ax = axes([0.4, 0.96], [-1.2, 0.9], x_length=7.4, y_length=4.8, xticks=[0.4, 0.5, 0.6, 0.7, 0.8, 0.9],
                  yticks=[-1.0, -0.5, 0.0, 0.5], xlabel=r"share of calories from coconuts, before the vouchers",
                  ylabel=r"price elasticity", font_size=17, xfmt=lambda x: f"{x:.1f}", yfmt=lambda y: f"{y:+.1f}",
                  center=LEFT * 2.2 + DOWN * 0.35)
        a = ax.ax
        grid = np.array(v["grid"])
        zero = DashedLine(a.c2p(0.4, 0), a.c2p(0.96, 0), color=GREY_B, stroke_width=2)
        lo_, hi_ = np.clip(v["lo"], -1.2, 0.9), np.clip(v["hi"], -1.2, 0.9)
        band = Polygon(*[a.c2p(x, y) for x, y in zip(grid, lo_)],
                       *[a.c2p(x, y) for x, y in zip(grid[::-1], hi_[::-1])], stroke_width=0,
                       fill_color=GIFF, fill_opacity=0.18)
        est = VMobject(stroke_color=GIFF, stroke_width=4).set_points_smoothly([a.c2p(x, y) for x, y in
                                                                              zip(grid, v["b"])])
        tru = DashedVMobject(VMobject(stroke_color=WHITE, stroke_width=3).set_points_smoothly(
            [a.c2p(x, y) for x, y in zip(grid, v["true_curve"])]), num_dashes=40)
        rows = v["rows"]
        ze, zn = v["zone_elas"], v["zone_n"]
        side = VGroup(
            label(rf"{v['households']:,} households, \ {v['villages']} villages".replace(",", "{,}"), font_size=22),
            label(r"vouchers: \ 10, 20 or 30 cents off a \$1.20 coconut", font_size=19, color=GREY_A),
            label(rf"planted: \ +{ze['subsistence']:.2f} in the middle zone \\ ({zn['subsistence']} households), \ "
                  rf"{ze['standard']:.2f} and {ze['deprived']:.0f} \\ either side", font_size=20, color=WHITE),
            label(rf"all households: \ {signed(rows['full'][0])} \ ({rows['full'][1]:.2f})", font_size=21,
                  color=GREY_A),
            label(rf"coconuts 60--80\%: \ {rows['share_060_080'][0]:+.2f} \ ({rows['share_060_080'][1]:.2f})",
                  font_size=21, color=GIFF),
            label(rf"their fish: \ {rows['fish_060_080'][0]:+.2f}", font_size=21, color=FISHC),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(RIGHT, buff=0.3).shift(UP * 0.2)
        leg = VGroup(VGroup(Line(ORIGIN, RIGHT * 0.5, color=GIFF, stroke_width=4),
                            label(r"estimated, with 95\% band", font_size=17, color=GIFF)).arrange(RIGHT, buff=0.15),
                     VGroup(DashedLine(ORIGIN, RIGHT * 0.5, color=WHITE, stroke_width=3),
                            label(r"planted", font_size=17)).arrange(RIGHT, buff=0.15)).arrange(RIGHT, buff=0.4)
        leg.next_to(ax, UP, buff=0.12)
        lesson = label(r"averaged over everyone, \ the Giffen households cancel out", font_size=24,
                       color=E.ACCENT).to_edge(DOWN, buff=0.25)
        tag = island_tag(r"simulated: the Island, Jensen and Miller's design", corner=UR, font_size=13)
        with self.voiceover(
            "Could the method have found nothing if nothing was there, or found the truth if it was? On the Island "
            "we can check, because we plant the truth. <bookmark mark='a'/> Thirteen hundred of the Island's poorest "
            "households, in eleven villages, live on coconuts and fish and a little oil and greens. They get "
            "Jensen and Miller's vouchers, at random, and the same three surveys, with consumption reported with "
            "error. <bookmark mark='b'/> We planted the subsistence model: households in its middle zone have an "
            "elasticity of plus nought point four three; those on either side, negative ones. "
            "<bookmark mark='c'/> Run their regression on everyone and you get almost exactly zero: the Giffen "
            "households and the others cancel. <bookmark mark='d'/> Restrict to households getting sixty to eighty "
            "percent of their calories from coconuts, and it's plus nought point three four, short of the planted "
            "value because mismeasured shares put some households in the wrong group. Their fish fall sharply, as "
            "the mechanism says. <bookmark mark='e'/> And the kernel-weighted curve, drawn the way they drew theirs, "
            "traces the planted inverted U. <bookmark mark='f'/> The lesson goes beyond Giffen goods: an average "
            "effect can be zero while a large group responds strongly, in the opposite direction from everyone "
            "else."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(side[2]), Create(tru), FadeIn(leg[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]), FadeIn(side[5]))
            vo.wait_until("e")
            self.play(FadeIn(band), Create(est), FadeIn(leg[0]), run_time=2.0)
            vo.wait_until("f")
            self.play(FadeIn(lesson, shift=UP * 0.1))
        self.clear_scene()
