from __future__ import annotations

from videos.economics.econ39.common import *  # noqa: F403


class Tasks(VoiceoverScene):
    def construct(self):
        card(self, 4, r"Tasks, \ not skills", r"What does a computer do to a job?",
             "Chapter four. Tasks, not skills.",
             lit={2003: r"Autor, \ Levy and Murnane", 2011: r"Acemoglu and Autor"}, scale=("firm", "nation"),
             horizon=("a decade",))
        self.quadrants()
        self.polarization()
        self.model()

    def quadrants(self):
        cells = [
            (r"routine cognitive", r"bookkeeping, \ filing, \\ checking claims", r"computers substitute", LOSS),
            (r"non-routine analytic \\ and interactive", r"research, \ management, \\ persuasion, \ diagnosis",
             r"computers complement", GAIN),
            (r"routine manual", r"assembling, \ sorting, \\ machine tending", r"computers substitute", LOSS),
            (r"non-routine manual", r"cleaning, \ cooking, \\ caring, \ driving", r"computers hardly touch", MIDS),
        ]
        boxes = VGroup()
        for t, ex, eff, col in cells:
            b = RoundedRectangle(width=5.2, height=2.1, corner_radius=0.12, stroke_color=col, stroke_width=2.5,
                                 fill_color="#141821", fill_opacity=1)
            g = VGroup(label(t, font_size=22, color=col), label(ex, font_size=18, color=GREY_A),
                       label(eff, font_size=19, color=WHITE)).arrange(DOWN, buff=0.18).move_to(b)
            boxes.add(VGroup(b, g))
        boxes.arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.35)).move_to(DOWN * 0.3)
        top = VGroup(label(r"routine", font_size=20, color=GREY_B).next_to(boxes[0], UP, buff=0.15),
                     label(r"non-routine", font_size=20, color=GREY_B).next_to(boxes[1], UP, buff=0.15))
        tag = published_tag(tables.ALM_2003.tag, corner=DR, font_size=11)
        with self.voiceover(
            "In 2003 David Autor, Frank Levy and Richard Murnane proposed looking not at workers' skills but at the "
            "tasks a job is made of. <bookmark mark='a'/> Routine cognitive tasks, like bookkeeping or checking a "
            "claim, follow explicit rules, and a computer can be programmed to follow them: it substitutes for the "
            "worker. <bookmark mark='b'/> Routine manual tasks, assembling or sorting, likewise. "
            "<bookmark mark='c'/> Non-routine analytic and interactive tasks, research, management, persuasion, are "
            "hard to write down, and the computer makes the people who do them more productive: it complements them. "
            "<bookmark mark='d'/> And non-routine manual tasks, cleaning, cooking, caring for someone, need eyes and "
            "hands in an unpredictable world, and computers have hardly touched them. Routine tasks were concentrated "
            "in middle-paid jobs: the factory floor and the back office."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(top), *[FadeIn(b[0]) for b in boxes])
            for mk, k in zip("abcd", (0, 2, 1, 3)):
                vo.wait_until(mk)
                self.play(FadeIn(boxes[k][1], shift=UP * 0.1))
        self.clear_scene()

    def polarization(self):
        P = load("polar")
        p = np.array(P["pctile"])
        ax = plane([0, 100], [-0.4, 0.5], center=LEFT * 1.4 + DOWN * 0.4, x_length=9.0, y_length=4.8,
                   xticks=[0, 20, 40, 60, 80, 100], yticks=[-0.4, -0.2, 0, 0.2, 0.4],
                   xlabel=r"occupations ranked by their 1980 mean wage \ (percentile)",
                   ylabel=r"change in employment share, \ percentage points", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:+.1f}", font_size=14)
        zero = seg(ax, 0, 0, 100, 0, GREY_B, 1.5, dashed=True)
        rt = np.array(P["routine"])
        rbars = VGroup()
        for x, r in zip(p, rt):
            p0, p1 = ax.ax.c2p(x - 0.45, -0.4), ax.ax.c2p(x + 0.45, -0.4 + 0.3 * r)
            rbars.add(Rectangle(width=p1[0] - p0[0], height=max(p1[1] - p0[1], 0.001), stroke_width=0,
                                fill_color=LOSS, fill_opacity=0.35).move_to((p0 + p1) / 2))
        ln = path(ax, p, P["smooth"], EMP, 3.6)
        raw = VGroup(*[dot(ax, x, y, GREY_B, 0.025) for x, y in zip(p, P["d8005"]) if -0.4 <= y <= 0.5])
        l1 = path(ax, p, P["smooth8090"], GREY_B, 2.0)
        side = VGroup(
            label(r"pink: \ 1980--2005", font_size=17, color=EMP),
            label(r"grey: \ the 1980s alone", font_size=17, color=GREY_B),
            label(r"pale red bars: \\ the share of each \\ percentile's jobs \\ that were routine \\ in 1980",
                  font_size=16, color=LOSS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        tag = data_tag(r"Autor and Dorn (2013), \ replication data", corner=DR, font_size=12)
        with self.voiceover(
            "Now count jobs instead of wages. Rank occupations by their 1980 wage, as before, and ask how each "
            "percentile's share of employment changed to 2005: each grey dot is one percentile. <bookmark mark='a'/> "
            "Smoothed, the curve is a U again: "
            "employment grew at the bottom and at the top, and shrank between the fifteenth and the fiftieth "
            "percentiles. <bookmark mark='b'/> In the 1980s alone, the bottom had barely grown: the U came later, "
            "as low-paid service jobs expanded. <bookmark mark='c'/> Underneath, the share of each percentile's jobs "
            "that were routine in 1980. The routine jobs were piled in the lower middle, exactly where employment "
            "fell. This is polarization: the labour market emptied in the middle and filled at both ends."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(zero), FadeIn(tag), FadeIn(raw, lag_ratio=0.01), run_time=2.0)
            vo.wait_until("a")
            self.play(Create(ln), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rbars, lag_ratio=0.01), FadeIn(side[2]), run_time=1.5)
        self.clear_scene()

    def model(self):
        T = load("tasks")
        B, A = T["before"], T["after"]
        a, b = T["auto"]
        x0, x1 = -5.5, 5.5

        def X(i):
            return x0 + (x1 - x0) * i

        def strip(res, y, auto):
            g = VGroup()
            if auto:
                spans = [(0, res["I_L"], LOWS), (res["I_L"], a, MIDS), (b, res["I_H"], MIDS), (res["I_H"], 1, HIGHS)]
            else:
                spans = [(0, res["I_L"], LOWS), (res["I_L"], res["I_H"], MIDS), (res["I_H"], 1, HIGHS)]
            for s0, s1, col in spans:
                g.add(Rectangle(width=X(s1) - X(s0), height=0.6, stroke_width=0, fill_color=col,
                                fill_opacity=0.85).move_to(np.array([(X(s0) + X(s1)) / 2, y, 0])))
            if auto:
                g.add(Rectangle(width=X(b) - X(a), height=0.6, stroke_width=0, fill_color=MACHINE,
                                fill_opacity=1).move_to(np.array([(X(a) + X(b)) / 2, y, 0])))
            return g
        s0 = strip(B, 1.3, False)
        s1 = strip(A, -0.6, True)
        lab0 = label(r"before", font_size=20, color=GREY_A).next_to(s0, LEFT, buff=0.2)
        lab1 = label(r"after", font_size=20, color=GREY_A).next_to(s1, LEFT, buff=0.2)
        ends = VGroup(label(r"simple tasks", font_size=16, color=GREY_A).next_to(s0, UP, buff=0.12).align_to(s0, LEFT),
                      label(r"complex tasks", font_size=16, color=GREY_A).next_to(s0, UP, buff=0.12).align_to(s0,
                                                                                                         RIGHT))
        keys = VGroup(label(r"low skill", font_size=18, color=LOWS), label(r"middle", font_size=18, color=MIDS),
                      label(r"high skill", font_size=18, color=HIGHS), label(r"machines", font_size=18,
                                                                             color=MACHINE)).arrange(RIGHT, buff=0.6)
        keys.to_edge(UP, buff=0.35)
        arrows = VGroup(Arrow(np.array([X(B["I_L"]), 0.95, 0]), np.array([X(A["I_L"]), -0.25, 0]), color=WHITE,
                              buff=0.05, stroke_width=3),
                        Arrow(np.array([X(B["I_H"]), 0.95, 0]), np.array([X(A["I_H"]), -0.25, 0]), color=WHITE,
                              buff=0.05, stroke_width=3))
        nums = VGroup(
            label(rf"middle over low: \ {B['wM_wL']:.2f} $\to$ {A['wM_wL']:.2f}", font_size=20, color=MIDS),
            label(rf"high over middle: \ {B['wH_wM']:.2f} $\to$ {A['wH_wM']:.2f}", font_size=20, color=HIGHS),
        ).arrange(RIGHT, buff=0.9).to_edge(DOWN, buff=0.9)
        note_ = label(r"Agora: \ a continuum of tasks, \ three skills, \ comparative advantage", font_size=16,
                      color=GREY_A).to_edge(DOWN, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Daron Acemoglu and David Autor turned this into a model, which Agora solves. Line up every task in the "
            "economy, from simplest to most complex. <bookmark mark='a'/> Three kinds of worker share them out: each "
            "is relatively better at more complex tasks the more skilled they are, so low-skill workers take the "
            "simple end, high-skill workers the complex end, and the middle takes the middle. The boundaries settle "
            "where an employer is indifferent between the two neighbouring kinds of worker. <bookmark mark='b'/> Now "
            f"let machines take over a band of middle tasks, a fifth of the line. <bookmark mark='c'/> Displaced "
            "middle-skill workers move down the line, into simpler tasks that low-skill workers used to do, and "
            "push them into fewer tasks still; high-skill workers keep the complex end. <bookmark mark='d'/> The "
            "middle's wage falls relative to both neighbours': the middle-to-low ratio "
            f"falls from {B['wM_wL']:.2f} to {A['wM_wL']:.2f}, and the high-to-middle ratio rises from "
            f"{B['wH_wM']:.2f} to {A['wH_wM']:.2f}. Technology that replaces tasks, not skills, hollows out the middle "
            "and can push its workers down the ladder."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(note_), FadeIn(keys[:3]))
            vo.wait_until("a")
            self.play(FadeIn(s0, lag_ratio=0.3), FadeIn(lab0), FadeIn(ends), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(keys[3]), FadeIn(lab1), FadeIn(s1[-1]))
            vo.wait_until("c")
            self.play(FadeIn(s1[:4], lag_ratio=0.3), GrowArrow(arrows[0]), GrowArrow(arrows[1]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(nums, shift=UP * 0.1))
        self.clear_scene()
