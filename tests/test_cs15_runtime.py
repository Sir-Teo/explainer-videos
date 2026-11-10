"""Part 15's runtime: the bytecode compiler, the reference VM and its collectors, the Pebble VM, tri-color marking,
the CEK machine and the tiny Prolog."""
import unittest

from explainer.cs.lang.lam import ml
from explainer.cs.pebble import programs as PR
from explainer.cs.runtime import bytecode as B
from explainer.cs.runtime import cek, prolog, pvm, tricolor
from explainer.cs.runtime import vm as V

TEXT = (b"It was the best of times, it was the worst of times, it was the age of wisdom, it was the age of "
        b"foolishness, it was the epoch of belief, it was the epoch of incredulity, it was the season of Light, "
        b"it was the season of Darkness.")


def run_value(src, heap=None):
    p = B.compile_program(ml.parse(src))
    vm = V.VM(p, heap or V.Cheney(4000)).run()
    return vm, vm.stack[vm.sp - 1]


class TestRuntime(unittest.TestCase):
    def test_job_under_every_collector(self):
        p = B.job_program()
        ref = PR.job_reference(TEXT)
        for heap in (V.Cheney(3000), V.MarkSweep(3600), V.MarkCompact(3600), V.Generational(512, 3000)):
            vm = V.VM(p, heap, tape=TEXT).run()
            self.assertEqual(bytes(vm.output), ref, heap.name)
            self.assertGreater(len(heap.log), 0, heap.name)

    def test_pebble_vm_agrees_with_reference(self):
        p = B.job_program()
        c = pvm.build(3000)
        m = pvm.run(c, p, TEXT)
        self.assertEqual(bytes(m.output), PR.job_reference(TEXT))
        vm = V.VM(p, V.Cheney(3000), tape=TEXT).run()
        st = pvm.stats(m, c)
        self.assertEqual(st["gcs"], len(vm.heap.log))
        self.assertEqual(st["copied"], sum(r["work"] for r in vm.heap.log))
        self.assertEqual(st["maxsp"], vm.stats["max_stack"])

    def test_tail_calls_reduce_stack_on_fixed_vocabulary(self):
        p = B.job_program()
        long = TEXT * 4
        on = V.VM(p, V.Cheney(20000), tape=long).run()
        off = V.VM(p, V.Cheney(20000), tape=long, tco=False).run()
        self.assertEqual(bytes(on.output), bytes(off.output))
        self.assertGreater(off.stats["max_stack"], 5 * on.stats["max_stack"])

    def test_closures_and_partial_application(self):
        vm, v = run_value("let add a b = a + b ;; let f = add 3 in f 4")
        self.assertEqual(v >> 1, 7)
        self.assertGreater(vm.stats["paps"], 0)
        vm, v = run_value("let make n = let g = fun x -> x * n in g ;; let t = make 3 in t 5")
        self.assertEqual(v >> 1, 15)
        _, v = run_value("let x = 1 ;; let f = fun y -> x + y in let x = 10 in f 0")
        self.assertEqual(v >> 1, 1)          # lexical scope

    def test_structural_equality_and_div(self):
        _, v = run_value("let a = [1; 2; 3] ;; if a = [1; 2; 3] then 0 - 7 / 2 else 99")
        self.assertEqual(v >> 1, -3)

    def test_tricolor_barriers(self):
        none = sum(tricolor.trial(s)["lost"] for s in range(200))
        self.assertGreater(none, 0)
        for b in ("dijkstra", "yuasa"):
            self.assertEqual(sum(tricolor.trial(s, barrier=b)["lost"] for s in range(200)), 0, b)

    def test_callcc_escape(self):
        v, st = cek.run(ml.parse(cek.PRODUCT + "product_exit [3; 0; 4]"))
        self.assertEqual(v, 0)
        self.assertEqual(st["mults"], 0)
        v, st = cek.run(ml.parse(cek.PRODUCT + "product_exit [3; 2; 4]"))
        self.assertEqual(v, 24)

    def test_prolog_append_backwards(self):
        ans, _ = prolog.solve(prolog.PROGRAM_APPEND, ("append", "X", "Y", prolog.plist([1, 2, 3])))
        self.assertEqual([(prolog.unlist(a["X"]), prolog.unlist(a["Y"])) for a in ans],
                         [([], [1, 2, 3]), ([1], [2, 3]), ([1, 2], [3]), ([1, 2, 3], [])])


