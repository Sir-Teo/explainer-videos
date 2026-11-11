from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (CCC, CCN, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.theorem()
        self.measured()
        self.open()

    def card(self):
        card = chapter_card(16, r"Frontier: \ can congestion control be fair?",
                            r"Is there an algorithm that is fast, low-delay and fair on every path?", lit=(2013, 2023),
                            extra=((2013, r"Winstein and Balakrishnan: \ Remy"),
                                   (2021, r"Arun et al.: \ verifying CCAs"),
                                   (2022, r"Arun, Alizadeh \\ and Balakrishnan: \\ starvation"),
                                   (2023, r"L4S: \ RFC 9330")), part=PART)
        with self.voiceover("Chapter sixteen. Frontier: can congestion control be fair?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def theorem(self):
        head = label(r"Starvation \ (2022)", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            wrapped_label(r"Modern algorithms want low delay, \ so they react to \textbf{delay}, \ not loss: \ "
                          r"Vegas, \ FAST, \ Copa, \ BBR. \ In steady state each keeps the queueing delay within some "
                          r"range $\delta(C)$ that depends on the link rate.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"But not all delay is congestion: \ Wi-Fi and cellular links batch ACKs, \ schedulers "
                          r"hold packets, \ routes differ by milliseconds. \ Call the bound on such "
                          r"\textit{non-congestive} delay $D$.", 12.4, font_size=24, color=KERN),
            wrapped_label(r"\textbf{Theorem} \ (Arun, Alizadeh and Balakrishnan). \ If $D > \delta$, \ then for "
                          r"any such algorithm there is a network with two flows in which one gets an "
                          r"\textit{arbitrarily small} share of the other's rate.", 12.4, font_size=25, color=NO),
            wrapped_label(r"Idea: \ a flow cannot tell its own queue from noise it cannot see; \ add noise to one "
                          r"flow's path and it believes the link is busier than it is, \ so it yields \ --- \ and "
                          r"for delay-convergent rules, \ by as much as you like.", 12.4, font_size=24, color=GREY_A),
            wrapped_label(r"So: \ low delay, \ high utilization, \ fairness under jitter: \ choose two.", 12.4,
                          font_size=27, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "Half a century after the alternating bit, congestion control still has open questions, and in 2022 it "
            "acquired an impossibility theorem. <bookmark mark='a'/> To keep queues short, modern algorithms "
            "react to delay rather than waiting for loss. Each, in steady state, keeps the queueing delay inside "
            "some small range. <bookmark mark='b'/> But some delay has nothing to do with congestion. Wi-Fi and "
            "cellular links deliver ACKs in batches; schedulers hold packets back; two paths differ by a few "
            "milliseconds. <bookmark mark='c'/> Venkat Arun, Mohammad Alizadeh and Hari Balakrishnan proved that "
            "if this non-congestive delay can exceed the range an algorithm converges to, there is a network in "
            "which one of two flows gets an arbitrarily small share. <bookmark mark='d'/> The reason is simple to "
            "state. A flow cannot tell its own queue apart from delay it cannot see the cause of. Add a little "
            "noise to one flow's path, and it believes the link is busier than it is, and yields. "
            "<bookmark mark='e'/> Low delay, full use of the link, and fairness despite jitter: you can choose two."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.6)
        self.clear_scene()

    def measured(self):
        f = load("frontier")
        head = label(r"Measured: \ jitter on one flow's ACKs", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 40, 10], [0, 1.05, 0.25], x_length=6.4, y_length=3.8, x_label=r"jitter on one flow's ACKs, "
                 r"\ ms", y_label=r"jittery flow's share", xticks=range(0, 41, 10), yticks=(0.25, 0.5, 0.75, 1.0),
                 fy=lambda v: f"{v:.2f}").move_to([-3.0, -0.4, 0])
        ax = g.ax
        fair = DashedLine(ax.c2p(0, 0.5), ax.c2p(40, 0.5), color=GREY_B, dash_length=0.1)
        lines = VGroup()
        for cc in ("vegas", "bbr", "reno"):
            rows = [r for r in f["rows"] if r["cc"] == cc]
            pts = [(r["jitter_ms"], r["jittery"] / (r["steady"] + r["jittery"])) for r in rows]
            lines.add(VGroup(trace(ax, pts, CCC[cc], width=3),
                             *[Dot(ax.c2p(x, y), radius=0.06, color=CCC[cc]) for x, y in pts]))
        leg = VGroup(*[label(CCN[c], font_size=20, color=CCC[c]) for c in ("vegas", "bbr", "reno")]).arrange(
            DOWN, aligned_edge=LEFT, buff=0.12).move_to([3.2, 1.7, 0])
        v40 = next(r for r in f["rows"] if r["cc"] == "vegas" and r["jitter_ms"] == 40)
        b40 = next(r for r in f["rows"] if r["cc"] == "bbr" and r["jitter_ms"] == 40)
        notes = VGroup(
            wrapped_label(r"two flows of the same algorithm, \ 20 Mb/s, \ RTT 40 ms; \ one flow's ACKs are delayed, "
                          r"in order, \ by up to $D$", 5.6, font_size=18, color=GREY_A),
            wrapped_label(rf"Vegas at 40 ms: \ {v40['steady']:.1f} against {v40['jittery']:.1f} Mb/s, \ and "
                          r"falling as the jitter grows", 5.6, font_size=19, color=CCC["vegas"]),
            wrapped_label(rf"BBR at 40 ms: \ {b40['steady']:.1f} against {b40['jittery']:.1f}: \ its min-RTT filter "
                          r"resists, \ but not entirely", 5.6, font_size=19, color=CCC["bbr"]),
            wrapped_label(r"Reno pays only the longer round trip, \ and stops there: \ it converges on loss, \ not "
                          r"delay \ --- \ and fills the buffer to do it", 5.6, font_size=19, color=CCC["reno"]),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.4, -1.1, 0])
        with self.voiceover(
            "We can watch it happen in our simulator. Two flows of the same algorithm share a twenty-megabit link, "
            "and one flow's ACKs are delayed by a random amount, up to D, kept in order, as a Wi-Fi link might "
            "deliver them. <bookmark mark='a'/> With Vegas, the jittery flow's share falls steadily: at forty "
            "milliseconds of jitter it gets one and a half megabits against seventeen point seven, and it keeps "
            "falling. <bookmark mark='b'/> BBR resists better, because its estimate of the propagation delay is a "
            "minimum, which filters noise out, but at forty milliseconds the split is fifteen to four. "
            "<bookmark mark='c'/> Reno is hurt only as any longer round trip hurts it, and the damage stops "
            "growing, because it converges on losses, not delays. Its price for that robustness is the full "
            "buffer of delay we saw in chapter nine."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), Create(fair), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(Create(lines[0]), FadeIn(leg[0]), FadeIn(notes[1]))
            vo.wait_until("b")
            self.play(Create(lines[1]), FadeIn(leg[1]), FadeIn(notes[2]))
            vo.wait_until("c")
            self.play(Create(lines[2]), FadeIn(leg[2]), FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Fairness under jitter}: \ how much queueing delay must an algorithm accept "
                          r"to stay within a factor $k$ of fair when non-congestive delay is up to $D$? \ The 2022 "
                          r"theorem gives the impossibility; \ the exact trade-off curve is open.", 12.4,
                          font_size=23, color=WHITE),
            wrapped_label(r"2. \ \textbf{Help from the network}: \ L4S \ (2023) \ has routers mark packets early "
                          r"with ECN, \ so senders see congestion without guessing from delay: \ sub-millisecond "
                          r"queues, \ if every sender cooperates; \ deployment has begun.", 12.4, font_size=23,
                          color=YES),
            wrapped_label(r"3. \ \textbf{Learned and verified control}: \ Remy \ (2013) \ searched for rules by "
                          r"computer; \ Aurora and Orca learned them; \ CCAC \ (2021) \ proved properties of real "
                          r"algorithms with an SMT solver, \ and found bugs in some.", 12.4, font_size=23, color=LAM),
            wrapped_label(r"4. \ \textbf{Coexistence}: \ no theory says what happens when Reno, \ CUBIC, \ BBR and "
                          r"QUIC's variants share a bottleneck; \ the Internet runs the experiment daily.", 12.4,
                          font_size=23, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.5)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ the delay--fairness trade-off, \ "
                             r"measured on our dumbbell", 12.4, font_size=21, color=HEAD).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where this leaves the field. <bookmark mark='a'/> The theorem says what is impossible, but not the "
            "exact price: how much queueing delay must an algorithm accept to stay within some factor of fair, "
            "when the noise can reach D? That curve is not known. <bookmark mark='b'/> One escape is to ask the "
            "network for help. L4S, standardized in 2023, has routers mark packets with explicit congestion "
            "notification long before queues build, so senders need not guess congestion from delay; if every "
            "sender on a link cooperates, queues stay under a millisecond. <bookmark mark='c'/> Another is to let "
            "computers design the rules. Remy, in 2013, searched for congestion control rules automatically; later "
            "systems learned them with reinforcement learning; and in 2021 Arun and colleagues used an SMT solver, "
            "the tool of Part 26, to prove properties of real algorithms, and found flaws in some. "
            "<bookmark mark='d'/> And no theory yet describes the Internet as it is, with Reno, CUBIC, BBR and a "
            "dozen variants of QUIC's control all sharing the same queues. <bookmark mark='e'/> This part's "
            "research problem asks you to measure that delay and fairness trade-off on our own simulator."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, grid_table)
