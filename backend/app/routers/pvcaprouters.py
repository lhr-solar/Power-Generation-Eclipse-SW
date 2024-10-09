from fastapi import APIRouter
import serial.tools.list_ports

pvcap_router = APIRouter(prefix='/pvcap')

@pvcap_router.get('/get-open-com-ports')
def get_open_com_ports():
    com_ports = [port for port in serial.tools.list_ports.comports()]
    print(com_ports)
    com_ports.append('COM3')
    com_ports.append('COM1')
    com_ports.sort()
    return com_ports