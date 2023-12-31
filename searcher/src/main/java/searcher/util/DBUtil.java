package searcher.util;

import javax.sql.rowset.CachedRowSet;
import javax.sql.rowset.RowSetProvider;

import java.sql.*;
import java.time.LocalDate;
import java.time.Instant;

public class DBUtil {
    //Declare JDBC Driver
    private static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";

    //Connection
    private static Connection conn = null;

    //Connection String
    private static final String connStr = "jdbc:mysql://localhost/storagetoo?user=StoAdmin&password=jikl1234";

    //Connect to DB
    public static void dbConnect() throws SQLException, ClassNotFoundException {
        //Setting Oracle JDBC Driver
        try {
            Class.forName(JDBC_DRIVER);
        } catch (ClassNotFoundException e) {
            System.out.println("Where is your MySQL JDBC Driver?");
            e.printStackTrace();
            throw e;
        }
        //Establish the Oracle Connection using Connection String
        try {
            conn = DriverManager.getConnection(connStr);
        } catch (SQLException e) {
            System.out.println("Connection Failed! Check output console" + e);
            e.printStackTrace();
            throw e;
        }
    }
    //Close Connection
    public static void dbDisconnect() throws SQLException {
        try {
            if (conn != null && !conn.isClosed()) {
                conn.close();
            }
        } catch (Exception e){
            throw e;
        }
    }

    //DB Execute Query Operation
    public static ResultSet dbExecuteQuery(String queryStmt) throws SQLException, ClassNotFoundException {
        //Declare statement, resultSet and CachedResultSet as null
        Statement stmt = null;
        ResultSet resultSet = null;
        CachedRowSet crs = RowSetProvider.newFactory().createCachedRowSet();
            
        try {
            //Connect to DB (Establish Mysql Connection)
            dbConnect();
            //System.out.println("Select statement: " + queryStmt + "\n");
            //Create statement
            stmt = conn.createStatement();
            //Execute select (query) operation
            resultSet = stmt.executeQuery(queryStmt);
            //CachedRowSet Implementation
            //In order to prevent "java.sql.SQLRecoverableException: Closed Connection: next" error
            //We are using CachedRowSet
            
            crs.populate(resultSet);
        } catch (SQLException e) {
            System.out.println("Problem occurred at executeQuery operation : " + e);
            throw e;
        } finally {
            if (resultSet != null) {
                //Close resultSet
                resultSet.close();
            }
            if (stmt != null) {
                //Close Statement
                stmt.close();
            }
            //Close connection
            dbDisconnect();
        }
        //Return CachedRowSet
        return crs;
    }

    //DB Execute Update (For Update/Insert/Delete) Operation
    public static void dbExecuteUpdate(String sqlStmt) throws SQLException, ClassNotFoundException {
        //Declare statement as null
        Statement stmt = null;
        try {
            //Connect to DB (Establish Mysql Connection)
            dbConnect();
            //Create Statement
            stmt = conn.createStatement();
            //Run executeUpdate operation with given sql statement
            stmt.executeUpdate(sqlStmt);
        } catch (SQLException e) {
            System.out.println("Problem occurred at executeUpdate operation : " + e);
            throw e;
        } finally {
            if (stmt != null) {
                //Close statement
                stmt.close();
            }
            //Close connection
            dbDisconnect();
        }
    }

    //Execute stored procedure
    public static Integer dbExecuteProcedureGetLesseeIdFromName(String sqlStmt, String param1) throws SQLException, ClassNotFoundException {
        //Declare statement as null
        CallableStatement stmt = null;
        try {
            //Connect to DB (Establish Mysql Connection)
            dbConnect();
            //Create Statement
            stmt = conn.prepareCall(sqlStmt);
            //Pass parameter
            stmt.setString(1, param1);
            stmt.registerOutParameter(2, java.sql.Types.INTEGER);
            //Run executeUpdate operation with given sql statement
            stmt.executeUpdate();
            return stmt.getInt(2);
        } catch (SQLException e) {
            System.out.println("Problem occurred at dbExecuteProcedureGetLesseeIdFromName operation : " + e);
            throw e;
        }

    }

