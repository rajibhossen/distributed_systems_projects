import fcntl
import time
from lockfile import LockFile


lockfile = open('test.txt', 'r+')
fcntl.flock(lockfile, fcntl.LOCK_EX)
content = int(lockfile.read())
print content
lockfile.seek(0)
lockfile.write(str(content+1))
time.sleep(10)
fcntl.flock(lockfile, fcntl.LOCK_UN)


