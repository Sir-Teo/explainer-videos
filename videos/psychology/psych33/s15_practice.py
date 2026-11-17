from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.hiring()
        self.faking()
        self.products()

    def card(self):
        card = chapter_card(14, r"In practice: \ hiring, \ faking and fit",
                            r"Where are personality scores used, \ and how well?",
                            lit={1991: r"Barrick \& Mount", 2006: r"Birkeland et al."}, part=PART,
                            scale=("person", "society"), marr=("what",))
        with self.voiceover("Chapter fourteen. In practice: hiring, faking and fit."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def hiring(self):
        head = heading(r"Personality at work")
        rows = rows_of([
            (r"Murray Barrick and Michael Mount, \ 1991: \ a meta-analysis of the five traits and job performance in "
             r"five occupational groups, \ from professionals to police to sales", WHITE),
            (r"conscientiousness was the one trait related to every criterion in every group", C_),
            (r"with good composite measures they later put its validity at about .31: \ in the range of Part 32's "
             r"corrected estimate for cognitive ability", YOU),
            (r"and the two barely overlap, \ so together they predict better than either: \ Part 53 builds the "
             r"selection system", GOOD),
        ], 12.4, 24, 0.42).move_to([0, -0.3, 0])
        tag = published_tag(r"Barrick \& Mount (1991)")
        with self.voiceover(
            "Employers use personality tests too. <bookmark mark='a'/> In 1991 Murray Barrick and Michael Mount "
            "meta-analysed the five traits against job performance in five occupational groups, from professionals "
            "to police to sales. <bookmark mark='b'/> Conscientiousness was the one trait related to every criterion "
            "in every group. <bookmark mark='c'/> With good composite measures, they later put its validity at about "
            "point three one, in the range of Part 32's corrected estimate for cognitive ability. "
            "<bookmark mark='d'/> And because the two measure different things, together they predict better than "
            "either alone. Part 53 builds the selection system."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def faking(self):
        d = load("faking")
        head = heading(r"When applicants fake")
        A = axes([-0.6, 2.6], [0, 1.0], x_length=5.6, y_length=3.8, xticks=None, yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 yfmt=lambda v: f"{v:g}", ylabel=r"share of people who faked", center=[-3.0, -0.4, 0], font_size=15)
        keys = ["s10", "s30", "s50"]
        pool = bars(A.ax, np.arange(3) - 0.18, [d[k]["faker_share_pool"] for k in keys], GREY_B, width=0.32)
        hired = bars(A.ax, np.arange(3) + 0.18, [d[k]["faker_share_hired"] for k in keys], N_, width=0.32)
        names = VGroup(*[label(rf"{n}\% fake", font_size=17, color=GREY_A).next_to(A.ax.c2p(i, 0), DOWN, buff=0.2)
                         for i, n in enumerate((10, 30, 50))])
        key = legend([(GREY_B, r"among applicants"), (N_, r"among those hired")], font_size=16).move_to(A.ax.c2p(0.4, 0.92))
        s = d["s30"]
        rows = rows_of([
            (r"Birkeland and colleagues, \ 2006: \ 33 studies comparing applicants with people taking the "
             r"same questionnaire for no stakes: \ applicants score higher, \ most on conscientiousness and emotional "
             r"stability", WHITE),
            (r"Psyche: \ some applicants add 0.8 of a standard deviation to their conscientiousness; \ the employer "
             r"hires the top tenth", MODEL),
            (rf"if 30\% fake, \ they are {pct(s['faker_share_hired'])} of those hired", N_),
            (rf"the hires still perform about as well, \ {s['perf_hired']:.2f} against {s['perf_honest']:.2f} SD, \ "
             r"because the test's validity was modest to begin with: \ faking mostly reshuffles who gets the job",
             YOU),
        ], 5.8, 20, 0.34).move_to([3.5, -0.3, 0])
        tag = psyche_tag(r"\texttt{personality.faking}; \ Birkeland et al.\ (2006)")
        with self.voiceover(
            "But applicants know what employers want. <bookmark mark='a'/> In 2006 Birkeland and colleagues "
            "pooled thirty-three studies comparing applicants with people answering the same questionnaire with "
            "nothing at stake. Applicants scored higher, most on conscientiousness and emotional stability. "
            "<bookmark mark='b'/> Psyche lets some applicants add eight tenths of a standard deviation to their "
            "conscientiousness, and the employer hires the top tenth. <bookmark mark='c'/> If thirty percent fake, "
            f"they make up {spct(s['faker_share_hired'])} of those hired. <bookmark mark='d'/> The hires still "
            f"perform about as well, {s['perf_hired']:.2f} of a standard deviation above average against "
            f"{s['perf_honest']:.2f} with honest answers, because the test's validity was modest to begin with. "
            "Faking mostly reshuffles who gets the job, which is its own question of fairness."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(pool), FadeIn(key), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(hired), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def products(self):
        head = heading(r"Products, \ judged")
        items = [
            (r"team ``fit'' and type workshops", r"types are unstable and lose information \ (chapter four)", LOST),
            (r"matching partners by personality", r"traits predict relationships modestly; \ ask whether the "
                                                  r"matching formula was ever tested against outcomes", N_),
            (r"marketing segments by personality", r"traits can be inferred; \ whether targeting moves people is "
                                                   r"contested \ (chapter twelve)", O_),
            (r"clinical assessment", r"validated inventories and structured interviews, \ not inkblots \ (chapter "
                                     r"ten)", GOOD),
        ]
        rows = VGroup()
        for what, verdict, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=21, width=4.6), wrapped_label(verdict, 7.2, 21, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([0, 0.2, 0])
        foot = wrapped_label(r"the questions to ask of any product: \ which trait, \ measured how reliably, \ "
                             r"predicting what, \ validated against what?", 12.0, 22, YOU).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Personality is also sold. <bookmark mark='a'/> Team fit and type workshops rest on types, which are "
            "unstable and lose information. <bookmark mark='b'/> Matching partners by personality: traits predict "
            "relationships modestly, so ask whether the matching formula was ever tested against "
            "outcomes. <bookmark mark='c'/> Marketing segments by personality: traits can be inferred, but whether "
            "targeting moves people is contested. <bookmark mark='d'/> And clinical assessment should rest on "
            "validated inventories and structured interviews, not inkblots. <bookmark mark='e'/> The questions to ask "
            "of any product are the same: which trait, measured how reliably, predicting what, and validated against "
            "what?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.clear_scene()
