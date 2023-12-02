package controller;
import javafx.event.ActionEvent;
import javafx.scene.control.Alert;
import searcher.Main;

public class RootLayoutController {
    //Exit the program
    public void handleExit(ActionEvent actionEvent) {
        System.exit(0);
    }
    //Help Menu button behavior
    public void handleHelp(ActionEvent actionEvent) {
        Alert alert = new Alert (Alert.AlertType.INFORMATION);
        alert.setTitle("Program Information");
        alert.setHeaderText("This is a sample JAVAFX application for StorageToo!");
        alert.setContentText("You can search, delete, update, insert a new lessee with this program.");
        alert.show();
    }
}