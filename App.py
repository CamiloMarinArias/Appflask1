from flask import Flask, render_template , request , redirect, url_for , flash
from flask_mysqldb import MySQL

app = Flask(__name__)
#Mysql conexion
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '1234'
app.config['MYSQL_DB'] = 'flaskcontacts'
mysql = MySQL(app)


#configuraciones
app.secret_key = 'mysecreatkey'

@app.route('/')
def Index():
    cur=mysql.connection.cursor()
    cur.execute('SELECT * FROM contacts')
    data = cur.fetchall()
    return render_template('index.html', contacts = data)

@app.route('/add_contact', methods=['POST'])
def add_contact():
    if request.method == 'POST':
        nombrecompleto = request.form['nombrecompleto']
        telefono = request.form['telefono']
        mail = request.form['mail']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO contacts (nombrecompleto, telefono, mail) VALUES (%s,  %s, %s)',
        (nombrecompleto, telefono, mail))
        mysql.connection.commit()
        flash('Contacto Agragado Satisfactoriamente.')
        return redirect(url_for('Index'))



@app.route('/edit/<id>')
def get_contact(id):
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM contacts WHERE id = %s', (id,) )
        data = cur.fetchall()
        return render_template('edit-contact.html' , contact = data [0])

@app.route('/update/<id>', methods =['POST'])
def update_contact(id):
    if request.method == 'POST':
        nombrecompleto = request.form['nombrecompleto']
        telefono = request.form['telefono']
        mail = request.form['mail']
        cur = mysql.connection.cursor()
        cur.execute(""" 
        UPDATE contacts
        SET nombrecompleto = %s,
            telefono = %s,
            mail = %s
        WHERE id = %s
       """, (nombrecompleto, telefono, mail, id))
        flash('Contacto Actualizado Correctamente.')
        mysql.connection.commit()
        return redirect(url_for('Index'))

@app.route('/delete/<string:id>')
def delete_contact(id):
  cur= mysql.connection.cursor()
  cur.execute('DELETE FROM contacts WHERE id = {0}'.format(id))
  mysql.connection.commit()
  flash('Contacto Removido Correctamente.')
  return redirect(url_for('Index'))

if __name__== '__main__':
    app.run(port= 3000, debug= True)