from mario import Task, File


class TextFile(File):
    extension = ".txt"


class RemoveDuplicateLines(Task):
    class Inputs:
        file = TextFile()

    class Outputs:
        file = TextFile()

    def run(self):
        self.Inputs
