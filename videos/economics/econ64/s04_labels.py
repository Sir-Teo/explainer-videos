from __future__ import annotations

from videos.economics.econ64.common import *  # noqa: F403


class Labels(VoiceoverScene):
    def construct(self):
        card(self, 3, r"Selective labels", r"How do you judge an algorithm on outcomes the judges never let "
             r"happen?", "Chapter three. Selective labels.", lit={2017: r"Lakkaraju et al.", 2018: r"Kleinberg et al."},
             scale=("person", "city"), horizon=("a year",))
        self.frontier()
        self.contract()
        self.naive()

    def frontier(self):
        Cc = load("courts")
        g = np.array(Cc["grid"])
        cr = 100 * np.array(Cc["crime"])
        J = Cc["judges"]
        ax = plane([0, 0.6], [0, 16], center=LEFT * 2.4 + DOWN * 0.3, x_length=6.6, y_length=4.6,
                   xticks=[0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0, 4, 8, 12, 16],
                   xlabel=r"share of defendants detained", ylabel=r"failures to appear per 100 defendants",
                   xfmt=lambda v: rf"{100 * v:.0f}\%", yfmt=lambda v: f"{v:.0f}", font_size=14)
        curve = path(ax, g, cr, ALGO, 3.4)
        qs = VGroup(*[dot(ax, q["detain"], 100 * q["crime"], JUDGE, 0.07) for q in Cc["quintiles"]])
        jd = dot(ax, J["detain"], 100 * J["crime"], WHITE, 0.1)
        aj = 100 * Cc["alg_at_judges"]
        v1 = Arrow(ax.ax.c2p(J["detain"], 100 * J["crime"]), ax.ax.c2p(J["detain"], aj), buff=0.08, color=GAIN,
                   stroke_width=3, tip_length=0.15)
        h1 = Arrow(ax.ax.c2p(J["detain"], 100 * J["crime"]), ax.ax.c2p(Cc["detain_at_judges_crime"],
                                                                         100 * J["crime"]),
                   buff=0.08, color=GAIN, stroke_width=3, tip_length=0.15)
        side = VGroup(
            label(r"blue: \ detain by the algorithm's ranking", font_size=19, color=ALGO),
            label(r"pink: \ the judges, \ by leniency, \ fifth by fifth", font_size=19, color=JUDGE),
            label(rf"same detention: \ {100 * Cc['crime_cut']:.0f}\% fewer failures", font_size=19, color=GAIN),
            label(rf"same failures: \ {100 * Cc['detain_cut']:.0f}\% fewer detained", font_size=19, color=GAIN),
            label(r"but this chart uses outcomes \\ only the simulation can see", font_size=19, color=HOLD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(r"the Island: \ test half, \ true outcomes; \ agora.learn.policy\_curves", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Here is the choice the court faces, on the test half. <bookmark mark='a'/> The blue curve: detain the "
            "share of defendants with the highest predicted risk, and count the failures to appear among everyone "
            "else. Detain more, fewer failures. <bookmark mark='b'/> The pink points are the judges, grouped by how "
            f"lenient they are, and the white point is all of them together: {100 * J['detain']:.0f} percent "
            f"detained, {100 * J['crime']:.1f} failures per hundred defendants. <bookmark mark='c'/> At the judges' "
            f"detention rate, the algorithm's ranking has {100 * Cc['crime_cut']:.0f} percent fewer failures. "
            f"<bookmark mark='d'/> Or, for the judges' failure rate, it detains {100 * Cc['detain_cut']:.0f} "
            "percent fewer people. <bookmark mark='e'/> But this picture cheats. It uses what every detained "
            "defendant would have done if released, which the Island knows and no real court ever does."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(curve), FadeIn(side[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(qs), FadeIn(jd), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(GrowArrow(v1), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(GrowArrow(h1), FadeIn(side[3]))
            vo.wait_until("e")
            self.play(FadeIn(side[4]))
        self.clear_scene()

    def contract(self):
        K = load("contraction")
        rows = K["rows"]
        steps = flow_chain([(r"take the most lenient fifth of judges", JUDGE),
                            (r"among those they released, \ detain more, \ highest predicted risk first", ALGO),
                            (r"until as many are detained as by a stricter fifth", ALGO),
                            (r"count failures among those still released: \ all observed", GAIN)],
                           box_w=2.9, box_h=1.3, font_size=18).to_edge(UP, buff=0.5)
        if steps.width > 13.0:
            steps.width = 13.0
        ax = plane([-0.6, 3.6], [0, 10], center=DOWN * 1.65 + LEFT * 1.6, x_length=6.4, y_length=2.9, xticks=[],
                   yticks=[0, 5, 10], ylabel=r"failures per 100", yfmt=lambda v: f"{v:.0f}", font_size=13)
        jb = bars(ax, [k - 0.17 for k in range(4)], [100 * r["judges"] for r in rows], [JUDGE] * 4, width=0.3)
        ab = bars(ax, [k + 0.17 for k in range(4)], [100 * r["algorithm"] for r in rows], [ALGO] * 4, width=0.3)
        labs = VGroup(*[label(rf"{100 * r['detain']:.0f}\% detained", font_size=13, color=GREY_A).next_to(
            ax.ax.c2p(k, 0), DOWN, buff=0.1) for k, r in enumerate(rows)])
        key = legend_rows([(JUDGE, r"the stricter judges"), (ALGO, r"the lenient judges' cases, \ contracted by "
                                                                  r"the algorithm")], font_size=16)
        key.next_to(ax, RIGHT, buff=0.4)
        tag = published_tag(r"Lakkaraju, \ Kleinberg, \ Leskovec, \ Ludwig and Mullainathan, \ KDD (2017); \ "
                            r"Kleinberg et al.\ (2018)", corner=DL, font_size=12)
        with self.voiceover(
            "The way round it is a design, not a model. Because cases go to judges at random, every judge sees the "
            "same kind of defendant. <bookmark mark='a'/> Take the most lenient fifth of the judges. <bookmark "
            "mark='b'/> Among the defendants they released, let the algorithm detain more, highest predicted risk "
            "first, <bookmark mark='c'/> until as many are detained as a stricter group of judges detained. "
            "<bookmark mark='d'/> Every failure among those still released was actually observed, because the "
            "lenient judges released them. This is the contraction design. <bookmark mark='e'/> Compare: at each "
            "stricter group's detention rate, the algorithm's contracted caseload has fewer failures than those "
            "judges' own, using no outcome that was never seen."
        ) as vo:
            self.play(FadeIn(tag))
            for k, mk in enumerate("abcd"):
                vo.wait_until(mk)
                anims = [FadeIn(steps.boxes[k])]
                if k:
                    anims.append(GrowArrow(steps.arrows[k - 1]))
                self.play(*anims)
            vo.wait_until("e")
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(key), *[GrowFromEdge(b, DOWN) for b in jb],
                      *[GrowFromEdge(b, DOWN) for b in ab], run_time=1.5)
        self.clear_scene()

    def naive(self):
        K = load("contraction")
        vals = [100 * K["naive"], 100 * K["truth"]]
        ax = plane([-0.6, 1.6], [0, 8], center=LEFT * 3.4 + DOWN * 0.3, x_length=3.6, y_length=4.4, xticks=[],
                   yticks=[0, 2, 4, 6, 8], ylabel=r"the algorithm's failures per 100", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        b = bars(ax, [0, 1], vals, [NAIVE, TRUTHC], width=0.55)
        labs = VGroup(label(r"filled in \\ by the model", font_size=14, color=NAIVE).next_to(ax.ax.c2p(0, 0), DOWN,
                                                                                            buff=0.12),
                      label(r"the truth", font_size=14, color=TRUTHC).next_to(ax.ax.c2p(1, 0), DOWN, buff=0.12))
        vl = VGroup(*[label(f"{v:.1f}", font_size=15, color=c).next_to(x, UP, buff=0.06)
                      for v, c, x in zip(vals, (NAIVE, TRUTHC), b)])
        side = VGroup(
            label(r"the tempting shortcut: \ fill in each detained \\ defendant's outcome with the model's own guess",
                  font_size=19, color=NAIVE),
            label(rf"the judges saw something in court: \\ the detained had a signal of "
                  rf"{K['s_detained']:+.2f}, \ the released {K['s_released']:+.2f}".replace("-", "{-}"),
                  font_size=19, color=JUDGE),
            label(rf"so the detained were riskier than their records: \\ truly {100 * K['p_detained']:.0f}\%, \ "
                  rf"predicted {100 * K['risk_detained']:.0f}\%", font_size=19, color=WHITE),
            label(r"the shortcut flatters the algorithm; \\ random assignment of judges is the check", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        tag = island_tag(r"the Island: \ the courtroom signal planted; \ agora.learn.contraction", corner=DL,
                         font_size=12)
        with self.voiceover(
            "Why not simply fill in the missing outcomes with the algorithm's own predictions? <bookmark mark='a'/> "
            "That shortcut says the algorithm would see "
            f"{vals[0]:.1f} failures per hundred at the judges' detention rate. <bookmark mark='b'/> The truth is "
            f"{vals[1]:.1f}. <bookmark mark='c'/> The gap comes from what the judges saw in court and the records do "
            "not: on the Island, a signal that the judges used and the algorithm cannot. <bookmark mark='d'/> The "
            f"defendants they detained were riskier than their records suggest: {100 * K['p_detained']:.0f} percent "
            f"in truth, {100 * K['risk_detained']:.0f} percent by the model. <bookmark mark='e'/> So the shortcut "
            "flatters the algorithm. Kleinberg and his coauthors relied instead on the random assignment of "
            "judges, the instrument idea of Part four: lenient and strict judges see the same kind of defendant."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(labs), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[0]))
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(vl[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(vl[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[1]))
            vo.wait_until("d")
            self.play(FadeIn(side[2]))
            vo.wait_until("e")
            self.play(FadeIn(side[3]))
        self.clear_scene()
