"""
RTP Packet Handler
Implements RTP packet encoding and decoding according to RFC 3550
"""

import sys
from time import time

HEADER_SIZE = 12


class RtpPacket:
    """
    RTP Packet structure:
    
    0                   1                   2                   3
    0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1 2 3 4 5 6 7 8 9 0 1
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |V=2|P|X|  CC   |M|     PT      |       sequence number         |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |                           timestamp                           |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    |           synchronization source (SSRC) identifier            |
    +=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+=+
    |                            payload                            |
    +-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+
    """
    
    header = bytearray(HEADER_SIZE)
    
    def __init__(self):
        self.version = 2
        self.padding = 0
        self.extension = 0
        self.cc = 0
        self.marker = 0
        self.pt = 26  # MJPEG type
        self.seqNum = 0
        self.timestamp = 0
        self.ssrc = 0
        self.payload = b''
    
    def encode(self):
        """Encode the RTP packet with header and payload"""
        # Set the first byte: V(2 bits), P(1 bit), X(1 bit), CC(4 bits)
        self.header[0] = (self.version << 6) | (self.padding << 5) | \
                         (self.extension << 4) | self.cc
        
        # Set the second byte: M(1 bit), PT(7 bits)
        self.header[1] = (self.marker << 7) | self.pt
        
        # Set sequence number (bytes 2-3)
        self.header[2] = (self.seqNum >> 8) & 0xFF
        self.header[3] = self.seqNum & 0xFF
        
        # Set timestamp (bytes 4-7)
        self.header[4] = (self.timestamp >> 24) & 0xFF
        self.header[5] = (self.timestamp >> 16) & 0xFF
        self.header[6] = (self.timestamp >> 8) & 0xFF
        self.header[7] = self.timestamp & 0xFF
        
        # Set SSRC (bytes 8-11)
        self.header[8] = (self.ssrc >> 24) & 0xFF
        self.header[9] = (self.ssrc >> 16) & 0xFF
        self.header[10] = (self.ssrc >> 8) & 0xFF
        self.header[11] = self.ssrc & 0xFF
        
        # Concatenate header and payload
        return bytes(self.header) + self.payload
    
    def decode(self, byteStream):
        """Decode the RTP packet from byte stream"""
        try:
            self.header = bytearray(byteStream[:HEADER_SIZE])
            
            # Parse the first byte
            self.version = (self.header[0] >> 6) & 0x03
            self.padding = (self.header[0] >> 5) & 0x01
            self.extension = (self.header[0] >> 4) & 0x01
            self.cc = self.header[0] & 0x0F
            
            # Parse the second byte
            self.marker = (self.header[1] >> 7) & 0x01
            self.pt = self.header[1] & 0x7F
            
            # Parse sequence number
            self.seqNum = (self.header[2] << 8) | self.header[3]
            
            # Parse timestamp
            self.timestamp = (self.header[4] << 24) | (self.header[5] << 16) | \
                           (self.header[6] << 8) | self.header[7]
            
            # Parse SSRC
            self.ssrc = (self.header[8] << 24) | (self.header[9] << 16) | \
                       (self.header[10] << 8) | self.header[11]
            
            # Extract payload
            self.payload = byteStream[HEADER_SIZE:]
            
        except Exception as e:
            print(f"Error decoding RTP packet: {e}")
            raise
    
    def getPayload(self):
        """Return the payload"""
        return self.payload
    
    def getSeqNum(self):
        """Return the sequence number"""
        return self.seqNum
    
    def getTimestamp(self):
        """Return the timestamp"""
        return self.timestamp
    
    def getPayloadType(self):
        """Return the payload type"""
        return self.pt
    
    def getVersion(self):
        """Return the RTP version"""
        return self.version
    
    def setPayload(self, payload):
        """Set the payload"""
        self.payload = payload
    
    def setSeqNum(self, seqNum):
        """Set the sequence number"""
        self.seqNum = seqNum
    
    def setTimestamp(self, timestamp):
        """Set the timestamp"""
        self.timestamp = int(timestamp)
    
    def setPayloadType(self, pt):
        """Set the payload type"""
        self.pt = pt
    
    def setMarker(self, marker):
        """Set the marker bit"""
        self.marker = marker
    
    def setSSRC(self, ssrc):
        """Set the SSRC"""
        self.ssrc = ssrc
