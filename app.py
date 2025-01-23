from flask import Flask,render_template,request,redirect,flash,url_for
import sqlite3 as sql

app=Flask(__name__)
app.secret_key="admin123" #this is used for secure the session and cookies.


# Types of Parameter:

# @app.route("/parameter/<username>")
# def parameter(username ):
#     return render_template("parameter.html",username1=username)


# @app.route('/post/<int:post_id>/cmt/<int:cmt_id>')
# def show_comment(post_id,cmt,cmt_id):
#     return f'Post ID: {post_id},cmd {cmt} Comment ID: {cmt_id}'







@app.route("/")
@app.route("/index")
def index():
    con=sql.connect("database.db")
    # then con-(connection-kku row factory nu oru attribute namma set pannalam edhukkuna database table la irundhu namakku kidaikkira ella values hu tuple value ha than kidaikkum like tuple index(0,1) so adha print pandrathu konjam kastama irukkum so namma "row_factory" nu oru attribute onnu use panna namakku table la irukka value namakku column name oda sendhu varum so namma value print kku column.value va easy ha print pannalam. )
    con.row_factory=sql.Row #this is fetch the value from user table and that value stored like column_name.value va enakku eduthuttu varum.
    cur=con.cursor()
    cur.execute("select * from user_table")
    data=cur.fetchall()

    return render_template("index.html", datas=data)
    # return "<h1>hello<h1>"

@app.route("/add_user",methods=["POST","GET"])
def add_user():
    if request.method=="POST":
        uname=request.form["uname"]
        contact=request.form["contact"]

        con=sql.connect("database.db")
        cur=con.cursor()

        cur.execute("CREATE TABLE IF NOT EXISTS user_table(UID INTEGER PRIMARY KEY AUTOINCREMENT,username VARCHAR(20),contact VARCHAR(10) PRIMARY KEY)")
        cur.execute("insert into user_table(username,contact)values(?,?)",(uname,contact))
         
        con.commit()
        con.close() #this is best practice and avoid the database lock error..... ("where is start the database lock error : 1. Unclosed Database Connections,2. Long-Running or Uncommitted Transactions,3. Multiple Connections or Threads,4. Incorrect File Permissions")
        # yield "User Added Successfully"
        # flash("User added")
        # flash("Success")
        return redirect("/index")

    return render_template("add_user.html")
  
@app.route("/edit_user/<string:uid>",methods=["POST","GET"])
def edit_user(uid):
    if request.method=="POST":
        uname=request.form["uname"]
        contact=request.form["contact"]

        con=sql.connect("database.db")
        cur=con.cursor()

        cur.execute("update user_table SET username=?,contact=? where UID=?",(uname,contact,uid))        
        con.commit()
        con.close() #this is best practice and avoid the database lock error..... ("where is start the database lock error : 1. Unclosed Database Connections,2. Long-Running or Uncommitted Transactions,3. Multiple Connections or Threads,4. Incorrect File Permissions")
        
        # flash("User added")
        flash("Success")
        return redirect("/index")

    con=sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from user_table Where UID=?",(uid,))
    data=cur.fetchone()
    return render_template("edit_user.html",datas=data)

@app.route("/delete_user/<int:uid>",methods=["POST","GET"])
def delete_user(uid):    
    con=sql.connect("database.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("DELETE from user_table where UID=?",(uid,))
    con.commit()
    con.close()
    return redirect("/index")

if __name__=="__main__":
    app.run(debug=True)