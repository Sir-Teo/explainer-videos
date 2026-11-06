from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, module_box, mono,
                                   tag_box)


def dollars(cents: int, sign=False) -> str:
    s = f"{abs(cents) / 100:,.2f}"
    if cents < 0:
        return r"$-$\$" + s
    return (r"$+$\$" if sign else r"\$") + s


class Payments(VoiceoverScene):
    def construct(self):
        self.card()
        self.entries()
        self.design()
        self.retries()
        self.states()
        self.reconcile()

    def card(self):
        card = chapter_card(8, r"A payment ledger", r"How is money never lost, \ and never taken twice?",
                            lit=(1981, 2012), extra=((1981, r"Gray: \ the transaction concept"),
                                                     (2012, r"Helland: \ idempotence")), part=PART)
        with self.voiceover("Chapter eight. A payment ledger."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def entries(self):
        head = label(r"Double entry: \ every entry sums to zero", font_size=36).to_edge(UP, buff=0.3)
        names = [r"customer", r"merchant", r"fees"]
        cols = [DATA, YES, KERN]
        payments = [5000, 2000]                         # cents; the fee is 3%, as in our ledger instrument
        lines = [[-a, a - a * 3 // 100, a * 3 // 100] for a in payments]
        acc = VGroup()
        for n, c in zip(names, cols):
            box = RoundedRectangle(width=3.0, height=1.2, corner_radius=0.12, stroke_color=c, stroke_width=2,
                                   fill_color=BG, fill_opacity=1)
            t = label(n, font_size=21, color=c).move_to(box).shift(UP * 0.28)
            acc.add(VGroup(box, t))
        acc.arrange(RIGHT, buff=0.6).next_to(head, DOWN, buff=0.45).shift(LEFT * 1.2)
        bal = [0, 0, 0]

        def bal_text(k):
            return label(dollars(bal[k]), font_size=22, color=WHITE).move_to(acc[k][0]).shift(DOWN * 0.22)
        bals = VGroup(*[bal_text(k) for k in range(3)])
        total = VGroup(label(r"sum of all balances", font_size=19, color=GREY_A),
                       label(dollars(0), font_size=24, color=YES)).arrange(DOWN, buff=0.12)
        total.next_to(acc, RIGHT, buff=0.6)
        rows = [[f"pay-{i + 1}", *[dollars(v, True) for v in ln], r"0"] for i, ln in enumerate(lines)]
        tab = grid_table([r"journal entry", *names, r"sum"], rows, widths=[2.6, 2.4, 2.4, 2.2, 1.4], row_h=0.7,
                         font_size=23, mono_cols=(0,))
        tab.next_to(acc, DOWN, buff=0.6).set_x(0)
        for r in (1, 2):
            tab.cells[r][4].set_color(YES)
        ill = note(r"amounts illustrative; \ integers in cents", font_size=16).next_to(tab, DOWN, buff=0.35)
        notes = VGroup(
            wrapped_label(r"each entry's lines sum to zero, \ so by induction \ (Part 2) \ the whole ledger does: \ "
                          r"money is moved, \ never made or lost", 12.4, font_size=20, color=YES),
            wrapped_label(r"entries are only appended; \ a mistake is corrected by a new, \ reversing entry, \ so the "
                          r"history is the audit trail", 12.4, font_size=20, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(ill, DOWN, buff=0.6).set_x(0)
        with self.voiceover(
            "A payment system is first of all a ledger, kept the way accountants have kept books for five hundred "
            "years. <bookmark mark='a'/> Every payment is a journal entry with several lines: fifty dollars leave the "
            "customer, forty-eight fifty reach the merchant, and a dollar fifty goes to fees. The lines sum to "
            "zero. Amounts are whole numbers of cents, never floating point, as Part 4 warned. "
            "<bookmark mark='b'/> A second payment, the same way. <bookmark mark='c'/> Because every entry sums to "
            "zero, the whole ledger does, by the induction of Part 2: money is moved, never made or lost. "
            "<bookmark mark='d'/> Entries are only ever appended. A "
            "mistake is fixed by a new entry that reverses it, so the ledger is its own audit trail."
        ) as vo:
            self.play(FadeIn(head), FadeIn(acc), FadeIn(bals), FadeIn(total), FadeIn(tab.rule),
                      FadeIn(VGroup(*tab.cells[0])), FadeIn(ill))
            for mk, r in zip("ab", (1, 2)):
                vo.wait_until(mk)
                self.play(FadeIn(VGroup(*tab.cells[r])))
                for k in range(3):
                    bal[k] += lines[r - 1][k]
                self.play(*[TransformFromCopy(tab.cells[r][k + 1], bals[k]) for k in range(3)], run_time=0.8)
                self.play(*[Transform(bals[k], bal_text(k)) for k in range(3)],
                          Indicate(total[1], color=YES), run_time=0.6)
            vo.wait_until("c")
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def design(self):
        head = label(r"Retries, \ and the idempotency key", font_size=36).to_edge(UP, buff=0.3)
        y = 1.2
        client = module_box(r"client", HEAD, w=1.7, h=0.75).move_to([-5.7, y, 0])
        api = module_box(r"payments API", KERN, w=2.3, h=0.75).move_to([-2.6, y, 0])
        ledger = module_box(r"ledger DB \ (one leader)", DATA, w=2.6, h=0.75).move_to([0.7, y, 0])
        proc = module_box(r"card processor", LAM, w=2.3, h=0.75).move_to([4.3, y, 0])
        outbox = module_box(r"outbox \ (Part 43)", GREY_B, w=2.2, h=0.6, font=17).next_to(ledger, DOWN, buff=0.5)

        def arr(a, b, col=GREY_C):
            return Arrow(a, b, buff=0.06, color=col, stroke_width=2, max_tip_length_to_length_ratio=0.15)
        links = VGroup(arr(client.get_right() + UP * 0.15, api.get_left() + UP * 0.15),
                       arr(api.get_right(), ledger.get_left()),
                       arr(ledger.get_bottom(), outbox.get_top()),
                       arr(outbox.get_right(), proc.get_bottom() + LEFT * 0.4))
        reply = arr(api.get_left() + DOWN * 0.15, client.get_right() + DOWN * 0.15, NO)
        keys = grid_table([r"idempotency key", r"state", r"stored reply"],
                          [[r"9f2c-7a41", r"done", r"200: \ paid \$50.00"]], widths=[2.6, 1.4, 2.8], row_h=0.48,
                          font_size=18, mono_cols=(0,))
        keys_t = label(r"in the same transaction as the entry", font_size=17, color=KERN)
        kt = VGroup(keys_t, keys).arrange(DOWN, buff=0.2).move_to([-2.6, -1.0, 0])
        ill = note(r"key illustrative", font_size=16).next_to(kt, DOWN, buff=0.1)
        req = tag_box(r"POST /pay  key=9f2c-7a41", color=HEAD, size=14)
        req.next_to(client, UP, buff=0.25).align_to(client, LEFT)
        lost = Cross(stroke_color=NO, stroke_width=5).scale(0.2).move_to(reply)
        notes = VGroup(
            wrapped_label(r"a timeout does not say whether the charge happened; \ the client must retry, \ so the "
                          r"server must make a retry harmless", 12.4, font_size=19, color=WHITE),
            wrapped_label(r"the client picks a key per payment; \ the server records it with the result, \ and a "
                          r"repeat returns the stored reply instead of charging again \ (Helland 2012; \ Part 43)",
                          12.4, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).to_edge(DOWN, buff=0.3)
        dot = Dot(radius=0.1, color=HEAD)
        with self.voiceover(
            "The design. <bookmark mark='a'/> A client asks the payments API to charge fifty "
            "dollars. The API writes the ledger entry to a single-leader database, and an outbox, Part 43's "
            "pattern, carries the request to the card processor. <bookmark mark='b'/> Then the reply is lost. The "
            "client cannot know whether the charge happened, so it must retry, and a naive server would charge "
            "twice. <bookmark mark='c'/> The cure is an idempotency key. The client chooses one key per payment and "
            "sends it with every attempt. The server records the key and its result in the same transaction as the "
            "ledger entry, so a repeat finds the key and returns the stored reply instead of charging again. "
            "<bookmark mark='d'/> Pat Helland put it simply in 2012: in a world of retries, every request should be "
            "idempotent."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in (client, api, ledger, outbox, proc)], lag_ratio=0.2),
                      LaggedStart(*[GrowArrow(a) for a in links], lag_ratio=0.2), FadeIn(req), run_time=2)
            path = VMobject().set_points_as_corners([client.get_right() + UP * 0.15, api.get_left() + UP * 0.15,
                                                     api.get_right(), ledger.get_left(), ledger.get_bottom(),
                                                     outbox.get_top(), outbox.get_right(),
                                                     proc.get_bottom() + LEFT * 0.4])
            dot.move_to(path.get_start())
            self.play(FadeIn(dot))
            self.play(MoveAlongPath(dot, path), run_time=2.2, rate_func=linear)
            self.play(FadeOut(dot))
            vo.wait_until("b")
            self.play(GrowArrow(reply))
            self.play(Create(lost), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(kt), FadeIn(ill))
            retry = Dot(radius=0.1, color=HEAD).move_to(client.get_right() + UP * 0.15)
            self.play(FadeIn(retry))
            self.play(retry.animate.move_to(api.get_left() + UP * 0.15), run_time=0.7)
            self.play(Indicate(keys.cells[1][0], color=YES), retry.animate.move_to(keys.cells[1][0]), run_time=0.8)
            self.play(retry.animate.move_to(client.get_right()).set_color(YES), FadeOut(lost), FadeIn(notes[1]),
                      run_time=0.8)
            self.play(FadeOut(retry))
            vo.wait_until("d")
            self.play(Indicate(notes[1], color=YES))
        self.wait(0.4)
        self.clear_scene()

    def retries(self):
        led = load("payments")
        nv, idm = led["naive"], led["idempotent"]
        head = label(r"Five thousand payments, \ with retries", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"payments", f"{nv['payments']:,}", f"{idm['payments']:,}"],
                [r"journal entries posted", f"{nv['entries']:,}", f"{idm['entries']:,}"],
                [r"payments charged twice", f"{nv['double_charges']:,}", f"{idm['double_charges']:,}"],
                [r"sum of all balances", f"{nv['sum']}", f"{idm['sum']}"]]
        tab = grid_table([r"", r"without keys", r"with idempotency keys"], rows, widths=[4.6, 3.4, 4.0],
                         row_h=0.72, font_size=24, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5)
        for r in (2, 3):
            tab.cells[r][1].set_color(NO)
            tab.cells[r][2].set_color(YES)
        for c in (1, 2):
            tab.cells[4][c].set_color(HEAD)
        ring = SurroundingRectangle(VGroup(*tab.cells[4]), color=HEAD, buff=0.1, corner_radius=0.06)
        lines = VGroup(
            wrapped_label(r"both ledgers balance: \ every double charge was itself a perfectly balanced entry", 12.4,
                          font_size=21, color=HEAD),
            wrapped_label(r"so $\sum = 0$ cannot catch it: \ ``at most one entry per payment'' is a second "
                          r"invariant, \ and the key table is what enforces it", 12.4, font_size=21, color=WHITE),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).next_to(tab, DOWN, buff=0.45)
        cap = note(r"simulated: \ random amounts, \ some attempts time out and are retried, \ some are declined",
                   font_size=16).to_edge(DOWN, buff=0.3)
        with self.voiceover(
            "We simulated it with our ledger instrument: five thousand payments of random amounts, where some "
            "attempts time out and are retried and some are declined. <bookmark mark='a'/> Without keys, six "
            "thousand two hundred and nine entries were posted, and one thousand three hundred and ninety payments, "
            "nearly three in ten, were charged twice. <bookmark mark='b'/> With keys, no payment was charged twice. "
            "<bookmark mark='c'/> Now look at the invariant. "
            "Both ledgers sum to exactly zero. Every double charge was itself a perfectly balanced entry, so the "
            "books balance and are still wrong. <bookmark mark='d'/> Balance is one invariant; at most one entry per "
            "payment is another, and only the key table enforces it."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])), FadeIn(VGroup(*tab.cells[1])),
                      FadeIn(cap))
            vo.wait_until("a")
            self.play(FadeIn(VGroup(tab.cells[2][0], tab.cells[2][1])))
            self.play(FadeIn(VGroup(tab.cells[3][0], tab.cells[3][1])))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(tab.cells[2][2], tab.cells[3][2])))
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[4])), Create(ring), FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def states(self):
        head = label(r"A payment is a state machine", font_size=36).to_edge(UP, buff=0.3)
        main = [r"created", r"authorized", r"captured", r"settled"]
        side = {r"declined": 0, r"voided": 1, r"refunded": 2}
        st = {}
        for i, n in enumerate(main):
            st[n] = tag_box(n, color=YES if n == r"settled" else DATA, size=17, w=2.3, h=0.65).move_to(
                [-4.8 + i * 3.2, 0.8, 0])
        for n, i in side.items():
            st[n] = tag_box(n, color=NO if n == r"declined" else LAM, size=17, w=2.3, h=0.65).move_to(
                [-4.8 + i * 3.2 + 1.6, -0.8, 0])
        arrows = VGroup(*[Arrow(st[a].get_right(), st[b].get_left(), buff=0.08, color=GREY_C, stroke_width=2,
                                max_tip_length_to_length_ratio=0.15) for a, b in zip(main, main[1:])])
        for n, i in side.items():
            arrows.add(Arrow(st[main[i]].get_bottom(), st[n].get_top(), buff=0.08, color=GREY_C, stroke_width=2,
                             max_tip_length_to_length_ratio=0.2))
        posts = VGroup(*[label(t, font_size=17, color=GREY_B).next_to(st[main[k + 1]], UP, buff=0.15) for k, t in
                         enumerate([r"a hold placed", r"money moves", r"cash arrives"])])
        token = Dot(radius=0.13, color=HEAD).move_to(st[r"created"].get_top() + UP * 0.75)
        notes = VGroup(
            wrapped_label(r"transitions only go forward, \ and each one is a compare-and-set on the current state: \ "
                          r"a duplicate ``capture'' finds the payment already captured and does nothing", 12.4,
                          font_size=19, color=WHITE),
            wrapped_label(r"the state change, \ its ledger lines and the outbox message are written in one "
                          r"transaction \ (Part 35), \ so no one is ever seen without the others", 12.4, font_size=19,
                          color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "A card payment is a state machine. <bookmark mark='a'/> It is created; the "
            "card's bank authorizes it, placing a hold; the merchant captures it, and money moves; days later it "
            "settles, and the cash arrives. Along the way it can be declined, voided before capture, or refunded "
            "after. <bookmark mark='b'/> Transitions only go forward, and each is a compare-and-set on the current "
            "state, so a duplicate capture finds the payment already captured and does nothing. "
            "<bookmark mark='c'/> The state change, its ledger lines and the outbox message are written in one "
            "database transaction, from Part 35, so none is ever seen without the others."
        ) as vo:
            self.play(FadeIn(head), *[FadeIn(b) for b in st.values()], FadeIn(arrows))
            vo.wait_until("a")
            self.play(FadeIn(token))
            for k, n in enumerate(main[1:]):
                self.play(token.animate.move_to(st[n].get_top() + UP * 0.75), FadeIn(posts[k]), run_time=0.9)
                self.play(Indicate(st[n], color=HEAD), run_time=0.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[0]))
            self.play(Indicate(st[r"captured"], color=YES))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def reconcile(self):
        head = label(r"Reconciliation, \ and choosing consistency", font_size=36).to_edge(UP, buff=0.3)
        ours = [(r"pay-1", 5000), (r"pay-2", 2000), (r"pay-3", 1250), (r"pay-4", 990)]
        theirs = [(r"pay-1", 5000), (r"pay-2", 2000), (r"pay-3", 1205), (r"pay-5", 400)]

        def col(title, rows, color):
            t = label(title, font_size=19, color=color)
            body = VGroup(*[VGroup(mono(k, size=15, color=GREY_A), label(dollars(v), font_size=18, color=WHITE))
                            .arrange(RIGHT, buff=0.35) for k, v in rows]).arrange(DOWN, buff=0.22, aligned_edge=LEFT)
            return VGroup(t, body).arrange(DOWN, buff=0.25)
        left = col(r"our ledger", ours, DATA).scale(1.3).move_to([-4.9, 0.5, 0])
        right = col(r"the processor's settlement file", theirs, LAM).scale(1.3).move_to([-0.4, 0.5, 0])
        links = VGroup()
        for i in range(4):
            ok = ours[i] == theirs[i]
            links.add(Line(left[1][i].get_right(), right[1][i].get_left(), color=YES if ok else NO,
                           stroke_width=2.5 if ok else 3, buff=0.1))
        tags = VGroup(label(r"amounts differ", font_size=16, color=NO), label(r"missing on each side", font_size=16,
                                                                             color=NO))
        tags[0].next_to(links[2], UP, buff=0.04)
        tags[1].next_to(links[3], DOWN, buff=0.04)
        ill = note(r"illustrative", font_size=16).next_to(VGroup(left, right), DOWN, buff=0.25)
        notes = VGroup(
            wrapped_label(r"every day, \ match each of our entries with the outside world's record; \ mismatches go "
                          r"to a queue for people", 4.6, font_size=19, color=WHITE),
            wrapped_label(r"during a partition, \ a ledger refuses writes rather than let two replicas disagree "
                          r"about a balance: \ consistency over availability \ (Part 39)", 4.6, font_size=19,
                          color=HEAD),
            wrapped_label(r"availability comes back at the edge: \ accept the request, \ answer ``pending'', \ and "
                          r"let the outbox finish it later", 4.6, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([4.4, -0.1, 0])
        with self.voiceover(
            "Two more duties remain. <bookmark mark='a'/> The ledger is only our account of events; the processor "
            "and the banks keep theirs. Every day, each of our entries is matched against the processor's "
            "settlement file. Most agree. <bookmark mark='b'/> Some do not: an amount that differs, an entry one "
            "side has and the other lacks. These go to a queue for people. "
            "<bookmark mark='c'/> The last trade-off is the one Part 39 named. During a "
            "network partition, a ledger refuses to write rather than let two replicas disagree about a balance; "
            "it chooses consistency over availability. <bookmark mark='d'/> Availability is won back at the edge: "
            "accept the request, answer pending, and let the outbox finish the work when the ledger can."
        ) as vo:
            self.play(FadeIn(head), FadeIn(left), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(right), FadeIn(notes[0]))
            self.play(LaggedStart(*[Create(ln) for ln in links[:2]], lag_ratio=0.3))
            vo.wait_until("b")
            self.play(Create(links[2]), FadeIn(tags[0]))
            self.play(Create(links[3]), FadeIn(tags[1]))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, HEAD, KERN, LAM, NO, YES)
