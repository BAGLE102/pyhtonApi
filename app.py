from flask import Flask, request, jsonify
import pyodbc
from sqlalchemy import create_engine
from sqlalchemy import text
import pandas as pd
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey
from sqlalchemy.exc import SQLAlchemyError
import requests
app = Flask(__name__)

# 数据库连接字符串
def get_conn_str():
    param = {
        'uid': "sa",
        'pwd': "ji3ao6u.3au/6y4",
        'srv': "210.240.202.114",
        'pno': 1443,
        'db': 'Trash',  
    }

    return f"mssql+pyodbc://{param['uid']}:{param['pwd']}@{param['srv']}:{param['pno']}/{param['db']}?driver=ODBC Driver 17 for SQL Server"

# 连接数据库
def connect_to_database():
    try:
        engine = create_engine(get_conn_str())
        return engine.connect()
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        return None

def check_user_exists(LineID):
    conn = connect_to_database()
    if conn:
        metadata = MetaData()
        users_table = Table('Users', metadata, autoload=True, autoload_with=conn)
        query = users_table.select().where(users_table.c.LineID == LineID)
        result = conn.execute(query).fetchone()
        conn.close()
        return result is not None
    return False

def get_user_data_from_database(user_id):
    conn = connect_to_database()
    if conn:
        metadata = MetaData()
        users_table = Table('Users', metadata, autoload=True, autoload_with=conn)
        query = users_table.select().where(users_table.c.LineID == user_id)
        result = conn.execute(query).fetchone()
        conn.close()
        if result:
            return {
                'user_id': result[0],
                'display_name': result[1],
                'picture_url': result[2]
            }
    return None



def insert_user_to_database(user_profile):
    conn = connect_to_database()
    if conn:
        try:
            metadata = MetaData()
            users_table = Table('Users', metadata, autoload=True, autoload_with=conn)
            query = users_table.insert().values(
                UserName=user_profile['display_name'],
                LineID=user_profile['user_id'],
                PicUrl=user_profile['picture_url']
            )
            conn.execute(query)
            conn.close()
            return True  # 返回 True 表示插入成功
        except SQLAlchemyError as e:
            print(f"An error occurred while inserting user data: {str(e)}")
            conn.close()
            return f"An error occurred while inserting user data: {str(e)}"  
    return False  # 返回 False 表示连接数据库失败

@app.route('/testConDB', methods=['GET'])
def test_connect_to_database():
    conn = connect_to_database()
    if conn:
        conn.close()
        return jsonify({'message': 'Database connection successful'})
    else:
        return jsonify({'error': 'Failed to connect to the database'})


@app.route('/getCode', methods=['GET'])
def get_data():
    param1 = request.args.get('code')
    param2 = request.args.get('state')

    url = 'https://api.line.me/oauth2/v2.1/token'
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'authorization_code',
        'code': param1,
        'redirect_uri': 'https://pyhtonapi.onrender.com/getCode',
        'client_id': '2004230225',
        'client_secret': 'a6fad92e499be2a30bd6a9bb5d9f99f3'
    }

    try:
        response = requests.post(url, headers=headers, data=data)

        if response.status_code == 200:
            response_json = response.json()
            access_token = response_json.get('access_token')
            
            
            user_profile = get_user_profile(access_token)
            
            # 检查用户是否存在于数据库中
            '''
            if check_user_exists(user_profile['user_id']):
                # 如果用户存在，则从数据库中获取用户数据
                user_data = get_user_data_from_database(user_profile['user_id'])
                return "user already in"
            else:
                # 如果用户不存在，则将用户数据插入到数据库中
                return insert_user_to_database(user_profile)
                user_data = user_profile
                return "no user"

            # 直接返回用户数据
            '''
            return jsonify(user_data)
        else:
            print(f'Error: {response.status_code}, {response.text}')
            return jsonify({'error': 'Failed to get access token'}), 500
    except requests.RequestException as e:
        print(f'Request Error: {e}')
        return jsonify({'error': 'Failed to send request'}), 500

def get_user_profile(access_token):
    url = 'https://api.line.me/v2/profile'
    headers = {
        'Authorization': f'Bearer {access_token}'
    }

    try:
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            response_json = response.json()
            user_id = response_json.get('userId')
            display_name = response_json.get('displayName')
            picture_url = response_json.get('pictureUrl')
            response_data = {
                'user_id': user_id,
                'display_name': display_name,
                'picture_url': picture_url
            }
            return response_data
        else:
            print(f'Error: {response.status_code}, {response.text}')
            return {'error': 'Failed to get user profile'}
    except requests.RequestException as e:
        print(f'Request Error: {e}')
        return {'error': 'Failed to send request'}




@app.route('/insert_data', methods=['POST'])
def insert_data():

    try:
        param = {
            'drv': "ODBC Driver 17 for SQL Server",
            'uid': "sa",
            'pwd': "ji3ao6u.3au/6y4",
            'srv': "210.240.202.114",  # IP
            'ins': "",
            'pno': 1443,
            'db': 'Trash',  
            'table': 'test'   
        }

        const_str = f"mssql+pyodbc://{param['uid']}:{param['pwd']}@{param['srv']}{param['ins']}:{param['pno']}/{param['db']}?driver={param['drv']}"
        engine = create_engine(const_str, fast_executemany=True)

        metadata = MetaData()

        test = Table('test',metadata,
            Column('TEST',String)
        )

        metadata.create_all(engine)

        # 抓取 POST 的 JSON 数据
        data = request.json

        # 解析 JSON，提取需要的字段数据
        test_value = data.get('TEST')

        query = f"INSERT INTO {param['table']}(TEST) VALUES (:test_value)"

        with engine.connect() as connection:
            connection.execute(text(query), {'test_value': test_value})
            connection.commit()
        
        '''

        # 准备参数化查询
       # query = "INSERT INTO test(TEST) VALUES ('aa')"
        query = f"INSERT INTO {param['table']}(TEST) VALUES (': test_value')"
 
        # 执行 SQL 语句
        with engine.connect() as connection:
            result = connection.execute(text(query), {'test_value': test_value})
        '''

        
        return jsonify({'status': 'success', 'message': 'Data inserted successfully '})
    except Exception as e:
        
        return jsonify({'status': 'error', 'message': str(e)}), 500
    
@app.route('/get_data', methods=['GET'])
def read_data():  
    try:
        param = {
            'drv': "ODBC Driver 17 for SQL Server",
            'uid': "sa",
            'pwd': "ji3ao6u.3au/6y4",
            'srv': "210.240.202.114",  # IP
            'ins': "",
            'pno': 1443,
            'db': 'Trash',  #f資料庫
            'table': 'test'  # 資料表
        }
        data_list = []

        const_str = f"mssql+pyodbc://{param['uid']}:{param['pwd']}@{param['srv']}{param['ins']}:{param['pno']}/{param['db']}?driver={param['drv']}"
        engine = create_engine(const_str, fast_executemany=True)
        query = f"SELECT top 100 * FROM {param['table']}"
        df = pd.read_sql(query, engine)
        
        # 将DataFrame转换为字典列表
        data_list = df.to_dict(orient='records')

        return jsonify(data_list)  #回傳json
    except Exception as e:
        error_subject = "Python 脚本错误"
        error_message = f"脚本发生错误:\n\n{str(e)}"

@app.route('/helloworld', methods=['GET'])
def hello():  
    return "22"
    
if __name__ == '__main__':
    app.run(debug=True)
