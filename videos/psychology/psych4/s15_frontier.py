from __future__ import annotations

from videos.psychology.psych4.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.audit()
        self.open_questions()

    def card(self):
        card = chapter_card(14, r"Frontier: \ have the reforms worked?", r"What is known about the repairs, and "
                            r"what is not?", lit={2018: r"Nature and Science, replicated"}, part=PART,
                            scale=("group", "culture"), marr=("what",))
        with self.voiceover(
            "Chapter fourteen. The frontier: have the reforms worked?"
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def audit(self):
        c, dr, pz = archive.CAMERER_2018.data, archive.DREBER_2015.data, archive.PROTZKO_2023.data
        head = heading(r"Three things that are known, and one that came apart")

        def block(title, color, text, width=6.1):
            head_ = label(title, font_size=30, color=color)
            if head_.width > width:
                head_.width = width
            return VGroup(head_, wrapped_label(text, width, 27, WHITE)).arrange(DOWN, aligned_edge=LEFT, buff=0.14)

        a = block(r"The best journals are not exempt", ORIG,
                  rf"{c['studies']} experiments from \emph{{Nature}} and \emph{{Science}}, 2010 to 2015, run again "
                  rf"with samples about {c['sample_ratio']} times larger: \ {c['replicated']} held "
                  rf"({pct(c['share'])}), at about half the size.")
        b = block(r"The field can price its own findings", REP,
                  rf"Betting markets on {dr['studies']} replications predicted the outcomes well. \ They put the "
                  rf"typical hypothesis's chance of being true, before it was tested, near {pct(dr['median_prior'])}.")
        c_ = block(r"Committing in advance changes what is printed", TRUTH,
                   r"Registered reports support their first hypothesis less than half the time; \ ordinary "
                   r"papers, nearly always.")
        e = block(rf"{pz['published']}, a claim of success; \ {pz['retracted']}, retracted", BAD, r"A study reporting that findings made with the reformed practices replicate at a high "
                  r"rate was withdrawn: \ analyses had not been preregistered as the paper said.")
        grid = VGroup(VGroup(a, b).arrange(DOWN, aligned_edge=LEFT, buff=0.5),
                      VGroup(c_, e).arrange(DOWN, aligned_edge=LEFT, buff=0.5)).arrange(RIGHT, buff=0.7,
                                                                                         aligned_edge=UP)
        grid.move_to([0, -0.25, 0])
        if grid.width > 13.3:
            grid.width = 13.3
        src = published_tag(rf"{archive.CAMERER_2018.cite}; \ {archive.DREBER_2015.cite}; \ "
                            rf"{archive.SCHEEL_2021.cite}; \ {archive.PROTZKO_2023.cite}")
        with self.voiceover(
            "So did it work? This is the frontier, and the answer isn't in yet. Here's what is. "
            f"<bookmark mark='a'/> The problem wasn't confined to obscure journals. When {c['studies']} "
            "experiments from Nature and Science were run again, with samples about five times the size, "
            f"{c['replicated']} held, and again at about half the size. <bookmark mark='b'/> The field can "
            "price its own findings: betting markets predicted which replications would succeed. And those "
            "markets carry a sobering number. They put the chance that a typical tested hypothesis was true, "
            f"before anyone ran the study, at around {100 * dr['median_prior']:.0f} per cent. Psychologists "
            "test bold ideas, and most bold ideas are wrong. <bookmark mark='c'/> Committing in advance does "
            "change what gets printed, as you saw. <bookmark mark='d'/> But the question that matters is "
            "whether findings made under the new rules are more often true. In 2023 a study reported that they "
            "are: that with the reformed practices, high replicability is achievable. In 2024 it was "
            "retracted. Analyses in it hadn't been preregistered in the way the paper said they had. A paper "
            "about the benefits of preregistration, withdrawn over its preregistration. Its authors agreed to "
            "the retraction. That doesn't show the reforms fail. It shows that the question is still open, and "
            "that the rules bind reformers too."
        ) as vo:
            self.play(FadeIn(head), FadeIn(src))
            for mark, blk in zip("abcd", (a, b, c_, e)):
                vo.wait_until(mark)
                self.play(FadeIn(blk, shift=UP * 0.15))
        self.clear_scene()

    def open_questions(self):
        head = heading(r"Open questions")
        qs = VGroup(
            wrapped_label(r"1. \ Are preregistered findings more often true, or only more often null? \ No "
                          r"experiment has yet randomized the practice.", 12.2, 29, WHITE),
            wrapped_label(r"2. \ When a replication fails, was the finding false, or narrower than claimed? \ What "
                          r"does a result from one sample of students license about people?", 12.2, 29, WHITE),
            wrapped_label(r"3. \ Meehl's problem is untouched by better statistics. \ What would theories look "
                          r"like that predict numbers, and can be wrong by a visible amount?", 12.2, 29, WHITE),
            wrapped_label(r"4. \ Careers are still built on the number of papers. \ Which incentives would make "
                          r"the careful study the rational one?", 12.2, 29, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.34).move_to([0, 0.35, 0])
        star = wrapped_label(r"$\star$ \ Research problem: \ design a study that could show whether registered "
                             r"reports produce truer findings, and not merely fewer positive ones.", 12.2, 28,
                             P.ACCENT).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Four questions that nobody has closed. <bookmark mark='a'/> One. Are preregistered findings more "
            "often true, or just more often null? A registered report that finds nothing is honest, but a "
            "literature of honest nothings isn't the goal. And nobody has yet run the experiment in which the "
            "practice itself is assigned at random. <bookmark mark='b'/> Two. When a replication fails, was the "
            "original false, or was it true of a narrower group than it claimed? That's the question from Part "
            "2 about who the participants were, and it has no general answer yet. <bookmark mark='c'/> Three. "
            "Meehl's problem is untouched by all of this. Cleaner statistics give you more trustworthy answers "
            "to a weak question. Stronger theories, ones that predict a number, are a different job, and most "
            "of this series is about how that job has been attempted. <bookmark mark='d'/> Four. The incentives "
            "have moved less than the methods have. <bookmark mark='e'/> And this part's research problem. "
            "Design a study that could show whether registered reports give truer findings, and not merely "
            "fewer positive ones. You'll have to say what truer means, and what you'd compare."
        ) as vo:
            self.play(FadeIn(head))
            for mark, q in zip("abcd", qs):
                vo.wait_until(mark)
                self.play(FadeIn(q, shift=UP * 0.12))
            vo.wait_until("e")
            self.play(FadeIn(star, shift=UP * 0.15))
        self.clear_scene()
