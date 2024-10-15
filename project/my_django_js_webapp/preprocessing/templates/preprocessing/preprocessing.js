$(document).ready(function(){
    console.log("aaaaaaaaaaaaaaa");
    let page = new preprocessingPage();
    page.init();
});

function preprocessingPage(){
    this.sampleVal = 1;
    this.preprocessingDataTable = undefined;
}
preprocessingPage.prototype.init = function(){
    console.log("init!!");
    console.log("value >>>", $("#preprocessingItemList").data("val"));
    this.initEvent();
    this.initDataTable();
}
preprocessingPage.prototype.initDataTable = function(){
    let self = this;
    this.preprocessingDataTable = $("#preprocessingItemList").DataTable({
        stateSave: false, 
        autoWidth: false,
        ajax: {
            url: "{% url 'get_preprocessing_list' %}",
            type: "POST", 
            data: function( d ){
                d.csrfmiddlewaretoken = $.cookie('csrftoken');
            },
            dataFilter : function(jsonStr){
                console.log("sampleVal >>>" , self.sampleVal);
                let json = JSON.parse(jsonStr);
                let dataList = json;
                return JSON.stringify(dataList);
            }
        },
        columnDefs: [
            {
                targets: 0,
                data : "snd_set_idx",
                orderable : false,
                render : function(data, type, row){
                    let $idCheckBox = $("<input type='checkbox'/>")
                    return $idCheckBox.prop("outerHTML")
                }
            },
            {
                targets: 1,
                data : "media_url"
            },
            {
                targets: 2,
                data : "reg_dt",
                render : function(data,type,row){
                    return data ? moment(data).format("YYYY/MM/DD HH:mm") : "-";
                }
            },
            {
                targets: 3,
                data : "snd_cate"
            },
            {
                targets: 4,
                data : "snd_sub_cate"
            },
            {
                targets: 5,
                data : "version"
            },
            {
                targets: 6,
                data : "lp_data_len"
            },
            {
                targets: 7,
                data : "snd_ni_db"
            },
            {
                targets: 8,
                data : "snd_cmnt"
            }
        ],
        paginate: true,
        
    });
    
}
preprocessingPage.prototype.initEvent = function(){
    let self = this;
    $("#datatable_reload_btn").click(function(){
        console.log("reload 클릭!")
        self.preprocessingDataTable.ajax.reload();
    });
    // 체크박스
    // $("#preprocessingItemList").on("click","input[type='checkbox']",function(){
    //     let $tr = $(this).parents("tr");
    //     let rowInfo = self.preprocessingDataTable.row($tr).data();
    //     console.log("rowInfo >>>", rowInfo);
    // });

    $("#preprocessing").on("click",function(){
        let detailIdList = self.checkItemId();
        $.ajax({
            url : "{% url 'preprocessing' %}",
            type : "POST",
            data : JSON.stringify(detailIdList),
            beforeSend : function(xhr){
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            },
            success : function(jsonData){
                console.log("preprocessing jsonData >>>", jsonData)
                self.preprocessingDataTable.ajax.reload();
            },
            error : function(jsonData){
                if(typeof jsonData.responseJSON != "undefined"){
                    console.log("Error Msg >>>",jsonData.responseJSON.msg)
                    alert(jsonData.responseJSON.msg)
                }
            }
        })
    });

    $("#preprocessingDelete").on("click",function(){
        let detailIdList = self.checkItemId();
        $.ajax({
            url : "{% url 'preprocessing_delete' %}",
            type : "POST",
            data : JSON.stringify(detailIdList),
            beforeSend : function(xhr){
                xhr.setRequestHeader("X-CSRFToken", $.cookie('csrftoken'));
            },
            success : function(jsonData){
                console.log("preprocessing delete jsonData >>>", jsonData)
                self.preprocessingDataTable.ajax.reload();
            },
            error : function(jsonData){
                if(typeof jsonData.responseJSON != "undefined"){
                    console.log("Error Msg >>>",jsonData.responseJSON.msg)
                    alert(jsonData.responseJSON.msg)
                }
            }
        })
    });

    $("#wholeChk").on("click",function(){
        if($(this).is(":checked")){
            $("#preprocessingItemList tbody input[type='checkbox']").prop("checked",true);
        }else{
            $("#preprocessingItemList tbody input[type='checkbox']").prop("checked",false);
        }
    });
}
preprocessingPage.prototype.checkItemId = function(){
    let self = this;
    let soundDetailList = []
    $("#preprocessingItemList tbody input[type='checkbox']").each(function(idx, item){
        if($(item).is(":checked")){
            let $tr = $(item).closest("tr");
            let rowInfo = self.preprocessingDataTable.row($tr).data();
            console.log("rowInfo >>>", rowInfo)
            soundDetailList.push(rowInfo["snd_set_idx"]);
        }
    });
    return soundDetailList;
}