from __future__ import annotations

import numpy as np

from videos.music.music4.common import *  # noqa: F403


class Loud(SoundScene):
    def construct(self):
        chapter(self, 4, r"How loud is loud?", r"Why does the same pressure not always sound equally loud?", lit=(1863,),
                extra=((1933, r"Fletcher and Munson's curves"), (1936, r"Stevens's sone")))
        self.sweep()
        self.three()
        self.sones()
        self.worked()

    # ------------------------------------------------------------------
    def sweep(self):
        d = load("loud")
        c = clip("loud.sweep")
        g = faxes(20, 16000, [-10, 90], x_length=9.2, y_length=3.3, ylabel=r"sound pressure level (dB)", yticks=[0, 20, 40, 60, 80], font_size=20)
        g.move_to(DOWN * 0.7)
        lo, hi, secs = d["sweep_lo"], d["sweep_hi"], d["sweep_seconds"]
        flat = Line(g.at(lo, 60), g.at(hi, 60), color=FORCE, stroke_width=3)
        fl = label(r"the tone: \ the same pressure throughout", font_size=24, color=FORCE).next_to(flat, UP, buff=0.15)
        dot = Dot(g.at(lo, 60), radius=0.12, color=TUNE)
        q = listen_note(r"One tone slides from 100 Hz up to 10,000 Hz, \ at constant pressure. \\ Does it stay equally loud?", width=9.4).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Now a different question about the same instrument. Part 2 measured the strength of a sound by its "
            "pressure, in decibels. Is that what you hear? Here is a tone that slides from a hundred hertz to ten "
            "thousand, with exactly the same pressure throughout. Listen to whether it stays equally loud."
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(g), FadeIn(flat), FadeIn(fl), FadeIn(dot))
        with self.listen(c) as snd:
            window(snd, r"100 Hz to 10,000 Hz, \ constant pressure", kind="synthesized", detail=r"needs bass at the start", corner=DR, tag_corner=DL)
            snd.drive(dot, lambda m, t: m.move_to(g.at(lo * (hi / lo) ** float(np.clip(t / secs, 0, 1)), 60)))
        thr = fcurve(g, d["f"], np.minimum(d["threshold"], 88), EAR)
        tl = label(r"the quietest sound a young ear can hear", font_size=24, color=EAR).move_to(g.at(900, 34))
        r = {int(x["hz"]): x for x in d["rows"]}
        marks = VGroup(*[VGroup(Dot(g.at(hz, r[hz]["threshold"]), radius=0.07, color=WHITE),
                                label(rf"{r[hz]['threshold']:.0f} dB", font_size=22).next_to(g.at(hz, r[hz]["threshold"]), DOWN if hz != 100 else RIGHT, buff=0.15))
                         for hz in (100, 1000, 3500)])
        with self.voiceover(
            "It did not. It began faint, swelled as it rose, was at its strongest between three and four "
            "thousand hertz, and then thinned out. <bookmark mark='a'/> Here is the reason, the curve from "
            "chapter one, now over the whole range: the quietest sound a young ear can detect. <bookmark mark='b'/> "
            f"At a thousand hertz it is about {say(r[1000]['threshold'])} decibels. Near three and a half "
            f"thousand, at the ear canal's resonance, it dips to {say(r[3500]['threshold'])}. But at a hundred "
            f"hertz it is {say(r[100]['threshold'])} decibels: a bass tone needs ten times the pressure of a "
            "mid-range tone merely to be heard at all. And below twenty hertz, and above fifteen or twenty "
            "thousand, no pressure is enough. Your pressure meter and your ear disagree, by a great deal."
        ) as vo:
            self.play(FadeOut(q))
            vo.wait_until("a")
            self.play(Create(thr), FadeIn(tl), run_time=2.0)
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(m) for m in (marks[1], marks[2], marks[0])], lag_ratio=0.8), run_time=6.0)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def three(self):
        d = load("loud")
        c = clip("loud.three")
        q = listen_card(r"Three tones with exactly the same pressure: \ 100 Hz, \ 1000 Hz, \ 3500 Hz. \\ Which is the softest? \ Which is the loudest?",
                        width=9.6).to_edge(UP, buff=0.45)
        bx = boxes((r"100 Hz", r"1000 Hz", r"3500 Hz"), buff=0.8, width=2.9, height=1.3, font_size=34).move_to(UP * 0.2)
        meters = VGroup(*[Meter(width=0.45, height=1.5, color=FORCE).next_to(b, DOWN, buff=0.3) for b in bx])
        for m in meters:
            m.set_level(0.7)
        ml = label(r"pressure: \ equal", font_size=22, color=FORCE).next_to(meters, RIGHT, buff=0.4)
        with self.voiceover(
            "Test it on steady tones. Three tones, a hundred hertz, a thousand, and thirty-five hundred, each "
            "with exactly the same pressure. Which is the softest, and which the loudest?"
        ):
            self.play(FadeIn(q, shift=DOWN * 0.2), FadeIn(bx), FadeIn(meters), FadeIn(ml))
        with self.listen(c) as snd:
            window(snd, r"three tones, \ equal pressure", kind="synthesized", detail=r"needs bass for the first", corner=DL, tag_corner=DR)
            for ev, b in zip(("low", "mid", "high"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 1.4)
        r = d["rows"]
        card = history_card(1933, r"Harvey Fletcher and Wilden Munson",
                            r"ask listeners to match tones of every frequency to a 1000 Hz tone, by loudness. The "
                            r"matched level is the tone's loudness level, in \textbf{phons}.", width=5.6).to_corner(DL, buff=0.4)
        g = faxes(20, 16000, [-55, 10], x_length=5.6, y_length=1.7, ylabel=r"the A-weighting of a sound level meter (dB)", yticks=[-40, -20, 0], font_size=18)
        g.to_corner(DR, buff=0.45)
        aw = fcurve(g, d["f"], d["a_weight"], GOOD)
        ans = VGroup(*[label(rf"{x['a_db']:+.0f} dB", font_size=28, color=GOOD).next_to(m, DOWN, buff=0.15) for x, m in zip(r, meters)])
        with self.voiceover(
            "The low tone is much the softest, if your loudspeakers reproduce it at all, and the high one the "
            "loudest. <bookmark mark='a'/> In 1933 Fletcher and Wilden Munson turned this into a measurement. They "
            "had listeners adjust tones of every frequency until each sounded as loud as a reference tone at a "
            "thousand hertz. The level of the matching reference is called the tone's loudness level, in phons. "
            "<bookmark mark='b'/> Sound level meters carry a simplified version of their curves, called the A "
            f"weighting. Before adding up the energy, the meter turns a tone at a hundred hertz down by "
            f"{say(abs(r[0]['a_db']))} decibels, and leaves one at a thousand alone. Whenever you see a noise "
            "level quoted in d B A, this is the correction that has been made."
        ) as vo:
            self.play(FadeOut(q), FadeOut(ml), VGroup(bx, meters).animate.shift(UP * 1.9))
            ans = VGroup(*[label(rf"{x['a_db']:+.0f} dB", font_size=28, color=GOOD).next_to(m, RIGHT, buff=0.2) for x, m in zip(r, meters)])
            vo.wait_until("a")
            self.play(FadeIn(card))
            vo.wait_until("b")
            self.play(FadeIn(g), Create(aw), FadeIn(ans), run_time=1.5)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def sones(self):
        d = load("loud")
        c = clip("loud.ten")
        card = history_card(1936, r"S. S. Stevens, \ Harvard",
                            r"does not ask ``are these equal?'' but ``make this one twice as loud''", width=5.4).to_corner(UL, buff=0.4)
        bx = boxes((r"one note", r"the same, \ $+10$ dB"), buff=0.8, width=3.4, height=1.3, font_size=30).move_to(RIGHT * 2.9 + UP * 1.9)
        with self.voiceover(
            "Phons say when two sounds are equally loud. They do not say how much louder one sound is than "
            "another. In 1936 Stanley Stevens asked listeners a blunter question: make this sound twice as loud. "
            "<bookmark mark='a'/> Try his result. Here is a note, and then the same note with ten times the "
            "power, ten decibels more. How much louder is the second?"
        ) as vo:
            self.play(FadeIn(card))
            vo.wait_until("a")
            self.play(FadeIn(bx))
        with self.listen(c) as snd:
            window(snd, r"one note, \ then ten times the power", detail=r"Part 1's string", corner=DL, tag_corner=DR)
            for ev, b in zip(("one", "ten"), bx):
                t0 = snd.time_of(ev)
                pulse(snd, b, t0, t0 + 1.6)
        g = axes([20, 100], [-2, 6], x_length=5.4, y_length=3.0, xlabel=r"loudness level (phons)", ylabel=r"loudness (sones)",
                 xticks=[20, 40, 60, 80, 100], yticks=[-2, 0, 2, 4, 6], yfmt=lambda v: f"{2 ** v:g}", font_size=20)
        g.move_to(RIGHT * 3.2 + DOWN * 1.3)
        line = curve(g.ax, d["phons"], np.log2(d["sones"]), LEVEL)
        dots = VGroup(*[Dot(g.ax.c2p(p, np.log2(s)), radius=0.06, color=LEVEL) for p, s in zip(d["phons"], d["sones"])])
        rule = VGroup(label(r"$+10$ dB \ = \ 10 times the power", font_size=28, color=FORCE),
                      label(r"= \ twice as loud", font_size=34, color=LEVEL),
                      label(r"loudness \ $\propto$ \ power$^{\,0.3}$", font_size=28, color=GREY_A)).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        rule.next_to(card, DOWN, buff=0.5).align_to(card, LEFT)
        back = label(r"Part 2: \ ten violins are $+10$ dB over one. \ Now we know: \ twice as loud.", font_size=26, color=GOOD).to_edge(DOWN, buff=0.3)
        g.shift(UP * 0.35)
        VGroup(line, dots).shift(UP * 0.35)
        with self.voiceover(
            "Most people say: about twice as loud. Not ten times. <bookmark mark='a'/> That is Stevens's law. Ten "
            "times the power is heard as twice the loudness, and his unit, the sone, doubles with every ten "
            "phons. Loudness grows as roughly the zero point three power of the sound's power. "
            "<bookmark mark='b'/> And it settles something from Part 2. We found there that ten violins playing "
            "together are ten decibels stronger than one. Now we can say what that sounds like: twice as loud. To "
            "double the loudness of a section, you do not hire a second player. You hire nine more."
        ) as vo:
            self.play(FadeOut(bx))
            vo.wait_until("a")
            self.play(FadeIn(rule), FadeIn(g), Create(line), FadeIn(dots))
            vo.wait_until("b")
            self.play(FadeIn(back))
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def worked(self):
        d = load("loud")
        title = label(r"A worked example: \ why sixteen first violins?", font_size=36).to_edge(UP, buff=0.45)
        fiddles = VGroup(*[Dot(radius=0.13, color=STR) for _ in range(16)]).arrange_in_grid(2, 8, buff=0.3).move_to(UP * 1.7)
        ask = pause_card(r"An orchestra seats sixteen first violins. \\ How much louder are they than one of them alone?", width=8.2).move_to(DOWN * 0.3)
        steps = VGroup(MathTex(rf"10\log_{{10}} 16 = {d['sixteen_db']:.0f}\ \text{{dB}}", font_size=36),
                       MathTex(rf"2^{{\,{d['sixteen_db']:.0f}/10}} = {d['sixteen_times']:.1f}\ \text{{times as loud}}", font_size=36, color=GOOD)
                       ).arrange(RIGHT, buff=1.0).move_to(DOWN * 0.1)
        rng = VGroup(label(r"the whole range of hearing: \ 120 dB \ = \ a million million in power", font_size=28, color=FORCE),
                     label(r"heard as twelve doublings: \ about 4000 in loudness", font_size=28, color=LEVEL)).arrange(DOWN, buff=0.2).move_to(DOWN * 2.2)
        with self.voiceover(
            "A worked example. A full orchestra seats sixteen first violins. How much louder are sixteen than "
            "one? Pause and work it out, in decibels and then in loudness."
        ):
            self.play(FadeIn(title), LaggedStart(*[FadeIn(f) for f in fiddles], lag_ratio=0.05), FadeIn(ask, shift=UP * 0.2))
        self.wait(1.5)
        with self.voiceover(
            f"Sixteen times the power is {say(d['sixteen_db'])} decibels, and at a doubling for every ten "
            f"decibels that is about {say(d['sixteen_times'], 1)} times as loud. Sixteen players, for a little "
            "more than twice the loudness. So composers do not double an instrument to make it louder. They "
            "double it to change its colour, and it is why one solo violin can still be heard against all "
            "sixteen. <bookmark mark='a'/> The same compression runs through the whole of hearing. From the "
            "quietest sound to the threshold of pain is a hundred and twenty decibels, a factor of a million "
            "million in power. The ear hears it as twelve doublings. Somewhere in there is a machine that "
            "squeezes a range of a million million into a few thousand, and we will find it in the last chapter."
        ) as vo:
            self.play(FadeOut(ask), FadeIn(steps))
            vo.wait_until("a")
            self.play(FadeIn(rng[0]))
            self.play(FadeIn(rng[1]))
        self.wait(0.3)
        self.clear_scene()
