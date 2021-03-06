from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from werkzeug.utils import secure_filename
from rct.models import db, Vlan, Node, Vlansw, Address, Type, vlanFromFile, addrFromFile, runupaddr, Location, locatFromFile, check_if_ip_is_network, Model, runupmodel, modeliFromFile, Device, check_if_id_aiu, check_if_mac_aiu, deviceFromFile, Modelswitch, modeliswFromFile, Switch, Typesw, Place, Ipaddr, Ipaddrsw, Port
import ipaddress
import json
from transliterate import translit
import os
from rct.forms import LocationFormAdd, ModelFormAdd, AddressSwitchAdd
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import time

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
        modelswToDelete = Modelswitch.query.get(request.form['delbtn'])

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


# УДаление узла с адреса
@app.route('/delnodes', methods = ['POST'])
def delnodes():

    try:
        ItemToDelete = Node.query.get(request.form['delbtn'])
        statusItemToDelete =  ItemToDelete.id
        db.session.delete(ItemToDelete)
        db.session.flush()
        db.session.commit()
        status = "Адрес: "+ str(statusItemToDelete) +" Успешно удален"
    except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления Адреса : " + statusItemToDelete
    return  render_template("delitem.html", status = status)


# Удаление коммутатора со склада с преварительной проверкой подключенных портов
@app.route('/delswitches', methods = ['POST'])
def delswitches():
    try:
        devToDelete = Switch.query.get(request.form['delbtn'])
        statusdevToDelete = devToDelete.id_aiu
        db.session.delete(devToDelete)
        db.session.flush()

        # Проверяем есть ли подключенные порты, иначе нельзя удалять:
        if db.session.query(Port).filter(Port.switch_id == devToDelete.id, Port.linksw_id != None).count() == 0 and db.session.query(Port).filter(Port.switch_id == devToDelete.id, Port.linkdev_id != None).count() == 0:
            db.session.query(Port).filter(Port.switch_id == devToDelete.id).delete()
            db.session.commit()
            status = "Коммутатор: " + statusdevToDelete + "\t Вместе с портами Успешно удален"
        else:
            db.session.rollback()
            status = "Коммутатор имеет подключенные устройства, удаление отменено : " + statusdevToDelete


    except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления коммутатора : " + statusdevToDelete

    return render_template("delitem.html", status=status)


# Редактирование
# @app.route('/editswitch', method =['POST'])
# def deleditswitch():
#     pass


