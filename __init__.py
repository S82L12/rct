from flask import Flask, render_template, request

from rct.models import db, Vlan
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
    if request.method == "POST":
        try:
            vlan = Vlan(id_vl=request.form['addvlanid'], name=request.form['addvlanname'])
            db.session.add(vlan)
            db.session.flush()
            db.session.commit()
        except:
            vlan = Vlan(id_vl=request.form['addvlanid'], name=request.form['addvlanname'])
            db.session.add(vlan)
            db.session.flush()
            db.session.commit()

            print("Ошибка добавления в Базу данных ")

    return render_template("vlans.html")




if __name__ == "__main__":
    app.run(debug = True)  # на этапе разработке True