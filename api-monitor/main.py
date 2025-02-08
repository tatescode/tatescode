import psutil # type: ignore
import click # type: ignore
from datetime import datetime, timezone

def list_processes():
    "List all running processes"
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

def kill_process(pid):
    "Kill a process by PID"
    try:
        process = psutil.Process(pid)
        process_name = process.name()
        if click.confirm(f"Are you sure you want to kill {process_name}"):
            process.terminate()
            print(f"Process {process_name} with PID {pid} killed")
        else:
            print("Process not killed")
    except psutil.NoSuchProcess:
        print("Process not found")
    except psutil.AccessDenied:
        print("Access Denied to Process")
        pass

def get_process_details(pid):
    "Get detailed information about a specific process"
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

@click.command()
@click.option('--list', is_flag=True, help='List all processes')
@click.option('--kill', type=int, help='Kill a process by PID')
@click.option('--details', type=int, help='Get detailed information about a process')

def main(list, kill, details):
    "SIMPLE PROCESS MONITOR"
    if list:
        list_processes()
    if kill:
        kill_process(kill)
    if details:
        get_process_details(details)

if __name__ == '__main__':
    main()