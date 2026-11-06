from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403


class Kaplan(VoiceoverScene):
    def construct(self):
        card = chapter_card(7, r"Indexicals and two dimensions", r"What does `I' mean?", lit=(1977, 2003), part=PART)
        with self.voiceover("Chapter seven. Indexicals and two dimensions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.character()
        self.here_now()
        self.matrices()
        self.monsters()

    def character(self):
        hc = history_card(1977, r"David Kaplan", r"`Demonstratives' \ (circulated 1977, \ published 1989)", width=6.6,
                          color=HIST).to_corner(UL, buff=0.3)
        boxes = VGroup()
        items = [(r"context", r"speaker, \ place, \ time, \ world", WORLD), (r"content", r"what is said", SENSE),
                 (r"extension", r"a truth value, \ an object", TRUTH)]
        for i, (a, b, c) in enumerate(items):
            box = RoundedRectangle(width=3.0, height=1.3, corner_radius=0.15, color=c).move_to([-4.4 + 4.4 * i, 0.4, 0])
            t = VGroup(label(a, font_size=24, color=c), label(b, font_size=17, color=GREY_A)).arrange(DOWN, buff=0.12)
            t.move_to(box)
            boxes.add(VGroup(box, t))
        ar = VGroup(Arrow(boxes[0].get_right(), boxes[1].get_left(), color=SENSE, buff=0.1),
                    Arrow(boxes[1].get_right(), boxes[2].get_left(), color=TRUTH, buff=0.1))
        al = VGroup(label(r"character", font_size=20, color=SENSE).next_to(ar[0], UP, buff=0.1),
                    label(r"at a world", font_size=20, color=TRUTH).next_to(ar[1], UP, buff=0.1))
        rows = stack([(r"`I': \ character = the agent of the context; \ content = that very person, \ in every world",
                       NAME),
                      (r"the character is what a competent speaker knows; \ the content is what is said", WHITE),
                      (r"`I' said by Ann and by Ben: \ the same character, \ different contents", REF)], font_size=21,
                     aligned_edge=LEFT, width=12.0, buff=0.26).move_to([0, -1.9, 0])
        with self.voiceover(
            "Words like I, here and now pose a different puzzle: their reference changes from one use to the next, "
            "though their meaning does not. David Kaplan's paper Demonstratives, circulated in 1977, gave the "
            "standard logic of them. <bookmark mark='a'/>A context of use supplies a speaker, a place, a time and a "
            "world. <bookmark mark='b'/>An expression's character is a rule that takes a context to a content, what "
            "is said. <bookmark mark='c'/>And a content, evaluated at a world, gives an extension: an object, or a "
            "truth value. <bookmark mark='d'/>The character of I is: the agent of the context. Its content, in a "
            "context, is that very person, in every world, so I is rigid. <bookmark mark='e'/>The character is what "
            "every competent speaker knows; the content is what a particular utterance says. "
            "<bookmark mark='f'/>When Ann says I am hungry and Ben says I am hungry, the character is the same and "
            "the contents differ."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(FadeIn(boxes[0]))
            vo.wait_until("b")
            self.play(GrowArrow(ar[0]), FadeIn(al[0]), FadeIn(boxes[1]))
            vo.wait_until("c")
            self.play(GrowArrow(ar[1]), FadeIn(al[1]), FadeIn(boxes[2]))
            for mk, r in zip("def", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def here_now(self):
        d = load("kaplan")
        head = label(r"`I am here now'", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        assert d["n_contexts"] == 8 and d["a_priori"] and d["contingent_in"] == 4
        hd = [r"\text{agent}", r"\text{place}", r"\text{time}", r"\text{world}", r"\text{true in its context}",
              r"\text{content true in}"]
        cells = []
        for r in d["rows"]:
            cells.append([label(r["agent"], font_size=19, color=NAME), label(r["place"], font_size=19, color=WORLD),
                          MathTex(str(r["time"]), font_size=22), label(r["world"], font_size=19, color=WORLD),
                          tv(r["true"], 22),
                          label(r", \ ".join(r["content"]), font_size=19, color=OK if r["necessary"] else BAD)])
        grid = ValueGrid(hd, cells, col_w=[1.3, 1.4, 1.0, 1.1, 2.6, 2.6], cell_h=0.38, font_size=18).move_to(
            [-2.0, -0.5, 0])
        side = stack([(r"8 proper contexts: \ the agent is at the place, \ at the time, \ in the world", WHITE),
                      (r"true in every one of them: \ a priori", OK),
                      (r"but in 4 of them, \ what is said is false in the other world: \ contingent", BAD),
                      (r"Kaplan: \ `I am here now' is a logical truth \ that is not necessary", GOAL)], font_size=20,
                     aligned_edge=LEFT, width=3.9, buff=0.28).move_to([5.0, -0.4, 0])
        with self.voiceover(
            "Now the sentence I am here now. <bookmark mark='a'/>The Reasoner builds a small model: two agents, two "
            "places, two times and two worlds, and lists every proper context, one whose agent is at its place at its "
            "time in its world. There are eight. <bookmark mark='b'/>In every one of them, I am here now is true. It "
            "cannot be uttered falsely, so it is knowable a priori. <bookmark mark='c'/>But take the content it "
            "expresses in a context, that this person is at this place at this time, and ask whether it holds in the "
            "other world too. In four of the eight contexts, it does not: I might have been elsewhere. "
            "<bookmark mark='d'/>So I am here now is, in Kaplan's logic, a logical truth that is not necessary. The "
            "a priori and the necessary come apart again, in the opposite direction from Kripke's."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(side[0]), FadeIn(grid.head), Create(grid.rule))
            for r in range(len(cells)):
                self.play(*[FadeIn(c) for c in grid.cell[r][:4]], run_time=0.25)
            vo.wait_until("b")
            self.play(*[FadeIn(grid.cell[r][4]) for r in range(len(cells))], FadeIn(side[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(grid.cell[r][5]) for r in range(len(cells))], FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(side[3]))
        self.clear_scene()

    def matrices(self):
        d = load("twod")
        head = label(r"Two dimensions", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ws = d["worlds"]
        mats = VGroup()
        for k, (s, v) in enumerate(d["sentences"].items()):
            cx = -4.4 + 4.4 * k
            title = label("`" + s.replace("H2O", r"H$_2$O") + "'", font_size=20, color=TRUTH).move_to([cx, 1.9, 0])
            cells = VGroup()
            for i in range(2):
                for j in range(2):
                    sq = Square(0.9, color=GOAL if i == j else GREY_C, stroke_width=3 if i == j else 1.5).move_to(
                        [cx - 0.3 + 0.95 * j, 0.9 - 0.95 * i, 0])
                    cells.add(VGroup(sq, tv(v["matrix"][i][j], 26).move_to(sq)))
            rl = VGroup(*[label(w_, font_size=14, color=WORLD).next_to(cells[2 * i], LEFT, buff=0.1)
                          for i, w_ in enumerate(ws)])
            verdict = stack([(r"a priori" if v["a_priori"] else r"a posteriori", OK if v["a_priori"] else BAD),
                             (r"necessary" if v["necessary"] else r"contingent", OK if v["necessary"] else BAD)],
                            font_size=19, buff=0.1).next_to(cells, DOWN, buff=0.3)
            mats.add(VGroup(title, cells, rl, verdict))
        s = d["sentences"]
        assert s["water = H2O"]["necessary"] and not s["water = H2O"]["a_priori"]
        assert s["water is the watery stuff"]["a_priori"] and not s["water is the watery stuff"]["necessary"]
        key = stack([(r"rows: \ the world taken as actual \ (it fixes what `water' refers to); \ columns: \ the world "
                      r"where the sentence is evaluated", GREY_A),
                     (r"the diagonal decides a priori truth; \ the actual row \ (the top) \ decides necessity", GOAL)],
                    font_size=19, aligned_edge=LEFT, width=12.6, buff=0.2).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "Kaplan's two steps, from context to content and from content to truth, can be drawn as a matrix. "
            "Robert Stalnaker and, later, David Chalmers built on the idea. <bookmark mark='a'/>Each row takes a "
            "world as actual, which fixes what the words refer to; each column evaluates the result at a world. Here "
            "the worlds are Earth and Twin Earth. <bookmark mark='b'/>Water is H2O: if Earth is actual, water is H2O "
            "everywhere, so the top row is all true, and the sentence is necessary. But if Twin Earth is actual, "
            "water is XYZ. The diagonal is not all true, so the sentence is not a priori: necessary, a posteriori. "
            "<bookmark mark='c'/>Water is the watery stuff: the diagonal is all true, since whatever world is actual, "
            "water is the stuff in its lakes. A priori. But the top row is not: had the lakes held XYZ, water, which "
            "is H2O, would not have been the watery stuff. Contingent, a priori. <bookmark mark='d'/>And H2O is H2O "
            "is true everywhere: necessary and a priori."
        ) as vo:
            self.play(FadeIn(head), FadeIn(key[0]))
            vo.wait_until("a")
            self.play(FadeIn(mats[0][0]), FadeIn(mats[0][1]), FadeIn(mats[0][2]))
            vo.wait_until("b")
            self.play(FadeIn(mats[0][3]), FadeIn(key[1]))
            vo.wait_until("c")
            self.play(FadeIn(mats[1]))
            vo.wait_until("d")
            self.play(FadeIn(mats[2]))
        self.clear_scene()

    def monsters(self):
        head = label(r"Monsters", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"Kaplan's thesis", r"no operator of English shifts the context: \ `in some contexts, \ I am hungry' "
                                 r"still means \textit{me}", SENSE),
            (r"monsters", r"operators that would shift it: \ Kaplan said English has none, \ `monsters begat by "
                          r"elegance'", BAD),
            (r"Schlenker \ (2003)", r"in Amharic, \ `John says that I am a hero' can mean that John says \textit{he} "
                                    r"is: \ the first person shifts under `say'", WORLD),
            (r"so", r"whether natural languages contain monsters is an empirical question, \ now studied across many "
                    r"languages", GOAL),
        ]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.8, x_text=-2.6, label_size=22, text_size=21)
        with self.voiceover(
            "Kaplan added a bold claim. <bookmark mark='a'/>No operator in English can shift the context that "
            "indexicals depend on. However you embed I, it refers to the speaker. <bookmark mark='b'/>An operator "
            "that could shift it he called a monster, and he said English has none: monsters, he wrote, begat by "
            "elegance. <bookmark mark='c'/>In 2003 Philippe Schlenker argued that Amharic has them: in a report like "
            "John says that I am a hero, the word for I can refer to John. <bookmark mark='d'/>So whether natural "
            "languages contain monsters turned out to be an empirical question, now studied across many languages."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
