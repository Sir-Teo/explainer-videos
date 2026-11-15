from __future__ import annotations

from videos.music.music67.common import *  # noqa: F403
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
        d = load("tune67")
        s = load("stemma")
        c = clip("tune.variation67")
        st = d["starts"]
        keys = d["names"]
        names = {"original": r"as written", "witness": rf"the worst copy: \ {d['witness_errors']} notes wrong", "rebuilt": rf"rebuilt from {s['n_survive']} copies"}
        head = VGroup(label(r"Variation 67", font_size=48, color=TUNE), label(r"a critical edition", font_size=30, color=GREY_A)).arrange(RIGHT, buff=0.5, aligned_edge=DOWN).to_edge(UP, buff=0.3)
        cells = VGroup(*[VGroup(RoundedRectangle(width=3.6, height=1.2, corner_radius=0.12, stroke_color=TUNE),
                                label(names[k], font_size=17, color=TUNE)).arrange(ORIGIN) for k in keys]).arrange(RIGHT, buff=0.3).move_to(DOWN * 0.2)
        note = label(r"the Tune as a lost original, \ known only through a simulated tradition of copies, \ and edited back", font_size=17, color=GREY_A).next_to(cells, DOWN, buff=0.45)
        with self.voiceover(
            "Every part ends by doing something to the Tune with what it built. <bookmark mark='a'/> Here the Tune becomes a "
            "lost original, known only through a tradition of copies, and is edited back: its critical edition. Hear it as "
            "written, as its most corrupt copy has it, and as rebuilt."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(cells), FadeIn(note))
        with self.listen(c) as snd:
            window(snd, r"Variation 67", kind="physical model", detail=r"Part 38's piano", corner=DL, tag_corner=DR)
            for i, k in enumerate(keys):
                end = st[keys[i + 1]] - 0.3 if i + 1 < len(keys) else c.duration
                pulse(snd, cells[i], st[k], end, buff=0.06)
        self.wait(0.3)
        self.clear_scene()

    # ------------------------------------------------------------------
    def ledger(self):
        v = load("variation")
        rws = (rows_before(PART) + [{"part": v["part"], "title": v["title"], "seconds": v["seconds"], "measure": v["measure"]}])[-6:]
        led = variations_ledger(rws, highlight=(len(rws) - 1,)).move_to(DOWN * 0.2)
        head = label(r"the Variations ledger", font_size=26, color=GREY_A).to_edge(UP, buff=0.4)
        with self.voiceover("Row sixty-seven of the ledger. One row is left, and it is not a variation like the others."):
            self.play(FadeIn(head), FadeIn(led, shift=UP * 0.2))
        self.wait(0.6)
        self.clear_scene()

    # ------------------------------------------------------------------
    def recap(self):
        card = objectives_card([
            r"six kinds of knowing, \ each with its failure and its check",
            r"shared errors recover a manuscript family, \ and its lost original",
            r"a rule measured on a canon is a rule about the canon",
            r"selective publication leaves a funnel with a bite: \ the first result is the luckiest",
            r"listening tests need trials: \ a 60\% listener needs 158",
            r"split by what repeats; \ re-run verdicts and report the spread",
        ], title=r"What we found", font_size=20).move_to(DOWN * 0.1)
        with self.voiceover(
            "What did we find? Music research knows in six ways, each with its failure and its check. <bookmark mark='a'/> "
            "Shared errors recover a family of manuscripts and its lost original. <bookmark mark='b'/> A rule measured on a "
            "canon is a rule about the canon. <bookmark mark='c'/> Selective publication leaves a funnel with a bite out of it, "
            "and the first result is usually the luckiest. <bookmark mark='d'/> Listening tests need many trials. "
            "<bookmark mark='e'/> And data must be split by what repeats, with verdicts re-run and their spread reported, "
            "including this series' own."
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
            r"A listener hears a difference 70\% of the time. \ How many ABX trials give 80\% power at the 5\% level?",
            r"Show that, \ if study $i$ is published only when $\hat\theta_i / s_i > 1.96$, \ small published studies overestimate $\theta$ most.",
            r"\textbf{Ear.} \ The lab plays the Tune, \ its worst copy and the rebuilt original; \ find the wrong notes by ear, \ then check.",
            r"\textbf{Build.} \ Add contamination to the manuscript tradition \ (a scribe copying from two exemplars) \ and test the tree.",
            r"$\bigstar$ \ Build an open benchmark of the verdicts of music research, \ re-run each year.",
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
            (r"the concert: \ every Variation, \ with its sources and its errata", [68]),
        ], font_size=25)
        with self.voiceover("Where does this come back? In the concert at the end, where every Variation is heard with its sources and its corrections."):
            self.play(FadeIn(pay.head), FadeIn(pay.rows))
        self.wait(0.4)
        self.clear_scene()
        prac = practice_card([
            (r"one sentence", r"state the claim, \ and what would refute it"),
            (r"plan the power", r"before the data, \ not after"),
            (r"split by what repeats", r"tunes, \ recordings, \ performers"),
            (r"report the spread", r"many runs, \ and the ones that failed"),
        ], font_size=25)
        with self.voiceover(
            "And in practice. State the claim in one sentence, with what would refute it. Plan the power before the data. "
            "Split by whatever can repeat: tunes, recordings, performers. And report the spread of many runs, including the ones "
            "that failed."
        ):
            self.play(FadeIn(prac.head), LaggedStart(*[FadeIn(r) for r in prac.rows], lag_ratio=0.3), run_time=3.0)
        self.wait(0.4)
        self.clear_scene()
        refs = reference_card(
            [r"E. Clarke and N. Cook \ (eds.), \ \textit{Empirical Musicology} \ (2004)",
             r"B. Nettl, \ \textit{The Study of Ethnomusicology} \ (3rd ed., \ 2015)",
             r"J. Grier, \ \textit{The Critical Editing of Music} \ (1996)",
             r"F. H. Rauscher, \ G. L. Shaw and K. N. Ky, \ `Music and spatial task performance' \ (\textit{Nature}, \ 1993)"],
            [r"C. F. Chabris, \ `Prelude or requiem for the ``Mozart effect''?' \ (\textit{Nature}, \ 1999)",
             r"J. Pietschnig, \ M. Voracek and A. K. Formann, \ `Mozart effect--Shmozart effect' \ (\textit{Intelligence}, \ 2010)",
             r"B. L. Sturm, \ `The GTZAN dataset' \ (2013); \ `A simple method to determine if a MIR system is a horse' \ (2014)",
             r"N. Saitou and M. Nei, \ `The neighbor-joining method' \ (1987)"],
            font_size=18)
        with self.voiceover("The books and papers this part follows. The full list, with notes, is in the README."):
            self.play(FadeIn(refs))
        self.wait(1.5)
        self.clear_scene()

    # ------------------------------------------------------------------
    def next_part(self):
        top = label(r"Act XII: \ coda", font_size=30, color=GREY_A).to_edge(UP, buff=0.8)
        lead = label(r"Bach's \textit{Goldberg Variations} end by playing the opening aria again, \ the same notes.", font_size=22, color=WHITE).move_to(UP * 1.7)
        q = label(r"it does not sound the same. \ \ What has changed is the listener.", font_size=27, color=EAR).move_to(UP * 0.4)
        nxt = VGroup(label(r"Part 68", font_size=32, color=GREY_B), label(r"The Variations", font_size=46, color=TUNE)).arrange(DOWN, buff=0.2).to_edge(DOWN, buff=0.8)
        with self.voiceover(
            "Bach's Goldberg Variations end by playing the opening aria again, the same notes. <bookmark mark='a'/> It does not "
            "sound the same: what has changed is the listener. <bookmark mark='b'/> Next time, the last part. Part 68: The "
            "Variations."
        ) as vo:
            self.play(FadeIn(top), FadeIn(lead))
            vo.wait_until("a")
            self.play(FadeIn(q))
            vo.wait_until("b")
            self.play(FadeIn(nxt, shift=UP * 0.2))
        self.wait(1.0)
        self.clear_scene()
