from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

FTP_PORT = 2121

FTP_USER = 'usuario1'
FTP_PASSWORD = 'contraseña1'
FTP_DIRECTORY = '/home/user1/ftpfiles'


def main():
    authorizer = DummyAuthorizer()
    authorizer.add_user(FTP_USER, FTP_PASSWORD, FTP_DIRECTORY, perm='elr')

    handler = FTPHandler
    handler.authorizer = authorizer
    handler.banner = 'Servidor FTP Listo'
    handler.passive_ports = range(60000, 65535)

    address = ('', FTP_PORT)
    server = FTPServer(address, handler)

    server.max_cons = 256
    server.max_cons_per_ip = 5

    server.serve_forever()



if __name__ == '__main__':
    main()