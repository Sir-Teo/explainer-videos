from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403

TYPE_TEX = {"e": r"e", "t": r"t", "<e,t>": r"\langle e,t\rangle", "<e,<e,t>>": r"\langle e,\langle e,t\rangle\rangle",
            "<<e,t>,t>": r"\langle\langle e,t\rangle,t\rangle",
            "<<e,t>,<<e,t>,t>>": r"\langle\langle e,t\rangle,\langle\langle e,t\rangle,t\rangle\rangle"}


def value_tex(v):
    if v is True or v is False:
        return r"\text{T}" if v else r"\text{F}"
    if isinstance(v, list):
        return r"\{" + ",".join(r"\mathit{" + x + "}" for x in v) + r"\}"
    return r"\mathit{" + str(v) + "}"


def draw_tree(key, x0, x1, y_top, dy, show_values=True):
    tree = M.TREES[key]
    data = load("fragment")[key]
    pos, leaves = tree_layout(tree, x0=x0, x1=x1, y_top=y_top, dy=dy)
    by_path = {n["path"]: n for n in data["nodes"]}
    mobs, edges = {}, VGroup()
    for path, (x, y) in pos.items():
        n = by_path[path]
        if path in leaves:
            word = n["label"]
            t = label(word, font_size=20, color=SPEAK if word.startswith("t") and word[1:].isdigit() else NAME)
        elif n["rule"] == "PA":
            t = MathTex(r"\lambda_{" + n["label"][1:] + "}", font_size=26, color=GOAL)
        else:
            t = MathTex(TYPE_TEX[n["type"]], font_size=20, color=SENSE)
        g = VGroup(t).move_to([x, y, 0])
        if show_values and n["value"] is not None and path not in leaves:
            g.add(MathTex(value_tex(n["value"]), font_size=18, color=REF).next_to(t, DOWN, buff=0.06))
        mobs[path] = g
    for path in pos:
        for suf in ("L", "R", "1"):
            if path + suf in pos:
                edges.add(Line(mobs[path][0].get_bottom(), mobs[path + suf][0].get_top(), color=GREY_C,
                               stroke_width=1.5, buff=0.06))
    return data, mobs, edges


