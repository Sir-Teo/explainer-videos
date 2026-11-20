from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Harder(VoiceoverScene):
    def construct(self):
        card(self, 6, r"Are ideas getting harder to find?", r"If growth rises with the number of researchers, \ why "
             r"hasn't it?", "Chapter six. Are ideas getting harder to find?",
             lit={1995: r"Jones", 2020: r"Bloom, Jones, Van Reenen, Webb"}, scale=("nation", "world"),
             horizon=("a century",))
        self.call()
        self.bloom()
        self.semi()

    def call(self):
        c = calls.CALLS["romer_scale"]
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.4,
                       font_size=21).move_to(UP * 0.1)
        tag = published_tag(r"Romer, JPE 98(5) (1990), \ abstract; \ Jones, QJE 110(2) (1995)", corner=DR,
                            font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> Romer's abstract of 1990 says it plainly: the stock of human capital "
            "determines the rate of growth. Put more people into research and the economy grows faster, for ever. "
            "<bookmark mark='b'/> After the Second World War the rich countries did exactly that. The number of "
            "scientists and engineers doing research multiplied. Growth did not. In 1995 Charles Jones showed that "
            "American growth had no persistent rise to match, and rejected the scale effect. "
            "<bookmark mark='c'/> As a forecast of what more researchers would do: wrong. The theory survived, but "
            "only by admitting that ideas get harder to find."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()

    def bloom(self):
        b = load("bloom")
        rows = VGroup(
            MathTex(r"\underbrace{\frac{\dot A}{A}}_{\text{growth}} \;=\; "
                    r"\underbrace{\alpha}_{\text{research productivity}} \;\times\; "
                    r"\underbrace{S}_{\text{effective researchers}}", font_size=44),
        ).move_to(UP * 2.2)
        bars = VGroup()
        specs = [(r"effective researchers, \ US, \ 1930s to 2010s", b["effort_factor"], RESEARCH, r"$\times$"),
                 (r"research productivity, \ same period", b["productivity_factor"], WEDGE, r"$\div$"),
                 (r"researchers to keep Moore's law going, \ since the early 1970s", b["moore_factor"], IDEA,
                  r"$\times$")]
        for i, (name, v, col, op) in enumerate(specs):
            w = 6.0 * np.log10(v) / np.log10(45)
            y = 0.6 - i * 1.0
            bar = Rectangle(width=w, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                [-1.2 + w / 2, y, 0])
            nm = label(name, font_size=19, color=GREY_A).next_to(bar, UP, buff=0.08).align_to(bar, LEFT)
            val = label(rf"{op}{v}", font_size=26, color=col).next_to(bar, RIGHT, buff=0.2)
            bars.add(VGroup(bar, nm, val))
        foot = label(rf"aggregate research productivity falls about {100 * b['aggregate_decline']:.1f}\% a year: \ it "
                     rf"halves every {b['half_life']} years", font_size=22, color=E.ACCENT).to_edge(DOWN, buff=0.7)
        tag = published_tag(tables.BLOOM_2020.tag + r", \ AER 110(4)", corner=DR, font_size=12)
        with self.voiceover(
            "In 2020 Nicholas Bloom, Charles Jones, John Van Reenen and Michael Webb measured how hard. "
            "<bookmark mark='a'/> Write growth as research productivity times the number of effective researchers. "
            "Both can be measured. <bookmark mark='b'/> For the American economy, the effective number of "
            f"researchers rose about {b['effort_factor']} times from the 1930s to the 2010s, about "
            f"{100 * b['effort_growth']:.1f} percent a year. Productivity growth did not rise. "
            f"<bookmark mark='c'/> So research productivity fell about {b['productivity_factor']} times. "
            "<bookmark mark='d'/> Inside one industry the pattern is the same: keeping Moore's law going, the "
            f"doubling of chip density every two years, takes more than {b['moore_factor']} times as many "
            "researchers as in the early 1970s. <bookmark mark='e'/> Across their cases, research productivity "
            f"falls about {100 * b['aggregate_decline']:.0f} percent a year, halving every {b['half_life']} years. "
            "The economy has to double its research effort every thirteen years just to keep growing at the same "
            "rate."
        ) as vo:
            self.play(FadeIn(tag), Write(rows[0]))
            vo.wait_until("a")
            for mk, br in zip("bcd", bars):
                vo.wait_until(mk)
                self.play(GrowFromEdge(br[0], LEFT), FadeIn(br[1]), FadeIn(br[2]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()

    def semi(self):
        s = load("semi")
        t = np.array(s["t"], float)
        ax = plane([0, 200], [0, 0.05], center=LEFT * 1.6 + DOWN * 0.45, x_length=8.4, y_length=4.6,
                   xticks=[0, 50, 100, 150, 200], yticks=[0, 0.01, 0.02, 0.03, 0.04, 0.05], xlabel=r"years",
                   ylabel=r"growth of ideas a year", yfmt=lambda v: f"{100 * v:.0f}\\%", font_size=16)
        gl = path(ax, t, s["gA"], color=IDEA, width=4, smooth=False)
        lr = DashedLine(ax.ax.c2p(0, s["long_run"]), ax.ax.c2p(200, s["long_run"]), color=CONS, stroke_width=2)
        p = s["params"]
        side = VGroup(
            MathTex(r"\dot A = \theta\, S^{\lambda} A^{\phi}, \quad \phi < 1", font_size=36),
            label(r"each idea makes the next one harder \\ when $\phi < 1$", font_size=19, color=GREY_A),
            MathTex(r"g_A \to \frac{\lambda n}{1-\phi}", font_size=40, color=CONS),
            label(rf"researchers grow {pc(p['n'])} a year, \\ $1-\phi = {1 - p['phi']:g}$: \ "
                  rf"$g_A \to {pc(s['long_run'])}$", font_size=19, color=CONS),
            label(r"growth now depends on the growth \\ of researchers, \ not their number", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.3)
        tag = agora_tag(corner=DR, font_size=14)
        with self.voiceover(
            "Jones's repair is called semi-endogenous growth. <bookmark mark='a'/> New ideas still come from "
            "researchers, but the ideas already found make the next ones harder to find whenever phi is below one. "
            "<bookmark mark='b'/> Run it with researchers growing as fast as Bloom and his co-authors measured, "
            f"{100 * p['n']:.1f} percent a year, and ideas getting harder at the rate their numbers imply. "
            "<bookmark mark='c'/> Wherever it starts, growth of ideas settles at lambda n over one minus phi, here "
            f"about {100 * s['long_run']:.1f} percent a year, the order of America's long-run productivity growth. "
            "<bookmark mark='d'/> The scale effect is gone. Growth no longer depends on how many researchers there "
            "are, but on how fast their number grows, which in the long run means how fast the population grows. "
            "Hold that thought until the frontier."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(side[1]))
            vo.wait_until("b")
            self.play(Create(gl), run_time=3)
            vo.wait_until("c")
            self.play(Create(lr), FadeIn(side[2]), FadeIn(side[3]))
            vo.wait_until("d")
            self.play(FadeIn(side[4]))
        self.clear_scene()
