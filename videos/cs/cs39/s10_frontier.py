from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs39.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.calm()
        self.causal()
        self.histories()
        self.open()

    def card(self):
        card = chapter_card(9, r"Frontier: \ how little coordination?", r"Which guarantees need machines to wait for "
                            r"each other?", lit=(2010, 2019),
                            extra=((2011, r"Mahajan, Alvisi and Dahlin: \ CAC"),
                                   (2014, r"Bailis et al.: \ invariant confluence"),
                                   (2019, r"Hellerstein and Alvaro: \ CALM")), part=PART)
        with self.voiceover("Chapter nine. Frontier: how little coordination can we get away with?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def calm(self):
        c = {r["kind"]: r for r in load("crdt")["rows"]}
        head = label(r"The CALM theorem", font_size=36).to_edge(UP, buff=0.3)
        thm = wrapped_label(r"a problem has a consistent, \ coordination-free distributed implementation \ "
                            r"\textbf{if and only if} \ it is \textbf{monotonic}: \ new information never retracts an "
                            r"earlier conclusion \ (Hellerstein 2010; \ Ameloot, Neven and Van den Bussche 2013)",
                            12.4, font_size=23, color=HEAD).next_to(head, DOWN, buff=0.45)
        rows = [[r"count likes; \ add to a set; \ OR-set", r"monotonic", f"{c['orset']['converged']:,} / 1{{,}}000",
                 r"no"],
                [r"remove from a plain set", r"not monotonic", f"{c['naive-set']['converged']} / 1{{,}}000", r"yes"],
                [r"usernames must be unique", r"not monotonic", r"---", r"yes, \ for new names"],
                [r"balance stays $\ge 0$", r"not monotonic", r"---", r"only for withdrawals"]]
        tab = grid_table([r"task", r"monotonic?", r"replicas converged \ (ours)", r"needs coordination?"], rows,
                         widths=[4.4, 2.4, 3.2, 2.6], row_h=0.48, font_size=20, mono_cols=())
        tab.next_to(thm, DOWN, buff=0.4).set_x(0)
        tab.cells[1][2].set_color(YES)
        tab.cells[2][2].set_color(NO)
        for k in (2, 3, 4):
            tab.cells[k][1].set_color(NO)
        tab.cells[1][1].set_color(YES)
        foot = wrapped_label(r"\textbf{invariant confluence} \ (Bailis et al., 2014) \ asks the same of each invariant "
                             r"of an application: \ in TPC-C, \ most invariants need no coordination at all", 12.4,
                             font_size=21, color=LAM).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Every guarantee in this part costs coordination: replicas waiting for each other, across a datacenter "
            "or an ocean. So which problems actually need it? <bookmark mark='a'/> Joseph Hellerstein conjectured "
            "an answer in 2010, and Tom Ameloot and his colleagues proved it: a problem can be solved consistently "
            "without coordination if and only if it is monotonic, meaning new information never retracts an "
            "earlier conclusion. <bookmark mark='b'/> Counting likes and adding to a set are monotonic, and our "
            "set replicas converged in all thousand runs. Removing from a plain set is not, and converged in only "
            "fifteen. Unique usernames and non-negative balances are not monotonic either: some operations must wait. "
            "<bookmark mark='c'/> Peter Bailis turned this into an engineering tool, invariant confluence: check "
            "each invariant of an application separately. In the standard TPC-C benchmark, most of them need no "
            "coordination at all, and a database that knows it can run them many times faster."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(thm))
            vo.wait_until("b")
            self.play(FadeIn(tab))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def causal(self):
        head = label(r"The strongest model that stays available", font_size=36).to_edge(UP, buff=0.3)
        ladder = VGroup(*[label(t, font_size=24, color=c) for t, c in (
            (r"linearizable", NO), (r"sequential", NO), (r"causal \ (real-time causal)", YES),
            (r"read your writes, \ monotonic reads", YES), (r"eventual", YES))]).arrange(DOWN, buff=0.36)
        ladder.move_to([-3.6, -0.4, 0])
        cut = DashedLine(ladder[1].get_bottom() + DOWN * 0.18 + LEFT * 2.2, ladder[1].get_bottom() + DOWN * 0.18 +
                         RIGHT * 2.2, color=HEAD)
        cl = label(r"CAP's line", font_size=18, color=HEAD).next_to(cut, RIGHT, buff=0.15)
        notes = VGroup(
            wrapped_label(r"\textbf{CAC} \ (Mahajan, Alvisi and Dahlin, 2011): \ no consistency model stronger than "
                          r"real-time causal can be both always available and convergent", 6.0, font_size=20,
                          color=YES),
            wrapped_label(r"causal consistency is achievable at geo-scale: \ COPS \ (2011), \ Eiger, \ and "
                          r"transactional causal consistency", 6.0, font_size=20, color=LAM),
            wrapped_label(r"open: \ the exact cost, \ in metadata per write, \ of tracking causality among millions "
                          r"of clients; \ the known lower bounds and the systems are far apart", 6.0, font_size=20,
                          color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).move_to([3.0, -0.4, 0])
        with self.voiceover(
            "CAP draws one line through the hierarchy of Chapter two: linearizable systems cannot stay available "
            "during a partition. <bookmark mark='a'/> But where exactly is the line? In 2011 Prince Mahajan, "
            "Lorenzo Alvisi and Mike Dahlin proved that no model stronger than a form of causal consistency can be "
            "both always available and convergent. Causality, Lamport's happened-before from Part 38, is the most "
            "an always-available system can promise. <bookmark mark='b'/> And it can be had at global scale: "
            "systems like COPS and Eiger give causal consistency across datacenters, even with transactions. "
            "<bookmark mark='c'/> What remains open is its price: how much metadata each write must carry to track "
            "causality among millions of clients. The lower bounds and the best systems are still far apart."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ladder), Create(cut), FadeIn(cl))
            for mk, n in zip("abc", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Coordination-avoiding programming}: \ languages \ (Bloom, \ Hydro) \ that "
                          r"find the monotonic parts of a program, \ and place coordination only where CALM says it "
                          r"is needed.", 12.4, font_size=25, color=WHITE),
            wrapped_label(r"2. \ \textbf{Sequence CRDTs}: \ collaborative text without interleaving anomalies, \ in "
                          r"bounded metadata; \ local-first software \ (Kleppmann et al., 2019).", 12.4, font_size=25,
                          color=YES),
            wrapped_label(r"3. \ \textbf{Metastability}: \ predicting which systems have a stable bad state, \ and "
                          r"how large a trigger tips them into it, \ before it happens in production.", 12.4,
                          font_size=25, color=NO),
            wrapped_label(r"4. \ \textbf{Tail-tolerant design}: \ hedging, \ retries and admission control "
                          r"interact; \ their combined effect on the tail has little theory.", 12.4, font_size=25,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ a retry policy for our simulator that "
                             r"provably recovers from any finite spike, \ yet keeps the tail benefit of hedging", 12.4,
                             font_size=24, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Where the field stands. <bookmark mark='a'/> Programming languages such as Bloom and Hydro try to find "
            "the monotonic parts of a program automatically, and to insert coordination only where the CALM "
            "theorem says it is unavoidable. <bookmark mark='b'/> Sequence CRDTs for collaborative text still "
            "struggle to avoid interleaving anomalies with bounded metadata, which matters for local-first "
            "software, where your data lives on your devices first. <bookmark mark='c'/> Metastable failures are "
            "found after they happen; predicting which systems have a stable bad state, and how big a trigger "
            "tips them over, is open. <bookmark mark='d'/> And hedging, retries and admission control interact in "
            "ways that have very little theory. <bookmark mark='e'/> This part's research problem sits right "
            "there: design a retry policy for our simulator that provably recovers from any finite spike, while "
            "keeping the tail benefit that hedging gave us."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()

    def histories(self):
        h = load("history")
        st, ok = h["stale replica"], h["serializable"]
        ex = st["example"]
        head = label(r"Checking what clients saw", font_size=36).to_edge(UP, buff=0.3)

        def opstr(op):
            if op[0] == "a":
                return rf"append {op[2]} to key {op[1]}"
            return rf"read key {op[1]}: \ [\dots, {', '.join(str(v) for v in op[2])}]"
        boxes = VGroup()
        for i, e in enumerate(ex[:2]):
            body = VGroup(label(rf"T{e['txn']}", font_size=26, color=HEAD if i == 0 else LAM),
                          *[label(opstr(op), font_size=21, color=WHITE) for op in e["ops"]]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1)
            fr = SurroundingRectangle(body, buff=0.15, color=GREY_C, corner_radius=0.1)
            boxes.add(VGroup(fr, body))
        boxes.arrange(RIGHT, buff=3.4).move_to([0, 1.4, 0])
        a1 = CurvedArrow(boxes[0].get_right() + UP * 0.25, boxes[1].get_left() + UP * 0.25, angle=-0.5, color=HEAD)
        a2 = CurvedArrow(boxes[1].get_left() + DOWN * 0.25, boxes[0].get_right() + DOWN * 0.25, angle=-0.5, color=NO)
        l1 = label(r"ww: \ 351 follows 350", font_size=21, color=HEAD).next_to(a1, UP, buff=0.1)
        l2 = label(r"rw: \ read key 4 without 350", font_size=21, color=NO).next_to(a2, DOWN, buff=0.1)
        rows = [[r"one copy, \ serial", f"{ok['txns']:,}", f"{ok['cyclic_components']}", f"{ok['txns_in_cycles']}"],
                [r"reads from a lagging replica", f"{st['txns']:,}", f"{st['cyclic_components']}",
                 f"{st['txns_in_cycles']}"]]
        tab = grid_table([r"store", r"transactions", r"cycles found", r"transactions in cycles"], rows,
                         widths=[4.6, 2.4, 1.6, 3.4], row_h=0.48, font_size=21, mono_cols=())
        tab.move_to([0, -1.35, 0])
        tab.cells[1][2].set_color(YES)
        tab.cells[2][2].set_color(NO)
        foot = wrapped_label(r"checking linearizability or serializability of an arbitrary history is NP-complete "
                             r"\ (Gibbons and Korach, 1997; \ Papadimitriou, 1979); \ unique values appended to "
                             r"lists make each read reveal its whole past, \ and the check becomes a cycle search: \ "
                             r"Elle \ (Kingsbury and Alvaro, 2020)", 12.4, font_size=19,
                             color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How would you know whether a database actually delivers what it promises? Watch only what clients "
            "saw, and look for a contradiction. In general this is hard: deciding whether a history is "
            "linearizable, or serializable, is NP-complete. <bookmark mark='a'/> Kyle Kingsbury and Peter Alvaro's "
            "Elle, in 2020, makes it easy by choosing the test. Every transaction appends unique numbers to lists "
            "and reads whole lists, so every read reveals exactly which writes came before it, and in what order. "
            "<bookmark mark='b'/> From that, Elle draws an edge whenever one transaction must have come before "
            "another. Here transaction three sixty appended three fifty to key four, and three sixty-two appended "
            "three fifty-one right after it, so three sixty came first. But three sixty-two had read key four "
            "without three fifty, so it came first. A cycle: no serial order explains what the clients saw. "
            "<bookmark mark='c'/> We ran two thousand transactions on two stores. On a single serial copy, no "
            "cycles. On a store that reads from a lagging replica, a hundred and forty-three of them, involving "
            "eight hundred and thirty-five transactions. Elle has found anomalies like these in a long list of "
            "production databases."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes))
            vo.wait_until("b")
            self.play(Create(a1), FadeIn(l1))
            self.play(Create(a2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(tab), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA,)
