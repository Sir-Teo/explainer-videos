from __future__ import annotations

import numpy as np

from videos.psychology.psych16.common import *  # noqa: F403
from videos.psychology.psych16.s01_hook import box


class Pavlov(VoiceoverScene):
    def construct(self):
        self.card()
        self.terms()
        self.gradient()
        self.substitution()

    def card(self):
        card = chapter_card(1, r"Pavlov's method", r"What does a signal come to do?",
                            lit={1927: r"Pavlov"}, part=PART, scale=("brain", "mind"), marr=("what",))
        with self.voiceover("Chapter one. Pavlov's method."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def terms(self):
        head = heading(r"Four terms, \ still in use")
        us = box(r"US: \ food", US, 3.2).move_to([-3.6, 1.7, 0])
        ur = box(r"UR: \ salivation", CR, 3.4).move_to([3.4, 1.7, 0])
        cs = box(r"CS: \ a metronome", CS, 3.2).move_to([-3.6, -0.3, 0])
        cr = box(r"CR: \ salivation", CR, 3.4).move_to([3.4, -0.3, 0])
        a1 = Arrow(us.get_right(), ur.get_left(), color=GREY_B, buff=0.15)
        t1 = label(r"unlearned: \ a reflex", font_size=22, color=GREY_B).next_to(a1, UP, buff=0.1)
        a2 = Arrow(cs.get_right(), cr.get_left(), color=CS, buff=0.15)
        t2 = label(r"learned, \ after pairings", font_size=22, color=CS).next_to(a2, UP, buff=0.1)
        rows = rows_of([
            (r"unconditioned stimulus and response: \ the reflex the animal is born with", WHITE),
            (r"conditioned stimulus and response: \ what the pairings create", CS),
            (r"``conditioned'' is a mistranslation of Pavlov's ``conditional'': \ a reflex that depends on "
             r"conditions", GREY_A),
        ], 12.4, 26, 0.28).to_edge(DOWN, buff=0.7)
        tag = historical_tag(archive.PAVLOV_1927.cite)
        with self.voiceover(
            "Pavlov's method came with a vocabulary, and it's still the vocabulary of the field. <bookmark mark='a'/> "
            "Food in the mouth produces saliva without any learning. Food is the unconditioned stimulus, the US, and "
            "salivation is the unconditioned response. <bookmark mark='b'/> A metronome, at first, produces nothing "
            "but a turn of the head. After pairings with food it produces saliva on its own: the metronome has become "
            "a conditioned stimulus, a CS, and the saliva it brings is the conditioned response. "
            "<bookmark mark='c'/> The English word is a slip of translation. Pavlov wrote of conditional reflexes: "
            "reflexes that depend on conditions, on the animal's history. That is the better word, because the "
            "whole question of this part is what those conditions are."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            vo.wait_until("a")
            self.play(FadeIn(us), FadeIn(ur), GrowArrow(a1), FadeIn(t1), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(cs), FadeIn(cr), GrowArrow(a2), FadeIn(t2), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def gradient(self):
        d = load("pavlov")
        head = heading(r"Generalization, \ and discrimination")
        lx = np.log2(d["f"] / 1000)
        A = axes([-2, 2], [0, 1.1], x_length=7.4, y_length=3.8, xticks=[-2, -1, 0, 1, 2],
                 xfmt=lambda v: {-2: "250", -1: "500", 0: "1000", 1: "2000", 2: "4000"}[int(v)], yticks=[0, 0.5, 1],
                 xlabel=r"test tone (Hz); \ trained on 1000 Hz", ylabel=r"response, \ share of the trained",
                 center=[-2.2, 0.0, 0])
        ax = A.ax
        g = curve(ax, lx, d["gen"], CR, stroke_width=4)
        pts = scatter(ax, np.log2(d["probe_f"] / 1000), d["probe_gen"], YOU, radius=0.07)
        rows = rows_of([
            (r"tones near the trained one bring saliva too, \ less the further away: \ a gradient", CR),
            (r"reward 1000 Hz but never 1400 Hz, \ and the gradient sharpens: \ discrimination", CS),
            (r"push the discrimination too hard, \ and Pavlov's dogs broke down: \ ``experimental neurosis''", INHIB),
        ], 4.4, 25, 0.34).move_to([4.6, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ a Gaussian gradient in octaves; \ Psyche's width")
        with self.voiceover(
            "Two more findings from Pavlov's laboratory. <bookmark mark='a'/> Train a dog on a tone of a thousand "
            "hertz, then test others. Nearby tones also bring saliva, and the further from the trained tone, the less. "
            "The response spreads along a gradient, here drawn on Psyche, with octaves as the distance. "
            "<bookmark mark='b'/> Now feed the dog after the thousand-hertz tone but never after fourteen hundred. "
            "The dog learns to respond to one and not the other, and the gradient sharpens. That's discrimination, and "
            "it became a way to ask animals what they can perceive. <bookmark mark='c'/> Pavlov also pushed it too "
            "far. When a circle signalled food and an ellipse didn't, and the ellipse was made rounder and rounder, "
            "some dogs became agitated and stopped working altogether. He called it experimental neurosis, an early "
            "and uncomfortable model of anxiety."
        ) as vo:
            self.play(FadeIn(head), FadeIn(A), FadeIn(tag))
            vo.wait_until("a")
            self.play(Create(g), FadeIn(pts), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
        self.clear_scene()

    def substitution(self):
        head = heading(r"What was learned? \ Pavlov's answer, \ and its trouble")
        rows = rows_of([
            (r"Pavlov: \ stimulus substitution; \ the signal becomes a stand-in for the food, \ wired to the "
             r"same reflex", CS),
            (r"but the conditioned response is often not the reflex: \ a tone before shock makes rats freeze, \ "
             r"not jump", INHIB),
            (r"and cues for a drug can bring the opposite of its effect: \ conditioned tolerance, \ Part 10", US),
            (r"the response prepares the animal for what is coming: \ the signal predicts, \ it does not "
             r"substitute", CR),
            (r"Rescorla, \ 1988: \ conditioning is how animals learn the relations among events", YOU),
        ], 12.6, 28, 0.38).move_to([0, -0.2, 0])
        with self.voiceover(
            "So what is learned? <bookmark mark='a'/> Pavlov's own answer was stimulus substitution: the signal "
            "becomes a stand-in for the food, wired in the brain to the same reflex. If that were right, the "
            "conditioned response would copy the unconditioned one. <bookmark mark='b'/> Often it doesn't. A shock "
            "makes a rat jump, but a tone that predicts a shock makes it freeze. <bookmark mark='c'/> And cues that "
            "predict a drug can produce the opposite of the drug's effect, the conditioned tolerance we met in "
            "Part 10, which is why an overdose is more likely in an unfamiliar place. <bookmark mark='d'/> The response "
            "is a preparation for what is coming. The signal doesn't stand in for the food. It predicts it. "
            "<bookmark mark='e'/> Robert Rescorla, whose experiments fill the middle of this part, put it this way in "
            "1988: conditioning isn't the low-level reflex business of the textbooks. It's how animals learn the "
            "relations among events in their world."
        ) as vo:
            self.play(FadeIn(head))
            for m, r in zip("abcde", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()
