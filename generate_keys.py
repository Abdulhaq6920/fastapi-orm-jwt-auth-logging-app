from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


# Generate a private RSA key
private_key = rsa.generate_private_key(
    public_exponent=65537,
    key_size=2048
)


# Convert private key to PEM format
private_pem = private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)


# Generate the public key from the private key
public_key = private_key.public_key()


# Convert public key to PEM format
public_pem = public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)


# Save private key
with open("private_key.pem", "wb") as f:
    f.write(private_pem)


# Save public key
with open("public_key.pem", "wb") as f:
    f.write(public_pem)


print("RSA key pair generated successfully!")