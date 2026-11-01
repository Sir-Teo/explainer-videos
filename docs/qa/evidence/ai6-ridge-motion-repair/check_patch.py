import ast,copy,hashlib,json,unittest
from pathlib import Path
import numpy as np
from manim import VMobject
R=Path('/workspace/runtime/ai6-ridge-reveal-repair');before=ast.parse((R/'before.py').read_text());after=ast.parse((R/'after.py').read_text())
def path_expr(tree):
 return next(n for n in ast.walk(tree) if isinstance(n,ast.ListComp) and isinstance(n.elt,ast.Call) and ast.unparse(n.elt.func)=='ax2.c2p')
def derive(tree):
 return next(n for n in ast.walk(tree) if isinstance(n,ast.FunctionDef) and n.name=='derive')
class Checks(unittest.TestCase):
 def test_only_three_append_flags_and_exact_traversal_changed(self):
  norm=copy.deepcopy(after);count=0
  for n in ast.walk(derive(norm)):
   if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='step' and n.args and isinstance(n.args[0],ast.Constant) and n.args[0].value in (1,2,3):
    self.assertEqual([(k.arg,ast.literal_eval(k.value)) for k in n.keywords],[('transform',False)]);n.keywords=[];count+=1
  self.assertEqual(count,3)
  new=path_expr(norm);old=path_expr(before);new.generators=copy.deepcopy(old.generators)
  self.assertEqual(ast.dump(norm,include_attributes=False),ast.dump(before,include_attributes=False))
 def test_actual_path_expression_has_same_vertices_strong_to_weak(self):
  class Axis:
   def c2p(self,x,y):return np.array([x,y,0.])
  lx=np.array([-1.,0.,2.,5.]);coef=np.array([[1.,-.5],[.9,-.45],[.2,-.15],[.001,-.001]])
  for j in range(2):
   env={'ax2':Axis(),'lx':lx,'coef':coef,'j':j,'zip':zip}
   old=eval(compile(ast.Expression(path_expr(before)),'before','eval'),env)
   new=eval(compile(ast.Expression(path_expr(after)),'after','eval'),env)
   np.testing.assert_array_equal(new,np.asarray(old)[::-1]);self.assertEqual(sorted(map(tuple,new)),sorted(map(tuple,old)))
   self.assertEqual(new[0][0],-lx[-1]);self.assertEqual(new[-1][0],-lx[0]);self.assertTrue(np.all(np.diff(np.array(new)[:,0])>0))
   line=VMobject().set_points_as_corners(new);np.testing.assert_array_equal(line.get_start(),new[0]);np.testing.assert_array_equal(line.get_end(),new[-1])
 def test_shared_ladder_write_branch_preserves_requested_duration(self):
  tree=ast.parse(Path('/workspace/explainer-videos/explainer/analysis/__init__.py').read_text());ladder=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='ladder');step=next(n for n in ast.walk(ladder) if isinstance(n,ast.FunctionDef) and n.name=='step')
  self.assertEqual(ast.literal_eval(step.args.defaults[0]),1.2)
  branch=next(n for n in ast.walk(step) if isinstance(n,ast.If) and 'not transform' in ast.unparse(n.test))
  writes=[n for n in ast.walk(branch) if isinstance(n,ast.Call) and ast.unparse(n.func)=='Write'];self.assertEqual(len(writes),1)
  play=next(n for n in ast.walk(branch) if isinstance(n,ast.Call) and ast.unparse(n.func)=='scene.play');self.assertIn('run_time=run_time',ast.unparse(play))
if __name__=='__main__':unittest.main(verbosity=2)
