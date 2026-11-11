from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load,
                                   module_box, mono, tag_box)


class Cdc(VoiceoverScene):
    def construct(self):
        self.card()
        self.dual()
        self.wal()
        self.outbox()
        self.fold()
        self.cqrs()

    def card(self):
        card = chapter_card(3, r"Changes as events", r"Can a database's history become everyone's input?",
                            lit=(2005,), extra=((2005, r"Fowler: \ event sourcing"),), part=PART)
        with self.voiceover("Chapter three. Changes as events."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def dual(self):
        head = label(r"Two writes, \ no transaction", font_size=36).to_edge(UP, buff=0.3)
        app = module_box(r"application", HEAD, w=2.4, h=0.7).move_to([-4.6, 1.0, 0])
        db = module_box(r"database", DATA, w=2.4, h=0.7).move_to([0.4, 1.9, 0])
        idx = module_box(r"search index", LAM, w=2.4, h=0.7).move_to([0.4, 0.1, 0])
        a1 = Arrow(app.get_right(), db.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5)
        a2 = Arrow(app.get_right(), idx.get_left(), buff=0.1, color=GREY_B, stroke_width=2.5)
        v_db = mono("price = 12", size=16, color=YES).next_to(db, RIGHT, buff=0.3)
        v_ix = mono("price = 10", size=16, color=NO).next_to(idx, RIGHT, buff=0.3)
        crash = Cross(scale_factor=0.25, stroke_color=NO, stroke_width=6).move_to(a2)
        crash_l = label(r"crash", font_size=18, color=NO).next_to(crash, DOWN, buff=0.1)
        race = VGroup(
            label(r"or two writers race:", font_size=19, color=GREY_A),
            mono("database:  A then B   ->  B wins", size=16, color=DATA),
            mono("index:     B then A   ->  A wins", size=16, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        illus = note(r"illustrative", font_size=16).next_to(idx, DOWN, buff=0.2)
        race.next_to(illus, DOWN, buff=0.4).align_to(idx, LEFT)
        notes = VGroup(
            wrapped_label(r"writing to two systems without a shared transaction leaves them disagreeing, \ and "
                          r"nothing notices: \ no error, \ just two answers", 12.4, font_size=21, color=NO),
            wrapped_label(r"the cure: \ write once, \ to the database, \ and derive every other copy from the order "
                          r"in which the database committed", 12.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "A company's data lives first in databases, and other systems need copies of it: a search index, a cache,"
            " the warehouse. <bookmark mark='a'/> The tempting design is a dual write: the application writes the "
            "database, then the index. <bookmark mark='b'/> If it crashes between the two, the database says twelve "
            "and the index says ten, for ever, with no error anywhere. <bookmark mark='c'/> Worse, two writers can "
            "race, and the two systems apply their writes in opposite orders. <bookmark mark='d'/> The cure is to "
            "write once, to the database, and derive every other copy from the one authoritative order: the order in "
            "which the database committed."
        ) as vo:
            self.play(FadeIn(head), FadeIn(app), FadeIn(db), FadeIn(idx), FadeIn(illus))
            vo.wait_until("a")
            self.play(GrowArrow(a1), FadeIn(v_db))
            vo.wait_until("b")
            self.play(GrowArrow(a2))
            self.play(Create(crash), FadeIn(crash_l), FadeIn(v_ix), FadeIn(notes[0]))
            vo.wait_until("c")
            self.play(FadeIn(race, shift=LEFT * 0.2))
            vo.wait_until("d")
            self.play(FadeIn(notes[1]))
        self.wait(0.4)
        self.clear_scene()

    def wal(self):
        head = label(r"The database's log, \ as a stream", font_size=36).to_edge(UP, buff=0.3)
        tab = grid_table([r"id", r"balance"], [["4", "120"], ["7", "50"], ["8", "75"], ["9", "10"]],
                         widths=[0.9, 1.4], row_h=0.42, font_size=18, mono_cols=(0, 1))
        tab.move_to([-5.2, 1.0, 0])
        row9 = VGroup(*tab.cells[4])
        row9.set_opacity(0)
        t_title = label(r"table \texttt{accounts}", font_size=18, color=DATA).next_to(tab, UP, buff=0.15)
        wal = code_block(["lsn 101  update id=7  50 -> 30", "lsn 102  insert id=9  10",
                          "lsn 103  delete id=4"], size=15)
        wal.move_to([-0.6, 1.0, 0])
        w_frame = SurroundingRectangle(wal, buff=0.18, corner_radius=0.08, color=KERN, stroke_width=1.5)
        w_title = label(r"write-ahead log \ (Part 35)", font_size=18, color=KERN).next_to(w_frame, UP, buff=0.15)
        parts = VGroup()
        for p in range(2):
            parts.add(VGroup(label(rf"partition {p}", font_size=16, color=GREY_A),
                             Line(ORIGIN, RIGHT * 2.0, color=GREY_D, stroke_width=1.5)).arrange(RIGHT, buff=0.2))
        parts.arrange(DOWN, aligned_edge=LEFT, buff=0.55).move_to([4.9, 1.0, 0])
        p_title = label(r"topic, \ keyed by id", font_size=18, color=YES).next_to(parts, UP, buff=0.3)
        ev = [("7: u", 1, 0), ("9: c", 1, 1), ("4: d", 0, 0)]
        evs = [tag_box(t, color=YES, size=15, w=0.85, h=0.42).move_to(
            [parts[p][1].get_left()[0] + 0.5 + 1.0 * j, parts[p][1].get_y(), 0]) for t, p, j in ev]
        ar1 = Arrow(w_frame.get_right(), parts.get_left() + LEFT * 0.05, buff=0.12, color=GREY_B, stroke_width=2)
        ar1_l = label(r"CDC", font_size=16, color=GREY_B).next_to(ar1, UP, buff=0.05)
        ar0 = Arrow(tab.get_right(), w_frame.get_left(), buff=0.12, color=GREY_B, stroke_width=2)
        js = code_block(['{"op": "u",', ' "before": {"id": 7, "balance": 50},', ' "after":  {"id": 7, "balance": 30},',
                         ' "source": {"lsn": 101, ...}}'], size=15)
        js.move_to([-3.6, -1.75, 0])
        js_t = label(r"one change event", font_size=16, color=YES).next_to(js, UP, buff=0.12).align_to(js, LEFT)
        notes = VGroup(
            wrapped_label(r"PostgreSQL's logical decoding and MySQL's binary log expose the log; \ Debezium turns "
                          r"each committed change into an event", 5.9, font_size=19, color=WHITE),
            wrapped_label(r"keyed by primary key, \ so each row's changes stay in order \ (chapter 1)", 5.9,
                          font_size=19, color=YES),
            wrapped_label(r"to start: \ snapshot the table, \ then follow the log from the position the snapshot "
                          r"saw", 5.9, font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22).move_to([3.6, -1.75, 0])
        illus = note(r"illustrative", font_size=16).next_to(tab, DOWN, buff=0.15)
        wl = list(wal)
        for w in wl:
            w.set_opacity(0)
        with self.voiceover(
            "And the database already writes that order down. <bookmark mark='a'/> Every committed change goes first "
            "into its write-ahead log, from Part 35. Change data capture reads that log and publishes each change as "
            "an event. <bookmark mark='b'/> An update, an insert and a delete become three events in a topic keyed by"
            " the row's id, so each row's changes stay in order, as in chapter one. <bookmark mark='c'/> An event "
            "carries the row before and after, and its position in the log. PostgreSQL exposes its log through "
            "logical decoding, MySQL through its binary log, and Debezium turns both into streams. "
            "<bookmark mark='d'/> To begin, the connector snapshots the table, then follows the log from exactly the "
            "position the snapshot saw."
        ) as vo:
            self.play(FadeIn(head), FadeIn(tab), FadeIn(t_title), FadeIn(illus), Create(w_frame), FadeIn(w_title),
                      FadeIn(parts), FadeIn(p_title))
            vo.wait_until("a")
            self.play(GrowArrow(ar0), GrowArrow(ar1), FadeIn(ar1_l))
            vo.wait_until("b")
            new7 = mono("30", size=18, color=HEAD).move_to(tab.cells[2][1])
            self.play(Transform(tab.cells[2][1], new7), wl[0].animate.set_opacity(1))
            self.play(TransformFromCopy(wl[0], evs[0]), run_time=0.8)
            self.play(row9.animate.set_opacity(1), wl[1].animate.set_opacity(1))
            self.play(TransformFromCopy(wl[1], evs[1]), run_time=0.8)
            self.play(VGroup(*tab.cells[1]).animate.set_opacity(0.25), wl[2].animate.set_opacity(1))
            self.play(TransformFromCopy(wl[2], evs[2]), run_time=0.8)
            vo.wait_until("c")
            self.play(FadeIn(js_t), FadeIn(js), FadeIn(notes[1]))
            self.play(FadeIn(notes[0]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def outbox(self):
        head = label(r"The outbox, \ again", font_size=36).to_edge(UP, buff=0.3)
        sql = code_block(["BEGIN;", "UPDATE orders SET status = 'paid' WHERE id = 42;",
                          "INSERT INTO outbox (event_id, type, payload)",
                          "  VALUES ('e-981', 'OrderPaid', '{\"order\": 42}');", "COMMIT;"], size=16)
        sql.move_to([-2.2, 1.55, 0])
        frame = SurroundingRectangle(sql, buff=0.2, corner_radius=0.08, color=HEAD, stroke_width=1.6)
        f_l = label(r"one transaction", font_size=18, color=HEAD).next_to(frame, UP, buff=0.1).align_to(frame, LEFT)
        sql[1].set_color(DATA)
        sql[2].set_color(YES)
        sql[3].set_color(YES)
        wal = module_box(r"write-ahead log", KERN, w=2.4, h=0.6).move_to([-4.6, -0.6, 0])
        cdc = module_box(r"CDC: \ outbox table only", GREY_B, w=3.0, h=0.6).move_to([-0.6, -0.6, 0])
        topic = module_box(r"topic \texttt{orders}", YES, w=2.2, h=0.6).move_to([3.4, -0.6, 0])
        flow = VGroup(Arrow(frame.get_bottom() + LEFT * 2.4, wal.get_top(), buff=0.1, color=GREY_B, stroke_width=2),
                      Arrow(wal.get_right(), cdc.get_left(), buff=0.1, color=GREY_B, stroke_width=2),
                      Arrow(cdc.get_right(), topic.get_left(), buff=0.1, color=GREY_B, stroke_width=2))
        ev = tag_box("OrderPaid  e-981", color=YES, size=15).next_to(topic, RIGHT, buff=0.2)
        if ev.get_right()[0] > 6.85:
            ev.next_to(topic, DOWN, buff=0.2)
        illus = note(r"illustrative", font_size=16).next_to(frame, RIGHT, buff=0.2).align_to(frame, UP)
        notes = VGroup(
            wrapped_label(r"the state change and the event commit together or not at all \ (Part 43): \ no dual "
                          r"write", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"the event is a designed contract, \ \texttt{OrderPaid}, \ not a copy of the internal "
                          r"table, \ so the table can change shape without breaking its readers", 12.4, font_size=20,
                          color=YES),
            wrapped_label(r"delivery is at least once, \ so readers drop duplicates by \texttt{event\_id}; \ "
                          r"exactly once comes in chapter 5", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Raw change capture has one drawback: it publishes the database's internal tables, and every reader comes"
            " to depend on their columns. Part 43's outbox fixes that. <bookmark mark='a'/> In the transaction that "
            "marks order forty-two as paid, the service also inserts a row into an outbox table, describing the "
            "event. Both commit, or neither does. <bookmark mark='b'/> Change data capture follows only the outbox, "
            "and publishes its rows to a topic. <bookmark mark='c'/> The event is a designed contract, order paid, "
            "not a copy of a table, and the table can now change shape freely. <bookmark mark='d'/> Delivery is still"
            " at least once: a connector that crashes before recording its position publishes again, so readers drop "
            "duplicates by the event's identifier."
        ) as vo:
            self.play(FadeIn(head), FadeIn(sql), Create(frame), FadeIn(f_l), FadeIn(illus))
            vo.wait_until("a")
            self.play(Indicate(sql[1], color=DATA, scale_factor=1.05))
            self.play(Indicate(sql[2:4], color=YES, scale_factor=1.05))
            self.play(FadeIn(notes[0]))
            vo.wait_until("b")
            self.play(FadeIn(wal), GrowArrow(flow[0]))
            self.play(GrowArrow(flow[1]), FadeIn(cdc))
            self.play(GrowArrow(flow[2]), FadeIn(topic))
            self.play(FadeIn(ev, shift=RIGHT * 0.2))
            vo.wait_until("c")
            self.play(FadeIn(notes[1]))
            vo.wait_until("d")
            self.play(FadeIn(notes[2]))
        self.wait(0.4)
        self.clear_scene()

    def fold(self):
        c = load("compaction")
        head = label(r"State is a fold over events", font_size=36).to_edge(UP, buff=0.3)
        events = [("opened", 0), ("deposited 50", 50), ("withdrew 20", -20), ("deposited 10", 10)]
        boxes = VGroup(*[tag_box(t, color=DATA, size=16, w=2.3, h=0.5) for t, _ in events]).arrange(RIGHT, buff=0.35)
        boxes.next_to(head, DOWN, buff=0.7)
        arrows = VGroup(*[Arrow(a.get_right(), b.get_left(), buff=0.04, color=GREY_C, stroke_width=1.5,
                                max_tip_length_to_length_ratio=0.3) for a, b in zip(boxes, boxes[1:])])
        bal, states = 0, []
        for _, d in events:
            bal += d
            states.append(bal)

        def state_box(v, k):
            b = tag_box(f"balance {v}", color=YES, size=17, w=2.3, h=0.5)
            return b.next_to(boxes[k], DOWN, buff=0.75)
        st = state_box(states[0], 0)
        arr = Arrow(boxes[0].get_bottom(), st.get_top(), buff=0.06, color=YES, stroke_width=2.5)
        illus = note(r"illustrative", font_size=16).next_to(boxes, UP, buff=0.12).align_to(boxes, RIGHT)
        formula = label(r"$\text{state}_n = \text{apply}(\text{state}_{n-1}, \ \text{event}_n)$, \ \ "
                        r"state $=$ fold(apply, empty, events)", font_size=22, color=WHITE)
        formula.next_to(st, DOWN, buff=0.45).set_x(0)
        dual = VGroup(
            module_box(r"stream of changes", DATA, w=2.9, h=0.6),
            module_box(r"table", YES, w=1.8, h=0.6),
        ).arrange(RIGHT, buff=3.0).next_to(formula, DOWN, buff=1.05).set_x(-1.7)
        top = CurvedArrow(dual[0].get_top() + UP * 0.05, dual[1].get_top() + UP * 0.05, angle=-0.6, color=YES,
                          stroke_width=2)
        bot = CurvedArrow(dual[1].get_bottom() + DOWN * 0.05, dual[0].get_bottom() + DOWN * 0.05, angle=-0.6,
                          color=DATA, stroke_width=2)
        tl = label(r"fold", font_size=17, color=YES).next_to(top, UP, buff=0.05)
        bl = label(r"record each change", font_size=17, color=DATA).next_to(bot, DOWN, buff=0.05)
        res = wrapped_label(rf"chapter 1's compacted topic: \ {c['events']:,} updates folded to {c['keys']} rows, "
                            r"\ the same table", 3.8, font_size=18, color=GREY_A).next_to(dual, RIGHT, buff=0.35)
        with self.voiceover(
            "Now turn the picture around. If every change is an event, the current state is a summary of the events "
            "so far. <bookmark mark='a'/> An account is opened, fifty is deposited, twenty withdrawn, ten deposited, "
            "and the balance runs zero, fifty, thirty, forty. <bookmark mark='b'/> The state is a fold: an apply "
            "function run over the events, starting from empty. The same events always give the same state. "
            "<bookmark mark='c'/> So streams and tables are two views of one thing. Folding a stream of changes gives"
            " a table; recording each change to a table gives a stream. Chapter one's compacted topic is exactly "
            "this: two thousand updates folded into fifty rows."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes[0]), FadeIn(illus))
            vo.wait_until("a")
            self.play(GrowArrow(arr), FadeIn(st))
            for k in range(1, len(events)):
                nxt = state_box(states[k], k)
                self.play(FadeIn(boxes[k]), GrowArrow(arrows[k - 1]), run_time=0.6)
                self.play(Transform(st, nxt), arr.animate.put_start_and_end_on(boxes[k].get_bottom() + DOWN * 0.06,
                                                                               nxt.get_top() + UP * 0.06),
                          run_time=0.9)
            vo.wait_until("b")
            self.play(FadeIn(formula))
            vo.wait_until("c")
            self.play(FadeIn(dual), Create(top), Create(bot), FadeIn(tl), FadeIn(bl))
            self.play(FadeIn(res))
        self.wait(0.4)
        self.clear_scene()

    def cqrs(self):
        head = label(r"Event sourcing and CQRS", font_size=36).to_edge(UP, buff=0.3)
        cmd = module_box(r"commands", HEAD, w=2.0, h=0.6).move_to([-5.6, 1.5, 0])
        log = VGroup(*[Rectangle(width=0.42, height=0.6, stroke_color=GREY_B, stroke_width=1.2, fill_color=DATA,
                                 fill_opacity=0.5) for _ in range(9)]).arrange(RIGHT, buff=0).move_to([-0.7, 1.5, 0])
        log_l = label(r"the event log: \ the system of record", font_size=17, color=DATA).next_to(log, UP, buff=0.12)
        a0 = Arrow(cmd.get_right(), log.get_left(), buff=0.1, color=GREY_B, stroke_width=2)
        a0_l = label(r"validate, \ append", font_size=16, color=GREY_B).next_to(a0, DOWN, buff=0.08)
        views = VGroup(*[module_box(t, c, w=2.8, h=0.55, font=17) for t, c in (
            (r"balances by account", YES), (r"monthly statements", LAM), (r"search index", KERN),
            (r"fraud features", NO))]).arrange(DOWN, buff=0.18).move_to([4.6, 1.0, 0])
        views_l = label(r"read models: \ folds", font_size=17, color=YES).next_to(views, UP, buff=0.12)
        fan = VGroup(*[Arrow(log.get_right(), v.get_left(), buff=0.1, color=GREY_C, stroke_width=1.5,
                             max_tip_length_to_length_ratio=0.08) for v in views])
        pros = VGroup(
            wrapped_label(r"commands and queries are separated: \ one write model, \ as many read models as there "
                          r"are questions, \ each rebuilt by replaying the log", 6.2, font_size=19, color=YES),
            wrapped_label(r"an audit trail for free, \ and a bug in a view is fixed by replaying into a corrected "
                          r"one", 6.2, font_size=19, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        cons = VGroup(
            wrapped_label(r"read models lag the log: \ a user may not see their own write at once \ (Part 39)", 6.0,
                          font_size=19, color=NO),
            wrapped_label(r"events are kept for ever, \ so their schemas must evolve compatibly \ (Part 43), \ and "
                          r"forgetting a person is hard", 6.0, font_size=19, color=NO),
            wrapped_label(r"replay grows with history: \ periodic snapshots of the state bound it", 6.0,
                          font_size=19, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.22)
        VGroup(pros, cons).arrange(RIGHT, buff=0.5, aligned_edge=UP).next_to(views, DOWN, buff=0.6).set_x(0)
        with self.voiceover(
            "Event sourcing, as Martin Fowler described it in 2005, builds a whole application this way. "
            "<bookmark mark='a'/> Commands are checked against the current state and, if valid, append events to a "
            "log, and that log is the system of record. <bookmark mark='b'/> Each question gets its own read model, a"
            " fold over the same events: balances, statements, a search index, fraud features. Separating the write "
            "model from the read models is called command query responsibility segregation, or CQRS. A buggy view is "
            "rebuilt by replay. <bookmark mark='c'/> The costs: read models lag the log, so users may not see their "
            "own writes at once. Events are kept for ever, so their schemas must evolve, as in Part 43, and "
            "forgetting a person is hard. And replay grows with history, which snapshots bound."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cmd))
            vo.wait_until("a")
            self.play(GrowArrow(a0), FadeIn(a0_l), FadeIn(log_l))
            self.play(LaggedStart(*[FadeIn(r, shift=LEFT * 0.2) for r in log], lag_ratio=0.2), run_time=1.8)
            vo.wait_until("b")
            self.play(FadeIn(views_l), LaggedStart(*[AnimationGroup(GrowArrow(f), FadeIn(v)) for f, v in
                                                     zip(fan, views)], lag_ratio=0.4), run_time=2.4)
            self.play(FadeIn(pros))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(x) for x in cons], lag_ratio=0.6), run_time=3)
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM)
