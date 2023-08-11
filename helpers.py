# Author: Edison Murairi
# Date: August 12th, 2023
# Build helper functions
#%%
import string
#%%
def ANF_from_alphabetical(nbits, anf_str):
    """ 
    int nbits: The numbe rof bits
    string example from alphabetical form: a & b ^ ~c & d representing the Algebraic Normal Form (ANF)
    return the string in B3 = {0,1,-} form. 
    Example:
    nbits = 4
    input a & b ^ ~c & d
    return 11-- --01
    """

    anf_str =anf_str.replace(" ", "")
    result = ""
    ii = 0
    while ii < len(anf_str):

        tmp = ["-"]*nbits
        parity = "1" # positive 
        while ii < len(anf_str) and anf_str[ii] != "^":
            if anf_str[ii] == "~":
                parity = "0" # negative
            
            elif anf_str[ii] == "&":
                pass
            
            else:
                ch = anf_str[ii]
                indx = string.ascii_lowercase.index(ch)
                if indx >= nbits:
                    print("We assume that the variables are chosen in order from the alphabet")
                    return
                tmp[indx] = parity
                parity = "1"
            
            ii += 1
        
        result += "".join(tmp) + " "

        ii += 1
    
    if result[-1] == " ":
        result = result[:-1]
    
    return result
