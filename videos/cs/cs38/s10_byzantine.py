from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, box, grid_table, load)


class Byzantine(VoiceoverScene):
    def construct(self):
        self.card()
        self.three()
        self.om()
        self.bound()
        self.pbft_flow()
        self.pbft()

    def card(self):
        card = chapter_card(9, r"Byzantine generals", r"Can loyal machines agree when some of them lie?",
                            lit=(1980, 2019), extra=((1982, r"Lamport, Shostak \\ and Pease"),
                                                     (1999, r"Castro and Liskov: \ PBFT"),
                                                     (2019, r"Yin et al.: \ HotStuff")), part=PART)
        with self.voiceover("Chapter nine. Byzantine generals."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def _tri(self, traitor, cmd_to, relay):
        pos = {0: [0, 1.4, 0], 1: [-1.8, -1.1, 0], 2: [1.8, -1.1, 0]}
        g = VGroup()
        names = {0: r"commander", 1: r"lieutenant 1", 2: r"lieutenant 2"}
        for i, p in pos.items():
            c = NO if i == traitor else YES
            g.add(VGroup(Circle(radius=0.38, color=c, stroke_width=3).move_to(p),
                         label(names[i], font_size=15, color=c).move_to(np.array(p) + DOWN * 0.62)))
        for (a, b), v in list(cmd_to.items()) + list(relay.items()):
            pa, pb = np.array(pos[a]), np.array(pos[b])
            ar = Arrow(pa, pb, buff=0.45, color=GREY_B, stroke_width=2.2, max_tip_length_to_length_ratio=0.12)
            t = label(v, font_size=16, color=HEAD).move_to(ar.get_center() + (UP * 0.22 if a != 1 or b != 2
                                                                               else DOWN * 0.22))
            g.add(ar, t)
        return g

    def three(self):
        head = label(r"Three generals, \ one traitor", font_size=36).to_edge(UP, buff=0.3)
        left = self._tri(1, {(0, 1): r"attack", (0, 2): r"attack"}, {(1, 2): r"``he said retreat''"})
        right = self._tri(0, {(0, 1): r"retreat", (0, 2): r"attack"}, {(1, 2): r"``he said retreat''"})
        left.scale(0.85).move_to([-3.4, 0.3, 0])
        right.scale(0.85).move_to([3.4, 0.3, 0])
        ll = label(r"lieutenant 1 is the traitor", font_size=19, color=NO).next_to(left, DOWN, buff=0.2)
        rl = label(r"the commander is the traitor", font_size=19, color=NO).next_to(right, DOWN, buff=0.2)
        foot = wrapped_label(r"in both worlds lieutenant 2 hears ``attack'' from the commander and ``he said "
                             r"retreat'' from lieutenant 1: \ it cannot tell the worlds apart, \ so it must act the "
                             r"same in both", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "In 1982 Lamport, Robert Shostak and Marshall Pease asked what happens when the faulty machines may "
            "lie. They told it as Byzantine generals: a commander sends an order, attack or retreat, to "
            "lieutenants, who then tell each other what they heard. Loyal lieutenants must agree, and if the "
            "commander is loyal, they must obey it. <bookmark mark='a'/> With three generals and one traitor it "
            "is impossible. On the left the commander is loyal and orders attack, but traitorous lieutenant one "
            "tells lieutenant two that the commander said retreat. <bookmark mark='b'/> On the right the commander "
            "is the traitor: it orders lieutenant one to retreat and lieutenant two to attack, and loyal lieutenant "
            "one truthfully reports: he said retreat. <bookmark mark='c'/> Lieutenant two receives exactly the same "
            "messages in both worlds, so it must act the same in both. On the left it must attack, to obey a loyal "
            "commander, so on the right it attacks too. Now apply the same argument to lieutenant one, comparing "
            "the right-hand world with one where the commander loyally orders retreat and lieutenant two is the "
            "liar: lieutenant one must retreat. On the right, the two loyal lieutenants disagree."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left), FadeIn(ll))
            vo.wait_until("b")
            self.play(FadeIn(right), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def om(self):
        b = load("byzantine")
        head = label(r"Oral messages, \ checked exhaustively", font_size=36).to_edge(UP, buff=0.3)
        alg = wrapped_label(r"\textbf{OM($m$)}: \ the commander sends its value; \ each lieutenant acts as commander "
                            r"in OM($m - 1$) to relay what it got; \ each decides the \textbf{majority} of what it "
                            r"received directly and through the others", 12.4, font_size=21,
                            color=WHITE).next_to(head, DOWN, buff=0.4)
        rows = []
        for r in b["rows"]:
            who = ", ".join(r"commander" if t == 0 else f"L{t}" for t in r["traitors"])
            rows.append([f"{r['n']}", f"{r['m']}", who, f"{min(r['strategies'], 200000):,}", r"always" if r["agree"] else
                         r"\textbf{broken}"])
        tab = grid_table([r"generals $n$", r"rounds $m$", r"traitors", r"lying strategies tried", r"loyal agree"],
                         rows, widths=[2.0, 1.8, 2.8, 3.0, 2.0], row_h=0.42, font_size=19, mono_cols=())
        tab.next_to(alg, DOWN, buff=0.4).set_x(0)
        for k, r in enumerate(b["rows"], start=1):
            tab.cells[k][4].set_color(YES if r["agree"] else NO)
        foot = wrapped_label(r"every message a traitor sends was chosen freely, \ 0 or 1, \ in every combination \ "
                             r"(for $n = 7$ the first 200{,}000 combinations)", 12.4, font_size=19,
                             color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "With more generals it works. <bookmark mark='a'/> In the oral messages algorithm, OM of m, the "
            "commander sends its value, and every lieutenant then acts as commander in a recursive OM of m minus "
            "one, to tell the others what it heard; each lieutenant decides the majority. <bookmark mark='b'/> We "
            "checked it exhaustively, letting every message a traitor sends be zero or one in every combination. "
            "Three generals with one traitor: broken, as the argument says. Four generals with one traitor, "
            "wherever it is: always agree. Four with two traitors: broken. Seven generals, two traitors and two "
            "rounds: always agree, in every strategy we tried."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(alg))
            vo.wait_until("b")
            self.play(FadeIn(tab), FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def bound(self):
        head = label(r"$n \ge 3f + 1$", font_size=40).to_edge(UP, buff=0.3)
        steps = VGroup(
            wrapped_label(r"\textbf{Necessary.} \ Suppose $n \le 3f$ generals could tolerate $f$ traitors. \ Split "
                          r"them into three groups of at most $f$; \ let each of three generals simulate one group. \ "
                          r"That would solve the three-general problem with one traitor \ --- \ impossible.",
                          12.4, font_size=25, color=NO),
            wrapped_label(r"\textbf{Sufficient.} \ OM($f$) works for $n \ge 3f + 1$, \ but sends $O(n^{f+1})$ "
                          r"messages.", 12.4, font_size=25, color=YES),
            wrapped_label(r"\textbf{Signatures} change the picture: \ a lieutenant cannot forge what the commander "
                          r"signed, \ and agreement is possible for any $n > f$ \ (Dolev and Strong) \ --- \ the "
                          r"signatures of Part 30.", 12.4, font_size=25, color=HEAD),
            wrapped_label(r"the same bound, \ $n > 3f$, \ holds for \textit{any} asynchronous Byzantine protocol "
                          r"\ (Bracha and Toueg, 1985): \ to survive one liar, \ four machines", 12.4, font_size=25,
                          color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The bound is exact. <bookmark mark='a'/> Necessary: if three f generals or fewer could tolerate f "
            "traitors, divide them into three groups of at most f, and let each of three generals simulate a "
            "whole group. That would solve the three-general problem with one traitor, which we just proved "
            "impossible. <bookmark mark='b'/> Sufficient: OM of f works whenever there are at least three f plus "
            "one generals, though its messages grow as n to the power f plus one. <bookmark mark='c'/> Signatures "
            "change everything: a traitor cannot forge what the commander signed, and with the digital signatures "
            "of Part 30, agreement is possible with any number of traitors. <bookmark mark='d'/> In an asynchronous "
            "network, the three f plus one bound holds for every Byzantine protocol. To survive one liar you need "
            "four machines; to survive two, seven."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcd", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.4)
        self.clear_scene()

    def pbft_flow(self):
        head = label(r"PBFT's normal case, \ four replicas", font_size=36).to_edge(UP, buff=0.3)
        ys = [1.9, 0.9, -0.1, -1.1, -2.1]
        names = [r"client", r"primary 0", r"replica 1", r"replica 2", r"replica 3 \ (faulty)"]
        cols = [GREY_A, YES, DATA, DATA, NO]
        x0, x1 = -4.6, 5.6
        lines = VGroup(*[VGroup(Line([x0, y, 0], [x1, y, 0], color=GREY_D, stroke_width=1.8),
                                label(n, font_size=17, color=c).next_to([x0, y, 0], LEFT, buff=0.15))
                         for y, n, c in zip(ys, names, cols)])
        phases = [(r"request", -4.0), (r"pre-prepare", -2.2), (r"prepare", -0.2), (r"commit", 1.9),
                  (r"reply", 4.0)]
        heads = VGroup(*[label(t, font_size=18, color=HEAD).move_to([x, 2.55, 0]) for t, x in phases])

        def arr(a, b, xa, xb, c=GREY_B):
            return Arrow([xa, ys[a], 0], [xb, ys[b], 0], buff=0.05, color=c, stroke_width=1.6,
                         max_tip_length_to_length_ratio=0.08, tip_length=0.12)
        groups = VGroup(
            VGroup(arr(0, 1, -4.6, -3.2, GREY_A)),
            VGroup(*[arr(1, r, -3.2, -1.2, YES) for r in (2, 3, 4)]),
            VGroup(*[arr(a, b, -1.2, 0.8, DATA) for a in (2, 3) for b in (1, 2, 3, 4) if a != b]),
            VGroup(*[arr(a, b, 0.8, 3.0, LAM) for a in (1, 2, 3) for b in (1, 2, 3, 4) if a != b]),
            VGroup(*[arr(a, 0, 3.0, 5.0, YES) for a in (1, 2, 3)]),
        )
        notes = VGroup(
            label(r"each replica moves on once it holds $2f + 1 = 3$ matching signed messages \ (its own "
                  r"included): \ any two such quorums share a loyal replica", font_size=18, color=WHITE),
            label(r"the client accepts a result once $f + 1 = 2$ replicas report it: \ at least one is loyal",
                  font_size=18, color=YES),
        ).arrange(DOWN, buff=0.12).to_edge(DOWN, buff=0.2)
        with self.voiceover(
            "Here is PBFT deciding one request, with four replicas, one of them faulty and silent. "
            "<bookmark mark='a'/> The client sends its request to the primary. <bookmark mark='b'/> The primary "
            "assigns it a sequence number and sends a pre-prepare to every backup. <bookmark mark='c'/> Each backup "
            "that accepts it broadcasts a prepare to all the others. A replica that holds the pre-prepare and "
            "matching prepares from two f plus one replicas, itself included, knows that no loyal replica can "
            "prepare a different request with this number. <bookmark mark='d'/> Then everyone broadcasts commit, "
            "and once two f plus one commits arrive, the request is executed. That second all-to-all round makes "
            "the order survive a change of primary. <bookmark mark='e'/> Each replica replies, and the client "
            "waits for f plus one identical answers, of which at least one is from a loyal replica. Faulty replica "
            "three said nothing, and nothing was lost."
        ) as vo:
            self.play(FadeIn(head), FadeIn(lines), FadeIn(heads))
            for mk, gr in zip("abcde", groups):
                vo.wait_until(mk)
                self.play(LaggedStart(*[GrowArrow(a) for a in gr], lag_ratio=0.05), run_time=1.2)
                if mk == "c":
                    self.play(FadeIn(notes[0]))
                if mk == "e":
                    self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def pbft(self):
        b = load("byzantine")
        head = label(r"Practical Byzantine fault tolerance", font_size=36).to_edge(UP, buff=0.3)
        rows = [[f"{m['n']}", f"{m['f']}", (f"{m['om']:,}" if isinstance(m["om"], int) else
                                            rf"$\approx 10^{{{len(m['om']) - 1}}}$"), f"{m['pbft']:,}",
                 f"{m['hotstuff']:,}"] for m in b["messages"]]
        tab = grid_table([r"replicas $n$", r"liars $f$", r"OM($f$)", r"PBFT", r"HotStuff"], rows,
                         widths=[2.0, 1.6, 2.4, 1.8, 1.8], row_h=0.42, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for k in range(1, len(rows) + 1):
            tab.cells[k][2].set_color(NO)
            tab.cells[k][3].set_color(HEAD)
            tab.cells[k][4].set_color(YES)
        lines = VGroup(
            wrapped_label(r"\textbf{PBFT} \ (Castro and Liskov, 1999): \ a primary orders requests; \ pre-prepare, "
                          r"\ prepare, \ commit, \ each waiting for $2f + 1$ matching signed messages; \ a "
                          r"\textbf{view change} replaces a faulty primary. \ All-to-all: \ $O(n^2)$ per decision.",
                          12.4, font_size=20, color=HEAD),
            wrapped_label(r"\textbf{HotStuff} \ (2019): \ votes go only to the leader, \ which combines them into one "
                          r"threshold signature: \ $O(n)$ per phase, \ and a simple leader change. \ It underlies "
                          r"several blockchains.", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.4)
        with self.voiceover(
            "Practical Byzantine protocols came much later. <bookmark mark='a'/> Miguel Castro and Barbara "
            "Liskov's PBFT, in 1999, ran a file system that tolerated lying replicas at nearly the speed of an "
            "unreplicated one. A primary orders the requests, and each passes three phases, pre-prepare, prepare "
            "and commit, each waiting for two f plus one matching signed messages, so that any two such quorums "
            "share a loyal replica. If the primary misbehaves, a view change replaces it. Every replica talks to "
            "every other, so the messages grow as n squared. <bookmark mark='b'/> HotStuff, in 2019, sends votes "
            "only to the leader, which combines them into a single threshold signature: linear messages per phase. "
            "For a hundred replicas, OM would need ten to the sixty-sixth messages, PBFT about twenty thousand, "
            "HotStuff six hundred."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab))
            vo.wait_until("a")
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, LAM, box)
