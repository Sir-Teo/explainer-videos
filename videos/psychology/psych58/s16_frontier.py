from __future__ import annotations

from videos.psychology.psych58.common import *  # noqa: F403


class Frontier(VoiceoverScene):
    def construct(self):
        card_section(self, 15, r"Frontier: \ one principle?", r"What would settle it?", scale=("brain", "person"))
        self.new()
        self.open()

    def new(self):
        chips_section(self, r"What is new", [
            (r"layer by layer", r"recordings across cortical layers and areas, \ shared openly, \ designed to test "
                                r"predictive coding against adaptation", MODEL),
            (r"efficient memory", r"rate-distortion accounts of working memory and of what is forgotten", PERSON),
            (r"deep networks as models", r"networks trained on images predict visual cortex's responses; \ which "
                                         r"objective makes them brain-like is an open test", GOOD),
            (r"sparse features in AI", r"Olshausen and Field's method, \ revived to read the features inside "
                                       r"language models", SYMP),
        ], "What would settle it? First, what's new. <bookmark mark='a'/> Recordings across cortical layers and "
           "areas, shared openly, and designed to test predictive coding against adaptation. <bookmark mark='b'/> "
           "Rate-distortion accounts of working memory, and of what's forgotten. <bookmark mark='c'/> Deep networks "
           "trained on images predict visual cortex's responses, and which objective makes them brain-like is an "
           "open test. <bookmark mark='d'/> And Olshausen and Field's method has been revived to read the features "
           "inside language models.", chip_w=4.2, text_w=8.0)

    def open(self):
        chips_section(self, r"Open problems", [
            (r"capacity", r"a normative account of why working memory and attention have the limits they do", AUTH),
            (r"learning", r"which learning rule cortex actually uses", MODEL),
            (r"risk", r"whether any unified theory makes a risky prediction that the special theories do not", PERSON),
            (r"objectives", r"what the brain is optimizing, \ if anything, \ beyond each sense's code", GOOD),
        ], "And the open problems. <bookmark mark='a'/> A normative account of why working memory and attention have "
           "the limits they do. <bookmark mark='b'/> Which learning rule cortex actually uses. <bookmark mark='c'/> "
           "Whether any unified theory makes a risky prediction that the special theories don't. "
           "<bookmark mark='d'/> And what the brain is optimizing, if anything, beyond each sense's code.")
