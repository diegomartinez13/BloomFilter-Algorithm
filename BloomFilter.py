"""
Project #2: Bloom Filter with multiple hashes.
Author: Diego Martinez Garcia

Pip installs: mmh3 & bitarray
"""
import mmh3, math, sys, csv
from bitarray import bitarray

class BloomFilter(object):
    '''
    Class for Bloom filter, using murmur3 hash function
    '''

    def __init__(self, num_items:int, false_pos:int):
        '''
        items_count : int
            Number of expected items to be stored in bloom filter
        false_pos : float
            False Positive probability in decimal
        '''
        
        # Size for bit array
        self.size = BloomFilterSize(num_items, false_pos)
        
        # Number of hash functions to use
        self.hash_count = HashAmount(self.size, num_items)
        
        # Creation of bitarray with all values equal to cero
        self.bit_array = bitarray(self.size)
        self.bit_array.setall(0)

    def add_to_filter(self, item:str):
        '''
        Add an item to the filter
        
        item : str
            Item to be added to the filter
        '''
        # Saving bits that will be turned on the bitarray.
        bits_pos = []
        
        for i in range(self.hash_count):
            #Creating hash fuction using 'i' as the seed value and saving hash value
            hash_value = mmh3.hash(item, i) % self.size
            bits_pos.append(hash_value)
            
            # Turning bit on using hash value
            self.bit_array[hash_value] = True

    def in_filter(self, item:str):
        '''
        Check if item is in filter
        
        item : int
            item to be searhed
        '''
        for i in range(self.hash_count):
            hash_value = mmh3.hash(item, i) % self.size
            if self.bit_array[hash_value] == False:
                # If condition is true, the item is not in filter
                return False
        #Else it may be in the filter
        return True


def BloomFilterSize(num_items:int, false_pos:int):
    '''
    Return the size of bit array to used using
    this formula:
    size = ceil((num_items * log(false_pos)) / log(1 / pow(2, log(2))))
    
    num_items : int
        number of items expected to be stored in filter
    false_pos : float
        False Positive probability in decimal
    '''
    
    size = math.ceil((num_items * math.log(false_pos)) / math.log(1 / pow(2, math.log(2))))
    return int(size)

def HashAmount(num_items: int, size: int):
    '''
    Return the hash function to be used using
    this formula:
    k = (size/num_items) * lg(2)
    
    size : int
        size of bit array
    num_items : int
        number of items expected to be stored in filter
    '''
    r = num_items / size
    k = math.log(2) * r
    return int(k)
    

if __name__ == "__main__":    
    #False positivity value:
    false_pos = 0.0000001
    num_items = 0
    
    #Checking if arguments where passed
    if len(sys.argv) > 1:
        
        #Saving file that was passed through the commandline in a variable
        input_db = sys.argv[1]
        check_db = sys.argv[2]
        
        # Test case made by me:
        input_db_test = "test1.csv" 
        check_db_test = "test2.csv"
        
        #Variable that will store the emails found on the csv
        emails = []
        with open(input_db, 'r') as csvfile:
            
            #Creation of file reader 
            csvreader = csv.reader(csvfile)
            
            for row in csvreader:
                #Saving email 
                email = row[0]
                
                #Checking if the row has the heathers/titles
                if email == "Email":
                    pass
                
                #Saving email on array
                else:
                    emails.append(email)
        
        #Ceating the BloomFilter Object
        bloom_filter = BloomFilter(len(emails), false_pos)
        
        #Adding emails to filter:
        for email in emails:
            bloom_filter.add_to_filter(email)
        
        
        with open(check_db, 'r') as csvfile2:
            
            #Creation of second file reader 
            csvreader2 = csv.reader(csvfile2)
            
            for row in csvreader2:
                #Saving email 
                email_check = row[0]
                
                #Checking if the row has the heathers/titles
                if email_check == "Email": pass
                
                #Printing if email is in the filter
                else:
                    if bloom_filter.in_filter(email_check) == True:
                        print(f"{email_check},Probably in the DB")
                    else:
                        print(f"{email_check},Not in the DB")
