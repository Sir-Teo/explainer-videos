from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs40.common import (DATA, HEAD, KERN, LAM, NO, PART, YES, code_block, grid_table)


class Design(VoiceoverScene):
    def construct(self):
        self.card()
        self.solid()
        self.patterns()
        self.expression()
        self.functional()

    def card(self):
        card = chapter_card(4, r"Design, \ in the large and the small", r"What shapes keep code changeable?",
                            lit=(1994, 2000), extra=((1994, r"Gamma, Helm, Johnson and Vlissides: \ Design Patterns"),
                                                     (1998, r"Wadler: \ the expression problem"),
                                                     (2000, r"Martin: \ SOLID")), part=PART)
        with self.voiceover("Chapter four. Design, in the large and the small."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def solid(self):
        head = label(r"SOLID, \ each with the mistake it prevents", font_size=34).to_edge(UP, buff=0.3)
        rows = [[r"\textbf{S}ingle responsibility", r"one reason to change", r"a report class that formats, "
                 r"queries and emails"],
                [r"\textbf{O}pen--closed", r"extend without editing", r"a \texttt{switch} on type, edited for every "
                 r"new case"],
                [r"\textbf{L}iskov substitution", r"subtypes keep the contract", r"\texttt{Square(Rectangle)}, \ "
                 r"Chapter 2"],
                [r"\textbf{I}nterface segregation", r"small, focused interfaces", r"a printer interface that forces "
                 r"\texttt{fax()} on every printer"],
                [r"\textbf{D}ependency inversion", r"depend on abstractions", r"policy importing a database driver, "
                 r"Chapter 3"]]
        tab = grid_table([r"principle", r"in one line", r"the counterexample"], rows, widths=[3.6, 3.4, 5.6],
                         row_h=0.62, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for k in range(1, 6):
            tab.cells[k][2].set_color(NO)
            tab.cells[k][0].set_color(HEAD)
        foot = wrapped_label(r"heuristics, \ not laws: \ each is Parnas' hiding seen from one side, \ and each can be "
                             r"overdone into layers of indirection nobody needs", 12.4, font_size=21,
                             color=GREY_A).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "Industry condensed decades of design advice into five letters, popularized by Robert Martin. "
            "<bookmark mark='a'/> Each is easiest to understand through the mistake it prevents. Single "
            "responsibility: a class that formats a report, queries the database and sends the email has three "
            "reasons to change. Open-closed: code that switches on a type must be edited for every new case. "
            "Liskov substitution is our square. Interface segregation: do not force every printer to implement "
            "fax. And dependency inversion is the cure for the cycles of the last chapter. "
            "<bookmark mark='b'/> They are heuristics, not laws. Each is Parnas' hiding seen from one side, and each "
            "can be overdone, into layers of indirection that hide nothing."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[k])) for k in range(6)], lag_ratio=0.35),
                      Create(tab.rule), run_time=4)
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def patterns(self):
        head = label(r"Patterns: \ shapes that recur", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"strategy", r"swap an algorithm behind one interface", r"the congestion controllers of Part 37"],
                [r"observer", r"subscribers notified of a change", r"GUI events, \ React state, \ webhooks"],
                [r"visitor", r"operations over a fixed tree of types", r"Part 13's compiler passes over the AST"],
                [r"adapter", r"wrap one interface as another", r"a storage driver behind a common API"],
                [r"decorator", r"add behaviour by wrapping", r"retries, \ caching, \ logging around a call"],
                [r"factory", r"decide which class to build", r"choosing a TTS engine at run time"]]
        tab = grid_table([r"pattern", r"what it does", r"where we met it"], rows, widths=[2.2, 5.0, 5.4],
                         row_h=0.52, font_size=20, mono_cols=())
        tab.next_to(head, DOWN, buff=0.5).set_x(0)
        for k in range(1, 7):
            tab.cells[k][0].set_color(YES)
        foot = wrapped_label(r"Gamma, Helm, Johnson and Vlissides \ (1994) \ named 23; \ in languages with "
                             r"first-class functions many shrink to a function passed as an argument \ (Norvig: \ 16 "
                             r"of the 23 become invisible or simpler)", 12.4, font_size=20, color=GREY_A).to_edge(
            DOWN, buff=0.4)
        with self.voiceover(
            "In 1994 four authors, the Gang of Four, catalogued design patterns: solutions that keep reappearing, "
            "given names so that people can talk about them. <bookmark mark='a'/> We have used many already. "
            "Strategy swaps an algorithm behind one interface, like the congestion controllers of Part 37. Observer "
            "notifies subscribers of changes. Visitor walks a fixed tree of types, as Part 13's compiler passes "
            "did. Adapter, decorator and factory wrap, extend and choose. <bookmark mark='b'/> Many patterns exist "
            "because the languages of 1994 lacked features. Peter Norvig showed that in a language with first-class "
            "functions, sixteen of the twenty-three become invisible or simpler: a strategy is just a function "
            "passed as an argument."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tab))
            vo.wait_until("b")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def expression(self):
        head = label(r"The expression problem", font_size=36).to_edge(UP, buff=0.3)
        ops = [r"evaluate", r"print", r"simplify"]
        kinds = [r"Number", r"Add", r"Multiply"]
        cell = 1.3
        grid = VGroup()
        for i in range(4):
            for j in range(4):
                sq = Square(cell, stroke_color=GREY_D, stroke_width=1.2)
                sq.move_to([-3.6 + j * cell, 1.0 - i * cell, 0])
                if i == 3 or j == 3:
                    sq.set_stroke(GREY_C, opacity=0.5).set_fill(NO, 0.08)
                grid.add(sq)
        for j, o in enumerate(ops + [r"new op?"]):
            grid.add(label(o, font_size=19, color=YES if j < 3 else NO).move_to([-3.6 + j * cell, 1.0 + cell * 0.75,
                                                                               0]))
        for i, k in enumerate(kinds + [r"new type?"]):
            grid.add(label(k, font_size=19, color=DATA if i < 3 else NO).move_to([-3.6 - cell * 1.05,
                                                                                1.0 - i * cell, 0]))
        notes = VGroup(
            wrapped_label(r"\textbf{objects} store the table by rows: \ a new type is one new class; \ a new "
                          r"operation edits every class", 5.4, font_size=20, color=DATA),
            wrapped_label(r"\textbf{functions over variants} \ (Part 14's algebraic types) \ store it by columns: \ "
                          r"a new operation is one function; \ a new type edits every function", 5.4, font_size=20,
                          color=YES),
            wrapped_label(r"Wadler \ (1998): \ add both, \ without editing or recompiling old code, \ and keep static "
                          r"type safety; \ answers include type classes, \ object algebras, \ open multimethods", 5.4,
                          font_size=20, color=HEAD),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).move_to([3.7, 0.0, 0])
        with self.voiceover(
            "One tension underlies much of design, and Philip Wadler named it the expression problem. "
            "<bookmark mark='a'/> Picture a table: rows are kinds of data, here numbers, sums and products; "
            "columns are operations, evaluate, print, simplify. Every cell is some code. "
            "<bookmark mark='b'/> Object-oriented code stores the table by rows: each class holds its row. Adding a "
            "new kind of data is one new class, but adding an operation means editing every class. "
            "<bookmark mark='c'/> Functional code, with Part 14's algebraic data types, stores it by columns. A new "
            "operation is one function, but a new kind of data means editing every function. "
            "<bookmark mark='d'/> The problem is to allow both, without touching old code and without losing type "
            "safety. Type classes, object algebras and multimethods are partial answers; which axis your program "
            "will grow along is the real design decision."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(grid))
            for mk, n in zip("bcd", notes):
                vo.wait_until(mk)
                self.play(FadeIn(n))
        self.wait(0.4)
        self.clear_scene()

    def functional(self):
        head = label(r"A pure core, \ an imperative shell", font_size=36).to_edge(UP, buff=0.3)
        bad = code_block([
            "# the order can be paid and also be cancelled:",
            "class Order:",
            "    paid: bool",
            "    cancelled: bool",
            "    tracking: str | None",
        ], size=17)
        good = code_block([
            "# make illegal states unrepresentable:",
            "Order = Pending(items)",
            "      | Paid(items, receipt)",
            "      | Shipped(items, receipt, tracking)",
            "      | Cancelled(reason)",
        ], size=17)
        pair = VGroup(bad, good).arrange(RIGHT, buff=1.0).next_to(head, DOWN, buff=0.6)
        lines = VGroup(
            wrapped_label(r"two booleans and an optional field allow 8 combinations; \ the business allows 4: \ give "
                          r"the type exactly 4 shapes and the other 4 cannot be built \ (Minsky)", 12.4,
                          font_size=21, color=YES),
            wrapped_label(r"\textbf{functional core, imperative shell}: \ decisions in pure functions, \ easy to test "
                          r"with plain values; \ input, \ output and time at the thin edge", 12.4, font_size=21,
                          color=HEAD),
            wrapped_label(r"\textbf{immutability}: \ values that cannot change can be shared across threads \ "
                          r"(Part 33) \ and cached without fear", 12.4, font_size=21, color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3).next_to(pair, DOWN, buff=0.55)
        with self.voiceover(
            "Industry has also absorbed functional ideas. <bookmark mark='a'/> On the left, an order with two "
            "flags and an optional tracking number: eight combinations, including an order that is both paid and "
            "cancelled. On the right, a type with exactly the four shapes the business allows. Yaron Minsky's "
            "slogan: make illegal states unrepresentable, and a whole class of bugs cannot be written. "
            "<bookmark mark='b'/> Gary Bernhardt's design puts every decision in pure functions, which can be tested "
            "with plain values, and keeps input, output and time in a thin shell around them. "
            "<bookmark mark='c'/> And immutable values can be shared between threads, Part 33's hardest problem, "
            "and cached without fear."
        ) as vo:
            self.play(FadeIn(head), FadeIn(pair))
            for mk, l in zip("abc", lines):
                vo.wait_until(mk)
                self.play(FadeIn(l))
        self.wait(0.4)
        self.clear_scene()


_ = (KERN,)
