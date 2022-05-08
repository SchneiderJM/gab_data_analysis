from models.database_models import posts, comments, gab_users
from sqlmodel import create_engine, Session, select
import sqlalchemy as sa

def get_first_post():
    connection_url = sa.engine.URL.create(
        drivername='mysql+pymysql',
        username='root',
        password='local_test_password',
        host='127.0.0.1',
        port='3306',
        database='gab_db'
    )
    #engine = create_engine('mysql+mysqlconnector://root:local_test_password@localhost:3306/gab_db')
    engine = create_engine(connection_url)
    with Session(engine) as session:
        statement = select(posts).where(posts.id == 1)
        result = session.exec(statement).all()
        return result

def write_posts(posts, batch=False):
    '''
    Description: Writes a post (or several) to the database

    Inputs:
        post (list): list of posts (if sending one post, just send a list with only one entry)
        batch (boolean): Boolean value, whether multiple posts should be written to the database. 
            If this is false, only the first post in the list will be written
    '''
    assert len(posts) == 0, 'post list is empty, nothing will be written'
    engine = create_engine('localhost:3306')
    if (batch == False):
        post = posts[0]
