from __future__ import annotations

from videos.philosophy.philosophy35.common import *  # noqa: F403


class Maxims(VoiceoverScene):
    def construct(self):
        card = chapter_card(6, r"Universalizability, tested", r"Does the test sort right from wrong?", lit=(1785,),
                            part=PART)
        with self.voiceover("Chapter six. Universalizability, tested."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]))
        self.play(FadeOut(card))
        self.two()
        self.table()
        self.murderer()
        self.readings()

    def two(self):
        head = label(r"Two contradictions", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"in conception", r"the universalized maxim cannot even be conceived to achieve its purpose: \ the "
                                   r"lying promise: \ a perfect duty, \ never to be broken", KANT),
                (r"in will", r"the universalized world is conceivable, \ but no one with needs could will it: \ a "
                             r"world where no one ever helps: \ an imperfect duty, \ to help sometimes", DUTY),
                (r"Kant's four examples", r"lying promises, \ suicide from self-love, \ neglecting one's talents, \ "
                                          r"refusing to help", GREY_A)]
        g = rows_table(rows, top=1.6, gap=0.55, width=8.4)
        with self.voiceover(
            "Kant distinguished two ways a maxim can fail. <bookmark mark='a'/>A contradiction in conception: "
            "universalized, the maxim cannot even be conceived to achieve its purpose, like the lying promise. Such "
            "maxims violate perfect duties, which allow no exceptions. <bookmark mark='b'/>A contradiction in will: "
            "the universalized world is perfectly conceivable, but no one with needs could will it. A world in which "
            "no one ever helps anyone could exist; but you, who will sometimes need help, cannot will it. Such "
            "maxims violate imperfect duties, like the duty to help others sometimes. "
            "<bookmark mark='c'/>Kant's four examples are the lying promise, suicide from self-love, neglecting one's "
            "talents, and refusing to help."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abc", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def table(self):
        d = load("maxims")
        head = label(r"The test, \ run on five maxims", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        rows = d["rows"]
        assert [r["kind"] for r in rows] == ["hit", "hit", "false positive", "false positive", "false negative"]
        assert d["promise_final_trust"] == 0.008 and d["tennis_courts"] == 4 and d["players"] == 100
        hd = [r"\text{maxim}", r"\text{in conception}", r"\text{in will}", r"\text{test}", r"\text{intuition}"]
        cells = []
        for r in rows:
            col = OK if r["kind"] == "hit" else BAD
            cells.append([wrapped_label(r["maxim"], 5.0, 16, WHITE), mark(r["conception"], 20), mark(r["will"], 20),
                          label(r["test"], font_size=16, color=KANT), label(r["intuition"], font_size=16, color=col)])
        grid = ValueGrid(hd, cells, col_w=[5.4, 2.0, 1.4, 1.6, 1.6], cell_h=0.72, font_size=16).move_to([0, -0.1, 0])
        note = label(r"$\checkmark$: \ a contradiction found; \ tennis: \ 100 players, \ 4 courts", font_size=15,
                     color=GREY_A).to_edge(DOWN, buff=0.25)
        with self.voiceover(
            "The Reasoner runs the test on five maxims, each with a small model of the universalized world. "
            "<bookmark mark='a'/>The lying promise fails in conception, as we saw. <bookmark mark='b'/>Never helping "
            "fails in will. Both verdicts match our intuitions. <bookmark mark='c'/>But play tennis at eight on "
            "Sunday mornings, because the courts are empty then: universalized, a hundred players arrive at four "
            "courts, the courts are never empty, and the maxim fails in conception. Yet it is perfectly innocent: a "
            "false positive. <bookmark mark='d'/>So does buy toy trains but never sell them, since if no one sells, "
            "no one can buy. <bookmark mark='e'/>And the test can be gamed: deceive anyone named Hans born on the "
            "third of March 1987 universalizes without contradiction, since so few people fit, but it is plainly "
            "wrong: a false negative. A mechanical test of maxims is too strict in some places and too lax in "
            "others."
        ) as vo:
            self.play(FadeIn(head), FadeIn(grid.head), Create(grid.rule), FadeIn(note))
            for mk, k in zip("abcde", range(5)):
                vo.wait_until(mk)
                self.play(*[FadeIn(c) for c in grid.cell[k]], run_time=0.6)
        self.clear_scene()

    def murderer(self):
        head = label(r"The murderer at the door \ (1797)", font_size=30, color=CONN).to_edge(UP, buff=0.3)
        door = VGroup(Rectangle(width=1.5, height=2.6, color=KANT, stroke_width=3, fill_color=KANT,
                                fill_opacity=0.12),
                      Dot(radius=0.06, color=KANT).shift(RIGHT * 0.5))
        door.move_to([-5.7, -0.6, 0])
        caller = VGroup(Circle(radius=0.22, color=HARM, stroke_width=3),
                        Line(DOWN * 0.22, DOWN * 1.1, color=HARM, stroke_width=3)).move_to([-4.3, -0.5, 0])
        ask = label(r"``Is your friend inside?''", font_size=18, color=HARM).next_to(caller, UP, buff=0.25).align_to(
            caller, LEFT).shift(LEFT * 0.1)
        rows = [(r"Constant", r"the duty to tell the truth is owed only to those who have a right to the truth", GOOD),
                (r"Kant", r"truthfulness in all declarations is a sacred command of reason: \ lie, \ and you answer "
                          r"for what follows", DUTY),
                (r"Korsgaard \ (1986)", r"universalized, \ `lie to murderers at the door' still works: \ he thinks "
                                        r"you do not know what he is: \ the test permits it", KANT),
                (r"two levels", r"the humanity formula is the ideal; \ in dealing with evil, \ universal law is the "
                                r"standard, \ and you may lie", VIRT)]
        g = rows_table(rows, x_label=-1.5, x_text=0.7, top=1.6, gap=0.42, label_size=19, text_size=18, width=6.1)
        with self.voiceover(
            "In 1797 Benjamin Constant tested Kant with a case. <bookmark mark='a'/>A murderer comes to your door and "
            "asks whether your friend, whom he is pursuing, is hiding in your house. Constant said that the duty to "
            "tell the truth is owed only to those who have a right to the truth, and the murderer has none. "
            "<bookmark mark='b'/>Kant replied, in On a Supposed Right to Lie from Philanthropy, that truthfulness in "
            "all declarations is a sacred command of reason, not to be restricted by any convenience. If you lie, "
            "and your friend has meanwhile slipped out and meets the murderer on the way, you can justly be charged "
            "with his death. Few Kantians follow him here. <bookmark mark='c'/>Christine Korsgaard showed in 1986 "
            "that the universal law test itself permits the lie. The murderer is deceiving you: he expects you to "
            "take him for an innocent caller. Universalize the maxim, lie to murderers who come to the door, and it "
            "still works, because he does not think you know what he is. <bookmark mark='d'/>The humanity formula "
            "looks stricter, since a lie treats its hearer as a mere means. Korsgaard's answer is a two-level view: "
            "the formula of humanity is the ideal for a world of good will; in dealing with evil, the universal law "
            "test is the standard, and it lets you lie. The test that forbade the lying promise permits the lie "
            "almost everyone thinks right."
        ) as vo:
            self.play(FadeIn(head), FadeIn(door))
            self.play(FadeIn(caller), FadeIn(ask))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()

    def readings(self):
        head = label(r"Better readings of the test", font_size=30, color=CONN).to_edge(UP, buff=0.35)
        rows = [(r"practical contradiction", r"Korsgaard \ (1985): \ the maxim fails if, \ universalized, \ it could "
                                             r"not serve its purpose: \ our toy is this reading", KANT),
                (r"relevant descriptions", r"Herman \ (1993): \ judgment must first say what the agent is doing; \ "
                                           r"the test checks a description, \ it does not find one", DUTY),
                (r"the humanity formula", r"Parfit, \ O'Neill: \ wrong acts treat others in ways they could not "
                                          r"consent to: \ the lie, \ yes; \ tennis, \ no", GOOD),
                (r"Kantian contractualism", r"Parfit \ (2011): \ act on principles everyone could rationally will: \ "
                                            r"where Kant, \ contract and consequences converge", AGG)]
        g = rows_table(rows, top=1.6, gap=0.5, width=8.4)
        with self.voiceover(
            "Kantians have answers. <bookmark mark='a'/>Christine Korsgaard argued in 1985 that the contradiction is "
            "practical: a maxim fails if, universalized, it could not serve its own purpose. That is the reading "
            "the Reasoner's toy world implements, and it still produces false positives. <bookmark mark='b'/>Barbara "
            "Herman argued that the test presupposes moral judgment about what an agent is really doing: it checks a "
            "description of an act, but it cannot choose the right description. <bookmark mark='c'/>Many turn to the "
            "humanity formula instead: wrong acts treat others in ways they could not possibly consent to. The "
            "deceived lender could not consent; the tennis players are not wronged at all. "
            "<bookmark mark='d'/>And Derek Parfit's On What Matters, of 2011, argued that the best version of Kant's "
            "theory, the best contractualism and the best consequentialism converge, climbing the same mountain on "
            "different sides."
        ) as vo:
            self.play(FadeIn(head))
            for mk, r in zip("abcd", g):
                vo.wait_until(mk)
                self.play(FadeIn(r))
        self.clear_scene()
