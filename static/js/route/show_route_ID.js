function OpenModal(pk) {

    $(document).ready(function () {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie !== '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) === (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            $.ajaxSetup({
                beforeSend: function (xhr, settings) {
                    if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                        // Only send the token to relative URLs i.e. locally.
                        xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
                    }
                }
            });
            let data = {"pk": pk};

                $.ajax({
                    type: 'POST',
                    url: url,
                    data: data,
                    dataType: 'json',
                    success: function (response) {

                      const inf = response.inf;


                      document.getElementById('rt_number').textContent = inf.rtPK;
                      //document.getElementById('route_number').textContent = inf.routeID;
                      document.getElementById('regist').textContent = inf.registration;
                      document.getElementById('date').textContent = inf.date;
                      document.getElementById('time').textContent = inf.time;

                      document.getElementById('recipient_fullname').textContent = inf.recipient;
                      document.getElementById('recipient_phone').textContent = 'Тел.: '+ inf.recipientPhone;

                      document.getElementById('sender_fullname').textContent = inf.sender;
                      document.getElementById('sender_phone').textContent = 'Тел.: '+inf.senderPhone;

                      document.getElementById('operator_fullname').textContent = inf.operator;

                      const products = response.products;
                      const tbody = document.getElementById("idBody");
                      $("#idBody").empty();
                      let tr,tn;
                      for(let i=0; i<products.length; i++)
                      {
                          tr = document.createElement("tr");
                          let tdP = document.createElement("td");
                          var str = products[i].product
                          tn = document.createTextNode(str.slice(0,10)+"...");
                          tdP.appendChild(tn);
                          tr.appendChild(tdP);

                          let tdCode = document.createElement("td");
                          tn = document.createTextNode(products[i].code);
                          tdCode.appendChild(tn);
                          tdCode.align='center';
                          tr.appendChild(tdCode);

                          let tdB = document.createElement("td");
                          tn = document.createTextNode(products[i].bag_number);
                          tdB.appendChild(tn);
                          tdB.align='center';
                          tr.appendChild(tdB);

                          let tdCount = document.createElement("td");
                          tn = document.createTextNode(products[i].count);
                          tdCount.appendChild(tn);
                          tdCount.align='center';
                          tr.appendChild(tdCount);

                          let tdW= document.createElement("td");
                          tn = document.createTextNode(products[i].weight);
                          tdW.appendChild(tn);
                          tdW.align='center';
                          tr.appendChild(tdW);
                          tbody.appendChild(tr);
                      }
                          let trL = document.createElement("tr");
                          let tdI = document.createElement("td");
                          tdI.align='center';
                          tdI.colSpan="2";
                          let tnI = document.createTextNode('Итого:');
                          tdI.appendChild(tnI);
                          trL.appendChild(tdI);

                          let tdBN = document.createElement("td");
                          tdBN.align='center';
                          let tnBN = document.createTextNode(response.CounterBagNumber);
                          tdBN.appendChild(tnBN);
                          trL.appendChild(tdBN);

                          let tdC = document.createElement("td");
                          tdC.align='center';
                          let tnC = document.createTextNode(response.SumCount);
                          tdC.appendChild(tnC);
                          trL.appendChild(tdC);

                          let tdW = document.createElement("td");
                          tdW.align='center';
                          let tnW = document.createTextNode(Math.trunc(response.SumWeight));
                          tdW.appendChild(tnW);
                          trL.appendChild(tdW);

                       tbody.appendChild( trL);

// ----------------------------------------------------------------------------------------
                      const services = response.services;
                      const tbody1 = document.getElementById("idBodyServices");
                      $("#idBodyServices").empty();
                      let tr1;

                      for(let i=0; i<services.length; i++) {
                          tr1 = document.createElement("tr");
                          let tdS = document.createElement("td");
                          let tnS = document.createTextNode(services[i].service);
                          tdS.appendChild(tnS);
                          tr1.appendChild(tdS);

                          let tdCount = document.createElement("td");
                          tdCount.align = 'right';
                          let tnCount = document.createTextNode(services[i].count);
                          tdCount.appendChild(tnCount);
                          tr1.appendChild(tdCount);

                          let tdpriceIV = document.createElement("td");
                          tdpriceIV.align = 'right';
                          let tnpriceIV = document.createTextNode(services[i].priceIV);
                          tdpriceIV.appendChild(tnpriceIV);
                          tr1.appendChild(tdpriceIV);

                          let tdpriceSom = document.createElement("td");
                          tdpriceSom.align = 'right';
                          let tnpriceSom = document.createTextNode(Math.trunc(services[i].priceSom));
                          tdpriceSom.appendChild(tnpriceSom);
                          tr1.appendChild(tdpriceSom);

                          let tdSumPriceIV = document.createElement("td");
                          tdSumPriceIV.align = 'right';
                          let tnSumPriceIV = document.createTextNode(Math.trunc(services[i].SumPriceIV));
                          tdSumPriceIV.appendChild(tnSumPriceIV);
                          tr1.appendChild(tdSumPriceIV);

                          let tdSumPriceSom = document.createElement("td");
                          tdSumPriceSom.align = 'right';
                          let tnSumPriceSom = document.createTextNode(Math.trunc(services[i].SumPriceSom));
                          tdSumPriceSom.appendChild(tnSumPriceSom);
                          tr1.appendChild(tdSumPriceSom);

                          let tdstatus = document.createElement("td");
                          tdstatus.align = 'center';
                          let tnstatus = document.createTextNode(services[i].status);
                          tdstatus.appendChild(tnstatus);
                          tr1.appendChild(tdstatus);
                          tbody1.appendChild(tr1);
                      }

                          let tr2 = document.createElement("tr");
                          let tdT = document.createElement("td");
                          tdT.align = 'center';
                          tdT.colSpan = "4";
                          let tnT1 = document.createTextNode("Итого к оплате");
                          let tnT2 = document.createTextNode("Остаток:");
                          let bold1 = document.createElement('strong');
                          let bold2 = document.createElement('strong');
                          let br = document.createElement('br');
                          bold1.appendChild(tnT1)
                          bold2.appendChild(tnT2)

                         tdT.appendChild(bold1);
                         tdT.appendChild(br);
                         tdT.appendChild(bold2);


                          tr2.appendChild(tdT);

                          let tdremainder = document.createElement("td");
                          tdremainder.align = 'right';
                          tdremainder.vAlign = "bottom";
                          let tnremainder = document.createTextNode(response.remainder);
                          bold1 = document.createElement('strong');
                          bold1.appendChild(tnremainder);
                          tdremainder.appendChild(bold1);
                          tr2.appendChild(tdremainder);

                          let tdTotalPayable = document.createElement("td");
                          tdTotalPayable.align = 'right';
                          tdTotalPayable.vAlign = "top";
                          let tnTotalPayable = document.createTextNode(parseInt(response.TotalPayable));
                          bold = document.createElement('strong');
                          bold.appendChild(tnTotalPayable);
                          tdTotalPayable.appendChild(bold);
                          tr2.appendChild(tdTotalPayable);

                          let tdEmp = document.createElement("td");
                          tr2.appendChild(tdEmp);

                          tbody1.appendChild(tr2);

      $('#modal-lg').modal('show');


                        return false;
                    },
                    error: function (response) {
                        console.log("error");
                    }
                });
            });


}
