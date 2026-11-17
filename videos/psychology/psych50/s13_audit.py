from __future__ import annotations

from videos.psychology.psych50.common import *  # noqa: F403


class Audit(VoiceoverScene):
    def construct(self):
        self.card()
        self.overall()
        self.byact()
        self.caveats()

    def card(self):
        card = chapter_card(12, r"The Ledger, \ audited", r"What does this series' own record say?", lit=(), part=PART,
                            scale=("society",), marr=("what",))
        with self.voiceover("Chapter twelve. The Ledger, audited."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def overall(self):
        d = load("audit")
        head = heading(rf"{d['n']} findings, \ one record")
        tot = np.asarray(d["total"])
        names = [str(s) for s in d["statuses"]]
        cols = [STATUS_COLOR.get(s, GREY_B) for s in names]
        A = axes([0.3, len(names) + 0.7], [0, 160], x_length=6.6, y_length=3.2, xticks=None, yticks=[0, 50, 100, 150],
                 yfmt=lambda v: f"{v:.0f}", ylabel=r"rows", center=[-2.8, 0.4, 0], font_size=12)
        b = bars(A.ax, list(range(1, len(names) + 1)), tot, cols, width=0.65)
        labs = VGroup(*[wrapped_label(n, 1.0, 11, c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1)
                        for i, (n, c) in enumerate(zip(names, cols))])
        held = int(tot[:3].sum())
        bad = int(tot[4] + tot[5])
        rows = rows_of([
            (rf"held: \ {held} of {d['n']} ({100 * held / d['n']:.0f}\%), \ counting those that held smaller or whose "
             rf"textbook story was wrong", GOOD),
            (rf"contested: \ {int(tot[3])} ({100 * tot[3] / d['n']:.0f}\%)", STATUS_COLOR.get("contested", GREY_B)),
            (rf"failed or retracted: \ {bad} ({100 * bad / d['n']:.0f}\%)", AUTH),
        ], 4.8, 19, 0.4).move_to([4.2, 0.3, 0])
        tag = psyche_tag(r"\texttt{meta.ledger\_audit}, \ rows up to Part 49")
        with self.voiceover(
            "Now the series audits itself. <bookmark mark='a'/> Through Part 49 the Ledger holds two hundred and "
            "sixty-three findings. <bookmark mark='b'/> About two thirds held, counting those that held smaller or "
            "whose textbook story was wrong. <bookmark mark='c'/> About one in five is contested. "
            "<bookmark mark='d'/> And about one in seven failed or was retracted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(labs))
            vo.wait_until("a")
            self.play(FadeIn(b))
            for m, r in zip("bcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def byact(self):
        d = load("audit")
        head = heading(r"Where the findings held")
        M = np.asarray(d["by_act"], float)
        acts = list(d["acts"])
        held = M[:, :3].sum(1) / M.sum(1)
        bad = (M[:, 4] + M[:, 5]) / M.sum(1)
        A = axes([0.3, len(acts) + 0.7], [0, 1.05], x_length=7.0, y_length=3.0, xticks=None, yticks=[0, 0.5, 1],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"share of the act's rows", center=[-2.6, 0.4, 0],
                 font_size=12)
        x = np.arange(1, len(acts) + 1)
        bh = bars(A.ax, x - 0.18, held, GOOD, width=0.34)
        bb = bars(A.ax, x + 0.18, bad, AUTH, width=0.34)
        labs = VGroup(*[label(a, font_size=13, color=GREY_A).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1)
                        for i, a in enumerate(acts)])
        key = VGroup(label(r"held", font_size=13, color=GOOD), label(r"failed or retracted", font_size=13, color=AUTH))
        key.arrange(RIGHT, buff=0.4).next_to(A, UP, buff=0.2)
        rows = rows_of([
            (r"by act: \ perception, \ learning and cognition (Acts III to VI) held 80\% or more", GOOD),
            (r"motivation, \ development, \ social and clinical psychology (Acts VII to X) about half, \ with most of "
             r"the failures", AUTH),
            (r"by the decade of the original study, \ findings from before 1960 held almost always; \ from the "
             r"2000s, \ about half", PERSON),
        ], 4.6, 18, 0.36).move_to([4.4, -0.1, 0])
        with self.voiceover(
            "Where did the findings hold? <bookmark mark='a'/> By act, perception, learning and cognition held at "
            "eighty percent or more. <bookmark mark='b'/> Motivation, development, social and clinical psychology held "
            "about half, and hold most of the failures. <bookmark mark='c'/> And by the decade of the original study, "
            "findings from before 1960 held almost always, and findings from the 2000s about half."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(labs), FadeIn(key), FadeIn(bh), FadeIn(bb))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def caveats(self):
        head = heading(r"Reading the audit with the part's own tools")
        rows = rows_of([
            (r"the Ledger is not a random sample: \ it holds the findings a course would teach, \ the famous and the "
             r"contested", AUTH),
            (r"old findings have had a century to be tested and forgotten if they failed: \ survivorship flatters the "
             r"past", PERSON),
            (r"precise, \ repeatable measurements of perception and learning make strong tests; \ effects that depend "
             r"on context and small samples make weak ones", MODEL),
            (r"the same pattern the replication projects found: \ the predictors of survival were sample size, \ effect "
             r"size and how surprising the claim was", GOOD),
            (r"every row has its sources and the date it was checked: \ the audit can be redone, \ and should be", YOU),
        ], 12.4, 22, 0.42).move_to([0, -0.3, 0])
        with self.voiceover(
            "Read the audit with this part's own tools. <bookmark mark='a'/> The Ledger isn't a random sample. It holds "
            "the findings a course would teach, the famous and the contested. <bookmark mark='b'/> Old findings have "
            "had a century to be tested, and forgotten if they failed. Survivorship flatters the past. "
            "<bookmark mark='c'/> Precise, repeatable measurements of perception and learning make strong tests. "
            "Effects that depend on context, studied in small samples, make weak ones. <bookmark mark='d'/> It's the "
            "same pattern the replication projects found: survival was predicted by sample size, effect size, and how "
            "surprising the claim was. <bookmark mark='e'/> Every row has its sources and the date it was checked, so "
            "the audit can be redone, and it should be."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
