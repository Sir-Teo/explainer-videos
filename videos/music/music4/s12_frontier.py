from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ the ear is alive", r"What is the amplifier, and what does it cost?", lit=(1863,),
                extra=((1948, r"Gold predicts it"), (1978, r"Kemp hears it"), (2000, r"prestin")))
        self.amplifier()
        self.edge()
        self.third()
        self.emissions()
        self.open()

    # ------------------------------------------------------------------
    def amplifier(self):
        d = load("wave")
        co = Cochlea(width=9.6, scale=1.0).move_to(UP * 0.75 + LEFT * 0.9)
        dead = co.lens(d["passive"], color=GREY_B, opacity=0.5)
        live = co.lens(d["active"], color=EAR, opacity=0.35)
        tags = VGroup(label(r"friction as in a dead ear", font_size=24, color=GREY_B), label(r"friction cut to a quarter", font_size=24, color=EAR),
                      label(rf"the peak: \ {d['gain_db']:.0f} dB taller, \ twice as sharp", font_size=24, color=GOOD)).arrange(DOWN, buff=0.14, aligned_edge=LEFT)
        tags.move_to(RIGHT * 4.2 + UP * 3.0)
        cards = VGroup(
            history_card(1971, r"William Rhode", r"measures the membrane in living squirrel monkeys: sharply tuned, and not proportional to the sound. After death: B\'ek\'esy's wave.", width=4.2, font_size=20),
            history_card(1985, r"William Brownell", r"an outer hair cell changes its length when its voltage changes. It is a motor.", width=4.2, font_size=20),
            history_card(2000, r"Jing Zheng, Peter Dallos and colleagues", r"find the motor's protein, and name it prestin.", width=4.2, font_size=20),
        ).arrange(RIGHT, buff=0.3, aligned_edge=UP).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "We left two mysteries open. Twelve thousand outer hair cells that tell the brain almost nothing. "
            "And Gold's argument that a passive ear cannot be as sharp as ours. They are the same mystery. "
            "<bookmark mark='a'/> Here is our model's wave for a tone of two thousand hertz, with the friction "
            "you would find in a dead cochlea: low and broad. <bookmark mark='b'/> Cut the friction to a quarter, "
            f"and the same tone gives a peak {say(d['gain_db'])} decibels taller and twice as sharp. That is what "
            "living ears look like. <bookmark mark='c'/> In 1971 William Rhode measured the membrane in living "
            "squirrel monkeys and found it sharply tuned, and, strangely, not proportional to the sound: double "
            "the pressure, and the motion less than doubled. When the animal died, the response turned into "
            "Békésy's. <bookmark mark='d'/> Something alive was cancelling the friction. In 1985 William Brownell "
            "found what. An outer hair cell changes its length when its voltage changes. It is a motor, fast "
            "enough to push on the membrane in time with the wave. <bookmark mark='e'/> In 2000 the protein that "
            "does it was found and named prestin. The outer hair cells do not report the sound. They amplify it."
        ) as vo:
            self.play(FadeIn(co))
            vo.wait_until("a")
            self.play(FadeIn(dead), FadeIn(tags[0]))
            vo.wait_until("b")
            self.play(FadeIn(live), FadeIn(tags[1]), FadeIn(tags[2]))
            for mark, c_ in zip("cde", cards):
                vo.wait_until(mark)
                self.play(FadeIn(c_))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def edge(self):
        d = load("active")
        g = axes([0, 100], [-100, 5], x_length=6.0, y_length=4.4, xlabel=r"sound going in (dB)", ylabel=r"motion coming out (dB)",
                 xticks=[0, 20, 40, 60, 80, 100], yticks=[-100, -80, -60, -40, -20, 0], font_size=20)
        g.move_to(RIGHT * 3.0 + DOWN * 0.2)
        pas = curve(g.ax, d["in_db"], d["passive_db"], GREY_B)
        act = curve(g.ax, d["in_db"], d["active_db"], EAR)
        pl = label(r"passive: \ 100 dB in, \ 100 dB out", font_size=22, color=GREY_B).move_to(g.ax.c2p(62, -72))
        al = label(rf"at the edge: \ 100 dB in, \ {d['range_out']:.0f} dB out", font_size=22, color=EAR).move_to(g.ax.c2p(32, -5))
        notes = VGroup(
            label(r"an amplifier that exactly cancels friction \\ is on the edge of oscillating by itself", font_size=26, color=GREY_A),
            MathTex(r"\text{response} \;\propto\; \text{force}^{1/3}", font_size=38, color=EAR),
            label(r"faint sounds: \ amplified enormously", font_size=26, color=GOOD),
            label(r"loud sounds: \ hardly at all", font_size=26, color=GOOD),
            label(r"the compressor of chapter 4", font_size=28, color=LEVEL),
        ).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(LEFT * 3.6 + UP * 0.1)
        src = label(r"Camalet, Duke, J\"ulicher and Prost; \ Egu\'iluz and colleagues \ (2000)", font_size=18, color=GREY_C).to_edge(DOWN, buff=0.3).align_to(notes, LEFT)
        with self.voiceover(
            "How much should an amplifier like that amplify? Think of a microphone held near its own loudspeaker. "
            "Turn up the gain, and just before the howl begins the system becomes extraordinarily sensitive. "
            "<bookmark mark='a'/> An amplifier that exactly cancels friction sits on that edge, and in the year "
            "2000 two groups of physicists pointed out that anything poised there obeys a universal law. "
            "<bookmark mark='b'/> At its own frequency, its response grows not in proportion to the force, but as "
            "the cube root of it. <bookmark mark='c'/> Here is what that means. A passive membrane turns a hundred "
            f"decibels of input into a hundred decibels of motion. An oscillator at the edge turns it into "
            f"{say(d['range_out'])}. <bookmark mark='d'/> Faint sounds are amplified enormously, loud ones hardly "
            "at all. <bookmark mark='e'/> This is the machine we were looking for in chapter four: the one that "
            "squeezes a million million into a few thousand. The ear's compression is not done in the brain. It "
            "is done by motors on the membrane, before the sound has even been detected."
        ) as vo:
            mic = VGroup(Circle(radius=0.28, stroke_color=GREY_A, stroke_width=3, fill_color=GREY_D, fill_opacity=0.6),
                         Line(DOWN * 0.28, DOWN * 0.9, color=GREY_A, stroke_width=4)).move_to(LEFT * 1.6)
            spk = speaker_icon(0.8, GREY_A).move_to(RIGHT * 1.6)
            there = CurvedArrow(mic.get_top() + UP * 0.1, spk.get_top() + UP * 0.1, angle=-PI / 2, color=EAR, stroke_width=3)
            back = CurvedArrow(spk.get_bottom() + DOWN * 0.1, mic.get_bottom() + DOWN * 0.1, angle=-PI / 2, color=EAR, stroke_width=3)
            loop = VGroup(mic, spk, there, back, label(r"just below the howl: \ extremely sensitive", font_size=28, color=EAR).move_to(DOWN * 2.2))
            self.play(FadeIn(mic), FadeIn(spk))
            self.play(Create(there), Create(back), run_time=1.5)
            self.play(FadeIn(loop[4]))
            vo.wait_until("a")
            self.play(FadeOut(loop), run_time=0.4)
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), FadeIn(src))
            vo.wait_until("c")
            self.play(FadeIn(g), Create(pas), FadeIn(pl), run_time=1.5)
            self.play(Create(act), FadeIn(al), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(notes[2]), FadeIn(notes[3]))
            vo.wait_until("e")
            self.play(FadeIn(notes[4]))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def third(self):
        d = load("two")
        c = clip("two.guide")
        q = listen_note(r"First a quiet guide tone, \ 800 Hz. \ Then the two tones from the opening of this part. \\ "
                        r"Listen underneath them for the guide's pitch. \ Then the guide again.", width=10.4, font_size=26).to_edge(UP, buff=0.35)
        g = axes([600, 1400], [0, 1.15], x_length=8.0, y_length=2.4, xlabel=r"frequency (Hz)", ylabel="", xticks=[600, 800, 1000, 1200, 1400], yticks=[], font_size=20)
        g.move_to(DOWN * 1.0)
        guide = Line(g.ax.c2p(800, 0), g.ax.c2p(800, 0.3), color=EAR, stroke_width=8)
        pair = VGroup(*[Line(g.ax.c2p(f, 0), g.ax.c2p(f, 1.0), color=TUNE, stroke_width=8) for f in (1000, 1200)])
        with self.voiceover(
            "The amplifier has a price, and you can hear it. An amplifier that responds as a cube root cannot "
            "handle two tones at once without mixing them. It is time to keep the promise made at the start. "
            "First you will hear a quiet guide tone at eight hundred hertz, so that you know what to listen for. "
            "Then the two tones again, a thousand and twelve hundred. Listen underneath them. Then the guide "
            "once more."
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(g), FadeIn(guide), FadeIn(pair))
        with self.listen(c) as snd:
            window(snd, r"guide, \ the two tones, \ guide", kind="synthesized", detail=r"three sines", corner=DL, tag_corner=DR)
            tg, tp, ta = (snd.time_of(e) for e in ("guide", "pair", "again"))
            snd.drive(guide, lambda m, t: m.set_stroke(opacity=(0.7 + 0.3 * np.sin(20 * t)) if (tg <= t < tg + 1.2 or t >= ta) else 0.12))
            snd.drive(pair, lambda m, t: m.set_stroke(opacity=(0.7 + 0.3 * np.sin(20 * t)) if tp <= t < tp + 3.0 else 0.12))
        guide.set_stroke(opacity=1)
        pair.set_stroke(opacity=1)
        eq = MathTex(r"2f_1 - f_2 \;=\; 2\times 1000 - 1200 \;=\; 800\ \text{Hz}", font_size=36, color=EAR).move_to(UP * 2.4)
        facts = VGroup(label(rf"in the recording: \ {abs(d['in_the_clip_db']):.0f} dB down. \ Not there.", font_size=26, color=GREY_A),
                       label(rf"in Monochord's oscillator at the edge: \ {abs(d['ear_third_db']):.0f} dB below the two tones. \ Audible.", font_size=26, color=EAR)
                       ).arrange(DOWN, buff=0.15).move_to(UP * 1.35)
        card = history_card(1754, r"Giuseppe Tartini", r"the violinist publishes his ``third sound'': a low tone heard under two notes played together, which he used to tune them", width=5.4, font_size=20)
        card.to_corner(DL, buff=0.35)
        baby = label(r"today: \ the same tone, \ measured in the ear canal, \\ is how a newborn's hearing is tested", font_size=24, color=GOOD).to_corner(DR, buff=0.5)
        with self.voiceover(
            "With the guide in your ear, most people find it: a faint tone at the guide's pitch, under the two. "
            "<bookmark mark='a'/> Twice the lower frequency, minus the upper one, is eight hundred hertz. That "
            f"tone is {say(abs(d['in_the_clip_db']))} decibels down in the recording, which is to say it is not "
            "there. <bookmark mark='b'/> But give the same two tones to an oscillator poised at the edge, tuned "
            f"to eight hundred hertz, and it produces that tone only {say(abs(d['ear_third_db']))} decibels below "
            "them. The ear makes it, on the membrane, as a real vibration. <bookmark mark='c'/> The violinist "
            "Giuseppe Tartini described it in 1754. He called it the third sound, and taught his pupils to "
            "listen for it when tuning two strings together. <bookmark mark='d'/> And because it is a real "
            "vibration, it travels back out through the middle ear and can be picked up with a microphone in "
            "the ear canal. That is now how the hearing of newborn babies is tested, a day or two after birth: "
            "two tones in, and if the third comes back, the amplifier is working."
        ) as vo:
            self.play(FadeOut(q))
            vo.wait_until("a")
            self.play(FadeIn(eq), FadeIn(facts[0]))
            vo.wait_until("b")
            self.play(FadeIn(facts[1]))
            vo.wait_until("c")
            self.play(g.animate.scale(0.75).shift(UP * 0.35), VGroup(guide, pair).animate.scale(0.75, about_point=g.get_center()).shift(UP * 0.35), FadeIn(card))
            vo.wait_until("d")
            self.play(FadeIn(baby))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def emissions(self):
        rows = VGroup(
            label(r"an amplifier at the edge \ldots", font_size=30, color=GREY_A),
            label(r"is extremely sensitive to faint sounds", font_size=30, color=GOOD),
            label(r"is sharply tuned", font_size=30, color=GOOD),
            label(r"compresses a huge range", font_size=30, color=GOOD),
            label(r"adds tones of its own when given two", font_size=30, color=EAR),
            label(r"rings after a click: \ Kemp's echo", font_size=30, color=EAR),
            label(r"sometimes tips over, \ and sings by itself", font_size=30, color=EAR),
        ).arrange(DOWN, buff=0.28, aligned_edge=LEFT).move_to(LEFT * 2.2)
        rows[0].shift(LEFT * 0.6)
        gold = history_card(1948, r"Thomas Gold", r"predicted that an ear with such an amplifier might ring by itself. Many healthy ears do: a faint, steady tone, measurable with a microphone.", width=4.6, font_size=20)
        gold.move_to(RIGHT * 4.2 + DOWN * 1.2)
        with self.voiceover(
            "Put the list together. An amplifier at the edge of oscillation <bookmark mark='a'/> is extremely "
            "sensitive to faint sounds, <bookmark mark='b'/> sharply tuned, <bookmark mark='c'/> and compresses "
            "a huge range of levels. Those are its benefits. <bookmark mark='d'/> It adds tones of its own when it "
            "is given two. <bookmark mark='e'/> It keeps ringing after a click, which is Kemp's echo. "
            "<bookmark mark='f'/> And every so often, a patch of it tips over the edge and sings by itself. Many "
            "healthy ears give out a faint steady tone that a microphone in the ear canal can record. Gold "
            "predicted it in 1948. He was thirty years early, and he was right about all of it."
        ) as vo:
            self.play(FadeIn(rows[0]))
            for mark, r in zip("abcdef", rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.5)
            self.play(FadeIn(gold))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def open(self):
        w = load("wave")
        head = label(r"What is not known", font_size=40, color=LIMIT).to_edge(UP, buff=0.4)
        cards = VGroup(
            VGroup(label(r"hidden hearing loss", font_size=30, color=LIMIT),
                   label(r"Kujawa and Liberman (2009): \ in mice, \ noise that only dulls hearing for a few days \\ permanently destroys the "
                         r"connections between hair cells and nerve. \\ The hearing test recovers. \ How much of this happens in people?", font_size=24, color=GREY_A)),
            VGroup(label(r"the amplifier itself", font_size=30, color=LIMIT),
                   label(r"new optical methods can watch the parts of the living cochlea move. \\ They move in ways no current model predicts.", font_size=24, color=GREY_A)),
            VGroup(label(r"music through an implant", font_size=30, color=LIMIT),
                   label(rf"more than a million people hear through cochlear implants: \ about twenty electrodes \\ in place of {w['inner']:,} hair cells. \ "
                         r"Speech works. \ Melody mostly does not.".replace(",", "{,}"), font_size=24, color=GREY_A)),
            VGroup(label(r"growing them back", font_size=30, color=LIMIT),
                   label(r"birds regrow hair cells; \ mammals do not. \ In 2024 gene therapy gave hearing \\ to children born without one protein of the hair cell's synapse.", font_size=24, color=GREY_A)),
        )
        for k, c_ in enumerate(cards):
            c_.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
            c_.move_to(LEFT * 6.2 + UP * (2.1 - 1.55 * k), aligned_edge=LEFT)
        with self.voiceover(
            "And here the textbook ends. Four things that are not known. <bookmark mark='a'/> First. In 2009 "
            "Sharon Kujawa and Charles Liberman exposed mice to noise that dulled their hearing for a few days, "
            "after which it tested as normal again. But inside the cochlea, up to half of the connections "
            "between the hair cells and the nerve had gone, for good. A standard hearing test cannot see that "
            "loss. Nobody yet knows how much of it people carry, and it may be why the ringing after a concert "
            "is not harmless. <bookmark mark='b'/> Second: the amplifier itself. New optical methods can watch "
            "the parts of a living cochlea move, and they move in ways that no current model predicts. "
            "<bookmark mark='c'/> Third. More than a million people now hear through cochlear implants, which "
            f"replace {say(w['inner'])} hair cells with about twenty electrodes. Speech comes through remarkably "
            "well. Melody mostly does not, for exactly the reasons in this part: twenty places are too few, and "
            "the implant's pulses carry almost none of the timing. Giving music back to implant users is an open "
            "problem. <bookmark mark='d'/> Fourth: growing hair cells back. Birds do it. We do not. But in 2024 "
            "a gene therapy gave hearing to children who were born deaf for lack of a single protein. That is "
            "one cause among hundreds, and it is a beginning."
        ) as vo:
            self.play(FadeIn(head))
            for mark, c_ in zip("abcd", cards):
                vo.wait_until(mark)
                self.play(FadeIn(c_), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()
