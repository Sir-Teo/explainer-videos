from __future__ import annotations

from videos.music.music65.common import *  # noqa: F403
from videos.music.variations import rows_before


class Outro(SoundScene):
    def construct(self):
        self.variation()
        self.ledger()
        self.recap()
        self.problems()
        self.payoffs()
        self.next_part()

    # ------------------------------------------------------------------
    def variation(self):
        d = load("tune65")
        c = clip("tune.variation65")
        st = d["starts"]
        keys = d["names"]
        head = VGroup(label(r"Variation 65", font_size=48, color=TUNE), label(r"continued by a machine", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(RoundedRectangle(width=2.2, height=1.1, corner_radius=0.12, stroke_color=TUNE),
                                label(rf"temperature {t:g}", font_size=16, color=TUNE)).arrange(ORIGIN) for t in d["temps"]]).arrange(RIGHT, buff=0.2).move_to(UP * 0.4)
        rolls = VGroup(*[tune_roll(d["opening"] + cont, width=2.2, height=0.9, marks=(len(d["opening"]), len(cont)), mark_color=EAR) for cont in d["continuations"]])
        for r, cell in zip(rolls, cells):
            r.next_to(cell, DOWN, buff=0.3)
        note = label(r"the Tune's first phrase \ (gold), \ then one draw at each temperature \ (red): \ uncurated, \ in the order drawn", font_size=17, color=GREY_A).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here the transformer "
            "hears the Tune's first phrase and continues it, once at each of five temperatures, from a quarter to one and a "
            "half. These are the first draws, uncurated: what the machine wrote, not what we liked."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(rolls), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"Variation 65", kind="synthesized", detail=r"the Tune; \ the transformer", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        d = load("tune65")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover(
            f"Row sixty-five of the ledger: five temperatures, and the longest run any continuation copied from Bach, "
            f"{say(max(d['copies']))} notes. The Tune is not a chorale, and the machine, which knows only chorales, answers it "
            "in the only language it has."
        ):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"composing machines: \ rules, \ chance, \ and statistics learnt from music",
            r"a Markov chain's order trades prediction for copying; \ order 2 predicts Bach best",
            r"order 8 copies whole chorales; \ Bach's own tunes share about a tenth",
            r"constraints sample exactly what must be true; \ recombination copies on purpose",
            r"a small transformer needs transposed data to beat its own memory",
            r"judge with uncurated samples, \ likelihood, \ copying and listeners",
        ], title=r"What we found", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Composing machines follow rules, shape chance, or learn statistics from music. "
            "<bookmark mark='a'/> A Markov chain's order trades prediction for copying, and order two predicts Bach best. "
            "<bookmark mark='b'/> Order eight copies whole chorales, where Bach's own tunes share about a tenth of their notes "
            "in copied runs. <bookmark mark='c'/> Constraints let a chain sample exactly what must be true, and recombination "
            "copies on purpose. <bookmark mark='d'/> A small transformer, given little music, memorizes; transposed copies "
            "make it learn instead. <bookmark mark='e'/> And a composing machine should be judged by uncurated samples, "
            "likelihood, copying and listeners together."
        ) as vo:
            self.play(FadeIn(card.head), FadeIn(card.rows[0]))
            for mark, rr in zip("abcde", card.rows[1:]):
                vo.wait_until(mark)
                self.play(FadeIn(rr), run_time=0.5)
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def problems(self):
        ps = problem_set([
            r"A corpus has 7,000 notes and 146 distinct notes. \ Roughly how many order-3 contexts are possible, \ and how many can it have seen?",
            r"Show that sampling forward with weights $P(x \mid s)\,\beta_{k-1}(s')$ draws exactly from the chain conditioned on the constraints.",
            r"\textbf{Ear.} \ The lab plays tunes from orders 1 to 6 in random order; \ rank them by how Bach-like they sound, \ then check how much each copied.",
            r"\textbf{Build.} \ Add a maximum-order constraint: \ forbid any run of more than 6 notes copied from one tune, \ and measure the cost in bits.",
            r"$\bigstar$ \ Is there a frontier of novelty against quality, \ and can a model be moved past it?",
        ], font_size=21)
        with self.voiceover(
            "Five problems. One to compute, one to prove, one for your ears, one to build, and a research problem, marked "
            "with a star. Solutions are in this part's notes. Pause here."
        ):
            self.play(FadeIn(ps.head), LaggedStart(*[FadeIn(r) for r in ps.rows], lag_ratio=0.25), run_time=3.0)
        self.wait(5.0)
        self.clear_scene()

    # ------------------------------------------------------------------
    def payoffs(self):
        pay = payoff_card([
            (r"generative audio: \ the same next-token idea, \ on sound itself", [66]),
            (r"research: \ evaluation, \ leakage and listening tests", [67]),
            (r"the concert: \ the Variations, \ some of them machine-made, \ labelled", [68]),
        ], font_size=25)
        with self.voiceover(
            "Where does this come back? In generative audio, where the same next-token idea runs on sound itself. In research, "
            "with evaluation, leakage and listening tests. And in the concert at the end, where some Variations were made by "
            "machines, and are labelled so."
        ):
            self.play(FadeIn(pay.head), LaggedStart(*[FadeIn(r) for r in pay.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"split by work", r"the same tune twice is a test already seen"),
            (r"measure copying", r"longest run and copied share, \ beside the real music's"),
            (r"show uncurated output", r"and say how many samples there were"),
            (r"know the data", r"whose music trained it, \ and on what terms"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. Split data by work, because the same tune twice is a test already seen. Measure copying, with "
            "real music's copying beside it. Show uncurated output, and say how many samples there were. And know the data: "
            "whose music trained the model, and on what terms."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"J.-P. Briot, \ G. Hadjeres and F.-D. Pachet, \ \textit{Deep Learning Techniques for Music Generation} \ (2020)",
             r"L. A. Hiller and L. M. Isaacson, \ \textit{Experimental Music} \ (1959)",
             r"D. Cope, \ \textit{Experiments in Musical Intelligence} \ (1996)",
             r"D. Hofstadter, \ `Staring Emmy straight in the eye' \ (in Cope, \ \textit{Virtual Music}, \ 2001)"],
            [r"F. Pachet and P. Roy, \ `Markov constraints' \ (\textit{Constraints}, \ 2011)",
             r"A. Papadopoulos, \ P. Roy and F. Pachet, \ `Avoiding plagiarism in Markov sequence generation' \ (AAAI, \ 2014)",
             r"G. Hadjeres, \ F. Pachet and F. Nielsen, \ `DeepBach' \ (ICML, \ 2017)",
             r"C.-Z. A. Huang et al., \ `Music Transformer' \ (ICLR, \ 2019)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        top = label(r"Act XI: \ listening machines", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"2016: \ a network writes sound itself, \ sixteen thousand decisions a second, \ and its piano noodles nowhere.", font_size=22, color=WHITE).move_to(UP * 1.7)
        q = label(r"a few years later, \ a sentence returns a finished song. \ \ What closed the gap?", font_size=27, color=EAR).move_to(UP * 0.4)
        nxt = VGroup(label(r"Part 66", font_size=32, color=GREY_B), label(r"Generative Audio", font_size=46, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "2016: a network writes sound itself, sixteen thousand decisions a second, and its piano noodles nowhere. "
            "<bookmark mark='a'/> A few years later a sentence returns a finished song, singer and all. What closed the gap? "
            "<bookmark mark='b'/> Next time. Part 66: Generative Audio."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
