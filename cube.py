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

        result = ""
        for i in range(len(self.expression)):

            if self.expression[i] == "0":

                result += "~" + string.ascii_lowercase[i] 
            
            if self.expression[i] == "1":

                result += f"{string.ascii_lowercase[i]}"
        
        return result