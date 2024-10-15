$(document).ready(function(){

    const dataTransfer = new DataTransfer();
    $("#multi_upload").on("change", function(e){
        const files = e.target.files;
        for (let i = 0; i < files.length; i++) {
            dataTransfer.items.add(files[i]);
        }
        updateFileList();
    });
    // 파일 삭제 시
    $(document).on('click', ".delete_file", function() {
        let index = $(this).val();
        console.log("index >>>", index)
        dataTransfer.items.remove(index);
        updateFileList();
    });
    $("#multi_upload_form").on("submit",function(e){
        e.preventDefault();
        let formData = new FormData($('#multi_upload_form')[0]);
        console.log("submit formData >>>", formData)
        // for (let i = 0; i < dataTransfer.files.length; i++) {
        //     formData.append('files[]', dataTransfer.files[i]);
        // }
        $.ajax({
            url:"{% url 'file_upload_examples:multipart_upload' %}",
            type : "POST",
            data : formData,
            processData: false, // jQuery가 데이터를 처리하지 않도록
            contentType: false,  
            success : function(jsonData){
                console.log("multipart_upload jsonData >>>", jsonData)
            },
            error : function(){

            }
        })
    });


    function updateFileList() {
        $('#file_list').empty();
        const files = dataTransfer.files;
        for (let i = 0; i < files.length; i++) {
            $('#file_list').append(`
                <li>
                    ${files[i].name}
                    <button type="button" class="delete_file" value="${i}">X</button>
                </li>
            `);
        }
        // input에 현재 파일 목록 업데이트
        $('#multi_upload')[0].files = dataTransfer.files;
    }
});
