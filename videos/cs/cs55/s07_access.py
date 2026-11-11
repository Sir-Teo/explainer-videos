from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs55.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono


def rights_text(rs) -> str:
    return ", ".join(rs) if rs else r"---"


def access_grid(subjects, objects, cells, cw=2.35, rh=0.62, lw=1.6, size=19):
    """Lampson's matrix: subjects down the side, objects across the top, the rights in each cell.  Returns the group
    with ``.cell[(s, o)]`` (box, text), ``.rows[s]`` and ``.cols[o]`` (the boxes of a row and of a column)."""
    g = VGroup()
    g.cell, g.rows, g.cols = {}, {s: VGroup() for s in subjects}, {o: VGroup() for o in objects}
    g.heads, g.names = VGroup(), VGroup()
    for j, o in enumerate(objects):
        t = mono(o, size=size - 1, color=LAM).move_to([lw + (j + 0.5) * cw, 0, 0])
        g.heads.add(t)
    for i, s in enumerate(subjects):
        y = -(i + 1) * rh
        n = mono(s, size=size - 1, color=DATA).move_to([lw / 2, y, 0])
        g.names.add(n)
        for j, o in enumerate(objects):
            box = Rectangle(width=cw, height=rh, stroke_color=GREY_C, stroke_width=1.2, fill_color=BG,
                            fill_opacity=1).move_to([lw + (j + 0.5) * cw, y, 0])
            rs = cells.get((s, o), [])
            t = label(rights_text(rs), font_size=size, color=WHITE if rs else GREY_D).move_to(box)
            c = VGroup(box, t)
            g.cell[(s, o)] = c
            g.rows[s].add(c)
            g.cols[o].add(c)
            g.add(c)
    g.add(g.heads, g.names)
    return g


def chip(text, color, size=18, w=None, h=0.5):
    t = label(text, font_size=size, color=color)
    box = RoundedRectangle(width=w or t.width + 0.4, height=h, corner_radius=0.08, stroke_color=color,
                           stroke_width=1.8, fill_color=BG, fill_opacity=1)
    t.move_to(box)
    return VGroup(box, t)


