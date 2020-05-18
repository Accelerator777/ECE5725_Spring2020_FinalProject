import multiprocessing
import subprocess
import time

def convertor_0():
    name = multiprocessing.current_process().name
    print (name, 'Starting')
    bashCommand_0 = "ffmpeg -i out0.wav temp0.mp3"
    output = subprocess.check_output(['bash','-c', bashCommand_0])
    print (name, 'Exiting')

def convertor_1():
    name = multiprocessing.current_process().name
    print (name, 'Starting')
    bashCommand_1 = "ffmpeg -i out1.wav temp1.mp3"
    output = subprocess.check_output(['bash','-c', bashCommand_1])
    print (name, 'Exiting')

def convertor_2():
    name = multiprocessing.current_process().name
    print (name, 'Starting')
    bashCommand_2 = "ffmpeg -i out2.wav temp2.mp3"
    output = subprocess.check_output(['bash','-c', bashCommand_2])
    print (name, 'Exiting')

def convertor_3():
    name = multiprocessing.current_process().name
    print (name, 'Starting')
    bashCommand_3 = "ffmpeg -i out3.wav temp3.mp3"
    output = subprocess.check_output(['bash','-c', bashCommand_3])
    print (name, 'Exiting')

# if __name__ == '__main__':
def parallel_convertor():
    worker_0 = multiprocessing.Process(name='worker 0', target=convertor_0)
    worker_1 = multiprocessing.Process(name='worker 1', target=convertor_1)
    worker_2 = multiprocessing.Process(name='worker 2', target=convertor_2)
    worker_3 = multiprocessing.Process(name='worker 3', target=convertor_3)

    worker_0.start()
    worker_1.start()
    worker_2.start()
    worker_3.start()

    worker_0.join()
    worker_1.join()
    worker_2.join()
    worker_3.join()