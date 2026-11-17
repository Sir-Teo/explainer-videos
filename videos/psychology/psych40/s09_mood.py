from __future__ import annotations

from videos.psychology.psych40.common import *  # noqa: F403


class Mood(VoiceoverScene):
    def construct(self):
        self.card()
        self.anhedonia()
        self.model()
        self.activation()

    def card(self):
        card = chapter_card(8, r"Reward and mood", r"Is low mood a learning signal gone flat?",
                            lit={2014: r"Rutledge et al."}, part=PART, scale=("circuit", "person"), marr=("what", "how"))
        with self.voiceover("Chapter eight. Reward and mood."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def anhedonia(self):
        head = heading(r"Anhedonia")
        rows = rows_of([
            (r"anhedonia, \ the loss of interest or pleasure, \ is one of depression's two core symptoms", WHITE),
            (r"Part 17's dopamine signal is a reward prediction error: \ how much better or worse things went than "
             r"expected", SYMP),
            (r"anhedonia could be a blunted response to those errors, \ less learning from good outcomes, \ or "
             r"less willingness to spend effort for reward", MODEL),
            (r"the three predict different things, \ and tasks that separate them are a frontier of Part 59's "
             r"computational psychiatry", YOU),
        ], 12.4, 23, 0.46).move_to([0, -0.3, 0])
        with self.voiceover(
            "Depression is also a problem of reward. <bookmark mark='a'/> Anhedonia, the loss of interest or "
            "pleasure, is one of its two core symptoms. <bookmark mark='b'/> In Part 17, dopamine carried a reward "
            "prediction error: how much better or worse things went than expected. <bookmark mark='c'/> Anhedonia "
            "could be a blunted response to those errors, less learning from good outcomes, or less willingness to "
            "spend effort for reward. <bookmark mark='d'/> The three predict different things, and tasks that tell "
            "them apart are a frontier of computational psychiatry, in Part 59."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def model(self):
        d = load("mood")
        head = heading(r"Momentary mood, \ modelled")
        n = len(d["happy"])
        t = np.arange(n)
        A = axes([0, n], [-1.5, 2.5], x_length=6.0, y_length=2.4, xticks=[0, 30, 60, 90], yticks=None,
                 xfmt=lambda v: f"{v:.0f}", xlabel=r"trial", ylabel=r"happiness", center=[-2.9, 0.9, 0], font_size=13)
        dots = scatter(A.ax, t, d["happy"], PERSON, radius=0.035)
        fit = curve(A.ax, t, d["fit"], MODEL, stroke_width=3)
        blunt = curve(A.ax, t, d["blunted"], AUTH, stroke_width=2)
        eq = MathTex(r"H_t = w_0 + w_1 \sum \gamma^{t-j} CR_j + w_2 \sum \gamma^{t-j} EV_j + w_3 \sum \gamma^{t-j} RPE_j",
                     font_size=26, color=MODEL).move_to([-2.9, -1.0, 0])
        rows = rows_of([
            (r"Rutledge and colleagues, \ 2014: \ in a gambling task, \ people rated their happiness every few "
             r"trials", WHITE),
            (r"happiness was explained by a decaying sum of recent certain rewards, \ expected values, \ and above "
             r"all reward prediction errors, \ in the lab and in thousands of smartphone players", PERSON),
            (rf"Psyche simulates 90 trials and fits the model: \ the prediction-error weight comes back as "
             rf"{d['w'][3]:.2f}, \ with forgetting $\gamma = {d['gamma']:.2f}$", MODEL),
            (rf"blunt the prediction errors to 40\%, \ and mood swings shrink: \ its SD falls from "
             rf"{d['sd_normal']:.2f} to {d['sd_blunted']:.2f}, \ a flat mood that good news barely moves", AUTH),
        ], 5.6, 19, 0.34).move_to([3.6, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.mood\_task}, \ \texttt{fit\_mood}; \ Rutledge et al.\ (2014)")
        with self.voiceover(
            "Mood itself can be modelled. <bookmark mark='a'/> In 2014 Robb Rutledge and colleagues had people "
            "rate their happiness every few trials of a gambling task. <bookmark mark='b'/> Happiness was explained "
            "by a decaying sum of recent certain rewards, expected values, and above all reward prediction errors. "
            "It held in the lab and in thousands of people playing on smartphones. <bookmark mark='c'/> Psyche "
            "simulates ninety trials and fits the model. The prediction-error weight comes back close to its true "
            "value. <bookmark mark='d'/> Now blunt the prediction errors to forty percent. The mood swings shrink: "
            "a flat mood that good news barely moves. It's one way anhedonia might look from the inside."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(dots))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), FadeIn(eq))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(fit), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), Create(blunt), run_time=2.0)
        self.clear_scene()

    def activation(self):
        d = load("activation")
        head = heading(r"The trap of doing less")
        n = len(d["alone_est"])
        t = np.arange(n)
        A = axes([0, n], [-0.7, 0.9], x_length=5.6, y_length=2.6, xticks=[0, 30, 60, 90], yticks=[-0.5, 0, 0.5],
                 xfmt=lambda v: f"{v:.0f}", yfmt=lambda v: f"{v:.1f}", xlabel=r"day", ylabel=r"expected value of "
                 r"acting", center=[-3.3, 0.9, 0], font_size=13)
        rest = DashedLine(A.ax.c2p(0, 0.2), A.ax.c2p(n, 0.2), color=GREY_B, stroke_width=1.5)
        r_l = label(r"resting", font_size=12, color=GREY_B).next_to(A.ax.c2p(n, 0.2), UP, buff=0.05)
        alone = curve(A.ax, t, d["alone_est"], AUTH, stroke_width=3)
        sched = curve(A.ax, t, d["scheduled_est"], GOOD, stroke_width=3)
        ticks = []
        for key, c, y in (("alone_act", AUTH, -1.25), ("scheduled_act", GOOD, -1.6)):
            g_ = VGroup()
            for day in np.flatnonzero(np.asarray(d[key]) > 0):
                x = A.ax.c2p(float(day), 0)[0]
                g_.add(Line([x, y - 0.1, 0], [x, y + 0.1, 0], color=c, stroke_width=2))
            ticks.append(g_)
        t_l = label(r"days active: \ left alone (red), \ scheduled for a fortnight (green)", font_size=13,
                    color=GREY_B).move_to([-3.3, -2.05, 0])
        rows = rows_of([
            (r"Psyche: \ each day, \ an activity whose rewards must be tried to be known, \ or rest, \ with a "
             r"small reward it knows", WHITE),
            (rf"after a loss its estimate of acting is low, \ so it rests, \ never tests the estimate, \ and in "
             rf"the last month is active on {pct(d['alone_share'])} of days", AUTH),
            (rf"schedule the activity for two weeks regardless of mood: \ the estimate is corrected, \ and it is "
             rf"active on {pct(d['scheduled_share'])} of days", GOOD),
            (r"that is behavioural activation: \ act first, \ let the learning follow; \ in trials it does about "
             r"as well as cognitive therapy (Part 42)", YOU),
        ], 6.0, 19, 0.34).move_to([3.4, -0.2, 0])
        tag = psyche_tag(r"\texttt{clinic.activation}, \ median of 21 runs")
        with self.voiceover(
            "Low mood can also trap itself, the way avoidance trapped fear. <bookmark mark='a'/> In Psyche, each day "
            "brings a choice: an activity whose rewards can only be known by trying it, or rest, with a small reward "
            "it already knows. <bookmark mark='b'/> After a loss, its estimate of acting is low, so it rests, and "
            "never tests the estimate. In the last month it's hardly ever active. <bookmark mark='c'/> Now schedule "
            "the activity for two weeks, whatever the mood. The estimate is corrected, and it stays active. "
            "<bookmark mark='d'/> That's behavioural activation: act first, and let the learning follow. In trials it "
            "does about as well as cognitive therapy, which Part 42 weighs."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(rest), FadeIn(r_l), FadeIn(t_l))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), Create(alone), FadeIn(ticks[0]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), Create(sched), FadeIn(ticks[1]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
