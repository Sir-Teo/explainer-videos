from __future__ import annotations

from videos.psychology.psych33.common import *  # noqa: F403


class Stability(VoiceoverScene):
    def construct(self):
        self.card()
        self.rank()
        self.means()
        self.change()

    def card(self):
        card = chapter_card(7, r"Stability and change", r"Is the person at twenty the person at sixty?",
                            lit={2000: r"Roberts \& DelVecchio", 2006: r"Roberts et al.", 2021: r"Stieger et al."},
                            part=PART, scale=("person",), marr=("what",))
        with self.voiceover("Chapter seven. Stability and change."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rank(self):
        head = heading(r"Keeping your place")
        A = axes([0, 75], [0, 1.0], x_length=6.0, y_length=3.8, xticks=[5, 20, 40, 60], yticks=[0, 0.25, 0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"age", ylabel=r"rank-order stability",
                 center=[-2.9, -0.4, 0], font_size=15)
        pts = [(4, 0.3, r"about .3"), (22, 0.6, r"about .6"), (55, 0.7, r"about .7")]
        line = curve(A.ax, [p[0] for p in pts], [p[1] for p in pts], PERSON, stroke_width=4)
        dots = VGroup(*[VGroup(Dot(A.ax.c2p(x, y), radius=0.08, color=PERSON),
                               label(t, font_size=17, color=PERSON).next_to(A.ax.c2p(x, y), UP, buff=0.12))
                        for x, y, t in pts])
        rows = rows_of([
            (r"rank-order stability: \ the correlation between people's scores now and some years later, \ "
             r"over an interval of about seven years", WHITE),
            (r"Brent Roberts and Wendy DelVecchio, \ 2000: \ 152 longitudinal studies: \ about .3 in early childhood, "
             r"\ about .6 by early adulthood, \ about .7 later", PERSON),
            (r"stability rises with age, \ but never reaches 1: \ people keep changing, \ more slowly", YOU),
        ], 5.6, 21, 0.38).move_to([3.6, -0.3, 0])
        tag = published_tag(r"Roberts \& DelVecchio (2000)")
        with self.voiceover(
            "Now time. First, do people keep their place in the order? <bookmark mark='a'/> Rank-order stability is "
            "the correlation between people's scores now and their scores some years later; here, over about seven "
            "years. <bookmark mark='b'/> In 2000 Brent Roberts and Wendy DelVecchio pooled a hundred and fifty-two "
            "longitudinal studies. Stability was about point three in early childhood, about point six by early "
            "adulthood, and about point seven later on. <bookmark mark='c'/> It rises with age, and never reaches "
            "one. People keep changing, more slowly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(line), LaggedStart(*[FadeIn(d_) for d_ in dots], lag_ratio=0.4), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def means(self):
        d = load("ages")
        head = heading(r"Growing up, \ on average")
        A = axes([15, 60], [2.6, 5.2], x_length=6.0, y_length=3.8, xticks=[20, 30, 40, 50, 60],
                 yticks=[3.0, 3.5, 4.0, 4.5, 5.0], xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}",
                 xlabel=r"age \ (SAPA, \ 2010: \ a cross-section)", ylabel=r"mean score \ (1 to 6)",
                 center=[-2.9, -0.4, 0], font_size=15)
        lines = VGroup()
        for t in ("A", "C", "E", "N", "O"):
            ys = d[f"m_{t}"]
            lines.add(VGroup(curve(A.ax, d["mid"], ys, TRAIT_COL[t], stroke_width=4),
                             scatter(A.ax, d["mid"], ys, TRAIT_COL[t], radius=0.06),
                             label(t, font_size=18, color=TRAIT_COL[t]).next_to(A.ax.c2p(d["mid"][-1], ys[-1]), RIGHT,
                                                                                buff=0.1)))
        rows = rows_of([
            (r"Brent Roberts, \ Kate Walton and Wolfgang Viechtbauer, \ 2006: \ 92 longitudinal samples: \ "
             r"conscientiousness, \ emotional stability and social dominance rise, \ most between 20 and 40", WHITE),
            (rf"the SAPA sample shows the same direction: \ agreeableness from {d['m_A'][0]:.2f} to "
             rf"{d['m_A'][-1]:.2f}, \ neuroticism from {d['m_N'][0]:.2f} to {d['m_N'][-1]:.2f}", A_),
            (r"but it is one year's cross-section: \ Part 31's warning applies, \ and age and cohort are tangled", COHORT),
            (r"the longitudinal studies agree on the direction: \ on average, \ people become more agreeable, \ "
             r"conscientious and calm, \ sometimes called the maturity principle", YOU),
        ], 5.6, 20, 0.34).move_to([3.6, -0.3, 0])
        tag = published_tag(r"Roberts et al.\ (2006); \ data: \ SAPA (2010)")
        with self.voiceover(
            "Second, do the averages change? <bookmark mark='a'/> In 2006 Brent Roberts, Kate Walton and Wolfgang "
            "Viechtbauer pooled ninety-two longitudinal samples. Conscientiousness, emotional stability and social "
            "dominance rose, mostly between twenty and forty. <bookmark mark='b'/> The SAPA sample points the same "
            f"way. Agreeableness rises from {d['m_A'][0]:.2f} in the late teens to {d['m_A'][-1]:.2f} after fifty, "
            f"and neuroticism falls from {d['m_N'][0]:.2f} to {d['m_N'][-1]:.2f}. <bookmark mark='c'/> But it's "
            "one year's cross-section, so Part 31's warning applies: age and cohort are tangled. "
            "<bookmark mark='d'/> The longitudinal studies agree on the direction. On average people become more "
            "agreeable, conscientious and calm as they grow up, a pattern sometimes called the maturity principle."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(l_) for l_ in lines], lag_ratio=0.3), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def change(self):
        head = heading(r"Changing on purpose")
        A = axes([-0.6, 2.6], [-0.8, 0.8], x_length=5.4, y_length=3.6, xticks=None, yticks=[-0.6, -0.3, 0, 0.3, 0.6],
                 yfmt=lambda v: f"{v:g}", ylabel=r"change, \ $d$", center=[-3.2, -0.4, 0], font_size=15)
        vals = [(0, 0.52, r"wanted more: \ self", GOOD), (1, -0.58, r"wanted less: \ self", N_),
                (2, 0.35, r"wanted more: \ observers", A_)]
        bs = VGroup()
        for x, v, t, c in vals:
            bs.add(VGroup(bars(A.ax, [x], [v], c, width=0.55), label(f"{v:+.2f}", font_size=16, color=c)
                          .next_to(A.ax.c2p(x, v), UP if v > 0 else DOWN, buff=0.1),
                          wrapped_label(t, 1.5, 15, GREY_A).next_to(A.ax.c2p(x, -0.8), DOWN, buff=0.15)))
        rows = rows_of([
            (r"Nathan Hudson and Chris Fraley, \ 2015: \ students who wanted to change a trait over 16 weeks changed "
             r"modestly in that direction, \ in self-reports and daily behaviour", WHITE),
            (r"Mirjam Stieger and colleagues, \ 2021: \ a three-month smartphone coach, \ randomized, \ 1{,}523 "
             r"people", GOOD),
            (r"self-reported change of about half a standard deviation either way; \ friends and family saw the "
             r"increases, \ $d = 0.35$, \ but not the decreases; \ the changes lasted three months", A_),
            (r"traits are stable enough to measure and open enough to change: \ the frontier is how far, \ and for "
             r"whom", YOU),
        ], 6.4, 20, 0.34).move_to([3.0, -0.3, 0])
        tag = published_tag(r"Hudson \& Fraley (2015); \ Stieger et al.\ (2021)")
        with self.voiceover(
            "Third, can you change on purpose? <bookmark mark='a'/> In 2015 Nathan Hudson and Chris Fraley followed "
            "students who wanted to change a trait for sixteen weeks. Those who wanted more of a trait gained a "
            "little of it, in self-reports and in daily behaviour. <bookmark mark='b'/> In 2021 Mirjam Stieger and "
            "colleagues randomized one thousand five hundred and twenty-three people to a three-month smartphone "
            "coach or a waiting list. <bookmark mark='c'/> People reported changes of about half a standard "
            "deviation in the direction they wanted. Friends and family saw the increases, with an effect of point "
            "three five, though not the decreases, and the changes lasted three months after the coaching ended. "
            "<bookmark mark='d'/> Traits are stable enough to measure and open enough to change. How far, and for "
            "whom, is the frontier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(b) for b in bs], lag_ratio=0.3), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
