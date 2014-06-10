'''
Created on Jun 9, 2014

@author: nectarios
'''

from Note import Note

class WaveletTree(object):
    
    def __init__(self, data=None):
        if data == None:
            print "Please give correct parameters"            
            return
        self.root = Note(data)
        
    def rank_query(self,letter=None, position=None):
        if letter==None or position==None or position <= 0:
            print "Please give correct parameters"
            return -1
        return self.root.get_rank_query(position,letter)
    
    def select_query(self,letter=None, position=None):
        if letter==None or position==None or position <= 0:
            print "Please give correct parameters"
            return -1
        return self.root.get_select_query(position, letter)
    
    def track_symbol(self,position=None):
        if position==None or position <= 0:
            print "Please give correct parameters"
            return -1
        return self.root.get_track_symbol(position)
        