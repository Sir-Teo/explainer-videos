from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, axes, grid_table, load)


class Flp(VoiceoverScene):
    def construct(self):
        self.card()
        self.valency()
        self.explored()
        self.proof()
        self.around()
        self.benor()

    def card(self):
        card = chapter_card(5, r"FLP", r"Why can't asynchronous machines guarantee agreement?", lit=(1983, 1985),
                            extra=((1983, r"Ben-Or: \ randomized consensus"),
                                   (1985, r"Fischer, Lynch and Paterson")), part=PART)
        with self.voiceover("Chapter five. FLP."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def valency(self):
        head = label(r"Valency", font_size=36).to_edge(UP, buff=0.3)
        defs = VGroup(
            wrapped_label(r"a \textbf{configuration}: \ every process's state, \ and every message in flight", 12.4,
                          font_size=22, color=WHITE),
            wrapped_label(r"it is \textbf{0-valent} if every continuation decides 0; \ \textbf{1-valent} if every "
                          r"one decides 1; \ \textbf{bivalent} if both are still reachable", 12.4, font_size=22,
                          color=HEAD),
            wrapped_label(r"a protocol decides when it moves from bivalent to univalent; \ FLP shows an adversary "
                          r"scheduler can keep it bivalent for ever", 12.4, font_size=22, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.5)
        tree = VGroup()
        root = Circle(radius=0.32, color=HEAD, fill_color=HEAD, fill_opacity=0.3).move_to([0, -1.2, 0])
        l = Circle(radius=0.28, color=DATA, fill_color=DATA, fill_opacity=0.3).move_to([-2.2, -2.6, 0])
        r = Circle(radius=0.28, color=YES, fill_color=YES, fill_opacity=0.3).move_to([2.2, -2.6, 0])
        tree.add(root, l, r, Line(root.get_bottom(), l.get_top(), color=GREY_B),
                 Line(root.get_bottom(), r.get_top(), color=GREY_B),
                 label(r"bivalent", font_size=18, color=HEAD).next_to(root, RIGHT, buff=0.15),
                 label(r"0-valent", font_size=18, color=DATA).next_to(l, LEFT, buff=0.15),
                 label(r"1-valent", font_size=18, color=YES).next_to(r, RIGHT, buff=0.15))
        with self.voiceover(
            "The proof of Fischer, Lynch and Paterson rests on one idea. <bookmark mark='a'/> A configuration is "
            "a snapshot of everything: every process's state and every message in flight. "
            "<bookmark mark='b'/> Call it zero-valent if every way the run can continue ends in the decision zero, "
            "one-valent if every way ends in one, and bivalent if both outcomes are still possible. "
            "<bookmark mark='c'/> A correct protocol must, at some step, pass from bivalent to univalent: that step "
            "is where the decision is really made. The theorem shows that an adversary who controls only the order "
            "of message delivery, and may crash one process, can always avoid that step."
        ) as vo:
            self.play(FadeIn(head), FadeIn(defs[0]))
            vo.wait_until("b")
            self.play(FadeIn(defs[1]), FadeIn(tree))
            vo.wait_until("c")
            self.play(FadeIn(defs[2]))
        self.wait(0.4)
        self.clear_scene()

    def explored(self):
        f = load("flp")
        head = label(r"Two tiny protocols, \ every schedule", font_size=36).to_edge(UP, buff=0.3)

        def rows(p):
            out = []
            for r in f[p]:
                v = r["valency"]
                val = r"bivalent" if len(v) > 1 else f"{v[0]}-valent"
                out.append(["".join(map(str, r["inputs"])), val, r"\textbf{yes}" if r["can_disagree"] else r"no",
                            r"\textbf{yes}" if r["can_block"] else r"no"])
            return out
        t1 = grid_table([r"inputs", r"valency", r"disagree?", r"block?"], rows("wait-n-f"),
                        widths=[1.2, 1.6, 1.5, 1.3], row_h=0.34, font_size=17, mono_cols=())
        t2 = grid_table([r"inputs", r"valency", r"disagree?", r"block?"], rows("wait-all"),
                        widths=[1.2, 1.6, 1.5, 1.3], row_h=0.34, font_size=17, mono_cols=())
        t1.move_to([-3.4, -0.6, 0])
        t2.move_to([3.4, -0.6, 0])
        for t, p in ((t1, "wait-n-f"), (t2, "wait-all")):
            for k, r in enumerate(f[p], start=1):
                if r["can_disagree"]:
                    t.cells[k][2].set_color(NO)
                if r["can_block"]:
                    t.cells[k][3].set_color(NO)
                if len(r["valency"]) > 1:
                    t.cells[k][1].set_color(HEAD)
        h1 = wrapped_label(r"wait for $n - f = 2$ values, \ decide the majority \ (ties to 0)", 5.8, font_size=19,
                           color=DATA).next_to(t1, UP, buff=0.2)
        h2 = wrapped_label(r"wait for all $n = 3$ values, \ decide the majority", 5.8, font_size=19,
                           color=LAM).next_to(t2, UP, buff=0.2)
        foot = label(r"three processes, \ one may crash: \ every interleaving of deliveries and crashes explored",
                     font_size=19, color=GREY_A).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "We can watch the dilemma on tiny protocols. Three processes, each with a bit; one may crash. Each "
            "sends its bit to the others, and our explorer tries every order of delivery and every crash. "
            "<bookmark mark='a'/> The first protocol waits for two values, since it cannot wait for a process that "
            "may have crashed, and decides the majority, breaking ties toward zero. Three input patterns are "
            "bivalent, and in each of them some schedule makes two processes decide differently: one hears zero "
            "and one, the other hears one and one. <bookmark mark='b'/> The second waits for all three values. "
            "It never disagrees, but if one process crashes, the others wait for ever. "
            "<bookmark mark='c'/> Wait too little and you can be wrong; wait for everyone and you can be stuck. "
            "FLP says every deterministic protocol, however clever, falls into one of these two holes."
        ) as vo:
            self.play(FadeIn(head), FadeIn(foot))
            vo.wait_until("a")
            self.play(FadeIn(h1), FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(h2), FadeIn(t2))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        head = label(r"The proof, \ in two lemmas", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            wrapped_label(r"\textbf{Lemma 1.} \ Some initial configuration is bivalent. \ Line the inputs up "
                          r"$000, 001, 011, 111$, \ each differing from the next in one process. \ The first is "
                          r"0-valent and the last 1-valent, \ so two neighbours $C, C'$ differ in valency. \ Crash "
                          r"the process where they differ, \ at the start: \ no one can tell $C$ from $C'$, \ so "
                          r"some run decides the same from both \ --- \ one of them was bivalent.", 12.4,
                          font_size=24, color=HEAD),
            wrapped_label(r"\textbf{Lemma 2.} \ From any bivalent configuration and any pending message $e$, \ some "
                          r"schedule ending with $e$ reaches a bivalent configuration again. \ \textit{Idea}: \ if "
                          r"delivering $e$ always made it univalent, \ two such steps on different processes "
                          r"would commute; \ on the same process, \ crash that process and the others cannot tell "
                          r"which happened.", 12.4, font_size=24, color=KERN),
            wrapped_label(r"\textbf{Theorem.} \ Start bivalent; \ repeatedly deliver the oldest pending message, \ "
                          r"staying bivalent. \ Every message is delivered eventually and at most one process is "
                          r"slow, \ a fair run, \ and no one ever decides.", 12.4, font_size=24, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        with self.voiceover(
            "The proof has two lemmas. <bookmark mark='a'/> The first says some starting configuration is "
            "bivalent. Line up the inputs from all zeros to all ones, changing one process at a time. The first is "
            "zero-valent and the last one-valent, so somewhere two neighbours differ. They differ only in one "
            "process's input, and if that process crashes at the very start, no one can tell them apart, so they "
            "cannot have opposite valencies after all: one of them must be bivalent. We saw three such "
            "configurations in our table. <bookmark mark='b'/> The second lemma says that from a bivalent "
            "configuration, whatever message is pending, the adversary can deliver it and still land somewhere "
            "bivalent. Otherwise there would be a critical step, and a case analysis shows that steps on "
            "different processes commute, while a step on the same process can be hidden by crashing that process. "
            "<bookmark mark='c'/> Now start bivalent and keep delivering the oldest message, staying bivalent each "
            "time. Every message arrives eventually; no one is ever silenced; and no one ever decides."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abc", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.5)
        self.clear_scene()

    def around(self):
        head = label(r"Three ways around", font_size=36).to_edge(UP, buff=0.3)
        rows = VGroup(
            wrapped_label(r"\textbf{give up determinism}: \ flip coins. \ Ben-Or (1983) decides with probability 1; "
                          r"\ the adversary cannot predict the coins", 12.4, font_size=25, color=YES),
            wrapped_label(r"\textbf{give up asynchrony}: \ assume partial synchrony \ (DLS 1988): \ always safe, \ and "
                          r"live once the network behaves for long enough", 12.4, font_size=25, color=HEAD),
            wrapped_label(r"\textbf{add an oracle}: \ a failure detector \ $\Diamond S$; \ in practice a timeout "
                          r"that is sometimes wrong", 12.4, font_size=25, color=LAM),
            wrapped_label(r"what nobody gets: \ a deterministic protocol that is \textit{always} safe \textit{and} "
                          r"\textit{always} live; \ Paxos and Raft keep safety unconditionally and give up liveness "
                          r"only while the network misbehaves", 12.4, font_size=25, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.38).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "FLP is about guarantees, and there are three ways to weaken what is guaranteed. "
            "<bookmark mark='a'/> Give up determinism: flip coins. The adversary controls the schedule but cannot "
            "predict the coins, and Michael Ben-Or's protocol of 1983 terminates with probability one. "
            "<bookmark mark='b'/> Give up pure asynchrony: assume the network eventually behaves, for long enough. "
            "Dwork, Lynch and Stockmeyer showed that protocols can then be always safe, and live whenever that "
            "happens. <bookmark mark='c'/> Or add an oracle: a failure detector, which in practice is a timeout "
            "that is sometimes wrong. <bookmark mark='d'/> What nobody can have is a deterministic protocol that is "
            "always safe and always live. Paxos and Raft choose: safety always, liveness only while the network "
            "is good. That is what the five Pebbles gave up."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    def benor(self):
        b = load("benor")
        head = label(r"Ben-Or: \ consensus by coin flips", font_size=36).to_edge(UP, buff=0.3)
        hist = b["random"]["hist"][:15]
        mx = max(c for _, c in hist)
        g = axes([0, 16, 1], [0, mx * 1.1, 200], x_length=7.0, y_length=3.6, x_label=r"rounds to decide",
                 y_label=r"runs \ (of 2{,}000)", xticks=range(1, 16, 2), yticks=range(200, int(mx * 1.1), 200),
                 fx=lambda v: f"{int(v)}", fy=lambda v: f"{int(v)}").move_to([-2.6, -0.6, 0])
        ax = g.ax
        bars = VGroup(*[Rectangle(width=0.32, height=max(0.02, ax.c2p(0, c)[1] - ax.c2p(0, 0)[1]), stroke_width=0,
                                  fill_color=YES, fill_opacity=0.8).move_to(ax.c2p(r, c / 2)) for r, c in hist])
        rule = VGroup(
            wrapped_label(r"each phase: \ report your value; \ if a majority report $v$, \ propose $v$; \ if more "
                          r"than $f$ propose $v$, \ \textbf{decide} it; \ if any do, adopt it; \ otherwise \textbf{flip "
                          r"a coin}", 5.2, font_size=19, color=WHITE),
            wrapped_label(rf"5 processes, \ 2 crashed, \ random delays: \ mean {b['random']['mean']:.1f} rounds, \ "
                          rf"{b['random']['p_le_5'] * 100:.0f}\% within 5, \ longest {b['random']['max']}", 5.2,
                          font_size=19, color=YES),
            wrapped_label(r"agreement in every run; \ termination with probability 1, \ but not by any fixed "
                          r"round", 5.2, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.8, -0.3, 0])
        with self.voiceover(
            "Here is Ben-Or's protocol at work. <bookmark mark='a'/> In each phase every process reports its "
            "value. If a majority reports the same value, a process proposes it; if more than f processes "
            "propose the same value, it decides; if it sees any proposal it adopts that value, and otherwise it "
            "flips a coin. Once enough coins agree, the next phase decides. <bookmark mark='b'/> With five "
            "processes, two of them crashed, and random delays, we ran it two thousand times. On average it decided "
            "in four rounds, three quarters of the time within five, and the longest run took twenty-seven. "
            "<bookmark mark='c'/> It never disagreed. It always terminated, eventually, but no bound on the number "
            "of rounds holds in every run, exactly as FLP requires."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(rule[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowFromEdge(br, DOWN) for br in bars], lag_ratio=0.05), FadeIn(rule[1]))
            vo.wait_until("c")
            self.play(FadeIn(rule[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, YES)
