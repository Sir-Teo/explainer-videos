from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403


class Continuo(SoundScene):
    def construct(self):
        chapter(self, 3, r"The figured bass", r"How much of the music is in the bass?", extra=((1689, r"Corelli's trio sonatas, \ Op. 3"),))
        self.figures()
        self.three()
        self.quiz()
        self.compare()
        self.partimento()

    # ------------------------------------------------------------------
    def figures(self):
        items = [
            (r"the continuo player reads only the bass, \ with numbers: \ the figures \ (Part 10)", WHITE),
            (r"no number: \ a third and a fifth; \ 6: \ a third and a sixth; \ 7: \ add a seventh", WHITE),
            (r"the player chooses the voicing and the rhythm: \ an improviser with rules", WHITE),
            (r"the trio sonata: \ two violins and continuo, \ four players reading three parts", TUNE),
            (r"Arcangelo Corelli, \ Rome, \ Op. 3 \ (1689): \ the model for a generation", GREY_A),
        ]
        rows_scene(self, r"the bass and its numbers", items,
                   "A continuo player read a single line, the bass, with numbers written above it, the figures we met in "
                   "Part 10. <bookmark mark='b'/> No number means a chord of a third and a fifth above the bass; a six, a "
                   "third and a sixth; a seven, add the seventh. <bookmark mark='c'/> How to space the chord, which note to "
                   "put on top, how to break it into rhythm: all that was the player's, an improviser following rules. "
                   "<bookmark mark='d'/> The most common chamber texture of the age was the trio sonata: two violins and the "
                   "continuo, usually four players reading three parts, the bass shared by a cello and a harpsichord or "
                   "organ. <bookmark mark='e'/> The model for a generation was Arcangelo Corelli, working in Rome, whose "
                   "trio sonatas began appearing in 1681; this chapter uses the Grave that opens his Opus 3, of 1689.")

    # ------------------------------------------------------------------
    def three(self):
        d = load("realize3")
        c = clip("continuo.three")
        figs = d["figures"]
        rolls = VGroup()
        for k, r in enumerate(d["realizations"]):
            g = voices_roll([r["chords"], d["bass"]], width=3.6, height=2.6, colors=[[TUNE, BLUE, EAR][k], GREY_A], lo=40, hi=86, bar_h=0.11)
            rolls.add(VGroup(label(rf"top note near {NAMES[r['top'] % 12]}", font_size=20, color=[TUNE, BLUE, EAR][k]), g).arrange(DOWN, buff=0.2))
        rolls.arrange(RIGHT, buff=0.5).move_to(DOWN * 0.2)
        fl = label(r"the figures: \ " + r" \ ".join(f if f else r"--" for f in figs), font_size=22, color=GREY_A).to_edge(UP, buff=0.5)
        cap = label(r"the same bass, \ the same figures, \ three correct realizations", font_size=22, color=WHITE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Before the test, see how much freedom the figures leave. Here are the first two bars of Corelli's bass, with "
            "the figures the violins imply, realized three times by the program, asked each time to start with its top "
            "voice in a different place. All three pass the realizer’s limited constraints; they differ at the start and then settle onto the same "
            "smoothest path. A real player would differ much more, breaking the chords and adding melody."
        ):
            self.play(FadeIn(fl), FadeIn(rolls), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"three realizations", detail=r"Part 1's string on Part 7's soundboard", corner=DL, tag_corner=DR)
            for k, key in enumerate(("r1", "r2", "r3")):
                r = d["realizations"][k]
                flash_voices(snd, rolls[k][1], [r["chords"], d["bass"]], d["starts"][key], d["unit"], colors=[[TUNE, BLUE, EAR][k], GREY_A])
                end = d["starts"][("r1", "r2", "r3")[k + 1]] - 0.4 if k < 2 else c.duration
                pulse(snd, rolls[k][0], d["starts"][key], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("corelli")
        c = clip("corelli.grave")
        card = listen_card(r"The same bass twice. \ Once with Corelli's own two violins above it; \ once with chords a program chose from the figures alone. \ "
                           r"Which is Corelli, \ A or B? \ Listen for melody above the bass.", width=10.6)
        with self.voiceover(
            "An experiment. Work out from Corelli's two violin parts which figures his bass would need, then throw the "
            "violins away and let Part 10's realizer fill in chords from the bass and the figures alone, as a continuo "
            "player might. Here is the same bass twice: once with Corelli's violins, once with the program's chords. Which "
            "is Corelli, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        gA = voices_roll([d["v1"], d["v2"], d["bass"]], width=5.6, height=2.8, colors=[TUNE, BLUE, GREY_A], lo=40, hi=88, bar_h=0.1).move_to(LEFT * 3.3 + DOWN * 0.3)
        gB = voices_roll([d["chords"], d["bass"]], width=5.6, height=2.8, colors=[EAR, GREY_A], lo=40, hi=88, bar_h=0.1).move_to(RIGHT * 3.3 + DOWN * 0.3)
        la = label(r"A", font_size=40, color=GREY_A).next_to(gA, UP, buff=0.3)
        lb = label(r"B", font_size=40, color=GREY_A).next_to(gB, UP, buff=0.3)
        self.play(FadeOut(card), FadeIn(gA), FadeIn(gB), FadeIn(la), FadeIn(lb))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"bowed violins, \ organ, \ harpsichord", kind="synthesized", corner=DL, tag_corner=DR)
            flash_voices(snd, gA, [d["v1"], d["v2"], d["bass"]], d["starts"]["corelli"], d["unit"], colors=[TUNE, BLUE, GREY_A])
            flash_voices(snd, gB, [d["chords"], d["bass"]], d["starts"]["realized"], d["unit"], colors=[EAR, GREY_A])
            pulse(snd, la, d["starts"]["corelli"], d["starts"]["realized"] - 0.5, buff=0.1)
            pulse(snd, lb, d["starts"]["realized"], c.duration, buff=0.1)
        ans = VGroup(label(r"Corelli: \ two violins in suspensions", font_size=22, color=TUNE).next_to(gA, DOWN, buff=0.35),
                     label(r"the realizer: \ the right chords, \ no melody", font_size=22, color=EAR).next_to(gB, DOWN, buff=0.35))
        with self.voiceover(
            "A is Corelli: two violins weaving in suspensions, one over the other, each a melody. B is the program: "
            "smooth, correct chords, and a deliberately plain upper line."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def compare(self):
        d = load("corelli")
        fc = d["figure_counts"]
        ag = d["agreement"]
        bars = columns([fc.get(k, 0) for k in ("", "6", "7", "6/5")], [r"none \ (5/3)", r"6", r"7", r"6/5"], width=5.6, height=2.6, color=TUNE, fmt="{:.0f}", font_size=20)
        bars.move_to(LEFT * 3.3 + DOWN * 0.4)
        t = label(rf"the {d['notes']} bass notes of the Grave, \ by the figure the violins imply", font_size=19, color=GREY_A).next_to(bars, UP, buff=0.35)
        side = VGroup(*[label(s, font_size=23, color=c_) for s, c_ in (
            (rf"the realizer's chords hold {100 * ag['pitch_classes']:.0f} in 100 of Corelli's notes", WHITE),
            (rf"its top note is the first violin's {100 * ag['top']:.0f} times in 100", WHITE),
            (rf"parallel fifths and octaves: \ {d['parallels']}", WHITE),
            (r"the figures carry the harmony; \ the composition is in the lines", TUNE))]).arrange(DOWN, buff=0.35, aligned_edge=LEFT)
        side.scale_to_fit_width(min(side.width, 6.2))
        side.move_to(RIGHT * 3.4 + DOWN * 0.2)
        with self.voiceover(
            f"The numbers. Over the Grave's {say(d['notes'])} bass notes, the violins imply no figure most often, then six, then seven: a texture rich in suspensions. <bookmark mark='a'/> The realizer's chords contain {say(round(100 * ag['pitch_classes']))} in a hundred of the notes Corelli's violins actually play: these figures were inferred from the very violin notes being compared, so this measures reconstruction with supplied harmonic information, not independent prediction from bass alone. <bookmark mark='b'/> But the realizer's top note is the first violin's only {say(round(100 * ag['top']))} times in a hundred. <bookmark mark='c'/> Its selected voicing path avoids the checked parallels; it does not reproduce Corelli’s melodic design. <bookmark mark='d'/> That is the Baroque division of labour: the bass and its figures carry the harmony, and the art of the composer, and of a good continuo player, is in the lines above it."
        ) as vo:
            self.play(FadeIn(t), FadeIn(bars))
            for mark, r in zip("abcd", side):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def partimento(self):
        items = [
            (r"Naples, \ eighteenth century: \ orphans trained as musicians in the conservatories", WHITE),
            (r"the partimento: \ an unfigured bass to be realized at the keyboard, \ day after day", WHITE),
            (r"the rule of the octave: \ a chord for every step of the scale in the bass \ (Part 18)", WHITE),
            (r"composition taught as improvisation over a bass", TUNE),
            (r"its graduates staffed the courts and opera houses of Europe", GREY_A),
        ]
        rows_scene(self, r"the bass as a school", items,
                   "The figured bass was also a school of composition. <bookmark mark='b'/> In the conservatories of Naples, which grew from charitable institutions with differing histories, boys were trained as musicians, <bookmark mark='c'/> and their daily exercise was the partimento: a bass, often without figures, to be realized at the keyboard. <bookmark mark='d'/> They learned the rule of the octave from Part 18, a chord for every step of the scale in the bass, and a stock of patterns for every situation. <bookmark mark='e'/> Composition was taught as improvisation over a bass, <bookmark mark='f'/> and the conservatories' graduates staffed the courts and opera houses of eighteenth-century Europe.", marks="cdef")
