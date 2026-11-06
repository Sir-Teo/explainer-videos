from __future__ import annotations

from videos.philosophy.philosophy21.common import *  # noqa: F403


class Discern(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"Black's spheres and quantum particles", r"Could two things share every property?",
                            lit=(1952, 2006), part=PART)
        with self.voiceover("Chapter two. Black's spheres and quantum particles."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.black()
        self.grades()
        self.quantum()
        self.shift()

    def black(self):
        hc = history_card(1952, r"Max Black", r"`The Identity of Indiscernibles', \ \textit{Mind}", width=6.0,
                          color=HIST).to_corner(UL, buff=0.3)
        s1 = Circle(radius=0.6, color=GREY_A, fill_opacity=0.5).move_to([-4.6, -0.6, 0])
        s2 = Circle(radius=0.6, color=GREY_A, fill_opacity=0.5).move_to([-1.4, -0.6, 0])
        d = DoubleArrow(s1.get_right(), s2.get_left(), buff=0.1, color=UNIV, stroke_width=2.5)
        dl = label(r"two miles apart", font_size=16, color=UNIV).next_to(d, UP, buff=0.1)
        rows = stack([(r"two iron spheres, \ alike in every quality, \ alone in a symmetric universe", WHITE),
                      (r"each is two miles from an iron sphere: \ so is the other", GREY_A),
                      (r"so they are indiscernible, \ yet two: \ PII is false", BAD),
                      (r"replies: \ `being identical to $a$' \ (trivial); \ or the universe is really one sphere, \ "
                       r"seen twice \ (Hacking, \ 1975)", GOAL)], font_size=20, aligned_edge=LEFT,
                     width=6.6).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Max Black wrote a dialogue against the principle. <bookmark mark='a'/>Imagine a universe containing "
            "nothing but two iron spheres, exactly alike, two miles apart. <bookmark mark='b'/>Every property one has, "
            "the other has: each is iron, each is a sphere, each is two miles from an iron sphere. "
            "<bookmark mark='c'/>So they are indiscernible, yet there are two of them, and the identity of "
            "indiscernibles is false. <bookmark mark='d'/>Defenders reply that the scenario is not what it seems. Ian "
            "Hacking suggested we might be describing a curved space with a single sphere, seen twice around."
        ) as vo:
            self.play(FadeIn(hc), FadeIn(s1), FadeIn(s2))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(GrowFromCenter(d), FadeIn(dl), FadeIn(rows[1]))
            for mk, r in zip("cd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def grades(self):
        d = load("discern")
        head = label(r"Grades of discernibility \ (Quine, \ 1976)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        defs = stack([(r"absolutely: \ some condition $\varphi(x)$ holds of one, \ not the other", OK),
                      (r"relatively: \ some relation holds from $a$ to $b$ \ but not from $b$ to $a$", UNIV),
                      (r"weakly: \ some irreflexive relation holds between them", ABS)], font_size=19,
                     aligned_edge=LEFT, width=7.0).move_to([-2.4, 1.9, 0])
        hd = [r"\text{structure}", r"\text{swaps}", r"\text{grade}"]
        cases = [("one red", r"a red one and a plain one"), ("arrow", r"one points at the other"),
                 ("spheres", r"Black's spheres: \ `two miles from'"), ("singlet", r"two electrons in the singlet"),
                 ("no relation", r"two things, \ nothing else")]
        cols = {"absolute": OK, "relative": UNIV, "weak": ABS, "indiscernible": BAD}
        rows = []
        for k, txt in cases:
            v = d[k]
            rows.append([MathTex(r"\text{" + txt.replace(r"\ ", " ") + "}", font_size=20),
                         MathTex(r"\text{yes}" if v["automorphisms"] > 1 else r"\text{no}", font_size=20),
                         MathTex(r"\text{" + v["grade"] + "}", font_size=22, color=cols[v["grade"]])])
        grid = ValueGrid(hd, rows, col_w=[5.2, 1.4, 2.6], cell_h=0.5, font_size=19).move_to([-1.2, -1.2, 0])
        note = label(r"`swaps': \ an automorphism exchanges the two", font_size=15, color=GREY_A).next_to(grid, DOWN,
                                                                                                    buff=0.1)
        side = stack([(r"Black's spheres are weakly discernible", ABS),
                      (r"so a weakened PII survives: \ distinct things differ at least weakly", GOAL)],
                     font_size=18, aligned_edge=LEFT, width=3.2).move_to([5.2, -1.0, 0])
        with self.voiceover(
            "Quine distinguished grades of discernibility. <bookmark mark='a'/>Two things are absolutely discernible "
            "if some condition holds of one and not the other; relatively discernible if some relation holds from one "
            "to the other but not back; and weakly discernible if some irreflexive relation holds between them. "
            "<bookmark mark='b'/>The Reasoner tests small structures by brute force, checking which permutations "
            "preserve everything. A red thing and a plain one: absolutely discernible. One pointing at the other: "
            "relatively. <bookmark mark='c'/>Black's spheres: a symmetry swaps them, so they are not absolutely "
            "discernible, but being two miles from holds between them and not between either and itself. They are "
            "weakly discernible. <bookmark mark='d'/>Only two things with no relation at all are fully "
            "indiscernible. <bookmark mark='e'/>So a weakened principle survives Black: distinct things always differ, "
            "at least weakly."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in defs], lag_ratio=0.4))
            vo.wait_until("b")
            self.play(FadeIn(grid.head), Create(grid.rule), FadeIn(note), FadeIn(VGroup(*grid.cell[0])),
                      FadeIn(VGroup(*grid.cell[1])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*grid.cell[2])), FadeIn(VGroup(*grid.cell[3])), FadeIn(side[0]))
            vo.wait_until("d")
            self.play(FadeIn(VGroup(*grid.cell[4])))
            vo.wait_until("e")
            self.play(FadeIn(side[1]))
        self.clear_scene()

    def quantum(self):
        head = label(r"Identical particles", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        f = MathTex(r"|\psi\rangle = \tfrac{1}{\sqrt2}\big(|{\uparrow}\rangle_1|{\downarrow}\rangle_2 - "
                    r"|{\downarrow}\rangle_1|{\uparrow}\rangle_2\big)", font_size=36, color=UNIV).next_to(head, DOWN,
                                                                                                   buff=0.35)
        rows = [
            (r"permutation", r"the state is antisymmetric: \ swapping the labels changes nothing measurable", GREY_A),
            (r"the worry", r"electrons in this state share every monadic property: \ PII seems to fail \ (French "
                           r"and Redhead, \ 1988)", BAD),
            (r"Saunders \ (2006)", r"`has opposite spin to' is irreflexive and holds between them: \ weakly "
                                   r"discernible", ABS),
            (r"Muller, \ Saunders, \ Seevinck", r"fermions \ (2008), \ and with more care bosons \ (2009), \ are at "
                                                r"least weakly discernible", OK),
            (r"structuralism", r"perhaps particles are not individuals at all: \ Part 18's ontic structural realism; "
                               r"\ Part 26", GOAL),
        ]
        g = rows_table(rows, top=0.7, gap=0.42, width=8.8, x_text=-2.4, label_size=20)
        with self.voiceover(
            "Physics supplies a real case. <bookmark mark='a'/>Two electrons in the singlet state: one spin up and one "
            "spin down, superposed with a minus sign, so that swapping the labels changes nothing measurable. "
            "<bookmark mark='b'/>Each electron has exactly the same monadic properties as the other, and Steven French "
            "and Michael Redhead argued that the identity of indiscernibles fails. <bookmark mark='c'/>Simon Saunders "
            "replied that the relation has opposite spin to holds between them and is irreflexive, so the electrons "
            "are weakly discernible, as the Reasoner's table shows. <bookmark mark='d'/>Fred Muller, with Saunders, "
            "extended the argument to all fermions, and with Michiel Seevinck, more delicately, to bosons. "
            "<bookmark mark='e'/>Or perhaps "
            "particles are not individuals at all, as the ontic structural realism of Part 18 suggested, a question "
            "for Part 26."
        ) as vo:
            self.play(FadeIn(head), Write(f))
            for mk, r in zip("abcde", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def shift(self):
        hc = history_card(1716, r"Leibniz and Clarke", r"the correspondence", width=5.0, color=HIST).to_corner(
            UL, buff=0.3)
        rng = np.random.default_rng(1716)
        pts = [np.array([rng.uniform(-6.0, -1.0), rng.uniform(-1.8, 1.0), 0]) for _ in range(9)]
        dots = VGroup(*[Dot(p, radius=0.1, color=UNIV) for p in pts])
        frame = Rectangle(width=6.0, height=3.4, color=GREY_D).move_to([-3.5, -0.4, 0])
        rows = stack([(r"Newton: \ space is a container, \ absolute", WHITE),
                      (r"then God could have made the whole universe five feet to the east", GREY_A),
                      (r"the two universes would be indiscernible in every respect", UNIV),
                      (r"by PII they are one: \ so there is no absolute space", GOAL),
                      (r"and the kinematic shift: \ the universe moving uniformly, \ or at rest \ (Part 18; \ "
                       r"Part 25)", BAD)], font_size=20, aligned_edge=LEFT, width=6.2).move_to([3.4, -0.4, 0])
        with self.voiceover(
            "Leibniz put the principle to work against Newton, in his correspondence with Samuel Clarke. "
            "<bookmark mark='a'/>If space were an absolute container, as Newton held, then God could have created "
            "the whole universe five feet to the east of where it is. <bookmark mark='b'/>The Reasoner shifts every "
            "object. <bookmark mark='c'/>The two universes would be indiscernible in every respect: every distance, "
            "every relation, the same. <bookmark mark='d'/>By the identity of indiscernibles they are one universe, "
            "so the supposed difference is unreal, and there is no absolute space. <bookmark mark='e'/>The same "
            "argument applied to uniform motion is the kinematic shift, met in Part 18's two Newtonian worlds, and it "
            "returns with full force in Part 25."
        ) as vo:
            self.play(FadeIn(hc), Create(frame), FadeIn(dots))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(dots.animate.shift(RIGHT * 1.2), frame.animate.shift(RIGHT * 0.0), run_time=2)
            for mk, r in zip("cde", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
