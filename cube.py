# Author: Edison Murairi
# August 12th, 2023
# Implemente the Cube class

from qiskit import QuantumCircuit , QuantumRegister
from qiskit.circuit.library import MCXGate
import string
class Cube:

    def __init__(self, expression):

        """ instantiate the cube class
          int n: lenght of the cube
          string expression: B3 string
          B3 = {0,1,-}  -> negative, positive and don't care
          """
        
        self.expression = expression
    
    
    def weight(self):

        return sum(self.expression[c] != "-" \
                   for c in range(len(self.expression)))


    def distance(self, other):

        assert len(self.expression) == len(other.expression)

        return sum(self.expression[c] != other.expression[c] \
                    for c in range(len(self.expression)))
    
    def xor_combine(self, other):

        combination_map = {"01":"-", "10":"-", \
                           "0-":"1", "-0":"1", \
                            "1-":"0", "-1":"0"}

        assert len(self.expression) == len(other.expression)
        assert self.distance(other) == 1

        new_expression = ""

        for i in range(len(self.expression)):

            if self.expression[i] != other.expression[i]:

                a = self.expression[i]
                b = other.expression[i]

                try:
                    new_expression += str(combination_map[f"{a}{b}"])
                except:
                    print("Weird in the combination")
                    return

            
            else:
                new_expression += self.expression[i]
        
        return Cube(new_expression)

    def copy(self):
        """ create a new cube with the same data """

        return Cube(self.expression)
    
    def change_literal(self, pos, newlit):

        new_expression = self.expression[:pos] + newlit + self.expression[pos+1:]

        self.expression = new_expression

        return
    
    def expansion(self):

        cubes_list = [self.copy()]
        n = len(self.expression)
        pos = 0

        while pos < n:

            tmp = []

            for cube in cubes_list:

                if cube.expression[pos] == "0":

                    exp1 = cube.expression[:pos] + "-" + cube.expression[pos+1:]
                    exp2 = cube.expression[:pos] + "1" + cube.expression[pos+1:]

                    tmp.append(Cube(exp1))
                    tmp.append(Cube(exp2))
                
                if cube.expression[pos] == "1":


                    exp1 = cube.expression[:pos] + "-" + cube.expression[pos+1:]
                    exp2 = cube.expression[:pos] + "0" + cube.expression[pos+1:]

                    tmp.append(Cube(exp1))
                    tmp.append(Cube(exp2))
                
                if cube.expression[pos] == "-":

                    exp1 = cube.expression[:pos] + "0" + cube.expression[pos+1:]
                    exp2 = cube.expression[:pos] + "1" + cube.expression[pos+1:]

                    tmp.append(Cube(exp1))
                    tmp.append(Cube(exp2))


            cubes_list = tmp
        
            pos += 1
        
        return cubes_list
    
    def toffoli_gate(self, labels = None, anc_label = None):
        """ convert the cube to a multi-controlled not gate also called Tofolli gate 
        """
        if labels is None:
            labels = 'q'
        if anc_label is None:
            anc_label = 'anc'

        qr = QuantumRegister(len(self.expression), labels)
        anc = QuantumRegister(1, anc_label)
        qc = QuantumCircuit(qr, anc)
        

        cares = []
        negatives = []
        for i in range(len(self.expression)):

            if self.expression[i] == "0":
                qc.x(qr[i])
                cares.append(i)
                negatives.append(i)
            
            if self.expression[i] == "1":
                cares.append(i)
        
        gate = MCXGate(len(cares))
        qc.append(gate, cares + [len(self.expression)])
        for neg in negatives:
            qc.x(neg)

        return qc  

    def __str__(self):

        if self.expression == "-"*len(self.expression):
            return "1"

        result = ""
        for i in range(len(self.expression) - 1):

            if self.expression[i] == "0":

                result += "~" + f"x{i} & "
            
            elif self.expression[i] == "1":
                result += f"x{i} & "
        
        i = len(self.expression) - 1
        if self.expression[i] == "0":

            result += "~" + f"x{i}"
        
        elif self.expression[i] == "1":
            result += f"x{i}"
        
        if result == "":
            return result

        if result[-1] == " ":
            result = result[:-1]

        if result[-1] == "&":
            result = result[:-1]
        
        return result