class Access(VoiceoverScene):
    def construct(self):
        self.card()
        self.matrix()
        self.slices()
        self.deputy()
        self.lattice()
        self.hru()
        self.undecidable()

    def card(self):
        card = chapter_card(6, r"Access control", r"Who may do what, \ to which thing?", lit=(1971, 1976, 1988),
                            extra=((1971, r"Lampson's matrix"), (1976, r"HRU"), (1988, r"the confused deputy")),
                            part=PART)
        with self.voiceover("Chapter six. Access control."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def matrix(self):
        m = load("access")["matrix"]
        cells = {tuple(k.split("->")): v for k, v in m["matrix"].items()}
        head = label(r"Lampson's access matrix \ (1971)", font_size=36).to_edge(UP, buff=0.3)
        g = access_grid(m["subjects"], m["objects"], cells, cw=2.8, rh=0.74, lw=1.9, size=22)
        g.move_to([0, 0.85, 0])
        sl = label(r"subjects", font_size=18, color=DATA).next_to(g.names, UP, buff=0.25)
        ol = label(r"objects", font_size=18, color=LAM).next_to(g.heads, UP, buff=0.2)
        notes = VGroup(
            wrapped_label(r"the \textbf{protection state}: \ for every subject and every object, \ the rights the "
                          r"one holds over the other", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"a reference monitor consults it on every access \ --- \ Chapter 1's complete mediation",
                          12.4, font_size=21, color=YES),
            wrapped_label(r"a real system has millions of subjects and objects and almost every cell empty, \ so "
                          r"nobody stores the matrix whole", 12.4, font_size=21, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(g, DOWN, buff=0.9)
        self.mat, self.mat_head = g, head
        with self.voiceover(
            "Authentication says who you are; access control decides what you may then do. <bookmark mark='a'/> "
            "Butler Lampson's paper Protection, in 1971, gave the field its picture: a matrix, with subjects such as "
            "users and processes down the side, objects such as files across the top, and in each cell the rights one "
            "holds over the other. <bookmark mark='b'/> A reference monitor consults it on every access. <bookmark "
            "mark='c'/> But real systems have millions of subjects and objects, with almost every cell empty, so no "
            "one stores the matrix whole."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g.heads), FadeIn(g.names), FadeIn(sl), FadeIn(ol))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in g.cell.values()], lag_ratio=0.12), run_time=2.5)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene(g, head)

    def slices(self):
        m = load("access")["matrix"]
        g, old = self.mat, self.mat_head
        head = label(r"Slice it two ways: \ ACLs and capabilities", font_size=36).to_edge(UP, buff=0.3)
        self.play(ReplacementTransform(old, head), g.animate.scale(0.8).move_to([0, 1.45, 0]))
        obj, sub = "payroll.db", "alice"
        acl = m["acls_by_object"][obj]
        caps = m["capabilities_by_subject"][sub]
        acl_lines = VGroup(*[label(rf"\texttt{{{s}}}: \ {rights_text(r)}", font_size=21, color=WHITE)
                             for s, r in acl.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        acl_t = label(rf"ACL of \texttt{{{obj}}}, \ kept with the object", font_size=22, color=LAM)
        acl_card = VGroup(acl_t, acl_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        acl_card.move_to([-3.5, -0.75, 0])
        cap_lines = VGroup(*[label(rf"\texttt{{{o}}}: \ {rights_text(r)}", font_size=21, color=WHITE)
                             for o, r in caps.items()]).arrange(DOWN, aligned_edge=LEFT, buff=0.12)
        cap_t = label(rf"capabilities of \texttt{{{sub}}}, \ held by the subject", font_size=22, color=DATA)
        cap_card = VGroup(cap_t, cap_lines).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        cap_card.move_to([3.4, -0.75, 0])
        col = g.cols[obj]
        row = g.rows[sub]
        colbox = SurroundingRectangle(col, color=LAM, buff=0.03, stroke_width=3)
        rowbox = SurroundingRectangle(row, color=DATA, buff=0.03, stroke_width=3)
        notes = VGroup(
            wrapped_label(r"an \textbf{ACL} answers ``who can touch this file?'': \ Unix permission bits, \ Windows "
                          r"ACLs", 5.8, font_size=20, color=LAM),
            wrapped_label(r"a \textbf{capability} answers ``what can this process reach?'': \ an unforgeable token "
                          r"that names an object and carries the right \ --- \ a file descriptor, \ a key, \ an "
                          r"unguessable URL", 5.8, font_size=20, color=DATA),
            wrapped_label(r"revoking is easy with ACLs, \ delegating is easy with capabilities", 12.4, font_size=21,
                          color=HEAD),
        )
        notes[0].next_to(acl_card, DOWN, buff=0.3).align_to(acl_card, LEFT)
        notes[1].next_to(cap_card, DOWN, buff=0.3).align_to(cap_card, LEFT)
        notes[2].to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So systems store it in slices, and there are two ways to cut. <bookmark mark='a'/> Down a column, kept "
            "with the object: an access-control list, everyone who may touch this file, and how. Unix permission bits "
            "are a compressed one. <bookmark mark='b'/> Along a row, held by the subject: a list of capabilities, "
            "unforgeable tokens that both name an object and carry a right to it, like a file descriptor, which after "
            "the open is checked by possession alone. <bookmark mark='c'/> With lists on objects, revoking is easy; "
            "with tokens in hand, delegating is easy, and so is avoiding a classic mistake."
        ) as vo:
            vo.wait_until("a")
            self.play(Create(colbox))
            self.play(TransformFromCopy(VGroup(*[g.cell[(s, obj)] for s in acl]), acl_lines), FadeIn(acl_t),
                      FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(Create(rowbox))
            self.play(TransformFromCopy(VGroup(*[g.cell[(sub, o)] for o in caps]), cap_lines), FadeIn(cap_t),
                      FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def deputy(self):
        d = load("access")["deputy"]
        amb, cap = d["ambient"], d["capability"]
        head = label(r"The confused deputy \ (Hardy, \ 1988)", font_size=36).to_edge(UP, buff=0.3)

        def row(y, title, color):
            t = label(title, font_size=21, color=color).move_to([0, y + 1.0, 0]).align_to([-6.45, 0, 0], LEFT)
            client = chip(r"client", DATA, w=1.7).move_to([-5.6, y, 0])
            dep = chip(r"compiler service", KERN, w=2.6).move_to([-0.6, y, 0])
            bill = chip(r"\texttt{BILL}", GREY_A, w=1.6).move_to([3.0, y + 0.42, 0])
            dbg = chip(r"\texttt{DEBUG}", GREY_A, w=1.6).move_to([3.0, y - 0.42, 0])
            ask = Arrow(client.get_right(), dep.get_left(), buff=0.06, stroke_width=2.5, color=DATA,
                        max_tip_length_to_length_ratio=0.12)
            al = label(r"``compile; \ debug output to \texttt{BILL}''", font_size=17,
                       color=DATA).move_to([ask.get_x(), y + 0.48, 0])
            return VGroup(t, client, dep, bill, dbg, ask, al)
        r1 = row(1.3, r"ambient authority", NO)
        r2 = row(-1.3, r"capabilities", YES)
        own = label(r"deputy's own rights: \ \texttt{BILL}, \ \texttt{DEBUG}", font_size=16,
                    color=KERN).next_to(r1[2], DOWN, buff=0.12)
        w1 = Arrow(r1[2].get_right(), r1[3].get_left(), buff=0.06, stroke_width=3, color=NO,
                   max_tip_length_to_length_ratio=0.12)
        v1 = label(r"write happens: \ the billing file is overwritten, \ with the deputy's authority" if
                   amb["write_happens"] else r"write refused", font_size=18, color=NO)
        v1.move_to([1.4, r1[1].get_y() - 0.95, 0])
        token = chip(r"cap: \texttt{DEBUG}", YES, size=16, w=1.6).next_to(r2[5], DOWN, buff=0.12)
        w2 = DashedLine(r2[2].get_right(), r2[3].get_left(), buff=0.06, stroke_width=2.5, color=NO)
        cross = Cross(scale_factor=0.18, stroke_color=NO, stroke_width=4).move_to(w2.get_center())
        v2 = label(r"denied: \ the client holds no capability for \texttt{BILL}" if not cap["write_happens"]
                   else r"write happens", font_size=18, color=YES)
        v2.move_to([1.4, r2[1].get_y() - 0.95, 0])
        lesson = wrapped_label(r"ambient authority lets a request borrow the deputy's rights by \textit{naming}; \ a "
                               r"capability binds the right to the designation, \ so it cannot be borrowed", 12.4,
                               font_size=20, color=HEAD).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Norm Hardy described that mistake in 1988, and called it the confused deputy. <bookmark mark='a'/> A "
            "compiler service may write two files of its own, a billing log and its debug output, and a client names "
            "the file for the debug output. <bookmark mark='b'/> With ambient authority the service writes with its "
            "own rights, whatever name it is given, so a client who names the billing file has it overwritten, with "
            "an authority the client never held. Our run does exactly that. <bookmark mark='c'/> With capabilities, "
            "the client must hand over a token for the output file, and it holds one only for its debug file, so the "
            "write is refused. <bookmark mark='d'/> Naming a thing and holding the right to it become one act."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(r1[:5]), FadeIn(own))
            self.play(GrowArrow(r1[5]), FadeIn(r1[6]))
            vo.wait_until("b")
            self.play(GrowArrow(w1))
            self.play(r1[3][0].animate.set_fill(NO, 0.5).set_stroke(NO), FadeIn(v1))
            vo.wait_until("c")
            self.play(FadeIn(r2[:5]), GrowArrow(r2[5]), FadeIn(r2[6]), FadeIn(token))
            self.play(Create(w2), Create(cross), FadeIn(v2))
            vo.wait_until("d")
            self.play(FadeIn(lesson))
        self.wait(0.4)
        self.clear_scene()

    def lattice(self):
        b = load("access")["blp"]
        head = label(r"Bell--LaPadula \ (1973): \ no read up, \ no write down", font_size=36).to_edge(UP, buff=0.3)
        names = [("topsecret", r"top secret"), ("secret", r"secret"), ("confidential", r"confidential"),
                 ("unclassified", r"unclassified")]
        lv = {}
        stack = VGroup()
        for k, (key, nm) in enumerate(names):
            c = [NO, HEAD, KERN, YES][k]
            box = RoundedRectangle(width=2.8, height=0.58, corner_radius=0.08, stroke_color=c, stroke_width=1.8,
                                   fill_color=c, fill_opacity=0.12)
            t = label(nm, font_size=21, color=WHITE).move_to(box)
            lv[key] = VGroup(box, t)
            stack.add(lv[key])
        stack.arrange(DOWN, buff=0.28).move_to([-5.1, 1.3, 0])

        def flow(src, dst, x, color, num):
            """An information flow between two levels, drawn beside the stack at x, numbered."""
            y0, y1 = lv[src].get_y(), lv[dst].get_y()
            a = Arrow([x, y0, 0], [x, y1, 0], buff=0.08, stroke_width=3, color=color,
                      max_tip_length_to_length_ratio=0.15)
            n = label(str(num), font_size=19, color=color).next_to(a, RIGHT, buff=0.05)
            return VGroup(a, n)
        ck = b["checks"]
        lvl = {"secret/ENG": "secret", "unclassified": "unclassified", "topsecret/ENG,OPS": "topsecret",
               "confidential/OPS": "confidential"}
        flows = VGroup()
        for i, c in enumerate(ck):
            s, o = lvl[c["subject"]], lvl[c["object"]]
            src, dst = (o, s) if c["op"] == "read" else (s, o)      # information moves from the read or written
            flows.add(flow(src, dst, -3.4 + 0.5 * i, YES if c["allowed"] else NO, i + 1))
        rows = []
        for i, c in enumerate(ck):
            rows.append([f"{i + 1}", c["subject"].replace("topsecret", "top secret"), c["op"],
                         c["object"].replace("topsecret", "top secret"),
                         r"allowed" if c["allowed"] else r"denied"])
        tab = grid_table([r"", r"subject", r"op", r"object", r"verdict"], rows, widths=[0.4, 1.9, 0.8, 2.6, 1.2],
                         row_h=0.4, font_size=19, mono_cols=(1, 3))
        for i, c in enumerate(ck):
            tab.cells[i + 1][4].set_color(YES if c["allowed"] else NO)
        tab.to_edge(LEFT, buff=0.4).set_y(-1.9)
        der = [MathTex(r"\text{read}(s, o_1)", r"\Rightarrow", r"\lambda(o_1) \le \lambda(s)", font_size=32),
               MathTex(r"\text{write}(s, o_2)", r"\Rightarrow", r"\lambda(s) \le \lambda(o_2)", font_size=32),
               MathTex(r"\lambda(o_1) \le \lambda(s)", r"\le \lambda(o_2)", font_size=32),
               MathTex(r"\lambda(o_1)", r"\le \lambda(o_2)", font_size=32)]
        whys = [r"simple security: \ no read up", r"the $\star$-property: \ no write down",
                r"$s$ copies $o_1$ into $o_2$", r"information only flows up"]
        ladder = VGroup(*[VGroup(e, label(w, font_size=18, color=GREY_A)).arrange(DOWN, buff=0.08)
                          for e, w in zip(der, whys)]).arrange(DOWN, buff=0.18)
        ladder.next_to(head, DOWN, buff=0.35).set_x(3.8)
        cat = wrapped_label(r"labels are a level \textit{and} a set of categories; \ $\le$ is a lattice, \ not a line: "
                            r"\ flow 5 goes up a level and is still denied", 5.4, font_size=18,
                            color=HEAD).next_to(ladder, DOWN, buff=0.35)
        biba = label(r"Biba \ (1977): \ the mirror image, \ for integrity", font_size=17,
                     color=GREY_B).next_to(cat, DOWN, buff=0.25).align_to(cat, LEFT)
        with self.voiceover(
            "Sometimes the rule is about secrecy, not ownership. <bookmark mark='a'/> In 1973 David Bell and Leonard "
            "LaPadula formalised military classification: every subject and object carries a label, a level and a set "
            "of categories. <bookmark mark='b'/> A subject may read only what its label dominates: no read up. "
            "<bookmark mark='c'/> And it may write only to what dominates it: no write down, so a secret process "
            "cannot copy into an unclassified file. <bookmark mark='d'/> Chain the two, and whatever a subject copies "
            "from one object to another moves up, never down. <bookmark mark='e'/> Our checks agree, including one "
            "flow that climbs a level and is still refused, for lack of a category. Biba's model of 1977 is the "
            "mirror image, for integrity."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(x) for x in stack], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(ladder[0]))
            vo.wait_until("c")
            self.play(FadeIn(ladder[1]))
            vo.wait_until("d")
            self.play(TransformFromCopy(VGroup(der[0][2], der[1][2]), der[2]), FadeIn(ladder[2][1]))
            self.play(TransformMatchingTex(der[2].copy(), der[3]), FadeIn(ladder[3][1]))
            vo.wait_until("e")
            self.play(LaggedStart(*[GrowArrow(f[0]) for f in flows], lag_ratio=0.3),
                      LaggedStart(*[FadeIn(f[1]) for f in flows], lag_ratio=0.3), FadeIn(tab), run_time=2.5)
            self.play(FadeIn(cat), FadeIn(biba))
        self.wait(0.4)
        self.clear_scene()

    def hru(self):
        a = load("access")
        leak, safe = a["hru_leak"], a["hru_safe"]
        head = label(r"Can a right ever leak? \ (Harrison, \ Ruzzo \& Ullman, \ 1976)", font_size=36)
        head.to_edge(UP, buff=0.3)
        code = VGroup(
            mono("command grant_read(s, o, t):", 19, color=KERN),
            mono("    if own in M[s, o]: enter read into M[t, o]", 19),
            mono("command grant_own(s, o, t):", 19, color=KERN),
            mono("    if own in M[s, o]: enter own into M[t, o]", 19),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.12).to_corner(UL, buff=0.5).shift(DOWN * 0.9)
        g = access_grid(["alice", "eve"], ["secret"], {("alice", "secret"): ["own", "read"]}, cw=2.6, rh=0.7,
                        lw=1.5, size=21)
        g.next_to(code, DOWN, buff=0.6).align_to(code, LEFT)
        newcell = label(r"read", font_size=21, color=NO).move_to(g.cell[("eve", "secret")])
        q = wrapped_label(r"\textbf{safety}: \ from this start, \ can any sequence of commands enter \textbf{read} "
                          r"into a cell that did not hold it?", 5.6, font_size=20, color=WHITE)
        q.move_to([3.7, 1.6, 0])
        tr = leak["trace"][0].replace("_", r"\_").replace(" ", "")
        r1 = wrapped_label(rf"our breadth-first search: \ a leak after {leak['states_explored']} states, \ "
                           rf"\texttt{{{tr}}}", 5.6, font_size=19, color=NO).next_to(q, DOWN, buff=0.4)
        r2 = wrapped_label(rf"a system whose only command revokes: \ {safe['states_explored']} states, \ no leak", 5.6,
                           font_size=19, color=YES).next_to(r1, DOWN, buff=0.3).align_to(r1, LEFT)
        r3 = wrapped_label(r"the search is \textit{bounded}: \ ``safe'' means no leak within its budget of "
                           r"subjects and objects", 5.6, font_size=19, color=HEAD).next_to(r2, DOWN, buff=0.3)
        r3.align_to(r1, LEFT)
        with self.voiceover(
            "Protection states also change, as owners grant rights. <bookmark mark='a'/> In 1976 Harrison, Ruzzo and "
            "Ullman modelled a system as commands, each a test on the matrix followed by primitive edits. Here an "
            "owner may grant read, and may grant ownership itself. <bookmark mark='b'/> Is it safe? Can any sequence "
            "of commands put read into a cell that lacked it? <bookmark mark='c'/> Our breadth-first search finds a "
            "leak at once: Alice grants Eve read. <bookmark mark='d'/> A system whose only command revokes is safe. "
            "But our search is bounded, so safe means safe within its budget."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(code), FadeIn(g))
            vo.wait_until("b")
            self.play(FadeIn(q))
            vo.wait_until("c")
            self.play(Indicate(code[1], color=NO), FadeIn(newcell), FadeIn(r1))
            vo.wait_until("d")
            self.play(FadeIn(r2))
            self.play(FadeIn(r3))
        self.wait(0.4)
        self.clear_scene()

    def undecidable(self):
        head = label(r"Safety is undecidable \ (Part 25)", font_size=36).to_edge(UP, buff=0.3)
        syms = ["1", "0", "1", "1", "\\_"]
        hpos = 2
        n = len(syms)
        tape = VGroup(*[Square(0.6, stroke_color=GREY_B, stroke_width=1.6) for _ in syms]).arrange(RIGHT, buff=0)
        tape.move_to([-3.4, 1.95, 0])
        tsym = VGroup(*[label(s, font_size=22, color=WHITE).move_to(c) for s, c in zip(syms, tape)])
        hd = VGroup(Triangle(color=HEAD, fill_opacity=1).scale(0.12).rotate(PI), label(r"$q$", font_size=20,
                                                                                         color=HEAD))
        hd.arrange(UP, buff=0.05).next_to(tape[hpos], UP, buff=0.05)
        tl = label(r"a Turing machine's tape \ (illustrative)", font_size=17, color=GREY_B).next_to(tape, DOWN,
                                                                                                    buff=0.15)
        cw = 0.82
        x0, y0 = -5.6, 0.55
        grid = VGroup()
        diag = VGroup()
        owns = VGroup()
        for i in range(n):
            for j in range(n):
                grid.add(Square(cw, stroke_color=GREY_D, stroke_width=1).move_to([x0 + j * cw, y0 - i * cw, 0]))
        for i in range(n):
            txt = syms[i] + (r", $q$" if i == hpos else "")
            diag.add(label(txt, font_size=20, color=HEAD if i == hpos else WHITE).move_to(
                [x0 + i * cw, y0 - i * cw, 0]))
            if i < n - 1:
                owns.add(label(r"own", font_size=16, color=DATA).move_to([x0 + (i + 1) * cw, y0 - i * cw, 0]))
        sub = VGroup(*[label(rf"$s_{i}$", font_size=18, color=DATA).move_to([x0 - cw * 0.85, y0 - i * cw, 0])
                       for i in range(n)])
        notes = VGroup(
            wrapped_label(r"cell $i$ of the tape becomes subject $s_i$; \ its symbol, \ and the state if the head is "
                          r"there, \ sit on the diagonal; \ \textbf{own} links each cell to the next", 6.0,
                          font_size=19, color=WHITE),
            wrapped_label(r"each transition of the machine becomes a command", 6.0, font_size=19, color=KERN),
            wrapped_label(r"the right $q_f$ ever appears \ $\iff$ \ the machine halts: \ a safety decider would "
                          r"decide halting", 6.0, font_size=19, color=NO),
            wrapped_label(r"decidable when each command makes one primitive change \ (mono-operational); \ in "
                          r"practice, \ keep the rules simple enough to analyse", 6.0, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.4, -0.3, 0])
        with self.voiceover(
            "Could a better search always answer? No, and the reason is Part 25. <bookmark mark='a'/> Take any Turing "
            "machine. Make each tape cell a subject, write its symbol, and the state where the head stands, on the "
            "diagonal, and let each cell own the next: the matrix is the tape. <bookmark mark='b'/> Each rule of the "
            "machine becomes a command. <bookmark mark='c'/> The halting state's right appears exactly when the "
            "machine halts, so deciding safety would decide halting. <bookmark mark='d'/> Safety is decidable only "
            "for restricted systems, such as those whose commands each make a single change: a strong argument for "
            "simple protection rules."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tape), FadeIn(tsym), FadeIn(hd), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(grid), FadeIn(sub))
            self.play(*[ReplacementTransform(tsym[i].copy(), diag[i]) for i in range(n)], FadeIn(owns),
                      run_time=1.6)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            vo.wait_until("d")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES, PART, mono)
