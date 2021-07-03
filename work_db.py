import sqlite3
import datetime


#init db
def create_table():
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS reminders(
            id INTEGER PRIMARY KEY NOT NULL,
            date TEXT NOT NULL,
            time TEXT NOT NULL,
            text TEXT
        )
    """)
    conn.commit()
    conn.close()


#update print time of notes (after reboot)
def update_time():
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reminders;")
    notes = cursor.fetchall()
    out_array = {}
    for note in notes:
        timer = get_time(note[1] + ' ' + note[2])
        if timer < 0:
            del_note(note[0])
        else:
            out_array[note[0]] = timer
    conn.commit()
    conn.close()
    return out_array


#get print time of note (in sec)
def get_time(msg):
    time_note = datetime.datetime.strptime(msg, "%d.%m.%Y %H:%M")
    now = datetime.datetime.now()
    delta = time_note - now
    return(delta.total_seconds() // 1)
    

#add new note in db
def input_note(msg):
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    print('--add note--')
    words = msg.split()
    date_note, time_note = words[0], words[1]
    text = ' '.join(words[2:])
    cursor.execute("INSERT INTO reminders(date, time, text) VALUES (?, ?, ?)",(date_note, time_note, text))
    id_note = cursor.lastrowid
    date_and_time = words[0] + ' ' + words[1]
    conn.commit()
    conn.close()

    timer = get_time(date_and_time)
    return id_note, timer


#delete note (msg == id)
def del_note(msg):
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    print('--delete node--')
    sql_delete = """DELETE FROM reminders WHERE id = ?"""
    cursor.execute(sql_delete, (msg, ))
    conn.commit()
    conn.close()


#get text of one note
def out_text_note(msg):
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    sql_info = """SELECT text FROM reminders WHERE id = ?"""
    cursor.execute(sql_info, (msg, ))
    note = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return note


#output all notes from db
def out_notes():
    conn = sqlite3.connect('reminders.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM reminders;")
    out = '{0:4} | {1:10} | {2:5} | {3}'.format('id', 'date', 'time', 'text') +'\n'
    notes = cursor.fetchall()
    for note in notes:
        out = out + '{0:4} | {1:10} | {2:5} | {3}'.format(str(note[0]), str(note[1]), str(note[2]), str(note[3])) + '\n'
        
    print(out)
    conn.close()
    return out


if __name__ == '__main__':
    update_time()