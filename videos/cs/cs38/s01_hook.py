from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, NO, PART, ROLEC, YES, load, role_strip)


class Hook(VoiceoverScene):
    def construct(self):
        self.storm()
        self.paradox()
        self.plan()

    def storm(self):
        h = load("hook")
        head = label(r"Five Pebbles, \ one log", font_size=36).to_edge(UP, buff=0.3)
        T = 9.0
        x0, W = -4.6, 10.6
        strips = VGroup()
        names = VGroup()
        for i in range(5):
            y = 1.6 - i * 0.62
            strips.add(role_strip(h["timeline"], i, T, width=W, h=0.36, x0=x0, y=y))
            names.add(label(rf"Pebble {i + 1}", font_size=19, color=GREY_A).move_to([x0 - 0.8, y, 0]))
        axis = Line([x0, -1.55, 0], [x0 + W, -1.55, 0], color=GREY_D, stroke_width=1.5)
        ticks = VGroup(*[label(f"{s} s", font_size=15, color=GREY_B).move_to([x0 + s / T * W, -1.8, 0])
                         for s in range(0, 10, 1)])
        marks = VGroup()
        for t, kind, kw in h["events"]:
            if kind in ("crash", "partition", "heal", "restart"):
                x = x0 + t / T * W
                c = {"crash": NO, "partition": KERN, "heal": YES, "restart": DATA}[kind]
                marks.add(DashedLine([x, 1.95, 0], [x, -1.45, 0], color=c, stroke_width=1.5, dash_length=0.06))
                txt = {"crash": r"crash", "partition": r"partition", "heal": r"heal", "restart": r"restart"}[kind]
                marks.add(label(txt, font_size=15, color=c).move_to([x, 2.15, 0]))
        leg = VGroup(*[VGroup(Square(0.22, stroke_width=0, fill_color=ROLEC[r], fill_opacity=0.85),
                              label(r, font_size=17, color=GREY_A)).arrange(RIGHT, buff=0.1)
                       for r in ("leader", "candidate", "follower", "down")]).arrange(RIGHT, buff=0.5).move_to(
            [0, -2.4, 0])
        c = h["campaign"]
        foot = label(rf"this run: \ {h['committed']} commands committed, \ {h['terms']} terms, \ "
                     rf"{h['violations']} violations. \ 1{{,}}000 random storms: \ "
                     rf"{c['violating_runs']} violations", font_size=21, color=YES).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Five Pebbles keep one log of commands between them, a replicated log, and agree on every entry. One "
            "of them leads; the others follow. <bookmark mark='a'/> Here are nine seconds of their lives, while we "
            "do our worst. At one and a half seconds we crash the leader. Within a fifth of a second the others "
            "notice, hold an election, and a new leader carries on. <bookmark mark='b'/> At three seconds we cut "
            "the network in two: two Pebbles on one side, three on the other, one of the three already down. "
            "Neither side has a majority, so neither can commit anything, and the candidates on one side call "
            "election after election, in vain. <bookmark mark='c'/> We heal the network, restart the dead, crash "
            "another leader. Every time, the survivors agree. <bookmark mark='d'/> In this run they commit two "
            "hundred and thirty-six commands through fifteen terms of leadership, and every check we know of "
            "passes. We ran a thousand random storms like it. Not one broke the agreement."
        ) as vo:
            self.play(FadeIn(head), FadeIn(names), Create(axis), FadeIn(ticks), FadeIn(leg))
            vo.wait_until("a")
            self.play(LaggedStart(*[Create(s) for s in strips], lag_ratio=0.1), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(marks))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.5)
        self.clear_scene()

    def paradox(self):
        head = label(r"And yet", font_size=36).to_edge(UP, buff=0.3)
        quote = label(r"``A distributed system is one in which the failure of a computer you didn't even know existed "
                      r"\\ can render your own computer unusable.'' \ --- Leslie Lamport, 1987", font_size=23,
                      color=GREY_A).next_to(head, DOWN, buff=0.5)
        flp = VGroup(
            label(r"\textbf{Fischer, Lynch and Paterson} \ (1985):", font_size=26, color=HEAD),
            label(r"no deterministic protocol can guarantee agreement \\ in an asynchronous network, \ if even one "
                  r"machine may crash", font_size=26, color=NO),
        ).arrange(DOWN, buff=0.25).next_to(quote, DOWN, buff=0.7)
        q = label(r"so what did those five Pebbles give up?", font_size=26, color=YES).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "And yet there is a theorem that says this is impossible. <bookmark mark='a'/> Leslie Lamport once "
            "defined a distributed system as one in which the failure of a computer you did not even know existed "
            "can render your own computer unusable. <bookmark mark='b'/> In 1985 Michael Fischer, Nancy Lynch and "
            "Michael Paterson proved that no deterministic protocol can guarantee that machines agree on even a "
            "single bit, if messages can be delayed without limit and even one machine may crash. "
            "<bookmark mark='c'/> The five Pebbles agree anyway. So what did they give up? That is the story of "
            "this part."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(quote))
            vo.wait_until("b")
            self.play(FadeIn(flp))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.wait(0.5)
        self.clear_scene()

    def plan(self):
        title = label(rf"Part {PART}: \ Distributed Systems I: \ Agreement", font_size=38).to_edge(UP, buff=0.3)
        smap = series_map(current=PART, done=PART - 1).scale(0.92).next_to(title, DOWN, buff=0.35)
        obj = objectives_card([
            r"partial failure and asynchrony: \ the two generals, \ proved hopeless",
            r"time without a clock: \ Lamport clocks, \ vector clocks, \ consistent snapshots",
            r"consensus: \ $f + 1$ rounds when time is kept; \ FLP when it is not",
            r"around FLP: \ randomness, \ failure detectors, \ partial synchrony",
            r"Paxos and Raft, \ proved safe, \ and our Raft attacked a thousand times",
            r"traitors: \ Byzantine generals, \ PBFT, \ and Nakamoto's longest chain",
        ], font_size=25).move_to(DOWN * 0.2)
        with self.voiceover(
            "This is Part 38 of Computer Science, Built: Distributed systems, agreement. <bookmark mark='a'/> We "
            "start with two generals who provably cannot coordinate, and with time when there is no clock to read: "
            "Lamport's clocks, vector clocks, and snapshots of a system that never stops. We define consensus, solve "
            "it in f plus one rounds when time is kept, and prove, with Fischer, Lynch and Paterson, that it cannot "
            "be guaranteed when it is not. Then the ways around: randomness, failure detectors, partial synchrony; "
            "Paxos and Raft, with their proofs; our own Raft, attacked a thousand times; and finally traitors, from "
            "the Byzantine generals to Bitcoin."
        ) as vo:
            self.play(FadeIn(title), FadeIn(smap))
            vo.wait_until("a")
            self.play(FadeOut(smap), FadeIn(obj))
        self.wait(0.5)
        self.clear_scene()
