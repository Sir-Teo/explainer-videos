from __future__ import annotations

from videos.psychology.psych28.common import *  # noqa: F403


class Wanting(VoiceoverScene):
    def construct(self):
        self.card()
        self.split()
        self.hotspots()
        self.salt_story()
        self.salt_model()

    def card(self):
        card = chapter_card(4, r"Wanting is not liking", r"Is dopamine pleasure?",
                            lit={1998: r"Berridge \& Robinson", 2003: r"Pe\~cina et al.", 2009: r"Zhang et al.",
                                 2013: r"Robinson \& Berridge"},
                            part=PART, scale=("molecule", "circuit", "mind"), marr=("what", "tissue"))
        with self.voiceover("Chapter four. Wanting is not liking."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def split(self):
        head = heading(r"Two things the word reward hides")
        face = Circle(radius=0.8, color=LIKE, fill_opacity=0.1).move_to([-4.6, 0.5, 0])
        tongue = Ellipse(width=0.35, height=0.25, color=LIKE, fill_opacity=0.8).move_to(face.get_bottom() + UP * 0.35)
        lab_like = label(r"liking: \ the face a sweet taste makes", font_size=18, color=LIKE).next_to(face, DOWN,
                                                                                                     buff=0.25)
        arrow = Arrow([-3.0, 0.5, 0], [-1.6, 0.5, 0], color=WANT, buff=0, stroke_width=5)
        lab_want = label(r"wanting: \ work, \ approach", font_size=18, color=WANT).next_to(arrow, DOWN, buff=0.3)
        rows = rows_of([
            (r"liking can be read without words: \ rats, \ monkeys and infants make the same tongue protrusions to "
             r"sweet tastes, \ and gapes to bitter ones", LIKE),
            (r"rats with nearly all their dopamine destroyed still make the liking faces to sugar, \ but will not "
             r"work for it, \ or even eat unaided", WANT),
            (r"mutant mice with extra dopamine work harder for sweet food, \ and like it no more", WANT),
            (r"Berridge and Robinson: \ dopamine is wanting, \ incentive salience, \ not pleasure", WHITE),
        ], 5.6, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Berridge \& Robinson (1998); \ Pe\~cina et al.\ (2003)")
        with self.voiceover(
            "Back to Olds and Milner's rat. Was it feeling pleasure? Kent Berridge spent decades showing that the "
            "question splits in two. <bookmark mark='a'/> Liking can be measured without words. Rats, monkeys and "
            "human infants make the same tongue protrusions to a sweet taste, and the same gapes to a bitter one, "
            "and those faces track how pleasant the taste is. <bookmark mark='b'/> Rats with nearly all of their "
            "dopamine destroyed still make the liking faces when sugar is put in their mouths, but they will not "
            "work for it, or even eat on their own. <bookmark mark='c'/> And mice engineered to have extra dopamine "
            "work harder to get sweet food, without liking it any more. <bookmark mark='d'/> So Berridge and Terry "
            "Robinson concluded in 1998: dopamine isn't pleasure. It is wanting, the pull that makes something an "
            "incentive. They called it incentive salience."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(face), FadeIn(tongue), FadeIn(lab_like))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), Indicate(tongue, color=LIKE))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), GrowArrow(arrow), FadeIn(lab_want))
            self.play(arrow.animate.set_opacity(0.2))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]), arrow.animate.set_opacity(1.0).scale(1.3))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()

    def hotspots(self):
        head = heading(r"Where liking lives")
        rows = rows_of([
            (r"liking has its own small sites: \ hedonic hotspots, \ about a cubic millimetre each in a rat, \ in "
             r"the nucleus accumbens shell and the ventral pallidum", LIKE),
            (r"opioid stimulation of a hotspot multiplies the liking faces to sugar; \ dopamine stimulation of the "
             r"same region raises wanting alone", WANT),
            (r"wanting's system is large and robust; \ liking's is small and fragile, \ which may be why pleasure "
             r"is harder to produce than desire", WHITE),
            (r"Olds and Milner's rat was probably wanting: \ stimulation that pulls without pleasing \ "
             r"(addiction, \ Part 41)", MODEL),
        ], 12.2, 27, 0.42).move_to([0, -0.2, 0])
        tag = published_tag(r"Pe\~cina \& Berridge (2005); \ Berridge \& Kringelbach (2015)")
        with self.voiceover(
            "Liking turned out to have its own machinery. <bookmark mark='a'/> Berridge's laboratory found small "
            "hedonic hotspots, about a cubic millimetre each in a rat's brain, in the shell of the nucleus accumbens "
            "and in the ventral pallidum. <bookmark mark='b'/> Stimulating opioid receptors in a hotspot multiplies "
            "the liking faces to sugar. Stimulating dopamine in the same region raises wanting alone. "
            "<bookmark mark='c'/> The wanting system is large and robust; the liking system is small and fragile, "
            "which may be why desire is easier to produce than pleasure. <bookmark mark='d'/> And Olds and "
            "Milner's rat was probably wanting: stimulation that pulls without pleasing. That gap between wanting "
            "and liking is at the centre of addiction, in Part 41."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag))
            for m, r in zip("abcd", rows):
                vo.wait_until(m)
                self.play(FadeIn(r, shift=RIGHT * 0.15))
        self.clear_scene()

    def salt_story(self):
        head = heading(r"A cue that changed value overnight")
        rod = RoundedRectangle(corner_radius=0.1, width=0.3, height=1.6, color=BODY, fill_opacity=0.6).move_to(
            [-4.6, 0.4, 0])
        rod_l = label(r"the cue", font_size=18, color=BODY).next_to(rod, DOWN, buff=0.2)
        drop = label(r"three times as salty as the sea", font_size=18, color=LOST).move_to([-2.4, 0.4, 0])
        rows = rows_of([
            (r"training: \ a lever-like rod enters the cage, \ and then intensely salty water is squirted into "
             r"the rat's mouth", BODY),
            (r"the rats learn to avoid the rod: \ its learned value is negative", LOST),
            (r"then a drug makes the body crave salt, \ a state these rats have never been in", WANT),
            (r"on the first test, \ with no salt ever given, \ they jump on the rod and nibble it", WANT),
        ], 5.6, 22, 0.32).move_to([3.4, -0.1, 0])
        tag = published_tag(r"Robinson \& Berridge (2013)")
        with self.voiceover(
            "The clearest demonstration came in 2013, from Mike Robinson and Berridge. <bookmark mark='a'/> In "
            "training, a lever-like rod enters the cage, and then a squirt of intensely salty water, about three "
            "times as salty as seawater, goes into the rat's mouth. <bookmark mark='b'/> The rats learn to avoid "
            "the rod. Whatever value they have learned for it is negative. <bookmark mark='c'/> Then a drug puts "
            "the rats' bodies into a state of salt appetite, a state they have never been in. "
            "<bookmark mark='d'/> On the very first test, with no salt delivered, they jump on the rod and nibble "
            "it. Nothing was relearned. The cue's value changed the moment the body's state did."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(rod), FadeIn(rod_l))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]), FadeIn(drop))
            vo.wait_until("b")
            self.play(FadeIn(rows[1]), rod.animate.set_color(LOST))
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3]), rod.animate.set_color(WANT), Wiggle(rod))
        self.clear_scene()

    def salt_model(self):
        d = load("salt")
        head = heading(r"Cached value, \ or value recomputed?")
        n = len(d["trial"])
        A = axes([0, n], [-1.1, 1.1], x_length=5.8, y_length=3.6, xticks=[0, 10, 20, 30, 40], yticks=[-1, 0, 1],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"trial", ylabel=r"the cue's value",
                 center=[-3.3, -0.2, 0], font_size=16)
        zero = DashedLine(A.ax.c2p(0, 0), A.ax.c2p(n, 0), color=GREY_D, stroke_width=2)
        sw = DashedLine(A.ax.c2p(d["switch"], -1.1), A.ax.c2p(d["switch"], 1.1), color=GREY_B, stroke_width=2)
        swl = label(r"salt appetite", font_size=16, color=WANT).next_to(A.ax.c2p(d["switch"], 1.1), UP, buff=0.05)
        cc = curve(A.ax, d["trial"], d["cached"], CTRL, 4)
        ci = curve(A.ax, d["trial"], d["incentive"], WANT, 4)
        key = legend([(CTRL, r"cached value \ (Part 17)"), (WANT, r"incentive value")], font_size=17)
        key.move_to(A.ax.c2p(12, 0.6))
        eq = MathTex(r"\tilde V(\text{cue}) = \gamma \, \tilde r(r, \kappa), \qquad \tilde r = \kappa\, r",
                     font_size=32)
        rows = rows_of([
            (r"Part 17's learner caches a value from what happened; \ in extinction, \ it can only decay toward "
             r"zero, \ never turn positive", CTRL),
            (r"Zhang, \ Berridge, \ Tindell, \ Smith and Aldridge, \ 2009: \ the cue's value is recomputed from the "
             r"learned outcome and the body's present state $\kappa$", WANT),
            (rf"the state flips the sign: \ the value jumps from {d['train_end']:.1f} to "
             rf"{d['test_incentive']:+.1f} on the first test", WANT),
            (r"wanting is computed at the moment of the cue, \ from memory and need together", WHITE),
        ], 5.6, 21, 0.3)
        right = VGroup(eq, rows).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([3.4, -0.1, 0])
        tag = psyche_tag(r"\texttt{drive.salt\_cue}")
        with self.voiceover(
            "Psyche can say what that requires. <bookmark mark='a'/> Part 17's learner caches a value from what has "
            "happened. During training the cue's value falls toward minus one. In the new state, with no salt "
            "delivered, it can only decay toward zero. It never turns positive. <bookmark mark='b'/> Jun Zhang, "
            "Berridge and their colleagues proposed in 2009 that incentive value is recomputed at the moment the "
            "cue appears, from the learned outcome and the body's present state, written kappa. "
            "<bookmark mark='c'/> Here the new state flips the sign of the salt's worth, and the cue's value jumps "
            f"from {d['train_end']:.1f} to plus {d['test_incentive']:.1f} on the first test, with no learning. "
            "<bookmark mark='d'/> Wanting is computed when the cue arrives, from memory and need together. That's "
            "the homeostatic loop of chapter two, reaching into the learner of Part 17."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero), FadeIn(sw), FadeIn(swl))
            vo.wait_until("a")
            self.play(Create(cc), FadeIn(key[0]), FadeIn(rows[0]), run_time=2.0)
            vo.wait_until("b")
            self.play(FadeIn(eq), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(Create(ci), FadeIn(key[1]), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
