from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs37.common import (CCC, CCN, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load, trace)


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.theorem()

    def card(self):
        self.chapter(16, r"Frontier: \ can congestion control be fair?", r"Is there an algorithm that is fast, low-delay and fair on every path?", lit=(2013, 2023), extra=((2013, r"Winstein and Balakrishnan: \ Remy"),
                                   (2021, r"Arun et al.: \ verifying CCAs"),
                                   (2022, r"Arun, Alizadeh \\ and Balakrishnan: \\ starvation"),
                                   (2023, r"L4S: \ RFC 9330")), part=PART, said="Chapter sixteen. Frontier: can congestion control be fair?")

    def theorem(self):
        self.ask(r"Delay-based congestion control, noisy delays. \\ Can it guarantee fairness?", [r"yes", r"no"], 1,
                 say="Modern algorithms react to delay, and delays are noisy. Can such an algorithm guarantee fairness?",
                 reveal="No: a 2022 theorem shows it must starve someone, or keep long queues.")
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




_ = (DATA, grid_table)
