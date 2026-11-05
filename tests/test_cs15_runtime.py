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

    def test_tail_calls_bound_the_stack(self):
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


if __name__ == "__main__":
    unittest.main()
