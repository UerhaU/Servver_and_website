import socket #импорт сокета

def start_server(): #Данная функция используется в 32 строке для запуска сервера
    try:
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #socket.AF_INET - ivp4 , socket.SOCK_STREAM - tcp
        server.bind(('/////////',2000)) #Адрес и порт, в моем случае локальный запуск на домашней сети
        server.listen(4) #до 4 подклчюений в очереди
        while True:
            print("Working...")
            client_socket, address = server.accept() #сокет для обмена данным с клиентом, адрес - адрес клиента
            data = client_socket.recv(1024).decode('utf-8')  #получение от клиентов до 1024 байта, декадировка из utf8 в байты
            content = load_page(data)  #переменная для функции для формирования содержимого страницы, декодировка идет от строки выше
            client_socket.send(content) #Сервер отправляет содержимое страницы клиенту, выполняя все действия которые присвоены выше
            client_socket.shutdown(socket.SHUT_WR) #cервер закрывает соединение на запись, указывая, что больше данных отправляться не будет
    except KeyboardInterrupt: #При нажатий клавиши ctrl c происходит следующее
        server.close() #Сокет закрывается
        print("Shitdown")

def load_page(request): #Данная функция
    HDRS = 'HTTP/1.1 200 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n' #HTTP/1.1 200 OK статус успешного ответа + указывает что содержимое html в кодирвоке utf8
    HDRS_404 = 'HTTP/1.1 404 OK\r\nContent-Type: text/html; charset=utf-8\r\n\r\n'#Всё то же самое, но статус не найденной страницы
    path = request.split(' ')[1] #разбитие запроса на части, извлекается путь к ресурсу
    response = '' #объявление переменной
    try:
        with open('views'+path,'rb') as file: #файл окутывается в режиме чтение бинарных файлов + путь
            response = file.read() #файл читается и сохраняется в переменную
        return HDRS.encode('utf-8') + response #возращение ответа с содержимым файла
    except FileNotFoundError: #если файла нет
        return (HDRS_404+'Данной страницы не существует').encode('utf-8') #Возвращаем инф

if __name__ == '__main__':
    start_server()
