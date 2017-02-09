const local = window.location;
const url = local.origin;


$("#local").text(local);
$("#url").text(url);




const barchart = (data,bind,x,value) => c3.generate({
  bindto: bind,
    data: {
      json : data,
      keys:{
        x:x,
        value:value
       },
      type:'bar'
    },
    axis:{
      x:{
        type:'category'
      }
    }
  });

const piechart = (data,bind) => c3.generate({
    bindto: bind,
    data: {
        columns : JSON.parse(JSON.stringify(data)),
        type : 'pie',
        onclick: function (d, i) { console.log("onclick", d, i); },
        onmouseover: function (d, i) { console.log("onmouseover", d, i); },
        onmouseout: function (d, i) { console.log("onmouseout", d, i); }
    }
});


$.getJSON(url + '/getdata',{key:'compare_ka',type:'bar'}, function(data) {
        //$("#result").text(data); 
        console.log(data);
        barchart(data,"#compkachart","診療科区分",['DPC総点数','出来高総点数','出来高対比']);
      });

$.getJSON(url + '/getdata',{key:'compare_byoto',type:'bar'}, function(data) {
        //$("#result").text(data); 
        console.log(data);
        barchart(data,"#compbyochart","病棟コード",['DPC総点数','出来高総点数','出来高対比']);
      });

$.getJSON(url + '/getdata',{key:'Percent_byoto',type:'pie'}, function(data) {
        //$("#result").text(data); 
        console.log(data);
        piechart(data,"#perbyochart");
      });


$.getJSON(url + '/getdata',{key:'Percent_ka',type:'pie'}, function(data) {
        //$("#result").text(data); 
        console.log(data);
        piechart(data,"#perkachart");
      });

$.getJSON(url + '/getdata',{key:'mdc2_dpcsum',type:'bar'}, function(data) {
        //$("#result").text(data); 
        console.log(data);
        barchart(data,"#mdc2dpcchart","MDC2",['DPC総点数']);
      });

$.getJSON(url + '/getdata',{key:'ka_dpcsum',type:'bar'}, function(data) {
        //$("#result").text(data); 
        console.log(data);
        barchart(data,"#kadpcchart","診療科区分",['DPC総点数']);
      });



