from flask_socketio import emit

def socketio_message_handlers(socketio):
  @socketio.on('text')
  def text(messageData):
    author = messageData.get('author', '')
    message = messageData.get('message', '')
    response_data = {
      'author': author,
      'message': message,
    }
    emit('message', response_data, broadcast=True )
  
  @socketio.on('greeting')
  def handle_message(data):
    emit('response', 'Message received: ' + data)