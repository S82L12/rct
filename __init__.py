from flask import Flask, render_template, request, send_file, send_from_directory

from rct.models import db, Vlan, Address, Type
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
        idvlan = str(vlanToDelete.id_vl)
        db.session.delete(vlanToDelete)
        db.session.flush()
        db.session.commit()
        status = "VLAN ID : "+ idvlan +" Успешно удален"
    except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления VLAN ID : " + idvlan


    return  render_template("delvlans.html", status = status)

@app.route('/deltype', methods = ['POST'])
def deltype():
    #status = request.form['delbtn']
    try:
        typeToDelete = Type.query.get(request.form['delbtn'])
        statustypeToDelete = typeToDelete.type
        db.session.delete(typeToDelete)
        db.session.flush()
        db.session.commit()
        status = "Type: "+ statustypeToDelete +" Успешно удален"
    except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления TYPE : " + statustypeToDelete


    return  render_template("delitem.html", status = status)

@app.route('/deladdr', methods = ['POST'])
def deladdr():
    #status = request.form['delbtn']
    try:
        addrToDelete = Address.query.get(request.form['delbtn'])
        statusaddrToDelete = addrToDelete.small_address
        db.session.delete(addrToDelete)
        db.session.flush()
        db.session.commit()
        status = "Адрес: "+ statusaddrToDelete +" Успешно удален"
    except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления Адреса : " + statusaddrToDelete


    return  render_template("delitem.html", status = status)



@app.route('/vlans', methods = ['POST', 'GET'])
def addvlans():
    list_address = db.session.query(Address).all()
    list_vlans = db.session.query(Vlan).order_by("id_vl").all()
    list_type =  db.session.query(Type).all()
    if request.method == "POST":
        try:
            addr = db.session.query(Address).filter_by(small_address=request.form['addrlist']).one()
            type = db.session.query(Type).filter_by(type=request.form['typelist']).one()
            vlan = Vlan(id_vl=request.form['addvlanid'], name=request.form['addvlanname'], address_id = addr.id, type_id = type.id)
            db.session.add(vlan)
            db.session.flush()
            db.session.commit()
            list_vlans = db.session.query(Vlan).order_by("id_vl").all()
            list_type = db.session.query(Type).all()
        except:
            db.session.rollback()
            print("Ошибка добавления адреса в базу")



    return render_template("vlans.html", list_address = list_address, list_vlans = list_vlans, list_type = list_type)

@app.route('/address', methods = ['POST', 'GET'])
def addaddress():
    list_addreses = db.session.query(Address).order_by("small_address").all()
    if request.method == "POST":
        try:
            address = Address(small_address = request.form['small_address'], rgis_address = request.form['rgis_address'])
            db.session.add(address)
            db.session.flush()
            db.session.commit()
            list_addreses = db.session.query(Address).order_by("small_address").all()
        except:
            db.session.rollback()
            print("Ошибка добавления адреса в базу")

    return render_template("address.html", list_addreses=list_addreses)

@app.route('/type', methods = ['POST', 'GET'])
def addtype():
    list_type = db.session.query(Type).order_by("type").all()
    if request.method == "POST":
        try:
            type = Type(type = request.form['type'])
            db.session.add(type)
            db.session.flush()
            db.session.commit()
            list_type = db.session.query(Type).order_by("type").all()
        except:
            db.session.rollback()
            print("Ошибка добавления адреса в базу")

    return render_template("type.html", list_type = list_type)



@app.route('/files', methods = ['POST'])
def downloadFile ():
    if request.form['btnfiles'] == 'downloadvlans':
        #For windows you need to use drive name [ex: F:/Example.pdf]
        #path = "files/vlans.xlsx"
        return send_file(app.config['DOWNLOAD_VLAN_FOLDER'], as_attachment=True)
        #return send_file(path, as_attachment=True)
    elif request.form['btnfiles'] == 'uploadvlans':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename=filename))


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

if __name__ == "__main__":
    app.run(debug = True)  # на этапе разработке True