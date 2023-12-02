package searcher.util;

import javax.sql.rowset.CachedRowSet;
import javax.sql.rowset.RowSetProvider;

import java.sql.*;

public class DBUtil {
        //Declare JDBC Driver
        private static final String JDBC_DRIVER = "com.mysql.cj.jdbc.Driver";

        //Connection
        private static Connection conn = null;
    
        //Connection String
        private static final String connStr = "jdbc:mysql://localhost/storagetoo?"
                                + "user=stoadmin&password=jikl1234";
    
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
            //System.out.println("MySQL JDBC Driver Registered!");
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

        //DB Paramaterized Query
        public static void dbParameterizedQuery(String sqlStmt, int num) throws SQLException, ClassNotFoundException {
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
                //int rowsAffected = stmt.executeUpdate();
                //System.out.println("rowsAffected is " + rowsAffected);
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
