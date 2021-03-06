from models.database_models import Post, Comment, GabUser
import utils.data_utils as du
from sqlmodel import create_engine, Session, select
from sqlalchemy.dialects.mysql import insert
import sqlalchemy as sa
import datetime


#Big note for a database (there's probably a better place to put this)
#Emojis cannot be stored by default in mysql databases and most social media uses a bunch of emojis
#After making the table run this:
#ALTER TABLE Tablename CONVERT TO CHARACTER SET utf8mb4 COLLATE utf8mb4_bin
#It changes the character set to utf8mb4 which allows emojis, just sub Tablename for the name of your table
def write_comments(comments: list):
    connection_url = sa.engine.URL.create(
        drivername='mysql+pymysql',
        username='root',
        password='local_test_password',
        host='127.0.0.1',
        port='3306',
        database='gab_db'
    )
    engine = create_engine(connection_url)
    with Session(engine) as session:
        for comment in comments:
            comment_info = du.unpack_comment_data(comment)
            user_gab_id = comment['account']['id']
            if comment_info[4] == 'null':
                insert_comment_query = '''INSERT INTO comments(gab_id, in_reply_to_id, content, created_at, revised_at, 
                                    reblogs_count, replies_count, favourites_count, id_gab_users)
                                    VALUES({}, {}, '{}', '{}', {}, {}, {}, {},
                                    (SELECT id FROM gab_users WHERE gab_id = {}))

                                    ON DUPLICATE KEY UPDATE

                                    content = '{}',
                                    created_at = '{}',
                                    revised_at = {},
                                    reblogs_count = {},
                                    replies_count = {},
                                    favourites_count = {}
                                '''.format(*comment_info, user_gab_id, *comment_info[2:])
            else:
                insert_comment_query = '''INSERT INTO comments(gab_id, in_reply_to_id, content, created_at, revised_at, 
                                    reblogs_count, replies_count, favourites_count, id_gab_users)
                                    VALUES({}, {}, '{}', '{}', '{}', {}, {}, {},
                                    (SELECT id FROM gab_users WHERE gab_id = {}))

                                    ON DUPLICATE KEY UPDATE

                                    content = '{}',
                                    created_at = '{}',
                                    revised_at = '{}',
                                    reblogs_count = {},
                                    replies_count = {},
                                    favourites_count = {}
                                '''.format(*comment_info, user_gab_id, *comment_info[1:])
            session.exec(insert_comment_query)

        session.commit()

def write_posts(posts: list):
    connection_url = sa.engine.URL.create(
        drivername='mysql+pymysql',
        username='root',
        password='local_test_password',
        host='127.0.0.1',
        port='3306',
        database='gab_db'
    )
    engine = create_engine(connection_url)
    with Session(engine) as session:
        for post in posts:
            post_info = du.unpack_post_data(post)
            user_gab_id = post['account']['id']
            if post_info[3] == 'null':
                insert_post_query = '''INSERT INTO posts(gab_id, content, created_at, revised_at, 
                                    reblogs_count, replies_count, favourites_count, reactions_counts, id_gab_users)
                                    VALUES({}, '{}', '{}', {}, {}, {}, {}, '{}',
                                    (SELECT id FROM gab_users WHERE gab_id = {}))

                                    ON DUPLICATE KEY UPDATE

                                    content = '{}',
                                    created_at = '{}',
                                    revised_at = {},
                                    reblogs_count = {},
                                    replies_count = {},
                                    favourites_count = {},
                                    reactions_counts = '{}'
                                '''.format(*post_info, user_gab_id, *post_info[1:])
            else:
                insert_post_query = '''INSERT INTO posts(gab_id, content, created_at, revised_at, 
                                    reblogs_count, replies_count, favourites_count, reactions_counts, id_gab_users)
                                    VALUES({}, '{}', '{}', '{}', {}, {}, {}, '{}',
                                    (SELECT id FROM gab_users WHERE gab_id = {}))

                                    ON DUPLICATE KEY UPDATE

                                    content = '{}',
                                    created_at = '{}',
                                    revised_at = '{}',
                                    reblogs_count = {},
                                    replies_count = {},
                                    favourites_count = {},
                                    reactions_counts = '{}'
                                '''.format(*post_info, user_gab_id, *post_info[1:])
            session.exec(insert_post_query)

        session.commit()

def write_users(users: list):
    connection_url = sa.engine.URL.create(
        drivername='mysql+pymysql',
        username='root',
        password='local_test_password',
        host='127.0.0.1',
        port='3306',
        database='gab_db'
    )
    engine = create_engine(connection_url)
    with Session(engine) as session:
        for user in users:
            account_info = du.get_author_info_from_user(user)
            insert_user_query = '''INSERT INTO gab_users(gab_id, username, name, display_name,
                                    is_verified, account_created_at, account_note, num_followers,
                                    created_at, is_bot, is_donor)
                                    
                                    VALUES({}, '{}', '{}', '{}', {}, '{}', '{}', {}, CURRENT_TIMESTAMP, {}, {})

                                    ON DUPLICATE KEY UPDATE

                                    username = '{}',
                                    name = '{}',
                                    display_name = '{}',
                                    is_verified = {},
                                    account_created_at = '{}',
                                    account_note = '{}',
                                    num_followers = {},
                                    is_bot = {},
                                    is_donor = {}
                                    
                                    '''.format(*account_info, *(account_info[1:]))
            session.exec(insert_user_query)
        
        session.commit()


def get_datetime(string_date: str):
    output = datetime.datetime.strptime(string_date, '%Y-%m-%dT%H:%M:%S.%fZ')
    return output

def __add_test_post__():
    connection_url = sa.engine.URL.create(
        drivername='mysql+pymysql',
        username='root',
        password='local_test_password',
        host='127.0.0.1',
        port='3306',
        database='gab_db'
    )
    engine = create_engine(connection_url)
    post = Post(gab_id=2, 
                content='test post', 
                created_at=datetime.datetime.now(),
                revised_at=datetime.datetime.now(),
                favourites_count=0,
                reblogs_count=0,
                replies_count=0,
                id_gab_users=0)
    with Session(engine) as session:
        session.add(post)
        session.commit()

def __get_first_post__():
    connection_url = sa.engine.URL.create(
        drivername='mysql+pymysql',
        username='root',
        password='local_test_password',
        host='127.0.0.1',
        port='3306',
        database='gab_db'
    )
    engine = create_engine(connection_url)
    with Session(engine) as session:
        statement = select(Post).where(Post.id == 1)
        result = session.exec(statement).all()
        return result

def __execute__ ():
    connection_url = sa.engine.URL.create(
        drivername='mysql+pymysql',
        username='root',
        password='local_test_password',
        host='127.0.0.1',
        port='3306',
        database='gab_db'
    )
    vals = []
    engine = create_engine(connection_url)
    with Session(engine) as session:
        result = session.exec('SELECT * FROM posts')
        for entry in result:
            vals.append(entry)
    return(vals)
