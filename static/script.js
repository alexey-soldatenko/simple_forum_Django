
 function dynamicSelect(id1, id2) {

// Сперва необходимо проверить поддержку W3C DOM в браузере

 if (document.getElementById && document.getElementsByTagName) {

// Определение переменных, ссылающихся на списки

  var sel1 = document.getElementById(id1);
  var sel2 = document.getElementById(id2);

// Клонирование динамического списка

  var clone = sel2.cloneNode(true);

// Определение переменных для клонированных элементов списка

  var clonedOptions = clone.getElementsByTagName("option");

// Вызов функции собирающей вызываемый список

  refreshDynamicSelectOptions(sel1, sel2, clonedOptions);

// При изменении выбранного элемента в первом списке: // вызов функции пересобирающей вызываемый список

  sel1.onchange = function() {
  refreshDynamicSelectOptions(sel1, sel2, clonedOptions);
  }
 }
}

// Функция для сборки динамического списка

function refreshDynamicSelectOptions(sel1, sel2, clonedOptions) {

// Удаление всех элементов динамического списка

 while (sel2.options.length) {
  sel2.remove(0);
 }
 var pattern1 = /( |^)(select)( |$)/;
 var pattern2 = new RegExp("( |^)(" + sel1.options[sel1.selectedIndex].value + ")( |$)");

// Перебор клонированных элементов списка

 for (var i = 0; i < clonedOptions.length; i++) {

// Если название класса клонированного option эквивалентно "select" // либо эквивалентно значению option первого списка

  if (clonedOptions[i].className.match(pattern1) ||
  clonedOptions[i].className.match(pattern2)) {

// его нужно клонировать в динамически создаваемый список

   sel2.appendChild(clonedOptions[i].cloneNode(true));
  }
 }
}
