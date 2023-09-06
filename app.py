import json
import sqlite3
from flask import request
from flask import Flask, render_template, jsonify
app = Flask(__name__)


@app.route('/')
def index():
    # empty the root_to_curr.txt file whenever index.html is loaded
    # it is called whenever users load the index.html
    # output: render index.html
    f = open("root_to_curr.txt", 'r+')
    f.truncate(0)
    return render_template('index.html')


@app.route('/tree.html', methods=["POST", "GET"])
def tree():
    # load the page tree.html
    # it is called when users clicked submit button the index.html
    # output: render the tree.html
    return render_template('tree.html')


@app.route('/root_to_curr', methods=['POST'])
def root_to_curr():
    # saving the path from root to current node as a txt file
    # it is called after users answer the question of the box, and when the new box appreas
    # output: the variable storing the path
    output = request.get_json()
    print(output)
    print(type(output))
    result = json.loads(output)
    print(result)
    print(type(result))

    f = open('root_to_curr.txt', 'a')
    for i in range(len(result)):
        i_str = str(i)
        if '-' not in result[i_str]:
            f.write('\n')
        f.write(result[i_str])
        f.write('\n')

    return result


@app.route('/root_to_keyword', methods=['POST'])
def root_to_desired():
    # saving the path from root to the box containing keyword as a txt file
    # it is called when the users search a box through keyword
    # output: the variable storing the path
    output = request.get_json()
    print(output)
    print(type(output))
    result = json.loads(output)
    print(result)
    print(type(result))

    f = open('root_to_keyword.txt', 'w')
    for i in range(len(result)):
        i_str = str(i)
        f.write(result[i_str])
        f.write('\n')

    return result


@app.route('/get_subtree', methods=['POST'])
def get_subtree():
    # saving the subtree as a txt file
    # it is called when users click the radio button "Nodes reachable from the path/tree so far", and then click "submit"
    # output: the variable storing th path result
    output = request.get_json()
    print(output)
    print(type(output))
    result = json.loads(output)
    print(result)
    print(type(result))

    f = open('root_to_keyword.txt', 'a')
    for i in range(len(result)):
        i_str = str(i)
        f.write(result[i_str])
        f.write('\n')

    f.write('\n')
    return result


@app.route('/get_sql', methods=['POST'])
def get_sql():
    # connect to the database, create a table in the database(I have commented it, so it won't create duplicate table),
    # and execute the sql command sent from the tree.js through ajax.
    # it is called when the text in the new box is a sql command.
    # output: send the result of the sql command back to tree.js
    output = request.get_json()
    print(output)
    print(type(output))
    result = json.loads(output)
    print(result)
    print(type(result))

    # connecting to the database
    connection = sqlite3.connect("dt.db")

    # cursor
    crsr = connection.cursor()

    # print statement will execute if there
    # are no errors
    print("Connected to the database")

    sql_command = """CREATE TABLE IF NOT EXISTS houses (
    house_number INTEGER PRIMARY KEY AUTOINCREMENT,
    house_name TEXT,
    num_of_bedrooms INTEGER,
    square_feet INTEGER,
    swimming_pool CHAR(1));"""
    crsr.execute(sql_command)

    # SQL command to insert the data in the table
    sql_command = """INSERT INTO houses (house_name, num_of_bedrooms, square_feet, swimming_pool) VALUES (?, ?, ?, ?);"""
    crsr.execute(sql_command, ("Goddard Hall", 1, 1600, 'N'))
    crsr.execute(sql_command, ("Palladium Hall", 2, 3100, 'Y'))
    crsr.execute(sql_command, ("Lipton Hall", 3, 3300, 'N'))

    # Commit changes
    connection.commit()

    crsr.execute(result['0'])
    sql_ans = crsr.fetchall()

    for i in sql_ans:
        print(i)

    # close the connection
    connection.close()

    return jsonify('', render_template('sql.html', x=sql_ans))

    # # Create Property table
    # sql_command = """
    # CREATE TABLE IF NOT EXISTS Property (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     legal_description TEXT NOT NULL,
    #     address TEXT,
    #     size REAL,
    #     age INTEGER
    # );
    # """
    # crsr.execute(sql_command)
    #     # Create ComparableSales table
    # sql_command = """
    # CREATE TABLE [IF NOT EXISTS] ComparableSales (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     property_id INTEGER,
    #     comparable_address TEXT,
    #     sale_date TEXT,
    #     sale_price REAL,
    #     FOREIGN KEY (property_id) REFERENCES Property(id)
    # );
    # """
    # crsr.execute(sql_command)
    # # Create AppraisalMethodology table
    # sql_command = """
    # CREATE TABLE [IF NOT EXISTS] AppraisalMethodology (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     property_id INTEGER,
    #     methodology_type TEXT CHECK(methodology_type IN ('Comparables Approach', 'Cost Approach', 'Income Approach')),
    #     FOREIGN KEY (property_id) REFERENCES Property(id)
    # );
    # """
    # crsr.execute(sql_command)
    # # Create FinalValuation table
    # sql_command = """
    # CREATE TABLE [IF NOT EXISTS] FinalValuation (
    #     id INTEGER PRIMARY KEY AUTOINCREMENT,
    #     property_id INTEGER,
    #     estimated_value REAL,
    #     valuation_date TEXT,
    #     FOREIGN KEY (property_id) REFERENCES Property(id)
    # );
    # """
    # crsr.execute(sql_command)

    # # Insert sample data
    # sql_command = """
    # INSERT INTO Property (legal_description, address, size, age) VALUES ('Legal Description Here', '123 Main St, City, Country', 2000, 10);
    # """
    # crsr.execute(sql_command)


if __name__ == "__main__":
    app.run(debug=True)
