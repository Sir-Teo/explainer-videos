from __future__ import annotations

from videos.psychology.psych51.common import *  # noqa: F403


class Tmi(VoiceoverScene):
    def construct(self):
        card_section(self, 4, r"A light that told the wrong story", r"What did the operators see?", marr=("how",))
        self.story()
        self.lessons()

    def story(self):
        rows_section(self, r"Three Mile Island, \ 1979", [
            (r"a relief valve in a nuclear plant's cooling circuit opened as designed, \ and then stuck open", WHITE),
            (r"a light on the panel went out: \ it showed that the valve had been commanded to close, \ not that it "
             r"had closed", AUTH),
            (r"believing the valve shut, \ and reading a rising pressurizer level as too much water, \ the operators "
             r"cut the emergency cooling", PERSON),
            (r"hundreds of alarms sounded in the first minutes; \ the core partly melted", AUTH),
            (r"the investigations found the operators had done what their displays and training implied", YOU),
        ], "Here's what design-induced error looks like at scale. <bookmark mark='a'/> In 1979, at Three Mile Island, a "
           "relief valve in a nuclear plant's cooling circuit opened as designed, and then stuck open. "
           "<bookmark mark='b'/> A light on the panel went out. It showed that the valve had been commanded to close, "
           "not that it had closed. <bookmark mark='c'/> Believing the valve shut, and reading a rising level in the "
           "pressurizer as too much water, the operators cut back the emergency cooling. <bookmark mark='d'/> "
           "Hundreds of alarms sounded in the first minutes, and the core partly melted. <bookmark mark='e'/> The "
           "investigations found that the operators had done what their displays and their training implied.")

    def lessons(self):
        chips_section(self, r"What changed", [
            (r"show the state", r"display what a component is doing, \ measured, \ not what it was told to do", GOOD),
            (r"prioritize alarms", r"rank, \ group and suppress consequences, \ so the first cause is visible "
                                   r"(chapter ten)", MODEL),
            (r"train for the unexpected", r"simulator training on failures the procedures do not cover: \ "
                                          r"knowledge-based work, \ practised", PERSON),
            (r"human factors by law", r"control-room design reviews became part of licensing", SYMP),
        ], "What changed afterwards? <bookmark mark='a'/> Show the state: display what a component is actually doing, "
           "measured, not what it was told to do. <bookmark mark='b'/> Prioritize alarms: rank them, group them, and "
           "suppress the consequences, so the first cause stays visible. <bookmark mark='c'/> Train for the "
           "unexpected, with simulator time on failures the procedures don't cover. <bookmark mark='d'/> And human "
           "factors by law: control-room design reviews became part of licensing.")
