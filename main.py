import sqlite3
import os

dbConn = None

def dbConnection():
    global dbConn
    if not os.path.exists("Database"):
        os.makedirs("Database")
    dbConn = sqlite3.connect("Database/test.db")

def createTable():
    if dbConn is None: dbConnection()
    dbCursor = dbConn.cursor()
    # 確保資料表存在，且包含所有欄位
    sqlStr = """CREATE TABLE IF NOT EXISTS Students (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                name TEXT NOT NULL, 
                gender TEXT NOT NULL, 
                department TEXT NOT NULL, 
                email TEXT NOT NULL, 
                phone TEXT NOT NULL, 
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP, 
                address TEXT); """
    dbCursor.execute(sqlStr)
    dbConn.commit()

# --- 對齊輔助工具 ---
def get_display_width(s):
    width = 0
    for char in str(s):
        if '\u4e00' <= char <= '\u9fff': width += 2
        else: width += 1
    return width

def pad_s(s, target):
    s = str(s) if s is not None else ""
    return s + " " * max(0, (target - get_display_width(s)))

# --- 功能實作區 ---

def insert_student():
    print("\n--- 新增學生資料 ---")
    name = input("姓名: ")
    gender = input("性別: ")
    dept = input("系所: ")
    email = input("Email: ")
    
    # --- 電話驗證開始 ---
    while True:
        phone = input("電話 (必填): ")
        if phone.strip():  # .strip() 去掉空格後，如果有內容
            break          # 跳出迴圈，繼續輸入地址
        else:
            print("錯誤：電話欄位不能為空，請重新輸入！")
    # --- 電話驗證結束 ---
    
    addr = input("地址: ")
    
    dbCursor = dbConn.cursor()
    dbCursor.execute(
        "INSERT INTO Students (name, gender, department, email, phone, address) VALUES (?, ?, ?, ?, ?, ?)",
        (name, gender, dept, email, phone, addr)
    )
    dbConn.commit()
    print(f"學生 {name} 已成功新增。")

def select_all_students():
    print(f"\n===學生資料列表 ===")
    dbCursor = dbConn.cursor()
    dbCursor.execute("SELECT * FROM Students")
    rows = dbCursor.fetchall()
    
    if not rows:
        print("目前沒有任何紀錄。")
        return

    # 定義欄位寬度: ID(4), 姓名(10), 性別(6), 系所(12), 電話(12), 地址(20)
    w = [4, 10, 6, 12, 25, 12, 25]
    header = f"{pad_s('ID',w[0])} | {pad_s('姓名',w[1])} | {pad_s('性別',w[2])} | {pad_s('系所',w[3])} | {pad_s('Email',w[4])} | {pad_s('電話',w[5])} | {pad_s('地址',w[6])}"
    print(header)
    print("-" * get_display_width(header))

    for r in rows:
        # 注意：地址在 row[7]，電話在 row[5]
        line = f"{pad_s(r[0],w[0])} | {pad_s(r[1],w[1])} | {pad_s(r[2],w[2])} | {pad_s(r[3],w[3])} | {pad_s(r[4],w[4])} | {pad_s(r[5],w[5])} | {pad_s(r[7],w[6])}"
        print(line)

def update_student():
    select_all_students()
    target_id = input("\n請輸入欲修改的學生 ID: ")
    new_phone = input("新電話 (不改請按 Enter): ")
    new_addr = input("新地址 (不改請按 Enter): ")
    
    dbCursor = dbConn.cursor()
    if new_phone:
        dbCursor.execute("UPDATE Students SET phone = ? WHERE id = ?", (new_phone, target_id))
    if new_addr:
        dbCursor.execute("UPDATE Students SET address = ? WHERE id = ?", (new_addr, target_id))
    dbConn.commit()
    print("修改完成。")

def delete_student():
    select_all_students()
    target_id = input("\n請輸入欲刪除的學生 ID: ")
    confirm = input(f"確定要刪除 ID {target_id} 嗎？(y/n): ").lower()
    if confirm == 'y':
        dbCursor = dbConn.cursor()
        dbCursor.execute("DELETE FROM Students WHERE id = ?", (target_id,))
        dbConn.commit()
        print("資料已移除。")

# --- 主程式進入點 ---

def main():
    dbConnection()
    createTable()
    
    while True:
        print("\n===== 學生管理系統 =====")
        print("1. 新增 (Insert)")
        print("2. 列表 (Select All)")
        print("3. 修改 (Update)")
        print("4. 刪除 (Delete)")
        print("0. 離開")
        choice = input("請選擇功能: ")

        if choice == '1': insert_student()
        elif choice == '2': select_all_students()
        elif choice == '3': update_student()
        elif choice == '4': delete_student()
        elif choice == '0': break
        else: 
            print("輸入錯誤。")

    if dbConn: 
        dbConn.close()

if __name__ == "__main__":
    main()