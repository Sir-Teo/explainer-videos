"""Terminal-language semantics and avoiding a redundant post-record model step."""
import torch
from videos.ai.ai19.grammar import Automaton,RECORD,build_index,generate

def test_completed_record_is_terminal_even_with_completed_literal_in_closure():
    auto=Automaton(RECORD)
    prefix=auto.run(auto.start,'{"name": "Ab", "age": 1')
    assert not auto.final(prefix)
    terminal=auto.step(prefix,'}')
    assert auto.accepting(terminal) and auto.final(terminal)
    assert auto.step(terminal,'x') is None

def test_accepting_optional_suffix_can_still_consume_more():
    auto=Automaton([('lit','x'),('cls','0-9',0,1)])
    prefix=auto.run(auto.start,'x')
    assert auto.accepting(prefix) and not auto.final(prefix)
    assert auto.final(auto.step(prefix,'1'))

def test_accepting_repetition_stops_only_at_its_maximum():
    auto=Automaton([('cls','A-Z',1,2)])
    prefix=auto.run(auto.start,'A')
    assert auto.accepting(prefix) and not auto.final(prefix)
    assert auto.final(auto.step(prefix,'B'))

def test_generator_does_not_evaluate_model_after_terminal_token():
    class EngineWitness:
        calls=0
        def new_cache(self,*args):return object()
        def forward(self,*args,**kwargs):
            self.calls+=1
            return torch.zeros(1,2)
    auto=Automaton([('lit','x')]);index,order=build_index(auto,['x','y'])
    engine=EngineWitness()
    assert generate(engine,[0],4,0,index=index,order=order,auto=auto)==[0]
    assert engine.calls==1  # prefill only; no unused logits after the closing token
