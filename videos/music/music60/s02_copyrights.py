from __future__ import annotations

from videos.music.music60.common import *  # noqa: F403


class Copyrights(SoundScene):
    def construct(self):
        chapter(self, 1, r"Two copyrights", r"When you play a recording, \ how many works are you hearing?")
        self.two()
        self.heard()
        self.terms()
        self.tune()
        self.machines()

    # ------------------------------------------------------------------
    def two(self):
        def box(title, lines, col, x):
            r = RoundedRectangle(width=5.4, height=3.2, corner_radius=0.15, stroke_color=col, stroke_width=3).move_to([x, -0.3, 0])
            t = label(title, font_size=24, color=col).next_to(r.get_top(), DOWN, buff=0.25)
            body = VGroup(*[label(s, font_size=17, color=WHITE) for s in lines]).arrange(DOWN, buff=0.2, aligned_edge=LEFT).next_to(t, DOWN, buff=0.3)
            return VGroup(r, t, body)
        comp = box(r"\textcopyright \ the composition", [r"the notes and the words", r"owned by songwriters and publishers",
                                                       r"lasts the writer's life plus 70 years", r"(US, EU, UK)"], TUNE, -3.0)
        rec = box(r"\textcircled{\scriptsize P} \ the sound recording", [r"this performance, \ fixed", r"owned by the label, \ or the artist",
                                                                  r"EU and UK: \ 70 years from release", r"US: \ federal only since 1972"], BLUE, 3.0)
        rights = label(r"each gives the right to copy, \ distribute, \ perform in public and adapt, \ and to license others to", font_size=18, color=GREY_A).to_edge(DOWN, buff=0.4)
        head = label(r"one song, \ two works", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "A recorded song can involve two distinct rights layers, composition and recording; their ownership may overlap or be split. <bookmark mark='a'/> The composition: the notes and the words, owned by the songwriters and their publishers, and often protected for life plus seventy years in these jurisdictions, with important exceptions for older works, corporate authorship and national rules. Its mark is the c in a circle. <bookmark mark='b'/> And the sound recording: this performance, fixed, owned by the label or the artist. In Europe and Britain it lasts seventy years from release; in America, recordings had no federal copyright at all until 1972. Its mark is the p in a circle, for phonogram. <bookmark mark='c'/> The precise bundle differs by jurisdiction and rights layer; US sound-recording public-performance rights are narrower than composition rights, and to license others to do so. Every payment in this part is for one of those permissions."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(comp))
            vo.wait_until("b")
            self.play(FadeIn(rec))
            vo.wait_until("c")
            self.play(FadeIn(rights))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def heard(self):
        d = load("rights")
        c = clip("rights.two")
        boxes = choice_boxes([r"our session's recording", r"a piano cover"], width=3.8, height=0.9, buff=1.0, size=20).move_to(UP * 0.5)
        note = VGroup(label(r"one composition \ (the Tune: \ public domain)", font_size=19, color=TUNE),
                      label(r"two sound recordings, \ two owners", font_size=19, color=BLUE)).arrange(DOWN, buff=0.25).next_to(boxes, DOWN, buff=0.6)
        head = label(r"one composition, \ two recordings", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the difference. Our session's recording of the Tune, then a pianist's cover of the same composition."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"recording, \ then cover", kind="physical model", detail=r"Part 56's session, \ Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["recording"], st["cover"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["cover"], c.duration, buff=0.08)
        with self.voiceover(
            "One composition, two sound recordings with two owners. US compulsory mechanical licensing can permit qualifying audio covers after authorized release, subject to notice, payment and arrangement restrictions; it does not automatically cover video or all territories; nobody may copy the recording itself without its owner's permission."
        ):
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def terms(self):
        items = [
            (r"1710: \ the Statute of Anne protects books; \ 1777: \ J. C. Bach wins a case that brings printed music under it", WHITE),
            (r"US: \ musical compositions protected from 1831, \ their public performance from 1897", WHITE),
            (r"sound recordings: \ the UK from 1911; \ the US federally only from 15 February 1972", WHITE),
            (r"US recordings made before 1972: \ brought in by the Music Modernization Act \ (2018), \ all free by 2067", WHITE),
            (r"terms are national; \ a work can be free in one country and owned in the next", TUNE),
        ]
        rows_scene(self, r"how long, \ and where", items,
                   "These rights are younger than the music. <bookmark mark='b'/> Britain's Statute of Anne protected books from "
                   "1710; in 1777 Johann Christian Bach won a case that brought printed music under it. <bookmark mark='c'/> America "
                   "protected musical compositions from 1831, and their public performance from 1897. <bookmark mark='d'/> Sound "
                   "recordings came later: Britain from 1911, the United States, federally, only from the fifteenth of February "
                   "1972. <bookmark mark='e'/> Older American recordings were brought in by the Music Modernization Act of 2018, on "
                   "a schedule that frees them all by 2067. <bookmark mark='f'/> And terms are national: a work can be free in one "
                   "country and owned in the next.", marks="bcdef")

    # ------------------------------------------------------------------
    def tune(self):
        items = [
            (r"the Tune: \ a French song, \ first printed in 1761, \ composer unknown: \ generally public domain in the jurisdictions discussed here; editions, arrangements and recordings must be considered separately", TUNE),
            (r"Mozart's twelve variations on it \ (K. 265, \ about 1781): \ public domain", WHITE),
            (r"Jane Taylor's `Twinkle, \ Twinkle, \ Little Star' \ (1806): \ public domain", WHITE),
            (r"but a new arrangement, \ and every new recording, \ is a new work, \ with a new owner", WHITE),
            (r"`Happy Birthday': \ its melody printed in 1893; \ royalties collected on it until a US court found the claim invalid in 2015", EAR),
        ]
        rows_scene(self, r"the Tune's own rights", items,
                   "And the Tune? <bookmark mark='b'/> A French song first printed in 1761, its composer unknown: generally public domain in the jurisdictions discussed here; editions, arrangements and recordings must be considered separately. <bookmark mark='c'/> Mozart's twelve variations on it, from about 1781: public domain. <bookmark mark='d'/> Jane Taylor's words, Twinkle, twinkle, little star, from 1806: public domain. <bookmark mark='e'/> But a new arrangement of it, and every new recording, is a new work with a new owner, including the session you have heard all series. <bookmark mark='f'/> Ownership can also be claimed wrongly: Happy Birthday's melody was printed in 1893, and a publisher collected royalties on the song until a court in California found its claim invalid in 2015.", marks="bcdef")

    # ------------------------------------------------------------------
    def machines(self):
        items = [
            (r"1908: \ a piano roll is not a copy, \ says the US Supreme Court; \ 1909: \ Congress creates the mechanical licence, \ 2 cents a copy", WHITE),
            (r"1914: \ ASCAP, \ to license public performance; \ the 1920s: \ radio, \ and the fights over what it should pay", WHITE),
            (r"the 1980s: \ the sampler; \ 1991: \ the first court to rule sampling without a licence an infringement", WHITE),
            (r"1999: \ Napster; \ the file breaks the album, \ then streaming replaces the file", WHITE),
            (r"the 2020s: \ models trained on recordings: \ the arrangement now being written", TUNE),
        ]
        rows_scene(self, r"each machine broke the last arrangement", items,
                   "And every new machine broke the arrangement before it. <bookmark mark='b'/> In 1908 the Supreme Court ruled "
                   "that a piano roll was not a copy of the song it played; the next year Congress created the mechanical licence, at "
                   "two cents a copy, a rate that stood until 1978. <bookmark mark='c'/> In 1914 composers formed ASCAP to license "
                   "public performance, and then radio arrived and fought over what it should pay. <bookmark mark='d'/> In the "
                   "1980s, the sampler; in 1991 a prominent US sampling infringement decision, not the first possible application of copyright to sampling. "
                   "<bookmark mark='e'/> In 1999, Napster: the file broke the album, and streaming later replaced the file. "
                   "<bookmark mark='f'/> And now, models trained on recordings: the arrangement still being written.", marks="bcdef")
