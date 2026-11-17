from __future__ import annotations

from videos.psychology.psych30.common import *  # noqa: F403


class Field(VoiceoverScene):
    def construct(self):
        self.card()
        self.facts()
        self.model()
        self.run_field()
        self.curves()

    def card(self):
        card = chapter_card(8, r"A-not-B as dynamics", r"Is the error a missing concept, \ or a mind in motion?",
                            lit={1937: r"Piaget", 1985: r"Diamond", 2001: r"Thelen et al."}, part=PART,
                            scale=("circuit", "person"), marr=("how",))
        with self.voiceover("Chapter eight. A-not-B as dynamics."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def facts(self):
        head = heading(r"What the error depends on")
        rows = rows_of([
            (r"the A-not-B error is one of the most reliable findings in infancy research: \ around eight to twelve "
             r"months, \ infants reach back to A", WHITE),
            (r"but it depends on details a missing concept cannot explain: \ the delay between hiding and reaching, "
             r"\ the number of A trials, \ how different the two lids look, \ whether the infant's posture changes", OBJ),
            (r"Adele Diamond: \ the delay an infant can bridge without erring grows with age, \ month by month", LOOK),
            (r"with no delay, \ infants who make the error usually reach correctly", GOOD),
        ], 12.2, 25, 0.4).move_to([0, -0.2, 0])
        tag = published_tag(r"Diamond (1985); \ Thelen et al.\ (2001)")
        with self.voiceover(
            "Back to the error from the start of this part. <bookmark mark='a'/> The A-not-B error is one of the "
            "most reliable findings in infancy research: around eight to twelve months, infants reach back to A. "
            "<bookmark mark='b'/> But it depends on details that a missing concept can't explain: the delay between "
            "hiding and reaching, the number of A trials, how different the two lids look, even whether the "
            "infant's posture changes between trials. <bookmark mark='c'/> Adele Diamond showed that the delay an "
            "infant can bridge without erring grows with age, month by month. <bookmark mark='d'/> And with no "
            "delay at all, infants who make the error usually reach correctly. A concept you either have or don't "
            "would not behave like this."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def model(self):
        head = heading(r"Derivation: \ a field over where to reach")
        eq = MathTex(r"\tau\,\dot u(x,t) = -u + h + S(x,t) + c\,m(x) + \int w(x - x')\,\sigma(u(x',t))\,dx'",
                     font_size=34).move_to([0, 2.0, 0])
        rows = rows_of([
            (r"$u(x,t)$: \ activation for reaching in direction $x$; \ the reach goes where it peaks when the lids "
             r"come off", WHITE),
            (r"$S$: \ the two lids, \ always there, \ plus the cue where the toy was hidden, \ for a second", OBJ),
            (r"$w$: \ near neighbours excite each other, \ distant ones inhibit; \ $h$: \ the resting level", LOOK),
            (r"$m(x)$: \ a memory trace that grows wherever the infant reached: \ six reaches to A build it at A",
             A_COL),
            (r"Esther Thelen, \ Gregor Sch\"oner, \ Christian Scheier and Linda Smith, \ 2001: \ with a low resting "
             r"level the peak cannot sustain itself through the delay; \ a more cooperative field, \ as with age, "
             r"\ holds it", MODEL),
        ], 12.2, 23, 0.32).move_to([0, -1.0, 0])
        tag = psyche_tag(r"\texttt{develop.a\_not\_b}")
        with self.voiceover(
            "Esther Thelen, Gregor Schöner, Christian Scheier and Linda Smith proposed in 2001 that the error is "
            "dynamics, and wrote it as a neural field. <bookmark mark='a'/> u of x is the activation for reaching in "
            "direction x. The reach goes wherever it peaks when the lids come off. <bookmark mark='b'/> The input S "
            "is the two lids, always there, plus the cue where the toy was hidden, for a second or so. "
            "<bookmark mark='c'/> The interaction w makes near neighbours excite each other and distant ones "
            "inhibit; h is the field's resting level. <bookmark mark='d'/> And m is a memory trace that grows "
            "wherever the infant reached. Six reaches to A build it up at A. <bookmark mark='e'/> With a low resting "
            "level, a peak cannot sustain itself once the cue is gone. A more cooperative field, as with age, holds "
            "it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), Write(eq))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def run_field(self):
        d = load("anotb")
        head = heading(r"The B trial, \ three seconds of delay")
        x = np.asarray(d["x"])
        def panel(key, center, title, col):
            A = axes([-12, 12], [-8, 8], x_length=5.4, y_length=3.0, xticks=[-4, 4], yticks=[0],
                     xfmt=lambda v: "A" if v < 0 else "B", yfmt=lambda v: f"{v:g}", xlabel=r"reach direction",
                     ylabel=r"$u$", center=center, font_size=16)
            U = np.asarray(d[f"field_{key}"])
            t = ValueTracker(0)
            line = always_redraw(lambda: curve(A.ax, x, np.clip(U[min(int(t.get_value()), len(U) - 1)], -8, 8), col, 3))
            zero = DashedLine(A.ax.c2p(-12, 0), A.ax.c2p(12, 0), color=GREY_B, stroke_width=1.5)
            ttl = label(title, font_size=20, color=col).next_to(A, UP, buff=0.1)
            return A, line, zero, ttl, t, U
        A1, l1, z1, t1, tr1, U1 = panel("young", [-3.4, 0.3, 0], rf"younger: \ $h = {d['h_young']:.0f}$", A_COL)
        A2, l2, z2, t2, tr2, U2 = panel("old", [3.4, 0.3, 0], rf"older: \ $h = {d['h_old']:.0f}$", B_COL)
        r1 = "A" if d["reach_young"] < 0 else "B"
        r2 = "A" if d["reach_old"] < 0 else "B"
        foot = rows_of([
            (rf"the cue at B makes a peak in both; \ in the younger field it fades, \ and the memory of A wins: \ "
             rf"reach to {r1}", A_COL),
            (rf"the older field holds its peak at B through the delay: \ reach to {r2}", B_COL),
        ], 12.4, 22, 0.25).to_edge(DOWN, buff=0.7)
        tag = psyche_tag(r"\texttt{develop.field\_snapshot}")
        with self.voiceover(
            "Here is one simulated infant of each kind on the B trial, after six reaches to A, with three seconds "
            "of delay. <bookmark mark='a'/> The cue at B raises a peak in both fields. <bookmark mark='b'/> In the "
            "younger field the peak fades once the cue is gone, and the memory trace at A takes over: it reaches to "
            f"{r1}. <bookmark mark='c'/> The older field holds its peak at B through the delay, and reaches to {r2}. "
            "Nothing in either field is a concept of the object. The error comes from how fast activation fades and "
            "how strong the habit is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A1), FadeIn(A2), FadeIn(z1), FadeIn(z2), FadeIn(t1),
                      FadeIn(t2))
            self.add(l1, l2)
            vo.wait_until("a")
            self.play(tr1.animate.set_value(5), tr2.animate.set_value(5), run_time=2.0)
            vo.wait_until("b")
            self.play(tr1.animate.set_value(len(U1) - 1), tr2.animate.set_value(len(U2) - 1), FadeIn(foot[0]),
                      run_time=5.0, rate_func=linear)
            vo.wait_until("c")
            self.play(FadeIn(foot[1]))
        self.clear_scene()

    def curves(self):
        d = load("anotb")
        head = heading(r"Three hundred simulated infants per point")
        A = axes([0, 10], [0, 1.0], x_length=5.4, y_length=3.4, xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 0.5, 1.0],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"delay \ (seconds)",
                 ylabel=r"share reaching to A on B", center=[-3.4, -0.3, 0], font_size=16)
        cy = curve(A.ax, d["delays"], d["err_young"], A_COL, 4)
        co = curve(A.ax, d["delays"], d["err_old"], B_COL, 4)
        ca = curve(A.ax, d["delays"], d["acc_young"], GREY_B, 2)
        key = legend([(A_COL, r"younger field"), (B_COL, r"older field"), (GREY_B, r"younger: \ correct on A trials")],
                     font_size=15).move_to(A.ax.c2p(7.0, 0.85))
        na = d["n_a"]
        rows = rows_of([
            (r"no delay: \ no error; \ a delay of two or three seconds: \ almost every younger field errs", A_COL),
            (r"longer delays: \ the error falls back toward chance, \ because even the A trials become guesses \ "
             r"(the model predicts an inverted U)", GREY_A),
            (rf"more A trials, \ more error: \ at three seconds, \ {100 * d['err_by_na'][0]:.0f}\% after one A "
             rf"trial, \ {100 * d['err_by_na'][3]:.0f}\% after six", OBJ),
            (r"the older field never errs: \ development as a change in a parameter, \ not the arrival of a "
             r"concept", B_COL),
        ], 5.6, 21, 0.3).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{develop.a\_not\_b}: \ 300 simulated infants per point")
        with self.voiceover(
            "Now run three hundred simulated infants at each delay. <bookmark mark='a'/> With no delay, no "
            "younger field errs. With a delay of two or three seconds, almost all of them do. "
            "<bookmark mark='b'/> At longer delays the error falls back toward chance, because even the A trials "
            "become guesses: the model predicts an inverted U. "
            f"<bookmark mark='c'/> More A trials build more habit: at three seconds, {100 * d['err_by_na'][0]:.0f} "
            f"percent err after one A trial, and {100 * d['err_by_na'][3]:.0f} percent after six. "
            "<bookmark mark='d'/> And the older field never errs. Development here is a change in a parameter, the "
            "field's ability to hold a peak, not the arrival of a concept. Knowing where the toy is, it turns out, "
            "is not a yes-or-no possession."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A))
            vo.wait_until("a")
            self.play(Create(cy), Create(co), Create(ca), FadeIn(key), FadeIn(rows[0]), run_time=2.5)
            for m, r in zip("bcd", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
