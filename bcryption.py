import bcrypt

password = "hello123"

hashed_password = bcrypt.hashpw(
    password.encode("utf-8"),
    bcrypt.gensalt()
)

print("Hash:", hashed_password)

correct = bcrypt.checkpw(
    password.encode("utf-8"),
    hashed_password
)

print("Correct password:", correct)

wrong = bcrypt.checkpw(
    "hello456".encode("utf-8"),
    hashed_password
)

print("Wrong password:", wrong)