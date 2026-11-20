from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Robots(VoiceoverScene):
    def construct(self):
        card(self, 5, r"Robots", r"What does an industrial robot do to a town?", "Chapter five. Robots.",
             lit={2020: r"Acemoglu and Restrepo"}, scale=("city", "nation"), horizon=("a decade",))
        self.design()
        self.island()
        self.findings()

    def design(self):
        R = load("robots")
        steps = flow_chain([(r"each industry \\ adopts robots \\ at its own pace", MACHINE),
                            (r"each town's mix \\ of industries", WORKER),
                            (r"the town's \\ exposure", E.ACCENT),
                            (r"its employment \\ and wages", WAGE)],
                           notes=[r"robots per thousand \\ workers, \ nationally", r"its employment \\ shares, \ "
                                  r"before", r"the shares times \\ the industries' rates", r"compared across \\ "
                                  r"commuting zones"], box_w=2.7, font_size=19, note_size=15).move_to(UP * 1.4)
        bars = VGroup()
        for k, (nm, v) in enumerate(zip(R["names"], R["robots"])):
            h = v / 8.0 * 2.0
            b = Rectangle(width=0.9, height=max(h, 0.02), stroke_width=0, fill_color=MACHINE,
                          fill_opacity=0.9).move_to(np.array([-3.3 + 1.3 * k, -2.6 + h / 2, 0]))
            bars.add(VGroup(b, label(nm, font_size=16, color=GREY_A).next_to(b, DOWN, buff=0.1),
                            label(f"{v:g}", font_size=16, color=WHITE).next_to(b, UP, buff=0.06)))
        cap = label(r"the Island's industries: \ new robots per thousand workers", font_size=17,
                    color=GREY_A).next_to(bars, UP, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Computers replaced routine office tasks; industrial robots replace routine tasks on the factory floor: "
            "welding, painting, assembling. Daron Acemoglu and Pascual Restrepo asked what they did to American "
            "towns. <bookmark mark='a'/> Industries adopt robots at very different rates; carmakers most of all. "
            "<bookmark mark='b'/> Towns differ in their mix of industries, <bookmark mark='c'/> so each town's "
            "exposure is its industries' adoption rates, weighted by how many of its people worked in each. "
            "<bookmark mark='d'/> Then compare towns, really commuting zones, by exposure: did the more exposed lose "
            "more jobs, and see slower wage growth? It is the same shift-share logic as the China shock in Part "
            "thirty-six. <bookmark mark='e'/> On the Island, six industries adopt robots at these rates."
        ) as vo:
            self.play(FadeIn(steps.boxes[0]), FadeIn(steps.notes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(steps.arrows[0]), FadeIn(steps.boxes[1]), FadeIn(steps.notes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(steps.arrows[1]), FadeIn(steps.boxes[2]), FadeIn(steps.notes[2]))
            vo.wait_until("d")
            self.play(GrowArrow(steps.arrows[2]), FadeIn(steps.boxes[3]), FadeIn(steps.notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(tag), FadeIn(cap), LaggedStart(*[FadeIn(b_, shift=UP * 0.1) for b_ in bars],
                                                            lag_ratio=0.15), run_time=1.5)
        self.clear_scene()

    def island(self):
        R = load("robots")
        ex, de, mf = np.array(R["exposure"]), np.array(R["demp"]), np.array(R["manuf"])
        ax = plane([0, 5], [-4.5, 1.0], center=LEFT * 2.0 + DOWN * 0.4, x_length=7.6, y_length=4.8,
                   xticks=[0, 1, 2, 3, 4, 5], yticks=[-4, -3, -2, -1, 0, 1],
                   xlabel=r"exposure: \ robots per thousand workers",
                   ylabel=r"change in employment rate, \ points", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.0f}", font_size=14)
        pts = VGroup(*[Dot(ax.ax.c2p(x, y), radius=0.04, color=interpolate_color(ManimColor(WORKER),
                                                                                  ManimColor(LOSS), float(m)))
                       for x, y, m in zip(ex, de, mf) if -4.5 <= y <= 1.0])
        b0 = np.polyfit(ex, de, 1)
        fit = seg(ax, 0, b0[1], 5, b0[1] + 5 * b0[0], WHITE, 3)
        side = VGroup(
            label(r"each dot: \ a commuting zone; \\ redder: \ more manufacturing", font_size=17, color=GREY_A),
            label(rf"simple slope: \ {say_num(R['naive'], 2).replace('minus ', '$-$')}", font_size=19, color=WHITE),
            label(rf"holding the manufacturing \\ share fixed: \ {R['ctrl']:.2f} \ (s.e.\ {R['ctrl_se']:.2f})",
                  font_size=19, color=E.ACCENT),
            label(rf"planted: \ {R['beta']:.2f}", font_size=19, color=GAIN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Run the design on the Island's three hundred commuting zones, where the truth is planted: each robot "
            f"per thousand workers lowers the employment rate by {say_num(-R['beta'], 1)} of a percentage point. "
            "<bookmark mark='a'/> Each dot is a zone. <bookmark mark='b'/> The simple slope says "
            f"{say_num(R['naive'], 2)}, more than three times the truth. Why? The zones with the most robots are "
            "manufacturing towns, and manufacturing was shrinking anyway, from trade and offshoring. "
            "<bookmark mark='c'/> Hold the manufacturing share fixed and the estimate falls to "
            f"{say_num(R['ctrl'], 2)}, with a standard error of {R['ctrl_se']:.2f}: <bookmark mark='d'/> the planted "
            f"{say_num(R['beta'], 1)} lies inside its interval. Acemoglu and Restrepo spend much of their paper on "
            "exactly this: separating robots from everything else hitting the same towns."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(pts, lag_ratio=0.005), run_time=2.0)
            vo.wait_until("a")
            self.play(FadeIn(side[0]), Indicate(pts, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(Create(fit), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def findings(self):
        A = tables.AR_2020.data
        cards = point_cards([
            (r"jobs", rf"one more robot per \\ thousand workers: \\ employment rate \\ $-${A['emp_pp']} points",
             LOSS),
            (r"wages", rf"and wages \\ $-${A['wage_pct']:.2f}\%", LOSS),
            (r"not something else", r"distinct from imports \\ from China and Mexico, \\ offshoring, \ other IT, \\ "
                                    r"routine decline", WHITE),
            (r"no pre-trends", r"the most exposed zones \\ did not differ \\ before 1990", GAIN),
        ], width=12.8, cols=4, font_size=19).move_to(DOWN * 0.1)
        head = label(r"what Acemoglu and Restrepo found, \ 1990--2007", font_size=26, color=E.ACCENT).to_edge(
            UP, buff=0.6)
        foot = label(r"next: \ artificial intelligence, \ which can do non-routine tasks too \ (Part 65)",
                     font_size=20, color=GREY_A).to_edge(DOWN, buff=0.6)
        tag = published_tag(tables.AR_2020.tag, corner=DR, font_size=11)
        with self.voiceover(
            "What did they find in America? <bookmark mark='a'/> One more robot per thousand workers lowered a "
            f"zone's employment-to-population ratio by {A['emp_pp']} percentage points, <bookmark mark='b'/> and its "
            f"wages by {A['wage_pct']:.2f} percent. <bookmark mark='c'/> The effects are distinct from imports from "
            "China and Mexico, offshoring, other information technology and the decline of routine jobs, "
            "<bookmark mark='d'/> and the most exposed zones showed no different trends before the robots came. "
            "Robots are still few, so their total effect so far is modest; but they show that some technology "
            "simply replaces workers, rather than making them more productive. <bookmark mark='e'/> The open "
            "question is artificial intelligence, which can do some non-routine tasks as well. Part sixty-five "
            "takes it up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
