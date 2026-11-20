from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class Top(VoiceoverScene):
    def construct(self):
        card(self, 3, r"A century of top incomes", r"What do the tax records say?",
             "Chapter three. A century of top incomes.", lit={1913: r"income tax", 2003: r"Piketty and Saez",
                                                                2024: r"Auten and Splinter"},
             scale=("nation", "world"), horizon=("a decade", "a century"))
        self.century()
        self.countries()
        self.dispute()

    def century(self):
        T = load("top")
        ys = np.array(T["years"])
        t10, t1 = np.array(T["top10"], float), np.array(T["top1"], float)
        ax = plane([1910, 2025], [0, 55], center=LEFT * 1.5 + DOWN * 0.4, x_length=9.2, y_length=4.9,
                   xticks=[1920, 1940, 1960, 1980, 2000, 2020], yticks=[0, 10, 20, 30, 40, 50],
                   ylabel=r"share of pre-tax income, \ excluding capital gains", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}\\%", font_size=14)
        m = np.isfinite(t10)
        l10 = path(ax, ys[m], t10[m], TOP, 3.2, smooth=False)
        l1 = path(ax, ys, t1, LOSS, 3.2, smooth=False)
        a = T["at"]
        side = VGroup(
            label(r"gold: \ the top 10\%", font_size=19, color=TOP),
            label(r"red: \ the top 1\%", font_size=19, color=LOSS),
            label(rf"1928: \ {a['1928']['top10']:.0f}\% \ and {a['1928']['top1']:.0f}\%", font_size=18, color=WHITE),
            label(rf"1970s: \ {a['1970']['top10']:.0f}\% \ and {a['1970']['top1']:.0f}\%", font_size=18,
                  color=WHITE),
            label(rf"2022: \ {a['2022']['top10']:.0f}\% \ and {a['2022']['top1']:.0f}\%", font_size=18, color=WHITE),
            label(r"a U, \ not a slow drift", font_size=19, color=E.ACCENT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_edge(RIGHT, buff=0.35)
        tag = data_tag(tables.PIKETTY_SAEZ_2003.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Surveys miss the top; tax records do not, at least for the income that is taxed. In 2003 Thomas Piketty "
            "and Emmanuel Saez used American income tax returns, which exist from 1913, to measure the shares of the "
            "top for ninety years, and Saez has kept the series going. <bookmark mark='a'/> The top ten percent's "
            f"share was {a['1928']['top10']:.0f} percent on the eve of the 1929 crash. It collapsed during the Second "
            "World War, and stayed near a third for four decades. <bookmark mark='b'/> The top one percent's share "
            f"fell from {a['1928']['top1']:.0f} percent to about {a['1970']['top1']:.0f}. <bookmark mark='c'/> Then, "
            f"from about 1980, both rose again: by 2022 the top ten percent took {a['2022']['top10']:.0f} percent, "
            f"and the top one percent {a['2022']['top1']:.0f}, back where they were in the 1920s. "
            "<bookmark mark='d'/> A U-shape over the century: the compression came fast, in war and depression, and "
            "the widening came within a generation."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            self.play(Create(l10), FadeIn(side[0]), run_time=2.5)
            vo.wait_until("a")
            self.play(FadeIn(side[2]))
            vo.wait_until("b")
            self.play(Create(l1), FadeIn(side[1]), FadeIn(side[3]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(side[4]))
            vo.wait_until("d")
            self.play(FadeIn(side[5]))
        self.clear_scene()

    def countries(self):
        T = load("top")
        W = T["wid"]
        ax = plane([1910, 2025], [0, 30], center=LEFT * 1.6 + DOWN * 0.4, x_length=9.0, y_length=4.9,
                   xticks=[1920, 1940, 1960, 1980, 2000, 2020], yticks=[0, 10, 20, 30],
                   ylabel=r"top 1\% share of pre-tax national income", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.0f}\\%", font_size=14)
        groups = (("United States", "United Kingdom"), ("France", "Sweden", "Germany"), ("China", "India", "Russia"))
        lines = []
        for g in groups:
            lines.append(VGroup(*[path(ax, W[c]["year"], W[c]["value"], COUNTRY[c], 3.0, smooth=False,
                                       xr=(1910, 2025), yr=(0, 30)) for c in g]))
        names = {"United States": "America", "United Kingdom": "Britain", "France": "France", "Sweden": "Sweden",
                 "Germany": "Germany", "China": "China", "India": "India", "Russia": "Russia"}
        side = VGroup(*[VGroup(*[label(names[c], font_size=18, color=COUNTRY[c]) for c in g]).arrange(
            RIGHT, buff=0.3) for g in groups])
        notes = VGroup(
            label(r"English-speaking: \ a U", font_size=17, color=GREY_A),
            label(r"continental Europe: \\ an L, \ a smaller rise", font_size=17, color=GREY_A),
            label(r"after reform and \\ opening: \ steep rises", font_size=17, color=GREY_A),
        )
        blocks = VGroup(*[VGroup(s_, n).arrange(DOWN, aligned_edge=LEFT, buff=0.1) for s_, n in zip(side, notes)])
        blocks.arrange(DOWN, aligned_edge=LEFT, buff=0.45).to_edge(RIGHT, buff=0.35).shift(UP * 0.4)
        tag = data_tag(r"World Inequality Database, \ via Our World in Data \ (years with sources)", corner=DR,
                       font_size=11)
        with self.voiceover(
            "The same method has now been applied in dozens of countries, gathered in the World Inequality "
            "Database. Its series measure all of national income, so their levels differ a little from the tax "
            "series. <bookmark mark='a'/> In America and Britain, the top one percent's share traces a U. "
            "<bookmark mark='b'/> In France, Sweden and Germany it fell just as far in the first half of the century, "
            "but rose much less afterwards: more an L than a U. The same technology reached all of them, so "
            "technology alone cannot explain the difference; Piketty and Saez point to taxes on top incomes and to "
            "how pay is set at the top. <bookmark mark='c'/> In China after 1978, India after 1991 and Russia after "
            "1991, the share rose steeply as markets opened: in Russia it went from under six percent in 1989 to over "
            "twenty by 2000; in India it more than doubled after 1991."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), run_time=1.0)
            for mk, k in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(Create(lines[k]), FadeIn(side[k]), FadeIn(notes[k]), run_time=2.0)
        self.clear_scene()

    def dispute(self):
        A = load("top")["as"]
        rows = [(r"top 1\% of fiscal income, \ tax units, \ 1962--2019", A["fiscal_2019"] - A["fiscal_1962"], TOP),
                (r"Piketty, \ Saez and Zucman: \ after taxes \\ and transfers, \ 1960--2019",
                 A["psz_after_2019"] - A["psz_after_1960"], LOSS),
                (r"Auten and Splinter: \ pre-tax, \\ early 1960s to 2019", A["as_pretax_pp"], BOTTOM),
                (r"Auten and Splinter: \ after taxes \\ and transfers, \ 1979--2019", A["as_aftertax_pp_1979"],
                 BOTTOM)]
        bars = VGroup()
        for k, (nm, v, col) in enumerate(rows):
            y = 1.6 - 1.15 * k
            r = Rectangle(width=v * 0.55, height=0.55, stroke_width=0, fill_color=col, fill_opacity=0.85).move_to(
                np.array([0.4 + v * 0.275, y, 0]))
            bars.add(VGroup(label(nm, font_size=18, color=WHITE).next_to(np.array([0.25, y, 0]), LEFT, buff=0.15),
                            r, label(f"+{v:g} points", font_size=19, color=col).next_to(r, RIGHT, buff=0.15)))
        head = label(r"how much did the top 1\% share rise? \ It depends what you count", font_size=26,
                     color=E.ACCENT).to_edge(UP, buff=0.45)
        foot = VGroup(
            label(r"at issue: \ income never reported on tax returns \ (whose is it?), \ the shift of business income "
                  r"onto individual returns after 1986, \ tax units against people", font_size=17, color=GREY_A),
        ).to_edge(DOWN, buff=0.45)
        tag = published_tag(tables.AUTEN_SPLINTER_2024.tag, corner=DR, font_size=10)
        with self.voiceover(
            "How much did the top really pull away? The measurement is disputed. <bookmark mark='a'/> On the income "
            f"reported on tax returns, the top one percent's share rose from {A['fiscal_1962']} to "
            f"{A['fiscal_2019']} percent between 1962 and 2019. But a third of that came around the tax reform of "
            "1986, when many business owners moved profits from corporate to personal returns; on one reading, much "
            "of that income moved rather than grew. <bookmark mark='b'/> Piketty, Saez and Zucman allocate all of "
            "national income, and "
            f"find the top share of income after taxes and transfers rising from {A['psz_after_1960']} to "
            f"{A['psz_after_2019']} percent. <bookmark mark='c'/> Gerald Auten and David Splinter, two government tax "
            "economists, make different assumptions about whose untaxed income it is, and "
            f"find a rise of only {A['as_pretax_pp']} points before tax since the early 1960s, "
            "<bookmark mark='d'/> and "
            f"{A['as_aftertax_pp_1979']} points after taxes and transfers since 1979. <bookmark mark='e'/> Both sides "
            "use the same tax returns. They differ over income that no return records, such as retained profits and "
            "underreported business income, and over how to count transfers. Whoever is right, the lesson is that a "
            "top share is a construction, and the assumptions belong on the label."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for mk, b_ in zip("abcd", bars):
                vo.wait_until(mk)
                self.play(FadeIn(b_, shift=RIGHT * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
