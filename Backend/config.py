SECRET_KEY = "20010508wzy"

HOSTNAME ="127.0.0.1"
PORT= "3306"
USERNAME="root"
PASSWORD="20010508wzy"
DATABASE= "new_schema_1"

DB_URI = f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
SQLALCHEMY_DATABASE_URI = DB_URI