# Работа с узлами 23 11 2021 остановился
@app.route('/addnode/<node>', methods = ['POST', 'GET'])
def show_node(node):
    all_node = []
    # Получаем объект УЗЕЛ (NODE)
    nodeObj = db.session.query(Node).get(node)

    # Получаем список доступных для добавления коммутаторов со склада и IP
    list_sw = db.session.query(Switch).filter(Typesw.id == Switch.type_id).filter(Typesw.typesw == 'swu').filter(Switch.address_id == None).order_by("id_aiu").all()
    list_ipsw = db.session.query(Ipaddrsw).order_by('id').filter(Switch.node_id == None, Ipaddrsw.status == 'free', Ipaddrsw.gw == '172.0.0.1').all()

    # 2 часть (добавление коммутатора - ACCESS on address
    form = AddressSwitchAdd()
    form.address.choices = [(address.id, address.small_address) for address in db.session.query(Address).all()] # получаем список кортежей адресов для возможности выбора
    form.switch.choices = [(switch.id, 'id_АИЮ: '+ str(switch.id_aiu) +'\t\t'+ 'Модель:'+ str(switch.modelswitch.modelsw))\
                           for switch in db.session.query(Switch).filter(Typesw.id == Switch.type_id).filter(Typesw.typesw == 'Access').filter(Switch.address_id == None).all()]


    """ 3 Часть. Список коммутаторов SWU установленных на узле"""


    list_sw_node = db.session.query(Switch).filter(Switch.node_id == nodeObj.id).all()
    #print('Список коммутаторов SWU установленных на узле',list_sw_node)
    # Ключи которые нам потребуются для добавления в словарь + ключи ports ipaddr
    relevant_keys = ['id', 'ipaddrsw_id', 'node_id', 'id_aiu', 'name', 'mac', 'docs', 'address_id']
    relevant_keys_port = ['id', 'name', 'address_id', 'switch_id', 'linksw_id', 'description']

    # Вот с этим списком мы будем потом работать
    list_sw_node_rel = []

    for i in list_sw_node:
        dict_swu = i.__dict__
        # Создаем словарь с релевантными ключами
        dict_swu = {key : dict_swu[key] for key in relevant_keys}

        # Получаем IP адреса коммутатора и вносим его в словарь (изначнально в словаре только ссылка на id таблицы с IP адресами)
        # добавляем в словарь с новым ключом
        ipaddr_obj =  db.session.query(Ipaddrsw).get(dict_swu["ipaddrsw_id"])
        dict_swu["ipaddr"] = ipaddr_obj.ipaddr


        #list_port = db.session.query(Switch, Port).filter(Switch.id == i.id).filter(Port.switch_id == i.ports).all()

        # начинаем заполнять ключ ports, он будет состоять из списка словарей   dict_port
        # поллучаем список портов у коммутатора

        list_port = db.session.query(Port).filter(Port.switch_id == i.id).all()
        list_ports_end = [] # используется для создания списка словарей портов (dict_port) в последующем нужно добавить этот список в значения ключа ports




        for port in list_port:

            #    print("Порт: ", port.name)
            dict_port = port.__dict__
            dict_port = {key: dict_port[key] for key in relevant_keys_port}

            # получаем адрес подключенный к порту

            addr_on_port = db.session.query(Address).get(dict_port["address_id"])
            #  print("Адрес подключенный к порту: ",addr_on_port)
            # GET value from OBJ address
            if addr_on_port is None:
                dict_port["address"] = 'Пустой'
            else:
                dict_port["address"] = addr_on_port.small_address
          #  print("ПредКонечный словарь",dict_port)
          #  print('Obj адрес подключенный к порту',addr_on_port, type(addr_on_port))

            # Добавляем список словарей коммутаторов к каждому порту.
            #sws_on_port =db.session.query(Switch).filter(Switch.address_id == addr_on_port.id).all()

            # db.session.query(Switch).filter(Port.linksw_id == , Typesw.typesw == 'swu').all()
            #print("Коммутаторы подключенные к порту:", sws_on_port)


            # Добавляем в список словарей портов list_ports_end получившийся словарь dict_port

            # port_addr = port.__dict__
            # port_addr = {key: port_addr[key] for key in ["id", "small_address"]}
            # print(port_addr)
            #
            #print("Словарь OBJ порт: ",dict_port)
            list_ports_end.append(dict_port)

        #print('Словарь коммутаторов на узле:', dict_swu)
        # Добавляем получившийся список в значения ключа ports в словаре swu_dict
        dict_swu["ports"] = list_ports_end
       # print('LIST ports dict2', dict_swu["ports"])

    # Добавляем наш словарь портов в основной список   !!!!!!!!!!  нужно в конец перенести
    list_sw_node_rel.append(dict_swu)
    print(list_sw_node_rel)

    #print(list_ports_end)







        #print(list_port)
        #print(dict_swu)





    list_sw_access = db.session.query(Port).all()


   # print('List SW', list_ipsw)
    #list_ipsw = db.session.query(Ipaddrsw).join(Vlansw).filter(Ipaddrsw.switch_id == 'free', Vlansw.id_vl == '27').all()

   # url_redirect = '/addnode/' + str(node.id)
    if request.method == 'POST':
        data = request.form.to_dict()
        print(data)
        print(dir(data))
        for i in data:
            print(i)

        # Обработка формы с добавлением коммутатора на узел
        if request.form['btnsubmit'] == 'btnadddswnode':
            try:
                 # synchronize_session=False объект удаляется
                db.session.query(Switch).filter(Switch.id == request.form.get('sw')).update({Switch.node_id: nodeObj.id, Switch.address_id : nodeObj.address_id, Switch.name: request.form["name"], Switch.ipaddrsw_id: request.form.get('ipsw')})
                ip = db.session.query(Ipaddrsw).get(request.form.get('ipsw'))#.update({Ipaddrsw.status: request.form.get('sw')})
                ip.status = request.form.get('sw')
                db.session.add(ip)
                db.session.commit()
                #return redirect(url_for('show_node', node=node))
            except Exception as e:
                err = type(e).__name__
                db.session.rollback()
                flash(err, "error")
                flash("Ошибка добавления адреса в базу", "error")
                print("Ошибка добавления адреса в базу")

        elif request.form['btnsubmit'] == 'btnaddswaddr':
            print('ПРИНЯЛИ')
            try:
                address = db.session.query(Address).get(form.address.data)
                switch = db.session.query(Switch).get(form.switch.data)
                address.switches.append(switch)
                db.session.add(switch)
                db.session.commit()
                flash('Успешно добавили')

            except Exception as e:
                err = type(e).__name__
                db.session.rollback()
                flash(err, "error")
                flash("Ошибка добавления коммутатора в базу на адрес", "error")
                print("Ошибка добавления адреса в базу")


            print(form.address.data, form.switch.data)


    return render_template('editnode.html', form = form, nodeObj = nodeObj, list_ports_end = list_ports_end, \
                               title = nodeObj.name, list_sw=list_sw, list_ipsw=list_ipsw, list_sw_node=list_sw_node, \
                               list_sw_node_rel = list_sw_node_rel, list_sw_access= list_sw_access)


