from __future__ import annotations

from videos.psychology.psych24.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.puzzles()
        self.usability()

    def card(self):
        card = chapter_card(13, r"In practice: \ puzzles, \ protocols, \ training", r"Where does the psychology of "
                            r"thinking do work?", lit={1985: r"Sweller \& Cooper", 1993: r"Nielsen \& Landauer",
                                                       1998: r"Schmidt \& Hunter"},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover("Chapter thirteen. In practice: puzzles, protocols and training."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def puzzles(self):
        head = heading(r"Interview puzzles")
        q = label(r"``How many golf balls fit in a school bus?''", font_size=34, color=CONTENT).move_to([0, 2.3, 0])
        # meta-analytic validities (correlation with later job performance), as published
        preds = [(r"general ability", 0.51, 0.31), (r"work sample", 0.54, 0.33), (r"structured interview", 0.51, 0.42),
                 (r"unstructured interview", 0.38, 0.19)]
        A = axes([0, 4], [0, 0.6], x_length=5.6, y_length=2.9, xticks=[], yticks=[0, 0.2, 0.4, 0.6],
                 yfmt=lambda v: f"{v:.1f}", ylabel=r"validity, \ $r$ with job performance", center=[-3.3, -0.4, 0],
                 font_size=16)
        old_b = VGroup(*[bars(A.ax, [k + 0.32], [v], GREY_B, 0.3) for k, (_, v, _) in enumerate(preds)])
        new_b = VGroup(*[bars(A.ax, [k + 0.68], [v], MODEL, 0.3) for k, (_, _, v) in enumerate(preds)])
        pn = VGroup(*[wrapped_label(t, 1.35, 16, GREY_A).next_to(A.ax.c2p(k + 0.5, 0), DOWN, buff=0.12)
                      for k, (t, _, _) in enumerate(preds)])
        key = legend([(GREY_B, r"Schmidt \& Hunter, \ 1998"), (MODEL, r"Sackett et al., \ 2022")],
                     font_size=16).move_to(A.ax.c2p(2.9, 0.56))
        assert max(preds, key=lambda p: p[2])[0] == r"structured interview"
        rows = rows_of([
            (r"puzzle questions were popular in hiring: \ they look like tests of reasoning", WHITE),
            (r"Google's head of people operations, \ 2013: \ in their own data, \ brainteasers were \emph{a complete "
             r"waste of time}", LOST),
            (r"what predicts job performance better: \ structured interviews, \ work samples, \ tests of general "
             r"ability; \ the 2022 revision lowers every estimate, \ and puts structured interviews first", MODEL),
            (r"this part's lesson: \ solving a puzzle depends on the right representation and on chunks from "
             r"experience, \ so a puzzle measures familiarity with puzzles", SEARCH),
            (r"training: \ novices learn more from studying worked examples than from solving problems "
             r"\ (Sweller \& Cooper, \ 1985); \ for experts the advantage reverses", INSIGHT),
        ], 5.8, 22, 0.32).move_to([3.6, -0.65, 0])
        tag = published_tag(r"Schmidt \& Hunter (1998); \ Sackett et al. (2022); \ Sweller \& Cooper (1985)")
        with self.voiceover(
            "Where is this used? Start with hiring. <bookmark mark='a'/> How many golf balls fit in a school bus? "
            "Puzzle questions were once popular in interviews, because they look like tests of reasoning. "
            "<bookmark mark='b'/> In 2013 Google's head of people operations said that, in the company's own data, "
            "brainteasers were a complete waste of time. <bookmark mark='c'/> What predicts job performance better "
            "is well studied: structured interviews, samples of the actual work, and tests of general ability, "
            "though the estimates have recently been revised down. Here is each one's correlation with later job "
            "performance, as Frank Schmidt and John Hunter pooled them in 1998, and as Paul Sackett and colleagues "
            "revised them in 2022: every estimate falls, and structured interviews come out on top. Personnel "
            "selection returns in Part 53. "
            "<bookmark mark='d'/> This part says why puzzles fail: solving one depends on finding the right "
            "representation, and on chunks from experience, so a puzzle mostly measures familiarity with puzzles. "
            "<bookmark mark='e'/> The same research shapes training. John Sweller found that novices learn more "
            "from studying worked examples than from solving problems themselves, while for experts the advantage "
            "reverses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(q), FadeIn(rows[0]))
            self.play(FadeIn(A), FadeIn(pn))
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "c":
                    self.play(LaggedStart(*[FadeIn(b) for b in old_b], lag_ratio=0.2), FadeIn(key[0]))
                    self.play(LaggedStart(*[FadeIn(b) for b in new_b], lag_ratio=0.2), FadeIn(key[1]))
        self.clear_scene()

    def usability(self):
        d = load("usability")
        head = heading(r"Thinking aloud, \ at work")
        A = axes([0, 15], [0, 1], x_length=5.4, y_length=3.2, xticks=[0, 5, 10, 15], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"test users",
                 ylabel=r"usability problems found", center=[-3.2, 0.2, 0], font_size=16)
        c = curve(A.ax, d["n"], d["found"], MODEL, 3)
        dot = Dot(A.ax.c2p(5, d["five"]), radius=0.08, color=CONTENT)
        dl = label(rf"5 users: \ {pct(d['five'])}", font_size=20, color=CONTENT).next_to(dot, DR, buff=0.1)
        rows = rows_of([
            (r"usability testing is Ericsson and Simon's protocol, \ put to work: \ users think aloud while they "
             r"try a design", WHITE),
            (rf"Nielsen \& Landauer, \ 1993: \ if each user meets a given problem with probability $L \approx "
             rf"{d['L']:.2f}$, \ $n$ users find $1 - (1 - L)^n$ of them", MODEL),
            (rf"five users find about {pct(d['five'])}: \ test small, \ fix, \ and test again", CONTENT),
            (r"but $L$ varies with the product and the people: \ for rare problems, \ five users miss a great deal",
             LOST),
            (r"designing for minds is Part 52", GREY_A),
        ], 5.8, 23, 0.34).move_to([3.6, 0.0, 0])
        tag = psyche_tag(r"Nielsen \& Landauer (1993), \ computed")
        assert abs(d["five"] - 0.84) < 0.01
        with self.voiceover(
            "Thinking aloud became an industry. <bookmark mark='a'/> Usability testing is Ericsson and Simon's "
            "protocol, put to work: people try a design and say what they're attending to, while a designer watches. "
            "<bookmark mark='b'/> How many people do you need? Jakob Nielsen and Thomas Landauer modelled it in "
            "1993. If each user runs into a given problem with probability about 0.31, then n users find one minus "
            "0.69 to the n of the problems. <bookmark mark='c'/> Five users find about eighty-four percent, which "
            "became the advice to test with a few people, fix, and test again. <bookmark mark='d'/> But that "
            "probability varies with the product and the users, and for rare problems five people miss a great deal. "
            "<bookmark mark='e'/> Designing for minds is Part 52."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(c), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(dot), FadeIn(dl), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
        self.clear_scene()
