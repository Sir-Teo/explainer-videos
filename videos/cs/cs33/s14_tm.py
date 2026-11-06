from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs33.common import (LAM, NO, PART, YES, grid_table, load, mono, num)


class Tm(VoiceoverScene):
    def construct(self):
        self.card()
        self.tm()
        self.messages()

    def card(self):
        card = chapter_card(13, r"Transactional memory, \ channels and actors",
                            r"Can we stop writing locks altogether?", lit=(1973, 1978, 1993),
                            extra=((1973, r"Hewitt: \ actors"), (1978, r"Hoare: \ CSP"),
                                   (1993, r"Herlihy and Moss: \ transactional memory")), part=PART)
        with self.voiceover("Chapter thirteen. Transactional memory, channels, and actors."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def tm(self):
        d = load("tsx")
        head = label(r"Transactional memory", font_size=36).to_edge(UP, buff=0.3)
        code = VGroup(mono("if (_xbegin() == _XBEGIN_STARTED) {", 19, YES),
                      mono("    x++;                    // tentative", 19, WHITE),
                      mono("    _xend();                // commit, all at once", 19, YES),
                      mono("} else {", 19, GREY_B),
                      mono("    lock(m); x++; unlock(m);   // fallback", 19, GREY_B),
                      mono("}", 19, GREY_B)).arrange(DOWN, aligned_edge=LEFT, buff=0.08)
        box = SurroundingRectangle(code, color=GREY_D, buff=0.18, corner_radius=0.08)
        cg = VGroup(box, code).next_to(head, DOWN, buff=0.4)
        items = VGroup(
            label(r"Herlihy and Moss \ (1993): \ run a block speculatively; \ if another core touches its cache "
                  r"lines, \ abort and retry", font_size=20, color=WHITE),
            label(r"the cache already tracks who has each line \ (MESI): \ a conflict is an invalidation",
                  font_size=20, color=LAM),
            label(rf"this machine has Intel's RTM: \ {num(d['committed'])} of {num(d['tried'])} tiny transactions "
                  rf"committed", font_size=20, color=YES),
            label(r"but: \ a bug disabled it on Haswell \ (2014), \ a leak \ (TAA, \ 2019) \ turned it off by "
                  r"default, \ and Intel's client chips dropped it", font_size=20, color=NO),
            label(r"always needs a fallback: \ a transaction may abort for reasons that never go away",
                  font_size=20, color=GREY_A),
        ).arrange(DOWN, buff=0.14).next_to(cg, DOWN, buff=0.35)
        with self.voiceover(
            "What if we could mark a block of code atomic, and let the hardware make it so? <bookmark mark='a'/> That "
            "is transactional memory, proposed by Herlihy and Moss in 1993. The block runs speculatively, its writes "
            "kept private, and commits all at once at the end. <bookmark mark='b'/> If another core touches any of "
            "its cache lines in the meantime, the coherence protocol notices, and the transaction aborts and starts "
            "again. <bookmark mark='c'/> This machine has Intel's version. We ran a million tiny transactions, and "
            "all but seventy-three committed. <bookmark mark='d'/> But hardware transactions have had a hard life. A "
            "bug forced Intel to disable them on its 2014 processors; in 2019 they turned out to leak data, and were "
            "switched off by default; and Intel's consumer processors no longer have them. <bookmark mark='e'/> And a "
            "transaction can abort forever, say because its data does not fit in the cache, so every use still needs "
            "an ordinary lock as a fallback."
        ) as vo:
            self.play(FadeIn(head), Create(box), FadeIn(code))
            for mk, it in zip("abcde", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
        self.wait(0.3)
        self.clear_scene()

    def messages(self):
        head = label(r"Share by communicating", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"model", r"the idea", r"in practice"], [
            [r"CSP \ (Hoare 1978)", r"processes share nothing; \ they meet on \textbf{channels}",
             r"Go's \texttt{chan} and \texttt{select}; \ Occam"],
            [r"actors \ (Hewitt 1973)", r"each actor has a mailbox and handles one message at a time",
             r"Erlang \ (1986): \ telephone switches; \ Akka"],
            [r"async / await", r"one thread, \ many tasks, \ switching only at \texttt{await}",
             r"C\# \ (2012), \ JavaScript, \ Python, \ Rust's tokio"],
        ], widths=[3.2, 5.8, 4.4], row_h=0.7, font_size=19, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        go = VGroup(mono("results := make(chan int)", 19, WHITE),
                    mono("go func() { results <- work() }()", 19, WHITE),
                    mono("x := <-results          // wait for it", 19, YES)).arrange(DOWN, aligned_edge=LEFT,
                                                                                     buff=0.08)
        lines = VGroup(
            label(r"``Do not communicate by sharing memory; \ share memory by communicating'' \ (Go's proverb)",
                  font_size=20, color=WHITE),
            label(r"no shared variables, \ no data races; \ but deadlock is still possible: \ two actors each waiting "
                  r"for the other", font_size=20, color=NO),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.4)
        go.next_to(lines, UP, buff=0.35)
        with self.voiceover(
            "Another answer is to stop sharing memory. <bookmark mark='a'/> In Hoare's communicating sequential "
            "processes, from 1978, processes share nothing and meet only on channels: a send waits for a matching "
            "receive. Go's channels come straight from it. <bookmark mark='b'/> In Hewitt's actors, each actor owns "
            "its state and a mailbox, and handles one message at a time. Erlang, built at Ericsson for telephone "
            "switches, runs millions of them. <bookmark mark='c'/> And async and await interleave many tasks on one "
            "thread, switching only at the points the programmer marks, which makes most races impossible. <bookmark "
            "mark='d'/> Go's proverb puts it well: do not communicate by sharing memory; share memory by "
            "communicating. <bookmark mark='e'/> Data races disappear. Deadlock does not: two actors can each wait for "
            "a message from the other forever."
        ) as vo:
            self.play(FadeIn(head), FadeIn(VGroup(*tab.cells[0])), FadeIn(tab.rule))
            for mk, r in zip("abc", tab.cells[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*r)))
            vo.wait_until("d")
            self.play(FadeIn(go), FadeIn(lines[0]))
            vo.wait_until("e")
            self.play(FadeIn(lines[1]))
        self.wait(0.3)
        self.clear_scene()
