from __future__ import annotations

import itertools

from videos.philosophy.philosophy12.common import *  # noqa: F403


class Systems(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Machines that must agree", r"How do computers agree without common knowledge?",
                            lit=(1982, 1985), part=PART)
        with self.voiceover("Chapter six. Machines that must agree."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.byzantine()
        self.flp()
        self.quorums()
        self.nakamoto()

    def byzantine(self):
        hc = history_card(1982, r"Lamport, \ Shostak \ and Pease", r"`The Byzantine Generals Problem'", width=5.6,
                          color=HIST).to_corner(UL, buff=0.35)
        n = 4
        pos = [np.array([4.4 + 1.5 * np.cos(PI / 2 - TAU * i / n), -0.3 + 1.5 * np.sin(PI / 2 - TAU * i / n), 0])
               for i in range(n)]
        nodes = VGroup(*[Circle(radius=0.35, color=(BAD if i == 3 else AG["A"]), fill_color="#16222F",
                                fill_opacity=1).move_to(p) for i, p in enumerate(pos)]).set_z_index(3)
        tags = VGroup(*[label(t, font_size=18, color=(BAD if i == 3 else WHITE)).move_to(p) for i, (t, p) in
                        enumerate(zip([r"1", r"2", r"3", r"traitor"], pos))]).set_z_index(4)
        links = VGroup(*[Line(pos[i], pos[j], color=GREY_D, stroke_width=2) for i, j in
                         itertools.combinations(range(n), 2)])
        rows = VGroup(
            label(r"some generals may be traitors, \ sending different orders to different peers", font_size=22),
            label(r"the loyal ones must still agree, \ on a plan a loyal commander proposed", font_size=22,
                  color=GREY_A),
            label(r"possible \ iff \ more than two-thirds are loyal: \ $n \geq 3f + 1$", font_size=25, color=GOAL),
            label(r"with signed messages: \ any number of traitors", font_size=21, color=GREY_A),
            label(r"today: \ aircraft control, \ blockchains, \ replicated databases", font_size=21,
                  color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        for r in rows:
            if r.width > 6.6:
                r.width = 6.6
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([-2.7, -0.6, 0])
        with self.voiceover(
            "Computers face the generals' problem every second, and engineers have learned to live with it. "
            "<bookmark mark='a'/>In 1982 Leslie Lamport, Robert Shostak and Marshall Pease made it harder. Some of "
            "the generals may be traitors, who send different orders to different peers. <bookmark mark='b'/>The "
            "loyal generals must still agree on one plan, and if the commander is loyal, on his. <bookmark mark='c'/>"
            "They proved that, with oral messages, this is possible exactly when more than two thirds of the "
            "generals are loyal: with f traitors you need at least three f plus one generals. Four generals can "
            "tolerate one traitor; three cannot. <bookmark mark='d'/>With unforgeable signatures, any number of "
            "traitors can be tolerated. <bookmark mark='e'/>Byzantine agreement now runs inside aircraft control "
            "systems, replicated databases and blockchains."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(Create(links), FadeIn(nodes), FadeIn(tags), FadeIn(rows[0]))
            for mk, r in zip("bcde", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def flp(self):
        hc = history_card(1985, r"Fischer, \ Lynch \ and Paterson", r"`Impossibility of Distributed Consensus with "
                          r"One Faulty Process'", width=6.6, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"no clock: \ a message may take any finite time", font_size=24),
            label(r"so a slow machine looks exactly like a crashed one", font_size=24, color=GREY_A),
            label(r"FLP: \ no deterministic protocol is guaranteed to reach consensus \ if even one machine may "
                  r"crash", font_size=25, color=BAD),
            label(r"the proof: \ some state is `bivalent', \ and an adversarial scheduler can keep it so forever",
                  font_size=22, color=GREY_A),
            label(r"the escape: \ give up the guarantee that you \textit{finish}, \ never the guarantee that you "
                  r"\textit{agree}", font_size=24, color=GOAL)).arrange(DOWN, buff=0.3).move_to([0, -0.5, 0])
        with self.voiceover(
            "In 1985 Michael Fischer, Nancy Lynch and Michael Paterson proved the most famous impossibility result in "
            "distributed computing. <bookmark mark='a'/>Suppose there is no shared clock, so a message may take any "
            "finite time to arrive. <bookmark mark='b'/>Then a slow machine looks exactly like a crashed one. "
            "<bookmark mark='c'/>FLP: no deterministic protocol is guaranteed to reach consensus if even one machine "
            "may crash. <bookmark mark='d'/>The proof finds a state from which either decision is still possible, and "
            "shows that a hostile scheduler, delaying the right message at the right time, can keep the system in "
            "such states forever. <bookmark mark='e'/>Every practical system escapes the same way. It gives up the "
            "guarantee that it will finish, and never gives up the guarantee that, when it finishes, everyone agrees."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
        self.clear_scene()

    def quorums(self):
        d = load("quorum")
        head = label(r"Paxos and Raft: \ majorities always overlap", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        n = 5
        pos = [np.array([-3.6 + 1.7 * np.cos(PI / 2 - TAU * i / n), -0.4 + 1.7 * np.sin(PI / 2 - TAU * i / n), 0])
               for i in range(n)]
        nodes = VGroup(*[Circle(radius=0.34, color=AG["A"], fill_opacity=0.2).move_to(p) for p in pos])
        nums = VGroup(*[label(str(i + 1), font_size=22).move_to(p) for i, p in enumerate(pos)])
        q1 = VGroup(*[Circle(radius=0.48, color=COMMON, stroke_width=4).move_to(pos[i]) for i in (0, 1, 2)])
        q2 = VGroup(*[Circle(radius=0.58, color=LOSS, stroke_width=4).move_to(pos[i]) for i in (2, 3, 4)])
        rows = VGroup(
            label(r"a value is chosen once a majority accepts it", font_size=23),
            label(r"a later leader must hear from a majority too", font_size=23, color=GREY_A),
            label(rf"the Reasoner: \ {d['quorums']} majorities of 5, \ {d['pairs']} pairs, \ "
                  rf"{d['intersecting']} of them overlap", font_size=23, color=COMMON),
            label(r"so the new leader always learns what was chosen: \ safety, \ always", font_size=23, color=OK),
            label(r"liveness, \ when the network behaves: \ timeouts and elections", font_size=23, color=GOAL),
            label(r"Lamport, \ `The Part-Time Parliament' (1998); \ Ongaro and Ousterhout, \ Raft (2014)",
                  font_size=20, color=GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.25).move_to([2.9, -0.4, 0])
        assert d["intersecting"] == d["pairs"]
        with self.voiceover(
            "How do real systems agree, then? Leslie Lamport's Paxos algorithm, and Raft, its more teachable "
            "descendant, rest on one combinatorial fact. <bookmark mark='a'/>A value counts as chosen once a "
            "majority of machines has accepted it. <bookmark mark='b'/>Any later leader must hear from a majority "
            "before proposing anything. <bookmark mark='c'/>And any two majorities share a member. The Reasoner "
            "checks it for five machines: ten possible majorities, forty-five pairs of them, and all forty-five "
            "overlap. <bookmark mark='d'/>So a new leader always learns what an old majority chose, and nothing chosen "
            "is ever contradicted. That is safety, guaranteed. <bookmark mark='e'/>Progress, liveness, is guaranteed "
            "only when the network behaves for long enough, using timeouts and elections, just as FLP said it must "
            "be. <bookmark mark='f'/>Your bank, your search engine and your cloud storage all run on this compromise."
        ) as vo:
            self.play(FadeIn(head), FadeIn(nodes), FadeIn(nums))
            vo.wait_until("a")
            self.play(Create(q1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(q2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Indicate(nodes[2], color=OK, scale_factor=1.3), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
            vo.wait_until("e")
            self.play(FadeIn(rows[4]))
            vo.wait_until("f")
            self.play(FadeIn(rows[5]))
        self.clear_scene()

    def nakamoto(self):
        d = load("nakamoto")
        hc = history_card(2008, r"Satoshi Nakamoto", r"`Bitcoin: \ A Peer-to-Peer Electronic Cash System'",
                          width=6.0, color=HIST).to_corner(UL, buff=0.35)
        rows = VGroup(
            label(r"no fixed membership, \ no majority vote: \ the longest chain of blocks wins", font_size=22),
            label(r"a payment buried under $z$ blocks can still be undone, \ if an attacker out-computes everyone "
                  r"else", font_size=22, color=GREY_A)).arrange(DOWN, buff=0.15).move_to([0, 1.5, 0])
        hd = [label(r"blocks on top, \ $z$", font_size=21, color=P.CLAIM),
              label(r"attacker with 10\%", font_size=21, color=P.CLAIM),
              label(r"attacker with 30\%", font_size=21, color=P.CLAIM)]

        def fmt(x):
            return r"$1$" if x > 0.999 else rf"${x:.7f}$"
        trs = [[label(str(r["z"]), font_size=21), label(fmt(r["p10"]), font_size=21),
                label(fmt(r["p30"]), font_size=21)] for r in d["rows"]]
        grid = ValueGrid(hd, trs, col_w=[2.2, 3.2, 3.2], cell_h=0.44, font_size=21).move_to([0, -0.9, 0])
        foot = label(r"never zero: \ finality only in probability, \ which is all the Wall allows", font_size=24,
                     color=GOAL).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Bitcoin, in 2008, took the compromise to its limit. <bookmark mark='a'/>Nobody knows who the "
            "participants are, so there is no majority to count; instead the longest chain of blocks wins. A payment "
            "buried under z later blocks can still be reversed, if an attacker builds a longer chain in secret. "
            "<bookmark mark='b'/>The Reasoner computes Nakamoto's formula for the chance that an attacker ever "
            "catches up. With a tenth of the computing power, the chance falls from about one in five, one block "
            "deep, to about one in four thousand, six blocks deep; with three tenths, it falls much more slowly. "
            "These are the numbers printed in Nakamoto's paper. <bookmark mark='c'/>The chance is never zero. "
            "Finality is only probable, which is all the Wall allows."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(rows))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), FadeIn(grid.rule), FadeIn(grid.rows_bg),
                      LaggedStart(*[FadeIn(VGroup(*grid.cell[r])) for r in range(len(trs))], lag_ratio=0.3),
                      run_time=4)
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.clear_scene()

