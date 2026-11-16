from __future__ import annotations

from videos.psychology.psych39.common import *  # noqa: F403

SYMPTOMS = [r"depressed mood", r"loss of interest", r"weight or appetite", r"sleep", r"agitation or slowing",
            r"fatigue", r"worthlessness or guilt", r"concentration", r"thoughts of death"]


class Valid(VoiceoverScene):
    def construct(self):
        self.card()
        self.validators()
        self.combinations()
        self.profiles()

    def card(self):
        card = chapter_card(5, r"Reliable is not valid", r"Does a diagnosis pick out one thing?",
                            lit={1970: r"Robins \& Guze", 2015: r"Fried \& Nesse"}, part=PART, scale=("person",),
                            marr=("what",))
        with self.voiceover("Chapter five. Reliable is not valid."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def validators(self):
        head = heading(r"How would we know a diagnosis is real?")
        items = [
            (r"description", r"a recognizable cluster of symptoms", SYMP),
            (r"laboratory", r"biological or psychological tests that pick it out", MODEL),
            (r"boundaries", r"it can be told apart from other disorders", PERSON),
            (r"course", r"people with it follow a similar course over time", GOOD),
            (r"families", r"it runs in families", WHITE),
        ]
        rows = VGroup()
        for what, how, c in items:
            rows.add(VGroup(word_chip(what, color=c, font_size=19, width=3.0), wrapped_label(how, 8.6, 21, WHITE))
                     .arrange(RIGHT, buff=0.4))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.36).move_to([0, 0.1, 0])
        foot = wrapped_label(r"Robins and Guze, \ 1970: \ five kinds of evidence a diagnosis should gather; \ "
                             r"Kraepelin's course is one of them", 12.0, 19, GREY_A).to_edge(DOWN, buff=0.75)
        tag = historical_tag(r"Robins \& Guze (1970)")
        with self.voiceover(
            "Agreement shows clinicians are measuring the same thing. It doesn't show the thing is real. "
            "<bookmark mark='a'/> In 1970 Eli Robins and Samuel Guze listed the evidence a diagnosis should gather. "
            "A recognizable description. <bookmark mark='b'/> Laboratory tests that pick it out. "
            "<bookmark mark='c'/> Boundaries from other disorders. <bookmark mark='d'/> A similar course over time, "
            "Kraepelin's test. <bookmark mark='e'/> And a tendency to run in families. Half a century on, most "
            "diagnoses meet some of these and few meet all."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(foot))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def combinations(self):
        d = load("combos")
        head = heading(r"Two people, \ one diagnosis")
        grid = VGroup()
        a = {0, 2, 3, 5, 6}
        b = {0, 1, 4, 7, 8}
        for k, s in enumerate(SYMPTOMS):
            name = label(s, font_size=16, color=GREY_A).move_to([-4.8, 2.0 - 0.45 * k, 0], aligned_edge=LEFT)
            ca = Circle(radius=0.14, color=PERSON, fill_opacity=0.9 if k in a else 0.0).move_to([-1.6, 2.0 - 0.45 * k, 0])
            cb = Circle(radius=0.14, color=SYMP, fill_opacity=0.9 if k in b else 0.0).move_to([-0.9, 2.0 - 0.45 * k, 0])
            grid.add(VGroup(name, ca, cb))
        hdr = VGroup(label(r"A", font_size=18, color=PERSON).move_to([-1.6, 2.5, 0]),
                     label(r"B", font_size=18, color=SYMP).move_to([-0.9, 2.5, 0]))
        rows = rows_of([
            (r"major depression: \ five or more of nine symptoms for two weeks, \ one of them depressed mood or loss "
             r"of interest", WHITE),
            (rf"counting the combinations that qualify: \ {d['n']}", MODEL),
            (rf"two people can share a diagnosis and only {d['min_overlap']} symptom, \ like A and B here", AUTH),
            (r"a reliable label for a heterogeneous group: \ which is why research on ``depression'' can average "
             r"over very different people", YOU),
        ], 5.6, 19, 0.36).move_to([3.5, -0.2, 0])
        tag = psyche_tag(r"counted in \texttt{psych39.compute}")
        with self.voiceover(
            "Validity has a second problem: what's inside a category. <bookmark mark='a'/> Major depression needs "
            "five or more of nine symptoms for two weeks, one of them depressed mood or loss of interest. "
            f"<bookmark mark='b'/> Count the combinations that qualify. There are {d['n']}. "
            f"<bookmark mark='c'/> Two people can share the diagnosis and only {d['min_overlap']} symptom, like A "
            "and B here. <bookmark mark='d'/> It's a reliable label for a varied group, which is why research on "
            "depression can end up averaging over very different people."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(hdr), FadeIn(VGroup(*[g[0] for g in grid])))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(VGroup(*[g[1] for g in grid])))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), FadeIn(VGroup(*[g[2] for g in grid])), Indicate(grid[0][1]),
                      Indicate(grid[0][2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def profiles(self):
        head = heading(r"1{,}030 profiles")
        A = axes([0, 1100], [0, 1.0], x_length=5.0, y_length=3.2, xticks=[0, 500, 1000], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{100 * v:.0f}\\%", xlabel=r"profiles, \ commonest first",
                 ylabel=r"share of patients covered", center=[-3.4, -0.2, 0], font_size=14)
        # schematic cumulative coverage: a few common profiles, a long tail of single people
        x = np.arange(1, 1031)
        y = 1 - np.exp(-x / 260) * 0.95
        y = y / y[-1]
        cum = curve(A.ax, x, y, SYMP, stroke_width=4)
        note = label(r"schematic shape", font_size=13, color=GREY_B).next_to(A, DOWN, buff=0.35)
        rows = rows_of([
            (r"Fried and Nesse, \ 2015: \ 3{,}703 outpatients with depression in a large trial, \ twelve symptoms "
             r"each recorded present or absent", WHITE),
            (r"1{,}030 different profiles; \ 501 of them belonged to a single person", SYMP),
            (r"84\% of the profiles were shared by five people or fewer", AUTH),
            (r"Fried's conclusion: \ study the symptoms, \ not just the sum", YOU),
        ], 6.0, 19, 0.36).move_to([3.4, -0.2, 0])
        tag = published_tag(r"Fried \& Nesse (2015)")
        with self.voiceover(
            "And in real patients? <bookmark mark='a'/> In 2015 Eiko Fried and Randolph Nesse looked at three "
            "thousand seven hundred outpatients with depression from a large trial, with twelve symptoms each "
            "recorded present or absent. <bookmark mark='b'/> They found one thousand and thirty different profiles. "
            "Five hundred and one of them belonged to a single person. <bookmark mark='c'/> Eighty-four "
            "percent of the profiles were shared by five people or fewer. <bookmark mark='d'/> Fried's conclusion: study the symptoms, not just their sum."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(cum), run_time=2.0)
            for m, r in zip("cd", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
