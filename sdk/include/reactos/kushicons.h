/* Kush icon presentation opt-in. UI resources only, original IDs stay stable.
 * Fluent artwork lives at ID + 40000; ClassicIcons keeps the original IDs. */
#pragma once
#ifndef RC_INVOKED
#include <windef.h>
#include <winbase.h>
#include <winreg.h>
#include <winuser.h>
#define KUSH_CLASSIC_ICON_OFFSET 40000
static __inline BOOL KushClassicIcons(void)
{
    HKEY key; DWORD value = 0, type = 0, size = sizeof(value);
    if (RegOpenKeyExW(HKEY_CURRENT_USER, L"Software\\Kush\\Shell", 0, KEY_QUERY_VALUE, &key)) return FALSE;
    LONG status = RegQueryValueExW(key, L"ClassicIcons", NULL, &type, (BYTE*)&value, &size);
    RegCloseKey(key);
    return status == ERROR_SUCCESS && type == REG_DWORD && size == sizeof(value) && value != 0;
}
static __inline UINT KushIconResourceId(HINSTANCE module, UINT id)
{
    UINT backup = id + KUSH_CLASSIC_ICON_OFFSET;
    if (module && id && id <= 25535 && backup <= 65535 && !KushClassicIcons() &&
        FindResourceW(module, MAKEINTRESOURCEW(backup), MAKEINTRESOURCEW(14))) return backup;
    return id;
}
static __inline UINT KushBitmapResourceId(HINSTANCE module, UINT id)
{
    UINT backup = id + KUSH_CLASSIC_ICON_OFFSET;
    if (module && id && id <= 25535 && KushClassicIcons() &&
        FindResourceW(module, MAKEINTRESOURCEW(backup), MAKEINTRESOURCEW(2))) return backup;
    return id;
}
static __inline UINT KushOwnIconId(UINT id)
{
    MEMORY_BASIC_INFORMATION info;
    if (!id || KushClassicIcons()) return id;
    if (VirtualQuery((LPCVOID)&KushOwnIconId, &info, sizeof(info)))
        return KushIconResourceId((HINSTANCE)info.AllocationBase, id);
    return id;
}
static __inline HICON KushLoadIconW(HINSTANCE module, LPCWSTR name)
{
    if (IS_INTRESOURCE(name)) name = MAKEINTRESOURCEW(KushIconResourceId(module, (UINT)(ULONG_PTR)name));
    return LoadIconW(module, name);
}
static __inline HICON KushLoadIconA(HINSTANCE module, LPCSTR name)
{
    if (IS_INTRESOURCE(name)) name = MAKEINTRESOURCEA(KushIconResourceId(module, (UINT)(ULONG_PTR)name));
    return LoadIconA(module, name);
}
static __inline HANDLE KushLoadImageW(HINSTANCE module, LPCWSTR name, UINT kind, int cx, int cy, UINT flags)
{
    if (kind == IMAGE_ICON && !(flags & LR_LOADFROMFILE) && IS_INTRESOURCE(name))
        name = MAKEINTRESOURCEW(KushIconResourceId(module, (UINT)(ULONG_PTR)name));
    return LoadImageW(module, name, kind, cx, cy, flags);
}
static __inline HANDLE KushLoadImageA(HINSTANCE module, LPCSTR name, UINT kind, int cx, int cy, UINT flags)
{
    if (kind == IMAGE_ICON && !(flags & LR_LOADFROMFILE) && IS_INTRESOURCE(name))
        name = MAKEINTRESOURCEA(KushIconResourceId(module, (UINT)(ULONG_PTR)name));
    return LoadImageA(module, name, kind, cx, cy, flags);
}
#ifndef KUSH_ICONS_NO_LOAD_MACROS
#define LoadIconW KushLoadIconW
#define LoadIconA KushLoadIconA
#define LoadImageW KushLoadImageW
#define LoadImageA KushLoadImageA
#endif
#endif
