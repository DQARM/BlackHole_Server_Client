from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer
from pyftpdlib.filesystems import AbstractedFS

class MemoryFS(AbstractedFS):

    def __init__(self, root, cmd_channel):
        super().__init__(root, cmd_channel)
        self.fs = {}

    def open(self, filename, mode):
        return open(filename, mode)

    def mkstemp(self, suffix='', prefix='', dir=None, text=False):
        raise NotImplementedError()

    def chdir(self, path):
        pass

    def mkdir(self, path):
        self.fs[path] = {}

    def listdir(self, path):
        return []

    def rmdir(self, path):
        del self.fs[path]

    def remove(self, path):
        del self.fs[path]

    def rename(self, src, dst):
        self.fs[dst] = self.fs[src]
        del self.fs[src]

    def isfile(self, path):
        return False

    def isdir(self, path):
        return True

    def getsize(self, path):
        return 0

    def getmtime(self, path):
        return 0

    def realpath(self, path):
        return path

    def lexists(self, path):
        return False

    def get_user_by_path(self, path):
        return 'ftp'

    def get_perms(self, path):
        return 'elradfmw'

    def get_ino(self, path):
        return 0

    def format_list(self, basedir, listing):
        return []

    def format_mlsx(self, basedir, listing, perms, type, unique, facts):
        return []

def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user("ftp", "ftp", "/", perm="elradfmw")

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.abstracted_fs = MemoryFS

    server = FTPServer(("0.0.0.0", 2121), handler)
    server.serve_forever()

if __name__ == "__main__":
    main()
