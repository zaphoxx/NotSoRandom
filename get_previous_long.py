#!/usr/bin/python
import notSoRandom
import struct
###############################################################################
# Example: calculate the previous random long number from a given long number #
# tokenId=0xec50a42755fea645 #64 bit value                                    #
###############################################################################
print("-"*80)
print("Example calculates based of provided long rnd number the seed,\n \
the next 5 long rnd numbers and the previous long rnd number.")
print("-"*80)
# known random number (64bit long value)
current = 0xec50a42755fea645
print("[+] current known long value : %s"% current)
nsr=notSoRandom.NotSoRandom()
print("[+] create a new 'NotSoRandom' object.")

# upper int is calculated first and lower int calculated last when generating a long rnd
# so the order of the two is crucial for the calculations to work properly
print("[+] get lower and upper int values from current long.")
(upper,lower)=nsr.getIntValuesFromLong(current)
print("[+] lower int : %s\n[+] upper int : %s"% (lower,upper))

# try to find the original seed. You can also use .findSeed(i1,i2,32) instead
print("[+] try to retrieve seed value from int values.")
seed=nsr.findSeedForInt(upper,lower)

# set seed to found value
nsr.setSeed(seed)

# calculate the next 5 long values:
for i in range(0,5):
    print("[+] round %d : rnd value in hex : %s"%(i+1,nsr.nextLong()))
    
# set seed back to found value
nsr.setSeed(seed)
# calculate the previous long value:
print("[+] calculate long rnd previous to current value : %d"% current)
print("[+] previous rnd long in hex : %s"% nsr.previousLong())
