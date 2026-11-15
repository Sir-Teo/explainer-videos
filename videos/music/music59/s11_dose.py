from __future__ import annotations

from videos.music.music59.common import *  # noqa: F403


class Dose(SoundScene):
    def construct(self):
        chapter(self, 10, r"Hearing health", r"How long can you stand at the barrier?")
        self.ear()
        self.rule()
        self.table()
        self.law()

    # ------------------------------------------------------------------
    def ear(self):
        items = [
            (r"loud sound damages the outer hair cells of the cochlea \ (Part 4's amplifier): \ first at 3 to 6 kHz", WHITE),
            (r"they do not grow back: \ the loss is permanent, \ and so is tinnitus", WHITE),
            (r"a temporary threshold shift after a concert \ (muffled ears, \ ringing) \ is the warning", WHITE),
            (r"and even when the threshold recovers, \ synapses behind the hair cells may not: \ `hidden' hearing loss \ (Kujawa and Liberman, \ 2009)", WHITE),
            (r"what counts is the dose: \ level and time together", TUNE),
        ]
        rows_scene(self, r"what loud sound does", items,
                   "All of this is loud, and loudness has a cost. <bookmark mark='b'/> Loud sound damages the outer hair cells of the "
                   "cochlea, Part 4's amplifier, first in the region tuned to three to six kilohertz. <bookmark mark='c'/> They do "
                   "not grow back: the loss is permanent, and so, often, is the ringing called tinnitus. <bookmark mark='d'/> The "
                   "muffled ears and ringing after a concert, a temporary threshold shift, are the warning. <bookmark mark='e'/> And "
                   "Kujawa and Liberman showed in 2009, in mice, that even when the threshold recovers, the synapses behind the hair "
                   "cells may not: a hidden loss, felt as trouble hearing speech in noise. <bookmark mark='f'/> What counts is the "
                   "dose: level and time together.", marks="bcdef")

    # ------------------------------------------------------------------
    def rule(self):
        d = load("dose")
        al = d["allowed"]
        keys = sorted(al, key=float)
        eq = MathTex(r"t_{\text{allowed}} = 8\ \text{h} \times 2^{-(L - 85)/3}, \qquad \text{dose} = \sum_i \frac{t_i}{t_{\text{allowed}}(L_i)}", font_size=34, color=TUNE).to_edge(UP, buff=1.0)

        def fmt(m):
            return f"{m / 60:g} h" if m >= 60 else (f"{m:g} min" if m >= 1 else f"{60 * m:.0f} s")
        cells = VGroup(*[VGroup(label(rf"{k} dBA", font_size=18, color=WHITE), label(fmt(al[k]), font_size=18, color=TUNE if float(k) <= 88 else EAR)).arrange(DOWN, buff=0.15) for k in keys]).arrange(RIGHT, buff=0.45).move_to(DOWN * 0.3)
        note = label(r"every 3 dB doubles the energy, \ and halves the time: \ NIOSH's recommendation \ (1998), \ A-weighted", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        head = label(r"the equal-energy rule", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        with self.voiceover(
            "The rule is equal energy. <bookmark mark='a'/> Eighty-five decibels, A-weighted, for eight hours is a full day's "
            "dose, in the American occupational recommendation of 1998; each three decibels doubles the energy and halves the "
            "time. <bookmark mark='b'/> So eighty-eight allows four hours, ninety-four one hour, a hundred fifteen minutes, "
            "and a hundred and six, a level many front rows reach, under four minutes. <bookmark mark='c'/> Doses add up through "
            "the day, as fractions of the allowance."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(eq))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(c_) for c_ in cells], lag_ratio=0.15), run_time=2.0)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def table(self):
        d = load("dose")
        rows_ = VGroup()
        for r in d["rows"]:
            col = TUNE if r["dose"] <= 100 else EAR
            rows_.add(VGroup(label(r["who"].replace("%", r"\%"), font_size=18, color=WHITE),
                             label(rf"{r['dose']:,.0f}\%", font_size=20, color=col)))
        rows_.arrange(DOWN, buff=0.38, aligned_edge=LEFT).move_to(LEFT * 1.0 + DOWN * 0.1)
        for r in rows_:
            r[1].move_to([5.3, r[0].get_center()[1], 0])
        top = label(r"day's dose", font_size=16, color=GREY_A).move_to([5.3, rows_.get_top()[1] + 0.4, 0])
        head = label(r"one night's dose", font_size=26, color=GREY_A).to_edge(UP, buff=0.35)
        dd = [r["dose"] for r in d["rows"]]
        with self.voiceover(
            f"So, one night. <bookmark mark='a'/> A fan at the barrier, two hours at a hundred and four: {say(dd[0])} percent "
            f"of a day's dose, twenty times over. <bookmark mark='b'/> Mid-arena at ninety-eight: {say(dd[1])} percent. "
            f"<bookmark mark='c'/> The same fan with fifteen-decibel earplugs: {say(dd[2])} percent, and the music still "
            "clear, because good plugs cut evenly across the spectrum. <bookmark mark='d'/> The engineer at the desk, five hours "
            f"of soundcheck and show at ninety-six: {say(dd[3])} percent. <bookmark mark='e'/> And a drummer whose kit is a "
            f"hundred and five, if the in-ear monitors seal well enough to hear it at eighty-eight: {say(dd[4])} percent."
        ) as vo:
            self.play(FadeIn(head), FadeIn(top))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def law(self):
        items = [
            (r"workers are protected by law: \ in the EU from 85 dBA a day \ (2003/10/EC), \ in the UK music and entertainment included since 2008", WHITE),
            (r"audiences have guidelines, \ not limits: \ the WHO's 2022 standard for venues: \ 100 dBA over any 15 minutes, \ measured and shown", WHITE),
            (r"so systems are tuned to a level as well as a curve: \ a meter at the desk, \ a log of the night", WHITE),
            (r"for musicians: \ custom earplugs, \ in-ear monitors at modest levels, \ quieter stages", WHITE),
            (r"and the trend runs the right way: \ arrays put the level where the audience is, \ not on the stage or in the front row", TUNE),
        ]
        rows_scene(self, r"rules and remedies", items,
                   "There are rules. <bookmark mark='b'/> Workers are protected by law: in the European Union from eighty-five "
                   "decibels a day under the noise directive of 2003, and in Britain the music and entertainment industry has been "
                   "covered since 2008. <bookmark mark='c'/> Audiences have guidelines, not limits: the World Health "
                   "Organization's standard of 2022 for venues and events asks for no more than a hundred decibels averaged over any "
                   "fifteen minutes, measured and displayed. <bookmark mark='d'/> So systems are tuned to a level as well as a "
                   "curve, with a meter at the desk and a log of the night. <bookmark mark='e'/> For musicians: custom earplugs, "
                   "in-ear monitors at modest levels, quieter stages. <bookmark mark='f'/> And the trend runs the right way: modern "
                   "arrays put the level where the audience is, evenly, not on the stage or in the front row.", marks="bcdef")
