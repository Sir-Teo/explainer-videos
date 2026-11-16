from __future__ import annotations

from videos.psychology.psych49.common import *  # noqa: F403


class Glm(VoiceoverScene):
    def construct(self):
        self.card()
        self.levels()
        self.maps()
        self.fixed()

    def card(self):
        card = chapter_card(3, r"The linear model, \ at two levels", r"Who is the sample: \ scans, \ or people?",
                            lit=(), part=PART, scale=("brain",), marr=("how",))
        with self.voiceover("Chapter three. The linear model, at two levels."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def levels(self):
        head = heading(r"Two levels, \ like Part 47's")
        first = MathTex(r"\text{level 1 (each person):}\quad y_v(t) = X(t)\,\beta_{v,p} + \varepsilon_v(t)",
                        font_size=34, color=SYMP)
        second = MathTex(r"\text{level 2 (the group):}\quad c^\top\hat\beta_{v,p} = \mu_v + u_{v,p} + e_{v,p}",
                         font_size=34, color=MODEL)
        test = MathTex(r"t_v = \frac{\bar{c}_v}{s_v/\sqrt{n}} \quad \text{($s_v$: the spread across people)}",
                       font_size=34, color=PERSON)
        eqs = VGroup(first, second, test).arrange(DOWN, buff=0.45).move_to([0, 1.0, 0])
        rows = rows_of([
            (r"Part 8 fitted the first level: \ each voxel's time series against the task, \ convolved with the "
             r"haemodynamic response", SYMP),
            (r"each person gives one contrast per voxel, \ such as faces minus houses", MODEL),
            (r"the second level treats people as a sample: \ the test's error is how much the contrast varies "
             r"across people", PERSON),
            (r"it is Part 47's multilevel model, \ with voxels in place of trials", YOU),
        ], 12.4, 21, 0.3).move_to([0, -2.1, 0])
        with self.voiceover(
            "The model has two levels, like Part 47's. <bookmark mark='a'/> Part 8 fitted the first: each voxel's "
            "time series against the task, convolved with the haemodynamic response. <bookmark mark='b'/> Each "
            "person then gives one contrast per voxel, such as faces minus houses. <bookmark mark='c'/> The second "
            "level treats people as a sample. The test's error is how much that contrast varies across people. "
            "<bookmark mark='d'/> It's Part 47's multilevel model, with voxels in place of trials."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(first), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(second), FadeIn(test), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def maps(self):
        d = load("groupmap")
        head = heading(r"One person, \ and thirty")
        mask = np.asarray(d["mask"], bool)
        h = 3.0
        m1 = heat(d["truth"], h, -0.2, 1.2, mask, center=[-4.6, 0.5, 0])
        m2 = heat(d["one"], h, -2.5, 2.5, mask, center=[-0.15, 0.5, 0])
        m3 = heat(d["t"], h, -2, 8, mask, center=[4.3, 0.5, 0])
        caps = VGroup(label(r"what Psyche planted", font_size=18, color=GOOD).next_to(m1, DOWN, buff=0.15),
                      label(r"one person's contrast", font_size=18, color=AUTH).next_to(m2, DOWN, buff=0.15),
                      label(r"the group's $t$ (30 people)", font_size=18, color=THRESH).next_to(m3, DOWN, buff=0.15))
        rows = rows_of([
            (r"five discs with planted effects from none to large; \ one person's map is mostly that person and noise",
             WHITE),
            (r"the group's $t$ shows the large effects plainly, \ the middle ones faintly, \ and the smallest not at "
             r"all: \ thirty people are enough for some questions and not others", PERSON),
        ], 12.4, 20, 0.28).move_to([0, -2.75, 0])
        tag = psyche_tag(r"\texttt{neurodata.subject\_maps}, \ \texttt{one\_sample\_t}")
        with self.voiceover(
            "Here it is on Psyche's brain. <bookmark mark='a'/> On the left, what was planted: five discs with "
            "effects from none to large. In the middle, one person's map. It's mostly that person, and noise. "
            "<bookmark mark='b'/> On the right, the group's t map from thirty people. The large effects stand out "
            "plainly, the middle ones faintly, and the smallest not at all. Thirty people are enough for some "
            "questions and not for others, which is why the pipelines split where they did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(m1), FadeIn(caps[0]))
            vo.wait_until("a")
            self.play(FadeIn(m2), FadeIn(caps[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(m3), FadeIn(caps[2]), FadeIn(rows[1]))
        self.wait(1.0)
        self.clear_scene()

    def fixed(self):
        d = load("fixed")
        head = heading(r"Scans are not people")
        A = axes([0.3, 2.7], [0, 0.16], x_length=4.0, y_length=3.0, xticks=None, yticks=[0, 0.05, 0.1, 0.15],
                 yfmt=lambda v: f"{100 * v:.0f}\\%", ylabel=r"null voxels below $p < 0.001$", center=[-3.8, 0.3, 0],
                 font_size=12)
        b = bars(A.ax, [1, 2], [d["fixed"], d["random"]], [AUTH, GOOD], width=0.6)
        names = VGroup(*[wrapped_label(t, 1.7, 12, c).next_to(A.ax.c2p(i + 1, 0), DOWN, buff=0.1) for i, (t, c) in
                         enumerate(((r"fixed effects: \ scan-to-scan error", AUTH),
                                    (r"random effects: \ person-to-person spread", GOOD)))])
        rows = rows_of([
            (r"20 people, \ no group effect; \ but each person's true effect differs (SD 1), \ and is measured with "
             r"error (SE 0.5)", WHITE),
            (rf"fixed effects tests against the measurement error alone: \ {100 * d['fixed']:.0f}\% of null voxels pass "
             rf"at $p < 0.001$", AUTH),
            (rf"random effects tests against the spread across people: \ {100 * d['random']:.2f}\%, \ as promised",
             GOOD),
            (r"fixed effects describes these 20 people; \ only random effects speaks for the population they came from",
             YOU),
        ], 6.4, 19, 0.38).move_to([3.3, -0.1, 0])
        tag = psyche_tag(r"\texttt{neurodata.fixed\_vs\_random}, \ 200 studies")
        with self.voiceover(
            "Why must the second level use the spread across people? <bookmark mark='a'/> Take twenty people and no "
            "group effect at all. But each person's true effect differs, and each is measured with some error. "
            "<bookmark mark='b'/> A fixed-effects test uses only the measurement error, as if the scans were the "
            "sample. Fourteen percent of null voxels pass at one in a thousand. <bookmark mark='c'/> A random-effects "
            "test uses the spread across people, and gets one in a thousand, as promised. <bookmark mark='d'/> Fixed "
            "effects describes these twenty people. Only random effects speaks for the population they came from. "
            "Early imaging studies often used fixed effects."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(names))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(b[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(b[1]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
