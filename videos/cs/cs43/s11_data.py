from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table, load, module_box, mono,
                                   tag_box)


def num(x: int) -> str:
    """An integer with thousands separators, for Tex."""
    return f"{x:,}".replace(",", "{,}")


def cylinder(color, w=1.0, h=0.62):
    """A database drawn as a cylinder."""
    body = Rectangle(width=w, height=h, stroke_width=0, fill_color=color, fill_opacity=0.12)
    sides = VGroup(Line([-w / 2, h / 2, 0], [-w / 2, -h / 2, 0]), Line([w / 2, h / 2, 0], [w / 2, -h / 2, 0]))
    sides.set_stroke(color, 2)
    bot = Arc(radius=1, start_angle=PI, angle=PI, color=color, stroke_width=2)
    bot.stretch_to_fit_width(w).stretch_to_fit_height(0.12).move_to([0, -h / 2 - 0.06, 0])
    top = Ellipse(width=w, height=0.24, stroke_color=color, stroke_width=2, fill_color=BG,
                  fill_opacity=1).move_to([0, h / 2, 0])
    return VGroup(body, sides, bot, top)


def crash_mark(size=0.26):
    """A crash: a red burst with its word underneath."""
    s = Star(n=8, outer_radius=size, inner_radius=size * 0.5, color=NO, fill_opacity=1, stroke_width=0)
    t = label(r"crash", font_size=16, color=NO).next_to(s, DOWN, buff=0.06)
    return VGroup(s, t)


