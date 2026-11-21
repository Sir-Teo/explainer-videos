from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403


def task_bar(n_lo, I, n_hi, width=10.0, height=0.7, origin=ORIGIN, x0=0.0, x1=1.6, new_from=1.0):
    """The task line from x0 to x1 (in task units) drawn as a bar; the tasks in [n_lo, n_hi] exist: machines do those
    below I (blue), people the rest (pink, green above ``new_from``: new tasks)."""
    scale = width / (x1 - x0)

    def xpos(v):
        return origin[0] - width / 2 + (v - x0) * scale

    g = VGroup()
    for a, b, c in ((n_lo, I, MACH), (I, min(n_hi, new_from), WORK), (max(I, new_from), n_hi, NEWT)):
        if b - a <= 1e-6:
            continue
        g.add(Rectangle(width=(b - a) * scale, height=height, stroke_width=1.2, stroke_color=c, fill_color=c,
                        fill_opacity=0.45).move_to([(xpos(a) + xpos(b)) / 2, origin[1], 0]))
    return g, xpos


class Tasks(VoiceoverScene):
    def construct(self):
        card(self, 3, r"The task model", r"When machines take a task, \ what happens to wages and to labour's share?",
             "Chapter three. The task model.", lit={1998: "Zeira", 2018: "Acemoglu and Restrepo"},
             scale=("firm", "nation"), horizon=("a decade",))
        self.line()
        self.decompose()
        self.curves()
        self.soso()
        self.evidence()

    def line(self):
        origin = UP * 0.6
        bar, xpos = task_bar(0.0, 0.3, 1.0, origin=origin)
        ticks = VGroup()
        for v, t in ((0.0, r"$N-1$"), (1.0, r"$N$")):
            ticks.add(label(t, font_size=20, color=GREY_A).move_to([xpos(v), origin[1] - 0.65, 0]))
        Ilab = label(r"$I$", font_size=22, color=E.ACCENT).move_to([xpos(0.3), origin[1] + 0.65, 0])
        cap = VGroup(label(r"machines", font_size=18, color=MACH), label(r"people", font_size=18, color=WORK))
        cap[0].move_to([xpos(0.15), origin[1], 0])
        cap[1].move_to([xpos(0.65), origin[1], 0])
        eq = MathTex(r"Y = \Big(\int_{N-1}^{N} y(i)^{\frac{\sigma-1}{\sigma}}\,di\Big)^{\frac{\sigma}{\sigma-1}}",
                     font_size=40).to_edge(UP, buff=0.4)
        notes = VGroup(
            label(r"automation: \ $I$ moves right; \ people lose tasks (displacement)", font_size=20, color=NAIVE),
            label(r"cheaper tasks raise output, \ and the demand for people in the rest (productivity)",
                  font_size=20, color=GDP),
            label(r"new tasks: \ $N$ moves right; \ people gain work (reinstatement)", font_size=20, color=NEWT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Zeira, \ QJE 113(4) (1998); \ Acemoglu and Restrepo, \ AER 108(6) (2018)",
                            corner=DL, font_size=12)
        bar2, _ = task_bar(0.0, 0.6, 1.0, origin=origin)
        bar3, _ = task_bar(0.3, 0.6, 1.3, origin=origin)
        with self.voiceover(
            "Economists think about this race with a model of tasks, from Joseph Zeira and, in its modern form, "
            "Daron Acemoglu and Pascual Restrepo. <bookmark mark='a'/> Output needs a range of tasks, from N minus "
            "one to N, combined with an elasticity sigma below one: the tasks are complements. <bookmark mark='b'/> "
            "Machines can do the tasks below a threshold I; people do the rest. <bookmark mark='c'/> Automation "
            "moves I to the right. People lose those tasks: that is displacement. <bookmark mark='d'/> But the "
            "automated tasks get cheaper, output rises, and so does the demand for people in the tasks they still "
            "do: the productivity effect. <bookmark mark='e'/> And the economy invents new tasks, in which people "
            "have the advantage: N moves right, the oldest tasks drop away, and people gain work: reinstatement."
        ) as vo:
            self.play(FadeIn(tag), Write(eq))
            vo.wait_until("a")
            self.play(FadeIn(ticks), Indicate(eq, scale_factor=1.03))
            vo.wait_until("b")
            self.play(FadeIn(bar), FadeIn(cap), FadeIn(Ilab))
            vo.wait_until("c")
            self.play(Transform(bar, bar2), Ilab.animate.move_to([xpos(0.6), origin[1] + 0.65, 0]),
                      cap[0].animate.move_to([xpos(0.3), origin[1], 0]),
                      cap[1].animate.move_to([xpos(0.8), origin[1], 0]), FadeIn(notes[0]), run_time=1.6)
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
            vo.wait_until("e")
            self.play(Transform(bar, bar3), ticks[0].animate.move_to([xpos(0.3), origin[1] - 0.65, 0]),
                      ticks[1].animate.move_to([xpos(1.3), origin[1] - 0.65, 0]),
                      cap[0].animate.move_to([xpos(0.45), origin[1], 0]), FadeIn(notes[2]), run_time=1.6)
        self.clear_scene()

    def decompose(self):
        T = load("tasks")
        eq = MathTex(r"\ln w = \tfrac{1}{\sigma}\ln Y", r"+ \tfrac{1}{\sigma}\ln(N - I)", r"+ \text{const}",
                     font_size=42).to_edge(UP, buff=0.5)
        eq[0].set_color(GDP)
        eq[1].set_color(NAIVE)
        vals = [100 * T["productivity"], 100 * T["displacement"], 100 * T["dlnw"]]
        ax = plane([-0.6, 2.6], [-120, 80], center=DOWN * 0.6 + LEFT * 1.0, x_length=7.0, y_length=4.4, xticks=[],
                   yticks=[-100, -50, 0, 50], ylabel=r"change in the log wage, \ $\times 100$",
                   yfmt=lambda v: f"{v:.0f}".replace("-", "{-}"), font_size=14)
        b = bars(ax, [0, 1, 2], vals, [GDP, NAIVE, WORK], width=0.6)
        names = VGroup(*[label(t, font_size=16, color=c).next_to(ax.ax.c2p(k, 0), DOWN if v > 0 else UP, buff=0.15)
                         for k, (t, c, v) in enumerate(((r"productivity", GDP, 1), (r"displacement", NAIVE, -1),
                                                         (r"net", WORK, -1)))])
        nums = VGroup(*[label(f"{v:+.0f}".replace("-", "{-}"), font_size=17, color=c).next_to(
            bb, UP if v > 0 else DOWN, buff=0.08) for bb, v, c in zip(b, vals, (GDP, NAIVE, WORK))])
        side = VGroup(label(r"capital fixed", font_size=17, color=GREY_A),
                      label(rf"automation from 20\% of tasks to {100 * T['parity']:.0f}\%,", font_size=17,
                            color=GREY_A),
                      label(r"where machines stop being cheaper", font_size=17, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        side.next_to(ax.ax, RIGHT, buff=0.4)
        if side.get_right()[0] > 6.9:
            side.shift(LEFT * (side.get_right()[0] - 6.9))
        tag = island_tag(r"computed: \ agora.automation.task\_paths \ ($\sigma = 0.8$)", corner=DL, font_size=12)
        with self.voiceover(
            "The model gives the wage in one line. <bookmark mark='a'/> The log wage is one over sigma times log "
            "output, the productivity effect, plus one over sigma times the log of the range of tasks people do, "
            "the displacement effect. <bookmark mark='b'/> Run it with capital fixed, in the short run, and "
            f"automate from a fifth of the tasks to {100 * T['parity']:.0f} percent, the point where machines stop "
            "being cheaper than people. <bookmark mark='c'/> Output rises: productivity adds "
            f"{vals[0]:.0f} log points to the wage. <bookmark mark='d'/> People's range of tasks shrinks: "
            f"displacement subtracts {-vals[1]:.0f}. <bookmark mark='e'/> Net, the wage falls by "
            f"{-vals[2]:.0f} log points. Automation is not a free lunch for workers. Whether it helps them depends "
            "on whether the productivity effect is bigger than the displacement."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(Write(eq))
            vo.wait_until("b")
            self.play(FadeIn(ax), FadeIn(side))
            for mk, k in zip("cde", range(3)):
                vo.wait_until(mk)
                self.play(GrowFromEdge(b[k], DOWN if vals[k] > 0 else UP), FadeIn(names[k]), FadeIn(nums[k]))
        self.clear_scene()

    def curves(self):
        T = load("tasks")
        Is = np.array(T["I"])
        axl = plane([0.2, 0.8], [0.8, 2.4], center=LEFT * 3.5 + DOWN * 0.3, x_length=5.4, y_length=4.4,
                    xticks=[0.2, 0.4, 0.6, 0.8], yticks=[1.0, 1.5, 2.0], xlabel=r"share of tasks machines can do",
                    ylabel=r"the wage", xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.1f}", font_size=13)
        ws = path(axl, Is, T["short"]["w"], WORK, 3.0, smooth=False)
        wl = path(axl, Is, T["long"]["w"], MACH, 3.0)
        par = vline(axl, T["parity"], 0.8, 2.4, GREY_C)
        plab = label(r"machines no \\ longer cheaper", font_size=13, color=GREY_B).next_to(
            axl.ax.c2p(T["parity"], 2.3), RIGHT, buff=0.08)
        kl = legend_rows([(WORK, "capital fixed (short run)"), (MACH, "capital supplied (long run)")],
                         font_size=14).next_to(axl.ax.c2p(0.2, 2.4), DR, buff=0.15)
        axr = plane([0, 1], [0, 1], center=RIGHT * 3.3 + DOWN * 0.3, x_length=5.4, y_length=4.4,
                    xticks=[], yticks=[0, 0.25, 0.5, 0.75, 1.0], xlabel=r"automation, \ then new tasks",
                    ylabel=r"labour's share of output", yfmt=lambda v: f"{100 * v:.0f}\\%",
                    font_size=13)
        xa = np.linspace(0, 0.5, len(Is))
        xb = np.linspace(0.5, 1.0, len(Is))
        sa = path(axr, xa, T["long"]["labour_share"], NAIVE, 3.0)
        sb = path(axr, xb, T["new_tasks"]["labour_share"], NEWT, 3.0)
        la = label(r"automation", font_size=14, color=NAIVE).next_to(axr.ax.c2p(0.25, 0), UP, buff=0.12)
        lb = label(r"new tasks", font_size=14, color=NEWT).next_to(axr.ax.c2p(0.75, 0), UP, buff=0.12)
        w0, w1 = T["new_tasks"]["w"][0], T["new_tasks"]["w"][-1]
        tag = island_tag(r"computed: \ agora.automation.task\_paths", corner=DL, font_size=12)
        ls = T["long"]["labour_share"]
        nt = T["new_tasks"]["labour_share"]
        with self.voiceover(
            "Now let the automation frontier sweep from a fifth of the tasks to four fifths. <bookmark mark='a'/> "
            "With capital fixed, the wage first rises, as cheap machines raise output, then falls, as people are "
            "pushed into fewer tasks, until machines are no longer cheaper and automation stops. <bookmark "
            "mark='b'/> In the long run capital is built to meet demand, at a fixed rental, and the productivity "
            "effect wins: the wage rises the whole way. <bookmark mark='c'/> But labour's share of output falls in "
            f"both. In the long run, from {100 * ls[0]:.0f} percent to {100 * ls[-1]:.0f}. Higher wages, a smaller "
            "slice. <bookmark mark='d'/> Then let new tasks arrive, in which people are more productive than in "
            f"the old ones. Labour's share climbs back to {100 * nt[-1]:.0f} percent, and the wage rises by another "
            f"{100 * (w1 / w0 - 1):.0f} percent. Acemoglu and Restrepo's reading of American history is that, "
            "until the late nineteen-eighties, new tasks kept pace with automation; since then, they have not."
        ) as vo:
            self.play(FadeIn(axl), FadeIn(axr), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(ws), FadeIn(par), FadeIn(plab), FadeIn(kl[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(Create(wl), FadeIn(kl[1]), run_time=1.6)
            vo.wait_until("c")
            self.play(Create(sa), FadeIn(la), run_time=1.6)
            vo.wait_until("d")
            self.play(Create(sb), FadeIn(lb), run_time=1.6)
        self.clear_scene()

    def soso(self):
        S = load("soso")["rows"]
        R = np.array([r["R"] for r in S])
        gain = np.array([100 * r["wage_gain"] for r in S])
        fall = np.array([100 * r["share_fall"] for r in S])
        ax = plane([0.25, 1.0], [0, 60], center=LEFT * 1.2 + DOWN * 0.3, x_length=8.4, y_length=4.6,
                   xticks=[0.3, 0.5, 0.7, 0.9], yticks=[0, 20, 40, 60],
                   xlabel=r"what a machine costs to do a task \ (below the wage throughout)",
                   ylabel=r"percentage points or percent", xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        g = path(ax, R, gain, GDP, 3.2)
        f = path(ax, R, fall, NAIVE, 3.2)
        key = legend_rows([(GDP, "the wage gain from automating 10% more tasks, %"),
                           (NAIVE, "the fall in labour's share, points")], font_size=15).next_to(
            ax.ax.c2p(0.25, 60), DR, buff=0.2).shift(RIGHT * 2.4)
        so = label(r"so-so automation", font_size=20, color=NAIVE).next_to(ax.ax.c2p(0.9, 12), UP, buff=0.3)
        tag = published_tag(r"Acemoglu and Restrepo, \ JEP 33(2) (2019); \ the Island: \ agora.automation.so\_so",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Which automation is good for workers? <bookmark mark='a'/> Automate ten percent more of the tasks, in "
            "the long run, and vary what the machine costs. <bookmark mark='b'/> If machines are far cheaper than "
            f"people, the productivity effect is large: the wage rises by about {gain[0]:.0f} percent. <bookmark "
            "mark='c'/> If machines are barely cheaper, the displacement is the same, and labour's share falls by "
            f"the same {fall.mean():.0f} or so points, but the gain is tiny: {gain[-1]:.0f} percent. Acemoglu and "
            "Restrepo call this so-so automation: self-checkout machines that save the shop a little and take a "
            "whole task from people. The worry about AI is not that it is brilliant. It is that much of it could "
            "be so-so."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(key))
            vo.wait_until("b")
            self.play(Create(g), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(f), FadeIn(so), run_time=1.6)
        self.clear_scene()

    def evidence(self):
        cards = point_cards([
            (r"robots and jobs", r"one more industrial robot per thousand workers: \ the employment-to-population "
             r"ratio 0.2 points lower, \ wages 0.42\% lower \ (Acemoglu and Restrepo, \ JPE 2020)", MACH),
            (r"tasks and inequality", r"50--70\% of the change in the US wage structure, \ 1980--2016, \ from "
             r"groups whose routine tasks were automated \ (Acemoglu and Restrepo, \ Econometrica 2022)", WORK),
            (r"routine tasks", r"computers take routine tasks and help with abstract ones: \ jobs polarize, \ "
             r"Part 39 \ (Autor, \ Levy and Murnane, \ 2003)", GDP),
            (r"what is new about AI", r"it reaches non-routine, \ cognitive tasks: \ writing, \ coding, \ "
             r"advising, \ the tasks the last wave left to people", IDEA),
        ], width=12.6, cols=2, font_size=19).move_to(DOWN * 0.2)
        head = label(r"what the evidence on earlier automation says", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.5)
        with self.voiceover(
            "The evidence from earlier waves fits the model. <bookmark mark='a'/> Across American commuting zones, "
            "Acemoglu and Restrepo find that one more industrial robot per thousand workers lowered the "
            "employment-to-population ratio by about 0.2 percentage points and wages by 0.42 percent. <bookmark "
            "mark='b'/> And they attribute between half and seventy percent of the change in the American wage "
            "structure from 1980 to 2016 to groups whose routine tasks were automated. <bookmark mark='c'/> That "
            "is the polarization of Part thirty-nine: computers took routine tasks and helped with abstract ones. "
            "<bookmark mark='d'/> What is new about generative AI is where it reaches: writing, coding, advising, "
            "the non-routine cognitive tasks the last wave left to people, often to the best paid."
        ) as vo:
            self.play(FadeIn(head))
            for mk, c in zip("abcd", cards.cards):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
