#author: Zhiyuan Lin

from pprint import pprint

def fromStringToBits(s):
    result = ''
    for c in s:
        bits = bin(ord(c))[2:]
        bits = '00000000'[len(bits):] + bits
        result = result + bits
    return result

def fromBitsToString(bits, lengthInByte=0):
    # make sure the output string is of correct length
    if (len(bits) < lengthInByte * 8):
        bits = str('0' * (lengthInByte * 8 - len(bits))) + bits
    else:
        if (lengthInByte != 0 and len(bits) > lengthInByte * 8):
            bits = bits[-lengthInByte * 8:]

    chars = []
    for b in range(len(bits) / 8):
        byte = bits[b*8:(b+1)*8]
        chars.append(chr(int(''.join([str(bit) for bit in byte]), 2)))

    return ''.join(chars)


def stringToRtpPacketDict(packetString):
    rtpPacketDict = {}
    try:
        bitString = fromStringToBits(packetString);
        rtpPacketDict["sourcePort"] = int(bitString[0:16], 2)
        rtpPacketDict["destPort"] = int(bitString[16:32], 2)
        rtpPacketDict["seqNum"] = int(bitString[32:64], 2)
        rtpPacketDict["ackNum"] = int(bitString[64:96], 2)
        rtpPacketDict["extraHeaderLen"] = int(bitString[96:100], 2)
        rtpPacketDict["ack"] = int(bitString[100:101], 2)
        rtpPacketDict["rst"] = int(bitString[101:102], 2)
        rtpPacketDict["syn"] = int(bitString[102:103], 2)
        rtpPacketDict["fin"] = int(bitString[103:104], 2)
        rtpPacketDict["receiveWindowSize"] = int(bitString[104:128], 2)
        rtpPacketDict["checksum"] = int(bitString[128:160], 2)
        if (rtpPacketDict["extraHeaderLen"] != 0):
            rtpPacketDict["option"] = int(bitString[160: (160 + rtpPacketDict["extraHeaderLen"]*32)], 2)
            rtpPacketDict["data"] = packetString[20 + rtpPacketDict["extraHeaderLen"] * 4:]
        else:
            rtpPacketDict["option"] = 0
            rtpPacketDict["data"] = packetString[20:]
    except:
        print "Unexpected error in stringToRtpPacketDict!"
        raise

    return rtpPacketDict

def rtpPacketDictToString(rtpPacketDict):
    rtpString = ""
    try:
        if "sourcePort" not in rtpPacketDict:
            rtpPacketDict["sourcePort"] = 0
        rtpString += fromBitsToString(str(bin(rtpPacketDict["sourcePort"]))[2:], 2)

        if "destPort" not in rtpPacketDict:
            rtpPacketDict["destPort"] = 0
        rtpString += fromBitsToString(str(bin(rtpPacketDict["destPort"]))[2:], 2)

        if "seqNum" not in rtpPacketDict:
            rtpPacketDict["seqNum"] = 0
        rtpString += fromBitsToString(str(bin(rtpPacketDict["seqNum"]))[2:], 4)

        if "ackNum" not in rtpPacketDict:
            rtpPacketDict["ackNum"] = 0
        rtpString += fromBitsToString(str(bin(rtpPacketDict["ackNum"]))[2:], 4)

        if "extraHeaderLen" not in rtpPacketDict:
            rtpPacketDict["extraHeaderLen"] = 0
        if "ack" not in rtpPacketDict:
            rtpPacketDict["ack"] = 0
        if "rst" not in rtpPacketDict:
            rtpPacketDict["rst"] = 0
        if "syn" not in rtpPacketDict:
            rtpPacketDict["syn"] = 0
        if "fin" not in rtpPacketDict:
            rtpPacketDict["fin"] = 0
        rtpString += fromBitsToString(str(bin(rtpPacketDict["extraHeaderLen"]))[2:] + str(bin(rtpPacketDict["ack"]))[2:] + str(bin(rtpPacketDict["rst"]))[2:] + str(bin(rtpPacketDict["syn"]))[2:] + str(bin(rtpPacketDict["fin"]))[2:], 1)
        
        if "receiveWindowSize" not in rtpPacketDict:
            rtpPacketDict["receiveWindowSize"] = 0
        rtpString += fromBitsToString(str(bin(rtpPacketDict["receiveWindowSize"]))[2:], 3)

        if "checksum" not in rtpPacketDict:
            rtpPacketDict["checksum"] = 0        
        rtpString += fromBitsToString(str(bin(rtpPacketDict["checksum"]))[2:], 4)
    
        if (rtpPacketDict["extraHeaderLen"] != 0):
            rtpString += fromBitsToString(str(bin(rtpPacketDict["option"]))[2:], rtpPacketDict["extraHeaderLen"] * 4)
        if "data" in rtpPacketDict:
            rtpString += rtpPacketDict["data"]
    except:
        print "Unexpected error in rtpPacketDictToString!"
        raise
        
    return rtpString

def updatePacketStringChecksum(packetString):
    checksumString = fromBitsToString(str(bin(bsdChecksum(packetString)))[2:], 4)
    return packetString[:16] + checksumString + packetString[20:]


def bsdChecksum(packetString):
    # remove checksum line
    packetString = packetString[:16] + packetString[20:]
    checksum = 0
    for ch in packetString:
        checksum = (checksum >> 1) + ((checksum & 1) << 31)
        checksum += ord(ch)
        checksum &= 0xffffffff
    return checksum





