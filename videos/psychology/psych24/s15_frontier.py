from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


def grid(cells, center=(0, 0, 0), s: float = 0.28) -> VGroup:
    """A small coloured grid, as in ARC tasks: ``cells`` is a list of strings, '.' empty."""
    colors = {"r": LOST, "b": SEARCH, "y": CONTENT, "g": MODEL, ".": "#1F2633"}
    g = VGroup()
    h, w = len(cells), len(cells[0])
    for i, row in enumerate(cells):
        for j, ch in enumerate(row):
            g.add(Square(s, stroke_width=0.6, stroke_color=GREY_D, fill_color=colors[ch], fill_opacity=1)
                  .move_to(np.array(center, float) + np.array([(j - (w - 1) / 2) * s, ((h - 1) / 2 - i) * s, 0])))
    return g


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.programs()
        self.analogies()

    def card(self):
        card = chapter_card(14, r"Frontier: \ machines that reason", r"Can a machine find the rule in a few "
                            r"examples, \ as a person does?", lit={2019: r"Chollet", 2021: r"Ellis et al.",
                                                                   2023: r"Webb et al."},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter fourteen. Frontier: machines that reason."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def programs(self):
        head = heading(r"Finding the rule from a few examples")
        ex = [(["r..", "...", "..."], ["rrr", "...", "..."]), ([".b.", "...", "..."], ["bbb", "...", "..."]),
              (["...", "..y", "..."], ["...", "yyy", "..."])]
        pairs = VGroup()
        for k, (a, b) in enumerate(ex):
            ga, gb = grid(a, (-5.6, 1.7 - 1.2 * k, 0)), grid(b, (-3.9, 1.7 - 1.2 * k, 0))
            pairs.add(VGroup(ga, Arrow(ga.get_right(), gb.get_left(), buff=0.12, color=GREY_B), gb))
        test = grid(["...", "...", "g.."], (-5.6, -2.0, 0))
        ans = grid(["...", "...", "ggg"], (-3.9, -2.0, 0))
        qm = Arrow(test.get_right(), ans.get_left(), buff=0.12, color=GREY_B)
        lab = label(r"an ARC-style task, \ invented here", font_size=19, color=GREY_B).next_to(VGroup(test, ans),
                                                                                                DOWN, buff=0.15)
        rows = rows_of([
            (r"Chollet, \ 2019: \ the Abstraction and Reasoning Corpus, \ hundreds of tasks like this, \ each with "
             r"a few examples", WHITE),
            (r"LeGris et al., \ 2024: \ 1{,}729 people; \ on the evaluation tasks the average person solved about "
             r"64\%, \ and almost every task was solved by someone", DATA),
            (r"programs that learn programs: \ DreamCoder \ (Ellis et al., \ 2021) \ grows a library of reusable "
             r"pieces, \ like chunks", MODEL),
            (r"by late 2024 a large reasoning model passed the average person on the original set, \ at great cost "
             r"in computation; \ harder versions followed", GREY_A),
            (r"the open question: \ what lets a person induce a rule from three examples with so little effort?",
             INSIGHT),
        ], 7.2, 23, 0.34).move_to([2.7, -0.1, 0])
        tag = published_tag(r"Ellis et al. (2021); \ Chollet (2019); \ LeGris et al. (2024)")
        with self.voiceover(
            "Every problem in this part was posed to people. The frontier asks how a machine might solve them. "
            "<bookmark mark='a'/> In 2019 François Chollet published the Abstraction and Reasoning Corpus: hundreds "
            "of small puzzles, each a few examples of coloured grids and a test. Here's one invented in that style. "
            "Each coloured square spreads across its row. <bookmark mark='b'/> In 2024 Solim LeGris and colleagues "
            "tested more than seventeen hundred people. On the evaluation tasks the average person solved about "
            "sixty-four percent, and almost every task was solved by someone. <bookmark mark='c'/> One approach "
            "learns programs. Kevin Ellis's DreamCoder solves tasks by writing small programs, and grows a library "
            "of reusable pieces as it goes, rather like the chunks of an expert. <bookmark mark='d'/> By late 2024 a "
            "large reasoning model passed the average person on the original set, at great cost in computation, and "
            "harder versions followed. <bookmark mark='e'/> The open question is what lets a person find a rule from "
            "three examples with so little effort."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pairs], lag_ratio=0.4), FadeIn(test), GrowArrow(qm),
                      FadeIn(lab), FadeIn(rows[0]), run_time=3)
            self.play(FadeIn(ans))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def analogies(self):
        head = heading(r"Do language models reason by analogy?")
        ex = VGroup(label(r"\texttt{a b c d} \ $\rightarrow$ \ \texttt{a b c e}", font_size=34, color=WHITE),
                    label(r"\texttt{i j k l} \ $\rightarrow$ \ \texttt{?}", font_size=34, color=CONTENT)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-4.0, 1.75, 0])
        el = label(r"a letter-string analogy \ (Hofstadter)", font_size=20, color=GREY_B).next_to(ex, DOWN, buff=0.25)
        alpha = "xylkwbfztnjrqahvgmuopdicse"
        assert sorted(alpha) == [chr(97 + k) for k in range(26)]
        pa = VGroup(label(r"\texttt{" + " ".join(alpha[:13]) + "}", font_size=24, color=GREY_A),
                    label(r"\texttt{" + " ".join(alpha[13:]) + "}", font_size=24, color=GREY_A)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.15)
        nxt = alpha[alpha.index(alpha[11]) + 1]
        cf = VGroup(label(r"a scrambled alphabet:", font_size=21, color=LOST), pa,
                    label(r"\texttt{" + " ".join(alpha[:4]) + r"} \ $\rightarrow$ \ \texttt{" + " ".join(alpha[:3])
                          + " " + alpha[4] + "}", font_size=30, color=WHITE),
                    label(r"\texttt{" + " ".join(alpha[8:12]) + r"} \ $\rightarrow$ \ \texttt{?}", font_size=30,
                          color=CONTENT),
                    label(r"answer: \ \texttt{" + " ".join(alpha[8:11]) + " " + nxt + r"}, \ the next letter in "
                          r"\emph{this} alphabet", font_size=19, color=GREY_B)
                    ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).move_to([-4.0, -1.55, 0])
        rows = rows_of([
            (r"Webb, \ Holyoak \& Lu, \ 2023: \ GPT-3 matched or beat college students on text matrix puzzles, "
             r"\ letter-string and verbal analogies", MODEL),
            (r"critics: \ on new versions, \ such as an alphabet in a scrambled order, \ models fall back and people "
             r"do not \ (Lewis \& Mitchell, \ 2024)", LOST),
            (r"what it would take to settle: \ tasks that cannot have been seen, \ and an account of the "
             r"representations a model maps between", INSIGHT),
            (r"cognitive architectures, \ which build in goals and rules, \ against end-to-end learning, \ which "
             r"learns everything: \ the argument of Part 60", GREY_A),
        ], 6.4, 24, 0.36).move_to([3.0, -0.3, 0])
        tag = published_tag(r"Webb, \ Holyoak \& Lu (2023), \ \emph{Nature Human Behaviour}")
        with self.voiceover(
            "And analogy, the subject of chapter eight. <bookmark mark='a'/> In 2023 Taylor Webb, Keith Holyoak and "
            "Hongjing Lu found that GPT-3 matched or beat college students on text versions of matrix puzzles and on "
            "letter-string and verbal analogies: if a b c d becomes a b c e, what does i j k l become? "
            "<bookmark mark='b'/> Critics replied with new versions of the same problems, such as letter strings in a "
            "scrambled alphabet. People still solve them; the models fall back. <bookmark mark='c'/> Settling it "
            "needs tasks that can't have been seen in training, and an account of what representations a model maps "
            "between, which is exactly what structure mapping was meant to supply. <bookmark mark='d'/> Behind it all "
            "is the old argument between architectures that build in goals and rules, and end-to-end learning that "
            "learns everything. That's Part 60."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ex), FadeIn(el))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "b":
                    self.play(FadeIn(cf, shift=UP * 0.1))
        self.clear_scene()
