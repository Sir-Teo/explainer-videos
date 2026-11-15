from __future__ import annotations

from videos.psychology.psych18.common import *  # noqa: F403


class Vigilance(VoiceoverScene):
    def construct(self):
        self.card()
        self.clock()
        self.prevalence()

    def card(self):
        card = chapter_card(11, r"Vigilance, \ and rare targets", r"Why does watching for something get harder?",
                            lit={1948: r"Mackworth", 2005: r"Wolfe et al.", 2007: r"Fleck \& Mitroff"}, part=PART, scale=("mind", "person"),
                            marr=("what",))
        with self.voiceover("Chapter eleven. Vigilance, and rare targets."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def clock(self):
        d = load("vigilance")
        head = heading(r"Mackworth's clock")
        face = Circle(1.4, color=GREY_B, stroke_width=3).move_to([-4.3, 0.9, 0])
        ticks = VGroup(*[Dot(face.get_center() + 1.25 * np.array([np.cos(a), np.sin(a), 0]), radius=0.03,
                             color=GREY_B) for a in np.linspace(0, 2 * PI, 60, endpoint=False)])
        hand = Line(face.get_center(), face.get_center() + UP * 1.15, color=ATT, stroke_width=5)
        fl = wrapped_label(r"a hand that jumps once a second; \ now and then, \ a double jump", 3.6, 19,
                           GREY_A).next_to(face, DOWN, buff=0.2)
        A = axes([0, 120], [0, 1], x_length=5.6, y_length=3.0, xticks=[0, 30, 60, 90, 120], yticks=[0, 0.5, 1],
                 xlabel=r"minutes on watch", ylabel=r"rate", center=[2.6, 0.9, 0], font_size=17)
        ax = A.ax
        ch = curve(ax, d["t"], d["hits"], GOOD, 4)
        cf = curve(ax, d["t"], d["fas"], BAD, 3)
        lg = legend([(GOOD, r"double jumps reported"), (BAD, r"false alarms")], font_size=18)
        lg.next_to(ax.c2p(60, 1), DOWN, buff=0.1)
        rows = rows_of([
            (r"1948: \ Norman Mackworth tests why radar operators missed submarine echoes late in a watch", WHITE),
            (r"detections fall within the first half hour, \ and stay low", GOOD),
            (r"both sensitivity and caution change: \ fewer hits, \ and fewer false alarms too", CONTROL),
            (r"a watch is demanding work, \ not idle waiting: \ breaks and rotation restore it", ATT),
        ], 12.4, 25, 0.28).to_edge(DOWN, buff=0.75)
        ptag = psyche_tag(r"\texttt{attention.vigilance}: \ $d'$ falls 2.6 $\to$ 1.7, \ the criterion rises")
        tag = historical_tag(archive.MACKWORTH_1948.cite)
        with self.voiceover(
            "Some attention is not search but waiting. <bookmark mark='a'/> Part 12 opened with Norman Mackworth's "
            "clock, built during the Second World War to find out why radar operators hunting submarines missed "
            "more echoes late in their watches. The hand jumps once a second, and now and then twice as far; the job "
            "is to report the double jumps, for two hours. <bookmark mark='b'/> Detection fell within the first "
            "half hour, and stayed low: the vigilance decrement, which Part 12 met as a story about criteria. "
            "<bookmark mark='c'/> Here it is as attention. Signal detection separates two changes. Observers become less sensitive, and also more cautious, so false "
            "alarms fall along with hits. Psyche's watch has both. <bookmark mark='d'/> Watching turns out to be hard "
            "work, not idleness: it is tiring and stressful, and short breaks or rotating people restore it, which is "
            "why air-traffic controllers and baggage screeners work in shifts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(face), FadeIn(ticks), FadeIn(hand), FadeIn(fl))
            for _ in range(3):
                self.play(Rotate(hand, -PI / 30, about_point=face.get_center()), run_time=0.4)
            self.play(Rotate(hand, -PI / 15, about_point=face.get_center()), run_time=0.4)
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(A))
            vo.wait_until("b")
            self.play(Create(ch), FadeIn(lg[0]), FadeIn(rows[1]), FadeIn(ptag), run_time=1.5)
            vo.wait_until("c")
            self.play(Create(cf), FadeIn(lg[1]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def prevalence(self):
        d = load("prevalence")
        head = heading(r"Rare targets, \ seen from search")
        A = axes([-2, np.log10(0.5)], [0, 0.6], x_length=6.0, y_length=3.2, xticks=[-2, -1, np.log10(0.5)],
                 yticks=[0, 0.3, 0.6], xfmt=lambda v: {-2: "1\\%", -1: "10\\%"}.get(int(round(v)), "50\\%"),
                 xlabel=r"how often the target is present", ylabel=r"targets missed", center=[-2.6, 0.6, 0],
                 font_size=17)
        ax = A.ax
        c = curve(ax, np.log10(d["p"]), d["miss"], MODEL, 4)
        dots = VGroup(*[Dot(ax.c2p(np.log10(x), y), radius=0.09, color=DATA) for x, y in zip(d["data_p"],
                                                                                           d["data_miss"])])
        dl = VGroup(*[label(rf"{pct(y)}", font_size=18, color=DATA).next_to(dt, UR, buff=0.06)
                      for dt, y in zip(dots, d["data_miss"])])
        lg = legend([(DATA, r"Wolfe, \ Horowitz and Kenner, \ 2005"),
                     (MODEL, rf"a criterion that moves {pct(d['shift'])} of the ideal way")], font_size=17)
        lg.next_to(A, DOWN, buff=0.15)
        rows = rows_of([
            (r"Part 12: \ misses of 11, \ 25 and 52\% as targets go from half the bags to one in a hundred", DATA),
            (rf"fitted here: \ $d'$ = {d['d_prime']:.2f}, \ and a criterion that moves {pct(d['shift'])} of the way "
             r"the base rate justifies", MODEL),
            (r"in search the criterion is also a quitting threshold: \ when no is usually right, \ search stops sooner",
             ATT),
            (r"and some misses are hasty keypresses: \ Fleck and Mitroff let people correct them, \ and many "
             r"vanished", GREY_A),
        ], 5.8, 23, 0.38).move_to([3.9, 0.1, 0])
        ptag = psyche_tag(r"\texttt{attention.prevalence\_misses}, \ fitted to the three points")
        tag = published_tag(archive.WOLFE_2005.cite)
        with self.voiceover(
            "Part 12 met a related problem: the things worth finding are usually rare. <bookmark mark='a'/> In "
            "Wolfe, Horowitz and Kenner's search through simulated bags, people missed eleven percent of targets "
            "when a target was in half the bags, a quarter when it was in one bag in ten, and half when it was in "
            "one in a hundred. <bookmark mark='b'/> Psyche fits those three points with two numbers: a sensitivity, "
            "and a criterion that moves about two thirds of the way that the base rate would justify for an ideal "
            "observer. <bookmark mark='c'/> In search, the criterion is also a quitting threshold. When no is "
            "almost always the right answer, people stop searching sooner, and say no more readily. "
            "<bookmark mark='d'/> Part of the effect is even faster than that: Mathias Fleck and Stephen Mitroff let "
            "people take back a response they had just made, and many of the extra misses disappeared. They were "
            "hasty keypresses, not targets unseen. Airport security and cancer screening are both searches for "
            "targets that almost never appear, which is why Chapter fourteen returns to them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), LaggedStart(*[FadeIn(x) for x in dots], lag_ratio=0.3), FadeIn(dl),
                      FadeIn(lg[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(c), FadeIn(lg[1]), FadeIn(ptag), run_time=1.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