class Parser(VoiceoverScene):
    def construct(self):
        card = chapter_card(10, r"A semantic parser, \ built", r"Can meanings be computed from trees?", lit=(1998,),
                            part=PART)
        with self.voiceover("Chapter ten. A semantic parser, built."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.rules()
        self.swiss()
        self.qr()
        self.scope()

    def rules(self):
        hc = history_card(1998, r"Irene Heim and Angelika Kratzer", r"\textit{Semantics in Generative Grammar}",
                          width=7.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"FA", r"functional application: \ if one daughter is a function on the other's type, \ apply it", SENSE),
            (r"PM", r"predicate modification: \ two properties combine into their conjunction \ (`Swiss linguist')",
             REF),
            (r"PA", r"predicate abstraction: \ a node $\lambda_n$ binds the trace $t_n$ below it, \ making a property",
             GOAL),
            (r"QR", r"quantifier raising: \ move a quantified phrase up, \ leave a trace, \ insert $\lambda_n$", BAD),
        ]
        g = rows_table(rows, top=1.0, gap=0.5, width=9.6, x_text=-4.8, label_size=26, text_size=21)
        with self.voiceover(
            "Irene Heim and Angelika Kratzer's textbook of 1998 reduced the system to a handful of rules that "
            "interpret a syntax tree from the bottom up. <bookmark mark='a'/>Functional application: if one branch "
            "denotes a function that takes the other's type, apply it. <bookmark mark='b'/>Predicate modification: "
            "two properties side by side, as in Swiss linguist, combine into their conjunction. "
            "<bookmark mark='c'/>Predicate abstraction: a node marked lambda n binds the trace t n beneath it, "
            "turning a sentence with a gap into a property. <bookmark mark='d'/>And quantifier raising, a rule of "
            "syntax: a quantified phrase moves to the top of the sentence, leaving a trace and a lambda behind. The "
            "Reasoner implements all four."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def tree_body(self, vo, key, title, expect, c_at="L"):
        head = label(title, font_size=30, color=CONN).to_edge(UP, buff=0.3)
        data, mobs, edges = draw_tree(key, -6.4, 0.6, 2.3, 1.05)
        assert data["value"] is expect
        panel_head = label(r"the term at the highlighted node", font_size=18, color=GREY_A).move_to([3.9, 1.9, 0])
        leaves = [n for n in data["nodes"] if n["rule"] in ("lexicon", "trace")]
        inner = [n for n in data["nodes"] if n["rule"] not in ("lexicon", "trace")]
        final = MathTex(data["tex"], font_size=26, color=TRUTH)
        if final.width > 6.0:
            final.width = 6.0
        final.move_to([3.9, -1.4, 0])
        verdict = label(r"in the model: \ " + (r"true" if expect else r"false"), font_size=22,
                        color=OK if expect else BAD).next_to(final, DOWN, buff=0.35)
        cur = None
        self.play(FadeIn(head), FadeIn(panel_head))
        vo.wait_until("a")
        self.play(LaggedStart(*[FadeIn(mobs[n["path"]][0]) for n in leaves], lag_ratio=0.15))
        vo.wait_until("b")
        self.play(Create(edges), run_time=1.0)
        for n in inner:
            if n["path"] == c_at:
                vo.wait_until("c")
            term = MathTex(n["tex"], font_size=24, color=SENSE)
            if term.width > 6.0:
                term.width = 6.0
            term.move_to([3.9, 0.6, 0])
            rule = label(n["rule"] + r": \ type $" + TYPE_TEX[n["type"]] + "$", font_size=18,
                         color=GOAL).next_to(term, UP, buff=0.2)
            anims = [FadeIn(mobs[n["path"]]), Indicate(mobs[n["path"]][0], color=TRUTH)]
            if cur is not None:
                anims.append(FadeOut(cur))
            cur = VGroup(term, rule)
            self.play(*anims, FadeIn(cur), run_time=0.9)
        vo.wait_until("d")
        self.play(FadeIn(final), FadeIn(verdict))

    def swiss(self):
        with self.voiceover(
            "Here is the parser on a first sentence: a Swiss linguist smokes. <bookmark mark='a'/>The tree comes from "
            "the syntax. At the leaves, the lexicon supplies a lambda term for each word. <bookmark mark='b'/>The "
            "Reasoner works upward. Swiss and linguist are both properties, so predicate modification makes Swiss "
            "linguist: the property of being both, true here only of Ann. <bookmark mark='c'/>The determiner a takes "
            "that property, and then smokes, by functional application, and beta reduction leaves a formula: there "
            "is an x that is Swiss, a linguist, and smokes. <bookmark mark='d'/>In the model, Ann is all three, so "
            "the sentence is true."
        ) as vo:
            self.tree_body(vo, "a Swiss linguist smokes", r"`A Swiss linguist smokes'", True)
        self.clear_scene()

    def qr(self):
        key = "Ann likes every student (QR)"
        with self.voiceover(
            "Now the sentence that defeated plain function application: Ann likes every student. "
            "<bookmark mark='a'/>Quantifier raising moves every student to the top and leaves a trace, t one, in "
            "object position. <bookmark mark='b'/>Now the types fit. Likes applies to the trace, an individual "
            "variable, then to Ann: Ann likes x one. Predicate abstraction at lambda one turns that into a property: "
            "the things Ann likes. In the model, Bob and Cy. <bookmark mark='c'/>Every student applies to that "
            "property. <bookmark mark='d'/>The result says that every student is liked by Ann. Ann is a student and "
            "does not like herself, so it is false."
        ) as vo:
            self.tree_body(vo, key, r"`Ann likes every student', \ after quantifier raising", False, c_at="")
        self.clear_scene()

    def scope(self):
        head = label(r"`Every student read a book': \ two readings", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        frag = load("fragment")
        s_key, i_key = "every student read a book (surface)", "every student read a book (inverse)"
        sv, iv = frag[s_key], frag[i_key]
        assert sv["value"] is True and iv["value"] is False
        _, mob_s, edg_s = draw_tree(s_key, -6.8, -1.4, 2.2, 0.62, show_values=False)
        _, mob_i, edg_i = draw_tree(i_key, -0.9, 4.5, 2.2, 0.62, show_values=False)
        ts = MathTex(sv["tex"], font_size=22, color=NAME)
        ti = MathTex(iv["tex"], font_size=22, color=SPEAK)
        for t in (ts, ti):
            if t.width > 5.6:
                t.width = 5.6
        ts.move_to([-4.1, -2.0, 0])
        ti.move_to([1.8, -2.0, 0])
        vs = VGroup(tv(True, 26), label(r"each student read some book", font_size=18, color=GREY_A)).arrange(
            RIGHT, buff=0.2).next_to(ts, DOWN, buff=0.2)
        vi = VGroup(tv(False, 26), label(r"no one book was read by all", font_size=18, color=GREY_A)).arrange(
            RIGHT, buff=0.2).next_to(ti, DOWN, buff=0.2)
        model = VGroup()
        reads = sorted(M.SCOPE_MODEL.preds["read"])
        for k, (st, bk) in enumerate(reads):
            a = label(st, font_size=17, color=NAME).move_to([5.6, 1.4 - 0.75 * k, 0])
            b = label(bk, font_size=17, color=REF).move_to([6.6, 1.4 - 0.75 * k, 0])
            model.add(VGroup(a, b, Arrow(a.get_right(), b.get_left(), buff=0.05, color=GREY_B, stroke_width=2,
                                         max_tip_length_to_length_ratio=0.2)))
        mtag = label(r"the model: \ who read what", font_size=16, color=GREY_A).next_to(model, UP, buff=0.15)
        with self.voiceover(
            "Quantifier raising also explains ambiguity. <bookmark mark='a'/>Every student read a book has two "
            "readings. On the surface reading, every student takes wide scope: each student read some book or "
            "other. <bookmark mark='b'/>On the inverse reading, a book takes wide scope: there is one book that every "
            "student read. The two logical forms differ only in which quantifier is raised higher. "
            "<bookmark mark='c'/>In the model, each student read a different book. <bookmark mark='d'/>The Reasoner "
            "computes both: the surface reading is true, the inverse reading false. One string of words, two trees, "
            "two truth values."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*mob_s.values())), Create(edg_s), FadeIn(ts))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*mob_i.values())), Create(edg_i), FadeIn(ti))
            vo.wait_until("c")
            self.play(FadeIn(model), FadeIn(mtag))
            vo.wait_until("d")
            self.play(FadeIn(vs))
            self.play(FadeIn(vi))
        self.clear_scene()
