from __future__ import annotations

import numpy as np

from videos.psychology.psych12.common import *  # noqa: F403
from videos.psychology.psych12.s04_roc import roc_axes


class Practice(VoiceoverScene):
    def construct(self):
        self.card()
        self.everywhere()
        self.readers()
        self.lineups()
        self.classifier()

    def card(self):
        card = chapter_card(13, r"In practice: \ screening, \ alarms and classifiers",
                            r"Where does this theory run every day?", lit={2000: r"Swets, Dawes and Monahan"}, part=PART,
                            scale=("person", "group"), marr=("what",))
        with self.voiceover(
            "Chapter thirteen. In practice: screening, alarms and classifiers."
        ):
            self.play(FadeIn(card, shift=UP * 0.2))
        self.clear_scene()

    def everywhere(self):
        head = heading(r"The same picture everywhere")
        data = [
            (r"radiology", r"a tumour", r"normal tissue", r"how suspicious before a recall"),
            (r"airport screening", r"a weapon", r"bags full of clutter", r"how sure before a bag search"),
            (r"smoke alarms", r"a fire", r"toast, steam", r"the sensor's setting"),
            (r"spam filters", r"spam", r"real mail", r"the score that sends to junk"),
            (r"hiring", r"a good employee", r"an applicant who would not be", r"the bar for an offer"),
        ]
        widths = [3.0, 2.4, 3.2, 4.0]
        cols = [WHITE, SIGNALC, NOISEC, CRIT]
        table = VGroup()
        hdr = [r"field", r"signal", r"noise", r"criterion"]
        for r, row in enumerate([hdr] + data):
            g = VGroup()
            x = -6.3
            for c, (txt, w) in enumerate(zip(row, widths)):
                t = wrapped_label(txt, w - 0.2, 24 if r else 25, GREY_A if r == 0 else cols[c])
                t.move_to([x + w / 2, 2.3 - 0.75 * r, 0])
                g.add(t)
                x += w
            table.add(g)
        rows = rows_of([
            (r"two jobs in every row: \ raise $d'$ (better instruments, \ two readers), \ and set $c$ (whose costs?)",
             THRESH),
            (r"Swets, \ Dawes and Monahan (2000): \ the decision process is the same across these fields, \ and so are "
             r"the tools to improve it", DATA),
        ], 12.4, 27, 0.24).to_edge(DOWN, buff=0.8)
        tag = published_tag(archive.SWETS_2000.cite)
        with self.voiceover(
            "Once you see the two distributions and the line, you see them everywhere. <bookmark mark='a'/> A "
            "radiologist looks for a tumour among normal tissue and decides how suspicious a shadow must be before "
            "a woman is called back. An airport screener looks for a weapon among clutter. A smoke alarm must tell "
            "a fire from toast. A spam filter scores every message and has a line for the junk folder. And a "
            "hiring panel has a bar for an offer. <bookmark mark='b'/> In every row there are two separate jobs. "
            "Raise d prime: better instruments, a second reader, more information. And set the criterion, which is "
            "a question about costs and therefore about values: who pays for a miss, and who for a false alarm? "
            "<bookmark mark='c'/> In 2000, John Swets, Robyn Dawes and John Monahan wrote a report arguing that this "
            "decision process is the same across fields, and that the tools of this part improve it in all of them."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(table[0]))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(r) for r in table[1:]], lag_ratio=0.6), run_time=6.0)
            vo.wait_until("b")
            self.play(FadeIn(rows[0]))
            vo.wait_until("c")
            self.play(FadeIn(rows[1]))
        self.clear_scene()

    def readers(self):
        d = load("readers")
        head = heading(r"Two readers: \ raise $d'$, \ or move $c$?")
        A = axes([0, 1], [1.4, 2.2], x_length=5.6, y_length=3.6, xticks=[0, 0.5, 1], yticks=[1.5, 1.75, 2.0],
                 xfmt=lambda v: f"{v:g}", yfmt=lambda v: f"{v:g}", xlabel=r"how correlated the two readers' errors are",
                 ylabel=r"$d'$ of the averaged judgement", center=[-3.3, -0.2, 0])
        ax = A.ax
        c = curve(ax, d["rho"], d["avg"], MODEL, stroke_width=5)
        one = DashedLine(ax.c2p(0, d["d"]), ax.c2p(1, d["d"]), color=GREY_B, stroke_width=2)
        ol = label(rf"one reader, \ $d' = {d['d']:.1f}$", font_size=22, color=GREY_B).next_to(ax.c2p(0.62, d["d"]), UP, buff=0.08)
        rows = rows_of([
            (rf"average two independent readings: \ $d' = {d['d']:.1f}\sqrt2 = {d['avg_0']:.2f}$", MODEL),
            (rf"but readers err alike: \ correlated at 0.5, \ {d['avg_05']:.2f}; \ fully, \ no gain", MODEL),
            (rf"``recall if either says yes'': \ hits {pct(d['one_h'])} $\to$ {pct(d['either_h'])}, \ false alarms "
             rf"{pct(d['one_f'])} $\to$ {pct(d['either_f'])}", FA),
            (rf"``recall only if both say yes'': \ hits {pct(d['both_h'])}, \ false alarms {pct(d['both_f'])}", HIT),
            (r"the either and both rules mostly move the criterion; \ only combining evidence raises $d'$", THRESH),
        ], 5.2, 25, 0.28).move_to([3.7, 0.0, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ two readers, \ each $d' = 1.5$")
        with self.voiceover(
            "Many screening programmes have each image read twice. What does the second reader buy? "
            "<bookmark mark='a'/> If the two readers' judgements were averaged, and their errors were independent, "
            f"d prime would grow by root two, from {d['d']:.1f} to {d['avg_0']:.2f}. <bookmark mark='b'/> But "
            "readers trained alike tend to err alike. With their errors correlated at a half, the gain shrinks to "
            f"{d['avg_05']:.2f}, and if they always agree, there's none. <bookmark mark='c'/> And programmes often "
            "don't average. A common rule recalls a patient if either reader says yes. Hits rise, from "
            f"{100 * d['one_h']:.0f} to {100 * d['either_h']:.0f} percent, but false alarms rise too, from "
            f"{100 * d['one_f']:.0f} to {100 * d['either_f']:.0f}. <bookmark mark='d'/> Recall only if both say "
            "yes, and the opposite happens. <bookmark mark='e'/> Those two rules mostly slide the criterion. Only "
            "combining the evidence itself raises d prime. Detection theory makes that distinction a calculation."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(A), Create(one), FadeIn(ol))
            vo.wait_until("a")
            self.play(Create(c), FadeIn(rows[0]), run_time=2.0)
            for m, r in zip("bcde", rows[1:]):
                vo.wait_until(m)
                self.play(FadeIn(r))
        self.clear_scene()

    def lineups(self):
        d = load("lineups")
        src = archive.MICKES_2012
        head = heading(r"Police line-ups: \ a ratio that misled")
        R = roc_axes([-3.3, -0.25, 0], size=4.6, xlabel=r"false identifications", ylabel=r"correct identifications")
        rx = R.ax
        diag = DashedLine(rx.c2p(0, 0), rx.c2p(1, 1), color=GREY_C, stroke_width=2)
        roc = curve(rx, d["fa"], d["hit"], ROCC, stroke_width=4)
        lines, dots = VGroup(), VGroup()
        for name, col in (("lax", HIT), ("strict", CRIT)):
            f, h, r = d[name]
            dots.add(Dot(rx.c2p(f, h), radius=0.09, color=col))
            end = min(1.0, 1.0 / r)
            lines.add(DashedLine(rx.c2p(0, 0), rx.c2p(end, end * r), color=col, stroke_width=2.5))
        labs = VGroup(label(rf"ratio {d['lax'][2]:.1f}", font_size=22, color=HIT).next_to(dots[0], RIGHT, buff=0.1),
                      label(rf"ratio {d['strict'][2]:.1f}", font_size=22, color=CRIT).next_to(dots[1], RIGHT, buff=0.1))
        rows = rows_of([
            (r"a line-up's old score: \ correct identifications over false ones, \ the diagnosticity ratio", WHITE),
            (r"one witness, \ one memory: \ a more cautious criterion raises the ratio with no gain in $d'$", CRIT),
            (rf"sequential line-ups (faces one at a time) scored higher: \ {d['ratio_seq']:.1f} against "
             rf"{d['ratio_sim']:.1f}, \ and were widely recommended", DATA),
            (r"Mickes, \ Flowe and Wixted (2012): \ by ROC, \ witnesses told guilty from innocent better in "
             r"simultaneous line-ups", ROCC),
            (r"the sequential line-up made witnesses cautious, \ not more accurate; \ the dispute continues (Part 21)",
             THRESH),
        ], 5.0, 25, 0.28).move_to([3.8, -0.1, 0])
        keep_in_frame(rows)
        tags = VGroup(published_tag(src.cite), psyche_tag(r"the curve: \ $d' = 1.2$, \ for illustration"))
        with self.voiceover(
            "The sharpest recent use of this theory was in the courtroom's waiting room: the police line-up. "
            "<bookmark mark='a'/> For decades, line-up procedures were scored by a ratio: correct identifications "
            "of the guilty person divided by false identifications of an innocent one. <bookmark mark='b'/> Here's "
            "the trouble. Take one witness with one memory, and move only the criterion. A more cautious witness "
            f"has a higher ratio, {d['strict'][2]:.1f} against {d['lax'][2]:.1f}, with exactly the same ability "
            "to tell guilty from innocent. <bookmark mark='c'/> Sequential line-ups, showing faces one at a time, "
            "scored the higher ratio and were widely recommended. <bookmark mark='d'/> In 2012 Laura Mickes, Heather "
            "Flowe and John Wixted measured the whole ROC instead. Simultaneous line-ups came out better at telling "
            "guilty from innocent. <bookmark mark='e'/> The sequential procedure had made witnesses more cautious, "
            "not more accurate. The argument over what this means for policy is still going, and Part 21 takes it "
            "up. But the lesson is chapter one's: a single number that mixes seeing with saying can point the wrong "
            "way."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tags), FadeIn(R), Create(diag), Create(roc))
            vo.wait_until("a")
            self.play(FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(dots), Create(lines), FadeIn(labs), FadeIn(rows[1]))
            for m, r in zip("cde", rows[2:]):
                vo.wait_until(m)
                self.play(FadeIn(r))
        self.clear_scene()

    def classifier(self):
        d = load("classifier")
        head = heading(r"Machine learning's ROC, \ and its blind spot")
        R = roc_axes([-4.0, -0.2, 0], size=3.8)
        rx = R.ax
        roc = curve(rx, d["fa"], d["hit"], ROCC, stroke_width=4)
        diag = DashedLine(rx.c2p(0, 0), rx.c2p(1, 1), color=GREY_C, stroke_width=2)
        P_ = roc_axes([1.0, -0.2, 0], size=3.8, xlabel=r"recall (hit rate)", ylabel=r"precision")
        px = P_.ax
        keep = d["hit"] > 0.02
        pc = curve(px, d["hit"][keep], d["precision_common"][keep], HIT, stroke_width=4)
        pr = curve(px, d["hit"][keep], d["precision_rare"][keep], MISS, stroke_width=4)
        lg = legend([(HIT, r"half the mail is spam"), (MISS, r"1 message in 100")], font_size=21).move_to(px.c2p(0.45, 0.55))
        tr = label(r"the same at any base rate", font_size=22, color=ROCC).next_to(R, UP, buff=0.15)
        rows = rows_of([
            (rf"a filter with $d' = 2$: \ area under the ROC {d['auc']:.2f}", ROCC),
            (r"the ROC ignores the base rate: \ the same curve either way", ROCC),
            (rf"precision, \ the share of flagged mail that is spam, \ at 80\% recall: \ "
             rf"{pct(d['prec_at_80_common'])} or {pct(d['prec_at_80_rare'])}", MISS),
            (r"for rare targets, \ report both curves: \ chapter 9 in another language", THRESH),
        ], 3.4, 24, 0.28).move_to([5.3, -0.1, 0])
        keep_in_frame(rows)
        tag = psyche_tag(r"computed: \ scores normal with $d' = 2$")
        with self.voiceover(
            "The ROC left psychology long ago. Medicine adopted it, and machine learning scores most classifiers by "
            "the area under it. <bookmark mark='a'/> Here's a spam filter whose scores separate spam from real mail "
            f"with d prime two: an area of {d['auc']:.2f}. <bookmark mark='b'/> The ROC doesn't depend on how much "
            "spam there is; it's built from two rates that are each conditioned on the truth. That's its strength, "
            "and its blind spot. <bookmark mark='c'/> Plot instead precision, the share of flagged messages that "
            "really are spam, against recall, the hit rate. When half the mail is spam, at eighty percent recall "
            f"the filter is right {100 * d['prec_at_80_common']:.0f} percent of the time. When one message in a "
            f"hundred is spam, it's right {100 * d['prec_at_80_rare']:.0f} percent of the time: the junk folder is "
            "mostly real mail. <bookmark mark='d'/> It's chapter nine's mammogram in another language. For rare "
            "targets, report both curves."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tag), FadeIn(R), Create(diag))
            vo.wait_until("a")
            self.play(Create(roc), FadeIn(rows[0]))
            vo.wait_until("b")
            self.play(FadeIn(tr), FadeIn(rows[1]))
            vo.wait_until("c")
            self.play(FadeIn(P_), Create(pc), Create(pr), FadeIn(lg), FadeIn(rows[2]), run_time=2.0)
            vo.wait_until("d")
            self.play(FadeIn(rows[3]))
        self.clear_scene()
