from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Blindness(VoiceoverScene):
    def construct(self):
        self.card()
        self.flicker_model()
        self.attentional_set()
        self.experts()

    def card(self):
        card = chapter_card(6, r"Seeing without attention", r"How much of a scene do we actually see?",
                            lit={1997: r"Rensink et al.", 1999: r"Simons \& Chabris", 2013: r"Drew et al."},
                            part=PART, scale=("mind", "person"), marr=("what",))
        with self.voiceover("Chapter six. Seeing without attention."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def flicker_model(self):
        d = load("flicker")
        p = archive.RENSINK_1997.data
        head = heading(r"Change blindness, \ as a model")
        rows = rows_of([
            (r"a scene of 40 things; \ attention samples about one a cycle, \ never the same twice", WHITE),
            (r"an interesting thing is weighted more: \ it tends to be sampled early", CUE),
            (r"the change is seen only when its item is sampled", ATT),
            (rf"two numbers fitted to Rensink's two means: \ {d['per']:.1f} items a cycle, \ interesting items "
             rf"{d['w_ci']:.0f} times as likely", MODEL),
            (r"the long tail is the point: \ a few observers need forty cycles or more", GREY_A),
        ], 6.2, 25, 0.42).to_edge(LEFT, buff=0.6).shift(DOWN * 0.05)
        A = axes([0, 60], [0, 0.16], x_length=5.0, y_length=3.0, xticks=[0, 20, 40, 60], yticks=[0, 0.08, 0.16],
                 xlabel=r"cycles before the change is seen", ylabel=r"share of observers", center=[3.7, 0.5, 0],
                 font_size=17)
        ax = A.ax
        bins = np.arange(0.5, 61.5, 2)

        def hist(x, col):
            h, e = np.histogram(x, bins=bins)
            h = h / x.size
            g = VGroup()
            for k, v in enumerate(h):
                if v <= 0:
                    continue
                lo, hi = ax.c2p(e[k], 0), ax.c2p(e[k + 1], min(v, 0.16))
                g.add(Rectangle(width=hi[0] - lo[0], height=hi[1] - lo[1], stroke_width=0, fill_color=col,
                                fill_opacity=0.55).move_to([(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, 0]))
            return g

        hc, hm = hist(d["dist_ci"], CUE), hist(d["dist_mi"], ATT)
        res = VGroup(label(rf"centre of interest: \ Psyche {d['ci']:.1f}, \ people {p['ci_alternations']}", font_size=18,
                           color=CUE),
                     label(rf"margin: \ Psyche {d['mi']:.1f}, \ people {p['mi_alternations']}", font_size=18, color=ATT))
        res.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(A, DOWN, buff=0.15)
        ptag = psyche_tag(r"\texttt{attention.flicker}: \ fitted on a grid, \ 2,000 simulated observers per change")
        tag = published_tag(archive.RENSINK_1997.cite)
        with self.voiceover(
            "What would explain Rensink's numbers? Psyche tries the simplest account. <bookmark mark='a'/> A scene "
            "holds about forty things. On each cycle of the flicker, attention samples about one of them, and "
            "doesn't go back to one it has already checked. <bookmark mark='b'/> Interesting things are more likely "
            "to be sampled early. <bookmark mark='c'/> The change is seen only when attention lands on the thing "
            "that changes; without attention, the change isn't registered at all. <bookmark mark='d'/> That model has "
            "two numbers, the sampling rate and the weight of interest, and fitting them to Rensink's two means "
            "gives a little more than one item a cycle, with interesting things four times as likely to be picked. "
            "The fit is close, not exact: Psyche needs about eight cycles for central changes, where people needed "
            "seven, and eighteen for marginal ones, where people needed seventeen. <bookmark mark='e'/> The shape is "
            "the lesson. About half of Psyche's observers find a marginal change within twenty cycles, and a few need "
            "forty or more, the long tail Rensink saw."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "d":
                    self.play(FadeIn(hc), FadeIn(hm), FadeIn(res), FadeIn(ptag))
        self.clear_scene()

    def attentional_set(self):
        d = load("notice")
        head = heading(r"What you are looking for decides what else you see")
        rows = rows_of([
            (r"in the gorilla video, \ counting the black team's passes made noticing the black gorilla about twice "
             r"as likely", WHITE),
            (r"2001: \ Most and colleagues vary the unexpected object's colour against the attended set", CUE),
            (r"the more it resembles what you attend, \ the likelier you are to see it", ATT),
            (r"and the harder the task, \ the fewer see it at all", CONTROL),
        ], 6.2, 25, 0.42).to_edge(LEFT, buff=0.6).shift(DOWN * 0.05)
        A = axes([0, 1], [0, 1], x_length=4.8, y_length=3.0, xticks=[0, 0.5, 1], yticks=[0, 0.5, 1],
                 xlabel=r"similarity to the attended items", ylabel=r"P(notice)", center=[3.7, 0.4, 0], font_size=17)
        ax = A.ax
        lo = curve(ax, d["s"], d["low"], ATT, 4)
        hi = curve(ax, d["s"], d["high"], CONTROL, 4)
        lg = legend([(ATT, r"an easy task"), (CONTROL, r"a hard task")], font_size=18)
        lg.next_to(ax.c2p(0, 1), RIGHT, buff=0.2).shift(DOWN * 0.3)
        ptag = psyche_tag(r"\texttt{attention.notice\_probability}: \ a logistic in similarity, \ shifted by load")
        tag = historical_tag(archive.SIMONS_CHABRIS_1999.cite)
        with self.voiceover(
            "Who sees the gorilla is not random. <bookmark mark='a'/> In the original study, observers counting the "
            "black team's passes noticed the black gorilla about twice as often as those counting the white team's. "
            "Attending to black things kept black things in view. <bookmark mark='b'/> In 2001 Steven Most, with "
            "Simons, Chabris and colleagues, varied this systematically, with shapes crossing a screen. "
            "<bookmark mark='c'/> The more the unexpected object resembled what people were attending to, the more "
            "of them saw it; the more it resembled what they were ignoring, the fewer. <bookmark mark='d'/> And "
            "harder tasks, like counting bounce passes and aerial passes separately, left fewer people noticing "
            "anything. Psyche's curve is only a summary of those two facts: a logistic in similarity, shifted by load."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
                if m == "c":
                    self.play(Create(lo), FadeIn(lg[0]), FadeIn(ptag))
                if m == "d":
                    self.play(Create(hi), FadeIn(lg[1]))
        self.clear_scene()

    def experts(self):
        p = archive.DREW_2013.data
        head = heading(r"Experts are not immune")
        lung = VGroup(Ellipse(width=1.6, height=2.6, color=GREY_B, stroke_width=3).move_to([-4.4, 0.9, 0]),
                      Ellipse(width=1.6, height=2.6, color=GREY_B, stroke_width=3).move_to([-2.4, 0.9, 0]))
        nod = VGroup(*[Dot(p_, radius=0.05, color=WHITE) for p_ in ([-4.6, 1.5, 0], [-4.1, 0.4, 0], [-2.2, 1.2, 0],
                                                                      [-2.6, 0.2, 0], [-4.4, 1.0, 0])])
        gor = VGroup(RoundedRectangle(width=0.32, height=0.55, corner_radius=0.12, stroke_color=GREY_C,
                                      stroke_width=2, fill_color="#3a3f47", fill_opacity=0.7),
                     Circle(0.11, stroke_color=GREY_C, stroke_width=2, fill_color="#3a3f47", fill_opacity=0.7)
                     .shift(UP * 0.36)).move_to([-2.35, 1.55, 0])
        gl = label(rf"a gorilla, \ {p['size_vs_nodule']} times a nodule's size", font_size=19, color=GREY_B)
        gl.next_to(lung, DOWN, buff=0.2)
        dots = VGroup(*[Dot(radius=0.13, color=BAD if k < p["missed"] else GOOD) for k in range(p["radiologists"])])
        dots.arrange_in_grid(rows=3, buff=0.18).move_to([2.8, 1.1, 0])
        dl = label(rf"{p['missed']} of {p['radiologists']} radiologists did not report it", font_size=22,
                   color=BAD).next_to(dots, DOWN, buff=0.25)
        rows = rows_of([
            (r"2013: \ Drew, \ V\~o and Wolfe ask radiologists to search lung scans for nodules", WHITE),
            (r"in the last case, \ a small gorilla is pasted into the scan", GREY_A),
            (r"eye tracking: \ most of those who missed it looked right at it", ATT),
            (r"not carelessness: \ expertise tunes attention to what the task says to look for", CUE),
        ], 12.4, 26, 0.3).to_edge(DOWN, buff=0.75)
        tag = published_tag(archive.DREW_2013.cite)
        with self.voiceover(
            "It would be comforting if this were a problem for students watching basketball. "
            "<bookmark mark='a'/> In 2013 Trafton Drew, Melissa Võ and Jeremy Wolfe asked radiologists to do what "
            "they do every day: search a stack of lung scan slices for nodules, the small bright spots that can be "
            "early cancers. <bookmark mark='b'/> In the last case, they had pasted in a gorilla, forty-eight times "
            "the size of a typical nodule, faint, but plain once you see it. <bookmark mark='c'/> Twenty of the "
            "twenty-four radiologists did not report it, and the eye tracker showed that most of those who missed it "
            "had looked directly at it. <bookmark mark='d'/> That isn't carelessness. Expertise tunes attention "
            "precisely to what the task says to look for, which is why experts are good, and why they can miss "
            "what they weren't asked about. Later work found that when radiologists are told to report anything "
            "abnormal, such misses become much rarer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(lung), FadeIn(nod))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(gor), FadeIn(gl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.05), FadeIn(dl), FadeIn(rows[2]),
                      run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
