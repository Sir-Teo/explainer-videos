from __future__ import annotations

import numpy as np

from videos.psychology.psych2.common import *  # noqa: F403


class Expectancy(VoiceoverScene):
    def construct(self):
        self.card()
        self.rats()
        self.classroom()
        self.dogs()
        self.subject()
        self.blinds()

    def card(self):
        card = chapter_card(7, r"The experimenter is a subject too", r"Can what the experimenter expects change "
                            r"what the subject does?", lit={1962: r"Orne: demand characteristics",
                                                             1963: r"Rosenthal \& Fode's rats",
                                                             1968: r"\emph{Pygmalion in the Classroom}"},
                            part=PART, scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter seven. The experimenter is a subject too."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def rats(self):
        d = load("expectancy")
        head = heading(r"1963: \ twelve students, sixty rats, and two labels")
        A = axes([0.5, 5.5], [0, 3.6], x_length=6.2, y_length=4.2, xlabel=r"day of training",
                 ylabel=r"correct runs per rat (of 10)", xticks=[1, 2, 3, 4, 5], yticks=[0, 1, 2, 3],
                 center=[-3.2, -0.6, 0])
        ax = A.ax
        days, bright, dull = np.asarray(d["days"]), np.asarray(d["bright"]), np.asarray(d["dull"])

        def series(y, color):
            ln = VMobject(color=color, stroke_width=5).set_points_as_corners([ax.c2p(a, b) for a, b in zip(days, y)])
            pts = VGroup(*[Dot(ax.c2p(a, b), radius=0.09, color=color) for a, b in zip(days, y)])
            return VGroup(ln, pts)

        sb, sd_ = series(bright, P.ACCENT), series(dull, BLIND)
        lb = label(r"told ``maze-bright''", font_size=26, color=P.ACCENT).next_to(ax.c2p(5, bright[-1]), UL, buff=0.12)
        ld = label(r"told ``maze-dull''", font_size=26, color=BLIND).next_to(ax.c2p(5, dull[-1]), DL, buff=0.2)
        facts = VGroup(
            wrapped_label(r"the rats were ordinary laboratory rats; \ the labels were dealt at random", 5.4, 26,
                          WHITE),
            label(rf"``bright'': \ {d['mean_bright']:.2f} correct a day", font_size=30, color=P.ACCENT),
            label(rf"``dull'': \ {d['mean_dull']:.2f}", font_size=30, color=BLIND),
            label(rf"half as many again, \ from a label", font_size=30, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.24).move_to([4.0, -1.0, 0])
        teams = VGroup()
        for text, color in ((r"six students: \ ``your rats are maze-bright''", P.ACCENT),
                            (r"six students: \ ``your rats are maze-dull''", BLIND)):
            teams.add(VGroup(people_row(6, color, height=0.55, buff=0.14), label(text, font_size=24, color=color))
                      .arrange(DOWN, buff=0.1, aligned_edge=LEFT))
        teams.arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to([4.0, 1.75, 0]).align_to(facts, LEFT)
        src = historical_tag(archive.ROSENTHAL_FODE_1963.cite + r", Table 1")
        assert 1.45 < d["ratio"] < 1.55
        with self.voiceover(
            "Pfungst's lesson took half a century to sink in, and the man who drove it home was Robert Rosenthal. In "
            f"1963 he gave {d['experimenters']} students in a laboratory course five rats each to train in a "
            "simple maze. Half the students were told their rats had been bred for brightness. The other half "
            "were told theirs had been bred to be dull. <bookmark mark='a'/> The rats were ordinary rats, and "
            "the labels had been handed out at random. <bookmark mark='b'/> Over five days, the rats called "
            f"bright made {d['mean_bright']:.2f} correct runs a day. <bookmark mark='c'/> The rats called dull, "
            f"{d['mean_dull']:.2f}. <bookmark mark='d'/> Half as many again, from a word on a cage. The students "
            "who thought their rats were bright rated them as more pleasant, and by their own account handled "
            "them more, and more gently. Nobody cheated, again. <bookmark mark='e'/> A caution, though, of the kind this series owes you: it "
            "was one small study, and the Ledger will have something to say about it at the end of the part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(src))
            self.play(FadeIn(teams[0], shift=LEFT * 0.15))
            self.play(FadeIn(teams[1], shift=LEFT * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(facts[0], shift=LEFT * 0.15))
            vo.wait_until("b")
            self.play(Create(sb[0]), FadeIn(sb[1], lag_ratio=0.2), FadeIn(lb), FadeIn(facts[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(Create(sd_[0]), FadeIn(sd_[1], lag_ratio=0.2), FadeIn(ld), FadeIn(facts[2]), run_time=2.5)
            vo.wait_until("d")
            self.play(FadeIn(facts[3], shift=UP * 0.15))
        self.clear_scene()

    def classroom(self):
        d = load("expectancy")
        ra = d["raudenbush"]
        head = heading(r"From the maze to the classroom")
        hc = history_card(1968, r"Rosenthal and Jacobson, \ \emph{Pygmalion in the Classroom}", r"teachers are told "
                          r"that certain pupils, picked at random, are about to bloom", color=P.ARCHIVE, width=6.4,
                          font_size=26).move_to([-3.75, 1.75, 0])
        claim = wrapped_label(r"reported: \ a year later, the named children had gained more in IQ, most of all "
                              r"in the first two grades", 6.2, 27, WHITE).next_to(hc, DOWN, buff=0.35)
        claim.align_to(hc, LEFT)
        # the record
        unit = 7.0
        x0 = 0.9
        bars = VGroup()
        for i, (lab_, e, k) in enumerate(zip(ra["labels"], ra["effect"], ra["k"])):
            y = 1.35 - 1.2 * i
            w = abs(e) * unit
            bar = Rectangle(width=max(w, 0.03), height=0.55, stroke_width=0,
                            fill_color=STATUS_COLOR["replicated, smaller"] if e > 0.1 else GREY_B, fill_opacity=0.9)
            bar.move_to([x0 + (w / 2 if e >= 0 else -w / 2), y, 0])
            nm = label(lab_, font_size=26, color=WHITE)
            nm.next_to([x0, y + 0.3, 0], UP, buff=0.06).align_to([x0 + 0.1, 0, 0], LEFT)
            val = label(rf"${e:+.2f}$", font_size=32, color=WHITE).next_to(bar, RIGHT if e >= 0 else LEFT, buff=0.15)
            kk = label(rf"{k} experiments", font_size=20, color=GREY_B).next_to(val, RIGHT, buff=0.25)
            if e < 0:
                val.next_to([x0, y, 0], RIGHT, buff=0.15)
                kk.next_to(val, RIGHT, buff=0.25)
            bars.add(VGroup(bar, nm, val, kk))
        base = Line([x0, 1.95, 0], [x0, -1.45, 0], color=GREY_B, stroke_width=2)
        rec = VGroup(label(rf"the record: \ {ra['experiments']} experiments", font_size=28, color=WHITE),
                     label(r"effect on IQ, in standard deviations, by how long the teacher", font_size=21,
                           color=GREY_A),
                     label(r"had known the class before being told", font_size=21, color=GREY_A))
        rec.arrange(DOWN, aligned_edge=LEFT, buff=0.06).move_to([x0 - 0.1, 2.6, 0], aligned_edge=LEFT)
        keep_in_frame(rec)
        chip = status_chip("replicated, smaller", 26).next_to(bars, DOWN, buff=0.35).align_to(bars, LEFT)
        moral = wrapped_label(r"The effect is there while the teacher knows nothing else about the child, and gone "
                              r"once she does.", 12.6, 32, P.ACCENT).to_edge(DOWN, buff=0.8)
        src = published_tag(archive.RAUDENBUSH_1984.cite)
        with self.voiceover(
            "Rosenthal's next subjects were teachers. In a California elementary school, he and the principal, "
            "Lenore Jacobson, told teachers at the start of the year that a test had picked out certain children "
            "who were about to bloom. The children had been picked at random. <bookmark mark='a'/> A year later, "
            "they reported, the named children had gained more in IQ. The book, Pygmalion in the Classroom, "
            "became one of the most famous in education, and one of the most disputed. <bookmark mark='b'/> So "
            f"what happened when it was run again? By 1984 there were {ra['experiments']} experiments, and "
            "Stephen Raudenbush sorted them by one thing: how long the teachers had known their pupils before "
            f"they were told. <bookmark mark='c'/> Not at all: an effect of {ra['effect'][0]:.2f} standard "
            f"deviations. <bookmark mark='d'/> One week: {ra['effect'][1]:.2f}. <bookmark mark='e'/> More than "
            "two weeks: nothing. <bookmark mark='f'/> Which makes sense of the quarrel. A teacher who has "
            "watched a child for a fortnight believes her own eyes over a researcher's list. The effect is "
            "real, and smaller and more fragile than its legend."
        ) as vo:
            self.play(FadeIn(head), FadeIn(hc, shift=UP * 0.15))
            vo.wait_until("a")
            self.play(FadeIn(claim, shift=UP * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(rec), Create(base), FadeIn(src))
            for mark, b in zip("cde", bars):
                vo.wait_until(mark)
                self.play(FadeIn(b[1]), GrowFromEdge(b[0], LEFT), FadeIn(b[2]), FadeIn(b[3]))
            vo.wait_until("f")
            self.play(FadeIn(chip, scale=1.2), FadeIn(moral, shift=UP * 0.15))
        self.clear_scene()

    def dogs(self):
        d = load("expectancy")["dogs"]
        head = heading(r"2011: \ police dogs, and what their handlers believed")
        room = RoundedRectangle(width=6.4, height=3.6, corner_radius=0.1, stroke_color=GREY_B, stroke_width=2,
                                fill_color=PANEL_FILL, fill_opacity=1).move_to([-3.2, -0.2, 0])
        marker = Rectangle(width=0.5, height=0.36, stroke_width=0, fill_color=BIAS, fill_opacity=1)
        marker.move_to(room.get_center() + UR * 1.0)
        m_lab = label(r"a red paper: \ ``the scent is here''", font_size=22, color=BIAS)
        m_lab.next_to(room.get_corner(UL), DR, buff=0.15)
        nothing = label(r"no drug or explosive scent anywhere", font_size=26, color=TRUTH)
        nothing.next_to(room, DOWN, buff=0.2)
        rng = np.random.default_rng(3)
        alerts = VGroup()
        for k in range(26):
            near = k < 15
            pos = (marker.get_center() + np.append(np.clip(rng.normal(0, 0.35, 2), -0.65, 0.65), 0) if near else
                   room.get_center() + np.array([rng.uniform(-2.8, 2.8), rng.uniform(-1.5, 1.5), 0]))
            alerts.add(Star(n=5, outer_radius=0.11, inner_radius=0.05, stroke_width=0, fill_color=P.ACCENT,
                            fill_opacity=0.9).move_to(pos))
        facts = VGroup(
            label(rf"{d['teams']} certified handler-and-dog teams", font_size=30),
            label(rf"{d['alerts']} alerts", font_size=56, color=P.ACCENT),
            wrapped_label(r"every one of them wrong, and more of them where the handler had been told the scent "
                          r"was", 5.2, 28, WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.1, 0])
        sch = note(r"room: schematic").next_to(room, UP, buff=0.08).align_to(room, LEFT)
        src = published_tag(archive.LIT_2011.cite)
        with self.voiceover(
            "If you think this belongs to the nineteen-sixties, here is Clever Hans in 2011. Lisa Lit and her "
            f"colleagues took {d['teams']} certified police teams, a handler and a dog trained to find drugs or "
            "explosives, and had them search a set of rooms. <bookmark mark='a'/> There was no drug or explosive "
            "scent in any of them. In some rooms a piece of red paper was pinned up, and the handlers were told, "
            f"falsely, that it marked where the scent was. <bookmark mark='b'/> The teams reported {d['alerts']} "
            "alerts. Every one was a false alarm. <bookmark mark='c'/> And the alerts gathered where the "
            "handlers believed the scent to be. The dogs were reading their handlers, or the handlers were "
            "reading alerts into their dogs. Either way, the belief at one end of the leash came out as the "
            "evidence at the other. A blind search, where the handler doesn't know the layout, is the same "
            "remedy Pfungst found."
        ) as vo:
            self.play(FadeIn(head), FadeIn(room), FadeIn(sch), FadeIn(src), FadeIn(facts[0]))
            vo.wait_until("a")
            self.play(FadeIn(nothing), FadeIn(marker), FadeIn(m_lab))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(a, scale=1.6) for a in alerts], lag_ratio=0.08), FadeIn(facts[1]),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(FadeIn(facts[2], shift=UP * 0.15), Circumscribe(marker, color=BIAS, buff=0.5))
        self.clear_scene()

    def subject(self):
        d = load("expectancy")["demand"]
        head = heading(r"And the subject is trying to help")
        hc = history_card(1962, r"Martin Orne", r"\emph{demand characteristics}: \ the cues that tell a subject what "
                          r"the experiment is hoping for", color=P.ARCHIVE, width=8.2, font_size=30)
        hc.to_edge(UP, buff=1.2)
        fig = little_person(1.2, color=P.HUMAN).move_to([-6.2, -1.2, 0])
        thought = VGroup(*[label(t, font_size=28, color=GREY_A) for t in (
            r"``What is this study about?''", r"``What would a good subject do?''")])
        thought.arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(fig, RIGHT, buff=0.35)
        size = VGroup(
            label(r"measured in 2018, in eleven standard tasks:", font_size=26, color=GREY_A),
            label(rf"hypothesis hinted: \ about {d['weak_mean']:.2f} SD", font_size=30, color=P.ACCENT),
            label(rf"asked outright to go along: \ {d['strong'][0]:.2f} to {d['strong'][1]:.0f} SD", font_size=30,
                  color=BIAS),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([4.0, -1.25, 0])
        keep_in_frame(size)
        if size.get_left()[0] < thought.get_right()[0] + 0.4:
            size.scale_to_fit_width(6.9 - thought.get_right()[0] - 0.4).set_x((6.9 + thought.get_right()[0] + 0.4) / 2)
        placebo = wrapped_label(r"The same thing in medicine has an older name: \ the placebo.", 12.4, 30, WHITE)
        placebo.to_edge(DOWN, buff=0.8)
        # the two directions of the leak
        e_fig = VGroup(little_person(1.5, color=P.ACCENT), label(r"the experimenter", font_size=28, color=P.ACCENT))
        s_fig = VGroup(little_person(1.5, color=P.HUMAN), label(r"the subject", font_size=28, color=P.HUMAN))
        for f_ in (e_fig, s_fig):
            f_.arrange(DOWN, buff=0.15)
        e_fig.move_to([-3.4, 0.1, 0])
        s_fig.move_to([3.4, 0.1, 0])
        there = Arrow(e_fig[0].get_right() + UP * 0.35, s_fig[0].get_left() + UP * 0.35, buff=0.3, color=P.ACCENT,
                      stroke_width=5)
        back = Arrow(s_fig[0].get_left() + DOWN * 0.35, e_fig[0].get_right() + DOWN * 0.35, buff=0.3, color=TREAT,
                     stroke_width=5)
        t_lab = label(r"what the experimenter expects", font_size=26, color=P.ACCENT).next_to(there, UP, buff=0.1)
        b_lab = label(r"what the subject thinks is wanted", font_size=26, color=TREAT).next_to(back, DOWN, buff=0.1)
        leak = VGroup(e_fig, s_fig, there, back, t_lab, b_lab)
        src = published_tag(archive.DE_QUIDT_2018.cite)
        with self.voiceover(
            "So far the leak has run from the experimenter to the subject. It also runs the other way, and "
            "human subjects add something a horse doesn't: they think about why they're there. "
            "<bookmark mark='a'/> In 1962 Martin Orne pointed out that a person in an experiment is not a "
            "passive object. They're trying to work out what the study is about, and most of them want to be "
            "good subjects and help it succeed. He called the hints they use demand characteristics. "
            "<bookmark mark='b'/> How big is it? In 2018 three economists measured it directly, by hinting at "
            "the hypothesis on purpose. A hint moved behaviour by about a tenth of a standard deviation. Asking "
            "people outright to go along with it moved some tasks by a whole one. <bookmark mark='c'/> Medicine "
            "met the same thing earlier and called it the placebo: people who believe they've been treated "
            "report feeling better. In every case the cure is the one from the courtyard in Berlin. Arrange "
            "that the person who could leak the answer doesn't have it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(e_fig), FadeIn(s_fig))
            self.play(GrowArrow(there), FadeIn(t_lab))
            self.play(GrowArrow(back), FadeIn(b_lab), run_time=1.5)
            vo.wait_until("a")
            self.play(FadeOut(leak))
            self.play(FadeIn(hc, shift=UP * 0.15), FadeIn(fig))
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.15) for t in thought], lag_ratio=0.6), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(size[0]), FadeIn(src))
            self.play(FadeIn(size[1], shift=LEFT * 0.15))
            self.play(FadeIn(size[2], shift=LEFT * 0.15))
            vo.wait_until("c")
            self.play(FadeIn(placebo, shift=UP * 0.15))
        self.clear_scene()

    def blinds(self):
        head = heading(r"Who knows which condition this is?")
        cols = [r"the subject", r"the experimenter", r"the analyst"]
        designs = [(r"open", (True, True, True), BIAS), (r"single blind", (False, True, True), "#F2A65A"),
                   (r"double blind", (False, False, True), P.ACCENT), (r"triple blind", (False, False, False), TRUTH)]
        x = [-1.2, 2.2, 5.3]
        head_row = VGroup(*[label(c, font_size=30, color=WHITE).move_to([xi, 2.0, 0]) for c, xi in zip(cols, x)])
        figs = VGroup(*[little_person(0.7, color=P.HUMAN).next_to(h, UP, buff=0.15) for h in head_row])
        rows = VGroup()
        for i, (name, knows, color) in enumerate(designs):
            y = 1.0 - 1.05 * i
            nm = label(name, font_size=34, color=color).move_to([-6.6, y, 0], aligned_edge=LEFT)
            cells = VGroup()
            for k, xi in zip(knows, x):
                if k:
                    cells.add(label(r"knows", font_size=28, color=BIAS).move_to([xi, y, 0]))
                else:
                    cells.add(VGroup(RoundedRectangle(width=1.5, height=0.5, corner_radius=0.2, stroke_width=0,
                                                      fill_color=BLIND, fill_opacity=0.9),
                                     label(r"blind", font_size=26, color=BLACK)).move_to([xi, y, 0]))
            rows.add(VGroup(nm, cells))
        pf = label(r"Pfungst, 1904: \ ``procedure without knowledge''", font_size=28, color=P.ARCHIVE)
        pf.to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "That gives a small table that's worth carrying around. For any study, ask who knows which condition "
            "each subject is in. <bookmark mark='a'/> If everyone knows, the study is open, and everything in "
            "this chapter can happen. <bookmark mark='b'/> Keep it from the subject: single blind. That handles "
            "demand and the placebo. <bookmark mark='c'/> Keep it from the experimenter as well: double blind. "
            "That handles Hans, the rats and the dogs. <bookmark mark='d'/> And keep it from the person analysing "
            "the data until the analysis is fixed, which handles a leak we haven't met yet, and which fills "
            "Part 4. <bookmark mark='e'/> The first row of that table was invented in a courtyard, for a horse."
        ) as vo:
            self.play(FadeIn(head), FadeIn(head_row), FadeIn(figs))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r[0], shift=RIGHT * 0.15), LaggedStart(*[FadeIn(c) for c in r[1]], lag_ratio=0.3))
            vo.wait_until("e")
            self.play(FadeIn(pf, shift=UP * 0.15))
        self.clear_scene()
