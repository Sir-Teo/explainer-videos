from __future__ import annotations

from videos.economics.econ22.common import *  # noqa: F403

NAMES = {"CHN": (r"China", "#F25F5C"), "USA": (r"United States", "#9FB8F2"), "JPN": (r"Japan", "#C9A0FF"),
         "KOR": (r"South Korea", "#F7D154"), "IND": (r"India", "#F29E8E"), "DEU": (r"Germany", "#B8C0CC")}


class China(VoiceoverScene):
    def construct(self):
        card(self, 12, r"The rich, \ bequests, \ and China", r"Why do the rich save so much, \ and why does China?",
             "Chapter twelve. The rich, bequests, and China.",
             lit={1981: r"Kotlikoff and Summers", 2004: r"Dynan, Skinner, Zeldes", 2011: r"Wei and Zhang"},
             scale=("household", "nation"), horizon=("a lifetime", "generations"))
        self.rich()
        self.china()
        self.why()

    def rich(self):
        rows = VGroup(
            label(r"do the rich save more? \ Friedman said only of transitory income", font_size=26, color=E.ACCENT),
            label(r"Karen Dynan, \ Jonathan Skinner and Stephen Zeldes, \ 2004: \ saving rates rise with "
                  r"\emph{lifetime} income too", font_size=22, color=SAVE),
            label(r"so Friedman explained part of Keynes's cross-section, \ not all of it", font_size=22,
                  color=GREY_A),
            label(r"why: \ bequests, \ wealth valued for itself \ (Christopher Carroll's capitalist spirit), \ "
                  r"and protection against old-age costs", font_size=22, color=GREY_A),
            label(r"how much wealth is inherited? \ Kotlikoff and Summers, \ 1981: \ about four-fifths; \ "
                  r"Modigliani, \ 1988: \ about a fifth", font_size=22, color=HOUSE),
            label(r"a debate about definitions as much as data, \ and still open", font_size=22, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Dynan, Skinner and Zeldes, JPE 112(2) (2004); \ Kotlikoff and Summers, JPE 89(4) "
                            r"(1981); \ Modigliani, JEP 2(2) (1988)", corner=DR, font_size=12)
        with self.voiceover(
            "Two pieces are still missing from the life cycle: the rich, and what people leave behind. "
            "<bookmark mark='a'/> Friedman's answer to Keynes said the rich only seem to save more, because a good "
            "year makes a household look rich. <bookmark mark='b'/> In 2004 Karen Dynan, Jonathan Skinner and "
            "Stephen Zeldes measured lifetime income more carefully, with education and income in other years, and "
            "found that saving rates rise with lifetime income too. <bookmark mark='c'/> So Friedman explained part "
            "of Keynes's cross-section, not all of it. <bookmark mark='d'/> Why would the lifetime rich save more? "
            "To leave bequests; because, as Christopher Carroll put it, wealth itself brings status and power, a "
            "capitalist spirit; and to guard against the costs of a long old age. <bookmark mark='e'/> How much of "
            "a nation's wealth is inherited rather than saved over a life? Laurence Kotlikoff and Lawrence Summers "
            "put it at about four-fifths in 1981; Modigliani, in 1988, at about a fifth. <bookmark mark='f'/> Much "
            "of the gap is about definitions, what counts as a transfer and how it grows, and it is still open."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def china(self):
        c = load("china")
        ax = plane([1970, 2020], [0.25, 0.8], center=LEFT * 1.5 + DOWN * 0.35, x_length=8.8, y_length=5.0,
                   xticks=[1970, 1980, 1990, 2000, 2010, 2020], yticks=[0.3, 0.4, 0.5, 0.6, 0.7, 0.8],
                   ylabel=r"household consumption, \ share of GDP", xfmt=lambda v: f"{v:.0f}",
                   yfmt=lambda v: f"{v:.1f}", font_size=16)
        lines = {k: path(ax, c["years"], c[k]["csh_c"], color=NAMES[k][1], width=5 if k == "CHN" else 3,
                         smooth=False) for k in NAMES}
        labs = VGroup(*[label(NAMES[k][0], font_size=17, color=NAMES[k][1]).next_to(
            ax.ax.c2p(2019, c[k]["csh_c"][-1]), RIGHT, buff=0.1) for k in NAMES])
        # keep the end labels apart
        order = sorted(range(len(labs)), key=lambda i: labs[i].get_center()[1])
        for a, b in zip(order[:-1], order[1:]):
            if labs[b].get_bottom()[1] < labs[a].get_top()[1] + 0.05:
                labs[b].shift(UP * (labs[a].get_top()[1] + 0.05 - labs[b].get_bottom()[1]))
        side = VGroup(
            label(rf"China: \ {c['chn_1990']:.2f} in 1990, \\ {c['chn_2010']:.2f} in 2010, \ {c['chn_2019']:.2f} "
                  rf"in 2019", font_size=19, color=NAMES["CHN"][1]),
            label(rf"United States: \ {c['usa_2019']:.2f}", font_size=19, color=NAMES["USA"][1]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).to_corner(UR, buff=0.4)
        tag = data_tag(r"Penn World Table 11.0: \ csh\_c, \ at current PPPs", corner=DR, font_size=12)
        with self.voiceover(
            "Now the largest saving puzzle of our time. <bookmark mark='a'/> Here is household consumption as a "
            "share of output, from the Penn World Table, for six economies. <bookmark mark='b'/> In the United "
            f"States it rose to about {c['usa_2019']:.2f}. <bookmark mark='c'/> In China it was "
            f"{c['chn_1990']:.2f} in 1990 and fell to {c['chn_2010']:.2f} by 2010, recovering only to "
            f"{c['chn_2019']:.2f}. Chinese households consumed about half as large a share of output as American "
            "households. Part of that is that households received a smaller share of income, as firms and the "
            "state saved too. But Chinese households also saved a very large share of what they received."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag))
            vo.wait_until("a")
            self.play(*[Create(lines[k]) for k in NAMES if k not in ("CHN", "USA")],
                      *[FadeIn(labs[i]) for i, k in enumerate(NAMES) if k not in ("CHN", "USA")], run_time=2)
            vo.wait_until("b")
            self.play(Create(lines["USA"]), FadeIn(labs[list(NAMES).index("USA")]), FadeIn(side[1]), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(lines["CHN"]), FadeIn(labs[list(NAMES).index("CHN")]), FadeIn(side[0]), run_time=2)
        self.clear_scene()

    def why(self):
        rows = VGroup(
            label(r"three explanations, \ each from this part", font_size=28, color=E.ACCENT),
            label(r"the life cycle: \ fast growth and the one-child policy \ (Modigliani and Cao, \ 2004)",
                  font_size=23, color=SAVE),
            label(r"precaution: \ reform ended the iron rice bowl, \ so housing, \ schooling, \ health and old age "
                  r"became private costs \ (Chamon and Prasad, \ 2010)", font_size=22, color=CASH),
            label(r"competition: \ parents of sons save to improve their marriage prospects as sex ratios rise",
                  font_size=22, color=HOUSE),
            label(r"\quad Wei and Zhang, \ 2011: \ by the authors' estimate, \ about half of the rise in household "
                  r"saving, \ 1990--2007", font_size=21, color=GREY_A),
            label(r"each has evidence; \ their shares are argued", font_size=23, color=HOLD),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Modigliani and Cao, JEL 42(1) (2004); \ Chamon and Prasad, AEJ: Macro 2(1) (2010); \ "
                            r"Wei and Zhang, JPE 119(3) (2011)", corner=DR, font_size=12)
        with self.voiceover(
            "Why? Each explanation comes from this part. <bookmark mark='a'/> The life cycle: when income grows "
            "fast, the young who save are much richer than the old who dissave, and the one-child policy left fewer "
            "children to support parents in old age. Franco Modigliani and Shi Larry Cao made that case in 2004. "
            "<bookmark mark='b'/> Precaution: the reforms of the 1990s ended the iron rice bowl of state jobs, "
            "housing, health care and pensions. Marcos Chamon and Eswar Prasad found that urban households of all "
            "ages saved more as housing, schooling and health became private costs. <bookmark mark='c'/> And "
            "competition. As the ratio of boys to girls rose, parents of sons saved to improve their sons' chances "
            "in the marriage market, and the pressure spilled over to other households. "
            "<bookmark mark='d'/> Shang-Jin Wei and Xiaobo Zhang estimated that this competitive saving accounts for "
            "about half of the rise in household saving from 1990 to 2007, an estimate from their own work. "
            "<bookmark mark='e'/> Each has evidence. How the shares divide is argued."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
