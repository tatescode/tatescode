import psutil # type: ignore
import click # type: ignore

@click.command()
@click.option('--list', is_flag=True, help='List all processes')
def main(list):
    "SIMPLE PROCESS MONITOR"
    if list:
        print("\nRunning Processes:")
        print("------------------")
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                print(f"PID: {proc.info['pid']:<6} Name: {proc.info['name']}")
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass

if __name__ == '__main__':
    main()