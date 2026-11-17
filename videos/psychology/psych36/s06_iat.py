from __future__ import annotations

from videos.psychology.psych36.common import *  # noqa: F403


class IAT(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.model()
        self.reliability()
        self.prediction()
        self.change()

    def card(self):
        card = chapter_card(5, r"Measuring by speed", r"What does an Implicit Association Test score mean?",
                            lit={1998: r"Greenwald et al.", 2013: r"Oswald et al.", 2019: r"Forscher et al."},
                            part=PART, scale=("person",), marr=("how",))
        with self.voiceover("Chapter five. Measuring by speed."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def task(self):
        head = heading(r"Two keys, \ two pairings")
        def screen(left, right, color):
            box = RoundedRectangle(corner_radius=0.1, width=4.4, height=2.0, stroke_color=color, fill_color="#14181F",
                                   fill_opacity=1)
            lt = label(left, font_size=17, color=color).move_to(box.get_corner(UL) + [1.0, -0.35, 0])
            rt = label(right, font_size=17, color=color).move_to(box.get_corner(UR) + [-1.0, -0.35, 0])
            keys = VGroup(label(r"E", font_size=18, color=GREY_A).move_to(box.get_corner(DL) + [0.5, 0.35, 0]),
                          label(r"I", font_size=18, color=GREY_A).move_to(box.get_corner(DR) + [-0.5, 0.35, 0]))
            return VGroup(box, lt, rt, keys)
        a = screen(r"flower or pleasant", r"insect or unpleasant", GOOD).move_to([-3.5, 1.3, 0])
        b = screen(r"insect or pleasant", r"flower or unpleasant", AUTH).move_to([-3.5, -1.2, 0])
        la = label(r"compatible: \ fast", font_size=16, color=GOOD).next_to(a, DOWN, buff=0.1)
        lb = label(r"incompatible: \ slower", font_size=16, color=AUTH).next_to(b, DOWN, buff=0.1)
        rows = rows_of([
            (r"Greenwald, \ McGhee and Schwartz, \ 1998: \ sort words and pictures with two keys, \ each key "
             r"shared by a category and an attribute", WHITE),
            (r"when the pairings match what goes together in your memory, \ sorting is fast; \ when they cross, \ "
             r"slower", CROWD),
            (r"the same procedure with pictures of Black and white faces, \ or of young and old, \ gives a measure "
             r"of association with groups that does not ask anything", PERSON),
            (r"the score, \ $D$, \ is the difference in mean times divided by their pooled spread", MODEL),
        ], 6.0, 20, 0.36).move_to([3.3, -0.2, 0])
        tag = historical_tag(r"Greenwald, \ McGhee \& Schwartz (1998)")
        with self.voiceover(
            "The second route is to stop asking. <bookmark mark='a'/> In 1998 Anthony Greenwald and colleagues "
            "introduced the Implicit Association Test. You sort words and pictures with two keys, each key shared "
            "by a category and an attribute. <bookmark mark='b'/> When the pairings match what goes together in "
            "your memory, flowers with pleasant, you sort fast. When they cross, insects with pleasant, you're "
            "slower. <bookmark mark='c'/> The same procedure with faces of Black and white people, or young and "
            "old, gives a measure of association with groups that doesn't ask anything. <bookmark mark='d'/> The "
            "score, called D, is the difference in mean times divided by their pooled spread."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(a), FadeIn(la))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(b), FadeIn(lb), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def model(self):
        head = heading(r"Psyche takes the test")
        A = axes([0, 1.4], [0, 1.0], x_length=5.6, y_length=3.0, xticks=[0, 0.5, 1.0], yticks=None,
                 xfmt=lambda v: f"{v:g} s", xlabel=r"decision time", center=[-3.2, -0.2, 0], font_size=15)
        from scipy.stats import invgauss
        t = np.linspace(0.36, 1.4, 160)
        def dens(drift):
            mu, lam = 1.2 / drift, 1.2 ** 2
            y = invgauss.pdf(t - 0.35, mu / lam, scale=lam)
            return y
        dc, di = dens(2.0 * 1.15), dens(2.0 * 0.85)
        m = max(dc.max(), di.max())
        cc = curve(A.ax, t, dc / m * 0.95, GOOD)
        ci = curve(A.ax, t, di / m * 0.95, AUTH)
        key = legend([(GOOD, r"compatible block"), (AUTH, r"incompatible block")], font_size=15).move_to(
            A.ax.c2p(1.05, 0.8))
        rows = rows_of([
            (r"each decision is a diffusion, \ Part 25's model: \ evidence drifts to a bound", WHITE),
            (r"an association speeds the drift in one block and slows it in the other", CROWD),
            (r"each Psyche person has a stable association, \ plus a part that changes from one occasion to the "
             r"next: \ mood, \ what was seen that morning, \ the room", PERSON),
            (r"and 60 trials per block leave sampling noise of their own", MODEL),
        ], 6.0, 20, 0.36).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{social.iat\_d}")
        with self.voiceover(
            "To see what a D score can tell us, Psyche takes the test. <bookmark mark='a'/> Each decision is a "
            "diffusion, Part 25's model: evidence drifts toward a bound. <bookmark mark='b'/> An association speeds "
            "the drift in one block and slows it in the other, so the incompatible times spread further to the "
            "right. <bookmark mark='c'/> Each of Psyche's people has a stable association, plus a part that changes "
            "from one occasion to the next: mood, what was seen that morning, the room. <bookmark mark='d'/> And "
            "sixty trials per block leave sampling noise of their own."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cc), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ci), FadeIn(key), FadeIn(rows[1]))
            for m_, r in zip("cd", rows[2:]):
                vo.wait_until(m_)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def reliability(self):
        d = load("iat")
        assert abs(d["retest"] - 0.5) < 0.05, d["retest"]
        head = heading(r"The same person, \ twice")
        A = axes([-0.3, 1.1], [-0.3, 1.1], x_length=4.2, y_length=4.2, xticks=[0, 0.5, 1.0], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"$D$, \ first session",
                 ylabel=r"$D$, \ second session", center=[-3.6, -0.3, 0], font_size=15)
        pts = scatter(A.ax, d["d1"], d["d2"], MODEL, radius=0.03, opacity=0.6)
        rows = rows_of([
            (r"400 of Psyche's people take the test twice", WHITE),
            (rf"the two scores correlate {d['retest']:.2f}: \ test-retest reliability", MODEL),
            (r"published estimates for the IAT are about .5, \ against .8 or more for a good questionnaire", CROWD),
            (rf"yet the average person scores {d['mean_d']:.2f}, \ with $t = {d['t']:.0f}$: \ the group's "
             r"association is clear while each person's is not", GOOD),
        ], 6.2, 20, 0.36).move_to([3.2, -0.3, 0])
        tag = psyche_tag(r"simulated: \ 400 people, \ two sessions")
        with self.voiceover(
            "Now four hundred of Psyche's people take the test twice. <bookmark mark='a'/> Each dot is a person, "
            "their first score against their second. <bookmark mark='b'/> The two correlate only about point five. "
            "That's the test-retest reliability. <bookmark mark='c'/> Published "
            "estimates for the real IAT are about point five, against point eight or more for a good "
            "questionnaire. <bookmark mark='d'/> Yet the average person scores clearly above zero, and the group's "
            "association is unmistakable. A measure can be good for a crowd and poor for a person."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(p) for p in pts], lag_ratio=0.004), run_time=2.0)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def prediction(self):
        d = load("iat")
        head = heading(r"What reliability does to prediction")
        A = axes([0, 0.75], [0, 0.3], x_length=4.6, y_length=3.4, xticks=[0, 0.25, 0.5, 0.75], yticks=[0, 0.1, 0.2, 0.3],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"test-retest reliability",
                 ylabel=r"correlation with behaviour", center=[-3.6, -0.3, 0], font_size=15)
        o = np.argsort(d["sweep_retest"])
        sim = scatter(A.ax, d["sweep_retest"][o], d["sweep_r"][o], MODEL, radius=0.06)
        ceil = curve(A.ax, d["sweep_retest"][o], d["sweep_ceiling"][o], GREY_A)
        key = legend([(MODEL, r"simulated"), (GREY_A, r"$0.3\sqrt{\text{reliability}}$")], font_size=14).move_to(
            A.ax.c2p(0.25, 0.27))
        rows = rows_of([
            (r"in Psyche, \ the stable association correlates 0.3 with a behaviour; \ more occasion-to-occasion "
             r"variation lowers reliability, \ and the observed correlation falls with its square root", WHITE),
            (r"Greenwald and colleagues, \ 2009: \ across studies, \ IAT scores predicted racially "
             r"discriminatory behaviour at $r = .24$, \ self-reports at $.12$", CROWD),
            (r"Oswald and colleagues, \ 2013: \ a reanalysis found IATs poor predictors of most kinds of "
             r"behaviour, \ and no better than simple explicit measures", AUTH),
            (r"either way, \ a correlation of .2 means a score is of little use for judging one person", YOU),
        ], 6.2, 19, 0.34).move_to([3.2, -0.3, 0])
        tag = published_tag(r"Greenwald et al.\ (2009); \ Oswald et al.\ (2013)")
        with self.voiceover(
            "Part 3 said that a noisy measure can't correlate with anything more than its reliability allows. "
            "<bookmark mark='a'/> In Psyche, the stable association correlates point three with a behaviour. As "
            "the occasion-to-occasion part grows, reliability falls, and the observed correlation falls with its "
            "square root. <bookmark mark='b'/> In 2009 Greenwald and colleagues pooled studies and found that IAT "
            "scores predicted racially discriminatory behaviour at about point two four, against point one two "
            "for self-reports. <bookmark mark='c'/> In 2013 Oswald and colleagues reanalyzed the literature and "
            "found IATs poor predictors of most kinds of behaviour, and no better than simple explicit measures. "
            "<bookmark mark='d'/> Either way, a correlation near point two means a score is of little use for "
            "judging one person."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(ceil), FadeIn(sim), FadeIn(key), FadeIn(rows[0]))
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def change(self):
        head = heading(r"Change the score, \ change the behaviour?")
        stages = VGroup(*[word_chip(t, color=c, font_size=20, width=3.0) for t, c in (
            (r"intervention", PERSON), (r"implicit score", MODEL), (r"behaviour", GOOD))]).arrange(RIGHT, buff=1.0)
        stages.move_to([0, 1.6, 0])
        a1 = Arrow(stages[0].get_right(), stages[1].get_left(), buff=0.08, color=MODEL)
        a2 = DashedLine(stages[1].get_right(), stages[2].get_left(), buff=0.08, color=GREY_B)
        x = label(r"?", font_size=34, color=AUTH).next_to(a2, UP, buff=0.05)
        rows = rows_of([
            (r"Forscher and colleagues, \ 2019: \ 492 studies, \ 87{,}418 people, \ of procedures meant to change "
             r"implicit measures", WHITE),
            (r"implicit scores can be changed, \ modestly", MODEL),
            (r"explicit measures changed less consistently, \ and behaviour hardly at all", AUTH),
            (r"changes in the implicit score did not carry through to behaviour: \ moving the measure is not "
             r"moving the thing you care about", YOU),
        ], 12.0, 22, 0.4).move_to([0, -1.2, 0])
        tag = published_tag(r"Forscher et al.\ (2019)")
        with self.voiceover(
            "The last test is causal. If you change someone's score, does their behaviour change? "
            "<bookmark mark='a'/> In 2019 Forscher and colleagues pooled four hundred and ninety-two studies, with "
            "eighty-seven thousand people, of procedures meant to change implicit measures. "
            "<bookmark mark='b'/> Implicit scores can be changed, modestly. <bookmark mark='c'/> Explicit measures "
            "changed less consistently, and behaviour hardly at all. <bookmark mark='d'/> And changes in the "
            "implicit score didn't carry through to behaviour. Moving the measure isn't moving the thing you care "
            "about."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(stages))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowArrow(a1), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(a2), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(x), FadeIn(rows[3]))
        self.clear_scene()
