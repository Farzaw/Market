var x = 0;

function addStoreOfClient() {
	if (x < 10) {
	var city = 'city' + (x+1);
	var  store = 'store' + (x+1);
	var row = 'row' + (x+1);
    var container = 'container' + (x+1);
    var btnRT = 'btnRT' + (x+1);

    var div3 = document.createElement('div3');

    var str3 = '<div class = "col-3"> ' +
                '<input type = "text" id="'+ city+'" name="'+city+'" class = "form-control" placeholder="Город" style="margin-bottom:10px;"> </div>'+

        '<div class="col-3">'+
            '<input type="text" id="'+store+'" name="'+store+'" class="form-control" placeholder="Рынок"> </div>'+

        '<div class="col-2">'+
            '<input type="text" id="'+ row +'" name="'+ row +'" class="form-control" placeholder="Ряд"> </div>'+

        '<div class="col-3">'+
            '<input type="text" id="'+container+'" name="'+container+'" class="form-control" placeholder="Контейнер"> </div>'+

        '<div class="col-1">'+
            '<button type="button" id="' + btnRT+ '" name="'+btnRT+'" class="btn btn-danger btn-flat"'+
        ' style="margin-bottom:10px;" onClick="RemoveRT(this.id)">'+
            '<i class="fa fa-trash-alt"></i></button>  </div>';

    div3.className = "row";
	div3.innerHTML = str3;
    document.getElementById('div0').append(div3);
    document.getElementById('countRT').value = x+1;
    x++;
  } else
  {
  	alert('STOP it!');
  }
}

function RemoveRT(id) {

    var elem = document.getElementById(id);
    elem.parentNode.removeChild(elem);

    var city_id = id.replace('btnRT','city');
    var elem_city = document.getElementById(city_id);
    elem_city.parentNode.removeChild(elem_city);

    var store_id = id.replace('btnRT','store');
    var elem_store= document.getElementById(store_id);
    elem_store.parentNode.removeChild(elem_store);

    var row_id = id.replace('btnRT','row');
    var elem_row= document.getElementById(row_id);
    elem_row.parentNode.removeChild(elem_row);

    var container_id = id.replace('btnRT','container');
    var elem_container = document.getElementById(container_id);
    elem_container.parentNode.removeChild(elem_container);
     --x;
    return false;
}

let y = 0;
function addInput() {

    if (y < 10) {
	let name_input = 'input' + (y+1);
	let name_button = 'but' + (y+1);
	let options_item = '';
    console.log(sender_js);
    console.log('in add');
	let div = document.createElement('div');

    let str = '<select name="category" class="form-control" name="'+name_input+'" id="'+name_input+'">';

        for (let i = 0; i < sender_js.length; i++){

            options_item += '<option value="'+sender_js[i].id+'">'+
            sender_js[i].fullname + '</option>';}

        options_item+='</select>';

        str+=options_item;

    str += '<span class="input-group-append">'+
    '<button type="button" id="' + name_button +'" class="btn btn-danger btn-flat"'+
    ' style="margin-bottom: 10px;" onClick="Remove(this.id)">'+
    '<i class="fa fa-trash-alt"></i></button> </span>';
	div.className = "input-group";
	div.innerHTML = str;
    document.getElementById('div1').append(div);
    document.getElementById('count').value = y+1;
    y++;
  } else
  {
  	alert('STOP it!');
  }
}
function Remove(name) {

    var elem = document.getElementById(name);
    elem.parentNode.removeChild(elem);
    name = name.replace('but','input')
    var elem2 = document.getElementById(name);
    elem2.parentNode.removeChild(elem2);

    alert(x)
    y--;
    return false;
}

let z = 0;
function addSender() {
	if (z < 10) {
    let sender = document.getElementById('sender_0');
        sender.setAttribute("sender_0",("sender_" + (z+1)));
    document.getElementById('sender_box').innerHTML = sender;
    z++;
  } else
  {
  	alert('STOP it!');
  }
}

var timepicker = new TimePicker('time', {
  lang: 'en',
  theme: 'dark'
});
timepicker.on('change', function(evt) {

  var value = (evt.hour || '00') + ':' + (evt.minute || '00');
  evt.element.value = value;

});
