#include <iostream>
#include <csignal>
#include <ctime>
#include <unistd.h>
#include <chrono>

#define PERIOD_NS 1e7
#define PERIOD_S (PERIOD_NS/1e9)

void timer_handler(int signum) {
    static int count = -1;
    static std::chrono::system_clock::time_point last_invocation; 
    static double jitter = 0.;

    auto invocation = std::chrono::system_clock::now();

    if(count++ == -1) {
        last_invocation = invocation;
        return;
    }

    auto period = invocation - last_invocation;

    double error = std::abs(1e-9 * (period.count() - PERIOD_NS));

    jitter = double(count)/(count+1) * jitter + 1./(count+1) * error;

    last_invocation = invocation;

    printf("Timer expired %6d times, error: %f, error%%: %f, jitter: %f, jitter%% %f\n", ++count, error, error/PERIOD_S, jitter, jitter/PERIOD_S);
}

int main() {
    // Define the signal action
    struct sigaction sa;
    sa.sa_flags = SA_SIGINFO;
    sa.sa_handler = timer_handler;
    sigemptyset(&sa.sa_mask);
    if (sigaction(SIGALRM, &sa, nullptr) == -1) {
        std::cerr << "Failed to set signal handler." << std::endl;
        return 1;
    }

    // Create the timer
    timer_t timerid;
    struct sigevent sev;
    sev.sigev_notify = SIGEV_SIGNAL;
    sev.sigev_signo = SIGALRM;
    sev.sigev_value.sival_ptr = &timerid;
    if (timer_create(CLOCK_REALTIME, &sev, &timerid) == -1) {
        std::cerr << "Failed to create timer." << std::endl;
        return 1;
    }

    // Set the timer to expire every 1 second

    struct itimerspec its;
    its.it_value.tv_sec = 0;  // Initial expiration
    its.it_value.tv_nsec = int(PERIOD_NS);
    its.it_interval.tv_sec = 0;  // Periodic interval
    its.it_interval.tv_nsec = int(PERIOD_NS);

    if (timer_settime(timerid, 0, &its, nullptr) == -1) {
        std::cerr << "Failed to start timer." << std::endl;
        return 1;
    }

    // Keep the program running to allow the timer to trigger
    while (true) {
        sleep(1);
    }

    return 0;
}