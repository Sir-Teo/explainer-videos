from __future__ import annotations

from explainer.ai import *  # noqa: F403
from videos.ai.ai29.common import AGENT, CLAIM, FAIL, GOOD, HIST, MONO, PART, REWARD, TOOL, WORLD, node_box, score_bar

# Scale AI's SWE-Bench Pro leaderboard, public set (labs.scale.com/leaderboard/swe_bench_pro_public, retrieved
# 29 October 2026): resolve rate in percent, with Scale's interval; mini-swe-agent harness, 250 turns
PRO_BOARD = [("Muse Spark 1.1", 61.5, 3.1), ("GPT-5.4 (xHigh)", 59.1, 3.56), ("Claude Opus 4.6 (thinking)", 51.9, 3.61),
             ("Gemini 3.1 Pro (thinking)", 46.1, 3.6)]


def mono(s, color=GREY_A, size=18):
    return data_text(s, font=MONO, font_size=size, color=color)


class Coding(VoiceoverScene):
    def construct(self):
        self.card()
        self.swebench()
        self.agent_interface()
        self.scores()
        self.terminal()

    def card(self):
        card = chapter_card(7, r"Coding agents", r"Can it fix a real bug?", lit=(2026,), part=PART)
        with self.voiceover("Chapter seven. Coding agents."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    # ------------------------------------------------------------------
    def swebench(self):
        tree = VGroup(*[mono(t, GREY_B, 17) for t in ("astropy/", "  io/", "    fits/", "      header.py",
                                                       "  modeling/", "    separable.py", "  tests/", "    test_separable.py")])
        tree.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        tl = label(r"a real repository", font_size=22, color=WORLD)
        repo = VGroup(tl, tree).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-5.0, 0.6, 0])
        issue = VGroup(label(r"a real issue", font_size=22, color=C.PENALTY),
                       mono("separability_matrix gives the wrong\nanswer for nested CompoundModels", GREY_A, 17))
        issue.arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-0.9, 2.3, 0])
        diff = VGroup(mono("-    cright[-right.shape[0]:, ...] = 1", FAIL, 16),
                      mono("+    cright[-right.shape[0]:, ...] = right", GOOD, 16))
        diff.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        dl = label(r"the agent's patch", font_size=22, color=AGENT)
        patch = VGroup(dl, diff).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-0.9, 0.2, 0])
        tests = VGroup(VGroup(mono("test_nested_compound", GREY_A, 17), label(r"fail $\to$ pass", font_size=20, color=GOOD))
                       .arrange(RIGHT, buff=0.3),
                       VGroup(mono("the other tests", GREY_A, 17), label(r"still pass", font_size=20, color=GOOD))
                       .arrange(RIGHT, buff=0.3)).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        tel = label(r"graded by the project's own tests", font_size=22, color=REWARD)
        tst = VGroup(tel, tests).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-0.9, -1.9, 0])
        hist = history_card(r"Oct 2023", r"SWE-bench \ (Jimenez, Yang, Wettig, Yao, Pei, Press \& Narasimhan)",
                            r"$2{,}294$ GitHub issues from $12$ popular Python projects, \ each with the tests its real "
                            r"fix made pass; \ the best model then, \ Claude 2, \ solved $1.96\%$", width=4.8,
                            color=HIST, font_size=18).to_corner(DR, buff=0.3).shift(UP * 0.4)
        tag = note(r"after an issue in SWE-bench (astropy), \ simplified").to_corner(DL, buff=0.25)
        with self.voiceover(
            "How do you test a coding agent? In 2023 Carlos Jimenez, John Yang and colleagues at Princeton built "
            "SWE-bench from the history of open-source software. <bookmark mark='a'/> Each problem is a real issue "
            "reported on GitHub, <bookmark mark='b'/> in a real repository, frozen at the moment before it was "
            "fixed. <bookmark mark='c'/> The agent must write a patch. <bookmark mark='d'/> Then the tests the real "
            "fix added are run: they must go from failing to passing, while every other test keeps passing. "
            "<bookmark mark='e'/> There were 2,294 problems from twelve Python projects. The best model of the day, "
            "Claude 2, solved under two percent of them."
        ) as vo:
            self.play(FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(issue, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(repo))
            vo.wait_until("c")
            self.play(FadeIn(patch))
            vo.wait_until("d")
            self.play(FadeIn(tst))
            vo.wait_until("e")
            self.play(FadeIn(hist, shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def agent_interface(self):
        cmds = VGroup(*[mono(t, AGENT, 18) for t in ("find_file separable.py", "open separable.py 240",
                                                    "edit 245:245  cright[...] = right", "python -m pytest tests/")])
        cmds.arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        cl = label(r"commands designed for a model", font_size=22, color=AGENT)
        left = VGroup(cl, cmds).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([-3.8, 1.2, 0])
        feed = VGroup(*[mono(t, GREY_B, 16) for t in ("[file: separable.py, lines 240-340 of 317]",
                                                     "Your edit introduced a syntax error;", "it was not applied.")])
        feed.arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        fl = label(r"compact, \ informative feedback", font_size=22, color=TOOL)
        right = VGroup(fl, feed).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.0, 1.2, 0])
        cards = VGroup(
            history_card(r"May 2024", r"SWE-agent \ (Yang, Jimenez et al.)", r"an agent--computer interface: \ with the "
                         r"same model (GPT-4 Turbo), \ $12.5\%$ of SWE-bench, \ from under $4\%$ without one", width=4.4,
                         color=HIST, font_size=18),
            history_card(r"Aug 2024", r"SWE-bench Verified \ (OpenAI)", r"$500$ problems that professional developers "
                         r"checked were well posed and fairly tested; \ GPT-4o solved $33.2\%$", width=4.4, color=HIST,
                         font_size=18),
            history_card(r"2025", r"agents in the terminal", r"Claude Code, \ OpenAI's Codex, \ Gemini CLI: \ the loop of "
                         r"chapter three, \ run on a developer's own machine", width=4.4, color=HIST, font_size=18),
        ).arrange(RIGHT, buff=0.25).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The first big gains came from the interface, not the model. <bookmark mark='a'/> In 2024 the same "
            "Princeton group gave GPT-4 commands made for it: find a file, look at a hundred lines at a time, edit a "
            "range of lines, run the tests. <bookmark mark='b'/> And the environment answers compactly, refusing an "
            "edit that would break the syntax. <bookmark mark='c'/> They called it an agent-computer interface, "
            "and with the same model it solved twelve and a half percent of SWE-bench, several times more than "
            "before. <bookmark mark='d'/> That August OpenAI had developers check every problem in a subset of five "
            "hundred, keeping those that were well posed: SWE-bench Verified, the standard yardstick for two years. "
            "<bookmark mark='e'/> And by 2025 the loop had moved into developers' own terminals."
        ) as vo:
            self.play(FadeIn(cl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c_, shift=RIGHT * 0.1) for c_ in cmds], lag_ratio=0.3), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(cards[0], shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(cards[1], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(cards[2], shift=UP * 0.15))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def scores(self):
        audit = history_card(r"Feb 2026", r"OpenAI stops reporting SWE-bench Verified", r"of $138$ problems its model "
                             r"kept failing, \ it judged $59.4\%$ to have flawed tests; \ given only a task's ID, \ "
                             r"three frontier models reproduced the real fix, \ comments and all: \ they had seen it in "
                             r"training", width=6.2, color=CLAIM, font_size=19).move_to([-3.4, 1.1, 0])
        pro = history_card(r"Sep 2025", r"SWE-Bench Pro \ (Scale AI)", r"$1{,}865$ problems from $41$ actively "
                           r"maintained repositories, \ some kept private, \ some from companies' own code: \ longer "
                           r"changes, \ harder to have memorized", width=6.2, color=HIST, font_size=19).move_to([3.4, 1.1, 0])
        W = 5.2
        board = VGroup()
        for name, v, ci in PRO_BOARD:
            n = label(name, font_size=19, color=GREY_A)
            bar = score_bar(v, 100, W, AGENT, 0.3)
            val = MathTex(rf"{v:.1f}\% \pm {ci:.1f}", font_size=22, color=AGENT)
            board.add(VGroup(n, bar, val))
        for r in board:
            r[0].set_x(-2.3 - r[0].width / 2)
            r[1].move_to([-2.1 + W / 2, 0, 0])
            r[2].next_to(r[1], RIGHT, buff=0.15)
        board.arrange(DOWN, buff=0.18)
        for r in board:
            r[0].align_to(board, LEFT)
        bl = label(r"SWE-Bench Pro, \ public set: \ Scale's leaderboard, \ October 2026", font_size=22, color=WORLD)
        tab = VGroup(bl, board).arrange(DOWN, buff=0.2).move_to([0, -2.1, 0])
        tag = note(r"scores: \ Scale AI (labs.scale.com), \ retrieved 29 Oct 2026; \ same harness, \ $250$ turns",
                   font_size=16).to_corner(DR, buff=0.15)
        top = PRO_BOARD[0]
        with self.voiceover(
            "Then the yardstick wore out. Frontier models came to solve most of Verified, and in February 2026 "
            "OpenAI announced it would stop reporting it. <bookmark mark='a'/> Of a hundred and thirty-eight problems "
            "its model kept failing, its engineers judged fifty-nine percent to have tests that reject correct "
            "fixes. And given nothing but a problem's ID, three frontier models wrote out the real fix, comments "
            "included: the answers had leaked into training data. Those are OpenAI's findings. "
            "<bookmark mark='b'/> Its suggested successor was Scale AI's SWE-Bench Pro: eighteen hundred and "
            "sixty-five problems from forty-one actively maintained repositories, some held back from the public, "
            "with bigger changes to make. When it appeared in September 2025, the best models solved about a "
            f"quarter of it. <bookmark mark='c'/> On Scale's leaderboard today, the top entry, {top[0]}, solves "
            f"{top[1]:.1f} percent of the public set, within a few points of the next."
        ) as vo:
            self.play(FadeIn(audit, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(Indicate(audit, color=CLAIM, scale_factor=1.02))
            vo.wait_until("b")
            self.play(FadeIn(pro, shift=UP * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(bl), LaggedStart(*[FadeIn(r_) for r_ in board], lag_ratio=0.2), FadeIn(tag), run_time=2.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def terminal(self):
        term = RoundedRectangle(width=6.6, height=3.4, corner_radius=0.12, stroke_color=GREY_B, stroke_width=2,
                                fill_color="#0B0F17", fill_opacity=1).move_to([-3.2, 0.9, 0])
        lines = VGroup(*[mono(t, c, 17) for t, c in (("$ docker build -t app .", AGENT),
                                                      ("ERROR: libssl not found", FAIL),
                                                      ("$ apt-get install -y libssl-dev", AGENT),
                                                      ("$ docker build -t app .", AGENT),
                                                      ("Successfully built 3f2a91", GOOD),
                                                      ("$ pytest -q   ->  12 passed", GOOD))])
        lines.arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to(term).align_to(term, LEFT).shift(RIGHT * 0.3)
        tl = label(r"a task in a container: \ graded by a script at the end", font_size=22, color=GREY_A)
        tl.next_to(term, UP, buff=0.15)
        tag = note(r"illustrative task").next_to(term, DOWN, buff=0.1).align_to(term, LEFT)
        cards = VGroup(
            history_card(r"2025", r"Terminal-Bench \ (Stanford and the Laude Institute)", r"hard tasks in a real "
                         r"terminal: \ compile, \ configure a server, \ train a model; \ version 2.0: \ $89$ "
                         r"tasks, \ frontier agents under $65\%$", width=5.6, color=HIST, font_size=18),
            history_card(r"2026", r"version 4.0", r"saturated tasks retired, \ others fixed; \ each task gets up to "
                         r"$8$ hours", width=5.6, color=HIST, font_size=18),
            history_card(r"Sep 2026", r"Anthropic, \ Claude Opus 5.5 \ (a company claim)", r"$66.4\%$ on Terminal-Bench "
                         r"4.0, \ in Anthropic's own runs", width=5.6, color=CLAIM, font_size=18),
        ).arrange(DOWN, buff=0.2).to_edge(RIGHT, buff=0.3)
        if cards.height > 7.0:
            cards.height = 7.0
            cards.to_edge(RIGHT, buff=0.3)
        with self.voiceover(
            "Real engineering is more than patches. <bookmark mark='a'/> Terminal-Bench, from Stanford and the Laude "
            "Institute in 2025, drops an agent into a terminal inside a container with a job to do, like building "
            "software, configuring a server or training a model, and a script checks the result at the end. "
            "<bookmark mark='b'/> Version 2.0 had eighty-nine such tasks, and frontier agents solved less than two "
            "thirds. <bookmark mark='c'/> Benchmarks now get retired as fast as models improve: version 4.0, in 2026, "
            "dropped the tasks every model solved and gave each task up to eight hours. <bookmark mark='d'/> In "
            "September 2026 Anthropic reported sixty-six percent on it for its newest model: a company's measurement "
            "of its own model, to be checked on public leaderboards."
        ) as vo:
            self.play(FadeIn(term), FadeIn(tl), FadeIn(tag))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.4), FadeIn(cards[0]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(cards[1], shift=LEFT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(cards[2], shift=LEFT * 0.15))
        self.wait(0.3)
        self.clear_scene()
