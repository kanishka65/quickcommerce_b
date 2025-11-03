
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()
password = 'test123'
hashed = bcrypt.generate_password_hash(password)
print('Hash works:', bcrypt.check_password_hash(hashed, password))