# Обработка привязки адреса к порту (Добавляем к порту узлового коммутатора адрес)
@app.route('/editaddrport', methods = ['POST'])
def editaddrport():
    try:
        data = request.form.to_dict()
        addressObj = db.session.query(Address).get(data["id_address"])
        portObj = db.session.query(Port).get(data["id_port"])
        addressObj.ports.append(portObj)
        db.session.add_all([addressObj,portObj])
        db.session.flush()
        db.session.commit()

        #print(addressObj.small_address, portObj.name)
        #time.sleep(1000)
    except:
        db.session.rollback()
        print("Ошибка удаления")
        status = "Ошибка удаления коммутатора : "
        return render_template("nodeandsw.html")


# Создание узлов... создаем имя и привязываем к адресу (непомню!!!!!!!!!)
@app.route('/nodeandsw', methods = ['GET'])
def nodeandsw():
    list_nodes = db.session.query(Node).order_by(Node.name).all()
    return render_template("nodeandsw.html",  list_nodes=list_nodes)


# Добавление Узла
@app.route('/addnode', methods = ['POST', 'GET'])
def addnode():
    list_address = db.session.query(Address).all()
    list_nodes = db.session.query(Node).order_by(Node.name).all()

    # Выбираем SW оторые никуда не установлены
    list_sw = db.session.query(Switch).order_by("id_aiu").filter(Switch.node_id == None).all()
    #dict_sw = {id_aiu.id : modelsw.modelswitch.modelsw for id_aiu in list_sw for modelsw in list_sw}


    if request.method == "POST":
       try:
           node = request.form.to_dict()
           node = Node(name=node["name"], description = node["description"], address_id = node["address_id"])
           db.session.add(node)
           db.session.flush()
           db.session.commit()
           return redirect(url_for('addnode'))

       except:
           flash("Ошибка добавления адреса в базу", "error")
           db.session.rollback()
           print("Ошибка добавления адреса в базу")
           return redirect(url_for('addnode'))

    #return redirect(url_for('addnode'))
    return render_template("addnode.html", list_address = list_address, title = 'Создание Узла', list_nodes=list_nodes)


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
        try:
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
        except Exception as e:
           err = type(e).__name__
           #message = e.message
           print(err)
           db.session.rollback()
           flash(err, "error")
           flash("Ошибка добавления адреса в базу", "error")
           print("Ошибка добавления адреса в базу")



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

