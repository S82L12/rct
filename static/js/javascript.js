function editportaddr(el) {

let id = el.value; // записали полученное ID в переменную
let element = document.getElementById(el.parentNode.getAttribute('id')); // получили родителя элемента кнопка

// клонируем список адресов
let cloneAddress = (document.getElementById("address")).cloneNode(true); //клонируем элемент ИМЕННО клонируем, иначе он при нажатии на кнопку начнет перемещаться по всему документу

// Надо удалить старые элементы (div и button) удаляем по тегу
el.remove();// удаляем старую кнопку

let oldDiv = element.querySelector('div'); //Метод elem.querySelector(css) возвращает первый элемент, соответствующий данному CSS-селектору.
oldDiv.remove(); // удаляем div со словом пустой

element.append(cloneAddress); // Добавляем форму выбора адреса в столбец

// Создаем кнопку "Сохранить"
var nBtn = document.createElement("INPUT");
    nBtn.setAttribute('class', 'btn btn-dark btn-sm');
    nBtn.type = "button";
    nBtn.name = id;
    nBtn.value = id;
    nBtn.value = "Сохранить";
    nBtn.innerHTML = "Сохранить";
   // nBtn.setAttribute("onclick", send);

element.append(nBtn); // Добавляем новую кнопку на страницу

// Начинаем писать обработчик для нажатия на кнопку
nBtn.addEventListener('click',send);

// Функция отправки данных на сервер по нажатию кнопки сохранить и обновления странице через 1с
function send() {
    var formData = new FormData();
    formData.append("id_address", cloneAddress.value);
    formData.append("id_port", id);

    // Отправка данных на сервер

    var request = new XMLHttpRequest();
    request.open("POST", "/editaddrport");
    request.send(formData);

    console.log('выполнение', id)
    console.log(id, ' : ID адреса: ', cloneAddress.value)
    setTimeout(function(){
	location.reload();
    }, 1000);
    }
}










/*
========================- РАБОТАЯ ВЕРСИЯ -========================================================================================
function editportaddr(el) {
let id = el.value;
console.log(el) ; // получили элемент кнопка
let element = document.getElementById(el.parentNode.getAttribute('id')); // получили родителя элемента кнопка
console.log(element);


// клонируем список адресов
//let cloneAddress = document.getElementById("address")
let cloneAddress = (document.getElementById("address")).cloneNode(true); //клонируем элемент ИМЕННО клонируем, иначе он при нажатии на кнопку начнет перемещаться по всему документу
console.log(cloneAddress)

console.log(el.parentNode.getAttribute('id') );


console.log('здесь 1 child',element.childNodes[0]);

console.log('здесь второй child КНОПКА',element.childNodes[1]);
console.log('до удаления',element.childNodes[1])
element.childNodes[1].remove();// удаляем старую кнопку
console.log('после удаления',element.childNodes[1])
replacedNode = element.replaceChild(cloneAddress, element.childNodes[0]); //меняем дочерние элементы (новый, старый)   АДРЕСС

let btn = document.createElement("button");
    btn.setAttribute('class', 'btn btn-dark btn-sm');
    btn.innerHTML = "Сохранить";
    btn.value = id;
    btn.name = id;
    btn.type = 'submit';
    //btn.onclick = send();
    //btn.setAttribute("onclick", mysend());
    //btn.addEventListener('click', mysend(), true);
    //btn.addEventListener = ("click", send);

     function mysend() {
    // Отправка данных на сервер
    alert('ВОТ ID:', id)
    console.log('выполнение')
    }

//buttonNew.innerHTML = "<button type="submit"  name ="btneditaddrport" value="{{port["id"]}}" class="btn btn-dark btn-sm">ДОБАВИТЬ</button>";






//replacedNode = element.replaceChild(btn, element.childNodes[1]); // замена КНОПКИ
//btn.addEventListener = ("click", send);


console.log(btn);

element.append(btn);

// run fetch



// возвращаем все обратно
setTimeout(function(){
	location.reload();
}, 49000);

}
=======================================================================================================









//let optionHTML = '';
  //  for (let address of list_sm_addr) {
    //        optionHTML += '<option value="' + el + '">' + address + '</option>';
    //}
    //address.innerHTML = optionHTML;


   // element.innerHTML = cloneAddress;

//alert(el.parentNode.id);
/*
// просмотреть всех детей элемента element
let childElements = element.children;
    for (let child of childElements ) {
    console.log(child)
    }


========================= версия вечер 27 11 21
function editportaddr(el) {
event.preventDefault();
let id = el.value;
console.log(el) ; // получили элемент кнопка
let element = document.getElementById(el.parentNode.getAttribute('id')); // получили родителя элемента кнопка
console.log(element);


// клонируем список адресов
//let cloneAddress = document.getElementById("address")
let cloneAddress = (document.getElementById("address")).cloneNode(true); //клонируем элемент ИМЕННО клонируем, иначе он при нажатии на кнопку начнет перемещаться по всему документу
console.log(cloneAddress)

console.log(el.parentNode.getAttribute('id') );


console.log('здесь 1 child',element.childNodes[0]);

console.log('здесь второй child КНОПКА',element.childNodes[1]);
console.log('до удаления',element.childNodes[1])
//element.childNodes[1].remove();// удаляем старую кнопку
el.remove();// удаляем старую кнопку
console.log('после удаления',element.childNodes[1])
replacedNode = element.replaceChild(cloneAddress, element.childNodes[0]); //меняем дочерние элементы (новый, старый)   АДРЕСС

let btn = document.createElement("button");
    btn.setAttribute('class', 'btn btn-dark btn-sm');
    btn.innerHTML = "Сохранить";
    btn.value = id;
    btn.name = id;
    btn.type = 'submit';
    //btn.onclick = send();
    //btn.setAttribute("onclick", mysend());
    //btn.addEventListener('click', mysend(), true);
    //btn.addEventListener = ("click", send);

     function mysend(id) {
    // Отправка данных на сервер
    alert('ВОТ ID:', id)
    console.log('выполнение')
    }

//buttonNew.innerHTML = "<button type="submit"  name ="btneditaddrport" value="{{port["id"]}}" class="btn btn-dark btn-sm">ДОБАВИТЬ</button>";






//replacedNode = element.replaceChild(btn, element.childNodes[1]); // замена КНОПКИ
//btn.addEventListener = ("click", send);


console.log(btn);

element.append(btn);

// run fetch



// возвращаем все обратно
setTimeout(function(){
	location.reload();
}, 49000);

}



*/
