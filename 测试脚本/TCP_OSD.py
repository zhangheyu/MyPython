import socket
import json
from ctypes import create_string_buffer
import struct

ip = '192.168.112.92'
port = 8131

client_fd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_fd.connect((ip, port))

OSD_TEXT = {
    "cmd": "set_osd_para",
    "body": {
        "user_osd": {
            "user_osd_param": [{
                "id": 0,
                "display": 1,
                "color": 0,
                "front_size": 3,
                "text": "56ys5LiA6KGM"
            }, {
                "id": 1,
                "display": 1,
                "color": 1,
                "front_size": 3,
                "text": "c2Vjb25kIGxpbmU="
            }, {
                "id": 2,
                "display": 1,
                "color": 2,
                "front_size": 3,
                "text": "dGjkuInooYw="
            }, {
                "id": 3,
                "display": 1,
                "color": 3,
                "front_size": 3,
                "text": "56ys5Zub6KGMT1NEIFRDUCA="
            }],
            "x_pos": 30,
            "y_pos": 20
        }
    }
}

print('send ', OSD_TEXT)
# print(type(OSD_TEXT))
osd_json = json.dumps(OSD_TEXT)
cmd_data = str(osd_json).encode()
cmd_len = len(cmd_data)
buf = create_string_buffer(cmd_len + 8)
struct.pack_into(">2B", buf, 0, 86, 90)  # 'VZ'
struct.pack_into(">I", buf, 4, cmd_len)
struct.pack_into(">" + str(cmd_len) + "s", buf, 8, cmd_data)

client_fd.sendall(buf)
client_fd.close()
