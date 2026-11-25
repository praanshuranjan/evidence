#include <stdio.h>
#include <unistd.h>
#include <time.h>
int main() {
    FILE *f = fopen("/Users/praanshu/heimdall_poc_c.log", "a");
    time_t t = time(NULL);
    fprintf(f, "[%s] START pid=%d (C binary)\n", ctime(&t), getpid());
    fflush(f); fclose(f);
    int tick = 0;
    while (1) {
        sleep(30);
        tick++;
        f = fopen("/Users/praanshu/heimdall_poc_c.log", "a");
        t = time(NULL);
        fprintf(f, "[%s] alive pid=%d tick=%d\n", ctime(&t), getpid(), tick);
        fflush(f); fclose(f);
    }
    return 0;
}
