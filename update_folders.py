#!/usr/bin/python3

import os
import sqlite3

if __name__ == '__main__':
    conn = sqlite3.connect('folders.db')
    db = conn.cursor()
    db.execute("DROP TABLE IF EXISTS folders")
    db.execute("CREATE TABLE folders (folder varchar(255), folder_id bigint(20), root_id bigint(20))")
    db.execute("INSERT INTO folders (folder, folder_id, root_id) values ('/', 1, 0)")

    root_path = os.path.dirname(os.path.realpath(__file__))
    data_dir = root_path + '/data'

    s = 1
    for n in range(1, 50):
        for line in [i for i in os.popen("find " + data_dir + " -maxdepth " + str(n) + " -mindepth " + str(n) + " -type d -printf '/%P\n' | sort").read().split('\n') if i]:
            s += 1
            name = line.split('/')[-1]
            root = line[0:line.rfind('/')] if line[0:line.rfind('/')] else '/'
            db.execute("SELECT folder_id FROM folders WHERE folder = '%s'"%(root))
            root_id = db.fetchone()[0]
            db.execute("INSERT INTO folders (folder, folder_id, root_id) VALUES ('%s',%s,%s)"%(line, str(s), str(root_id)))

    conn.commit()
    conn.close()
