from matlab_interface import MatlabInterface
import sys

args = [float(x) for x in sys.argv[1:]]
print(args)

m_inf = MatlabInterface()
y = m_inf.compute_result(args)
print(y)
