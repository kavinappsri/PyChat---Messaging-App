import sys
import threading
import os

#_get_char() | Hardware adaptive

if os.name == 'nt':
    #Windows adapter

    import msvcrt
    def _get_char():
        ch = msvcrt.getch()
        if ch in (b'\x00', b'\xe0'):
            mcvrct.getch()
            return None
        return ch.decode("utf-8", errors = "ignore")

else:
    #Linux adapter

    import tty
    import termios
    def _get_char():
        fd = sys.stdin.fileno()
        oldSettings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, oldSettings)
        return ch

# CLASS - userInt

class userInt:
    def __init__(self, prompt):
        self.prompt = prompt
        self.inputBuffer = ""
        self.lock = threading.Lock()

    def _redraw(self):
        sys.stdout.write(f"\r\033[K{self.prompt}{self.inputBuffer}")
        sys.stdout.flush()

    def clear(self):
        print("\033[H\033[2J", end="")

    def print(self, message):
        with self.lock:
            sys.stdout.write(f"\r\033[K{message}\n")
            self._redraw()

    def getInput(self):
        while True:
            ch = _get_char()
            if ch is None:
                continue

            with self.lock:
                if ch in ('\r', '\n'):
                    finalText = self.inputBuffer
                    self.inputBuffer = ""
                    sys.stdout.write("\r\033[K")
                    sys.stdout.flush()
                    return finalText
                    
                elif ch in ('\x7f', '\x08'):
                    if len(self.inputBuffer) > 0:
                        self.inputBuffer = self.inputBuffer[:-1]
                        
                elif ord(ch) < 32:
                    continue
                else:
                    self.inputBuffer += ch
                self._redraw()

