from __future__ import annotations

from videos.psychology.psych13.common import *  # noqa: F403


class Ledger(VoiceoverScene):
    def construct(self):
        self.card()
        self.quanta()
        self.rate()
        self.orientation()
        self.csf()
        self.dress()

    def card(self):
        card = chapter_card(13, r"The Ledger", r"What happened when today's findings were checked?", lit=(),
                            part=PART, scale=("mind",), marr=("what",))
        with self.voiceover("Chapter thirteen. The Ledger."):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    @staticmethod
    def _row(key):
        return {f.key: f for f in ledger.rows(part=PART)}[key]

    def _show(self, card, vo, marks="abcd"):
        self.play(FadeIn(card.box), FadeIn(card.tag), FadeIn(card.claim))
        vo.wait_until(marks[0])
        self.play(FadeIn(card.original, shift=RIGHT * 0.15))
        vo.wait_until(marks[1])
        self.play(LaggedStart(*[FadeIn(r, shift=RIGHT * 0.15) for r in card.record], lag_ratio=0.6), run_time=1.5)
        vo.wait_until(marks[2])
        self.play(FadeIn(card.note))
        vo.wait_until(marks[3])
        self.play(FadeIn(card.status, scale=1.3))

    def quanta(self):
        card = ledger_card(self._row("few_quanta"), width=12.8, font_size=25)
        with self.voiceover(
            "Five rows today. The first: a fully dark-adapted eye sees a flash when only a handful of quanta, roughly "
            "five to fourteen, are absorbed, spread so thinly that a rod must respond to a single quantum. <bookmark mark='a'/> The original: "
            "Hecht, Shlaer and Pirenne, 1942. <bookmark mark='b'/> The record: Baylor, Lamb and Yau's single rods in "
            "1979, and in 2016 the single-photon experiment, with its fifty-one point six percent. "
            "<bookmark mark='c'/> The note matters. That a few quanta suffice, and that a rod answers one, is "
            "settled and has been repeated many times. That a person can report a single photon rests on one study, "
            "whose overall result sat at the edge of significance, and nobody has yet repeated it directly. "
            "<bookmark mark='d'/> For the claim as stated: replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def rate(self):
        card = ledger_card(self._row("rate_code"), width=12.8, font_size=25)
        with self.voiceover(
            "The second, carried over from Part 5. The claim: a single sensory fibre signals the strength of a "
            "stimulus by how often it fires, not by the size of its impulses, and its rate falls during a steady "
            "stimulus. <bookmark mark='a'/> The original: Adrian and Zotterman, 1926. <bookmark mark='b'/> The "
            "record: Hartline and Graham found the same in a single fibre from the horseshoe crab's eye in 1932, "
            "and it's been found in every sense since. <bookmark mark='c'/> With a qualification: rate isn't the "
            "only code. The timing of the first spike, and the pattern across many fibres, carry information too. "
            "<bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def orientation(self):
        card = ledger_card(self._row("orientation_cells"), width=12.8, font_size=25)
        with self.voiceover(
            "The third. The claim: neurons in primary visual cortex respond best to an edge or a bar at one "
            "orientation, and simple cells' fields are built from aligned centre-surround inputs. "
            "<bookmark mark='a'/> The original: Hubel and Wiesel, 1959. <bookmark mark='b'/> The record: the same cells in "
            "monkeys, in 1968, and Reid and Alonso's paired recordings in 1995, built on Kuffler's centre and "
            "surround. <bookmark mark='c'/> Orientation tuning has been confirmed in every mammal with a visual "
            "cortex that's been studied. The hierarchy holds as a first approximation, and the frontier will say "
            "how much it leaves out. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def csf(self):
        card = ledger_card(self._row("csf_channels"), width=12.8, font_size=25)
        with self.voiceover(
            "The fourth. The claim: sensitivity to contrast is band-pass, peaking at a few cycles per degree, and "
            "adapting to one grating lowers sensitivity mainly near its own frequency and orientation. "
            "<bookmark mark='a'/> The original: Campbell and Robson, 1968. <bookmark mark='b'/> The record: Blakemore "
            "and Campbell's adaptation in 1969, and the quick estimates of Lesmes and colleagues in 2010, which "
            "recover the same shape in about fifty trials. <bookmark mark='c'/> It's one of the best-replicated curves "
            "in vision, and it's used in clinics. Whether the channels are truly separate mechanisms or a convenient "
            "description is still discussed. <bookmark mark='d'/> Replicated."
        ) as vo:
            self._show(card, vo)
        self.wait(1.0)
        self.clear_scene()

    def dress(self):
        card = ledger_card(self._row("dress_illuminant"), width=12.8, font_size=25)
        total = len(ledger.rows(upto=PART))
        tally = label(rf"the Ledger so far: \ {total} rows", font_size=28, color=GREY_A).to_edge(DOWN, buff=0.4)
        if card.get_bottom()[1] < tally.get_top()[1] + 0.2:
            card.shift(UP * (tally.get_top()[1] + 0.2 - card.get_bottom()[1]))
        with self.voiceover(
            "The fifth. The claim: people who see the dress as white and gold, rather than blue and black, are "
            "assuming it's lit by bluish light, and discounting it. <bookmark mark='a'/> The original: Lafer-Sousa, "
            "Hermann and Conway, 2015. <bookmark mark='b'/> The record: Wallisch's two large surveys, and Witzel, "
            "Racey and O'Regan, both in 2017. <bookmark mark='c'/> Three groups, with different methods, tie the "
            "split to assumptions about the light. Why people differ in those assumptions is less settled. "
            f"<bookmark mark='d'/> Replicated. <bookmark mark='e'/> That makes {total} rows. Five today, all "
            "replicated, with one honest asterisk: the single photon. Vision science has more replicated findings than "
            "most of psychology, partly because it can measure in physics' units."
        ) as vo:
            self._show(card, vo)
            vo.wait_until("e")
            self.play(FadeIn(tally, shift=UP * 0.15))
        self.clear_scene()
