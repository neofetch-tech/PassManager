from cryptography.fernet import Fernet
key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(password.encode()).decode()
decrypted = cipher.decrypt(encrypted.encode()).decode()