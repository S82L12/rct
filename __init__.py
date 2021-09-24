from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from rct.models import db, Vlan, Address, Type, vlanFromFile, addrFromFile, runupaddr, Location, locatFromFile, check_if_ip_is_network, Model, runupmodel
import rct.models
from transliterate import translit
import os
from rct.forms import LocationFormAdd, ModelFormAdd



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

@app.route('/delmodel', methods = ['POST'])
def delmodel():
    try:
        modelToDelete = Model.query.get(request.form['delbtn'])
        status = modelToDelete.model
        db.session.delete(modelToDelete)
        db.session.flush()
        db.session.commit()
        status = "Type: " + status + " Успешно удален"
    except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления Модели : " + statusmodelToDelete


    return  render_template("delitem.html", status = status)




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


@app.route('/dellocat', methods = ['POST'])
def dellocat():
   try:
        locatToDelete = Location.query.get(request.form['delbtn'])
        status = locatToDelete.small_location
        db.session.delete(locatToDelete)
        db.session.flush()
        db.session.commit()
        status = "Type: "+ status +" Успешно удален"

   except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления TYPE : " + status

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
            if check_if_ip_is_network(request.form['addipnet'],request.form['addipnetmask']):
                addr = db.session.query(Address).filter_by(small_address=request.form['addrlist']).one()
                type = db.session.query(Type).filter_by(type=request.form['typelist']).one()
                vlan = Vlan(id_vl=request.form['addvlanid'], name=request.form['addvlanname'], address_id = addr.id, type_id = type.id, ipnet=request.form['addipnet'], netmask=request.form['addipnetmask'])
                db.session.add(vlan)
                db.session.flush()
                db.session.commit()
                list_vlans = db.session.query(Vlan).order_by("id_vl").all()
                list_type = db.session.query(Type).all()
            else:
                flash("Проверьте правильность адреса подсети", "error")
                print("Проверьте правильность адреса подсети")
        except:
            db.session.rollback()
            print("Ошибка добавления адреса в базу")



    return render_template("vlans.html", list_address = list_address, list_vlans = list_vlans, list_type = list_type, title = 'Добавление Vlan & IpNetwork')


@app.route('/address', methods = ['POST', 'GET'])
def addaddress():
    list_addreses = db.session.query(Address).order_by("small_address").all()
    if request.method == "POST":
        try:
            small_address = runupaddr(request.form['small_address'])
            translate = translit(small_address, language_code='ru', reversed=True)
            translate = translate.replace("'", "")
            address = Address(small_address = small_address, rgis_address = request.form['rgis_address'], translate = translate)
            db.session.add(address)
            db.session.flush()
            db.session.commit()
            list_addreses = db.session.query(Address).order_by("small_address").all()
        except:
            db.session.rollback()
            print("Ошибка добавления адреса в базу")

    return render_template("address.html", list_addreses=list_addreses, title = 'Адреса')


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

# Добавление моделей
@app.route('/modeli', methods=['POST', 'GET'])
def addmodeli():
    list_models = db.session.query(Model).order_by("model").all()
    form = ModelFormAdd()
    if form.validate_on_submit():
        try:
            model = form.model.data
            model = runupmodel(model)
            modl = Model(model=model)
            db.session.add(modl)
            db.session.flush()
            db.session.commit()
            return redirect(url_for('addmodeli'))

        except:
            db.session.rollback()
            print("Ошибка добавления модели в базу")
            flash("Ошибка добавления адреса в базу", "error")
            return redirect(url_for("addmodeli"))


    return render_template("modeli.html", list_models=list_models, title="Справочник Моделей", form=form)


@app.route('/files', methods = ['POST'])
def downloadFile ():
    """Обработчик загрузки и выгрузки файлов"""
    # Выгрузка файлов:
    # - vlan.xlsx
    if request.form['btnfiles'] == 'downloadvlans':
        return send_file(app.config['DOWNLOAD_VLAN_FOLDER'], as_attachment=True)
    # - address.xlsx
    elif request.form['btnfiles'] == 'downloadaddress':
        return send_file(app.config['DOWNLOAD_ADDRESS_FOLDER'], as_attachment=True)
    # - location.xlsx
    elif request.form['btnfiles'] == 'downloadlocat':
        return send_file(app.config['DOWNLOAD_LOCAT_FOLDER'], as_attachment=True)

    # Загрузка из файла
    # from vlan
    elif request.form['btnfiles'] == 'uploadvlans':
       try:
            file = request.files['file']
            if not file.filename:
                status = "Проверьте имя файла"
                return render_template("delitem.html", status=status)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # status = str(filename) + " Успешно загружен"
                # return  render_template("delitem.html", status = status)

                return render_template("statuspage.html", status_list =vlanFromFile(filename, app))

       except:
           status = "Что-то пошло не так :("
           return render_template("delitem.html", status=status)


    # from address
    elif request.form['btnfiles'] == 'uploadaddress':
        try:
            file = request.files['file']
            if not file.filename:
                status = "Проверьте имя файла"
                return render_template("delitem.html", status=status)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template("statuspage.html", status_list =addrFromFile(filename, app,translit))

        except:
            status = "Что-то пошло не так :("
            return render_template("delitem.html", status=status)

    # from locat
    elif request.form['btnfiles'] == 'uploadlocat':
        #try:
            file = request.files['file']
            if not file.filename:
                status = "Проверьте имя файла"
                return render_template("delitem.html", status=status)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                # status = str(filename) + " Успешно загружен"
                # return  render_template("delitem.html", status = status)

                return render_template("statuspage.html", status_list=locatFromFile(filename, app))

        # except:
        #     status = "Что-то пошло не так :("
        #     return render_template("delitem.html", status=status)




@app.route('/location', methods = ['POST', 'GET'])
def location():
    list_locations = db.session.query(Location).order_by("small_location").all()
    form = LocationFormAdd()
    if form.validate_on_submit():
       try:
            small_location = form.small_location.data
            location = Location(small_location=small_location)
            db.session.add(location)
            db.session.flush()
            db.session.commit()
            list_locations = db.session.query(Location).order_by("small_location").all()
            return redirect(url_for("location"))

       except:
            db.session.rollback()
            print("Ошибка добавления адреса в базу")
            flash("Ошибка добавления адреса в базу", "error")
            return redirect(url_for("location"))

    return render_template("location.html", list_locations = list_locations, title = 'Локация', form = form)



def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in app.config['ALLOWED_EXTENSIONS']




if __name__ == "__main__":
    app.run(debug = True)  # на этапе разработке True