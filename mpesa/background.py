from threading import Timer


class RepeatedTimer(object):
    def __init__(self, interval, function, checkoutRequestId):
        self._timer = None
        self.interval = interval
        self.function = function
        self.checkoutRequestId = checkoutRequestId
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        result = self.function(self.checkoutRequestId)

        if result[0]:
            print(result[1])
            self.stop()
        else:
            print(result[1])

    def start(self):
        if not self.is_running:
            self._timer = Timer(self.interval, self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False