    //Execute stored procedure procAddLessee
    public static void dbExecuteProcedureAddLessee(String sqlStmt, String label, String name, String addrL1, String addrL2, String city, String state,  Integer zip, String phone) throws SQLException, ClassNotFoundException {
        //Declare statement as null
        CallableStatement stmt = null;
        try {
            //Connect to DB (Establish Mysql Connection)
            dbConnect();
            //Create Statement
            stmt = conn.prepareCall(sqlStmt);
            //Pass parameters
            stmt.setString(1, name);
            stmt.setString(2, addrL1);
            stmt.setString(3, addrL2);
            stmt.setString(4, city);
            stmt.setString(5, state);
            stmt.setInt(6, zip);
            stmt.setString(7, phone);
            stmt.setString(8, label); 
            //Run executeUpdate operation with given sql statement
            stmt.executeUpdate();
            return;
        } catch (SQLException e) {
            System.out.println("Problem occurred at dbExecuteProcedureAddLessee operation : " + e);
            throw e;
        }

    }

    //Execute stored procedure procSearch
    public static ResultSet dbExecuteProcedureSearchLessee(String sqlStmt, String unitLabel, String name, String phone) throws SQLException, ClassNotFoundException {
        //Declare statement as null
        CallableStatement stmt = null;
        try {
            //Connect to DB (Establish Mysql Connection)
            dbConnect();
            //Create Statement
            stmt = conn.prepareCall(sqlStmt);
            //Pass parameters
            stmt.setString(1, name);
            stmt.setString(2, unitLabel);
            stmt.setString(3, phone);
            //Run executeUpdate operation with given sql statement
            stmt.executeUpdate();
            ResultSet rsReturn = stmt.getResultSet();
            return rsReturn;
        } catch (SQLException e) {
            System.out.println("Problem occurred at dbExecuteProcedureAddLessee operation : " + e);
            throw e;
        }
    }
     
    //DB deactivate Lessee Paramaterized Query
    public static void dbDeactivateLessee(String sqlStmt, int num) throws SQLException, ClassNotFoundException {
        System.out.println(sqlStmt + " ** " + num);
        //Declare statement as null
        CallableStatement stmt = null;
        try {
            //Connect to DB (Establish Mysql Connection)
            dbConnect();
            //Create Statement
            stmt = conn.prepareCall(sqlStmt);
            //Pass parameter
            stmt.setInt(1, num);
            //Run executeUpdate operation with given sql statement
            stmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println("Problem occurred at dbDeactivateLessee operation : " + e);
            throw e;
        } finally {
            if (stmt != null) {
                //Close statement
                stmt.close();
            }
            //Close connection
            dbDisconnect();
        }
    }
    
    //DB Payment Parameterized Query
    public static void dbCommitPmt(String unitTitle, Double amt, LocalDate nextDueDate) throws SQLException, ClassNotFoundException {
        //Declare statement as null
        CallableStatement stmt = null;
        try {
            //Prepare now for Timestamp in db
            Timestamp now = Timestamp.from(Instant.now());
            //Calculate next due date
            LocalDate nextDue = nextDueDate.plusMonths(1);
            //Convert nextDue to java.sql.Date
            java.sql.Date sqlNextDue = java.sql.Date.valueOf(nextDue);
            //Establish sql string
            String sqlStmt = "CALL procCommitPmt(?,?,?,?)";
            //Connect to DB (Establish Mysql Connection)
            dbConnect();
            //Create Statement
            stmt = conn.prepareCall(sqlStmt);
            //Pass parameters
            stmt.setString(1, unitTitle);
            stmt.setDouble(2, amt);
            stmt.setTimestamp(3, now);
            stmt.setDate(4, sqlNextDue);
            //Run executeUpdate operation with given sql statement
            stmt.executeUpdate();
        } catch (SQLException e) {
            System.out.println("Problem occurred at dbParameterizedQuery operation : " + e);
            throw e;
        } finally {
            if (stmt != null) {
                //Close statement
                stmt.close();
            }
            //Close connection
            dbDisconnect();
        }
    }  
}
