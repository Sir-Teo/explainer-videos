from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs38.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, box, grid_table, load, seq_diagram)


class Generals(VoiceoverScene):
    def construct(self):
        self.card()
        self.partial()
        self.generals()
        self.proof()

    def card(self):
        card = chapter_card(1, r"Partial failure", r"Can two parties agree over a link that loses messages?",
                            lit=(1975, 1978), extra=((1975, r"Akkoyunlu et al.: \ the problem"),
                                                     (1978, r"Gray: \ the two generals")), part=PART)
        with self.voiceover("Chapter one. Partial failure."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def partial(self):
        head = label(r"Three things one computer never faces", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            VGroup(box(3.2, 0.8, r"partial failure", NO, font_size=22),
                   wrapped_label(r"some machines crash while others run on; \ a single computer either works or "
                                 r"does not", 8.2, font_size=21, color=WHITE)).arrange(RIGHT, buff=0.5),
            VGroup(box(3.2, 0.8, r"no global clock", KERN, font_size=22),
                   wrapped_label(r"each machine's clock drifts \ (typically 10 to 100 parts per million: \ up to "
                                 r"8 s a day); \ ``at the same time'' has no meaning to check", 8.2, font_size=21,
                                 color=WHITE)).arrange(RIGHT, buff=0.5),
            VGroup(box(3.2, 0.8, r"asynchrony", DATA, font_size=22),
                   wrapped_label(r"a message may take any time to arrive; \ a slow machine and a dead one look "
                                 r"exactly the same from outside", 8.2, font_size=21, color=WHITE)).arrange(
                RIGHT, buff=0.5),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"every protocol in this part is a way of living with these three, \ and every "
                             r"impossibility theorem is one of them, \ made precise", 12.4, font_size=22,
                             color=YES).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "A program on one computer never has to think about three things that every distributed program must. "
            "<bookmark mark='a'/> Partial failure: some machines crash while the rest carry on, and the rest must "
            "decide what to do without them. <bookmark mark='b'/> No global clock: every machine's clock drifts, "
            "by tens of parts per million, seconds a day, so two machines cannot even agree what time it is. "
            "<bookmark mark='c'/> And asynchrony: a message can take any time to arrive. Wait for a reply that "
            "does not come, and you cannot tell whether the other machine is dead or merely slow. "
            "<bookmark mark='d'/> Every protocol in this part is a way of living with these three facts, and every "
            "impossibility theorem in it is one of them, stated precisely."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abc", items):
                vo.wait_until(mk)
                self.play(FadeIn(it, shift=RIGHT * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def generals(self):
        g = load("generals")
        head = label(r"The two generals", font_size=36).to_edge(UP, buff=0.3)
        ev = [(0.0, 1.0, r"attack at dawn", True, DATA), (1.0, 2.0, r"agreed", False, YES),
              (2.0, 3.0, r"got your ``agreed''", True, DATA), (3.0, None, r"got your ``got''", False, YES)]
        sd = seq_diagram(ev, t_max=3.8, height=4.4, gap=5.0, names=(r"general A", r"general B")).move_to(
            [-3.3, -0.5, 0])
        side = VGroup(
            wrapped_label(r"two armies on two hills must attack together or not at all; \ messengers cross a valley "
                          r"where any one may be captured", 5.4, font_size=20, color=WHITE),
            wrapped_label(r"every message needs an acknowledgement, \ and so does every acknowledgement", 5.4,
                          font_size=20, color=KERN),
            wrapped_label(r"the last messenger is always the one whose loss leaves its sender unsure", 5.4,
                          font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.5, 0.9, 0])
        rows = [[f"{r['loss']:.0%}".replace("%", r"\%"), f"{r['confidence'] * 100:g}\\%", f"{r['messengers']}"]
                for r in g["rows"]]
        tab = grid_table([r"capture", r"to be this sure", r"messengers"], rows, widths=[1.5, 2.2, 1.7], row_h=0.36,
                         font_size=18, mono_cols=())
        tab.move_to([3.5, -2.0, 0])
        with self.voiceover(
            "Jim Gray told the problem as a story in 1978. Two generals camp on two hills with an enemy in the "
            "valley between. Together they can win; alone, either is destroyed. They can communicate only by "
            "messenger, and any messenger may be captured. <bookmark mark='a'/> General A sends: attack at dawn. "
            "But A cannot attack until it knows B got the message, so B must reply. Then B cannot attack until it "
            "knows its reply arrived, so A must acknowledge the reply. <bookmark mark='b'/> And so on, for ever. "
            "<bookmark mark='c'/> Whatever the last message is, its sender does not know whether it arrived. "
            "<bookmark mark='d'/> Sending many messengers makes success likely: with one in ten captured, six "
            "messengers make it a millionth of a chance that all are lost. But likely is not certain, and the "
            "theorem says certain is impossible."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sd[:4]), FadeIn(side[0]))
            vo.wait_until("a")
            self.play(FadeIn(sd.arrows[0]), FadeIn(sd.arrows[1]), FadeIn(side[1]))
            vo.wait_until("b")
            self.play(FadeIn(sd.arrows[2]))
            vo.wait_until("c")
            self.play(FadeIn(sd.arrows[3]), FadeIn(side[2]))
            vo.wait_until("d")
            self.play(FadeIn(tab))
        self.wait(0.4)
        self.clear_scene()

    def proof(self):
        head = label(r"Why no protocol works", font_size=36).to_edge(UP, buff=0.3)
        steps = VGroup(
            wrapped_label(r"\textbf{Claim.} \ No protocol over a link that can lose any message guarantees that both "
                          r"generals attack, or neither.", 12.4, font_size=26, color=HEAD),
            wrapped_label(r"Suppose one does, \ and take a run in which both attack using the \textbf{fewest} "
                          r"messages, $k$.", 12.4, font_size=25, color=WHITE),
            wrapped_label(r"Remove the last message. \ Its sender cannot tell the difference, \ so still attacks. \ "
                          r"So the receiver must attack too, \ with $k - 1$ messages.", 12.4, font_size=25,
                          color=KERN),
            wrapped_label(r"That contradicts minimality \ --- \ unless $k = 0$, \ and with no messages at all neither "
                          r"general can know the other's plan.", 12.4, font_size=25, color=NO),
            wrapped_label(r"The argument is \textbf{induction on messages}: \ no message can be the one that makes "
                          r"agreement certain. \ TCP's handshake and teardown live with this: \ they make "
                          r"agreement likely, \ and time out.", 12.4, font_size=25, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.32).next_to(head, DOWN, buff=0.5)
        with self.voiceover(
            "The proof is an induction on messages. <bookmark mark='a'/> Suppose some protocol does guarantee "
            "that both attack or neither does. <bookmark mark='b'/> Look at a run in which both attack, using as "
            "few messages as possible: k of them. <bookmark mark='c'/> Now imagine the last message is lost. Its "
            "sender sees exactly what it saw before, so it still attacks, and so, for the guarantee to hold, the "
            "receiver must attack too. But that is a run with k minus one messages in which both attack: fewer "
            "than the fewest. <bookmark mark='d'/> The only escape is k equal to zero, and with no messages "
            "neither general can know the other's plan. <bookmark mark='e'/> No single message can be the one "
            "that makes agreement certain. Real protocols, like TCP's handshake and its closing, settle for "
            "likely, and use timeouts for the rest."
        ) as vo:
            self.play(FadeIn(head))
            for mk, s in zip("abcde", steps):
                vo.wait_until(mk)
                self.play(FadeIn(s))
        self.wait(0.5)
        self.clear_scene()


_ = (LAM, YES)
