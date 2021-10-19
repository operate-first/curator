import psycopg2, time, os


database_name = os.environ.get("DATABASE_NAME")
database_user = os.environ.get("DATABASE_USER")
database_password = os.environ.get("DATABASE_PASSWORD")
database_host_name = os.environ.get("DATABASE_HOST_NAME")
port = os.environ.get("PORT_NUMBER")


def execute_sql_commands(command):
    '''
        Execute the sql commands for table creation, stored procedures, functions, etc.,
        Args:
            string commands - sql command
    '''
    conn = None
    try:
        conn = psycopg2.connect(database=database_name, user=database_user,
                                password=database_password, host=database_host_name, port=port)  # postgres database connection string

        cursor = conn.cursor()
        
        cursor.execute(command)
        # commit the changes
        conn.commit()

        # close communication with the PostgreSQL database server
        cursor.close()

        
        
        print("The schema command is executed successfully")
    except Exception as exp:
        print("An error is occured while execute the sql commands {}".format(exp))
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__": 

    #print(os.listdir(os.path.dirname(__file__)))
    with open(os.path.join(os.path.dirname(__file__), 'generate_report.psql'), mode='r') as sql_cmd_file: 
        report = sql_cmd_file.read()
        execute_sql_commands(report)     
    with open(os.path.join(os.path.dirname(__file__), 'create_table.psql'), mode='r') as sql_cmd_file:
        report = sql_cmd_file.read()
        execute_sql_commands(report) 