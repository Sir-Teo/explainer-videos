from __future__ import annotations

from videos.psychology.psych43.common import *  # noqa: F403


def yes_no(flag) -> str:
    return "met" if bool(flag) else "not met"


def bf_words(bf: float) -> str:
    if bf > 1e6:
        return "more than a million to one for the original's effect"
    if bf > 1:
        return f"{bf:.0f} to one for the original's effect"
    return f"about {1 / bf:.0f} to one for no effect"


class Verdict(VoiceoverScene):
    def construct(self):
        self.card()
        self.criteria()
        self.board()
        self.meanings()

    def card(self):
        card = chapter_card(9, r"Was it a replication?", r"Three criteria, \ and a Bayes factor",
                            lit={2014: r"Verhagen \& Wagenmakers"}, part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter nine. Was it a replication?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def criteria(self):
        head = heading(r"Three questions, \ and a fourth")
        rows = rows_of([
            (r"significance: \ is the pooled effect significant in the predicted direction?", SYMP),
            (r"consistency: \ does the replication's 95\% interval contain the original estimate?", PERSON),
            (r"small telescopes: \ does the interval reach $d_{33}$, \ the effect the original could have seen?", MODEL),
            (r"Verhagen and Wagenmakers, \ 2014: \ the replication Bayes factor weighs the new data under the original's "
             r"estimate against no effect at all", GOOD),
            (r"the three can disagree: \ an effect can be real and smaller than first reported", YOU),
        ], 12.4, 23, 0.44).move_to([0, -0.3, 0])
        eq = MathTex(r"\mathrm{BF}_{r0} = \frac{N\big(\hat d_r;\ \hat d_o,\ \mathrm{se}_o^2 + \mathrm{se}_r^2\big)}"
                     r"{N\big(\hat d_r;\ 0,\ \mathrm{se}_r^2\big)}", font_size=30, color=GOOD).to_edge(DOWN, buff=0.4)
        tag = published_tag(r"Verhagen \& Wagenmakers (2014)")
        with self.voiceover(
            "Was it a replication? The plan fixed three questions in advance. <bookmark mark='a'/> Significance: is "
            "the pooled effect significant in the predicted direction? <bookmark mark='b'/> Consistency: does the "
            "replication's interval contain the original estimate? <bookmark mark='c'/> Small telescopes: does the "
            "interval reach d thirty-three, the effect the original could have seen? <bookmark mark='d'/> And a "
            "fourth, from Josine Verhagen and Eric-Jan Wagenmakers in 2014: the replication Bayes factor, which weighs "
            "the new data under the original's estimate against no effect at all. <bookmark mark='e'/> The three can "
            "disagree. An effect can be real, and smaller than first reported."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "d":
                    self.play(FadeIn(eq))
        self.clear_scene()

    def board(self):
        v = load("verdict")
        head = heading(r"The verdict")
        cols = [r"", r"verbal overshadowing", r"ego depletion"]
        rows_def = [(r"significant", "significant"), (r"original inside the interval", "original_inside"),
                    (r"reaches $d_{33}$", "not_below_d33")]
        grid = VGroup()
        for j, cname in enumerate(cols):
            grid.add(label(cname, font_size=19, color=GREY_A).move_to([-3.0 + j * 3.6, 2.0, 0]))
        marks = VGroup()
        for i, (name, key) in enumerate(rows_def):
            y = 1.1 - i * 0.8
            grid.add(label(name, font_size=19, color=WHITE).move_to([-3.0, y, 0]))
            for j, t in enumerate(("vo", "ed")):
                ok = bool(v[f"{t}_{key}"])
                marks.add(label(r"yes" if ok else r"no", font_size=24, color=GOOD if ok else AUTH).move_to(
                    [0.6 + j * 3.6, y, 0]))
        bfs = VGroup(label(r"replication Bayes factor", font_size=19, color=WHITE).move_to([-3.0, -1.3, 0]),
                     label(rf"{bf_words(v['vo_bf_r0'])}", font_size=15, color=GOOD).move_to([0.6, -1.3, 0]),
                     label(rf"{bf_words(v['ed_bf_r0'])}", font_size=15, color=AUTH).move_to([4.2, -1.3, 0]))
        vo_met, ed_met = f"{v['vo_n_met']:.0f}", f"{v['ed_n_met']:.0f}"
        vo_bf, ed_bf = bf_words(v["vo_bf_r0"]), bf_words(v["ed_bf_r0"])
        foot = wrapped_label(rf"verbal overshadowing: \ {vo_met} of 3 criteria; \ ego depletion: \ {ed_met} of 3", 12.0, 22,
                             YOU).move_to([0, -2.4, 0])
        with self.voiceover(
            f"Here's the verdict. <bookmark mark='a'/> Verbal overshadowing meets {vo_met} of the three criteria. The "
            f"effect is significant, but smaller than the original's, whose estimate falls outside the interval. The "
            f"Bayes factor: {vo_bf}. <bookmark mark='b'/> Ego depletion meets {ed_met} of the three. The interval "
            f"stops short of the effect the original study could have seen. The Bayes factor: {ed_bf}. "
            f"<bookmark mark='c'/> So one effect replicated, smaller than reported, and one did not."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid))
            vo.wait_until("a")
            self.play(*[FadeIn(marks[i]) for i in (0, 2, 4)], FadeIn(bfs[0]), FadeIn(bfs[1]))
            vo.wait_until("b")
            self.play(*[FadeIn(marks[i]) for i in (1, 3, 5)], FadeIn(bfs[2]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

    def meanings(self):
        head = heading(r"What each result would have meant")
        data = (
            (r"significant, \ and the original inside the interval", r"replicated, \ about as large as reported", GOOD),
            (r"significant, \ the original above the interval", r"replicated, \ smaller: \ verbal overshadowing",
             SYMP),
            (r"not significant, \ and the interval excludes $d_{33}$", r"failed: \ effects the original could have "
                                                                     r"seen are ruled out: \ ego depletion", AUTH),
            (r"not significant, \ and the interval includes $d_{33}$", r"inconclusive: \ the study could not tell", GREY_B),
        )
        rows = VGroup()
        for cond, meaning, c in data:
            rows.add(VGroup(wrapped_label(cond, 5.4, 19, WHITE), label(r"$\Rightarrow$", font_size=22, color=GREY_B),
                            wrapped_label(meaning, 5.6, 19, c)).arrange(RIGHT, buff=0.35))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.42).move_to([0, 0.2, 0])
        foot = wrapped_label(r"the table was written in the plan, \ before the data: \ the verdict was a lookup, \ "
                             r"not a judgment made after seeing the result", 12.0, 21, YOU).move_to([0, -2.6, 0])
        with self.voiceover(
            "One more thing the plan fixed in advance: what each possible result would mean. "
            "<bookmark mark='a'/> Significant, with the original estimate inside the interval: replicated, about as "
            "large as reported. <bookmark mark='b'/> Significant, with the original above the interval: replicated, "
            "smaller. That's verbal overshadowing. <bookmark mark='c'/> Not significant, with an interval that "
            "excludes the effect the original could have seen: failed. That's ego depletion. <bookmark mark='d'/> "
            "And not significant, with an interval that includes it: inconclusive. The study couldn't tell. "
            "<bookmark mark='e'/> Because the table was written before the data, the verdict was a lookup, not a "
            "judgment made after seeing the result."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
