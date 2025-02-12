from monitor import ProcessMonitor
import psutil

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
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            print("Access Denied or Process not found")
