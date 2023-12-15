package searcher.controller;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.event.ActionEvent;
import javafx.fxml.FXML;
import javafx.fxml.FXMLLoader;
import javafx.stage.Stage;
import javafx.scene.Scene;
import java.io.IOException;
import javafx.scene.control.TableColumn;
import javafx.scene.control.TableView;
import javafx.scene.control.TextArea;
import javafx.scene.control.TextField;
import javafx.scene.control.Dialog;
import javafx.scene.control.ButtonBar.ButtonData;
import javafx.scene.control.ButtonType;
import javafx.scene.control.ComboBox;

import java.time.Instant;
import java.time.LocalDate;
import java.time.YearMonth;
import java.time.ZoneId;
import java.util.Locale;

import searcher.model.Lessee;
import searcher.model.LesseeDAO;
import searcher.model.PaymentDAO;
import searcher.util.DBUtil;

import java.util.Date;
import java.sql.SQLException;
import java.text.NumberFormat;

public class LesseeController {
    
    
    @FXML
    private TextField nameText;
    @FXML
    private ComboBox<String> cmbUnit;
    @FXML
    private TextField addrL1Text;
    @FXML
    private TextField addrL2Text;
    @FXML
    private TextField cityText;
    @FXML
    private TextField stateText;
    @FXML
    private TextField zipText;
    @FXML
    private TextField phoneText;
    @FXML
    private TextArea resultArea;
    @FXML
    private TextField lesseeIdText;
    @FXML
    private TextField newPhoneText;
    @FXML
    private TableView<Lessee> lesseeTable;
    @FXML
    private TableColumn<Lessee, String>  lesseeUnitColumn;
    @FXML
    private TableColumn<Lessee, String>  lesseeNameColumn;
    @FXML
    private TableColumn<Lessee, String> lesseeAddrL1Column;
    @FXML
    private TableColumn<Lessee, String> lesseeAddrL2Column;
    @FXML
    private TableColumn<Lessee, String> lesseeCityColumn;
    @FXML
    private TableColumn<Lessee, String> lesseeStateColumn;
    @FXML
    private TableColumn<Lessee, Integer> lesseeZipColumn;
    @FXML
    private TableColumn<Lessee, String> lesseePhoneColumn;
    @FXML
    private TableColumn<Lessee, Boolean> lesseeActiveColumn;

    //Search a lessee
    @FXML
    private void searchLessee (ActionEvent actionEvent) throws ClassNotFoundException, SQLException {
        try {
            //Get Lessee information
            Integer lesseeID = Integer.parseInt(lesseeIdText.getText());
            Lessee lessee = LesseeDAO.searchLessee(lesseeID);
            if (lessee != null) {
                System.out.println(lessee.getUnitLabel());
            }
            //Populate Lessee on TableView and Display on TextArea
            populateAndShowLessee(lessee);
        } catch (SQLException e) {
            e.printStackTrace();
            resultArea.setText("Error occurred while getting lessee information from DB.\n" + e);
            throw e;
        }
    }
    
    //Search all lessees
    @FXML
    private void searchLessees(ActionEvent actionEvent) throws SQLException, ClassNotFoundException {
        try {
            //Get all Lessees information
            ObservableList<Lessee> lesseeData = LesseeDAO.searchLessees();
            //Populate Lessees on TableView
            populateLessees(lesseeData);
        } catch (SQLException e){
            System.out.println("Error occurred while getting lessees information from DB.\n" + e);
            throw e;
        }
    }
    
    //Initializing the controller class.
    //This method is automatically called after the fxml file has been loaded.
    @FXML
    private void initialize () throws SQLException, ClassNotFoundException {
        /*
        The setCellValueFactory(...) that we set on the table columns are used to determine
        which field inside the Lessee objects should be used for the particular column.
        The arrow -> indicates that we're using a Java 8 feature called Lambdas.
        (Another option would be to use a PropertyValueFactory, but this is not type-safe
        We're only using StringProperty values for our table columns in this example.
        When you want to use IntegerProperty or DoubleProperty, the setCellValueFactory(...)
        must have an additional asObject():
        */
        lesseeUnitColumn.setCellValueFactory(cellData -> cellData.getValue().unitLabelProperty());
        lesseeNameColumn.setCellValueFactory(cellData -> cellData.getValue().lesseeNameProperty());
        lesseeAddrL1Column.setCellValueFactory(cellData -> cellData.getValue().addrL1Property());
        lesseeAddrL2Column.setCellValueFactory(cellData -> cellData.getValue().addrL2Property());
        lesseeCityColumn.setCellValueFactory(cellData -> cellData.getValue().cityProperty());
        lesseeStateColumn.setCellValueFactory(cellData -> cellData.getValue().stateProperty());
        lesseeZipColumn.setCellValueFactory(cellData -> cellData.getValue().zipProperty().asObject());
        lesseePhoneColumn.setCellValueFactory(cellData -> cellData.getValue().phoneProperty());
        lesseeActiveColumn.setCellValueFactory(cellData -> cellData.getValue().activeProperty().asObject());

        //populate combo box with unit titles
        try {
            ResultSet rsAvailUnits = LesseeDAO.getAllAvailableUnits();
            while (rsAvailUnits.next()) {
                cmbUnit.getItems().addAll(rsAvailUnits.getString("label"));
            }
        }  catch (SQLException e) {
            System.out.println("SQL select operation to fill combo box lessee availables has failed: " + e);
            //Return exception
            throw e;
        }
    }

