from datetime import datetime, timezone
import psutil
import click
from monitor import ProcessMonitor

class ProcessManager(ProcessMonitor):
    def list_processes(self):
        """List all running processes"""
        print("\nRunning Processes:")
        print("------------------")
    
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                print(f"PID: {proc.info['pid']:<6} Name: {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

    def kill_process(self, pid):
        """Kill a process by PID"""
        try:
            if self.get_process(pid):
                process_name = self.process.name()
                if click.confirm(f"Are you sure you want to kill {process_name}"):
                    self.process.terminate()
                    print(f"Process {process_name} with PID {pid} killed")
                else:
                    print("Process not killed")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print("Access Denied or Process not found")

class ProcessInfo(ProcessMonitor):
    def get_details(self, pid):
        """Get detailed information about a specific process"""
        try:
            process = psutil.Process(pid)
            created_time = datetime.fromtimestamp(process.create_time(), 
                                                tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

            print(f"\nProcess Details for PID: {pid}:")
            print("-" * 30)
            print(f"Name: {process.name()}")
            print(f"Status: {process.status()}")
            print(f"CPU Usage: {process.cpu_percent()}%")
            print(f"Memory Usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
            print(f"Created: {created_time}")
            print(f"Parent PID: {process.ppid()}")
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print("Access Denied or Process not found")
