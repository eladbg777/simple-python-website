import hashlib


def calculate_password_hash(config, password):
    secret = config.password_secret
    module = hashlib.md5()
    string = f'{password}+{secret}'
    module.update(bytes(string, encoding='utf-8'))
    password_hash = module.hexdigest()
    return password_hash


def verify_hash(config, password, password_hash):
    calculated_hash = calculate_password_hash(config, password)
    if calculated_hash == password_hash:
        return True
    else:
        return False


def get_user_name(db, username):
    row = db.execute('SELECT firstname from users where username=?', (username,)).fetchone()
    if row:
        name = row['firstname']
        if name and name != '':
            return name
        else:
            return username

