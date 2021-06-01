import re
import random
import os
import traceback
import importlib
from sgFile import SgFile
from string import punctuation, ascii_lowercase, ascii_uppercase
from entity import Entity

'''
Surrogate Generation
'''
class SurrogateGeneration:
    
    def __init__(self, parameters):
        self.parameters = parameters
        module = importlib.import_module('lang.'+parameters['settings']['lang'])
        self.lang = getattr(module, module.__all__[0])()
        self.nrFiles = 0
    
    # generate random characters
    def genRandomChars(self, tokenTxt):
        surrogate = ''
        for char in tokenTxt:
            if char.isdigit():
                char = str(random.randint(0,9))
            elif char.isalpha():
                if char.islower():
                    char = random.choice(ascii_lowercase)
                else:
                    char = random.choice(ascii_uppercase)
            surrogate += char
        return surrogate  
       
    # substitute entity with random letters and numbers
    def subChar(self, sgFile, token):
        token.setNormCase(token.text.lower())
        if token.normCase in sgFile.sub[token.label]:
            return sgFile.sub[token.label].get(token.text, sgFile.sub[token.label][token.normCase])
        else:
            surrogate = self.genRandomChars(token.text)
            sgFile.sub[token.label][token.text] = surrogate
            sgFile.sub[token.label][token.normCase] = surrogate
            return surrogate  
        
    # substitute EMAIL and URL
    def subUri (self, sgFile, token):
        token.setNormCase(token.text.lower())
        if token.normCase in sgFile.sub[token.label]:
            return sgFile.sub[token.label].get(token.text, sgFile.sub[token.label][token.normCase])
        else:
            diff = len(token.text)-len(re.sub('^(<?ftp:|<?file:|<?mailto:|((<?https?:)?(<?www)?))','',token.text))
            surrogate = token.text[:diff] + self.genRandomChars(token.text[diff:])
            sgFile.sub[token.label][token.text] = surrogate
            sgFile.sub[token.label][token.normCase] = surrogate
            return surrogate                 
    
    
    # get substitute
    def getSubstitute(self, sgFile, token):
        if token.text in punctuation: # punctuation is returned unchanged only special char if not UFID etc...
            return token.text
        elif token.label in ['UFID', 'PHONE', 'ZIP', 'STREETNO', 'PASS', 'USER']:
            return self.subChar(sgFile, token)
        elif token.label in ['URL','EMAIL']:
            return self.subUri(sgFile, token)
        elif token.label == 'DATE':
            return self.lang.getCoSurrogate(sgFile, token) or self.lang.subDate(sgFile, token)
        elif token.label == 'STREET':
            return self.lang.getCoSurrogate(sgFile, token) or self.lang.subStreet(sgFile, token)  
        elif token.label == 'CITY':
            return self.lang.getCoSurrogate(sgFile, token) or self.lang.getSurrogateAbbreviation(sgFile, token.text, token.label, self.lang.city) or self.lang.subCity(sgFile, token)       
        elif token.label == 'FEMALE':
            return self.lang.getCoSurrogate(sgFile, token) or self.lang.getSurrogateAbbreviation(sgFile, token.text, token.label, self.lang.female) or self.lang.subFemale(sgFile, token)
        elif token.label == 'MALE':
            return self.lang.getCoSurrogate(sgFile, token) or self.lang.getSurrogateAbbreviation(sgFile, token.text, token.label, self.lang.male) or self.lang.subMale(sgFile, token)
        elif token.label == 'FAMILY':
            return self.lang.getCoSurrogate(sgFile, token) or self.lang.getSurrogateAbbreviation(sgFile, token.text, token.label, self.lang.family) or self.lang.subFamily(sgFile, token)
        elif token.label == 'ORG':
            return self.lang.getCoSurrogate(sgFile, token) or self.lang.subOrg(sgFile, token)
    
    # substitute privacy-sensitive annotations in file
    def subFile(self, sgFile, annotations):       
        newText = '' 
        begin = 0  
        outputAnn = '' 
        for i, token in enumerate(annotations):   
            sub = self.getSubstitute(sgFile, token) or token.text
            newText+= sgFile.txt[begin:token.start] + sub   
            begin = token.end      
            outputAnn += 'T' + str(i+1) + '\t' + token.label + ' ' + str(len(newText)-len(sub)) + ' ' + str(len(newText)) + '\t' + sub + '\n'
        newText += sgFile.txt[begin:]
        
        fileOutputAnn = os.path.join(self.parameters['settings']['path_output'], os.path.relpath(sgFile.file, self.parameters['settings']['path_input']))
        fileOutputTxt = re.sub('.ann', '.txt', fileOutputAnn)
        os.makedirs(os.path.dirname(fileOutputAnn), exist_ok=True)
        with open(fileOutputTxt, 'w', encoding='utf-8', newline='') as fileOutputTxt:
            fileOutputTxt.write(newText)
        with open(fileOutputAnn, 'w', encoding='utf-8') as fileOutputAnn:
            fileOutputAnn.write(outputAnn.rstrip())
    
    # process files        
    def collectFiles(self, subset, threadName):
        for file in subset:
            print(file)
            try:
                with open(re.sub('.ann$', '.txt', file), 'r', encoding='utf-8', newline='') as fileInputTxt:
                    inputTxt = fileInputTxt.read()
                with open (file, 'r', encoding='utf-8') as fileInputAnn:
                    annos = {}
                    for line in fileInputAnn.readlines():
                        # TODO: handle discontinuous annotations
                        lineSplitted = line.rstrip().split(None, 4)
                        annos[(int(lineSplitted[2]), int(lineSplitted[3]))] = Entity(lineSplitted[4], lineSplitted[1], int(lineSplitted[2]), int(lineSplitted[3]))
                sgFile = SgFile(file, threadName, inputTxt, self.lang.freqMapFemale, self.lang.freqMapMale, self.lang.freqMapFamily, self.lang.freqMapOrg, self.lang.freqMapStreet, self.lang.freqMapCity)
                self.subFile(sgFile, [annos[anno] for anno in sorted(annos)]) 
                self.nrFiles += 1
            except Exception:
                print(file + ' not processed:')
                traceback.print_exc()