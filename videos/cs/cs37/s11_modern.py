from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (CCC, CCN, DATA, HEAD, KERN, LAM, NO, PART, WIN, YES, axes, grid_table, load,
                                   trace)


class Modern(VoiceoverScene):
    def construct(self):
        self.card()
        self.cubic()
        self.kleinrock()
        self.bbr()
        self.compare()
        self.coexist()

    def card(self):
        card = chapter_card(10, r"Modern congestion control", r"Must a sender fill the queue to find the pipe?",
                            lit=(1994, 2016), extra=((1994, r"Brakmo and Peterson: \ Vegas"),
                                                     (2008, r"Ha, Rhee and Xu: \ CUBIC"),
                                                     (2010, r"Alizadeh et al.: \ DCTCP"),
                                                     (2016, r"Cardwell et al.: \ BBR")), part=PART)
        with self.voiceover("Chapter ten. Modern congestion control."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def cubic(self):
        head = label(r"CUBIC: \ grow with the clock", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 12, 2], [0, 1.4, 0.5], x_length=6.4, y_length=3.6, x_label=r"seconds since the last loss",
                 y_label=r"window", xticks=range(0, 13, 2), yticks=(0.7, 1.0), fy=lambda v: {0.7: r"$0.7\,W_{\max}$",
                                                                                         1.0: r"$W_{\max}$"}.get(
                     round(v, 1), f"{v:g}")).move_to([-3.0, -0.4, 0])
        ax = g.ax
        C, beta = 0.4, 0.7
        Wm = 100.0
        K = (Wm * (1 - beta) / C) ** (1 / 3)
        f = ax.plot(lambda t: (C * (t - K) ** 3 + Wm) / Wm, x_range=[0, 8.7], color=CCC["cubic"], stroke_width=3)
        wm = DashedLine(ax.c2p(0, 1), ax.c2p(12, 1), color=GREY_B, dash_length=0.1)
        kl = DashedLine(ax.c2p(K, 0), ax.c2p(K, 1), color=GREY_B, dash_length=0.08)
        kt = MathTex(r"K", font_size=26, color=GREY_B).next_to(ax.c2p(K, 0), DOWN, buff=0.1)
        eq = MathTex(r"W(t) = C\,(t - K)^3 + W_{\max}, \quad K = \sqrt[3]{W_{\max}(1-\beta)/C}", font_size=30,
                     color=CCC["cubic"]).move_to([3.4, 1.6, 0])
        if eq.width > 6.4:
            eq.width = 6.4
        notes = VGroup(
            wrapped_label(r"after a loss, \ cut to $0.7\,W_{\max}$; \ climb fast, \ \textbf{flatten} near the window "
                          r"where the last loss happened, \ then probe beyond it", 6.0, font_size=20, color=WHITE),
            wrapped_label(r"growth depends on \textbf{time}, \ not on round trips: \ flows with long RTTs are not "
                          r"penalized as under Reno", 6.0, font_size=20, color=LAM),
            wrapped_label(r"the Linux default since 2006; \ Windows and macOS too", 6.0, font_size=20,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([3.4, -0.9, 0])
        with self.voiceover(
            "On fast, long paths Reno is hopeless: after a single loss on our hundred-megabit transatlantic path, "
            "climbing back by one packet per round trip takes over a minute and a half. Injong Rhee and his "
            "students replaced the line with a cubic. <bookmark mark='a'/> After a loss, CUBIC remembers the window "
            "where it happened, cuts to seven tenths of it, and follows a cubic curve in time: steep at first, "
            "flattening as it approaches the old window, where the last trouble was, and then accelerating "
            "beyond it to probe for more. <bookmark mark='b'/> Its growth depends on the clock, not on the "
            "number of round trips, so a distant flow grows as fast as a nearby one. <bookmark mark='c'/> CUBIC "
            "has been the default in Linux since 2006, and so in most of the servers on the Internet."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(wm))
            vo.wait_until("a")
            self.play(Create(f), run_time=2.5)
            self.play(Create(kl), FadeIn(kt), Write(eq), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def kleinrock(self):
        m = load("modern")
        head = label(r"Kleinrock's operating point", font_size=36).to_edge(UP, buff=0.3)
        kl = m["kleinrock"]
        bdp = m["bdp"]
        g1 = axes([0, 3, 1], [0, 120, 50], x_length=5.4, y_length=2.4, y_label=r"delivery rate, \ Mb/s",
                  xticks=(1, 2, 3), yticks=(50, 100), fx=lambda v: rf"{v:g} BDP").move_to([-3.3, 1.0, 0])
        g2 = axes([0, 3, 1], [0, 350, 100], x_length=5.4, y_length=2.4, y_label=r"round trip, \ ms",
                  x_label=r"data in flight", xticks=(1, 2, 3), yticks=(100, 200, 300),
                  fx=lambda v: rf"{v:g} BDP").move_to([-3.3, -2.1, 0])
        r1 = trace(g1.ax, [(k["inflight"] / bdp, k["rate"]) for k in kl], YES, width=3)
        r2 = trace(g2.ax, [(k["inflight"] / bdp, k["rtt_ms"]) for k in kl], NO, width=3)
        opt1 = DashedLine(g1.ax.c2p(1, 0), g1.ax.c2p(1, 115), color=WHITE, dash_length=0.08)
        opt2 = DashedLine(g2.ax.c2p(1, 0), g2.ax.c2p(1, 340), color=WHITE, dash_length=0.08)
        b1 = Brace(Line(g2.ax.c2p(1, 0), g2.ax.c2p(2, 0)), UP, color=CCC["reno"]).shift(UP * 1.4)
        notes = VGroup(
            wrapped_label(r"below one BDP in flight: \ the pipe is not full, \ the round trip is just "
                          r"propagation", 5.8, font_size=20, color=WHITE),
            wrapped_label(r"above it: \ no more throughput, \ only queue; \ the round trip grows with every packet",
                          5.8, font_size=20, color=NO),
            wrapped_label(r"\textbf{Kleinrock (1979)}: \ operate at the knee, \ full rate at minimum delay", 5.8,
                          font_size=20, color=YES),
            wrapped_label(r"loss-based TCP operates at the \textit{cliff}: \ pipe $+$ buffer, \ because a loss is "
                          r"its only signal", 5.8, font_size=20, color=CCC["reno"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.28).move_to([3.5, -0.4, 0])
        with self.voiceover(
            "What is the ideal amount of data to have in flight? Plot two things against it. "
            "<bookmark mark='a'/> Below one bandwidth-delay product, the pipe is not full: the delivery rate grows "
            "with the data in flight, and the round trip is just propagation. <bookmark mark='b'/> Above it, the "
            "rate is stuck at the bottleneck's, and every extra packet only waits in a queue, lengthening the "
            "round trip. <bookmark mark='c'/> Leonard Kleinrock observed in 1979 that the best place to operate "
            "is the knee: exactly one bandwidth-delay product in flight, full rate at minimum delay. "
            "<bookmark mark='d'/> Loss-based congestion control cannot operate there. Its only signal is a loss, "
            "and a loss happens only when the buffer is full, so it lives at the cliff, at the far end of the "
            "queue, and pays the whole buffer in delay."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1), FadeIn(g2))
            vo.wait_until("a")
            self.play(Create(r1), Create(r2), run_time=2)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(Create(opt1), Create(opt2), FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]), GrowFromCenter(b1))
        self.wait(0.4)
        self.clear_scene()

    def bbr(self):
        m = load("modern")
        head = label(r"BBR: \ model the path", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 60, 10], [0, 2800, 900], x_length=6.6, y_length=3.6, x_label=r"seconds",
                 y_label=r"window, \ packets", xticks=range(0, 61, 10), yticks=(900, 1800, 2700),
                 fy=lambda v: f"{v:,.0f}").move_to([-3.0, -0.4, 0])
        ax = g.ax
        tr = trace(ax, m["solo"]["bbr"]["trace"], CCC["bbr"], width=2.4)
        bd = DashedLine(ax.c2p(0, 900), ax.c2p(60, 900), color=GREY_B, dash_length=0.1)
        steps = VGroup(
            wrapped_label(r"estimate the \textbf{bottleneck bandwidth}: \ the highest delivery rate over the last "
                          r"10 round trips", 5.8, font_size=19, color=YES),
            wrapped_label(r"estimate the \textbf{propagation delay}: \ the lowest RTT over the last 10 s", 5.8,
                          font_size=19, color=DATA),
            wrapped_label(r"\textbf{pace} packets at the bandwidth; \ keep about one BDP in flight; \ every 8 round "
                          r"trips probe at 1.25$\times$, \ then drain at 0.75$\times$", 5.8, font_size=19,
                          color=WHITE),
            wrapped_label(r"startup doubles like slow start, \ then drains the queue it built; \ every 10 s, \ "
                          r"\textbf{PROBE\_RTT} empties the pipe to re-measure the delay", 5.8, font_size=19,
                          color=KERN),
            wrapped_label(r"a loss is \textit{not} taken as congestion", 5.8, font_size=19, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.5, -0.3, 0])
        with self.voiceover(
            "In 2016 Neal Cardwell, Yuchung Cheng, Van Jacobson and their colleagues at Google published BBR, a "
            "congestion control that aims for Kleinrock's point. Instead of reacting to losses, it builds a model "
            "of the path. <bookmark mark='a'/> The bottleneck bandwidth is estimated as the highest rate at which "
            "ACKs have come back in the last ten round trips. <bookmark mark='b'/> The propagation delay is the "
            "lowest round trip seen in the last ten seconds. <bookmark mark='c'/> BBR then paces its packets out at "
            "the estimated bandwidth, keeps about one bandwidth-delay product in flight, and every eight round trips "
            "sends a little faster for one round, to see if the pipe has grown, and a little slower for the next, "
            "to drain what that added. <bookmark mark='d'/> It starts up by doubling, like slow start, then drains "
            "the queue that built; and every ten seconds it briefly empties the pipe, to measure the delay again. "
            "Here is our BBR's window on the transatlantic path: the startup spike, then a steady cap at two "
            "pipes, while pacing keeps about one pipe actually in flight, with the dips of those re-measurements. <bookmark mark='e'/> And losses it does not treat as "
            "congestion at all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(bd))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
            self.play(Create(tr), run_time=2.5)
            vo.wait_until("e")
            self.play(FadeIn(steps[4]))
        self.wait(0.4)
        self.clear_scene()

    def compare(self):
        m = load("modern")
        head = label(r"Three algorithms, \ one transatlantic path", font_size=36).to_edge(UP, buff=0.3)
        rows = [[CCN[c], f"{m['solo'][c]['mbps']:.1f}", f"{m['solo'][c]['queue_ms']:.0f} ms",
                 f"{m['lossy'][c]:.1f}"] for c in ("reno", "cubic", "bbr")]
        tab = grid_table([r"alone on 100 Mb/s, \ RTT 108 ms", r"Mb/s", r"mean queue", r"Mb/s with 0.1\% loss"],
                         rows, widths=[3.8, 1.6, 2.2, 3.2], row_h=0.48, font_size=21, mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        for k, c in enumerate(("reno", "cubic", "bbr"), start=1):
            for j in range(4):
                tab.cells[k][j].set_color(CCC[c])
        lines = VGroup(
            wrapped_label(r"all three fill a clean pipe; \ BBR does it with a tenth of CUBIC's queue", 12.4,
                          font_size=21, color=WHITE),
            wrapped_label(r"random loss, \ one packet in a thousand, \ caps Reno and CUBIC as Mathis predicts; \ "
                          r"BBR barely notices", 12.4, font_size=21, color=YES),
            wrapped_label(r"Google reported YouTube and its WAN getting 2 to 25 times the throughput, \ and a third "
                          r"less delay, \ after switching \ (2016--17)", 12.4, font_size=21, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.55)
        with self.voiceover(
            "We ran each algorithm alone on the transatlantic path, a hundred megabits a second, a buffer of one "
            "bandwidth-delay product. <bookmark mark='a'/> On a clean path, all three fill the pipe, about "
            "ninety-five megabits a second. But CUBIC keeps the queue eighty milliseconds long on average, and BBR "
            "eight: the same throughput at a tenth of the delay. <bookmark mark='b'/> Now lose one packet in a "
            "thousand at random, as a noisy radio link or a failing cable might. Reno falls to five and a half "
            "megabits, CUBIC to eight, as the Mathis formula says. BBR, which does not read random loss as "
            "congestion, keeps ninety-five. <bookmark mark='c'/> When Google switched its servers to BBR, it "
            "reported large gains on exactly such paths. That is the hook's answer: the eleven times was a theory "
            "of what a lost packet means."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k][:3])) for k in range(1, 4)], lag_ratio=0.3),
                      FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(tab.cells[k][3]) for k in range(1, 4)], lag_ratio=0.3),
                      FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def coexist(self):
        m = load("modern")
        head = label(r"Sharing: \ the hard part", font_size=36).to_edge(UP, buff=0.3)
        rows = [[rf"{x['mult']:g} $\times$ BDP", f"{x['bbr']:.1f}", f"{x['cubic']:.1f}"] for x in m["mixed"]]
        tab = grid_table([r"buffer", r"BBR, \ Mb/s", r"CUBIC, \ Mb/s"], rows, widths=[2.4, 2.2, 2.2], row_h=0.44,
                         font_size=20, mono_cols=())
        tab.move_to([-3.4, 1.0, 0])
        for k in range(1, 4):
            tab.cells[k][1].set_color(CCC["bbr"])
            tab.cells[k][2].set_color(CCC["cubic"])
        v = m["vegas"]
        vt = grid_table([r"Vegas alone", r"Vegas with Reno", r"Reno"],
                        [[f"{v['mbps']:.1f} Mb/s, \\ {v['queue_pkts']:.1f} queued", f"{v['with_reno'][0]:.1f}",
                          f"{v['with_reno'][1]:.1f}"]], widths=[3.4, 2.4, 1.4], row_h=0.44, font_size=19,
                        mono_cols=())
        vt.move_to([-3.0, -1.4, 0])
        vt.cells[1][1].set_color(NO)
        notes = VGroup(
            wrapped_label(r"BBR beside CUBIC on 50 Mb/s: \ in shallow buffers BBR's loss-blind pacing takes almost "
                          r"everything; \ in deep ones CUBIC's queue inflates BBR's RTT estimate and it backs off", 5.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"\textbf{Vegas} \ (1994) \ backs off when \textit{it} sees delay; \ Reno, \ beside it, \ "
                          r"fills the queue and takes the link", 5.4, font_size=19, color=CCC["vegas"]),
            wrapped_label(r"a polite algorithm loses to a greedy one: \ which is why delay-based control spread only "
                          r"where one owner controls every sender: \ \textbf{DCTCP} in data centres, \ marking "
                          r"packets with ECN instead of dropping them", 5.4, font_size=19, color=HEAD),
            wrapped_label(r"BBRv2 and v3 now react to loss and ECN as well", 5.4, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.5, -0.2, 0])
        with self.voiceover(
            "The hardest problem in congestion control is not one flow; it is different algorithms sharing a link. "
            "<bookmark mark='a'/> Put BBR and CUBIC together on fifty megabits a second. With a shallow buffer, "
            "BBR, which ignores the losses that keep CUBIC down, takes forty-seven megabits and leaves CUBIC one "
            "point three. With a buffer four times the product, CUBIC fills the queue, BBR's round trip estimate "
            "inflates, and the split is thirty to eighteen. Neither is fair. <bookmark mark='b'/> The older story "
            "runs the other way. TCP Vegas, by Lawrence Brakmo and Larry Peterson in 1994, was the first "
            "delay-based algorithm: it slows down as soon as it sees its own packets queueing, keeping about four "
            "in the queue. Alone, it fills the link with a near-empty queue. Beside Reno, which keeps filling the "
            "queue, Vegas sees only delay, backs off, and gets nothing at all. <bookmark mark='c'/> A polite "
            "algorithm loses to a greedy one. So delay-based control spread where one owner controls every sender: "
            "in data centres, DCTCP has switches mark packets instead of dropping them, and senders back off in "
            "proportion to the marks, keeping queues tiny. <bookmark mark='d'/> Newer versions of BBR now respond "
            "to loss and marks too."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(vt), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, WIN)
