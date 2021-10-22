from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from rct.models import db, Vlan, Vlansw, Address, Type, vlanFromFile, addrFromFile, runupaddr, Location, locatFromFile, check_if_ip_is_network, Model, runupmodel, modeliFromFile, Device, check_if_id_aiu, check_if_mac_aiu, deviceFromFile, ModelSwitch, modeliswFromFile, Switch, Typesw, Place, Ipaddr, Ipaddrsw
import ipaddress
from transliterate import translit
import os
from rct.forms import LocationFormAdd, ModelFormAdd
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

#from flask_migrate import Migrate#, MigrateCommand


app = Flask(__name__, instance_relative_config=True)

# Читаем config
app.config.from_pyfile("config_ins.py")


# Инициализируем объект приложения
db.init_app(app)

# создать экземпляр класса Migrate, передав экземпляр приложения (app) и объект SQLAlchemy (db)
migrate = Migrate(app, db)
#manager.add_command('db', MigrateCommand)




# создаем все таблица в БД
db.create_all(app=app)

@app.route('/')
def main():
    return render_template("index.html")

# Удаление VLANSW
@app.route('/delvlanssw', methods = ['POST'])
def delvlanssw():

    try:
        vlanswToDelete = Vlansw.query.get(request.form['delbtn'])

        # Удаляем IP (каскадно не получается (sqllite))
        db.session.query(Ipaddrsw).filter(Ipaddrsw.vlansw_id == vlanswToDelete.id).delete()

        #
        idvlan = str(vlanswToDelete.id_vl)
        db.session.delete(vlanswToDelete)
        db.session.flush()
        db.session.commit()
        status = "VLAN ID: "+ idvlan +"\t и подсеть: "+ vlanswToDelete.ipnet +" Успешно удалена, \t все IP адреса из этой подсети - удалены"
    except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления VLAN ID : " + idvlan


    return  render_template("delvlans.html", status = status)


# Удаление VLAN
@app.route('/delvlans', methods = ['POST'])
def delvlans():

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

@app.route('/delmodelsw', methods = ['POST'])
def delmodelsw():
    try:
        modelswToDelete = ModelSwitch.query.get(request.form['delbtn'])

        status = modelswToDelete.modelsw

        db.session.delete(modelswToDelete)
        db.session.flush()
        db.session.commit()
        status = "Модель: " + status + " Успешно удалена"
    except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления Модели "


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


@app.route('/deltypesw', methods = ['POST'])
def deltypesw():
    #status = request.form['delbtn']
    try:
        typeswToDelete = Typesw.query.get(request.form['delbtn'])
        statustypeToDelete = typeswToDelete.typesw
        db.session.delete(typeswToDelete)
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

@app.route('/deldevice', methods = ['POST'])
def deldevice():

    try:
        devToDelete = Device.query.get(request.form['delbtn'])
        statusdevToDelete = devToDelete.id_aiu
        db.session.delete(devToDelete)
        db.session.flush()
        db.session.commit()
        status = "Адрес: "+ statusdevToDelete +" Успешно удален"
    except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления Адреса : " + statusdevToDelete


    return  render_template("delitem.html", status = status)


# Добавление VLAN и Network for DEVICE
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
            flash("Ошибка добавления адреса в базу", "error")
            db.session.rollback()
            print("Ошибка добавления адреса в базу")



    return render_template("vlans.html", list_address = list_address, list_vlans = list_vlans, list_type = list_type, title = 'Добавление Vlan & IpNetwork')

# Добавление VLAN и Network for SWITCH
@app.route('/vlanssw', methods = ['POST', 'GET'])
def addvlansw():
    list_address = db.session.query(Address).all()
    list_vlanssw = db.session.query(Vlansw).order_by("id_vl").all()

    if request.method == "POST":
        # try:
            vlansw = request.form.to_dict()

            if check_if_ip_is_network(vlansw["ipnet"], vlansw["netmask"]):
                addr = db.session.query(Address).filter_by(small_address=vlansw["address_id"]).one()
                vlansw["address_id"] = addr.id
                vlansw["gw"] = str(ipaddress.ip_network(str(vlansw["ipnet"])+'/'+str(vlansw["netmask"])).network_address+1)
                vlansw = Vlansw(**vlansw)
                db.session.add(vlansw)
                db.session.flush()
                db.session.commit()
                #auto_create_ipaddr(vlansw)
                Ipaddrsw.createips(vlansw)

                list_vlanssw = db.session.query(Vlansw).order_by("id_vl").all()

            else:
                flash("Проверьте правильность адреса подсети", "error")
                print("Проверьте правильность адреса подсети")
        # except Exception as e:
        #    err = type(e).__name__
        #    #message = e.message
        #    print(err)
        #    db.session.rollback()
        #    flash(err, "error")
        #    flash("Ошибка добавления адреса в базу", "error")
        #    print("Ошибка добавления адреса в базу")



    return render_template("vlanssw.html", list_address = list_address, list_vlanssw = list_vlanssw, title = 'Добавление Vlan & IpNetwork switch')


