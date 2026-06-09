import json
import os

class jsonDB:
    def __init__(self, path, default):
        self.path = path

        if not os.path.exists(path):
            with open(path, 'w') as f:
                json.dump(default, f, indent = 4)
                self.data = default
                return

        with open(path, 'r') as f:
            self.data = json.load(f)
                
            
    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent = 4)