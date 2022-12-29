"""
Project #2: Bloom Filter with multiple hashes using no third party libraries.
Author: Diego Martinez Garcia

"""
import math, sys, csv, array


class BitArray(object):
    """Class for the bit array that will be used."""

    def __init__(self, bitSize, fill=0):
        """
        bitSize : int
            Size of the bit array
        """
        intSize = bitSize >> 5  # number of 32 bit integers
        if bitSize & 31:  # if bitSize != (32 * n) add
            intSize += 1  #    a record for stragglers
        if fill == 1:
            fill = 4294967295  # all bits set
        else:
            fill = 0  # all bits cleared

        bitArray = array.array("I")  # 'I' = unsigned 32-bit integer
        bitArray.extend((fill,) * intSize)
        self.bitarray = bitArray

    def setBit(self, bit_num):
        """
        setBit() returns an integer with the bit at 'bit_num' set to 1.

        bit_num : int
            Position of the bit we want to set to 1
        """

        record = bit_num >> 5
        offset = bit_num & 31
        mask = 1 << offset
        self.bitarray[record] |= mask
        # return(self.bitarray[record])

    def testBit(self, bit_num):
        """
        testBit() returns a nonzero result, 2**offset, if the bit at 'bit_num' is set to 1.

        bit_num : int
            Position of the bit we want to return
        """
        record = bit_num >> 5
        offset = bit_num & 31
        mask = 1 << offset
        return self.bitarray[record] & mask


class BloomFilter(object):
    """
    Class for Bloom filter
    """

    def __init__(self, num_items, false_pos):
        """
        items_count : int
            Number of expected items to be stored in bloom filter
        false_pos : float
            False Positive probability in decimal
        """

        # Size for bit array
        self.size = BloomFilterSize(num_items, false_pos)

        # Number of hash functions to use
        self.hash_count = HashAmount(self.size, num_items)

        # Creation of bitarray with all values equal to cero
        self.bit_array = BitArray(self.size)

    def add_to_filter(self, item):
        """
        Add an item to the filter

        item : str
            Item to be added to the filter
        """

        for i in range(self.hash_count):
            # Creating hash fuction using 'i' as the seed value and saving hash value
            hash_value = hash(str(i) + item) % self.size
            # Turning bit on using hash value
            self.bit_array.setBit(hash_value)

    def in_filter(self, item):
        """
        Check if item is in filter

        item : int
            item to be searhed
        """
        for i in range(self.hash_count):
            # Returning hash value using 'i' as the seed value
            hash_value = hash(str(i) + item) % self.size
            if self.bit_array.testBit(hash_value) != 2 ** (hash_value & 31):
                # If condition is true, the item is not in filter
                return False
        # Else it may be in the filter
        return True


def BloomFilterSize(num_items, false_pos):
    """
    Return the size of the bitarray that we need using this formula:
    size = ceil((num_items * log(false_pos)) / log(1 / pow(2, log(2))))

    num_items : int
        number of items expected to be stored in filter
    false_pos : float
        False Positive probability in decimal
    """

    size = math.ceil(
        (num_items * math.log(false_pos)) / math.log(1 / pow(2, math.log(2)))
    )
    return int(size)


def HashAmount(num_items, size):
    """
    Return the number of hash functions to be used using this formula:
    k = (size/num_items) * lg(2)

    size : int
        size of bit array
    num_items : int
        number of items expected to be stored in filter
    """
    r = num_items / size
    k = math.log(2) * r
    return int(k)


if __name__ == "__main__":
    # False positivity value:
    false_pos = 0.0000001
    num_items = 0

    # Checking if arguments where passed
    if len(sys.argv) > 1:

        # Saving file that was passed through the commandline in a variable
        input_db = sys.argv[1]
        check_db = sys.argv[2]

        # Test case made by me:
        # input_db = "test1.csv"
        # check_db = "test2.csv"

        # Variable that will store the emails found on the csv
        emails = []
        with open(input_db, "r") as csvfile:

            # Creation of file reader
            csvreader = csv.reader(csvfile)

            for row in csvreader:
                # Saving email
                email = row[0]

                # Checking if the row has the heathers/titles
                possible_headers = ["Email", "E-mail", "email", "e-mail"]
                if email in possible_headers:
                    pass

                # Saving email on array
                else:
                    emails.append(email)

        # Ceating the BloomFilter Object
        bloom_filter = BloomFilter(len(emails), false_pos)

        # Adding emails to filter:
        for email in emails:
            bloom_filter.add_to_filter(email)

        with open(check_db, "r") as csvfile2:

            # Creation of second file reader
            csvreader2 = csv.reader(csvfile2)

            for row in csvreader2:
                # Saving email
                email_check = row[0]

                # Checking if the row has the heathers/titles
                possible_headers = ["Email", "E-mail", "email", "e-mail"]
                if email_check in possible_headers:
                    pass

                else:
                    # Printing if email is in the filter
                    if bloom_filter.in_filter(email_check) == True:
                        print(email_check + ",Probably in the DB")
                    else:
                        print(email_check + ",Not in the DB")
