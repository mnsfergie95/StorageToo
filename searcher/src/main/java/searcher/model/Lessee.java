package searcher.model;

import javafx.beans.property.*;

public class Lessee {
    
        //Declare Lessee Table Columns
        private IntegerProperty lessee_id;
        private IntegerProperty unit_id;
        private StringProperty unitLabel;
        private StringProperty lesseename;
        private StringProperty addrl1;
        private StringProperty addrl2;
        private StringProperty city;
        private StringProperty state;
        private IntegerProperty zip;
        private StringProperty phone;
        private BooleanProperty active;
    
        //Constructor
        public Lessee() {
            this.lessee_id = new SimpleIntegerProperty();
            this.unit_id = new SimpleIntegerProperty();
            this.unitLabel = new SimpleStringProperty();
            this.lesseename = new SimpleStringProperty();
            this.addrl1 = new SimpleStringProperty();
            this.addrl2 = new SimpleStringProperty();
            this.city = new SimpleStringProperty();
            this.state = new SimpleStringProperty();
            this.zip = new SimpleIntegerProperty();
            this.phone = new SimpleStringProperty();
            this.active = new SimpleBooleanProperty();
        }
    
        //lesseeid
        public int getLesseeId() {
            return lessee_id.get();
        }
        
        public void setLesseeId(int lesseeId){
            this.lessee_id.set(lesseeId);
        }
        
        public IntegerProperty lesseeIdProperty(){
            return lessee_id;
        }
    
        //unitid
        public int getUnitId() {
            return unit_id.get();
        }
        
        public void setUnitId(int unitId){
            this.unit_id.set(unitId);
        }
        
        public IntegerProperty unitIdProperty(){
            return unit_id;
        }

        //unitLabel
        public String getUnitLabel() {
            return unitLabel.get();
        }
        
        public void setUnitLabel(String unitLabel){
            this.unitLabel.set(unitLabel);
        }
        
        public StringProperty unitLabelProperty(){
            return unitLabel;
        }
    
        //lesseename
        public String getLesseeName() {
            return lesseename.get();
        }
        
        public void setLesseeName(String lesseeName){
            this.lesseename.set(lesseeName);
        }
        
        public StringProperty lesseeNameProperty(){
            return lesseename;
        }
    
        //addrl1
        public String getaddrL1() {
            return addrl1.get();
        }
        
        public void setAddrL1(String AddrL1){
            this.addrl1.set(AddrL1);
        }
        
        public StringProperty addrL1Property(){
            return addrl1;
        }
    
        //addrl2
        public String getaddrL2() {
            return addrl2.get();
        }
        
        public void setAddrL2(String AddrL2){
            this.addrl2.set(AddrL2);
        }
        
        public StringProperty addrL2Property(){
            return addrl2;
        }
    
        //city
        public String getCity() {
            return city.get();
        }
        
        public void setCity(String City){
            this.city.set(City);
        }
        
        public StringProperty cityProperty(){
            return city;
        }
    
        //state
        public String getState() {
            return state.get();
        }
        
        public void setState(String State){
            this.state.set(State);
        }
        
        public StringProperty stateProperty(){
            return state;
        }
    
        //zip
        public int getZip() {
            return zip.get();
        }
        
        public void setZip(Integer Zip){
            this.zip.set(Zip);
        }
        
        public IntegerProperty zipProperty(){
            return zip;
        }
    
        //phone
        public String getPhone() {
            return phone.get();
        }
        
        public void setPhone(String Phone){
            this.phone.set(Phone);
        }
        
        public StringProperty phoneProperty(){
            return phone;
        }

        //active
        public Boolean getActive() {
            return active.get();
        }
        
        public void setActive(Boolean Active){
            this.active.set(Active);
        }
        
        public BooleanProperty activeProperty(){
            return active;
        }
    }

