from __future__ import annotations

from videos.music.music60.common import *  # noqa: F403


def melody_roll(pitches, width=10.0, height=1.5, hot=8, color=TUNE, cold=GREY_B):
    """A generated melody (semitones above the tonic, plain rhythm) as a roll; its first ``hot`` notes in ``color``."""
    beats = [2.0 if (i + 1) % 8 == 0 else 1.0 for i in range(len(pitches))]
    t, notes = 0.0, []
    for p, b in zip(pitches, beats):
        notes.append([60 + p, t, b])
        t += b
    g = mroll(notes, width=width, height=height, lo=60 + min(pitches) - 2, hi=60 + max(pitches) + 2, color=color, total=t)
    for k, n in enumerate(g.notes):
        if k >= hot:
            n.set_fill(cold)
    return g


class Hook(SoundScene):
    def construct(self):
        self.quiz()
        self.reveal()
        self.story()
        self.plan()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("hook")
        c = clip("hook.two")
        card = listen_card(r"Two melodies. \ They open with the same eight notes. \ Did one composer copy the other, \ or could it be chance?", width=10.0)
        with self.voiceover(
            "This part follows one stream's fraction of a cent from a phone to a songwriter. First, a case for your ears and for a jury. Two melodies. They open with the same eight notes. Did one composer copy "
            "the other, or could it be chance?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        ra = melody_roll(d["a"]).move_to(UP * 1.3)
        rb = melody_roll(d["b"], color=BLUE).move_to(DOWN * 1.0)
        la = label(r"first", font_size=18, color=TUNE).next_to(ra, LEFT, buff=0.3)
        lb = label(r"second", font_size=18, color=BLUE).next_to(rb, LEFT, buff=0.3)
        self.play(FadeOut(card), FadeIn(ra), FadeIn(rb), FadeIn(la), FadeIn(lb))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"two melodies", kind="physical model", detail=r"Part 14's model, \ Part 38's piano", corner=DL, tag_corner=DR)
            pulse(snd, VGroup(ra, la), st["first"], st["second"] - 0.4, buff=0.12)
            pulse(snd, VGroup(rb, lb), st["second"], c.duration, buff=0.12)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def reveal(self):
        d = load("hook")
        m = load("melodies")
        lines = VGroup(
            label(r"neither copied: \ both were drawn, \ independently, \ from Part 14's model of folk melody", font_size=24, color=TUNE),
            label(rf"we drew melodies until two shared an eight-note opening: \ it took {d['tried']}", font_size=22, color=WHITE),
            label(rf"the model makes about {m['effective']['8']:,.0f} effectively different eight-note openings, \ not {m['alphabet']}$^8 \approx 2.6 \times 10^{{10}}$", font_size=22, color=WHITE),
            label(r"and courts have decided cases like this one, \ for millions of dollars, \ in both directions", font_size=22, color=EAR),
        ).arrange(DOWN, buff=0.45)
        head = label(r"chance", font_size=30, color=GREY_A).to_edge(UP, buff=0.5)
        with self.voiceover(
            "Chance. <bookmark mark='a'/> Neither copied the other: both were drawn, independently, from Part 14's model of folk "
            f"melody. <bookmark mark='b'/> We drew melodies until two shared an eight-note opening, and it took only "
            f"{say(d['tried'])}. <bookmark mark='c'/> Melodies are not spread evenly over everything twelve notes could do; they "
            "crowd into steps, the tonic and the scale, and our model makes only about fifty thousand effectively different "
            "eight-note openings. <bookmark mark='d'/> And courts have decided cases like this one, for millions of dollars, in "
            "both directions. Chapter 9 counts the melodies."
        ) as vo:
            self.play(FadeIn(head))
            for mark, ln in zip("abcd", lines):
                vo.wait_until(mark)
                self.play(FadeIn(ln))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def story(self):
        items = [
            (r"follow one stream's fraction of a cent from a phone to a songwriter", WHITE),
            (r"on the way it passes two copyrights, \ four kinds of licence, \ and half a dozen intermediaries", WHITE),
            (r"each arrangement made when a new machine broke the last: \ the piano roll, \ radio, \ the sampler, \ the file, \ the model", WHITE),
            (r"everything here is dated, \ mostly American, \ on illustrative terms, \ and not legal or financial advice", GREY_A),
            (r"the arithmetic, \ though, \ is general: \ shares, \ pools, \ power laws and the odds of coincidence", TUNE),
        ]
        rows_scene(self, r"the business of music", items,
                   "This part is about money. <bookmark mark='b'/> We will follow one stream's fraction of a cent from a phone to a "
                   "songwriter. <bookmark mark='c'/> On the way it passes two copyrights, four kinds of licence, and half a dozen "
                   "intermediaries. <bookmark mark='d'/> Each arrangement was made when a new machine broke the last one: the "
                   "player piano, radio, the sampler, the file, and now the model. <bookmark mark='e'/> Everything here is dated, "
                   "mostly American, on illustrative terms, and it is not legal or financial advice. <bookmark mark='f'/> The "
                   "arithmetic, though, is general: shares, pools, power laws, and the odds of coincidence.", marks="bcdef")

    # ------------------------------------------------------------------
    def plan(self):
        card = objectives_card([
            r"two copyrights, \ four licences, \ and who collects",
            r"where a stream's money goes; \ deals and recoupment",
            r"dividing the pool: \ pro rata or user by user",
            r"superstars, \ social influence and the charts",
            r"live music: \ the cost disease and the price of a ticket",
            r"how many melodies there are; \ sampling, \ and machines",
        ], title=r"In this part", font_size=22).move_to(DOWN * 0.1)
        with self.voiceover(
            "Here is the plan. Two copyrights, four licences, and who collects. <bookmark mark='b'/> Where a stream's money goes, "
            "and how deals and advances work. <bookmark mark='c'/> Two ways of dividing a streaming service's pool. "
            "<bookmark mark='d'/> Superstars, social influence and the charts. <bookmark mark='e'/> Live music: the cost disease "
            "and the price of a ticket. <bookmark mark='f'/> And how many melodies there are, sampling, and machines that "
            "learn from music."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("bcdef", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()
