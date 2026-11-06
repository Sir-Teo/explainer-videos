from __future__ import annotations

from explainer.cs import *  # noqa: F403
from videos.cs.cs50.common import BG, DATA, HEAD, KERN, LAM, NO, PART, YES, load


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
        self.gray()
        self.boundary()
        self.research()
        self.open()

    def card(self):
        card = chapter_card(15, r"Frontier: \ gray failure and metastability",
                            r"Can we predict the failures that persist?", lit=(2017, 2022),
                            extra=((2017, r"Huang et al.: \ gray failure"),
                                   (2022, r"Huang et al.: \ metastable failures in the wild")), part=PART)
        with self.voiceover("Chapter fifteen, the frontier. Can we predict the failures that persist?"):
            self.play(FadeIn(card[0], shift=UP * 0.2), FadeIn(card[1]), FadeIn(card[2]))
        self.play(FadeOut(card))

    def gray(self):
        head = label(r"Gray failure: \ healthy to itself, \ broken to its users", font_size=36).to_edge(UP, buff=0.3)
        box = RoundedRectangle(width=3.0, height=1.4, corner_radius=0.15, stroke_color=KERN, stroke_width=2.5,
                               fill_color=BG, fill_opacity=1)
        srv = VGroup(box, label(r"a replica", font_size=22, color=KERN).move_to(box)).move_to(ORIGIN + UP * 0.3)
        probe = label(r"health check: \ OK", font_size=20, color=YES).next_to(srv, LEFT, buff=1.6)
        users = label(r"users: \ timeouts", font_size=20, color=NO).next_to(srv, RIGHT, buff=1.6)
        a1 = Arrow(probe.get_right(), srv.get_left(), buff=0.15, color=YES, stroke_width=2.5)
        a2 = Arrow(users.get_left(), srv.get_right(), buff=0.15, color=NO, stroke_width=2.5)
        note_ = wrapped_label(r"Huang et al. \ (HotOS 2017): \ differential observability, \ where the failure "
                              r"detector and the application see different things; \ a slow disk, \ a lossy link, \ a "
                              r"stuck thread", 12.0, font_size=20, color=GREY_A).next_to(srv, DOWN, buff=0.9)
        fix = wrapped_label(r"the remedy is to judge health as users do: \ outlier ejection from real requests, \ as "
                            r"the Job's client did", 12.0, font_size=21, color=WHITE).to_edge(DOWN, buff=0.5)
        with self.voiceover(
            "The easy failures are the ones where something stops. <bookmark mark='a'/> The hard ones are gray: a "
            "replica whose health check answers OK, because the check is cheap and fast, <bookmark mark='b'/> while "
            "the users' real requests time out on a slow disk, a lossy link or a stuck thread. "
            "<bookmark mark='c'/> Peng Huang and colleagues named this in 2017, and called its cause differential "
            "observability: the failure detector and the application see different worlds. "
            "<bookmark mark='d'/> The remedy is to judge health the way users do, from the outcomes of real "
            "requests, as the Job's best client did when it ejected the slow replica."
        ) as vo:
            self.play(FadeIn(head), FadeIn(srv))
            vo.wait_until("a")
            self.play(FadeIn(probe), GrowArrow(a1))
            vo.wait_until("b")
            self.play(FadeIn(users), GrowArrow(a2), Wiggle(srv))
            vo.wait_until("c")
            self.play(FadeIn(note_))
            vo.wait_until("d")
            self.play(FadeIn(fix))
        self.wait(0.4)
        self.clear_scene()

    def boundary(self):
        rows = load("trigger")["rows"]
        head = label(r"Where does a trigger tip the system over?", font_size=36).to_edge(UP, buff=0.3)
        drops = sorted({r["drop"] for r in rows}, reverse=True)
        lens = sorted({r["seconds"] for r in rows})
        cell = 1.05
        grid = VGroup()
        stuck = {(r["drop"], r["seconds"]): r["stuck"] for r in rows}
        for i, d in enumerate(drops):
            for j, L in enumerate(lens):
                s = stuck[(d, L)]
                sq = Square(side_length=cell, stroke_color=GREY_D, stroke_width=1, fill_color=NO if s else YES,
                            fill_opacity=0.75 if s else 0.35)
                sq.move_to([j * cell, -i * cell, 0])
                grid.add(sq)
        grid.move_to(LEFT * 2.2 + DOWN * 0.4)
        xl = VGroup(*[label(rf"{L} s", font_size=18, color=GREY_B).next_to(grid[j], UP, buff=0.12)
                      for j, L in enumerate(lens)])
        yl = VGroup(*[label(rf"{100 * d:.0f}\%", font_size=18, color=GREY_B).next_to(grid[i * len(lens)], LEFT,
                                                                                   buff=0.15)
                      for i, d in enumerate(drops)])
        xt = label(r"how long the trigger lasts", font_size=18, color=GREY_A).next_to(xl, UP, buff=0.15)
        yt = label(r"capacity left", font_size=18, color=GREY_A).rotate(PI / 2).next_to(yl, LEFT, buff=0.2)
        key = VGroup(label(r"red: \ still collapsed 60 s after the trigger ends", font_size=18, color=NO),
                     label(r"green: \ recovered", font_size=18, color=YES)).arrange(DOWN, aligned_edge=LEFT,
                                                                                    buff=0.15)
        key.next_to(grid, RIGHT, buff=0.8).shift(UP * 0.8)
        side = wrapped_label(r"the same server, \ load and retry policy \ (80\% busy, \ 1 s timeout, \ 3 retries); "
                             r"\ only the trigger varies", 4.6, font_size=18, color=GREY_A).next_to(key, DOWN,
                                                                                                 buff=0.5)
        side.align_to(key, LEFT)
        n_stuck = sum(1 for r in rows if r["stuck"])
        with self.voiceover(
            "Metastable failures are the frontier's sharpest problem. Nathan Bronson and colleagues described them in "
            "2021, and Lexiang Huang and colleagues found them in production systems at many companies the year "
            "after. <bookmark mark='a'/> Here is our retrying server from chapter three, hit by triggers of "
            "different sizes: its capacity falls to some fraction of normal, for some number of seconds. "
            f"<bookmark mark='b'/> In {n_stuck} of these {len(rows)} cases the system is still collapsed a minute "
            "after the trigger has gone, held there by its own retries. <bookmark mark='c'/> The boundary between "
            "green and red is the thing an operator most needs to know, and today it is found by experiment, or "
            "by an outage. There is no general theory that predicts it from a system's design."
        ) as vo:
            self.play(FadeIn(head))
            vo.wait_until("a")
            self.play(FadeIn(xl), FadeIn(yl), FadeIn(xt), FadeIn(yt), FadeIn(side))
            vo.wait_until("b")
            self.play(LaggedStart(*[FadeIn(s) for s in grid], lag_ratio=0.05), FadeIn(key), run_time=2.5)
            vo.wait_until("c")
            self.play(Indicate(grid, color=HEAD, scale_factor=1.02))
        self.wait(0.4)
        self.clear_scene()

    def research(self):
        head = label(r"Research on keeping systems running", font_size=36).to_edge(UP, buff=0.3)
        tiles = VGroup(
            tile(r"metastability models", r"queueing models and simulators that locate the boundary between "
                 r"recovery and collapse before an outage does \ (Huang et al. \ 2022 and after)", NO),
            tile(r"safer change", r"most outages follow changes \ (Part 49): \ progressive delivery, \ automatic "
                 r"rollback, \ and verifying configuration before it ships", HEAD),
            tile(r"machines on call", r"language models that read alerts, \ logs and past incidents and propose a "
                 r"root cause; \ studied at Microsoft and elsewhere, \ judged by people", DATA),
        ).arrange(RIGHT, buff=0.3).next_to(head, DOWN, buff=0.6)
        foot = wrapped_label(r"open: \ guarantees about a running system as a whole, \ not just about its parts", 12.4,
                             font_size=21, color=LAM).to_edge(DOWN, buff=0.6)
        with self.voiceover(
            "Three lines of research. <bookmark mark='a'/> Models of metastability: queueing models and "
            "simulators that find the boundary between recovery and collapse, so that it can be designed for rather "
            "than discovered. <bookmark mark='b'/> Safer change: since most outages follow a change, progressive "
            "delivery, automatic rollback, and checking configuration the way we check code. <bookmark mark='c'/> "
            "And machines on call: language models that read alerts, logs and past incidents and propose a root "
            "cause. Microsoft and others have published studies of such systems; their suggestions are still judged "
            "by people. <bookmark mark='d'/> Under all three sits one open question: how to state and check "
            "guarantees about a running system as a whole."
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
            wrapped_label(r"1. \ \textbf{Predicting metastability}: \ the trigger sizes a design survives, \ from the "
                          r"design.", 12.4, font_size=24, color=WHITE),
            wrapped_label(r"2. \ \textbf{Detecting gray failure}: \ fast, \ with few false alarms, \ from users' "
                          r"requests.", 12.4, font_size=24, color=YES),
            wrapped_label(r"3. \ \textbf{Safe change at scale}: \ how slowly to roll out, \ for a given risk.", 12.4,
                          font_size=24, color=HEAD),
            wrapped_label(r"4. \ \textbf{Root cause from telemetry}: \ which signals suffice, \ and how much a model "
                          r"can be trusted.", 12.4, font_size=24, color=KERN),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35).next_to(head, DOWN, buff=0.45)
        star = wrapped_label(r"$\bigstar$ \ this part's research problem: \ for a server with capacity, \ load, \ "
                             r"timeout and retry policy given, \ characterize the triggers \ (depth and duration) "
                             r"after which it cannot recover, \ with a proof", 12.4, font_size=23,
                             color=LAM).to_edge(DOWN, buff=0.35)
        with self.voiceover(
            "Open problems. <bookmark mark='a'/> Predicting from a design which triggers it will survive. "
            "<bookmark mark='b'/> Detecting gray failure quickly, with few false alarms, from users' own requests. "
            "<bookmark mark='c'/> Deciding how slowly to roll out a change, for a given appetite for risk. "
            "<bookmark mark='d'/> And finding root causes from telemetry: which signals are enough, and how far a "
            "model's answer can be trusted. <bookmark mark='e'/> This part's research problem asks for the map we "
            "just drew, derived rather than simulated: for a server of given capacity, load, timeout and retry "
            "policy, the exact set of triggers after which it can no longer recover, with a proof."
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
