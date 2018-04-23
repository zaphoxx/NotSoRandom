#!/usr/bin/python
import struct
import sys
from struct import pack,unpack,calcsize

class NotSoRandom():
    '''
    NotSoRandom() can find the seed for two sequentially calculated int rnd values or one rnd long value.
    These values need to be provided by the java.util.Random module.
    NotSoRandom can then find the original seed and calculate the next() rnd values or previous() rnd values.
    See the original java.util.Random documentation for further details.
    from https://docs.oracle.com/javase/7/docs/api/java/util/Random.html:
    An instance of this class is used to generate a stream of pseudorandom numbers. 
    The class uses a 48-bit seed, which is modified using a linear congruential formula. 
    (See Donald Knuth, The Art of Computer Programming, Volume 2, Section 3.2.1.)
    '''
    # constant values MULT and ADDEND and Modulo/Mask from wikipedia https://en.wikipedia.org/wiki/Linear_congruential_generator
    MULT=0x5DEECE66D
    INV_MULT=246154705703781 # modular multiplicative inverse calculated from https://planetcalc.com/3311/
    ADDEND=0xB
    MASK=(1<<48)-1 # aka 0xFFFFFFFFFFFF (2^48-1)
    # MASK only assures that values returned from next are 48 bit long (according to java.util.Random)
    
    def __init__(self,seed=None):
        self.seed=seed
        # set a basic initial seed if nothing is provided on class definition - warn user !
        if self.seed==None:
            self.setJavaSeed(0)
            print("[warning] seed not defined by user! used setSeed() to define user specific seed values. (default = 0)")
        
    # setSeed as defined in oracle java java.util.random
    def setJavaSeed(self,seed):
        self.seed=(seed ^ self.MULT) & self.MASK
        
    def setSeed(self,seed):
        if seed != None:
            self.seed=seed #self.slong(seed) >> 16
        else:
            print("[-] could not assign seed! seed=%s."% seed)
    '''	
        next() returns next pseudorandom number based on parameter seed or based on self.seed
        returns a 48bit value
        # if int is required you need to shiftright the output by 16bit 
    '''    
    def next(self,seed=None):
        if seed != None:
            self.seed=seed
        elif self.seed == None:
            print("[-] seed not defined")
            return None
            
        self.seed=((self.seed * self.MULT) + self.ADDEND & self.MASK)
        return self.seed
        
    def nextInt(self,seed=None):
        return self.sint(self.next(seed) >> 16) 
            
    
    def nextLong(self,seed=None):
        if seed != None:
            self.setSeed(seed)
        uppernext=self.nextInt()
        lowernext=self.nextInt()
        
        return self.slong(self.slong(self.sint(uppernext) << 32) + lowernext)
        
    '''
        getSeed() returns self.seed value
    '''
    def getSeed(self):
        return self.seed

    '''
        getIntValuesFromLong()
        returns a tuple containing the two int (32bit) values from which the long value (64bit) was derived from
    '''
    def getIntValuesFromLong(self,value):
        r1=self.signedInt(value>>32)
        r2=self.signedInt(value & (2**32-1))
        return (r1,r2)
    
    '''
        findSeed()
        tries to find original seed for two given prn <=48bit size
        no check is made on r1 or r2, so you need to make sure these are <=48 bit values
        values r1,r2 must have been calculated in given sequence
    '''    
    def findSeed(self,r1,r2,bits=None):
        seed=0
        if bits==None:
            bits=48
            #seed=self.previous(r1)
    
        shift=2**(48-bits) # 2^16
        #seed=r1*shift
        for i in range(0,shift):
            # original seed is 48 bits
            # so left shift r1 shift and loop through all possible values 0 .. shift
            seed=(r1 * shift) + i 
            # transform unsigned/signed for compatibility
            # first try to fit it into 32bit, if that fails
            # try to fit it into 64bit
            # compare the result to the second value, if match, then seed has been found
            try:
                if self.signedInt(self.next(seed)>>(48-bits))==r2:
                    break
                else:
                    seed=None
            except:
                try:
                    if self.signedLong(self.next(seed)>>(48-bits))==r2:
                        break
                    else:
                        seed=None
                except:
                    print("[-] error in findSeed - self.signedLong()!!!")
                    #sys.exit(0)
                    seed=None
                    
        if seed!=None:        
            print("[+] Found Seed: {}".format(seed))
        else:
            print("[-] Could not determine Seed.")
        return seed
    
    # find seed providing int values
    def findSeedForInt(self,r1,r2):
        return self.findSeed(r1,r2,32)
        
    '''
        calculates the previous 48 bit prn for a prn >=48 bit
        for 32 bit prns you will need to retrieve the original seed before you can use previous
        due to the 16bit right shift for these.
    '''
    def previous(self):
        self.seed=self.signedLong((((self.signedLong(self.seed) - self.ADDEND)) * self.INV_MULT) & self.MASK)
        return self.seed
    
    '''
        calculate previous Long value. Long value consists of two 32bit random values calculated in sequence.
        see also snippet from https://docs.oracle.com/javase/7/docs/api/java/util/Random.html below
    '''
    def previousLong(self):
        lowerprevious=self.previous()
        lowerInt=self.signedInt(lowerprevious>>16)
        upperprevious=self.previous()
        previousLong=self.signedLong(self.signedLong(self.signedInt(upperprevious>>16)<<32)+lowerInt)
        return previousLong

    # definitions to transform unsigned to signed values for int 4byte values and long (Q,q in python for 8 byte) 8 byte values        
    def signedInt(self,value):
        import struct
        try:
            return struct.unpack("i",struct.pack("I",value))[0]
        except:
            try:
                return struct.unpack("i",struct.pack("i",value))[0]
            except:
                print("[-] Error in signedInt()!")
                return value
                
    def signedLong(self,value):
        import struct
        try:
            return struct.unpack("q",struct.pack("Q",value))[0]
        except:
            try:
                return struct.unpack("q",struct.pack("q",value))[0]
            except:
                print("[-] Error in signedLong()!")
                return value
        
    def slong(self,value):
        return self.signedLong(value)
    def sint(self,value):
        return self.signedInt(value)
    
if __name__=="__main__":
    main()


