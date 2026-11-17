from __future__ import annotations

from videos.psychology.psych46.common import *  # noqa: F403


class Luce(VoiceoverScene):
    def construct(self):
        self.card()
        self.axiom()
        self.mm()
        self.arena()

    def card(self):
        card = chapter_card(3, r"Luce's choice axiom", r"What if the odds between two options ignore the rest?",
                            lit={1952: r"Bradley \& Terry", 1959: r"Luce"}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter three. Luce's choice axiom."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def axiom(self):
        head = heading(r"One axiom")
        eqs = VGroup(
            MathTex(r"\frac{P(i \mid \text{menu})}{P(j \mid \text{menu})} = \frac{v_i}{v_j}", r"\quad\text{whatever else is on the menu}",
                    font_size=34, color=MODEL),
            MathTex(r"P(i \mid \text{menu}) = \frac{v_i}{\sum_{k \in \text{menu}} v_k}, \qquad "
                    r"P(i \succ j) = \frac{v_i}{v_i + v_j}", font_size=36, color=GOOD),
        ).arrange(DOWN, buff=0.45).move_to([0, 1.4, 0])
        rows = rows_of([
            (r"Luce, \ 1959: \ the odds of choosing one option over another do not depend on what else is offered: \ "
             r"independence from irrelevant alternatives", MODEL),
            (r"then every option has a strength $v$, \ fixed up to a common factor: \ a ratio scale, \ derived from one "
             r"assumption about choice", GOOD),
            (r"for pairs it is Bradley and Terry's model of 1952, \ and Elo's chess ratings in another form", PERSON),
            (r"on logs, \ $\log v$ is a scale like Thurstone's; \ the logistic replaces his normal curve", WHITE),
        ], 12.4, 21, 0.38).move_to([0, -1.6, 0])
        with self.voiceover(
            "Luce's starting point was an axiom, not a mechanism. <bookmark mark='a'/> The odds of choosing one "
            "option over another don't depend on what else is offered. It's called independence from irrelevant "
            "alternatives. <bookmark mark='b'/> If that holds, every option has a strength, fixed up to a common "
            "factor. A ratio scale, from one assumption about choice. <bookmark mark='c'/> For pairs, it's Bradley "
            "and Terry's model of 1952, and in another form, the chess ratings of Arpad Elo. <bookmark mark='d'/> "
            "Take logs, and the strengths become a scale like Thurstone's, with the logistic curve in place of his "
            "normal one."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(eqs[1]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def mm(self):
        d = load("veg")
        head = heading(r"Fitting it: \ an algorithm that always climbs")
        eq = MathTex(r"v_i \leftarrow \frac{w_i}{\sum_{j} n_{ij} / (v_i + v_j)}", font_size=40,
                     color=MODEL).move_to([-3.4, 1.8, 0])
        A = axes([-1.1, 0.8], [-2, 1.3], x_length=4.4, y_length=3.0, xticks=[-1, 0, 0.5], yticks=[-2, -1, 0, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"Thurstone scale",
                 ylabel=r"$\log v$ (Bradley-Terry)", center=[-3.4, -1.0, 0], font_size=12)
        dots = VGroup(*[Dot(A.ax.c2p(x, y), radius=0.07, color=PERSON) for x, y in zip(d["thurstone"], d["btl"])])
        rows = rows_of([
            (r"$w_i$: \ option $i$'s wins; \ $n_{ij}$: \ comparisons of $i$ and $j$", WHITE),
            (r"each update increases the likelihood: \ a minorize-maximize (MM) algorithm (Hunter, \ 2004; \ "
             r"\emph{Statistics, Built}'s optimizer)", MODEL),
            (rf"on the vegetables, \ {d['btl_iters']} updates; \ the two scales agree almost perfectly (correlation "
             rf"{d['corr']:.4f}), \ with a slope of {d['slope']:.2f}", PERSON),
            (r"the slope is the old rule of thumb: \ a logistic curve is a normal curve stretched by about 1.7", GOOD),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.btl\_fit}; \ Guilford's vegetables")
        with self.voiceover(
            "Fitting Luce's model is easy. <bookmark mark='a'/> Count each option's wins, and the comparisons between "
            "each pair. <bookmark mark='b'/> Then update every strength by this rule, again and again. Each update "
            "increases the likelihood. It's a minorize-maximize algorithm. <bookmark mark='c'/> On the vegetables, it "
            "takes about ninety updates, and Luce's scale and Thurstone's agree almost perfectly. "
            "<bookmark mark='d'/> The slope between them is the old rule of thumb: a logistic curve is a normal curve "
            "stretched by about one point seven."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(eq), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.15), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def arena(self):
        d = load("arena")
        head = heading(r"A leaderboard from random votes")
        A = axes([0, 3400], [0, 1.05], x_length=5.6, y_length=3.0, xticks=[200, 800, 1600, 3200], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:g}", xlabel=r"votes on random pairs",
                 ylabel=r"", center=[-3.3, 0.3, 0], font_size=13)
        cr = curve(A.ax, d["m"], d["rho"], MODEL, stroke_width=4)
        ct = curve(A.ax, d["m"], d["top"], PERSON, stroke_width=4)
        key = VGroup(label(r"rank correlation with the truth", font_size=13, color=MODEL),
                     label(r"the best entrant ranked first", font_size=13, color=PERSON)).arrange(DOWN, buff=0.1,
                                                                                               aligned_edge=LEFT)
        key.next_to(A, UP, buff=0.2)
        i400 = list(d["m"]).index(400)
        rows = rows_of([
            (r"twenty entrants with Bradley-Terry strengths; \ each vote compares a random pair; \ the board is the "
             r"MM fit", WHITE),
            (rf"after 400 votes the order is nearly right: \ rank correlation {d['rho'][i400]:.2f}", MODEL),
            (rf"but the true best is on top only {100 * d['top'][i400]:.0f}\% of the time; \ after 3,200 votes, \ "
             rf"{100 * d['top'][-1]:.0f}\%", PERSON),
            (r"the whole order is learned fast, \ the top slowly: \ neighbours at the top differ little, \ and few "
             r"votes compare them; \ report intervals, \ not just ranks", YOU),
        ], 6.0, 19, 0.38).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{scaling.btl\_fit}, \ 100 simulated boards each")
        with self.voiceover(
            "Luce's model now runs leaderboards, so how many votes does one need? <bookmark mark='a'/> Twenty "
            "entrants with Bradley-Terry strengths. Each vote compares a random pair, and the board is the fit. "
            "<bookmark mark='b'/> After four hundred votes the order is nearly right. <bookmark mark='c'/> But the "
            "true best is on top less than half the time. After three thousand two hundred votes, about four times "
            "in five. <bookmark mark='d'/> The whole order is learned fast and the top slowly, because neighbours at "
            "the top differ little and few votes compare them. Report intervals, not just ranks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cr))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(ct))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
