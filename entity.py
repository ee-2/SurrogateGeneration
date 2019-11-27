'''
Entity properties
'''
class Entity:
    
    def __init__(self, text, label, start, end):
        self.text = text
        self.label = label
        self.start = start
        self.end = end
    
    # set case normalized token 
    def setNormCase(self, tokenNormCase):
        self.normCase = tokenNormCase