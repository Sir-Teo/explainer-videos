from __future__ import annotations

from videos.philosophy.philosophy19.common import *  # noqa: F403


class Species(VoiceoverScene):
    def construct(self):
        card = chapter_card(9, r"Species and trees", r"Are species natural kinds, \ or individuals?", lit=(1942, 1974),
                            part=PART)
        with self.voiceover("Chapter nine. Species and trees."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.concepts()
        self.ring()
        self.tree()
        self.kinds()

    def concepts(self):
        head = label(r"The species problem", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"biological \ (Mayr, \ 1942)", r"groups of interbreeding populations, \ reproductively isolated from "
                                             r"others", GENE),
            (r"morphological", r"organisms that look alike: \ the museum taxonomist's working concept", ORG),
            (r"ecological", r"lineages occupying the same adaptive zone", ALT),
            (r"phylogenetic", r"the smallest diagnosable cluster with a common ancestry", GROUP),
            (r"the count", r"Mayden \ (1997) \ listed twenty-two concepts in use", BAD),
            (r"Ghiselin \ (1974), \ Hull", r"species are not kinds but \textit{individuals}: \ spatiotemporally "
                                           r"bounded lineages, \ with births and deaths", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.2, x_text=-2.0, label_size=20)
        with self.voiceover(
            "What is a species? <bookmark mark='a'/>Ernst Mayr's biological species concept: groups of interbreeding "
            "populations, reproductively isolated from other such groups. <bookmark mark='b'/>The morphological "
            "concept, used in practice by museum taxonomists: organisms that look alike. <bookmark mark='c'/>The "
            "ecological concept: lineages that occupy the same adaptive zone. <bookmark mark='d'/>The phylogenetic "
            "concept: the smallest diagnosable cluster of organisms sharing a common ancestry. "
            "<bookmark mark='e'/>Richard Mayden counted twenty-two concepts in use. <bookmark mark='f'/>Michael "
            "Ghiselin and David Hull drew a metaphysical moral: species are not kinds, like gold, defined by an "
            "essence, but individuals: lineages with a beginning and an end, of which organisms are parts, not "
            "members."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def ring(self):
        head = label(r"A ring species: \ the greenish warbler", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        centre = np.array([-3.0, -0.3, 0])
        plateau = Ellipse(width=2.4, height=1.6, color=GREY_D, fill_opacity=0.2).move_to(centre)
        pl = label(r"Tibetan plateau", font_size=16, color=GREY_A).move_to(centre)
        n = 9
        dots = VGroup()
        for i in range(n):
            a = -PI / 2 + 0.25 + i * (2 * PI - 0.5) / (n - 1)
            col = interpolate_color(ManimColor(GENE), ManimColor(ALT), i / (n - 1))
            dots.add(Dot(centre + np.array([2.4 * np.cos(a), 1.7 * np.sin(a), 0]), radius=0.14, color=col))
        links = VGroup(*[Line(dots[i].get_center(), dots[i + 1].get_center(), color=GREY_B, stroke_width=2)
                         for i in range(n - 1)])
        gap = DashedLine(dots[0].get_center(), dots[-1].get_center(), color=BAD)
        gl = label(r"no interbreeding", font_size=16, color=BAD).next_to(gap, DOWN, buff=0.1)
        rows = stack([(r"neighbouring populations interbreed all the way round", WHITE),
                      (r"where the two ends meet in Siberia, \ they do not", BAD),
                      (r"`interbreeds with' is not transitive: \ so where is the species boundary?", GOAL),
                      (r"speciation laid out in space instead of time \ (Irwin et al., \ 2001)", GENE)],
                     font_size=20, aligned_edge=LEFT, width=6.2).move_to([3.4, -0.3, 0])
        with self.voiceover(
            "Nature refuses to respect sharp boundaries. <bookmark mark='a'/>Greenish warblers form a ring around "
            "the Tibetan plateau. Each population interbreeds with its neighbours. <bookmark mark='b'/>But where the "
            "two ends of the ring meet, in Siberia, the birds do not interbreed: their songs no longer match. "
            "<bookmark mark='c'/>Interbreeding is not transitive, so the biological species concept gives no answer "
            "about where one species ends. <bookmark mark='d'/>Darren Irwin and colleagues described it as "
            "speciation laid out in space rather than time: the gradual divergence that usually happens over "
            "thousands of generations, visible all at once."
        ) as vo:
            self.play(FadeIn(head), FadeIn(plateau), FadeIn(pl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(dt) for dt in dots], lag_ratio=0.1), Create(links), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(gap), FadeIn(gl), FadeIn(rows[1]))
            for mk, r in zip("cd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def tree(self):
        d = load("tree")
        head = label(r"Cladistics: \ trees by shared novelties \ (Hennig)", font_size=30, color=CONN).to_edge(
            UP, buff=0.3)
        tree = d["tree"]

        def leaves(t):
            return [t] if isinstance(t, str) else leaves(t[0]) + leaves(t[1])

        def depth(t):
            return 0 if isinstance(t, str) else 1 + max(depth(t[0]), depth(t[1]))

        order = leaves(tree)
        x0, dx, y0, dy = -6.3, 0.82, -2.3, 0.62
        pos, lines, branch = {}, VGroup(), {}

        def place(t):
            if isinstance(t, str):
                p_ = np.array([x0 + order.index(t) * dx, y0, 0])
            else:
                a_, b_ = place(t[0]), place(t[1])
                p_ = np.array([(a_[0] + b_[0]) / 2, y0 + dy * depth(t), 0])
                for child, cp in ((t[0], a_), (t[1], b_)):
                    ln = Line(p_, cp, color=GREY_B, stroke_width=2.5)
                    lines.add(ln)
                    branch[tuple(sorted(leaves(child)))] = ln
            pos[tuple(sorted(leaves(t)))] = p_
            return p_

        root = place(tree)
        stem = Line(root, root + UP * 0.35, color=GREY_B, stroke_width=2.5)
        names = VGroup(*[label(t, font_size=16, color=WHITE).next_to(pos[(t,)], DOWN, buff=0.12) for t in order])
        marks = VGroup()
        for c, clade in d["gains"].items():
            ln = branch[tuple(sorted(clade))]
            m = ln.point_from_proportion(0.5)
            tick = Line(m + LEFT * 0.09, m + RIGHT * 0.09, color=GOAL, stroke_width=4)
            tl = label(c, font_size=15, color=GOAL).next_to(m, LEFT if len(clade) > 1 else RIGHT, buff=0.12)
            marks.add(VGroup(tick, tl))
        diap = SurroundingRectangle(VGroup(names[order.index("lizard")], names[order.index("pigeon")]), buff=0.1,
                                    color=ALT, stroke_width=2)
        dl = label(r"birds sit with lizards", font_size=14, color=ALT).next_to(diap, DOWN, buff=0.08)
        sc = d["scores"]
        rows = stack([(r"8 animals, \ 8 characters, \ each present or absent", GREY_A),
                      (r"Fitch parsimony: \ count the changes each tree needs", WHITE),
                      (r"this tree: \ " + f"{sc['nested']}" + r" changes, \ one per character: \ the minimum \ (" +
                       f"{d['min_possible']}" + r")", OK),
                      (r"lizards with mice, \ pigeons with chimps: \ " + f"{sc['alt1']}" + r" changes", BAD),
                      (r"sharks with chimps: \ " + f"{sc['alt2']}" + r" changes", BAD),
                      (r"a group counts only if it holds an ancestor and \textit{all} its descendants", GOAL),
                      (r"so `reptiles' without birds is not a group at all", GOAL)], font_size=20, aligned_edge=LEFT,
                     width=5.6).move_to([3.7, 0.0, 0])
        with self.voiceover(
            "Willi Hennig's cladistics classifies organisms by their branching history. <bookmark mark='a'/>Here "
            "are eight animals, scored for eight characters: jaws, a bony skeleton, four limbs, the amniotic egg, "
            "a skull with two openings behind each eye, feathers, fur and opposable thumbs. "
            "<bookmark mark='b'/>Fitch's algorithm counts how many evolutionary changes a tree needs to explain the "
            "data. <bookmark mark='c'/>On this tree each character arises exactly once, on a single branch, so it "
            "needs eight changes, the minimum possible. <bookmark mark='d'/>Grouping lizards with mice and pigeons "
            "with chimps needs ten; grouping sharks with chimps needs twelve. <bookmark mark='e'/>Cladistics "
            "accepts only groups that contain an ancestor and all its descendants. <bookmark mark='f'/>On the best "
            "tree, birds sit with lizards: they are reptiles that took to the air. So reptiles, as traditionally "
            "defined to leave out the birds, are not a natural group at all."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(names), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(stem), Create(lines), FadeIn(rows[1]), run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(m) for m in marks], lag_ratio=0.25), FadeIn(rows[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), FadeIn(rows[4]))
            vo.wait_until("e")
            self.play(FadeIn(rows[5]))
            vo.wait_until("f")
            self.play(Create(diap), FadeIn(dl), FadeIn(rows[6]))
        self.clear_scene()

    def kinds(self):
        head = label(r"Kinds after all?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the old view", r"a kind has an essence: \ gold is the element with 79 protons", GREY_A),
            (r"Mayr; \ Hull", r"species have no essence: \ variation is the reality, \ the type an abstraction", BAD),
            (r"Boyd \ (1991)", r"homeostatic property clusters: \ properties that co-occur because mechanisms "
                               r"\ (interbreeding, \ shared development) \ hold them together", GENE),
            (r"Okasha \ (2002)", r"relational essentialism: \ membership is fixed by relations, \ such as descent, "
                                 r"\ not intrinsic traits", ORG),
            (r"Kitcher \ (1984); \ Ereshefsky", r"pluralism: \ several species concepts, \ each picking out real "
                                                r"groupings for different questions", GROUP),
            (r"Part 20", r"what makes any kind natural \ (and whether kinds exist at all)", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.42, width=8.4, x_text=-2.4, label_size=20)
        with self.voiceover(
            "If species are individuals, are there any biological kinds? <bookmark mark='a'/>On the traditional "
            "view, a natural kind has an essence: gold is whatever has seventy-nine protons. "
            "<bookmark mark='b'/>Ernst Mayr and David Hull argued that species have no essence. Variation within "
            "them is the reality; the type is an abstraction. <bookmark mark='c'/>Richard Boyd proposed a middle "
            "way: homeostatic property cluster kinds, whose properties tend to occur together because underlying "
            "mechanisms, such as interbreeding and shared development, keep them together. Kinds without sharp "
            "boundaries. <bookmark mark='d'/>Samir Okasha defended relational essentialism: what makes an organism "
            "a member of a species is its relations, such as descent, not its intrinsic traits. "
            "<bookmark mark='e'/>Philip Kitcher and Marc Ereshefsky drew the pluralist conclusion: several species "
            "concepts, each picking out real groupings, for different scientific purposes. "
            "<bookmark mark='f'/>What makes any kind natural is a question for Part 20."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcdef", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
