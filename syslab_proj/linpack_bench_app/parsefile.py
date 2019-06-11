import re

# filename = 'sysinfo'
# tester_pattern = 

class SysInfoParser:
	def parse_sysinfo(self, file):
		data = file.read().decode('utf-8')

		# gets motherboard name
		match = re.search(r'Motherboard:\s*([\w\.-]+)', data)
		# print("@motherboard name: " + match.group(1))
		self.motherboard = match.group(1)

		# gets bios date
		match = re.search(r'BIOS ver:\s*(\d\d/\d\d/\d\d\d\d)', data)
		# print("@bios version: " + match.group(1))
		self.bios_date = match.group(1)

		# gets ipmi version
		match = re.search(r'IPMI ver:\s*([\d.]+)', data)
		# print("@ipmi version: " + match.group(1))
		self.ipmi_version = match.group(1)

		# gets processor info
		match = re.search(r'Processor:\s*([^\n]+)', data)
		# print("@processor info: " + match.group(1))
		self.processor = match.group(1)

		# gets processor freq data
		match = re.search(r'Frequency:\s*([^\n]+)', data)
		# print("@Frequency: " + match.group(1))
		self.processor_freq = match.group(1)

		# gets processor count
		match = re.search(r'Processor Count:\s*([\d]+)', data)
		# print("@Processor Count: " + match.group(1))
		self.processor_count = match.group(1)

		# gets total core count
		match = re.search(r'Total Core Count:\s*([\d]+)+', data)
		# print("@total core count: " + match.group(1))
		self.processor_total_core_count = match.group(1)

		# gets number of DIMMS
		match = re.search(r'Number of DIMMs:\s*([\d]+)', data)
		# print("@total number of dimms: " + match.group(1))
		self.dimm_count = match.group(1)

		# gets dimm freq
		match = re.search(r'Configured Clock Speed:\s*([^\n]+)', data)
		# print("@dimm clock speed: " + match.group(1))
		self.dimm_freq = match.group(1)

		# gets list of dimm manu. 
		dimm_manu_list = re.findall(r'DIMM Manufacturer:\s*([^\n]+)', data)
		# print("@dimm manufacturer list: " + str(dimm_manu_list))
		self.dimm_manu_list = dimm_manu_list

		# gets dimm part numbers
		dimm_PN_list = re.findall(r'DIMM P/N:\s*([^\n]+)', data)
		# print("@dimm part Number list: " + str(dimm_PN_list))
		self.dimm_PN_list = dimm_PN_list

		# gets total dimm memory size
		match = re.search(r'Total Memory:\s*([^\n]+)', data)
		# print("@dimm memory size: " + match.group(1))
		self.dimm_total_mem_size = match.group(1)


		# gets processor family
		match = re.search(r'Processor is\s*([^\n]+)', data)
		# print("@processor family: " + match.group(1))
		self.processor_family = match.group(1)


		# get HPL dat block size
		match = re.search(r'Block Size =\s*([\d]+)', data)
		# print("@HPL Block size: " + match.group(1))
		self.HPL_block_size = match.group(1)

		# get HPL Problem size
		match = re.search(r'Problem Size =\s*([\d]+)', data)
		# print("@HPL problem size: " + match.group(1))
		self.HPL_problem_size = match.group(1)

		# get linpack theoretical score
		match = re.search(r'Theoretical Score =\s*([^\n]+)', data)
		# print("@linpack theoretical GFLOPS: " + match.group(1))
		self.linpack_theoretical_GFLOPS = match.group(1)


	def __init__(self, file=None):
		if not file:
			file = open("sysinfo")

		self.parse_sysinfo(file)


