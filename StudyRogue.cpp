#include <Wt/WApplication.h>
#include <Wt/WContainerWidget.h>
#include <Wt/WPaintDevice.h>
#include <Wt/WPainter.h>
#include <Wt/WText.h>

using namespace Wt;

class SmileyFaceWidget : public WContainerWidget {
public:
    SmileyFaceWidget() {
        resize(200, 200);
    }

protected:
    void paintEvent(Wt::WPaintDevice *paintDevice) override {
        WPainter painter(paintDevice);
        painter.setRenderHint(RenderHint::Antialiasing);

        // Draw face
        painter.setPen(Wt::Pen(WColor(0, 0, 0), 2));
        painter.setBrush(Wt::Brush(WColor(255, 255, 0)));
        painter.drawEllipse(25, 25, 150, 150);

        // Draw eyes
        painter.setBrush(Wt::Brush(WColor(0, 0, 0)));
        painter.drawEllipse(60, 60, 20, 20);
        painter.drawEllipse(120, 60, 20, 20);

        // Draw mouth
        painter.setPen(Wt::Pen(WColor(0, 0, 0), 3));
        painter.drawLine(60, 120, 140, 120);
        painter.drawArc(70, 90, 60, 60, 0, -180 * 16);
    }
};

class SmileyApplication : public WApplication {
public:
    SmileyApplication(const WEnvironment& env) : WApplication(env) {
        setTitle("Smiley Face");
        useStyleSheet("styles.css"); // Optional: Add CSS styling
        root()->addWidget(std::make_unique<SmileyFaceWidget>());
    }
};

int main(int argc, char** argv) {
    return WRun(argc, argv, [](const WEnvironment& env) {
        return std::make_unique<SmileyApplication>(env);
    });
}
