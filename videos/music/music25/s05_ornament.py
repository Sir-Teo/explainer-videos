from __future__ import annotations

import numpy as np

from videos.music.music25.common import *  # noqa: F403


class Ornament(SoundScene):
    def construct(self):
        chapter(self, 4, r"Affect and ornament", r"What did a Baroque performer add to the page?", extra=((1739, r"Mattheson's \textit{Capellmeister}"),))
        self.affect()
        self.heard()
        self.tastes()
        self.rules()

    # ------------------------------------------------------------------
    def affect(self):
        items = [
            (r"the doctrine of the affections: \ a piece, \ or a movement, \ portrays one passion", WHITE),
            (r"joy, \ grief, \ anger, \ tenderness: \ each with its keys, \ tempos, \ intervals and figures", WHITE),
            (r"Johann Mattheson, \ \textit{The Complete Kapellmeister} \ (1739): \ a catalogue of them", WHITE),
            (r"rhetoric as a model: \ musical figures named like figures of speech", TUNE),
            (r"governing affects are one historical ideal; \ movements can contain internal contrast", GREY_A),
        ]
        rows_scene(self, r"one passion at a time", items,
                   "Baroque writers explained music's power with a theory of the passions. <bookmark mark='b'/> A piece, or a movement, should portray one affect, joy or grief, anger or tenderness, each with its suitable keys, tempos, intervals and figures. <bookmark mark='c'/> The Hamburg critic Johann Mattheson catalogued them in his Complete Kapellmeister of 1739. <bookmark mark='d'/> The model was rhetoric: theorists named musical figures after figures of speech, a rising line for exaltation, a falling chromatic line for lament. <bookmark mark='e'/> One-affect descriptions are a teaching generalization; Baroque movements also contain internal contrasts. Part 26 examines later approaches to contrast.")

    # ------------------------------------------------------------------
    def heard(self):
        d = load("ornaments")
        c = clip("ornaments.four")
        tot = max(n[1] + n[2] for n in d["plain"])
        g1 = mroll(d["plain"], width=5.2, height=1.4, lo=70, hi=81, total=tot)
        g2 = mroll(d["ornamented"], width=5.2, height=1.4, lo=70, hi=81, total=tot, bar_h=0.11)
        tot2 = max(n[1] + n[2] for n in d["straight"])
        g3 = mroll(d["straight"], width=5.2, height=1.4, lo=69, hi=81, total=tot2, color=BLUE)
        g4 = mroll(d["inegale"], width=5.2, height=1.4, lo=69, hi=81, total=tot2, color=BLUE)
        cells = VGroup(*[VGroup(label(t, font_size=20, color=GREY_A), g).arrange(DOWN, buff=0.15) for t, g in (
            (r"plain", g1), (r"ornamented: \ appoggiatura, \ mordent, \ trill", g2), (r"straight eighths", g3), (r"\textit{notes inégales}: \ long, \ short", g4))])
        cells.arrange_in_grid(rows=2, cols=2, buff=(0.8, 0.5)).move_to(DOWN * 0.2)
        head = label(r"what the page does not show", font_size=28, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            "The page also left the ornaments to the player. Here is a plain line, then the same line as a player might "
            "decorate it: a leaning note, an appoggiatura, on the first beat; a quick mordent; a trill from the upper note "
            "at the cadence. Then a run of even eighth notes, and the same run as a French player would have played it, "
            "long, short, long, short, the notes inégales, unequal notes, often left implicit in the relevant French performance conventions."
        ):
            self.play(FadeIn(head), FadeIn(cells))
        with self.listen(c) as snd:
            window(snd, r"plain, \ ornamented, \ straight, \ unequal", detail=r"Part 1's string on Part 7's soundboard", corner=DL, tag_corner=DR)
            for g, k, u in ((g1, "plain", d["unit"]), (g2, "ornamented", d["unit"]), (g3, "straight", d["unit2"]), (g4, "inegale", d["unit2"])):
                flash(snd, g.notes, [d["starts"][k] + n[1] * u for n in d[k]], hot=WHITE, base=TUNE if k in ("plain", "ornamented") else BLUE)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def rules(self):
        items = [
            (r"tables of ornaments: \ d'Anglebert \ (1689), \ Couperin \ (1713), \ Bach's for his son \ (1720)", WHITE),
            (r"a trill begins on the note above, \ on the beat: \ a dissonance resolved", WHITE),
            (r"an appoggiatura takes half the note \ (two thirds of a dotted one)", WHITE),
            (r"inequality: \ in French music, \ pairs of the shortest common notes, \ in stepwise passages", WHITE),
            (r"the rules are contested: \ how much, \ how fast, \ and where, \ is still argued", TUNE),
        ]
        rows_scene(self, r"the rules of ornament", items,
                   "Composers and teachers printed tables of the signs. <bookmark mark='b'/> Jean-Henri d'Anglebert in "
                   "1689, François Couperin in 1713, and Bach in the little book he wrote out for his son Wilhelm Friedemann "
                   "in 1720. <bookmark mark='c'/> A trill, by these rules, begins on the note above, on the beat, so that "
                   "it starts as a dissonance and resolves. <bookmark mark='d'/> In a common teaching convention, an appoggiatura takes half the value of "
                   "the note it leans on, or two thirds of a dotted one. <bookmark mark='e'/> Inequality applied, in French "
                   "music, to pairs of the shortest common notes moving by step. <bookmark mark='f'/> How much of this "
                   "applied where, in Bach as against Couperin, in Italy as against France, is still argued over by "
                   "performers today; chapter ten returns to that kind of evidence.", marks="cdef")

    # ------------------------------------------------------------------
    def tastes(self):
        items = [
            (r"1702: \ François Raguenet praises Italian music: \ bold, \ virtuosic, \ surprising", WHITE),
            (r"1704: \ Le Cerf de la Viéville replies: \ French music is natural, \ tender, \ reasonable", WHITE),
            (r"Italy: \ the singer's free ornaments; \ France: \ small ornaments written as signs", WHITE),
            (r"1724: \ Couperin's \textit{Les goûts réunis}: \ the tastes reunited", TUNE),
            (r"Germany's composers, \ Bach among them, \ took from both", GREY_A),
        ]
        rows_scene(self, r"French and Italian taste", items,
                   "Ornament was also a matter of national taste. <bookmark mark='b'/> In 1702 a French priest, François Raguenet, published a comparison praising Italian music for its boldness and surprise. <bookmark mark='c'/> A Parisian critic, Le Cerf de la Viéville, replied that French music was more natural, tender and reasonable. <bookmark mark='d'/> Italians left ornaments to the singer's invention; the French wrote small ornaments into the score as signs. <bookmark mark='e'/> In 1724 Couperin published a set called The Tastes Reunited, <bookmark mark='f'/> and German composers, Bach among them, took freely from both.", marks="cdef")
