import click
from process import ProcessManager, ProcessInfo
from network import NetworkMonitor

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
