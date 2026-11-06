from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, LAM, NO, PART, ROLEC, YES, box, grid_table, load)


def log_row(entries, cell=0.55, committed=0, font=16):
    """entries: list of terms; returns a row of squares labelled by term."""
    cols = [DATA, LAM, KERN, YES, HEAD, NO]
    g = VGroup()
    for i, t in enumerate(entries):
        c = cols[(t - 1) % len(cols)]
        sq = VGroup(Square(cell, stroke_color=c, stroke_width=1.8, fill_color=c,
                           fill_opacity=0.45 if i < committed else 0.15), label(str(t), font_size=font, color=c))
        g.add(sq)
    g.arrange(RIGHT, buff=0.04)
    return g


class Raft(VoiceoverScene):
    def construct(self):
        self.card()
        self.roles()
        self.elections()
        self.replication()
        self.commit_rule()

    def card(self):
        card = chapter_card(7, r"Raft", r"Can consensus be made understandable?", lit=(2014, 2014),
                            extra=((2014, r"Ongaro and Ousterhout: \ In Search of an \\ Understandable Consensus "
                                          r"Algorithm"),), part=PART)
        with self.voiceover("Chapter seven. Raft."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def roles(self):
        head = label(r"Terms, \ and three roles", font_size=36).to_edge(UP, buff=0.3)
        f = box(2.4, 0.8, r"follower", ROLEC["follower"], font_size=22).move_to([-4.2, 0.6, 0])
        c = box(2.4, 0.8, r"candidate", ROLEC["candidate"], font_size=22).move_to([0, 0.6, 0])
        ld = box(2.4, 0.8, r"leader", ROLEC["leader"], font_size=22).move_to([4.2, 0.6, 0])
        a1 = CurvedArrow(f.get_top(), c.get_top(), angle=-0.8, color=GREY_B)
        a2 = CurvedArrow(c.get_top(), ld.get_top(), angle=-0.8, color=GREY_B)
        a3 = CurvedArrow(ld.get_bottom(), f.get_bottom(), angle=-0.6, color=GREY_B)
        l1 = label(r"no word from a leader: \ time out", font_size=17, color=GREY_A).next_to(a1, UP, buff=0.05)
        l2 = label(r"votes from a majority", font_size=17, color=GREY_A).next_to(a2, UP, buff=0.05)
        l3 = label(r"sees a higher term", font_size=17, color=GREY_A).next_to(a3, DOWN, buff=0.05)
        lines = VGroup(
            wrapped_label(r"time is divided into \textbf{terms}, \ numbered; \ each has at most one leader, \ "
                          r"elected by a majority; \ every message carries its sender's term", 12.4, font_size=21,
                          color=WHITE),
            wrapped_label(r"Raft's design goal was understandability: \ in a study, \ students scored higher on Raft "
                          r"questions than on Paxos questions \ (Ongaro and Ousterhout, 2014)", 12.4, font_size=20,
                          color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Diego Ongaro and John Ousterhout designed Raft in 2014 with one explicit goal: to be understood. It "
            "decomposes consensus into leader election, log replication and safety. <bookmark mark='a'/> Every "
            "server is a follower, a candidate or a leader. A follower that hears nothing from a leader for a while "
            "times out and becomes a candidate; a candidate that gathers votes from a majority becomes leader; "
            "anyone who sees a message from a higher term steps down to follower. <bookmark mark='b'/> Time is cut "
            "into numbered terms, each with at most one leader, and every message carries its sender's term, which "
            "plays the role of Paxos's ballot. <bookmark mark='c'/> In a study with students at Stanford and "
            "Berkeley, Raft was indeed easier to learn than Paxos."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(f), FadeIn(c), FadeIn(ld))
            self.play(Create(a1), FadeIn(l1), Create(a2), FadeIn(l2), Create(a3), FadeIn(l3))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def elections(self):
        e = load("election")
        head = label(r"Elections, \ and why timeouts are random", font_size=36).to_edge(UP, buff=0.3)
        rules = VGroup(
            wrapped_label(r"a candidate increments the term, \ votes for itself, \ asks everyone; \ each server grants "
                          r"\textbf{one} vote per term, \ first come, \ and only to a candidate whose log is at least "
                          r"as up to date as its own", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"if several time out together, \ the vote splits, \ no one wins, \ and all time out "
                          r"again: \ FLP's endless bivalence, \ in practice", 12.4, font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(head, DOWN, buff=0.4)
        rows = []
        for r in e["rows"]:
            sp = r["spread"]
            rows.append([rf"$[T, {1 + sp:g}T]$", f"{r['no_leader']} of {r['runs']}",
                         f"{r['mean_terms']:.1f}" if r["mean_terms"] else r"--",
                         f"{r['median_ms']:.0f} ms" if r["median_ms"] else r"--",
                         f"{r['p99_ms']:.0f} ms" if r["p99_ms"] else r"--"])
        tab = grid_table([r"timeout", r"never elected", r"terms needed", r"median", r"99th pct"], rows,
                         widths=[2.0, 2.6, 2.2, 1.8, 1.8], row_h=0.4, font_size=20, mono_cols=())
        tab.next_to(rules, DOWN, buff=0.45).set_x(0)
        for k, r in enumerate(e["rows"], start=1):
            tab.cells[k][1].set_color(NO if r["no_leader"] else YES)
        foot = label(r"5 servers, \ $T$ = 150 ms, \ delays 2 to 12 ms: \ the leader crashes, \ how long until a new "
                     r"one?", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "An election. <bookmark mark='a'/> The candidate increments the term, votes for itself, and asks "
            "everyone else. Each server grants one vote per term, to the first candidate that asks, and only if "
            "that candidate's log is at least as up to date as its own; we will see why. "
            "<bookmark mark='b'/> If two servers time out at the same moment, they split the votes, nobody wins, "
            "and they time out together again: FLP's endless indecision, in practice. Raft's remedy is to "
            "randomize the timeouts. <bookmark mark='c'/> We crashed the leader of five servers three hundred times "
            "and timed the election. With identical timeouts, nobody was ever elected, not even at the start. With "
            "two percent of randomness, most runs never elected a leader either, and the rest needed ten terms. "
            "With timeouts spread over a factor of two, as the paper recommends, a new leader took one term and "
            "under two hundred milliseconds."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(rules[0]))
            vo.wait_until("b")
            self.play(FadeIn(rules[1]))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def replication(self):
        head = label(r"Log replication", font_size=36).to_edge(UP, buff=0.3)
        L = log_row([1, 1, 1, 2, 3, 3, 3], committed=5)
        F1 = log_row([1, 1, 1, 2, 3, 3], committed=5)
        F2 = log_row([1, 1, 1, 2], committed=4)
        F3 = log_row([1, 1, 1, 2, 2, 2], committed=4)
        rows = VGroup()
        for name, lg, col in ((r"leader, \ term 3", L, YES), (r"follower", F1, DATA), (r"follower", F2, DATA),
                              (r"follower", F3, KERN)):
            rows.add(VGroup(label(name, font_size=18, color=col), lg).arrange(RIGHT, buff=0.4))
        for k, r in enumerate(rows):
            r[1].move_to([0, 1.7 - k * 0.75, 0]).align_to([-2.4, 0, 0], LEFT)
            r[0].next_to(r[1], LEFT, buff=0.35)
        notes = VGroup(
            wrapped_label(r"\textbf{AppendEntries} carries new entries and the index and term of the entry just "
                          r"before them; \ a follower whose log disagrees there \textbf{refuses}, \ and the leader "
                          r"backs up until they agree, \ then overwrites the rest", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"\textbf{Log matching}: \ if two logs have an entry with the same index and term, \ they "
                          r"are identical up to it \ (by induction: \ each append checks its predecessor)", 12.4,
                          font_size=20, color=YES),
            wrapped_label(r"the third follower's two uncommitted term-2 entries, \ from a deposed leader, \ are "
                          r"replaced", 12.4, font_size=20, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Once elected, the leader takes commands from clients, appends them to its log, and sends them to the "
            "followers. Each square here is a log entry, labelled with the term in which a leader created it. "
            "<bookmark mark='a'/> Each AppendEntries message carries the new entries and the index and term of "
            "the entry just before them. A follower whose log does not hold that entry refuses, and the leader "
            "backs up one entry and tries again, until it finds where they agree; then the follower discards "
            "anything after that point and takes the leader's entries. <bookmark mark='b'/> This gives the log "
            "matching property: if two logs hold an entry with the same index and term, they are identical up to "
            "that point, by induction, since every append checked its predecessor. <bookmark mark='c'/> The third "
            "follower here holds two entries from term two that a deposed leader never managed to commit. They "
            "will be overwritten."
        ) as vo:
            self.play(FadeIn(head), LaggedStart(*[FadeIn(r) for r in rows], lag_ratio=0.2))
            for mk, n in zip("abc", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n))
        self.wait(0.4)
        self.clear_scene()

    def commit_rule(self):
        r = load("raft")
        bug = r["commit-old-term"]
        head = label(r"The commit rule, \ and the subtle part", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"an entry is \textbf{committed} once the leader that created it has it on a majority; \ "
                          r"committed entries are applied to the state machine", 12.4, font_size=23, color=WHITE),
            wrapped_label(r"\textbf{the election restriction} \ (vote only for logs at least as up to date) \ plus "
                          r"majority intersection gives \textbf{leader completeness}: \ every committed entry is in "
                          r"every later leader's log", 12.4, font_size=23, color=YES),
            wrapped_label(r"\textbf{but}: \ a new leader must not count replicas of an \textit{older} term's entry to "
                          r"commit it; \ such an entry can be on a majority and still be overwritten \ (the paper's "
                          r"Figure 8). \ It commits them only indirectly, \ by committing an entry of its own term "
                          r"after them.", 12.4, font_size=23, color=NO),
            wrapped_label(rf"we planted that bug: \ in 1{{,}}000 random fault schedules, \ "
                          rf"{bug['violating_runs']} exposed it \ (schedule {bug['first']['seed']}: \ "
                          rf"``{bug['first']['violation'][1]}'')", 12.4, font_size=22, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.6)
        with self.voiceover(
            "When is an entry safe? <bookmark mark='a'/> An entry is committed once the leader that created it "
            "has stored it on a majority of servers, and committed entries are applied, in order, to each "
            "server's state machine. <bookmark mark='b'/> Commitment must survive changes of leader. That is the "
            "job of the voting restriction: a server votes only for a candidate whose log is at least as up to "
            "date, and since a winner needs a majority of votes, and the entry is on a majority, some voter holds "
            "it, so the winner must too. Every committed entry is in every later leader's log. "
            "<bookmark mark='c'/> There is one subtle trap, the paper's Figure 8. A leader must not commit an entry "
            "from an earlier term just by counting replicas: such an entry can sit on a majority and still be "
            "overwritten by a later leader. It commits old entries only indirectly, by committing one of its own "
            "term after them. <bookmark mark='d'/> We planted exactly that bug in our Raft. In a thousand random "
            "fault schedules, it was exposed once: a later leader lacked an entry that had been committed. The bug "
            "is real, and random testing barely finds it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.5)
        self.clear_scene()


_ = (HEAD, LAM)
