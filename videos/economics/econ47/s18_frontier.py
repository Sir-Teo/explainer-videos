from __future__ import annotations

from videos.economics.econ47.common import *  # noqa: F403

BACK_COLS = {"Hungary": "#F2C14E", "Turkey": "#F25F5C", "Venezuela": "#C9A0FF", "Russia": "#7EC8F5"}


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 16, r"Frontier: \ populism and the digital state", r"What is still being worked out?",
             "Chapter sixteen. Frontier: populism, and the digital state.",
             lit={2016: r"Muralidharan, Niehaus and Sukhtankar", 2023: r"Funke, Schularick and Trebesch"},
             scale=("nation", "world"), horizon=("a decade",))
        self.backsliding()
        self.populism()
        self.digital()

    def backsliding(self):
        D = load("democracy")
        W = D["world"]
        ax = plane([1985, 2026], [0, 1], center=LEFT * 1.7 + DOWN * 0.35, x_length=8.6, y_length=4.6,
                   xticks=[1990, 2000, 2010, 2020], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                   ylabel=r"V-Dem's electoral democracy index", xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.2f}",
                   font_size=14)
        lines, names = VGroup(), VGroup()
        for c, d in D["backslid"].items():
            ys = [y for y in d["year"] if y >= 1985]
            vs = [v for y, v in zip(d["year"], d["value"]) if y >= 1985]
            lines.add(path(ax, ys, vs, BACK_COLS[c], 2.6, smooth=False))
            names.add(label(rf"{c}: \ {d['peak']:.2f} at best, \ {d['last']:.2f} now", font_size=15,
                            color=BACK_COLS[c]))
        wy = [y for y in W["year"] if y >= 1985]
        wv = [v for y, v in zip(W["year"], W["value"]) if y >= 1985]
        world = path(ax, wy, wv, WHITE, 3.4, smooth=False)
        names.add(label(r"white: \ the world's average", font_size=15, color=WHITE))
        names.arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(RIGHT, buff=0.3)
        tag = data_tag(r"V-Dem Institute, \ Democracy Report v16 (2026), \ via Our World in Data", corner=DL,
                       font_size=12)
        with self.voiceover(
            "The first frontier is a reversal. <bookmark mark='a'/> After 1990, the world's average on V-Dem's "
            "index rose for two decades, and has fallen since about 2012. <bookmark mark='b'/> Some countries moved "
            "back a long way: Hungary, Turkey, Venezuela and Russia, each led for years by leaders who won "
            "elections and then weakened the courts, the press and the opposition. "
            "Economists are trying to understand why voters support this, and what it costs."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            vo.wait_until("a")
            self.play(Create(world), FadeIn(names[-1]), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[Create(ln) for ln in lines], lag_ratio=0.3), FadeIn(names[:-1]), run_time=3.5)
        self.clear_scene()

    def populism(self):
        T = tables.FRONTIER47.data
        rows = VGroup(
            label(rf"Funke, \ Schularick and \\ Trebesch, \ 2023: \\ {T['leaders']} populist presidents \\ and prime "
                  r"ministers, \ 1900--2020", font_size=19, color=WHITE),
            label(r"a populist: \ ``the people'' \\ against ``the elite'', \\ from the left or the right",
                  font_size=19, color=GREY_A),
            label(rf"after {T['years']} years, \ GDP per head \\ about {T['loss']}\% below a \\ plausible "
                  r"non-populist path", font_size=21, color=LOSS),
            label(r"with less trade, \\ less macroeconomic stability \\ and weaker institutions", font_size=19,
                  color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        head = label(r"the economics of populism", font_size=30, color=E.ACCENT).to_edge(UP, buff=0.5)
        ax = plane([0, 15], [-12, 2], center=LEFT * 2.4 + DOWN * 0.4, x_length=6.6, y_length=4.4,
                   xticks=[0, 5, 10, 15], yticks=[-12, -8, -4, 0], xlabel=r"years after a populist takes office",
                   ylabel=r"GDP per head, \ \% against a comparable path",
                   xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}".replace("-", "{-}") if v else "0",
                   font_size=14)
        zero = DashedLine(ax.ax.c2p(0, 0), ax.ax.c2p(15, 0), color=GREY_B, stroke_width=1.4)
        ts = np.linspace(0, 15, 31)
        sketch = path(ax, ts, -T["loss"] * ts / T["years"], LOSS, 3.2, smooth=False)
        pin = dot(ax, T["years"], -T["loss"], E.ACCENT, 0.09)
        pin_l = label(rf"about {T['loss']}\% lower \\ after {T['years']} years", font_size=17,
                      color=E.ACCENT).next_to(pin, UL, buff=0.1)
        note = label(r"a sketch of the shape, \ not the published estimates year by year", font_size=14,
                     color=GREY_B).next_to(ax, DOWN, buff=0.55)
        tag = published_tag(tables.FRONTIER47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "What does populism cost? <bookmark mark='a'/> Manuel Funke, Moritz Schularick and Christoph Trebesch "
            f"assembled {T['leaders']} populist presidents and prime ministers, from 1900 to 2020, <bookmark "
            "mark='b'/> defining populists as leaders who claim to speak for the people against a corrupt elite, "
            "whether from the left or the right. <bookmark mark='c'/> Fifteen years after such a leader takes "
            f"office, GDP per head is about {T['loss']} percent below a comparable path without one. <bookmark "
            "mark='d'/> The losses come with less trade, less stable macroeconomic policy, and weaker "
            "institutions. Why voters choose such leaders anyway, after crises, trade shocks and the rest of this "
            "part's forces, is the open question."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0], shift=RIGHT * 0.1), FadeIn(ax), Create(zero),
                      FadeIn(note))
            vo.wait_until("a")
            self.play(Indicate(rows[0], color=WHITE, scale_factor=1.03))
            for mk, r_ in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.1))
                if mk == "c":
                    self.play(Create(sketch), run_time=2.5)
                    self.play(FadeIn(pin), FadeIn(pin_l))
        self.clear_scene()

    def digital(self):
        T = tables.FRONTIER47.data
        chain = flow_chain([(r"payments through \\ local officials", CORRUPT), (r"a biometric card, \\ a local agent",
                                                                                AUDIT),
                            (r"faster, \ more \\ predictable", GAIN), (r"less leakage", GAIN)],
                           notes=[r"employment and \\ pension programmes", rf"rolled out at random: \\ "
                                                                           rf"{T['subdistricts']} sub-districts, "
                                                                           rf"\\ {T['people_m']} million people",
                                  r"and preferred by \\ the people paid", r"and the time saved \\ paid for it"],
                           box_w=2.8, font_size=19, note_size=16).move_to(UP * 0.8)
        foot = label(r"the digital state: \ identity, \ payments and records that are harder to steal from, \\ "
                     r"and new questions of privacy and exclusion", font_size=20, color=E.ACCENT).to_edge(DOWN,
                                                                                                  buff=0.8)
        tag = published_tag(tables.FRONTIER47.tag, corner=DR, font_size=11)
        with self.voiceover(
            "The second frontier is the digital state. <bookmark mark='a'/> In the Indian state of Andhra Pradesh, "
            "payments for a public employment programme and for pensions passed through local officials, and much "
            "of the money leaked. <bookmark mark='b'/> The state introduced biometric smartcards, paid out by "
            "local agents, and Karthik Muralidharan, Paul Niehaus and Sandip Sukhtankar evaluated the roll-out, "
            f"randomized across {T['subdistricts']} sub-districts with about {T['people_m']} million people. "
            "<bookmark mark='c'/> Payments became faster and more predictable, and beneficiaries preferred the new "
            "system. <bookmark mark='d'/> Leakage fell significantly, and the time saved alone was worth about what "
            "the system cost. State capacity, in this frontier, is built from identity systems, digital payments and "
            "records, which raise their own questions about privacy, and about who gets left out."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(chain.boxes[0]), run_time=1.0)
            vo.wait_until("a")
            self.play(FadeIn(chain.notes[0]))
            for k, mk in enumerate("bcd"):
                vo.wait_until(mk)
                self.play(GrowArrow(chain.arrows[k]), FadeIn(chain.boxes[k + 1]), FadeIn(chain.notes[k + 1]))
            self.play(FadeIn(foot))
        self.clear_scene()
