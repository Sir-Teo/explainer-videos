from __future__ import annotations

from videos.economics.econ8.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ intangibles, AI and the boundary of the firm", r"What happens to production "
             r"functions and firm boundaries when capital is code and coordination is cheap?", "Chapter fifteen. "
             "Frontier: intangibles, AI and the boundary of the firm.", lit={2020: r"the pandemic"},
             scale=("firm", "market", "nation"), horizon=("a decade",))
        self.intangibles()
        self.ai_at_work()
        self.coasean()

    def intangibles(self):
        hc = history_card(2018, r"Haskel and Westlake, \ \emph{Capitalism without Capital}", r"firms now invest "
                          r"heavily in software, data, R\&D, design, brands and organization: \ capital you can't "
                          r"touch", color=OUT, width=11.6, font_size=24).to_edge(UP, buff=0.5)
        four = point_cards([
            (r"scalable", r"a program can be used \\ a million times at once", OUT),
            (r"sunk", r"hard to sell if the firm fails", CAP),
            (r"spillovers", r"competitors learn from it", LAB),
            (r"synergies", r"ideas pay most \\ in combination", FIRM),
        ], width=12.4, cols=4, font_size=21).next_to(hc, DOWN, buff=0.45)
        foot = label(r"for a production function: \ near-zero marginal cost, \ increasing returns, \ and capital that "
                     r"national accounts \\ long missed (Part 3)", font_size=23, color=E.ACCENT).next_to(four, DOWN,
                                                                                              buff=0.45)
        tag = published_tag(r"Haskel and Westlake (2018); Corrado, Hulten and Sichel (2009)", corner=DR, font_size=13)
        with self.voiceover(
            "The production function of this part had slipways and shipwrights. Modern firms' most important capital "
            "is often neither. <bookmark mark='a'/> Jonathan Haskel and Stian Westlake called it capitalism without "
            "capital: firms invest more and more in software, data, research, design, brands and ways of "
            "organizing, capital you can't touch. <bookmark mark='b'/> They pointed to four properties. Intangibles "
            "are scalable: a program can be used a million times at once. They're sunk: hard to sell if the firm "
            "fails. They spill over to competitors. And they have synergies: ideas pay most in combination. "
            "<bookmark mark='c'/> For a production function, that means near-zero marginal costs and increasing "
            "returns, and capital that the national accounts of Part three were slow to count."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, shift=UP * 0.1) for c in four.cards], lag_ratio=0.5), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def ai_at_work(self):
        c = study_card(r"Generative AI at Work", r"Brynjolfsson, Li and Raymond, \emph{QJE} (2025); NBER WP 31161",
                       [(r"sample", r"5{,}172 customer-support agents at one firm; \ an AI assistant rolled out "
                                    r"over time"),
                        (r"result", r"issues resolved per hour: \ about $+14\%$ on average"),
                        (r"who gains", r"about $+34\%$ for novice and low-skilled agents; \ little for the most "
                                       r"experienced"),
                        (r"how", r"the tool spread the practices of the best agents to the rest")],
                       design="event study", width=11.8, font_size=23).move_to(UP * 0.6)
        foot = label(r"a new input that substitutes for experience: \ the sigma of chapter 2, \ for a new kind of "
                     r"capital", font_size=24, color=E.ACCENT).next_to(c, DOWN, buff=0.45)
        tag = published_tag(r"Brynjolfsson, Li and Raymond (2025); the working paper's figures", corner=DR,
                            font_size=13)
        with self.voiceover(
            "Generative AI is the newest kind of intangible capital, and the first careful studies of it inside firms "
            "are production-function studies. <bookmark mark='a'/> Erik Brynjolfsson, Danielle Li and Lindsey "
            "Raymond followed five thousand one hundred and seventy-two customer-support agents at one company as an "
            "AI assistant was rolled out. The number of problems resolved per hour rose by about fourteen percent "
            "on average, and by about a third for novices and the least skilled, with little gain for the most "
            "experienced. The tool seemed to pass the best agents' practices on to everyone else. "
            "<bookmark mark='b'/> In this part's language, a new input that substitutes for experience. Part "
            "sixty-five returns to it."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(c, shift=UP * 0.2))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.clear_scene()

    def coasean(self):
        hc = history_card(2025, r"``The Coasean Singularity?''", r"Shahidi, Rusak, Manning, Fradkin and Horton: \ AI "
                          r"agents that search, negotiate and contract on our behalf \ could cut the costs of using "
                          r"markets sharply", color=MARKET, width=11.6, font_size=24).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"Coase's logic, run forward:", font_size=27),
            label(r"if AI makes the market cheaper to use, \ more is bought outside: \ smaller firms", font_size=25,
                  color=MARKET),
            label(r"if AI makes organizing cheaper, \ more is done inside: \ bigger firms", font_size=25, color=FIRM),
            label(r"new frictions too: \ congestion, \ prices made deliberately hard to compare", font_size=24,
                  color=HOLD),
            label(r"which effect wins is an empirical question, \ and an open one", font_size=26, color=E.ACCENT),
        ).arrange(DOWN, buff=0.32).next_to(hc, DOWN, buff=0.5)
        tag = published_tag(r"Shahidi et al., NBER WP 34468 (2025)", corner=DR, font_size=14)
        with self.voiceover(
            "Coase's question is back at the frontier. <bookmark mark='a'/> In 2025 Peyman Shahidi, John Horton and "
            "their colleagues asked what happens when AI agents search, negotiate and contract on our behalf. Their "
            "answer: the costs of using markets could fall sharply, which they called, with a question mark, the "
            "Coasean singularity. <bookmark mark='b'/> Run Coase's logic forward. If AI makes the market cheaper to "
            "use, firms should buy more from outside and shrink. <bookmark mark='c'/> If it makes organizing cheaper, "
            "firms should do more inside and grow. <bookmark mark='d'/> And agents bring new frictions of their own: "
            "congestion, and prices made deliberately hard to compare. <bookmark mark='e'/> Which effect wins is an "
            "empirical question, and an open one. The boundary of the firm, set at a margin, is moving again."
        ) as vo:
            self.play(FadeIn(tag), FadeIn(hc, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            for mk, r_ in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
