from __future__ import annotations

import numpy as np

from videos.psychology.psych10.common import *  # noqa: F403


class Light(VoiceoverScene):
    def construct(self):
        self.card()
        self.eye()
        self.prc()
        self.jetlag()

    def card(self):
        card = chapter_card(2, r"Light sets the clock", r"What moves it, and which way?", lit=(), part=PART,
                            scale=("neuron", "brain", "person"), marr=("what", "how"))
        with self.voiceover(
            "Chapter two. Light sets the clock."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def eye(self):
        head = heading(r"How light reaches the clock")
        ch = chain([r"light", r"the retina: \ a third kind of light-sensitive cell", r"the clock",
                    r"the pineal gland: \ melatonin, by night"], [LIGHTC, LIGHTC, CLOCKC, SLEEPC], width=13.0, font_size=27,
                   height=1.5).move_to([0, 1.55, 0])
        rows = rows_of([
            (r"not the rods and cones we see with: \ a few of the retina's output cells carry a pigment of their own, \ "
             r"most sensitive to blue light", LIGHTC),
            (r"they make no pictures: \ they report how bright the world is, \ and their fibres run straight to the clock",
             WHITE),
            (r"melatonin: \ released in darkness, \ shut off by light at the eye: \ the body's signal for night", SLEEPC),
            (r"so light in the evening does two things: \ it shuts off the night signal, \ and it moves the clock", THRESH),
        ], 12.6, 29, 0.26).move_to([0, -1.45, 0])
        tag = note(r"a diagram").to_corner(DR, buff=0.3)
        with self.voiceover(
            "How does light reach the clock? <bookmark mark='a'/> Not through the cells you see with. The "
            "retina has rods and cones, which Part 13 will take apart. Around the year 2000 a third kind "
            "of light-sensitive cell turned up there: a small number of the retina's output cells, which "
            "carry a pigment of their own, most sensitive to blue light. <bookmark mark='b'/> They don't "
            "make pictures. They report how bright the world is, and their fibres run straight to the "
            "clock. <bookmark mark='c'/> The clock passes the news on. One of its outputs reaches the "
            "pineal gland, which releases the hormone melatonin during the night, and stops when light "
            "hits the eye. Melatonin is the body's signal that it's dark. <bookmark mark='d'/> So light in "
            "the evening does two things. It shuts off the night signal. And, as we'll now see, it moves "
            "the clock."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(ch.boxes[0]))
            vo.wait_until("a")
            self.play(FadeIn(ch.arrows[0]), FadeIn(ch.boxes[1]), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(ch.arrows[1]), FadeIn(ch.boxes[2]), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(ch.arrows[2]), FadeIn(ch.boxes[3]), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def prc(self):
        d = load("light")
        c = load("clock")
        head = heading(r"The same light, \ opposite effects")
        A = axes([-12, 12], [-1.5, 1.2], x_length=7.6, y_length=4.4, xticks=[-12, -8, -4, 0, 4, 8, 12], yticks=[-1, 0, 1],
                 xfmt=lambda v: f"{v:+.0f}" if v else "0", yfmt=lambda v: f"{v:+.0f}" if v else "0",
                 xlabel=r"when the light falls: \ hours from the clock's low point", ylabel=r"", center=[-3.0, -0.35, 0])
        ax = A.ax
        zero = Line(ax.c2p(-12, 0), ax.c2p(12, 0), color=GREY_C, stroke_width=2)
        mid = DashedLine(ax.c2p(0, -1.5), ax.c2p(0, 1.2), color=WHITE, stroke_width=2)
        order = np.argsort(d["prc_h"])
        h, s = d["prc_h"][order], d["prc_shift"][order]
        line = curve(ax, h, s, CLOCKC, stroke_width=4.5)
        ylab_up = label(r"the clock moves earlier", font_size=25, color=MODEL).move_to(ax.c2p(-7.2, 0.8))
        ylab_dn = label(r"the clock moves later", font_size=25, color=OPP).move_to(ax.c2p(6.6, -1.2))
        low = label(rf"low point, \ about {clock_time(c['home_minimum'])}", font_size=24, color=WHITE)
        low.next_to(ax.c2p(0, 1.2), UP, buff=0.08).shift(LEFT * 1.6)
        pd = Dot(ax.c2p(d["delay_at"], d["max_delay"]), radius=0.1, color=OPP)
        pa = Dot(ax.c2p(d["advance_at"], d["max_advance"]), radius=0.1, color=MODEL)
        pdl = label(rf"${d['max_delay']:+.1f}$ h", font_size=28, color=OPP).next_to(pd, LEFT, buff=0.15)
        pal = label(rf"${d['max_advance']:+.1f}$ h", font_size=28, color=MODEL).next_to(pa, UP, buff=0.12)
        rows = rows_of([
            (r"the experiment: \ three hours of bright light, \ at one time of the clock's day; \ how far has the rhythm "
             r"moved?", WHITE),
            (rf"before the low point, \ evening and early night: \ later, \ by up to ${abs(d['max_delay']):.1f}$ hours", OPP),
            (rf"after it, \ the early morning: \ earlier, \ by up to ${d['max_advance']:.1f}$ hours", MODEL),
            (r"the clock loses ten minutes a day; \ morning light makes it up. \ That is what locking on means", THRESH),
        ], 4.7, 28, 0.26).move_to([4.55, -0.25, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: Psyche's clock; \ a phase response curve")
        with self.voiceover(
            "Here's the experiment, on Psyche's clock. Keep it in the dark. Give it three hours of bright "
            "light at one time of its day, and measure how far its rhythm has moved. Then repeat, at every "
            "other time. <bookmark mark='a'/> The curve that comes out is called a phase response curve, "
            "and it has two halves. <bookmark mark='b'/> Light that falls before the low point, in the "
            f"evening and the first part of the night, moves the clock later: by up to "
            f"{abs(d['max_delay']):.1f} hours. <bookmark mark='c'/> Light after the low point, in the "
            f"early morning, moves it earlier: by up to {d['max_advance']:.1f}. The same light, opposite "
            "effects, and the changeover comes in the small hours. Experiments on people give a curve of "
            "this shape. <bookmark mark='d'/> Now put two facts together. The clock runs slow, by ten "
            "minutes or so a day. Morning light pulls it earlier. So every ordinary morning, daylight "
            "makes up the difference, and that's what locking on means. And every evening spent under "
            "bright lamps, or in front of a bright screen, pushes the other way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(zero), FadeIn(mid), FadeIn(low), FadeIn(rows[0]))
            vo.wait_until("a")
            self.play(Create(line), run_time=3.0)
            vo.wait_until("b")
            self.play(FadeIn(pd, scale=1.5), FadeIn(pdl), FadeIn(ylab_dn), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(pa, scale=1.5), FadeIn(pal), FadeIn(ylab_up), FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()

    def jetlag(self):
        d = load("light")
        e6, w6, w9 = d["east_6_days"], d["west_6_days"], d["west_9_days"]
        head = heading(r"Fly somewhere, \ and the clock stays behind")
        A = axes([0, 11], [0, 10], x_length=7.0, y_length=4.5, xticks=[0, 2, 4, 6, 8, 10], yticks=[0, 3, 6, 9],
                 xlabel=r"days after landing", ylabel=r"hours wrong", center=[-3.0, -0.4, 0])
        ax = A.ax
        days = np.arange(12)
        cols = {3: GREY_A, 6: CLOCKC, 9: LIGHTC}
        lines = VGroup()
        for z in (3, 6, 9):
            east = curve(ax, days, np.abs(d[f"east_{z}_off"]), cols[z], stroke_width=4)
            west = DashedVMobject(curve(ax, days, np.abs(d[f"west_{z}_off"]), cols[z], stroke_width=4), num_dashes=28)
            lab = label(rf"{z} time zones", font_size=26, color=cols[z])
            lines.add(VGroup(east, west, lab))
        VGroup(*[ln[2] for ln in lines[::-1]]).arrange(DOWN, aligned_edge=LEFT, buff=0.14).move_to(ax.c2p(8.6, 5.6))
        lg = label(r"solid: flying east; \ \ dashed: flying west", font_size=25, color=GREY_A).move_to(ax.c2p(6.6, 9.4))
        rows = rows_of([
            (r"the sun, \ the lamps and the meals jump at once; \ the clock is where you left it", WHITE),
            (rf"light drags it across: \ six zones take {e6:.0f} to {w6:.0f} days, \ nine take up to {w9:.0f}", CLOCKC),
            (r"caution: \ here east comes out easier; \ travellers report the opposite. \ Take the timescale from the "
             r"model, \ not the direction", BAD),
            (r"three night shifts a week: \ eight time zones out on Monday, \ and back on Thursday", THRESH),
        ], 5.0, 28, 0.26).move_to([4.4, -0.3, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: Psyche's clock; \ lights on from 7:00 to 23:00, local time")
        with self.voiceover(
            "And now fly somewhere. <bookmark mark='a'/> Cross six time zones, and the sun, the lamps and "
            "the meal times all jump six hours at once. The clock doesn't. It's where you left it, and "
            "light has to drag it across, an hour or so a day. <bookmark mark='b'/> In the model, six "
            f"zones take {e6:.0f} to {w6:.0f} days, and nine zones take up to {w9:.0f}. For those days the "
            "clock calls for sleep in the afternoon, and for breakfast at midnight. That's jet lag. "
            "Nothing is wrong with you except the time. <bookmark mark='c'/> One caution. In this model, "
            "flying east comes out easier than flying west. Most travellers report the opposite. The "
            "answer depends on exactly when the traveller sees light, before the low point or after it, "
            "and the model's traveller keeps a fixed schedule that real ones don't. So take the timescale "
            "from the model, days and not hours, and don't take the direction. <bookmark mark='d'/> And "
            "think what this means for someone who works nights three days a week. They cross eight time "
            "zones on Monday, and come back on Thursday, every week, without leaving town."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), FadeIn(lg))
            vo.wait_until("a")
            self.play(Create(lines[1][0]), Create(lines[1][1]), FadeIn(lines[1][2]), FadeIn(rows[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(*[Create(lines[k][j]) for k in (0, 2) for j in (0, 1)], FadeIn(lines[0][2]), FadeIn(lines[2][2]),
                      FadeIn(rows[1]), run_time=2.5)
            vo.wait_until("c")
            self.play(FadeIn(rows[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows[3], shift=UP * 0.1))
        self.clear_scene()
