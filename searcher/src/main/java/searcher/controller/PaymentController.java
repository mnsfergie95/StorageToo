package searcher.controller;

import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.scene.Scene;
import javafx.scene.layout.AnchorPane;
import javafx.scene.control.Label;
import javafx.scene.control.ComboBox;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableCell;
import javafx.scene.control.TableView;
import javafx.scene.control.ScrollPane;
import javafx.scene.paint.Color;
import javafx.scene.text.Text;
import javafx.scene.text.TextFlow;
import javafx.stage.Stage;
import searcher.model.Payment;
import searcher.model.PaymentDAO;
import searcher.util.printMe;

import java.io.IOException;

import java.sql.Timestamp;
import java.sql.ResultSet;
import java.sql.SQLException;
import java.text.NumberFormat;
import java.time.LocalDate;
import java.util.Locale;

public class PaymentController {

    @FXML
    private ComboBox<String> cmbUnit;
    @FXML
    private ScrollPane scrollResult;
    @FXML
    private TableView<Payment> paymentsTable;
    @FXML
    private TableColumn<Payment, Timestamp> paymentDateColumn;
    @FXML
    private TableColumn<Payment, Double> paymentAmountColumn;
    @FXML
    private TableColumn<Payment, String>  paymentUnitColumn;

    //total amount owed
    public static Double amtTotalOwed;
    //unit title
    public static String unitString;
    //increment due date by 1 month
    public static LocalDate newNextDueDate;
    
    //days late
    private Integer daysLate;
    //regular monthly amount
    private Double monthlyAmt;
    //late fee
    private Double amtLate;
    

    @FXML
    private void initialize () throws SQLException, ClassNotFoundException {
        //Setup tableview
        paymentDateColumn.setCellValueFactory(cellData -> cellData.getValue().dateProperty());
        paymentAmountColumn.setCellValueFactory(cellData -> cellData.getValue().amountProperty().asObject());
        paymentUnitColumn.setCellValueFactory(cellData -> cellData.getValue().unitLabelProperty());
        paymentAmountColumn.setStyle("-fx-alignment: BASELINE_CENTER;");
        paymentUnitColumn.setStyle("-fx-alignment: BASELINE_CENTER;");

        //Setup amount cellFactory which defines how to display it
        NumberFormat currencyFormat = NumberFormat.getCurrencyInstance();
        paymentAmountColumn.setCellFactory(tc -> new TableCell<Payment, Double>() {
            @Override
            protected void updateItem(Double amount, boolean empty) {
                super.updateItem(amount, empty);
                if (empty) {
                    setText(null);
                } else {
                    setText(currencyFormat.format(amount));
                }
            }
        });

        //populate combo box with unit titles
        try {
            ResultSet rsAvailUnits = PaymentDAO.getAllLeasedUnits();
            while (rsAvailUnits.next()) {
                cmbUnit.getItems().addAll(rsAvailUnits.getString("label"));
            }
        }  catch (SQLException e) {
            System.out.println("SQL select operation has failed: " + e);
            //Return exception
            throw e;
        }

        //initialize variables
        amtTotalOwed = 0.0;  //initialize to 0.0
        daysLate = 0;
        monthlyAmt = 0.0;
        amtLate = 0.0;  //initialize to 0.0
        newNextDueDate = null;
        unitString = "";
    }

    //get payment history
    @FXML
    private void getPaymentHistory(ActionEvent actionEvent) throws SQLException, ClassNotFoundException {
        String Input = cmbUnit.getValue();
        if (Input != null) {
            try {
                //Get all Payments info
                ObservableList<Payment> pmtData = PaymentDAO.searchPayments(Input);
                //Populate Payments on TableView
                populatePayments(pmtData);
            } catch (SQLException e) {
                System.out.println("Error occurred while getting payment history information from DB.\n" + e);
                throw e;
            }
        }
    }

    //Populate Payments on TableView
    @FXML
    private void populatePayments (ObservableList<Payment> pmtData) throws ClassNotFoundException {
        //Set items to the paymentsTable
        paymentsTable.setItems(pmtData);
    }

    //Calculate and display amount owed for a unit
    @FXML
    private void calculateAndDisplayAmtOwed (ActionEvent actionEvent) throws SQLException, ClassNotFoundException {
        try {
            getAmtOwed();
            showAmountOwed();
        } catch (SQLException e) {
            System.out.println("Error occurred while getting payment data from DB.\n" + e);
            throw e;
        }
    }

