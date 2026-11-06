from __future__ import annotations

import math

from explainer.cs import *  # noqa: F403
from videos.cs.cs43.common import (BG, DATA, HEAD, KERN, LAM, NO, PART, YES, axes, code_block, grid_table, mono,
                                   module_box, tag_box, timeline_bar, trace)

# Hyrum's law as a model (illustrative, computed here): each of N consumers independently comes to rely on one
# incidental behaviour with probability p; the chance that somebody does is 1 - (1 - p)^N.
HYRUM_P = (0.01, 0.001, 0.0001)


def p_somebody(p: float, n: float) -> float:
    return 1 - (1 - p) ** n


def half_point(p: float) -> float:
    """The number of consumers at which somebody relies on the behaviour with probability one half."""
    return math.log(2) / -math.log(1 - p)


class Design(VoiceoverScene):
    def construct(self):
        self.card()
        self.hyrum()
        self.additive()
        self.versions()
        self.resources()
        self.contracts()
        self.postel()

    def card(self):
        card = chapter_card(6, r"Designing and versioning APIs", r"How does an interface change without breaking "
                            r"its users?", lit=(1981, 2019, 2023),
                            extra=((1981, r"Postel: \ the robustness principle"), (2019, r"RFC 8594: \ Sunset"),
                                   (2023, r"RFC 9413")), part=PART)
        with self.voiceover("Chapter six. Designing and versioning APIs."):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def hyrum(self):
        head = label(r"Hyrum's law, \ as a model", font_size=36).to_edge(UP, buff=0.3)
        g = axes([0, 4.5, 1], [0, 1.2, 0.25], x_length=6.4, y_length=4.8, x_label=r"consumers $N$ \ (log scale)",
                 y_label=r"chance that somebody relies on it", xticks=range(5), yticks=(0, 0.5, 1),
                 fx=lambda v: f"{10 ** v:,.0f}", fy=lambda v: f"{v:g}")
        g.next_to(head, DOWN, buff=0.45).to_edge(LEFT, buff=0.8)
        ax = g.ax
        cols = (NO, HEAD, LAM)
        curves, tags, dots = VGroup(), VGroup(), VGroup()
        for p, c in zip(HYRUM_P, cols):
            pts = [(x / 50, p_somebody(p, 10 ** (x / 50))) for x in range(201)]
            curves.add(trace(ax, pts, c, width=3))
            h = half_point(p)
            dots.add(VGroup(Dot(ax.c2p(math.log10(h), 0.5), radius=0.07, color=c),
                            label(rf"{h:,.0f}", font_size=16, color=c).next_to(ax.c2p(math.log10(h), 0.5), DR,
                                                                               buff=0.06)))
            tags.add(label(rf"$p = {p:g}$", font_size=18, color=c))
        tags.arrange(DOWN, aligned_edge=LEFT, buff=0.12).next_to(ax.c2p(0.05, 1.0), DR, buff=0.1)
        half = DashedLine(ax.c2p(0, 0.5), ax.c2p(4, 0.5), color=GREY_D, dash_length=0.08)
        notes = VGroup(
            wrapped_label(r"\textbf{Hyrum's law} \ (Hyrum Wright, \ Google; \ Part 40): \ with enough users, \ every "
                          r"observable behaviour will be depended on by somebody", 5.3, font_size=21, color=WHITE),
            wrapped_label(r"a model, \ illustrative: \ each of $N$ consumers relies on one incidental behaviour "
                          r"independently, \ with probability $p$; \ then somebody does with probability "
                          r"$1 - (1 - p)^N$", 5.3, font_size=21, color=GREY_A),
            wrapped_label(r"it passes one half at $N \approx 0.69 / p$, \ whatever $p$ is", 5.3, font_size=21,
                          color=HEAD),
            wrapped_label(r"in an API: \ the order of fields, \ an error's wording, \ a list that happened to come "
                          r"back sorted, \ how long a call takes", 5.3, font_size=21, color=NO),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4).shift(DOWN * 0.1)
        with self.voiceover(
            "Part 40 met Hyrum Wright's law: with enough users, every observable behaviour of a system will be "
            "depended on by somebody, and an API's users are programs written by strangers. <bookmark mark='a'/> "
            "Suppose each consumer, independently, relies on some incidental behaviour with a small probability p. "
            "Then somebody does with probability one minus one minus p, to the power N. "
            "<bookmark mark='b'/> However small p is, the curve passes one half at about seven tenths over p "
            "consumers, then climbs towards certainty. <bookmark mark='c'/> And the behaviours are things nobody "
            "promised: the order of fields, an error's wording, a list that happened to be sorted."
        ) as vo:
            self.play(FadeIn(head), FadeIn(g), FadeIn(notes[0]))
            vo.wait_until("a")
            self.play(FadeIn(notes[1]), Create(half))
            self.play(LaggedStart(*[Create(c) for c in curves], lag_ratio=0.4), FadeIn(tags), run_time=3)
            vo.wait_until("b")
            self.play(FadeIn(notes[2]), LaggedStart(*[FadeIn(d, scale=0.5) for d in dots], lag_ratio=0.3))
            vo.wait_until("c")
            self.play(FadeIn(notes[3]))
        self.wait(0.4)
        self.clear_scene()

    def additive(self):
        head = label(r"Changes that break, \ and changes that don't", font_size=36).to_edge(UP, buff=0.3)
        code = code_block(["{", '  "id": 42,', '  "title": "Moby-Dick",', '  "price": 1299,',
                           '  "status": "in_stock",', '  "isbn": "978-..."', "}"], size=21)
        code[5].set_color(YES)
        cl = label(r"a response \ (illustrative)", font_size=19, color=GREY_A)
        cg = VGroup(cl, code).arrange(DOWN, aligned_edge=LEFT, buff=0.15).next_to(head, DOWN, buff=0.6).to_edge(
            LEFT, buff=0.6)
        changes = [("safe", YES, r"add a response field \ (\texttt{isbn})", 5),
                   ("safe", YES, r"add an optional request parameter", None),
                   ("breaks", NO, r"remove a field \ (\texttt{price})", 3),
                   ("breaks", NO, r"rename a field \ (\texttt{title} to \texttt{name})", 2),
                   ("breaks", NO, r"change a type \ (\texttt{1299} to the string \texttt{12.99})", 3),
                   ("breaks", NO, r"add a required request parameter", None),
                   ("risky", HEAD, r"add an enum value \ (\texttt{preorder}): \ breaks clients that handle every case",
                    4)]
        rows = VGroup()
        for tag, col, text, _ in changes:
            t = tag_box(tag, col, size=18, w=1.35, h=0.46)
            rows.add(VGroup(t, wrapped_label(text, 6.0, font_size=21, color=WHITE)).arrange(RIGHT, buff=0.3))
        rows.arrange(DOWN, aligned_edge=LEFT, buff=0.26).to_edge(RIGHT, buff=0.4).align_to(cg, UP)
        strike = Line(code[3].get_left() + LEFT * 0.05, code[3].get_right() + RIGHT * 0.05, color=NO, stroke_width=3)
        foot = wrapped_label(r"the rule: \ add, \ never remove or change; \ new inputs optional; \ and every reader "
                             r"ignores fields it does not know \ (the tolerant reader); \ chapter 3's compatibility, "
                             r"\ for a whole API", 12.4, font_size=20, color=YES).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "So the only safe changes are ones nobody could have observed: additions. <bookmark mark='a'/> A new "
            "response field is safe, if every client ignores fields it does not recognise; so is a new optional "
            "parameter. <bookmark mark='b'/> Removing a field breaks whoever read it. So does renaming one, or "
            "changing its type, here a price in cents becoming a string, or adding a required parameter. "
            "<bookmark mark='c'/> Some changes only look additive: a new enumeration value breaks clients that "
            "handle every case with no default. <bookmark mark='d'/> These are chapter three's compatibility "
            "rules, applied to a whole API."
        ) as vo:
            self.play(FadeIn(head), FadeIn(cl), FadeIn(code[:5]), FadeIn(code[6]))
            vo.wait_until("a")
            self.play(FadeIn(code[5], shift=LEFT * 0.2), FadeIn(rows[0]))
            self.play(FadeIn(rows[1]))
            vo.wait_until("b")
            self.play(FadeIn(rows[2]), Create(strike))
            self.play(FadeIn(rows[3]), Indicate(code[2], color=NO))
            self.play(FadeIn(rows[4]), Indicate(code[3], color=NO))
            self.play(FadeIn(rows[5]))
            vo.wait_until("c")
            self.play(FadeIn(rows[6]), Indicate(code[4], color=HEAD))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def versions(self):
        head = label(r"Versions, \ deprecation, \ sunset", font_size=36).to_edge(UP, buff=0.3)
        y1, y2 = 1.75, 1.15
        v1 = timeline_bar(-6.0, -0.6, y1, DATA, h=0.4, label_text=r"v1", size=18)
        dep = timeline_bar(-0.6, 2.8, y1, HEAD, h=0.4, label_text=r"v1, \ deprecated", size=18)
        v2 = timeline_bar(-2.4, 6.4, y2, YES, h=0.4, label_text=r"v2", size=18)
        gone = label(r"410 Gone", font_size=18, color=NO).next_to([2.8, y1, 0], RIGHT, buff=0.15)
        ticks = VGroup()
        for x, t, c in ((-2.4, r"v2 released", YES), (-0.6, r"v1 deprecated", HEAD), (2.8, r"sunset", NO)):
            ticks.add(VGroup(DashedLine([x, y1 + 0.3, 0], [x, y2 - 0.3, 0], color=c, dash_length=0.06),
                             label(t, font_size=17, color=c).move_to([x, y1 + 0.5, 0])))
        tl = label(r"time \ (illustrative)", font_size=16, color=GREY_B).next_to([6.4, y2, 0], DOWN, buff=0.3,
                                                                               aligned_edge=RIGHT)
        tl.align_to([6.4, 0, 0], RIGHT)
        hdr = code_block(["HTTP/1.1 200 OK", "Sunset: Sat, 31 Jul 2027 23:59:59 GMT",
                          'Link: </docs/v1-sunset>; rel="sunset"'], size=18)
        hdr[1].set_color(HEAD)
        hl = label(r"a v1 response during the window", font_size=19, color=HEAD)
        hg = VGroup(hl, hdr).arrange(DOWN, aligned_edge=LEFT, buff=0.15).move_to([-3.4, -0.5, 0])
        styles = VGroup(
            VGroup(label(r"in the path", font_size=21, color=DATA), mono("GET /v1/books/42", size=17)).arrange(
                DOWN, aligned_edge=LEFT, buff=0.1),
            VGroup(label(r"in a header", font_size=21, color=LAM),
                   mono("Accept: application/vnd.example.v2+json", size=17)).arrange(DOWN, aligned_edge=LEFT,
                                                                                      buff=0.1),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).move_to([3.7, -0.5, 0])
        foot = wrapped_label(r"semantic versioning \ (Parts 40 and 41): \ only the MAJOR number belongs in a path or "
                             r"header; \ MINOR and PATCH changes are additive, \ so no client needs to choose them",
                             12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.4)
        with self.voiceover(
            "When a break is unavoidable, it becomes a new version, and the old one is retired slowly. "
            "<bookmark mark='a'/> Version two is released beside version one, which keeps working. "
            "<bookmark mark='b'/> Then version one is deprecated: its responses announce the date it will stop, in "
            "a Sunset header, standardised as RFC 8594 in 2019, so clients can see it coming. "
            "<bookmark mark='c'/> Only after that window does it stop answering. <bookmark mark='d'/> The version "
            "can travel in the path, visible and easy to route, or in a header, keeping one URL per resource. "
            "<bookmark mark='e'/> Either way only the major number belongs there: minor and patch changes are "
            "additive."
        ) as vo:
            self.play(FadeIn(head), FadeIn(v1), FadeIn(tl))
            vo.wait_until("a")
            self.play(FadeIn(ticks[0]), GrowFromEdge(v2, LEFT))
            vo.wait_until("b")
            self.play(FadeIn(ticks[1]), GrowFromEdge(dep, LEFT))
            self.play(FadeIn(hg))
            vo.wait_until("c")
            self.play(FadeIn(ticks[2]), FadeIn(gone))
            vo.wait_until("d")
            self.play(FadeIn(styles[0]))
            self.play(FadeIn(styles[1]))
            vo.wait_until("e")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def resources(self):
        head = label(r"Resource-oriented design", font_size=36).to_edge(UP, buff=0.3)
        chain = VGroup()
        for t, kind in ((r"publishers", "c"), (r"123", "r"), (r"books", "c"), (r"456", "r")):
            col = DATA if kind == "c" else HEAD
            b = module_box(rf"\texttt{{{t}}}", col, w=2.1, h=0.6, font=20)
            cap = label(r"collection" if kind == "c" else r"resource", font_size=16, color=col).next_to(b, DOWN,
                                                                                                    buff=0.1)
            chain.add(VGroup(b, cap))
        chain.arrange(RIGHT, buff=0.55).next_to(head, DOWN, buff=0.5)
        links = VGroup(*[Arrow(chain[i][0].get_right(), chain[i + 1][0].get_left(), buff=0.05, color=GREY_B,
                               stroke_width=2, max_tip_length_to_length_ratio=0.25) for i in range(3)])
        rname = VGroup(label(r"resource name:", font_size=20, color=GREY_A),
                       mono("publishers/123/books/456", size=19, color=HEAD)).arrange(RIGHT, buff=0.2)
        rname.next_to(chain, DOWN, buff=0.25)
        rows = [[r"List", r"GET", r"/v1/publishers/123/books"], [r"Get", r"GET", r"/v1/publishers/123/books/456"],
                [r"Create", r"POST", r"/v1/publishers/123/books"],
                [r"Update", r"PATCH", r"/v1/publishers/123/books/456"],
                [r"Delete", r"DELETE", r"/v1/publishers/123/books/456"],
                [r"custom", r"POST", r"/v1/publishers/123/books/456:undelete"]]
        colors = [[YES, WHITE, WHITE]] * 5 + [[LAM, WHITE, WHITE]]
        tab = grid_table([r"method", r"HTTP", r"path"], rows, widths=[2.2, 2.0, 7.2], row_h=0.46, font_size=21,
                         colors=colors, mono_cols=(1, 2))
        tab.next_to(rname, DOWN, buff=0.35).set_x(0)
        foot = wrapped_label(r"Google's API design guide: \ many nouns, \ few verbs; \ the same five standard methods "
                             r"on every collection, \ for REST and gRPC alike, \ so clients, \ permissions and "
                             r"documentation are built once", 12.4, font_size=20, color=WHITE).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Google's API design guide turns these lessons into a style. <bookmark mark='a'/> An API is a hierarchy "
            "of resources, collections and the resources inside them, named by paths like a file system. "
            "<bookmark mark='b'/> Every collection gets the same standard methods, list, get, create, update and "
            "delete, mapped onto HTTP's methods with chapter four's safety and idempotency. <bookmark mark='c'/> "
            "Anything else becomes a custom method after a colon, like undelete. <bookmark mark='d'/> The point is "
            "predictability: with the same few verbs over different nouns, client libraries, permissions and "
            "documentation are built once, for every API."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(c) for c in chain], lag_ratio=0.3), Create(links), run_time=2)
            self.play(FadeIn(rname))
            vo.wait_until("b")
            self.play(FadeIn(VGroup(*tab.cells[0])), Create(tab.rule))
            self.play(LaggedStart(*[FadeIn(VGroup(*tab.cells[r])) for r in range(1, 6)], lag_ratio=0.3), run_time=2)
            vo.wait_until("c")
            self.play(FadeIn(VGroup(*tab.cells[6])))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def contracts(self):
        head = label(r"Consumer-driven contract tests", font_size=36).to_edge(UP, buff=0.3)
        cons = [(r"web", DATA, "reads: title, price"), (r"mobile app", LAM, "reads: title, author.name"),
                (r"billing", KERN, "reads: price")]
        ys = (1.45, 0.05, -1.35)
        boxes, tags = VGroup(), VGroup()
        for (name, col, reads), y in zip(cons, ys):
            b = module_box(name, col, w=2.0, h=0.65, font=20).move_to([-5.6, y, 0])
            t = tag_box(reads, col, size=18).next_to(b, RIGHT, buff=0.3)
            boxes.add(b)
            tags.add(t)
        tags_r = max(t.get_right()[0] for t in tags)
        prov = module_box(r"books service", YES, w=2.5, h=0.85, font=21).move_to([5.3, ys[1], 0])
        pull = VGroup(*[Arrow([tags_r + 0.15, t.get_y(), 0], prov.get_left() + UP * (t.get_y() - ys[1]) * 0.2,
                              buff=0.1, color=GREY_B, stroke_width=2, max_tip_length_to_length_ratio=0.08)
                        for t in tags])
        ctl = label(r"contracts", font_size=17, color=GREY_A).next_to(tags, UP, buff=0.15)
        build = label(r"the provider's build replays every contract", font_size=18, color=YES).next_to(prov, DOWN,
                                                                                                   buff=0.55)
        build.align_to([6.6, 0, 0], RIGHT)
        change = VGroup(label(r"change: \ rename \texttt{author.name}", font_size=18, color=HEAD),
                        label(r"to \texttt{author.display\_name}", font_size=18, color=HEAD)).arrange(
            DOWN, aligned_edge=LEFT, buff=0.08).next_to(prov, UP, buff=0.3).align_to([6.6, 0, 0], RIGHT)
        marks = VGroup()
        for t, ok in zip(tags, (True, False, True)):
            sym = label(r"$\checkmark$" if ok else r"$\times$", font_size=30, color=YES if ok else NO)
            marks.add(sym.next_to(t, UP, buff=0.05).align_to(t, RIGHT))
        verdict = label(r"one contract fails: \ the change stops before it ships", font_size=19, color=NO).next_to(
            build, DOWN, buff=0.2).align_to([6.6, 0, 0], RIGHT)
        foot = wrapped_label(r"each consumer's own tests record the requests it makes and the fields it reads, \ "
                             r"and publish them \ (tools such as Pact); \ the contracts are Hyrum's law written down "
                             r"\ (illustrative example)", 12.4, font_size=20, color=GREY_A).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "How can a provider know which changes are safe, when that depends on what consumers actually do? It "
            "asks them. <bookmark mark='a'/> In consumer-driven contract testing, with tools such as Pact, each "
            "consumer's own tests record the requests it makes and the response fields it reads, and publish them "
            "as a contract. <bookmark mark='b'/> The provider's build replays every contract against the new code. "
            "<bookmark mark='c'/> Here the provider renames the author's name field. The web client and billing "
            "never read it, and pass. The mobile app does, and fails, so the change stops before it ships. "
            "<bookmark mark='d'/> The contracts turn Hyrum's law from a surprise into a list."
        ) as vo:
            self.play(FadeIn(head), FadeIn(boxes), FadeIn(prov))
            vo.wait_until("a")
            self.play(LaggedStart(*[FadeIn(t, shift=RIGHT * 0.2) for t in tags], lag_ratio=0.3), FadeIn(ctl))
            vo.wait_until("b")
            self.play(LaggedStart(*[GrowArrow(a) for a in pull], lag_ratio=0.2), FadeIn(build))
            vo.wait_until("c")
            self.play(FadeIn(change))
            for t, mk in zip(tags, marks):
                self.play(Indicate(t, color=WHITE, scale_factor=1.05), FadeIn(mk), run_time=0.6)
            self.play(tags[1][0].animate.set_stroke(NO), tags[1][1].animate.set_color(NO), FadeIn(verdict))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def postel(self):
        head = label(r"Be liberal in what you accept?", font_size=36).to_edge(UP, buff=0.3)
        c = np.array([-3.7, -0.3, 0])
        spec = Circle(radius=1.0, color=YES, stroke_width=3).set_fill(YES, 0.15).move_to(c)
        sl = label(r"the specification", font_size=17, color=YES).move_to(c)
        acc = Ellipse(width=2.0, height=2.0, color=HEAD, stroke_width=2.5).move_to(c)
        big = Ellipse(width=5.4, height=3.6, color=HEAD, stroke_width=2.5).move_to(c)
        al = label(r"what receivers accept", font_size=17, color=HEAD).next_to(big, UP, buff=0.1)
        bad_pts = [(-1.7, 0.6), (1.6, 0.9), (-2.0, -0.5), (1.8, -0.4), (0.3, -1.4), (-0.9, 1.35)]
        bad = VGroup(*[Dot(c + np.array([x, y, 0]), radius=0.08, color=NO) for x, y in bad_pts])
        crosses = VGroup(*[Cross(scale_factor=0.12, stroke_color=NO, stroke_width=4).move_to(d) for d in bad])
        real = DashedVMobject(Ellipse(width=5.4, height=3.6, color=NO, stroke_width=2.5).move_to(c), num_dashes=40)
        rl = label(r"the real protocol", font_size=17, color=NO).next_to(big, DOWN, buff=0.1)
        notes = VGroup(
            wrapped_label(r"Jon Postel, \ TCP's specification \ (RFC 793, \ 1981): \ ``be conservative in what you do, "
                          r"\ be liberal in what you accept from others''", 5.4, font_size=21, color=WHITE),
            wrapped_label(r"every tolerated mistake is observable behaviour: \ senders come to depend on it, \ and "
                          r"each new receiver must tolerate it too \ (Hyrum's law again)", 5.4, font_size=21,
                          color=NO),
            wrapped_label(r"RFC 9413 \ (Thomson and Schinazi, \ 2023): \ maintain protocols actively, \ and reject "
                          r"what the specification does not allow, \ early and visibly, \ while mistakes are cheap "
                          r"to fix", 5.4, font_size=21, color=YES),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).to_edge(RIGHT, buff=0.4)
        ill = label(r"schematic", font_size=16, color=GREY_B).to_corner(DL, buff=0.4)
        with self.voiceover(
            "One old rule pulls the other way. <bookmark mark='a'/> Jon Postel's robustness principle, from TCP's "
            "specification of 1981: be conservative in what you do, be liberal in what you accept from others. "
            "<bookmark mark='b'/> But every tolerated mistake is "
            "observable behaviour. Senders come to depend on it, every new receiver must tolerate it too, and the "
            "real protocol becomes the specification plus every accident anyone accepted. <bookmark mark='c'/> RFC "
            "9413, by Martin Thomson and David Schinazi in 2023, argues for the opposite: maintain protocols "
            "actively, and reject what they do not allow, early and visibly, while mistakes are cheap to fix."
        ) as vo:
            self.play(FadeIn(head), FadeIn(spec), FadeIn(sl), FadeIn(ill))
            vo.wait_until("a")
            self.play(FadeIn(notes[0]), FadeIn(acc))
            self.play(Transform(acc, big), FadeIn(al), run_time=1.5)
            vo.wait_until("b")
            self.play(FadeIn(notes[1]), LaggedStart(*[FadeIn(d, scale=0.3) for d in bad], lag_ratio=0.25))
            self.play(Create(real), FadeIn(rl))
            vo.wait_until("c")
            self.play(FadeIn(notes[2]))
            self.play(FadeOut(real), FadeOut(rl), FadeOut(al),
                      Transform(acc, Ellipse(width=2.0, height=2.0, color=HEAD, stroke_width=2.5).move_to(c)),
                      ReplacementTransform(bad, crosses), run_time=1.5)
        self.wait(0.4)
        self.clear_scene()


_ = (BG, DATA, KERN, LAM)
