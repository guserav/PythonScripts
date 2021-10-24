import getpass
import time
import sys, tty, termios

pprompt = lambda: (getpass.getpass(), getpass.getpass('Retype password: '))

p1, p2 = pprompt()
while p1 != p2:
    print('Passwords do not match. Try again')
    p1, p2 = pprompt()

print("Length {}".format(len(p1)))
print(p1, end='\r')
fd = sys.stdin.fileno()

old_settings = termios.tcgetattr(fd)
try:
    tty.setraw(sys.stdin.fileno())
    ch = sys.stdin.read(1)
finally:
    termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)

print("*" * len(p1))
password = p1
print("Retype the password as long as you like end with typing 'end'")
inputStr = None
while inputStr != 'end':
    inputStr = getpass.getpass()
    if inputStr == password:
        print("Correct")
    else:
        print("Wrong")