# Devices
@app.route('/devices', methods = ['POST', 'GET'])
def devices():
    list_type = db.session.query(Type).order_by("type").all()
    list_devices = db.session.query(Device).order_by("id_aiu").all()
    list_models = db.session.query(Model).order_by("model").all()
    if request.method == "POST":

        type = db.session.query(Type).filter_by(type=request.form["typelist"]).one()
        model = db.session.query(Model).filter_by(model=request.form["modelslist"]).one()
        id_aiu = request.form["id_aiu"]
        mac = request.form["addmac"]
        mac = check_if_mac_aiu(mac)
        docs = request.form["doc"]
        try:
            id_aiu = check_if_id_aiu(id_aiu)

            #mac = check_if_mac_aiu(mac)
            device = Device(id_aiu = id_aiu, mac = mac, docs=docs, type_id = type.id, model_id = model.id)
            db.session.add(device)
            db.session.flush()
            db.session.commit()
            list_devices = db.session.query(Device).order_by("id_aiu").all()
            return redirect(url_for("devices"))

        except:
            db.session.rollback()
            print("Ошибка добавления адреса в базу")
            flash("Ошибка добавления адреса в базу", "error")
            return redirect(url_for("devices"))

    return render_template("devices.html", list_devices=list_devices, list_type = list_type, list_models= list_models, title='Устройства')

# Добавление коммутаторов
@app.route('/switches',methods = ['POST', 'GET'])
def switches():
    list_switches = db.session.query(Switch).order_by("name").all()
    list_ModelSwitch = db.session.query(ModelSwitch).order_by("modelsw").all()
    list_typesw = db.session.query(Typesw).order_by("typesw").all()
    list_addreses = db.session.query(Address).order_by("small_address").all()
    list_ip_addreses = db.session.query(Ipaddrsw).filter(Ipaddrsw.status == 'free').all()
    print(list_ip_addreses)


    if request.method == 'POST':
        # GET obj
        typesw = db.session.query(Typesw).filter_by(typesw=request.form["type_id"]).one()
        modelswitch = db.session.query(ModelSwitch).filter_by(modelsw=request.form["model_id"]).one()
        addressswitch = db.session.query(Address).filter_by(small_address=request.form["address_id"]).one()
        ip_addreses = db.session.query(Ipaddrsw).filter_by(ipaddr=request.form["ipaddrsw_id"]).one()
        print(ip_addreses)
        print(ip_addreses.id)
        # try:
            # ImmutableMultiDic - > dict
        sw = request.form.to_dict()
        # Change fild on id.obj
        sw["type_id"] = typesw.id
        sw["model_id"] = modelswitch.id
        sw["mac"] = check_if_mac_aiu(sw["mac"])
        sw["address_id"]=addressswitch.id
        sw["ipaddrsw_id"] = ip_addreses.id

        sw = Switch(**sw)
        db.session.add(sw)
        db.session.flush()
        db.session.commit()

        # Изменяем статус IP на ID коммутатора
        ip_addreses.status = sw.id
        db.session.add(ip_addreses)
        db.session.flush()
        db.session.commit()

        #возвращаем список свободных адресов
        list_ip_addreses = db.session.query(Ipaddrsw).filter(Ipaddrsw.status == 'free').all()
        list_switches = db.session.query(Switch).order_by("name").all()

        # except:
        #     db.session.rollback()
        #     print("Ошибка добавления в базу")
        #     flash("Ошибка добавления в базу", "error")

    return render_template("switches.html", list_switches=list_switches, title='Коммутаторы', list_ModelSwitch = list_ModelSwitch, list_typesw = list_typesw, list_addreses = list_addreses, list_ip_addreses =list_ip_addreses)


