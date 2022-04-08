import socket


def submit_data(data, client, address):
    with client as my_s:
        my_s.connect(address)
        my_s.send(data.encode())
