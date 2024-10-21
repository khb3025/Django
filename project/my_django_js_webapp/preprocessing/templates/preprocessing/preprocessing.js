$(document).ready(function(){

    let page = new preprocessingPage();
    page.init();
});

function preprocessingPage(){
    this.sampleVal = 1;
    this.preprocessingDataTable = undefined;
    this.beforePreprocessingDatatable = undefined;

    this.waveSurfer = undefined;
    this.regionsPlugin = undefined;
    this.activeRegion = undefined;
    this.regionsLoop = true;

    this.timeLinePlugin = undefined;


    this.langKor = {
        select : {
                rows : ""
        },
        decimal : "",
        emptyTable : "데이터가 없습니다.",
        //info : "_START_ - _END_ (총 _TOTAL_ 명)",
        info : "_TOTAL_",
        infoEmpty : "0명",
        infoFiltered : "(전체 _MAX_ 명 중 검색결과)",
        infoPostFix : "",
        thousands : ",",
        lengthMenu : "_MENU_",
        loadingRecords : "로딩중...",
        processing : "처리중...",
        search : "검색 : ",
        zeroRecords : "검색된 데이터가 없습니다.",
        paginate : {
            "first" : "첫 페이지",
            "last" : "마지막 페이지",
            "next" : "다음",
            "previous" : "이전"
        },
        aria : {
                "sortAscending" : " :  오름차순 정렬",
                "sortDescending" : " :  내림차순 정렬"
        }
    }
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
        lengthMenu: [[10, 25, 50, -1], ["10개씩 보기", "20개씩 보기", "50개씩 보기", "All"]],
        ajax: {
            url: "{% url 'preprocessing:get_preprocessing_list' %}",
            type: "POST", 
            headers: {
                'X-CSRFToken': $("#csrf_token").val()
            },
            data: function( d ){

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
                    let $checkDiv = $("<div class='checkbox-custom checkbox-warning'></div>");
                    let $checkInput = $("<input type='checkbox' id='checkItem'>");
                    let $checkLabel = $("<label for='checkItem'></label>");
                    $checkDiv.append($checkInput);
                    $checkDiv.append($checkLabel);
                    return $checkDiv.prop("outerHTML")
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
        buttons : [
            {
                text : "엑셀다운",
                className : "datatable-btn-excel",
                action : function(e, dt, node, config) {
                        console.log(e);
                        console.log(dt);
                        console.log(node);
                        console.log(config);
                }
            },
            {
                text : "정제",
                className : "datatable-btn-normal",
                action: function (e, dt, node, config, cb) {
                    console.log("정제버튼 클릭")
                    $.magnificPopup.open({
                        items: {
                            src: $("#preprocessingBeforePopup").html()
                        },
                        mainClass: 'modal-block-lg'
                    });
                    
                    // 정제 버튼 클릭시 beforeProcessingDataTable 셋팅.
                    // mfp-content 내 복제된 테이블로 적용
                    // mfp-content 는 magnificPopup이 닫힐때 지워짐
                    let copyTable = $(document).find(".mfp-content #beforePreprocessingItemList");
                    copyTable.attr("id","copyPreprocessingBeforePopup")
                    console.log("copyTable Info data >>>", copyTable.attr("id"))
                    self.beforePreprocessingDatatable = $("#copyPreprocessingBeforePopup").DataTable({
                        stateSave: false, 
                        autoWidth: false,
                        ajax : {
                            url: "{% url 'preprocessing:get_origin_source_list' %}",
                            type: "POST", 
                            headers: {
                                'X-CSRFToken': $("#csrf_token").val()
                            },
                            data: function( d ){
                
                            },
                            dataFilter : function(jsonStr){
                                console.log("sampleVal >>>" , self.sampleVal);
                                console.log("jsonStr >>>" , jsonStr);
                                
                                let json = JSON.parse(jsonStr);
                                let dataList = json;
                                return JSON.stringify(dataList);
                            }
                        },
                        columnDefs: [
                            {
                                targets: 0,
                                data : "data_set_idx",
                                orderable : false,
                                render : function(data, type, row){
                                    let $checkDiv = $("<div class='checkbox-custom checkbox-warning'></div>");
                                    let $checkInput = $("<input type='checkbox' id='checkItem'>");
                                    let $checkLabel = $("<label for='checkItem'></label>");
                                    $checkDiv.append($checkInput);
                                    $checkDiv.append($checkLabel);
                                    return $checkDiv.prop("outerHTML")
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
                                data : "video_path"
                            },
                            {
                                targets: 6,
                                data : "snd_place"
                            },
                            {
                                targets: 7,
                                data : "version" // 상태값대신사용
                            }
                        ],
                        searching : false,
                        lengthMenu: [[10, 30, 50, -1], ["10개씩 보기", "30개씩 보기", "50개씩 보기", "All"]],
                        buttons : [
                            {
                                text : "엑셀다운",
                                className : "datatable-btn-excel",
                                attr : {
                                    role : "excelDown"
                                },
                                action : function(e, dt, node, config) {
                                        console.log(e);
                                        console.log(dt);
                                        console.log(node);
                                        console.log(config);
                                }
                            },
                            {
                                text : "파일 검증",
                                className : "datatable-btn-normal",
                                attr : {
                                    role : "audioFileVerification"
                                },
                                action : function(e, dt, node, config) {
                                    let detailIdList = self.beforePreprocessingChkItemId();
                                    $.ajax({
                                        url : "{% url 'preprocessing:confirm_library_active' %}",
                                        type : "POST",
                                        data : JSON.stringify(detailIdList),
                                        beforeSend : function(xhr){
                                            xhr.setRequestHeader("X-CSRFToken", $("#csrf_token").val());
                                        },
                                        success : function(jsonData){
                                            console.log("preprocessing jsonData >>>", jsonData)
                                            alert("파일 검증 완료");
                                            /*
                                            new PNotify({
                                                title: 'File State Change',
                                                text: '검증이 완료 되었습니다.',
                                                type: 'custom',
                                                addclass: 'notification-success',
                                                icon: 'fa fa-check'
                                            });
                                            */
                                            self.beforePreprocessingDatatable.ajax.reload();
                                        },
                                        error : function(jsonData){
                                            if(typeof jsonData.responseJSON != "undefined"){
                                                console.log("Error Msg >>>",jsonData.responseJSON.msg)
                                                alert(jsonData.responseJSON.msg)
                                            }
                                        }
                                    })
                                }
                            },
                            {
                                text : "전처리 화면",
                                className : "modal-with-form datatable-btn-confirm",
                                attr : {
                                    role : "audioFileVerification"
                                },
                                action : function(e, dt, node, config) {
                                    let metaIdList = self.beforePreprocessingChkItemId();
                                    console.log("detailIdList >>>", metaIdList)
                                    if(metaIdList.length == 0){
                                        alert("전처리하고자 하는 파일을 선택하세요.");
                                        return false;
                                    }else if(metaIdList.length > 1){
                                        alert("전처리하고자 하는 파일을 하나만 선택하세요.");    
                                        return false;
                                    }
                                    let metaId = metaIdList[0];
                                    self.waveSurfer = undefined;
                                    self.regionsPlugin = undefined;
                                    
                                    // 한 화면에 여러 음원파일을 넣어야 할 수 있음으로 eq(0)를 통한코드 작성
                                    $("#waveform div").eq(0).remove();
                                    $("#waveform label").eq(0).remove();
                                    self.regionsPlugin = RegionsPlugin.create();
                                    self.timeLinePlugin = TimelinePlugin.create();
                                    let $loopLabel = $("<label>Loop regions</label>");
                                    let $loopChk = $("<input type='checkbox' checked/>");
                                    let $metaId = $("<input type='hidden' value='"+metaId+"'>")
                                    $loopLabel.prepend($loopChk);
                                    $loopLabel.append($metaId);
                                    $("#waveform").append($loopLabel);
                                    self.waveSurfer = WaveSurfer.create({
                                        container: "#waveform",
                                        waveColor: "#4F4A85",
                                        progressColor: "#383351",
                                        mediaControls: true,
                                        url: "{% url 'preprocessing:show_audio_wave' %}?id="+metaId,
                                        plugins: [
                                            self.regionsPlugin,
                                            self.timeLinePlugin
                                        ],
                                    });
                                    const randomColor = () => `rgba(${Math.random(0, 255)}, ${Math.random(0, 255)}, ${Math.random(0, 255)}, 0.5)`
                                    self.waveSurfer.on("decode",function(){
                                        self.regionsPlugin.addRegion({
                                            start: 0,
                                            end: 5,
                                            content: "Resize me",
                                            color: randomColor(),
                                            drag: true,
                                            resize: true,
                                          })
                                    });
                                    self.waveSurfer.on('error', function (error) {
                                        console.error('WaveSurfer error:', error);
                                        alert('오디오 파일을 로드하는 데 문제가 발생했습니다. 파일을 확인하세요.');
                                    });
                                    // region 설정
                                    self.regionsPlugin.on('region-created', (region) => {
                                        if (!self.activeRegion) {
                                            self.activeRegion = region; // 첫 번째 region을 기본 activeRegion으로 설정
                                        }
                                    });
                                    self.regionsPlugin.on('region-in',(region, e) => {
                                        console.log('region-in', region)
                                        self.activeRegion = region
                                    })
                                    self.regionsPlugin.on('region-out', (region) => {
                                        console.log('region-out', region)
                                        if (self.activeRegion === region) {
                                            if(self.regionsLoop){
                                                region.play()
                                            }else{
                                                self.activeRegion = null
                                            }
                                        }
                                    })
                                    // region 클릭 이벤트
                                    self.regionsPlugin.on('region-clicked', (region, e) => {
                                        console.log("region >>> " , region)
                                        e.stopPropagation() // prevent triggering a click on the waveform
                                        self.activeRegion = region
                                        region.play()
                                        region.setOptions({ color: randomColor() })
                                    });
                                    $("#preprocessingPopup").modal("show");
                                
                                    
                                }
                            }
                        ],
                        dom : "<'col-sm-2'i><'col-sm-10 pr0'Bl>frtp",
                        language : self.langKor
                    
                    });
                }
                    
                
            },    
            {
                text : "삭제",
                className : "datatable-btn-normal",
                action : function(e, dt, node, config) {
                        console.log(e);
                        console.log(dt);
                        console.log(node);
                        console.log(config);
                }
            }, 
            
        ],
        dom : "<'col-sm-2'i><'col-sm-10 pr0'Bl>frtp",
        language : self.langKor
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

    $("#preprocessingDelete").on("click",function(){
        let detailIdList = self.beforePreprocessingChkItemId();
        $.ajax({
            url : "{% url 'preprocessing:preprocessing_delete' %}",
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



    // 원천데이터 팝업
    // 닫기
    $("#preprocessingPopupClose").click(function(e){
        e.stopPropagation();
        self.waveSurfer.pause();
        $('#preprocessingPopup').modal("hide");
    });
    // 원천데이터 전체 체크
    $(document).on("change", ".mfp-content #beforeWholeChk", function(){
        if($(this).is(":checked")){
            $("#copyPreprocessingBeforePopup tbody input[type='checkbox']").prop("checked",true);
        }else{
            $("#copyPreprocessingBeforePopup tbody input[type='checkbox']").prop("checked",false);
        }
    });


    // 전처리 Region 무한루프 on, off [# 하나의 파일에 대해서만 구현중]
    //$(document).on("click","#waveform > label > input[type=checkbox]",function(){
    $(document).on("change", "#waveform > label:eq(0) input[type='checkbox']", function(){
        console.log("change!!!")
        if($(this).is(":checked")){
            self.regionsLoop = true;
        }else{
            self.regionsLoop = false;
        }
    });

    $("#preprocessing").on("click", function(){
        
        console.log("region >>>", self.activeRegion);
        console.log("id >>>" , self.activeRegion["id"]);
        console.log("start >>>" , self.activeRegion["start"]);
        console.log("end >>>" , self.activeRegion["end"]);
        let sliceInfoList = []
        $("#waveform label").each(function(idx, item){
            let metaId = $(item).find("input[type='hidden']").val();
            let sliceInfo = {}
            sliceInfo["id"] = metaId
            // 여러 Wave를 처리하도록 바뀌게 되면 activeRegion은 activeRegionList로써
            // 복수 객체가 만들어질 예정
            sliceInfo["start"] = self.activeRegion["start"];
            sliceInfo["end"] = self.activeRegion["end"];
            sliceInfoList.push(sliceInfo);
        });
        console.log("preprocessing sliceInfo >>>",sliceInfoList);
        $.ajax({
            url : "{% url 'preprocessing:preprocessing' %}",
            type : "POST",
            headers: {
                'X-CSRFToken': $("#csrf_token").val()
            },
            data : JSON.stringify(sliceInfoList),
            success : function(jsonData){
                console.log("jsonData >>>", jsonData);
                if(typeof jsonData["result_list"] != "undefined"){
                    $.each(jsonData["result_list"], function(idx, item){
                        let msg = "원본 파일명: " + item["origin_file_name"] + "\n"
                        msg += "전처리 파일명: " + item["preprocessing_file_name"] +"\n"
                        msg += "============================\n"                        
                        alert(msg);
                    });
                } 
            },
            error : function(){

            }
        });
    });

}
preprocessingPage.prototype.beforePreprocessingChkItemId = function(){
    let self = this;
    let metadataList = []

    self.beforePreprocessingDatatable.rows().every(function(rowIdx, tableLoop, rowLoop) {
        let rowData = this.data(); // 현재 행의 데이터
        let $row = $(this.node()); // 현재 행의 DOM 노드

        // 현재 행의 체크박스 선택
        let $checkbox = $row.find("input[type='checkbox']");
        if ($checkbox.is(":checked")) {
            console.log("rowInfo >>>", rowData);
            metadataList.push(rowData["data_set_idx"]); // 데이터 추가
            
        }
    });

    console.log("metadataList >>>", metadataList);
    return metadataList;
}