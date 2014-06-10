'''
Created on Jun 9, 2014

@author: nectarios
'''

BLOCKS_NUM = 3
BITS_NUM = 5
SUPER_BLOCK___size = 3

class Note(object):
    '''
    classdocs
    '''
    
    def __init__(self, data=None, parent=None, from_left_parent=None):
        '''
        Constructor
        '''
        if data == None:
            print "Please give correct parameters"
            return
        self.full_data = data
        self.data = list(set(data))
        self.data.sort(cmp=None, key=None, reverse=False)
        self.bits_data = []
        self.bits_full_data = []
        self.childern = []
        self.parent = parent
        self.from_left_parent = from_left_parent
        self.rs = []
        self.rb = []
        self.__decode_data()
        self.__create_RRR()
        if self.__size() == 1:
            return
        self.__gen_tree()
    
    def get_rank_query(self,position=None, letter=None):
        if self.__full_size() < position:
            return -1
        bit = self.__get_bit(letter)
        position___size = self.__get_rank(position, bit)
        if self.__size() == 2:
            return position___size
        if bit:
            return self.childern[1].get_rank_query(position___size,letter)
        return self.childern[0].get_rank_query(position___size,letter)
    
    def get_select_query(self,position=None, letter=None):
        leaf = self.__get_leaf(letter)
        return leaf.__get_select(position,leaf.bits_data[leaf.data.index(letter)])

    def get_track_symbol(self,position=None):
        if self.__size() == 2:
            return self.full_data[position-1]
        if self.__full_size() < position:
            return -1
        bit = self.bits_full_data[position-1]
        position_size = self.__get_rank(position, bit)
        
        if bit:
            return self.childern[1].get_track_symbol(position_size)
        return self.childern[0].get_track_symbol(position_size)

#######################################################################
###########################Private Functions###########################
#######################################################################

    def __get_select(self,position=None,bit=None):
        curent_position = self.__find_position(position, bit)
        if self.parent == None:
            return curent_position
        if self.from_left_parent:
            return self.parent.__get_select(curent_position, False)
        return self.parent.__get_select(curent_position, True)
    #ToDo optimize 
    def __find_position(self,position=None, bit=None):
        position_size = 0
        curent_position = self.__get_rank(position, bit)
        for d in self.bits_full_data[position : self.__full_size()]:
            if d == bit:
                position_size += 1
            if position_size == position:
                return curent_position
            curent_position += 1
        return -1
    
    def __get_rank(self, position=None, bit=None):
        if position==None or bit==None:
            print "Please give correct parameters"
            return -1
        rs_position = position/(BLOCKS_NUM*BITS_NUM)

        rb_position = position/BITS_NUM

        rank = self.rs[rs_position]
        if (((position % (BLOCKS_NUM*BITS_NUM)) != 0) and (((rs_position*BLOCKS_NUM) != rb_position) or (rs_position == 0)) ):
            rank += self.rb[rb_position]
        
        last_position = (BITS_NUM*rb_position)
        while (last_position < position):
            value = self.bits_full_data[last_position]
            if value: 
                rank += 1
            last_position += 1
        
        if bit:
            return rank
        return position - rank

    def __get_leaf(self,letter):
        index = self.data.index(letter)
        if self.__size() == 2:
            return self
        value = self.bits_data[index]
        if value:
            return self.childern[1].__get_leaf(letter)
        return self.childern[0].__get_leaf(letter)
    
    def __gen_tree(self):
        left = []
        right = []
        index = 0
        for data in self.bits_full_data:
            if data:
                right.append(self.full_data[index])
            else:
                left.append(self.full_data[index])
            index += 1
        self.__add_child(Note(left, self, True))
        self.__add_child(Note(right, self, False))
    
    def __decode_data(self):
        while len(self.bits_data) != self.__size():
            if len(self.bits_data) < self.__size() /2:
                self.bits_data.append(False)
            else:
                self.bits_data.append(True)
        self.__set_bits()
    
    def __set_bits(self):
        for d in self.full_data:
            index = self.data.index(d)
            bit = self.bits_data[index]
            self.bits_full_data.append(bit)

    def __add_child(self,obj):
        self.childern.append(obj)
    
    def __size(self):
        return len(self.data)
    
    def __full_size(self):
        return len(self.full_data)
    
    def __get_bit(self,letter=None):
        if letter == None:
            return letter
        for data in self.data:
            if letter==data:
                return self.bits_data[self.data.index(data)]
        return None
        
    def __create_RRR(self):
        counter = 0
        num_of_super_block = 0;
        num_of_block = 0;
        rs_counter = 0
        rb_counter = 0
        self.rb.append(rb_counter)
        for data in self.bits_full_data:
            if ((counter % BITS_NUM) == 0) and (counter != 0):
                self.rb.append(rb_counter)
                num_of_block += 1
                            
            if (counter % (BLOCKS_NUM * BITS_NUM) == 0):
                self.rs.append(rs_counter)
                num_of_super_block += 1
                rb_counter = 0
                
            if data:
                rs_counter += 1
                rb_counter += 1
            counter += 1
        self.rb.append(rb_counter)
        while (num_of_super_block < SUPER_BLOCK___size + 1):
            self.rs.append(rs_counter)
            num_of_super_block += 1
                        
#######################################################################
###########################Private Functions###########################
#######################################################################