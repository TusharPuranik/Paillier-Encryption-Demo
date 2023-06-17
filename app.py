import tkinter as tk
from tkinter import ttk, messagebox
from Crypto.Util.number import getPrime
from random import randint
import webbrowser
from flask import Flask, render_template, request, redirect, url_for, session
import timeit
import matplotlib.pyplot as plt


app = Flask(__name__)
app.secret_key = "your_secret_key"


class Paillier:
    def __init__(self, bit_length=128):
        p = getPrime(bit_length)
        q = getPrime(bit_length)

        self.n = p * q
        self.n_square = self.n * self.n
        self.g = self.n + 1

        self.lmbda = (p - 1) * (q - 1)
        self.mu = self.mod_inverse(self.lmbda, self.n)

    def mod_inverse(self, a, m):
        def egcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                g, x, y = egcd(b % a, a)
                return g, y - (b // a) * x, x

        g, x, _ = egcd(a, m)
        if g != 1:
            raise Exception("Modular inverse does not exist.")
        else:
            return x % m

    def encrypt(self, plaintext):
        r = randint(1, self.n - 1)

        c = (
            pow(self.g, plaintext, self.n_square) * pow(r, self.n, self.n_square)
        ) % self.n_square

        return c

    def decrypt(self, ciphertext):
        numerator = pow(ciphertext, self.lmbda, self.n_square) - 1
        plaintext = (numerator // self.n * self.mu) % self.n

        return plaintext

    def homomorphic_addition(self, ciphertext1, ciphertext2):
        c = (ciphertext1 * ciphertext2) % self.n_square
        return c

    def homomorphic_multiplication(self, ciphertext, constant):
        c = pow(ciphertext, constant, self.n_square)
        return c


def create_paillier():
    global paillier
    paillier = Paillier()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["username"] = username
        session["password"] = password
        create_paillier()
        return redirect(url_for("demo"))
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if "username" in session and "password" in session:
            if session["username"] == username and session["password"] == password:
                return redirect(url_for("demo"))
        error = "Invalid username or password."
        return render_template("login.html", error=error)
    return render_template("login.html")


@app.route("/demo", methods=["GET", "POST"])
def demo():
    if "username" not in session or "password" not in session:
        return redirect(url_for("login"))

    if request.method == "POST":
        try:
            a = int(request.form["number1"])
            b = int(request.form["number2"])

            encrypted_a = paillier.encrypt(a)
            encrypted_b = paillier.encrypt(b)

            sum_result = paillier.homomorphic_addition(encrypted_a, encrypted_b)
            mul_result = paillier.homomorphic_multiplication(encrypted_a, b)

            decrypted_a = paillier.decrypt(encrypted_a)
            decrypted_b = paillier.decrypt(encrypted_b)
            decrypted_sum = paillier.decrypt(sum_result)
            decrypted_mul = paillier.decrypt(mul_result)

            result_text = (
                f"{'Encrypted A:':<18} {encrypted_a}\n"
                f"{'Encrypted B:':<18} {encrypted_b}\n\n"
                f"{'Decrypted A:':<18} {decrypted_a}\n"
                f"{'Decrypted B:':<18} {decrypted_b}\n\n"
                f"{'Encrypted Sum:':<18} {sum_result}\n"
                f"{'Encrypted Multiplication:':<18} {mul_result}\n\n"
                f"{'Decrypted Sum:':<18} {decrypted_sum}\n"
                f"{'Decrypted Multiplication:':<18} {decrypted_mul}"
            )

            return render_template("result.html", result_text=result_text)
        except ValueError:
            error = "Invalid input! Please enter valid integers."
            return render_template("demo.html", error=error)
    return render_template("demo.html")


@app.route("/efficiency")
def efficiency():
    if "username" not in session or "password" not in session:
        return redirect(url_for("login"))

    return render_template("efficiency.html")


@app.route("/compute_efficiency", methods=["POST"])
def compute_efficiency():
    if "username" not in session or "password" not in session:
        return redirect(url_for("login"))

    try:
        num_iterations = int(request.form["num_iterations"])
        a = int(request.form["entry_a"])
        b = int(request.form["entry_b"])
        encrypted_a_times = []
        encrypted_b_times = []

        for i in range(num_iterations):
            encrypt_time_a = (
                timeit.timeit(lambda: paillier.encrypt(a), number=100) / 100
            )
            encrypt_time_b = (
                timeit.timeit(lambda: paillier.encrypt(b), number=100) / 100
            )

            encrypted_a_times.append(encrypt_time_a)
            encrypted_b_times.append(encrypt_time_b)

        avg_encryption_time_a = sum(encrypted_a_times) / len(encrypted_a_times)
        avg_encryption_time_b = sum(encrypted_b_times) / len(encrypted_b_times)

        result_text = (
            f"Average Encryption Time for A: {avg_encryption_time_a:.6f} seconds\n"
        )
        result_text += (
            f"Average Encryption Time for B: {avg_encryption_time_b:.6f} seconds"
        )

        return render_template(
            "result.html", result_text=result_text
        )  # Pass result_text to the template

    except ValueError:
        error = "Invalid input! Please enter valid values."
        return render_template("efficiency.html", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True)
