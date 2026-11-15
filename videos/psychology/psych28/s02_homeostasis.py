from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Homeostasis(VoiceoverScene):
    def construct(self):
        self.card()
        self.history()
        self.derive()
        self.integral()
        self.limits()

    def card(self):
        card = chapter_card(1, r"Drives and homeostasis", r"Is a motive a control loop?",
                            lit={1865: r"Bernard", 1932: r"Cannon", 1943: r"Hull"},
                            part=PART, scale=("brain", "mind"), marr=("what", "how"))
        with self.voiceover("Chapter one. Drives and homeostasis."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def history(self):
        head = heading(r"Keeping the inside constant")
        items = [
            (r"1865", r"Claude Bernard: \ the body keeps an internal environment constant, \ whatever the world "
                      r"outside does", BODY),
            (r"1932", r"Walter Cannon, \ \emph{The Wisdom of the Body}: \ homeostasis, \ temperature, \ salt, "
                      r"\ sugar and water held near set values by feedback", BODY),
            (r"1943", r"Clark Hull: \ a need produces a drive, \ an aversive state; \ whatever reduces the drive is "
                      r"reinforced, \ and that is learning", WANT),
        ]
        rows = VGroup()
        for yr, txt, c in items:
            rows.add(VGroup(label(yr, font_size=30, color=c), wrapped_label(txt, 10.6, 26, WHITE)).arrange(
                RIGHT, buff=0.4, aligned_edge=UP))
        for r in rows:
            r[1].shift(RIGHT * (1.4 - r[0].width))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([0, 0.1, 0])
        tag = historical_tag(r"Bernard (1865); \ Cannon (1932); \ Hull (1943)")
        with self.voiceover(
            "The oldest answer to why animals act is that they are keeping something constant. "
            "<bookmark mark='a'/> In the 1860s the French physiologist Claude Bernard argued that the body keeps an "
            "internal environment steady whatever the world outside does. <bookmark mark='b'/> In 1932 Walter "
            "Cannon named the idea homeostasis: temperature, salt, sugar and water, each held near a set value by "
            "feedback. <bookmark mark='c'/> And in 1943 Clark Hull built a theory of behaviour on it. A need creates "
            "a drive, an unpleasant state of arousal. Anything that reduces the drive is reinforced, and that, for "
            "Hull, was what learning is."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abc", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def derive(self):
        d = load("thermostat")
        head = heading(r"Derivation: \ a thermostat")
        eqs = VGroup(
            MathTex(r"\frac{dx}{dt} = -k\,(x - s) + D", font_size=40),
            MathTex(r"x(t) = s + \frac{D}{k} + \Big(x_0 - s - \frac{D}{k}\Big) e^{-kt}", font_size=36),
            MathTex(r"D = 0: \ x \to s, \quad t_{1/2} = \frac{\ln 2}{k}", font_size=34),
            MathTex(r"D \ne 0: \ x \to s + \frac{D}{k}", font_size=34, color=LOST),
        ).arrange(DOWN, buff=0.45).move_to([3.4, 0.2, 0])
        A = axes([0, 80], [12, 22], x_length=5.8, y_length=3.6, xticks=[0, 20, 40, 60, 80], yticks=[14, 16, 18, 20],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"minutes", ylabel=r"temperature, \ C",
                 center=[-3.3, -0.2, 0], font_size=16)
        setl = DashedLine(A.ax.c2p(0, 20), A.ax.c2p(80, 20), color=GREY_B, stroke_width=2)
        cp = curve(A.ax, d["t"], d["p"], BODY, 4)
        win = label(r"a window opens", font_size=16, color=LOST).next_to(A.ax.c2p(20, 15.2), DOWN, buff=0.1)
        tag = psyche_tag(r"\texttt{drive.thermostat}: \ $k = 0.2$ a minute")
        with self.voiceover(
            "The simplest such loop is a thermostat, and it's worth deriving. <bookmark mark='a'/> Let x be the "
            "room's temperature and s the set point. The heater pushes back in proportion to the error, at a rate "
            "k, and the world adds a disturbance D. <bookmark mark='b'/> This equation can be solved exactly. The "
            "temperature approaches its resting value exponentially. <bookmark mark='c'/> With no disturbance it "
            "returns to the set point, and half the error is gone after ln 2 over k, about three and a half minutes "
            "here. <bookmark mark='d'/> But open a window, a constant disturbance, and the loop settles somewhere "
            "else: at the set point plus D over k. A loop that only pushes in proportion to the error has to be "
            f"off by something to push at all. Here it settles at {d['p_end']:.0f} degrees, not 20."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(setl))
            vo.wait_until("a")
            self.play(Write(eqs[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), Create(cp), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(eqs[2]))
            vo.wait_until("d")
            self.play(FadeIn(eqs[3]), FadeIn(win))
        self.clear_scene()

    def integral(self):
        d = load("thermostat")
        head = heading(r"Remembering the error")
        A = axes([0, 80], [12, 22], x_length=5.8, y_length=3.6, xticks=[0, 20, 40, 60, 80], yticks=[14, 16, 18, 20],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"minutes", ylabel=r"temperature, \ C",
                 center=[-3.3, -0.2, 0], font_size=16)
        setl = DashedLine(A.ax.c2p(0, 20), A.ax.c2p(80, 20), color=GREY_B, stroke_width=2)
        cp = curve(A.ax, d["t"], d["p20"], BODY, 3)
        ci = curve(A.ax, d["t"], d["pi20"], INTR, 4)
        key = legend([(BODY, r"in proportion to the error"), (INTR, r"plus its running total")], font_size=17)
        key.move_to(A.ax.c2p(52, 16.6))
        eq = MathTex(r"\frac{dx}{dt} = -k\,(x - s) - k_i \!\int_0^t (x - s)\,d\tau + D", font_size=34)
        rows = rows_of([
            (r"add a term that pushes in proportion to the accumulated error, \ and the steady error vanishes: "
             r"\ integral control", INTR),
            (rf"the same window: \ the room dips to {d['pi_low']:.1f} C, \ then returns to {d['pi_end']:.0f} C", WHITE),
            (r"bodies do both: \ a fast response to the error now, \ and slower changes that build up while the "
             r"error lasts", BODY),
            (r"the set point itself can move: \ fever raises the thermostat; \ that is allostasis, \ regulation by "
             r"anticipation and need", WANT),
        ], 5.6, 22, 0.32)
        right = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.45).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.thermostat}: \ $k_i = 0.05$")
        with self.voiceover(
            "Engineers fix the steady error by giving the loop a memory. <bookmark mark='a'/> Add a term that pushes "
            "in proportion to the accumulated error, its running total, and the only resting state is zero error. "
            "That's called integral control. <bookmark mark='b'/> Start at the set point and open the same window. "
            f"The room dips to {d['pi_low']:.1f} degrees, and then returns to {d['pi_end']:.0f}. "
            "<bookmark mark='c'/> Bodies use both kinds of "
            "correction: fast responses to the error right now, and slower changes, in hormones and in behaviour, "
            "that build up while the error lasts. <bookmark mark='d'/> And the set point itself can move. A fever is "
            "the thermostat turned up on purpose. Regulation that changes the target in anticipation of need is "
            "sometimes called allostasis."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(setl), FadeIn(cp), FadeIn(eq))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Create(ci), FadeIn(key), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def limits(self):
        head = heading(r"What drive reduction cannot explain")
        rows = rows_of([
            (r"rats work for saccharin, \ which is sweet and has no calories: \ no need is reduced", WANT),
            (r"monkeys solve puzzles and open windows for nothing but the solving and the view \ (chapter three)",
             INTR),
            (r"the rat at the lever: \ the current raises arousal, \ and is sought anyway", LOST),
            (r"what survives of Hull: \ the loops are real, \ and needs change how much things are worth; \ but "
             r"behaviour is pulled by incentives, \ not only pushed by drives", WHITE),
        ], 12.2, 27, 0.42).move_to([0, -0.2, 0])
        tag = historical_tag(r"Sheffield \& Roby (1950); \ Olds \& Milner (1954)")
        with self.voiceover(
            "Drive reduction explained a great deal, and then ran into animals doing things for no need at all. "
            "<bookmark mark='a'/> Rats work for saccharin, which is sweet and has no calories, so no need is reduced. "
            "<bookmark mark='b'/> Monkeys solve mechanical puzzles and open windows just to look out, as we'll see "
            "in chapter three. <bookmark mark='c'/> And the rat at the lever was seeking stimulation that raised its "
            "arousal rather than lowering it. <bookmark mark='d'/> What survived is this. The loops are real, and a "
            "need changes how much things are worth: food is worth more to the hungry. But behaviour is pulled "
            "toward incentives as well as pushed by drives, and that pull is where the rest of this part lives."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
