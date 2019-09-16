import fcntl
import sys

def lock(filename):
    lock_file = open(filename, 'w')
    try:
        fcntl.lockf(lock_file, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        return False
    return True

lock_filename = '/tmp/sample-locking.lock'
locked = lock(lock_filename)

if not locked:
    print('Cannot lock: ' + lock_filename)
    sys.exit(1)

print('Locked! Running code...')

quit = False
while quit is not True:
    quit = input('Press q to quit ')
    quit = str(quit) == 'q'

print('Bye!')
sys.exit(0)
