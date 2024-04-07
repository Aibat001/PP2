import psycopg2


def add_user():
    print("How many users you want to insert")
    n = int(input())

    flag = True
    uncorrect = []
    updated = []

    add_flag = False

    cursor.execute("SELECT * FROM phonebook ")
    table = cursor.fetchall()
    while n >= 1:
        add = input().split()
        n -= 1
        correct_number = False
        for i in add[1]:
            if i >= '0' and i <= '9':
                correct_number = True
            else:
                correct_number = False
                break
        if correct_number == False:
            uncorrect.append(add)
        flag_mult = True
        for row in table:
            if add[0] == row[0] and correct_number == True:
                postgre_query = """UPDATE phonebook SET phonenumber = %s WHERE user_name = %s """
                cursor.execute(postgre_query, (add[1], add[0]))
                conn.commit()
                flag_mult = False
                updated.append(add)
                add_flag = True
        if flag_mult and correct_number == True:
            data_toinsert = (add[0], add[1])
            postgre_query = """INSERT INTO phonebook( user_name, phonenumber) VALUES (%s, %s) """
            cursor.execute(postgre_query, data_toinsert)
            conn.commit()
            add_flag = True
    if len(updated) > 0:
        print('\nUpdated numbers')
        for i in updated:
            print(i[0] + ' ' + i[1])
    if len(uncorrect) > 0:
        print("\nUnappropriate numbers:")
        for i in uncorrect:
            print(i[0] + ' ' + i[1])
    if add_flag:
        print("\nData added!")


def fetch_users():
    print("How many user you want to see")
    n = input()
    i = 0
    if n == 'all':
        print(
            "   ID    |             Names           |        Number\n-------------------------------------------------------------------")
        str = "SELECT * FROM phonebook"
        cursor.execute(str)
        table = cursor.fetchall()
        for row in table:
            i += 1
            print("{0:1}{1:4}{2:15}{3:23}{4:5}{5:35}".format(" ", i, " ", row[0], " ", row[1]))
    else:
        print(
            "ID    |             Names           |        Number\n-------------------------------------------------------------------")
        str = "SELECT * FROM phonebook LIMIT {}".format(n)
        cursor.execute(str)
        table = cursor.fetchall()
        for row in table:
            i += 1
            print("{0:1}{1:3}{2:15}{3:23}{4:3}{5:35}".format(" ", i, " ", row[0], " ", row[1]))


def update():
    print("Type who's number you want to change")
    name = input()
    print("New number")
    number = input()
    postgre_query = """UPDATE phonebook SET phonenumber = %s WHERE user_name = %s """
    cursor.execute(postgre_query, (number, name))

    conn.commit()
    print("Data updated!")


def find():
    print("Insert name who's number you want to see")
    name = input()
    cursor.execute("SELECT * FROM phonebook ")
    table = cursor.fetchall()
    for row in table:
        if name == row[0]:
            c = row[0] + " " + row[1]
            print(c)


def delete_user():
    print("Insert name you want to delete")
    name = input()
    postgre_query = """DELETE FROM phonebook WHERE user_name = %s """
    cursor.execute(postgre_query, (name,))

    conn.commit()
    print("Data deleted!")


try:
    cond = False
    conn = psycopg2.connect("dbname=postgres user=postgres password=1994almaZ_")
    cursor = conn.cursor()

    while not cond:
        print(
            "\nChoose action:\n1.Add user and number\n2.Change number of existing user\n3.Delete user\n4.Find number by name\n5.Show names and numbers\n6.Exit")
        action = input()
        if action == '1':
            print("Insert data")
            add_user()
        elif action == '2':
            update()
        elif action == '3':
            delete_user()
        elif action == '4':
            find()
        elif action == '5':
            fetch_users()
        elif action == '6':
            cond = True

except psycopg2.Error as e:
    print("Failed!")

finally:
    cursor.close()
    conn.close()
    print("Connection closed!")