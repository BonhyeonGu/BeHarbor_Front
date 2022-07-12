import os

class Util:
    def outDirList(self, location):
        return os.listdir(location)

    def outDirByte(self, location):
        total = 0
        with os.scandir(location) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self.outDirByte(entry.path)
        return total