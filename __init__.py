from flask import Flask, render_template, request

from rct.models import db, Vlan, Address
import rct.models


app = Flask(__name__, instance_relative_config=True)

# Читаем config
app.config.from_pyfile("config_ins.py")


# Инициализируем объект приложения
db.init_app(app)

# создаем все таблица в БД
db.create_all(app=app)

@app.route('/')
def main():
    return render_template("index.html")


@app.route('/vlans', methods = ['POST', 'GET'])
def addvlans():
    list_address = db.session.query(Address).all()
    list_vlans = db.session.query(Vlan).all()
    if request.method == "POST":
        try:
            addr = db.session.query(Address).filter_by(small_address=request.form['addrlist']).one()
            vlan = Vlan(id_vl=request.form['addvlanid'], name=request.form['addvlanname'], address_id = addr.id)
            db.session.add(vlan)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления адреса в базу")


    return render_template("vlans.html", list_address = list_address, list_vlans = list_vlans)

@app.route('/address', methods = ['POST', 'GET'])
def addaddress():
    if request.method == "POST":
        try:
            address = Address(small_address = request.form['small_address'], rgis_address = request.form['rgis_address'])
            db.session.add(address)
            db.session.flush()
            db.session.commit()
        except:
            db.session.rollback()
            print("Ошибка добавления адреса в базу")

    return render_template("address.html")

if __name__ == "__main__":
    app.run(debug = True)  # на этапе разработке True