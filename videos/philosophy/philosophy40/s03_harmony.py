from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Harmony(VoiceoverScene):
    def construct(self):
        card = chapter_card(2, r"The arithmetic of harmony", r"Is consonance a matter of number?", lit=(-530,), part=PART)
        with self.voiceover("Chapter two. The arithmetic of harmony."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.pythagoreans()
        self.spiral()
        self.temperament()
        self.meantone()
        self.scales()

    def pythagoreans(self):
        head = history_card(-530, r"the Pythagoreans", r"consonance as ratio", width=6.0, color=HIST).to_corner(UL, buff=0.3)
        rows = [
                (r"the discovery", r"consonant intervals are simple ratios of string lengths: \ 2:1, \ 3:2, \ 4:3", HARM),
                (r"the tetractys", r"1 + 2 + 3 + 4 = 10: \ the numbers of the consonances, \ held sacred", FORM),
                (r"the music of the spheres", r"the planets' motions in harmonic ratios \ (Plato's \textit{Timaeus}; \ Kepler, \ \textit{Harmonices Mundi}, \ 1619)", TASTE),
                (r"the claim", r"beauty is mathematical order: \ the first theory of beauty, \ and still the boldest", GOAL)]
        g = rows_table(rows, top=1.0, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The Pythagoreans, in the sixth century before the common era, made the first theory of beauty "
            "mathematical. <bookmark mark='a'/>Consonant intervals, they found, come from simple ratios of string "
            "lengths: two to one, three to two, four to three. <bookmark mark='b'/>The numbers one, two, three and "
            "four, which add up to ten, formed the tetractys, which they held sacred. <bookmark mark='c'/>They heard "
            "the same ratios in the heavens, the music of the spheres, an idea that runs through Plato's Timaeus to "
            "Johannes Kepler's Harmony of the World, of 1619. <bookmark mark='d'/>The claim is that beauty is "
            "mathematical order. This part tests it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def spiral(self):
        t = load("tuning")
        assert (t["comma_num"], t["comma_den"], t["comma_cents"]) == (531441, 524288, 23.46)
        head = label(r"Twelve fifths do not make seven octaves", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        c0 = np.array([-3.0, -0.4, 0])
        R = 2.6
        circle = Circle(radius=R, color=GREY_C, stroke_width=1.5).move_to(c0)
        names = ["C", "G", "D", "A", "E", "B", r"F$\sharp$", r"C$\sharp$", r"G$\sharp$", r"D$\sharp$", r"A$\sharp$",
                 r"F", r"C$'$"]

        def pt(cents_, rad):
            ang = PI / 2 - 2 * PI * cents_ / 1200
            return c0 + rad * np.array([math.cos(ang), math.sin(ang), 0])

        dots, labs, segs = VGroup(), VGroup(), VGroup()
        prev = None
        for k, s in enumerate(t["spiral"]):
            rad = R - 0.09 * k
            p = pt(s["cents_mod_octave"], rad)
            d = Dot(p, radius=0.06, color=HARM if k < 12 else BAD)
            dots.add(d)
            labs.add(label(names[k], font_size=17, color=GREY_A if k < 12 else BAD).move_to(
                c0 + (rad + 0.35) * (p - c0) / np.linalg.norm(p - c0)))
            if prev is not None:
                segs.add(Line(prev, p, color=HARM, stroke_width=1.6, stroke_opacity=0.7))
            prev = p
        gap = label(rf"the twelfth fifth overshoots by {t['comma_cents']} cents", font_size=19,
                    color=BAD).next_to(circle, DOWN, buff=0.25)
        f1 = MathTex(r"\left(\tfrac{3}{2}\right)^{12} \Big/ \, 2^{7} \;=\; \frac{3^{12}}{2^{19}} \;=\; "
                     r"\frac{531441}{524288} \;\approx\; 1.01364", font_size=32, color=WHITE).move_to([3.6, 1.4, 0])
        f2 = label(r"the Pythagorean comma: \ 23.46 cents \ (a semitone is 100)", font_size=21,
                   color=BAD).next_to(f1, DOWN, buff=0.35)
        f3 = MathTex(r"\text{cents}(r) = 1200 \log_2 r", font_size=30, color=GREY_A).next_to(f2, DOWN, buff=0.45)
        f4 = label(r"no power of $3/2$ is a power of $2$: \ the circle of fifths cannot close", font_size=21,
                   color=GOAL).next_to(f3, DOWN, buff=0.4)
        with self.voiceover(
            "Pythagoras, legend says, heard harmony in a smithy and found it in numbers. Strings whose lengths are in "
            "ratio two to one sound an octave; three to two, a fifth; four to three, a fourth. <bookmark "
            "mark='a'/>Build a scale from fifths alone. Start on C and go up a fifth, a ratio of three to two, again "
            "and again, folding each note back into one octave. The notes walk round the circle: G, D, A, E, B, and "
            "on. <bookmark mark='b'/>After twelve fifths you expect to be back on C, seven octaves up. You are not. "
            "<bookmark mark='c'/>Three halves to the twelfth, divided by two to the seventh, is three to the twelfth "
            "over two to the nineteenth, about one point zero one three six. <bookmark mark='d'/>The overshoot is the "
            "Pythagorean comma, twenty three and a half cents, almost a quarter of a semitone. <bookmark mark='e'/>No "
            "power of three halves is a power of two, because one is odd and the other even, so the circle of fifths "
            "can never close. Every tuning system is a compromise with this fact."
        ) as vo:
            self.play(FadeIn(head), Create(circle))
            vo.wait_until("a")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(dots[k]), FadeIn(labs[k]),
                                                   *([Create(segs[k - 1])] if k else []))
                                    for k in range(12)], lag_ratio=0.3), run_time=5)
            vo.wait_until("b")
            self.play(Create(segs[11]), FadeIn(dots[12]), FadeIn(labs[12]))
            self.play(FadeIn(gap), Indicate(dots[12], color=BAD, scale_factor=2))
            vo.wait_until("c")
            self.play(Write(f1))
            vo.wait_until("d")
            self.play(FadeIn(f2), FadeIn(f3))
            vo.wait_until("e")
            self.play(FadeIn(f4))
        self.clear_scene()

    def temperament(self):
        t = load("tuning")
        assert t["semitone"] == 1.059463 and [e["error"] for e in t["equal"]] == [0.0, -1.96, 1.96, 13.69, -15.64, 15.64]
        head = label(r"Equal temperament: \ $2^{1/12}$ per semitone", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{interval}", r"\text{just ratio}", r"\text{just, cents}", r"\text{equal, cents}",
              r"\text{error}"]
        cells = []
        for e in t["equal"]:
            big = abs(e["error"]) > 5
            cells.append([label(e["interval"], font_size=20, color=HARM), label(e["just"], font_size=20),
                          label(f"{e['just_cents']:.2f}", font_size=20, color=GREY_A),
                          label(str(e["et_cents"]), font_size=20),
                          label(f"{e['error']:+.2f}", font_size=20, color=BAD if big else OK)])
        grid = ValueGrid(hd, cells, col_w=[2.6, 2.0, 2.4, 2.4, 1.8], cell_h=0.52, font_size=19).move_to([0, 0.7, 0])
        foot = stack([(r"each semitone multiplies frequency by $2^{1/12} \approx 1.059463$: \ every key equally in tune, "
                       r"\ and none exactly", GREY_A),
                      (r"fifths and fourths are off by 2 cents; \ thirds and sixths by 14 to 16", BAD),
                      (r"Zhu Zaiyu \ (1584) \ and Stevin computed it; \ it spread in Europe with the keyboard", EAST)],
                     font_size=20, buff=0.2).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The modern compromise spreads the comma evenly. <bookmark mark='a'/>In equal temperament every semitone "
            "multiplies the frequency by the twelfth root of two, about one point zero five nine. Every key is "
            "equally in tune, and no interval except the octave is exactly in tune. <bookmark mark='b'/>The Reasoner "
            "measures the damage in cents. Fifths and fourths are off by only two cents. Major thirds are fourteen "
            "cents sharp, minor thirds sixteen flat. <bookmark mark='c'/>The Chinese prince Zhu Zaiyu calculated the "
            "twelfth root of two to great accuracy in 1584, and Simon Stevin in the Netherlands around the same time; "
            "the system spread in Europe with keyboard music."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(FadeIn(foot[0]), *[FadeIn(c) for row in grid.cell for c in row[:4]])
            vo.wait_until("b")
            self.play(*[FadeIn(row[4]) for row in grid.cell], FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot[2]))
        self.clear_scene()

    def meantone(self):
        t = load("temper")
        S = {s["system"]: s for s in t["systems"]}
        assert S["quarter-comma meantone"]["major_third"] == 386.31 and S["Pythagorean"]["wolf"] == 678.49
        head = label(r"Where to put the comma", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{system}", r"\text{fifth}", r"\text{major third}", r"\text{third's error}", r"\text{wolf fifth}"]
        cells = []
        for name in ("Pythagorean", "quarter-comma meantone", "equal"):
            s0 = S[name]
            cells.append([label(name, font_size=20, color=HARM), label(f"{s0['fifth']:.2f}", font_size=20),
                          label(f"{s0['major_third']:.2f}", font_size=20),
                          label(f"{s0['third_error']:+.2f}", font_size=20, color=OK if s0["third_error"] == 0 else BAD),
                          label(f"{s0['wolf']:.2f}", font_size=20, color=BAD if abs(s0["wolf"] - 700) > 5 else OK)])
        grid = ValueGrid(hd, cells, col_w=[4.2, 1.6, 2.2, 2.2, 2.0], cell_h=0.6, font_size=19).move_to([0, 0.9, 0])
        foot = stack([(rf"just major third 5:4 = {t['just_third']} cents; \ the syntonic comma 81:80 = "
                       rf"{t['syntonic_cents']} cents", GREY_A),
                      (r"Pythagorean: \ pure fifths, \ harsh thirds; \ meantone: \ pure thirds, \ one howling `wolf'", HARM),
                      (r"equal: \ no wolf, \ every key usable, \ every third a little rough", GOAL)],
                     font_size=21, buff=0.22).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Before equal temperament, musicians chose where to put the comma. The Reasoner compares three systems in "
            "cents. <bookmark mark='a'/>Pythagorean tuning keeps every fifth pure, but its major third, four fifths "
            "up, is twenty one and a half cents sharp, and the last fifth, the wolf, is badly flat. <bookmark "
            "mark='b'/>Quarter-comma meantone, the Renaissance favourite, narrows each fifth by a quarter of the "
            "syntonic comma, eighty one to eighty, so that four fifths make a perfectly pure major third; the price "
            "is a wolf fifth thirty seven cents too wide, and keys that cannot be used. <bookmark mark='c'/>Equal "
            "temperament has no wolf and every key is usable, and every major third is fourteen cents rough. Each "
            "system is a different answer to the same impossibility."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(*[FadeIn(c) for c in grid.cell[0]], FadeIn(foot[0]))
            vo.wait_until("b")
            self.play(*[FadeIn(c) for c in grid.cell[1]], FadeIn(foot[1]))
            vo.wait_until("c")
            self.play(*[FadeIn(c) for c in grid.cell[2]], FadeIn(foot[2]))
        self.clear_scene()

    def scales(self):
        head = label(r"Other scales", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"pentatonic", r"five notes from four fifths: \ found in Chinese, \ Scottish and West African music", EAST),
                (r"India", r"twenty two \textit{shrutis} in the octave, \ from which the notes of each \textit{raga} are chosen", TASTE),
                (r"maqam", r"Arabic modes use intervals between the Western semitone and whole tone", ART),
                (r"the lesson", r"simple ratios recur everywhere; \ how they are tempered is culture", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Western scales are one answer among several. <bookmark mark='a'/>The pentatonic scale, five notes built "
            "from four fifths, appears in Chinese, Scottish and West African music. <bookmark mark='b'/>Indian theory "
            "divides the octave into twenty two shrutis, from which the notes of each raga are chosen. <bookmark "
            "mark='c'/>The Arabic maqam system uses intervals between the Western semitone and whole tone. <bookmark "
            "mark='d'/>Simple ratios such as the octave and the fifth recur almost everywhere; how the rest are "
            "tempered is a matter of culture."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
