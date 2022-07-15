#!/usr/bin/env python3

import base64
import sys
import argparse


n = 100

def binary_code(sc_data): 
    bcode = ''
    for byte in sc_data:
        bcode += "\\x" + hex(byte)[2:].zfill(2)
    
    return bcode

def binary_encode(sc_data):

    # Just raw binary blog base64 encoded
    encoded_raw = base64.b64encode(sc_data)
    chunks = [encoded_raw[i:i+n] for i in range(0, len(encoded_raw), n)]
    
    return chunks


def standard_shellcode(sc_data):
    # Print in "standard" shellcode format \x41\x42\x43....
    bcode = binary_code(sc_data)
    binary_chunks = [bcode[i:i+n] for i in range(0, len(bcode), n)]
    
    return binary_chunks

def csharp_shellcode(sc_data):
    bcode = binary_code(sc_data)
    # Convert this into a C# style shellcode format
    cs_shellcode = "0" + ",0".join(bcode.split("\\")[1:])

    return cs_shellcode

def cs_encode_shellcode(cs_data):

    cs_shellcode = csharp_shellcode(sc_data)

    # Base 64 encode the C# code (for use with certain payloads :))
    encoded_cs = base64.b64encode(cs_shellcode.encode())

    return encoded_cs




if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t','--transform', default = 's', choices =['be','s','cs','cse'], help='be: Binary encoded, \ns: Standard, \ncs: C# shellcode,\ncse: C# shellcode Encode\n(default = s)')
    parser.add_argument('-f','--file', help='binary file containing shellcode you are converting')
    args = parser.parse_args()
   
    t = args.transform

    with open(args.file, 'rb') as sc_handle:
        sc_data = sc_handle.read()

    # Write out the files to disk (edit this path as needed)
    with open('formatted_helloworld_shellcode.txt', 'w') as format_out:
        if t == 's':
            chunks = standard_shellcode(sc_data)
            for item in chunks: 
                format_out.write(f"\"{item}\"\n")
        elif t == 'be':
            binary_chunks = binary_encode(sc_data)
            for item in binary_chunks: 
                format_out.write(f"\"{item.decode('ascii')}\"\n")
        elif t == 'cs':
            format_out.write(csharp_shellcode(sc_data))
        elif t == 'cse':
            format_out.write(str(cs_encode_shellcode(sc_data)))
