from __future__ import annotations

import numpy as np

from videos.music.music55.common import *  # noqa: F403


def dcol(az):
    a = abs(az)
    return GREY_A if a < 25 else (EAR if a > 155 else TUNE)


class Halls(SoundScene):
    def construct(self):
        chapter(self, 4, r"Early reflections and hall shapes", r"Two halls ring for the same time. \ Why does one sound better?")
        self.early()
        self.train()
        self.lateral()
        self.width()
        self.quiz()
        self.shapes()

    # ------------------------------------------------------------------
    def early(self):
        items = [
            (r"the first reflections, \ within 30 ms or so, \ fuse with the direct sound: \ heard as one, \ from the source \ (the precedence effect)", WHITE),
            (r"they make the sound louder and closer; \ Beranek prized a short gap before the first of them, \ about 20 ms, \ as intimacy", WHITE),
            (r"clarity: \ $C_{80}$, \ the energy in the first 80 ms over the energy after, \ in decibels", WHITE),
            (r"reverberation joins the notes; \ early reflections decide how clear, \ loud, \ near and wide they are", TUNE),
            (r"Philharmonic Hall's trouble lay here: \ overhead panels reflected the treble, \ not the bass, \ and not from the sides", GREY_A),
        ]
        rows_scene(self, r"the first 80 milliseconds", items,
                   "Two halls can ring for exactly the same time and sound nothing alike. The difference is in the first eighty "
                   "milliseconds. <bookmark mark='b'/> Reflections that arrive within thirty milliseconds or so of the direct sound "
                   "fuse with it: we hear one sound, from the source, which is the precedence effect of Wallach and of Haas. "
                   "<bookmark mark='c'/> They make the sound louder and nearer; Leo Beranek, surveying the world's halls, prized a "
                   "short gap before the first of them, about twenty milliseconds, and called it intimacy. "
                   "<bookmark mark='d'/> Clarity, C eighty, is the energy in the first eighty milliseconds against everything "
                   "after, in decibels. <bookmark mark='e'/> Reverberation joins the notes; the early reflections decide how clear, "
                   "how loud, how near and how wide they are. <bookmark mark='f'/> Philharmonic Hall's trouble lay exactly here: "
                   "its overhead panels reflected the treble but not the bass, and nothing came from the sides.", marks="bcdef")

    # ------------------------------------------------------------------
    def train(self):
        d = load("halls")
        ax = frame_axes(width=10.0, height=2.8, xlo=0, xhi=100, ylo=0, yhi=1.05, center=DOWN * 0.4)
        st = VGroup()
        for t, g, az in d["early"]:
            st.add(VGroup(Line(ax.to(t, 0), ax.to(t, g), color=dcol(az), stroke_width=3), Dot(ax.to(t, g), radius=0.055, color=dcol(az))))
        xt = VGroup(*[label(f"{v} ms", font_size=15, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.12) for v in (0, 20, 40, 60, 80, 100)])
        key = VGroup(label(r"from in front, \ the floor or the ceiling", font_size=17, color=GREY_A), label(r"from the sides", font_size=17, color=TUNE),
                     label(r"from behind", font_size=17, color=EAR)).arrange(RIGHT, buff=0.7).to_edge(UP, buff=1.0)
        gap = BraceBetweenPoints(ax.to(0.6, 0.75), ax.to(18.7, 0.75), UP, color=GREY_A)
        gl = label(r"18 ms gap", font_size=15, color=GREY_A).next_to(gap, UP, buff=0.08)
        note = label(r"an 18 m wide shoebox hall, \ seat 20 m from the stage: \ reflections up to two bounces, \ by the image method of Chapter 5", font_size=17, color=WHITE).to_edge(DOWN, buff=0.4)
        head = label(r"what arrives, \ and from where", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Here is what reaches one seat in a shoebox hall eighteen metres wide, twenty metres from the stage, in the first "
            "hundred milliseconds. <bookmark mark='a'/> The direct sound, and half a millisecond later its reflection from the "
            "floor. <bookmark mark='b'/> Then a gap of eighteen milliseconds, and the first reflections from the two side walls, "
            "from forty degrees left and right. <bookmark mark='c'/> Then the ceiling, more side walls, and after eighty "
            "milliseconds the back wall. Every one of these is computed by the image method we will meet in Chapter 5."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(key), FadeIn(note), FadeIn(ghost(st, 0.25)))
            vo.wait_until("a")
            self.play(FadeIn(st[0]), FadeIn(st[1]))
            vo.wait_until("b")
            self.play(FadeIn(gap), FadeIn(gl), LaggedStart(*[FadeIn(s) for s in st[2:6]], lag_ratio=0.2), run_time=1.4)
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(s) for s in st[6:]], lag_ratio=0.1), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def lateral(self):
        eq = MathTex(r"LF = \frac{\int_{5\,\mathrm{ms}}^{80\,\mathrm{ms}} p^2(t)\cos^2\theta\,dt}{\int_{0}^{80\,\mathrm{ms}} p^2(t)\,dt}", font_size=40, color=TUNE).move_to(UP * 1.3)
        items = [
            (r"Marshall \ (1967) \ and Barron \ (1971, \ 1981): \ reflections from the sides make the sound wide and enveloping, \ \textit{spatial impression}", WHITE),
            (r"the two ears hear different sounds; \ the brain hears the source broaden and the hall surround it", WHITE),
            (r"the lateral fraction: \ the early energy from the sides \ ($\theta$ measured from the line through the ears) \ over all the early energy", WHITE),
            (r"good halls: \ 0.15 to 0.35", GREY_A),
        ]
        rows = text_rows(items, font_size=22).move_to(DOWN * 1.2)
        head = label(r"the sides", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The reflections from the sides are special. <bookmark mark='a'/> Harold Marshall in 1967, and Michael Barron in "
            "experiments from 1971, found that they make the sound wide and enveloping, a quality they called spatial "
            "impression. <bookmark mark='b'/> A reflection from the side reaches the two ears differently, so the ears hear "
            "different sounds, and the brain hears the source broaden and the hall surround it. <bookmark mark='c'/> The "
            "measure is the lateral fraction: the early energy arriving from the sides, weighted by the cosine squared of the "
            "angle from the line through the ears, over all the early energy. <bookmark mark='d'/> Good halls lie between about "
            "nought point one five and nought point three five."
        ) as vo:
            self.play(FadeIn(head), FadeIn(eq))
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def width(self):
        d = load("halls")
        w = np.array(d["widths"], float)
        lf = np.array(d["lf"])
        ax = frame_axes(width=8.6, height=3.0, xlo=10, xhi=42, ylo=0.0, yhi=0.25, center=DOWN * 0.3 + LEFT * 0.3)
        cv = curve(w, lf, ax.to, color=TUNE, width=3)
        dots = VGroup(*[Dot(ax.to(x, y), radius=0.07, color=TUNE) for x, y in zip(w, lf)])
        xt = VGroup(*[label(f"{int(v)} m", font_size=15, color=GREY_A).next_to(ax.to(v, 0), DOWN, buff=0.12) for v in (14, 22, 30, 40)])
        yt = VGroup(*[label(f"{v:.2f}", font_size=15, color=GREY_A).next_to(ax.to(10, v), LEFT, buff=0.12) for v in (0.0, 0.1, 0.2)])
        band = Rectangle(width=8.6, height=3.0 * 0.10 / 0.25, stroke_width=0, fill_color=TUNE, fill_opacity=0.08).move_to((ax.to(10, 0.15) + ax.to(42, 0.25)) / 2)
        xl = label(r"hall width \ (length 40 m, \ height 16 m, \ the same seat)", font_size=16, color=GREY_A).next_to(xt, DOWN, buff=0.15)
        note = label(rf"lateral fraction: \ {lf[0]:.2f} at 14 m, \ {lf[-1]:.2f} at 40 m: \ the side walls move away and their reflections arrive late and faint", font_size=17, color=WHITE).to_edge(DOWN, buff=0.35)
        head = label(r"narrow halls surround you", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "So the width of a hall matters. <bookmark mark='a'/> Here is the lateral fraction at one seat as the hall is "
            f"widened from fourteen metres to forty, all else equal: from {say(lf[0], 2)} down to {say(lf[-1], 2)}. "
            "<bookmark mark='b'/> As the side walls move away, their reflections arrive later and fainter, and more of the early "
            "energy comes from the ceiling, overhead, which the two ears hear alike. The best old halls are narrow shoeboxes, "
            "and their builders did not know why."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ax), FadeIn(xt), FadeIn(yt), FadeIn(xl), FadeIn(band), FadeIn(ghost(cv, 0.3)))
            vo.wait_until("a")
            self.play(Create(cv), FadeIn(dots), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("halls")
        c = clip("halls.two")
        card = listen_card(r"Headphones on. \ A voice from the stage of two shoebox halls that ring for the same 1.9 seconds: \ "
                           r"one 18 metres wide, \ one 40. \ Which was the narrow hall?", width=10.0)
        with self.voiceover(
            "Your turn, with headphones. A voice from the stage of two shoebox halls that ring for the same time, one point nine "
            "seconds. One is eighteen metres wide, the other forty. Which was the narrow hall?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second"]).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two halls", kind="physical model", detail=r"Part 8's voice, \ simulated halls, \ headphones", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["narrow"], st["wide"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["wide"], c.duration, buff=0.08)
        res = label(rf"the first: \ lateral fraction {d['lf_pair']['narrow']:.2f} against {d['lf_pair']['wide']:.2f}; \ the voice sounds wider, \ the hall closer round you",
                    font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            "The first. Its early reflections come from the sides, strongly and soon, so the voice sounds broader and the hall "
            f"wraps round you; the lateral fraction is {say(d['lf_pair']['narrow'], 2)} against {say(d['lf_pair']['wide'], 2)}. "
            "In the wide hall the same reverberation sounds further off, as if heard through a door."
        ):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def shapes(self):
        items = [
            (r"the shoebox: \ Vienna's Musikverein \ (1870), \ Amsterdam's Concertgebouw \ (1888), \ Boston \ (1900): \ narrow, \ tall, \ ornamented", WHITE),
            (r"the fan: \ wide at the back for more seats and sight lines; \ few side reflections, \ and often disappointing", WHITE),
            (r"the vineyard: \ Berlin's Philharmonie \ (Scharoun and Cremer, \ 1963): \ the audience on terraces whose walls reflect to the sides", WHITE),
            (r"the surround: \ Hamburg's Elbphilharmonie \ (2017): \ 10,000 different gypsum panels, \ each cell shaped to scatter", WHITE),
            (r"since the 1980s, \ every major hall is first built as a computer model, \ and often as a 1:10 scale model as well", TUNE),
        ]
        rows_scene(self, r"the shapes of halls", items,
                   "Hall shapes follow from all this. <bookmark mark='b'/> The shoebox: Vienna's Musikverein of 1870, Amsterdam's "
                   "Concertgebouw of 1888, Boston's Symphony Hall: narrow, tall and ornamented, full of side reflections and "
                   "scattering. <bookmark mark='c'/> The fan: wide at the back for more seats and better sight lines, with few side "
                   "reflections, and often disappointing. <bookmark mark='d'/> The vineyard: Berlin's Philharmonie, by Hans "
                   "Scharoun with the acoustician Lothar Cremer, 1963, with the audience on terraces whose low walls reflect sound "
                   "sideways. <bookmark mark='e'/> The surround: Hamburg's Elbphilharmonie of 2017, lined with ten thousand "
                   "different gypsum panels, each cell shaped to scatter. <bookmark mark='f'/> Since the 1980s every major hall "
                   "has been built first as a computer model, and often as a model at a tenth of the size as well. How do you "
                   "simulate a hall?", marks="bcdef")
