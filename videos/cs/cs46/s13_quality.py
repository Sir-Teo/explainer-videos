from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs46.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table, load,
                                   module_box, mono, tag_box)


def tick(ok: bool, size=20):
    return label(r"\checkmark" if ok else r"$\times$", font_size=size, color=YES if ok else NO)


class Quality(VoiceoverScene):
    def construct(self):
        self.card()
        self.evolution()
        self.contracts()
        self.tests()
        self.lineage()
        self.publish()

    def card(self):
        card = chapter_card(12, r"Data you can trust", r"How do you know the numbers on the dashboard are right?",
                            lit=(2009, 2016), extra=((2009, r"Apache Avro"), (2016, r"dbt")), part=PART)
        with self.voiceover("Chapter twelve. Data you can trust."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def evolution(self):
        head = label(r"Schema evolution", font_size=36).to_edge(UP, buff=0.3)
        v1 = code_block(["record Order {", "  long   order_id;", "  long   amount;", "  string city;", "}"], size=16)
        v2 = code_block(["record Order {", "  long   order_id;", "  long   amount;", "  string city;",
                         '  string currency = "GBP";', "}"], size=16)
        v2[4].set_color(YES)
        t1 = label(r"version 1: \ last year's records", font_size=18, color=GREY_A)
        t2 = label(r"version 2: \ a field with a default", font_size=18, color=YES)
        g1 = VGroup(t1, v1).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        g2 = VGroup(t2, v2).arrange(DOWN, aligned_edge=LEFT, buff=0.15)
        VGroup(g1, g2).arrange(DOWN, aligned_edge=LEFT, buff=0.4).move_to([-4.6, 0.45, 0]).align_to(
            [-6.6, 0, 0], LEFT)
        y, n = True, False
        rules = [(r"add a field with a default", y, y), (r"add a field without one", n, y),
                 (r"remove a field that had a default", y, y), (r"rename a field \ (no alias)", n, n),
                 (r"widen \texttt{int} to \texttt{long}", y, n)]
        rows = [[t, r"yes" if b else r"no", r"yes" if f else r"no"] for t, b, f in rules]
        colors = [[WHITE, YES if b else NO, YES if f else NO] for _, b, f in rules]
        tab = grid_table([r"change \ (Avro's rules)", r"new reads old", r"old reads new"], rows,
                         widths=[4.6, 2.0, 2.0], row_h=0.52, font_size=21, colors=colors, mono_cols=())
        tab.move_to([2.45, 1.2, 0])
        sub = VGroup(label(r"\textbf{backward}: \ new readers, \ old data", font_size=19, color=DATA),
                     label(r"\textbf{forward}: \ old readers, \ new data", font_size=19, color=LAM)).arrange(
            RIGHT, buff=0.6).next_to(tab, DOWN, buff=0.3).align_to(tab, LEFT)
        fill = label(r"an old record read as version 2: \ currency $=$ ``GBP''", font_size=19, color=YES).next_to(
            sub, DOWN, buff=0.22).align_to(tab, LEFT)
        lines = VGroup(
            wrapped_label(r"a \textbf{schema registry} checks each new version against the rule its topic chose, \ "
                          r"backward by default, \ before any producer may use it", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"Iceberg tracks columns by numeric ID, \ not by name or position, \ so renaming and "
                          r"reordering are safe: \ Part 43's API evolution, \ for data", 12.4, font_size=20,
                          color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "The first threat to a pipeline is its input changing shape. <bookmark mark='a'/> An order record gains "
            "a currency field; last year's records lack it. <bookmark mark='b'/> Backward compatibility asks whether "
            "new readers can read old data: yes, because the new field has a default, which the reader fills in. "
            "Forward compatibility asks whether old readers can read new data: yes again; they skip fields they do "
            "not know. <bookmark mark='c'/> Avro's rules settle every change. A field without a default breaks "
            "backward compatibility, widening an integer breaks forward, and a rename breaks both. <bookmark "
            "mark='d'/> A schema registry checks each new version against its topic's rule, backward by default, "
            "before producers use it. And Iceberg names columns by number, so renames are safe there: Part 43's API "
            "evolution, for data."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g1))
            vo.wait_until("a")
            self.play(TransformFromCopy(v1, v2), FadeIn(t2))
            vo.wait_until("b")
            self.play(FadeIn(sub), FadeIn(VGroup(*tab.cells[0], tab.rule)), FadeIn(VGroup(*tab.cells[1])))
            self.play(FadeIn(fill))
            vo.wait_until("c")
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[2:]], lag_ratio=0.3), run_time=2)
            vo.wait_until("d")
            self.play(FadeIn(lines[0]))
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def contracts(self):
        head = label(r"Data contracts", font_size=36).to_edge(UP, buff=0.3)
        px = -5.3
        svc = module_box(r"orders service", KERN, w=2.4, h=0.55).move_to([px, 2.0, 0])
        db = module_box(r"its database", KERN, w=2.4, h=0.55).move_to([px, 0.9, 0])
        topic = module_box(r"outbox topic", KERN, w=2.4, h=0.55).move_to([px, -0.2, 0])
        down = VGroup(Arrow(svc.get_bottom(), db.get_top(), buff=0.05, stroke_width=2, color=GREY_B,
                            max_tip_length_to_length_ratio=0.25),
                      Arrow(db.get_bottom(), topic.get_top(), buff=0.05, stroke_width=2, color=GREY_B,
                            max_tip_length_to_length_ratio=0.25))
        terms = VGroup(*[VGroup(label(k, font_size=17, color=GREY_B), label(v, font_size=18, color=WHITE)).arrange(
            RIGHT, buff=0.2, aligned_edge=UP) for k, v in (
            (r"fields", r"\texttt{order\_id} long, \ \texttt{amount} long, \ \texttt{currency}"),
            (r"meaning", r"amount in pence, \ including VAT"),
            (r"freshness", r"within 15 minutes"),
            (r"owner", r"the payments team"),
            (r"changes", r"backward compatible only"))])
        for t in terms:
            t[1].next_to(t[0], RIGHT, buff=0.2)
        col = max(t[0].width for t in terms)
        for t in terms:
            t[1].shift(RIGHT * (col - t[0].width))
        terms.arrange(DOWN, aligned_edge=LEFT, buff=0.18)
        c_title = label(r"contract: \ \texttt{OrderPaid}, \ version 3", font_size=20, color=HEAD)
        c_body = VGroup(c_title, terms).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        c_box = SurroundingRectangle(c_body, color=HEAD, buff=0.22, corner_radius=0.1)
        contract = VGroup(c_box, c_body).move_to([-0.55, 0.9, 0])
        cons = VGroup(*[module_box(t, DATA, w=2.6, h=0.55) for t in (r"warehouse", r"fraud model",
                                                                     r"finance dashboard")]).arrange(
            DOWN, buff=0.4).move_to([5.0, 0.9, 0])
        feed = Arrow(topic.get_right(), contract.get_left() + DOWN * 0.6, buff=0.08, stroke_width=2, color=GREY_B,
                     max_tip_length_to_length_ratio=0.1)
        outs = VGroup(*[Arrow(contract.get_right(), c.get_left(), buff=0.08, stroke_width=2, color=DATA,
                              max_tip_length_to_length_ratio=0.12) for c in cons])
        pr = label(r"pull request: \ rename \texttt{amount} to \texttt{total}", font_size=18, color=HEAD)
        ci = label(r"contract check fails: \ blocked before deploy", font_size=18, color=NO)
        VGroup(pr, ci).arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(topic, DOWN, buff=0.45).align_to(
            [-6.6, 0, 0], LEFT)
        illus = note(r"illustrative", font_size=16).next_to(contract, DOWN, buff=0.15).align_to(contract, RIGHT)
        lines = VGroup(
            wrapped_label(r"the interface between teams, \ made explicit and versioned like an API; \ consumers "
                          r"build on it, \ never on the service's internal tables \ (Chapter 3's designed events)",
                          12.4, font_size=20, color=WHITE),
            wrapped_label(r"checked where the change is made, \ by the team that makes it: \ a breaking change needs a "
                          r"new version, \ run beside the old until consumers move", 12.4, font_size=20, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Most pipelines begin in a database that another team owns. <bookmark mark='a'/> The orders service "
            "writes its tables and publishes changes, through chapter three's outbox, to a topic. <bookmark "
            "mark='b'/> A data contract makes that interface explicit, like an API: fields and types, meanings, such "
            "as amount in pence including tax, freshness, ownership, and which changes are allowed. <bookmark "
            "mark='c'/> Consumers build on the contract, never on the service's internal tables. <bookmark "
            "mark='d'/> Now a developer renames amount to total. The contract is checked in the producer's "
            "continuous integration, so the change fails there, before deployment, not in a dashboard three days "
            "later. A breaking change needs a new version, run beside the old."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(svc), FadeIn(db), FadeIn(topic), Create(down))
            vo.wait_until("b")
            self.play(Create(c_box), FadeIn(c_title), GrowArrow(feed))
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.1) for t in terms], lag_ratio=0.3), FadeIn(illus),
                      run_time=2)
            vo.wait_until("c")
            self.play(LaggedStart(*[GrowArrow(o) for o in outs], lag_ratio=0.2), FadeIn(cons), FadeIn(lines[0]))
            vo.wait_until("d")
            self.play(FadeIn(pr))
            self.play(Indicate(terms[0], color=NO), FadeIn(ci))
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()

    def tests(self):
        j = load("job")
        r = j["results"]
        src = j["words"]
        over = (r["no dedup"]["total"] - src) / src * 100
        under = (src - r["watermark lag 5 s"]["total"]) / src * 100
        dups = [b + 1 for b in j["duplicated"]]          # books numbered from 1, as Chapter 13 shows them
        head = label(r"Tests on data", font_size=36).to_edge(UP, buff=0.3)
        yml = code_block(["- name: order_id", "  tests: [unique, not_null]", "- name: status", "  tests:",
                          "    - accepted_values:", "        values: [paid, refunded]", "- name: customer_id",
                          "  tests:", "    - relationships:", "        to: ref('customers')", "        field: id"],
                         size=16)
        y_t = label(r"declared beside the table \ (dbt)", font_size=18, color=GREY_A)
        VGroup(y_t, yml).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-4.6, 0.9, 0]).align_to(
            [-6.6, 0, 0], LEFT)
        sql = code_block(["select order_id", "from orders", "group by order_id", "having count(*) > 1"], size=16,
                         color=HEAD)
        s_t = label(r"\texttt{unique} compiles to a query for the rows that break it; \ none returned: \ pass",
                    font_size=18, color=HEAD)
        g_s = VGroup(s_t, sql).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([2.6, 1.75, 0]).align_to(
            [-0.9, 0, 0], LEFT)
        res_t = label(r"the same tests on Chapter 13's stream of novels", font_size=20, color=GREY_A)
        checks = [(rf"unique book in the arrivals: \ books {dups[0]} and {dups[1]} arrive twice", False),
                  (rf"word total equals the source's: \ without deduplication, \ {over:+.1f}\%", False),
                  (rf"word total, \ with a 5 s watermark: \ $-${under:.1f}\% \ ({len(j['late'])} late books "
                   r"dropped)", False),
                  (r"word total, \ exactly once: \ equal", True)]
        res = VGroup(*[VGroup(tick(ok), label(t, font_size=18, color=WHITE)).arrange(RIGHT, buff=0.2)
                       for t, ok in checks]).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        VGroup(res_t, res).arrange(DOWN, aligned_edge=LEFT, buff=0.22).next_to(g_s, DOWN, buff=0.5).align_to(
            g_s, LEFT)
        foot = wrapped_label(r"and checks no one writes by hand: \ today's row count against last week's, \ the "
                             r"newest timestamp against the clock", 12.4, font_size=20, color=WHITE).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Contracts say what data should be; tests check what it is. <bookmark mark='a'/> In dbt, which builds "
            "warehouse tables from SQL, tests sit beside each table: this key is unique and never empty, this status "
            "takes only these values, every customer exists in the customers table. <bookmark mark='b'/> Each test "
            "compiles to a query for the rows that break it, and passes when the query returns nothing. <bookmark "
            "mark='c'/> Run such tests on chapter thirteen's stream of novels. Uniqueness finds two books sent "
            "twice. Reconciling word totals with the source catches the pipeline without deduplication, nearly seven "
            "percent high, and the early watermark, ten percent low. <bookmark mark='d'/> Volume and freshness "
            "checks catch the failures nobody wrote a rule for."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(y_t), LaggedStart(*[FadeIn(ln) for ln in yml], lag_ratio=0.1), run_time=2)
            vo.wait_until("b")
            self.play(Indicate(yml[1], color=HEAD), FadeIn(g_s))
            vo.wait_until("c")
            self.play(FadeIn(res_t))
            for row in res:
                self.play(FadeIn(row, shift=RIGHT * 0.1), run_time=0.7)
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def lineage(self):
        head = label(r"Lineage", font_size=36).to_edge(UP, buff=0.3)
        layers = [
            (r"sources", KERN, [("orders", r"orders database"), ("pay", r"payments API"), ("clicks", r"clickstream")]),
            (r"staging", LAM, [("s_orders", r"\texttt{stg\_orders}"), ("s_pay", r"\texttt{stg\_payments}"),
                               ("s_clicks", r"\texttt{stg\_clicks}")]),
            (r"marts", DATA, [("rev", r"\texttt{revenue}"), ("ltv", r"\texttt{customer\_ltv}"),
                              ("funnel", r"\texttt{funnel}")]),
            (r"consumers", YES, [("fin", r"finance dashboard"), ("churn", r"churn model"),
                                 ("email", r"weekly email")]),
        ]
        edges = [("orders", "s_orders"), ("pay", "s_pay"), ("clicks", "s_clicks"), ("s_orders", "rev"),
                 ("s_pay", "rev"), ("s_orders", "ltv"), ("s_pay", "ltv"), ("s_orders", "funnel"),
                 ("s_clicks", "funnel"), ("rev", "fin"), ("ltv", "churn"), ("rev", "email"), ("funnel", "email")]
        xs = [-5.3, -1.85, 1.6, 5.05]
        ys = [1.75, 0.65, -0.45]
        node, titles = {}, VGroup()
        for (title, color, items), x in zip(layers, xs):
            titles.add(label(title, font_size=18, color=GREY_B).move_to([x, 2.6, 0]))
            for (key, text), y in zip(items, ys):
                node[key] = module_box(text, color, w=2.6, h=0.55, font=17).move_to([x, y, 0])
        arrows = {(a, b): Arrow(node[a].get_right(), node[b].get_left(), buff=0.06, stroke_width=1.8, color=GREY_C,
                                max_tip_length_to_length_ratio=0.1) for a, b in edges}
        bad = "s_pay"

        def reach(start, forward=True):
            seen, todo = set(), [start]
            while todo:
                v = todo.pop()
                for a, b in edges:
                    nxt = b if forward else a
                    if (a if forward else b) == v and nxt not in seen:
                        seen.add(nxt)
                        todo.append(nxt)
            return seen
        down, up = reach(bad), reach(bad, forward=False)
        cross = label(r"test fails", font_size=17, color=NO).next_to(node[bad], DOWN, buff=0.12)
        lines = VGroup(
            wrapped_label(r"dbt reads the graph from each model's \texttt{ref()} calls and builds in topological "
                          r"order: \ Part 41's build system, \ with tables for files", 12.4, font_size=20,
                          color=WHITE),
            wrapped_label(r"forward from a failure: \ everything now suspect, \ to stop and to warn; \ backward: \ "
                          r"the way to the cause", 12.4, font_size=20, color=NO),
            wrapped_label(r"lineage by column narrows it further; \ OpenLineage is an open format in which "
                          r"schedulers and engines report these edges as they run", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Tables are built from tables, and their dependencies form a graph. <bookmark mark='a'/> Sources feed "
            "staging tables, which feed the marts analysts query, which feed dashboards, models and reports. dbt "
            "reads this graph from the references in each model's SQL and builds it in topological order: Part 41's "
            "build system, with tables for files. <bookmark mark='b'/> Now a test on the staging payments table "
            "fails. Following edges forward, the graph names everything now suspect; those builds stop, and their "
            "owners are told. <bookmark mark='c'/> Following edges backward leads towards the cause, the payments "
            "interface. <bookmark mark='d'/> Column-level lineage narrows it further, and the OpenLineage standard "
            "lets engines report these edges as they run."
        ) as vo:
            self.play(FadeIn(head), FadeIn(titles))
            vo.wait_until("a")
            for k in range(4):
                keys = [key for key, _ in layers[k][2]]
                into = [arrows[e] for e in edges if e[1] in keys]
                self.play(*[GrowArrow(a) for a in into], *[FadeIn(node[key]) for key in keys], run_time=0.8)
            self.play(FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(node[bad][0].animate.set_stroke(NO, width=4).set_fill(NO, opacity=0.3), FadeIn(cross))
            self.play(*[node[k][0].animate.set_stroke(NO, width=3).set_fill(NO, opacity=0.15) for k in down],
                      *[a.animate.set_color(NO) for (s, t), a in arrows.items() if s == bad or s in down],
                      run_time=1.5)
            self.play(FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(*[node[k][0].animate.set_stroke(HEAD, width=4) for k in up],
                      *[a.animate.set_color(HEAD) for (s, t), a in arrows.items() if t == bad or t in up])
            vo.wait_until("d")
            self.play(FadeIn(lines[2]))
        self.wait(0.4)
        self.clear_scene()

    def publish(self):
        head = label(r"Write, \ audit, \ publish", font_size=36).to_edge(UP, buff=0.3)
        y = 1.2
        xs = [-5.2, -3.0, -0.4]
        strip = Line([-6.2, y, 0], [6.4, y, 0], color=GREY_D, stroke_width=2)
        dots = VGroup(Dot([xs[0], y, 0], radius=0.12, color=DATA), Dot([xs[1], y, 0], radius=0.12, color=DATA))
        names = VGroup(*[label(f"v{40 + k}", font_size=18, color=GREY_A).next_to(d, DOWN, buff=0.15)
                         for k, d in enumerate(dots)])
        staged = DashedVMobject(Circle(radius=0.17, color=HEAD, stroke_width=3), num_dashes=10).move_to([xs[2], y, 0])
        staged_l = label(r"v42, \ staged", font_size=18, color=HEAD).next_to(staged, DOWN, buff=0.15)
        cur = label(r"what readers see", font_size=18, color=YES)
        arr = Arrow(UP * 0.5, ORIGIN, buff=0, stroke_width=3, color=YES, max_tip_length_to_length_ratio=0.35)
        pointer = VGroup(cur, arr).arrange(DOWN, buff=0.05).next_to(dots[1], UP, buff=0.08)
        audit = VGroup(*[VGroup(tick(True, 18), label(t, font_size=18, color=WHITE)).arrange(RIGHT, buff=0.15)
                         for t in (r"unique", r"not null", r"totals reconcile")]).arrange(DOWN, aligned_edge=LEFT,
                                                                                       buff=0.12)
        audit.next_to(staged_l, DOWN, buff=0.3).align_to(staged_l, LEFT)
        v42 = Dot([xs[2], y, 0], radius=0.12, color=DATA)
        bad = DashedVMobject(Circle(radius=0.17, color=NO, stroke_width=3), num_dashes=10).move_to([2.4, y, 0])
        bad_l = label(r"v43, \ staged", font_size=18, color=NO).next_to(bad, DOWN, buff=0.15)
        bad_t = VGroup(tick(False, 18), label(r"audit fails: \ never published; \ readers keep v42", font_size=18,
                                              color=NO)).arrange(RIGHT, buff=0.15)
        bad_t.next_to(bad_l, DOWN, buff=0.3).align_to(bad_l, LEFT)
        lines = VGroup(
            wrapped_label(r"Chapter 10's atomic commit makes publishing one pointer swap; \ Iceberg supports the "
                          r"pattern with branches of a table", 12.4, font_size=20, color=WHITE),
            wrapped_label(r"trust is engineered: \ contracts where data is made, \ tests at every step, \ lineage to "
                          r"trace a failure, \ and nobody ever sees half of one", 12.4, font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Tests help most before anyone reads the data. <bookmark mark='a'/> Chapter ten's tables make that "
            "cheap: a job writes its new snapshot but does not publish it, and readers still see version forty-one. "
            "<bookmark mark='b'/> The tests run on the staged snapshot. If they pass, publishing is one atomic "
            "pointer swap, and every reader moves to forty-two at once. <bookmark mark='c'/> If they fail, the "
            "snapshot is never published, and readers keep the last good version. This is write, audit, publish, "
            "which Iceberg supports with branches of a table. <bookmark mark='d'/> Trust, then, is engineered: "
            "contracts where data is made, tests at every step, lineage to trace failures, and atomic publishing."
        ) as vo:
            self.play(FadeIn(head), Create(strip), FadeIn(dots), FadeIn(names), FadeIn(pointer))
            vo.wait_until("a")
            self.play(Create(staged), FadeIn(staged_l))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(a, shift=RIGHT * 0.1) for a in audit], lag_ratio=0.3))
            self.play(FadeTransform(staged, v42), pointer.animate.next_to(v42, UP, buff=0.08),
                      Transform(staged_l, label(r"v42", font_size=18, color=GREY_A).move_to(staged_l)))
            self.play(FadeIn(lines[0]))
            vo.wait_until("c")
            self.play(Create(bad), FadeIn(bad_l))
            self.play(FadeIn(bad_t))
            vo.wait_until("d")
            self.play(FadeIn(lines[1]))
        self.wait(0.4)
        self.clear_scene()


_ = (BG, LAM, mono, tag_box)
