import subprocess
import ast

def compute_result(tempPG):
	args_list = ["python", "/home/riaps/Sample/SampleProject/riaps_apps/RASApplication/compute_result.py"]
	for pg in tempPG:
		args_list.append(str(pg))
	result_string = subprocess.check_output(args_list, universal_newlines=True).split("\n")[-2]
	result_list = ast.literal_eval(result_string)
	result = [x[0] for x in result_list]
	return result
