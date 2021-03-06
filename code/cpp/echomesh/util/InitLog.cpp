#include "echomesh/util/InitLog.h"

namespace echomesh {

namespace {

bool initialized = false;

class PythonLogger : public google::base::Logger {
  public:
    PythonLogger(StringCaller caller, void* callback)
            : caller_(caller), callback_(callback) {
    }

    virtual void Write(bool force_flush,
                       time_t timestamp,
                       const char* message,
                       int message_len) {
        string s(message, message_len);
        caller_(callback_, s);
        logSize_ += message_len;
    }

    // Flush any buffered messages
    virtual void Flush() {}

    // Get the current LOG file size.
    // The returned value is approximate since some
    // logged data may not have been flushed to disk yet.
    virtual uint32 LogSize() { return logSize_; }

  private:
    StringCaller const caller_;
    void* const callback_;
    uint32 logSize_;
};


}  // namespace

void initLog() {
    initialized = true;
    google::InitGoogleLogging("echomesh");
    FLAGS_logtostderr = true;
}

void setLogger(int logLevel, StringCaller caller, void* callback) {
    google::base::Logger* logger = (caller and callback) ?
            new PythonLogger(caller, callback) : nullptr;
    google::base::SetLogger(logLevel, logger);
}

}  // namespace echomesh
