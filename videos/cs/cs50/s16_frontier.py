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


class Frontier(WatchScene):
    def construct(self):
        self.card()
        self.gray()

    def card(self):
        self.chapter(15, r"Frontier: \ gray failure and metastability", r"Can we predict the failures that persist?", lit=(2017, 2022), extra=((2017, r"Huang et al.: \ gray failure"),
                                   (2022, r"Huang et al.: \ metastable failures in the wild")), part=PART, said="Chapter fifteen, the frontier. Can we predict the failures that persist?")

    def gray(self):
        self.ask(r"A replica's health check answers OK, \\ but its real requests fail. This is...", [r"fail-stop",
                 r"gray failure"], 1,
                 say="A replica's health check answers OK, but its real requests fail. What kind of failure is that?",
                 reveal="Gray failure: different observers see different truths.")
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





_ = (DATA, KERN, LAM, NO, YES)
