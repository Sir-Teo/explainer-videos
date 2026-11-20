from __future__ import annotations

from videos.economics.econ29.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.paper()
        self.twins()
        self.question()
        self.title()
        self.objectives()

    def paper(self):
        rows = VGroup(
            label(r"\emph{Econometrica}, \ November 1982", font_size=30, color=E.ACCENT),
            label(r"Finn Kydland and Edward Prescott, \ ``Time to Build and Aggregate Fluctuations''", font_size=24,
                  color=GREY_A),
            label(r"take the growth model; \ add random shocks to technology; \ choose the numbers from growth facts",
                  font_size=23, color=TECH),
            label(r"the result looks like the American business cycle", font_size=24, color=OUTPUT),
            label(r"if so, \ recessions are not failures, \ and policy has nothing to fix", font_size=24,
                  color=HOLD),
            label(r"the claim was mostly wrong; \ the method won completely", font_size=25, color=E.ACCENT),
        ).arrange(DOWN, buff=0.45).move_to(UP * 0.1)
        tag = published_tag(r"Kydland and Prescott, \ \emph{Econometrica} 50(6) (1982): \ 1345--1370; \ Nobel "
                            r"Prize 2004", corner=DR, font_size=12)
        with self.voiceover(
            "In November 1982, the journal Econometrica published a paper by Finn Kydland and Edward Prescott "
            "called Time to Build and Aggregate Fluctuations. <bookmark mark='a'/> They took the growth model of "
            "Part twenty, added random shocks to technology, and chose its numbers from the long-run facts of "
            "growth. <bookmark mark='b'/> The result, they said, looked like the American business cycle. "
            "<bookmark mark='c'/> If that was true, recessions were not failures at all. They were the economy's "
            "best response to bad luck, and policy had nothing to fix. <bookmark mark='d'/> That claim turned out "
            "to be mostly wrong. But the method they used to make it won completely, and it is the method this part "
            "teaches."
        ) as vo:
            self.play(FadeIn(rows[0]), FadeIn(rows[1]), FadeIn(tag))
            for mk, r_ in zip("abcd", rows[2:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=UP * 0.1))
        self.clear_scene()

    def twins(self):
        F = load("facts")
        R = load("rbc")
        us = np.array(F["cyc"]["y"])[-200:]
        isl = np.array(R["sim_hp"]["y"])[-200:]
        q = np.arange(200)
        top = plane([0, 200], [-7, 7], center=UP * 1.55 + LEFT * 1.6, x_length=9.4, y_length=2.5,
                    yticks=[-5, 0, 5], yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        bot = plane([0, 200], [-7, 7], center=DOWN * 1.75 + LEFT * 1.6, x_length=9.4, y_length=2.5,
                    yticks=[-5, 0, 5], yfmt=lambda v: f"{v:+.0f}" if v else "0", font_size=15)
        z1, z2 = seg(top, 0, 0, 200, 0, GREY_D, 1.5), seg(bot, 0, 0, 200, 0, GREY_D, 1.5)
        a = path(top, q, np.clip(us, -7, 7), OUTPUT, 2.5, smooth=False)
        b = path(bot, q, np.clip(isl, -7, 7), OUTPUT, 2.5, smooth=False)
        la = label(r"A", font_size=34, color=E.ACCENT).next_to(top, LEFT, buff=0.25)
        lb = label(r"B", font_size=34, color=E.ACCENT).next_to(bot, LEFT, buff=0.25)
        unit = label(r"output, \ \% from trend, \ 200 quarters", font_size=17, color=GREY_B).next_to(top, UP,
                                                                                                    buff=0.12)
        ka = label(r"America, \\ 1970--2019", font_size=21, color=OUTPUT).next_to(top, RIGHT, buff=0.3)
        kb = label(r"the Island's model: \\ no money, \\ no unemployment, \\ no market failure", font_size=19,
                   color=TECH).next_to(bot, RIGHT, buff=0.3)
        for k in (ka, kb):
            if k.get_right()[0] > 7.0:
                k.shift(LEFT * (k.get_right()[0] - 6.95))
        tag = data_tag(r"BEA: \ real GDP, \ via FRED; \ the Island: \ simulated", corner=DR, font_size=12)
        with self.voiceover(
            "Here is what they meant. Two series of output, each measured as a percentage gap from its trend, two "
            "hundred quarters each. <bookmark mark='a'/> One of them is America's. <bookmark mark='b'/> The other is "
            "a model with no money, no unemployment, no monopolies and no market failures of any kind: a single "
            "household that saves and works as it pleases, hit by random changes in technology. "
            "<bookmark mark='c'/> Which is which? A is America, from 1970 to 2019. B is the Island's model, which "
            "you will build in this part. They are not the same, but at a glance they are hard to tell apart, and "
            "that resemblance changed macroeconomics."
        ) as vo:
            self.play(FadeIn(top), FadeIn(bot), FadeIn(z1), FadeIn(z2), FadeIn(la), FadeIn(lb), FadeIn(unit),
                      FadeIn(tag), run_time=0.8)
            vo.wait_until("a")
            self.play(Create(a), run_time=2.5)
            vo.wait_until("b")
            self.play(Create(b), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(ka), FadeIn(kb))
        self.clear_scene()

    def question(self):
        q = wrapped_label(ASK, 12.0, 40, E.ACCENT).to_edge(UP, buff=0.8)
        rows = VGroup(
            label(r"how do you solve a problem that never ends? \ \ (dynamic programming)", font_size=25,
                  color=VALUE),
            label(r"how do you build, \ calibrate and solve a whole economy with shocks?", font_size=25,
                  color=TECH),
            label(r"how close does it come to the data, \ and where does it fail?", font_size=25, color=OUTPUT),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(q, DOWN, buff=0.7)
        with self.voiceover(
            "This part's question: could booms and slumps be an economy's best response to shocks it cannot avoid? "
            "<bookmark mark='a'/> To answer it you need a tool for problems that never end: dynamic programming. "
            "<bookmark mark='b'/> Then a way to build an economy with shocks in it, choose its numbers, and solve "
            "it. <bookmark mark='c'/> And then the test: how close does it come to the data, and where exactly does "
            "it fail?"
        ) as vo:
            self.play(FadeIn(q, shift=DOWN * 0.2))
            for mk, r_ in zip("abc", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()

    def title(self):
        R = load("rbc")
        mini = plane([0, 120], [-4, 4], x_length=4.2, y_length=1.4)
        logo = path(mini, np.arange(120), np.clip(np.array(R["sim_hp"]["y"])[-120:], -4, 4), OUTPUT, 3, smooth=False)
        t = label(r"Economics, Built", font_size=60)
        sub = label(r"Part 29 \ $\cdot$ \ The Cycle as Equilibrium", font_size=34, color=E.ACCENT)
        VGroup(logo, t, sub).arrange(DOWN, buff=0.45)
        with self.voiceover("Economics, Built. Part twenty-nine: the cycle as equilibrium."):
            self.play(Create(logo), run_time=1.6)
            self.play(Write(t), run_time=1.2)
            self.play(FadeIn(sub, shift=UP * 0.15))
        self.wait(1.0)
        self.clear_scene()

    def objectives(self):
        head = label(r"Act VI \ $\cdot$ \ Money and the Cycle", font_size=40, color=E.ACCENT)
        obj = objectives_card([
            r"what a business cycle is, \ and how filters define it; \ which series leads",
            r"dynamic programming: \ the cake, \ Bellman's equation, \ value function iteration",
            r"the stochastic growth model; \ shocks as Markov chains; \ labour supply",
            r"calibration; \ log-linearization; \ the saddle path as a count of roots",
            r"the model beside the data; \ the critics; \ what survived; \ the Frisch dial",
        ], color=E.ACCENT, font_size=31, width=13.0)
        with self.voiceover(
            "Here is the plan. <bookmark mark='a'/> What a business cycle is, how a filter defines it, and a game: "
            "which series turns first? <bookmark mark='b'/> Dynamic programming from scratch, with a cake. "
            "<bookmark mark='c'/> The stochastic growth model, shocks as Markov chains, and why people work more in "
            "a boom. <bookmark mark='d'/> Calibration, and how to solve the whole model by counting the roots of a "
            "matrix. <bookmark mark='e'/> Then the model beside the data, its critics, what survived them, and a "
            "new dial: how much people change their hours when wages change."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeOut(head), FadeIn(obj.head), FadeIn(obj.rows[0], shift=RIGHT * 0.2))
            for mk, r_ in zip("bcde", obj.rows[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(r_, shift=RIGHT * 0.2))
        self.clear_scene()
