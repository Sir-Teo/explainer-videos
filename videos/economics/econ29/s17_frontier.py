from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card(self, 15, r"Frontier: \ beyond one household and one shock", r"Where does this method go next?",
             "Chapter fifteen. Frontier: beyond one household and one shock.",
             lit={1998: r"Krusell and Smith", 2018: r"Kaplan, \ Moll and Violante"}, scale=("person", "nation"),
             horizon=("a quarter", "a decade"))
        self.limits()
        self.many()
        self.compute()

    def limits(self):
        rows = VGroup(
            label(r"what this part assumed", font_size=27, color=E.ACCENT),
            label(r"one household stands for everyone", font_size=22, color=CONS),
            label(r"the economy stays close to its steady state, \ so a straight line will do", font_size=22,
                  color=TECH),
            label(r"a few states: \ capital and technology", font_size=22, color=VALUE),
            label(r"each assumption is now being dropped", font_size=23, color=HOLD),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = island_tag(corner=DR, font_size=14)
        with self.voiceover(
            "This part's model made three assumptions to stay solvable. <bookmark mark='a'/> One household stands "
            "for everyone. <bookmark mark='b'/> The economy stays close to its steady state, so a straight-line "
            "approximation will do. <bookmark mark='c'/> And there are only a few state variables. "
            "<bookmark mark='d'/> The frontier is dropping each of them."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def many(self):
        rows = VGroup(
            label(r"many households", font_size=27, color=E.ACCENT),
            label(r"Krusell and Smith, \ 1998: \ a whole distribution of wealth inside the growth model", font_size=21,
                  color=CONS),
            label(r"their surprise: \ the aggregate behaved almost as if there were one household", font_size=21,
                  color=GREY_A),
            label(r"Kaplan, \ Moll and Violante, \ 2018: \ with realistic wealth and hand-to-mouth households, \ "
                  r"\\ how monetary policy works changes", font_size=21, color=INVEST),
            label(r"Part 52: \ Many Agents", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Krusell and Smith, \ \emph{JPE} 106(5) (1998); \ Kaplan, \ Moll and Violante, \ "
                            r"\emph{AER} 108(3) (2018)", corner=DR, font_size=12)
        with self.voiceover(
            "First, many households. <bookmark mark='a'/> In 1998, Per Krusell and Anthony Smith put a whole "
            "distribution of wealth inside the growth model, with households facing their own risks. "
            "<bookmark mark='b'/> To general relief, the aggregate behaved almost as if there were one household. "
            "<bookmark mark='c'/> Twenty years later, Greg Kaplan, Benjamin Moll and Giovanni Violante gave the "
            "model realistic wealth, including the many households who spend what they earn, and found that how "
            "monetary policy works changes: most of its effect runs through income, not interest rates. "
            "<bookmark mark='d'/> Part fifty-two builds these economies."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def compute(self):
        rows = VGroup(
            label(r"solving what has no formula", font_size=27, color=E.ACCENT),
            label(r"global methods: \ the whole policy function, \ not a straight line near the steady state",
                  font_size=21, color=VALUE),
            label(r"occasionally binding limits: \ the zero lower bound, \ borrowing constraints", font_size=21,
                  color=TECH),
            label(r"continuous time and sparse grids; \ neural networks as policy functions for many states",
                  font_size=21, color=INVEST),
            label(r"and the old question: \ is the answer right? \ \ Euler-equation errors", font_size=21,
                  color=HOLD),
            label(r"Part 51: \ Computing Economies", font_size=23, color=E.ACCENT),
        ).arrange(DOWN, buff=0.42).move_to(UP * 0.1)
        tag = published_tag(r"Judd, \ \emph{Numerical Methods in Economics} (1998); \ Den Haan and Marcet (1994)",
                            corner=DR, font_size=12)
        with self.voiceover(
            "Second, solving what has no formula. <bookmark mark='a'/> Global methods find the whole policy "
            "function, not a straight line near the steady state, which matters when the economy is far from "
            "normal. <bookmark mark='b'/> Some limits bind only sometimes, like the zero lower bound on interest "
            "rates or a borrowing limit, and a linear solution cannot see them. <bookmark mark='c'/> New tools, "
            "continuous time, sparse grids, and neural networks trained to be policy functions, handle models with "
            "many states. <bookmark mark='d'/> And every method faces the cake's question: is the answer right? "
            "Part fifty-one answers with Euler-equation errors. <bookmark mark='e'/> That part, Computing "
            "Economies, takes this chapter's tools to their limits."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r_ in zip("abcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()
