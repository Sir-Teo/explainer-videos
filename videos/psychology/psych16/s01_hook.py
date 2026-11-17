from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403


def box(text, color, w=2.6, h=1.0, font_size=26):
    r = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=color, stroke_width=3,
                         fill_color="#05070B", fill_opacity=1)
    return VGroup(r, label(text, font_size=font_size, color=color).move_to(r))


class Hook(VoiceoverScene):
    def construct(self):
        self.lab()
        self.drops()
        self.puzzle()
        self.question()
        self.objectives()

    def lab(self):
        head = heading(r"St Petersburg, \ around 1900")
        dog = box(r"the dog", WHITE, 2.4, 1.2, 30).move_to([0, 0.6, 0])
        cs = box(r"a metronome", CS).move_to([-4.3, 1.6, 0])
        us = box(r"food", US).move_to([-4.3, -0.4, 0])
        out = box(r"drops of saliva", CR, 3.0).move_to([4.4, 0.6, 0])
        a1 = Arrow(cs.get_right(), dog.get_left() + UP * 0.25, color=CS, buff=0.1)
        a2 = Arrow(us.get_right(), dog.get_left() + DOWN * 0.25, color=US, buff=0.1)
        a3 = Arrow(dog.get_right(), out.get_left(), color=CR, buff=0.1)
        rows = rows_of([
            (r"Pavlov, \ Nobel Prize 1904, \ for the physiology of digestion", WHITE),
            (r"his dogs salivated before the food arrived: \ at the dish, \ the footsteps, \ the attendant", US),
            (r"a tube from the salivary gland: \ secretion counted in drops", CR),
            (r"the signals were metronomes, \ buzzers, \ lights and touches; \ the famous bell is mostly legend", CS),
        ], 12.4, 27, 0.26).to_edge(DOWN, buff=0.75)
        tag = historical_tag(archive.PAVLOV_1927.cite)
        with self.voiceover(
            "In 1904 Ivan Pavlov won the Nobel Prize, not for anything to do with psychology, but for his work on "
            "digestion. <bookmark mark='a'/> His dogs had a habit that spoiled his measurements: they began to "
            "salivate before the food arrived. At the sight of the dish, at footsteps, at the attendant who fed them. "
            "<bookmark mark='b'/> Pavlov turned the nuisance into a method. A small tube from a salivary gland "
            "carried the secretion outside, where it could be counted, drop by drop. <bookmark mark='c'/> Then he "
            "paired a neutral signal with food, again and again, and counted. The signals were metronomes, buzzers, "
            "lights and touches on the skin. The bell everyone remembers is mostly legend: in decades of his "
            "laboratory's records, his biographer Daniel Todes found it used only rarely."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rows[0]), FadeIn(dog))
            vo.wait_until("a")
            self.play(FadeIn(us), GrowArrow(a2), FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(out), GrowArrow(a3), FadeIn(rows[2]))
            vo.wait_until("c")
            self.play(FadeIn(cs), GrowArrow(a1), FadeIn(rows[3]))
        self.clear_scene()

    def drops(self):
        d = load("pavlov")
        head = heading(r"A response that comes, \ goes, \ and comes back")
        A = axes([0, 58], [0, 14], x_length=8.6, y_length=4.0, xticks=[0, 10, 20, 30, 40, 50],
                 yticks=[0, 4, 8, 12], xlabel=r"trial", ylabel=r"drops of saliva to the signal", center=[-1.6, 0.2, 0])
        ax = A.ax
        n = 30
        acq = scatter(ax, d["trial"][:n], d["drops"][:n], CR, radius=0.05)
        ext = scatter(ax, d["trial"][n:], d["drops"][n:], INHIB, radius=0.05)
        gap = DashedLine(ax.c2p(55.5, 0), ax.c2p(55.5, 14), color=GREY_C, stroke_width=2)
        rec = Dot(ax.c2p(57, d["drops_recovered"]), radius=0.08, color=YOU)
        lab1 = label(r"signal, \ then food", font_size=22, color=CR).move_to(ax.c2p(15, 13.2))
        lab2 = label(r"signal alone", font_size=22, color=INHIB).move_to(ax.c2p(43, 13.2))
        lab3 = label(r"next day", font_size=20, color=YOU).next_to(rec, UP, buff=0.15)
        rows = rows_of([
            (r"acquisition: \ the signal comes to bring saliva", CR),
            (r"extinction: \ signal without food, \ and the response fades", INHIB),
            (r"spontaneous recovery: \ a day later, \ part of it is back", YOU),
        ], 3.6, 25, 0.35).move_to([5.0, 0.2, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ Psyche's dog, \ \texttt{conditioning.extinction\_in\_context}")
        with self.voiceover(
            "Here is the pattern his laboratory found, run on Psyche. <bookmark mark='a'/> Pair the signal with food, "
            "and over a few dozen trials the signal alone brings more and more saliva. That's acquisition. "
            "<bookmark mark='b'/> Now present the signal without food. The response fades, trial by trial, until "
            "nothing comes. That's extinction. It looks like forgetting. <bookmark mark='c'/> But wait a day and "
            "present the signal again, and part of the response is back. Something was learned in extinction, but it "
            "wasn't the erasure of the first lesson. That puzzle, a response that can come back from nothing, will "
            "take us to the end of this part."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(lab1), LaggedStart(*[FadeIn(p) for p in acq], lag_ratio=0.05), FadeIn(rows[0]),
                      run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(lab2), LaggedStart(*[FadeIn(p) for p in ext], lag_ratio=0.05), FadeIn(rows[1]),
                      run_time=3.0)
            vo.wait_until("c")
            self.play(Create(gap), FadeIn(rec, scale=1.5), FadeIn(lab3), FadeIn(rows[2]))
        self.clear_scene()

    def puzzle(self):
        head = heading(r"Two dogs, \ the same number of pairings")
        left = rows_of([
            (r"dog 1", CS),
            (r"signal, \ then food: \ 40 times", WHITE),
            (r"food never comes without the signal", WHITE),
        ], 5.6, 28, 0.3)
        right = rows_of([
            (r"dog 2", US),
            (r"signal, \ then food: \ 40 times", WHITE),
            (r"and food just as often when there is no signal", WHITE),
        ], 5.6, 28, 0.3)
        g = VGroup(left, right).arrange(RIGHT, buff=1.0, aligned_edge=UP).move_to([0, 1.0, 0])
        q = wrapped_label(r"Pavlov's answer: \ both learn equally; \ pairing is what counts. \ In 1968 that answer "
                          r"turned out to be wrong.", 11.6, 30, YOU).next_to(g, DOWN, buff=0.8)
        with self.voiceover(
            "Here's a puzzle to carry through the part. <bookmark mark='a'/> Two dogs each get forty pairings of a "
            "signal with food. For the first, food never comes any other way. <bookmark mark='b'/> For the second, "
            "food also arrives, just as often, when there's no signal at all. <bookmark mark='c'/> Do they learn the "
            "same thing? On the view Pavlov's work made standard, they should: same pairings, same learning. In 1968 "
            "an experiment of exactly this design, with rats and mild shocks instead of dogs and food, showed that the "
            "second animal learns nothing at all about the signal. Learning isn't about pairing. It's about prediction."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(left))
            vo.wait_until("b")
            self.play(FadeIn(right))
            vo.wait_until("c")
            self.play(FadeIn(q))
        self.clear_scene()

    def question(self):
        head = heading(r"Today: \ what exactly is learned?")
        rows = rows_of([
            (r"when a signal comes to mean food, \ what has changed: \ a reflex, \ a link, \ a prediction?", CS),
            (r"why does a perfectly paired cue sometimes teach nothing at all?", US),
            (r"how do rewards shape what animals do, \ and how they divide their time?", CR),
            (r"why do extinguished fears come back, \ and what does that mean for therapy?", INHIB),
        ], 11.8, 31, 0.45).move_to([0, -0.2, 0])
        with self.voiceover(
            "Act Three was about the senses: how the mind measures the world. Act Four is about how it changes with "
            "experience, and it starts here. <bookmark mark='a'/> When a signal comes to mean food, what has "
            "changed? A reflex, a link between two ideas, or a prediction? <bookmark mark='b'/> Why does a cue that is "
            "perfectly paired with food sometimes teach an animal nothing? <bookmark mark='c'/> How do rewards shape "
            "what animals do, and how they divide their time between options? <bookmark mark='d'/> And why do fears "
            "that therapy has extinguished come back?"
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def objectives(self):
        head = VGroup(label(r"Part 16", font_size=34, color=GREY_B), label(r"Conditioning", font_size=64))
        head.arrange(DOWN, buff=0.25)
        obj = objectives_card([
            r"Pavlov's method, \ Thorndike's law of effect, \ and Skinner's schedules of reinforcement",
            r"contingency, \ not pairing: \ Rescorla's random control, \ and a game you play",
            r"blocking, \ and the idea that learning is driven by surprise",
            r"the Rescorla-Wagner rule, \ derived as gradient descent, \ and everything it predicts",
            r"what it gets wrong: \ extinction as new learning, \ attention, \ timing",
            r"choice and the matching law; \ the limits set by biology; \ therapy, \ training and loot boxes",
        ], color=P.ACCENT, font_size=31, width=13.2)
        with self.voiceover(
            "This is Part 16 of Psychology, Built: conditioning. <bookmark mark='a'/> We'll start with the three "
            "founders: Pavlov's method, Thorndike's law of effect, and Skinner's schedules of reinforcement. Then "
            "the discovery that learning follows contingency rather than pairing, with a game for you to play. Then "
            "blocking, and the idea that animals learn only when they're surprised. Then one line of algebra, the "
            "Rescorla-Wagner rule, which we'll derive as gradient descent and run on every classic design. Then what "
            "it gets wrong: extinction that is new learning, attention, and time. And at the end, how animals divide "
            "their choices, the limits that biology sets, and where all this is used: in therapy, animal training, "
            "treatment for addiction, and the design of games that are hard to put down."
        ) as vo:
            self.play(FadeIn(head, shift=UP * 0.2))
            vo.wait_until("a")
            self.play(head.animate.scale(0.6).to_edge(UP, buff=0.3))
            obj.next_to(head, DOWN, buff=0.45)
            self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.2) for r in obj], lag_ratio=0.9), run_time=26.0)
        self.clear_scene()
