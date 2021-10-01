from flask import Flask, request, jsonify
from postgres_interface import postgres_execute

app = Flask(__name__)


@app.route('/report')
def report():
    sql = 'select * from reports where 1 = 1 '
    for k, v in request.args.items():
        sql += " AND {} = '{}' ".format(k, v)
    print(sql)
    table = postgres_execute(sql, result=True)
    print(table)
    return jsonify(table)


if __name__ == '__main__':
    app.run()
