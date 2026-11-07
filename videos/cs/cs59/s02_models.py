from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs59.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, mono


def proc(name, color=GREY_B, r=0.3, size=18):
    """A process drawn as a circle with its name inside."""
    c = Circle(radius=r, stroke_color=color, stroke_width=2, fill_color=BG, fill_opacity=1)
    return VGroup(c, label(name, font_size=size, color=WHITE).move_to(c))


def msg(a, b, color=DATA, sw=2.2, dashed=False):
    """A message as an arrow from point a to point b."""
    if dashed:
        return DashedLine(a, b, color=color, stroke_width=sw, dash_length=0.08).add_tip(tip_length=0.12)
    return Arrow(a, b, buff=0, stroke_width=sw, color=color, tip_length=0.13, max_tip_length_to_length_ratio=0.2)


def cross(at, color=NO, s=0.14):
    return VGroup(Line(at + np.array([-s, -s, 0]), at + np.array([s, s, 0]), color=color, stroke_width=4),
                  Line(at + np.array([-s, s, 0]), at + np.array([s, -s, 0]), color=color, stroke_width=4))


class Models(VoiceoverScene):
    def construct(self):
        self.card()
        self.timing()
        self.media()
        self.faults()
        self.consensus()
        self.local()

    def card(self):
        card = chapter_card(1, r"Models and faults", r"What exactly may a distributed system assume?",
                            lit=(1982, 2000), extra=((1982, r"Lamport, \ Shostak and Pease: \ Byzantine generals"),
                                                     (2000, r"Peleg: \ the LOCAL and CONGEST models")), part=PART)
        with self.voiceover("Chapter one. Models and faults."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def timing(self):
        head = label(r"Synchronous and asynchronous", font_size=36).to_edge(UP, buff=0.3)
        ys = [1.6, 0.6, -0.4]
        names = [r"$p_1$", r"$p_2$", r"$p_3$"]

        def lanes(x0, x1):
            g = VGroup()
            for y, nm in zip(ys, names):
                g.add(Line([x0, y, 0], [x1, y, 0], color=GREY_C, stroke_width=1.5))
                g.add(label(nm, font_size=18, color=GREY_A).next_to([x0, y, 0], LEFT, buff=0.12))
            return g
        sx0, sw = -6.0, 1.7
        sync = lanes(sx0, sx0 + 3 * sw)
        bounds = VGroup(*[DashedLine([sx0 + k * sw, 2.05, 0], [sx0 + k * sw, -0.75, 0], color=GREY_D,
                                     stroke_width=1.2, dash_length=0.07) for k in range(4)])
        rlab = VGroup(*[label(rf"round {k + 1}", font_size=16, color=GREY_B).move_to([sx0 + (k + 0.5) * sw, 2.25, 0])
                        for k in range(3)])
        pairs = [[(0, 1), (1, 2), (2, 0), (0, 2)], [(1, 0), (2, 1), (0, 1)], [(2, 0), (0, 2), (1, 2), (2, 1)]]
        smsgs = [VGroup(*[msg([sx0 + k * sw + 0.12, ys[i], 0], [sx0 + (k + 1) * sw - 0.12, ys[j], 0])
                          for i, j in pr]) for k, pr in enumerate(pairs)]
        ax0, ax1 = 1.0, 6.5
        asy = lanes(ax0, ax1)
        amsgs = VGroup(
            msg([1.2, ys[0], 0], [2.0, ys[1], 0], color=LAM),
            msg([1.5, ys[1], 0], [3.9, ys[2], 0], color=LAM),
            msg([2.4, ys[2], 0], [2.9, ys[0], 0], color=LAM),
            msg([3.3, ys[0], 0], [5.4, ys[2], 0], color=LAM),
            msg([4.2, ys[1], 0], [4.6, ys[0], 0], color=LAM),
        )
        late = msg([1.3, ys[2], 0], [6.3, ys[1], 0], color=HEAD, dashed=True)
        q = label(r"slow, \ or crashed?", font_size=18, color=HEAD).move_to([5.0, -0.85, 0])
        tl = VGroup(label(r"synchronous", font_size=24, color=DATA).move_to([sx0 + 1.5 * sw, 2.75, 0]),
                    label(r"asynchronous", font_size=24, color=LAM).move_to([(ax0 + ax1) / 2, 2.75, 0]))
        notes = VGroup(
            wrapped_label(r"lockstep rounds: \ a message sent in a round arrives before the next one begins, \ so a "
                          r"missing message proves a fault", 5.8, font_size=19, color=DATA),
            wrapped_label(r"no bound on delays or speeds: \ a process cannot tell a slow neighbour from a dead one "
                          r"\ (Part 38's FLP)", 5.6, font_size=19, color=LAM),
        )
        notes[0].move_to([-3.45, -1.75, 0])
        notes[1].move_to([3.75, -1.75, 0])
        foot = wrapped_label(r"in between, \ \textbf{partial synchrony} \ (Dwork, \ Lynch and Stockmeyer, \ 1988): \ "
                             r"bounds that hold only eventually, \ the world Raft lives in", 12.4, font_size=19,
                             color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A model fixes three things: how time behaves, how processes talk, and how they may fail. Start with "
            "time. <bookmark mark='a'/> In a synchronous system the processes move in lockstep rounds. In each "
            "round every process sends its messages, every message arrives before the round ends, and then each "
            "process computes. So if an expected message does not arrive, its sender has certainly failed. "
            "<bookmark mark='b'/> In an asynchronous system there is no bound on how long a message takes or how "
            "fast a process runs. <bookmark mark='c'/> A message that has not arrived may still be on its way, so "
            "no process can ever tell a slow neighbour from a dead one, which is the root of Part 38's FLP theorem. "
            "<bookmark mark='d'/> Real networks sit in between: Dwork, Lynch and Stockmeyer's partial synchrony, "
            "where bounds hold only eventually, is where Raft lives."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sync), FadeIn(bounds), FadeIn(rlab), FadeIn(tl[0]))
            vo.wait_until("a")
            for g in smsgs:
                self.play(LaggedStart(*[GrowArrow(m) for m in g], lag_ratio=0.1), run_time=0.9)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(asy), FadeIn(tl[1]))
            self.play(LaggedStart(*[GrowArrow(m) for m in amsgs], lag_ratio=0.35), run_time=2.4)
            vo.wait_until("c")
            self.play(Create(late), run_time=2.0)
            self.play(FadeIn(q), FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def media(self):
        head = label(r"Messages and shared memory", font_size=36).to_edge(UP, buff=0.3)
        c0 = np.array([-3.5, 0.55, 0])
        pos = [c0 + 1.65 * np.array([np.cos(PI / 2 + k * TAU / 5), np.sin(PI / 2 + k * TAU / 5), 0]) for k in range(5)]
        nodes = VGroup(*[proc(rf"$p_{k + 1}$").move_to(p) for k, p in enumerate(pos)])
        edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (0, 2), (1, 4)]
        links = VGroup(*[Line(pos[a], pos[b], color=GREY_D, stroke_width=2) for a, b in edges])
        links.set_z_index(-1)
        envs = VGroup(*[Rectangle(width=0.24, height=0.16, stroke_color=DATA, stroke_width=1.5, fill_color=DATA,
                                  fill_opacity=0.6).move_to(pos[a]) for a, b in edges])
        envs.set_z_index(2)
        # shared memory: three registers and four processes around them
        regs = VGroup(*[tag_box_(rf"$R_{k + 1}$", v) for k, v in enumerate(("7", "0", "3"))]).arrange(RIGHT, buff=0.25)
        regs.move_to([3.6, 0.55, 0])
        ps = VGroup(*[proc(rf"$q_{k + 1}$") for k in range(4)])
        ps[0].move_to([2.2, 2.05, 0])
        ps[1].move_to([5.0, 2.05, 0])
        ps[2].move_to([2.2, -0.95, 0])
        ps[3].move_to([5.0, -0.95, 0])
        ops = VGroup(
            msg(ps[0].get_bottom(), regs[0].get_top(), color=KERN),
            msg(regs[1].get_top(), ps[1].get_bottom() + LEFT * 0.1, color=DATA),
            msg(regs[2].get_bottom(), ps[3].get_top(), color=DATA),
            msg(ps[2].get_top(), regs[0].get_bottom(), color=KERN),
        )
        opl = VGroup(label(r"write", font_size=16, color=KERN).next_to(ops[0], LEFT, buff=0.08),
                     label(r"read", font_size=16, color=DATA).next_to(ops[1], RIGHT, buff=0.08),
                     label(r"read", font_size=16, color=DATA).next_to(ops[2], RIGHT, buff=0.08),
                     label(r"write", font_size=16, color=KERN).next_to(ops[3], LEFT, buff=0.08))
        notes = VGroup(
            wrapped_label(r"\textbf{message passing}: \ send and receive along links; \ the network may delay, \ "
                          r"reorder or lose", 5.6, font_size=19, color=DATA),
            wrapped_label(r"\textbf{shared memory}: \ read and write registers, \ or stronger objects such as "
                          r"compare-and-swap \ (Chapter 6)", 5.6, font_size=19, color=KERN),
        )
        notes[0].move_to([-3.5, -1.95, 0])
        notes[1].move_to([3.6, -1.95, 0])
        foot = wrapped_label(r"Attiya, \ Bar-Noy and Dolev \ (1995): \ while a majority of processes is correct, \ "
                             r"messages can simulate a register, \ so many results carry over", 12.4, font_size=19,
                             color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Next, how processes talk. <bookmark mark='a'/> In message passing, processes are nodes of a network and "
            "communicate only by sending messages along its links, which may be delayed, reordered or lost. "
            "<bookmark mark='b'/> In shared memory, processes never send anything: they read and write shared "
            "registers, or use stronger objects like the compare-and-swap of Part 33, and Chapter six ranks those "
            "objects by power. <bookmark mark='c'/> The two worlds are closer than they look. Hagit Attiya, Amotz "
            "Bar-Noy and Danny Dolev showed in 1995 that as long as a majority of processes is correct, messages can "
            "simulate a shared register, so an algorithm for one model often runs in the other."
        ) as vo:
            self.play(FadeIn(head), Create(links), FadeIn(nodes))
            vo.wait_until("a")
            self.play(FadeIn(envs, run_time=0.3))
            self.play(*[envs[k].animate.move_to(pos[b]) for k, (a, b) in enumerate(edges)], run_time=1.4)
            self.play(*[envs[k].animate.move_to(pos[a]) for k, (a, b) in enumerate(edges)], run_time=1.4)
            self.play(FadeOut(envs), FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(regs), FadeIn(ps))
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(o), FadeIn(t)) for o, t in zip(ops, opl)],
                                  lag_ratio=0.4), run_time=2.4)
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def faults(self):
        head = label(r"Three kinds of fault", font_size=36).to_edge(UP, buff=0.3)
        boxes = VGroup()
        for (w, h), c, t in (((5.8, 4.3), NO, r"\textbf{Byzantine}: \ anything at all, \ even lies"),
                             ((4.8, 2.9), HEAD, r"\textbf{omission}: \ some messages lost"),
                             ((3.6, 1.5), YES, r"\textbf{crash}: \ stops, \ forever")):
            r = RoundedRectangle(width=w, height=h, corner_radius=0.2, stroke_color=c, stroke_width=2.2,
                                 fill_color=c, fill_opacity=0.06)
            boxes.add(VGroup(r, label(t, font_size=19, color=c)))
        for b in boxes:
            b[0].move_to([-3.6, 0.15, 0])
        boxes[0][1].next_to(boxes[0][0].get_top(), DOWN, buff=0.22)
        boxes[1][1].next_to(boxes[1][0].get_top(), DOWN, buff=0.22)
        boxes[2][1].move_to(boxes[2][0])

        def mini(kind):
            p = proc(r"$p$").move_to([0, 0, 0])
            qs = VGroup(*[proc(rf"$q_{k + 1}$", r=0.24, size=16).move_to([1.45, 0.75 - 0.75 * k, 0]) for k in range(3)])
            arr = VGroup()
            extra = VGroup()
            if kind == "crash":
                arr.add(msg(p.get_right(), qs[0].get_left(), color=YES))
                extra.add(cross(p.get_center()))
            elif kind == "omission":
                arr.add(msg(p.get_right(), qs[0].get_left(), color=HEAD))
                lost = DashedLine(p.get_right(), qs[1].get_left(), color=GREY_D, stroke_width=1.8, dash_length=0.07)
                arr.add(lost)
                extra.add(cross(lost.get_center(), color=HEAD, s=0.1))
                arr.add(msg(p.get_right(), qs[2].get_left(), color=HEAD))
            else:
                for k, v in enumerate("011"):
                    a = msg(p.get_right(), qs[k].get_left(), color=NO)
                    arr.add(a)
                    extra.add(label(v, font_size=17, color=NO).move_to(a.point_from_proportion(0.55) + UP * 0.17))
            return VGroup(p, qs, arr, extra)
        minis = VGroup(mini("crash"), mini("omission"), mini("byz")).arrange(RIGHT, buff=0.4)
        if minis.width > 6.3:
            minis.scale_to_fit_width(6.3)
        minis.move_to([3.65, 1.4, 0])
        caps = VGroup(*[wrapped_label(t, 2.0, font_size=17, color=c).next_to(m, DOWN, buff=0.15)
                        for m, t, c in zip(minis, (r"sends to $q_1$, \ dies", r"drops one, \ lives on",
                                                   r"tells $q_1$ 0, \ the others 1"), (YES, HEAD, NO))])
        notes = VGroup(
            wrapped_label(r"each kind contains the one inside it: \ an algorithm that survives Byzantine faults "
                          r"survives the others", 6.0, font_size=19, color=WHITE),
            wrapped_label(r"bounds are stated for $n$ processes, \ at most $f$ of them faulty; \ harder faults cost "
                          r"more: \ synchronous crashes allow any $f$, \ Byzantine ones need $n > 3f$", 6.0,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, -1.85, 0])
        with self.voiceover(
            "Third, how processes fail. <bookmark mark='a'/> A crashed process simply stops, possibly halfway "
            "through sending a round's messages, and never returns. <bookmark mark='b'/> An omission fault is "
            "subtler: the process keeps running but some of its messages are never sent or never received. "
            "<bookmark mark='c'/> And a Byzantine process may do anything at all, including telling different "
            "processes different things. The name comes from Leslie Lamport, Robert Shostak and Marshall Pease's "
            "paper of 1982 on the Byzantine generals. <bookmark mark='d'/> Each kind contains the one before, so "
            "an algorithm that survives liars survives crashes too. <bookmark mark='e'/> Every bound in this part "
            "is stated for n processes of which at most f are faulty, and the harder the faults, the more it "
            "costs."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(boxes[2]), FadeIn(minis[0][:2]), FadeIn(caps[0]))
            self.play(GrowArrow(minis[0][2][0]), run_time=0.6)
            self.play(Create(minis[0][3]))
            vo.wait_until("b")
            self.play(FadeIn(boxes[1]), FadeIn(minis[1][:2]), FadeIn(caps[1]))
            self.play(Create(minis[1][2]), FadeIn(minis[1][3]), run_time=1.0)
            vo.wait_until("c")
            self.play(FadeIn(boxes[0]), FadeIn(minis[2][:2]), FadeIn(caps[2]))
            self.play(Create(minis[2][2]), FadeIn(minis[2][3]), run_time=1.0)
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            vo.wait_until("e")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def consensus(self):
        head = label(r"Consensus, \ and the map of what is possible", font_size=36).to_edge(UP, buff=0.3)
        ins = [0, 1, 1, 0]
        ps = VGroup(*[proc(rf"$p_{k + 1}$") for k in range(4)]).arrange(RIGHT, buff=0.55).move_to([-3.9, 1.75, 0])
        inl = VGroup(*[label(rf"in {v}", font_size=17, color=DATA).next_to(p, UP, buff=0.1) for p, v in zip(ps, ins)])
        dec = VGroup(*[tag_box_(r"", "1", color=YES).next_to(p, DOWN, buff=0.55) for p in ps])
        arr = VGroup(*[Arrow(p.get_bottom(), d.get_top(), buff=0.05, stroke_width=2, color=GREY_B,
                             max_tip_length_to_length_ratio=0.3) for p, d in zip(ps, dec)])
        ill = note(r"illustrative", font_size=16).next_to(dec, DOWN, buff=0.12)
        props = VGroup(
            label(r"\textbf{agreement}: \ no two correct processes decide differently", font_size=19, color=YES),
            label(r"\textbf{validity}: \ if every input is $v$, \ the decision is $v$", font_size=19, color=DATA),
            label(r"\textbf{termination}: \ every correct process decides", font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.3, 1.45, 0])
        rows = [[r"synchronous", r"any $f$; \ $f + 1$ rounds \ (Ch.\ 4)",
                 r"$n > 3f$; \ signed broadcast: \ any $f$ \ (Ch.\ 4)"],
                [r"asynchronous", r"deterministic: \ impossible \ (FLP 1985); \ randomized: \ $n > 2f$ \ (Ch.\ 5)",
                 r"randomized: \ $n > 3f$ \ (Bracha 1987)"],
                [r"shared memory", r"registers: \ impossible; \ stronger objects: \ a hierarchy \ (Ch.\ 6)", r"---"]]
        tab = grid_table([r"model", r"crash faults", r"Byzantine faults"], rows, widths=[2.4, 6.0, 4.0], row_h=0.6,
                         font_size=20, mono_cols=())
        tab.move_to([0, -1.85, 0])
        for k, c in ((1, YES), (2, NO)):
            tab.cells[0][k].set_color(c)
        with self.voiceover(
            "The problem at the centre of the theory is consensus. <bookmark mark='a'/> Each process starts with an "
            "input, here a bit, and must decide on an output. <bookmark mark='b'/> Three rules: agreement, no two "
            "correct processes decide differently; validity, if every input is the same value then that is the "
            "decision; and termination, every correct process eventually decides. Without validity, always "
            "deciding zero would do. <bookmark mark='c'/> Here is the map this part will prove. With synchronous "
            "rounds and crashes, any number of faults can be tolerated, at a cost of f plus one rounds. Byzantine "
            "faults need more than three f processes, unless messages are signed. <bookmark mark='d'/> Without "
            "synchrony, no deterministic algorithm survives even one crash, but coins rescue us, and in shared "
            "memory the answer depends on the objects you are given."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(ps), FadeIn(inl))
            self.play(LaggedStart(*[GrowArrow(a) for a in arr], lag_ratio=0.2), FadeIn(dec), FadeIn(ill))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(p) for p in props], lag_ratio=0.5), run_time=2.4)
            vo.wait_until("c")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            self.play(FadeIn(VGroup(*tab.cells[1])))
            vo.wait_until("d")
            self.play(LaggedStart(*[FadeIn(VGroup(*c)) for c in tab.cells[2:]], lag_ratio=0.5))
        self.wait(0.4)
        self.clear_scene()

    def local(self):
        head = label(r"LOCAL and CONGEST: \ counting rounds", font_size=36).to_edge(UP, buff=0.3)
        pts = {0: (-5.6, 1.3), 1: (-4.2, 2.0), 2: (-2.7, 1.5), 3: (-1.6, 0.4), 4: (-4.5, 0.5), 5: (-3.2, -0.3),
               6: (-5.4, -0.6), 7: (-2.0, -1.0)}
        E = [(0, 1), (1, 2), (2, 3), (0, 4), (1, 4), (4, 5), (2, 5), (4, 6), (5, 7), (3, 7), (6, 5)]
        P = {k: np.array([x, y, 0]) for k, (x, y) in pts.items()}
        links = VGroup(*[Line(P[a], P[b], color=GREY_D, stroke_width=2) for a, b in E]).set_z_index(-1)
        nodes = VGroup(*[Dot(P[k], radius=0.17, color=HEAD if k == 6 else GREY_B) for k in pts])
        vlab = label(r"$v$", font_size=20, color=HEAD).next_to(nodes[6], DOWN, buff=0.1)
        ball = label(r"what $v$ knows after $t$ rounds: \ everything within $t$ hops", font_size=18,
                     color=HEAD).move_to([-3.7, -1.65, 0])
        lit = [6]

        def wave(big):
            ds = VGroup()
            for a, b in E:
                for u, v in ((a, b), (b, a)):
                    d = Square(side_length=0.2 if big else 0.1, stroke_width=0, fill_color=HEAD if big else DATA,
                               fill_opacity=0.9).move_to(P[u])
                    d.target_pt = P[v]
                    ds.add(d)
            return ds.set_z_index(2)
        tiles = VGroup()
        for t, b, c in ((r"LOCAL", r"synchronous rounds, \ no faults, \ unique ids, \ messages of any size; \ the "
                         r"cost is the number of rounds", HEAD),
                        (r"CONGEST", r"the same, \ but each link carries $O(\log n)$ bits per round: \ a few ids; \ "
                         r"now bandwidth matters too", DATA)):
            frame = RoundedRectangle(width=5.6, height=1.55, corner_radius=0.12, stroke_color=c, stroke_width=1.8,
                                     fill_color=BG, fill_opacity=1)
            g = VGroup(label(t, font_size=22, color=c), wrapped_label(b, 5.2, font_size=18, color=GREY_A)).arrange(
                DOWN, buff=0.12).move_to(frame)
            tiles.add(VGroup(frame, g))
        tiles.arrange(DOWN, buff=0.25).move_to([3.4, 0.75, 0])
        notes = VGroup(
            wrapped_label(r"in LOCAL every problem takes at most the diameter: \ gather the whole graph, \ then "
                          r"compute; \ the question is which problems need far fewer rounds", 12.4, font_size=19,
                          color=WHITE),
            wrapped_label(r"Peleg's book \ (2000) \ fixed these names; \ Chapters 2 and 3 ask how fast a ring can be "
                          r"coloured", 12.4, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "One more pair of models measures something else: not fault tolerance, but distance. "
            "<bookmark mark='a'/> In the LOCAL model the network itself is the input. There are no faults, every "
            "node has a unique identifier, and in each synchronous round every node may send a message of any "
            "size to each neighbour. The only cost is the number of rounds. <bookmark mark='b'/> In each round, "
            "information moves one hop. <bookmark mark='c'/> The CONGEST model is the same, except that a message "
            "may carry only about log n bits, a few identifiers, so bandwidth matters too. <bookmark mark='d'/> "
            "In LOCAL, every problem can be solved in as many rounds as the network's diameter: gather the whole "
            "graph and compute. The interesting question is what can be done in far fewer, and the next two "
            "chapters answer it for colouring a ring. David Peleg's book of 2000 fixed these names."
        ) as vo:
            self.play(FadeIn(head), Create(links), FadeIn(nodes), FadeIn(vlab))
            vo.wait_until("a")
            self.play(FadeIn(tiles[0]))
            vo.wait_until("b")
            for big in (True, True):
                w = wave(big)
                self.play(FadeIn(w, run_time=0.2))
                self.play(*[d.animate.move_to(d.target_pt) for d in w], run_time=1.1)
                self.play(FadeOut(w, run_time=0.2))
                newlit = set(lit)
                for a, b in E:
                    if a in lit:
                        newlit.add(b)
                    if b in lit:
                        newlit.add(a)
                lit = sorted(newlit)
                self.play(*[nodes[k].animate.set_color(HEAD) for k in lit], run_time=0.4)
            self.play(FadeIn(ball))
            vo.wait_until("c")
            self.play(FadeIn(tiles[1]))
            w = wave(False)
            self.play(FadeIn(w, run_time=0.2))
            self.play(*[d.animate.move_to(d.target_pt) for d in w], run_time=1.1)
            self.play(FadeOut(w, run_time=0.2))
            vo.wait_until("d")
            self.play(FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()


def tag_box_(name, value, color=DATA):
    """A register or a decision: a small box holding a value, with an optional name above it."""
    box = RoundedRectangle(width=0.75, height=0.55, corner_radius=0.08, stroke_color=color, stroke_width=1.8,
                           fill_color=BG, fill_opacity=1)
    v = mono(value, size=20, color=color).move_to(box)
    g = VGroup(box, v)
    if name:
        g.add(label(name, font_size=17, color=GREY_A).next_to(box, UP, buff=0.08))
    return g


_ = (KERN, LAM, NO)
