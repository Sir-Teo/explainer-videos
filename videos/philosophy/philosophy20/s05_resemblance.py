from __future__ import annotations

from videos.philosophy.philosophy20.common import *  # noqa: F403


class Resemblance(VoiceoverScene):
    def construct(self):
        card = chapter_card(4, r"Resemblance and its troubles", r"Can properties be classes of resembling things?",
                            lit=(1951, 2002), part=PART)
        with self.voiceover("Chapter four. Resemblance and its troubles."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.idea()
        self.imperfect()
        self.companion()
        self.replies()

    def idea(self):
        head = label(r"Resemblance nominalism", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = stack([(r"take resemblance as primitive: \ two things resemble, \ and that is basic", NOM),
                      (r"a property is a maximal class of things that all resemble one another", WHITE),
                      (r"red things are red because they resemble the red paradigms, \ not because they share redness",
                       GREY_A),
                      (r"Russell \ (1912): \ but then resemblance itself is a universal", BAD),
                      (r"Goodman \ (1951): \ two structural troubles, \ even if resemblance is granted", GOAL)],
                     font_size=21, width=11.6).move_to([0, -0.2, 0])
        with self.voiceover(
            "The nominalist has to say something about agreement in colour. One answer takes resemblance as "
            "primitive. <bookmark mark='a'/>Two things resemble one another, and that is a basic fact, not to be "
            "explained by a shared universal. <bookmark mark='b'/>A property is then a maximal class of things that "
            "all resemble one another. <bookmark mark='c'/>Red things are red because they resemble each other, not "
            "because they share redness. <bookmark mark='d'/>Russell objected that resemblance is then itself a "
            "universal, and the nominalist has not escaped. <bookmark mark='e'/>Nelson Goodman found two deeper, "
            "structural troubles, which survive even if resemblance is granted. The Reasoner computes both."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def _triangle(self, names, objs, center, res_pairs, colors):
        c = np.array(center, float)
        pos = {n: c + 1.3 * np.array([np.cos(PI / 2 + 2 * PI * i / 3), np.sin(PI / 2 + 2 * PI * i / 3), 0])
               for i, n in enumerate(names)}
        dots = VGroup(*[Dot(pos[n], radius=0.16, color=NOM) for n in names])
        labs = VGroup(*[label(n + r": \ " + ", ".join(objs[n]), font_size=18, color=WHITE).next_to(
            pos[n], UP if i == 0 else DOWN, buff=0.2) for i, n in enumerate(names)])
        lines = VGroup(*[Line(pos[a], pos[b], color=colors.get((a, b), GREY_B), stroke_width=3)
                         for a, b in res_pairs])
        return VGroup(lines, dots, labs), pos

    def imperfect(self):
        d = load("goodman")["imperfect"]
        head = label(r"The imperfect community", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        objs = d["objects"]
        names = list(objs)
        pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
        tri, pos = self._triangle(names, objs, [-3.6, -0.2, 0], pairs, {})
        shared = VGroup(*[label(r"$" + (set(objs[a]) & set(objs[b])).pop() + r"$", font_size=20, color=UNIV).move_to(
            (pos[a] + pos[b]) / 2 + 0.3 * normalize(np.cross((pos[b] - pos[a]), OUT))) for a, b in pairs])
        cls = d["classes"]
        hd = [r"\text{maximal resemblance class}", r"\text{a property?}"]
        rows_ = [[MathTex(r"\{" + ", ".join(c) + r"\}", font_size=26, color=NOM),
                  MathTex(r"\text{no: nothing all three share}", font_size=22, color=BAD)] for c in cls]
        grid = ValueGrid(hd, rows_, col_w=[3.8, 4.0], cell_h=0.6, font_size=20).move_to([2.8, 1.2, 0])
        ext = d["extensions"]
        miss = stack([(r"$" + p + r"$: \ $\{" + ", ".join(e) + r"\}$ \ \ not maximal: \ lost", BAD) for p, e in
                      ext.items()], font_size=20, aligned_edge=LEFT).move_to([2.8, -0.9, 0])
        note = label(r"every pair resembles, \ so the three form one class: \ the wrong one", font_size=20,
                     color=GOAL).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "The first trouble is the imperfect community. <bookmark mark='a'/>Three objects: a is F and G, b is G "
            "and H, c is F and H. <bookmark mark='b'/>Every pair shares a property, so every pair resembles. "
            "<bookmark mark='c'/>The Reasoner finds the maximal classes of pairwise resembling things. There is "
            "only one: all three. But no property is common to all three. <bookmark mark='d'/>And the real "
            "properties, F, G and H, each pick out a pair, which is not maximal, so the theory loses them all. "
            "<bookmark mark='e'/>Pairwise resemblance is not enough to make a community."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tri[1]), FadeIn(tri[2]))
            vo.wait_until("b")
            self.play(Create(tri[0]), FadeIn(shared))
            vo.wait_until("c")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(VGroup(*grid.cell[0])))
            vo.wait_until("d")
            self.play(FadeIn(miss))
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.clear_scene()

    def companion(self):
        d = load("goodman")["companionship"]
        head = label(r"Companionship", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        objs = d["objects"]
        names = list(objs)
        pairs = [(a, b) for i, a in enumerate(names) for b in names[i + 1:]]
        tri, pos = self._triangle(names, objs, [-3.6, -0.2, 0], pairs, {})
        ext = d["extensions"]
        rows = stack([(r"every $F$ is a $G$: \ $F = \{" + ", ".join(ext["F"]) + r"\} \subset G = \{" +
                       ", ".join(ext["G"]) + r"\}$", WHITE),
                      (r"maximal resemblance classes: \ $\{" + "\\}, \\ \\{".join(", ".join(c) for c in d["classes"])
                       + r"\}$", NOM),
                      (r"so $F$ is never a resemblance class: \ its members always resemble $f$ too", BAD),
                      (r"a property with a constant companion cannot be told apart from it", GOAL)],
                     font_size=21, aligned_edge=LEFT, width=6.6).move_to([3.1, -0.2, 0])
        with self.voiceover(
            "The second trouble is companionship. <bookmark mark='a'/>Suppose every F is also G, but not every G is "
            "F: here d and e are F and G, and f is only G. <bookmark mark='b'/>The Reasoner finds one maximal "
            "resemblance class, the three things together. <bookmark mark='c'/>The F things, d and e, always resemble "
            "f as well, since they share G with it, so the class of F things is never maximal. "
            "<bookmark mark='d'/>A property whose instances always come with a companion property cannot be "
            "distinguished from it by resemblance alone."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tri[1]), FadeIn(tri[2]))
            vo.wait_until("a")
            self.play(Create(tri[0]), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def replies(self):
        head = label(r"Replies", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Rodriguez-Pereyra \ (2002)", r"resemblance holds between \textit{pairs}: \ a class is a property only if "
                                            r"all its pairs of pairs resemble: \ the imperfect community fails this",
             NOM),
            (r"companionship", r"answered by appeal to possible objects: \ some possible $F$ is not $G$ \ (Lewis's "
                               r"modal realism, \ Part 22)", ABS),
            (r"the cost", r"primitive resemblance, \ and a plenitude of possibilia", BAD),
            (r"trope theory", r"exact resemblance between tropes avoids both troubles, \ but needs tropes", UNIV),
            (r"the pattern", r"every view buys economy in one place with a primitive in another", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.4, x_text=-2.2, label_size=20)
        with self.voiceover(
            "Nominalists have replies. <bookmark mark='a'/>Gonzalo Rodriguez-Pereyra makes resemblance hold between "
            "pairs of things, and requires that a property class be one whose pairs all resemble one another as "
            "pairs. The imperfect community fails that test. <bookmark mark='b'/>For companionship he appeals to "
            "merely possible objects: somewhere there is a possible F that is not G, so the classes differ. "
            "<bookmark mark='c'/>The price is primitive resemblance, and the possible worlds of Part 22. "
            "<bookmark mark='d'/>Trope theory avoids both troubles, since tropes resemble exactly or not at all, but "
            "it pays in tropes. <bookmark mark='e'/>The pattern recurs throughout ontology: every view buys economy "
            "in one place with a primitive somewhere else."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
