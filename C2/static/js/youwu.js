function Active(id){
    var navi = document.getElementById(id);
    navi.className = "active";
}
function CreateNameTD(Name){
    var text_name=document.createTextNode(Name);
    var table_data=document.createElement('td');
    table_data.appendChild(text_name);
    return table_data;
}
function CreateBinaryTD(Binary){
    var table_data=document.createElement('td');
    for(i in Binary){
        var bin = Binary[i];
        var name=bin[0];
        var path=bin[1];
        var hyperlink = CreateDownloadHref(name,path)
        table_data.appendChild(hyperlink);
        table_data.appendChild(document.createElement("br"));
    }
    return table_data;
}
function CreateDownloadHref(Name,Path){
    var hyperlink = document.createElement('a');
    url="/Download?type=Daily&path="+Path
    hyperlink.href=url;
    hyperlink.onclick =function() {
        return confirm("是否确认下载?");
    };
    hyperlink.download ="";
    var text_name=document.createTextNode(Name);
    hyperlink.appendChild(text_name);
    return hyperlink;
}
function CreateCommitHistoryHref(Path){
    var hyperlink = document.createElement('a');
    url="/CommitHistory?type=Daily&path="+Path
    hyperlink.href=url;
    var text_name=document.createTextNode("查看");
    hyperlink.appendChild(text_name);
    return hyperlink;
}
function CreateDebugInfo(DebugInfo){
    var table_data=document.createElement('td');
    for(i in DebugInfo){
        var info = DebugInfo[i];
        var name=info[0];
        var path=info[1];
        var hyperlink = CreateDownloadHref(name,path)
        table_data.appendChild(hyperlink);
        table_data.appendChild(document.createElement("br"));
    }
    return table_data;
}
function CreateCommitHistory(CommitHistory){
    var table_data=document.createElement('td');
    if (CommitHistory != "None"){
        var hyperlink = CreateCommitHistoryHref(CommitHistory)
        table_data.appendChild(hyperlink);
    }
    return table_data;
}
function CreateReleaseNotesHref(Path){
    var hyperlink = document.createElement('a');
    url="/CommitHistory?type=Daily&path="+Path
    hyperlink.href=url;
    var text_name=document.createTextNode("查看");
    hyperlink.appendChild(text_name);
    return hyperlink;
}
function CreateUpload(Name){
    var table_data=document.createElement('td');
    var URN=CreateUploadButton(Name,"ReleaseNotes");
    var UR=CreateUploadButton(Name,"Report");
    table_data.appendChild(URN);
    table_data.appendChild(document.createElement('br'))
    table_data.appendChild(UR);
    return table_data;
}
function CreateUploadButton(Data,Type){
    var Div=document.createElement('div');
    if (Type=="ReleaseNotes"){
        var ClassName="fileUpload btn btn-primary upload-btn";
        var Name="发布说明";
    }else if (Type=="Report"){
        var ClassName="fileUpload btn btn-success upload-btn";
        var Name="测试报告";
    }
    Div.className=ClassName;
    var Span =document.createElement("span")
    var TextUpload=document.createTextNode(Name);
    Span.appendChild(TextUpload);
    var Input =document.createElement("input");
    Input.type="file";
    Input.className="upload uploadBtn";
    Input.x=Data;
    Input.y=Type;
    Input.addEventListener("change",AjaxUpload);
    Div.appendChild(Span);
    Div.appendChild(Input);
    return Div;
}

function CreateReleaseNotes(ReleaseNotes){
    var table_data=document.createElement('td');
    if (ReleaseNotes != "None"){
        var hyperlink = CreateReleaseNotesHref(ReleaseNotes)
        table_data.appendChild(hyperlink);
    }
    return table_data;
}
function CreateTestReports(TestReports){
    var table_data=document.createElement('td');
    for(i in TestReports){
        var info = TestReports[i];
        var name=info[0];
        var path=info[1];
        var hyperlink = CreateDownloadHref(name,path)
        table_data.appendChild(hyperlink);
        table_data.appendChild(document.createElement("br"));
    }
    return table_data;
}

function AjaxUpload(){
        var xhr = new XMLHttpRequest();
        var formData = new FormData();
        var file = this.files[0];
        var file_name= file.name;
        formData.append('file',file);
        formData.append('version',this.x);
        formData.append('type',this.y);
        xhr.open('post', '/Upload/', true);
        xhr.onreadystatechange = function () {
            if (xhr.readyState == 4) {
                var response=xhr.responseText;
                alert(response);
                if(response=="上传成功"){
                    location.reload();
                }
            }
        };
        xhr.send(formData);
}
