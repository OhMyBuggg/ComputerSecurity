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
enlarge_size = cat_size - infect_size - 8
for i in range(enlarge_size):
    concat += 'a'
concat += 'deadbeaf'
infect.write(concat)
# os.system('echo {} >> a.out'.format(concat))