class Data(VoiceoverScene):
    def construct(self):
        self.card()
        self.own()
        self.dualwrite()
        self.outbox()
        self.saga()
        self.outcomes()
        self.isolation()

    def card(self):
        card = chapter_card(10, r"Data across services", r"How do services agree on facts without sharing a database?",
                            lit=(1987, 2018), extra=((1987, r"Garcia-Molina and Salem: \ sagas"),
                                                     (2018, r"Richardson: \ \textit{Microservices Patterns}")),
                            part=PART)
        with self.voiceover("Chapter ten. Data across services."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def own(self):
        head = label(r"A database per service", font_size=36).to_edge(UP, buff=0.3)
        specs = ((r"orders", HEAD), (r"payments", YES), (r"stock", KERN))
        xs = (-4.4, 0.0, 4.4)
        svcs, dbs, links, wires = VGroup(), VGroup(), VGroup(), VGroup()
        broker = Rectangle(width=12.4, height=0.55, stroke_color=GREY_B, stroke_width=1.5).move_to([0, -0.75, 0])
        bl = label(r"broker", font_size=17, color=GREY_A).move_to(broker).align_to(broker, RIGHT).shift(LEFT * 0.15)
        for (n, c), x in zip(specs, xs):
            s = module_box(n, c, w=2.1, h=0.55, font=19).move_to([x, 1.75, 0])
            d = cylinder(c).move_to([x + 0.55, 0.45, 0])
            svcs.add(s)
            dbs.add(d)
            links.add(Line([x + 0.55, s.get_bottom()[1], 0], d.get_top(), color=c, stroke_width=2))
            a, b = [x - 0.55, s.get_bottom()[1], 0], [x - 0.55, broker.get_top()[1], 0]
            wires.add(Arrow(a, b, buff=0, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.12)
                      if n == r"orders" else
                      Arrow(b, a, buff=0, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.12))
        bad = DashedLine(svcs[1].get_left(), dbs[0].get_right(), color=NO, stroke_width=2, dash_length=0.1)
        cross = label(r"$\times$", font_size=44, color=NO).move_to(bad.get_center())
        row = tag_box("1042", HEAD, size=15).move_to(dbs[0])
        ev = tag_box("OrderPlaced 1042", HEAD, size=15).move_to([xs[0] - 0.55, 1.0, 0])
        notes = VGroup(
            wrapped_label(r"each service owns its tables; \ others ask through its API or listen to its events; \ a "
                          r"shared database would make them one program again \ (chapter 9's distributed monolith)",
                          12.4, font_size=20, color=WHITE),
            wrapped_label(r"placing an order is two writes, \ to two systems, \ with no transaction that spans both: "
                          r"\ \textbf{the dual-write problem}", 12.4, font_size=20, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Chapter nine left us data that more than one service needs. <bookmark mark='a'/> The rule is that each "
            "service owns its database: orders, payments and stock each keep their own tables. <bookmark mark='b'/> "
            "No service reads another's tables directly; that would weld them back into one program. Others ask "
            "through its interface, or listen to its events. <bookmark mark='c'/> So placing an order is two writes: "
            "a row in the orders database, and an event on the broker. Two systems, and no transaction that spans "
            "both: the dual-write problem."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(svcs), FadeIn(dbs), Create(links), Create(broker), FadeIn(bl))
            vo.wait_until("b")
            self.play(Create(bad), FadeIn(cross), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(Create(wires))
            self.play(FadeIn(row, scale=0.6))
            self.play(FadeIn(ev))
            self.play(ev.animate.move_to([xs[0] - 0.55, broker.get_y(), 0]))
            self.play(ev.animate.move_to([xs[1] - 0.55 + 1.6, broker.get_y(), 0]),
                      Indicate(svcs[1], scale_factor=1.06), Indicate(svcs[2], scale_factor=1.06), run_time=1.2)
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def lane(self, title, steps, y, color):
        """One ordering of the two writes: its title, its two steps and the arrow between them."""
        t = label(title, font_size=21, color=color).move_to([-6.6, y + 0.62, 0], aligned_edge=LEFT)
        a = module_box(steps[0], DATA, w=2.3, h=0.55, font=18).move_to([-5.3, y, 0])
        b = module_box(steps[1], DATA, w=2.3, h=0.55, font=18).move_to([-1.5, y, 0])
        arr = Arrow(a.get_right(), b.get_left(), buff=0.05, color=GREY_B, stroke_width=2,
                    max_tip_length_to_length_ratio=0.1)
        return VGroup(t, a, b, arr)

    def dualwrite(self):
        o = load("outbox")
        M = o["modes"]
        n = o["orders"]
        head = label(r"Two writes, \ one crash", font_size=36).to_edge(UP, buff=0.3)
        sub = label(rf"{num(n)} orders; \ a crash with probability {o['crash'] * 100:.0f}\% at the worst moment",
                    font_size=19, color=GREY_A).next_to(head, DOWN, buff=0.2)
        l1 = self.lane(r"commit, \ then publish", (r"commit the row", r"publish the event"), 1.15, HEAD)
        l2 = self.lane(r"publish, \ then commit", (r"publish the event", r"commit the row"), -1.0, LAM)
        c1 = crash_mark().move_to([l1[3].get_x(), 1.15 - 0.08, 0])
        c2 = crash_mark().move_to([l2[3].get_x(), -1.0 - 0.08, 0])
        a, b = M["commit then publish"], M["publish then commit"]
        r1 = wrapped_label(rf"the order is saved, \ the event never sent: \ {num(a['committed'])} committed, \ "
                           rf"\textbf{{{a['lost_events']} events lost}}; \ payments and stock never hear of them",
                           5.4, font_size=19, color=NO).move_to([3.75, 1.15, 0])
        r2 = wrapped_label(rf"the event is sent, \ the order never saved: \ {num(b['committed'])} committed, \ "
                           rf"\textbf{{{b['phantom_events']} phantom orders}} announced, \ which others may act on",
                           5.4, font_size=19, color=NO).move_to([3.75, -1.0, 0])
        note = wrapped_label(r"swapping the order swaps the failure; \ retrying cannot help, \ because the process "
                             r"that would retry is the one that crashed", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.45)
        comp = label(r"computed", font_size=16, color=GREY_B).next_to(sub, RIGHT, buff=0.3)

        def run(ln, cm, res):
            self.play(ln[1][0].animate.set_fill(YES, opacity=0.45), run_time=0.6)
            self.play(FadeIn(cm, scale=0.4), run_time=0.5)
            self.play(ln[2].animate.set_opacity(0.25), ln[3].animate.set_opacity(0.25), FadeIn(res), run_time=0.8)
        with self.voiceover(
            "Suppose the service simply does the two writes in turn. We simulated ten thousand orders, with a one "
            "percent chance of a crash between them. <bookmark mark='a'/> Commit first, then publish: every order is "
            "saved, but after a crash no event is sent. A hundred and ten orders were never heard of. "
            "<bookmark mark='b'/> Publish first, then commit: a crash leaves an event for an order that was never "
            "saved. A hundred and ten phantom orders were announced. <bookmark mark='c'/> Swapping the order only "
            "swaps the failure, and retrying cannot help: the process that would retry is the one that crashed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub), FadeIn(comp), FadeIn(l1), FadeIn(l2))
            vo.wait_until("a")
            run(l1, c1, r1)
            vo.wait_until("b")
            run(l2, c2, r2)
            vo.wait_until("c")
            self.play(FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def outbox(self):
        o = load("outbox")
        M = o["modes"]
        head = label(r"The transactional outbox", font_size=36).to_edge(UP, buff=0.3)
        orders_t = VGroup(mono("orders", size=16, color=HEAD), mono("1042  placed", size=16, color=WHITE)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.1)
        sent = mono("no", size=16, color=NO)
        out_row = VGroup(mono("1042  OrderPlaced  sent:", size=16, color=WHITE), sent).arrange(RIGHT, buff=0.12)
        out_t = VGroup(mono("outbox", size=16, color=HEAD), out_row).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        rows = VGroup(orders_t, out_t).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        frame = DashedVMobject(RoundedRectangle(width=rows.width + 0.5, height=rows.height + 0.45, corner_radius=0.12,
                                                color=HEAD, stroke_width=2), num_dashes=50)
        rows.move_to([-4.5, 1.25, 0])
        frame.move_to(rows)
        ft = label(r"one local transaction", font_size=17, color=HEAD).next_to(frame, UP, buff=0.08)
        relay = module_box(r"relay", KERN, w=1.8, h=0.6, font=19).move_to([-0.3, 1.25, 0])
        broker = Rectangle(width=2.9, height=0.7, stroke_color=GREY_B, stroke_width=1.5).move_to([3.0, 1.25, 0])
        bt = label(r"broker", font_size=17, color=GREY_A).next_to(broker, UP, buff=0.08)
        cons = module_box(r"payments", YES, w=2.0, h=0.55, font=18).move_to([5.75, 1.25, 0])
        a1 = Arrow(frame.get_right(), relay.get_left(), buff=0.08, color=GREY_B, stroke_width=2,
                   max_tip_length_to_length_ratio=0.15)
        a2 = Arrow(relay.get_right(), broker.get_left(), buff=0.08, color=GREY_B, stroke_width=2,
                   max_tip_length_to_length_ratio=0.15)
        ev1 = tag_box("1042", HEAD, size=15).move_to(out_row)
        ev2 = tag_box("1042", HEAD, size=15).move_to(out_row)
        cm = crash_mark(0.2).next_to(relay, DOWN, buff=0.1)
        seen = label(r"seen 1042: \ ignore \ (chapter 5)", font_size=17, color=YES).next_to(cons, DOWN, buff=0.2)
        seen.align_to(cons, RIGHT)
        rows_t = []
        for k, name in (("commit then publish", r"commit, \ then publish"),
                        ("publish then commit", r"publish, \ then commit"), ("outbox", r"outbox")):
            m = M[k]
            rows_t.append([name, num(m["committed"]), str(m["lost_events"]), str(m["phantom_events"]),
                           str(m["duplicate_events"])])
        tab = grid_table([r"", r"orders committed", r"events lost", r"phantoms", r"duplicates"], rows_t,
                         widths=[3.2, 2.6, 2.0, 1.9, 2.0], row_h=0.42, font_size=19, mono_cols=())
        tab.move_to([0, -1.05, 0])
        for i, r in enumerate(rows_t, 1):
            for j in (2, 3):
                if r[j] != "0":
                    tab.cells[i][j].set_color(NO)
            if r[4] != "0":
                tab.cells[i][4].set_color(HEAD)
        tab.cells[3][0].set_color(YES)
        wal = VGroup(*[Rectangle(width=0.34, height=0.26, stroke_color=GREY_B, stroke_width=1, fill_color=DATA,
                                 fill_opacity=0.25 + 0.06 * i) for i in range(6)]).arrange(RIGHT, buff=0.04)
        wal.next_to(frame, DOWN, buff=0.3).align_to(frame, LEFT)
        wl = label(r"write-ahead log", font_size=16, color=DATA).next_to(wal, RIGHT, buff=0.12)
        a3 = Arrow(wl.get_right(), relay.get_bottom() + LEFT * 0.4, buff=0.08, color=DATA, stroke_width=2,
                   max_tip_length_to_length_ratio=0.15)
        cdc = wrapped_label(r"\textbf{change data capture}: \ instead of polling a table, \ a connector such as "
                            r"Debezium reads the database's own write-ahead log and publishes each committed change "
                            r"\ (Part 46)", 12.4, font_size=19, color=DATA).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The cure is to make the two writes one. <bookmark mark='a'/> In the same local transaction as the order,"
            " the service inserts the event into an outbox table. Both rows commit, or neither does. "
            "<bookmark mark='b'/> A relay publishes unsent rows, then marks them sent. If it crashes in between, it "
            "publishes again when it restarts. <bookmark mark='c'/> So an outbox never loses an event or invents one."
            " It can only duplicate, and chapter five's deduplication removes duplicates. <bookmark mark='d'/> Over "
            "the same ten thousand orders: nothing lost, no phantoms, a hundred and ten harmless duplicates. "
            "<bookmark mark='e'/> Change data capture tools such as Debezium read the database's own write-ahead log "
            "instead, as Part 46 will show."
        ) as vo:
            self.play(FadeIn(head), FadeIn(relay), FadeIn(broker), FadeIn(bt), FadeIn(cons), GrowArrow(a1),
                      GrowArrow(a2))
            vo.wait_until("a")
            self.play(Create(frame), FadeIn(ft), FadeIn(orders_t), FadeIn(out_t))
            vo.wait_until("b")
            self.play(Indicate(out_row, color=HEAD))
            self.add(ev1)
            self.play(ev1.animate.move_to(relay), run_time=0.6)
            self.play(ev1.animate.move_to(broker.get_center() + LEFT * 0.6), run_time=0.6)
            self.play(FadeIn(cm, scale=0.4), relay[0].animate.set_stroke(NO), run_time=0.5)
            self.play(FadeOut(cm), relay[0].animate.set_stroke(KERN), run_time=0.5)
            self.add(ev2)
            self.play(ev2.animate.move_to(relay), run_time=0.6)
            self.play(ev2.animate.move_to(broker.get_center() + RIGHT * 0.6), run_time=0.6)
            self.play(Transform(sent, mono("yes", size=16, color=YES).move_to(sent, aligned_edge=LEFT)))
            vo.wait_until("c")
            self.play(ev1.animate.move_to(cons.get_bottom() + DOWN * 0.05 + LEFT * 0.5).set_opacity(0),
                      Indicate(cons, scale_factor=1.06), run_time=0.8)
            strike = Line(ev2.get_left(), ev2.get_right(), color=NO, stroke_width=3)
            self.play(Create(strike), FadeIn(seen))
            vo.wait_until("d")
            self.play(FadeIn(tab))
            vo.wait_until("e")
            self.play(FadeIn(wal), FadeIn(wl), GrowArrow(a3), Transform(relay[1], label(
                r"Debezium", font_size=19, color=WHITE).move_to(relay)), FadeIn(cdc))
        self.wait(0.4)
        self.clear_scene()

    def saga(self):
        s = load("saga")
        head = label(r"Sagas: \ undo what cannot finish", font_size=36).to_edge(UP, buff=0.3)
        fwd = [r"reserve stock", r"charge card", r"book courier", r"send confirmation"]
        back = [r"release stock", r"refund card", r"cancel courier", None]
        tops = VGroup(*[module_box(t, DATA, w=2.6, h=0.6, font=19) for t in fwd]).arrange(RIGHT, buff=0.55)
        tops.move_to([0, 1.75, 0])
        bots = VGroup()
        for t, top in zip(back, tops):
            if t:
                bots.add(module_box(t, LAM, w=2.6, h=0.6, font=19).move_to(top).shift(DOWN * 1.35))
        fa = VGroup(*[Arrow(tops[i].get_right(), tops[i + 1].get_left(), buff=0.05, color=GREY_B, stroke_width=2,
                            max_tip_length_to_length_ratio=0.25) for i in range(3)])
        ba = VGroup(*[DashedLine(bots[i + 1].get_left(), bots[i].get_right(), buff=0.05, color=LAM, stroke_width=2,
                                 dash_length=0.08).add_tip(tip_length=0.15) for i in range(2)])
        ties = VGroup(*[DashedLine(tops[i].get_bottom(), bots[i].get_top(), color=GREY_D, stroke_width=1.5,
                                   dash_length=0.06) for i in range(3)])
        tl = label(r"$T_1 \ \dots\ T_n$: \ local transactions, \ each committed at once", font_size=17,
                   color=DATA).next_to(tops, UP, buff=0.15)
        cl = label(r"$C_1 \ \dots\ C_{n-1}$: \ their compensations, \ run in reverse", font_size=17,
                   color=LAM).next_to(bots, DOWN, buff=0.15).align_to(bots, LEFT)
        names = {t: i for i, t in enumerate(fwd)}
        comps = {t: i for i, t in enumerate(back) if t}
        log = VGroup(*[mono(f"{e[0]:<10} {e[1]}", size=16, color={"do": YES, "fail": NO, "compensate": LAM}[e[0]])
                       for e in s["example"]]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        lt = label(r"one order's log", font_size=17, color=GREY_A)
        VGroup(lt, log).arrange(DOWN, aligned_edge=LEFT, buff=0.12).move_to([-4.3, -2.35, 0])
        note = wrapped_label(r"Hector Garcia-Molina and Kenneth Salem \ (1987): \ a long transaction as a sequence of "
                             r"short ones, \ each with a compensating transaction; \ a compensation is a semantic "
                             r"undo \ --- \ a refund, \ not a deletion \ --- \ and is retried until it succeeds, \ so "
                             r"it must be idempotent", 7.0, font_size=19, color=WHITE).move_to([2.95, -2.35, 0])
        with self.voiceover(
            "An action that spans services needs more. <bookmark mark='a'/> In 1987 Hector Garcia-Molina and Kenneth "
            "Salem proposed the saga: a long transaction written as a sequence of short local ones, each committed at"
            " once and paired with a compensation that undoes it. Our order saga reserves stock, charges the card, "
            "books a courier and confirms. <bookmark mark='b'/> Here stock is reserved, the card is charged, and then"
            " no courier can be booked. <bookmark mark='c'/> So the saga runs backwards: refund the card, then "
            "release the stock. A compensation is a semantic undo, a refund rather than an erased charge, and it is "
            "retried until it succeeds, so it must be idempotent."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tops), GrowArrow(fa[0]), GrowArrow(fa[1]), GrowArrow(fa[2]), FadeIn(tl))
            self.play(FadeIn(bots), Create(ties), FadeIn(ba), FadeIn(cl), FadeIn(note))
            self.play(FadeIn(lt))
            vo.wait_until("b")
            for k, e in enumerate(s["example"]):
                if k == 3:
                    vo.wait_until("c")
                if e[0] == "do":
                    self.play(tops[names[e[1]]][0].animate.set_fill(YES, opacity=0.45), FadeIn(log[k]), run_time=0.7)
                elif e[0] == "fail":
                    box = tops[names[e[1]]]
                    x = label(r"$\times$", font_size=40, color=NO).next_to(box, UP, buff=0.02).shift(RIGHT * 0.9)
                    self.play(box[0].animate.set_fill(NO, opacity=0.45), FadeIn(x), FadeIn(log[k]), run_time=0.7)
                else:
                    i = comps[e[1]]
                    self.play(bots[i][0].animate.set_fill(LAM, opacity=0.5),
                              tops[i][0].animate.set_fill(GREY_D, opacity=0.3), FadeIn(log[k]), run_time=0.8)
        self.wait(0.4)
        self.clear_scene()

    def outcomes(self):
        s = load("saga")
        n = s["orders"]
        head = label(rf"{num(n)} sagas", font_size=36).to_edge(UP, buff=0.3)
        sub = label(r"failure probabilities 1\%, \ 3\% and 2\% at the first three steps; \ computed", font_size=19,
                    color=GREY_A).next_to(head, DOWN, buff=0.2)
        W, x0 = 12.0, -6.0
        wc = W * s["completed"] / n
        done = Rectangle(width=wc, height=0.55, stroke_width=0, fill_color=YES, fill_opacity=0.8)
        comp = Rectangle(width=W - wc, height=0.55, stroke_width=0, fill_color=LAM, fill_opacity=0.9)
        done.move_to([x0 + wc / 2, 1.5, 0])
        comp.next_to(done, RIGHT, buff=0)
        dl = label(rf"completed: \ {num(s['completed'])}", font_size=21, color=BLACK).move_to(done)
        cl = label(rf"compensated: \ {s['compensated']}", font_size=19, color=LAM).next_to(comp, UP, buff=0.12)
        cl.align_to(comp, RIGHT)
        # the compensated orders, opened out by the step that failed
        steps = [k for k in s["failed_at"] if s["failed_at"][k]]
        cols = [KERN, NO, HEAD]
        segs = VGroup()
        xx = x0
        short = {"reserve stock": r"stock", "charge card": r"charge", "book courier": r"courier"}
        for k, c in zip(steps, cols):
            w = W * s["failed_at"][k] / s["compensated"]
            r = Rectangle(width=w, height=0.55, stroke_width=0, fill_color=c, fill_opacity=0.8)
            r.move_to([xx + w / 2, 0.0, 0])
            t = label(rf"{short.get(k, k)}: \ {s['failed_at'][k]}", font_size=19, color=BLACK)
            if t.width > w - 0.1:
                t.width = w - 0.1
            t.move_to(r)
            segs.add(VGroup(r, t))
            xx += w
        fan = VGroup(DashedLine(comp.get_corner(DL), segs[0][0].get_corner(UL), color=GREY_C, stroke_width=1.5),
                     DashedLine(comp.get_corner(DR), segs[-1][0].get_corner(UR), color=GREY_C, stroke_width=1.5))
        fan.set_z_index(-1)
        cap = label(r"the compensated orders, \ by the step that failed", font_size=18, color=GREY_A).next_to(
            segs, DOWN, buff=0.12).align_to(segs, LEFT)
        retry = wrapped_label(rf"compensations that failed and were retried: \ {s['compensation_retries']}", 5.6,
                              font_size=21, color=LAM)
        inc = label(rf"orders left half done: \ {s['inconsistent']}", font_size=30, color=YES)
        box = SurroundingRectangle(inc, color=YES, buff=0.18, corner_radius=0.1)
        VGroup(retry, VGroup(inc, box)).arrange(RIGHT, buff=0.8).move_to([0, -1.35, 0])
        note = wrapped_label(r"the invariant checked on every order: \ it ends either fully done or fully undone "
                             r"\ --- \ no charge without stock, \ no courier without payment", 12.4, font_size=20,
                             color=WHITE).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "We ran ten thousand orders through the saga, with failures injected at the first three steps. "
            "<bookmark mark='a'/> Nine thousand three hundred and fifty-nine completed; six hundred and forty-one "
            "were compensated. <bookmark mark='b'/> A hundred and six failed reserving stock, three hundred and "
            "seventeen at the charge, and two hundred and eighteen at the courier. <bookmark mark='c'/> Fifty-seven "
            "compensations failed and were retried. And the number of orders left half done, money taken with no "
            "stock or a courier with no payment, was zero."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sub))
            vo.wait_until("a")
            self.play(GrowFromEdge(done, LEFT), FadeIn(dl), run_time=1.2)
            self.play(GrowFromEdge(comp, LEFT), FadeIn(cl))
            vo.wait_until("b")
            self.play(Create(fan))
            self.play(LaggedStart(*[FadeIn(g) for g in segs], lag_ratio=0.5), FadeIn(cap), run_time=1.8)
            vo.wait_until("c")
            self.play(FadeIn(retry))
            self.play(FadeIn(inc), Create(box), FadeIn(note))
        self.wait(0.4)
        self.clear_scene()

    def isolation(self):
        head = label(r"No isolation, \ and no two-phase commit", font_size=36).to_edge(UP, buff=0.3)
        x0, x1 = -6.2, -0.4
        y = 1.6
        axis = Arrow([x0, y - 0.45, 0], [x1, y - 0.45, 0], buff=0, color=GREY_C, stroke_width=1.5,
                     max_tip_length_to_length_ratio=0.04)
        segs = [(r"reserved", 0.0, 0.25, DATA), (r"charged", 0.25, 0.5, DATA), (r"refunded", 0.5, 0.75, LAM),
                (r"released", 0.75, 1.0, LAM)]
        bars = VGroup()
        for t, a, b, c in segs:
            r = Rectangle(width=(x1 - x0) * (b - a) - 0.04, height=0.42, stroke_width=0, fill_color=c,
                          fill_opacity=0.7).move_to([x0 + (x1 - x0) * (a + b) / 2, y, 0])
            bars.add(VGroup(r, label(t, font_size=17, color=BLACK).move_to(r)))
        sl = label(r"one saga, \ over time", font_size=17, color=GREY_A).next_to(bars, UP, buff=0.12).align_to(
            bars, LEFT)
        xr = x0 + (x1 - x0) * 0.37
        peek = Arrow([xr, y - 1.25, 0], [xr, y - 0.25, 0], buff=0, color=NO, stroke_width=3,
                     max_tip_length_to_length_ratio=0.2)
        pl = wrapped_label(r"another request reads now: \ the order looks paid, \ though it will be undone", 3.4,
                           font_size=18, color=NO).next_to(peek, RIGHT, buff=0.12).shift(DOWN * 0.35)
        fixes = VGroup(
            wrapped_label(r"\textbf{semantic lock}: \ the order says \texttt{PENDING} until the saga ends, \ and "
                          r"readers treat it so", 5.8, font_size=18, color=YES),
            wrapped_label(r"\textbf{commutative updates}: \ add and subtract, \ never overwrite, \ so steps and "
                          r"undos may interleave", 5.8, font_size=18, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.18).next_to(axis, DOWN, buff=1.05).align_to(axis, LEFT)
        # orchestration and choreography
        cy = 1.2
        specs = ((r"stock", KERN), (r"pay", YES), (r"courier", DATA))
        orch = module_box(r"orchestrator", HEAD, w=1.7, h=0.5, font=17).move_to([1.05, cy, 0])
        sv = VGroup(*[module_box(t, c, w=1.2, h=0.42, font=16) for t, c in specs]).arrange(DOWN, buff=0.14)
        sv.move_to([3.0, cy, 0])
        oa = VGroup(*[Arrow(orch.get_right(), s.get_left(), buff=0.05, color=HEAD, stroke_width=1.5,
                            max_tip_length_to_length_ratio=0.12) for s in sv])
        ol = label(r"orchestration", font_size=18, color=HEAD).move_to([2.0, 2.3, 0])
        ring = VGroup(*[module_box(t, c, w=1.2, h=0.42, font=16) for t, c in specs])
        for m, ang in zip(ring, (90, 210, 330)):
            m.move_to([5.4 + 0.9 * np.cos(np.radians(ang)), cy - 0.1 + 0.75 * np.sin(np.radians(ang)), 0])
        ends = ((ring[0].get_left(), ring[1].get_top()), (ring[1].get_right(), ring[2].get_left()),
                (ring[2].get_top(), ring[0].get_right()))
        ra = VGroup(*[CurvedArrow(a + 0.05 * (b - a), b, angle=0.5, color=GREY_B, stroke_width=1.5, tip_length=0.12)
                      for a, b in ends])
        rl = label(r"choreography", font_size=18, color=LAM).move_to([5.4, 2.3, 0])
        ocnote = wrapped_label(r"one coordinator that knows the steps, \ or services reacting to each other's "
                               r"events", 6.4, font_size=18, color=GREY_A).move_to([3.5, -0.3, 0])
        tpc = wrapped_label(r"why not \textbf{two-phase commit} across services? \ Part 39: \ every participant "
                            r"holds its locks until the coordinator decides, \ and a coordinator that dies blocks "
                            r"them all; \ one slow service would stall everyone, \ and brokers and outside APIs "
                            r"rarely take part", 12.4, font_size=19, color=NO).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Sagas pay for this. <bookmark mark='a'/> Each step commits at once, so there is no isolation: another "
            "request can see the order paid, just before the refund. <bookmark mark='b'/> Designs work around it with"
            " semantic locks, marking the order pending until the saga ends, and commutative updates that add and "
            "subtract rather than overwrite. <bookmark mark='c'/> An orchestrator can drive the steps, or services "
            "can react to each other's events: choreography. <bookmark mark='d'/> Why not two-phase commit across "
            "services? Part 39 showed that participants hold their locks until the coordinator decides, and a dead "
            "coordinator blocks them all."
        ) as vo:
            self.play(FadeIn(head), Create(axis), FadeIn(sl))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(b) for b in bars], lag_ratio=0.4), run_time=1.6)
            self.play(GrowArrow(peek), FadeIn(pl))
            vo.wait_until("b")
            self.play(FadeIn(fixes[0]))
            self.play(FadeIn(fixes[1]))
            vo.wait_until("c")
            self.play(FadeIn(orch), FadeIn(sv), Create(oa), FadeIn(ol))
            self.play(FadeIn(ring), Create(ra), FadeIn(rl), FadeIn(ocnote))
            vo.wait_until("d")
            self.play(FadeIn(tpc))
        self.wait(0.4)
        self.clear_scene()


_ = (BG,)
