import json
import sqlite3
from flask import request
from flask import Flask, render_template, jsonify
import csv
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

    # print statement will execute if there are no errors
    print("Connected to the database")


    sql_command = """CREATE TABLE IF NOT EXISTS houses (
    house_number INTEGER PRIMARY KEY AUTOINCREMENT,
    house_name TEXT,
    num_of_bedrooms INTEGER,
    square_feet INTEGER,
    swimming_pool CHAR(1));"""
    crsr.execute(sql_command)
    
    # SQL command to insert the data in the table
    # sql_command = """INSERT INTO houses (house_name, num_of_bedrooms, square_feet, swimming_pool) VALUES (?, ?, ?, ?);"""
    # crsr.execute(sql_command, ("Goddard Hall", 1, 1600, 'N'))
    # crsr.execute(sql_command, ("Palladium Hall", 2, 3100, 'Y'))
    # crsr.execute(sql_command, ("Lipton Hall", 3, 3300, 'N'))

    # sql_command = """DROP TABLE IF EXISTS comparableApproach;"""
    # crsr.execute(sql_command)

    sql_command = """CREATE TABLE IF NOT EXISTS comparableInfo (
    house_number INTEGER PRIMARY KEY AUTOINCREMENT,
    zip INTEGER,
    sale_price INTEGER,
    house_square_footage INTEGER,
    bedrooms INTEGER);"""
    crsr.execute(sql_command)

    with open('comparables_dataset.csv', 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)  # Skip header row

        # sql_insert_command = """INSERT INTO comparableInfo (zip, sale_price, house_square_footage, bedrooms) 
        #                         VALUES (?, ?, ?, ?, ?, ?);"""

        for row in csv_reader:
            zip = int(row[0])  # 'zipcode' column
            sale_price = int(row[1])  # 'price' column
            house_square_footage = int(row[2])  # 'sqft_living' column
            bedrooms = int(row[3])  # 'bedrooms' column

            crsr.execute("""INSERT INTO comparableInfo (zip, sale_price, house_square_footage, bedrooms) 
                                VALUES (?, ?, ?, ?, ?, ?);""", (zip, sale_price, house_square_footage, bedrooms))

    # sql_command = """INSERT INTO comparableInfo (address, zip_code, sale_price, house_square_footage, bedroom_nums, bathroom_nums, amenities_cost) VALUES (?, ?, ?, ?, ?, ?, ?);"""
    # crsr.execute(sql_command, ("57 Saxton St. Brooklyn, NY 11207", 11207, 500000, 1600, 3, 2, 50000))
    # crsr.execute(sql_command, ("9263 North Dunbar Street Jamaica, NY 11434", 11207,400000, 1500, 3, 2.5, 0))    
    # crsr.execute(sql_command, ("64 Foster St. Rego Park, NY 11374", 11207, 900000, 2000, 4, 3, 100000))

    
    sql_command = """CREATE TABLE IF NOT EXISTS costApproach (
    lot_value INTEGER, 
    replacement_cost_of_improvements INTEGER,
    depreciation REAL);"""
    crsr.execute(sql_command)

    
    # sql_command = """INSERT INTO costApproach (lot_value, replacement_cost_of_improvements, depreciation) VALUES (?, ?, ?)"""
    # crsr.execute(sql_command, (100000, 200000, 0.05))
    # crsr.execute(sql_command, (150000, 220000, 0.03))
    # crsr.execute(sql_command, (200000, 250000, 0.04))
    # crsr.execute(sql_command, (175000, 230000, 0.06))
    # crsr.execute(sql_command, (120000, 210000, 0.02))
    # crsr.execute(sql_command, (160000, 260000, 0.07))
    # crsr.execute(sql_command, (130000, 215000, 0.05))
    # crsr.execute(sql_command, (110000, 190000, 0.01))
    # crsr.execute(sql_command, (140000, 225000, 0.03))
    # crsr.execute(sql_command, (125000, 240000, 0.04))
    # crsr.execute(sql_command, (190000, 270000, 0.02))
    # crsr.execute(sql_command, (180000, 260000, 0.03))
    # crsr.execute(sql_command, (170000, 245000, 0.05))
    # crsr.execute(sql_command, (135000, 205000, 0.06))
    # crsr.execute(sql_command, (145000, 230000, 0.07))
    # crsr.execute(sql_command, (115000, 220000, 0.01))
    # crsr.execute(sql_command, (155000, 250000, 0.02))
    # crsr.execute(sql_command, (165000, 265000, 0.04))
    # crsr.execute(sql_command, (105000, 200000, 0.03))
    # crsr.execute(sql_command, (195000, 280000, 0.05))
    # crsr.execute(sql_command, (185000, 275000, 0.01))
    # crsr.execute(sql_command, (210000, 290000, 0.02))
    # crsr.execute(sql_command, (205000, 300000, 0.06))
    # crsr.execute(sql_command, (215000, 310000, 0.04))
    # crsr.execute(sql_command, (220000, 320000, 0.07))
    # crsr.execute(sql_command, (230000, 330000, 0.01))
    # crsr.execute(sql_command, (240000, 340000, 0.02))
    # crsr.execute(sql_command, (250000, 350000, 0.03))
    # crsr.execute(sql_command, (260000, 360000, 0.05))
    # crsr.execute(sql_command, (270000, 370000, 0.06))
    # crsr.execute(sql_command, (280000, 380000, 0.04))
    # crsr.execute(sql_command, (290000, 390000, 0.07))
    # crsr.execute(sql_command, (300000, 400000, 0.01))
    # crsr.execute(sql_command, (310000, 410000, 0.02))
    # crsr.execute(sql_command, (320000, 420000, 0.03))
    # crsr.execute(sql_command, (330000, 430000, 0.05))
    # crsr.execute(sql_command, (340000, 440000, 0.06))
    # crsr.execute(sql_command, (350000, 450000, 0.04))
    # crsr.execute(sql_command, (360000, 460000, 0.07))
    # crsr.execute(sql_command, (370000, 470000, 0.01))
    # crsr.execute(sql_command, (380000, 480000, 0.02))
    # crsr.execute(sql_command, (390000, 490000, 0.03))
    # crsr.execute(sql_command, (400000, 500000, 0.05))
    # crsr.execute(sql_command, (410000, 510000, 0.06))
    # crsr.execute(sql_command, (420000, 520000, 0.04))
    # crsr.execute(sql_command, (430000, 530000, 0.07))
    # crsr.execute(sql_command, (440000, 540000, 0.01))
    # crsr.execute(sql_command, (450000, 550000, 0.02))
    # crsr.execute(sql_command, (460000, 560000, 0.03))
    # crsr.execute(sql_command, (470000, 570000, 0.05))
    # crsr.execute(sql_command, (480000, 580000, 0.06))    


    sql_command = """
    CREATE TABLE IF NOT EXISTS incomeApproach (
    comparable_monthly_rental_rates INTEGER,
    monthly_operating_costs INTEGER,
    capitalization_rate REAL);"""
    crsr.execute(sql_command)

    # sql_command = """INSERT INTO incomeApproach (comparable_monthly_rental_rates, monthly_operating_costs, capitalization_rate) VALUES(?, ?, ?)"""
    # crsr.execute(sql_command, (2000, 500, 0.05))
    # crsr.execute(sql_command, (3000, 800, 0.06))
    # crsr.execute(sql_command, (1800, 450, 0.07))
    # crsr.execute(sql_command, (2500, 600, 0.04))
    # crsr.execute(sql_command, (4000, 1000, 0.08))
    # crsr.execute(sql_command, (3200, 750, 0.05))    
    # crsr.execute(sql_command, (1500, 400, 0.03))
    # crsr.execute(sql_command, (3600, 900, 0.06))
    # crsr.execute(sql_command, (2700, 650, 0.07))
    # crsr.execute(sql_command, (2200, 550, 0.04))


    # Commit changes
    connection.commit()

    crsr.execute(result['0'])
    sql_ans = crsr.fetchall()

    for i in sql_ans:
        print(i)

    # close the connection
    connection.close()

    return jsonify('', render_template('sql.html', x=sql_ans))


@app.route('/input_query', methods=['POST'])
def input_query():
    data = request.get_json()
    input_number = data.get("userInput")
    query = data.get("query")    
    # Connect to SQLite database
    connection = sqlite3.connect("dt.db")
    crsr = connection.cursor()
    
    # Execute SQL query based on the input_number
    crsr.execute(query, (input_number,))
    result = crsr.fetchall()
    
    # Close the connection
    connection.close()
    
    return jsonify(result)




if __name__ == "__main__":
    app.run(debug=True)
