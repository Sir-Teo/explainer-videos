from __future__ import annotations

from videos.stats.stats20.common import *  # noqa: F403


class Cleaning(VoiceoverScene):
    def construct(self):
        self.card()
        self.codebook()
        self.readings()
        self.implausible()
        self.funnel()
        self.meds()
        self.rules()

    def card(self):
        card = chapter_card(3, r"Cleaning", r"Every decision, \ in a log", part=PART)
        with self.voiceover("Chapter three. Cleaning."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))

    def codebook(self):
        d = load("clean")
        c = d["diet_codes"]
        rows = [
            cmath(r"\texttt{DR1DRSTZ} = 1", r":", rf"\text{{reliable recall: \ {c['1']:,}}}", font_size=28),
            cmath(r"\texttt{DR1DRSTZ} = 2", r":", rf"\text{{not reliable: \ {c['2']}}}", font_size=28),
            cmath(r"\texttt{DR1DRSTZ} = 5", r":", rf"\text{{not done: \ {c['5']}}}", font_size=28),
            cmath(r"\texttt{RIDAGEYR} = 80", r":", rf"\text{{``80 or older'': \ {d['age80']}}}", font_size=28),
            cmath(r"\texttt{BPXDI} = 0", r":", rf"\text{{a diastolic of zero: \ {d['dbp_zero']} readings}}", font_size=28),
        ]
        rows[3][2].set_color(OBS)
        rows[4][2].set_color(RES)
        whys = [why(r"adults 20+"), why(r"too few foods, \ or the interviewer's doubts"), why(r"refused or missed"),
                why(r"top-coded, \ for privacy: \ not an age"), why(r"sounds heard to zero: \ not a pressure")]
        with self.voiceover(
            "Cleaning starts with the codebook, because the numbers in a survey file aren't all measurements. "
            "<bookmark mark='a'/> The variable D R 1 D R S T Z rates each dietary recall: one means reliable, four thousand seven "
            "hundred and forty-two adults. <bookmark mark='b'/> Two means the interviewer judged it unreliable. "
            "<bookmark mark='c'/> Five means the recall wasn't done. Treat those codes as numbers and you'd be averaging "
            "nonsense. <bookmark mark='d'/> Age is top-coded: three hundred and eighty-two adults appear as eighty, meaning "
            "eighty or older, to protect the oldest from identification. <bookmark mark='e'/> And eighty-seven diastolic "
            "readings are zero, which happens when the examiner hears the pulse all the way down. It's a code for a "
            "measurement problem, not a blood pressure. We use only systolic pressure, but it's a warning to read the codebook "
            "first."
        ) as vo:
            step = ladder(self, rows, whys, keep=5, top=2.8, x=-0.8, buff=0.62, edge=6.9)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def readings(self):
        d = load("clean")
        nr = d["n_read"]
        cols = [("3", "three readings", HIT), ("2", "two", OBS), ("1", "one", SALT), ("0", "none", RES)]
        total = sum(nr[k] for k, _, _ in cols)
        bar = VGroup()
        for k, t, c in cols:
            w = 11.0 * nr[k] / total
            bar.add(Rectangle(width=max(w, 0.06), height=0.7, stroke_width=0, fill_color=c, fill_opacity=0.85))
        bar.arrange(RIGHT, buff=0.03).move_to([0, 1.6, 0])
        labs = VGroup(*[label(rf"{t}: \ {nr[k]:,}", font_size=20, color=c) for k, t, c in cols]).arrange(RIGHT, buff=0.6)
        labs.next_to(bar, DOWN, buff=0.3)
        rows = fit_rows(VGroup(
            label(r"the rule: \ average readings 2 and 3; \ if only one, \ use it", font_size=24),
            label(rf"first reading minus later ones: \ {d['first_minus_later']:+.1f} mm Hg on average", font_size=24, color=BP),
            label(r"the first is often higher: \ nerves, \ the cuff, \ the ``white coat''", font_size=22, color=GREY_A),
            label(r"none: \ the outcome is missing, \ so the adult leaves the sample", font_size=22, color=RES),
        ), 12.0, 0.35, [0, -1.5, 0])
        with self.voiceover(
            "<bookmark mark='a'/> Next, the outcome. Most adults have three systolic readings; seventy have two, thirty-five "
            "one, and two hundred and sixty-six none at all. <bookmark mark='b'/> Our rule, written in the plan: average the "
            "second and later readings, and if there's only one, use it. <bookmark mark='c'/> Why skip the first? Here the "
            "first reading is only half a millimetre higher than the later ones on average, <bookmark mark='d'/> but in many "
            "surveys it runs higher: people are nervous, or still settling, the white-coat effect. Clinical guidelines average "
            "later readings for the same reason. <bookmark mark='e'/> Adults with no reading have no outcome, and leave the "
            "sample. Whether that's harmless depends on why they're missing, the question of Part 41."
        ) as vo:
            vo.wait_until("a")
            self.play(LaggedStart(*[GrowFromEdge(b, LEFT) for b in bar], lag_ratio=0.3), FadeIn(labs), run_time=2.0)
            for k, m_ in enumerate("bcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def implausible(self):
        d = load("clean")
        rows = [
            cmath(r"\text{energy} < 500 \text{ kcal}", r":", rf"\text{{{d['kcal_low']} adults}}", font_size=28),
            cmath(r"\text{energy} > 5{,}000 \text{ kcal}", r":", rf"\text{{{d['kcal_high']} adults}}", font_size=28),
            cmath(r"\text{sodium} = 0", r":", rf"\text{{{d['na_zero']} adult}}", font_size=28),
            cmath(r"\text{largest sodium}", r":", rf"\text{{{d['na_max']:,.0f} mg in a day}}", font_size=28),
            cmath(r"\text{the rule}", r":", r"\text{impossible, \ by a rule fixed in advance}", font_size=28),
        ]
        rows[4][2].set_color(OBS)
        whys = [why(r"less than a day's minimum"), why(r"more than most athletes"), why(r"a day without salt?"),
                why(r"about 65 g of salt: \ kept, \ if the day is plausible"), why(r"not: \ surprising, \ or inconvenient")]
        with self.voiceover(
            "<bookmark mark='a'/> Some recalls can't be right. Fifty-seven adults report under five hundred kilocalories for "
            "the whole day, <bookmark mark='b'/> sixty-seven over five thousand. <bookmark mark='c'/> One reports no sodium at "
            "all, <bookmark mark='d'/> and the largest value is nearly twenty-six thousand milligrams, about sixty-five grams of "
            "salt in a day. <bookmark mark='e'/> The temptation is to delete whatever looks odd. The rule we use, fixed in "
            "advance, drops days with energy outside five hundred to five thousand kilocalories as implausible, and keeps "
            "everything else, however surprising. Deleting values because they're inconvenient is how analyses quietly "
            "produce the answer someone wanted."
        ) as vo:
            step = ladder(self, rows, whys, keep=5, top=2.8, x=-0.8, buff=0.62, edge=6.9)
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                step(k, transform=False)
        self.clear_scene()

    def funnel(self):
        d = load("clean")
        log = d["log"]
        n0 = log[0]["left"]
        bars, labs, rems = VGroup(), VGroup(), VGroup()
        for i, s in enumerate(log):
            w = 7.0 * s["left"] / n0
            y = 2.6 - i * 0.68
            col = SALT if i == len(log) - 1 else (NH if i == 0 else DES)
            bars.add(Rectangle(width=w, height=0.5, stroke_width=0, fill_color=col, fill_opacity=0.8).move_to([-0.4 + w / 2, y, 0]))
            labs.add(label(s["step"], font_size=20, color=GREY_A).move_to([-0.6, y, 0], aligned_edge=RIGHT))
            rems.add(label(rf"{s['left']:,}" + (rf" \ ($-${s['removed']:,})" if i else ""), font_size=20,
                           color=RES if s["removed"] > 300 else WHITE).next_to(bars[-1], RIGHT, buff=0.15))
        g = VGroup(bars, labs, rems)
        g.move_to([0.3, -0.1, 0])
        head = label(r"The decision log", font_size=32).to_edge(UP, buff=0.3)
        with self.voiceover(
            "<bookmark mark='a'/> Here is the whole decision log as a funnel. Five thousand five hundred and thirty-three "
            "examined adults of eighteen and over. <bookmark mark='b'/> Two hundred and sixty-eight are under twenty, outside the "
            "estimand; fifty-five are pregnant; two hundred and sixty-two have no pressure reading; four hundred have no "
            "reliable first recall; a hundred and nineteen have implausible energy; thirty-nine have no BMI. "
            "<bookmark mark='c'/> And the largest single step comes last: one thousand three hundred and nineteen adults are "
            "taking blood-pressure medicine. That leaves three thousand and seventy-one in the primary analysis. Every step is "
            "in the code, with its reason, and anyone can rerun it."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(GrowFromEdge(bars[0], LEFT), FadeIn(labs[0]), FadeIn(rems[0]))
            vo.wait_until("b")
            self.play(LaggedStart(*[AnimationGroup(GrowFromEdge(bars[i], LEFT), FadeIn(labs[i]), FadeIn(rems[i]))
                                    for i in range(1, len(log) - 1)], lag_ratio=0.6), run_time=8.0)
            vo.wait_until("c")
            self.play(GrowFromEdge(bars[-1], LEFT), FadeIn(labs[-1]), FadeIn(rems[-1]))
        self.wait(1.0)
        self.clear_scene()

    def meds(self):
        r = load("reverse")
        rows = fit_rows(VGroup(
            label(rf"on BP medicine: \ {100 * r['meds_share']:.0f}\% of adults", font_size=26, color=BP),
            label(r"their pressure reflects the drug, \ not the diet", font_size=24),
            label(r"so the primary sample excludes them, \ and the estimand changes:", font_size=24, color=OBS),
            label(r"``US adults 20+ \emph{not taking blood-pressure medicine}''", font_size=26, color=SALT),
            label(r"a cleaning step that redefines the question must say so, \ in the report", font_size=22, color=RES),
        ), 12.4, 0.45, [0, 0, 0])
        with self.voiceover(
            "<bookmark mark='a'/> That last step deserves a pause. Twenty-four percent of American adults take medicine for "
            "blood pressure. <bookmark mark='b'/> Their pressure reflects the drug far more than their diet, so including them "
            "would blur the very relationship we're after. <bookmark mark='c'/> But dropping them is not just cleaning: it "
            "changes the estimand. <bookmark mark='d'/> Our population is now American adults not taking blood-pressure "
            "medicine, a younger and healthier group. <bookmark mark='e'/> That's a legitimate choice, made in advance, but the "
            "report has to state it plainly, and chapter eight will show what happens if we choose otherwise."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()

    def rules(self):
        rows = fit_rows(VGroup(
            label(r"read the codebook before the data", font_size=24),
            label(r"never overwrite the raw file; \ clean in code, \ from the raw file, \ every time", font_size=24, color=DES),
            label(r"log every exclusion: \ what, \ why, \ how many", font_size=24, color=OBS),
            label(r"rules fixed in advance; \ never ``remove the outliers'' after the fit", font_size=24, color=RES),
            label(r"a step that changes the population changes the estimand: \ say so", font_size=24, color=SALT),
        ), 12.4, 0.5, [0, 0, 0])
        with self.voiceover(
            "So the rules of cleaning. <bookmark mark='a'/> Read the codebook before the data. <bookmark mark='b'/> Never edit "
            "the raw file: do every step in code, starting from the original download, so the whole chain can be rerun. "
            "<bookmark mark='c'/> Log each exclusion, with its reason and its count. <bookmark mark='d'/> Fix the rules before "
            "fitting, and never drop points afterwards because they pull the line the wrong way. <bookmark mark='e'/> And when a "
            "step changes who is in the population, it changes the question, and the report must say so."
        ) as vo:
            for k, m_ in enumerate("abcde"):
                vo.wait_until(m_)
                self.play(FadeIn(rows[k], shift=RIGHT * 0.2))
        self.clear_scene()
