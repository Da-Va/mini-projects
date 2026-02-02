// Attempt to identify a window by name or attribute.
// originally written by Adam Pierce <adam@doctort.org>
// revised by Dario Pellegrini <pellegrini.dario@gmail.com>

#include <X11/Xlib.h>
#include <X11/Xatom.h>
#include <iostream>
#include <vector>
#include <thread>
#include <chrono>


std::vector<Window> pid2windows(pid_t pid, Display* display, Window w) {
  struct implementation {
    struct FreeWrapRAII {
      void * data;
      FreeWrapRAII(void * data): data(data) {}
      ~FreeWrapRAII(){ XFree(data); }
    };

    std::vector<Window> result;
    pid_t pid;
    Display* display;
    Atom atomPID;

    implementation(pid_t pid, Display* display): pid(pid), display(display) {
      // Get the PID property atom
      atomPID = XInternAtom(display, "_NET_WM_PID", True);
      if(atomPID == None) {
        throw std::runtime_error("pid2windows: no such atom");
      }
    }

    std::vector<Window> getChildren(Window w) {
      Window    wRoot;
      Window    wParent;
      Window   *wChild;
      unsigned  nChildren;
      std::vector<Window> children;
      if(0 != XQueryTree(display, w, &wRoot, &wParent, &wChild, &nChildren)) {
        FreeWrapRAII tmp( wChild );
        children.insert(children.end(), wChild, wChild+nChildren);
      }
      return children;
    }

    void emplaceIfMatches(Window w) {
      // Get the PID for the given Window
      Atom           type;
      int            format;
      unsigned long  nItems;
      unsigned long  bytesAfter;
      unsigned char *propPID = 0;
      if(Success == XGetWindowProperty(display, w, atomPID, 0, 1, False, XA_CARDINAL,
                                       &type, &format, &nItems, &bytesAfter, &propPID)) {
        if(propPID != 0) {
          FreeWrapRAII tmp( propPID );
          if(pid == *reinterpret_cast<pid_t*>(propPID)) {
            result.emplace_back(w);
          }
        }
      }
    }

    void recurse( Window w) {
      emplaceIfMatches(w);
      for (auto & child: getChildren(w)) {
        recurse(child);
      }
    }

    std::vector<Window> operator()( Window w ) {
      result.clear();
      recurse(w);
      return result;
    }
  };
  //back to pid2windows function
  return implementation{pid, display}(w);
}

std::vector<Window> pid2windows(const size_t pid, Display* display) {
  return pid2windows(pid, display, XDefaultRootWindow(display));
}


int main(int argc, char **argv) {
  if(argc < 2)
    return 1;

  int pid = atoi(argv[1]);
  std::cout << "Searching for windows associated with PID " << pid << std::endl;

  // Start with the root window.
  Display *display = XOpenDisplay(0);
  auto res = pid2windows(pid, display);

  // Print the result.
  for( auto & w: res) {
    std::cout << "Window #"
              << std::hex << static_cast<unsigned long>(w) << std::dec
              << '\n';
  }
  
  XWindowAttributes attr;
  
  XGetWindowAttributes(display, res[1], &attr);
  
  std::cout << attr.y << " " << attr.x << " " << attr.height << " " << attr.width << '\n';
  
  // Window parent = XCreateSimpleWindow(display, XDefaultRootWindow(display), attr.x, attr.y +50, attr.width, attr.height-50, 0, 244, 244);
  Window parent = XCreateSimpleWindow(display, res[0], attr.x + 50, attr.y + 50, attr.width, attr.height, 0, 244, 244);

  
  // XUnmapWindow(display, res[1]);
  XMapWindow(display, parent);
  
  XReparentWindow(display, res[1], parent, 0, 0);
  XSync(display, 0);
  
  // std::this_thread::sleep_for(std::chrono::milliseconds(100000));

  XCloseDisplay(display);
  return 0;
}
