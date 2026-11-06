from __future__ import annotations

import re

from explainer.cs import *  # noqa: F403
from videos.cs.cs42.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, mono, tag_box

SHOWN = {"green": YES, "grey": GREY_B, "red": NO}       # the example's colour names, drawn in their own colours
WORDS = {1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven", 8: "eight", 9: "nine",
         10: "ten"}


def elements(src):
    """The example page's elements in document order, as (label, parent index); the same order as the
    instrument's walk over the parsed tree."""
    out, stack = [], []
    for m in re.finditer(r"<(/?)([a-z]+)([^>]*)>", src):
        if m.group(1):
            while stack and out[stack[-1]][1] != m.group(2):
                stack.pop()
            stack.pop()
        else:
            a = m.group(3).strip()
            out.append((f"<{m.group(2)}{' ' + a if a else ''}>", m.group(2), stack[-1] if stack else None))
            stack.append(len(out) - 1)
    return [(lab, par) for lab, _, par in out]


def rules_of(css):
    """(selector, declarations) for each rule, in order: one rule per line in the example."""
    out = []
    for ln in css.split("\n"):
        m = re.match(r"\s*([^{]+)\{([^}]*)\}", ln)
        out.append((m.group(1).strip(), m.group(2).strip()))
    return out


def el_tree(els, x0, y0, step=0.5, size=17, color=WHITE):
    """An element outline: boxes indented by depth, with elbow connectors.  Returns (group, boxes)."""
    depth, boxes, g = [], [], VGroup()
    for k, (lab, par) in enumerate(els):
        d = 0 if par is None else depth[par] + 1
        depth.append(d)
        b = tag_box(lab, color=color, size=size, h=0.38)
        b.move_to([x0 + d * 0.55, y0 - k * step, 0], aligned_edge=LEFT)
        boxes.append(b)
        g.add(b)
        if par is not None:
            px = boxes[par].get_left()[0] + 0.18
            g.add(VMobject(stroke_color=GREY_C, stroke_width=1.5).set_points_as_corners(
                [[px, boxes[par].get_bottom()[1], 0], [px, b.get_y(), 0], [b.get_left()[0], b.get_y(), 0]]))
    return g, boxes


def bucket_key(sel):
    """Where an engine files a rule: the rightmost compound's id, else a class, else its tag, else '*'."""
    last = sel.split()[-1]
    ids, cls = re.findall(r"#([\w-]+)", last), re.findall(r"\.([\w-]+)", last)
    tag = re.match(r"^[a-z0-9]+", last)
    return f"#{ids[0]}" if ids else (f".{cls[0]}" if cls else (tag.group(0) if tag else "*"))


def tint(box, col):
    """Recolour a tag box's outline and text (not its fill, which keeps the background)."""
    return AnimationGroup(box[0].animate.set_stroke(col), box[1].animate.set_color(col))


