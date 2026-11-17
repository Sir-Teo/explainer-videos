from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403


class Forgetting(VoiceoverScene):
    def construct(self):
        self.card()
        self.task()
        self.trials()
        self.simple()

    def card(self):
        card = chapter_card(3, r"Forgetting in eighteen seconds", r"Does a memory fade with time, \ or get crowded out?",
                            lit={1958: r"Brown", 1959: r"Peterson \& Peterson", 1962: r"Keppel \& Underwood"},
                            part=PART, scale=("mind",), marr=("what", "how"))
        with self.voiceover("Chapter three. Forgetting in eighteen seconds."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def task(self):
        d = load("forgetting")
        p = archive.PETERSON_1959.data
        head = heading(r"The Brown-Peterson task")
        strip = trial_strip([
            (r"three consonants", label(r"K \ B \ F", font_size=40, color=MEM), r"0.5 s"),
            (r"a number", label(r"309", font_size=40), r"0.5 s"),
            (r"count back by threes, \ aloud", label(r"306, \ 303, \ 300 \ ...", font_size=30, color=GREY_B),
             r"3 to 18 s"),
            (r"recall the consonants", label(r"?", font_size=44, color=YOU), ""),
        ], frame_w=2.6, frame_h=1.2, font_size=19).move_to([0, 1.95, 0])
        A = axes([0, 18], [0, 1], x_length=6.2, y_length=2.8, xticks=[0, 3, 6, 9, 12, 15, 18], yticks=[0, 0.5, 1],
                 xlabel=r"seconds of counting", ylabel=r"recalled correctly", center=[-2.7, -1.15, 0], font_size=18,
                 yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        c = curve_in(ax, d["delay"], d["late"], MODEL, 4)
        pts = VGroup(Dot(ax.c2p(3, p["recall_3s"]), radius=0.08, color=DATA),
                     Dot(ax.c2p(18, p["recall_18s"]), radius=0.08, color=DATA))
        pl = VGroup(label(rf"about {pct(p['recall_3s'])}", font_size=19, color=DATA).next_to(pts[0], UR, buff=0.08),
                    label(rf"about {pct(p['recall_18s'])}", font_size=19, color=DATA).next_to(pts[1], UP, buff=0.12))
        rows = rows_of([
            (r"1958 and 1959: \ John Brown in Britain, \ Lloyd and Margaret Peterson in Indiana", WHITE),
            (r"counting backwards stops rehearsal; \ after 18 seconds almost nothing is left", LOST),
            (r"their reading: \ a trace decays with time unless it is rehearsed", GREY_A),
        ], 5.0, 23, 0.32).move_to([4.2, -1.1, 0])
        tag = historical_tag(archive.PETERSON_1959.cite)
        with self.voiceover(
            "Short-term memory is short. But how short, and why? <bookmark mark='a'/> In 1958 John Brown in Britain, "
            "and a year later Lloyd and Margaret Peterson in Indiana, found a way to stop people rehearsing. "
            "Hear three consonants, then a number, and immediately start counting backwards by threes from it, aloud, "
            "until a light tells you to recall the consonants. <bookmark mark='b'/> Three consonants is far below "
            f"span, and yet after three seconds of counting about {pct(p['recall_3s'])} were recalled, and after "
            f"eighteen seconds about {pct(p['recall_18s'])}. <bookmark mark='c'/> The obvious reading, and the "
            "Petersons', was decay: a trace fades with time unless rehearsal refreshes it, and counting prevents "
            "rehearsal. The curve here is a model that says something quite different, and we'll build it in a "
            "minute."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(strip))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(A))
            vo.wait_until("b")
            self.play(FadeIn(pts), FadeIn(pl), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(c), FadeIn(rows[2]), run_time=1.5)
        self.clear_scene()

    def trials(self):
        d = load("forgetting")
        head = heading(r"The first trial shows no forgetting")
        A = axes([0, 18], [0, 1.05], x_length=6.6, y_length=3.6, xticks=[0, 3, 6, 9, 12, 15, 18], yticks=[0, 0.5, 1],
                 xlabel=r"seconds of counting", ylabel=r"recalled correctly", center=[-2.6, 0.45, 0], font_size=18,
                 yfmt=lambda v: f"{100 * v:.0f}\\%")
        ax = A.ax
        cols = (GOOD, MEM, SLOT, LOST)
        cs = VGroup(*[curve_in(ax, d["delay"], d[k], col, 4) for k, col in
                      zip(("trial1", "trial2", "trial3", "late"), cols)])
        key = legend([(GOOD, r"trial 1"), (MEM, r"trial 2"), (SLOT, r"trial 3"), (LOST, r"later trials")],
                     font_size=19).next_to(A, DOWN, buff=0.35)
        rows = rows_of([
            (r"1962: \ Keppel and Underwood look at each trial separately", WHITE),
            (r"on the first trial, \ 18 seconds of counting cost almost nothing", GOOD),
            (r"forgetting appears on trial 2, \ and grows as earlier trials pile up", MEM),
            (r"if time alone destroyed the trace, \ the first trial would show it too", LOST),
            (r"the culprit is proactive interference: \ old items crowd the new one", EXEC),
            (r"change the kind of item, \ letters to digits, \ and recall jumps back up: \ release from it", GREY_A),
        ], 5.4, 22, 0.28).move_to([3.85, 0.15, 0])
        ptag = psyche_tag(r"\texttt{wm.brown\_peterson}: \ SIMPLE, \ fitted to about 80 and 10\%")
        tag = historical_tag(archive.KEPPEL_UNDERWOOD_1962.cite)
        with self.voiceover(
            "The Petersons had averaged over a whole session. <bookmark mark='a'/> In 1962 Geoffrey Keppel and "
            "Benton Underwood looked at the trials one at a time. <bookmark mark='b'/> On the very first trial of a "
            "session there was almost no forgetting, even after eighteen seconds of counting. "
            "<bookmark mark='c'/> Forgetting appeared on the second trial and grew over the next few. "
            "<bookmark mark='d'/> That is fatal for pure decay. Time passes just as surely on the first trial as on "
            "the tenth. <bookmark mark='e'/> What differs is how many similar items came before: proactive "
            "interference, the old crowding the new. <bookmark mark='f'/> And Delos Wickens found that if you switch "
            "the kind of item, from letters to digits say, recall on the next trial jumps back up. The crowding is "
            "between similar things."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(key), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(cs[0]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(cs[1]), Create(cs[2]), Create(cs[3]), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def simple(self):
        head = heading(r"Derived: \ forgetting as crowding in time")
        line = NumberLine(x_range=[0, 4.2, 1], length=11.0, include_numbers=False, color=GREY_C).move_to([0, 1.7, 0])
        ticks = VGroup()
        for s, txt in ((1, "1 s"), (3, "3 s"), (10, "10 s"), (30, "30 s"), (100, "100 s")):
            x = np.log10(s) + 0.6
            ticks.add(label(txt, font_size=18, color=GREY_B).next_to(line.n2p(x), DOWN, buff=0.15))
        lname = label(r"time since each item was studied, \ on a log scale", font_size=20, color=GREY_A)
        lname.next_to(line, UP, buff=0.95)

        def pos(age):
            return line.n2p(np.log10(age) + 0.6)

        old = [21 + 3 + 21 * k + 9 * k for k in range(4)]  # earlier trials: 20 s gaps plus their own 9 s delays
        early = VGroup(*[Dot(pos(a), radius=0.11, color=GREY_B) for a in old])
        short = Dot(pos(3), radius=0.13, color=MEM)
        long_ = Dot(pos(18), radius=0.13, color=LOST)
        sl = label(r"after 3 s: \ far from the others", font_size=19, color=MEM).next_to(short, UP, buff=0.2)
        sl.shift(LEFT * 0.6)
        ll = label(r"after 18 s: \ close to them", font_size=19, color=LOST).next_to(long_, UP, buff=0.2)
        ll.shift(RIGHT * 0.6)
        eq = MathTex(r"s_{ij} = e^{-c\,|\log T_i - \log T_j|}", r"\qquad", r"D_i = \frac{1}{\sum_j s_{ij}}",
                     font_size=40).move_to([0, -0.15, 0])
        eq[0].set_color(EXEC)
        eq[2].set_color(MEM)
        rows = rows_of([
            (r"SIMPLE \ (Brown, \ Neath and Chater, \ 2007): \ memories are points on a log-time line", WHITE),
            (r"an item is recalled if it is distinct from its neighbours: \ $D_i$ is Luce's choice rule", MEM),
            (r"a fresh item is far from everything; \ as it ages, \ it slides toward the crowd", LOST),
            (r"on trial 1 there is no crowd: \ $D = 1$ at any delay; \ the ratio of ages, \ not time, \ is what matters",
             GOOD),
        ], 12.4, 24, 0.22).to_edge(DOWN, buff=0.75)
        ptag = psyche_tag(r"\texttt{wm.simple\_recall}: \ $c = 1$, \ a soft threshold at $D = 0.5$")
        with self.voiceover(
            "Here is a model that explains both findings with a single idea. <bookmark mark='a'/> Gordon Brown, Ian "
            "Neath and Nick Chater's model, called SIMPLE, places every memory on a line of how long ago it was "
            "studied, on a logarithmic scale, like the receding telegraph poles seen from a train. "
            "<bookmark mark='b'/> The similarity of two memories falls off exponentially with their distance on that "
            "line, and an item can be recalled to the extent that it stands out from the others: one over the sum of "
            "its similarities, Luce's choice rule again. <bookmark mark='c'/> Three seconds after study, the new "
            "trigram is far from the earlier trials' items, which are tens of seconds old. Eighteen seconds after "
            "study, on a log scale, it has slid most of the way toward them, and becomes hard to pick out. "
            "<bookmark mark='d'/> On the first trial there's nothing to be confused with, so the item is perfectly "
            "distinct at any delay: no forgetting, exactly as Keppel and Underwood found. Forgetting, in this view, "
            "is not caused by time. It's caused by the ratio of ages, by how much the past crowds the present."
        ) as vo:
            self.play(FadeIn(head), Create(line), FadeIn(ticks), FadeIn(lname), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(FadeIn(early))
            vo.wait_until("b")
            self.play(FadeIn(eq), FadeIn(rows[1]), FadeIn(ptag))
            vo.wait_until("c")
            self.play(FadeIn(short), FadeIn(sl))
            self.play(TransformFromCopy(short, long_), FadeIn(ll), FadeIn(rows[2]), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeOut(early), FadeIn(rows[3]))
        self.clear_scene()
