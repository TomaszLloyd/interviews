#!/usr/bin/env python3

from src import KVinterface as KV

class Tests:

    def testSimplePutAndGet(self):
        item = KV.KVInterface()
        item.put('hello', 'lorem ipsum')
        assert item.get('hello') == "lorem ipsum"
        assert item.getNumberOfFreeAddresses() == 1022

    def testDynamicAllocation(self):
        item = KV.KVInterface()
        for i in range(1024):
            item.put(f'hello_{i}', 'there')
        assert item.getNumberOfFreeAddresses() == 0
        item.delete('hello_0')
        assert item.getNumberOfFreeAddresses() == 1
        # this should succeed
        item.put(f'test', 'input')


if __name__ == "__main__":
    tests = Tests()
    tests.testSimplePutAndGet()