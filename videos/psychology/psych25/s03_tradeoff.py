from __future__ import annotations

from videos.psychology.psych25.common import *  # noqa: F403


class Tradeoff(VoiceoverScene):
    def construct(self):
        self.card()
        self.people()
        self.curve()

    def card(self):
        card = chapter_card(2, r"The speed--accuracy trade-off", r"What does a second buy?",
                            lit={1974: r"Pachella", 1977: r"Wickelgren", 2008: r"Wagenmakers et al."},
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter two. The speed-accuracy trade-off."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def people(self):
        d = load("selective")
        head = heading(r"17 people, \ two instructions")
        A = axes([0.4, 1.1], [0.65, 1.0], x_length=6.0, y_length=4.0, xticks=[0.4, 0.6, 0.8, 1.0],
                 yticks=[0.7, 0.8, 0.9, 1.0], xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{100 * v:.0f}\\%",
                 xlabel=r"mean response time, \ s", ylabel=r"proportion correct", center=[-3.2, -0.1, 0],
                 font_size=16)
        pc, mrt = d["pc"], d["mrt"]
        links = VGroup(*[Line(A.ax.c2p(mrt[k, 0], pc[k, 0]), A.ax.c2p(mrt[k, 1], pc[k, 1]), color=GREY_D,
                              stroke_width=1.5) for k in range(len(pc))])
        sp = scatter(A.ax, mrt[:, 0], pc[:, 0], SPEED, 0.07, 1)
        ac = scatter(A.ax, mrt[:, 1], pc[:, 1], CAREFUL, 0.07, 1)
        key = legend([(SPEED, r"``be fast''"), (CAREFUL, r"``be accurate''")], font_size=17).move_to(
            A.ax.c2p(0.95, 0.75))
        slower = int((mrt[:, 1] > mrt[:, 0]).sum())
        better = int((pc[:, 1] > pc[:, 0]).sum())
        gain = float(np.median(pc[:, 1] - pc[:, 0]))
        cost = float(np.median(mrt[:, 1] - mrt[:, 0]))
        assert slower == len(pc) and better >= len(pc) - 1
        rows = rows_of([
            (r"Wagenmakers et al., \ 2008: \ is this string a word? \ blocks that said \emph{be fast} or "
             r"\emph{be accurate}", WHITE),
            (rf"all {len(pc)} were slower when asked to be accurate, \ and {better} were more often right", CAREFUL),
            (rf"the median person paid {1000 * cost:.0f} ms for {100 * gain:.0f} points of accuracy", BOUND),
            (r"the same people, \ the same words: \ the trade is chosen, \ not imposed", MODEL),
        ], 5.6, 23, 0.36).move_to([3.6, 0.0, 0])
        tag = psyche_tag(r"open data: \ Wagenmakers, \ Ratcliff, \ Gomez \& McKoon (2008), \ via rtdists")
        with self.voiceover(
            "In the moving dots you traded accuracy for time. Here is the same trade in open data. "
            "<bookmark mark='a'/> In 2008 Eric-Jan Wagenmakers, Roger Ratcliff, Pablo Gomez and Gail McKoon asked "
            "people whether strings of letters were words, in blocks that told them either to be fast or to be "
            "accurate. Here are seventeen of them, each a pair of dots joined by a line. <bookmark mark='b'/> "
            f"Every one was slower when asked to be accurate, and {better} of the {len(pc)} were right more often. "
            f"<bookmark mark='c'/> The median person paid about {1000 * cost:.0f} milliseconds for "
            f"{100 * gain:.0f} points of accuracy. <bookmark mark='d'/> Same people, same words. Nothing about "
            "the task changed except what they were asked to care about, so the trade is something a person "
            "chooses."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(sp), FadeIn(ac), FadeIn(key))
            vo.wait_until("b")
            self.play(Create(links), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def curve(self):
        d = load("ddm")
        head = heading(r"One person, \ a whole curve")
        A = axes([0.3, 1.5], [0.5, 1.0], x_length=6.0, y_length=3.8, xticks=[0.4, 0.8, 1.2], yticks=[0.5, 0.75, 1.0],
                 xfmt=lambda v: f"{v:.1f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"mean response time, \ s",
                 ylabel=r"proportion correct", center=[-3.2, -0.1, 0], font_size=16)
        cv = curve_in(A.ax, d["sat_rt"], d["sat_acc"], MODEL, 4)
        ks = [int(np.argmin(np.abs(d["a_grid"] - a))) for a in (0.6, 1.8)]
        marks = VGroup(*[Dot(A.ax.c2p(d["sat_rt"][k], d["sat_acc"][k]), radius=0.1, color=c)
                         for k, c in zip(ks, (SPEED, CAREFUL))])
        mlab = VGroup(label(r"Ann: \ fast", font_size=19, color=SPEED).next_to(marks[0], RIGHT, buff=0.15),
                      label(r"Bob: \ careful", font_size=19, color=CAREFUL).next_to(marks[1], DOWN, buff=0.15))
        rows = rows_of([
            (r"Psyche's diffusion model \ (chapter five): \ the same evidence, \ the bound moved from low to high",
             MODEL),
            (r"every point is the same mind; \ only its caution differs", BOUND),
            (r"Pachella, \ 1974; \ Wickelgren, \ 1977: \ compare people by mean time alone, \ and a careful "
             r"person looks slow", LOST),
            (r"so a model of choice must give accuracy and time together, \ from one set of parameters", WHITE),
        ], 5.6, 23, 0.36).move_to([3.6, 0.0, 0])
        tag = psyche_tag(r"\texttt{decide.p\_upper}, \ \texttt{mean\_dt}: \ drift 1.5, \ bound 0.3 to 2.6")
        assert d["sat_acc"][ks[1]] > d["sat_acc"][ks[0]] and d["sat_rt"][ks[1]] > d["sat_rt"][ks[0]]
        with self.voiceover(
            "Now one mind, many settings. <bookmark mark='a'/> This is the curve Psyche's decision maker traces, "
            "from the model of chapter five, as it moves a single dial, how much evidence it asks for, from low to "
            "high. The evidence itself doesn't change. <bookmark mark='b'/> Every point on the curve is the same "
            "mind, differing only in caution. <bookmark mark='c'/> Which is why Robert Pachella and Wayne Wickelgren "
            "warned in the 1970s against comparing people, or groups, or drugs, by mean response time alone. Put Ann "
            "here and Bob here, and Bob looks slow, though he's no worse at the task; he's simply more careful. "
            "<bookmark mark='d'/> Any model of choice has to produce accuracy and time together, from one set of "
            "parameters, or it isn't a model of choice."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(rows[0]), run_time=2)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(marks), FadeIn(mlab), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
