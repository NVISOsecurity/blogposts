// Shellcode.cpp : This file contains the 'main' function. Program execution begins and ends there.
//

#include "Shellcode.h"

int main()
{
    char path[MAX_PATH];
    HANDLE hFile;
    LARGE_INTEGER lFileSize;
    DWORD dReadSize;
    LPVOID lpShellcode;
    wchar_t buffer[200];

    printf("Path to the shellcode for process %d: ", GetCurrentProcessId());

    // Get the shellcode path
    fgets(path, MAX_PATH, stdin);
    if ((strlen(path) > 0) && (path[strlen(path) - 1] == '\n'))
        path[strlen(path) - 1] = '\0';

    // Open the file
    hFile = CreateFileA(path, GENERIC_READ, FILE_SHARE_READ, NULL, OPEN_EXISTING, FILE_ATTRIBUTE_NORMAL, NULL);
    if (hFile == INVALID_HANDLE_VALUE)
    {
        printf("Unable to open file \"%s\" for read (error %d).\n", path, GetLastError());
        return 2;
    }

    // Get the file's size
    if (!GetFileSizeEx(hFile, &lFileSize))
    {
        printf("Couldn't get file size (error %d).\n", GetLastError());
        return 3;
    }

    // Allocate the needed memory
    lpShellcode = VirtualAlloc(NULL, lFileSize.LowPart, MEM_COMMIT | MEM_RESERVE, PAGE_EXECUTE_READWRITE);
    if (!lpShellcode)
    {
        printf("Couldn't allocate %d bytes of memory (error %d).\n", lFileSize.LowPart, GetLastError());
        return 4;
    }

    // Copy the shellcode
    if (!ReadFile(hFile, lpShellcode, lFileSize.LowPart, &dReadSize, NULL) && dReadSize != lFileSize.LowPart)
    {
        printf("Couldn't copy shellcode, got %d bytes out of %d (error %d).\n", dReadSize, lFileSize.LowPart, GetLastError());
        VirtualFree(lpShellcode, NULL, MEM_FREE);
        return 5;
    }

    // Issue a warning
    swprintf(buffer, 200, L"You are about to execute %d bytes of shellcode located at %p in process %d.", lFileSize.LowPart, lpShellcode, GetCurrentProcessId());
    if (IDCANCEL == MessageBox(NULL, buffer, L"Shellcode", MB_ICONWARNING | MB_OKCANCEL | MB_DEFBUTTON2))
    {
        printf("Shellcode execution aborted.\n");
        VirtualFree(lpShellcode, NULL, MEM_FREE);
        return 6;
    }

    // While shellcode will trigger
    ((void(*)())lpShellcode)();
}