# редактирование коммутаторов и узлов этот шаблон не используется!
@app.route('/switches',methods = ['POST', 'GET'])
def switches():
    list_switches = db.session.query(Switch).order_by("name").all()
    list_modelswitch = db.session.query(Modelswitch).order_by("modelsw").all()
    list_typesw = db.session.query(Typesw).order_by("typesw").all()
    list_addreses = db.session.query(Address).order_by("small_address").all()
    list_ip_addreses = db.session.query(Ipaddrsw).filter(Ipaddrsw.status == 'free').all()



    if request.method == 'POST':
        # GET obj
        typesw = db.session.query(Typesw).filter_by(typesw=request.form["type_id"]).one()
        modelswitch = db.session.query(Modelswitch).filter_by(modelsw=request.form["model_id"]).one()
        addressswitch = db.session.query(Address).filter_by(small_address=request.form["address_id"]).one()
        ip_addreses = db.session.query(Ipaddrsw).filter_by(ipaddr=request.form["ipaddrsw_id"]).one()


        try:
            # ImmutableMultiDic - > dict
            sw = request.form.to_dict()
            # Change fild on id.obj
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

            # Изменяем статус IP на ID коммутатора (чтобы список был из снезянятых IP)
            ip_addreses.status = sw.id
            db.session.add(ip_addreses)
            db.session.flush()
            db.session.commit()

            #возвращаем список свободных адресов
            list_ip_addreses = db.session.query(Ipaddrsw).filter(Ipaddrsw.status == 'free').all()
            list_switches = db.session.query(Switch).order_by("name").all()


            Port.createports(sw)

        except:
            db.session.rollback()
            print("Ошибка добавления в базу")
            flash("Ошибка добавления в базу", "error")

    return render_template("switches.html", list_switches=list_switches, title='Коммутаторы', list_modelswitch = list_modelswitch, list_typesw = list_typesw, list_addreses = list_addreses, list_ip_addreses =list_ip_addreses)

# Добавление коммутаторов на склад
@app.route('/addswitches', methods = ['POST', 'GET'])
def addswitches():
    list_modelswitch = db.session.query(Modelswitch).order_by("modelsw").all()
    list_typesw = db.session.query(Typesw).order_by("typesw").all()
    list_switches = db.session.query(Switch).order_by("name").all()
    if request.method == 'POST':
        # GET obj
        typesw = db.session.query(Typesw).filter_by(typesw=request.form["type_id"]).one()
        modelswitch = db.session.query(Modelswitch).filter_by(modelsw=request.form["model_id"]).one()
        try:


            # ImmutableMultiDic - > dict
            sw = request.form.to_dict()
            # Change fild on id.obj
            sw["type_id"] = typesw.id
            sw["model_id"] = modelswitch.id
            sw["mac"] = check_if_mac_aiu(sw["mac"])


            sw = Switch(**sw)
            db.session.add(sw)
            db.session.flush()
            # Создание коммутаторов
            Port.createports(sw)

            db.session.commit()

            list_switches = db.session.query(Switch).order_by("name").all()

        except:
            db.session.rollback()
            print("Ошибка добавления в базу")
            flash("Ошибка добавления в базу", "error")

    return render_template("addswitches.html", title='Добавление Коммутаторов', list_modelswitch=list_modelswitch, list_typesw=list_typesw, list_switches = list_switches)
#-----------------------

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
    list_models_sw = db.session.query(Modelswitch).order_by("modelsw").all()

    if request.method == "POST":
        try:
            model_sw = request.form
            model_sw = Modelswitch(**model_sw)
            db.session.add(model_sw)
            db.session.flush()
            db.session.commit()
            list_models_sw = db.session.query(Modelswitch).order_by("modelsw").all()
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