class MeasurementBoundaries(unittest.TestCase):
    def test_allocation_count_handles_different_object_sizes(self):
        from unittest.mock import patch
        from videos.cs.cs15 import compute as C
        program = B.compile_program(ml.parse('let f x = x ;; (f 1, [2])'))
        with patch.object(C, '_job', return_value=program), patch.object(C, '_chapter', return_value=b''), \
             patch.object(C, '_sh', return_value='collected 0 0.01'), patch.object(C, '_version', return_value='test'):
            result = C.compute_rc()
        self.assertEqual(result['objects'], 3)
        self.assertEqual(result['allocated_words'], 8)
        self.assertEqual(result['schema'], C.SCHEMAS['rc'])

    def test_major_already_evacuates_nursery(self):
        from types import SimpleNamespace
        heap=V.Generational(6,12)
        heap.vm=SimpleNamespace(stack=[0],sp=1,globals=[])
        for cycle in range(4):
            heap.reserve(3)
            a=heap.alloc((2<<4)|V.CONS,[2*cycle+1,0])
            heap.vm.stack[0]=a<<1
            heap.reserve(3);heap.alloc((2<<4)|V.CONS,[99,0])
            heap.minor()
        self.assertEqual([r['kind'] for r in heap.log],['minor','minor','minor','major'])
        self.assertEqual(heap.nfree,1)
        root=heap.vm.stack[0]>>1
        self.assertEqual(heap.mem[root+1]>>1,3)
        heap.reserve(3)
        self.assertEqual(heap.nfree,1)

    def test_minor_uses_consumed_words_not_capacity(self):
        from types import SimpleNamespace
        heap=V.Generational(8,32)
        heap.vm=SimpleNamespace(stack=[0],sp=1,globals=[])
        a=heap.alloc((2<<4)|V.CONS,[3,0]);heap.vm.stack[0]=a<<1
        heap.minor()
        event=heap.log[-1]
        self.assertEqual(event['nursery_used'],3)
        self.assertEqual(event['live'],3)
        self.assertEqual(event['live']/event['nursery_used'],1)

    def test_zero_observed_age_can_be_live(self):
        from videos.cs.cs15.measurements import ObservedCheney
        heap=ObservedCheney(1000)
        run_value('[1;2;3]',heap)
        report=heap.observation_summary()
        self.assertEqual(heap.lifetimes,[0,0,0])
        self.assertEqual(report['collections'],0)
        self.assertEqual(report['reachable_at_end_never_observed'],3)
        heap.collect()
        report=heap.observation_summary()
        self.assertEqual(report['observed_at_collection'],3)
        self.assertEqual(report['reachable_at_end_never_observed'],0)

    def test_tco_does_not_bound_every_recursion(self):
        depths=[]
        for n in (20,80,200):
            tape=b' '.join(bytes((97+i//26,97+i%26)) for i in range(n))+b' '
            vm=V.VM(B.job_program(),V.Cheney(20000),tape=tape).run()
            self.assertEqual(bytes(vm.output),PR.job_reference(tape))
            depths.append(vm.stats['max_stack'])
        self.assertLess(depths[0],depths[1]);self.assertLess(depths[1],depths[2])

    def test_failed_tool_is_not_a_measurement(self):
        import subprocess,sys
        from videos.cs.cs15.compute import _sh
        with self.assertRaises(subprocess.CalledProcessError):
            _sh([sys.executable,'-c','import sys; print("not a timing"); sys.exit(7)'])

    def test_schema_upgrade_is_guarded_at_instance_entry(self):
        import json,tempfile
        from pathlib import Path
        from unittest.mock import patch
        from videos.cs.cs15 import compute as C
        from tools.qa_series import StaleDataError,require_current_cache
        with tempfile.TemporaryDirectory() as directory:
            cache=C.RuntimeCache('cs15');cache.dir=Path(directory)
            cache.path('gen').write_text(json.dumps({'schema':1,'historical':True}))
            calls=[]
            def producer():calls.append(True);return {'schema':C.SCHEMAS['gen'],'corrected':True}
            with patch.object(C,'CACHE',cache),patch.dict(C.ITEMS,gen=producer):
                with self.assertRaises(StaleDataError):
                    require_current_cache(C,'cs15',cache.path('gen'),'gen')
                self.assertEqual(calls,[])
                self.assertTrue(C.load('gen')['corrected'])
                self.assertEqual(calls,[True])
                self.assertTrue(C.cache_current('gen'))

    def test_pause_records_and_workload_checksum(self):
        from videos.cs.cs15.measurements import java_pause_events,go_pause_events,checked_churn_result
        java='[0.1s][info][gc] GC(0) Pause Young (Normal) 10M->1M(20M) 1.250ms\n'
        self.assertEqual([r['ms'] for r in java_pause_events(java)],[1.25])
        zgc='[0.145s][info][gc,phases] GC(0) Y: Pause Mark Start (Major) 0.015ms\n'
        self.assertEqual([r['ms'] for r in java_pause_events(zgc)],[.015])
        self.assertEqual([r['ms'] for r in java_pause_events(zgc.replace('Y:', 'y:'))],[.015])
        go='gc 1 @0.01s 2%: 0.1+1.5+0.2 ms clock, 0.3+0/1/0+0.4 ms cpu\n'
        self.assertEqual([r['ms'] for r in go_pause_events(go)],[.1,.2])
        self.assertEqual(checked_churn_result('45 0.5\n',10),.5)
        with self.assertRaises(AssertionError):checked_churn_result('44 0.5\n',10)
        with self.assertRaises(ValueError):checked_churn_result('45 0\n',10)

    def test_same_barrier_moves_preserve_reachable_target(self):
        from videos.cs.cs15.measurements import barrier_color_witness
        rows=barrier_color_witness()
        self.assertTrue(all(r['reachable'] for r in rows))
        self.assertEqual([r['lost'] for r in rows],[True,False,False])
        self.assertEqual([r['colors'][-1] for r in rows],[tricolor.WHITE,tricolor.BLACK,tricolor.BLACK])


if __name__ == "__main__":
    unittest.main()
