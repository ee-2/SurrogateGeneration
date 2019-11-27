import random
from collections import defaultdict
from string import ascii_uppercase

'''
Properties of each file
'''
class SgFile:
    # initialize letter to letter mappings and date shift separately for each file
    def __init__(self, file, threadName, txt, freqMapFemale, freqMapMale, freqMapFamily, freqMapOrg, freqMapStreet, freqMapCity):
        self.file = file
        self.threadName = threadName
        self.txt = txt
        self.doc = None
        self.firstLetterMaps = self.getFirstLetterMap(freqMapFemale, freqMapMale, freqMapFamily, freqMapOrg, freqMapStreet, freqMapCity) 
        self.dateShift = random.randint(-365,365) # 1 year forward/backward 
        self.sub = defaultdict(dict)    
    
    # get mapping for a character, if not in mapping get random first letter substitution provided that entries starting with that character exist in the lexicon
    def getMapForChar(self, label, char, lex):
        origCharSub = self.firstLetterMaps[label].get(char)
        if origCharSub and origCharSub in lex:
            return origCharSub
        while True: 
            subChar = random.choice(ascii_uppercase)
            if subChar in lex:
                break            
        self.firstLetterMaps[label][char] = subChar
        return subChar
        
    # generate random capital mappings
    def genRandomFirstLetterMappings(self, freqMap):
        firstLetterMap = {}
        for chars, mapping in freqMap:
            random.shuffle(mapping)
            firstLetterMap.update(dict(zip(chars, mapping)))
        return firstLetterMap
    
    # get capital mappings
    def getFirstLetterMap(self, freqMapFemale, freqMapMale, freqMapFamily, freqMapOrg, freqMapStreet, freqMapCity):
        return {'FEMALE':self.genRandomFirstLetterMappings(freqMapFemale),
                'MALE':self.genRandomFirstLetterMappings(freqMapMale),
                'FAMILY':self.genRandomFirstLetterMappings(freqMapFamily),
                'ORG':self.genRandomFirstLetterMappings(freqMapOrg),
                'STREET':self.genRandomFirstLetterMappings(freqMapStreet),
                'CITY':self.genRandomFirstLetterMappings(freqMapCity)}
        
    
    # add different spellings of name, for organizations original spelling of substitution is kept
    def addSpellings(self, token, newToken, normToken, normNewToken, label):
        if label == 'ORG':
            for spelling, newSpelling in zip([token, token.lower(), token.upper(), normToken],[newToken, newToken, newToken, newToken]): 
                self.sub[label][spelling] = newSpelling   
        else:          
            for spelling, newSpelling in zip([token, token.lower(), token.upper(), normToken],[newToken, newToken.lower(), newToken.upper(), normNewToken]): 
                self.sub[label][spelling] = newSpelling