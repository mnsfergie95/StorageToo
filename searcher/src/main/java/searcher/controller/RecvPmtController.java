package searcher.controller;

import java.sql.SQLException;
import java.text.NumberFormat;
import java.time.LocalDate;
import java.util.Locale;

import javafx.fxml.FXML;
import javafx.scene.control.TextField;
import searcher.util.DBUtil;

public class RecvPmtController {
    
    @FXML
    private TextField txtUnit;
    @FXML
    private TextField txtAmount;

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
        LocalDate now = LocalDate.now();
        try {
            String SqlStmt = "CALL procCommitPmt('" + unitTitle + "', '" + amtOwed + "','" + now + "','" + newDueDate + "')";
            DBUtil.dbExecuteUpdate(SqlStmt);
        } catch (SQLException e) {
            System.out.println("Error occurred while inserting payment amount to DB.\n" + e);
            throw e;
        } 

        
    }

}
