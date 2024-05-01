#!/usr/bin/env python3

class BD:
    def __init__(self, block_length, blocks):
        """I don't recall the implementation here, using this as a placeholder"""
        self.blocks = blocks
        self.block_length = block_length
        self.data = ['*'*block_length for i in range(blocks)]

    def write(self, index, content):
        self.data[index] = content

    def read(self, index):
        return self.data[index]

class KVInterface:
    def __init__(self, bd=None, block_length=8, blocks=1024):
        self.__blocks = blocks
        self.__block_length = block_length
        self.__bd = bd if bd is not None else BD(block_length=self.__block_length, blocks=self.__blocks)

        # keep track of items with a name
        self.__map = {}

        # keep track of a list of the addresses from 0 to 1023
        self.__addresses = [i for i in range(self.__blocks)]

    def getNumberOfFreeAddresses(self):
        """Helper method for testing"""
        return len(self.__addresses)

    def put(self, name, content):
        """Append item at key 'name' if there's room"""
        number_of_blocks = len(content) / self.__block_length if len(content) % self.__block_length == 0 else len(content) // self.__block_length + 1

        # check to ensure we have at least this many blocks available
        if number_of_blocks > len(self.__addresses):
            raise Exception(f"Not enough addresses available, requested: {number_of_blocks}, available: {len(self.__addresses)}")

        new_addresses = []
        for i in range(number_of_blocks):
            # pop N items off our address pool and save them 
            new_addresses.append(self.__addresses.pop())

        for index, value in enumerate(new_addresses):
            # write to the new addresses in the same order, with a block sized portion of the content
            self.__bd.write(value, content[index*self.__block_length:(i+1)*self.__block_length])

        # keep track of the length of the original content and the list of addresses in use
        self.__map[name] = (len(content), new_addresses)

        return content

    def get(self, name):
        """Get item at index if it exists"""
        if name not in self.__map:
            raise ValueError()
        
        string = ""
        length, indices = self.__map[name]

        for index in indices:
            # iterate over the indices we saved
            string += self.__bd.read(index)

        return string[:length]

    def delete(self, name):
        """Check for existence of mapped item and free up memory"""
        if name in self.__map:
            # add addresses back into our pool of available addresses
            _, indices = self.__map[name]
            self.__addresses.extend(indices)
            del self.__map[name]
        return