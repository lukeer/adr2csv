# read OperaMail addresss file and write back as csv file
# 1) Check which categories are available
# 2) Fill in empty entries with "None"
# 3) Create csv file from gathered info

import argparse
from asyncore import read
parser = argparse.ArgumentParser()
parser.add_argument("-i", "--Input", help = "Input Filename")
parser.add_argument("-o", "--Output", help = "Output Filename")
args = parser.parse_args()
# print("All arguments: ")
# print(args._get_args())
# print('\n')
# print("Input: " + str(args.Input))
# print("Output: " + str(args.Output))

_keys = []
class Contact:
    def __init__(self, keylist:list) -> None:
        self.Properties = dict.fromkeys(keylist)

    def __str__(self) -> str:
        output = "C "
        if(self.Properties["NAME"] != None):
            output += self.Properties["NAME"]
        if(self.Properties["MAIL"] != None):
            output += self.Properties["MAIL"]
        return(output)

_contacts = []

with open(args.Input) as reader:
    isFirstContactFound = False
    for newLine in reader:
        if(newLine.startswith("#CONTACT")):
            isFirstContactFound = True
        elif(isFirstContactFound):
            if(newLine.startswith('\t')):
                equalsPosition = newLine.find("=")
                if(equalsPosition > 1):
                    currentKey = newLine[1 : equalsPosition]
                    if(currentKey not in _keys):
                        _keys.append(currentKey)

    print("Keys: " + str(_keys))

    _currentContact = None
    reader.seek(0)
    for newLine in reader:
        if(newLine.startswith("#CONTACT")):
            _currentContact = Contact(_keys)
            _contacts.append(_currentContact)
        elif(_currentContact != None):
            if(newLine.startswith('\t')):
                equalsPosition = newLine.find("=")
                if(equalsPosition > 1):
                    currentKey = newLine[1 : equalsPosition]
                    currentValue = newLine[equalsPosition + 1 : -1]
                    _currentContact.Properties[currentKey] = currentValue

ValueDelimiter = '\t'
LineDelimiter = '\n'
with open(args.Output, 'x') as writer:
    for oneKey in _keys:
        writer.write(oneKey + ValueDelimiter)
    writer.write(LineDelimiter)

    for oneContact in _contacts:
        for oneKey in _keys:
            oneValue = oneContact.Properties[oneKey]
            if(oneValue != None):
                writer.write(oneValue)
            writer.write(ValueDelimiter)
        writer.write(LineDelimiter)

