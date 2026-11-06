from __future__ import annotations

from videos.philosophy.philosophy11.common import *  # noqa: F403


class Hook(VoiceoverScene):
    def construct(self):
        self.title()
        self.clocks()
        self.question()
        self.objectives()

    def title(self):
        t = part_title(PART)
        q = quote_card(r"This is the very thing about which I am in doubt and which I cannot satisfactorily grasp by "
                       r"myself: what knowledge really is.", r"Socrates", r"Plato, \textit{Theaetetus} 145e \ (trans. "
                       r"Fowler)", width=9.6,
                       font_size=28).next_to(t, DOWN, buff=0.6)
        with self.voiceover(
            "Part 10 asked where knowledge comes from. Part 11 asks what it is. <bookmark mark='a'/>Socrates put the "
            "question to a young mathematician, Theaetetus, about twenty-four centuries ago, and admitted that he "
            "could not answer it himself. <bookmark mark='b'/>This part follows the question from that conversation "
            "to the present, and the Reasoner builds the cases that drove it."
        ) as vo:
            self.play(FadeIn(t, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(Indicate(q, color=KNOW, scale_factor=1.03))
        self.clear_scene()

    def clocks(self):
        head = label(r"Two people, \ one true belief", font_size=34, color=CONN).to_edge(UP, buff=0.4)
        c1 = clock(7 * 60, radius=1.15).move_to([-3.4, 0.9, 0])
        c2 = clock(8 * 60, radius=1.15, stopped=True).move_to([3.4, 0.9, 0])
        l1 = label(r"Ann reads a working clock", font_size=24, color=WHITE).next_to(c1, DOWN, buff=0.35)
        l2 = label(r"Ben reads a clock that stopped at 8:00", font_size=24, color=WHITE).next_to(c2, DOWN,
                                                                                                buff=0.6)
        l1.set_y(l2.get_y())
        both = label(r"it is 8:00 \ for both of them, \ and both believe it is 8:00 \ on good evidence",
                     font_size=24, color=JUST).move_to([0, -1.7, 0])
        verdict = VGroup(label(r"Ann knows the time", font_size=26, color=OK).move_to([-3.4, -2.6, 0]),
                         label(r"Ben is only lucky", font_size=26, color=LUCK).move_to([3.4, -2.6, 0]))
        with self.voiceover(
            "Here is the problem in one picture. <bookmark mark='a'/>Ann glances at a working clock. It says eight "
            "o'clock, and it is eight o'clock. <bookmark mark='b'/>Ben glances at a clock that stopped, long ago, at "
            "eight. By chance he looks at exactly eight o'clock. <bookmark mark='c'/>Both believe the same thing. "
            "Both are right. Both have good evidence: clocks are usually reliable. <bookmark mark='d'/>Yet Ann knows "
            "the time, and Ben does not. He is merely lucky. What is the difference? Bertrand Russell described this "
            "case in 1948; a philosopher in eighth-century India had a case like it; and in 1963 three pages by "
            "Edmund Gettier turned it into the central problem of the theory of knowledge."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(Create(c1), FadeIn(l1))
            self.play(Rotate(c1.minute, -TAU, about_point=c1.face.get_center()),
                      Rotate(c1.hour, -TAU / 12, about_point=c1.face.get_center()), run_time=1.5)
            vo.wait_until("b")
            self.play(Create(c2), FadeIn(l2))
            vo.wait_until("c")
            self.play(FadeIn(both))
            vo.wait_until("d")
            self.play(FadeIn(verdict[0]), FadeIn(verdict[1]))
        self.clear_scene()

    def question(self):
        head = label(r"What must be added to true belief?", font_size=34, color=CONN).to_edge(UP, buff=0.5)
        rows = VGroup(
            label(r"Plato: \ an account \quad Gettier: \ justification is not enough", font_size=24),
            label(r"reliability? \ tracking the truth? \ safety? \ virtue?", font_size=24, color=BEL),
            label(r"or is knowledge the starting point, \ not the thing to analyse?", font_size=24, color=KNOW),
            label(r"and can we know anything at all? \ the skeptic, \ the butterfly, \ the web", font_size=24,
                  color=SKEP)).arrange(DOWN, buff=0.45).move_to([0, 0.1, 0])
        wall_note = label(r"this part's brick in the Wall: \ Gettier's cases, \ and anti-luminosity", font_size=24,
                          color=P.WALL).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "So the question of this part is what must be added to true belief to make knowledge. "
            "<bookmark mark='a'/>Plato proposed an account; the twentieth century proposed justification, until "
            "Gettier. <bookmark mark='b'/>Then came a parade of candidates: reliability, tracking the truth, safety, "
            "intellectual virtue. The Reasoner builds a checker for each, and runs them on the same cases. "
            "<bookmark mark='c'/>Or perhaps knowledge cannot be analysed at all, and should be the starting point. "
            "<bookmark mark='d'/>And behind all of this stands the skeptic, who asks whether we know anything. "
            "<bookmark mark='e'/>On the way we lay this part's brick in the Wall: Gettier's cases, and Timothy "
            "Williamson's proof that no interesting condition is luminous."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", rows):
                vo.wait_until(mk)
                self.play(FadeIn(r, shift=UP * 0.1))
            vo.wait_until("e")
            self.play(FadeIn(wall_note))
        self.clear_scene()

    def objectives(self):
        card = objectives_card([
            r"Plato's definitions, \ and justified true belief",
            r"Gettier's cases, \ built as models; \ older cases; \ the failed repairs",
            r"reliability, \ sensitivity, \ safety, \ virtue: \ four checkers, \ one set of cases",
            r"knowledge first: \ anti-luminosity, \ and why KK fails",
            r"the skeptic, \ closure, \ and four answers; \ the butterfly and the Pyrrhonists",
            r"foundations, \ coherence, \ infinite chains; \ inside or outside the head",
            r"Quine's web of belief; \ what ordinary people say",
        ], font_size=25)
        with self.voiceover(
            "The plan. <bookmark mark='a'/>Plato, and the definition the twentieth century took from him. "
            "<bookmark mark='b'/>Gettier's cases, built as models the Reasoner can check, their older cousins, and the "
            "repairs that failed. <bookmark mark='c'/>Four theories, each a checker run on the same cases. "
            "<bookmark mark='d'/>Knowledge first, with two theorems about margins for error. <bookmark mark='e'/>The "
            "skeptic and the answers to her, and two older ways of living with doubt. <bookmark mark='f'/>The "
            "structure of justification, and whether it lies inside the head. <bookmark mark='g'/>And Quine's web of "
            "belief, and what happens when you ask ordinary people about Gettier's cases."
        ) as vo:
            self.play(FadeIn(card.head))
            for mk, i in zip("abcdefg", range(7)):
                vo.wait_until(mk)
                self.play(FadeIn(card.rows[i], shift=RIGHT * 0.2))
        self.clear_scene()
