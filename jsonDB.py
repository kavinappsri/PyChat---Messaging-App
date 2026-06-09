import json
import os

#CLASS JSONDB
class jsonDB:
    #Provides a simple database API with read and write capability
    def __init__(self, path, default):
        self.path = path

        #Creates a file with the default value if file doesn't exist
        if not os.path.exists(path):
            with open(path, 'w') as f:
                json.dump(default, f, indent = 4)
                self.data = default
                return

        with open(path, 'r') as f:
            self.data = json.load(f)
                
    
    #saves changes in self.data to the file        
    def save(self):
        with open(self.path, 'w') as f:
            json.dump(self.data, f, indent = 4)