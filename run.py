from logging import debug

from sqlalchemy.sql.expression import true
from brevity import create_app,db


app = create_app()


if __name__ == '__main__':
    app.run(debug=true)