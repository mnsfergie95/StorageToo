package searcher.controller;

import java.sql.SQLException;
import java.text.NumberFormat;
import java.util.Locale;

import javafx.fxml.FXML;
import javafx.scene.control.TextField;

public class RecvPmtController {
    
    @FXML
    private TextField txtUnit;
    @FXML
    private TextField txtAmount;

    private LocalDate newDueDate; 
    
    @FXML
    private void initialize () throws SQLException, ClassNotFoundException {
        String unitTitle = PaymentController.unitString;
        Double amtOwed = PaymentController.amtTotalOwed;
        newDueDate = PaymentController.newNextDueDate;
        NumberFormat currencyFormatter = NumberFormat.getCurrencyInstance(Locale.getDefault());
        txtUnit.setText(unitTitle);
        txtAmount.setText(currencyFormatter.format(amtOwed));
    }

    @FXML
    private void pmtCommit() {
        
    }

}
