function deleteNote(noteid){
    fetch("/delete-note",{method: "POST",body : JSON.stringify({noteId:noteid}),}).then((_res)=>{
        window.location.href = "/home";
    });
}


function noteDone(noteid){
    fetch("/note-done",{method: "POST",body : JSON.stringify({noteId:noteid}),}).then((_res)=>{
        window.location.href = "/home";
    });
}

