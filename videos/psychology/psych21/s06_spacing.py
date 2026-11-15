from __future__ import annotations

from videos.psychology.psych21.common import *  # noqa: F403

RI_COL = (TRACE, CUE, CTX, FALSE)


class Spacing(VoiceoverScene):
    def construct(self):
        self.card()
        self.effect()
        self.ridge()
        self.model()
        self.fit()
        self.why()

    def card(self):
        card = chapter_card(5, r"Spacing", r"When should you study again?",
                            lit={1885: r"Ebbinghaus", 2005: r"Pavlik \& Anderson", 2006: r"Cepeda et al.",
                                 2008: r"Cepeda et al."},
                            part=PART, scale=("mind", "person"), marr=("what", "how"))
        with self.voiceover("Chapter five. Spacing."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def effect(self):
        head = heading(r"The spacing effect")
        massed = VGroup(*[Rectangle(width=0.18, height=0.6, fill_color=CUE, fill_opacity=0.9, stroke_width=0)
                          for _ in range(6)]).arrange(RIGHT, buff=0.04)
        spaced = VGroup(*[Rectangle(width=0.18, height=0.6, fill_color=TRACE, fill_opacity=0.9, stroke_width=0)
                          for _ in range(6)]).arrange(RIGHT, buff=0.9)
        line1 = NumberLine(x_range=[0, 10, 1], length=9.0, include_numbers=False, color=GREY_C)
        line2 = line1.copy()
        g1 = VGroup(label(r"massed", font_size=26, color=CUE), line1).arrange(RIGHT, buff=0.4).move_to([0, 1.7, 0])
        g2 = VGroup(label(r"spaced", font_size=26, color=TRACE), line2).arrange(RIGHT, buff=0.4).move_to([0, 0.5, 0])
        massed.move_to(line1.n2p(0.8)).align_to(line1, DOWN).shift(UP * 0.02)
        spaced.move_to(line2.n2p(4.5)).align_to(line2, DOWN).shift(UP * 0.02)
        test = VGroup(*[label(r"test", font_size=22, color=LOST).next_to(l_.n2p(10), UP, buff=0.1)
                        for l_ in (line1, line2)])
        rows = rows_of([
            (r"the same study time, \ the same test: \ spread out, \ it is remembered far better", WHITE),
            (r"Ebbinghaus saw it in 1885: \ 38 repetitions over three days beat 68 in one", TRACE),
            (r"Cepeda and colleagues, \ 2006: \ hundreds of experiments over a century; \ spacing wins almost "
             r"everywhere", CUE),
            (r"one of the largest and most general effects in all of psychology, \ and rarely used: \ schools mass "
             r"by topic, \ students cram", LOST),
        ], 12.4, 25, 0.3).to_edge(DOWN, buff=0.65)
        tag = historical_tag(r"Ebbinghaus (1885); \ Cepeda et al.\ (2006)")
        with self.voiceover(
            "Now the first of two ways to forget less. <bookmark mark='a'/> Give two groups the same amount of study "
            "and the same test. One studies all at once; the other spreads the same study out. The spread-out group "
            "remembers far more. <bookmark mark='b'/> Ebbinghaus saw this too: thirty-eight repetitions of a list "
            "spread over three days did as well as sixty-eight crammed into one. <bookmark mark='c'/> In 2006 "
            "Nicholas Cepeda and colleagues reviewed the experiments of a century, hundreds of them, and spacing "
            "beat massing almost everywhere, for words, facts, skills, children and adults. "
            "<bookmark mark='d'/> It's one of the largest and most general effects in psychology, and one of the "
            "least used. Schools teach a topic in a block and move on, and students cram the night before."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(g1), FadeIn(g2), FadeIn(test))
            vo.wait_until("a")
            self.play(FadeIn(massed), FadeIn(spaced), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def ridge(self):
        c = archive.CEPEDA_2008.data
        head = heading(r"How long a gap? \ It depends on how long you need it")
        strip = trial_strip([
            (r"session 1", label(r"learn 32 facts", font_size=24, color=TRACE), r"to criterion"),
            (r"gap: \ 0 to 105 days", label(r"\dots", font_size=34, color=GREY_B), ""),
            (r"session 2", label(r"study again", font_size=24, color=CUE), r"with feedback"),
            (r"retention: \ 7 to 350 days", label(r"\dots", font_size=34, color=GREY_B), ""),
            (r"final test", label(r"recall", font_size=24, color=LOST), ""),
        ], frame_w=2.2, frame_h=1.0, font_size=17).move_to([0, 1.6, 0])
        rows = rows_of([
            (rf"Cepeda, \ Vul, \ Rohrer, \ Wixted and Pashler, \ 2008: \ {num(c['n'])} people online, \ 32 obscure "
             r"facts, \ 26 combinations of gap and retention interval", WHITE),
            (r"for each retention interval there is a best gap: \ too short and too long are both worse", TRACE),
            (r"the best gap grows with the retention interval, \ but more slowly: \ about 20 to 40\% of a week, \ "
             r"about 5 to 10\% of a year", CUE),
            (r"so: \ to remember for a year, \ review after about a month, \ not the next day", MODEL),
        ], 12.4, 25, 0.32).to_edge(DOWN, buff=0.65)
        tag = historical_tag(archive.CEPEDA_2008.cite)
        with self.voiceover(
            "So when should you study again? In 2008 Cepeda, Edward Vul, Doug Rohrer, John Wixted and Hal Pashler "
            "ran the study that answers it. <bookmark mark='a'/> More than thirteen hundred people, online, learnt "
            "thirty-two obscure facts. After a gap of anything from zero to a hundred and five days, they studied "
            "them again. And after a retention interval of a week, five weeks, ten weeks or almost a year, they "
            "were tested. <bookmark mark='b'/> For each retention interval there was a best gap. Too short was "
            "worse, and so was too long. <bookmark mark='c'/> And the best gap grew with the time you need to "
            "remember, but more slowly than it: about twenty to forty percent of a one-week interval, and about five "
            "to ten percent of a year. Cepeda called it the temporal ridgeline. <bookmark mark='d'/> To remember for "
            "an exam next week, review in a day or two. To remember for a year, review after a month or so."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(strip))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def model(self):
        head = heading(r"Derivation: \ Pavlik and Anderson's model")
        eqs = VGroup(
            MathTex(r"m(t) = \ln \sum_{j} (t - t_j)^{-d_j}", font_size=40),
            MathTex(r"d_j = c\, e^{m(t_j)} + a", font_size=40, color=CUE),
            MathTex(r"P(\text{recall}) = \frac{1}{1 + e^{-(m - \theta)/s}}", font_size=36, color=TRACE),
        ).arrange(DOWN, buff=0.4).move_to([-3.2, 0.4, 0])
        rows = rows_of([
            (r"each study at time $t_j$ leaves a trace that decays as a power of its age: \ ACT-R's activation "
             r"\ (Part 20)", GREY_A),
            (r"the new idea: \ the trace's decay $d_j$ depends on how active the memory was \emph{when it was "
             r"studied}", CUE),
            (r"study it again while it is still strong, \ and the new trace decays fast; \ wait until it has "
             r"weakened, \ and it decays slowly", TRACE),
            (r"so massed study buys a quick, \ short-lived boost, \ and spacing a slower, \ lasting one", MODEL),
        ], 6.2, 22, 0.3).move_to([3.6, 0.2, 0])
        tag = published_tag(r"Pavlik \& Anderson (2005)")
        with self.voiceover(
            "Why should a gap help? Philip Pavlik and John Anderson extended ACT-R's activation from the last part. "
            "<bookmark mark='a'/> Each time you study something, at time t j, you leave a trace that decays as a "
            "power of its age, and the memory's activation is the log of the sum of its traces. "
            "<bookmark mark='b'/> Their new idea is the second line. The decay rate of each new trace depends on "
            "how active the memory was at the moment you studied it. <bookmark mark='c'/> Study it again while "
            "it's still strong, and the new trace decays fast. Wait until it has weakened, and the new trace decays "
            "slowly. <bookmark mark='d'/> So cramming buys a quick boost that's soon gone, and spacing a slower one "
            "that lasts. And a logistic of the activation gives the chance of recall."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Indicate(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(Write(eqs[2]), FadeIn(rows[3]))
        self.clear_scene()

    def fit(self):
        d = load("spacing")
        c = archive.CEPEDA_2008.data
        head = heading(r"The model's ridgeline, \ against Cepeda's")
        gaps, R = d["gaps"], d["recall"]
        A = axes([0, 120], [0.55, 0.95], x_length=6.0, y_length=3.6, xticks=[0, 30, 60, 90, 120],
                 yticks=[0.6, 0.7, 0.8, 0.9], yfmt=lambda v: f"{100 * v:.0f}\\%",
                 xlabel=r"gap between the two study sessions \ (days)", ylabel=r"the model: \ recall at the test",
                 center=[-3.4, 0.35, 0], font_size=18)
        cs = VGroup(*[curve(A.ax, gaps, R[i], RI_COL[i], 4) for i in range(4)])
        tops = VGroup(*[Dot(A.ax.c2p(d["best"][i], R[i].max()), radius=0.08, color=RI_COL[i]) for i in range(4)])
        key = legend([(RI_COL[i], rf"tested after {int(d['ri'][i])} days") for i in range(4)], font_size=18)
        key.arrange_in_grid(rows=2, cols=2, buff=(0.4, 0.1)).next_to(A, DOWN, buff=0.2)
        lri = np.log10(d["ri"])
        B = axes([0.7, 2.7], [0.0, 1.6], x_length=4.2, y_length=3.2, xticks=list(lri), yticks=[0, 1],
                 xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: {0: "1", 1: "10"}[int(round(v))],
                 xlabel=r"retention interval \ (days)", ylabel=r"best gap \ (days)", center=[3.6, 0.6, 0],
                 font_size=18)
        data_pts = VGroup(*[Dot(B.ax.c2p(x, np.log10(g)), radius=0.09, color=DATA) for x, g in
                            zip(lri, c["optimal_gap_days"])])
        model_pts = VGroup(*[Dot(B.ax.c2p(x, np.log10(g)), radius=0.08, color=MODEL) for x, g in
                             zip(lri, d["best"])])
        bkey = legend([(DATA, r"Cepeda's data \ (interpolated)"), (MODEL, r"the model")], font_size=18)
        bkey.next_to(B, UP, buff=0.15)
        gain = R.max(1) / R[:, 0] - 1
        rows = rows_of([
            (rf"the peak moves later, \ and more slowly than the interval: \ "
             rf"{100 * d['ratio'][0]:.0f}\% of a week, \ {100 * d['ratio'][3]:.0f}\% of a year", MODEL),
            (rf"but the size is wrong: \ the data's best gap beat a zero gap by "
             rf"{100 * c['recall_gain'][0]:.0f} to {100 * max(c['recall_gain']):.0f}\%; \ the model's, \ by "
             rf"{100 * gain.max():.0f}\% at most", LOST),
        ], 5.4, 20, 0.2).move_to([3.6, -2.35, 0])
        ptag = psyche_tag(r"\texttt{memory.spacing\_ridge}: \ set once, \ not fitted")
        with self.voiceover(
            "Run the model on Cepeda's design. Study once, study again after a gap, and test after each of the four "
            "retention intervals. <bookmark mark='a'/> For each interval there's a best gap, and recall falls on "
            "both sides of it. <bookmark mark='b'/> On the right are the best gaps: the ones Cepeda interpolated "
            "from his data, about three, eight, twelve and twenty-seven days, and the model's. The peak moves later "
            "as the interval grows, and more slowly than the interval: "
            f"{100 * d['ratio'][0]:.0f} percent of a week, {100 * d['ratio'][3]:.0f} percent of almost a year. "
            "The model's parameters weren't fitted to these data. The ridgeline falls out of one idea: a trace laid "
            "down on a weakened memory lasts longer. <bookmark mark='c'/> But look at the size. In the data, the "
            f"best gap beat studying twice in a row by {100 * c['recall_gain'][0]:.0f} percent at a week and by more "
            f"than a hundred percent at ten weeks. In the model, by {100 * gain.max():.0f} percent at most. It gets the "
            "timing right and the size wrong, and fitting it to Cepeda's recall is one of this part's lab tasks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(ptag))
            self.play(LaggedStart(*[Create(c_) for c_ in cs], lag_ratio=0.3), FadeIn(key), run_time=3.0)
            vo.wait_until("a")
            self.play(FadeIn(tops))
            vo.wait_until("b")
            self.play(FadeIn(B), FadeIn(bkey), FadeIn(data_pts), FadeIn(model_pts), FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def why(self):
        head = heading(r"Why spacing works: \ three accounts")
        rows = rows_of([
            (r"deficient processing: \ a repetition straight after the first feels familiar, \ and gets less "
             r"attention", CUE),
            (r"encoding variability: \ context drifts \ (Part 20), \ so spaced repetitions bind the item to more "
             r"contexts, \ and more cues will find it later", CTX),
            (r"study-phase retrieval: \ the second study reminds you of the first; \ an effortful reminder, \ after "
             r"a gap, \ strengthens more: \ Pavlik and Anderson's rule", TRACE),
            (r"they are not exclusive, \ and the last one leads straight to the next chapter: \ retrieval itself "
             r"is what strengthens", MODEL),
        ], 12.4, 26, 0.42).move_to([0, -0.2, 0])
        with self.voiceover(
            "Why does it work? There are three classic accounts. <bookmark mark='a'/> Deficient processing: a "
            "repetition right after the first feels familiar, so it gets less attention. <bookmark mark='b'/> "
            "Encoding variability, which the last part's drifting context makes precise: spaced repetitions bind "
            "the item to more different contexts, so more future cues will find it. <bookmark mark='c'/> And "
            "study-phase retrieval: the second study reminds you of the first, and a reminder that takes effort, "
            "after a gap, strengthens more. That's Pavlik and Anderson's rule in words. "
            "<bookmark mark='d'/> They aren't exclusive, and the last of them leads to the next chapter. If "
            "retrieving a memory is what strengthens it, then the best way to study may be to test yourself."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
