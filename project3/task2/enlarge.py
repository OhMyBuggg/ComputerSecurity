import os

def getSize(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size

cat = open('cat_backup', 'rb')
cat_size = getSize(cat)
infect = open('a.out', 'rb')
infect_size = getSize(infect)
infect.close()

infect = open('a.out', 'a')
concat = ''
enlarge_size = cat_size - infect_size - 4
for i in range(enlarge_size):
    concat += 'a'
# concat += b'deadbeaf
infect.write(concat)
infect.close()
infect = open('a.out', 'ab+')
w = b"\xde\xad\xbe\xef"
infect.write(w)
infect.close()
# os.system('echo {} >> a.out'.format(concat))
