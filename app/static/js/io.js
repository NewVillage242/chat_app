const url = 'http://' + document.domain + ":8000"
var socket = io.connect(url)

// Customize the behavior of clicking the send button.
document.addEventListener('DOMContentLoaded', ()=>{
    document.querySelector(".input-box").addEventListener('submit', (event) => {
        event.preventDefault()
        let form = document.querySelector('.input-box')
        const formData = new FormData(form)
        fetch('/messages/send_message', {
        method: 'POST',
        body: formData
        })
        let author = document.querySelector("#author").value
        let message= document.querySelector("#message").value
        const messageData = {
        "author": author,
        "message":message,
        }
        socket.emit('text', messageData)
        document.querySelector("#message").value=""
    })
})

// If get `message` from server
socket.on('message', function(data) {
    console.log('Received from server: ', data)
    // Insert new message to chatting room
    const tbody = document.querySelector('tbody')
    const newRow = document.createElement('tr')
    const me = document.querySelector('#author').value 
    if(data.author == me) {
        newRow.classList.add('user')
    }

    const idCell = document.createElement('td')
    idCell.classList.add('id')
    idCell.textContent = 112
    newRow.appendChild(idCell)

    const authorCell = document.createElement('td')
    authorCell.classList.add('author')
    authorCell.textContent = data.author
    newRow.appendChild(authorCell)

    const messageCell = document.createElement('td')
    if(data.author == me){
        messageCell.classList.add('message', 'user_message')
    } else {
        messageCell.classList.add('message')
    }
    messageCell.textContent = data.message
    linkfy(messageCell)
    newRow.appendChild(messageCell)

    const lastRow = tbody.lastElementChild
    if(lastRow){
        tbody.insertBefore(newRow, lastRow)
    } else {
        tbody.appendChild(newRow)
    }
    scrollToBottom()
})        

function linkfy(cell) {
    const urlRegex = /(http:\/\/|https:\/\/)([a-zA-Z0-9\-._~:\/?#\[\]@!$&'()*+,;=]+)/g;
    
    // Replace URLs with anchor tags
    cell.innerHTML = cell.innerHTML.replace(urlRegex, function(url) {
        return `<a href="${url}" target="_blank">${url}</a>`;
        });
    return cell 
}