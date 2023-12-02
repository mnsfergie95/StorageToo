package searcher.util;

import javafx.print.PageLayout;
import javafx.print.PrinterJob;
import javafx.scene.image.Image;
import javafx.scene.shape.Rectangle;
import javafx.print.Printer;
import javafx.scene.Node;
import javafx.scene.transform.Scale;


public class printMe {

    public static void print(Node node) {
        PrinterJob job = PrinterJob.createPrinterJob();
        if (job != null && job.showPrintDialog(node.getScene().getWindow())) {
            PageLayout pageLayout = job.getJobSettings().getPageLayout();
            double scaleX = 1.0;
            if (pageLayout.getPrintableWidth() < node.getBoundsInParent().getWidth()) {
                scaleX = pageLayout.getPrintableWidth() / node.getBoundsInParent().getWidth();
            }
            double scaleY = 1.0;
            if (pageLayout.getPrintableHeight() < node.getBoundsInParent().getHeight()) {
                scaleY = pageLayout.getPrintableHeight() / node.getBoundsInParent().getHeight();
            }
            double scaleXY = Double.min(scaleX, scaleY);
            Scale scale = new Scale(scaleXY, scaleXY);
            node.getTransforms().add(scale);
            boolean success = job.printPage(node);
            node.getTransforms().remove(scale);
            if (success) {
                job.endJob();
            }
        }
    }
}

