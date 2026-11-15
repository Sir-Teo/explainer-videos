from __future__ import annotations

from videos.music.music60.common import *  # noqa: F403


class Charts(SoundScene):
    def construct(self):
        chapter(self, 7, r"Charts and attention", r"How does the way plays are counted change the music?")
        self.history()
        self.intro()
        self.attention()

    # ------------------------------------------------------------------
    def history(self):
        items = [
            (r"1958: \ Billboard's Hot 100, \ from sales reported by shops and plays reported by radio stations", WHITE),
            (r"1991: \ SoundScan counts sales at the till; \ overnight, \ country and hip-hop rise up the charts", WHITE),
            (r"2012 and 2013: \ on-demand streams, \ then YouTube views, \ join the Hot 100; \ 2014: \ albums counted in equivalent units", WHITE),
            (r"what is counted is rewarded, \ and what is rewarded is made", WHITE),
            (r"Goodhart's law, \ in music: \ a measure that becomes a target changes what it measured", TUNE),
        ]
        rows_scene(self, r"how the charts count", items,
                   "Charts are measurements, and measurement changes music. <bookmark mark='b'/> Billboard's Hot 100 began in 1958, "
                   "built from sales reported by shops and plays reported by radio stations. <bookmark mark='c'/> In 1991 SoundScan "
                   "began counting sales at the till, and overnight country and hip-hop rose up the charts: they had been selling "
                   "all along. <bookmark mark='d'/> In 2012 and 2013 on-demand streams and then YouTube views joined the Hot 100, and "
                   "from 2014 albums were counted in equivalent units. <bookmark mark='e'/> What is counted is rewarded, and what is "
                   "rewarded is made. <bookmark mark='f'/> Goodhart's law, in music: a measure that becomes a target changes what it "
                   "measured.", marks="bcdef")

    # ------------------------------------------------------------------
    def intro(self):
        d = load("intro")
        c = clip("intro.two")
        boxes = choice_boxes([rf"a {d['intro_s']:.0f}-second introduction", r"the voice at once"], width=4.0, height=0.9, buff=0.9, size=20).move_to(UP * 0.5)
        note = VGroup(label(r"a stream pays only after 30 seconds, \ and a quarter of plays are skipped within five \ (Lamere, \ 2014)", font_size=18, color=WHITE),
                      label(r"hits' introductions shrank from about 20 seconds in the mid-1980s to about 5 by 2015 \ (Léveillé Gauvin, \ 2018)", font_size=18, color=TUNE)).arrange(DOWN, buff=0.3).next_to(boxes, DOWN, buff=0.6)
        head = label(r"the first seconds", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover("Hear the same song opened two ways: after a long instrumental introduction, and with the voice from the first beat."):
            self.play(FadeIn(head), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"long, \ then short", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["long"], st["short"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["short"], c.duration, buff=0.08)
        with self.voiceover(
            "On a service the first seconds decide everything. A stream pays only after thirty seconds, and in 2014 Paul Lamere "
            "found that about a quarter of plays were skipped within five. <bookmark mark='a'/> Hugues Léveillé Gauvin measured "
            "hits' introductions: about twenty seconds in the mid-1980s, about five by 2015."
        ) as vo:
            self.play(FadeIn(note[0]))
            vo.wait_until("a")
            self.play(FadeIn(note[1]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def attention(self):
        items = [
            (r"paying per stream, \ whatever its length, \ rewards shorter tracks and more of them", WHITE),
            (r"playlists became the new radio: \ a place on a large one can make a career", WHITE),
            (r"background listening: \ `chill' and `sleep' playlists, \ and tracks made to fill them", WHITE),
            (r"short-video platforms: \ a song's fifteen seconds can matter more than the song", WHITE),
            (r"every format shaped music: \ the 78's three minutes, \ the LP's forty, \ radio's single, \ the stream's thirty seconds", TUNE),
        ]
        rows_scene(self, r"the attention economy", items,
                   "And the rest of the system leans the same way. <bookmark mark='b'/> Paying per stream, whatever its length, "
                   "rewards shorter tracks and more of them. <bookmark mark='c'/> Playlists became the new radio: a place on a large "
                   "one can make a career. <bookmark mark='d'/> Background listening grew, chill and sleep playlists, and tracks "
                   "made to fill them. <bookmark mark='e'/> On short-video platforms, a song's fifteen seconds can matter more "
                   "than the song. <bookmark mark='f'/> It was always so: the seventy-eight's three minutes, the LP's forty, radio's "
                   "single, and now the stream's thirty seconds all shaped the music made for them.", marks="bcdef")
