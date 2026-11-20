from __future__ import annotations

from videos.economics.econ21.common import *  # noqa: F403


class Institutions(VoiceoverScene):
    def construct(self):
        card(self, 9, r"Institutions and settler mortality", r"Do property rights and limits on power cause "
             r"prosperity, \ and how could anyone tell?", "Chapter nine. Institutions and settler mortality.",
             lit={2001: r"Acemoglu, Johnson, Robinson", 2012: r"Albouy"}, scale=("nation", "world"),
             horizon=("a century",))
        self.problem()
        self.chain()
        self.fit()
        self.critique()

    def problem(self):
        rows = VGroup(
            label(r"institutions: \ the rules of the game \ (Douglass North)", font_size=26, color=INST),
            label(r"countries with secure property and limits on rulers are richer", font_size=23, color=GREY_A),
            label(r"but richer countries can afford better institutions: \ reverse causation", font_size=23,
                  color=WEDGE),
            label(r"and something else may cause both: \ omitted variables", font_size=23, color=WEDGE),
            label(r"needed: \ something that moved institutions, \ and touched income only through them", font_size=24,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        with self.voiceover(
            "The deepest explanation on offer is institutions, which Douglass North called the rules of the game. "
            "<bookmark mark='a'/> Countries where property is secure and rulers are constrained are much richer. "
            "<bookmark mark='b'/> But that correlation proves little. Rich countries can afford courts and clean "
            "police: causation may run backwards. <bookmark mark='c'/> And something else, geography or culture, "
            "may cause both. <bookmark mark='d'/> To find the effect of institutions you need an instrument, in "
            "the sense of part four: something that moved institutions, and touched income only through them."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mk, r in zip("abcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def chain(self):
        steps = [(r"settler mortality", MORT), (r"settlements", GREY_A), (r"early institutions", INST),
                 (r"institutions today", INST), (r"income today", OUTPUT)]
        boxes = VGroup()
        for t, c in steps:
            b = RoundedRectangle(width=2.3, height=1.0, corner_radius=0.12, stroke_color=c, stroke_width=3)
            boxes.add(VGroup(b, label(t, font_size=19, color=c).move_to(b)))
        boxes.arrange(RIGHT, buff=0.45).move_to(UP * 1.0)
        arrows = VGroup(*[Arrow(boxes[i].get_right(), boxes[i + 1].get_left(), buff=0.06, color=GREY_B)
                          for i in range(4)])
        notes = VGroup(
            label(r"where Europeans died in large numbers, \ they did not settle: \ they set up extractive colonies",
                  font_size=21, color=GREY_A),
            label(r"where they survived, \ they settled, \ and built institutions to protect themselves", font_size=21,
                  color=GREY_A),
            label(r"those institutions persisted after independence", font_size=21, color=GREY_A),
            label(r"the claim: \ mortality affects income today only through institutions", font_size=22,
                  color=E.ACCENT),
        ).arrange(DOWN, buff=0.3).next_to(boxes, DOWN, buff=0.7)
        tag = published_tag(r"Acemoglu, Johnson and Robinson, AER 91(5) (2001): \ 1369--1401", corner=DR,
                            font_size=12)
        with self.voiceover(
            "In 2001 Daron Acemoglu, Simon Johnson and James Robinson proposed one, from the history of colonies. "
            "<bookmark mark='a'/> Where European settlers died in large numbers, from malaria and yellow fever, they "
            "did not settle. They set up colonies to extract resources, with institutions to match. "
            "<bookmark mark='b'/> Where they survived, they settled, and built institutions to protect their own "
            "property and limit their rulers. <bookmark mark='c'/> Those institutions outlived independence. "
            "<bookmark mark='d'/> So the death rates of soldiers and bishops centuries ago should predict "
            "institutions today, and through them, and only through them, income today."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(b_) for b_ in boxes], lag_ratio=0.2),
                      LaggedStart(*[GrowArrow(a_) for a_ in arrows], lag_ratio=0.2), FadeIn(tag), run_time=2.5)
            for mk, n_ in zip("abcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n_, shift=UP * 0.1))
        self.clear_scene()

    def fit(self):
        a = load("ajr")
        z, x, y = np.array(a["logMort"]), np.array(a["Exprop"]), np.array(a["GDP"])
        ax1 = plane([2, 8.2], [3, 10.5], center=LEFT * 3.4 + DOWN * 0.7, x_length=5.4, y_length=4.2,
                    xticks=[np.log(v) for v in (10, 100, 1000)], yticks=[4, 6, 8, 10],
                    xlabel=r"settler deaths per 1{,}000 a year \ (log)", ylabel=r"protection against expropriation",
                    xfmt=lambda v: commas(np.exp(v)), yfmt=lambda v: f"{v:g}", font_size=14)
        ax2 = plane([3, 10.5], [6, 10.5], center=RIGHT * 3.2 + DOWN * 0.7, x_length=5.4, y_length=4.2,
                    xticks=[4, 6, 8, 10], yticks=[6, 7, 8, 9, 10],
                    xlabel=r"protection against expropriation", ylabel=r"log GDP per head, \ 1995",
                    xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", font_size=14)
        d1 = VGroup(*[Dot(ax1.ax.c2p(a_, b_), radius=0.05, color=MORT) for a_, b_ in zip(z, x)])
        d2 = VGroup(*[Dot(ax2.ax.c2p(a_, b_), radius=0.05, color=INST) for a_, b_ in zip(x, y)])
        b1, c1 = np.polyfit(z, x, 1)
        l1 = Line(ax1.ax.c2p(2.2, c1 + b1 * 2.2), ax1.ax.c2p(8.0, c1 + b1 * 8.0), color=WHITE, stroke_width=3)
        b2, c2 = np.polyfit(x, y, 1)
        l2 = Line(ax2.ax.c2p(3.5, c2 + b2 * 3.5), ax2.ax.c2p(10.2, c2 + b2 * 10.2), color=GREY_B, stroke_width=3)
        xm, ym = x.mean(), y.mean()
        x_lo = max(3.2, xm + (6.1 - ym) / a["iv"])
        x_hi = min(10.3, xm + (10.4 - ym) / a["iv"])
        l3 = Line(ax2.ax.c2p(x_lo, ym + a["iv"] * (x_lo - xm)), ax2.ax.c2p(x_hi, ym + a["iv"] * (x_hi - xm)),
                  color=E.ACCENT, stroke_width=4)
        t1 = label(rf"first stage: \ ${a['first']:.2f}$ \ (s.e. {a['first_se']:.2f})", font_size=18,
                   color=WHITE).next_to(ax1, UP, buff=0.2)
        t2 = VGroup(label(rf"OLS: \ {a['ols']:.2f}", font_size=18, color=GREY_B),
                    label(rf"2SLS: \ {a['iv']:.2f} \ (s.e. {a['iv_se']:.2f}; \ published 0.94)", font_size=18,
                          color=E.ACCENT)).arrange(DOWN, buff=0.08).next_to(ax2, UP, buff=0.2)
        src = data_tag(r"Acemoglu, Johnson and Robinson's base sample \ (64 countries), \ via the R package hdm",
                       corner=DR, font_size=11)
        with self.voiceover(
            f"Here are their sixty-four former colonies, refitted from their data. <bookmark mark='a'/> Settler "
            f"mortality ranged from about {a['mort_range'][0]:.0f} to nearly {a['mort_range'][1]:,.0f} deaths per "
            "thousand a year. Where it was high, protection against expropriation is weak today: the first stage, a "
            f"slope of {say_num(a['first'], 2)} on the log of mortality, with a first-stage F of about "
            f"{a['F']:.0f}. <bookmark mark='b'/> And where protection is strong, income is high. Ordinary least "
            f"squares gives {a['ols']:.2f}: a point more protection, on a ten-point scale, goes with about "
            f"{100 * (np.exp(a['ols']) - 1):.0f} percent more income. <bookmark mark='c'/> Two-stage least squares, "
            f"using mortality as the instrument, gives {a['iv']:.2f}, larger, not smaller: about "
            f"{np.exp(a['iv']):.1f} times the income for each point. Their published estimate was 0.94. If the "
            "instrument is valid, institutions explain most of the gap between rich and poor former colonies."
        ) as vo:
            self.play(FadeIn(ax1), FadeIn(ax2), FadeIn(src))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(d) for d in d1], lag_ratio=0.02), run_time=2)
            self.play(Create(l1), FadeIn(t1))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(d) for d in d2], lag_ratio=0.02), run_time=2)
            self.play(Create(l2), FadeIn(t2[0]))
            vo.wait_until("c")
            self.play(Create(l3), FadeIn(t2[1]))
        self.clear_scene()

    def critique(self):
        rows = VGroup(
            label(r"the critics", font_size=30, color=HOLD),
            label(r"David Albouy, \ 2012: \ only 28 of the 64 countries have mortality rates measured there", font_size=22,
                  color=GREY_A),
            label(r"the other 36 were assigned from countries thought to have similar diseases", font_size=22,
                  color=GREY_A),
            label(r"with his corrections the first stage weakens, \ and the 2SLS intervals can become unbounded",
                  font_size=22, color=WEDGE),
            label(r"exclusion: \ disease may hurt income today directly, \ not only through institutions", font_size=22,
                  color=WEDGE),
            label(r"the authors replied, \ disputing the corrections; \ the debate is not settled", font_size=22,
                  color=GREY_A),
            label(r"reversal of fortune \ (2002): \ colonies rich in 1500 are poor today; \ but traced by ancestry, \ "
                  r"peoples with early states and early farming are mostly still rich", font_size=21, color=INST),
        ).arrange(DOWN, buff=0.32).move_to(UP * 0.1)
        tag = published_tag(r"Albouy, AER 102(6) (2012): \ 3059--3076; \ Acemoglu, Johnson and Robinson, QJE 117(4) "
                            r"(2002); \ Putterman and Weil, QJE 125(4) (2010)", corner=DR, font_size=12)
        with self.voiceover(
            "The paper was a landmark, and it was attacked. <bookmark mark='a'/> David Albouy found that only "
            "twenty-eight of the sixty-four countries have mortality rates measured on their own soil. "
            "<bookmark mark='b'/> The other thirty-six were assigned rates from other places judged to have a "
            "similar disease environment. <bookmark mark='c'/> Correcting the assignments he disputed, the first "
            "stage weakened, and the instrumental-variable confidence intervals often became unbounded. "
            "<bookmark mark='d'/> And the exclusion restriction can be questioned on its face: the diseases that "
            "killed settlers may still hold back income directly. <bookmark mark='e'/> Acemoglu, Johnson and "
            "Robinson replied, disputing his corrections, and the debate is not settled. <bookmark mark='f'/> A "
            "companion paper found a reversal of fortune: the colonies that were richest in 1500, measured by "
            "urbanization and population density, are among the poorest today. But Louis Putterman and David Weil "
            "traced today's populations back to where their ancestors lived in 1500, and found that the descendants "
            "of the early states and early farmers are mostly still rich: the reversal is one of places, not of "
            "peoples. Institutions matter. How much they explain is still argued."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(tag))
            for mk, r in zip("abcdef", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()
