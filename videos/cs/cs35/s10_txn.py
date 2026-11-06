from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (DATA, HEAD, KERN, LAM, NO, PART, T1C, T2C, YES, load, precedence_view,
                                   schedule_view)


class Txn(VoiceoverScene):
    def construct(self):
        self.card()
        self.acid()
        self.conflicts()
        self.view()

    def card(self):
        card = chapter_card(9, r"Transactions", r"What does it mean for concurrent work to be correct?",
                            lit=(1976, 1981), extra=((1976, r"Eswaran et al.: \ serializability"),
                                                     (1981, r"Gray: \ the transaction concept")), part=PART)
        with self.voiceover("Chapter nine. Transactions."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def acid(self):
        head = label(r"A transaction: \ all of it, \ or none, \ as if alone", font_size=36).to_edge(UP, buff=0.3)
        code_ = VGroup(*[Text(t, font="DejaVu Sans Mono", font_size=17, color=c) for t, c in (
            ("BEGIN;", GREY_A),
            ("UPDATE accounts SET balance = balance - 100 WHERE name = 'ana';", T1C),
            ("UPDATE accounts SET balance = balance + 100 WHERE name = 'ben';", T1C),
            ("COMMIT;", YES))]).arrange(DOWN, aligned_edge=LEFT, buff=0.08).next_to(head, DOWN, buff=0.45)
        props = VGroup(
            label(r"\textbf{Atomic}: \ a crash between the two updates must not leave the money half moved",
                  font_size=20, color=NO),
            label(r"\textbf{Consistent}: \ each transaction takes a correct database to a correct one \ (total "
                  r"money unchanged)", font_size=20, color=LAM),
            label(r"\textbf{Isolated}: \ running together, \ transactions behave as if they ran one at a time",
                  font_size=20, color=HEAD),
            label(r"\textbf{Durable}: \ once \texttt{COMMIT} returns, \ the change survives any crash",
                  font_size=20, color=YES),
            label(r"Gray \ (1981) \ framed the concept; \ H\"arder and Reuter \ (1983) \ named it ACID; \ "
                  r"atomicity and durability are chapter 13, \ isolation the next four", font_size=18, color=GREY_A),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(code_, DOWN, buff=0.5)
        with self.voiceover(
            "Now the second machine inside a database. Move a hundred from Ana's account to Ben's: two updates, "
            "wrapped in a transaction. <bookmark mark='a'/> It must be atomic: if the machine crashes between the "
            "updates, the money must not vanish from one account without arriving in the other. "
            "<bookmark mark='b'/> Each transaction, run alone, keeps the data consistent: here, the total stays the "
            "same. <bookmark mark='c'/> It must be isolated: while thousands of transactions run at once, each must "
            "behave as if it ran by itself. <bookmark mark='d'/> And it must be durable: once the commit returns, the "
            "transfer survives any crash. <bookmark mark='e'/> Jim Gray set out these ideas; Härder and Reuter gave "
            "them their initials, ACID. Atomicity and durability come in chapter thirteen. Isolation takes the next "
            "four."
        ) as vo:
            self.play(FadeIn(head), FadeIn(code_))
            for mk, p in zip("abcde", props):
                vo.wait_until(mk)
                self.play(FadeIn(p))
        self.wait(0.3)
        self.clear_scene()

    def conflicts(self):
        s = load("serial")
        ex = s["examples"]
        head = label(r"Schedules, \ conflicts, \ and a graph", font_size=36).to_edge(UP, buff=0.3)
        lost = schedule_view(ex["lost update"]["schedule"]).move_to([-2.4, 1.6, 0])
        ll = label(r"two deposits to $x$, \ interleaved", font_size=19, color=NO).next_to(lost, UP, buff=0.15)
        g1 = precedence_view(ex["lost update"]["edges"], [1, 2]).move_to([4.2, 1.5, 0])
        ok = schedule_view(ex["serializable"]["schedule"], step=0.72).move_to([-1.9, -1.0, 0])
        ol = label(r"interleaved, \ but in a consistent order", font_size=19, color=YES).next_to(ok, UP, buff=0.15)
        g2 = precedence_view(ex["serializable"]["edges"], [1, 2]).move_to([4.6, -1.1, 0])
        rule = label(r"two operations \textbf{conflict} if they are in different transactions, \ touch the same item, "
                     r"\ and one writes: \ an edge from the earlier one's transaction to the later's", font_size=18,
                     color=WHITE).to_edge(DOWN, buff=0.75)
        thm = label(r"\textbf{conflict-serializable} \ $\Leftrightarrow$ \ the graph has no cycle: \ any topological "
                    r"order is an equivalent serial order \ (Eswaran et al., 1976)", font_size=18,
                    color=HEAD).to_edge(DOWN, buff=0.3)
        lost_note = label(r"cycle: \ \textbf{lost update}", font_size=19, color=NO).next_to(g1, DOWN, buff=0.15)
        ok_note = label(r"no cycle: \ same as $T_1$ then $T_2$", font_size=19, color=YES).next_to(g2, DOWN, buff=0.15)
        with self.voiceover(
            "What does it mean for interleaved transactions to be correct? A schedule is the order in which their "
            "steps happen. <bookmark mark='a'/> Here two transactions each read x and write it back, plus something: "
            "two deposits. Both read the old balance; both write; the second write overwrites the first, and one "
            "deposit is lost. <bookmark mark='b'/> Two steps conflict if they come from different transactions, touch "
            "the same item, and at least one writes; then their order matters. Draw an arrow from the transaction "
            "that went first to the one that went second. <bookmark mark='c'/> Here T1 read x before T2 wrote it, and "
            "T2 read x before T1 wrote it: arrows both ways, a cycle. No serial order is equivalent. "
            "<bookmark mark='d'/> Here is another interleaving, of two transactions touching x and y. Every conflict "
            "has T1 first, so the graph is one arrow, and the schedule is equivalent to running T1, then T2. "
            "<bookmark mark='e'/> That is the theorem of Eswaran, Gray, Lorie and Traiger, from 1976: a schedule is "
            "conflict-serializable exactly when its graph has no cycle."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(lost), FadeIn(ll))
            vo.wait_until("b")
            self.play(FadeIn(rule))
            vo.wait_until("c")
            self.play(FadeIn(g1), FadeIn(lost_note))
            vo.wait_until("d")
            self.play(FadeIn(ok), FadeIn(ol), FadeIn(g2), FadeIn(ok_note))
            vo.wait_until("e")
            self.play(FadeIn(thm))
        self.wait(0.3)
        self.clear_scene()

    def view(self):
        s = load("serial")
        bl = s["examples"]["blind writes"]
        head = label(r"A wider notion, \ and the cost of testing it", font_size=36).to_edge(UP, buff=0.3)
        sv = schedule_view(bl["schedule"]).move_to([-2.4, 1.5, 0])
        g = precedence_view(bl["edges"], [1, 2, 3], r=0.9).move_to([4.2, 1.4, 0])
        lines = VGroup(
            label(r"$T_2$ and $T_3$ write $x$ \textit{blindly}, \ without reading it; \ the graph has a cycle", font_size=20,
                  color=NO),
            label(rf"yet every read sees what it would in the serial order $T_1, T_2, T_3$, \ and $T_3$ writes last: "
                  rf"\ \textbf{{view-serializable}} \ ({'yes' if bl['view'] else 'no'})", font_size=20, color=YES),
            label(r"testing view serializability is NP-complete \ (Papadimitriou, 1979); \ conflicts are a cycle check",
                  font_size=20, color=HEAD),
            label(rf"three transactions of two steps each: \ {s['interleavings']} interleavings, \ "
                  rf"{s['conflict']} conflict-serializable, \ {s['view']} view-serializable", font_size=20, color=LAM),
            label(r"so real systems enforce the stronger, checkable property, \ and they do it as they go: \ the "
                  r"scheduler must decide each step \textit{now}", font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(sv, DOWN, buff=0.6).set_x(0)
        with self.voiceover(
            "There is a wider definition. <bookmark mark='a'/> In this schedule, T2 and T3 write x without reading it, "
            "blind writes, and the conflict graph has a cycle. <bookmark mark='b'/> Yet T1 reads the value it would "
            "read if the three ran in order, and the last write is T3's, as in that order. The schedule is view "
            "serializable: no one could tell the difference. <bookmark mark='c'/> But testing view serializability is "
            "NP-complete, as Christos Papadimitriou showed in 1979, while a cycle check takes linear time. "
            "<bookmark mark='d'/> Our checker enumerates all ninety interleavings of three small transactions. Ten are "
            "conflict-serializable, and here no others are view-serializable either. <bookmark mark='e'/> So "
            "databases aim for conflict serializability, and they must achieve it on the fly, deciding each step as "
            "it arrives, without knowing what comes next."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sv))
            vo.wait_until("a")
            self.play(FadeIn(g), FadeIn(lines[0]))
            for mk, ln in zip("bcde", lines[1:]):
                vo.wait_until(mk)
                self.play(FadeIn(ln))
        self.wait(0.3)
        self.clear_scene()


_ = (DATA, KERN, T2C)
