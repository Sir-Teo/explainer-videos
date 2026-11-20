from __future__ import annotations

from videos.economics.econ20.common import *  # noqa: F403


class Kaldor(VoiceoverScene):
    def construct(self):
        card(self, 1, r"Kaldor's six facts, \ checked", r"Do the facts of growth listed in 1961 still hold in the data?",
             "Chapter one. Kaldor's six facts, checked.", lit={1961: r"Kaldor's list", 2025: r"PWT 11.0"},
             scale=("nation", "world"), horizon=("decades",))
        self.six()
        self.verdict()

    def panel(self, k, x_range, y_range, yticks, ylabel, center, yfmt=None, log=False):
        ax = plane(x_range, y_range, center=center, x_length=3.7, y_length=1.9, xticks=[1960, 1990, 2020],
                   yticks=yticks, ylabel=ylabel, xfmt=lambda v: f"{v:.0f}", yfmt=yfmt, font_size=13)
        return ax

    def six(self):
        k = load("kaldor")
        yrs = k["years"]
        cols = [LEFT * 4.55, LEFT * 0.1, RIGHT * 4.35]
        top, bot = UP * 1.35, DOWN * 2.05
        base_y = k["ypw"][0]
        a1 = self.panel(k, [1948, 2025], [0, np.log10(4)], [0, np.log10(2), np.log10(4)],
                        r"output per worker \ (1950 = 1, \ log)", cols[0] + top,
                        yfmt=lambda v: f"{10 ** v:.0f}")
        l1 = path(a1, yrs, [np.log10(v / base_y) for v in k["ypw"]], color=OUTPUT, width=3, smooth=False)
        base_k = k["kpw"][0]
        a2 = self.panel(k, [1948, 2025], [0, np.log10(4)], [0, np.log10(2), np.log10(4)],
                        r"capital per worker \ (1950 = 1, \ log)", cols[1] + top,
                        yfmt=lambda v: f"{10 ** v:.0f}")
        l2 = path(a2, yrs, [np.log10(v / base_k) for v in k["kpw"]], color=CAPITAL, width=3, smooth=False)
        a3 = self.panel(k, [1948, 2025], [0, 0.15], [0, 0.05, 0.10, 0.15], r"return on capital", cols[2] + top,
                        yfmt=lambda v: f"{100 * v:.0f}\\%")
        l3 = path(a3, k["irr_years"], k["irr"], color=RATE, width=3, smooth=False)
        a4 = self.panel(k, [1948, 2025], [0, 5], [0, 1, 2, 3, 4, 5], r"capital $\div$ output", cols[0] + bot)
        l4 = path(a4, yrs, k["ky"], color=BREAK, width=3, smooth=False)
        a5 = self.panel(k, [1948, 2025], [0, 0.8], [0, 0.2, 0.4, 0.6, 0.8], r"labour's share of income",
                        cols[1] + bot, yfmt=lambda v: f"{100 * v:.0f}\\%")
        l5 = path(a5, yrs, k["labsh"], color=LABOUR, width=3, smooth=False)
        cr = k["cross"]
        g = np.array(cr["growth"])
        a6 = plane([-0.03, 0.07], [0, 1], center=cols[2] + bot, x_length=3.7, y_length=1.9,
                   xticks=[-0.02, 0, 0.02, 0.04, 0.06], yticks=[], xfmt=lambda v: f"{100 * v:.0f}\\%",
                   ylabel=r"growth of GDP per head, \ 1960--2019", font_size=13)
        rng = np.random.default_rng(3)
        jit = 0.15 + 0.7 * rng.random(len(g))
        dots6 = VGroup(*[Dot(a6.ax.c2p(v, j), radius=0.035, color=OUTPUT) for v, j in zip(g, jit)])
        lab = [
            label(rf"{pc(k['g_ypw'])} a year", font_size=15, color=OUTPUT).move_to(a1.ax.c2p(1975, np.log10(3.2))),
            label(rf"{pc(k['g_kpw'])} a year", font_size=15, color=CAPITAL).move_to(a2.ax.c2p(1975, np.log10(3.2))),
            label(rf"{pc(k['irr_range'][0], 0)} to {pc(k['irr_range'][1], 0)}", font_size=15,
                  color=RATE).move_to(a3.ax.c2p(1985, 0.135)),
            label(rf"{k['ky_range'][0]:.1f} to {k['ky_range'][1]:.1f}", font_size=15,
                  color=BREAK).move_to(a4.ax.c2p(1985, 4.6)),
            label(rf"{pc(k['ls_1950_79'], 0)} $\to$ {pc(k['ls_2010_'], 0)}", font_size=15,
                  color=LABOUR).move_to(a5.ax.c2p(1985, 0.75)),
            label(rf"{cr['n']} countries", font_size=15, color=OUTPUT).move_to(a6.ax.c2p(-0.015, 0.95)),
        ]
        nums = VGroup(*[label(rf"{i}", font_size=20, color=E.ACCENT) for i in range(1, 7)])
        for n_, ax in zip(nums, (a1, a2, a3, a4, a5, a6)):
            n_.next_to(ax, LEFT, buff=0.12).align_to(ax, UP)
        head = label(r"Kaldor's facts \ (1961), \ the United States, \ 1950--2023", font_size=24,
                     color=GREY_A).to_edge(UP, buff=0.22)
        src = data_tag(r"Penn World Table 11.0 \ (Feenstra, Inklaar and Timmer): \ rgdpna, rnna, emp, irr, labsh",
                       corner=DR, font_size=11)
        lo_c, hi_c = COUNTRY.get(cr["lo"][0], (cr["lo"][0], OUTPUT))[0], COUNTRY.get(cr["hi"][0],
                                                                                    (cr["hi"][0], OUTPUT))[0]
        groups = [(a1, l1), (a2, l2), (a3, l3), (a4, l4), (a5, l5), (a6, dots6)]
        with self.voiceover(
            "In 1961 Nicholas Kaldor listed six facts of growth that any theory would have to explain. Part three "
            "entered them on the series' list. Here they are, checked on the newest Penn World Table. "
            "<bookmark mark='a'/> One. Output per worker grows at a roughly steady rate: in the United States, about "
            f"{100 * k['g_ypw']:.1f} percent a year since 1950, a little faster before 1985 than after. "
            "<bookmark mark='b'/> Two. Capital per worker grows too, at about the same rate, "
            f"{100 * k['g_kpw']:.1f} percent. <bookmark mark='c'/> Three. The return on capital shows no trend: "
            f"between about {100 * k['irr_range'][0]:.0f} and {100 * k['irr_range'][1]:.0f} percent a year for "
            "seventy years. <bookmark mark='d'/> Four. So the ratio of capital to output is roughly steady, between "
            f"{k['ky_range'][0]:.1f} and {k['ky_range'][1]:.1f} years of output. <bookmark mark='e'/> Five. The "
            f"shares of income are roughly steady: labour's was about {100 * k['ls_1950_79']:.0f} percent until "
            f"1980; since 2010 it has averaged about {100 * k['ls_2010_']:.0f}, the one fact that has slipped. "
            "<bookmark mark='f'/> And six. Growth rates differ enormously across countries. Over 1960 to 2019, "
            f"across {cr['n']} countries, from {say_pct(cr['lo'][1], 1)} a year in {lo_c} to "
            f"{100 * cr['hi'][1]:.1f} percent in {hi_c}."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src), *[FadeIn(ax) for ax, _ in groups], *[FadeIn(nm) for nm in nums],
                      run_time=1.5)
            for mk, (ax, ln), lb, nm in zip("abcdef", groups, lab, nums):
                vo.wait_until(mk)
                anim = Create(ln) if not isinstance(ln, VGroup) else LaggedStart(*[FadeIn(d) for d in ln],
                                                                                 lag_ratio=0.01)
                self.play(anim, Indicate(nm, color=WHITE), run_time=1.6)
                self.play(FadeIn(lb), run_time=0.5)
        self.clear_scene()

    def verdict(self):
        rows = VGroup(
            label(r"facts 1--4: \ the economy grows along a balanced path", font_size=26, color=OUTPUT),
            label(r"fact 5: \ held for decades; \ labour's share has fallen since about 2000 \ (Part 39)",
                  font_size=24, color=LABOUR),
            label(r"fact 6: \ countries are not on one path", font_size=26, color=E.ACCENT),
            label(r"the model to come explains 1--5 \ in one stroke, \ and 6 only partly", font_size=26,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "So, sixty years on: <bookmark mark='a'/> the first four facts still describe the richest economy: output "
            "and capital per worker grow together at a steady rate, with a steady return and a steady ratio of one to "
            "the other. Economists call that a balanced growth path. <bookmark mark='b'/> The fifth held for decades "
            "and has slipped since about 2000; part thirty-nine asks why. <bookmark mark='c'/> And the sixth says "
            "that countries are not all on one path. <bookmark mark='d'/> The model in chapter three explains the "
            "first five in a single stroke. The sixth is harder, and it is what the rest of this part is about."
        ) as vo:
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
