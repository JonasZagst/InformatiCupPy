class OutputParser:
    @staticmethod
    def parse_output_files(solvers: list, input):
        for solver in solvers:
            output_str = solver.solve(input)
            file = open("../input-output/output-" + solver.get_name() + ".txt", "w+")
            file.write(output_str)
            file.close()
