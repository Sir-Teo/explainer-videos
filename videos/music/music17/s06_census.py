from __future__ import annotations

import numpy as np

from videos.music.music17.common import *  # noqa: F403


class Census(SoundScene):
    def construct(self):
        chapter(self, 5, r"How often Bach breaks them", r"Does the master obey the rules?")
        self.count()
        self.pairs()
        self.hear()
        self.others()

    # ------------------------------------------------------------------
    def count(self):
        d = load("census")
        par = d["parallel"]
        n = par["fifths"] + par["octaves"]
        big = VGroup(label(rf"{d['moves']:,} changes of chord".replace(",", "{,}"), font_size=34, color=WHITE),
                     label(rf"parallel fifths: \ {par['fifths']} \qquad parallel octaves: \ {par['octaves']}", font_size=34, color=RED),
                     label(rf"one in {d['rate']:.0f}", font_size=48, color=TUNE)).arrange(DOWN, buff=0.5).move_to(UP * 0.4)
        note = label(r"counted at every moment any voice moves, \ between every pair of voices", font_size=22, color=GREY_B).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Take every moment in every chorale where any voice moves to a new note: "
            f"{say(round(d['moves'], -2))} changes of chord. At each, check all six pairs of voices. "
            f"<bookmark mark='a'/> Bach writes parallel fifths {say(par['fifths'])} times and parallel "
            f"octaves {say(par['octaves'])} times. <bookmark mark='b'/> That is once in about "
            f"{say(round(d['rate'], -1))} changes of chord, or about once in every five chorales. The "
            "rule is real: by chance alone, writing four voices that move by step, you would make "
            "parallels many times in every chorale, as the chord-chooser did in the hook. And Bach does "
            "break it, now and then."
        ) as vo:
            self.play(FadeIn(big[0]), FadeIn(note))
            vo.wait_until("a")
            self.play(FadeIn(big[1]))
            vo.wait_until("b")
            self.play(FadeIn(big[2]))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def pairs(self):
        d = load("census")
        order = ["S–A", "S–T", "S–B", "A–T", "A–B", "T–B"]
        vals = [d["pairs"].get(k, 0) for k in order]
        ch = columns(vals, [k.replace("–", "--") for k in order], width=7.0, height=2.6, color=WEAK, hot=(1,), hot_color=RED, fmt="{:.0f}", font_size=24).move_to(LEFT * 2.4 + DOWN * 0.7)
        t = label(r"Bach's parallels, \ by pair of voices", font_size=24, color=GREY_A).next_to(ch, UP, buff=0.35)
        off = len(d["all"]) - d["on_beat"]
        side = VGroup(label(rf"{off} of {len(d['all'])}", font_size=40, color=TUNE), label(r"fall between the beats: \\ one of the notes is a passing note", font_size=24, color=WHITE)).arrange(DOWN, buff=0.25).move_to(RIGHT * 4.2 + DOWN * 0.2)
        with self.voiceover(
            "Where do they fall? <bookmark mark='a'/> Between every pair of voices, the most often between "
            "soprano and tenor. <bookmark mark='b'/> And "
            f"{say(off)} of the {say(len(d['all']))} happen between the beats, where one of the two "
            "voices is moving through a passing note, a quick note that is not part of either chord. "
            "Most of Bach's parallels are fleeting: an eighth note long, in an inner voice."
        ) as vo:
            vo.wait_until("a")
            self.play(FadeIn(ch), FadeIn(t))
            vo.wait_until("b")
            self.play(FadeIn(side))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def hear(self):
        d = load("census")
        c = clip("census.two")
        gs = VGroup()
        for k, h in enumerate(d["heard"]):
            g = choir_roll(h["voices"], width=5.6, height=3.0, lo=40, hi=80, thick=0.11).move_to(LEFT * 3.3 * (1 - 2 * k) + DOWN * 0.3)
            x0, x1 = g.x(g.base + h["at"][0]), g.x(g.base + h["at"][1])
            mark = Rectangle(width=max(x1 - x0, 0.2) + 0.5, height=3.2, stroke_color=RED, stroke_width=2, fill_opacity=0).move_to([(x0 + x1) / 2 + 0.15, g.get_center()[1], 0])
            lab = label(rf"{h['name'].replace('bwv', 'BWV ')}: \ {h['pair'].replace('–', '--')}", font_size=22, color=GREY_A).next_to(g, UP, buff=0.3)
            gs.add(VGroup(g, mark, lab))
        with self.voiceover(
            "Here are two of the few that fall on the beat, each with a beat or two around it. The red "
            "box marks the move. Listen for whether you can hear anything wrong."
        ):
            self.play(*[FadeIn(x[0]) for x in gs], *[FadeIn(x[2]) for x in gs])
            self.play(*[Create(x[1]) for x in gs])
        with self.listen(c) as snd:
            window(snd, r"two of Bach's parallel fifths", kind="synthesized", detail=r"a model choir", corner=DL, tag_corner=DR)
            for k, key in enumerate("ab"):
                sing_roll(snd, gs[k][0], d["heard"][k]["times"], start=d["starts"][key])
                pulse(snd, gs[k][2], d["starts"][key], (d["starts"]["b"] - 0.5) if k == 0 else c.duration, buff=0.1)
        with self.voiceover(
            "They are hard to pick out. In a full texture of four voices, with the other two moving "
            "differently, two voices moving in fifths for a single step do not fuse into one. The "
            "rule matters most where few voices are sounding, or where the parallel voices are the outer "
            "ones and exposed. Bach seems to have known exactly how much it mattered, and where."
        ):
            self.wait(0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def others(self):
        d = load("census")
        ch = d["chords"]
        rows_ = [(r"fifths or octaves in contrary motion", f"{d['contrary'].get('fifths', 0) + d['contrary'].get('octaves', 0)}", f"{d['moves']}"),
                 (r"hidden fifths or octaves, \ outer voices", f"{d['hidden']}", f"{d['moves']}"),
                 (r"a voice overlapping its neighbour's last note", f"{d['overlap']}", f"{d['moves']}"),
                 (r"voices crossed", f"{d['crossing']}", f"{ch}"),
                 (r"upper voices more than an octave apart", f"{d['spacing']}", f"{ch}"),
                 (r"outside the textbook's ranges", f"{d['out_of_range']}", f"{ch}")]
        tab = VGroup()
        for k, (a, b, n) in enumerate(rows_):
            share = 100 * int(b) / int(n)
            r = VGroup(label(a, font_size=24, color=GREY_A), label(b, font_size=26, color=TUNE), label(rf"{share:.1f} in a hundred", font_size=22, color=GREY_B))
            r[0].move_to([-0.6, 2.2 - 0.62 * k, 0], aligned_edge=RIGHT)
            r[1].move_to([0.4, 2.2 - 0.62 * k, 0], aligned_edge=LEFT)
            r[2].move_to([2.0, 2.2 - 0.62 * k, 0], aligned_edge=LEFT)
            tab.add(r)
        cap = label(r"rules of avoidance, \ obeyed between 94 and 99.7 times in a hundred", font_size=28, color=TUNE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The other rules, counted the same way. Fifths and octaves reached in contrary motion, which "
            f"some textbooks also forbid: {say(d['contrary'].get('fifths', 0) + d['contrary'].get('octaves', 0))} times. "
            f"Hidden fifths and octaves between soprano and bass: {say(d['hidden'])}. A voice moving past "
            f"where its neighbour just was: about one move in seventeen, the most common licence. Voices "
            f"crossed: {say(round(100 * d['crossing'] / ch, 1))} chords in a hundred. Upper voices spread "
            f"wider than an octave, or notes outside the textbook ranges: about one chord in a hundred. "
            "<bookmark mark='a'/> Every rule is obeyed nearly always and broken sometimes. That is the "
            "signature of a style, not a law: a strong preference, set aside when something else matters "
            "more."
        ) as vo:
            self.play(LaggedStart(*[FadeIn(r) for r in tab], lag_ratio=0.4), run_time=6.0)
            vo.wait_until("a")
            self.play(FadeIn(cap))
        self.wait(0.4)
        self.clear_scene()
