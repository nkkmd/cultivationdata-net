# NOSTR NIP-19 Entity Converter

## 1. Overview
This is a Python script for handling Bech32-encoded NOSTR entities in compliance with the [NIP-19 specification](https://github.com/nostr-protocol/nips/blob/master/19.md). It enables encoding and decoding of various identifiers (such as public keys, secret keys, and event IDs) used in the NOSTR protocol.

## 2. Key Features
1. Bech32 format encoding/decoding
2. TLV (Type-Length-Value) data parsing
3. Conversion of various NOSTR entities

## 3. Supported Entity Types
| Prefix | Description | Data Structure |
|--------|-------------|----------------|
| npub | Public Key | 32-byte hexadecimal string |
| nsec | Secret Key | 32-byte hexadecimal string |
| note | Note ID | 32-byte hexadecimal string |
| nevent | Event Information | Includes TLV format metadata |
| nprofile | Profile Information | Includes TLV format metadata |

## 4. Data Class Structures

### TLV
```python
@dataclass
class TLV:
    type: int      # 1 byte indicating data type
    length: int    # 1 byte indicating value length
    value: bytes   # Actual data
```

### Classes for Storing Decoded Results
Dedicated data classes are provided for each entity type:
- `DecodedNote`: Stores note ID
- `DecodedPubkey`: Stores public key
- `DecodedSeckey`: Stores secret key
- `DecodedEvent`: Stores event information and metadata
- `DecodedProfile`: Stores profile information and relay information

## 5. TLV Type Definitions
The following TLV types are defined in NIP-19:

| Type Value | Description | Usage |
|------------|-------------|--------|
| 0 | special | Primary data for each entity (pubkey/event id etc.) |
| 1 | relay | Relay server URL |
| 2 | author | Author's public key |
| 3 | kind | Event type |

## 6. Core Methods Explanation

### decode_bech32
```python
@staticmethod
def decode_bech32(bech32_str: str) -> Tuple[str, bytes]
```
Decodes a Bech32 format string and returns the HRP (Human Readable Part) and data portion.

### encode_bech32
```python
@staticmethod
def encode_bech32(hrp: str, data: bytes) -> str
```
Encodes data into a Bech32 format string.

### parse_tlv
```python
@staticmethod
def parse_tlv(data: bytes) -> List[TLV]
```
Parses TLV format data from binary data and returns a list of TLV objects.

### decode
```python
@staticmethod
def decode(bech32_str: str) -> Tuple[str, any]
```
Fully decodes a Bech32-encoded string and returns a tuple of (type, decoded_data).

### hex_to_bech32
```python
@staticmethod
def hex_to_bech32(hex_str: str, type: str) -> str
```
Converts a hexadecimal format string to Bech32 format.

## 7. Usage Examples

### Decoding an Event ID
```python
nevent = "nevent1qqs8l95us0smltxjryemq0wxtd9tegwnyy6r7jcs9amz94ua5ncmqdqpz4mhxue69u"
type_, decoded = Nip19.decode(nevent)
```

### Encoding a Public Key
```python
hex_pubkey = "df017e0bae04ae21548c1c49687fcace43664e77570ad992be5cbe6b885b5ffe"
npub = Nip19.hex_to_bech32(hex_pubkey, "npub")
```

### Encoding/Decoding a Secret Key
```python
hex_seckey = "a4e9708dcc3d86d68d0b7043387b28f721d4a4459e21396320fd69a4f5725b7b"
# hex -> nsec
nsec = Nip19.hex_to_bech32(hex_seckey, "nsec")
# decode nsec
type_, decoded = Nip19.decode(nsec)
```

## 8. Complete Source Code
```python
import bech32
from dataclasses import dataclass
from typing import List, Optional, Tuple
import struct

@dataclass
class TLV:
    type: int
    length: int
    value: bytes

@dataclass
class DecodedNote:
    note_id: str

@dataclass
class DecodedPubkey:
    pubkey: str

@dataclass
class DecodedSeckey:
    seckey: str

@dataclass
class DecodedEvent:
    id: str
    relays: List[str]
    author: Optional[str]
    kind: Optional[int]

@dataclass
class DecodedProfile:
    pubkey: str
    relays: List[str]

class Nip19:
    """
    Decoder for Bech32-encoded NOSTR entities compliant with NIP-19
    """
    
    @staticmethod
    def decode_bech32(bech32_str: str) -> Tuple[str, bytes]:
        """Decode a bech32 string and return HRP and data"""
        hrp, data = bech32.bech32_decode(bech32_str)
        if hrp is None or data is None:
            raise ValueError("Invalid bech32 string")
        return hrp, bytes(bech32.convertbits(data, 5, 8, False))

    @staticmethod
    def encode_bech32(hrp: str, data: bytes) -> str:
        """Encode data to a bech32 string"""
        converted_bits = bech32.convertbits(list(data), 8, 5, True)
        return bech32.bech32_encode(hrp, converted_bits)

    @staticmethod
    def parse_tlv(data: bytes) -> List[TLV]:
        """Parse TLV data"""
        tlv_list = []
        i = 0
        while i < len(data):
            if i + 2 > len(data):
                raise ValueError("Invalid TLV data")
            t = data[i]
            l = data[i + 1]
            if i + 2 + l > len(data):
                raise ValueError("Invalid TLV length")
            v = data[i + 2:i + 2 + l]
            tlv_list.append(TLV(t, l, v))
            i += 2 + l
        return tlv_list

    @staticmethod
    def decode(bech32_str: str) -> Tuple[str, any]:
        """
        Decode a Bech32-encoded string
        Returns: (type, decoded_data)
        """
        hrp, data = Nip19.decode_bech32(bech32_str)
        
        if hrp == "note":
            return "note", DecodedNote(data.hex())
            
        elif hrp == "npub":
            return "npub", DecodedPubkey(data.hex())
            
        elif hrp == "nsec":
            return "nsec", DecodedSeckey(data.hex())
            
        elif hrp == "nevent":
            tlvs = Nip19.parse_tlv(data)
            event_data = DecodedEvent(
                id="",
                relays=[],
                author=None,
                kind=None
            )
            
            for tlv in tlvs:
                if tlv.type == 0:  # special (event id)
                    event_data.id = tlv.value.hex()
                elif tlv.type == 1:  # relay
                    event_data.relays.append(tlv.value.decode('ascii'))
                elif tlv.type == 2:  # author
                    event_data.author = tlv.value.hex()
                elif tlv.type == 3:  # kind
                    event_data.kind = int.from_bytes(tlv.value, 'big')
                    
            return "nevent", event_data
            
        elif hrp == "nprofile":
            tlvs = Nip19.parse_tlv(data)
            profile_data = DecodedProfile(
                pubkey="",
                relays=[]
            )
            
            for tlv in tlvs:
                if tlv.type == 0:  # special (pubkey)
                    profile_data.pubkey = tlv.value.hex()
                elif tlv.type == 1:  # relay
                    profile_data.relays.append(tlv.value.decode('ascii'))
                    
            return "nprofile", profile_data
            
        else:
            raise ValueError(f"Unsupported bech32 prefix: {hrp}")

    @staticmethod
    def hex_to_bech32(hex_str: str, type: str) -> str:
        """Convert a hexadecimal string to bech32 format"""
        data = bytes.fromhex(hex_str)
        return Nip19.encode_bech32(type, data)

def main():
    # Example of decoding an event ID
    nevent = "nevent1qqs8l95us0smltxjryemq0wxtd9tegwnyy6r7jcs9amz94ua5ncmqdqpz4mhxue69uhhyetvv9ujuerpd46hxtnfduhsygxlq9lqhtsy4cs4frquf958ljkwgdnyua6hptve90juhe4csk6llce3xrpy"
    try:
        type_, decoded = Nip19.decode(nevent)
        print(f"Type: {type_}")
        print(f"Decoded data: {decoded}")
    except ValueError as e:
        print(f"Error: {e}")

    # Example of encoding a public key
    hex_pubkey = "7e7e9c42a91bfef19fa929e5fda1b72e0ebc1a4c1141673e2794234d86addf4e"
    try:
        npub = Nip19.hex_to_bech32(hex_pubkey, "npub")
        print(f"\nEncoded pubkey: {npub}")
    except ValueError as e:
        print(f"Error: {e}")

    # Example of encoding/decoding a secret key
    hex_seckey = "67dea2ed018072d675f5415ecfaed7d2597555e202d85b3d65ea4e58d2d92ffa"
    try:
        # hex -> nsec
        nsec = Nip19.hex_to_bech32(hex_seckey, "nsec")
        print(f"\nEncoded secret key: {nsec}")
        
        # decode nsec
        type_, decoded = Nip19.decode(nsec)
        print(f"Decoded type: {type_}")
        print(f"Decoded secret key: {decoded}")
    except ValueError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
```

## 9. Error Handling
ValueError is raised in the following cases:
- When an invalid Bech32 string is input
- When an unsupported Bech32 prefix is used
- When TLV data format is invalid

## 10. Notes
1. Please use hexadecimal format within the actual NOSTR protocol.
2. Unknown types are ignored during TLV data parsing.
3. Care should be taken when processing large data sets, as TLV parsing requires loading the entire data into memory.
4. Exercise extreme caution when handling secret keys (nsec), as they provide full access to NOSTR identities.

## 11. Dependencies
- bech32: For Bech32 encoding/decoding operations
- dataclasses: For defining structured data classes with type annotations
- typing: For providing type hints and improving code readability
- struct: For handling binary data structures and conversions

---
- Created: 2024-10-29
- Updated: 2024-10-30