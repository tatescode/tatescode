from monitor import ProcessMonitor
import win32api
import win32con
import win32process
import win32security
import win32service
from ctypes import *
from ctypes.wintypes import *

class APIMonitor(ProcessMonitor):
    def __init__(self):
        super().__init__()
        self.hooks = {}

    def hook_process_creation(self, pid):
        """Monitor Process Creation APIs"""
        try:
            if self.get_process(pid):
                print(f"Setting up API hooks for PID:{pid}:")
        except Exception as e:
                print(f"Error setting up hooks: {e}")

    def monitor_process_injection(self, pid):
        """Monitor common process injection techniques"""
        try:
            if self.get_process(pid):
                self.hook_create_process(pid)
        except Exception as e:
            print(f"Error monitoring process injection: {e}")
        
    def hook_create_process(self, pid):
        """Hook the CreateProcessW API call"""
        try:
            if self.get_process(pid):
                CreateProcessW_Proto = WINFUNCTYPE(
                    BOOL,     # Return Type
                    LPCWSTR,  # lpApplicationName
                    LPWSTR,   # lpCommandLine
                    LPSECURITY_ATTRIBUTES,  # lpProcessAttributes
                    LPSECURITY_ATTRIBUTES,  # lpThreadAttributes
                    BOOL,    # bInheritHandles
                    DWORD,   # dwCreationFlags
                    LPVOID,  # lpEnvironment
                    LPCWSTR, # lpCurrentDirectory
                    LPSTARTUPINFOW,  # lpStartupInfo
                    LPPROCESS_INFORMATION  # lpProcessInformation
                )

                kernel32 = windll.kernel32
                create_process_addr = kernal32.GetProcAddress(
                    kernal32._handle,
                    "CreateProcessW"
                )

                print(f"[+] Found CreateProcessW at address: {hex(create_process_addr)}")
                self.hooks["CreateProcessW"] = create_process_addr

        except Exception as e:
            print(f"Error hooking CreateProcessW: {e}")