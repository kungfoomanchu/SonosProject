import re

# compile a RegEx
# This should find most barcodes. it'll find any number, anywhere that has 8 or more digits. alphanumeric can preceed or follow
re_barcode = re.compile('/[0-9]{8,}/gm')
print(re_barcode)

# Test match of regex
match = re_barcode.match('98274589781')
print(match)

# Test group function (should print the string the regex found)
barcode = match.group()
print(barcode)

if match:
    print('Match found: ', match.group())
else:
    print('No match')