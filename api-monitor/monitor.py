import psutil

class ProcessMonitor:
    def __init__(self):
        self.process = None
    
    def get_process(self, pid):
        """Get process by PID and handle common exceptions"""
        try:
            self.process = psutil.Process(pid)
            return True
        except psutil.NoSuchProcess:
            print("Process not found")
        except psutil.AccessDenied:
            print("Access Denied to Process")
        return False
