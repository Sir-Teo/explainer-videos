from __future__ import annotations

import numpy as np

from videos.music.music47.common import *  # noqa: F403

SHORT = {"the Tune": r"the Tune", "Alphabet Song": r"Alphabet", "Baa, Baa, Black Sheep": r"Baa, \ Baa", "Frère Jacques": r"Fr\`ere Jacques",
         "Mary Had a Little Lamb": r"Mary", "London Bridge": r"London Bridge", "Yankee Doodle": r"Yankee Doodle",
         "Hot Cross Buns": r"Hot Cross Buns", "Au clair de la lune": r"Au clair", "Lightly Row (Hänschen klein)": r"H\"anschen klein",
         "Alle meine Entchen": r"Alle meine Entchen"}


class Families(SoundScene):
    def construct(self):
        chapter(self, 7, r"Tune families", r"Can we draw a tune's family tree?")
        self.bayard()
        self.hear()
        self.alignment()
        self.relatives()
        self.simulated()
        self.savage()

    # ------------------------------------------------------------------
    def bayard(self):
        items = [
            (r"Samuel Bayard \ (1950): \ a tune family is a set of melodies descended from one ancestor by singing and copying", WHITE),
            (r"the Tune is a family: \ `Ah! \ vous dirai-je, \ maman', \ `Twinkle, \ Twinkle', \ the Alphabet Song, \ `Baa, \ Baa, \ Black Sheep'", WHITE),
            (r"`Morgen kommt der Weihnachtsmann' in German, \ `Altijd is Kortjakje ziek' in Dutch; \ Mozart's variations \ (Part 26)", WHITE),
            (r"members share an outline but differ in rhythm, \ ornament and words", TUNE),
            (r"to measure kinship we need a distance between melodies", GREY_A),
        ]
        rows_scene(self, r"one ancestor, \ many descendants", items,
                   "Tunes that travel this way form families. <bookmark mark='b'/> In 1950 the folklorist Samuel Bayard defined "
                   "a tune family as a set of melodies descended from one ancestor by singing and copying. "
                   "<bookmark mark='c'/> The Tune is one: Ah! vous dirai-je, maman; Twinkle, Twinkle, Little Star; the Alphabet "
                   "Song; Baa, Baa, Black Sheep. <bookmark mark='d'/> Morgen kommt der Weihnachtsmann in German, Altijd is "
                   "Kortjakje ziek in Dutch, and Mozart's variations, from Part 26. <bookmark mark='e'/> Members share an "
                   "outline but differ in rhythm, ornament and words. <bookmark mark='f'/> To measure kinship, we need a "
                   "distance between melodies.", marks="bcdef")

    # ------------------------------------------------------------------
    def hear(self):
        d = load("relatives")
        c = clip("relatives.three")
        from videos.music.music47.compute import ALPHABET, BAA_BAA, TUNE_MEL, as_mel
        from explainer.music.monochord import melody as M
        mels = [TUNE_MEL[:7], as_mel(M.parse(ALPHABET))[:7], as_mel(M.parse(BAA_BAA))[:9]]
        rolls = VGroup()
        for i, (m, n) in enumerate(zip(mels, (r"the Tune", r"the Alphabet Song", r"Baa, \ Baa, \ Black Sheep"))):
            r = mroll(mel_notes(m, base=60), width=1.2 * sum(x[1] for x in m), height=1.0, lo=59, hi=70, color=[TUNE, BLUE, EAR][i])
            rolls.add(VGroup(label(n, font_size=19, color=[TUNE, BLUE, EAR][i]), r).arrange(DOWN, buff=0.15, aligned_edge=LEFT))
        rolls.arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(DOWN * 0.1)
        head = label(r"three relatives: \ the first phrase of each", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the first phrase of three of them: the Tune, the Alphabet Song, and Baa, Baa, Black Sheep."):
            self.play(FadeIn(head), FadeIn(rolls))
        st = d["starts"]
        beat = 0.38
        with self.listen(c) as snd:
            window(snd, r"three relatives", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for key, r, m in zip(("tune", "alphabet", "baa"), rolls, mels):
                on = np.concatenate([[0.0], np.cumsum([x[1] for x in m])[:-1]])
                flash(snd, r[1].notes, [st[key] + beat * o for o in on], hot=WHITE, base=r[0].get_color())
        with self.voiceover(
            "The first phrase of the Alphabet Song is the Tune's, note for note; it is the second phrase where the letters "
            "L, M, N, O come in quick notes. Baa, Baa, Black Sheep splits the Tune's two A's into four quick ones, for "
            "have you any. Same outline, different rhythms: a family resemblance."
        ):
            self.play(Indicate(rolls[2][1], color=EAR, scale_factor=1.03))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def alignment(self):
        from videos.music.music47.compute import BAA_BAA, TUNE_MEL, as_mel
        from explainer.music.monochord import melody as M
        from explainer.music.monochord import origins as O
        a = TUNE_MEL[:14]
        b = as_mel(M.parse(BAA_BAA))[:16]
        r = O.align(a, b)
        names_ = ["C", "C$\\sharp$", "D", "E$\\flat$", "E", "F", "F$\\sharp$", "G", "A$\\flat$", "A", "B$\\flat$", "B"]
        cols = VGroup()
        for i, j in r["pairs"]:
            top = label(names_[int(a[i][0]) % 12] if i is not None else r"--", font_size=26, color=TUNE if i is not None else GREY_B)
            bot = label(names_[int(b[j][0]) % 12] if j is not None else r"--", font_size=26, color=EAR if j is not None else GREY_B)
            same = i is not None and j is not None and abs(a[i][0] - b[j][0]) < 0.5 and abs(np.log(a[i][1] / b[j][1])) < 0.1
            sub = i is not None and j is not None and not same
            mark = label(r"=" if same else (r"$\sim$" if sub else r"gap"), font_size=18, color=GREY_A if same else GOLD if sub else RED)
            cols.add(VGroup(top, mark, bot).arrange(DOWN, buff=0.18))
        cols.arrange(RIGHT, buff=0.32).move_to(UP * 0.5)
        if cols.width > 13:
            cols.set_width(13)
        if cols.width > 11.0:
            cols.set_width(11.0).move_to(UP * 0.5 + RIGHT * 0.8)
        rl = VGroup(label(r"the Tune", font_size=20, color=TUNE).next_to(cols[0][0], LEFT, buff=0.3),
                    label(r"Baa, \ Baa", font_size=20, color=EAR).next_to(cols[0][2], LEFT, buff=0.3))
        rows_ = text_rows([
            (r"line the notes up so the total cost is least: \ a match costs nothing, \ a gap costs 1", WHITE),
            (r"a substitution costs by size: \ a whole tone \ 0.5, \ a doubled length \ 0.5 \ (at most 1.5)", WHITE),
            (rf"dynamic programming finds the best alignment \ (Needleman and Wunsch, \ 1970, \ for proteins): \ here {r['cost']:.1f}, \ or {r['per_note']:.2f} a note", TUNE),
        ], font_size=21).to_edge(DOWN, buff=0.45)
        head = label(r"aligning two melodies, \ as biologists align genes", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Biologists measure kinship between genes by aligning them, and melodies can be aligned the same way. "
            "<bookmark mark='a'/> Write two melodies one above the other, and line the notes up so the total cost is least: "
            "a matching note costs nothing, a gap costs one. <bookmark mark='b'/> A substituted note costs by how far it "
            "moved: a whole tone half a point, a doubled length half a point. <bookmark mark='c'/> Saul Needleman and "
            "Christian Wunsch's dynamic programming, invented in 1970 for proteins, finds the cheapest alignment. For the "
            f"Tune's first two phrases against Baa, Baa's, it costs {say(r['cost'], 1)}, or {say(r['per_note'], 2)} a note: "
            "the four quick notes on have you any meet the Tune's two A's as two halved lengths and two gaps."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cols), FadeIn(rl), FadeIn(ghost(rows_, 0.15)))
            for mark, rr in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(rr))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def relatives(self):
        d = load("relatives")
        cols = {"the Tune": TUNE, "Alphabet Song": TUNE, "Baa, Baa, Black Sheep": TUNE}
        tr = dendro(d["tree"], width=12.0, height=3.4, size=15, labels=SHORT, leaf_colors=cols).move_to(UP * 0.1)
        for t in tr.tags.values():
            t.rotate(0.6).shift(DOWN * 0.15)
        fam = tr.clades.get(frozenset(["the Tune", "Alphabet Song", "Baa, Baa, Black Sheep"]))
        cap = label(r"joined by average alignment cost \ (UPGMA); \ the higher a join, \ the more distant", font_size=16, color=GREY_A).to_edge(DOWN, buff=0.35)
        head = label(r"eleven tunes, \ clustered by alignment", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        D = np.array(d["D"])
        with self.voiceover(
            "Align every pair among eleven tunes: the Tune, its two relatives, and eight unrelated children's songs from the "
            "series' corpus. Then cluster: join the two closest, treat them as one, and repeat. "
            f"<bookmark mark='a'/> The Tune's family comes out as a branch of its own: the Alphabet Song "
            f"{say(D[0, 1], 2)} a note from the Tune, Baa, Baa {say(D[0, 2], 2)}; every other tune is at least "
            f"{say(min(D[0, 3:]), 2)} away. The clustering recovers known similarity in this selected set, without independently proving ancestry or excluding borrowing and convergence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tr), FadeIn(cap))
            vo.wait_until("a")
            if fam is not None:
                self.play(fam.animate.set_stroke(TUNE, width=6))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def simulated(self):
        d = load("family")
        t1 = dendro(d["true"], width=5.2, height=2.4, size=18)
        t2 = dendro(d["built"], width=5.2, height=2.4, size=18)
        true_cl = {frozenset(tree_leaves(x)) for x in self._clades(d["true"])}
        for k, v in t2.clades.items():
            if k in true_cl and len(k) < 8:
                v.set_stroke(TUNE, width=5)
        g = VGroup(VGroup(label(r"the family as it really branched", font_size=19, color=GREY_A), t1).arrange(DOWN, buff=0.35),
                   VGroup(label(r"the tree rebuilt from alignments", font_size=19, color=GREY_A), t2).arrange(DOWN, buff=0.35)).arrange(RIGHT, buff=1.2).move_to(UP * 0.4)
        tr = d["trials"]
        rn = d["random"]
        cap = label(rf"in 20 such families, \ on average {np.mean(tr):.1f} of 6 branchings recovered; \ a random tree of the same shape: \ {np.mean(rn):.1f}",
                    font_size=18, color=WHITE).to_edge(DOWN, buff=0.8)
        verdict = (r"Here it gets every branching right." if d["correct"] == 6 else
                   f"Here it gets {say(d['correct'])} of the six branchings right, in gold.")
        head = label(rf"the Tune handed down a family of singers: \ {d['generations']} along every branch", font_size=24, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Does the method find history when we know the answer? Hand the Tune down a branching family: it splits in two, "
            f"each branch splits again, and again, with {say(d['generations'])} singers along every branch, giving eight "
            "descendants, A to H. <bookmark mark='a'/> On the left, how the family really branched. <bookmark mark='b'/> On "
            f"the right, the tree rebuilt from alignment distances alone. {verdict} <bookmark mark='c'/> Over twenty such "
            f"families it recovers {say(np.mean(tr), 1)} of the six branchings on average, where a random tree would get "
            f"{say(np.mean(rn), 1)}. When it fails, it is usually because the same simplification happened independently in "
            "two branches, which biologists call convergence."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g[0][0]), FadeIn(g[1][0]))
            vo.wait_until("a")
            self.play(FadeIn(t1))
            vo.wait_until("b")
            self.play(FadeIn(t2))
            vo.wait_until("c")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()

    @staticmethod
    def _clades(t):
        out = []
        def walk(x):
            if isinstance(x, (list, tuple)):
                out.append(x)
                walk(x[0])
                walk(x[1])
        walk(t)
        return out

    # ------------------------------------------------------------------
    def savage(self):
        items = [
            (r"Savage and colleagues \ (2022): \ 10,062 folk melodies, \ English-language and Japanese, \ aligned like genes", WHITE),
            (r"328 pairs were close enough to be relatives", WHITE),
            (r"notes on strong beats, \ and above all final notes, \ changed least; \ ornamental notes changed most", WHITE),
            (r"notes were added and dropped more often than replaced, \ the reverse of DNA; \ replacements were mostly to a neighbouring note", TUNE),
            (r"the same in both traditions: \ regularities of musical evolution, \ not of one culture", GREY_A),
        ]
        rows_scene(self, r"evolution in real tune families", items,
                   "The same tools have now been used at scale. <bookmark mark='b'/> In 2022 Savage and colleagues aligned "
                   "10,062 folk melodies, from English-language and Japanese traditions, like genes, <bookmark mark='c'/> and "
                   "found 328 pairs close enough to be relatives. <bookmark mark='d'/> Notes on strong beats, and above all "
                   "final notes, changed least; ornamental notes changed most. <bookmark mark='e'/> Notes were added and dropped "
                   "more often than replaced, the reverse of DNA, and replacements were mostly to a neighbouring note. "
                   "<bookmark mark='f'/> The same held in both traditions: regularities of musical evolution, not of one "
                   "culture. Our simulated singers know nothing of strong beats; real ones protect the notes that matter.", marks="bcdef")
