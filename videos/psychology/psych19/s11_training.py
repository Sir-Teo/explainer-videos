from __future__ import annotations

from videos.psychology.psych19.common import *  # noqa: F403


class Training(VoiceoverScene):
    def construct(self):
        self.card()
        self.jaeggi()
        self.controls()
        self.simulation()
        self.verdict()

    def card(self):
        card = chapter_card(10, r"Can you train it?", r"Does practising a memory task make you smarter?",
                            lit={2008: r"Jaeggi et al.", 2013: r"Redick et al.", 2016: r"Simons et al."}, part=PART,
                            scale=("person", "culture"), marr=("what",))
        with self.voiceover("Chapter ten. Can you train it?"):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def jaeggi(self):
        p = archive.JAEGGI_2008.data
        head = heading(r"Dual n-back, \ and a claim about intelligence")
        grid = VGroup(*[Square(0.55, color=GREY_C, stroke_width=2) for _ in range(9)]).arrange_in_grid(3, 3, buff=0.06)
        grid.move_to([-4.2, 1.3, 0])
        lit = grid[5].copy().set_fill(LOOP, 0.8)
        letter = label(r"``K''", font_size=34, color=MEM).next_to(grid, RIGHT, buff=0.35)
        cap = wrapped_label(r"press if the square, \ or the spoken letter, \ matches the one 2 back", 4.2, 20,
                            GREY_A).next_to(grid, DOWN, buff=0.2)
        keep_in_frame(cap)
        rows = rows_of([
            (r"2008: \ Jaeggi, \ Buschkuehl, \ Jonides and Perrig; \ a place and a letter at once, \ each to be "
             r"matched with $n$ steps back", WHITE),
            (r"the task gets harder as you improve: \ $n$ climbs", GREY_A),
            (rf"groups trained for {p['training_days'][0]}, \ {p['training_days'][1]}, \ {p['training_days'][2]} or "
             rf"{p['training_days'][3]} days; \ gains on a reasoning test grew with training", MEM),
            (r"a no-contact control; \ short, \ speeded tests; \ small groups", LOST),
            (r"the paper launched an industry, \ and a decade of replications", EXEC),
        ], 6.6, 23, 0.3).move_to([3.0, 0.3, 0])
        tag = published_tag(archive.JAEGGI_2008.cite)
        with self.voiceover(
            "In 2008 a paper in the Proceedings of the National Academy of Sciences made a striking claim. "
            "<bookmark mark='a'/> Susanne Jaeggi, Martin Buschkuehl, John Jonides and Walter Perrig trained young "
            "adults on the dual n-back task: a square lights up on a grid while a letter is spoken, and you press a "
            "key whenever the place, or the letter, matches the one n steps back. <bookmark mark='b'/> As you improve, "
            "n goes up, so the task never gets easy. <bookmark mark='c'/> Groups trained for "
            f"{p['training_days'][0]}, {p['training_days'][1]}, {p['training_days'][2]} or {p['training_days'][3]} "
            "days, and their gains on a test of fluid reasoning grew with the amount of training. Training working "
            "memory, the authors concluded, could improve fluid intelligence. <bookmark mark='d'/> The design had "
            "weaknesses that matter: the comparison group simply had no contact between tests, the reasoning tests "
            "were shortened and timed, and the groups were small. <bookmark mark='e'/> It also arrived at the right "
            "moment for a new business."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(grid), FadeIn(lit), FadeIn(letter), FadeIn(cap))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def controls(self):
        p = archive.REDICK_2013.data
        q = archive.MELBY_LERVAG_2016.data
        head = heading(r"What happened with an active control")
        rows = rows_of([
            (rf"2013: \ Redick and colleagues: \ {p['sessions']} sessions of dual n-back, \ against {p['sessions']} "
             r"of an adaptive visual search game, \ and a no-contact group", WHITE),
            (r"everyone improved on what they practised; \ nobody improved on the tests of reasoning, \ memory and "
             r"speed", MEM),
            (r"a placebo control matters: \ people who believe they were trained expect to do better, \ and try harder",
             EXEC),
            (rf"2016: \ Melby-Lerv\aa{{}}g, \ Redick and Hulme: \ {q['publications']} publications, \ "
             rf"{q['comparisons']} comparisons", DATA),
            (r"gains on similar memory tasks, \ near transfer; \ against active controls, \ no reliable far transfer",
             MEM),
            (r"and no relation between how much memory improved and how much anything else did", LOST),
        ], 12.4, 26, 0.32).move_to([0, -0.2, 0])
        tag = published_tag(archive.MELBY_LERVAG_2016.cite)
        with self.voiceover(
            "The replications came quickly. <bookmark mark='a'/> In 2013 Thomas Redick and his colleagues gave "
            f"people {p['sessions']} sessions of dual n-back, and compared them both with a group that did "
            f"{p['sessions']} sessions of an adaptive visual search game, a placebo that feels like training, and "
            "with a no-contact group. <bookmark mark='b'/> Everyone improved at what they practised. Nobody improved "
            "on the measures of reasoning, memory capacity, multitasking and speed. <bookmark mark='c'/> The active "
            "control matters because people who believe they've been trained expect to improve, and try harder at "
            "the post-test. A no-contact group can't control for that. <bookmark mark='d'/> By 2016 Monica "
            f"Melby-Lervåg, Redick and Charles Hulme could meta-analyse {q['publications']} publications with "
            f"{q['comparisons']} comparisons. <bookmark mark='e'/> Training produced reliable gains on similar memory "
            "tasks, near transfer, and, against active controls, no convincing far transfer to reasoning, reading or "
            "arithmetic. <bookmark mark='f'/> And how much a person's memory improved didn't predict how much "
            "anything else did, which is what transfer would require."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def simulation(self):
        d = load("training")
        head = heading(r"Psyche runs 400 training trials")
        edges = np.linspace(-1.2, 1.6, 29)
        A = axes([-1.2, 1.6], [0, 1.6], x_length=5.6, y_length=3.0, xticks=[-1, 0, 1], yticks=[],
                 xlabel=r"effect on reasoning, \ Cohen's $d$", ylabel=r"share of trials", center=[-3.4, 0.6, 0],
                 font_size=17)
        hp = hist(A.ax, edges, np.histogram(d["passive_far"], edges, density=True)[0], LOST, opacity=0.5)
        ha = hist(A.ax, edges, np.histogram(d["active_far"], edges, density=True)[0], MODEL, opacity=0.5)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(0, 1.6), color=GREY_B, stroke_width=2)
        key = legend([(LOST, r"against a no-contact control"), (MODEL, r"against an active control")], font_size=18)
        key.next_to(A, DOWN, buff=0.3)
        sig_p = float(np.mean(d["passive_far"] > 0.45))
        rows = rows_of([
            (r"the truth, \ known: \ near transfer $d = 0.6$, \ far transfer $0$, \ expectation $0.25$ on anything", WHITE),
            (rf"no-contact control: \ mean far effect {np.mean(d['passive_far']):.2f}; \ {pct(sig_p)} of trials "
             r"look like success", LOST),
            (rf"active control: \ mean {np.mean(d['active_far']):.2f}; \ the expectation cancels", MODEL),
            (r"40 people a group: \ wide scatter, \ so a single trial can show almost anything", GREY_A),
        ], 5.4, 22, 0.32).move_to([3.85, 0.3, 0])
        ptag = psyche_tag(r"\texttt{wm.training\_trial}: \ reliability 0.8, \ 400 trials per design")
        with self.voiceover(
            "Psyche can show why the control group decides the answer. <bookmark mark='a'/> In this simulation the "
            "truth is known: training improves the trained kind of task by six tenths of a standard deviation, "
            "improves reasoning by exactly nothing, and anyone who believes they were trained gains a quarter of a "
            "standard deviation on any test, from effort and expectation. Each trial has forty people a group. "
            "<bookmark mark='b'/> Against a no-contact control, the average effect on reasoning is about "
            f"{np.mean(d['passive_far']):.2f}, and {pct(sig_p)} of trials find an effect larger than a typical "
            "published one. <bookmark mark='c'/> Against an active control, who also believe they were trained, "
            f"the expectation cancels and the average is {np.mean(d['active_far']):.2f}. <bookmark mark='d'/> And with "
            "forty people a group, single trials scatter widely either way. Which trials get published, and talked "
            "about, is the subject of Part 4."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), Create(zero), FadeIn(ptag))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(hp), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(ha), FadeIn(key), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def verdict(self):
        s = archive.SIMONS_2016.data
        f = archive.FTC_LUMOSITY_2016.data
        head = heading(r"Scientists, \ and then a regulator")
        rows = rows_of([
            (rf"2014: \ about {s['consensus_signatories']} scientists sign a consensus: \ brain-game claims are "
             r"frequently exaggerated and at times misleading", WHITE),
            (r"weeks later, \ more than a hundred others reply: \ some training has benefits", GREY_A),
            (r"2016: \ Simons and colleagues review the evidence cited by the companies themselves", EXEC),
            (r"improvement on the trained tasks; \ little on closely related ones; \ little evidence for everyday "
             r"cognition", MEM),
            (rf"January 2016: \ the Federal Trade Commission and Lumosity: \ \$2 million in refunds, \ a "
             rf"\$50 million judgment suspended", LOST),
            (r"and an order: \ no claims about cognition without competent and reliable scientific evidence", DATA),
        ], 12.4, 26, 0.32).move_to([0, -0.2, 0])
        tag = published_tag(archive.SIMONS_2016.cite)
        with self.voiceover(
            "The argument moved outside the laboratory. <bookmark mark='a'/> In 2014 about seventy scientists, "
            "organised by the Stanford Center on Longevity and the Max Planck Institute for Human Development, signed "
            "a statement that claims for brain games were frequently exaggerated and at times misleading. "
            "<bookmark mark='b'/> Weeks later more than a hundred others signed a reply arguing that some forms of "
            "training do have benefits. <bookmark mark='c'/> In 2016 Daniel Simons and six colleagues reviewed the "
            "studies the companies themselves cited. <bookmark mark='d'/> They found plenty of evidence that people "
            "improve on the trained tasks, less that they improve on closely related tasks, and little that training "
            "improves everyday cognition. <bookmark mark='e'/> In January 2016 the Federal Trade Commission settled "
            "with the makers of Lumosity over its advertising: two million dollars in refunds, with a fifty million "
            "dollar judgment suspended. <bookmark mark='f'/> The order forbids claims about cognitive benefits "
            "without competent and reliable scientific evidence, which is a sentence the Ledger would happily adopt."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcdef", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
