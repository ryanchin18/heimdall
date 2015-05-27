import sys
import getopt
from twisted.internet import reactor
from twisted.python import log
from interceptor import ProxyFactory
from modeller import ModellerListener
from analyser import AnalyserListener
from common import REDIS_POOL, config


def main(argv):
    log.startLogging(sys.stdout)
    ml = None
    al = None
    start_interceptor = False
    terminate_immediately = False

    try:
        opts, args = getopt.getopt(argv, "imad", ["interceptor", "modeller", "analyser", "dashboard", "help"])
    except getopt.GetoptError:
        print 'orion.py -imad'
        sys.exit(2)

    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print 'orion.py -imad'
            sys.exit()

        elif opt in ("-i", "--interceptor"):
            # run interceptor
            start_interceptor = True
            pass

        elif opt in ("-m", "--modeller"):
            # initialize the ModellerListener and listen on a separate thread
            ml = ModellerListener(connection_pool=REDIS_POOL)
            ml.listen()
            print 'modeller started.'
            pass

        elif opt in ("-a", "--analyser"):
            # initialize the AnalyserListener and listen on a separate thread
            al = AnalyserListener(connection_pool=REDIS_POOL)
            al.listen()
            print 'analyser started.'
            pass

        elif opt in ("-d", "--dashboard"):
            # run dashboard
            print 'please run dashboard separately.'
            pass

    if start_interceptor:
        # initialize and start the interceptor reactor
        reactor.listenTCP(config.interceptor.get('port', 9191), ProxyFactory())
        reactor.run()
        terminate_immediately = True
        pass

    try:
        while not terminate_immediately:
            # loop to keep modeller and analyser running
            pass
    except KeyboardInterrupt:
        print "stopping orion detection system"
        pass

    # this is only reachable once the reactor
    # is shutdown. once the reactor receive SIGINT
    # and shutdown stop the Event Listeners too.
    if ml is not None:
        ml.stop()
        pass

    if al is not None:
        al.stop()
        pass

    pass


if __name__ == '__main__':
    main(sys.argv[1:])
    pass