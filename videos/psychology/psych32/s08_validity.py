from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403


class Validity(VoiceoverScene):
    def construct(self):
        self.card()
        self.school()
        self.restriction()
        self.health()

    def card(self):
        card = chapter_card(7, r"What it predicts", r"How much does a test score tell about a life?",
                            lit={1998: r"Schmidt \& Hunter", 2007: r"Deary et al.", 2022: r"Sackett et al."},
                            part=PART, scale=("person", "group", "society"), marr=("what",))
        with self.voiceover("Chapter seven. What it predicts."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def school(self):
        head = heading(r"School, \ work and income")
        items = [(r"school exams at 16 \ (latent)", 0.81, GOOD), (r"years of education", 0.56, G),
                 (r"occupational status", 0.43, G), (r"job performance \ (2022)", 0.31, VERB), (r"income", 0.20, G)]
        A = axes([0, 1.0], [-0.5, 4.5], x_length=5.4, y_length=4.0, xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"correlation with IQ", center=[-2.0, -0.3, 0], font_size=15)
        bs = VGroup()
        for i, (t, r, c) in enumerate(items):
            y = 4 - i
            b = Rectangle(width=abs(A.ax.c2p(r, 0)[0] - A.ax.c2p(0, 0)[0]), height=0.45, stroke_width=0,
                          fill_color=c, fill_opacity=0.85)
            b.move_to(A.ax.c2p(r / 2, y))
            bs.add(VGroup(b, label(t, font_size=17).next_to(A.ax.c2p(0, y), LEFT, buff=0.15),
                          label(f"{r:.2f}", font_size=17, color=c).next_to(b, RIGHT, buff=0.08)))
        rows = rows_of([
            (r"Ian Deary and colleagues, \ 2007: \ 70{,}000 English children; \ a general factor at 11 and exam "
             r"results at 16 correlated 0.81", GOOD),
            (r"Tarmo Strenze, \ 2007, \ a meta-analysis of longitudinal studies: \ education 0.56, \ occupation "
             r"0.43, \ income 0.20", G),
            (r"Paul Sackett and colleagues, \ 2022: \ job performance about 0.31, \ well below the classic figure "
             r"of about 0.5", VERB),
            (r"strong for school, \ moderate for work, \ weak for money: \ much of a life is not in the score", YOU),
        ], 5.6, 20, 0.34).move_to([3.7, -0.2, 0])
        tag = published_tag(r"Deary et al.\ (2007); \ Strenze (2007); \ Sackett et al.\ (2022)")
        with self.voiceover(
            "Whatever g is, the scores predict. <bookmark mark='a'/> In 2007 Ian Deary and colleagues followed "
            "seventy thousand English children. A general factor measured at eleven and a latent factor of exam "
            "results at sixteen correlated 0.81. <bookmark mark='b'/> In the same year Tarmo Strenze's meta-analysis "
            "of longitudinal studies found correlations of 0.56 with years of education, 0.43 with occupational "
            "status, and 0.20 with income. <bookmark mark='c'/> For job performance, the classic estimate was "
            "about 0.5; in 2022 Paul Sackett and colleagues revised it to about 0.31, for a reason the next "
            "section takes apart. <bookmark mark='d'/> Strong for school, moderate for work, weak for money: much of "
            "a life is not in the score."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(bs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(bs[1]), FadeIn(bs[2]), FadeIn(bs[4]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(bs[3]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def restriction(self):
        d = load("validity")
        head = heading(r"Range restriction")
        A = axes([-3.5, 3.5], [-3.5, 3.5], x_length=4.8, y_length=4.8, xticks=None, yticks=None,
                 xlabel=r"test score", ylabel=r"job performance", center=[-3.4, -0.4, 0], font_size=15)
        x, y, sel = np.asarray(d["x"]), np.asarray(d["y"]), np.asarray(d["sel_idx"], bool)
        out_pts = scatter(A.ax, x[~sel], y[~sel], GREY_B, radius=0.025, opacity=0.5)
        in_pts = scatter(A.ax, x[sel], y[sel], G, radius=0.03, opacity=0.9)
        cut = DashedLine(A.ax.c2p(d["cut"], -3.5), A.ax.c2p(d["cut"], 3.5), color=LOST, stroke_width=2)
        eq = label(r"$R = \dfrac{r/u}{\sqrt{1 - r^2 + r^2/u^2}}$", font_size=30, color=MODEL)
        rows = rows_of([
            (rf"in Psyche's applicants the test predicts performance with $r = {d['r_pop']:.2f}$", WHITE),
            (rf"but only the top 30\% are hired, \ and only they have performance ratings: \ among them $r = "
             rf"{d['r_sel']:.2f}$", G),
            (rf"Thorndike's correction, \ with $u = {d['u']:.2f}$ the hired group's spread over the applicants', \ "
             rf"gives back {d['r_corrected']:.2f}", MODEL),
            (r"Sackett's point: \ the old meta-analyses applied large corrections where the real restriction was "
             r"small or unknown, \ and so overstated validity", VERB),
        ], 5.6, 20, 0.34).move_to([3.4, -0.6, 0])
        eq.next_to(rows, UP, buff=0.3)
        tag = psyche_tag(r"\texttt{traits.restriction\_corrected}; \ simulated applicants")
        with self.voiceover(
            "Validity studies have a hidden problem. <bookmark mark='a'/> In Psyche's population of applicants, a "
            f"test predicts job performance with a correlation of {d['r_pop']:.2f}. <bookmark mark='b'/> But only "
            "the top thirty percent are hired, and only they ever get performance ratings. Among them the "
            f"correlation is {d['r_sel']:.2f}. <bookmark mark='c'/> Thorndike's correction for range restriction "
            "uses the ratio u of the hired group's spread to the applicants', and gives back "
            f"{d['r_corrected']:.2f}, when its assumptions hold. <bookmark mark='d'/> Sackett's argument is that "
            "the older meta-analyses applied large corrections in studies where the real restriction was small or "
            "unknown, and so overstated validity. Corrected properly, it's about 0.31: still useful, and no longer "
            "the clear best predictor of job performance."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(out_pts), FadeIn(in_pts), FadeIn(rows[0]), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(cut), out_pts.animate.set_opacity(0.15), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(eq), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def health(self):
        head = heading(r"Health and a longer life")
        A = axes([0, 1.1], [-0.6, 2.6], x_length=4.6, y_length=3.4, xticks=[0, 0.25, 0.5, 0.75, 1.0], yticks=None,
                 xfmt=lambda v: f"{v:g}", xlabel=r"share of the association left", center=[-3.9, -0.2, 0],
                 font_size=14)
        left = [1.0, 0.66, 0.46]
        names = [r"unadjusted", r"after adult SES", r"after education"]
        hb = VGroup()
        for i, (v, nm) in enumerate(zip(left, names)):
            y = 2.0 - 1.0 * i
            r_ = Rectangle(width=A.ax.c2p(v, 0)[0] - A.ax.c2p(0, 0)[0], height=0.42, stroke_width=0,
                           fill_color=[GOOD, G, VERB][i], fill_opacity=0.85)
            r_.move_to(A.ax.c2p(0, y), aligned_edge=LEFT)
            hb.add(VGroup(r_, label(nm, font_size=16, color=GREY_A).next_to(r_, UP, buff=0.06, aligned_edge=LEFT)))
        rows = rows_of([
            (r"Catherine Calvin and colleagues, \ 2011: \ 16 studies following people from youth for up to 69 years",
             WHITE),
            (r"one standard deviation higher in early test scores, \ about 15 IQ points: \ about 24\% lower risk of "
             r"death during follow-up", GOOD),
            (r"adjusting for adult socioeconomic status shrank the association by about a third, \ for education by "
             r"about a half", G),
            (r"so part of the link runs through the lives people go on to have; \ the rest is unexplained, \ and the "
             r"field that studies it is called cognitive epidemiology", VERB),
        ], 7.0, 22, 0.38).move_to([2.9, -0.3, 0])
        tag = published_tag(r"Calvin et al.\ (2011)")
        with self.voiceover(
            "The scores even predict how long people live. <bookmark mark='a'/> In 2011 Catherine Calvin and "
            "colleagues pooled sixteen studies that followed people from youth for up to sixty-nine years. "
            "<bookmark mark='b'/> One standard deviation higher in early test scores, about fifteen IQ points, went "
            "with about a twenty-four percent lower risk of death during follow-up. <bookmark mark='c'/> Adjusting "
            "for adult socioeconomic status shrank the association by about a third, and for education by about a "
            "half. <bookmark mark='d'/> So part of the link runs through the lives people go on to have. The rest is "
            "unexplained, and the field that studies it is called cognitive epidemiology."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hb[0], shift=RIGHT * 0.15), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b_, shift=RIGHT * 0.15) for b_ in hb[1:]], lag_ratio=0.4), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=RIGHT * 0.15))
        self.clear_scene()
