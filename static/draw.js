
// let now_json = "";

function get_json(asn=0){
  // $.ajaxSetup({ 
  //   async : false 
  // });
	now_json = "";  
	let myajax = $.get("json",{
    asn: asn,
  })
	.done(function (data){
		// console.log(data);
		now_json = JSON.parse(data);
	}).fail(function (xhr, status) {
     console.log("fail!");
  });
}

let vm = new Vue({
  el: '#inputdiv',
  data: {
    asn: "12735",
  },
  methods: {
    redraw: function (type) {
      clear();
      // get_json(this.asn);
      let myajax = $.get("json",{
        asn: this.asn,
        type: type
      })
      .done(function (data){
        // console.log(data);
        let now_json = JSON.parse(data);
        draw_topo(now_json, this.asn);
      }).fail(function (xhr, status) {
         console.log("fail!");
      });
      
    },
    drawtree: function () {
      clear();
      let myajax = $.get("json",{
        asn: this.asn,
        type: 2
      })
      .done(function (data){
        // console.log(data);
        let now_json = JSON.parse(data);        
        draw2tree(now_json);
      }).fail(function (xhr, status) {
         console.log("fail!");
      });
    },
  }
})

// let tab_vm = new Vue({
//   el: '#tabsDiv',
//   data: {
    
//   },
//   methods: {
    
//   }
// })
