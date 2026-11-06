from __future__ import annotations

from videos.philosophy.philosophy40.common import *  # noqa: F403


class Roughness(VoiceoverScene):
    def construct(self):
        card = chapter_card(3, r"Why some intervals sound smooth", r"Can physics explain consonance?", lit=(1863, 1965), part=PART)
        with self.voiceover("Chapter three. Why some intervals sound smooth."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.beats()
        self.curve()
        self.ear()
        self.shifted()
        self.culture()
        self.tonality()

    def culture(self):
        head = label(r"Nature or culture?", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"Helmholtz \ (1863)", r"\textit{On the Sensations of Tone}: \ consonance is the absence of roughness", HARM),
                (r"harmonicity", r"we also like tones whose partials fit one harmonic series \ (McDermott et al., \ 2010)", SYM),
                (r"the Tsimane'", r"McDermott et al. \ (2016): \ an Amazonian people with little Western music showed no preference for consonance", ART),
                (r"the lesson", r"roughness is universal; \ liking consonance is partly learned", GOAL)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Is the preference natural or cultural? <bookmark mark='a'/>Helmholtz's On the Sensations of Tone made "
            "consonance the absence of roughness, a fact about the ear. <bookmark mark='b'/>Josh McDermott and "
            "colleagues found in 2010 that listeners' liking for consonance tracks harmonicity, how well the partials "
            "fit a single harmonic series, more than roughness. <bookmark mark='c'/>And in 2016 they found that the "
            "Tsimane', an Amazonian people with little exposure to Western music, rated consonant and dissonant "
            "chords as equally pleasant, though, like Americans, they disliked rough sounds. <bookmark mark='d'/>Roughness is a "
            "universal fact of hearing; the pleasure taken in consonance is partly learned. The first test of beauty "
            "as number already needs a listener."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def curve(self):
        c, s = load("curve"), load("stretched")
        assert [m["nearest_just"] for m in c["minima"]] == ["6:5", "5:4", "4:3", "3:2", "5:3", "2:1"]
        assert s["minima"][-1]["ratio"] == 2.1
        head = label(r"The dissonance curve, \ computed", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[1.0, 2.3, 0.1], y_range=[0, 1.05, 0.25], x_length=11.0, y_length=4.4,
                  axis_config={"color": GREY_B, "include_tip": False, "font_size": 16},
                  x_axis_config={"numbers_to_include": [1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2],
                                 "decimal_number_config": {"num_decimal_places": 1}},
                  y_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1.0],
                                 "decimal_number_config": {"num_decimal_places": 2}}).move_to([0, -0.4, 0])
        xl = label(r"frequency ratio of the two tones", font_size=18, color=HARM).next_to(ax.x_axis, DOWN, buff=0.35)
        yl = label(r"sensory roughness \ (relative)", font_size=18, color=GREY_A).next_to(ax, UP, buff=0.05).align_to(ax, LEFT)
        curve = VMobject(color=HARM, stroke_width=3.5).set_points_as_corners([ax.c2p(x, y) for x, y in zip(c["r"], c["d"])])
        curve2 = VMobject(color=ART, stroke_width=3).set_points_as_corners([ax.c2p(x, y) for x, y in zip(s["r"], s["d"])])

        def interp(rs, ds, x):
            return float(np.interp(x, rs, ds))

        dips, dlabs = VGroup(), VGroup()
        for m in c["minima"]:
            y = interp(c["r"], c["d"], m["ratio"])
            dips.add(Dot(ax.c2p(m["ratio"], y), radius=0.08, color=GOAL))
            dlabs.add(label(m["nearest_just"], font_size=18, color=GOAL).next_to(ax.c2p(m["ratio"], y), DOWN, buff=0.15))
        dips2 = VGroup(*[Dot(ax.c2p(m["ratio"], interp(s["r"], s["d"], m["ratio"])), radius=0.07, color=ART)
                         for m in s["minima"]])
        leg = stack([(r"two tones, \ each with 6 harmonic partials \ (amplitudes $0.88^k$)", HARM),
                     (r"partials stretched so that the `octave' is 2.1", ART)], font_size=18, buff=0.12,
                    aligned_edge=LEFT).move_to([3.4, 2.35, 0])
        with self.voiceover(
            "Why should simple ratios sound smooth? Hermann von Helmholtz answered in 1863: roughness. <bookmark "
            "mark='a'/>When two pure tones are close in pitch they beat, and at certain separations the beating is "
            "heard as roughness. Reinier Plomp and Willem Levelt measured how roughness depends on the separation in "
            "1965. A real tone is not pure; it has partials at two, three, four times its frequency. <bookmark "
            "mark='b'/>The Reasoner adds up the roughness of every pair of partials for two tones with six harmonic "
            "partials each, as the interval between them slides from a unison to beyond an octave. <bookmark "
            "mark='c'/>The curve dips exactly at six to five, five to four, four to three, three to two, five to "
            "three and two to one: the consonances of Pythagoras, found without any number mysticism, because at "
            "those ratios the partials of the two tones coincide. <bookmark mark='d'/>Now stretch the partials, as "
            "William Sethares did, so that the second partial sits at two point one times the fundamental. The dips "
            "move: the smoothest octave is now two point one, and the old consonances sound rough. Consonance depends "
            "on timbre."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(ax), FadeIn(xl), FadeIn(yl))
            vo.wait_until("b")
            self.play(Create(curve), FadeIn(leg[0]), run_time=3)
            vo.wait_until("c")
            self.play(LaggedStart(*[AnimationGroup(FadeIn(d, scale=2), FadeIn(l)) for d, l in zip(dips, dlabs)],
                                  lag_ratio=0.3))
            vo.wait_until("d")
            self.play(Create(curve2), FadeIn(leg[1]), run_time=2.5)
            self.play(LaggedStart(*[FadeIn(d, scale=2) for d in dips2], lag_ratio=0.2))
        self.clear_scene()

    def shifted(self):
        s = load("stretched")
        head = label(r"With stretched partials, \ the consonances move", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        hd = [r"\text{dip at}", r"\text{nearest just ratio}", r"\text{off by, cents}"]
        cells = [[label(f"{m['ratio']:.3f}", font_size=21, color=ART), label(m["nearest_just"], font_size=21),
                  label(f"{m['off_cents']:+.1f}", font_size=21, color=BAD)] for m in s["minima"]]
        grid = ValueGrid(hd, cells, col_w=[2.4, 3.4, 2.6], cell_h=0.5, font_size=19).move_to([0, 0.6, 0])
        foot = stack([(r"Sethares \ (1993): \ choose the timbre, \ and you choose which scale sounds consonant", GOAL),
                      (r"gamelan metallophones, \ with inharmonic partials, \ go with non-Western tunings", EAST)],
                     font_size=21, buff=0.22).to_edge(DOWN, buff=0.55)
        with self.voiceover(
            "The Reasoner tabulates the moved dips. <bookmark mark='a'/>Each sits between twenty and eighty five "
            "cents away from the just ratio it replaces, and the further up, the larger the shift. <bookmark "
            "mark='b'/>William Sethares's Tuning, Timbre, Spectrum, Scale argued from this that timbre and scale "
            "belong together: choose the spectrum of your instruments, and you have chosen which intervals sound "
            "consonant. <bookmark mark='c'/>The metallophones of the Javanese gamelan have strongly inharmonic "
            "partials, and their tunings differ from Western ones."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in grid.cell], lag_ratio=0.2))
            vo.wait_until("b")
            self.play(FadeIn(foot[0]))
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def beats(self):
        head = label(r"Beats: \ where roughness comes from", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        ax = Axes(x_range=[0, 1, 0.25], y_range=[-2.2, 2.2, 1], x_length=11, y_length=3.0,
                  axis_config={"color": GREY_C, "include_tip": False, "font_size": 16},
                  x_axis_config={"numbers_to_include": [0.25, 0.5, 0.75, 1.0],
                                 "decimal_number_config": {"num_decimal_places": 2}}).move_to([0, 0.3, 0])
        f1, f2 = 40.0, 44.0     # scaled down for display: 4 beats per second either way
        w1 = ax.plot(lambda t: math.sin(2 * PI * f1 * t), x_range=[0, 1, 0.0008], color=HARM, stroke_width=1.2)
        w2 = ax.plot(lambda t: math.sin(2 * PI * f2 * t), x_range=[0, 1, 0.0008], color=ART, stroke_width=1.2)
        s = ax.plot(lambda t: math.sin(2 * PI * f1 * t) + math.sin(2 * PI * f2 * t), x_range=[0, 1, 0.0008],
                    color=WHITE, stroke_width=1.4)
        env = ax.plot(lambda t: 2 * abs(math.cos(PI * (f2 - f1) * t)), x_range=[0, 1, 0.002], color=TASTE,
                      stroke_width=3)
        f = MathTex(r"\sin 2\pi f_1 t + \sin 2\pi f_2 t \;=\; 2\cos\!\big(\pi (f_2 - f_1) t\big)\,\sin\!\big(\pi (f_1 + f_2) t\big)",
                    font_size=30).to_edge(DOWN, buff=1.3)
        foot = label(r"the loudness swells $f_2 - f_1$ times a second: \ slow beats are heard as beating, \ fast ones "
                     r"as roughness", font_size=20, color=GREY_A).to_edge(DOWN, buff=0.5)
        xl = label(r"time, \ seconds", font_size=16, color=GREY_B).next_to(ax.x_axis, DOWN, buff=0.3)
        with self.voiceover(
            "Roughness comes from beats. <bookmark mark='a'/>Two tones of nearly the same frequency, drawn here "
            "slowed down, drift in and out of step. <bookmark mark='b'/>Added together, they reinforce and cancel by "
            "turns, and the loudness swells and fades. <bookmark mark='c'/>A trigonometric identity shows why: the "
            "sum is a tone at the average frequency, multiplied by a slow envelope whose rate is the difference of "
            "the two. <bookmark mark='d'/>A few beats a second are heard as beating, a familiar sound when tuning a "
            "guitar; twenty or thirty a second are heard as roughness; and when the tones are far apart, the ear "
            "resolves them as separate pitches, and the roughness fades. That is the shape Plomp and Levelt measured."
        ) as vo:
            self.play(FadeIn(head), Create(ax), FadeIn(xl))
            vo.wait_until("a")
            self.play(Create(w1), Create(w2), run_time=2)
            vo.wait_until("b")
            self.play(FadeOut(w1), FadeOut(w2), Create(s), run_time=2)
            self.play(Create(env))
            vo.wait_until("c")
            self.play(Write(f))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.clear_scene()

    def ear(self):
        head = label(r"The ear as an analyser", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"the cochlea", r"each place on the basilar membrane responds to a band of frequencies \ (von Békésy; \ Nobel 1961)", HARM),
                (r"critical bands", r"two tones within about a minor third interact; \ beyond it, \ they are heard apart \ (Fletcher, \ 1940)", SYM),
                (r"so", r"roughness peaks at about a quarter of a critical band, \ and the curve has its shape", TASTE),
                (r"Rameau \ (1722)", r"harmony as derived from the fundamental bass: \ a theory older than the physics", HIST)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "The shape of the curve comes from the ear itself. <bookmark mark='a'/>Each place along the basilar "
            "membrane of the cochlea responds to a band of frequencies, as Georg von Békésy showed, for which he won "
            "the Nobel prize in 1961. <bookmark mark='b'/>Two tones within a critical band, roughly a minor third in "
            "the middle range, interact; beyond it, they are heard apart, as Harvey Fletcher found in 1940. <bookmark "
            "mark='c'/>Roughness peaks when tones are about a quarter of a critical band apart, which is why the "
            "curve rises steeply from a unison and then falls. <bookmark mark='d'/>Jean-Philippe Rameau's Treatise on "
            "Harmony, of 1722, had already derived harmony from a fundamental bass, a theory of music older than the "
            "physics that would explain it."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def tonality(self):
        head = label(r"Beyond the single interval", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [
                (r"tonality", r"Krumhansl \ (1990): \ listeners rate how well each note fits a key, \ and the profile is stable", HARM),
                (r"expectation", r"Meyer \ (1956); \ Huron \ (2006): \ musical pleasure as expectation, \ delayed and fulfilled", TASTE),
                (r"the limit", r"no curve of roughness explains a symphony", BAD)]
        g = rows_table(rows, top=1.5, gap=0.5, width=8.4, x_text=-2.0, label_size=20, text_size=20)
        with self.voiceover(
            "Single intervals are only the start. <bookmark mark='a'/>Carol Krumhansl measured in 1990 how well "
            "listeners judge each note to fit a key, and found stable profiles that track how often notes occur in "
            "music. <bookmark mark='b'/>Leonard Meyer's Emotion and Meaning in Music, of 1956, and David Huron's "
            "Sweet Anticipation, of 2006, located musical pleasure in expectation, delayed and then fulfilled or "
            "surprised. <bookmark mark='c'/>No roughness curve explains a symphony; physics sets the stage, and "
            "culture writes the play."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
