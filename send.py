import socket
import cv2
import numpy
from imutils.video import FileVideoStream
from imutils.video import FPS
import imutils
import pxssh


def start_tcp(hosts):
    for i in range(len(hosts)):
    s = pxssh.pxssh()
    if not s.login (hosts[i], 'remoteman', 'cheese'):
        print "SSH session failed on login."
        print str(s)
    else:
        print "SSH session login successful"
        s.sendline ('uptime')
        s.prompt()         # match the prompt
        print s.before     # print everything before the prompt.
        s.logout()
#We can also execute multiple command like this:
s.sendline ('uptime;df -h')
tcp_ip = ['129.169.172.176','129.169..172.175']
TCP_PORT = 5001
video="video.mp4"
counter = 0
fvs = FileVideoStream(video).start()
def send():
    if(fvs.more()):
        sock = socket.socket()
        sock.connect((tcp_ip[counter%2], TCP_PORT))
        frame = fvs.read()
        cv2.imshow("Frame", frame)
        cv2.waitKey(1)
        encode_param=[int(cv2.IMWRITE_JPEG_QUALITY),90]
        result, imgencode = cv2.imencode('.jpg', frame, encode_param)
        data = numpy.array(imgencode)
        stringData = data.tostring()
        sock.send( str(len(stringData)).ljust(16));
        sock.send( stringData );
        print("Data sent, should be on frame", counter)
        sock.close()
        counter+=1
        send()
    else:
        return False
send()
cv2.destroyAllWindows()
fvs.stop()

