import os

def getSize(fileobject):
    fileobject.seek(0,2) # move the cursor to the end of the file
    size = fileobject.tell()
    return size

cat = open('cat_backup', 'rb')
cat_size = getSize(cat)
infect = open('a.out', 'rb')
infect_size = getSize(infect)

concat = ''
enlarge_size = cat_size - infect_size - 9
for i in range(enlarge_size):
    concat += 'a'
concat += 'deadbeaf'
os.system('echo {} >> a.out'.format(concat))
