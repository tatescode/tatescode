import psutil # type: ignore
import click # type: ignore

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

@click.command()
@click.option('--list', is_flag=True, help='List all processes')
@click.option('--kill', type=int, help='Kill a process by PID')

def main(list, kill):
    "SIMPLE PROCESS MONITOR"
    if list:
        list_processes()
    if kill:
        kill_process(kill)

if __name__ == '__main__':
    main()