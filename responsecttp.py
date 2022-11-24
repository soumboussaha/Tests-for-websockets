import requests
import random

def Taintgenerator(intervals,encoding_type):
    if encoding_type == "x-taint-detailed":
        pass
    elif encoding_type == "x-taint-bin" :
        result=""
        for x in intervals:
            result=result+str(encode_unsigned_leb128(x[0]))
            result=result+str(encode_unsigned_leb128(x[1]))
    else :
        print ('wrong Taint type - application stopped')
    return str(result).replace("b\'","").replace("\'","")

def DataGenerator(Lengthofpacket):
    Data=""
    Taintintervals =[]
    last="X"
    for i in range(Lengthofpacket):

        if random.randint(0, 1) == 0 :
            if last == "X":
                Taintintervals.append([i+1,1])
                #Taintintervals[len(Taintintervals)-1]
            else:
                Taintintervals[len(Taintintervals)-1]=[Taintintervals[len(Taintintervals)-1][0],i-Taintintervals[len(Taintintervals)-1][0]+2]

            Data=Data+"S"
            last="S"
        else:
            Data=Data+"X"
            last="X"   
    return Data , Taintintervals
            
def encode_unsigned_leb128(number):
    result = bytearray()

    # While number is greater than a byte
    while number.bit_length() > 7:
        # Get first 7 bits and append 1 on 8th bit
        single_byte = (number & 0b01111111) | 0b10000000
        # Append the byte to result
        result.append(single_byte)
        # Truncate right 7 bits
        number = number >> 7

    # Append remaining byte to result
    result.append(number)

    # As we appended earlier no need to reverse the bytes
    return bytes(result)

def decode_unsigned_leb128(byte_array, offset=0):
    needle = offset
    pair_count = 0
    result = 0

    while True:
        single_byte = byte_array[needle]

        # If first bit is 1
        if single_byte & 0b10000000 == 0:
            break

        # Remove first bit
        single_byte = single_byte & 0b01111111

        # Push number of bits we already have calculated
        single_byte = single_byte << (pair_count * 7)

        # Merge byte with result
        result = result | single_byte

        needle = needle + 1
        pair_count = pair_count + 1

    # Merge last byte with result
    single_byte = single_byte << (pair_count * 7)
    result = result | single_byteq

    return result

data,inters = DataGenerator(20000)

print (data)
print (inters)

url = 'http://localhost:8081'
headers = {'Request-Taint': '1'} # if you put it 0 your turn off the CTTP support 
body = {'data':data}

proxy_servers = {
   'http': 'http://localhost:8080',
}
   
taintspec=open('test.txt','w') 

taint=Taintgenerator(inters,"x-taint-bin")
print (taint)
taintspec.write("application/x-taint-bin"+taint)
taintspec.close()
files = {'Content-Type': open('test.txt', 'rb')}

r=requests.get(url, headers=headers, data=body ,proxies=proxy_servers , files=files)
print(r)
