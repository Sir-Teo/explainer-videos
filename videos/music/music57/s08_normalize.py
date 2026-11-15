from __future__ import annotations

from videos.music.music57.common import *  # noqa: F403


class Normalize(SoundScene):
    def construct(self):
        chapter(self, 7, r"Normalization", r"What happens to a loud master when the player turns everything to the same loudness?")
        self.how()
        self.gains()
        self.quiz()
        self.album()

    # ------------------------------------------------------------------
    def how(self):
        items = [
            (r"a player measures each track's integrated loudness \ (stored as metadata), \ and plays it with one gain", WHITE),
            (r"gain $= $ target $-$ the track's loudness: \ louder masters are turned down", WHITE),
            (r"quieter ones are turned up only as far as their true peak allows, \ or not at all", WHITE),
            (r"from the early 2010s it became the default on radio, \ television and the big streaming services", WHITE),
            (r"the arms race lost its prize: \ a master 6 dB louder is played 6 dB quieter", TUNE),
        ]
        rows_scene(self, r"one gain per track", items,
                   "Here is how the war ended. <bookmark mark='b'/> A player measures each track's integrated loudness, or reads it "
                   "from the file, and plays the track with one gain. <bookmark mark='c'/> The gain is the target minus the track's "
                   "loudness, so louder masters are turned down. <bookmark mark='d'/> Quieter ones are turned up only as far as "
                   "their true peak allows, or not at all. <bookmark mark='e'/> From the early 2010s it became the default on radio, "
                   "on television under R 128, and on the big streaming services. <bookmark mark='f'/> The arms race lost its prize: "
                   "a master six decibels louder is simply played six decibels quieter.", marks="bcdef")

    # ------------------------------------------------------------------
    def gains(self):
        d = load("norm")
        war = {round(r["target"]): r for r in load("war")["rows"]}
        rows = VGroup(VGroup(label(r"master", font_size=17, color=GREY_A), label(r"its true peak", font_size=17, color=GREY_A), label(r"the player's gain", font_size=17, color=GREY_A),
                             label(r"plays at", font_size=17, color=GREY_A), label(r"its peaks then reach", font_size=17, color=GREY_A)))
        tps = {-20: war[-20]["tp"], -14: war[-14]["tp"], -8: -1.0}
        for tg, col in ((-20, GREY_A), (-14, TUNE), (-8, EAR)):
            gdb = d["gains"][f"{float(tg)}"]
            rows.add(VGroup(label(f"{tg} LUFS", font_size=19, color=col), label(f"{tps[tg]:.1f} dBTP", font_size=19, color=WHITE), label(f"{gdb:+.1f} dB", font_size=19, color=col),
                            label(f"{tg + gdb:.1f} LUFS", font_size=19, color=WHITE), label(f"{tps[tg] + gdb:.1f} dBTP", font_size=19, color=col)))
        rows.arrange(DOWN, buff=0.4)
        for r in rows:
            for i, m in enumerate(r):
                m.set_x(-5.0 + 2.5 * i)
        rows.move_to(UP * 0.1)
        note = label(r"after normalization the loud master's peaks are the lowest: \ the gentle masters now have 6 dB more room for their drums", font_size=17, color=WHITE).to_edge(DOWN, buff=0.5)
        head = label(r"three masters, \ normalized to $-14$ LUFS", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "Take three of our masters to a player normalizing to minus fourteen. <bookmark mark='a'/> The minus twenty master "
            f"is turned up by {say(d['gains']['-20.0'], 1)} decibels, as far as its peaks allow. The minus fourteen master is "
            f"left alone. The minus eight master is turned down by {say(-d['gains']['-8.0'], 1)}. <bookmark mark='b'/> All three "
            "now play at nearly the same loudness, but the loud master's peaks are now the lowest of the three: the drums of "
            "the gentle masters hit six decibels harder."
        ) as vo:
            self.play(FadeIn(head), FadeIn(rows[0]), FadeIn(ghost(rows[1:], 0.25)))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in rows[1:]], lag_ratio=0.3), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def quiz(self):
        d = load("norm")
        c = clip("norm.three")
        card = listen_card(r"The three masters, \ $-20$, \ $-14$ and $-8$ LUFS, \ in some order, \ each played as a streaming service "
                           r"would play it. \ Which was mastered loudest?", width=10.0)
        with self.voiceover(
            "Your turn. The same three masters, in some order, each played as a streaming service would play it. Which was "
            "mastered loudest?"
        ):
            self.play(FadeIn(card))
        self.wait(0.8)
        boxes = choice_boxes([r"first", r"second", r"third"], width=2.6, buff=0.9).move_to(UP * 0.6)
        self.play(FadeOut(card), FadeIn(boxes))
        st = d["starts"]
        with self.listen(c) as snd:
            window(snd, r"three masters, \ normalized", kind="physical model", detail=r"Part 56's session", corner=DL, tag_corner=DR)
            pulse(snd, boxes[0], st["first"], st["second"] - 0.4, buff=0.08)
            pulse(snd, boxes[1], st["second"], st["third"] - 0.4, buff=0.08)
            pulse(snd, boxes[2], st["third"], c.duration, buff=0.08)
        res = label(r"the first: \ $-8$ LUFS, \ turned down 6 dB; \ then $-20$ \ (turned up 3.8) \ and $-14$ \ (untouched)", font_size=19, color=TUNE).move_to(DOWN * 1.4)
        with self.voiceover(
            "The first. Normalized, it is no louder than the others, and it is the flattest: its drums hit softest. The war's "
            "master is now the one that sounds smallest."
        ):
            self.play(boxes[0][0].animate.set_stroke(TUNE, width=4), FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def album(self):
        items = [
            (r"track normalization: \ every song to the target; \ a quiet ballad comes up as loud as the single", WHITE),
            (r"album normalization: \ one gain for the whole album, \ keeping the mastering engineer's balance between songs", WHITE),
            (r"services play albums album-normalized when they can tell they are playing an album", WHITE),
            (r"so the right master is no longer the loudest, \ but the one that sounds best at the target", TUNE),
        ]
        rows_scene(self, r"tracks and albums", items,
                   "One detail matters for albums. <bookmark mark='b'/> Track normalization brings every song to the target, so a "
                   "quiet ballad comes up as loud as the single. <bookmark mark='c'/> Album normalization uses one gain for the "
                   "whole album, keeping the balance the mastering engineer chose between songs. <bookmark mark='d'/> Services play "
                   "albums album-normalized when they can tell an album is being played. <bookmark mark='e'/> So the right master "
                   "is no longer the loudest, but the one that sounds best at the target.", marks="bcde")
