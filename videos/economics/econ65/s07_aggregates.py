from __future__ import annotations

from videos.economics.econ65.common import *  # noqa: F403


def heat(v, vmax):
    """A colour from dark blue (0) to gold (vmax)."""
    t = float(np.clip(v / vmax, 0, 1))
    return interpolate_color(ManimColor("#1C2A44"), ManimColor(TRUTHC), t ** 0.6)


class Aggregates(VoiceoverScene):
    def construct(self):
        card(self, 6, r"From tasks to aggregates", r"If AI makes some tasks much cheaper, \ how much richer does the "
             r"whole economy get?", "Chapter six. From tasks to aggregates.",
             lit={2024: "Eloundou et al.; Acemoglu"}, scale=("nation",), horizon=("a decade",))
        self.exposure()
        self.hulten()
        self.readings()
        self.grid()

    def exposure(self):
        rows = VGroup(
            VGroup(label(r"80\%", font_size=54, color=MACH),
                   label(r"of American workers could have at least a tenth of their tasks affected by language "
                         r"models", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.4),
            VGroup(label(r"19\%", font_size=54, color=WORK),
                   label(r"at least half of their tasks", font_size=20, color=GREY_A)).arrange(RIGHT, buff=0.4),
            VGroup(label(r"$\uparrow$", font_size=54, color=GDP),
                   label(r"exposure rises with pay: \ the reverse of the robots", font_size=20,
                         color=GREY_A)).arrange(RIGHT, buff=0.4),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).move_to(UP * 0.2)
        for r in rows:
            if r.width > 12.4:
                r.scale_to_fit_width(12.4)
        caveat = label(r"exposure is a possibility, \ judged task by task: \ not adoption, \ not a forecast",
                       font_size=20, color=HOLD).to_edge(DOWN, buff=0.6)
        tag = published_tag(r"Eloundou, \ Manning, \ Mishkin and Rock, \ Science 384 (2024); \ O*NET task "
                            r"lists", corner=DL, font_size=12)
        head = label(r"how many tasks could a language model touch?", font_size=28, color=E.ACCENT).to_edge(
            UP, buff=0.5)
        how = label(r"every task in the American occupational database \ (O*NET), \ rated by people and by a "
                    r"model: \ could it be done in half the time?", font_size=19, color=GREY_A).next_to(head, DOWN,
                                                                                                     buff=0.3)
        with self.voiceover(
            "To go from a task to the economy, first ask how many tasks AI could touch. Tyna Eloundou, Sam "
            "Manning, Pamela Mishkin and Daniel Rock rated every task in the American occupational database, "
            "with human raters and with a model, asking whether a language model could cut the time it takes by "
            "half. <bookmark mark='a'/> About eighty percent of American workers, they found, could have at least "
            "a tenth of their tasks affected; <bookmark mark='b'/> about nineteen percent, at least half. <bookmark "
            "mark='c'/> And exposure rises with pay, the opposite of the robots, which reached the factory floor "
            "first. <bookmark mark='d'/> But exposure is a judgement that a task could be sped up. It is not "
            "adoption, and it is not a forecast of jobs lost."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(head), FadeIn(how))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(caveat))
        self.clear_scene()

    def hulten(self):
        H = load("hulten")["rows"][0]
        eq = MathTex(r"\Delta\ln\text{TFP}", r"\;=\;", r"\text{share of GDP in tasks made cheaper}", r"\times",
                     r"\text{average cost saving}", font_size=34).to_edge(UP, buff=0.5)
        eq[2].set_color(MACH)
        eq[4].set_color(GDP)
        steps = [
            (rf"{100 * H['exposed']:.0f}\%", r"of tasks exposed", r"Eloundou et al.", MACH),
            (rf"$\times$ \ {100 * H['adopted']:.0f}\%", r"of those worth doing with AI within ten years",
             r"Svanberg, \ Thompson et al.", MACH),
            (rf"$=$ \ {100 * H['share']:.1f}\%", r"of GDP in tasks made cheaper", r"", MACH),
            (rf"$\times$ \ {100 * H['cost_saving']:.1f}\%", rf"cost saving: \ {100 * H['saving']:.0f}\% of the "
             rf"labour cost, \ labour {100 * 0.535:.1f}\% of those tasks' costs", r"the experiments", GDP),
            (rf"$=$ \ {100 * H['tfp']:.2f}\%", r"higher TFP after ten years: \ about 0.07 points a year",
             r"", E.ACCENT),
        ]
        rows = VGroup()
        for big, txt, src, c in steps:
            r = VGroup(label(big, font_size=34, color=c), label(txt, font_size=19, color=GREY_A))
            r.arrange(RIGHT, buff=0.35)
            if src:
                r.add(label(rf"({src})", font_size=14, color=GREY_B).next_to(r, RIGHT, buff=0.25))
            rows.add(r)
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(eq, DOWN, buff=0.55)
        if rows.width > 12.8:
            rows.scale_to_fit_width(12.8)
        tag = published_tag(r"Acemoglu, \ \emph{The Simple Macroeconomics of AI}, \ NBER WP 32487 (2024); "
                            r"\ Economic Policy 40 (2025)", corner=DL, font_size=12)
        with self.voiceover(
            "Then use the theorem of Part sixty-three. Hulten's theorem says that, to a first approximation, a "
            "saving in some part of the economy raises total factor productivity by the share of GDP it touches "
            "times the saving. <bookmark mark='a'/> Daron Acemoglu did this arithmetic in 2024. <bookmark "
            "mark='b'/> About a fifth of tasks are exposed. <bookmark mark='c'/> Of "
            "those, he took about twenty-three percent as worth doing with AI within ten years, from a study of "
            "when computer vision pays. <bookmark mark='d'/> That is about four and a half percent of GDP. "
            "<bookmark mark='e'/> From the experiments, a saving of about twenty-seven percent of labour costs, "
            "and labour is a little over half of those tasks' costs: a cost saving of about fourteen percent. "
            "<bookmark mark='f'/> Multiply: about two thirds of one percent higher productivity, after ten years. "
            "Less than a tenth of a percentage point a year. Allowing for harder tasks, his estimate falls to about "
            "half a percent."
        ) as vo:
            self.play(FadeIn(tag), Write(eq))
            vo.wait_until("a")
            self.play(Indicate(eq[2], color=MACH, scale_factor=1.03), Indicate(eq[4], color=GDP, scale_factor=1.03))
            for mk, r_ in zip("bcdef", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.15))
        self.clear_scene()

    def readings(self):
        R = load("hulten")["rows"]
        ax = plane([-0.6, 2.6], [0, 12], center=LEFT * 2.6 + DOWN * 0.4, x_length=6.0, y_length=4.6, xticks=[],
                   yticks=[0, 3, 6, 9, 12], ylabel=r"higher TFP after ten years, \ \%", yfmt=lambda v: f"{v:.0f}",
                   font_size=14)
        cols = [GDP, MACH, IDEA]
        b = bars(ax, range(3), [100 * r["tfp"] for r in R], cols, width=0.6)
        names = VGroup(*[label(r["name"], font_size=14, color=c).next_to(ax.ax.c2p(k, 0), DOWN, buff=0.15)
                         for k, (r, c) in enumerate(zip(R, cols))])
        vals = VGroup(*[label(rf"{100 * r['tfp']:.1f} \ ({100 * r['per_year']:.2f} a year)", font_size=14,
                              color=c).next_to(bb, UP, buff=0.08) for bb, r, c in zip(b, R, cols)])
        side = VGroup(
            label(r"the large forecasts:", font_size=19, color=E.ACCENT),
            label(r"Goldman Sachs (2023): \ +1.5 points a year of US \\ labour productivity growth, \ for ten "
                  r"years", font_size=16, color=GREY_A),
            label(r"Aghion and Bunel (2024): \ +0.8 to 1.3 points a year, \\ from past general-purpose "
                  r"technologies", font_size=16, color=GREY_A),
            label(r"what separates them: \ how much is adopted, \\ how big the savings, \ and whether AI also "
                  r"speeds \\ up the invention of new things", font_size=16, color=WORK),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(ax.ax, RIGHT, buff=0.6)
        tag = published_tag(r"Briggs and Kodnani, \ Goldman Sachs (2023); \ Aghion and Bunel, \ \emph{AI and "
                            r"Growth: \ Where Do We Stand?} (2024); \ agora.automation.hulten\_scenarios",
                            corner=DL, font_size=12)
        with self.voiceover(
            "Other forecasts are many times larger. <bookmark mark='a'/> Joseph Briggs and Devesh Kodnani at "
            "Goldman Sachs projected one and a half percentage points a year of extra American labour productivity "
            "growth, for a decade, with wide adoption. Philippe Aghion and Simon Bunel, reasoning from electricity "
            "and the computer, got between 0.8 and 1.3 points a year. <bookmark mark='b'/> The same arithmetic "
            "shows what separates them. <bookmark mark='c'/> Keep a fifth of tasks exposed, but let sixty percent "
            "of them adopt, at a saving of forty percent: "
            f"{100 * R[1]['tfp']:.1f} percent over ten years. <bookmark mark='d'/> Let half of all tasks be "
            f"exposed, and all of them adopt: {100 * R[2]['tfp']:.0f} percent, about one point a year. To get the "
            "large numbers, AI has to reach far more of the economy than today's experiments, or do something the "
            "formula leaves out: speed up the invention of new products and ideas. That is the subject of chapter "
            "eight."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(side[:3]))
            vo.wait_until("b")
            self.play(GrowFromEdge(b[0], DOWN), FadeIn(names[0]), FadeIn(vals[0]))
            vo.wait_until("c")
            self.play(GrowFromEdge(b[1], DOWN), FadeIn(names[1]), FadeIn(vals[1]))
            vo.wait_until("d")
            self.play(GrowFromEdge(b[2], DOWN), FadeIn(names[2]), FadeIn(vals[2]), FadeIn(side[3]))
        self.clear_scene()

    def grid(self):
        G = load("hulten")["grid"]
        ex, ad, tfp = np.array(G["exposed"]), np.array(G["adopted"]), 100 * np.array(G["tfp"])
        ax = plane([0.0, 0.65], [0.05, 1.05], center=LEFT * 1.6 + DOWN * 0.3, x_length=7.4, y_length=4.8,
                   xticks=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6], yticks=[0.2, 0.4, 0.6, 0.8, 1.0],
                   xlabel=r"share of tasks exposed", ylabel=r"share of those adopted",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=14)
        dx, dy = ex[1] - ex[0], ad[1] - ad[0]
        cells = VGroup()
        vmax = tfp.max()
        for i, e in enumerate(ex):
            for j, a in enumerate(ad):
                p0, p1 = ax.ax.c2p(e - dx / 2, a - dy / 2), ax.ax.c2p(e + dx / 2, a + dy / 2)
                cells.add(Rectangle(width=p1[0] - p0[0], height=p1[1] - p0[1], stroke_width=0.5,
                                    stroke_color=BLACK, fill_color=heat(tfp[i, j], vmax),
                                    fill_opacity=0.95).move_to((p0 + p1) / 2))
        ace = dot(ax, 0.20, 0.23, WHITEC, 0.1)
        alab = label(r"Acemoglu", font_size=15, color=WHITEC).next_to(ace, RIGHT, buff=0.1)
        cont = VGroup(*[label(rf"{v:.0f}\%", font_size=13, color=BLACK if v > 0.5 * vmax else GREY_A).move_to(
            ax.ax.c2p(ex[i], ad[j])) for i in range(1, len(ex), 2) for j in range(1, len(ad), 2)
            for v in [tfp[i, j]]])
        side = label(r"higher TFP after ten years, \\ at a 27\% labour-cost saving", font_size=17,
                     color=GREY_A).next_to(ax.ax, RIGHT, buff=0.4)
        tag = island_tag(r"computed: \ agora.automation.hulten\_ai", corner=DL, font_size=12)
        with self.voiceover(
            "Here is the whole map, at the experiments' twenty-seven percent saving. <bookmark mark='a'/> Across, "
            "the share of tasks exposed; up, the share of those adopted; the colour, the gain in productivity after "
            "ten years. <bookmark mark='b'/> Acemoglu's inputs sit in the dark corner. <bookmark mark='c'/> The "
            "bright corner needs most of the economy to be exposed and nearly all of it to adopt. Where the economy "
            "lands is an empirical question, and the next decade's data will answer it. Watch the adoption share: "
            "it is the number the experiments cannot give."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in cells], lag_ratio=0.005), run_time=2.0)
            self.play(FadeIn(cont))
            vo.wait_until("b")
            self.play(FadeIn(ace, scale=1.5), FadeIn(alab))
            vo.wait_until("c")
            self.play(Indicate(cells[-1], scale_factor=1.0))
        self.clear_scene()
