from __future__ import annotations

from videos.economics.econ26.common import *  # noqa: F403

PANICS = ((r"Dec 1930: \\ Bank of United States", 1930.5, 400),
          (r"spring 1931", 1931.3, 260),
          (r"Oct 1931: \\ after Britain \\ leaves gold", 1931.35, 470),
          (r"early 1933", 1932.75, 330))


class Evidence(VoiceoverScene):
    def construct(self):
        card(self, 11, r"Runs in the data", r"Were the runs panics, \ or bad banks found out?", "Chapter eleven. "
             "Runs in the data.", lit={2003: r"Calomiris and Mason", 2024: r"Jiang, Matvos, Piskorski and Seru"},
             scale=("firm", "nation"), horizon=("a month", "years"))
        self.depression()
        self.verdict()
        self.uninsured()

    def depression(self):
        s = load("suspensions")
        t, v = np.array(s["m_t"]), np.array(s["monthly"])
        k = t >= 1929.0
        ax = plane([1929, 1933.2], [0, 560], center=LEFT * 0.6 + DOWN * 0.4, x_length=10.4, y_length=4.8,
                   xticks=[1929, 1930, 1931, 1932, 1933], yticks=[0, 100, 200, 300, 400, 500],
                   ylabel=r"US banks suspended, \ a month", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}",
                   font_size=16)
        bars = VGroup()
        for x, y in zip(t[k], v[k]):
            lo, hi = ax.ax.c2p(x + 1 / 24, 0), ax.ax.c2p(x + 1 / 24, max(y, 2))
            bars.add(Rectangle(width=0.16, height=hi[1] - lo[1], fill_color=RUN, fill_opacity=0.8,
                               stroke_width=0).move_to((lo + hi) / 2))
        tags = VGroup()
        for say, x, y in PANICS:
            tags.add(label(say, font_size=15, color=STAY).move_to(ax.ax.c2p(x, y)))
        tag = data_tag(r"NBER Macrohistory Database: \ number of suspended banks, \ all banks, \ monthly, \ via FRED",
                       corner=DR, font_size=12)
        oct31 = int(v[np.argmin(np.abs(t - 1931.75))])
        with self.voiceover(
            "Were the runs of the Great Depression panics, sunspots in Diamond and Dybvig's sense, or were bad "
            "banks simply found out? Here are American bank suspensions month by month, from 1929 to February 1933. "
            "<bookmark mark='a'/> Milton Friedman and Anna Schwartz picked out four banking crises. The first came "
            "at the end of 1930, when the Bank of United States, a large New York bank, closed in December. "
            "<bookmark mark='b'/> The second in the spring and summer of 1931. <bookmark mark='c'/> The third after "
            f"Britain left the gold standard in September 1931: {oct31} banks were suspended in October alone. "
            "<bookmark mark='d'/> And the last in early 1933, which ended with every bank in the country closed by "
            "the banking holiday of March."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), LaggedStart(*[GrowFromEdge(b, DOWN) for b in bars], lag_ratio=0.02),
                      run_time=2.5)
            for mk, r_ in zip("abcd", tags):
                vo.wait_until(mk)
                self.play(FadeIn(r_))
        self.clear_scene()

    def verdict(self):
        rows = VGroup(
            label(r"Calomiris and Mason, \ 2003: \ a model of each Fed member bank's failure risk", font_size=24,
                  color=E.ACCENT),
            label(r"its fundamentals: \ the bank's balance sheet, \ and its county's economy", font_size=22,
                  color=GREY_A),
            label(r"1930 and spring 1931: \ no unexplained rise in failures", font_size=23, color=LOAN),
            label(r"autumn 1931: \ ambiguous, \ and small in total", font_size=23, color=GREY_A),
            label(r"early 1933: \ a large unexplained rise: \ a panic", font_size=23, color=RUN),
            label(r"mostly bad banks found out, \ with local contagion, \ until the end", font_size=23,
                  color=STAY),
        ).arrange(DOWN, buff=0.38).move_to(UP * 0.1)
        tag = published_tag(r"Calomiris and Mason, \ AER 93(5) (2003): \ 1615--1647", corner=DR, font_size=12)
        with self.voiceover(
            "Charles Calomiris and Joseph Mason tested the question bank by bank. <bookmark mark='a'/> They built a "
            "model of each Federal Reserve member bank's risk of failing, <bookmark mark='b'/> from its own balance "
            "sheet and the state of its county's economy. Then they looked for failures the fundamentals could not "
            "explain. <bookmark mark='c'/> In the crises of 1930 and the spring of 1931, they found none: banks "
            "failed when their fundamentals said they would. <bookmark mark='d'/> In the autumn of 1931 the "
            "evidence is ambiguous, and the unexplained part is small. <bookmark mark='e'/> In early 1933 there was a "
            "large unexplained rise in failures: a panic. <bookmark mark='f'/> So, mostly, weak banks were found out, "
            "with some contagion between neighbouring banks, until the very end. Fundamentals and runs work "
            "together, as the global game says they should."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def uninsured(self):
        s = load("svb")
        rows = VGroup(
            label(r"2023: \ Jiang, \ Matvos, \ Piskorski and Seru mark every American bank's assets to market",
                  font_size=22, color=E.ACCENT),
            label(r"after the rate rises of 2022: \ assets about \$2 trillion below book value, \ about 10\% on "
                  r"average", font_size=22, color=BOND),
            label(r"insured depositors have no reason to run: \ the loss threatens only if uninsured depositors "
                  r"leave", font_size=22, color=DEPOSIT),
            label(r"if half the uninsured withdrew: \ about 190 banks, \ with about \$300 billion of assets, \ could "
                  r"be impaired", font_size=22, color=RUN),
            label(rf"Silicon Valley Bank: \ large losses, \ and {100 * s['uninsured_share']:.0f}\% of deposits "
                  r"uninsured", font_size=23, color=RUN),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Jiang, \ Matvos, \ Piskorski and Seru, \ J.\ Financial Economics 159 (2024)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "In 2023 the same question came back. <bookmark mark='a'/> Erica Jiang, Gregor Matvos, Tomasz Piskorski "
            "and Amit Seru valued the assets of every American bank at market prices. <bookmark mark='b'/> After "
            "the rate rises of 2022, those assets were worth about two trillion dollars less than their book "
            "value, about ten percent on average. <bookmark mark='c'/> A loss like that need not sink a bank whose "
            "depositors are insured, because they have no reason to run. It matters when uninsured depositors can "
            "leave. <bookmark mark='d'/> If only half of the uninsured withdrew, they estimated, about a hundred "
            "and ninety banks, with about three hundred billion dollars of assets, could be left unable to pay "
            f"everyone. <bookmark mark='e'/> Silicon Valley Bank had large losses, and "
            f"{100 * s['uninsured_share']:.0f} "
            "percent of its deposits uninsured. Weak fundamentals made the run possible; the uninsured made it "
            "happen."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
