// The following ifdef block is the standard way of creating macros which make exporting
// from a DLL simpler. All files within this DLL are compiled with the METASPLOP_EXPORTS
// symbol defined on the command line. This symbol should not be defined on any project
// that uses this DLL. This way any other project whose source files include this file see
// METASPLOP_API functions as being imported from a DLL, whereas this DLL sees symbols
// defined with this macro as being exported.
#ifdef METASPLOP_EXPORTS
#define METASPLOP_API __declspec(dllexport)
#else
#define METASPLOP_API __declspec(dllimport)
#endif

#define EXPORT comment(linker, "/EXPORT:" __FUNCTION__ "=" __FUNCDNAME__)

extern HMODULE hPayload;

void
MessageBoxError(LPCSTR lpText);

METASPLOP_API
void
Inject(HWND hwnd, HINSTANCE hinst, LPSTR lpszCmdLine, int nCmdShow);

WINBASEAPI
_Ret_maybenull_
HMODULE
WINAPI
LoadLibraryA(
	_In_ LPCSTR lpLibFileName
);

// PEB-related functionality source: https://gist.github.com/Spl3en/9c0ea329bb7878df9b9b#file-modulesfrompeb-c
/* Windows structures */
typedef struct _PEB_LDR_DATA {
    BYTE       Reserved1[8];
    PVOID      Reserved2[3];
    LIST_ENTRY InMemoryOrderModuleList;
} PEB_LDR_DATA, * PPEB_LDR_DATA;

typedef struct _RTL_USER_PROCESS_PARAMETERS {
    UCHAR           Reserved1[16];
    PVOID           Reserved2[10];
    UNICODE_STRING  ImagePathName;
    UNICODE_STRING  CommandLine;
} RTL_USER_PROCESS_PARAMETERS, * PRTL_USER_PROCESS_PARAMETERS;

typedef struct _LDR_DATA_TABLE_ENTRY {
    LIST_ENTRY InLoadOrderLinks;
    LIST_ENTRY InMemoryOrderModuleList;
    LIST_ENTRY InInitializationOrderModuleList;
    PVOID DllBase;
    PVOID EntryPoint;
    ULONG SizeOfImage;
    UNICODE_STRING FullDllName;
    UNICODE_STRING BaseDllName;
    ULONG Flags;
    USHORT LoadCount;
    USHORT TlsIndex;
    union {
        LIST_ENTRY HashLinks;
        struct
        {
            PVOID SectionPointer;
            ULONG CheckSum;
        };
    };
    union {
        ULONG TimeDateStamp;
        PVOID LoadedImports;
    };
    PVOID EntryPointActivationContext;
    PVOID PatchInformation;
} LDR_DATA_TABLE_ENTRY, * PLDR_DATA_TABLE_ENTRY;

typedef struct _PEB {
    BYTE                          Reserved1[2];
    BYTE                          BeingDebugged;
    BYTE                          Reserved2[1];
    PVOID                         Reserved3[2];
    PPEB_LDR_DATA                 Ldr;
    PRTL_USER_PROCESS_PARAMETERS  ProcessParameters;
    BYTE                          Reserved4[104];
    PVOID                         Reserved5[52];
    PVOID                         PostProcessInitRoutine;
    BYTE                          Reserved6[128];
    PVOID                         Reserved7[1];
    ULONG                         SessionId;
} PEB, * PPEB;

typedef struct _PROCESS_BASIC_INFORMATION {
    PVOID ExitStatus;
    PPEB PebBaseAddress;
    PVOID Reserved2[2];
    ULONG_PTR UniqueProcessId;
    PVOID Reserved3;
} PROCESS_BASIC_INFORMATION, * PPROCESS_BASIC_INFORMATION;

typedef enum _PROCESSINFOCLASS {
    ProcessBasicInformation
    // We don't need the others
} PROCESSINFOCLASS;

// MODULE_ENTRY contains basic information about a module
typedef struct _MODULE_ENTRY {
    UNICODE_STRING BaseName; // BaseName of the module
    UNICODE_STRING FullName; // FullName of the module
    ULONG SizeOfImage; // Size in bytes of the module
    PVOID BaseAddress; // Base address of the module
    PVOID EntryPoint; // Entrypoint of the module
} MODULE_ENTRY, * PMODULE_ENTRY;

// MODULE_INFORMATION_TABLE contains basic information about all the modules of a given process
typedef struct _MODULE_INFORMATION_TABLE {
    ULONG Pid; // PID of the process
    ULONG ModuleCount; // Modules count for the above pointer
    PMODULE_ENTRY Modules; // Pointer to 0...* modules
} MODULE_INFORMATION_TABLE, * PMODULE_INFORMATION_TABLE;

typedef NTSTATUS(NTAPI* pfnNtQueryInformationProcess)(
    IN  HANDLE ProcessHandle,
    IN  PROCESSINFOCLASS ProcessInformationClass,
    OUT PVOID ProcessInformation,
    IN  ULONG ProcessInformationLength,
    OUT PULONG ReturnLength    OPTIONAL
    );

void
Metasplop();