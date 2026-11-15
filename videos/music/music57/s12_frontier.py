from __future__ import annotations

from videos.music.music57.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ loudness and preference", r"Once loudness is equal, \ what do listeners actually prefer?")
        self.found()
        self.ended()
        self.ai()
        self.problem()

    # ------------------------------------------------------------------
    def found(self):
        items = [
            (r"at matched loudness, \ heavy limiting lowers listeners' ratings of quality \ (Croghan, \ Arehart and Kates, \ 2012)", WHITE),
            (r"moderate limiting often goes unnoticed: \ the effect depends on the music and on how much \ (Hjortkjær and Walther-Hansen, \ 2014)", WHITE),
            (r"listeners are more sensitive to distortion and lost transients than to lost dynamics as such", WHITE),
            (r"preferences differ by genre and by listener: \ some music is meant to be dense", WHITE),
            (r"and almost every older study played music loud, \ in quiet rooms: \ not on earbuds on a bus", TUNE),
        ]
        rows_scene(self, r"what experiments found", items,
                   "What do listeners prefer, once loudness is equal? <bookmark mark='b'/> Naomi Croghan, Kathryn Arehart and James "
                   "Kates found in 2012 that heavy limiting, compared at matched loudness, lowered listeners' ratings of quality. "
                   "<bookmark mark='c'/> Jens Hjortkjær and Mads Walther-Hansen found in 2014 that moderate limiting often goes "
                   "unnoticed: the effect depends on the music and on how much. <bookmark mark='d'/> Listeners seem more sensitive "
                   "to distortion and lost transients than to lost dynamics as such. <bookmark mark='e'/> Preferences differ by genre "
                   "and by listener; some music is meant to be dense. <bookmark mark='f'/> And almost every study played the music "
                   "loud, in a quiet room: not on earbuds on a bus.", marks="bcdef")

    # ------------------------------------------------------------------
    def ended(self):
        items = [
            (r"has normalization ended the war? \ measurements of new releases suggest masters have eased a little, \ not much", WHITE),
            (r"engineers still master loud: \ for clubs, \ for radio processors, \ for previews, \ and because the sound itself is now a style", WHITE),
            (r"and density is not only loudness: \ a dense master sounds closer and more present on small loudspeakers in noise", WHITE),
            (r"the open question is no longer `how loud', \ but `what master serves which listening'", TUNE),
        ]
        rows_scene(self, r"after the war", items,
                   "Has normalization ended the war? <bookmark mark='b'/> Measurements of new releases suggest masters have eased a "
                   "little, not much. <bookmark mark='c'/> Engineers still master loud, for clubs, for radio's own processors, for "
                   "previews, and because the dense sound is now a style of its own. <bookmark mark='d'/> And density is not only "
                   "loudness: a dense master sounds closer and more present on small loudspeakers in noise. "
                   "<bookmark mark='e'/> The open question is no longer how loud, but which master serves which kind of listening.", marks="bcde")

    # ------------------------------------------------------------------
    def ai(self):
        items = [
            (r"automatic mastering services \ (from about 2014): \ upload a mix, \ receive a master", WHITE),
            (r"they match a mix's spectrum and loudness to a reference or a learned target, \ then limit", WHITE),
            (r"the same loudness bias applies to judging them: \ compare at equal loudness, \ blind", WHITE),
            (r"playback that adapts: \ a phone could set the master's dynamics for the room it is in, \ from its own microphone", TUNE),
        ]
        rows_scene(self, r"machines that master", items,
                   "Machines master too. <bookmark mark='b'/> Automatic mastering services, since about 2014, take a mix and return "
                   "a master. <bookmark mark='c'/> They match its spectrum and loudness to a reference or a learned target, and "
                   "limit. <bookmark mark='d'/> The same loudness bias applies to judging them: compare at equal loudness, blind. "
                   "<bookmark mark='e'/> And playback could adapt: a phone could set the master's dynamics for the room it is in, "
                   "listening through its own microphone.", marks="bcde")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take a set of mixes in several genres, \ and master each at several peak-to-loudness ratios", WHITE),
            (r"normalize all to one loudness, \ and play them in several places: \ studio, \ living room, \ earbuds in recorded street noise", WHITE),
            (r"collect blind preferences, \ and model them against the music, \ the place and the listener", WHITE),
            (r"$\bigstar$ \ research problem: \ once everything is normalized, \ what peak-to-loudness ratio do listeners prefer, \ and does it depend on where they listen?", EAR),
            (r"an answer would tell mastering engineers what to make, \ and players what to adapt", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Take mixes in several genres and master each at several "
            "peak-to-loudness ratios. <bookmark mark='b'/> Normalize them all to one loudness and play them in several places: "
            "a studio, a living room, earbuds in recorded street noise. <bookmark mark='c'/> Collect blind preferences, and "
            "model them against the music, the place and the listener. <bookmark mark='d'/> The question: once everything is "
            "normalized, what peak-to-loudness ratio do listeners prefer, and does it depend on where they listen? "
            "<bookmark mark='e'/> An answer would tell mastering engineers what to make, and players what to adapt."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()
