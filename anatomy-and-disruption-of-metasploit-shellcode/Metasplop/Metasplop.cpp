// Metasplop.cpp : Defines the exported functions for the DLL.
// PEB-related functionality source: https://gist.github.com/Spl3en/9c0ea329bb7878df9b9b#file-modulesfrompeb-c

#include "pch.h"

void
MessageBoxError(LPCSTR lpText)
{
    MessageBoxA(
        NULL,
        lpText,
        "NVISO Mock AV",
        MB_ICONERROR | MB_OK
    );
}

_Ret_maybenull_
HMODULE
WINAPI
LoadLibraryA(_In_ LPCSTR lpLibFileName)
{
    #pragma EXPORT
    // Raise the error message
    char buffer[200];
    if (sprintf_s(buffer, 200, "The process %d has attempted to load \"%s\" through LoadLibraryA using Metasploit's dynamic import resolution.\n", GetCurrentProcessId(), lpLibFileName) > 0)
    {
        MessageBoxError(buffer);
    }
    // Exit the process
    ExitProcess(-1);
}

PPROCESS_BASIC_INFORMATION
QueryProcessInformation(
    IN HANDLE Process,
    IN PROCESSINFOCLASS ProcessInformationClass,
    IN DWORD ProcessInformationLength
) {
    PPROCESS_BASIC_INFORMATION pProcessInformation = NULL;
    pfnNtQueryInformationProcess gNtQueryInformationProcess;
    ULONG ReturnLength = 0;
    NTSTATUS Status;
    HMODULE hNtDll;

    if (!(hNtDll = LoadLibrary(L"ntdll.dll"))) {
        MessageBoxError("Cannot load ntdll.dll.");
        return NULL;
    }

    if (!(gNtQueryInformationProcess = (pfnNtQueryInformationProcess)GetProcAddress(hNtDll, "NtQueryInformationProcess"))) {
        MessageBoxError("Cannot load NtQueryInformationProcess.");
        return NULL;
    }

    // Allocate the memory for the requested structure
    if ((pProcessInformation = (PPROCESS_BASIC_INFORMATION)malloc(ProcessInformationLength)) == NULL) {
        MessageBoxError("ExAllocatePoolWithTag failed.");
        return NULL;
    }

    // Fill the requested structure
    if (!NT_SUCCESS(Status = gNtQueryInformationProcess(Process, ProcessInformationClass, pProcessInformation, ProcessInformationLength, &ReturnLength))) {
        char message[200];
        if (sprintf_s(message, 200, "NtQueryInformationProcess should return NT_SUCCESS (Status = %#x).", Status) > 0)
        {
            MessageBoxError(message);
        }
        free(pProcessInformation);
        return NULL;
    }

    // Check the requested structure size with the one returned by NtQueryInformationProcess
    if (ReturnLength != ProcessInformationLength) {
        MessageBoxError("Warning : NtQueryInformationProcess ReturnLength is different than ProcessInformationLength");
        return NULL;
    }

    return pProcessInformation;
}

PPEB
GetCurrentPebProcess() {
    PPROCESS_BASIC_INFORMATION pProcessInformation = NULL;
    DWORD ProcessInformationLength = sizeof(PROCESS_BASIC_INFORMATION);
    HANDLE Process = GetCurrentProcess();
    PPEB pPeb = NULL;

    // ProcessBasicInformation returns information about the PebBaseAddress
    if ((pProcessInformation = QueryProcessInformation(Process, ProcessBasicInformation, ProcessInformationLength)) == NULL) {
        char message[200];
        if (sprintf_s(message, 200, "Handle=%p : QueryProcessInformation failed.", Process) > 0)
        {
            MessageBoxError(message);
        }
        return NULL;
    }

    // Check the correctness of the value returned
    if (pProcessInformation->PebBaseAddress == NULL) {
        char message[200];
        if (sprintf_s(message, 200, "Handle=%p : PEB address cannot be found", Process) > 0)
        {
            MessageBoxError(message);
        }
        free(pProcessInformation);
        return NULL;
    }

    pPeb = pProcessInformation->PebBaseAddress;

    // Cleaning
    free(pProcessInformation);

    return pPeb;
}

void
Metasplop() {
    PPEB pPeb = NULL;
    PPEB_LDR_DATA pLdrData = NULL;
    PLIST_ENTRY pHeadEntry = NULL;
    PLIST_ENTRY pEntry = NULL;
    PLDR_DATA_TABLE_ENTRY pLdrEntry = NULL;
    USHORT MaximumLength = NULL;

    // Read the PEB from the current process
    if ((pPeb = GetCurrentPebProcess()) == NULL) {
        MessageBoxError("GetPebCurrentProcess failed.");
        return;
    }

    // Get the InMemoryOrderModuleList
    pLdrData = pPeb->Ldr;
    pHeadEntry = &pLdrData->InMemoryOrderModuleList;

    // Loop the modules
    for (pEntry = pHeadEntry->Flink; pEntry != pHeadEntry; pEntry = pEntry->Flink) {
        pLdrEntry = CONTAINING_RECORD(pEntry, LDR_DATA_TABLE_ENTRY, InMemoryOrderModuleList);
        // Skip modules which aren't kernel32.dll
        if (lstrcmpiW(pLdrEntry->BaseDllName.Buffer, L"KERNEL32.DLL")) continue;
        // Compute the new maximum length
        MaximumLength = pLdrEntry->BaseDllName.MaximumLength + 1;
        // Create a new increased buffer
        wchar_t* NewBuffer = new wchar_t[MaximumLength];
        wcscpy_s(NewBuffer, MaximumLength, pLdrEntry->BaseDllName.Buffer);
        // Update the BaseDllName
        pLdrEntry->BaseDllName.Buffer = NewBuffer;
        pLdrEntry->BaseDllName.MaximumLength = MaximumLength;
        break;
    }
    return;
}