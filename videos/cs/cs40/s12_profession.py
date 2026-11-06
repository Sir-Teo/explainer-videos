from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table)


class Profession(VoiceoverScene):
    def construct(self):
        self.card()
        self.licenses()
        self.failures()
        self.obligations()

    def card(self):
        card = chapter_card(11, r"The profession", r"What do software engineers owe, \ and to whom?",
                            lit=(1985, 2018), extra=((1989, r"the GNU GPL"), (1992, r"the ACM Code of Ethics"),
                                                     (2018, r"the GDPR")), part=PART)
        with self.voiceover("Chapter eleven. The profession."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def licenses(self):
        head = label(r"Licenses and open source", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"permissive", r"MIT, \ BSD, \ Apache 2.0", r"use, \ change, \ sell; \ keep the notice \ (Apache: "
                 r"also a patent grant)"],
                [r"weak copyleft", r"LGPL, \ MPL", r"changes to \textit{these files} must stay open"],
                [r"copyleft", r"GPL", r"distribute a derived program, \ distribute its source under the GPL"],
                [r"network copyleft", r"AGPL", r"running it as a service counts as distributing"]]
        tab = grid_table([r"kind", r"examples", r"the obligation"], rows, widths=[2.6, 3.0, 7.0], row_h=0.58,
                         font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.55).set_x(0)
        for i, c in zip(range(1, 5), (YES, HEAD, NO, NO)):
            tab.cells[i][0].set_color(c)
        lines = VGroup(
            wrapped_label(r"almost every program today is mostly other people's code: \ dependency licenses are "
                          r"legal obligations, \ checked in the build \ (Part 41)", 12.4, font_size=21, color=WHITE),
            wrapped_label(r"the economics: \ a few volunteers maintain code that much of industry relies on; \ the "
                          r"2014 Heartbleed bug sat in OpenSSL, \ then kept up by a handful of people", 12.4,
                          font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(tab, DOWN, buff=0.45)
        with self.voiceover(
            "Almost every program written today is mostly other people's code, and that code comes with licenses. "
            "<bookmark mark='a'/> Permissive licenses, like MIT, BSD and Apache, let anyone use, change and sell the "
            "code, asking mainly that the notice be kept. Weak copyleft, like the LGPL, keeps changes to those "
            "particular files open. The GPL, Richard Stallman's copyleft, requires anyone who distributes a derived "
            "program to share its source on the same terms, and the AGPL extends that to programs offered as a "
            "service. <bookmark mark='b'/> These are legal obligations, and builds check them, as Part 41 will. "
            "<bookmark mark='c'/> And there is an economic oddity: code that much of industry depends on is often "
            "maintained by a few volunteers. When the Heartbleed bug was found in OpenSSL in 2014, the library that "
            "secured a large part of the web was being maintained by a handful of people."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def obligations(self):
        head = label(r"Obligations beyond the code", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{privacy by design}: \ collect only what the purpose needs \ (minimization), \ use "
                          r"it only for that purpose, \ delete it when done \ (the EU's GDPR, 2018)", 12.4,
                          font_size=23, color=HEAD),
            wrapped_label(r"\textbf{accessibility}: \ software that works with screen readers, \ keyboards and "
                          r"captions \ (WCAG); \ a legal duty in many countries, \ and part of quality", 12.4,
                          font_size=23, color=YES),
            wrapped_label(r"\textbf{safety}: \ the Therac-25 radiation machine \ (1985--87) \ overdosed patients "
                          r"after a race condition replaced hardware interlocks \ (Leveson and Turner, 1993)", 12.4,
                          font_size=23, color=NO),
            wrapped_label(r"\textbf{the ACM Code of Ethics}: \ contribute to society, \ avoid harm, \ be honest, \ "
                          r"respect privacy, \ and give comprehensive reviews of systems and their risks", 12.4,
                          font_size=23, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "A profession has obligations beyond the code. <bookmark mark='a'/> Privacy by design: collect only the "
            "data a purpose needs, use it only for that purpose, and delete it when done, principles that the "
            "European Union's data protection regulation made law in 2018. <bookmark mark='b'/> Accessibility: "
            "software that works with screen readers, keyboards alone and captions, which many countries require "
            "and every user benefits from. <bookmark mark='c'/> Safety: in the nineteen eighties the Therac-25 "
            "radiation machine gave massive overdoses to patients, after software, with a race condition of the kind "
            "Part 33 studied, replaced the hardware interlocks of earlier models. Nancy Leveson's investigation is "
            "still required reading. <bookmark mark='d'/> The ACM's Code of Ethics asks computing professionals to "
            "contribute to society, avoid harm, be honest, respect privacy, and review systems and their risks "
            "thoroughly. None of this is separate from engineering: privacy is a requirement like latency, "
            "accessibility a requirement like correctness, and the safest systems are those whose designers "
            "assumed that their own code, like every other code, contains bugs."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()

    def failures(self):
        head = label(r"When software fails people", font_size=36).to_edge(UP, buff=0.3)
        lines = VGroup(
            wrapped_label(r"\textbf{the Post Office Horizon scandal} \ (United Kingdom, \ 1999--2015): \ an "
                          r"accounting system's errors showed shortfalls at branch counters; \ more than 900 "
                          r"sub-postmasters were prosecuted, \ and courts presumed the computer was right", 12.4,
                          font_size=22, color=NO),
            wrapped_label(r"the 2019 judgment found that Horizon had bugs, \ errors and defects that could cause the "
                          r"shortfalls; \ convictions have since been overturned, \ some after the people convicted "
                          r"had died", 12.4, font_size=22, color=HEAD),
            wrapped_label(r"\textbf{the Boeing 737 MAX} \ (2018--19): \ flight software acting on a single sensor, \ "
                          r"documented too little for pilots, \ contributed to two crashes that killed 346 people", 12.4,
                          font_size=22, color=NO),
            wrapped_label(r"the engineering lessons are this part's: \ evidence over assumption, \ honest reviews of "
                          r"risk, \ and no single point of failure, \ technical or human", 12.4, font_size=22,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.36).next_to(head, DOWN, buff=0.55)
        with self.voiceover(
            "Engineering ethics is not abstract. <bookmark mark='a'/> From 1999, the British Post Office's Horizon "
            "accounting system showed shortfalls at branch counters, and the Post Office prosecuted more than nine "
            "hundred sub-postmasters for theft and false accounting. Courts presumed that the computer was right. "
            "<bookmark mark='b'/> In 2019 a High Court judgment found that Horizon had bugs, errors and defects "
            "capable of causing such shortfalls. Convictions have since been overturned, some after the people "
            "convicted had died. <bookmark mark='c'/> In 2018 and 2019, two Boeing 737 MAX aircraft crashed, killing "
            "three hundred and forty-six people, after flight-control software acted on a single faulty sensor, in "
            "a system that pilots had been told too little about. <bookmark mark='d'/> The lessons are this part's "
            "own: evidence over assumption, honest reviews of risk, and no single point of failure, whether a "
            "sensor or a presumption."
        ) as vo:
            self.play(FadeIn(head))
            for mk, l in zip("abcd", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (DATA, KERN)
