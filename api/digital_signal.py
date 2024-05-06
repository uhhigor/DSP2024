import numpy as np


class DigitalSignal:
    def __init__(self, file_path: str = None, start_time: float = None, sampling_rate: float = None, samples: [] = None, time: [] = None):
        if file_path is not None:
            self.load_from_file(file_path)
        else:
            if start_time is None or sampling_rate is None or samples is None or time is None:
                raise ValueError('Invalid parameters')
            self.start_time = start_time
            self.sampling_rate = sampling_rate
            self.samples = samples
            self.time = time

    def save_to_file(self, file_path: str):
        with open(file_path, 'wb') as file:
            file.write(np.array(['start_time'], dtype=np.float64).tobytes())
            file.write(np.array(['sampling_frequency'], dtype=np.float64).tobytes())
            file.write(np.array(['num_samples'], dtype=np.int32).tobytes())
            file.write(self.samples.tobytes())

    def load_from_file(self, file_path: str):
        with open(file_path, 'rb') as file:
            self.start_time = np.frombuffer(file.read(8), dtype=np.float64)[0]
            self.sampling_rate = np.frombuffer(file.read(8), dtype=np.float64)[0]
            num_samples = np.frombuffer(file.read(4), dtype=np.int32)[0]
            self.samples = np.frombuffer(file.read(), dtype=np.float64)
            self.time = np.linspace(self.start_time, self.start_time + num_samples / self.sampling_rate, num_samples, endpoint=False)

