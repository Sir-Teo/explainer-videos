from __future__ import annotations

import numpy as np

from videos.music.music10.common import *  # noqa: F403


def profile_curve(profile, img, width: float = 1.5, color=INK) -> VMobject:
    """The ink in every row, drawn beside the picture it was measured from."""
    p = np.asarray(profile, dtype=float)
    top, bottom, x0 = img.get_top()[1], img.get_bottom()[1], img.get_right()[0] + 0.25
    ys = np.linspace(top, bottom, len(p))
    return VMobject(color=color, stroke_width=2).set_points_as_corners([np.array([x0 + width * v / max(p.max(), 0.6), y, 0]) for v, y in zip(p, ys)])


def head_spots(img, count: int = 42, per_line: int = 14, space: int = 12, margin: int = 40, gap: int = 8, shape=(464, 596)) -> VGroup:
    """Rings where the page's note heads are (the layout of ``raster.page``)."""
    notes = [n.pitch.staff_position() for n in TUNE_SCORE.voices[0].notes][:count]
    g = VGroup()
    for k, pos in enumerate(notes):
        r, c = divmod(k, per_line)
        bottom = margin + 2 * space + r * (4 + gap) * space + 4 * space
        px = margin + space + c * 3 * space + (3 * space) // 2
        py = bottom - pos * space / 2.0
        x = img.get_left()[0] + img.width * px / shape[1]
        y = img.get_top()[1] - img.height * py / shape[0]
        g.add(Circle(radius=0.14, color=INK, stroke_width=2.5).move_to([x, y, 0]))
    return g


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 10, r"Frontier: \ reading the page back", r"Can a machine read music?", extra=((1966, r"the first music-reading programs"), (2018, r"neural readers")),
                spoken="Chapter 10. The frontier: reading the page back.")
        self.pipeline()
        self.breaks()
        self.listen_back()
        self.state()

    # ------------------------------------------------------------------
    def pipeline(self):
        d = load("omr")
        img = page_image(d["page"], 4.7).move_to(LEFT * 3.5 + DOWN * 0.2)
        prof = profile_curve(d["profile"], img)
        steps = VGroup(label(r"1 \ \ add up the ink in every row: \\ a staff is five spikes", font_size=26, color=INK),
                       label(r"2 \ \ erase the lines", font_size=26, color=GREY_A),
                       label(r"3 \ \ each blob left is a note head: \\ its height is its pitch; \\ hollow or filled, \ its length", font_size=26, color=GREY_A),
                       label(rf"{round(42 * d['clean_accuracy'])} of 42 notes read", font_size=30, color=GOOD)).arrange(DOWN, buff=0.45, aligned_edge=LEFT).move_to(RIGHT * 4.3 + DOWN * 0.1)
        spots = head_spots(img)
        back = VGroup(label(r"so far: \ music $\rightarrow$ page", font_size=30, color=GREY_A), label(r"now: \ page $\rightarrow$ music", font_size=34, color=LIMIT),
                      label(r"first programs: \ the 1960s. \\ Still an open problem.", font_size=26, color=GREY_B)).arrange(DOWN, buff=0.5).move_to(RIGHT * 4.0)
        head = label(r"optical music recognition: \ a toy", font_size=30, color=LIMIT).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Everything so far wrote music down. The frontier is the trip back: a machine that reads a "
            "page of music as a musician does. It is called optical music recognition. The first programs "
            "were written in the nineteen sixties, and the problem is still open. To see why, here is the "
            "textbook method, built into Monochord as a toy. <bookmark mark='a'/> This is a page of the "
            "Tune as a scanner sees it: pixels. Step one: add up the ink in every row. Staff lines run the "
            "whole width of the page, so each staff shows up as five spikes. <bookmark mark='b'/> Step "
            "two: erase the lines. <bookmark mark='c'/> Step three: every blob that is left is a note "
            "head. How high it sits among the lines gives its pitch, and whether it is hollow gives its "
            "length. <bookmark mark='d'/> On this clean page the toy reads all forty-two notes correctly."
        ) as vo:
            self.play(FadeIn(head), FadeIn(img), FadeIn(back))
            vo.wait_until("a")
            self.play(FadeOut(back))
            self.play(Create(prof), FadeIn(steps[0]), run_time=2.5)
            vo.wait_until("b")
            self.play(FadeIn(steps[1]))
            vo.wait_until("c")
            self.play(FadeIn(steps[2]), LaggedStart(*[FadeIn(s, scale=1.6) for s in spots], lag_ratio=0.05), run_time=3.0)
            vo.wait_until("d")
            self.play(FadeIn(steps[3]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def breaks(self):
        d = load("omr")
        img = page_image(d["tilted"], 3.6).move_to(LEFT * 4.1 + UP * 1.3)
        prof = profile_curve(d["tilted_profile"], img, width=1.1)
        cap = label(r"turned by one degree: \ no spikes, \ no staff, \ nothing read", font_size=24, color=BAD).next_to(img, DOWN, buff=0.25).shift(RIGHT * 0.5)
        g = axes([0, 2.05], [0, 1.08], x_length=5.4, y_length=2.6, xlabel=r"tilt of the page, \ degrees", ylabel=r"notes read", xticks=[0, 0.5, 1, 1.5, 2], yticks=[0, 0.5, 1], font_size=20).move_to(RIGHT * 3.4 + UP * 1.5)
        naive = curve(g.ax, np.asarray(d["angles"], dtype=float), np.asarray(d["naive"], dtype=float), BAD, stroke_width=4)
        fixed = curve(g.ax, np.asarray(d["angles"], dtype=float), np.asarray(d["deskewed"], dtype=float) - 0.012, GOOD, stroke_width=4)
        ln = label(r"as it is", font_size=22, color=BAD).next_to(g.ax.c2p(0.45, 0.25), RIGHT, buff=0.1)
        lf = label(r"straightened first", font_size=22, color=GOOD).next_to(g.ax.c2p(1.0, 0.86), DOWN, buff=0.1)
        g2 = axes([0, 0.125], [0, 1.08], x_length=5.4, y_length=1.9, xlabel=r"fraction of pixels flipped by specks", ylabel=r"notes read", xticks=[0, 0.04, 0.08, 0.12], yticks=[0, 0.5, 1], font_size=20).move_to(RIGHT * 3.4 + DOWN * 2.0)
        speck = curve(g2.ax, np.asarray(d["speck_levels"], dtype=float), np.asarray(d["speck_accuracy"], dtype=float), LIMIT, stroke_width=4)
        with self.voiceover(
            "Now turn the page by one degree, as any hand-fed scanner will. <bookmark mark='a'/> The staff "
            "lines no longer lie along the rows of pixels. The spikes smear out, the reader finds no staff, "
            "and it reads nothing at all. <bookmark mark='b'/> Here is its accuracy against the tilt. Up "
            f"to three tenths of a degree it is fine. At {say(d['breaks_at'], 1)} of a degree it reads "
            "nothing. <bookmark mark='c'/> That fault can be repaired: turn the image until its rows are "
            "as unequal as they can be, and then read. The green line. <bookmark mark='d'/> But sprinkle "
            "the page with specks, as on an old photocopy, and the accuracy falls away again. Each repair "
            "handles one kind of damage. A real page has warped paper, ink showing through from the other "
            "side, handwriting, slurs crossing stems, two voices sharing a staff, and words among the "
            "notes."
        ) as vo:
            self.play(FadeIn(img))
            vo.wait_until("a")
            self.play(Create(prof), FadeIn(cap), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(g), Create(naive), FadeIn(ln), run_time=2.0)
            vo.wait_until("c")
            self.play(Create(fixed), FadeIn(lf), run_time=1.5)
            vo.wait_until("d")
            self.play(FadeIn(g2), Create(speck), run_time=2.0)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def listen_back(self):
        d = load("omr")
        c = clip("omr.read")
        img = page_image(d["bad"], 2.9).move_to(UP * 1.9)
        card = listen_card(r"The toy has read this speckled scan of the Tune's first four phrases. \ How many mistakes do you hear?", width=9.6).move_to(DOWN * 1.6)
        with self.voiceover("Here is what the toy makes of a speckled scan of the Tune's first four phrases. Listen to what it read. How many mistakes do you hear?"):
            self.play(FadeIn(img), FadeIn(card))
        self.wait(1.0)
        rows, t = [], 0.0
        for key, b in zip(d["bad_keys"], d["bad_beats"]):
            rows.append((t, b, key))
            t += b
        roll = piano_roll(rows, width=12.0, height=2.3, lo=59, hi=70, color=PAGE).move_to(DOWN * 1.6)
        self.play(FadeOut(card), FadeIn(roll.frame), FadeIn(roll.grid))
        with self.listen(c) as snd:
            window(snd, r"the Tune, \ as the toy read it", detail=r"Part 7's piano", corner=DL, tag_corner=DR)
            for k, n in enumerate(roll.notes):
                snd.wait_until(f"n{k}")
                self.play(FadeIn(n, scale=0.7), run_time=0.2)
        wrong = [k for k, f in enumerate(d["bad_flags"]) if f]
        ans = label(rf"{len(wrong)} mistakes: \ one note that is not on the page, \ and {len(wrong) - 1} quarter notes read as half notes", font_size=26, color=BAD).next_to(roll, UP, buff=0.2)
        with self.voiceover(
            f"{say(len(wrong)).capitalize()}. <bookmark mark='a'/> One note that is not on the page at all: a "
            f"cluster of specks that looked like a note head. And {say(len(wrong) - 1)} quarter notes read "
            "as half notes, because specks had fallen inside them and the reader took the filled heads "
            "for hollow ones, or the other way about. You heard every one of them at once. Your ear "
            "knows the Tune; the toy knows only blobs."
        ) as vo:
            vo.wait_until("a")
            self.play(*[roll.notes[k].animate.set_fill(BAD) for k in wrong], FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def state(self):
        head = label(r"Where it stands", font_size=38, color=LIMIT).to_edge(UP, buff=0.4)
        rows = rows_card([
            (r"what works", r"since about 2018, \ networks trained from end to end read a clean, \\ printed, \ single line of music with very few errors."),
            (r"what does not, \ yet", r"dense orchestral pages, \ handwriting, \ and the older notations of this part. \\ There is not even an agreed way to count a reader's mistakes."),
            (r"the encodings", r"MusicXML 4 (2021), \ MEI 5 (2023), \ a successor called MNX in draft; \\ and one standard, \ SMuFL, \ for where every symbol lives in a font."),
            (r"editions as data", r"not one text chosen by an editor, \ but every source and every variant, \\ encoded, \ so that a reader can ask what each manuscript says."),
        ], left=-6.5, text_left=-2.9, top=1.9, step=1.42, name_size=26, text_size=23, color=LIMIT)
        self.play(FadeIn(head), run_time=0.5)
        with self.voiceover(
            "Real systems are far better than the toy. <bookmark mark='a'/> Since about 2018, neural "
            "networks trained from end to end have learned to read a clean, printed, single line of music "
            "with very few errors. <bookmark mark='b'/> What is not solved is everything harder: a dense "
            "orchestral page, handwriting, and the older notations we met in this part. The field does not "
            "even agree yet on how to score a reader. What counts as one mistake, on a page where a wrong "
            "clef makes every note wrong? <bookmark mark='c'/> The encodings are still moving as well. "
            "MusicXML reached its fourth version in 2021 and MEI its fifth in 2023; a successor to "
            "MusicXML is being drafted; and a standard called SMuFL now fixes where every musical symbol "
            "lives in a font. <bookmark mark='d'/> And scholars are using these formats to make a new kind "
            "of edition: not one text chosen by an editor, but every source and every variant, encoded, so "
            "that a reader can ask what each manuscript says. The tablet from Ugarit was written for "
            "people who shared its writer's knowledge. Every one of these standards is an attempt to write "
            "that knowledge down too, so that a reader three thousand years from now needs only the file."
        ) as vo:
            for mark, r in zip("abcd", rows):
                vo.wait_until(mark)
                self.play(FadeIn(r), run_time=0.6)
        self.wait(0.3)
        self.clear_scene()
