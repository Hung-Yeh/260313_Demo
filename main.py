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
                email TEXT NOT NULL UNIQUE, 
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
    
    # --- Email 重複檢查開始 ---
    while True:
        email = input("Email: ")
        if not email.strip():
            print("Email 不能為空！")
            continue
            
        dbCursor = dbConn.cursor()
        # 查詢資料庫中是否已有此 Email
        dbCursor.execute("SELECT * FROM Students WHERE email = ?", (email,))
        if dbCursor.fetchone():
            print(f"錯誤：Email '{email}' 已被使用，請輸入其他 Email！")
        else:
            break # 沒重複，跳出迴圈
    # --- Email 重複檢查結束 ---

    while True:
        phone = input("電話 (必填): ")
        if phone.strip():
            break
        print("電話不能為空！")
        
    addr = input("地址: ")
    
    dbCursor = dbConn.cursor()
    dbCursor.execute(
        "INSERT INTO Students (name, gender, department, email, phone, address) VALUES (?, ?, ?, ?, ?, ?)",
        (name, gender, dept, email, phone, addr)
    )
    dbConn.commit()
    print(f"學生 {name} 已成功新增。")

def show_department_stats():
    print(f"\n=== 各系人數統計 ===")
    if dbConn is None: dbConnection()
    dbCursor = dbConn.cursor()
    
    # 使用 SQL 的 GROUP BY 功能來統計各系人數
    sqlStr = """
        SELECT department, COUNT(*) 
        FROM Students 
        GROUP BY department 
        ORDER BY COUNT(*) DESC
    """
    dbCursor.execute(sqlStr)
    rows = dbCursor.fetchall()
    
    if not rows:
        print("目前沒有任何學生資料。")
        return

    # 定義顯示寬度
    w_dept = 15
    w_count = 6
    
    header = f"{pad_s('系所名稱', w_dept)} | {pad_s('人數', w_count)}"
    print(header)
    print("-" * get_display_width(header))
    
    total_students = 0
    for r in rows:
        dept_name = r[0]
        count = r[1]
        total_students += count
        print(f"{pad_s(dept_name, w_dept)} | {pad_s(count, w_count)} 人")
    
    print("-" * get_display_width(header))
    print(f"總計學生人數：{total_students} 人")

def search_students():
    print("\n=== 搜尋學生 (姓名或地址) ===")
    keyword = input("請輸入關鍵字: ")
    if not keyword.strip():
        print("關鍵字不能為空！")
        return

    if dbConn is None: dbConnection()
    dbCursor = dbConn.cursor()
    
    # 使用 LIKE 進行模糊搜尋，% 代表關鍵字前後可以有任何字元
    # 我們同時檢查 name 或是 address 欄位
    sqlStr = """
        SELECT * FROM Students 
        WHERE name LIKE ? OR address LIKE ?
    """
    search_pattern = f"%{keyword}%"
    dbCursor.execute(sqlStr, (search_pattern, search_pattern))
    rows = dbCursor.fetchall()
    
    if not rows:
        print(f"找不到包含 '{keyword}' 的相關紀錄。")
        return

    # 沿用你之前的對齊格式顯示結果
    w = [4, 10, 6, 12, 25, 12, 25]
    header = f"{pad_s('ID',w[0])} | {pad_s('姓名',w[1])} | {pad_s('性別',w[2])} | {pad_s('系所',w[3])} | {pad_s('Email',w[4])} | {pad_s('電話',w[5])} | {pad_s('地址',w[6])}"
    print(header)
    print("-" * get_display_width(header))

    for r in rows:
        line = f"{pad_s(r[0],w[0])} | {pad_s(r[1],w[1])} | {pad_s(r[2],w[2])} | {pad_s(r[3],w[3])} | {pad_s(r[4],w[4])} | {pad_s(r[5],w[5])} | {pad_s(r[7],w[6])}"
        print(line)
        
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
    
def view_student_detail():
    print("\n--- 查詢單筆詳細資訊 ---")
    target_id = input("請輸入學生 ID: ")
    if not target_id.strip():
        print("ID 不能为空！")
        return

    if dbConn is None: dbConnection()
    dbCursor = dbConn.cursor()
    
    # 根據 ID 進行精確查詢
    dbCursor.execute("SELECT * FROM Students WHERE id = ?", (target_id,))
    row = dbCursor.fetchone()
    
    if not row:
        print(f"找不到 ID 為 {target_id} 的學生。")
        return

    # 垂直排版顯示詳細資訊
    print("-" * 30)
    print(f"【 學 生 詳 細 資 料 】")
    print(f"系統 ID  : {row[0]}")
    print(f"姓    名 : {row[1]}")
    print(f"性    別 : {row[2]}")
    print(f"系    所 : {row[3]}")
    print(f"Email   : {row[4]}")
    print(f"電    話 : {row[5]}")
    print(f"建立時間 : {row[6]}")
    print(f"地    址 : {row[7]}")
    print("-" * 30)

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
        print("5. 統計 (Dept Stats)")
        print("6. 搜尋 (Search)")
        print("7. ID 詳細查詢 (View Detail)")
        print("0. 離開")
        choice = input("請選擇功能: ")

        if choice == '1': 
            insert_student()
        elif choice == '2': 
            select_all_students()
        elif choice == '3': 
            update_student()
        elif choice == '4': 
            delete_student()
        elif choice == '5': 
            show_department_stats()
        elif choice == '6':
            search_students()
        elif choice == '7': 
            view_student_detail()
        elif choice == '0': 
            break
        else: 
            print("輸入錯誤。")

    if dbConn: 
        dbConn.close()

if __name__ == "__main__":
    main()