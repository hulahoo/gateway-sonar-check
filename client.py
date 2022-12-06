import socket

tcp_socket = socket.socket()
tcp_socket.connect(("gateway", 8000))
text = b'URL URL:http://site.com?ycid=123 URL_domain URL_domain:site.com Destination_port dstPort:80 Event_code event_code:403 Event_name eventName:Access Permitted Log_source logSourceType:ZECURION srcAssetName:WGO-ADM00000288.go.rshbank.ru Log_source_identifier logSourceIdentifier:10.26.93.142 Log_source_type logSourceType:ZECURION Source_IP src:10.23.65.66 Source_Net_Name srcAssetName:w62sc.ska000353.go.rshbbank.ru Source_port srcPort:9093'
tcp_socket.send(text)
tcp_socket.close()
