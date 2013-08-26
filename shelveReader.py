import shelve

file1 = shelve.open("sections.dat")
print file1.keys()
print ""
print file1.values()
raw_input()
