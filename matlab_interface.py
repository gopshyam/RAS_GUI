import matlab.engine

EXCEL_FILE = "Demo.xlsx"

class MatlabInterface():
    def __init__(self):
        self.is_ready = False
        self.eng = matlab.engine.start_matlab()

        self.C = self.eng.xlrd(EXCEL_FILE, "C")
        self.X = self.eng.xlrd(EXCEL_FILE, "X")
        self.b = self.eng.xlrd(EXCEL_FILE, "b")
        self.lb = self.eng.xlrd(EXCEL_FILE, "lb")
        self.ub = self.eng.xlrd(EXCEL_FILE, "ub")
        self.H = self.eng.xlrd(EXCEL_FILE, "H")
        self.Aeq = matlab.double([])
        self.beq = matlab.double([])

        self.is_ready = True

    def compute_result(self, tempPG):
        if(not self.is_ready):
            return None

        self.H[1][0] = tempPG[1]/100.0
        self.H[8][1] = tempPG[2]/100.0
        self.H[10][2] = tempPG[3]/100.0
        self.H[0][3] = (tempPG[0]-100)/100.0

        A = self.eng.multiply(self.C, self.X, self.H)

        f = matlab.double([-1 * tempPG[1], -1 * tempPG[2], -1 * tempPG[3], 0]) 

        x = self.eng.linprog(f, A, self.b, self.Aeq, self.beq, self.lb, self.ub)

        return x
