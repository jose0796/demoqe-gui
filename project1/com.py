

def unframeData(frame,channel=1,digital=0):
    
    if channel == 1:
        if digital == 0:
            return ((frame[0] & 0x3f) << 6 ) | (frame[1] & 0x3f)
        else: 
            return (frame[0] & 0xb0) >> 6
    elif channel == 2:
        if digital == 0:
            return ((frame[2] & 0x3f) << 6 ) | (frame[3] & 0x3f)
        else:
            return (frame[1] & 0xb0) >> 6 


def synchronize(dataSerial):
    
    while(True):
        b = dataSerial.read(1)
        if ((b[0] & 0x8f) >> 7 ) == 0x00:
            garbage = dataSerial.read(3)
            break

def startReceiving(dataSerial):
    frames = dataSerial.read(4)
    if ((frames[0] & 0x8f) >> 7) == 0 and ((frames[1] & 0x8f) >> 7) == 1 and ((frames[2] & 0x8f) >> 7) == 1 and ((frames[3] & 0x8f) >> 7) == 1 : 
        channel1 = unframeData(frames)
        channel2 = unframeData(frames,2)
        return channel1,channel2
    else: 
        synchronize(dataSerial)
        return 0,0


