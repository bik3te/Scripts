#include "stdafx.h"
#include "windows.h"

void _tmain(int argc, _TCHAR* argv[])
{
  LoadLibrary(L"hijackme.dll");
}
