from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

#Generate Private Key
private_key = rsa.generate_private_key(
    public_exponent = 65537,
    key_size = 2048,
    backend = default_backend()
)

#Serialize and save private key
pem_private = private_key.private_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PrivateFormat.TraditionalOpenSSL,
    encryption_algorithm = serialization.NoEncryption() 
)

with open("private_key.pem", "wb") as f:
    f.write(pem_private)

#Generate and serialize public key
public_key = private_key.public_key()
pem_public = public_key.public_bytes(
    encoding = serialization.Encoding.PEM,
    format = serialization.PublicFormat.SubjectPublicKeyInfo
)

with open("public_key.pem", "wb") as f:
    f.write(pem_public)
    
print(pem_private)
print(pem_public)

