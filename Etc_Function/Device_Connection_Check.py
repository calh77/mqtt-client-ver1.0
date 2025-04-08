import time
import threading

class connectionManager:
    """
    이 클래스는 디바이스 데이터를 주기적으로 확인하여, 오프라인 상태를 체크합니다.
    """
    def __init__(self, device_data, check_interval=60, timeout_seconds=600):
        """
        :param device_data: 외부에서 주입받은 device_data (defaultdict)
        :param check_interval: 주기적 체크 간격(초)
        :param timeout_seconds: 마지막 수신 후 오프라인 판정 시간(초)
        """
        self.device_data = device_data
        self.check_interval = check_interval
        self.timeout_seconds = timeout_seconds
        self.timer_started = False

    def update_device_data(self, device_id, payload, timestamp):
        """ device_data 업데이트 """
        self.device_data[device_id]["count"] += 1
        self.device_data[device_id]["last_payload"] = payload
        self.device_data[device_id]["last_time"] = timestamp

    def start_offline_checker(self):
        if not self.timer_started:
            self.timer_started = True
            threading.Timer(self.check_interval, self._check_offline_devices).start()

    def _check_offline_devices(self):
        now = time.time()
        for device_id, data in self.device_data.items():
            last_time = data["last_time"]
            if last_time is not None:
                diff = now - last_time.timestamp()
                if diff >= self.timeout_seconds:
                    print(f"[OFFLINE] {device_id} (no data for {self.timeout_seconds} seconds)")

        # 다음 체크 예약
        threading.Timer(self.check_interval, self._check_offline_devices).start()