    //Show payment view
    @FXML
    private void pmtShowView () throws IOException {
        Stage newWindow = new Stage();
        newWindow.setTitle("Payments");
        FXMLLoader loader = new FXMLLoader(getClass().getResource("/searcher/view/pmtWindow.fxml"));
        newWindow.setScene(new Scene(loader.load()));
        newWindow.show();
    }

    //Populate Lessee
    @FXML
    private void populateLessee (Lessee lessee) throws ClassNotFoundException {
        //Declare and ObservableList for table view
        ObservableList<Lessee> lesseeData = FXCollections.observableArrayList();
        //Add lessee to the ObservableList
        lesseeData.add(lessee);
        //Set items to the lesseeTable
        lesseeTable.setItems(lesseeData);
    }

    //Set Lessee information to Text Area
    @FXML
    private void setLesseeInfoToTextArea ( Lessee lessee) {
        resultArea.setText("Name: " + lessee.getLesseeName() + "\n" +
                "Unit: " + lessee.getUnitId());
    }

    //Populate Lessee for TableView and Display Lessee on TextArea
    @FXML
    private void populateAndShowLessee(Lessee lessee) throws ClassNotFoundException {
        if (lessee != null) {
            populateLessee(lessee);
            setLesseeInfoToTextArea(lessee);
        } else {
            resultArea.setText("This lessee does not exist!\n");
        }
    }

    //Populate Lessees for TableView
    @FXML
    private void populateLessees (ObservableList<Lessee> lesseeData) throws ClassNotFoundException {
        //Set items to the lesseeTable
        lesseeTable.setItems(lesseeData);
    }

    //Update lessee's phone number with the phone number which is written on phoneText field
    @FXML
    private void updateLesseePhone (ActionEvent actionEvent) throws SQLException, ClassNotFoundException {
        try {
            LesseeDAO.updateLesseePhone(Integer.parseInt(lesseeIdText.getText()), phoneText.getText());
            resultArea.setText("Phone number has been updated for, lessee id: " + lesseeIdText.getText() + "\n");
        } catch (SQLException e) {
            resultArea.setText("Problem occrurred while updating phone number " + e);
            throw e;
        }
    }

    static int getLastDayOfMonth(YearMonth date) {
        return date.atEndOfMonth().getDayOfMonth();
    }

    //Add a lessee to DB
    @FXML
    private void insertLessee (ActionEvent actionEvent) throws ClassNotFoundException, SQLException {
        if ((nameText.getText() != null) && (phoneText.getText() != null)) {
            String unitLabel = unitText.getText().toLowerCase();
            //******************** 
            //** See if unit is available or make unit a combobox
            //********************
            //calculate partial payment
            Date date = new Date();
            YearMonth today = YearMonth.from(date.toInstant().atZone(ZoneId.systemDefault()).toLocalDate());
            LocalDate hoy = LocalDate.now();
            Integer LastDayOfMonth = getLastDayOfMonth(today);
            Integer DaysLeftInMonth = LastDayOfMonth - hoy.getDayOfMonth();
            //monthlyprice*DaysLeftInMonth/lastDayOfMonth
            Double monthlyPrice = PaymentDAO.getMonthlyAmt(unitLabel);
            Double partialPmt = Math.round((monthlyPrice * DaysLeftInMonth / LastDayOfMonth) * 100d) / 100d;
            LocalDate firstOfThisMonth = hoy.withDayOfMonth(1);
            //popup a dialog showing prorated amt to end of month
            Dialog<String> dialog = new Dialog<String>();
            dialog.setTitle("Initial Payment");
            ButtonType type = new ButtonType("Commit to DB", ButtonData.OK_DONE);
            dialog.setContentText("Prorated initial payment is " + partialPmt.toString());
            dialog.getDialogPane().getButtonTypes().add(type);
            dialog.showAndWait();
            try {
                //Insert Lessee info
                Boolean yes = true;
                Integer unitID = LesseeDAO.getUnitID(unitLabel);
                Integer zip = Integer.parseInt(zipText.getText());
                LesseeDAO.insertLessee(unitID, nameText.getText(), addrL1Text.getText(), addrL2Text.getText(), cityText.getText(), stateText.getText(), zip, phoneText.getText(), yes);
                //Add partial pmt to payment table in DB
                DBUtil.dbCommitPmt(unitLabel, partialPmt, firstOfThisMonth);
            } catch (SQLException e) {
                e.printStackTrace();
                resultArea.setText("Error occurred while adding lessee to DB.\n" + e);
            }
            //popup a dialog showing successful lessee addition to DB 
            Dialog<String> dialogg = new Dialog<String>();
            dialogg.setTitle("Success!");
            ButtonType typee = new ButtonType("Ok", ButtonData.OK_DONE);
            dialogg.setContentText("Payment successfully added to DB");
            dialogg.getDialogPane().getButtonTypes().add(typee);
            dialogg.showAndWait();
            // zero out textfields
            nameText.setText("");
            cmbUnit.setText("");
            addrL1Text.setText("");
            addrL2Text.setText("");
            cityText.setText("");
            zipText.setText("");
            phoneText.setText("");
        }
    }

    //Delete a lessee with a given lesseeID from DB
    @FXML
    private void deleteLessee(ActionEvent actionEvent) throws ClassNotFoundException, SQLException {
        try {
            //Delete lessee info
            LesseeDAO.deleteLesseeWithId(lesseeIdText.getText());
            resultArea.setText("Lessee deleted! Lessee id: " + lesseeIdText.getText() + "\n");
        } catch (SQLException e) {
            e.printStackTrace();
            resultArea.setText("Error occurred while deleting lessee from DB.\n" + e);
        }
    }

}
