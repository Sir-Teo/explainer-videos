from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.values()
        self.traits()

    def card(self):
        card = chapter_card(14, r"Frontier: \ values, \ attention and traits", r"Does the model reach beyond the "
                                                                                 r"laboratory's dots?",
                            lit={2010: r"Krajbich et al.", 2017: r"Lerche \& Voss", 2018: r"Hedge et al."},
                            part=PART, scale=("mind", "person"), marr=("how",))
        with self.voiceover("Chapter fourteen. Frontier: values, attention and traits."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def values(self):
        d = load("addm")
        head = heading(r"Choosing a snack, \ with your eyes")
        A = axes([0, 2.4], [-1.1, 1.1], x_length=5.6, y_length=2.4, xticks=[0, 1, 2], yticks=[-1, 0, 1],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:+.0f}" if v else "0", xlabel=r"time, \ s",
                 ylabel=r"relative value", center=[-3.3, 1.2, 0], font_size=15)
        shades = VGroup()
        for t0, t1, left in d["looks"]:
            t1 = min(t1, 2.4)
            r = Rectangle(width=abs(A.ax.c2p(t1, 0)[0] - A.ax.c2p(t0, 0)[0]),
                          height=abs(A.ax.c2p(0, 1.1)[1] - A.ax.c2p(0, -1.1)[1]), stroke_width=0,
                          fill_color=MODEL if left else LOST, fill_opacity=0.12)
            r.move_to(A.ax.c2p(t0, 0), aligned_edge=LEFT)
            shades.add(r)
        p = d["path"]
        keep = p[:, 0] <= 2.4
        path = VMobject(color=EVIDENCE, stroke_width=2.5).set_points_as_corners(
            [A.ax.c2p(float(t), float(min(max(x, -1.1), 1.1))) for t, x in p[keep]])
        bounds_ = VGroup(DashedLine(A.ax.c2p(0, 1), A.ax.c2p(2.4, 1), color=BOUND, stroke_width=2),
                         DashedLine(A.ax.c2p(0, -1), A.ax.c2p(2.4, -1), color=BOUND, stroke_width=2))
        lk = legend([(MODEL, r"looking left \ (worth 4)"), (LOST, r"looking right \ (worth 2)")], font_size=15
                    ).next_to(A, DOWN, buff=0.3).align_to(A, RIGHT)
        B = axes([-1.0, 1.0], [0, 1], x_length=5.0, y_length=2.0, xticks=[-1, 0, 1], yticks=[0, 0.5, 1],
                 xfmt=lambda v: f"{v:+.0f}" if v else "0", yfmt=lambda v: f"{v:.1f}",
                 xlabel=r"left looked at longer by, \ s", ylabel=r"P(choose left)", center=[-3.3, -2.25, 0],
                 font_size=14)
        gb = VGroup(curve(B.ax, d["adv_mid"], d["p_left"], MODEL, 3), scatter(B.ax, d["adv_mid"], d["p_left"], MODEL,
                                                                              0.06, 1))
        half = DashedLine(B.ax.c2p(-1, 0.5), B.ax.c2p(1, 0.5), color=GREY_D)
        assert d["p_left"][0] < 0.35 and d["p_left"][-1] > 0.65
        rows = rows_of([
            (r"Krajbich, \ Armel \& Rangel, \ 2010: \ hungry people chose between snacks while a camera tracked "
             r"their eyes", WHITE),
            (r"their model: \ the evidence drifts toward whichever item is being looked at; \ the other counts "
             r"only partly", EVIDENCE),
            (rf"Psyche, \ with two equally good snacks: \ look longer at one and you choose it far more often; \ "
             rf"the last item looked at wins {pct(d['p_last'])} of the time", MODEL),
            (r"attention shapes preference, \ not only the reverse: \ judgement and choice are Part 26", BOUND),
        ], 5.4, 21, 0.34).move_to([3.7, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.addm}; \ Krajbich, \ Armel \& Rangel (2010)")
        with self.voiceover(
            "The model was built for dots and letters. Does it reach any further? <bookmark mark='a'/> In 2010 Ian "
            "Krajbich, Carrie Armel and Antonio Rangel asked hungry people to choose between pairs of snacks while a "
            "camera tracked their eyes. <bookmark mark='b'/> Their model is a diffusion whose drift depends on where "
            "you're looking: evidence builds for the item you're looking at, and the other one counts only partly. "
            "Here's one trial: green while looking left, red while looking right. <bookmark mark='c'/> Psyche runs "
            "the model with two snacks of equal value. Look longer at one, and you're far more likely to choose it, "
            f"and the last item looked at wins {spct(d['p_last'])} of the time, just as the people's choices did. "
            "<bookmark mark='d'/> Attention doesn't just follow preference; it shapes it. Judgement and choice are "
            "the subject of the next part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(bounds_))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(shades), FadeIn(lk), FadeIn(rows[1]))
            self.play(Create(path), run_time=3, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(B), Create(half), FadeIn(gb), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def traits(self):
        d = load("traits")
        head = heading(r"Is your drift a trait?")
        A = axes([0, 3], [0, 1], x_length=5.6, y_length=3.4, xticks=[np.log10(x) for x in (10, 100, 1000)],
                 yticks=[0, 0.5, 1], xfmt=lambda v: f"{10 ** v:.0f}", yfmt=lambda v: f"{v:.1f}",
                 xlabel=r"trials per session \ (log scale)", ylabel=r"test--retest correlation of drift",
                 center=[-3.3, -0.2, 0], font_size=16)
        lx = np.log10(d["trials"])
        line = curve(A.ax, lx, d["r"], MODEL, 3)
        pts = scatter(A.ax, lx, d["r"], MODEL, 0.08, 1)
        assert d["r"][-1] > 0.8 and d["r"][0] < 0.5
        rows = rows_of([
            (r"to study people, \ not conditions, \ a parameter must be stable within a person", WHITE),
            (rf"Psyche: \ 100 simulated people tested twice; \ with {d['trials'][0]} trials a session the fitted "
             rf"drifts correlate {d['r'][0]:.2f}, \ with {d['trials'][-1]}, \ {d['r'][-1]:.2f}", MODEL),
            (r"Hedge, \ Powell \& Sumner, \ 2018: \ the tasks with the most reliable effects across people are often "
             r"the least reliable for telling people apart", LOST),
            (r"Lerche \& Voss, \ 2017: \ diffusion parameters are moderately stable over a week, \ given enough trials; \ "
             r"individual differences and their measurement are Part 59", BOUND),
        ], 5.4, 21, 0.34).move_to([3.7, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.retest}; \ Hedge, \ Powell \& Sumner (2018); \ Lerche \& Voss (2017)")
        with self.voiceover(
            "The last frontier is you. Is your drift, or your caution, a trait, like your height? "
            "<bookmark mark='a'/> To use these numbers to compare people rather than conditions, they have to be "
            "stable within a person. <bookmark mark='b'/> Psyche tests a hundred simulated people twice. With "
            f"twenty trials a session, their fitted drifts correlate only {d['r'][0]:.2f} from one session to the "
            f"next. With five hundred, {d['r'][-1]:.2f}. Precision costs trials. <bookmark mark='c'/> And Craig "
            "Hedge, Gareth Powell and Petroc Sumner showed in 2018 a paradox: the tasks whose effects replicate best "
            "across people are often the worst at telling people apart, because everyone shows the effect to a "
            "similar degree. <bookmark mark='d'/> Veronika Lerche and Andreas Voss found diffusion parameters "
            "moderately stable over a week, given enough trials. Measuring individual differences is Part 59."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(line), FadeIn(pts), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
