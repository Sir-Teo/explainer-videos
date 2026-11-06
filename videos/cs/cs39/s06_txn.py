from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, box, grid_table, load, seq_diagram)


class Txn(VoiceoverScene):
    def construct(self):
        self.card()
        self.two_pc()
        self.blocking()
        self.spanner()
        self.hlc()
        self.coordination()

    def card(self):
        card = chapter_card(5, r"Transactions across machines", r"How do machines commit together?",
                            lit=(1978, 2012), extra=((1978, r"Gray: \ two-phase commit"),
                                                     (1981, r"Skeen: \ three-phase commit"),
                                                     (2012, r"Corbett et al.: \ Spanner")), part=PART)
        with self.voiceover("Chapter five. Transactions across machines."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def two_pc(self):
        head = label(r"Two-phase commit", font_size=36).to_edge(UP, buff=0.3)
        ev = [(0.0, 1.0, r"PREPARE", True, DATA), (1.0, 2.0, r"YES \ (locks held)", False, YES),
              (2.3, 3.3, r"COMMIT", True, DATA), (3.3, 4.3, r"done", False, YES)]
        sd = seq_diagram(ev, t_max=4.8, height=4.6, gap=5.0, names=(r"coordinator", r"participant")).move_to(
            [-3.2, -0.5, 0])
        log1 = label(r"writes COMMIT \\ to its log", font_size=16, color=HEAD).next_to(sd[0], LEFT, buff=0.1).shift(
            DOWN * 0.2)
        notes = VGroup(
            wrapped_label(r"\textbf{phase 1}: \ every participant makes its part durable and votes; \ a YES is a "
                          r"promise to commit if told to, \ even after a crash", 5.6, font_size=20, color=WHITE),
            wrapped_label(r"\textbf{phase 2}: \ all YES $\Rightarrow$ COMMIT, \ any NO $\Rightarrow$ ABORT; \ the "
                          r"decision is final once the coordinator logs it", 5.6, font_size=20, color=YES),
            wrapped_label(r"it is \textbf{atomic commitment}, \ not consensus: \ any single participant can veto", 5.6,
                          font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.5, -0.3, 0])
        with self.voiceover(
            "A transaction that touches data on several machines must commit everywhere or nowhere. Jim Gray's "
            "two-phase commit, from 1978, does it with a coordinator. <bookmark mark='a'/> In phase one the "
            "coordinator asks every participant to prepare. Each one makes its part of the transaction durable, "
            "holds its locks, and votes. A yes vote is a promise: I will commit if you tell me to, even if I crash "
            "and restart. <bookmark mark='b'/> If every vote is yes, the coordinator writes commit to its own log, "
            "which is the moment of decision, and tells everyone; any no means abort. <bookmark mark='c'/> Unlike "
            "consensus, any single participant can veto the outcome. That is what makes it atomic commitment."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd[:4]))
            vo.wait_until("a")
            self.play(FadeIn(sd.arrows[0]), FadeIn(sd.arrows[1]), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(log1), FadeIn(sd.arrows[2]), FadeIn(sd.arrows[3]), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def blocking(self):
        t = load("txn")["two_pc"]
        head = label(r"Where two-phase commit blocks", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{e[0]:.3f} s" if e[0] < 1 else f"{e[0]:.1f} s", e[1], e[2]] for e in t["events"]]
        tab = grid_table([r"time", r"who", r"what"], rows, widths=[1.6, 2.4, 6.4], row_h=0.38, font_size=19,
                         mono_cols=())
        tab.next_to(head, DOWN, buff=0.45).set_x(0)
        for k, e in enumerate(t["events"], start=1):
            if e[2] == "crash":
                for j in range(3):
                    tab.cells[k][j].set_color(NO)
        lines = VGroup(
            wrapped_label(rf"the coordinator crashes after deciding, \ before telling anyone: \ the participants "
                          rf"voted YES, \ so they may not abort, \ and do not know the decision: \ "
                          rf"\textbf{{{t['blocked_seconds']:.0f} s}} holding their locks", 12.4, font_size=21, color=NO),
            wrapped_label(r"\textbf{three-phase commit} \ (Skeen, 1981) \ adds a round so participants can decide "
                          r"among themselves, \ but only if the network is synchronous; \ in practice, \ run 2PC's "
                          r"coordinator as a Paxos or Raft group \ (Spanner)", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.35)
        with self.voiceover(
            "The weakness is one moment. <bookmark mark='a'/> Here the coordinator crashes just after deciding to "
            "commit and before telling anyone. The participants voted yes, so they are not allowed to abort; they do "
            "not know the decision, so they cannot commit. They wait, holding their locks, for thirty-one seconds, "
            "until the coordinator recovers and reads its log. No other transaction can touch those rows in the "
            "meantime. <bookmark mark='b'/> Three-phase commit adds a round so participants can finish on their "
            "own, but it is safe only if the network is synchronous. Real systems do something simpler: they make "
            "the coordinator itself a replicated state machine, a Paxos or Raft group, so it never really goes "
            "away."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def spanner(self):
        s = load("txn")["spanner"]
        head = label(r"Spanner: \ consistency from clocks", font_size=36).to_edge(UP, buff=0.3)
        e = s[2]

        def X(t):
            return -6.2 + (t + 6) * 0.5
        axis = Arrow([X(-6), -0.6, 0], [X(19), -0.6, 0], buff=0, color=GREY_D, stroke_width=2,
                     max_tip_length_to_length_ratio=0.02)
        ticks = VGroup(*[label(f"{t} ms", font_size=15, color=GREY_B).move_to([X(t), -0.9, 0])
                         for t in range(-4, 19, 4)])
        lock_t = e["timestamp_ms"] - e["epsilon_ms"]
        interval = Rectangle(width=2 * e["epsilon_ms"] * 0.5, height=0.4, stroke_color=HEAD, fill_color=HEAD,
                             fill_opacity=0.25).move_to([X(lock_t), 0.1, 0])
        il = label(r"TT.now() at true time 2 ms: \ $[t - \varepsilon, \ t + \varepsilon]$", font_size=18,
                   color=HEAD).next_to(interval, UP, buff=0.1)
        stamp = DashedLine([X(e["timestamp_ms"]), 1.4, 0], [X(e["timestamp_ms"]), -0.6, 0], color=YES)
        sl = label(rf"timestamp $s$ = latest = {e['timestamp_ms']:.0f} ms", font_size=17, color=YES).next_to(
            stamp, UP, buff=0.05).shift(RIGHT * 1.2)
        wait = Rectangle(width=e["commit_wait_ms"] * 0.5, height=0.3, stroke_width=0, fill_color=NO,
                         fill_opacity=0.6).move_to([X(lock_t + e["commit_wait_ms"] / 2), -0.35, 0])
        wl = label(rf"commit wait \ $\approx 2\varepsilon$ = {e['commit_wait_ms']:.0f} ms", font_size=17,
                   color=NO).next_to(wait, DOWN, buff=0.5)
        rows = [[f"{x['epsilon_ms']:.0f} ms", f"{x['commit_wait_ms']:.0f} ms", f"{x['paxos_done_ms']:.0f} ms",
                 f"{x['release_ms']:.0f} ms"] for x in s]
        tab = grid_table([r"$\varepsilon$", r"commit wait", r"Paxos done", r"locks released"], rows,
                         widths=[1.4, 2.0, 2.0, 2.4], row_h=0.38, font_size=18, mono_cols=())
        tab.to_edge(DOWN, buff=0.35).set_x(-1.0)
        side = wrapped_label(r"GPS receivers and atomic clocks in every datacenter keep $\varepsilon$ near "
                             r"\ 1 to 7 ms; \ waiting out the uncertainty makes timestamp order match real time: \ "
                             r"\textbf{external consistency}", 3.8, font_size=17, color=WHITE).move_to([4.8, -2.4, 0])
        with self.voiceover(
            "Google's Spanner, in 2012, ran transactions across datacenters on several continents and made them "
            "linearizable, using clocks. <bookmark mark='a'/> Its TrueTime interface does not return a time; it "
            "returns an interval guaranteed to contain the true time, a few milliseconds wide, kept narrow by GPS "
            "receivers and atomic clocks in every datacenter. <bookmark mark='b'/> To commit, a coordinator picks "
            "as timestamp the latest possible current time, and then waits until the earliest possible current time "
            "has passed it, about two epsilon, before releasing locks and reporting success. <bookmark mark='c'/> "
            "After that wait, any transaction that starts later in real time is certain to get a larger timestamp, "
            "so timestamp order is real-time order. The wait overlaps the Paxos round that replicates the commit, "
            "so with an epsilon of one or four milliseconds it costs nothing; with seven it adds six."
        ) as vo:
            self.play(FadeIn(head), GrowArrow(axis), FadeIn(ticks))
            vo.wait_until("a")
            self.play(FadeIn(interval), FadeIn(il))
            vo.wait_until("b")
            self.play(Create(stamp), FadeIn(sl), FadeIn(wait), FadeIn(wl))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    def coordination(self):
        head = label(r"Coordination services, \ and fencing", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{Chubby} \ (Google, 2006) \ and \textbf{ZooKeeper} \ (Yahoo!, 2010): \ a small "
                          r"replicated store of locks, \ leader elections and configuration, \ so that everything "
                          r"else need not run consensus itself", 12.4, font_size=22, color=WHITE),
            wrapped_label(r"a lock is really a \textbf{lease}: \ it expires if the holder stops renewing it", 12.4,
                          font_size=22, color=HEAD),
            wrapped_label(r"a holder paused past its lease \ (garbage collection, \ a swapped-out page) \ wakes up "
                          r"and writes, \ unaware: \ two writers", 12.4, font_size=22, color=NO),
            wrapped_label(r"\textbf{fencing tokens}: \ every grant carries a number that only grows; \ the storage "
                          r"rejects writes with a number older than one it has seen", 12.4, font_size=22, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "Most systems do not run consensus themselves. <bookmark mark='a'/> They ask a small coordination "
            "service, Google's Chubby or Apache ZooKeeper, built on Paxos-like protocols, to hold their locks, elect "
            "their leaders and store their configuration. <bookmark mark='b'/> A lock in such a service is really a "
            "lease: it expires unless the holder keeps renewing it, so a crashed holder cannot block everyone for "
            "ever. <bookmark mark='c'/> But a holder that is merely paused, by a long garbage collection, can wake "
            "up after its lease has expired and been granted to someone else, and write, unaware. "
            "<bookmark mark='d'/> The fix is a fencing token: every grant carries a number that only increases, and "
            "the storage refuses any write carrying a smaller number than one it has already seen."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def hlc(self):
        h = load("hlc")
        sc = h["schemes"]
        head = label(r"Without atomic clocks: \ hybrid logical clocks", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"physical clock", f"{sc['physical']['violations'] * 100:.1f}\\%",
                 rf"$\le$ {sc['physical']['max_drift_ms']:.1f} ms"],
                [r"Lamport clock", f"{sc['lamport']['violations'] * 100:.0f}\\%",
                 rf"unrelated \ (reached {sc['lamport']['final_value']:,} after 10 s)"],
                [r"hybrid logical clock", f"{sc['hlc']['violations'] * 100:.0f}\\%",
                 rf"$\le$ {sc['hlc']['max_drift_ms']:.1f} ms, \ counter $\le$ {h['max_c']}"]]
        tab = grid_table([r"timestamp", r"receives stamped before their send", r"distance from true time"], rows,
                         widths=[3.2, 4.4, 4.6], row_h=0.5, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        tab.cells[1][1].set_color(NO)
        tab.cells[2][2].set_color(NO)
        tab.cells[3][1].set_color(YES)
        tab.cells[3][2].set_color(YES)
        rule = VGroup(
            MathTex(r"l \leftarrow \max(l,\ l_{\text{msg}},\ \text{pt})", font_size=32, color=HEAD),
            label(r"if $l$ did not change, \ $c \leftarrow c + 1$, \ else $c \leftarrow 0$; \ order by $(l, c)$",
                  font_size=21, color=HEAD),
        ).arrange(DOWN, buff=0.2).next_to(tab, DOWN, buff=0.45)
        foot = wrapped_label(rf"four processes, \ clocks up to {h['eps_ms']:.0f} ms apart, \ {h['messages']:,} "
                             r"messages; \ CockroachDB and MongoDB stamp transactions this way, \ and restart a read "
                             r"that meets a value inside its clock uncertainty", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Most of us do not have atomic clocks in every building. <bookmark mark='a'/> We ran four processes "
            "whose clocks disagree by up to five milliseconds, sending each other messages that take up to three. "
            "Stamped with their physical clocks, one message in five appears to arrive before it was sent. "
            "Lamport's clock never gets causality wrong, but its numbers have nothing to do with time: after ten "
            "seconds it reads six thousand. <bookmark mark='b'/> Sandeep Kulkarni and his colleagues combined the "
            "two in 2014. A hybrid logical clock keeps the largest physical time it has heard of, from its own "
            "clock or from any message, plus a small counter to break ties. <bookmark mark='c'/> It never gets "
            "causality wrong, it never strays from true time by more than the clocks' own disagreement, and the "
            "counter stayed below eight. CockroachDB and MongoDB stamp their transactions this way. Without "
            "Spanner's guaranteed bound they cannot simply wait it out, so a read that meets a value within its "
            "clock uncertainty restarts at a later timestamp instead."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule), FadeIn(VGroup(*tab.cells[1])),
                      FadeIn(VGroup(*tab.cells[2])))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[3])), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (LAM, box)
