from __future__ import annotations

from videos.music.music53.common import *  # noqa: F403


class Frontier(SoundScene):
    def construct(self):
        chapter(self, 11, r"Frontier: \ learning in the audio thread; \ networked performance", r"Can a network meet a deadline, \ or a band play across a continent?")
        self.neural()
        self.network()
        self.browser()
        self.problem()

    # ------------------------------------------------------------------
    def neural(self):
        items = [
            (r"neural instruments and effects now run inside plug-ins: \ RAVE \ (Antoine Caillon and Philippe Esling, \ 2021) \ in real time on a laptop", WHITE),
            (r"a network's cost is predictable, \ but large: \ it must fit every block's deadline, \ every time", WHITE),
            (r"many need look-ahead or long blocks, \ so they add latency the graph must compensate", WHITE),
            (r"learning while playing is harder still: \ training must happen outside the audio thread", WHITE),
            (r"the open question: \ the best model that never misses a deadline", TUNE),
        ]
        rows_scene(self, r"learning in the audio thread", items,
                   "Two frontiers meet this part's engine. <bookmark mark='b'/> Neural instruments and effects now run inside "
                   "plug-ins; RAVE, from Antoine Caillon and Philippe Esling in 2021, runs in real time on a laptop. "
                   "<bookmark mark='c'/> A network's cost is predictable but large, and it must fit every block's deadline, every "
                   "time. <bookmark mark='d'/> Many need look-ahead or long blocks, so they add latency the graph must compensate. "
                   "<bookmark mark='e'/> Learning while playing is harder still: training must happen outside the audio thread. "
                   "<bookmark mark='f'/> The open question is the best model that never misses a deadline.", marks="bcdef")

    # ------------------------------------------------------------------
    def network(self):
        items = [
            (r"networked performance: \ musicians in different cities, \ one piece", WHITE),
            (r"light in fibre travels about 200 km a millisecond: \ 1000 km costs 5 ms each way before any buffering", WHITE),
            (r"Chris Chafe's JackTrip \ (Stanford, \ 2000s) \ sends uncompressed audio with the smallest buffers it dares", WHITE),
            (r"clapping experiments: \ duos keep a steady tempo up to about 20--25 ms of delay; \ beyond it they slow down", WHITE),
            (r"the speed of light sets a radius for real-time ensemble playing", TUNE),
        ]
        rows_scene(self, r"networked performance", items,
                   "The second frontier is distance. <bookmark mark='b'/> In networked performance, musicians in different cities "
                   "play one piece. <bookmark mark='c'/> Light in fibre travels about two hundred kilometres a millisecond, so a "
                   "thousand kilometres costs five milliseconds each way before any buffering. <bookmark mark='d'/> Chris Chafe's "
                   "JackTrip, from Stanford, sends uncompressed audio with the smallest buffers it dares. <bookmark mark='e'/> In "
                   "clapping experiments, duos keep a steady tempo up to about twenty to twenty-five milliseconds of delay, and "
                   "beyond it they slow down. <bookmark mark='f'/> The speed of light sets a radius for real-time ensemble "
                   "playing.", marks="bcdef")

    # ------------------------------------------------------------------
    def problem(self):
        rows_ = text_rows([
            (r"take a neural effect and the engine of this part; \ measure its cost per block across a thousand runs", WHITE),
            (r"find its worst case, \ not its average: \ the deadline is set by the slowest block", WHITE),
            (r"trade model size against block size and look-ahead, \ and judge each by blind listening", WHITE),
            (r"$\bigstar$ \ research problem: \ what is the best-sounding model that is guaranteed never to miss a deadline?", EAR),
            (r"an answer would tell plug-in makers how much learning fits in two milliseconds", TUNE),
        ])
        head = label(r"a research problem", font_size=30, color=GREY_A).to_edge(UP, buff=0.45)
        with self.voiceover(
            "A research problem to end on. <bookmark mark='a'/> Take a neural effect and the engine of this part, and measure its "
            "cost per block across a thousand runs. <bookmark mark='b'/> Find its worst case, not its average, because the "
            "deadline is set by the slowest block. <bookmark mark='c'/> Trade model size against block size and look-ahead, "
            "and judge each by blind listening. <bookmark mark='d'/> The question: what is the best-sounding model that is "
            "guaranteed never to miss a deadline? <bookmark mark='e'/> An answer would tell plug-in makers how much learning "
            "fits in two milliseconds."
        ) as vo:
            self.play(FadeIn(head), FadeIn(ghost(rows_, 0.15)))
            for mark, r in zip("abcde", rows_):
                vo.wait_until(mark)
                self.play(FadeIn(r))
        self.wait(0.4)
        self.clear_scene()

    # ------------------------------------------------------------------
    def browser(self):
        items = [
            (r"the Web Audio API \ (from 2011) \ put an audio graph in every browser; \ AudioWorklet \ (2018) \ lets pages run their own nodes", WHITE),
            (r"Web MIDI lets a page talk to a keyboard on the desk", WHITE),
            (r"this course's interactives use the same graph, \ a small DAW in a page", WHITE),
            (r"collaborative sessions now share one project from several places, \ if not one moment", WHITE),
            (r"the engine is everywhere; \ the deadline comes with it", TUNE),
        ]
        rows_scene(self, r"the browser as a studio", items,
                   "The engine has also left the studio. <bookmark mark='b'/> The Web Audio API, from 2011, put an audio graph in "
                   "every browser, and AudioWorklet, from 2018, lets a page run its own nodes in the audio thread. "
                   "<bookmark mark='c'/> Web MIDI lets a page talk to a keyboard on the desk. <bookmark mark='d'/> This course's "
                   "interactives use the same graph: a small workstation in a page. <bookmark mark='e'/> Collaborative sessions now "
                   "share one project from several places, if not one moment. <bookmark mark='f'/> The engine is everywhere, and the "
                   "deadline comes with it.", marks="bcdef")
