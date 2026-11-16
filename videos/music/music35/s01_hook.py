from __future__ import annotations

import numpy as np

from videos.music.music35.common import *  # noqa: F403


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.cairo()
        self.plan()
        self.where()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.quiz")
        card = listen_card(r"C on the oud, \ with three different thirds above it: \ each alone, \ together, \ then in a short phrase. \ "
                           r"One is the piano's E, \ one its E$\flat$, \ and one lies between. \ Which is between, \ A, \ B or C?", width=10.6)
        with self.voiceover(
            "Start with your ears. An oud plays C, then a third above it, then both together, then a short phrase. Three "
            "times, with three different thirds. One is the piano's E, one is its E flat, and one lies exactly between them, "
            "a note the piano does not have. Which is the one between, A, B or C?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ruler = cents_ruler([[0, 300], [0, 400], [0, 350]], width=6.0, top=500, labels=["A", "B", "C"], colors=[GREY_A, GREY_A, GREY_A]).move_to(UP * 0.6)
        for r in ruler.rows:
            r[1][1].set_opacity(0.0)
        self.play(FadeOut(card), FadeIn(ruler))
        with self.listen(c) as snd:
            window(snd, r"A, \ B, \ C", detail=r"an oud model", corner=DL, tag_corner=DR)
            for i, k in enumerate("ABC"):
                end = d["starts"]["ABC"[i + 1]] - 0.6 if i < 2 else c.duration
                pulse(snd, ruler.rows[i][3], d["starts"][k], end, buff=0.08)
        ans = label(r"A: \ 300 cents \ (E$\flat$); \ B: \ 400 \ (E); \ C: \ 350, \ the third of maqam Rast", font_size=22, color=TUNE).to_edge(DOWN, buff=1.0)
        with self.voiceover(
            "C lies between: three hundred and fifty cents, half way from E flat to E. It is the simplified twenty-four-step third used for our Rast example, an important Arabic maqam, and it is neither major nor minor. Musicians call such notes half-flat. This part is about a music whose notes lie between the piano's keys."
        ):
            self.play(*[r[1][1].animate.set_opacity(1.0) for r in ruler.rows], FadeIn(ans))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def cairo(self):
        items = [
            (r"Cairo, \ 1932: \ the Congress of Arab Music, \ with scholars from Egypt, \ Syria, \ Iraq, \ Turkey and Europe", WHITE),
            (r"one committee's task: \ fix the Arab scale, \ perhaps as 24 equal quarter tones", WHITE),
            (r"reports of its work: \ the intervals musicians actually played did not fit a grid of equal quarter tones", WHITE),
            (r"the committee could not agree on a single standard", TUNE),
            (r"the same question as Part 34's shruti: \ theory's grid, \ or the musicians' practice?", GREY_A),
        ]
        rows_scene(self, r"a congress in Cairo", items,
                   "In 1932 a Congress of Arab Music met in Cairo, with musicians and scholars from Egypt, Syria, Iraq, Turkey "
                   "and Europe, Béla Bartók and Paul Hindemith among them. <bookmark mark='b'/> One committee was asked to fix "
                   "the Arab scale, perhaps as twenty-four equal quarter tones. <bookmark mark='c'/> By the accounts of its work, "
                   "the intervals that musicians actually played did not fit such a grid; <bookmark mark='d'/> and the committee "
                   "could not agree on a single standard. <bookmark mark='e'/> It is the same question as Part 34's shrutis: "
                   "theory's grid, or the musicians' practice?", marks="bcde")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"ajnas: \ the four-note building blocks",
            r"maqamat: \ ajnas joined, \ with paths of their own",
            r"neutral intervals, \ from al-F\=ar\=ab\=\i\ to 24 and 53 equal steps",
            r"Turkish makam in commas; \ the Persian dastgah",
            r"rhythmic cycles, \ and the taqsim",
            r"the instruments, \ and machines that measure the music",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. The ajnas, the four-note building blocks. <bookmark mark='b'/> The maqamat, built from ajnas "
            "and each with a path of its own. <bookmark mark='c'/> Neutral intervals, from a medieval treatise to twenty-four "
            "and fifty-three equal steps. <bookmark mark='d'/> Turkish makam, theorised in commas, and the Persian dastgah. "
            "<bookmark mark='e'/> Rhythmic cycles, and the improvised prelude called taqsim. <bookmark mark='f'/> The "
            "instruments, and the machines now measuring this music."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def where(self):
        items = [
            (r"the Arab world from Morocco to Iraq; \ Turkey; \ Iran and Azerbaijan; \ Central Asia", WHITE),
            (r"in mosques and churches, \ in synagogues and Sufi lodges, \ in cafes and concert halls", WHITE),
            (r"Jewish communities of the Middle East sing their liturgy in maqam", WHITE),
            (r"related systems, \ different names: \ maqam, \ makam, \ mugham, \ shashmaqam, \ dastgah", TUNE),
            (r"many languages, \ religions and centuries share one family of musical ideas", GREY_A),
        ]
        rows_scene(self, r"where maqam lives", items,
                   "Maqam is not one country's music. <bookmark mark='b'/> It lives across the Arab world from Morocco to Iraq, in Turkey, in Iran and Azerbaijan, and in Central Asia; <bookmark mark='c'/> in mosques and churches, synagogues and Sufi lodges, cafes and concert halls. <bookmark mark='d'/> The Jewish communities of the Middle East sing their liturgy in maqam. <bookmark mark='e'/> Related systems go by related names: maqam, makam, mugham, shashmaqam, dastgah. <bookmark mark='f'/> Many languages, religions and centuries share one family of musical ideas.", marks="cdef")
