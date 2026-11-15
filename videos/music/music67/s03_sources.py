from __future__ import annotations

import numpy as np

from videos.music.music67.common import *  # noqa: F403


class Sources(SoundScene):
    def construct(self):
        chapter(self, 2, r"Sources and editions", r"How do you recover a piece when the composer's copy is lost?")
        self.problem()
        self.tradition()
        self.copies()
        self.tree()
        self.heard()
        self.evidence()

    # ------------------------------------------------------------------
    def problem(self):
        items = [
            (r"most early music survives only in copies of copies; \ every scribe made mistakes, \ and later scribes copied them", WHITE),
            (r"Lachmann's method \ (19th century, \ for classical texts): \ shared errors reveal who copied from whom", WHITE),
            (r"build the family tree, \ the stemma; \ then reconstruct the lost original from its branches", WHITE),
            (r"the same mathematics as biology's family trees of species", TUNE),
        ]
        rows_scene(self, r"copies of copies", items,
                   "Most early music survives only in copies of copies, and every scribe made mistakes that later scribes copied. "
                   "<bookmark mark='c'/> Karl Lachmann's method, made for classical texts in the nineteenth century, uses shared "
                   "errors to reveal who copied from whom. <bookmark mark='d'/> Build the family tree, the stemma, then reconstruct "
                   "the lost original from its branches. <bookmark mark='e'/> It is the same mathematics as biology's family trees "
                   "of species.", marks="cde")

    # ------------------------------------------------------------------
    def tradition(self):
        d = load("stemma")
        errs = d["witness_errors"]
        gens = d["gens"]
        bars = VGroup(*[VGroup(Rectangle(width=0.42, height=0.25 * e, stroke_width=0, fill_color=[TUNE, BLUE, EAR, GREY_B][g - 1], fill_opacity=0.85),
                               label(str(e), font_size=13, color=GREY_A)) for e, g in zip(errs, gens)])
        for i, b in enumerate(bars):
            b[0].move_to([-5.4 + 0.6 * i, -1.8 + 0.125 * errs[i], 0])
            b[1].next_to(b[0], UP, buff=0.06)
        key = VGroup(*[label(rf"generation {g}", font_size=15, color=c) for g, c in zip((1, 2, 3, 4), (TUNE, BLUE, EAR, GREY_B))]).arrange(RIGHT, buff=0.5).to_edge(DOWN, buff=0.4)
        head = label(r"a tradition of the Tune, \ simulated", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            f"Monochord simulates one. The Tune, {say(d['n_notes'])} notes, is copied by scribes for four generations, each "
            f"copy misreading about one note in twenty on top of its exemplar's mistakes: {say(d['n_mss'])} manuscripts in all. "
            f"The original is lost, and so are many copies; {say(d['n_survive'])} survive. <bookmark mark='a'/> Here is how "
            f"many notes each survivor gets wrong, from {say(min(errs))} to {say(max(errs))}, coloured by generation: the "
            "later the copy, the more errors it has inherited. Every one of them is wrong somewhere."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.08), run_time=2.0)
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def tree(self):
        d = load("stemma")
        D = np.array(d["D"])
        n = len(D)
        pic = heat_image(-D, -D.max(), 0, width=4.2, height=4.2, smooth=False).move_to(LEFT * 3.6 + DOWN * 0.3)
        lab = label(r"notes on which each pair of copies differ", font_size=15, color=GREY_A).next_to(pic, DOWN, buff=0.2)
        rf = d["rf"]
        side = VGroup(label(r"neighbour joining \ (Saitou and Nei, \ 1987): \ join the closest pair, \ again and again", font_size=18, color=WHITE),
                      label(rf"the true tree has {rf['true_splits']} groupings of the surviving copies", font_size=18, color=WHITE),
                      label(rf"the recovered tree finds {rf['recovered']} of them", font_size=20, color=TUNE),
                      label(r"what it misses: \ copies whose shared ancestor added no error of its own", font_size=16, color=GREY_A)).arrange(DOWN, buff=0.35, aligned_edge=LEFT).move_to(RIGHT * 2.4 + DOWN * 0.3)
        head = label(r"the family tree, \ from the errors", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now forget the history and recover it. <bookmark mark='a'/> Count, for every pair of surviving copies, the notes "
            "on which they differ: copies that share a lost ancestor share its errors, and differ less. <bookmark mark='b'/> "
            "Neighbour joining, a method of Naruya Saitou and Masatoshi Nei from 1987, builds a tree by joining the closest pair "
            f"again and again. <bookmark mark='c'/> The true tree groups the survivors in {say(rf['true_splits'])} ways; the "
            f"recovered tree finds {say(rf['recovered'])} of them. What it misses are copies whose common ancestor made no "
            "mistake of its own, and so left no trace."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(pic), FadeIn(lab))
            vo.wait_until("b")
            self.play(FadeIn(side[0]))
            vo.wait_until("c")
            self.play(FadeIn(side[1:]))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("stemma")
        c = clip("stemma.three")
        boxes = choice_boxes([r"the Tune as written", rf"the worst copy \ ({d['witness_errors'][d['worst']]} notes wrong)", rf"rebuilt \ ({d['majority_errors']} wrong)"],
                             width=3.8, height=0.9, buff=0.35, size=17).move_to(UP * 0.6)
        res = VGroup(label(rf"majority of all {d['n_survive']} copies: \ {d['majority_errors']} notes wrong", font_size=18, color=TUNE),
                     label(rf"one vote for each of the {d['branches']} branches \ (Lachmann's idea): \ {d['branch_errors']} wrong", font_size=18, color=TUNE)).arrange(DOWN, buff=0.25).next_to(boxes, DOWN, buff=0.6)
        head = label(r"an edition, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        card = listen_card(r"The Tune three times: \ as written, \ as the worst surviving copy has it, \ and as rebuilt from all the copies, \ in some order. \ Which is the corrupt copy?", width=9.8)
        with self.voiceover("Your turn. Rebuild the original from the copies, and hear three versions: the Tune as written, the worst surviving copy, and the reconstruction, in some order. Which is the corrupt copy?"):
            self.play(FadeIn(card))
        self.wait(0.8)
        plain = choice_boxes([r"first", r"second", r"third"], width=2.8, buff=0.8).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(head), FadeIn(plain))
        st = d["starts"]
        ks = ["original", "witness", "rebuilt"]
        with self.listen(c) as snd:
            window(snd, r"written, \ copied, \ rebuilt", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, plain[i], st[k], end, buff=0.06)
        self.play(FadeOut(plain), FadeIn(boxes))
        with self.voiceover(
            f"The second was the corrupt copy, {say(d['witness_errors'][d['worst']])} notes wrong; the first was the Tune as "
            "written, and the third the reconstruction. A simple majority of the copies gets {say(d['majority_errors'])} notes wrong. Lachmann's refinement, one vote for "
            "each branch of the tradition so that a prolific branch cannot outvote the rest, gets "
            f"{say(d['branch_errors'])}. Editors of real music face worse: copies that mix two exemplars, scribes who corrected "
            "what they thought were errors, and composers who changed their minds."
        ):
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def evidence(self):
        items = [
            (r"the paper: \ watermarks and chain lines date a sheet, \ and match it to a mill and a year", WHITE),
            (r"the ruling: \ the rastrum that drew the staves leaves a signature of spacings \ (rastrology)", WHITE),
            (r"the hand: \ a scribe's clefs, \ stems and custos identify a copyist across manuscripts", WHITE),
            (r"the print: \ plate numbers and later corrections order the issues of an edition", WHITE),
            (r"a stemma from readings is one witness among these; \ an edition weighs them all", TUNE),
        ]
        rows_scene(self, r"other evidence in the sources", items,
                   "Readings are not the only evidence a source carries. <bookmark mark='b'/> The paper: watermarks and chain lines "
                   "date a sheet and can match it to a mill and a year. <bookmark mark='c'/> The ruling: the rastrum that drew the "
                   "staves leaves a signature in their spacing. <bookmark mark='d'/> The hand: a scribe's clefs and stems identify "
                   "the same copyist across manuscripts. <bookmark mark='e'/> The print: plate numbers and later corrections put "
                   "the issues of an edition in order. <bookmark mark='f'/> A family tree from readings is one witness among these, "
                   "and an edition weighs them all.", marks="bcdef")

    # ------------------------------------------------------------------
    def copies(self):
        d = load("copies")
        c = clip("copies.three")
        boxes = choice_boxes([rf"generation {g}: \ {e} wrong" for g, e in zip(d["gens"], d["errors"])], width=3.6, height=0.9, buff=0.4, size=17).move_to(UP * 0.6)
        note = label(r"the Tune's first phrase, \ as three surviving copies have it", font_size=17, color=GREY_A).next_to(boxes, DOWN, buff=0.6)
        head = label(r"three copies, \ heard", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the first phrase as three surviving copies have it: one from the first generation of copying, one from the second, one from the fourth."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        ks = d["names"]
        with self.listen(c) as snd:
            window(snd, r"three copies", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(ks):
                end = st[ks[i + 1]] - 0.4 if i + 1 < len(ks) else c.duration
                pulse(snd, boxes[i], st[k], end, buff=0.06)
        with self.voiceover(
            f"In this phrase the first two copies happen to be right; their errors fall later in the tune. The fourth-generation "
            f"copy has {say(d['errors'][-1])} notes wrong here, inherited and its own together. A listener who knew only that "
            "copy would hear its errors as the Tune."
        ):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()
