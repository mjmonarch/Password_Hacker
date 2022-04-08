# -------------------------------------------STAGE 1-------------------------------------------
# import socket
# import sys
#
# if len(sys.argv) != 4:
#     print("error")
# else:
#     hostname = sys.argv[1]
#     port = int(sys.argv[2])
#     psw = sys.argv[3]
#
#     with socket.socket() as my_s:
#         my_s.connect((hostname, port))
#         my_s.send(psw.encode())
#
#         respond = my_s.recv(1024).decode()
#         print(respond)

# -------------------------------------------STAGE 2-------------------------------------------
import itertools
import socket
import string
import sys

NUMBERS = [str(x) for x in range(10)]
LITERAS = list(string.ascii_lowercase)

if len(sys.argv) != 3:
    print("error")
    sys.exit()

hostname = sys.argv[1]
port = int(sys.argv[2])

with socket.socket() as my_s:
    my_s.connect((hostname, port))

    i = 1
    finished = False
    while not finished:
        for attempt in itertools.combinations(NUMBERS + LITERAS, i):
            attempt = "".join(attempt)
            my_s.send(attempt.encode())
            respond = my_s.recv(1024).decode()
            if respond == "Connection success!":
                print(attempt)
                finished = True
                break
        i += 1
