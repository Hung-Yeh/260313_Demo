import sqlite3
import os

dbConn = None

def dbConnection():
    global dbConn
    # 確保 Database 資料夾存在
    if not os.path.exists("Database"):
        os.makedirs("Database")
    dbConn = sqlite3.connect("Database/test.db")

def createTable():
    if dbConn is None: 
        dbConnection()
    dbCursor = dbConn.cursor()
    sqlStr = """CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL, 
                gender TEXT NOT NULL, 
                department TEXT NOT NULL, 
                email TEXT NOT NULL, 
                phone TEXT NOT NULL, 
                address TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP); """
    dbCursor.execute(sqlStr)
    dbConn.commit()

# --- 功能實作區 ---

def insert_student():
    print("\n--- 新增學生資料 ---")
    name = input("姓名: ")
    gender = input("性別: ")
    dept = input("科系: ")
    email = input("Email: ")
    phone = input("電話: ")
    address = input("地址: ")
    
    dbCursor = dbConn.cursor()
    dbCursor.execute(
        "INSERT INTO Students (name, gender, department, email, phone, address) VALUES (?, ?, ?, ?, ?, ?)",
        (name, gender, dept, email, phone, address)
    )
    dbConn.commit()
    print(f"學生 {name} 已成功新增。")

def select_all_students():
    print("\n--- 所有學生紀錄 ---")
    dbCursor = dbConn.cursor()
    dbCursor.execute("SELECT * FROM Students")
    rows = dbCursor.fetchall()
    
    if not rows:
        print("目前沒有任何紀錄。")
        return

    print(f"{'ID':<3} | {'姓名':<10} | {'電話':<12} | {'地址'}")
    print("-" * 50)
    for row in rows:
        # row[0]=id, row[1]=name, row[5]=phone, row[6]=address
        print(f"{row[0]:<3} | {row[1]:<10} | {row[5]:<12} | {row[6]}")

def update_student():
    select_all_students()
    target_id = input("\n請輸入要修改的學生 ID: ")
    new_phone = input("請輸入新電話 (若不修改請直接按 Enter): ")
    new_address = input("請輸入新地址 (若不修改請直接按 Enter): ")
    
    dbCursor = dbConn.cursor()
    if new_phone:
        dbCursor.execute("UPDATE Students SET phone = ? WHERE id = ?", (new_phone, target_id))
    if new_address:
        dbCursor.execute("UPDATE Students SET address = ? WHERE id = ?", (new_address, target_id))
    
    dbConn.commit()
    print("資料更新成功！")

def delete_student():
    select_all_students()
    target_id = input("\n請輸入要刪除的學生 ID: ")
    
    # 二次確認 (Y/N) 邏輯
    confirm = input(f"確定要刪除 ID 為 {target_id} 的資料嗎？(y/n): ").lower()
    if confirm == 'y':
        dbCursor = dbConn.cursor()
        dbCursor.execute("DELETE FROM Students WHERE id = ?", (target_id,))
        dbConn.commit()
        print("資料已移除。")
    else:
        print("刪除操作已取消。")

# --- 主選單 ---

def main():
    dbConnection()
    createTable()
    
    while True:
        print("\n===== 學生資料管理系統 =====")
        print("1. 新增 (Insert)")
        print("2. 列表 (Select All)")
        print("3. 修改 (Update)")
        print("4. 刪除 (Delete)")
        print("0. 離開系統")
        choice = input("請選擇功能: ")

        if choice == '1':
            insert_student()
        elif choice == '2':
            select_all_students()
        elif choice == '3':
            update_student()
        elif choice == '4':
            delete_student()
        elif choice == '0':
            print("系統已結束。")
            break
        else:
            print("無效的選擇，請重新輸入。")

    if dbConn:
        dbConn.close()

if __name__ == "__main__":
    main()