@app.route('/address', methods = ['POST', 'GET'])
def addaddress():
    list_addreses = db.session.query(Address).order_by("small_address").all()
    if request.method == "POST":
        try:
            #addr = request.form   ТАК ТОЖЕ РАБОТАЕТ !!!!!
            small_address = runupaddr(request.form['small_address'])
            translate = translit(small_address, language_code='ru', reversed=True)
            translate = translate.replace("'", "")
            #address = Address(**addr, translate = translate)   ТАК ТОЖЕ РАБОТАЕТ !!!!!
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

@app.route('/typesw', methods = ['POST', 'GET'])
def addtypesw():
    list_typesw = db.session.query(Typesw).order_by("typesw").all()
    #print(list_typesw)
    if request.method == "POST":
        try:
            type_sw = request.form
            tps = Typesw(**type_sw)
            db.session.add(tps)
            db.session.flush()
            db.session.commit()
            list_typesw = db.session.query(Typesw).order_by("typesw").all()
        except:
            db.session.rollback()
            flash("Ошибка добавления в базу", "error")
            print("Ошибка добавления в базу")

    return render_template("typesw.html", list_typesw = list_typesw)

# Добавление моделей
@app.route('/modeli', methods=['POST', 'GET'])
def addmodeli():
    list_models = db.session.query(Model).order_by("model").all()
    form = ModelFormAdd()
    if form.validate_on_submit():
        try:
            model = form.model.data
            model = runupmodel(model)
            modl = Model(model, vendor="unknow")
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

# Добавление моделей коммутаторов
@app.route('/modelisw', methods=['POST', 'GET'])
def addmodelisw():
    list_models_sw = db.session.query(ModelSwitch).order_by("modelsw").all()

    if request.method == "POST":
        try:
            model_sw = request.form
            model_sw = ModelSwitch(**model_sw)
            db.session.add(model_sw)
            db.session.flush()
            db.session.commit()
            list_models_sw = db.session.query(ModelSwitch).order_by("modelsw").all()
        except:
            db.session.rollback()
            flash("Ошибка добавления в базу", "error")
            print("Ошибка добавления в базу")

    return render_template("modelisw.html", list_models_sw=list_models_sw, title='Модели Коммутаторов')



# Выгрузка файла на ПК , выгрузка файла
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
    # - Modeli.xlsx
    elif request.form['btnfiles'] == 'downloadmodeli':
        return send_file(app.config['DOWNLOAD_MODEL_FOLDER'], as_attachment=True)
    # - Modelisw.xlsx
    elif request.form['btnfiles'] == 'downloadmodelisw':
        return send_file(app.config['DOWNLOAD_MODELSW_FOLDER'], as_attachment=True)
    # - Devices.xlsx
    elif request.form['btnfiles'] == 'downloaddevices':
        return send_file(app.config['DOWNLOAD_DEVICE_FOLDER'], as_attachment=True)


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

    # From Devices
    elif request.form['btnfiles'] == 'uploaddevices':
       try:
            file = request.files['file']
            if not file.filename:
                status = "Проверьте имя файла"
                return render_template("delitem.html", status=status)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                return render_template("statuspage.html", status_list =deviceFromFile(filename, app))

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
        try:
            file = request.files['file']
            if not file.filename:
                status = "Проверьте имя файла"
                return render_template("delitem.html", status=status)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


                return render_template("statuspage.html", status_list=locatFromFile(filename, app))

        except:
            status = "Что-то пошло не так :("
            return render_template("delitem.html", status=status)

    # from modeli
    elif request.form['btnfiles'] == 'uploadmodeli':
        try:
            file = request.files['file']
            if not file.filename:
                status = "Проверьте имя файла"
                return render_template("delitem.html", status=status)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))


                return render_template("statuspage.html", status_list=modeliFromFile(filename, app))

        except:
            status = "Что-то пошло не так :("
            return render_template("delitem.html", status=status)

    # from modelisw
    elif request.form['btnfiles'] == 'uploadmodelisw':
        try:
            file = request.files['file']
            if not file.filename:
                status = "Проверьте имя файла"
                return render_template("delitem.html", status=status)

            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

                return render_template("statuspage.html", status_list=modeliswFromFile(filename, app))

        except:
            status = "Что-то пошло не так :("
            return render_template("delitem.html", status=status)



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
           # ВОТ ДО СЮДА
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


def type_choices():
    return db.session.query(Type).order_by("type").all()



if __name__ == "__main__":
    app.run(debug = True)  # на этапе разработке True