class Css(VoiceoverScene):
    def construct(self):
        self.card()
        self.specificity()
        self.order()
        self.worked()
        self.render_tree()
        self.matching()
        self.buckets()

    def card(self):
        card = chapter_card(3, r"The cascade", r"When several rules disagree, \ which one wins?",
                            lit=(1994, 1996), extra=((1994, r"Lie proposes style sheets"), (1996, r"CSS level 1")),
                            part=PART)
        with self.voiceover("Chapter three. The cascade."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def specificity(self):
        ranked = load("specificity")["ranked"]
        head = label(r"Specificity", font_size=36).to_edge(UP, buff=0.3)
        rows = [[s, f"{a}", f"{b}", f"{c}"] for s, (a, b, c) in ranked]
        tab = grid_table([r"selector", r"ids", r"classes", r"tags"], rows, widths=[3.3, 0.9, 1.2, 0.9], row_h=0.42,
                         font_size=19, mono_cols=(0,))
        tab.move_to([-3.4, -0.25, 0])
        weak = label(r"weakest", font_size=16, color=GREY_B).next_to(tab.cells[1][3], RIGHT, buff=0.3)
        strong = label(r"strongest", font_size=16, color=GREY_B).next_to(tab.cells[-1][3], RIGHT, buff=0.3)
        arrow = Arrow(weak.get_bottom(), strong.get_top(), buff=0.1, stroke_width=2, color=GREY_C,
                      max_tip_length_to_length_ratio=0.05)
        sels = [s for s, _ in ranked]
        r_cls, r_id = sels.index(".a.b.c") + 1, sels.index("#main") + 1
        tie = [k + 1 for k, (s, t) in enumerate(ranked) if [x for _, x in ranked].count(t) > 1]

        def triple(sel, t, col):
            m = MathTex(r"(", f"{t[0]}", r",\,", f"{t[1]}", r",\,", f"{t[2]}", r")", font_size=44, color=col)
            return VGroup(mono(sel, size=18, color=col), m).arrange(RIGHT, buff=0.35)
        tc = triple(".a.b.c", ranked[r_cls - 1][1], LAM)
        ti = triple("#main", ranked[r_id - 1][1], HEAD)
        cmp = VGroup(tc, ti).arrange(DOWN, buff=0.4, aligned_edge=RIGHT).move_to([3.9, 1.6, 0])
        first = VGroup(SurroundingRectangle(tc[1][1], color=WHITE, buff=0.08),
                       SurroundingRectangle(ti[1][1], color=WHITE, buff=0.08))
        notes = VGroup(
            wrapped_label(r"compared like words in a dictionary: \ ids first; \ classes only if the ids tie; \ "
                          r"tags only if both tie", 5.6, font_size=19, color=WHITE),
            wrapped_label(r"so one id outranks any number of classes: \ it is an order on triples, \ not a sum",
                          5.6, font_size=19, color=HEAD),
            wrapped_label(r"an exact tie, \ like \texttt{p.lead} and \texttt{.note p}, \ goes to the rule that comes "
                          r"later", 5.6, font_size=19, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(cmp, DOWN, buff=0.5).set_x(3.9)
        with self.voiceover(
            "When rules disagree about a property, the cascade decides which one wins, and its best-known tool is "
            "specificity. <bookmark mark='a'/> A selector's specificity is three counts: its ids, its classes, and "
            "its tag names. Here are ten selectors, weakest first. <bookmark mark='b'/> The counts are compared like "
            "words in a dictionary: ids first, classes only if the ids tie, tags last. So one id beats any number of "
            "classes. <bookmark mark='c'/> When two selectors tie exactly, like p dot lead and dot note p, the later "
            "rule wins."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0]), tab.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in range(1, len(tab.cells))],
                                  lag_ratio=0.25), FadeIn(weak), FadeIn(strong), GrowArrow(arrow), run_time=3)
            vo.wait_until("b")
            self.play(*[c.animate.set_color(LAM) for c in tab.cells[r_cls]],
                      *[c.animate.set_color(HEAD) for c in tab.cells[r_id]], FadeIn(cmp), FadeIn(notes[0]))
            self.play(Create(first))
            self.play(Indicate(ti[1][1], color=HEAD, scale_factor=1.4), FadeIn(notes[1]))
            vo.wait_until("c")
            self.play(*[c.animate.set_color(YES) for k in tie for c in tab.cells[k]], FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def order(self):
        head = label(r"The cascade's sort key", font_size=36).to_edge(UP, buff=0.3)
        keys = [(r"origin and importance", KERN), (r"specificity", HEAD), (r"order of appearance", LAM)]
        slots = VGroup()
        for t, col in keys:
            r = RoundedRectangle(width=3.6, height=0.8, corner_radius=0.12, stroke_color=col, stroke_width=2,
                                 fill_color=col, fill_opacity=0.12)
            slots.add(VGroup(r, label(t, font_size=22, color=col).move_to(r)))
        slots.arrange(RIGHT, buff=0.75).move_to([0, 1.85, 0])
        then = VGroup(*[label(r"then", font_size=18, color=GREY_B).move_to(
            (slots[k].get_right() + slots[k + 1].get_left()) / 2) for k in range(2)])
        details = [
            [r"normal: \ the browser's defaults, \ then the user's, \ then the author's",
             r"\texttt{!important}: \ the same three, \ reversed",
             r"so a user's important preference beats the page"],
            [r"$(a, b, c)$, \ compared in order", r"a \texttt{style} attribute on the element beats every selector"],
            [r"the later of two equal declarations wins", r"style sheets count in the order they are linked"],
        ]
        cols = VGroup()
        for (t, col), ds, s in zip(keys, details, slots):
            g = VGroup(*[wrapped_label(d, 3.6, font_size=18, color=GREY_A) for d in ds]).arrange(
                DOWN, aligned_edge=LEFT, buff=0.2)
            g.next_to(s, DOWN, buff=0.35).align_to(s, LEFT)
            cols.add(g)
        sort = wrapped_label(r"collect every declaration that matches the element, \ sort by the key, \ and the "
                             r"last one wins", 12.4, font_size=21, color=YES).move_to([0, -1.9, 0])
        newer = wrapped_label(r"newer specifications add cascade layers \ (in browsers since 2022) \ and shadow-tree "
                              r"boundaries to the key; \ the idea is unchanged", 12.4, font_size=19,
                              color=GREY_B).next_to(sort, DOWN, buff=0.3)
        with self.voiceover(
            "Specificity is only part of the cascade's sort key. <bookmark mark='a'/> First comes origin and "
            "importance: the browser's defaults, then the user's style sheet, then the author's, with important "
            "declarations in reverse, so a user's important preferences beat the page. <bookmark mark='b'/> Then "
            "specificity, with a style attribute beating every selector. <bookmark mark='c'/> Then order of "
            "appearance. <bookmark mark='d'/> Sort every matching declaration by that key, and the last one wins. "
            "Cascade layers, in browsers since 2022, add a step, but not a new idea."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s, c in zip("abc", slots, cols):
                vo.wait_until(mk)
                anims = [FadeIn(s, shift=DOWN * 0.15), FadeIn(c)]
                if mk != "a":
                    anims.append(FadeIn(then["abc".index(mk) - 1]))
                self.play(*anims)
            vo.wait_until("d")
            self.play(FadeIn(sort))
            self.play(FadeIn(newer))
        self.wait(0.4)
        self.clear_scene()

    def worked(self):
        sp = load("specificity")
        els = elements(sp["src"])
        assert [lab.split()[0].strip("<>") for lab, _ in els] == [e["tag"] for e in sp["elements"]]
        rules = rules_of(sp["css"])
        head = label(r"The cascade, \ worked through", font_size=36).to_edge(UP, buff=0.3)
        css = VGroup(*[VGroup(mono(f"{k + 1}", size=16, color=GREY_B), mono(ln, size=17, color=WHITE)).arrange(
            RIGHT, buff=0.25) for k, ln in enumerate(sp["css"].split("\n"))]).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.12)
        css.move_to([-6.6, 2.15, 0], aligned_edge=LEFT)
        tree, boxes = el_tree(els, -6.6, 0.75, step=0.5)
        target = next(k for k, e in enumerate(sp["elements"]) if e["matched"] and len(e["matched"]) > 1)
        tel = sp["elements"][target]
        matched = sorted(tel["matched"], key=lambda m: (m[1], m[2]))
        win = {}
        for s, t, o in matched:
            for d in rules[o][1].split(";"):
                if ":" in d:
                    win[d.split(":")[0].strip()] = o
        rows = [[s, rf"$({t[0]}, {t[1]}, {t[2]})$", f"{o + 1}", rules[o][1]] for s, t, o in matched]
        tab = grid_table([r"selector", r"$(a, b, c)$", r"rule", r"declaration"], rows, widths=[2.6, 1.6, 0.8, 2.6],
                         row_h=0.44, font_size=19, mono_cols=(0, 3))
        tab.move_to([2.95, 1.75, 0])
        cap = label(rf"the rules that match \texttt{{{els[target][0][1:-1].replace(' class=', '.')}}}, \ in cascade "
                    r"order", font_size=17, color=GREY_B).next_to(tab, DOWN, buff=0.15)
        strikes, winners = VGroup(), VGroup()
        for r, (s, t, o) in enumerate(matched, start=1):
            prop = rules[o][1].split(":")[0].strip()
            cell = tab.cells[r][3]
            if win[prop] == o:
                winners.add(cell)
            else:
                strikes.add(Line(cell.get_left() + LEFT * 0.05, cell.get_right() + RIGHT * 0.05, color=NO,
                                 stroke_width=3))
        st = tel["style"]
        result = mono("computed: " + "; ".join(f"{k}: {v}" for k, v in st.items()), size=17, color=YES).next_to(
            cap, DOWN, buff=0.3)
        child = next(k for k, (_, p) in enumerate(els) if p == target)
        inh = CurvedArrow(boxes[target].get_right() + RIGHT * 0.05, boxes[child].get_right() + RIGHT * 0.05,
                          angle=-1.6, color=YES, stroke_width=2.5, tip_length=0.15)
        inh_t = label(r"inherited", font_size=17, color=YES).next_to(inh, RIGHT, buff=0.1)
        plain = len(els) - 1
        notes = VGroup(
            wrapped_label(r"\texttt{b} matches no rule, \ but colour and font size are \textbf{inherited}: \ with no "
                          r"value of its own, \ an element takes its parent's", 6.6, font_size=19, color=YES),
            wrapped_label(r"widths, \ borders and margins are not inherited", 6.6, font_size=19, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).move_to([3.3, -2.35, 0])

        def paint(k):
            c = sp["elements"][k]["style"].get("color")
            return tint(boxes[k], SHOWN.get(c, WHITE))
        with self.voiceover(
            "Now a small page with four rules. <bookmark mark='a'/> Four selectors match the paragraph of class lead."
            " Sorted by specificity, then by order, three of them set its colour, and the last, the one with an id, "
            "wins. <bookmark mark='b'/> So the paragraph is green, and from p dot lead it takes a font size of "
            "eighteen pixels. <bookmark mark='c'/> The bold element inside matches no rule, but colour and font size "
            "are inherited: with no value of its own, an element takes its parent's, so the bold word is green too. "
            "<bookmark mark='d'/> The plain paragraph matches only p, and is grey."
        ) as vo:
            self.play(FadeIn(head), FadeIn(css), FadeIn(tree))
            vo.wait_until("a")
            self.play(tint(boxes[target], HEAD), FadeIn(VGroup(*tab.cells[0]), tab.rule), FadeIn(cap))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(1, len(tab.cells))],
                                  lag_ratio=0.4), run_time=2.5)
            self.play(Create(strikes))
            vo.wait_until("b")
            self.play(*[Indicate(w, color=YES) for w in winners], FadeIn(result), paint(target))
            vo.wait_until("c")
            self.play(Create(inh), FadeIn(inh_t), paint(child), FadeIn(notes[0]))
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(paint(plain))
        self.wait(0.4)
        self.clear_scene()

    def render_tree(self):
        sp = load("specificity")
        els = elements(sp["src"])
        rules = rules_of(sp["css"])
        head = label(r"DOM + CSSOM = render tree", font_size=36).to_edge(UP, buff=0.3)
        dom_t = label(r"the DOM", font_size=20, color=DATA).move_to([-4.4, 2.75, 0])
        dom, dboxes = el_tree(els, -6.5, 2.3, step=0.44, size=16, color=DATA)
        om_t = label(r"the CSSOM", font_size=20, color=LAM).move_to([3.6, 2.75, 0])
        sheet = tag_box("style sheet", color=LAM, size=16, h=0.38).move_to([1.0, 2.3, 0], aligned_edge=LEFT)
        rboxes = VGroup(*[VGroup(tag_box(s, color=LAM, size=16, h=0.36), mono(d, size=16, color=GREY_A)).arrange(
            RIGHT, buff=0.2) for s, d in rules]).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        rboxes.next_to(sheet, DOWN, buff=0.12).align_to(sheet, LEFT).shift(RIGHT * 0.55)
        rlinks = VGroup(*[VMobject(stroke_color=GREY_C, stroke_width=1.5).set_points_as_corners(
            [[sheet.get_left()[0] + 0.18, sheet.get_bottom()[1], 0], [sheet.get_left()[0] + 0.18, r.get_y(), 0],
             [r.get_left()[0], r.get_y(), 0]]) for r in rboxes])
        # the render tree: the same elements, each with its computed style
        rt_t = label(r"the render tree: \ every displayed element, \ every property resolved", font_size=20,
                     color=YES).move_to([0, -0.05, 0])
        rt, rtb = el_tree(els, -5.6, -0.55, step=0.46, size=16, color=YES)
        chips = VGroup()
        for k, e in enumerate(sp["elements"]):
            s = "; ".join(f"{p}: {v}" for p, v in e["style"].items()) or "(defaults only)"
            chips.add(mono(s, size=16, color=SHOWN.get(e["style"].get("color"), GREY_B)).move_to(
                [0.6, rtb[k].get_y(), 0], aligned_edge=LEFT))
        note_t = wrapped_label(r"elements not displayed \ (\texttt{display: none}, \ the \texttt{head}) \ get no "
                               r"entry; \ a pseudo-element such as \texttt{::before} gets one the DOM lacks", 12.6,
                               font_size=18, color=GREY_A).to_edge(DOWN, buff=0.2)
        srcs = []
        for k, e in enumerate(sp["elements"]):
            for s, t, o in e["matched"]:
                srcs.append((o, k))
        with self.voiceover(
            "The DOM says what the page contains, <bookmark mark='a'/> and the parsed style sheets form the CSS "
            "object model, the CSSOM. <bookmark mark='b'/> Matching one against the other gives every element its "
            "computed style, and the result is the render tree, which Chrome now calls the layout tree: one entry for"
            " each element that will be drawn. <bookmark mark='c'/> An element with display none gets no entry, and a"
            " pseudo-element such as before gets one that the DOM lacks. Layout works on this tree."
        ) as vo:
            self.play(FadeIn(head), FadeIn(dom_t), FadeIn(dom))
            vo.wait_until("a")
            self.play(FadeIn(om_t), FadeIn(sheet), FadeIn(rboxes), Create(rlinks))
            vo.wait_until("b")
            self.play(FadeIn(rt_t), TransformFromCopy(dom, rt), run_time=1.5)
            ghosts = [rboxes[o][1].copy() for o, _ in srcs]
            self.play(LaggedStart(*[g.animate.move_to(chips[k]).set_opacity(0.2) for g, (_, k) in zip(ghosts, srcs)],
                                  lag_ratio=0.25), run_time=2.5)
            self.remove(*ghosts)
            self.play(*[FadeIn(chips[k]) for k in range(len(chips))])
            vo.wait_until("c")
            self.play(FadeIn(note_t))
        self.wait(0.4)
        self.clear_scene()

    def matching(self):
        m = load("matching")
        head = label(r"Matching right to left", font_size=36).to_edge(UP, buff=0.3)
        comps = VGroup(mono("div", size=22, color=WHITE), mono(".nav", size=22, color=WHITE),
                       mono("a", size=22, color=WHITE)).arrange(RIGHT, buff=0.35).move_to([-4.2, 2.45, 0])
        chain = VGroup(*[tag_box(t, color=DATA, size=17, w=2.2, h=0.42) for t in
                         ("<body>", "<div>", "<ul class=nav>", "<li>", "<a>")]).arrange(DOWN, buff=0.32)
        chain.move_to([-4.6, 0.0, 0])
        links = VGroup(*[Line(chain[k].get_bottom(), chain[k + 1].get_top(), color=GREY_C, stroke_width=1.5)
                         for k in range(4)])
        illus = note(r"illustrative", font_size=16).next_to(chain, DOWN, buff=0.2)
        steps = [(2, 4, True), (1, 3, False), (1, 2, True), (0, 1, True)]
        marks = VGroup(*[label(r"$\checkmark$" if ok else r"$\times$", font_size=26, color=YES if ok else NO)
                         .next_to(chain[n], RIGHT, buff=0.2) for _, n, ok in steps])
        cur = SurroundingRectangle(comps[2], buff=0.06, color=HEAD, stroke_width=2.5)

        def bars(title, d, y):
            vmax = max(d["right_to_left"], d["left_to_right"])
            t = label(title, font_size=18, color=WHITE).move_to([0.3, y, 0], aligned_edge=LEFT)
            g = VGroup(t)
            for k, (key, name, col) in enumerate((("right_to_left", r"right to left", DATA),
                                                  ("left_to_right", r"left to right", LAM))):
                yy = y - 0.5 - k * 0.45
                n = label(name, font_size=16, color=col).move_to([1.95, yy, 0], aligned_edge=RIGHT)
                r = Rectangle(width=3.7 * d[key] / vmax, height=0.3, stroke_width=0, fill_color=col,
                              fill_opacity=0.85).move_to([2.1, yy, 0], aligned_edge=LEFT)
                v = label(f"{d[key]:,}", font_size=17, color=col).next_to(r, RIGHT, buff=0.1)
                g.add(VGroup(n, r, v))
            return g
        pg, rd = m["page"], m["readme"]
        b1 = bars(rf"a synthetic page: \ {pg['elements']:,} elements, \ mean depth {m['mean_depth']:.1f}", pg, 1.9)
        b2 = bars(rf"this series' README: \ {rd['elements']:,} elements, \ shallow", rd, -0.1)
        btitle = label(rf"element tests for {pg['selectors']} selectors", font_size=16, color=GREY_B).next_to(
            b2, DOWN, buff=0.25).align_to(b2, LEFT)
        cap = wrapped_label(r"right to left, \ most elements fail the first test and cost one; \ left to right, \ "
                            r"every element matching the leftmost part searches its whole subtree, \ and deep pages "
                            r"make subtrees large", 12.6, font_size=19, color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "Matching rules to elements is the expensive part of style, and browsers do it backwards. <bookmark "
            "mark='a'/> To test div dot nav a against a link, start at the right: is this element an a? Yes. Then "
            "walk up its ancestors for one of class nav, and above that, a div. <bookmark mark='b'/> Most elements "
            "fail the first test. Left to right would start from every div and search everything below it. <bookmark "
            "mark='c'/> On a synthetic page of two thousand elements, with a mean depth of about "
            f"{m['mean_depth']:.0f}, our ten selectors cost about {pg['right_to_left']/1000:.0f} thousand element "
            f"tests right to left, against {pg['left_to_right']/1000:.0f} thousand left to right. <bookmark mark='d'/>"
            " On this series' shallow README the two are about equal, and left to right is even slightly cheaper: "
            "depth makes the difference."
        ) as vo:
            self.play(FadeIn(head), FadeIn(comps), FadeIn(chain), Create(links), FadeIn(illus))
            vo.wait_until("a")
            self.play(Create(cur))
            hl = SurroundingRectangle(chain[4], buff=0.05, color=HEAD, stroke_width=2.5)
            self.play(Create(hl), FadeIn(marks[0]), comps[2].animate.set_color(YES))
            for (c, n, ok), mk in zip(steps[1:], marks[1:]):
                self.play(cur.animate.surround(comps[c], buff=0.06), hl.animate.surround(chain[n], buff=0.05),
                          run_time=0.6)
                self.play(FadeIn(mk), *([comps[c].animate.set_color(YES)] if ok else []), run_time=0.4)
            self.play(FadeOut(cur), FadeOut(hl))
            vo.wait_until("b")
            self.play(FadeIn(cap))
            vo.wait_until("c")
            self.play(FadeIn(b1[0]), *[GrowFromEdge(r[1], LEFT) for r in b1[1:]],
                      *[FadeIn(r[0]) for r in b1[1:]], *[FadeIn(r[2]) for r in b1[1:]], FadeIn(btitle))
            vo.wait_until("d")
            self.play(FadeIn(b2[0]), *[GrowFromEdge(r[1], LEFT) for r in b2[1:]],
                      *[FadeIn(r[0]) for r in b2[1:]], *[FadeIn(r[2]) for r in b2[1:]])
        self.wait(0.4)
        self.clear_scene()

    def buckets(self):
        ranked = load("specificity")["ranked"]
        sels = [s for s, _ in ranked]
        head = label(r"Hashing the rules", font_size=36).to_edge(UP, buff=0.3)
        table = {}
        for s in sels:
            table.setdefault(bucket_key(s), []).append(s)
        keys = list(table)
        rows = VGroup()
        for k in keys:
            kb = tag_box(k, color=KERN, size=17, w=1.2, h=0.42)
            chips = VGroup(*[tag_box(s, color=DATA, size=16, h=0.38) for s in table[k]]).arrange(RIGHT, buff=0.2)
            chips.next_to(kb, RIGHT, buff=0.45)
            ar = Arrow(kb.get_right(), chips.get_left(), buff=0.05, stroke_width=1.6, color=GREY_C,
                       max_tip_length_to_length_ratio=0.3)
            rows.add(VGroup(kb, ar, chips))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.16).move_to([-6.5, 0.4, 0], aligned_edge=LEFT)
        illus = note(r"illustrative style sheet: \ the ten selectors ranked earlier", font_size=16).next_to(
            rows, DOWN, buff=0.15).align_to(rows, LEFT)
        el = tag_box("<p class=lead>", color=HEAD, size=18, h=0.45).move_to([4.9, 1.9, 0])
        look = ["p", ".lead", "*"]
        lk = VGroup(*[tag_box(k, color=HEAD, size=17, w=1.0, h=0.4) for k in look]).arrange(RIGHT, buff=0.2)
        lk.next_to(el, DOWN, buff=0.5)
        lk_t = label(r"look up its tag, \ its classes, \ $*$", font_size=17, color=GREY_A).next_to(lk, DOWN,
                                                                                                    buff=0.15)
        tried = sum(len(table[k]) for k in look if k in table)
        res = label(rf"{tried} of {len(sels)} rules tried; \ {len(sels) - tried} never looked at", font_size=19,
                    color=YES).next_to(lk_t, DOWN, buff=0.35)
        cap = wrapped_label(r"real engines file rules this way \ (a hash map, \ Part 17), \ and keep a \textbf{Bloom "
                            r"filter} \ (Part 20) \ of the ancestors' ids, \ classes and tags, \ so \texttt{.nav a} "
                            r"can often be rejected without walking up", 12.6, font_size=19,
                            color=GREY_A).to_edge(DOWN, buff=0.25)
        on = [r for k, r in zip(keys, rows) if k in look]
        off = [r for k, r in zip(keys, rows) if k not in look]
        with self.voiceover(
            "Most of those tests are never made, thanks to Part 17's hash maps. <bookmark mark='a'/> Each rule is "
            "filed under the rightmost part of its selector: its id, or else a class, or else its tag. <bookmark "
            "mark='b'/> To style a paragraph of class lead, look up only the buckets for p, for lead, and for the "
            f"universal selector: {WORDS[tried]} of these {WORDS[len(sels)]} rules are tried, and the other "
            f"{WORDS[len(sels)-tried]} are never looked at. <bookmark mark='c'/> Engines also keep a Bloom filter, "
            "from Part 20, of the ancestors' ids, classes and tags, so a selector needing an ancestor of class nav is"
            " often rejected at once."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in rows], lag_ratio=0.25), FadeIn(illus),
                      run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(el))
            self.play(LaggedStart(*[TransformFromCopy(el, b) for b in lk], lag_ratio=0.3), FadeIn(lk_t))
            self.play(*[r.animate.set_opacity(0.25) for r in off],
                      *[r[0][0].animate.set_fill(HEAD, opacity=0.3) for r in on],
                      *[c[0].animate.set_stroke(HEAD) for r in on for c in r[2]])
            self.play(FadeIn(res))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, KERN, LAM)
