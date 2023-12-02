package searcher.model;

import javafx.beans.property.*;
import java.sql.Date;

public class Payment {
     
    //Declare Payment Table Columns
    private IntegerProperty pmt_id;
    private DoubleProperty amount;
    private SimpleObjectProperty<Date> pmtDate;
    private SimpleObjectProperty<Date> pmtDueDate;
    private IntegerProperty unit_id;
    private StringProperty unitLabel;

    //Constructor
    public Payment() {
        this.pmt_id = new SimpleIntegerProperty();
        this.amount = new SimpleDoubleProperty();
        this.pmtDate = new SimpleObjectProperty<Date>();
        this.pmtDueDate = new SimpleObjectProperty<Date>();
        this.unit_id = new SimpleIntegerProperty();
        this.unitLabel = new SimpleStringProperty();
    }

    //pmt_id
    public int getPaymentId() {
        return pmt_id.get();
    }

    public void setPaymentId(int paymentId) {
        this.pmt_id.set(paymentId);
    }

    public IntegerProperty paymentIdProperty() {
        return pmt_id;
    }

    //amount
    public double getAmount() {
        return amount.get();
    }

    public void setAmount(double amt) {
        this.amount.set(amt);
    }

    public DoubleProperty amountProperty() {
        return amount;
    }

    //pmt_date
    public Date getPmtDate() {
        return pmtDate.get();
    }

    public void setPmtDate(Date pmt_date) {
        this.pmtDate.set(pmt_date);
    }

    public SimpleObjectProperty<Date> dateProperty() {
        return pmtDate;
    }

    //pmt_due_date
    public Date getPmtDueDate() {
        return pmtDueDate.get();
    }

    public void setPmtDueDate(Date pmt_due_date) {
        this.pmtDueDate.set(pmt_due_date);
    }

    public SimpleObjectProperty<Date> dateDueProperty() {
        return pmtDueDate;
    }

    //unit_id
    public int getUnitId() {
        return unit_id.get();
    }

    public void setUnitId(int unitId) {
        this.unit_id.set(unitId);
    }

    public IntegerProperty unitIdProperty() {
        return unit_id;
    }

    //unitLabel
    public String getUnitLabel() {
        return unitLabel.get();
    }

    public void setUnitLabel(String unitLabel) {
        this.unitLabel.set(unitLabel);
    }

    public StringProperty unitLabelProperty() {
        return unitLabel;
    }
}
