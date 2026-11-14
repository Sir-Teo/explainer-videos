from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403


class Turkish(SoundScene):
    def construct(self):
        chapter(self, 5, r"Turkish makam in commas", r"Why fifty-three?")
        self.aeu()
        self.quiz()
        self.debate()
        self.accidentals()
        self.ottoman()

    # ------------------------------------------------------------------
    def aeu(self):
        d = load("turkish")
        tr = d["turkish"]
        steps = tr["steps"]
        names = ["Rast", "D\\\"ugah", "Segah", "\\c{C}argah", "Neva", "H\\\"useyni", "Evi\\c{c}", "Gerdaniye"]
        boxes = VGroup()
        x = -5.5
        for i, st in enumerate(steps):
            w = 11.0 * st / 53
            boxes.add(VGroup(Rectangle(width=w - 0.04, height=0.5, stroke_width=0, fill_color=TUNE if st == 9 else (BLUE if st == 8 else EAR), fill_opacity=0.85).move_to([x + w / 2, 0.6, 0]),
                             label(str(st), font_size=18, color=BLACK).move_to([x + w / 2, 0.6, 0])))
            x += w
        nm = VGroup(*[label(n, font_size=15, color=GREY_A).move_to([-5.5 + 11.0 * c / 53, 1.15, 0]) for n, c in zip(names, tr["commas"])])
        rows_ = VGroup(*[label(s, font_size=21, color=c_) for s, c_ in (
            (r"Arel--Ezgi--Uzdilek \ (early 20th century): \ the octave as 53 Holdrian commas of 22.6 cents", WHITE),
            (r"a whole tone is 9 commas; \ intervals of 1, \ 4, \ 5, \ 8 and 9 commas have names", WHITE),
            (rf"Rast: \ 9, \ 8, \ 5, \ 9, \ 9, \ 8, \ 5 commas: \ Segah at {d['third']['turkish']:.0f} cents, \ near the pure 5:4", TUNE))]).arrange(DOWN, buff=0.3).to_edge(DOWN, buff=0.6)
        head = label(r"Turkish Rast, \ in commas", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Turkish theory went another way. <bookmark mark='a'/> In the early twentieth century the theorists Arel, Ezgi "
            "and Uzdilek divided the octave into fifty-three commas, each about twenty-two and a half cents, a nearly "
            "Pythagorean system. <bookmark mark='b'/> A whole tone is nine commas, and intervals of one, four, five, eight and "
            "nine commas each have names. <bookmark mark='c'/> Turkish Rast steps nine, eight, five, nine, nine, eight, five. "
            f"Its third note, segah, is seventeen commas up, {say(round(d['third']['turkish']))} cents: not three hundred and fifty "
            "like the Arabic E half-flat, but close to a pure major third."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(nm))
            for mark, r in zip("abc", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("turkish")
        c = clip("turkish.quiz")
        card = listen_card(r"The lower half of Rast, \ twice, \ then its tonic, \ third and fifth together. \ "
                           r"One uses the Arabic third, \ 350 cents; \ the other the Turkish, \ 385. \ Which third is higher, \ A or B?", width=10.4)
        with self.voiceover(
            "A question for your ears. The lower half of Rast, up and down, and then its tonic, third and fifth sounded "
            "together, twice. One uses the Arabic third of three hundred and fifty cents; the other the Turkish segah of three "
            "hundred and eighty-five. Which third is higher, A or B?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ruler = cents_ruler([d["arabic"][:5], d["turkish"]["cents"][:5]], width=7.0, top=750, labels=["A", "B"], colors=[GREY_A, GREY_A]).move_to(UP * 0.4)
        self.play(FadeOut(card), FadeIn(ruler))
        with self.listen(c) as snd:
            window(snd, r"A, \ then B", detail=r"an oud model", corner=DL, tag_corner=DR)
            pulse(snd, ruler.rows[0][3], d["starts"]["A"], d["starts"]["B"] - 0.6, buff=0.08)
            pulse(snd, ruler.rows[1][3], d["starts"]["B"], c.duration, buff=0.08)
        ans = label(r"B: \ the Turkish segah, \ 385 cents; \ A: \ the Arabic E half-flat, \ 350", font_size=22, color=TUNE).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "B is higher: the Turkish segah. Thirty-five cents is a third of a semitone, and with the tonic and fifth sounding "
            "the difference is plain: A has the neutral colour, B sounds almost like a major chord. The two traditions share "
            "names, Rast and segah among them, but not always the same pitches."
        ):
            self.play(FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def debate(self):
        items = [
            (r"Turkish musicians often play differently from the 53-comma theory", WHITE),
            (r"Bozkurt, \ Yarman and others measured recordings: \ some theory pitches are off by several commas", WHITE),
            (r"alternatives: \ Yarman's 79-tone system, \ or simply measured pitch distributions", WHITE),
            (r"the theory came from a desire for system; \ the practice from an oral tradition", TUNE),
            (r"the same tension as Cairo, \ argued in commas", GREY_A),
        ]
        rows_scene(self, r"theory against practice", items,
                   "Here too theory and practice part. <bookmark mark='b'/> Turkish musicians often play differently from the "
                   "fifty-three-comma theory, <bookmark mark='c'/> and Barış Bozkurt, Ozan Yarman and others, measuring "
                   "recordings, found some theoretical pitches several commas away from what performers play. "
                   "<bookmark mark='d'/> Alternatives have been proposed, such as Yarman's seventy-nine-tone system, or simply describing the "
                   "measured distributions. <bookmark mark='e'/> The theory grew from a desire for system; the practice from an "
                   "oral tradition. <bookmark mark='f'/> It is Cairo's question again, argued in commas.", marks="cdef")

    # ------------------------------------------------------------------
    def ottoman(self):
        items = [
            (r"Ottoman court music: \ composers, \ treatises, \ a large repertory of vocal and instrumental forms", WHITE),
            (r"Dimitrie Cantemir \ (about 1700): \ a notation system and hundreds of pieces written down", WHITE),
            (r"the Mevlevi order's ceremony: \ the ney and the whirling dance", WHITE),
            (r"much was transmitted orally until the 20th century's notations", TUNE),
            (r"the same tension again: \ written theory, \ oral practice", GREY_A),
        ]
        rows_scene(self, r"Ottoman music", items,
                   "Turkish theory grew from a long court tradition. <bookmark mark='b'/> Ottoman court music had its composers, treatises and a large repertory of vocal and instrumental forms. <bookmark mark='c'/> Around 1700 the Moldavian prince Dimitrie Cantemir devised a notation and wrote down hundreds of pieces. <bookmark mark='d'/> The Mevlevi order's ceremony joined the ney with the whirling dance. <bookmark mark='e'/> Much was passed on orally until the notations of the twentieth century: <bookmark mark='f'/> the same tension again, written theory and oral practice.", marks="cdef")

    # ------------------------------------------------------------------
    def accidentals(self):
        items = [
            (r"Turkish notation uses special accidentals for 1, \ 4, \ 5 and 8 commas", WHITE),
            (r"a flat of one comma, \ a sharp of four: \ the page shows the theory's pitches", WHITE),
            (r"teachers say the signs are reminders, \ not instructions to tune exactly", WHITE),
            (r"notation as memory, \ again: \ Parts 10 and 34", TUNE),
            (r"the debate is partly about what notation is for", GREY_A),
        ]
        rows_scene(self, r"writing commas down", items,
                   "The commas reach the page. <bookmark mark='b'/> Turkish notation has special accidentals for one, four, five and eight commas, <bookmark mark='c'/> so a score shows the theory's pitches. <bookmark mark='d'/> Teachers say the signs are reminders, not instructions to tune exactly. <bookmark mark='e'/> It is notation as memory again, as in Parts 10 and 34, <bookmark mark='f'/> and the debate is partly about what notation is for.", marks="cdef")
