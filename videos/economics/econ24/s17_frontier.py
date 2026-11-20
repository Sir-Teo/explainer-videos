from __future__ import annotations

from videos.economics.econ24.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ online vacancies, \ remote work, \ the geography of search", r"What can "
             r"millions of job ads tell us, \ and does distance still matter?",
             "Chapter fifteen. Frontier: online vacancies, remote work, and the geography of search.",
             lit={2018: r"Hershbein and Kahn; \ Marinescu and Rathelot", 2023: r"Hansen et al."},
             scale=("market", "world"), horizon=("years",))
        self.postings()
        self.distance()
        self.remote()
        self.open_()

    def postings(self):
        rows = VGroup(
            label(r"JOLTS counts openings; \ online postings say what each opening asks for", font_size=24,
                  color=E.ACCENT),
            label(r"hundreds of millions of ads, \ scraped and coded by occupation, \ skills, \ pay and place",
                  font_size=22, color=GREY_A),
            label(r"Hershbein and Kahn, \ 2018: \ after the Great Recession, \ skill requirements rose most in the "
                  r"cities it hit hardest", font_size=22, color=JOB),
            label(r"and stayed up, \ alongside new investment in capital: \ the slump sped up a change in technology",
                  font_size=22, color=TIGHT),
            label(r"so a vacancy is not a vacancy: \ the matching function's $V$ has a composition", font_size=23,
                  color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Hershbein and Kahn, AER 108(7) (2018): \ 1737--1772", corner=DR, font_size=12)
        with self.voiceover(
            "The frontier starts with new data. <bookmark mark='a'/> JOLTS tells us how many openings there are. "
            "Online job postings tell us what each one asks for. <bookmark mark='b'/> Companies that scrape job "
            "boards have coded hundreds of millions of ads by occupation, skills, pay and place. "
            "<bookmark mark='c'/> Brad Hershbein and Lisa Kahn used them to show that after the Great Recession, "
            "the skills employers asked for rose most in the cities the recession hit hardest. "
            "<bookmark mark='d'/> The higher requirements persisted, alongside new investment in capital: the "
            "slump seems to have sped up a shift toward technologies that need more skilled workers. "
            "<bookmark mark='e'/> So a vacancy is not just a vacancy. The V in the matching function has a "
            "composition, and a job seeker whose skills no longer match it is searching in a thinner market than "
            "the totals suggest."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def distance(self):
        ax = plane([-0.6, 1.6], [0, 1.1], center=LEFT * 2.4 + DOWN * 0.3, x_length=5.8, y_length=4.6, xticks=[],
                   yticks=[0, 0.25, 0.5, 0.75, 1.0], ylabel=r"chance of applying, \ relative to a job next door",
                   yfmt=lambda v: f"{v:g}", font_size=16)
        vals = ((1.0, r"in your \\ ZIP code", WORKER), (0.65, r"ten miles \\ away", SEP))
        bars, tops, names = VGroup(), VGroup(), VGroup()
        for k, (val, name, c) in enumerate(vals):
            lo, hi = ax.ax.c2p(k, 0), ax.ax.c2p(k, val)
            bars.add(Rectangle(width=0.9, height=hi[1] - lo[1], fill_color=c, fill_opacity=0.8,
                               stroke_width=0).move_to((lo + hi) / 2))
            tops.add(label(f"{val:.2f}", font_size=22, color=c).next_to(bars[-1], UP, buff=0.08))
            names.add(label(name, font_size=17, color=c).next_to(lo, DOWN, buff=0.15))
        side = VGroup(
            label(r"Marinescu and Rathelot, \ 2018: \\ applications on CareerBuilder", font_size=20, color=GREY_A),
            label(r"35\% less likely to apply \\ to a job ten miles away", font_size=22, color=SEP),
            label(r"yet moving searchers to \\ where the jobs are would cut \\ unemployment by only 5.3\%", font_size=21,
                  color=E.ACCENT),
            label(r"people live near enough \\ to the jobs: \ geographic \\ mismatch is a minor cause", font_size=19,
                  color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).to_edge(RIGHT, buff=0.4)
        tag = published_tag(r"Marinescu and Rathelot, AEJ: Macro 10(3) (2018): \ 42--70, \ with its appendix",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Does distance matter? <bookmark mark='a'/> Ioana Marinescu and Roland Rathelot studied who applied to "
            "which jobs on CareerBuilder, a large American job board. <bookmark mark='b'/> Job seekers were about "
            "thirty-five percent less likely to apply to a job ten miles from their home ZIP code than to one in "
            "it. People search locally. <bookmark mark='c'/> And yet, in their matching model, moving job seekers "
            "to wherever would minimize unemployment would cut it by only about five percent. "
            "<bookmark mark='d'/> Most people already live close enough to the jobs that their dislike of distance "
            "costs little in total: geographic mismatch is a minor cause of American unemployment."
        ) as vo:
            self.play(FadeIn(ax), FadeIn(tag), FadeIn(side[0]), GrowFromEdge(bars[0], DOWN), FadeIn(tops[0]),
                      FadeIn(names[0]))
            vo.wait_until("b")
            self.play(GrowFromEdge(bars[1], DOWN), FadeIn(tops[1]), FadeIn(names[1]), FadeIn(side[1]))
            vo.wait_until("c")
            self.play(FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def remote(self):
        rows = VGroup(
            label(r"Hansen, \ Lambert, \ Bloom, \ Davis, \ Sadun and Taska: \ hundreds of millions of postings in "
                  r"five English-speaking countries", font_size=21, color=GREY_A),
            label(r"the share of postings that allow remote work at least one day a week, \ 2019 to 2023:",
                  font_size=23, color=WHITE),
            label(r"more than tripled in the United States", font_size=27, color=TIGHT),
            label(r"rose fivefold or more in Australia, \ Canada, \ New Zealand and Britain", font_size=25,
                  color=TIGHT),
            label(r"unevenly: \ by city, \ industry, \ occupation and company", font_size=22, color=GREY_A),
            label(r"if a job need not be near, \ the matching function's market is no longer a city", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.4).move_to(UP * 0.1)
        tag = published_tag(r"Hansen, Lambert, Bloom, Davis, Sadun and Taska, NBER WP 31007 (2023, revised)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Then the pandemic changed where work can be done. <bookmark mark='a'/> Stephen Hansen, Peter Lambert, "
            "Nicholas Bloom, Steven Davis, Raffaella Sadun and Bledi Taska read hundreds of millions of job postings "
            "in five English-speaking countries with a language model, looking for one thing: <bookmark mark='b'/> "
            "whether the job allows working from home at least one day a week. <bookmark mark='c'/> From 2019 to "
            "early 2023, that share more than tripled in the United States, <bookmark mark='d'/> and rose fivefold "
            "or more in Australia, Canada, New Zealand and Britain. <bookmark mark='e'/> Very unevenly, though: by "
            "city, industry, occupation and company. "
            "<bookmark mark='f'/> If a job no longer has to be near, the market it is matched in is no longer a "
            "city. That could make matching more efficient, and change who competes with whom."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("bcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def open_(self):
        cards = point_cards([
            (r"the fundamental surplus", r"how much of a job's output \\ is really left over?", HOLD),
            (r"wages of new hires", r"how sticky, \ and \\ how measured?", WAGE),
            (r"engineered matching", r"do platforms raise $A$, \\ or only move who gets hired?", MATCH),
            (r"applications written by AI", r"when everyone's letter is good, \\ what does a letter signal?", JOB),
        ], width=12.0, cols=2, font_size=22).move_to(DOWN * 0.2)
        head = label(r"open questions", font_size=34, color=E.ACCENT).to_edge(UP, buff=0.6)
        with self.voiceover(
            "Four open questions. <bookmark mark='a'/> How much of a job's output is really left over after paying "
            "what the worker could get elsewhere: the number that decides the volatility puzzle. "
            "<bookmark mark='b'/> How sticky are the wages of new hires, and how should they be measured? "
            "<bookmark mark='c'/> Do platforms raise the efficiency of matching overall, or mostly change who gets "
            "hired? <bookmark mark='d'/> And when software can write anyone a good application, what will an "
            "application signal? Part thirteen's question about signals, in the labour market of the next decade."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cards.cards[0], shift=UP * 0.1))
            for mk, c in zip("bcd", cards.cards[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(c, shift=UP * 0.1))
        self.clear_scene()
