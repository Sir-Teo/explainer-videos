from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, box, grid_table, load)


class Paxos(VoiceoverScene):
    def construct(self):
        self.card()
        self.protocol()
        self.invariant()
        self.duel()
        self.multi()

    def card(self):
        card = chapter_card(6, r"Paxos", r"How do you choose one value when proposers and acceptors can fail?",
                            lit=(1989, 2001), extra=((1989, r"Lamport: \ The Part-Time Parliament"),
                                                     (1988, r"Oki and Liskov: \ Viewstamped Replication"),
                                                     (2001, r"Paxos Made Simple")), part=PART)
        with self.voiceover("Chapter six. Paxos."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def protocol(self):
        head = label(r"Two phases, \ numbered ballots", font_size=36).to_edge(UP, buff=0.3)
        P = box(2.2, 0.8, r"proposer", DATA, font_size=22).move_to([-5.0, 0.4, 0])
        accs = VGroup(*[box(1.6, 0.6, rf"acceptor {i + 1}", LAM, font_size=18) for i in range(5)]).arrange(
            DOWN, buff=0.18).move_to([0.2, 0.0, 0])
        arr = VGroup(*[Arrow(P.get_right(), a.get_left(), buff=0.1, color=GREY_B, stroke_width=1.8) for a in accs])
        steps = VGroup(
            wrapped_label(r"\textbf{1a prepare}$(b)$: \ ``I want to propose with ballot $b$''", 4.8, font_size=19,
                          color=DATA),
            wrapped_label(r"\textbf{1b promise}: \ ``I will ignore ballots below $b$; \ here is the highest-ballot "
                          r"value I have accepted, \ if any''", 4.8, font_size=19, color=LAM),
            wrapped_label(r"\textbf{2a accept}$(b, v)$: \ with promises from a majority, \ $v$ is the value of the "
                          r"highest ballot reported, \ or the proposer's own if none", 4.8, font_size=19,
                          color=HEAD),
            wrapped_label(r"\textbf{2b accepted}: \ unless it promised a higher ballot. \ $v$ is \textbf{chosen} "
                          r"once a majority accept it in the same ballot", 4.8, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([4.5, -0.2, 0])
        with self.voiceover(
            "Leslie Lamport wrote Paxos up in 1989 as the legislature of an imaginary Greek island, and the "
            "parable was so baffling that the paper waited nine years to be published. Here it is plainly. Some "
            "processes propose values, and a set of acceptors, five here, vote. <bookmark mark='a'/> In phase one "
            "a proposer picks a ballot number larger than any it has used, and asks every acceptor to prepare. "
            "<bookmark mark='b'/> Each acceptor that has not promised a higher ballot promises to ignore lower ones "
            "from now on, and reports the highest-numbered proposal it has already accepted, if any. "
            "<bookmark mark='c'/> With promises from a majority, the proposer enters phase two. It must propose "
            "the value of the highest ballot reported to it; only if none was reported may it propose its own. "
            "<bookmark mark='d'/> Acceptors accept unless they have since promised a higher ballot, and a value is "
            "chosen the moment a majority have accepted it in the same ballot."
        ) as vo:
            self.play(FadeIn(head), FadeIn(P), FadeIn(accs), Create(arr))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()

    def invariant(self):
        head = label(r"Why only one value is ever chosen", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            wrapped_label(r"\textbf{Invariant.} \ If $v$ is chosen in ballot $b$, \ every accept request with a "
                          r"ballot $b' > b$ carries $v$.", 12.4, font_size=26, color=HEAD),
            wrapped_label(r"\textbf{Induction on $b'$.} \ The proposer of $b'$ heard promises from a majority $Q$; "
                          r"the majority $A$ that accepted $v$ in $b$ meets $Q$ \ (two majorities of five share at "
                          r"least one acceptor).", 12.4, font_size=25, color=WHITE),
            wrapped_label(r"That shared acceptor reported an accepted ballot $\ge b$. \ The highest reported ballot $c$ "
                          r"therefore has $b \le c < b'$, \ and by induction its value is $v$. \ So the proposer of "
                          r"$b'$ must propose $v$.", 12.4, font_size=25, color=KERN),
            wrapped_label(r"Hence any value chosen later, \ in any ballot, \ is $v$: \ \textbf{agreement}, \ with no "
                          r"assumption about timing at all. \ Majorities intersecting is the whole trick.", 12.4,
                          font_size=25, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Safety is a short induction. <bookmark mark='a'/> Suppose v was chosen in ballot b. We show every "
            "accept request with a larger ballot carries v. <bookmark mark='b'/> Take such a ballot, b prime. Its "
            "proposer collected promises from some majority, and the majority that accepted v in ballot b overlaps "
            "it, because any two majorities of five acceptors share at least one. <bookmark mark='c'/> That shared "
            "acceptor reported having accepted something in ballot b or later, so the highest ballot reported to "
            "the proposer lies between b and b prime, and by the induction its value is v. The proposer is forced "
            "to propose v. <bookmark mark='d'/> So whatever happens later, and however messages are delayed, no "
            "other value can ever be chosen. The proof uses no timing assumption at all; the intersection of "
            "majorities does all the work."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.5)
        self.clear_scene()

    def duel(self):
        p = load("paxos")
        head = label(r"Duelling proposers", font_size=36).to_edge(UP, buff=0.3)
        rows = []
        for P in (1, 2, 3, 4):
            a = next(r for r in p["rows"] if r["proposers"] == P and r["backoff"])
            b = next(r for r in p["rows"] if r["proposers"] == P and not r["backoff"])
            rows.append([f"{P}", f"{b['attempts']:.1f}", f"{b['time_ms']:.0f} ms", f"{a['attempts']:.1f}",
                         f"{a['time_ms']:.0f} ms"])
        tab = grid_table([r"proposers", r"ballots, \ retry at once", r"to choose", r"ballots, \ random backoff",
                          r"to choose"], rows, widths=[1.8, 2.8, 1.8, 2.8, 1.8], row_h=0.42, font_size=20,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.6).set_x(0)
        for k in range(1, 5):
            tab.cells[k][1].set_color(NO)
            tab.cells[k][2].set_color(NO)
            tab.cells[k][3].set_color(YES)
            tab.cells[k][4].set_color(YES)
        lines = VGroup(
            wrapped_label(r"A's prepare is overtaken by B's higher ballot; \ A, \ refused, \ prepares higher still, \ "
                          r"and refuses B's accepts in turn: \ a livelock FLP permits", 12.4, font_size=21,
                          color=WHITE),
            wrapped_label(r"in 400 runs each, \ with 5\% loss: \ safety held every time; \ only progress suffered", 12.4,
                          font_size=21, color=HEAD),
            wrapped_label(r"the cure is to elect a \textbf{distinguished proposer}, \ a leader \ --- \ which needs "
                          r"timeouts, \ and so partial synchrony", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.5)
        with self.voiceover(
            "Paxos is always safe, but it need not make progress. <bookmark mark='a'/> Two proposers can duel: A "
            "prepares ballot one, B prepares ballot two before A's accepts arrive, so A's accepts are refused; A "
            "prepares ballot three, which refuses B's accepts; and so on. We ran it four hundred times with one to "
            "four proposers, five percent loss, and proposers that retry the instant they are refused. With four, "
            "a value took thirty-four ballots on average. With a random pause before retrying, about four. "
            "<bookmark mark='b'/> Safety held in every run; only progress suffered, which is exactly the freedom "
            "FLP leaves. <bookmark mark='c'/> The real cure is to elect one distinguished proposer, a leader, and "
            "electing a leader needs timeouts, so it relies on the network eventually behaving."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def multi(self):
        head = label(r"Multi-Paxos: \ a log of decisions", font_size=36).to_edge(UP, buff=0.3)
        slots = VGroup(*[VGroup(Square(0.8, stroke_color=YES if i < 5 else GREY_C, stroke_width=2,
                                       fill_color=YES, fill_opacity=0.25 if i < 5 else 0),
                                label(t, font_size=21, color=YES if i < 5 else GREY_B))
                         for i, t in enumerate(["put x", "put y", "del x", "put z", "get y", "", "", ""])]).arrange(
            RIGHT, buff=0.08).next_to(head, DOWN, buff=0.6)
        sl = label(r"one Paxos instance per log slot", font_size=22, color=GREY_A).next_to(slots, DOWN, buff=0.15)
        lines = VGroup(
            wrapped_label(r"a stable leader runs phase 1 \textbf{once} for all future slots, \ then each command "
                          r"costs one round trip: \ accept, \ accepted", 12.4, font_size=25, color=WHITE),
            wrapped_label(r"in production: \ Google's Chubby lock service \ (2006) \ and Spanner \ (Part 39); \ "
                          r"Viewstamped Replication \ (1988) \ found the same protocol independently", 12.4,
                          font_size=25, color=LAM),
            wrapped_label(r"``Paxos Made Live'' \ (2007): \ the paper is a page; \ the system took years, \ with disk "
                          r"corruption, \ leases, \ snapshots and membership changes left to the implementer", 12.4,
                          font_size=25, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(sl, DOWN, buff=0.5)
        with self.voiceover(
            "One decision is not a system. Multi-Paxos runs one instance per slot of a log. "
            "<bookmark mark='a'/> A stable leader runs phase one once, for all future slots at once, and from then "
            "on each command costs a single round trip to a majority. <bookmark mark='b'/> Google built its Chubby "
            "lock service on this, and later Spanner. Brian Oki and Barbara Liskov's viewstamped replication, of "
            "1988, is essentially the same protocol, found independently. <bookmark mark='c'/> But the engineers "
            "who built Chubby wrote that the gap between the paper and a working system was enormous: disk "
            "corruption, leases, snapshots, changing the set of machines, all left as exercises. Raft was designed "
            "to close that gap."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(s) for s in slots], lag_ratio=0.1), FadeIn(sl))
            for mk, l in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (NO,)
