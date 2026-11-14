from __future__ import annotations

import numpy as np

from videos.music.music23.common import *  # noqa: F403


class Notre(SoundScene):
    def construct(self):
        chapter(self, 6, r"Notre Dame", r"What did Léonin and Pérotin build?", extra=((1280, r"Anonymous IV names them"),))
        self.names()
        self.clausula()
        self.exchange()

    # ------------------------------------------------------------------
    def names(self):
        items = [
            (r"about 1280, \ an English student in Paris, \ known only as `Anonymous IV', \ looks back a century", WHITE),
            (r"Leoninus, \ `the best maker of organum', \ wrote a great book of organa, \ the \textit{Magnus liber}", WHITE),
            (r"Perotinus, \ `the best maker of discant', \ revised it, \ and wrote organa in three and four voices", WHITE),
            (r"the \textit{Magnus liber} survives in later copies: \ chant for the whole church year, \ in two voices", WHITE),
            (r"almost everything we know of the two men is in a few sentences of that one treatise", GREY_A),
        ]
        rows_scene(self, r"two names", items,
                   "The names of the Notre Dame composers come to us almost by accident. <bookmark mark='b'/> Around "
                   "1280 an English student in Paris, whom scholars call Anonymous the Fourth because he was the fourth "
                   "anonymous treatise in a nineteenth-century edition, looked back about a century and named two "
                   "singers. <bookmark mark='c'/> Leoninus, he says, was the best maker of organum, and wrote a great "
                   "book of organa for the whole church year, the Magnus liber organi. <bookmark mark='d'/> Perotinus, "
                   "the best maker of discant, revised that book and wrote organa in three and four voices, Viderunt and "
                   "Sederunt among them. <bookmark mark='e'/> The Magnus liber survives only in later copies, and almost "
                   "everything we know about the two men is in a few sentences of that one student's notes.")

    # ------------------------------------------------------------------
    def clausula(self):
        d = load("notre")
        c = clip("notre.clausula")
        g = voices_roll([d["duplum"], d["tenor"]], width=11.0, height=2.8, colors=[TUNE, GREY_A], bar_h=0.13).move_to(DOWN * 0.1)
        lt = label(r"the chant, \ in fifth-mode longs", font_size=19, color=GREY_A).next_to(g.parts[1].notes[0], DOWN, buff=0.2).align_to(g, LEFT)
        ld = label(r"the added voice, \ first mode: \ long, \ short", font_size=19, color=TUNE).next_to(g, UP, buff=0.15).align_to(g, LEFT)
        head = label(r"a discant clausula \ (ours)", font_size=28, color=GREY_A).to_edge(UP, buff=0.35)
        cap = label(r"at the start of every perfection, \ a fifth or an octave; \ the short note may be anything", font_size=21, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "A Notre Dame organum for two voices alternates the two styles. Where the chant has few notes to a syllable, "
            "the chant is held and the upper voice flourishes freely, organum purum. Where the chant has many notes to "
            "a syllable, both voices move in rhythmic modes, the chant in steady fifth-mode longs and the upper voice in "
            "the first mode, a passage called a clausula. This one is computed for the film. At the start of every "
            "perfection the voices meet on a fifth or an octave; in between, the short note goes where the line wants."
        ):
            self.play(FadeIn(head), FadeIn(g), FadeIn(lt), FadeIn(ld), FadeIn(cap))
        with self.listen(c) as snd:
            window(snd, r"a discant clausula", detail=r"two synthetic voices", kind="synthesized", corner=UR, tag_corner=UL)
            flash_voices(snd, g, [d["duplum"], d["tenor"]], 0.0, d["unit"], colors=[TUNE, GREY_A])
            cursor(snd, g, 0.0, d["unit"])
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def exchange(self):
        d = load("hook")
        lines = d["lines"]
        up = lines[:3]
        P = d["perfections"]
        tenor = lines[3][0][0]
        on = [(p - tenor) % 12 for v in up for p, a, _ in v if a % 3 == 0]
        off = [(p - tenor) % 12 for v in up for p, a, _ in v if a % 3 != 0]
        cons_on = np.mean([x in (0, 7) for x in on])
        diss_off = np.mean([x not in (0, 3, 4, 7, 8, 9) for x in off])
        g = voices_roll(up, width=11.0, height=2.6, colors=[TUNE, BLUE, EAR], bar_h=0.11).move_to(UP * 0.5)
        blocks = VGroup()
        for k in range(0, P, 6):
            for j, off_ in ((0, 0), (1, 3)):
                x0 = g.frame.get_left()[0] + g.frame.width * 3 * (k + off_) / g.total
                w = g.frame.width * 9 / g.total
                if k + off_ + 3 <= P:
                    blocks.add(Rectangle(width=w, height=g.frame.height + 0.2, stroke_color=GREY_B, stroke_width=1.2, fill_opacity=0.04).move_to([x0 + w / 2, g.frame.get_center()[1], 0]))
        rows_ = VGroup(*[label(t, font_size=22, color=c_) for t, c_ in (
            (rf"perfection starts: \ {100 * cons_on:.0f} in 100 a unison, \ fifth or octave with the held note", WHITE),
            (rf"the short notes in between \ (ours: \ always a step away): \ {100 * diss_off:.0f} in 100 dissonant", WHITE),
            (r"\textit{Stimmtausch}: \ two voices swap their phrases, \ the same sounds, \ redistributed", TUNE),
            (r"Pérotin's quadrupla last ten minutes or more on a few notes of chant", GREY_A))]).arrange(DOWN, buff=0.22, aligned_edge=LEFT).to_edge(DOWN, buff=0.4)
        rows_.scale_to_fit_width(min(rows_.width, 12.4))
        with self.voiceover(
            "Back to the four-voice organum of the opening, to see how it holds together. <bookmark mark='a'/> At the "
            f"start of every perfection, every upper voice is a unison, fifth or octave from the held note: {say(round(100 * cons_on))} "
            "times in a hundred, by construction, as in Pérotin. <bookmark mark='b'/> The short notes in between are free, "
            f"and in this version {say(round(100 * diss_off))} in a hundred are dissonant, more than Pérotin wrote, since our "
            "short notes are always a step away. Consonance is a rule about where the beat falls, not about every note. <bookmark mark='c'/> And Pérotin's voices trade phrases, a device called voice exchange: "
            "one voice sings what another just sang, so the same sounds return, rearranged. It is how a long piece on one "
            "held note stays coherent. <bookmark mark='d'/> His quadrupla run ten minutes or more on a handful of chant "
            "notes, built from exactly these three things: the menu of rhythms, consonance on the beat, and exchange."
        ) as vo:
            self.play(FadeIn(g))
            vo.wait_until("a")
            self.play(FadeIn(rows_[0]))
            vo.wait_until("b")
            self.play(FadeIn(rows_[1]))
            vo.wait_until("c")
            self.play(Create(blocks), FadeIn(rows_[2]))
            vo.wait_until("d")
            self.play(FadeIn(rows_[3]))
        self.wait(0.4)
        self.clear_scene()
