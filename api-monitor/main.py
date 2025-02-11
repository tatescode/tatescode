import psutil # type: ignore
import click # type: ignore
from datetime import datetime, timezone
import socket
from collections import defaultdict

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

class ProcessManager(ProcessMonitor):
    def list_processes(self):
        """List all running processes"""
        print("\nRunning Processes:")
        print("------------------")
    
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                print(f"PID: {proc.info['pid']:<6} Name: {proc.info['name']}")
            except psutil.NoSuchProcess:
                print("Process not found")
            except psutil.AccessDenied:
                print("Access Denied to Process")
            pass

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
        except psutil.NoSuchProcess:
            print("Process not found")
        except psutil.AccessDenied:
            print("Access Denied to Process")
        pass

class ProcessInfo(ProcessMonitor):
    def get_details(self, pid):
        """Get detailed information about a specific process"""
        try:
            process = psutil.Process(pid)
            created_time = datetime.fromtimestamp(process.create_time(), tz=timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')

            print(f"\nProcess Details for PID: {pid}:")
            print("-" * 30)
            print(f"Name: {process.name()}")
            print(f"Status: {process.status()}")
            print(f"CPU Usage: {process.cpu_percent()}%")
            print(f"Memory Usage: {process.memory_info().rss / 1024 / 1024:.2f} MB")
            print(f"Created: {created_time}")
            print(f"Parent PID: {process.ppid()}")
        except psutil.NoSuchProcess:
            print("Processs not found")
        except psutil.AccessDenied:
            print("Access Denied to Process")

class NetworkMonitor(ProcessMonitor):
    def get_connections(self, pid):
        """Get network connections for a process"""
        try:
            if self.get_process(pid):
                connections = self.process.net_connections()
                print(f"\nNetwork Connections for PID: {self.process.name()} (PID: {pid}):")
                print("-" * 50)

                if not connections:
                    print(f"No active connections for PID: {pid}")
                    return
                
                for conn in connections:
                    if conn.laddr:
                        local = f"{conn.laddr.ip}:{conn.laddr.port}"
                    else:
                        local = "Not available"

                    if conn.raddr:
                        remote = f"{conn.raddr.ip}:{conn.raddr.port}"
                    else:
                        remote = "Not available"
                    
                    print(f"Status: {conn.status}")
                    print(f"Local Address: {local}")
                    print(f"Remote Address: {remote}")
                    print("-" * 30)
        except psutil.NoSuchProcess:
            print("Process not found")
        except psutil.AccessDenied:
            print("Access Denied to Process")

@click.command()
@click.option('--list', is_flag=True, help='List all processes')
@click.option('--kill', type=int, help='Kill a process by PID')
@click.option('--details', type=int, help='Get detailed information about a process')
@click.option('--connections', type=int, help='Get network connections for a process')

def main(list, kill, details, connections):
    "SIMPLE PROCESS MONITOR"
    
    if not any([list, kill, details, connections]):
        print("Error: No options provided. Use --help to see available options.")
        return

    process_manager = ProcessManager()
    process_info = ProcessInfo()
    network_monitor = NetworkMonitor()

    if list:
        process_manager.list_processes()
    if kill:
        process_manager.kill_process(kill)
    if details:
        process_info.get_details(details)
    if connections:
        network_monitor.get_connections(connections)

if __name__ == '__main__':
    main()
