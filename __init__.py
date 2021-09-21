from flask import Flask, render_template, request, send_file

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


@app.route('/delvlans', methods = ['POST'])
def delvlans():
    #status = request.form['delbtn']
    try:
        vlanToDelete = Vlan.query.get(request.form['delbtn'])
        db.session.delete(vlanToDelete)
        db.session.flush()
        db.session.commit()
        status = "VLAN: "+ request.form['delbtn'] +" Успешно удален"
    except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления VLAN : " + request.form['delbtn']


    return  render_template("delvlans.html", status = status)


@app.route('/vlans', methods = ['POST', 'GET'])
def addvlans():
    list_address = db.session.query(Address).all()
    list_vlans = db.session.query(Vlan).order_by("id_vl").all()
    if request.method == "POST":
        try:
            addr = db.session.query(Address).filter_by(small_address=request.form['addrlist']).one()
            vlan = Vlan(id_vl=request.form['addvlanid'], name=request.form['addvlanname'], address_id = addr.id)
            db.session.add(vlan)
            db.session.flush()
            db.session.commit()
            list_vlans = db.session.query(Vlan).order_by("id_vl").all()
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

@app.route('/files', methods = ['POST'])
def downloadFile ():
    if request.form['btnfiles'] == 'downloadvlans':
        #For windows you need to use drive name [ex: F:/Example.pdf]
        path = "files/vlans.xlsx"
        return send_file(path, as_attachment=True)
    elif request.form['btnfiles'] == 'uploadvlans':
        print('OK')
        return "OK"


@app.route('/uploadvlans', methods = ['POST'])
def uploadsFileVlans ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = "/Examples.pdf"
    return send_file(path, as_attachment=True)




if __name__ == "__main__":
    app.run(debug = True)  # на этапе разработке True