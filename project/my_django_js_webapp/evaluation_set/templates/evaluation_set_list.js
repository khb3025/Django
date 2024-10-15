$(document).ready(function(){
    $("#evaluation_set_list_table").DataTable({
        ordering: true,
        stateSave: false, // 캐시 비활성화
        order: [[0, "desc"]],
        ajax: {
            url: "{% url 'evaluation_set_list' %}",
            method: "POST",
            data: {
                "csrfmiddlewaretoken": $.cookie("csrftoken")
            }
        },
        columnDefs: [
            {
                targets: 0,
                data: "noise__ni_info",
                render: function (data) {
                    return data ? moment(data).format("YYYY/MM/DD HH:mm:ss") : "-";
                }
            },
            {
                targets: 1,
                data: "noise__ni_info"
            },
            {
                targets: 2,
                data: "noise__ni_info",
                render: function(data){
                    return data;
                }
            },
            {
                targets: 3,
                data: "noise__ni_info",
                render: function(data){
                    return "";
                }
            },
            {
                targets: 4,
                data: "noise__ni_info",
                render: function (data) {
                    return data ? moment(data).format("YYYY/MM/DD HH:mm:ss") : "-";
                }
            },
            {
                targets: 5,
                data: "noise__ni_info",
                render: function (data) {
                    return data ? moment(data).format("YYYY/MM/DD HH:mm:ss") : "-";
                }
            },
            {
                targets: 6,
                data: "noise__ni_info",
                render: function (data) {
                    return data ? moment(data).format("YYYY/MM/DD HH:mm:ss") : "-";
                }
            },
            {
                targets: 7,
                data: "cre_dt",
                render: function (data) {
                    return data ? moment(data).format("YYYY/MM/DD HH:mm:ss") : "-";
                }
            },
            {
                targets: "_all",
                defaultContent: "-",
                render: function (data, type, row, meta) {
                    if (type === "display" && $.isNumeric(data)) {
                        // 숫자인 경우 원하는 서식으로 변환
                        return data ? $.fn.dataTable.render.number( "," ).display(data) : "0";
                    } else {
                        return data; // 숫자가 아닌 경우 원래 값 반환
                    }
                }
            }
        ],
        initComplete: function () {
        }
    });

    $("#source_data_list_table").DataTable({
        ordering: true,
        stateSave: false, // 캐시 비활성화
        order: [[0, "desc"]],
        ajax: {
            url: "{% url 'evaluation_set_list' %}",
            method: "POST",
            data: {
                "csrfmiddlewaretoken": $.cookie("csrftoken")
            }
        },
        columnDefs: [
            {
                targets: 0,
                data: "noise__ni_info",
                render: function (data) {
                    return data ? moment(data).format("YYYY/MM/DD HH:mm:ss") : "-";
                }
            },
            {
                targets: 1,
                data: "noise__ni_info"
            },
            {
                targets: 2,
                data: "noise__ni_info",
                render: function(data){
                    return data;
                }
            },
            {
                targets: 3,
                data: "noise__ni_info",
                render: function(data){
                    return "";
                }
            },
            {
                targets: 4,
                data: "noise__ni_info",
                render: function (data) {
                    return data ? moment(data).format("YYYY/MM/DD HH:mm:ss") : "-";
                }
            },
            {
                targets: 5,
                data: "noise__ni_info",
                render: function (data) {
                    return data ? moment(data).format("YYYY/MM/DD HH:mm:ss") : "-";
                }
            },
            {
                targets: 6,
                data: "noise__ni_info",
                render: function (data) {
                    return data ? moment(data).format("YYYY/MM/DD HH:mm:ss") : "-";
                }
            },
            {
                targets: 7,
                data: "cre_dt",
                render: function (data) {
                    return data ? moment(data).format("YYYY/MM/DD HH:mm:ss") : "-";
                }
            },
            {
                targets: "_all",
                defaultContent: "-",
                render: function (data, type, row, meta) {
                    if (type === "display" && $.isNumeric(data)) {
                        // 숫자인 경우 원하는 서식으로 변환
                        return data ? $.fn.dataTable.render.number( "," ).display(data) : "0";
                    } else {
                        return data; // 숫자가 아닌 경우 원래 값 반환
                    }
                }
            }
        ],
        initComplete: function () {
        }
    });
})

function file_upload(){

    var file = $("#orgLicenseFile")[0].files[0];

    if (file != undefined) {

        var obj = new FormData();

        obj.append("files", $("#orgLicenseFile")[0].files[0]);
        obj.append("csrfmiddlewaretoken", $.cookie("csrftoken"));

        $.ajax({
            url: "{% url 'new_data_set_upload' %}",
            method: "POST",
            data: obj,
            contentType: false,
            processData: false,
            success: function (data) {
                if(data.success){
                    alert(data.msg);
                }
            }
        });

    }else{
    }

}

function existing_source_data_selection_excel_download(){
    $.ajax({
        url: "{% url 'existing_source_data_selection_excel_download' %}",
        method: "POST",
        data: {
            "csrfmiddlewaretoken": $.cookie("csrftoken")
        },
        success: function(data){
            if(data.success){
                const tag_a = document.createElement("a");
                tag_a.href = data.save_path;
                tag_a.download = data.file_name;
                tag_a.click();
            }else{
                alert(data.message);
            }
        },
    })
}