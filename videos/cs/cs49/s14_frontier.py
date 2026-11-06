from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs49.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, grid_table


def tile(title, body, col, w=4.2, h=3.0):
    frame = RoundedRectangle(width=w, height=h, corner_radius=0.15, stroke_color=col, stroke_width=2, fill_color=BG,
                             fill_opacity=1)
    t = label(title, font_size=22, color=col)
    b = wrapped_label(body, w - 0.4, font_size=18, color=GREY_A)
    VGroup(t, b).arrange(DOWN, buff=0.3).move_to(frame)
    return VGroup(frame, t, b)


class Frontier(VoiceoverScene):
    def construct(self):
        self.card()
        self.failures()
        self.checklist()
        self.research()
        self.open()

    def card(self):
        card = chapter_card(13, r"Frontier: \ how designs fail, \ and what is unknown",
                            r"What do outages teach that designs miss?", lit=(2014, 2016),
                            extra=((2014, r"Yuan et al.: \ simple testing"),
                                   (2016, r"Gunawi et al.: \ cloud outages")), part=PART)
        with self.voiceover("Chapter thirteen, the frontier. What do real outages teach, that designs miss?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def failures(self):
        head = label(r"How systems actually fail", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"error handling", r"Yuan et al. \ (OSDI 2014) \ studied failures of five distributed systems: \ "
                 r"most catastrophic ones came from mishandled non-fatal errors, \ often in code no test had run", NO),
            tile(r"changes", r"Google's SRE book \ (2016) \ estimates that about 70\% of outages are caused by "
                 r"changes to a live system: \ deploys, \ configuration, \ migrations", HEAD),
            tile(r"the cloud itself", r"Gunawi et al. \ (2016) \ read hundreds of public outage reports: \ upgrades, "
                 r"\ configuration, \ load and cascading failures recur, \ hardware rarely", LAM),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"designs are drawn for the happy path; \ outages live in the error paths, \ the "
                             r"changes, \ and the coupling between blocks", 12.4, font_size=21, color=WHITE).to_edge(
            DOWN, buff=0.6)
        with self.voiceover(
            "Real outages are studied the way accidents are. <bookmark mark='a'/> Ding Yuan and colleagues analysed "
            "failures in five widely used distributed systems in 2014, and found that most of the catastrophic "
            "ones came from mishandling errors that were not fatal in themselves, often in code that no test had ever "
            "run. <bookmark mark='b'/> Google's site reliability engineers estimate that about seventy percent of "
            "their outages are caused by changes to a live system: deploys, configuration and migrations. "
            "<bookmark mark='c'/> And Haryadi Gunawi and colleagues read hundreds of public reports of cloud "
            "outages: upgrades, configuration, overload and cascading failures recur; plain hardware failure "
            "rarely causes them alone. <bookmark mark='d'/> Designs are drawn for the happy path. Outages live in the "
            "error paths, the changes, and the coupling between the blocks."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def checklist(self):
        head = label(r"Eight designs, \ five trade-offs", font_size=36).to_edge(UP, buff=0.3)
        rows = [[r"shortener", r"eventual", r"low", r"low", r"low"],
                [r"news feed", r"eventual", r"low", r"high", r"medium"],
                [r"chat", r"per-conversation order", r"low", r"medium", r"high"],
                [r"crawler", r"none needed", r"high is fine", r"high", r"medium"],
                [r"dispatch", r"fresh locations", r"seconds", r"medium", r"high"],
                [r"video", r"eventual", r"startup matters", r"very high", r"medium"],
                [r"ledger", r"strong", r"moderate", r"low", r"high"],
                [r"editor", r"convergence", r"low", r"low", r"high"]]
        tab = grid_table([r"system", r"consistency", r"latency", r"cost driver", r"complexity"], rows,
                         widths=[2.2, 3.4, 2.4, 2.2, 2.0], row_h=0.48, font_size=18, mono_cols=())
        tab.next_to(head, DOWN, buff=0.35)
        note_ = note(r"a qualitative summary of this part's designs, \ not measurements", font_size=16).to_edge(
            DOWN, buff=0.35)
        with self.voiceover(
            "Every design in this part was a set of choices among the same few trade-offs. <bookmark mark='a'/> How "
            "consistent it must be, from eventual for a feed to strict for a ledger. How fast it must answer. What "
            "dominates its cost: storage and bandwidth for video, fan-out for a feed. And how much complexity it "
            "carries, which is also how much can go wrong in operation. <bookmark mark='b'/> The table is a summary, "
            "not a measurement. Its point is that no design is good in every column, and that a good design knows "
            "which columns it has given up."
        ) as vo:
            self.play(FadeIn(head), FadeIn(note_))
            vo.wait_until("a")
            self.play(FadeIn(tab.rule), FadeIn(VGroup(*tab.cells[0])))
            self.play(LaggedStart(*[FadeIn(VGroup(*r)) for r in tab.cells[1:]], lag_ratio=0.25), run_time=4)
            vo.wait_until("b")
            self.play(Indicate(VGroup(*tab.cells[7]), color=HEAD))
        self.wait(0.4)
        self.clear_scene()

    def research(self):
        head = label(r"Research on design itself", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"lightweight formal models", r"designs written in TLA$^+$ or P and model-checked before code "
                 r"\ (Part 43): \ Amazon and Microsoft now do it for storage and messaging", YES),
            tile(r"deterministic simulation", r"whole systems run under simulated networks, \ disks and clocks, \ "
                 r"failures injected from a seed \ (FoundationDB, \ Antithesis)", DATA),
            tile(r"designs from requirements", r"tools that propose architectures and capacity from stated "
                 r"requirements; \ language models as design assistants, \ with the same caution as Part 40", KERN),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"open: \ a calculus of designs, \ composing blocks with known guarantees into systems "
                             r"whose guarantees can be derived", 12.4, font_size=21, color=NO).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "System design is starting to become a subject of research in its own right. <bookmark mark='a'/> "
            "Lightweight formal models, in TLA-plus or the P language, are written and model-checked before code, as "
            "Amazon and Microsoft now do for storage and messaging services. <bookmark mark='b'/> Deterministic "
            "simulation runs a whole system against simulated networks, disks and clocks, injecting failures from a "
            "random seed so that every bug can be replayed. <bookmark mark='c'/> And tools are appearing that "
            "propose designs and capacity from requirements, language models among them, which deserve the same "
            "caution as Part 40's automated authors. <bookmark mark='d'/> What does not yet exist is a calculus of "
            "design: blocks with known guarantees, composed into systems whose guarantees follow."
        ) as vo:
            self.play(FadeIn(head))
            for mk, t in zip("abc", tiles):
                vo.wait_until(mk)
                self.play(FadeIn(t, shift=UP * 0.15))
            vo.wait_until("d")
            self.play(FadeIn(foot))
        self.wait(0.4)
        self.clear_scene()

    def open(self):
        head = label(r"Open", font_size=36).to_edge(UP, buff=0.3)
        items = VGroup(
            wrapped_label(r"1. \ \textbf{Composable guarantees}: \ deriving a system's latency and consistency from "
                          r"its blocks'.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Testing error paths}: \ finding the mishandled non-fatal errors before "
                          r"production does.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Feed ranking and fan-out together}: \ the cheapest timeline construction "
                          r"for a given ranking quality.", 12.4, font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Adaptive bitrate}: \ control with guarantees on rebuffering under unknown "
                          r"bandwidth.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ the fan-out policy, \ per user and per "
                             r"post, \ that minimizes the total work of a feed for a given power law and read-write "
                             r"ratio, \ with a proof", 12.4, font_size=23, color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Deriving a whole system's latency and consistency from the "
            "guarantees of its blocks. <bookmark mark='b'/> Finding the mishandled non-fatal errors before "
            "production finds them. <bookmark mark='c'/> Building timelines at the least cost for a given quality of "
            "ranking. <bookmark mark='d'/> And bitrate adaptation with guarantees on rebuffering when the bandwidth "
            "is unknown. <bookmark mark='e'/> This part's research problem asks for the best fan-out policy, chosen "
            "per user and per post, for a follower graph with a given power law and a given ratio of reads to "
            "writes, together with a proof that it is best."
        ) as vo:
            self.play(FadeIn(head))
            for mk, it in zip("abcd", items):
                vo.wait_until(mk)
                self.play(FadeIn(it))
            vo.wait_until("e")
            self.play(FadeIn(star))
        self.wait(0.6)
        self.clear_scene()


_ = (DATA, KERN, LAM, NO, YES)
