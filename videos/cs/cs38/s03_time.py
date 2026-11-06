from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, seq_diagram,
                                   space_time)


class Time(VoiceoverScene):
    def construct(self):
        self.card()
        self.ntp()
        self.happened_before()
        self.lamport()
        self.vector()

    def card(self):
        card = chapter_card(2, r"Time without a clock", r"What can ``before'' mean with no shared clock?",
                            lit=(1978, 1991), extra=((1978, r"Lamport: \ Time, Clocks, \\ and the Ordering of Events"),
                                                     (1988, r"Fidge, Mattern: \ vector clocks"),
                                                     (1991, r"Mills: \ NTP")), part=PART)
        with self.voiceover("Chapter two. Time without a clock."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def ntp(self):
        c = load("clocks")
        head = label(r"Setting a clock over a network", font_size=36).to_edge(UP, buff=0.3)
        ev = [(0.0, 1.0, r"$t_0$ \ $\to$ \ $t_1$", True, DATA), (1.3, 2.3, r"$t_2$ \ $\to$ \ $t_3$", False, YES)]
        sd = seq_diagram(ev, t_max=2.8, height=3.6, gap=5.0, names=(r"client", r"time server")).move_to(
            [-3.3, 0.3, 0])
        eqs = VGroup(
            MathTex(r"\theta = \frac{(t_1 - t_0) + (t_2 - t_3)}{2}", font_size=36, color=HEAD),
            MathTex(r"\delta = (t_3 - t_0) - (t_2 - t_1)", font_size=34, color=GREY_A),
        ).arrange(DOWN, buff=0.3).move_to([3.4, 1.3, 0])
        rows = [[f"{r['out_ms']:.0f} ms", f"{r['back_ms']:.0f} ms", f"{r['error_ms']:.0f} ms"] for r in c["ntp"]]
        tab = grid_table([r"there", r"back", r"error in $\theta$"], rows, widths=[1.5, 1.5, 2.0], row_h=0.4,
                         font_size=19, mono_cols=())
        tab.move_to([3.4, -0.9, 0])
        for k in (2, 3):
            tab.cells[k][2].set_color(NO)
        foot = wrapped_label(r"a clock is only as good as the assumption that the two directions take equal time: "
                             r"\ the error is half the asymmetry, \ and no measurement can reveal it", 12.4,
                             font_size=21, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "First, the obvious approach: set every clock from a good one. David Mills's network time protocol "
            "does this across the Internet. <bookmark mark='a'/> The client notes its time when it sends a request, "
            "t zero; the server notes when it receives it, t one, and when it replies, t two; the client notes when "
            "the reply arrives, t three. <bookmark mark='b'/> If the trip there and the trip back take equal time, "
            "the offset between the clocks is this average, and the round trip is this difference. "
            "<bookmark mark='c'/> With a true offset of five seconds and forty milliseconds each way, the estimate "
            "is exact. But if the request takes seventy milliseconds and the reply ten, the estimate is thirty "
            "milliseconds off, and nothing the client can measure reveals it. <bookmark mark='d'/> Clocks set "
            "this way are good to milliseconds on the Internet and microseconds on a local network. Useful, but "
            "never good enough to decide which of two nearly simultaneous events came first."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd[:4]))
            vo.wait_until("a")
            self.play(FadeIn(sd.arrows))
            vo.wait_until("b")
            self.play(Write(eqs))
            vo.wait_until("c")
            self.play(FadeIn(tab))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def happened_before(self):
        c = load("clocks")
        tr = c["trace"]
        head = label(r"Happened before", font_size=36).to_edge(UP, buff=0.3)
        st = space_time(3, tr, x0=-5.4, x1=5.8, y0=1.6, dy=1.3)
        rules = VGroup(
            label(r"$a \to b$ \ if $a$ comes before $b$ on the same process,", font_size=25, color=WHITE),
            label(r"\ or $a$ is the sending of a message and $b$ its receipt,", font_size=25, color=WHITE),
            label(r"\ or $a \to c$ and $c \to b$ for some $c$. \ \ Otherwise $a$ and $b$ are \textbf{concurrent}: "
                  r"$a \parallel b$", font_size=22, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1978 Leslie Lamport replaced time by causality. Draw each process as a line, its events as dots "
            "in order, and messages as arrows. <bookmark mark='a'/> Event a happened before event b if a comes "
            "earlier on the same process, or a sends a message that b receives, or there is a chain of such steps "
            "from a to b. <bookmark mark='b'/> If neither happened before the other, they are concurrent: no "
            "information could have passed between them, so no observer can ever say which came first, and it "
            "does not matter. Happened-before is a partial order, and it is the only order a distributed system "
            "can know."
        ) as vo:
            self.play(FadeIn(head), FadeIn(st.lines))
            self.play(LaggedStart(*[FadeIn(d) for d in st.dots], lag_ratio=0.08), FadeIn(st.arrows))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]), FadeIn(rules[1]))
            vo.wait_until("b")
            self.play(FadeIn(rules[2]))
        self.wait(0.4)
        self.clear_scene()

    def lamport(self):
        c = load("clocks")
        tr = c["trace"]
        head = label(r"Lamport clocks", font_size=36).to_edge(UP, buff=0.3)
        st = space_time(3, tr, x0=-5.4, x1=5.8, y0=1.6, dy=1.3, stamps=[str(x) for x in c["lamport"]],
                        stamp_color=HEAD, font=26)
        rules = VGroup(
            label(r"each process keeps a counter: \ $+1$ at every event; \ every message carries it; \ on "
                  r"receipt, \ $C \leftarrow \max(C, C_{\text{msg}}) + 1$", font_size=21, color=WHITE),
            label(r"\textbf{clock condition}: \ $a \to b \Rightarrow C(a) < C(b)$ \ \ but not the converse", font_size=25,
                  color=HEAD),
        ).arrange(DOWN, buff=0.15).to_edge(DOWN, buff=0.4)
        ag = c["aggregate"]
        with self.voiceover(
            "Lamport's clocks turn the partial order into numbers. <bookmark mark='a'/> Each process keeps a "
            "counter and adds one at every event. Every message carries the sender's counter, and the receiver "
            "jumps past it: the maximum of its own and the message's, plus one. <bookmark mark='b'/> Then if a "
            "happened before b, a's number is smaller. Ties are broken by process number, and the result is a "
            "total order that every process agrees on, consistent with causality, which is enough to build a "
            "mutual exclusion lock with no central server. <bookmark mark='c'/> But the converse fails. In two "
            "hundred random executions we checked, concurrent pairs got different numbers almost every time, "
            "nineteen thousand of twenty-three thousand, so a smaller number does not mean earlier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(st.lines), FadeIn(st.dots), FadeIn(st.arrows))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]), LaggedStart(*[FadeIn(t) for t in st.labels], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]))
            vo.wait_until("c")
            self.play(Indicate(rules[1], color=NO))
        self.wait(0.4)
        self.clear_scene()
        _ = ag

    def vector(self):
        c = load("clocks")
        tr = c["trace"]
        head = label(r"Vector clocks", font_size=36).to_edge(UP, buff=0.3)
        st = space_time(3, tr, x0=-5.4, x1=5.8, y0=1.7, dy=1.3,
                        stamps=["(" + ",".join(map(str, v)) + ")" for v in c["vector"]], stamp_color=LAM, font=21)
        ag = c["aggregate"]
        rules = VGroup(
            label(r"each process keeps a vector: \ its own entry $+1$ at every event; \ on receipt, \ "
                  r"take the element-wise maximum", font_size=20, color=WHITE),
            label(r"\textbf{Theorem.} \ $a \to b \iff V(a) < V(b)$ \ (every entry $\le$, \ some $<$)", font_size=25,
                  color=YES),
            label(rf"checked on {ag['runs']} random executions, \ {ag['pairs']:,} pairs: \ "
                  rf"{ag['vector_ok']} of {ag['runs']} exact; \ race detectors use exactly this \ (Part 33)",
                  font_size=19, color=GREY_A),
        ).arrange(DOWN, buff=0.13).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "To capture causality exactly, each process keeps not one counter but a vector, one entry per process: "
            "how many events of each process it has heard of. This is Colin Fidge's and Friedemann Mattern's "
            "vector clock, from 1988. <bookmark mark='a'/> A process increments its own entry at each event, and on "
            "receiving a message takes the element-wise maximum with the vector it carries. "
            "<bookmark mark='b'/> Now a happened before b exactly when a's vector is less than or equal to b's in "
            "every entry and smaller in one. The proof: a's entry for its own process counts a's position, and b's "
            "vector reaches that count only if some chain of messages carried it there. <bookmark mark='c'/> We "
            "checked the theorem on two hundred random executions, forty-two thousand pairs of events: exact every "
            "time. The data race detectors of Part 33 use exactly this, with threads for processes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(st.lines), FadeIn(st.dots), FadeIn(st.arrows))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]), LaggedStart(*[FadeIn(t) for t in st.labels], lag_ratio=0.1))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]))
            vo.wait_until("c")
            self.play(FadeIn(rules[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN, YES)
