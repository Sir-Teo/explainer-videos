from __future__ import annotations

from videos.psychology.psych32.common import *  # noqa: F403

HS_SHORT = [r"visual perception", r"cubes", r"lozenges", r"paragraphs", r"sentences", r"word meaning",
            r"addition", r"counting dots", r"straight/curved"]


class Many(VoiceoverScene):
    def construct(self):
        self.card()
        self.thurstone()
        self.three()
        self.hierarchy()

    def card(self):
        card = chapter_card(3, r"One factor or many", r"Is it $g$, \ or several abilities, \ or both?",
                            lit={1938: r"Thurstone", 1993: r"Carroll"}, part=PART, scale=("group",), marr=("what",))
        with self.voiceover("Chapter three. One factor or many."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def thurstone(self):
        head = heading(r"Thurstone's answer, \ 1938")
        pmas = [r"verbal comprehension", r"word fluency", r"number", r"spatial visualization",
                r"associative memory", r"perceptual speed", r"reasoning"]
        chips = VGroup(*[word_chip(p_, color=VERB, font_size=20, width=3.6) for p_ in pmas])
        chips.arrange_in_grid(rows=4, cols=2, buff=(0.3, 0.22)).move_to([-3.2, -0.3, 0])
        rows = rows_of([
            (r"Louis Thurstone gave 56 tests to students and rotated the factors to make each test load on as few as "
             r"possible", WHITE),
            (r"seven ``primary mental abilities'' appeared, \ and no general factor", VERB),
            (r"but the seven primaries themselves correlated positively: \ factor them, \ and $g$ comes back one "
             r"level up", G),
            (r"the disagreement was partly about rotation: \ the same matrix, \ described two ways", MODEL),
        ], 5.6, 22, 0.38).move_to([3.6, -0.2, 0])
        tag = historical_tag(r"Thurstone (1938)")
        with self.voiceover(
            "The best-known challenge to Spearman came from Chicago. <bookmark mark='a'/> In 1938 Louis Thurstone "
            "gave fifty-six tests to students and rotated the factors so that each test loaded on as few of them as "
            "possible. <bookmark mark='b'/> Seven primary mental abilities appeared: verbal comprehension, word "
            "fluency, number, spatial visualization, associative memory, perceptual speed and reasoning, and no "
            "general factor. <bookmark mark='c'/> But the primaries themselves correlated positively. Factor those "
            "correlations, and g comes back one level up. <bookmark mark='d'/> Much of the disagreement was about "
            "rotation: the same matrix, described two ways."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c, scale=0.9) for c in chips], lag_ratio=0.2), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def three(self):
        d = load("holzinger")
        head = heading(r"Three factors in the real battery")
        L = np.asarray(d["L3"])
        cell = 0.5
        grid = VGroup()
        cols = (VIS, VERB, SPEED)
        for i in range(9):
            for j in range(3):
                v = float(L[i, j])
                t = min(1.0, max(0.0, v) / 0.9)
                sq = Square(side_length=cell, stroke_width=1, stroke_color=BLACK,
                            fill_color=interpolate_color(ManimColor("#14181F"), ManimColor(cols[j]), t),
                            fill_opacity=1).move_to([j * cell * 1.6, -i * cell, 0])
                grid.add(VGroup(sq, label(f"{v:.2f}", font_size=15, color=BLACK if t > 0.55 else WHITE).move_to(sq)))
        names = VGroup(*[label(n, font_size=16, color=GREY_A) for n in HS_SHORT])
        for i, n in enumerate(names):
            n.next_to(grid[3 * i], LEFT, buff=0.15)
        tops = VGroup(*[label(t, font_size=17, color=c).next_to(grid[j], UP, buff=0.15)
                        for j, (t, c) in enumerate(((r"visual", VIS), (r"verbal", VERB), (r"speed", SPEED)))])
        table = VGroup(grid, names, tops).move_to([-2.4, -0.4, 0])
        rows = rows_of([
            (r"three maximum-likelihood factors, \ rotated by varimax so each test loads mainly on one", MODEL),
            (r"visual perception, \ cubes and lozenges on the first; \ paragraphs, \ sentences and word meaning on "
             r"the second; \ the speeded tests on the third", WHITE),
            (r"straight-or-curved capitals splits between speed and the visual factor", SPEED),
        ], 5.6, 22, 0.38).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{statkit.multi.varimax}; \ data: Holzinger \& Swineford (1939)")
        with self.voiceover(
            "Here are three factors in Holzinger and Swineford's battery. <bookmark mark='a'/> Maximum likelihood "
            "extracts them, and varimax rotates them so that each test loads mainly on one. "
            "<bookmark mark='b'/> Visual perception, cubes and lozenges go together; paragraphs, sentences and word "
            "meaning; and the three speeded tests. <bookmark mark='c'/> One test, telling straight from curved "
            "capitals at speed, splits between speed and the visual factor, which makes sense of what it asks."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(names), FadeIn(tops))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in grid], lag_ratio=0.02), FadeIn(rows[0]), run_time=2.0)
            for m, r in zip("bc", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def hierarchy(self):
        d = load("holzinger")
        head = heading(r"The compromise: \ a hierarchy")
        gn = VGroup(Circle(radius=0.42, color=G, fill_color=G, fill_opacity=0.2), label(r"$g$", font_size=32, color=G))
        gn.move_to([-3.0, 2.0, 0])
        broad = VGroup()
        for j, (t, c) in enumerate(((r"visual", VIS), (r"verbal", VERB), (r"speed", SPEED))):
            b = VGroup(RoundedRectangle(corner_radius=0.1, width=1.6, height=0.55, color=c), label(t, font_size=20,
                                                                                                    color=c))
            b[1].move_to(b[0])
            b.move_to([-5.0 + 2.0 * j, 0.4, 0])
            broad.add(b)
        tests = VGroup()
        for i in range(9):
            t = Rectangle(width=0.5, height=0.35, color=GREY_B, stroke_width=2).move_to([-5.6 + 0.66 * i, -1.1, 0])
            tests.add(t)
        up = VGroup(*[Arrow(gn.get_bottom(), b.get_top(), buff=0.08, color=G, stroke_width=3) for b in broad])
        down = VGroup(*[Arrow(broad[i // 3].get_bottom(), tests[i].get_top(), buff=0.06, color=GREY_B,
                              stroke_width=2, max_tip_length_to_length_ratio=0.15) for i in range(9)])
        sec = d["second"]
        lab = VGroup(*[label(f"{sec[j]:.2f}", font_size=16, color=G).move_to(up[j].point_from_proportion(0.5) +
                                                                            LEFT * 0.28) for j in range(3)])
        strata = VGroup(label(r"stratum III", font_size=17, color=GREY_B).next_to(gn, LEFT, buff=1.2),
                        label(r"stratum II", font_size=17, color=GREY_B).next_to(broad, LEFT, buff=0.25),
                        label(r"stratum I", font_size=17, color=GREY_B).next_to(tests, LEFT, buff=0.25))
        for s_ in strata:
            keep_in_frame(s_)
        rows = rows_of([
            (rf"the three composite scores correlate {d['Rc'][0, 1]:.2f}, \ {d['Rc'][0, 2]:.2f} and "
             rf"{d['Rc'][1, 2]:.2f}: \ positive, \ so a factor sits above them", G),
            (r"John Carroll, \ 1993: \ more than 460 data sets reanalysed: \ narrow abilities, \ a few broad ones, "
             r"\ and $g$ at the top", WHITE),
            (r"merged with Cattell and Horn's fluid and crystallized abilities as the Cattell--Horn--Carroll model, "
             r"\ the basis of most modern test batteries", VERB),
            (r"so there is one factor and many: \ which one you see depends on how far up you look", YOU),
        ], 5.6, 21, 0.36).move_to([3.7, -0.2, 0])
        tag = published_tag(r"Carroll (1993)")
        with self.voiceover(
            "The modern answer is a hierarchy. <bookmark mark='a'/> The three composite scores in Holzinger and "
            f"Swineford's battery correlate {d['Rc'][0, 1]:.2f}, {d['Rc'][0, 2]:.2f} and {d['Rc'][1, 2]:.2f}: "
            "positive, so a factor sits above them. <bookmark mark='b'/> In 1993 John Carroll reanalysed more than "
            "four hundred and sixty data sets from the factor-analytic literature and found the same shape "
            "everywhere: narrow abilities at the bottom, a few broad ones above, and g at the top. "
            "<bookmark mark='c'/> Merged with Cattell and Horn's fluid and crystallized abilities, it became the "
            "Cattell-Horn-Carroll model, the basis of most modern test batteries. <bookmark mark='d'/> So there's "
            "one factor and there are many. Which you see depends on how far up you look."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(tests), FadeIn(broad), Create(down), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(gn), Create(up), FadeIn(lab), FadeIn(strata), FadeIn(rows[1]))
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
