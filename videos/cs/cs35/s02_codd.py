from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs35.common import (CODE, DATA, HEAD, LAM, NO, PART, YES, box, code, load, mono)


class Codd(VoiceoverScene):
    def construct(self):
        self.card()
        self.before()
        self.relations()
        self.independence()

    def card(self):
        card = chapter_card(1, r"Ask for what, \ not how", r"Can a program stop caring where the data is?",
                            lit=(1968, 1970), extra=((1968, r"IBM's IMS"), (1970, r"Codd: \ the relational model")),
                            part=PART)
        with self.voiceover("Chapter one. Ask for what, not how."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def before(self):
        head = label(r"Before Codd: \ databases you walk", font_size=36).to_edge(UP, buff=0.3)
        root = box(2.0, 0.6, r"\text{library}", GREY_B, font_size=20).move_to([-4.2, 1.8, 0])
        books = VGroup(*[box(1.8, 0.55, rf"\text{{{b}}}", DATA, font_size=18) for b in ("Emma", "Dracula")]).arrange(
            RIGHT, buff=0.5).move_to([-4.2, 0.6, 0])
        chs = VGroup(*[box(1.0, 0.5, rf"\text{{ch {k}}}", HEAD, font_size=16) for k in (1, 2, 3)]).arrange(
            RIGHT, buff=0.2).move_to([-5.1, -0.6, 0])
        e = VGroup(*[Line(root.get_bottom(), b.get_top(), color=GREY_B) for b in books],
                   *[Line(books[0].get_bottom(), c.get_top(), color=GREY_B) for c in chs])
        tree = VGroup(root, books, chs, e)
        prog = code([
            "GU   BOOK(TITLE='Emma')       get unique",
            "GNP  CHAPTER                  get next within parent",
            "GNP  CHAPTER",
            "...                           (until status GE)",
        ], size=16).move_to([2.8, 1.2, 0])
        lines = VGroup(
            label(r"IBM's IMS \ (1968, \ for Apollo's parts lists): \ records in a hierarchy; \ CODASYL \ (1969): "
                  r"records joined by pointers", font_size=20, color=WHITE),
            label(r"a program \textbf{navigates}: \ start at a record, \ follow pointers one at a time", font_size=20,
                  color=HEAD),
            label(r"a new question means a new program; \ a new layout on disk means rewriting the old ones",
                  font_size=20, color=NO),
        ).arrange(DOWN, buff=0.14).to_edge(DOWN, buff=0.45)
        with self.voiceover(
            "The first databases were structures you walked. <bookmark mark='a'/> IBM's IMS, built in the 1960s "
            "for the parts lists of the Apollo programme, stored records in a hierarchy: a library holds books, a "
            "book holds chapters. The CODASYL standard of 1969 joined records with pointers into a network. "
            "<bookmark mark='b'/> A program navigated: get this book; get the next chapter within it; and again, "
            "until the status code said there were no more. <bookmark mark='c'/> Every new question was a new "
            "program, written by someone who knew the pointers. And if the data was reorganised on disk, for speed, "
            "the old programs broke."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(tree), FadeIn(lines[0]))
            vo.wait_until("b")
            self.play(FadeIn(prog), FadeIn(lines[1]))
            vo.wait_until("c")
            self.play(FadeIn(lines[2]))
        self.wait(0.3)
        self.clear_scene()

    def relations(self):
        head = label(r"Codd, \ 1970: \ relations", font_size=36).to_edge(UP, buff=0.3)
        quote = label(r"``Future users of large data banks must be protected from having to know how the data is "
                      r"organized in the machine''", font_size=22, color=GREY_A).next_to(head, DOWN, buff=0.4)
        if quote.width > 12.5:
            quote.width = 12.5
        cite = label(r"E. F. Codd, \ \textit{A Relational Model of Data for Large Shared Data Banks}", font_size=17,
                     color=GREY_B).next_to(quote, DOWN, buff=0.12)
        pts = VGroup(
            label(r"a \textbf{relation}: \ a set of tuples, \ a table; \ no pointers, \ no order", font_size=22,
                  color=DATA),
            label(r"a \textbf{key}: \ attributes that identify a tuple; \ tables connect by \textit{values}, \ not "
                  r"addresses", font_size=22, color=HEAD),
            label(r"a query states the \textbf{result} in logic; \ the system finds the way", font_size=22,
                  color=YES),
            label(r"\textbf{data independence}: \ change indexes or layout, \ and no query changes", font_size=22,
                  color=LAM),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25).next_to(cite, DOWN, buff=0.5)
        hist = label(r"System R at IBM and Ingres at Berkeley \ (1974--77) \ proved it could be fast; \ SEQUEL "
                     r"became SQL; \ Codd's Turing Award, \ 1981", font_size=19, color=GREY_A).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "In 1970 Edgar Codd, a mathematician at IBM, proposed something else. <bookmark mark='a'/> Users of "
            "large shared databases, he wrote, must be protected from having to know how the data is organised in the "
            "machine. <bookmark mark='b'/> Data should be relations: sets of tuples, tables, with no pointers and no "
            "order. <bookmark mark='c'/> Tables connect through values: a key that identifies a book appears in the "
            "rows that refer to it. <bookmark mark='d'/> A query states what the result is, in logic, and the system "
            "works out how to compute it. <bookmark mark='e'/> And so the physical design, indexes, layout, the order "
            "of rows, can change without changing a single query. <bookmark mark='f'/> Many at IBM doubted it could be "
            "made fast. System R and Berkeley's Ingres proved it could, and System R's query language, SEQUEL, became "
            "SQL."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(quote), FadeIn(cite))
            for mk, p in zip("bcde", pts):
                vo.wait_until(mk)
                self.play(FadeIn(p, shift=RIGHT * 0.1))
            vo.wait_until("f")
            self.play(FadeIn(hist))
        self.wait(0.3)
        self.clear_scene()

    def independence(self):
        it = load("iterators")
        head = label(r"Data independence, \ measured", font_size=36).to_edge(UP, buff=0.3)
        q = VGroup(*[mono(t, 17, YES) for t in (
            "SELECT title, COUNT(*) FROM words JOIN books",
            "  ON words.book_id = books.book_id WHERE word = 'whale'",
            "  GROUP BY title ORDER BY 2 DESC LIMIT 3")]).arrange(DOWN, aligned_edge=LEFT, buff=0.06)
        q.next_to(head, DOWN, buff=0.45)
        ch = it["plans"]["chosen"]
        sc = it["plans"]["hash join, full scan"]
        cols = VGroup()
        for title, p, c in ((r"no index on \texttt{word}: \ scan every row", sc, NO),
                            (r"with a B+ tree on \texttt{word}", ch, YES)):
            g = VGroup(label(title, font_size=20, color=c),
                       label(rf"{p['stats']['pages']:.0f} pages read", font_size=24, color=WHITE),
                       label(r"answer: \ " + r", \ ".join(rf"\textit{{{t}}} {n}" for t, n in p["rows"][:2]),
                             font_size=18, color=GREY_A)).arrange(DOWN, buff=0.15)
            cols.add(g)
        cols.arrange(RIGHT, buff=1.4).next_to(q, DOWN, buff=0.7)
        foot = label(r"the same query, \ the same answer: \ only the plan changed, \ and the database chose it",
                     font_size=21, color=LAM).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "We can watch data independence at work in our own database. Here is a question about the novels: which "
            "books use the word whale most? <bookmark mark='a'/> Without an index on the word column, the database "
            "must read every page of the words table: twelve hundred pages, on a sample of the corpus. <bookmark "
            "mark='b'/> Add a B-plus tree on that column, and the same query, unchanged, reads 85 pages, because the "
            "optimizer now finds the whale rows through the index. <bookmark mark='c'/> Moby Dick, of course. The "
            "query never mentioned the index. That is Codd's point."
        ) as vo:
            self.play(FadeIn(head), FadeIn(q))
            vo.wait_until("a")
            self.play(FadeIn(cols[0]))
            vo.wait_until("b")
            self.play(FadeIn(cols[1]))
            vo.wait_until("c")
            self.play(FadeIn(foot))
        self.wait(0.3)
        self.clear_scene()


_ = (CODE,)
