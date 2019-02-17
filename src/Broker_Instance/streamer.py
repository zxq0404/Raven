import zmq

def main():

    try:
        context = zmq.Context(1)
        # Socket facing clients
        frontend = context.socket(zmq.PULL)
        frontend.bind("tcp://*:5556")

        # Socket facing services
        backend = context.socket(zmq.PUSH)
        backend.bind("tcp://*:5557")

        zmq.device(zmq.STREAMER, frontend, backend)
    except Exception as e:
        print(e)
        print("bringing down zmq device")
    finally:
        pass
        frontend.close()
        backend.close()
                                                              1,1           Top
if __name__ == "__main__":
    main()
