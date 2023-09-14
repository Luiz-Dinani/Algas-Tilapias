import hashlib

def hash_password(texto):
  hash_object = hashlib.sha256()
  hash_object.update(texto.encode("utf-8"))
  return hash_object.hexdigest()