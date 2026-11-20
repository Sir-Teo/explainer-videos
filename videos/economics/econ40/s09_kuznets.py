from __future__ import annotations

from videos.economics.econ40.common import *  # noqa: F403


class Kuznets(VoiceoverScene):
    def construct(self):
        card(self, 7, r"Kuznets's curve", r"Does growth first widen inequality, \ then narrow it?",
             "Chapter seven. Kuznets's curve.", lit={1955: r"Kuznets"}, scale=("nation",),
             horizon=("a century",))
        self.dual()
        self.data()
        self.called()

    def dual(self):
        K = load("kuznets")
        sh, g = np.array(K["share"]), np.array(K["gini"])
        ax = plane([0, 1], [0.15, 0.5], center=LEFT * 2.0 + DOWN * 0.5, x_length=7.4, y_length=4.4,
                   xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=[0.2, 0.3, 0.4, 0.5],
                   xlabel=r"share of people in the modern sector", ylabel=r"Gini index",
                   xfmt=lambda v: f"{100 * v:.0f}\\%", yfmt=lambda v: f"{v:.1f}", font_size=14)
        ln = path(ax, sh, g, TOP, 3.4)
        k = int(np.argmax(g))
        ends = VGroup(dot(ax, sh[0], g[0], BOTTOM, 0.08), dot(ax, sh[k], g[k], TOP, 0.09),
                      dot(ax, sh[-1], g[-1], MIDDLE, 0.08))
        eq = MathTex(r"\mathrm{var}(\ln x) = s\,\sigma_m^2 + (1-s)\,\sigma_a^2 + s(1-s)\,\Delta^2",
                     font_size=30).to_edge(UP, buff=0.35)
        side = VGroup(
            label(rf"all on the land: \\ Gini {g[0]:.2f}", font_size=18, color=BOTTOM),
            label(rf"half moved: \\ Gini {g[k]:.2f}, \ the peak", font_size=18, color=TOP),
            label(rf"all in the cities: \\ Gini {g[-1]:.2f}", font_size=18, color=MIDDLE),
            label(r"the last term: \\ the gap between \\ sectors, \ largest \\ when $s$ is a half", font_size=17,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).to_edge(RIGHT, buff=0.35)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "In December 1954 Simon Kuznets gave his presidential address to the American Economic Association. "
            "His argument was arithmetic. Picture a country where most people farm, with low and fairly equal "
            "incomes, and a modern sector in the cities, with higher and more unequal ones. <bookmark mark='a'/> When "
            f"everyone farms, inequality is modest: on the Island, a Gini of {g[0]:.2f}. <bookmark mark='b'/> As "
            "people move to the cities, the gap between the sectors adds inequality, most of all when the population "
            f"is split in half: the Gini peaks at {g[k]:.2f}. <bookmark mark='c'/> When nearly everyone has moved, the "
            f"gap stops mattering, and the Gini falls back to {g[-1]:.2f}. <bookmark mark='d'/> The variance of log "
            "income makes the reason plain: the term for the gap between sectors is largest when the shares are "
            "equal. Growth first widens inequality, then narrows it: an inverted U."
        ) as vo:
            self.play(Write(eq), FadeIn(ax), FadeIn(tag), Create(ln), run_time=2.0)
            for mk, k_ in zip("abc", range(3)):
                vo.wait_until(mk)
                self.play(FadeIn(ends[k_], scale=1.5), FadeIn(side[k_]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]), Indicate(eq, color=E.ACCENT, scale_factor=1.03))
        self.clear_scene()

    def data(self):
        K = load("kuznets")
        ys, v = np.array(K["years"]), np.array(K["top10"])
        ax = plane([1915, 2025], [25, 55], center=LEFT * 1.6 + DOWN * 0.4, x_length=8.8, y_length=4.8,
                   xticks=[1920, 1940, 1960, 1980, 2000, 2020], yticks=[30, 35, 40, 45, 50, 55],
                   ylabel=r"top 10\% share of income", xfmt=lambda x: f"{x:.0f}", yfmt=lambda y: f"{y:.0f}\\%",
                   font_size=14)
        before = path(ax, ys[ys <= 1955], v[ys <= 1955], TOP, 3.4, smooth=False)
        after = path(ax, ys[ys >= 1955], v[ys >= 1955], GREY_B, 3.0, smooth=False)
        mark = vline(ax, 1955, 25, 55, E.ACCENT)
        ml = label(r"1955: \ Kuznets writes", font_size=17, color=E.ACCENT).next_to(ax.ax.c2p(1955, 55), DOWN,
                                                                                      buff=0.1).shift(RIGHT * 1.1)
        side = VGroup(
            label(rf"1928: \ {K['top10_1928']:.0f}\%", font_size=19, color=TOP),
            label(rf"1970: \ {K['top10_1970']:.0f}\%", font_size=19, color=GREY_B),
            label(rf"2022: \ {K['top10_2022']:.0f}\%", font_size=19, color=GREY_B),
            label(r"he saw the downslope; \\ the upslope came \\ after industry, \ not before", font_size=17,
                  color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.35)
        qc = quote_card(r"The paper is perhaps 5 per cent empirical information and 95 per cent speculation, \ "
                        r"some of it possibly tainted by wishful thinking.", r"Simon Kuznets (1955)", width=10.0)
        qc.move_to(UP * 0.3)
        tag = data_tag(tables.PIKETTY_SAEZ_2003.tag, corner=DR, font_size=11)
        with self.voiceover(
            "Kuznets was candid about his evidence: a few series for America, Britain and Germany. "
            "<bookmark mark='a'/> He called the paper perhaps five percent empirical information and ninety-five "
            "percent speculation. <bookmark mark='b'/> What he could see was the downslope: the American top ten "
            f"percent's share had fallen from {K['top10_1928']:.0f} percent in 1928. <bookmark mark='c'/> The tax "
            "records since show what came next: the share stayed low until the 1970s, <bookmark mark='d'/> then "
            f"climbed back to {K['top10_2022']:.0f} percent, long after America had finished industrializing. "
            "And the fall he saw was concentrated in depression and war, when capital incomes collapsed and taxes "
            "rose, not spread over decades of migration."
        ) as vo:
            self.play(FadeIn(qc, shift=DOWN * 0.1), run_time=1.0)
            vo.wait_until("a")
            self.play(Indicate(qc, color=WHITE, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeOut(qc), run_time=0.6)
            self.play(FadeIn(ax), FadeIn(tag), Create(before), Create(mark), FadeIn(ml), FadeIn(side[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(after), FadeIn(side[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(side[2]), FadeIn(side[3]))
        self.clear_scene()

    def called(self):
        c = calls.CALLS["kuznets_1955"]
        K = load("kuznets")
        cc = call_card(tex_safe(c.who), c.when, tex_safe(c.said), tex_safe(c.outcome), c.verdict, width=12.6,
                       font_size=21)
        foot = label(rf"America's top 10\%: \ {K['top10_1928']:.0f}\% in 1928, \ {K['top10_1970']:.0f}\% in 1970, \ "
                     rf"{K['top10_2022']:.0f}\% in 2022", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.5)
        tag = published_tag(tables.KUZNETS_1955.tag + r"; \ Piketty and Saez", corner=DR, font_size=12)
        with self.voiceover(
            "Called it? <bookmark mark='a'/> In 1954 Kuznets predicted that inequality widens in the early phases "
            "of growth, as people leave the land, and narrows later. <bookmark mark='b'/> In rich countries "
            "inequality did narrow until the 1970s, but mostly through depression, war and policy, not migration; "
            "and from about 1980 it widened again in America and Britain, long after industrialization. Within "
            "countries that are still urbanizing, his arithmetic still bites. <bookmark mark='c'/> The verdict: "
            "partly right. The mechanism is real; the law is not."
        ) as vo:
            self.play(FadeIn(cc.card), FadeIn(cc[1]), FadeIn(tag))
            vo.wait_until("b")
            self.play(Indicate(cc.right, color=WHITE, scale_factor=1.01), FadeIn(foot))
            vo.wait_until("c")
            self.play(FadeIn(cc.stamp, scale=1.3))
        self.clear_scene()