    //get amount owed
    private void getAmtOwed() throws SQLException, ClassNotFoundException {
        String whichUnitString = cmbUnit.getValue();
        if (whichUnitString != null) {
            try {
                Payment pmt = new Payment();
                pmt = PaymentDAO.getLastPayment(whichUnitString);
                if (pmt != null) {
                    monthlyAmt = PaymentDAO.getMonthlyAmt(whichUnitString);
                    LocalDate nextDueDate = pmt.getPmtDueDate().toLocalDate();
                    newNextDueDate = nextDueDate.plusMonths(1);
                    LocalDate now = LocalDate.now();
                    LocalDate fortyFiveDaysLate = nextDueDate.plusDays(45);
                    LocalDate thirtyDaysLate = nextDueDate.plusDays(30);
                    LocalDate fifteenDaysLate = nextDueDate.plusDays(15);
                    if (now.isAfter(fortyFiveDaysLate)) {
                        daysLate = 45;
                        amtTotalOwed = 999.0;
                    } else if (now.isAfter(thirtyDaysLate)) {
                        daysLate = 30;
                        amtLate = 30.00;
                        amtTotalOwed = monthlyAmt + amtLate;
                    } else if (now.isAfter(fifteenDaysLate)) {
                        daysLate = 15;
                        amtLate = 15.00;
                        amtTotalOwed = monthlyAmt + amtLate;
                    } else {
                        daysLate = 0;
                        amtTotalOwed = monthlyAmt;
                    }
                } else {
                    daysLate = 99;
                }
            } catch (SQLException e) {
                System.out.println("Error occurred while getting payment amount from DB.\n" + e);
                throw e;
            } catch (ClassNotFoundException e) {
                System.out.println("Error occurred while getting payment amount from DB.\n" + e);
                throw e;
            }
        }
    }

    //Display amount owed
    private void showAmountOwed() {
        TextFlow textFlow = new TextFlow();
        String amtDisplay;
        NumberFormat currencyFormatter = NumberFormat.getCurrencyInstance(Locale.getDefault());
        if (daysLate == 45) {
            Text txt1 = new Text("45 DAYS LATE - NEED TO EVICT!\n");
            txt1.setFill(Color.RED);
            textFlow.getChildren().add(txt1);
        }
        if (daysLate == 30) {
            amtDisplay = currencyFormatter.format(amtTotalOwed);
            Text text1 = new Text("Amt Owed is\n" + currencyFormatter.format(monthlyAmt) + " Regular + " + currencyFormatter.format(amtLate) + " Late\nFor a Total Due of "); 
            text1.setFill(Color.BLACK);
            Text text2 = new Text(amtDisplay);
            text2.setFill(Color.RED);
            textFlow.getChildren().addAll(text1, text2);
        }
        if (daysLate == 15) {
            amtDisplay = currencyFormatter.format(amtTotalOwed);
            Text text1 = new Text("Amt Owed is\n" + currencyFormatter.format(monthlyAmt) + " Regular + " + currencyFormatter.format(amtLate) + " Late\nFor a Total Due of "); 
            text1.setFill(Color.BLACK);
            Text text2 = new Text(amtDisplay);
            text2.setFill(Color.RED);
            textFlow.setPrefWidth(200);
            textFlow.getChildren().addAll(text1, text2);
        }
        if (daysLate == 0) {
            amtDisplay = currencyFormatter.format(monthlyAmt);
            Text text1 = new Text("Amt owed is ");
            text1.setFill(Color.BLACK);
            Text text2 = new Text(amtDisplay);
            text2.setFill(Color.RED);
            textFlow.getChildren().addAll(text1, text2);
        }
        if (daysLate == 99) {
            Text text1 = new Text("Get payment amount returned null");
            text1.setFill(Color.RED);
            textFlow.getChildren().add(text1);
        }
        scrollResult.setContent(textFlow);
    }

    //Show payment commit window
    @FXML
    private void pmtCommit(ActionEvent actionEvent) throws SQLException, IOException, ClassNotFoundException {
        String Input = cmbUnit.getValue();
        if (Input != null) {
            try {
                getAmtOwed();
            } catch (SQLException e) {
                System.out.println("Error occurred with getAmt in pmtCommit method" + e);
                throw e;
            }
            unitString = Input;
            Stage newWindow = new Stage();
            newWindow.setTitle("Receive Payment");
            FXMLLoader loader = new FXMLLoader(getClass().getResource("/searcher/view/recvPmtWindow.fxml"));
            newWindow.setScene(new Scene(loader.load()));
            newWindow.show();
        }
    }

    //Print a test page
    @FXML
    private void printNow() throws IOException {
        Label lblHelloWorld = new Label();
        lblHelloWorld.setText("Hello World!");
        AnchorPane pane = new AnchorPane();
        pane.setPrefSize(200, 200);
        pane.getChildren().add(lblHelloWorld);
        Scene scene = new Scene(pane);
        Stage stage = new Stage();
        stage.setScene(scene);
        stage.show(); 
        printMe.print(pane);
    }
}


