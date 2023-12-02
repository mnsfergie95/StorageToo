package searcher.model;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import searcher.util.DBUtil;
import java.sql.ResultSet;
import java.sql.SQLException;

public class PaymentDAO {
    //*************************************
    //List units available
    //*************************************
    public static ResultSet getAllLeasedUnits () throws SQLException, ClassNotFoundException {
        //Declare a stored procedure call statement
        String selectStmt = "CALL procListAllLeasedUnits";
        //Execute SELECT statement
        try {
            //Get ResultSet from dbExecuteQuery method
            ResultSet rsAvailUnits = DBUtil.dbExecuteQuery(selectStmt);
            return rsAvailUnits;
        }  catch (SQLException e) {
            System.out.println("SQL getAllLeaseUnits operation has failed: " + e);
            //Return exception
            throw e;
        }
    }

    //*******************************
    //SELECT Payments
    //*******************************
    public static ObservableList<Payment> searchPayments (String Inputer) throws SQLException, ClassNotFoundException {
        //Declare a SELECT statement
        String sqlStmt = "CALL procGetAllPaymentsOnUnit('" + Inputer + "')";
        //Execute SELECT statement
        try {
            //Get ResultSet from dbExecuteQuery method
            ResultSet rsPayments = DBUtil.dbExecuteQuery(sqlStmt);
            //Send ResultSet to the getPaymentList method and get Payment object
            ObservableList<Payment> paymentList = getPaymentList(rsPayments);
            //Return payment object
            return paymentList;
        } catch (SQLException e) {
            System.out.println("SQL searchPayments operation has failed: " + e);
            //Return exception
            throw e;
        }
    }

    //*******************************
    //Select * from payment operation
    //*******************************

    private static ObservableList<Payment> getPaymentList(ResultSet rs) throws SQLException, ClassNotFoundException {
        //Declare a observable List which comprises of Payment objects
        ObservableList<Payment> paymentList = FXCollections.observableArrayList();
        while (rs.next()) {
            Payment payment = new Payment();
            
            payment.setPaymentId(rs.getInt("pmt_id"));
            payment.setUnitId(rs.getInt("unit_id"));
            payment.setUnitLabel(rs.getString("label"));
            payment.setAmount(rs.getDouble("amount"));
            payment.setPmtDate(rs.getDate("pmt_date"));
            payment.setPmtDueDate(rs.getDate("NextDueDate"));
            
            //Add payment to the ObservableList
            paymentList.add(payment);
        }
        return paymentList;
    }

    //*******************************
    //Select latest payment
    //*******************************
    public static Payment getLastPayment(String whichUnit) throws SQLException, ClassNotFoundException {
        String selectStmt = "CALL procGenerateLastPayment('" + whichUnit + "')";
        try {
             //Get ResultSet from dbExecuteQuery method
            ResultSet rsLatestPmt = DBUtil.dbExecuteQuery(selectStmt);
            if (rsLatestPmt.next()) {
                Payment payment = new Payment();
                payment.setPaymentId(rsLatestPmt.getInt("pmt_id"));
                payment.setUnitId(rsLatestPmt.getInt("unit_id"));
                payment.setUnitLabel(rsLatestPmt.getString("label"));
                payment.setAmount(rsLatestPmt.getDouble("amount"));
                payment.setPmtDate(rsLatestPmt.getDate("pmt_date"));
                payment.setPmtDueDate(rsLatestPmt.getDate("NextDueDate"));
                return payment;
                //String resultString = rsLatestPmt.getString("amount");
                //float result = Float.valueOf(resultString);
                //returnValue = result;
            }
        } catch (SQLException e) {
            System.out.println("SQL getLastPayment operation has failed: " + e);
            //Return exception
            throw e;
        }
        return null;
        
    }

    //*******************************
    //Get monthly lease amount
    //******************************* 
    public static Double getMonthlyAmt(String whichUnit) throws SQLException, ClassNotFoundException {
        try {
            String sqlStmt = "CALL procMonthly('" + whichUnit + "')";
            ResultSet rsMonthly = DBUtil.dbExecuteQuery(sqlStmt);
            if (rsMonthly.next()) {
                return rsMonthly.getDouble("monthly_price");
            } else {
                return (Double)0.0;
            }
        } catch (SQLException e) {
            System.out.println("SQL getMonthlyAmt operation has failed: " + e);
            //Return exception
            throw e;
        }
    }

    //*******************************
    //Commit a payment to DB
    //******************************* 
    public static void commitPayment(Double amount, String unit) throws SQLException, ClassNotFoundException {
        try {
            String sqlStmt = "CALL procCommitPayment('" + amount + "', '" + unit +"')";
            ResultSet rsMonthly = DBUtil.dbExecuteQuery(sqlStmt);
            //if NextDueDate then 
            //    max(NextDueDate) + 1 month
            //else
            //    NextDueDate is Month+1, Day=1
            //if new lease, then there is a partial payment that needs to be calculated
            //maybe this is part of lesseeView and accomplished in LesseeController????
            //in stored proc code do get unit_id from unit where label =unit
        } catch (SQLException e) {
            System.out.println("commitPayment db operation failed: " + e);
        }
    }
}