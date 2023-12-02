package searcher.model;

import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import searcher.util.DBUtil;
import java.sql.ResultSet;
import java.sql.SQLException;

public class LesseeDAO {
    
    //*******************************
    //SELECT a Lessee
    //*******************************
    public static Lessee searchLessee (Integer lesseeId) throws SQLException, ClassNotFoundException {
        //Declare a SELECT statement
        String selectStmt = "SELECT * FROM lessee LEFT JOIN unit ON lessee.unit_id = unit.unitid WHERE lessee_id="+lesseeId;
        //Execute SELECT statement
        try {
            //Get ResultSet from dbExecuteQuery method
            ResultSet rsLessee = DBUtil.dbExecuteQuery(selectStmt);
            //Send ResultSet to the getLesseeFromResultSet method and get lessee object
            Lessee lessee = getLesseeFromResultSet(rsLessee);
            //Return lessee object
            return lessee;
        } catch (SQLException e) {
            System.out.println("While searching a lessee with " + lesseeId + " id, an error occurred: " + e);
            //Return exception
            throw e;
        }
    }

    //*******************************
    //Use ResultSet from DB as parameter and set Lessee Object's attributes and return lessee object.
    //*******************************
    private static Lessee getLesseeFromResultSet(ResultSet rs) throws SQLException {
        Lessee lessee = null;
        if (rs.next()) {
            lessee = new Lessee();
            lessee.setLesseeId(rs.getInt("lessee_id"));
            lessee.setUnitId(rs.getInt("unit_id"));
            lessee.setUnitLabel(rs.getString("label"));;
            lessee.setLesseeName(rs.getString("lesseename"));
            lessee.setAddrL1(rs.getString("addrl1"));
            lessee.setAddrL2(rs.getString("addrl2"));
            lessee.setCity(rs.getString("city"));
            lessee.setState(rs.getString("state"));
            lessee.setZip(rs.getInt("zip"));
            lessee.setPhone(rs.getString("phone"));
            lessee.setActive(rs.getBoolean("active"));
        }
        return lessee;
    }

    //*******************************
    //get unitID from label
    //*******************************
    public static Integer getUnitID(String unitLabel) throws SQLException, ClassNotFoundException {
        //Declare SELECT statement
        String selectStmt = "SELECT unit_id FROM unit WHERE label = '" + unitLabel.toLowerCase() + "'";
        //Execute SELECT statement
        try {
            //Get ResultSet from dbExecuteQuery method
            ResultSet rsUnit = DBUtil.dbExecuteQuery(selectStmt);
            //Get unitID from rsUnit
            Integer unitID = null;
            if (rsUnit.next()) {
                unitID = rsUnit.getInt("unit_id");
            }    
            //Return lessee object
            return unitID;
        } catch (SQLException e) {
            System.out.println("While getting unitID from unitLabel, an error occurred: " + e);
            //Return exception
            throw e;
        }
    }

    //*******************************
    //SELECT Lessees
    //*******************************
    public static ObservableList<Lessee> searchLessees () throws SQLException, ClassNotFoundException {
        //Declare a SELECT statement
        String selectStmt = "SELECT * FROM lessee LEFT JOIN unit ON lessee.unit_id = unit.unitid";
        //Execute SELECT statement
        try {
            //Get ResultSet from dbExecuteQuery method
            ResultSet rsLessees = DBUtil.dbExecuteQuery(selectStmt);
            //Send ResultSet to the getLesseeList method and get Lessee object
            ObservableList<Lessee> lesseeList = getLesseeList(rsLessees);
            //Return lessee object
            return lesseeList;
        } catch (SQLException e) {
            System.out.println("SQL select operation has failed: " + e);
            //Return exception
            throw e;
        }
    }

    //*******************************
    //Select * from lessee operation
    //*******************************

    private static ObservableList<Lessee> getLesseeList(ResultSet rs) throws SQLException, ClassNotFoundException {
        //Declare a observable List which comprises of Lessee objects
        ObservableList<Lessee> lesseeList = FXCollections.observableArrayList();
        while (rs.next()) {
            Lessee lessee = new Lessee();
            lessee.setLesseeId(rs.getInt("lessee_id"));
            lessee.setUnitId(rs.getInt("unit_id"));
            lessee.setUnitLabel(rs.getString("label"));
            lessee.setLesseeName(rs.getString("lesseename"));
            lessee.setAddrL1(rs.getString("addrl1"));
            lessee.setAddrL2(rs.getString("addrl2"));
            lessee.setCity(rs.getString("city"));
            lessee.setState(rs.getString("city"));
            lessee.setZip(rs.getInt("zip"));
            lessee.setPhone(rs.getString("phone"));
            lessee.setActive(rs.getBoolean("active"));
            //Add lessee to the ObservableList
            lesseeList.add(lessee);
        }
        //return lesseeList (ObservableList of Lessees)
        return lesseeList;
    }

    //*************************************
    //UPDATE a lessee's phone
    //*************************************
    public static void updateLesseePhone(Integer lesseeID, String phone) throws SQLException, ClassNotFoundException {
        //Declare an UPDATE statement
        String updateStmt = "UPDATE lessee SET phone = '" + phone + "' WHERE lessee_id = " + lesseeID;

        //Execute UPDATE operation
        try {
            DBUtil.dbExecuteUpdate(updateStmt);
        } catch (SQLException e) {
            System.out.print("Error occurred while UPDATE Operation: " + e);
            throw e;
        }
    }

    //*************************************
    //DELETE a lessee
    //*************************************
    public static void deleteLesseeWithId (String lesseeId) throws SQLException, ClassNotFoundException {
        //Declare a sql statement using stored procedure procDeactivateLessee
        String deactivateStmt = "CALL procDeactivateLessee(?)";
        //Convert string lesseeId to integer
        Integer lesseeID = Integer.valueOf(lesseeId);
        //System.out.println("sql is" + deactivateStmt);
        //Execute sql operation
        try {
            DBUtil.dbParameterizedQuery(deactivateStmt, lesseeID);
        } catch (SQLException e) {
            System.out.print("Error occurred while using stored procedure procDeactivateLessee: " + e);
            throw e;
        }
    }

    //*************************************
    //INSERT a lessee
    //*************************************
    public static void insertLessee (Integer unitID, String name, String addrL1, String addrL2, String city, String state, Integer zip, String phone, Boolean active) throws SQLException, ClassNotFoundException {
        //Declare an INSERT statement
        String updateStmt = "INSERT INTO lessee VALUES (0, "+unitID+", '"+name+"', '"+addrL1+"', '"+addrL2+"', '"+city+"', '"+state+"', "+zip+", '"+phone+"', "+active+")";
        //System.out.print("updateStmt is " + updateStmt);
        //Execute UPDATE operation
        try {
            DBUtil.dbExecuteUpdate(updateStmt);
        } catch (SQLException e) {
            System.out.print("Error occurred while UPDATE Operation: " + e);
            throw e;
        }
    }

    //*************************************
    //List units available
    //*************************************
    public static ResultSet getAvailableUnits () throws SQLException, ClassNotFoundException {
        //Declare a stored procedure call statement
        String selectStmt = "CALL procListAllLeasedUnits";
        //Execute SELECT statement
        try {
            //Get ResultSet from dbExecuteQuery method
            ResultSet rsAvailUnits = DBUtil.dbExecuteQuery(selectStmt);
            return rsAvailUnits;
        }  catch (SQLException e) {
            System.out.println("SQL select operation has failed: " + e);
            //Return exception
            throw e;
        }
    }
}
