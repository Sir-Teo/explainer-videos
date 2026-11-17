from __future__ import annotations

from videos.psychology.psych35.common import *  # noqa: F403


class Power(VoiceoverScene):
    def construct(self):
        self.card()
        self.story()
        self.curse()

    def card(self):
        card = chapter_card(8, r"Power posing", r"Can two minutes of posture change your hormones?",
                            lit={2010: r"Carney, \ Cuddy \& Yap", 2015: r"Ranehill et al."}, part=PART,
                            scale=("person", "body"), marr=("what",))
        with self.voiceover("Chapter eight. Power posing."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def story(self):
        head = heading(r"A pose, \ a talk, \ and a reversal")
        rows = rows_of([
            (r"Carney, \ Cuddy and Yap, \ 2010: \ 42 people held expansive or contracted poses for a few minutes; "
             r"\ expansive posers showed more testosterone, \ less cortisol and more risk-taking", WHITE),
            (r"a talk about it became one of the most watched of its kind", CROWD),
            (r"Ranehill and colleagues, \ 2015: \ 200 people: \ they felt "
             r"more powerful, \ but there was no effect on hormones or on behaviour", AUTH),
            (r"in 2016 the first author, \ Dana Carney, \ posted that she no longer believed the effects were real "
             r"and had stopped studying them", PERSON),
            (r"what remains: \ a small effect on how powerful people say they feel; \ Amy Cuddy maintains that "
             r"posture feeds back on feelings", YOU),
        ], 12.4, 22, 0.36).move_to([0, -0.3, 0])
        tag = published_tag(r"Carney, \ Cuddy \& Yap (2010); \ Ranehill et al.\ (2015)")
        with self.voiceover(
            "The second collapse was more public. <bookmark mark='a'/> In 2010 Carney, Cuddy and Yap "
            "had forty-two people hold expansive or contracted poses for a few minutes. The expansive posers showed "
            "more testosterone, less cortisol, and more appetite for risk. <bookmark mark='b'/> A talk about it "
            "became one of the most watched talks of its kind. <bookmark mark='c'/> In 2015 Ranehill and "
            "colleagues repeated it with two hundred people. "
            "People felt more powerful, but there was no effect on hormones or on behaviour. "
            "<bookmark mark='d'/> In 2016 the first author, Carney, posted that she no longer believed the effects "
            "were real, and had stopped studying them. <bookmark mark='e'/> What remains is a small effect on how "
            "powerful people say they feel. Cuddy maintains that posture feeds back on feelings."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def curse(self):
        d = load("curse")
        head = heading(r"Why small significant studies look big")
        edges = np.linspace(0, 1.6, 33)
        mids = (edges[:-1] + edges[1:]) / 2
        A = axes([0, 1.6], [0, 1.0], x_length=6.0, y_length=3.4, xticks=[0, 0.4, 0.8, 1.2, 1.6], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"effect size $d$ reported", center=[-3.0, -0.4, 0], font_size=15)
        h_small = np.asarray(d["d2_n21_hist"], float)
        h_big = np.asarray(d["d2_n100_hist"], float)
        hs = VGroup(bars(A.ax, mids, h_small / h_small.max() * 0.9, AUTH, width=0.045, opacity=0.7),
                    bars(A.ax, mids, h_big / h_big.max() * 0.9, CROWD, width=0.045, opacity=0.5))
        true = DashedLine(A.ax.c2p(0.2, 0), A.ax.c2p(0.2, 1.0), color=GOOD, stroke_width=3)
        tl = label(r"true $d = 0.2$", font_size=16, color=GOOD).next_to(A.ax.c2p(0.2, 1.0), RIGHT, buff=0.08)
        key = legend([(AUTH, r"21 per group, \ significant ones"), (CROWD, r"100 per group, \ significant ones")],
                     font_size=15).move_to(A.ax.c2p(1.1, 0.75))
        rows = rows_of([
            (r"Psyche runs 20{,}000 studies of a true effect of $d = 0.2$, \ with 21 people per group, \ about the "
             r"size of the 2010 study, \ and with 100", WHITE),
            (rf"with 21 per group only {pct(d['d2_n21_power'])} reach significance, \ and those report an average "
             rf"$d$ of {d['d2_n21_dsig']:.2f}: \ nearly four times the truth", AUTH),
            (rf"with 100 per group, \ {pct(d['d2_n100_power'])} do, \ reporting {d['d2_n100_dsig']:.2f}", CROWD),
            (r"a small study that clears the bar must have overestimated: \ the winner's curse; \ a larger replication "
             r"then looks like a failure even when the effect is real", YOU),
        ], 5.6, 19, 0.32).move_to([3.6, -0.3, 0])
        tag = psyche_tag(r"simulated: \ the winner's curse")
        with self.voiceover(
            "Why do small studies with striking results so often shrink? <bookmark mark='a'/> Psyche runs twenty "
            "thousand studies of a real but small effect, with twenty-one people per group, about the size of the "
            "2010 study, and with a hundred. <bookmark mark='b'/> With twenty-one per group, only "
            f"{spct(d['d2_n21_power'])} reach significance, and those report an average effect nearly four times "
            "the truth. <bookmark mark='c'/> With a hundred per group, "
            f"{spct(d['d2_n100_power'])} do, and they overestimate by much less. <bookmark mark='d'/> A small study "
            "that clears the bar must have overestimated. It's called the winner's curse, Part 4's lesson, and it "
            "means a larger replication looks like a failure even when the effect is real."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(true), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hs[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(hs[1]), FadeIn(key), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
