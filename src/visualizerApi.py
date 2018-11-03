import argparse
from concurrent.futures import ThreadPoolExecutor
import json
import logging.config
import os
from time import time, sleep

from tornado import gen
from tornado.ioloop import  IOLoop
from tornado.routing import URLSpec
from tornado.web import  RequestHandler, Application

executor = ThreadPoolExecutor(max_workers=100)

#AyncHandler supporting non-async functions. Eg: sleep
class AsyncHandler(RequestHandler):
    @gen.coroutine
    def get(self):
        logger.debug('RootHandler get called')
        t = time()
        res = yield executor.submit(lambda:self.blocking_task())
        self.write("Started at {} got {}".format(t, res))
        self.finish()
    
    def blocking_task(self):
        logger.info('executing getHomePage in background thread')
        sleep(10)
        return "Visualizer API"

class RootHandler(RequestHandler):  
    
    def get(self):
        self.write("Running")
        #self.finish
    
def getWebApplication():
    routes = [
        URLSpec(r"/", RootHandler),
        URLSpec(r"/async", AsyncHandler),
        URLSpec(r"/sync", RootHandler)
    ]
    return Application(routes, debug=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--port", action="store", type=int, default=7212, dest="port", help="Override default port on which server runs")
    args = parser.parse_args()
    path="../conf/logging.json"
    if os.path.exists(path):
        with open(path, 'rt') as f:
            config = json.load(f)
        logging.config.dictConfig(config)
    else:
        print('logging config not found. using basic logger')
        logging.basicConfig(level="INFO")
    logger = logging.getLogger("visualizer")
    
    app = getWebApplication()
    app.listen(args.port)
    logger.info(' Visualizer app started on port:%s',args.port)
    IOLoop.instance().start()