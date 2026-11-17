from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Goals(VoiceoverScene):
    def construct(self):
        self.card()
        self.atkinson()
        self.setting()
        self.ifthen()

    def card(self):
        card = chapter_card(6, r"Goals", r"Which goals move people?",
                            lit={1957: r"Atkinson", 1968: r"Locke", 1999: r"Gollwitzer", 2002: r"Locke \& Latham"},
                            part=PART, scale=("mind", "person"), marr=("what", "how"))
        with self.voiceover("Chapter six. Goals."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def atkinson(self):
        d = load("atkinson")
        head = heading(r"Derivation: \ expectancy times value")
        eqs = VGroup(
            MathTex(r"T_s = M_s \cdot P \cdot I_s, \qquad I_s = 1 - P", font_size=34),
            MathTex(r"T = (M_s - M_{af})\, P\,(1 - P)", font_size=36),
        ).arrange(DOWN, buff=0.35)
        A = axes([0, 1], [-0.2, 0.2], x_length=5.6, y_length=3.6, xticks=[0, 0.5, 1.0], yticks=[-0.15, 0, 0.15],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"chance of success, \ $P$",
                 ylabel=r"tendency to take the task on, \ $T$", center=[-3.3, -0.2, 0], font_size=16)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(1, 0), color=GREY_D, stroke_width=2)
        cs = curve(A.ax, d["P"], d["success"], INTR, 4)
        ca = curve(A.ax, d["P"], d["anxious"], LOST, 4)
        key = legend([(INTR, r"success-oriented"), (LOST, r"anxious about failure")], font_size=17)
        key.arrange(RIGHT, buff=0.5).next_to(A, DOWN, buff=0.2)
        rows = rows_of([
            (r"Atkinson, \ 1957: \ the pull of a task is the motive to succeed, \ times the chance of success, "
             r"\ times the pride of succeeding, \ which is larger the harder the task", WHITE),
            (r"the product peaks at even odds: \ the success-oriented choose tasks of middling difficulty", INTR),
            (r"for people more afraid of failing, \ the sign flips: \ they choose the very easy or the impossible",
             LOST),
            (r"children throwing rings at a peg, \ free to stand where they like, \ show both patterns", BODY),
        ], 5.6, 21, 0.3)
        right = VGroup(eqs, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.atkinson}: \ $M_s, M_{af} = 1, 0.3$ and $0.3, 1$")
        with self.voiceover(
            "Goals bring the future into motivation, and the oldest formal model of them is still instructive. "
            "<bookmark mark='a'/> John Atkinson proposed in 1957 that the pull of a task is a person's motive to "
            "succeed, times the chance of success, times the incentive of succeeding, and that the incentive is "
            "larger the harder the task: pride in an easy win is small. Set the incentive to one minus P. "
            "<bookmark mark='b'/> The product P times one minus P peaks at even odds. People driven mainly by the "
            "hope of success should choose tasks of middling difficulty. <bookmark mark='c'/> For people more "
            "afraid of failing, the same algebra flips the sign, and they should prefer tasks so easy they can't "
            "fail or so hard that failing says nothing. <bookmark mark='d'/> In ring-toss games where people stand "
            "wherever they like, both patterns appear, in roughly the people the theory predicts."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero))
            vo.wait_until("a")
            self.play(Write(eqs[0]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(Write(eqs[1]), Create(cs), FadeIn(key[0]), FadeIn(rows[1]), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(ca), FadeIn(key[1]), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def setting(self):
        head = heading(r"Specific, \ difficult goals")
        src = label(r"Locke and Latham: \ hundreds of studies, \ from loggers to scientists", font_size=22,
                    color=GREY_A).next_to(head, DOWN, buff=0.3)
        chain = flow_chain([(r"a specific, \ difficult goal", INTR),
                            (r"attention, \ effort, \ persistence, \ strategy", BODY),
                            (r"better performance than \emph{do your best}", WHITE)],
                           box_w=3.5, box_h=1.25, buff=0.75, font_size=23)
        chain.move_to([0, 0.75, 0])
        vague = label(r"\emph{do your best} \ sets no standard", font_size=19, color=GREY_B)
        vague.next_to(chain.boxes[2], DOWN, buff=0.18)
        cards = point_cards([
            (r"When they work", r"with commitment, \ feedback and the ability to reach them; \ for a complex new "
             r"task, \ a goal to learn beats a goal to perform", WANT),
            (r"The cost", r"goals narrow attention to what they measure; \ hard targets invite cutting corners "
             r"and cheating \ (Ord\'o\~nez et al., \ 2009)", LOST),
        ], width=12.0, font_size=22)
        cards.move_to([0, -2.05, 0])
        tag = published_tag(r"Locke \& Latham (2002); \ Ord\'o\~nez et al.\ (2009)")
        with self.voiceover(
            "The most successful theory of goals is also one of the plainest. <bookmark mark='a'/> Edwin Locke and "
            "Gary Latham gathered hundreds of studies, in laboratories and workplaces, of people from loggers to "
            "scientists. <bookmark mark='b'/> A specific, difficult goal leads to better performance than being told "
            "to do your best, which in practice sets no standard at all. <bookmark mark='c'/> Goals work by directing "
            "attention, raising effort, extending persistence, and prompting a search for strategies. "
            "<bookmark mark='d'/> They work when people are committed, get feedback, and can reach the goal. For a "
            "complex task that's new, a goal to learn how beats a goal to perform. <bookmark mark='e'/> And they have "
            "costs. A goal narrows attention to what it measures, and in 2009 Lisa Ordóñez and colleagues gathered "
            "cases where hard targets invited cutting corners, and outright cheating."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(src, shift=DOWN * 0.1))
            vo.wait_until("b")
            self.play(FadeIn(chain.boxes[0]), GrowArrow(chain.arrows[0]), FadeIn(chain.boxes[1]),
                      GrowArrow(chain.arrows[1]), FadeIn(chain.boxes[2]), FadeIn(vague), run_time=1.6)
            vo.wait_until("c")
            self.play(Indicate(chain.boxes[1], color=BODY, scale_factor=1.06))
            vo.wait_until("d")
            self.play(FadeIn(cards.cards[0], shift=UP * 0.15))
            vo.wait_until("e")
            self.play(FadeIn(cards.cards[1], shift=UP * 0.15))
        self.clear_scene()

    def ifthen(self):
        head = heading(r"If, \ then: \ implementation intentions")
        card_ = RoundedRectangle(corner_radius=0.15, width=5.6, height=2.2, color=INTR, fill_opacity=0.08).move_to(
            [-3.4, 0.3, 0])
        txt = VGroup(label(r"goal: \ I will exercise more", font_size=22, color=GREY_B),
                     label(r"plan: \ if it is 7 a.m.\ on a weekday,", font_size=22, color=INTR),
                     label(r"then I put on my shoes and run", font_size=22, color=INTR)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.18).move_to(card_)
        rows = rows_of([
            (r"Gollwitzer, \ 1999: \ a goal says what; \ an implementation intention says when, \ where and how, "
             r"\ as if--then", WHITE),
            (r"the cue in the if-clause comes to trigger the action, \ like a habit made on purpose", INTR),
            (r"a meta-analysis of many studies found moderate to large effects on reaching goals; \ a literature "
             r"of small studies can overstate an effect \ (chapter eight)", WANT),
            (r"the gap between intending and doing is the problem; \ planning the moment is a partial answer",
             BODY),
        ], 5.6, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Gollwitzer (1999); \ Gollwitzer \& Sheeran (2006)")
        with self.voiceover(
            "Most goals fail not at the setting but at the doing. <bookmark mark='a'/> Peter Gollwitzer's answer, "
            "in 1999, is the implementation intention. A goal says what you will do; an implementation intention "
            "says when, where and how, in the form if this, then that. <bookmark mark='b'/> The idea is that the cue "
            "in the if-clause comes to trigger the action automatically, like a habit made on purpose. "
            "<bookmark mark='c'/> A meta-analysis of many studies by Gollwitzer and Paschal Sheeran in 2006 "
            "found moderate to large effects on reaching goals. But a literature built from many small studies can "
            "overstate an effect, as chapter eight will show in detail. <bookmark mark='d'/> The gap between intending and "
            "doing is the real problem of motivation, and planning the moment is a partial answer."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(card_), FadeIn(txt[0]))
            vo.wait_until("a")
            self.play(FadeIn(txt[1:]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