class LinpackParser:
	def parse_linpack_info(self, sysinfo_file, output_file):
		sysinfo_data = sysinfo_file.read().decode()
		output_file_data = output_file.read().decode()

		# get tester name
		match = re.search(r'Tester:\s*([\w\.-]+)', sysinfo_data)
		# print("@tester_name: " + match.group(1))
		self.tester_name = match.group(1)

		# get N
		match = re.search(r'N\s*:\s*([\d]+)', output_file_data)
		# print("@N: " + match.group(1))
		self.N = match.group(1)

		# get NB
		match = re.search(r'NB\s*:\s*([\d]+)', output_file_data)
		# print("@NB: " + match.group(1))
		self.NB = match.group(1)

		# get PMAP
		match = re.search(r'PMAP\s*:\s*([^\n]+)', output_file_data)
		# print("@PMAP: " + match.group(1))
		self.PMAP = match.group(1)

		#get P
		match = re.search(r'P\s*:\s*([\d]+)', output_file_data)
		# print("@P: " + match.group(1))
		self.P = match.group(1)

		# get Q
		match = re.search(r'Q\s*:\s*([\d]+)', output_file_data)
		# print("@Q: " + match.group(1))
		self.Q = match.group(1)

		# get PFACT
		match = re.search(r'PFACT\s*:\s*([^\n]+)', output_file_data)
		# print("@PFACT: ", match.group(1))
		self.PFACT = match.group(1)

		# get NBMIN
		match = re.search(r'NBMIN\s*:\s*([\d]+)', output_file_data)
		# print("@NBMIN: " + match.group(1))
		self.NBMIN = match.group(1)

		# get NDIV
		match = re.search(r'NDIV\s*:\s*([\d]+)', output_file_data)
		# print("@NDIV: " + match.group(1))
		self.NDIV = match.group(1)

		# get RFACT
		match = re.search(r'RFACT\s*:\s*([^\n]+)', output_file_data)
		# print("@RFACT: ", match.group(1))
		self.RFACT = match.group(1)

		# get BCAST
		match = re.search(r'BCAST\s*:\s*([^\n]+)', output_file_data)
		# print("@BCAST: ", match.group(1))
		self.BCAST = match.group(1)

		# get DEPTH
		match = re.search(r'DEPTH\s*:\s*([\d]+)', output_file_data)
		# print("@DEPTH: " + match.group(1))
		self.DEPTH = match.group(1)

		# get SWAP
		match = re.search(r'SWAP\s*:\s*([^\n]+)', output_file_data)
		# print("@SWAP: ", match.group(1))
		self.SWAP = match.group(1)

		# get L1
		match = re.search(r'L1\s*:\s*([^\n]+)', output_file_data)
		# print("@L1: ", match.group(1))
		self.L1 = match.group(1)

		# get U
		match = re.search(r'U\s*:\s*([^\n]+)', output_file_data)
		# print("@U: ", match.group(1))
		self.U = match.group(1)

		# get EQUIL
		match = re.search(r'EQUIL\s*:\s*([^\n]+)', output_file_data)
		# print("@EQUIL: ", match.group(1))
		self.EQUIL = match.group(1)

		# get ALIGN
		match = re.search(r'ALIGN\s*:\s*([^\n]+)', output_file_data)
		# print("@ALIGN: ", match.group(1))
		self.ALIGN = match.group(1)

		# get actual GFLOPS
		match = re.search(r'[\w]+\s+[\d]+\s+[\d]+\s+[\d]+\s+[\d]+\s+[\d\.]+\s+([\w\.\+]+)', output_file_data)
		# print("@actual GFLOPS: " + match.group(1))
		self.actual_GFLOPS = match.group(1)

		# get answer result
		match = re.search(r'([^\n=]+)=\s*([\w.]+)\s*\.\.\.\.\.\.\s*([\w]+)', output_file_data)
		if match:
			# print("@given_problem: " + match.group(1))
			self.given_problem = match.group(1)
			# print("@expected_answer: " + match.group(2))
			self.expected_answer = match.group(2)
			# print("@answer_result: " + match.group(3))
			self.answer_result = match.group(3)

		#	read into DB. add fields on model to save uploaded files


	def __init__(self, sysinfo_file=None, output_file=None):
		if not sysinfo_file:
			sysinfo_file = open("sysinfo")
		if not output_file:
			output_file = open("output")

		self.parse_linpack_info(sysinfo_file, output_file)


def test_sysinfo():
	#sysinfo_obj = SysInfoParser()
	file = open("sysinfo")
	sysinfo_obj = SysInfoParser(file)

def test_linpack():
	sysinfo_file = open("sysinfo")
	hpl_file = open("HPL.dat")
	output_file = open("output")

	linpack_test_obj = LinpackParser(sysinfo_file, output_file)


def main():
	test_sysinfo()
	test_linpack()


if __name__ == "__main__":
	main()