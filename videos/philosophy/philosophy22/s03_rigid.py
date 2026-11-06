from __future__ import annotations

from videos.philosophy.philosophy22.common import *  # noqa: F403


class Rigid(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Names and rigid designation", r"Does a name mean a description?", lit=(1970, 1980),
                            part=PART)
        with self.voiceover("Chapter two. Names and rigid designation."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.descriptivism()
        self.modal()
        self.arguments()
        self.chain()

    def descriptivism(self):
        head = label(r"The description theory of names", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        eq = MathTex(r"\text{`Aristotle'} \;=\; \text{`the teacher of Alexander, born in Stagira, \ldots'}",
                     font_size=32, color=DESC).next_to(head, DOWN, buff=0.45)
        rows = [
            (r"Frege, \ Russell", r"a name abbreviates a description, \ which fixes what it refers to", DESC),
            (r"Searle \ (1958)", r"a cluster of descriptions: \ the name refers to whatever satisfies enough of them",
             NAME),
            (r"its virtues", r"why `Hesperus = Phosphorus' is informative \ (different descriptions); \ how we "
                             r"manage to refer at all", OK),
            (r"empty names", r"`Vulcan' \ (the planet inside Mercury's orbit) \ means a description nothing "
                             r"satisfies", GREY_A),
        ]
        g = rows_table(rows, top=1.1, gap=0.45, width=8.6, x_text=-2.4, label_size=21)
        with self.voiceover(
            "What does a proper name mean? <bookmark mark='a'/>The tradition from Frege and Russell answered: a "
            "description. The name Aristotle abbreviates something like the teacher of Alexander the Great, born in "
            "Stagira, who wrote the Metaphysics. <bookmark mark='b'/>The description fixes the reference: the name "
            "refers to whatever satisfies it. <bookmark mark='c'/>John Searle loosened this into a cluster: the name "
            "refers to whatever satisfies enough of the descriptions its users associate with it. "
            "<bookmark mark='d'/>The theory has real virtues. It explains why Hesperus is Phosphorus is informative: "
            "the two names come with different descriptions. And it explains how we manage to refer at all. "
            "<bookmark mark='e'/>It even handles empty names: Vulcan, the planet once posited inside Mercury's "
            "orbit, means a description that nothing satisfies."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Write(eq))
            for mk, r in zip("bcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def modal(self):
        d = load("rigid")
        hc = history_card(1970, r"Saul Kripke", r"\textit{Naming and Necessity}, \ lectures at Princeton", width=6.4,
                          color=HIST).to_corner(UL, buff=0.3)
        W = d["worlds"]
        isl = VGroup()
        nm_marks, ds_marks = VGroup(), VGroup()
        people = ["Aristotle", "Xenocrates", "Speusippus"]
        for i, w in enumerate(W):
            c = np.array([-5.1 + 3.4 * i, -0.2, 0])
            I = island(c, w=2.95, h=2.1, seed=50 + i, color=NAME if w == "@" else WORLD,
                       name=r"actual" if w == "@" else rf"$w_{i}$", font_size=19)
            dots = VGroup()
            pos = {}
            for k, p in enumerate(people):
                pp = c + np.array([-0.95 + 0.95 * k, 0.05 + (0.3 if k == 1 else 0.0), 0])
                pos[p] = pp
                dots.add(person(pp, color=GREY_A, name=p, font_size=15, r=0.11))
            tl = label(r"taught Alexander: \ " + d["desc"][w], font_size=15, color=GREY_A).move_to(c + DOWN * 0.72)
            isl.add(VGroup(I, dots, tl))
            nm_marks.add(Circle(radius=0.2, color=NAME, stroke_width=3).move_to(pos[d["name"][w]]))
            ds_marks.add(Square(side_length=0.36, color=DESC, stroke_width=3).move_to(pos[d["desc"][w]]))
        key = VGroup(VGroup(Circle(radius=0.12, color=NAME, stroke_width=3),
                            label(r"`Aristotle' picks out", font_size=18, color=NAME)).arrange(RIGHT, buff=0.15),
                     VGroup(Square(side_length=0.22, color=DESC, stroke_width=3),
                            label(r"`the teacher of Alexander' picks out", font_size=18, color=DESC)).arrange(
                         RIGHT, buff=0.15)).arrange(RIGHT, buff=0.8).move_to([0, 1.65, 0])
        rows = stack([(r"`Aristotle might not have taught Alexander': \ true", OK),
                      (r"`The teacher of Alexander might not have taught Alexander': \ false \ (read de dicto)", BAD),
                      (r"so `Aristotle' does not mean `the teacher of Alexander'", GOAL),
                      (r"a rigid designator picks out the same object at every world where it exists", NAME)],
                     font_size=20, aligned_edge=LEFT, width=12.4).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "In three lectures at Princeton in January 1970, Saul Kripke attacked the description theory. "
            "<bookmark mark='a'/>Take four worlds. In ours and in w one, Aristotle taught Alexander. In w two, "
            "Xenocrates did; in w three, Speusippus. <bookmark mark='b'/>Follow the name. Aristotle picks out the "
            "same man at every world: Aristotle, whatever he did there. <bookmark mark='c'/>Follow the description. "
            "The teacher of Alexander picks out whoever taught Alexander there: a different man in w two and w three. "
            "<bookmark mark='d'/>Now compare two sentences. Aristotle might not have taught Alexander: true, as w two "
            "shows. The teacher of Alexander might not have taught Alexander: false, read as a claim about whoever "
            "fits the description. <bookmark mark='e'/>Substituting the description for the name changes the truth "
            "value, so the name does not mean the description. <bookmark mark='f'/>Kripke's diagnosis: names are "
            "rigid designators. They designate the same object at every world where it exists. Most descriptions are "
            "not rigid."
        ) as vo:
            self.play(FadeIn(hc))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(g) for g in isl], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(key[0]), LaggedStart(*[Create(m) for m in nm_marks], lag_ratio=0.2))
            vo.wait_until("c")
            self.play(FadeIn(key[1]), LaggedStart(*[Create(m) for m in ds_marks], lag_ratio=0.2))
            vo.wait_until("d")
            self.play(FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
            vo.wait_until("e")
            self.play(FadeIn(rows[2]))
            vo.wait_until("f")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def arguments(self):
        head = label(r"Two more arguments", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
            (r"the epistemic argument", r"`Aristotle, \ if he existed, \ taught Alexander' is not knowable a "
                                        r"priori, \ as it would be if the name meant the description", WORLD),
            (r"Gödel and Schmidt", r"suppose a man named Schmidt proved incompleteness and Gödel stole the proof: "
                                   r"\ `Gödel' would still refer to Gödel", DESC),
            (r"Feynman", r"most speakers know only `a physicist': \ no uniquely identifying description, \ yet they "
                         r"refer to Feynman", NAME),
            (r"the replies", r"rigidified descriptions \ (`the \textit{actual} teacher of Alexander'); \ "
                             r"descriptions of the name's causal history", GREY_A),
        ]
        g = rows_table(rows, top=1.9, gap=0.48, width=8.4, x_text=-2.2, label_size=21)
        with self.voiceover(
            "Kripke added two further arguments. <bookmark mark='a'/>The epistemic argument: if Aristotle meant the "
            "teacher of Alexander, then Aristotle, if he existed, taught Alexander would be knowable a priori, like a "
            "definition. It is not; historians could find it false. <bookmark mark='b'/>The semantic argument. "
            "Most of us associate the name Gödel with one description: the man who proved the incompleteness of "
            "arithmetic. Suppose that in fact a man named Schmidt found the proof, and Gödel stole it. On the "
            "description theory, our word Gödel would refer to Schmidt. It plainly would not; we would say that "
            "Gödel stole Schmidt's proof. <bookmark mark='c'/>And many speakers know only that Feynman was a "
            "physicist. That fits thousands of people, yet they refer to Feynman. <bookmark mark='d'/>Descriptivists "
            "have replies: use rigidified descriptions, the actual teacher of Alexander, or descriptions of the "
            "name's own history. The debate is alive, and it returns in Part 27."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def chain(self):
        head = label(r"The causal picture of reference", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        n = 7
        pts = [np.array([-5.6 + 1.85 * i, 0.9 + 0.35 * np.sin(i * 1.3), 0]) for i in range(n)]
        nodes = VGroup(*[Dot(p, radius=0.17, color=NAME if i == 0 else (DESC if i == n - 1 else GREY_A))
                         for i, p in enumerate(pts)])
        arrows = VGroup(*[Arrow(pts[i], pts[i + 1], buff=0.22, color=CPT, stroke_width=3,
                                max_tip_length_to_length_ratio=0.15) for i in range(n - 1)])
        bap = label(r"a baptism: \ `this child is Aristotle'", font_size=18, color=NAME).next_to(nodes[0], UP,
                                                                                               buff=0.2)
        bap.align_to(nodes[0], LEFT).shift(LEFT * 0.4)
        you = label(r"you, \ today", font_size=18, color=DESC).next_to(nodes[-1], UP, buff=0.2)
        lab = label(r"the name is passed on, \ each user intending to refer as the last did", font_size=18,
                    color=CPT).next_to(arrows, DOWN, buff=0.45)
        rows = stack([(r"reference is fixed by a chain of uses back to the object, \ not by what the speaker knows",
                       WHITE),
                      (r"a description may \textit{fix} the reference \ (`one metre: \ the length of this bar'), \ "
                       r"without giving the meaning", NAME),
                      (r"Evans \ (1973): \ `Madagascar' once named part of the African mainland; \ Marco Polo's "
                       r"mistake shifted it", BAD),
                      (r"so chains need repair: \ the dominant source of the information matters too", GOAL)],
                     font_size=20, aligned_edge=LEFT, width=12.2).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In place of descriptions Kripke offered a picture, not quite a theory. <bookmark mark='a'/>A name is "
            "attached to a thing at a baptism: this child is Aristotle. <bookmark mark='b'/>Then it is passed from "
            "speaker to speaker, each intending to use it as the one they learned it from did, <bookmark mark='c'/>"
            "down to you, today. Your word refers to Aristotle because it stands at the end of this chain, not "
            "because of anything you know about him. <bookmark mark='d'/>A description may still fix the reference "
            "at the start, as when the metre was fixed as the length of a certain bar, without becoming the meaning "
            "of the word. <bookmark mark='e'/>Gareth Evans found the picture too simple. Madagascar was once a name "
            "for a part of the African mainland; Marco Polo, misunderstanding his sources, applied it to the island, "
            "and now it names the island. <bookmark mark='f'/>So chains can shift; what matters is also where the "
            "speaker's information dominantly comes from."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(nodes[0]), FadeIn(bap))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowArrow(a), FadeIn(nodes[i + 1])) for i, a in
                                    enumerate(arrows)], lag_ratio=0.3), FadeIn(lab), run_time=3)
            vo.wait_until("c")
            self.play(FadeIn(you), FadeIn(rows[0]))
            for mk, r in zip("def", rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
