 document.addEventListener('DOMContentLoaded', ()=>{
            update_screen_view()
            
            make_url_clickable()

            // Convert table to chat bubbles.
            const uname =  window.location.pathname.split('/')[2]
            document.querySelector("thead").style.display = 'none'
            document.querySelector("table").classList.remove("table-dark")
            const rows = document.querySelectorAll("tbody tr ")
            rows.forEach(row => {
                const authorCell = row.querySelector('.author')
                if(authorCell && authorCell.textContent.trim() === uname){
                    row.classList.add('user')
                    row.querySelector('.message').classList.add('user_message')
                }
            })
            let emptyTR = document.createElement("tr")
            emptyTR.classList.add("emptyTR")
            document.querySelector("tbody").appendChild(emptyTR)
            scrollToBottom()
        })
function scrollToBottom() {
            const chatContainer = document.querySelector('.messages');
            chatContainer.scrollTop = chatContainer.scrollHeight;
        }
        window.addEventListener('resize', ()=>{
          // shorten 'send message' to 'send' while window's width is short.
          update_screen_view()
        })
        function update_screen_view(){
            if(window.innerWidth > 600){
                document.querySelector(".btn_send").value = 'Send Message'
            } else {
                document.querySelector('.btn_send').value = 'Send'
            }
        }
        function make_url_clickable(){
            const messageCells = document.querySelectorAll("td.message");
            const urlRegex = /(http:\/\/|https:\/\/)([a-zA-Z0-9\-._~:\/?#\[\]@!$&'()*+,;=]+)/g;
            
            messageCells.forEach(function(cell) {
            // Replace URLs with anchor tags
            cell.innerHTML = cell.innerHTML.replace(urlRegex, function(url) {
                return `<a href="${url}" target="_blank">${url}</a>`;
                });
            });

        }