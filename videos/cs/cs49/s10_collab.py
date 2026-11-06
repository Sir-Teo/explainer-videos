from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, bar_chart, load, module_box, mono


def cells(s, hi=None, w=0.36, size=19, color=WHITE):
    """A text as a row of character cells; spaces drawn as a faint dot; ``hi`` maps index -> colour."""
    g = VGroup()
    for k, ch in enumerate(s):
        box = Square(side_length=w, stroke_color=GREY_D, stroke_width=1.2, fill_color=BG, fill_opacity=1)
        c = (hi or {}).get(k, GREY_D if ch == " " else color)
        t = mono("·" if ch == " " else ch, size=size, color=c).move_to(box)
        g.add(VGroup(box, t))
    return g.arrange(RIGHT, buff=0)


def tile(title, body, col, w=5.8, h=2.2):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.25).move_to(frame)
    return VGroup(frame, t, b)


class Collab(VoiceoverScene):
    def construct(self):
        self.card()
        self.design()
        self.positions()
        self.transform()
        self.crdt()
        self.cursors()

    def card(self):
        card = chapter_card(9, r"A collaborative editor", r"How do several people type into one document at once?",
                            lit=(1989, 2011), extra=((1989, r"Ellis and Gibbs: \ transformation"),
                                                     (2011, r"Shapiro et al.: \ CRDTs")), part=PART)
        with self.voiceover("Chapter nine. A collaborative editor."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def design(self):
        head = label(r"Requirements, \ and the design", font_size=36).to_edge(UP, buff=0.3)
        clients = VGroup(*[module_box(rf"editor {n}", DATA, w=1.7, h=0.6) for n in "ABC"]).arrange(DOWN, buff=0.6)
        clients.move_to([-5.6, 0.4, 0])
        server = module_box(r"collaboration server", KERN, w=2.5, h=0.8).move_to([-2.3, 0.4, 0])
        log = module_box(r"operation log", LAM, w=2.0, h=0.6).move_to([0.75, 1.3, 0])
        snap = module_box(r"snapshots", GREY_B, w=2.0, h=0.6).move_to([0.75, -0.5, 0])
        links = VGroup(*[Line(c.get_right(), server.get_left(), color=GREY_C, stroke_width=2) for c in clients])
        ws = label(r"WebSockets \ (Part 48)", font_size=16, color=GREY_B).next_to(clients, DOWN, buff=0.3)
        a1 = Arrow(server.get_right(), log.get_left(), buff=0.08, color=GREY_C, stroke_width=2)
        a2 = Arrow(log.get_bottom(), snap.get_top(), buff=0.08, color=GREY_C, stroke_width=2)
        comp = label(r"compacted", font_size=16, color=GREY_B).next_to(a2, RIGHT, buff=0.1)
        reqs = VGroup(
            wrapped_label(r"\textbf{local first}: \ a keystroke shows at once on the typist's own screen", 4.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"\textbf{convergence}: \ when the typing stops, \ every copy holds the same text", 4.4,
                          font_size=19, color=YES),
            wrapped_label(r"\textbf{intention}: \ an edit lands where its author meant, \ whatever others typed "
                          r"meanwhile", 4.4, font_size=19, color=HEAD),
            wrapped_label(r"napkin: \ 10 people $\times$ 5 keys a second $=$ 50 operations a second per document: \ "
                          r"tiny; \ the order is the hard part", 4.4, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.55, 0.2, 0])
        ill = note(r"illustrative", font_size=16).next_to(reqs[3], DOWN, buff=0.12).align_to(reqs[3], LEFT)
        op = mono('ins(4, "f")', size=16, color=HEAD).next_to(clients[0], UP, buff=0.15)
        with self.voiceover(
            "A collaborative editor lets several people type into one document at once. <bookmark mark='a'/> Every "
            "keystroke must appear at once on the typist's own screen; nobody waits for a server. "
            "<bookmark mark='b'/> When the typing stops, every copy must hold the same text: convergence. "
            "<bookmark mark='c'/> And each edit should land where its author meant it, whatever others typed "
            "meanwhile. <bookmark mark='d'/> The design is small. Editors hold WebSocket connections to a "
            "collaboration server, which relays each operation and appends it to a log, compacted into snapshots. "
            "<bookmark mark='e'/> The load is tiny, perhaps fifty operations a second for a busy document. The hard "
            "part is order."
        ) as vo:
            self.play(FadeIn(head), FadeIn(clients))
            vo.wait_until("a")
            self.play(FadeIn(reqs[0]))
            vo.wait_until("b")
            self.play(FadeIn(reqs[1]))
            vo.wait_until("c")
            self.play(FadeIn(reqs[2]))
            vo.wait_until("d")
            self.play(Create(links), FadeIn(ws), FadeIn(server), GrowArrow(a1), FadeIn(log), GrowArrow(a2),
                      FadeIn(snap), FadeIn(comp))
            p = Dot(clients[0].get_right(), radius=0.09, color=HEAD)
            self.play(FadeIn(p), FadeIn(op))
            self.play(p.animate.move_to(server.get_left()), run_time=0.8)
            q = [p.copy() for _ in range(3)]
            self.add(*q)
            self.play(q[0].animate.move_to(clients[1].get_right()), q[1].animate.move_to(clients[2].get_right()),
                      q[2].animate.move_to(log.get_left()), FadeOut(p), run_time=1.0)
            self.play(*[FadeOut(x) for x in q], FadeOut(op))
            vo.wait_until("e")
            self.play(FadeIn(reqs[3]), FadeIn(ill))
        self.wait(0.4)
        self.clear_scene()

    def positions(self):
        o = load("ot")["example"]
        a, b = o["a"], o["b"]
        head = label(r"Concurrent edits: \ positions shift", font_size=36).to_edge(UP, buff=0.3)
        start = cells(o["start"]).move_to([0, 2.15, 0])
        idx = VGroup(*[label(f"{k}", font_size=16, color=GREY_B).next_to(c, DOWN, buff=0.06)
                       for k, c in enumerate(start)])
        sa = o["start"][:a[1]] + a[2] + o["start"][a[1]:]
        sb = o["start"][:b[1]] + b[2] + o["start"][b[1]:]
        cols = []
        for x, name, col, own, mine, other, final, hi1, hi2, good in (
                (-3.5, r"site A", DATA, a, sa, b, o["naive"][0], {a[1]: HEAD}, {a[1]: HEAD, b[1]: NO}, False),
                (3.5, r"site B", LAM, b, sb, a, o["naive"][1], {b[1]: HEAD}, {a[1]: HEAD, b[1] + 1: HEAD}, True)):
            t = label(name, font_size=22, color=col)
            o1 = label(rf"own edit: \ insert \texttt{{{own[2]}}} at {own[1]}", font_size=18, color=GREY_A)
            r1 = cells(mine, hi=hi1)
            o2 = label(rf"then the other's, \ as sent: \ insert \texttt{{{other[2]}}} at {other[1]}", font_size=18,
                       color=GREY_A)
            r2 = cells(final, hi=hi2)
            g = VGroup(t, o1, r1, o2, r2).arrange(DOWN, buff=0.2).move_to([x, -0.35, 0])
            mark = label(r"right" if good else r"wrong place", font_size=18, color=YES if good else NO).next_to(
                r2, DOWN, buff=0.15)
            cols.append((g, mark))
        verdict = wrapped_label(r"two copies, \ two texts: \ a position means something only in the state it was "
                                r"made in", 12.0, font_size=21, color=NO).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Here is why order is hard. <bookmark mark='a'/> Two people share the text, the cat sat. "
            "<bookmark mark='b'/> At the same moment, A inserts the letter z at position one, and B appends an x at "
            "position eleven, the end. <bookmark mark='c'/> Then each applies the other's operation as sent. At B, "
            "that is still right. But at A, position eleven no longer means the end: the z pushed everything one "
            "place right, so the x lands between the a and the t. <bookmark mark='d'/> Two copies, two texts. A "
            "position only means something in the state it was made in."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(start), FadeIn(idx))
            vo.wait_until("b")
            self.play(*[FadeIn(VGroup(*g[:3])) for g, _ in cols])
            vo.wait_until("c")
            self.play(FadeIn(cols[1][0][3:]), FadeIn(cols[1][1]))
            self.play(FadeIn(cols[0][0][3:]), FadeIn(cols[0][1]))
            vo.wait_until("d")
            self.play(FadeIn(verdict))
        self.wait(0.4)
        self.clear_scene()

    def transform(self):
        d = load("ot")
        o = d["example"]
        a, b = o["a"], o["b"]
        head = label(r"Operational transformation \ (Ellis \& Gibbs, \ 1989)", font_size=36).to_edge(UP, buff=0.3)
        c1 = mono(f'ins({b[1]}, "{b[2]}")', size=20, color=LAM)
        c2 = mono(f'ins({b[1] + 1}, "{b[2]}")', size=20, color=YES)
        VGroup(c1, c2).arrange(RIGHT, buff=4.2).move_to([0, 2.25, 0])
        arr = Arrow(c1.get_right(), c2.get_left(), buff=0.2, color=GREY_B, stroke_width=2.5)
        why = label(rf"A's concurrent insert was at {a[1]} $<$ {b[1]}: \ shift right", font_size=18,
                    color=HEAD).next_to(arr, DOWN, buff=0.12)
        fin = VGroup()
        for x, name, col, s in ((-3.5, r"site A", DATA, o["transformed"][0]), (3.5, r"site B", LAM,
                                                                              o["transformed"][1])):
            r = cells(s, hi={a[1]: HEAD, b[1] + 1: HEAD})
            fin.add(VGroup(label(name, font_size=20, color=col), r).arrange(RIGHT, buff=0.3).move_to([x, 0.95, 0]))
        same = label(r"the same text", font_size=19, color=YES).next_to(fin, DOWN, buff=0.18)
        rules = VGroup(
            wrapped_label(r"\texttt{transform(op, other)}: \ an insert before op's position shifts it right; \ a "
                          r"delete before it shifts it left; \ a tie at one position is settled by a fixed site "
                          r"priority", 6.0, font_size=19, color=WHITE),
            wrapped_label(r"the property it must have \ (TP1): \ $a$ then $b'$ gives the same text as $b$ then $a'$",
                          6.0, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([-3.4, -1.95, 0])
        vals = [100 * d["converged_transformed"], 100 * d["converged_naive"]]
        chart = bar_chart(vals, [r"transformed", r"applied as sent"], [YES, NO], height=1.6, bar_w=1.0, gap=1.5,
                          vmax=100, fmt_=lambda v: rf"{v:.0f}\%" if v >= 99.5 else rf"{v:.1f}\%")
        cap = label(rf"{d['trials']:,} random pairs of concurrent edits: \ converged", font_size=18, color=GREY_A)
        VGroup(cap, chart).arrange(DOWN, buff=0.25).move_to([3.4, -1.75, 0])
        with self.voiceover(
            "Operational transformation, from Clarence Ellis and Simon Gibbs in 1989, repairs an operation before "
            "applying it. <bookmark mark='a'/> A transforms B's insert at eleven against its own concurrent insert "
            "at one. That came earlier in the text, so B's position shifts right, to twelve. <bookmark mark='b'/> "
            "Now both copies agree. <bookmark mark='c'/> The rules are few: an insert before you pushes you right, a "
            "delete before you pulls you left, and a tie is settled by a fixed priority between sites. "
            "<bookmark mark='d'/> Over five thousand random pairs of concurrent edits, transformation converged "
            "every time; applied as sent, only about six in a hundred did. <bookmark mark='e'/> With many sites the "
            "original algorithm was later found to diverge, so Jupiter, in 1995, and later Google Docs route every "
            "operation through one server, which fixes a single order."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(c1))
            self.play(GrowArrow(arr), FadeIn(why), FadeIn(c2))
            vo.wait_until("b")
            self.play(FadeIn(fin), FadeIn(same))
            vo.wait_until("c")
            self.play(FadeIn(rules[0]))
            vo.wait_until("d")
            self.play(FadeIn(cap), FadeIn(chart))
            vo.wait_until("e")
            self.play(FadeIn(rules[1]))
        self.wait(0.4)
        self.clear_scene()

    def crdt(self):
        r = load("rga")
        head = label(r"A sequence CRDT: \ names, \ not positions", font_size=36).to_edge(UP, buff=0.3)

        def elem(ch, ident, col=WHITE):
            c = cells(ch, color=col, w=0.46, size=21)
            i = mono(ident, size=16, color=GREY_B).next_to(c, DOWN, buff=0.08)
            return VGroup(c, i)
        base = VGroup(*[elem(ch, f"{k + 1},1") for k, ch in enumerate("cat")]).arrange(RIGHT, buff=0.12)
        base.move_to([-4.9, 1.75, 0])
        i1 = elem("!", "4,1", DATA).move_to([-2.4, 2.35, 0])
        i2 = elem("s", "4,2", LAM).move_to([-2.4, 1.15, 0])
        w1 = label(r"user 1", font_size=16, color=DATA).next_to(i1, RIGHT, buff=0.15)
        w2 = label(r"user 2", font_size=16, color=LAM).next_to(i2, RIGHT, buff=0.15)
        r1 = Arrow(i1[0].get_left(), base[2][0].get_right() + UP * 0.08, buff=0.08, color=DATA, stroke_width=2,
                   max_tip_length_to_length_ratio=0.15)
        r2 = Arrow(i2[0].get_left(), base[2][0].get_right() + DOWN * 0.08, buff=0.08, color=LAM, stroke_width=2,
                   max_tip_length_to_length_ratio=0.15)
        after = label(r"both: \ ``after 3,1''", font_size=16, color=GREY_A).next_to(base, DOWN, buff=0.45)
        merged = VGroup(*[elem(ch, ident, col) for ch, ident, col in
                          (("c", "1,1", WHITE), ("a", "2,1", WHITE), ("t", "3,1", WHITE), ("s", "4,2", LAM),
                           ("!", "4,1", DATA))]).arrange(RIGHT, buff=0.12).move_to([3.2, 2.05, 0])
        arr = Arrow([-0.8, 1.75, 0], merged.get_left() + LEFT * 0.1 + DOWN * 0.3, buff=0.1, color=GREY_B,
                    stroke_width=2)
        rule = wrapped_label(r"same reference: \ the larger name first, \ (4,2) before (4,1); \ every replica, \ in "
                             r"any arrival order; \ a deleted element stays as a tombstone", 5.0, font_size=18,
                             color=HEAD).next_to(merged, DOWN, buff=0.3)
        res = VGroup()
        for x, title, kind, col in ((-3.4, r"replicated growable array \ (Roh et al., \ 2011)", "rga", YES),
                                    (3.4, r"positions replayed as sent", "naive", NO)):
            t = label(title, font_size=20, color=col)
            txt = VGroup(*[mono(s.replace(" ", "·"), size=18, color=col) for s in r[kind]["example"]["texts"]])
            txt.arrange(DOWN, buff=0.12)
            v = label(rf"converged in {100 * r[kind]['converged']:.0f}\% of 50 sessions", font_size=19, color=col)
            res.add(VGroup(t, txt, v).arrange(DOWN, buff=0.2).move_to([x, -1.65, 0]))
        cap = label(r"three people, \ 30 edits a session, \ delivered in random order: \ one session's three copies",
                    font_size=18, color=GREY_B).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The other answer is to stop using positions. <bookmark mark='a'/> In a sequence CRDT, here the "
            "replicated growable array of Roh and colleagues, 2011, every character gets a permanent name: a "
            "counter, and the replica that made it. <bookmark mark='b'/> An insert names the character it goes "
            "after. Here two people type after the t at once. <bookmark mark='c'/> A fixed rule decides: the larger "
            "name comes first, on every replica, in any arrival order. A deleted character stays as a tombstone, so "
            "later inserts can still name it. <bookmark mark='d'/> In fifty sessions of three people making thirty "
            "edits, delivered in random order, the array always converged. Replaying positions as sent, no session "
            "did."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(base))
            vo.wait_until("b")
            self.play(FadeIn(i1), FadeIn(w1), GrowArrow(r1), FadeIn(i2), FadeIn(w2), GrowArrow(r2), FadeIn(after))
            vo.wait_until("c")
            self.play(GrowArrow(arr), FadeIn(merged))
            self.play(FadeIn(rule))
            vo.wait_until("d")
            self.play(FadeIn(res[0]), FadeIn(res[1]), FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    def cursors(self):
        head = label(r"Cursors, \ presence, \ and the trade-off", font_size=36).to_edge(UP, buff=0.3)
        old_s, new_s, at = "the cat sat", "the big cat sat", 8
        x0 = -4.8
        old = cells(old_s, w=0.42, size=21)
        old.move_to([x0 + old.width / 2, 1.85, 0])
        new = cells(new_s, w=0.42, size=21, hi={k: HEAD for k in range(4, 8)})
        new.move_to([x0 + new.width / 2, 1.85, 0])

        def caret(cell, col):
            return Line(cell.get_corner(DL) + DOWN * 0.08, cell.get_corner(UL) + UP * 0.08, color=col,
                        stroke_width=5)
        good = caret(old[at], YES)
        bad = caret(old[at], NO)
        gl = label(r"B's cursor, \ anchored to the name of the s", font_size=18, color=YES)
        bl = label(rf"stored as an offset: \ {at}", font_size=18, color=NO)
        gl.next_to(good, UP, buff=0.15)
        bl.next_to(bad, DOWN, buff=0.15)
        typed = label(r"A types ``big '' at 4", font_size=18, color=HEAD).next_to(new, RIGHT, buff=0.35)
        pres = wrapped_label(r"\textbf{presence} \ (who is here, \ where each cursor is) \ rides the same "
                             r"connections but is never logged: \ a lost update is replaced by the next", 12.4,
                             font_size=19, color=WHITE).move_to([0, 0.3, 0])
        tiles = VGroup(
            tile(r"operational transformation",
                 r"small operations, \ small documents; \ needs one server to fix the order \ (Jupiter, \ "
                 r"Google Docs)", KERN),
            tile(r"sequence CRDT",
                 r"merges in any order, \ offline or peer to peer \ (Yjs, \ Automerge); \ pays with names and "
                 r"tombstones kept in the document \ (Part 39)", YES),
        ).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Cursors raise the same question. <bookmark mark='a'/> B's cursor sits before the s of sat. Stored as an "
            "offset, eight, it points into cat once A types big in front. <bookmark mark='b'/> Anchored to the name "
            "of the s, it moves with the text. <bookmark mark='c'/> Presence, who is here and where each cursor is, "
            "shares those connections but is never logged: a lost update is replaced by the next. "
            "<bookmark mark='d'/> So which to choose? Transformation keeps operations and documents small, but wants "
            "one server to fix the order. <bookmark mark='e'/> A CRDT merges in any order, offline or peer to peer, "
            "as in Yjs and Automerge, and pays with the names and tombstones the document keeps, as Part 39 "
            "measured."
        ) as vo:
            self.play(FadeIn(head), FadeIn(old))
            vo.wait_until("a")
            self.play(Create(good), Create(bad), FadeIn(gl), FadeIn(bl))
            self.play(ReplacementTransform(old[:4], new[:4]), ReplacementTransform(old[4:], new[8:]),
                      FadeIn(new[4:8]), FadeIn(typed),
                      bad.animate.move_to(caret(new[at], NO)),
                      good.animate.move_to(caret(new[12], YES)), gl.animate.next_to(caret(new[12], YES), UP,
                                                                                   buff=0.15),
                      bl.animate.next_to(caret(new[at], NO), DOWN, buff=0.15), run_time=1.6)
            vo.wait_until("b")
            self.play(Indicate(good, color=YES), Indicate(gl, color=YES))
            vo.wait_until("c")
            self.play(FadeIn(pres))
            vo.wait_until("d")
            self.play(FadeIn(tiles[0], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(tiles[1], shift=UP * 0.15))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN)
