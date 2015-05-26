from twisted.internet import reactor
from twisted.python import log
from interceptor import ProxyFactory
from modeller import ModellerListener
from analyser import AnalyserListener
from common import REDIS_POOL, config
import sys, getopt


def main(argv):
    log.startLogging(sys.stdout)

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
            pass

        elif opt in ("-i", "--modeller"):
            # run modeller
            pass

        elif opt in ("-i", "--analyser"):
            # run analyser
            pass

        elif opt in ("-i", "--dashboard"):
            # run dashboard
            pass

    # initialize the ModellerListener and listen on a separate thread
    ml = ModellerListener(connection_pool=REDIS_POOL)
    ml.listen()

    # initialize the AnalyserListener and listen on a separate thread
    al = AnalyserListener(connection_pool=REDIS_POOL)
    al.listen()

    # initialize and start the interceptor reactor
    reactor.listenTCP(config.interceptor.get('port', 9191), ProxyFactory())
    reactor.run()

    # this is only reachable once the reactor
    # is shutdown. once the reactor receive SIGINT
    # and shutdown stop the Event Listeners too.
    ml.stop()
    al.stop()
    pass


if __name__ == '__main__':
    main(sys.argv[1:])
    pass