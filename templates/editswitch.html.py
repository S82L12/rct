{% extends 'base.html' %}

{% block title %}
Адреса
{% endblock %}

{% block body %}

<main class="col-md-9 ms-sm-auto col-lg-10 px-md-4"><div class="chartjs-size-monitor"><div class="chartjs-size-monitor-expand"><div class=""></div></div><div class="chartjs-size-monitor-shrink"><div class=""></div></div></div>



  <ul class="navbar-nav px-3">
    <li class="nav-item text-nowrap">


    </li>
  </ul>

</header>
    <h2>{{title}}</h2>

     <form method="POST" enctype=multipart/form-data action="/files">
        <div class="pb-1" >
        <button type="submit" name ="btnfiles" value="downloaddevices" class="btn btn-secondary ">Загрузить шаблон EXCEL</button>
        </div>
        <div class="pb-1" >
        <button type="submit" name ="btnfiles" value="uploaddevices" class="btn btn-secondary ">Загрузить список Устройств из файла EXCEL</button>
        </div>
        <p><input type="file" name="file"></p>
    </form>

      <div class="table-responsive">
        <table class="table table-striped table-sm">
          <thead>
            <tr>
              <th scope="col">ID_АИЮ</th>
              <th scope="col">Имя</th>
              <th scope="col">Тип</th>
              <th scope="col">Модель</th>
              <th scope="col">MAC</th>
              <th scope="col">Адрес</th>
              <th scope="col">IP адрес</th>
              <th scope="col">Накладная</th>
              <th scope="col">Примечание</th>
              <th scope="col">Действие</th>


            </tr>
          </thead>
          <tbody>

          <form method="post" name="switches" >
            <tr>
              <td><input class="form-control form-control-dark w-100" name="id_aiu"  type="text" placeholder="ID АИЮ" aria-label="Search"></td>
              <td><input class="form-control form-control-dark w-100" name="name" type="text" placeholder="sw1lenina1k2"></td>
              <td><select name="type_id" class="form-control form-control-dark w-100">
                      <option>Тип</option>
                      {% for i in list_typesw %}
                      <option>{{i.typesw}}</option>
                      {% endfor %}
                  </select>
              </td>
              <td><select name="model_id" class="form-control form-control-dark w-100">
                      <option>Модель</option>
                      {% for i in list_ModelSwitch %}
                      <option>{{i.modelsw}}</option>
                      {% endfor %}
                  </select>
              </td>
                <td><input class="form-control form-control-dark w-100" name="mac" type="text" placeholder="00:00:00:00:00:00"></td>

                <td><select name="address_id" class="form-control form-control-dark w-100">
                      <option>Адрес</option>
                      {% for i in list_addreses %}
                      <option>{{i.small_address}}</option>
                      {% endfor %}
                  </select></td>
                <td><select name="ipaddrsw_id" class="form-control form-control-dark w-100">
                      <option>Адрес</option>
                      {% for i in list_ip_addreses %}
                      <option>{{i.ipaddr}}</option>
                      {% endfor %}
                  </select></td>

                <td><input class="form-control form-control-dark w-100" name="docs" type="text" placeholder="Номер и дата накладной"></td>
                <td><input class="form-control form-control-dark w-100" name="description" type="text" placeholder="Примечание"></td>

                <td><button type="submit" class="btn btn-dark btn-sm">ДОБАВИТЬ</button></td>

            </tr>
          </form>

          {% with messages = get_flashed_messages(with_categories=true) %}
            {% if messages %}

                    {% for category, message in messages %}
          <tr><p class="text-danger">{{ message }}</p></tr>

                    {% endfor %}

            {% endif %}
          {% endwith %}


            {% for i in list_switches %}

          <form action = "/delswitches" method = "POST"">
            <tr>
              <td>{{i.id_aiu}}</td>
              <td>{{i.name}}</td>
              <td>{{i.typeswitch.typesw}}</td>
              <td>{{i.modelswitch.modelsw}}</td>
              <td>{{i.mac}}</td>
               <td>{{i.addressswitch.small_address}}</td>
                <td>{{i.switchip.ipaddr}}</td>
                <td>{{i.docs}}</td>
                <td>{{i.description}}</td>



              <td><button type="submit" name = "delbtn" value = "{{i.id}}" class="btn btn-dark btn-sm">Удалить</button></td>
            </tr></form>

              {%  endfor %}

          </tbody>
        </table>
      </div>
    </main>

{% endblock %}