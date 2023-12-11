package searcher.controller;

import java.sql.SQLException;
import java.text.NumberFormat;
import java.time.LocalDate;
import java.util.Locale;

import javafx.fxml.FXML;
import javafx.stage.Stage;
import javafx.scene.control.Dialog;
import javafx.scene.control.ButtonBar.ButtonData;
import javafx.scene.control.ButtonType;
import javafx.scene.control.TextField;
import javafx.scene.control.Button;

import searcher.util.DBUtil;

public class RecvPmtController {
    
    @FXML
    private TextField txtUnit;
    @FXML
    private TextField txtAmount;
    @FXML
    private Button btnCommit;

    //declare class variables
    private String unitTitle;
    private Double amtOwed;
    private LocalDate newDueDate;
    
    @FXML
    private void initialize () throws SQLException, ClassNotFoundException {
        unitTitle = PaymentController.unitString;
        amtOwed = PaymentController.amtTotalOwed;
        newDueDate = PaymentController.newNextDueDate;
        NumberFormat currencyFormatter = NumberFormat.getCurrencyInstance(Locale.getDefault());
        txtUnit.setText(unitTitle);
        txtAmount.setText(currencyFormatter.format(amtOwed));
    }

    @FXML
    private void pmtCommit() throws SQLException, ClassNotFoundException {
        try {
            DBUtil.dbCommitPmt(unitTitle, amtOwed, newDueDate);
        } catch (SQLException e) {
            System.out.println("Error occurred while inserting payment amount to DB.\n" + e);
            throw e;
        }
        //popup a dialog showing successful payment addition to DB 
        Dialog<String> dialog = new Dialog<String>();
        dialog.setTitle("Success!");
        ButtonType type = new ButtonType("Ok", ButtonData.OK_DONE);
        dialog.setContentText("Payment successfully added to DB");
        dialog.getDialogPane().getButtonTypes().add(type);
        dialog.showAndWait();
        //close receive pmt window
        Stage stage = (Stage) btnCommit.getScene().getWindow();
        stage.close();
    }

}
