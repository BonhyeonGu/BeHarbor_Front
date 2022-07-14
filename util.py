import os
import time

class Util:
    def outDirList(self, location):
        files = os.listdir(location)
        dates_edit = []
        for file in files:
            dates_edit.append(time.ctime(os.path.getmtime(location + '/' + file)))
        return files, dates_edit

    def outDirByte(self, location):
        total = 0
        with os.scandir(location) as it:
            for entry in it:
                if entry.is_file():
                    total += entry.stat().st_size
                elif entry.is_dir():
                    total += self.outDirByte(entry.path)
        return total

    def pathJoin(self, a, b):
        return os.path.join(a, b)