from __future__ import annotations

from videos.philosophy.philosophy27.common import *  # noqa: F403

PEOPLE = {"godel": (r"Gödel", NAME), "schmidt": (r"Schmidt", REF), "neumann": (r"von Neumann", SENSE)}


class Kripke(VoiceoverScene):
    def construct(self):
        card = chapter_card(5, r"Naming and necessity", r"Do names abbreviate descriptions?", lit=(1970, 1973),
                            part=PART)
        with self.voiceover("Chapter five. Naming and necessity."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.descriptivism()
        self.rigid()
        self.schmidt()
        self.chain()

    def descriptivism(self):
        hc = history_card(1970, r"Saul Kripke", r"`Naming and Necessity', \ lectures at Princeton", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        rows = [
            (r"descriptivism", r"a name means what some description, \ or a cluster of them \ (Searle, \ 1958), \ "
                               r"means: \ `Aristotle' = `the teacher of Alexander, \dots'", NAME),
            (r"the modal argument", r"names and descriptions behave differently in counterfactuals", SENSE),
            (r"the epistemic argument", r"`Aristotle taught Alexander' is not known a priori", WORLD),
            (r"the semantic argument", r"we can refer with a name while the description we attach fits someone "
                                       r"else, \ or no one", REF),
        ]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.6, x_text=-2.4, label_size=22, text_size=21)
        with self.voiceover(
            "In January 1970, in three lectures at Princeton given without notes, Saul Kripke attacked "
            "descriptivism. <bookmark mark='a'/>Descriptivism says a name means what some description means, or, in "
            "John Searle's version of 1958, a cluster of descriptions: Aristotle means the teacher of Alexander, the "
            "author of the Metaphysics, and so on. <bookmark mark='b'/>Kripke gave three arguments against it. The "
            "modal argument: names and descriptions behave differently when we talk about how things might have "
            "been. <bookmark mark='c'/>The epistemic argument: that Aristotle taught Alexander is not something we "
            "know a priori, as we would if it were part of the name's meaning. <bookmark mark='d'/>And the semantic "
            "argument: we can refer with a name even when the description we attach to it fits someone else, or "
            "nobody at all."
        ) as vo:
            self.play(FadeIn(hc))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def rigid(self):
        d = load("rigid")
        head = label(r"Rigid designation", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows_d = d["rows"]
        boxes, dots, worlds = VGroup(), {}, []
        for i, r in enumerate(rows_d):
            x = -5.1 + 3.4 * i
            box = RoundedRectangle(width=3.0, height=2.0, corner_radius=0.15, color=WORLD).move_to([x, 0.0, 0])
            wt = label(r["world"].replace("Godel", "Gödel"), font_size=16, color=WORLD).next_to(box, UP, buff=0.08)
            if wt.width > 3.0:
                wt.width = 3.0
            ds = {}
            for j, (p, (nm, col)) in enumerate(PEOPLE.items()):
                dt = Dot([x - 0.9 + 0.9 * j, -0.1, 0], radius=0.11, color=col)
                ds[p] = VGroup(dt, label(nm, font_size=14, color=col).next_to(dt, DOWN, buff=0.08))
            boxes.add(VGroup(box, wt, *ds.values()))
            dots[i] = ds
            worlds.append(r)
        name_lab = label(r"the name `Gödel'", font_size=22, color=NAME).move_to([-5.4, 2.4, 0])
        desc_lab = label(r"`the man who proved the incompleteness of arithmetic'", font_size=22, color=REF).move_to(
            [0.5, -2.3, 0])
        name_arrows = VGroup(*[Arrow(name_lab.get_bottom() + RIGHT * 0.1 * i, dots[i]["godel"][0].get_center(),
                                     buff=0.15, color=NAME, stroke_width=2.5, max_tip_length_to_length_ratio=0.06)
                               for i in range(len(worlds))])
        desc_arrows = VGroup()
        for i, r in enumerate(worlds):
            if r["description"] is None:
                desc_arrows.add(Cross(scale_factor=0.18, stroke_color=BAD).move_to(boxes[i][0].get_bottom() + UP * 0.3))
            else:
                desc_arrows.add(Arrow(desc_lab.get_top(), dots[i][r["description"]][0].get_center(), buff=0.15,
                                      color=REF, stroke_width=2.5, max_tip_length_to_length_ratio=0.06))
        assert d["name_rigid"] and not d["description_rigid"]
        assert d["godel_might_not_have"] and d["prover_de_re"] and not d["prover_de_dicto"]
        foot = stack([(r"`Gödel might not have proved it': \ true", OK),
                      (r"`the prover might not have proved it', \ read de dicto: \ false", BAD)], font_size=20,
                     buff=0.15).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The modal argument rests on a notion Kripke made precise. <bookmark mark='a'/>Picture four possible "
            "worlds: the actual one, as Kripke's story will have it; one where things went as we believe; one where "
            "Gödel became a lawyer and von Neumann proved the theorem; and one where nobody did. "
            "<bookmark mark='b'/>The name Gödel picks out the same man in every world. It is a rigid designator. "
            "<bookmark mark='c'/>The description, the man who proved the incompleteness of arithmetic, picks out "
            "whoever proved it in each world, or nobody. It is not rigid. <bookmark mark='d'/>So Gödel might not "
            "have proved the theorem is true. But if Gödel meant the man who proved it, that sentence would mean the "
            "man who proved it might not have proved it, which, read de dicto, is false. The name cannot mean the "
            "description."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(name_lab), LaggedStart(*[GrowArrow(a) for a in name_arrows], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(desc_lab), LaggedStart(*[GrowArrow(a) if isinstance(a, Arrow) else FadeIn(a)
                                                     for a in desc_arrows], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(foot[0]))
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def schmidt(self):
        d = load("rigid")
        head = label(r"Gödel and Schmidt", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        assert d["actual_description_refers_to"] == "schmidt"
        rows = [
            (r"the story", r"suppose an unknown man, \ Schmidt, \ actually proved the theorem, \ and Gödel took the "
                           r"credit", REF),
            (r"descriptivism says", r"`Gödel' then refers to Schmidt, \ since he fits the description", BAD),
            (r"but", r"when we say `Gödel' we still mean Gödel, \ the fraud", OK),
            (r"Feynman", r"most who use the name know only `a famous physicist': \ no description singles him out; "
                         r"\ they still refer to him", SPEAK),
            (r"the necessary a posteriori", r"names are rigid, \ so if Hesperus is Phosphorus, \ it is so in every "
                                            r"world: \ necessary, \ yet discovered", GOAL),
        ]
        g = rows_table(rows, top=1.7, gap=0.45, width=8.4, x_text=-2.2, label_size=22, text_size=21)
        with self.voiceover(
            "The semantic argument is a story. <bookmark mark='a'/>Suppose the incompleteness theorem was actually "
            "proved by an unknown man called Schmidt, whose body was found in Vienna, and Gödel got hold of the "
            "manuscript and took the credit. <bookmark mark='b'/>If the name Gödel meant the man who proved "
            "incompleteness, then when we say Gödel we would be talking about Schmidt. <bookmark mark='c'/>But we "
            "would not. We would be talking about Gödel, the fraud. <bookmark mark='d'/>Kripke's other example: most "
            "people who use the name Feynman know only that he was a famous physicist, a description that fits many "
            "people. They still refer to Feynman. <bookmark mark='e'/>And the payoff for Frege's puzzle: since names "
            "are rigid, if Hesperus is Phosphorus, it is so in every possible world. The identity is necessary, and "
            "yet it was discovered by observation. Kripke separated what is necessary from what is known a priori."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def chain(self):
        head = label(r"The causal-historical picture", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        pts = [np.array([x, y, 0]) for x, y in ((-5.6, 0.8), (-3.8, 1.4), (-3.6, 0.0), (-1.8, 0.9), (-1.6, -0.5),
                                                (0.2, 0.3), (0.4, 1.6), (2.0, -0.2))]
        nodes = VGroup(*[Dot(p, radius=0.11, color=SPEAK if i else TRUTH) for i, p in enumerate(pts)])
        links = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (3, 6), (4, 7)]
        arrows = VGroup(*[Arrow(pts[a], pts[b], buff=0.13, color=GREY_B, stroke_width=2,
                                max_tip_length_to_length_ratio=0.12) for a, b in links])
        btag = label(r"baptism: \ `this baby is Richard'", font_size=18, color=TRUTH).next_to(nodes[0], DOWN, buff=0.15)
        ctag = label(r"each speaker borrows the name, \ intending to use it as the last one did", font_size=18,
                     color=SPEAK).move_to([-1.6, -1.6, 0])
        side = stack([(r"reference is fixed by a chain of uses, \ not by a description in the head", OK),
                      (r"natural kinds too: \ `water', \ `gold', \ `tiger' \ (chapter 6)", WORLD),
                      (r"Evans \ (1973): \ `Madagascar' first named part of mainland Africa; \ Marco Polo's mistake "
                       r"shifted it to the island", BAD),
                      (r"so chains alone cannot be the whole story: \ what the community now intends matters", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=4.6, buff=0.3).move_to([4.6, 0.2, 0])
        with self.voiceover(
            "In place of descriptivism Kripke offered a picture, not a theory, he insisted. "
            "<bookmark mark='a'/>A name is introduced at a baptism: this baby is Richard, or the star we see there "
            "is Hesperus. <bookmark mark='b'/>Then it passes from speaker to speaker. Each borrows it, intending to "
            "refer to whatever the person they learned it from referred to. <bookmark mark='c'/>Reference is fixed by "
            "that chain of uses, not by a description in anyone's head. <bookmark mark='d'/>Kripke extended the "
            "picture to natural kind terms like water and gold, which the next chapter takes up. "
            "<bookmark mark='e'/>Gareth Evans found a problem in 1973. Madagascar was, apparently, a native name for "
            "part of the African mainland; Marco Polo, mistaking what he heard, applied it to the island, and the "
            "island is what it names now. <bookmark mark='f'/>So the chain alone does not fix reference. What a "
            "community now uses a name to talk about can override where the chain began."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(nodes[0], scale=1.5), FadeIn(btag))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(arrows[k]), FadeIn(nodes[links[k][1]]))
                                    for k in range(len(links))], lag_ratio=0.3), FadeIn(ctag), run_time=3)
            for mk, r in zip("cdef", side):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
