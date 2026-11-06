from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Copies(VoiceoverScene):
    def construct(self):
        card = chapter_card(14, r"Copies, uploads and model instances", r"What carries over to minds that can be "
                            r"copied?", lit=(2008, 2023), part=PART)
        with self.voiceover("Chapter fourteen. Copies, uploads and model instances."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.upload()
        self.instances()
        self.table()
        self.ethics()
        self.forks()
        self.versions()

    def upload(self):
        head = label(r"Uploading", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"emulation", r"Sandberg and Bostrom \ (2008): \ scan a brain at sufficient resolution and run it as "
                           r"software", UNIV),
            (r"gradual", r"replace neurons one by one with functional duplicates: \ Parfit's spectrum, \ run forward",
             PARTC),
            (r"destructive", r"scan and destroy: \ the teletransporter, \ with a computer as Mars", NOM),
            (r"non-destructive", r"the original survives: \ the branch-line case, \ or fission", BAD),
            (r"what matters", r"on Parfit's view, \ continuity by any cause: \ a good upload is survival", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Fission and teleportation were thought experiments; uploading would make them engineering. "
            "<bookmark mark='a'/>Anders Sandberg and Nick Bostrom's roadmap for whole brain emulation: scan a brain "
            "at sufficient resolution, and run the result as software. <bookmark mark='b'/>Done gradually, neuron by "
            "neuron, it is Parfit's spectrum run forwards. <bookmark mark='c'/>Done destructively, it is the "
            "teletransporter, with a computer in place of Mars. <bookmark mark='d'/>Done without destroying the "
            "original, it is the branch-line case, or fission. <bookmark mark='e'/>If Parfit is right that continuity "
            "by any cause is what matters, a faithful upload is as good as survival."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def instances(self):
        head = label(r"One set of weights, \ many instances", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        w = VGroup(RoundedRectangle(width=1.8, height=1.0, corner_radius=0.15, color=ABS, fill_opacity=0.25),
                   label(r"weights", font_size=18, color=ABS)).move_to([-4.6, 0.2, 0])
        w[1].move_to(w[0])
        inst = VGroup()
        for k in range(5):
            b = VGroup(RoundedRectangle(width=1.4, height=0.55, corner_radius=0.1, color=NOM, fill_opacity=0.2),
                       label(r"instance " + str(k + 1), font_size=14, color=NOM))
            b[1].move_to(b[0])
            b.move_to([-1.2, 1.8 - 0.8 * k, 0])
            inst.add(b)
        arrows = VGroup(*[Arrow(w.get_right(), b.get_left(), buff=0.08, color=GREY_B, stroke_width=2,
                                max_tip_length_to_length_ratio=0.15) for b in inst])
        rows = stack([(r"a trained model can run as thousands of simultaneous instances", WHITE),
                      (r"each conversation has its own context, \ and none remembers the others", NOM),
                      (r"fission without an operation: \ branching is the normal case", BAD),
                      (r"`which one is the model?' \ looks like an empty question, \ in Parfit's sense", GOAL)],
                     font_size=19, aligned_edge=LEFT, width=5.8).move_to([3.7, -0.2, 0])
        with self.voiceover(
            "The modern case needs no surgery. <bookmark mark='a'/>A trained language model is a single set of "
            "weights, which can run as thousands of simultaneous instances. <bookmark mark='b'/>Each conversation has "
            "its own context, and no instance remembers the others. <bookmark mark='c'/>That is fission without an "
            "operation: branching is the ordinary condition, not a bizarre exception. <bookmark mark='d'/>Asking which "
            "instance is the model looks like what Parfit called an empty question: every fact can be known, and the "
            "question still has no answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(w))
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowArrow(a) for a in arrows], lag_ratio=0.15),
                      LaggedStart(*[FadeIn(b) for b in inst], lag_ratio=0.15), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def table(self):
        head = label(r"What transfers, \ and what is only analogy", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{feature of the debate}", r"\text{for model instances}"]
        data = [(r"\text{branching continuity}", r"\text{transfers: exactly the structure}", OK),
                (r"\text{no further fact}", r"\text{transfers, if reductionism holds}", OK),
                (r"\text{memory as a criterion}", r"\text{partly: context, not long-term memory}", GOAL),
                (r"\text{a single body or animal}", r"\text{analogy only: no organism}", BAD),
                (r"\text{a subject of experience}", r"\text{unknown: the question of Part 31}", BAD),
                (r"\text{what matters, morally}", r"\text{open: Parts 35 and 42}", GOAL)]
        rows = [[MathTex(a, font_size=22), MathTex(b, font_size=22, color=c)] for a, b, c in data]
        grid = ValueGrid(hd, rows, col_w=[5.0, 6.4], cell_h=0.6, font_size=20).move_to([0, 0.2, 0])
        note = label(r"where the cases differ, \ the label is `analogy'; \ no claim is made that models are persons",
                     font_size=18, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "Which parts of the personal identity debate transfer, and which are only analogy? "
            "<bookmark mark='a'/>Branching continuity transfers exactly. If reductionism is true, so does the absence "
            "of a further fact. <bookmark mark='b'/>Memory transfers only partly: an instance has a context, not a "
            "lifetime of memories. <bookmark mark='c'/>A single body or animal has no counterpart: animalism has "
            "nothing to say here. Whether there is any subject of experience is unknown, the question of Part 31. "
            "<bookmark mark='d'/>And what matters morally is open, for Parts 35 and 42. <bookmark mark='e'/>Where the "
            "cases differ, the right word is analogy. Nothing here claims that models are persons; the point is that "
            "the logic of identity applies to them as it does to ships."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(*grid.cell[0])), FadeIn(VGroup(*grid.cell[1])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*grid.cell[2])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[3])), FadeIn(VGroup(*grid.cell[4])))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*grid.cell[5])))
            vo.wait_until("e")
            self.play(FadeIn(note))
        self.clear_scene()

    def ethics(self):
        head = label(r"Ethics for copyable minds", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"backups", r"if a restore is survival, \ is deleting an unused copy a death?", BAD),
            (r"counting", r"one mind run a thousand times: \ one interest, \ or a thousand? \ \ (Shulman and Bostrom, "
                          r"\ 2021)", GOAL),
            (r"merging", r"instances that rejoin, \ pooling memories: \ fusion, \ the reverse of fission", UNIV),
            (r"responsibility", r"which instance answers for what another instance did? \ Locke's forensic person "
                                r"\ (chapter 9)", NOM),
            (r"onward", r"moral status \ (Part 31); \ population ethics \ (Part 36); \ alignment \ (Part 42)", GREY_A),
        ]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.8, x_text=-2.4, label_size=21)
        with self.voiceover(
            "Copyable minds, if they have interests, would raise new ethical questions. <bookmark mark='a'/>If "
            "restoring from a backup is survival, is deleting an unused copy a death? <bookmark mark='b'/>If one mind "
            "runs a thousand times, does it have one interest or a thousand? Carl Shulman and Nick Bostrom argue that "
            "such questions will need answers. <bookmark mark='c'/>Instances that rejoin, pooling their memories, would "
            "be fusion, the reverse of fission. <bookmark mark='d'/>And which instance answers for what another "
            "instance did? Locke's forensic person returns. <bookmark mark='e'/>Moral status is the subject of Part "
            "31; counting minds, of Part 36; and aligning such systems, of the finale."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def forks(self):
        head = label(r"Forks", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        trunk = Line([-6.0, -0.4, 0], [-3.4, -0.4, 0], color=WHOLE, stroke_width=8)
        up = Line([-3.4, -0.4, 0], [-1.0, 0.8, 0], color=WHOLE, stroke_width=8)
        dn = Line([-3.4, -0.4, 0], [-1.0, -1.6, 0], color=PARTC, stroke_width=8)
        ul = label(r"keeps the name", font_size=16, color=WHOLE).next_to(up.get_end(), RIGHT, buff=0.1)
        dl = label(r"keeps the developers", font_size=16, color=PARTC).next_to(dn.get_end(), RIGHT, buff=0.1)
        rows = stack([(r"open-source projects fork: \ one history, \ two futures", WHITE),
                      (r"which is `the' project? \ the one with the name, \ the community, \ the trademark?", GOAL),
                      (r"communities settle it by convention: \ Nozick's closest continuer, \ in practice", UNIV),
                      (r"and nobody thinks a deep fact was missed: \ Parfit's empty question", OK)],
                     font_size=19, aligned_edge=LEFT, width=6.4).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Software already lives with fission. <bookmark mark='a'/>An open-source project forks: one shared "
            "history, then two futures. <bookmark mark='b'/>Which is the project? The fork that keeps the name, the "
            "one that keeps the developers, or the one with the trademark? <bookmark mark='c'/>Communities settle it "
            "by convention and by weight of continuity, a working version of Nozick's closest continuer. "
            "<bookmark mark='d'/>And nobody thinks a deep fact was missed. When every fact about the code and the "
            "people is known, which one is really the project is Parfit's empty question."
        ) as vo:
            self.play(FadeIn(head), Create(trunk))
            vo.wait_until("a")
            self.play(Create(up), Create(dn), FadeIn(ul), FadeIn(dl), FadeIn(rows[0]))
            for mk, r in zip("bcd", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def versions(self):
        d = load("drift")
        head = label(r"Model versions as ships of Theseus", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        n = d["steps"]
        ax = Axes(x_range=[0, n, 10], y_range=[0, 1, 0.25], x_length=6.0, y_length=3.6,
                  axis_config={"color": GREY_B, "font_size": 18}, x_axis_config={"include_numbers": True},
                  y_axis_config={"include_numbers": True}).move_to([-3.3, -0.5, 0])
        orig = series_plot(ax, d["to_original"], NOM, width=3.5)
        prev = series_plot(ax, d["to_previous"], UNIV, xs=list(range(1, n + 1)), width=3.5)
        xl = label(r"update", font_size=18, color=GREY_A).next_to(ax.x_axis, RIGHT, buff=0.12)
        yl = label(r"cosine similarity", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.1)
        lo = label(r"to the original", font_size=18, color=NOM).next_to(ax.c2p(n, d["final"]), UP,
                                                                        buff=0.3).shift(LEFT * 0.4)
        lp = label(r"to the version before", font_size=18, color=UNIV).next_to(ax.c2p(n, d["to_previous"][-1]),
                                                                             DOWN, buff=0.15).shift(LEFT * 1.2)
        rows = stack([(r"a unit vector in " + f"{d['dim']}" + r" dimensions: \ " + f"{n}" + r" small random "
                       r"updates, \ like rounds of fine-tuning", WHITE),
                      (r"similarity to the original falls below one half by update " + f"{d['below_half_at']}" +
                       r", \ and ends at " + f"{d['final']:.2f}", NOM),
                      (r"each version stays within " + f"{d['min_step']:.2f}" + r" of the last", UNIV),
                      (r"connectedness fades, \ continuity holds: \ Parfit's two relations, \ in weight space", GOAL),
                      (r"`the same model'? \ a version name, \ like a ship's, \ follows continuity and use", OK)],
                     font_size=20, aligned_edge=LEFT, width=5.6).move_to([3.95, -0.4, 0])
        with self.voiceover(
            "One more case, built. A trained model is often updated: fine-tuned, patched, retrained on new data, "
            "while keeping its name. <bookmark mark='a'/>The Reasoner takes a vector of weights in five hundred and "
            "twelve dimensions and applies forty small random updates, one after another. <bookmark mark='b'/>Its "
            "similarity to the original version falls steadily: below one half by the twenty-fourth update, and to "
            "under a third by the end. <bookmark mark='c'/>Yet every version is almost exactly like the one before "
            "it: the similarity between neighbours never drops below ninety-six percent. <bookmark mark='d'/>This is "
            "Parfit's distinction again, in weight space: connectedness to the original fades, while continuity, a "
            "chain of strong overlaps, holds throughout. <bookmark mark='e'/>Is the fortieth version the same model "
            "as the first? Its name follows continuity and use, like the name of a ship whose planks have all been "
            "replaced; and, as with the ship, once every fact about the weights is known, nothing further is left "
            "to discover."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(orig), run_time=2.5)
            self.play(FadeIn(lo), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(prev), run_time=2.0)
            self.play(FadeIn(lp), FadeIn(rows[2]))
            for mk, r in zip("de", rows[3:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
