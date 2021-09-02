// Metasplop.cpp : Defines the exported functions for the DLL.
//

#include "pch.h"

METASPLOP_API
void
Inject(HWND hwnd, HINSTANCE hinst, LPSTR lpszCmdLine, int nCmdShow)
{
    #pragma EXPORT
    int PID;
    HMODULE hKernel32;
    FARPROC fLoadLibraryA;
    HANDLE hProcess;
    LPVOID lpInject;

    // Recover the current module path
    char payload[MAX_PATH];
    int size;
    if ((size = GetModuleFileNameA(hPayload, payload, MAX_PATH)) == NULL)
    {
        MessageBoxError("Unable to get module file name.");
        return;
    }
    
    // Recover LoadLibraryA 
    hKernel32 = GetModuleHandle(L"Kernel32");
    if (hKernel32 == NULL)
    {
        MessageBoxError("Unable to get a handle to Kernel32.");
        return;
    }
    fLoadLibraryA = GetProcAddress(hKernel32, "LoadLibraryA");
    if (fLoadLibraryA == NULL)
    {
        MessageBoxError("Unable to get LoadLibraryA address.");
        return;
    }

    // Open the processes
    PID = std::stoi(lpszCmdLine);
    hProcess = OpenProcess(PROCESS_ALL_ACCESS, FALSE, PID);
    if (!hProcess)
    {
        char message[200];
        if (sprintf_s(message, 200, "Unable to open process %d.", PID) > 0)
        {
            MessageBoxError(message);
        }
        return;
    }

    lpInject = VirtualAllocEx(hProcess, NULL, size + 1, MEM_COMMIT, PAGE_READWRITE);
    if (lpInject)
    {
        wchar_t buffer[100];
        wsprintfW(buffer, L"You are about to execute the injected library in process %d.", PID);
        if (WriteProcessMemory(hProcess, lpInject, payload, size + 1, NULL) && IDCANCEL != MessageBox(NULL, buffer, L"NVISO Mock AV", MB_ICONINFORMATION | MB_OKCANCEL))
        {
            CreateRemoteThread(hProcess, NULL, NULL, (LPTHREAD_START_ROUTINE)fLoadLibraryA, lpInject, NULL, NULL);
        }
        else
        {
            VirtualFreeEx(hProcess, lpInject, NULL, MEM_RELEASE);
        }
    }
    else
    {
        char message[200];
        if (sprintf_s(message, 200, "Unable to allocate %d bytes.", size+1) > 0)
        {
            MessageBoxError(message);
        }
    }
    CloseHandle(hProcess);
    return;
}